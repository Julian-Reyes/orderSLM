"""PIZZA benchmark: download, sample, build the benchmark catalog, convert orders (docs/PIZZA.md).

The PIZZA dataset (amazon-science/pizza-semantic-parsing-dataset) is CC-BY-NC-4.0: no
redistribution. Everything this module writes goes to the gitignored `data/external/pizza/`,
including the benchmark catalog and every report. Only this script is committed.

    uv run python -m orderslm.data.pizza --download --convert

Steps (M1 review, item 4):
1. Sample N orders from the dataset's test split with a fixed seed. Orders are never filtered
   to fit a menu; an order that can't be converted is reported, not dropped silently.
2. Build the PIZZA benchmark catalog from only the entities the sample mentions, plus unused
   catalog entities as distractors up to a realistic menu size.
3. Convert each order to a one-message conversation with a gold `ExtractionOutput`. The gold
   items come from the dataset's EXR parse; evidence spans come from its TOP parse, which must
   resolve to the same suborders. Order-level fields are never stated in PIZZA, so they are
   not_mentioned and the missing-info rules (core/missing.py) fill `missing_or_ambiguous`.
   PIZZA results are scored on items only.

The benchmark is evaluation-only: `load_cases()` needs ORDERSLM_UNSEAL_TEST, like the test split.
"""

import argparse
import hashlib
import json
import os
import random
import re
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, time
from pathlib import Path
from zoneinfo import ZoneInfo

from pydantic import Field

from orderslm.checks import check_all
from orderslm.core.missing import required_missing
from orderslm.core.replies import template_question
from orderslm.paths import EXTERNAL, UNSEAL_ENV, SealedSplitError
from orderslm.schema.common import ID_PATTERN, Evidence, Strict
from orderslm.schema.conversation import Conversation, Message, Role, Source, Split
from orderslm.schema.extraction import Amount, ExtractionOutput, ItemProposal, Modification, ModificationKind
from orderslm.schema.menu import DeliveryPolicy, MenuCatalog, MenuItem, Modifier, Variant

from .sexp import Node, parse

REPO = "amazon-science/pizza-semantic-parsing-dataset"
COMMIT = "814d6d0f0e26e9ba5c45be281fd432dc4d069b05"  # main as of 2026-10-07 (last change 2022-12-07)
CATALOG_FILES = {
    "TOPPING": "topping",
    "NUMBER": "number",
    "SIZE": "size",
    "STYLE": "style",
    "QUANTITY": "quant_qualifier",
    "DRINKTYPE": "drinks",
    "VOLUME": "drink_volume",
    "CONTAINERTYPE": "container",
}
FILES = ["data/PIZZA_test.json", "LICENSE", "README.md"] + [
    f"utils/catalogs/{name}.txt" for name in CATALOG_FILES.values()
]

PIZZA_DIR = EXTERNAL / "pizza"
OUT_DIR = PIZZA_DIR / "benchmark"
BUSINESS_ID = "pizza-benchmark"
SEED = 20261007
N_ORDERS = 200

# Styles that are a crust or dough (an exclusive "crust" modifier); every other style is a recipe
# pizza (a menu item). This is how the conversion reads the dataset's STYLE label.
CRUST_STYLES = {
    "CAULIFLOWER_CRUST",
    "CHICAGO_STYLE",
    "DEEP_DISH",
    "GLUTEN_FREE_CRUST",
    "KETO_CRUST",
    "NEAPOLITAN",
    "NEW_YORK_STYLE",
    "SOURDOUGH_CRUST",
    "STUFFED_CRUST",
    "THICK_CRUST",
    "THIN_CRUST",
}
# Realistic menu size: pad with unused catalog entities up to these counts (never trim).
TARGETS = {"toppings": 35, "recipes": 6, "crusts": 4, "pizza_sizes": 4, "drinks": 8}
DRINK_DEFAULT = "regular"  # a drink ordered with no size, volume or container
SENT_AT = datetime(2026, 1, 1, 12, 0)


# ---------------------------------------------------------------- download


def download(dest: Path = PIZZA_DIR) -> dict[str, str]:
    """Fetch the pinned files into data/external/pizza/ and record their sha256 in MANIFEST.json."""
    hashes: dict[str, str] = {}
    for rel in FILES:
        url = f"https://raw.githubusercontent.com/{REPO}/{COMMIT}/{rel}"
        target = dest / rel.removeprefix("data/").removeprefix("utils/")
        target.parent.mkdir(parents=True, exist_ok=True)
        with urllib.request.urlopen(url, timeout=60) as resp:  # noqa: S310 (fixed https URL)
            body = resp.read()
        target.write_bytes(body)
        hashes[rel] = hashlib.sha256(body).hexdigest()
    manifest = {"repo": REPO, "commit": COMMIT, "license": "CC-BY-NC-4.0", "sha256": hashes}
    (dest / "MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return hashes


# ---------------------------------------------------------------- reading parses


def _canon(raw: str) -> str:
    """Catalog value `volume(12, FLOZ)` or EXR leaf `12 FLOZ` -> `12 FLOZ`."""
    inner = raw[raw.index("(") + 1 : raw.rindex(")")] if "(" in raw else raw
    return " ".join(inner.replace(",", " ").split())


def load_catalogs(root: Path = PIZZA_DIR) -> dict[str, dict[str, str]]:
    """label -> {surface text: canonical value}, e.g. TOPPING -> {"black olives": "OLIVES"}."""
    out: dict[str, dict[str, str]] = {}
    for label, name in CATALOG_FILES.items():
        table: dict[str, str] = {}
        for line in (root / "catalogs" / f"{name}.txt").read_text().splitlines():
            if "\t" in line:
                surface, value = line.split("\t", 1)
                table[" ".join(surface.lower().split())] = _canon(value)
        out[label] = table
    return out


class Unresolved(ValueError):
    pass


@dataclass(frozen=True)
class Attr:
    """One attribute of a suborder. In a TOP parse, `value`/`amount` are None when the customer's
    wording isn't in the dataset's catalog ("bell peppers"); alignment fills them from EXR."""

    label: str  # NUMBER SIZE STYLE TOPPING DRINKTYPE VOLUME CONTAINERTYPE
    value: str | None
    negated: bool = False
    amount: str | None = "normal"  # TOPPING only: normal | extra | light
    text: str = ""

    def fits(self, exr: "Attr") -> bool:
        return (
            self.label == exr.label
            and self.negated == exr.negated
            and self.value in (None, exr.value)
            and self.amount in (None, exr.amount)
        )


@dataclass(frozen=True)
class Topping:
    code: str
    amount: str = "normal"  # normal | extra | light
    negated: bool = False
    text: str = ""


@dataclass(frozen=True)
class Style:
    code: str
    negated: bool = False
    text: str = ""


@dataclass
class SubOrder:
    kind: str  # pizza | drink
    number: int = 1
    size: str | None = None
    styles: list[Style] = field(default_factory=list)
    toppings: list[Topping] = field(default_factory=list)
    drink: str | None = None
    volume: str | None = None
    container: str | None = None
    span: str = ""

    @classmethod
    def from_attrs(cls, kind: str, span: str, attrs: list[Attr]) -> "SubOrder":
        sub = cls(kind=kind, span=span)
        for a in attrs:
            match a.label:
                case "NUMBER":
                    sub.number = int(a.value)
                case "SIZE":
                    sub.size = a.value
                case "STYLE":
                    sub.styles.append(Style(a.value, a.negated, a.text))
                case "TOPPING":
                    sub.toppings.append(Topping(a.value, a.amount, a.negated, a.text))
                case "DRINKTYPE":
                    sub.drink = a.value
                case "VOLUME":
                    sub.volume = a.value
                case "CONTAINERTYPE":
                    sub.container = a.value
        return sub


Parsed = list[tuple[str, str, list[Attr]]]  # (kind, span text, attributes) per suborder


def _add(attrs: list[Attr], n: Node, negated: bool, resolve) -> None:
    if n.label == "COMPLEX_TOPPING":
        (q,), (t,) = n.nodes("QUANTITY"), n.nodes("TOPPING")
        amount = resolve("QUANTITY", q)
        attrs.append(Attr("TOPPING", resolve("TOPPING", t), negated, amount and amount.lower(), n.text()))
    elif n.label == "NOT":
        if negated:
            raise Unresolved("nested NOT")
        for inner in n.nodes():
            _add(attrs, inner, True, resolve)
    elif n.label in CATALOG_FILES and n.label != "QUANTITY":
        attrs.append(Attr(n.label, resolve(n.label, n), negated, text=n.text()))
    else:
        raise Unresolved(f"unexpected attribute {n.label}")


def _attrs(tree: Node, resolve) -> Parsed:
    if tree.label != "ORDER":
        raise Unresolved(f"root is {tree.label}, not ORDER")
    out: Parsed = []
    for node in tree.nodes():
        if node.label not in ("PIZZAORDER", "DRINKORDER"):
            raise Unresolved(f"unexpected suborder {node.label}")
        attrs: list[Attr] = []
        for attr in node.nodes():
            _add(attrs, attr, False, resolve)
        out.append(("pizza" if node.label == "PIZZAORDER" else "drink", node.text(), attrs))
    return out


def _align(top: Parsed, exr: Parsed) -> list[list[list[Attr]]]:
    """Every way to pair TOP suborders/attributes with EXR ones; returns the filled-in TOP attributes
    per solution, de-duplicated. One solution = the parses agree; more = ambiguous; none = disagree."""
    solutions: dict[tuple, list[list[Attr]]] = {}

    def attrs_match(t: list[Attr], e: list[Attr]) -> list[list[Attr]]:
        if len(t) != len(e):
            return []
        found: list[list[Attr]] = []

        def go(i: int, left: list[Attr], acc: list[Attr]) -> None:
            if i == len(t):
                found.append(list(acc))
                return
            for j, cand in enumerate(left):
                if t[i].fits(cand):
                    filled = Attr(cand.label, cand.value, cand.negated, cand.amount, t[i].text)
                    go(i + 1, left[:j] + left[j + 1 :], [*acc, filled])

        go(0, list(e), [])
        return found

    def subs(i: int, left: Parsed, acc: list[list[Attr]]) -> None:
        if len(solutions) > 1:
            return
        if i == len(top):
            key = tuple(tuple((a.label, a.value, a.negated, a.amount, a.text) for a in s) for s in acc)
            solutions.setdefault(key, [list(s) for s in acc])
            return
        kind, _, t_attrs = top[i]
        for j, (e_kind, _, e_attrs) in enumerate(left):
            if e_kind == kind:
                for filled in attrs_match(t_attrs, e_attrs):
                    subs(i + 1, left[:j] + left[j + 1 :], [*acc, filled])

    if len(top) == len(exr):
        subs(0, list(exr), [])
    return list(solutions.values())


def read_order(row: dict, catalogs: dict[str, dict[str, str]]) -> tuple[list[SubOrder], int]:
    """Suborders with values from EXR and spans from TOP. Returns (suborders, how many TOP words were
    not in the catalog and took their value from EXR). Raises Unresolved if the parses can't be paired
    in exactly one way."""
    split = next(k.split(".")[0] for k in row if k.endswith(".SRC"))
    exr = _attrs(parse(row[f"{split}.EXR"]), lambda label, n: _canon(n.text()))
    unknown = 0

    def from_catalog(label: str, n: Node) -> str | None:
        nonlocal unknown
        value = catalogs[label].get(" ".join(n.text().lower().split()))
        unknown += value is None
        return value

    top = _attrs(parse(row[f"{split}.TOP"]), from_catalog)
    for _, _, attrs in top:
        if not any(a.label == "NUMBER" for a in attrs):
            attrs.append(Attr("NUMBER", "1"))  # EXR states an implicit 1 ("large pie with onions")
    solutions = _align(top, exr)
    if not solutions:
        raise Unresolved("TOP and EXR parses disagree")
    if len(solutions) > 1:
        raise Unresolved("TOP words not in the catalog can be paired with EXR values in more than one way")
    return [
        SubOrder.from_attrs(kind, span, attrs)
        for (kind, span, _), attrs in zip(top, solutions[0], strict=True)
    ], unknown


# ---------------------------------------------------------------- sampling and the catalog


def load_rows(root: Path = PIZZA_DIR) -> list[dict]:
    return [json.loads(line) for line in (root / "PIZZA_test.json").read_text().splitlines() if line.strip()]


def sample_indices(n_rows: int, n: int = N_ORDERS, seed: int = SEED) -> list[int]:
    """Fixed-seed sample of row indices, chosen before looking at any order's contents."""
    return sorted(random.Random(seed).sample(range(n_rows), min(n, n_rows)))


def _slug(value: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    if not re.fullmatch(ID_PATTERN, s):
        raise ValueError(f"can't make an id from {value!r}")
    return s


def _name(code: str) -> str:
    return code.replace("_", " ").replace("REGULARSIZE", "REGULAR SIZE").capitalize()


def drink_variant(sub: SubOrder) -> str:
    """One variant per distinct size/volume/container combination: lossless, reviewed in M2."""
    parts = [p for p in (sub.size, sub.volume, sub.container) if p]
    return _slug(" ".join(parts)) if parts else DRINK_DEFAULT


@dataclass
class Used:
    toppings: Counter = field(default_factory=Counter)
    recipes: Counter = field(default_factory=Counter)
    crusts: Counter = field(default_factory=Counter)
    pizza_sizes: Counter = field(default_factory=Counter)
    drinks: Counter = field(default_factory=Counter)
    drink_variants: Counter = field(default_factory=Counter)
    quantities: Counter = field(default_factory=Counter)

    def add(self, sub: SubOrder) -> None:
        if sub.kind == "drink":
            self.drinks[sub.drink] += 1
            self.drink_variants[drink_variant(sub)] += 1
            return
        if sub.size:
            self.pizza_sizes[sub.size] += 1
        for s in sub.styles:
            (self.crusts if s.code in CRUST_STYLES else self.recipes)[s.code] += 1
        for t in sub.toppings:
            self.toppings[t.code] += 1
            if t.amount != "normal":
                self.quantities[t.amount] += 1


def _pad(used: set[str], pool: set[str], target: int, rng: random.Random) -> list[str]:
    extra = sorted(pool - used)
    rng.shuffle(extra)
    return sorted(used) + sorted(extra[: max(0, target - len(used))])


def build_catalog(
    used: Used, catalogs: dict[str, dict[str, str]], seed: int = SEED
) -> tuple[MenuCatalog, dict]:
    """The benchmark menu: every entity the sample uses, plus distractors (reported separately)."""
    rng = random.Random(seed + 1)
    styles = set(catalogs["STYLE"].values())
    pools = {
        "toppings": set(catalogs["TOPPING"].values()),
        "recipes": styles - CRUST_STYLES,
        "crusts": styles & CRUST_STYLES,
        "pizza_sizes": set(catalogs["SIZE"].values()),
        "drinks": set(catalogs["DRINKTYPE"].values()),
    }
    chosen = {k: _pad(set(getattr(used, k)), pool, TARGETS[k], rng) for k, pool in pools.items()}

    modifiers = [
        Modifier(id=_slug(t), name=_name(t), group="topping", price_cents=150) for t in chosen["toppings"]
    ]
    modifiers += [
        Modifier(id=_slug(c), name=_name(c), group="crust", price_cents=0) for c in chosen["crusts"]
    ]
    addon_ids = [m.id for m in modifiers]
    sizes = [Variant(id=_slug(s), name=_name(s)) for s in chosen["pizza_sizes"]]

    def pizza(item_id: str, name: str) -> MenuItem:
        return MenuItem(
            id=item_id,
            name=name,
            category="pizzas",
            base_price_cents=1199,
            variants=sizes,
            addon_ids=addon_ids,
            splittable=True,
        )

    items = [pizza("pizza", "Pizza")]
    items += [pizza(f"{_slug(r)}_pizza", f"{_name(r)} pizza") for r in chosen["recipes"]]
    drink_variants = sorted(set(used.drink_variants) | {DRINK_DEFAULT})
    for d in chosen["drinks"]:
        items.append(
            MenuItem(
                id=_slug(d),
                name=_name(d),
                category="drinks",
                base_price_cents=199,
                variants=[Variant(id=v, name=v.replace("_", " ")) for v in drink_variants],
                default_variant_id=DRINK_DEFAULT,
            )
        )
    menu = MenuCatalog(
        business_id=BUSINESS_ID,
        name="PIZZA benchmark catalog",
        timezone="America/New_York",
        opens_at=time(11, 0),
        closes_at=time(23, 0),
        delivery=DeliveryPolicy(available=True, fee_cents=299),
        exclusive_groups=["crust"],
        modifiers=modifiers,
        items=items,
    )
    counts = {
        k: {
            "used": len(getattr(used, k)),
            "distractors": len(chosen[k]) - len(getattr(used, k)),
            "menu": len(chosen[k]),
        }
        for k in chosen
    }
    counts["drink_variants"] = {"used": len(used.drink_variants), "menu": len(drink_variants)}
    counts["quantities"] = {"used": len(used.quantities)}
    return menu, counts


# ---------------------------------------------------------------- conversion


class PizzaCase(Strict):
    """One converted PIZZA order. Evaluation-only; scored on `gold_extraction.items`."""

    id: str = Field(pattern=ID_PATTERN)
    source_index: int = Field(ge=0, description="line number in PIZZA_test.json")
    conversation: Conversation
    gold_extraction: ExtractionOutput
    dropped_negated_amounts: int = Field(
        default=0, description="'no extra cheese' kept the default amount: no modification (docs/PIZZA.md)"
    )


def _quote(text: str, source: str) -> str:
    if text not in source:
        raise Unresolved(f"span {text!r} is not in the message")
    return text


def convert(index: int, row: dict, subs: list[SubOrder], menu: MenuCatalog) -> PizzaCase:
    src = " ".join(row[next(k for k in row if k.endswith(".SRC"))].split())
    tz = ZoneInfo(menu.timezone)
    conversation = Conversation(
        id=f"pizza-test-{index:04d}",
        business_id=menu.business_id,
        split=Split.benchmark,
        source=Source.human,
        messages=[Message(index=0, role=Role.customer, text=src, sent_at=SENT_AT.replace(tzinfo=tz))],
    )
    items: list[ItemProposal] = []
    dropped = 0
    for n, sub in enumerate(subs, start=1):
        ev = [Evidence(message_index=0, quote=_quote(sub.span, src))]
        line = f"L{n}"
        if sub.kind == "drink":
            items.append(
                ItemProposal(
                    line_id=line,
                    menu_item_id=_slug(sub.drink),
                    quantity=sub.number,
                    variant_id=drink_variant(sub),
                    evidence=ev,
                )
            )
            continue
        recipes = [s for s in sub.styles if s.code not in CRUST_STYLES]
        if any(s.negated for s in recipes):
            raise Unresolved("a negated recipe style ('not hawaiian') has no menu meaning")
        if len(recipes) > 1:
            raise Unresolved("two recipe styles on one pizza")
        mods: list[Modification] = []
        for s in sub.styles:
            if s.code in CRUST_STYLES:
                kind = ModificationKind.remove if s.negated else ModificationKind.add
                mods.append(Modification(kind=kind, modifier_id=_slug(s.code), raw_text=s.text))
        for t in sub.toppings:
            if t.negated and t.amount != "normal":
                dropped += 1  # "no extra cheese": the default amount, so no modification
                continue
            kind = ModificationKind.remove if t.negated else ModificationKind.add
            mods.append(
                Modification(kind=kind, modifier_id=_slug(t.code), amount=Amount(t.amount), raw_text=t.text)
            )
        items.append(
            ItemProposal(
                line_id=line,
                menu_item_id=f"{_slug(recipes[0].code)}_pizza" if recipes else "pizza",
                quantity=sub.number,
                variant_id=_slug(sub.size) if sub.size else None,
                modifications=mods,
                evidence=ev,
            )
        )
    gold = ExtractionOutput.empty().model_copy(update={"items": items})
    missing = required_missing(gold, menu)
    gold = ExtractionOutput.model_validate(
        gold.model_dump()
        | {
            "missing_or_ambiguous": [m.model_dump() for m in missing],
            "clarification_question": template_question(missing, gold, menu) if missing else None,
        }
    )
    if issues := check_all(gold, conversation, menu):
        raise Unresolved(f"gold fails checks: {[i.code for i in issues]}")
    return PizzaCase(
        id=conversation.id,
        source_index=index,
        conversation=conversation,
        gold_extraction=gold,
        dropped_negated_amounts=dropped,
    )


def build(root: Path = PIZZA_DIR, n: int = N_ORDERS, seed: int = SEED) -> dict:
    """Sample, build the catalog, convert. Writes everything under data/external/pizza/benchmark/."""
    catalogs = load_catalogs(root)
    rows = load_rows(root)
    picked = sample_indices(len(rows), n, seed)
    read: dict[int, list[SubOrder]] = {}
    filled_from_exr: dict[int, int] = {}  # index -> TOP words not in the dataset's catalog
    failures: list[dict] = []
    for i in picked:
        try:
            read[i], filled = read_order(rows[i], catalogs)
            if filled:
                filled_from_exr[i] = filled
        except (Unresolved, ValueError) as e:
            failures.append({"index": i, "stage": "read", "reason": str(e)})
    used = Used()
    for subs in read.values():
        for sub in subs:
            used.add(sub)
    menu, counts = build_catalog(used, catalogs, seed)
    cases: list[PizzaCase] = []
    for i, subs in read.items():
        try:
            cases.append(convert(i, rows[i], subs, menu))
        except (Unresolved, ValueError) as e:
            failures.append({"index": i, "stage": "convert", "reason": str(e)})

    out = root / "benchmark"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{BUSINESS_ID}.json").write_text(menu.model_dump_json(indent=2) + "\n")
    with (out / "cases.jsonl").open("w") as f:
        for c in cases:
            f.write(c.model_dump_json() + "\n")
    coverage = {
        "toppings": {t: _slug(t) for t in used.toppings},
        "styles": {
            s: (_slug(s) if s in CRUST_STYLES else f"{_slug(s)}_pizza") for s in used.recipes | used.crusts
        },
        "pizza_sizes": {s: _slug(s) for s in used.pizza_sizes},
        "drinks": {d: _slug(d) for d in used.drinks},
    }
    (out / "coverage.json").write_text(json.dumps(coverage, indent=2, sort_keys=True) + "\n")
    examples: dict[str, list[str]] = {}
    for c in cases:
        for item in c.gold_extraction.items:
            if menu.item(item.menu_item_id or "").category == "drinks":
                examples.setdefault(item.variant_id, []).append(item.evidence[0].quote)
    report = {
        "dataset": {"repo": REPO, "commit": COMMIT, "split": "test", "rows": len(rows)},
        "seed": seed,
        "sampled": len(picked),
        "sample_indices": picked,
        "converted": len(cases),
        "failures": failures,
        "entities": counts,
        "used": {k: dict(sorted(getattr(used, k).items())) for k in vars(used)},
        "top_words_filled_from_exr": filled_from_exr,
        "dropped_negated_amounts": sum(c.dropped_negated_amounts for c in cases),
        "drink_variant_examples": {k: v[:5] for k, v in sorted(examples.items())},
    }
    (out / "report.json").write_text(json.dumps(report, indent=2) + "\n")
    return report


def load_cases(root: Path = PIZZA_DIR) -> tuple[MenuCatalog, list[PizzaCase]]:
    """For the PIZZA evaluation only: sealed like the test split."""
    if not os.environ.get(UNSEAL_ENV, "").strip():
        raise SealedSplitError(
            f"The PIZZA benchmark is evaluation-only. Set {UNSEAL_ENV}=<reason> for an eval run."
        )
    out = root / "benchmark"
    menu = MenuCatalog.model_validate_json((out / f"{BUSINESS_ID}.json").read_text())
    cases = [PizzaCase.model_validate_json(line) for line in (out / "cases.jsonl").read_text().splitlines()]
    return menu, cases


def main(argv: list[str] | None = None) -> None:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--download", action="store_true", help=f"fetch the pinned files from {REPO}")
    ap.add_argument("--convert", action="store_true", help="sample, build the catalog, convert")
    ap.add_argument("--n", type=int, default=N_ORDERS)
    ap.add_argument("--seed", type=int, default=SEED)
    args = ap.parse_args(argv)
    if not (args.download or args.convert):
        ap.error("nothing to do: pass --download and/or --convert")
    if args.download:
        for rel, digest in download().items():
            print(f"{digest[:12]}  {rel}")
    if args.convert:
        r = build(n=args.n, seed=args.seed)
        print(
            f"sampled {r['sampled']} of {r['dataset']['rows']} (seed {r['seed']}); converted {r['converted']}"
        )
        for k, v in r["entities"].items():
            print(f"  {k:15} " + "  ".join(f"{a}={b}" for a, b in v.items()))
        print(f"  failures: {len(r['failures'])}; 'no extra X' kept default: {r['dropped_negated_amounts']}")
        print(f"report: {OUT_DIR / 'report.json'}")


if __name__ == "__main__":
    main()
