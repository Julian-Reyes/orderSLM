"""Menu catalogs: the only source of item ids and prices.

menu@0.3: modifiers are ingredients/add-ons, not add/remove kinds. Each item lists
the modifiers it includes (`ingredient_ids`: removable, adjustable to extra/light)
and those a customer may add (`addon_ids`). Pricing rules: docs/PRICING.md.

menu@0.4: pizza sizes carry `diameter_cm` and `slices` for the reply layer only. The extractor gets
`MenuCatalog.extractor_view()`, which drops them, so it can never turn "feeds 10 people" into a
quantity (ExtractionRequest rejects a menu that still has them).

menu@0.5: `accepted_kitchen_requests` lists the preparation requests this business can always do
("well done", "cut in squares", "warm"). Code matches a request with no catalog id against it first
(core/requests.py); a match is a free kitchen note whatever the model said.

menu@0.6: `sold_as: order` marks items sold by the order (garlic knots, fries), optionally with
`pieces_per_order`. The quantity question asks "how many orders of …", and the extractor sees the piece
count so "12 garlic knots" can be read as 2 orders (docs/ANNOTATION_GUIDE.md).
"""

from datetime import time
from enum import StrEnum

from pydantic import Field, model_validator

from orderslm.domain.money import Cents

from .common import ID_PATTERN, Strict


class Variant(Strict):
    """A size or style of an item (S/M/L, 12-inch). Price is a delta on the item's base price."""

    id: str = Field(pattern=ID_PATTERN)
    name: str
    aliases: list[str] = Field(default_factory=list, description="'large', '2 liter', 'lunch size'")
    price_delta_cents: int = 0  # may be negative (a small size)
    diameter_cm: int | None = Field(default=None, ge=1, description="reply layer only (pizza sizes)")
    slices: int | None = Field(default=None, ge=1, description="reply layer only (pizza sizes)")


REPLY_ONLY_VARIANT_FIELDS = ("diameter_cm", "slices")
"""Never shown to an extractor: see MenuCatalog.extractor_view()."""


class Modifier(Strict):
    """An ingredient or add-on. Removing is free; adding costs price_cents (see docs/PRICING.md)."""

    id: str = Field(pattern=ID_PATTERN)
    name: str
    aliases: list[str] = Field(default_factory=list)
    group: str = Field(default="general", pattern=ID_PATTERN, description="topping, sauce, crust, milk, ...")
    price_cents: Cents = 0


class KitchenRequest(Strict):
    """A preparation request the kitchen always accepts. Matched on whole words of the request text."""

    id: str = Field(pattern=ID_PATTERN)
    name: str = Field(description="as printed on the ticket, e.g. 'well done'")
    aliases: list[str] = Field(
        default_factory=list, description="other wordings: 'extra well', 'cooked through'"
    )
    categories: list[str] = Field(
        default_factory=list, description="item categories it applies to; empty = all"
    )


class ComboSlot(Strict):
    """One choice inside a combo, e.g. side: fries | onion rings. Choices are included in the combo price."""

    id: str = Field(pattern=ID_PATTERN)
    name: str
    choices: list[str] = Field(min_length=1, description="menu item ids")


class SoldAs(StrEnum):
    each = "each"
    order = "order"


class MenuItem(Strict):
    id: str = Field(pattern=ID_PATTERN)
    name: str
    category: str = Field(pattern=ID_PATTERN)
    aliases: list[str] = Field(default_factory=list, description="informal names customers use")
    base_price_cents: Cents
    variants: list[Variant] = Field(default_factory=list)
    default_variant_id: str | None = Field(
        default=None, description="used when no variant is stated; null + variants = customer must choose"
    )
    ingredient_ids: list[str] = Field(default_factory=list, description="included by default")
    addon_ids: list[str] = Field(default_factory=list, description="may be added for a price")
    splittable: bool = Field(default=False, description="half-and-half allowed (pizza)")
    combo_slots: list[ComboSlot] = Field(default_factory=list)
    available: bool = True
    sold_as: SoldAs = Field(default=SoldAs.each, description="'order': quantity counts orders, not pieces")
    pieces_per_order: int | None = Field(default=None, ge=2, description="only with sold_as 'order'")

    @model_validator(mode="after")
    def _variants(self) -> "MenuItem":
        if self.pieces_per_order is not None and self.sold_as is not SoldAs.order:
            raise ValueError(f"{self.id}: pieces_per_order needs sold_as 'order'")
        ids = [v.id for v in self.variants]
        if len(ids) != len(set(ids)):
            raise ValueError(f"{self.id}: duplicate variant ids")
        if self.default_variant_id is not None and self.default_variant_id not in ids:
            raise ValueError(f"{self.id}: default_variant_id {self.default_variant_id!r} is not a variant")
        both = set(self.ingredient_ids) & set(self.addon_ids)
        if both:
            raise ValueError(f"{self.id}: {sorted(both)} listed as both ingredient and add-on")
        return self

    @property
    def allowed_modifier_ids(self) -> set[str]:
        return set(self.ingredient_ids) | set(self.addon_ids)

    def variant(self, variant_id: str) -> Variant | None:
        return next((v for v in self.variants if v.id == variant_id), None)


class DeliveryPolicy(Strict):
    available: bool = True
    fee_cents: Cents = 0
    min_order_cents: Cents = 0


class MenuCatalog(Strict):
    business_id: str = Field(pattern=ID_PATTERN)
    name: str
    currency: str = Field(default="USD", pattern=r"^[A-Z]{3}$")
    timezone: str = "America/New_York"
    opens_at: time
    closes_at: time
    delivery: DeliveryPolicy
    accepts_payment: list[str] = Field(default_factory=lambda: ["card", "cash"])
    held_out: bool = Field(default=False, description="true only for the test-only generalization menu")
    name_required_for_pickup: bool = Field(
        default=False,
        description="pickup orders without a customer name get a customer_name/missing clarification",
    )
    exclusive_groups: list[str] = Field(
        default_factory=list, description="modifier groups where an item takes at most one (crust, milk)"
    )
    modifiers: list[Modifier] = Field(default_factory=list)
    items: list[MenuItem] = Field(min_length=1)
    accepted_kitchen_requests: list[KitchenRequest] = Field(
        default_factory=list, description="requests with no catalog id that are free kitchen notes (menu@0.5)"
    )

    @model_validator(mode="after")
    def _references(self) -> "MenuCatalog":
        item_ids = [i.id for i in self.items]
        mod_ids = [m.id for m in self.modifiers]
        for name, ids in (("item", item_ids), ("modifier", mod_ids)):
            dupes = {x for x in ids if ids.count(x) > 1}
            if dupes:
                raise ValueError(f"duplicate {name} ids: {sorted(dupes)}")
        for item in self.items:
            unknown = item.allowed_modifier_ids - set(mod_ids)
            if unknown:
                raise ValueError(f"{item.id}: unknown modifier ids {sorted(unknown)}")
            for slot in item.combo_slots:
                missing = set(slot.choices) - set(item_ids)
                if missing:
                    raise ValueError(f"{item.id}.{slot.id}: unknown choice ids {sorted(missing)}")
        categories = {i.category for i in self.items}
        for kr in self.accepted_kitchen_requests:
            if unknown_cats := set(kr.categories) - categories:
                raise ValueError(f"kitchen request {kr.id}: unknown categories {sorted(unknown_cats)}")
        groups = {m.group for m in self.modifiers}
        if unknown_groups := set(self.exclusive_groups) - groups:
            raise ValueError(f"exclusive_groups not used by any modifier: {sorted(unknown_groups)}")
        return self

    def item(self, item_id: str) -> MenuItem | None:
        return next((i for i in self.items if i.id == item_id), None)

    def has_reply_only_fields(self) -> bool:
        return any(
            getattr(v, f) is not None
            for i in self.items
            for v in i.variants
            for f in REPLY_ONLY_VARIANT_FIELDS
        )

    def extractor_view(self) -> "MenuCatalog":
        """The menu as an extractor sees it: identical except the reply-only size facts are removed."""
        clear = dict.fromkeys(REPLY_ONLY_VARIANT_FIELDS)
        items = [
            i.model_copy(update={"variants": [v.model_copy(update=clear) for v in i.variants]})
            for i in self.items
        ]
        return self.model_copy(update={"items": items})

    def modifier(self, modifier_id: str) -> Modifier | None:
        return next((m for m in self.modifiers if m.id == modifier_id), None)
