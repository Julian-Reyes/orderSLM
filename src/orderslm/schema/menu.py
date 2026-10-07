"""Menu catalogs: the only source of item ids and prices.

M0 defines the contract; M1 creates the three business menus and the held-out menu.
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
    price_delta_cents: int = 0  # may be negative (a small size)


class ModifierKind(StrEnum):
    add = "add"  # extra bacon (+ price)
    remove = "remove"  # no onions (free)


class Modifier(Strict):
    id: str = Field(pattern=ID_PATTERN)
    name: str
    kind: ModifierKind
    price_cents: Cents = 0


class ComboSlot(Strict):
    """One choice inside a combo, e.g. side: fries | onion rings."""

    id: str = Field(pattern=ID_PATTERN)
    name: str
    choices: list[str] = Field(min_length=1, description="menu item ids")


class MenuItem(Strict):
    id: str = Field(pattern=ID_PATTERN)
    name: str
    category: str = Field(pattern=ID_PATTERN)
    aliases: list[str] = Field(default_factory=list, description="informal names customers use")
    base_price_cents: Cents
    variants: list[Variant] = Field(default_factory=list)
    default_variant_id: str | None = None
    modifier_ids: list[str] = Field(default_factory=list, description="modifiers allowed on this item")
    splittable: bool = Field(default=False, description="half-and-half allowed (pizza)")
    combo_slots: list[ComboSlot] = Field(default_factory=list)
    available: bool = True

    @model_validator(mode="after")
    def _variants(self) -> "MenuItem":
        ids = [v.id for v in self.variants]
        if len(ids) != len(set(ids)):
            raise ValueError(f"{self.id}: duplicate variant ids")
        if self.default_variant_id is not None and self.default_variant_id not in ids:
            raise ValueError(f"{self.id}: default_variant_id {self.default_variant_id!r} is not a variant")
        return self


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
    modifiers: list[Modifier] = Field(default_factory=list)
    items: list[MenuItem] = Field(min_length=1)

    @model_validator(mode="after")
    def _references(self) -> "MenuCatalog":
        item_ids = [i.id for i in self.items]
        mod_ids = [m.id for m in self.modifiers]
        for name, ids in (("item", item_ids), ("modifier", mod_ids)):
            dupes = {x for x in ids if ids.count(x) > 1}
            if dupes:
                raise ValueError(f"duplicate {name} ids: {sorted(dupes)}")
        for item in self.items:
            unknown = set(item.modifier_ids) - set(mod_ids)
            if unknown:
                raise ValueError(f"{item.id}: unknown modifier ids {sorted(unknown)}")
            for slot in item.combo_slots:
                missing = set(slot.choices) - set(item_ids)
                if missing:
                    raise ValueError(f"{item.id}.{slot.id}: unknown choice ids {sorted(missing)}")
        return self

    def item(self, item_id: str) -> MenuItem | None:
        return next((i for i in self.items if i.id == item_id), None)

    def modifier(self, modifier_id: str) -> Modifier | None:
        return next((m for m in self.modifiers if m.id == modifier_id), None)
