"""Pilot analysis per generator (spec §7: data audit, distribution log, drop rate, cost): style and diversity of
the customer text, card agreement per scenario, intents, and a seeded audit sample for Julian. Everything is
computed from the saved files in runs/synth/<batch>/ (run.report calls this)."""

import random
import re
import statistics
from collections import Counter, defaultdict
from typing import Any

from orderslm.schema.conversation import Role
from orderslm.schema.synthetic import LabeledConversation, SynthCard, SyntheticConversation

from .dedup import customer_text, jaccard, shingles

EMOJI = re.compile("[\U0001f300-\U0001faff☀-➿]")
AUDIT_SEED = 20261016


def _customer_messages(s: SyntheticConversation) -> list[str]:
    return [m.text for m in s.conversation.messages if m.role is Role.customer]


def style_stats(convs: list[SyntheticConversation]) -> dict[str, Any]:
    if not convs:
        return {}
    msgs = [t for s in convs for t in _customer_messages(s)]
    words = [len(t.split()) for t in msgs]
    letters = [c for t in msgs for c in t if c.isalpha()]
    first = [_customer_messages(s)[0] for s in convs]
    openers = Counter(" ".join(re.findall(r"[a-z']+", t.casefold())[:2]) for t in first)
    return {
        "chats": len(convs),
        "customer_messages_per_chat": round(len(msgs) / len(convs), 2),
        "business_messages_per_chat": round(
            sum(1 for s in convs for m in s.conversation.messages if m.role is Role.business) / len(convs), 2
        ),
        "words_per_customer_message": round(statistics.mean(words), 1),
        "share_lowercase_messages": round(sum(1 for t in msgs if t == t.lower()) / len(msgs), 3),
        "share_all_caps_messages": round(
            sum(1 for t in msgs if sum(c.isalpha() for c in t) > 3 and t == t.upper()) / len(msgs), 3
        ),
        "share_messages_with_emoji": round(sum(1 for t in msgs if EMOJI.search(t)) / len(msgs), 3),
        "share_uppercase_letters": round(sum(c.isupper() for c in letters) / max(len(letters), 1), 3),
        "distinct_openers": round(len(openers) / len(first), 3),
        "top_openers": dict(openers.most_common(5)),
    }


def diversity(convs: list[SyntheticConversation]) -> dict[str, Any]:
    """Mean over chats of the highest customer-text similarity to another chat from the same generator (lower is
    more varied), and the share of distinct customer word 3-grams."""
    sh = [shingles(customer_text(s.conversation)) for s in convs]
    if len(sh) < 2:
        return {}
    nearest = [max(jaccard(a, b) for j, b in enumerate(sh) if j != i) for i, a in enumerate(sh)]
    grams = [g for s in sh for g in s]
    return {
        "mean_nearest_similarity": round(statistics.mean(nearest), 3),
        "max_nearest_similarity": round(max(nearest), 3),
        "distinct_3gram_share": round(len(set(grams)) / max(len(grams), 1), 3),
    }


def addresses(convs: list[SyntheticConversation], cards: dict[str, SynthCard]) -> dict[str, Any]:
    """How often the card's address appears in the chat as written (case-insensitive, number + street name)."""
    with_addr = [s for s in convs if cards[s.card_id].address]
    if not with_addr:
        return {}
    used = 0
    for s in with_addr:
        number, street = cards[s.card_id].address.split()[:2]  # type: ignore[union-attr]
        text = customer_text(s.conversation).casefold()
        used += number in text and street.casefold() in text
    return {"cards_with_address": len(with_addr), "card_address_used": used}


def agreement_by_scenario(
    agreement: dict[str, dict], cards: dict[str, SynthCard]
) -> dict[str, dict[str, dict[str, int]]]:
    """{scenario: {generator: {labeled, all_agree}}}."""
    out: dict[str, dict[str, dict[str, int]]] = defaultdict(
        lambda: defaultdict(lambda: {"labeled": 0, "agree": 0})
    )
    for cid, a in agreement.items():
        c = cards[cid]
        row = out[c.scenario.value][c.generator]
        row["labeled"] += 1
        row["agree"] += not a["flags"]
    return {k: dict(v) for k, v in out.items()}


def intents_by_generator(
    labels: dict[str, LabeledConversation], cards: dict[str, SynthCard]
) -> dict[str, dict]:
    out: dict[str, Counter] = defaultdict(Counter)
    for cid, lc in labels.items():
        for i in lc.intents:
            out[cards[cid].generator][i.primary.value] += 1
    return {g: dict(c.most_common()) for g, c in out.items()}


def audit_sample(
    convs: dict[str, SyntheticConversation],
    agreement: dict[str, dict],
    cards: dict[str, SynthCard],
    per_gen: int,
) -> list[str]:
    """Seeded sample for Julian's hand audit: per generator, half from the card-agreeing chats and half from the
    flagged ones (or more agreeing ones when there are few flags)."""
    rng = random.Random(AUDIT_SEED)
    picked: list[str] = []
    for g in sorted({c.generator for c in cards.values()}):
        mine = sorted(cid for cid in convs if cards[cid].generator == g and cid in agreement)
        flagged = [cid for cid in mine if agreement[cid]["flags"]]
        clean = [cid for cid in mine if not agreement[cid]["flags"]]
        k_flag = min(len(flagged), per_gen // 2)
        picked += rng.sample(flagged, k_flag) + rng.sample(clean, min(len(clean), per_gen - k_flag))
    return sorted(picked)


def _pct(n: int, d: int) -> str:
    return f"{n}/{d} ({100 * n / d:.0f}%)" if d else "–"


def render(summary: dict[str, Any], cards: dict[str, SynthCard]) -> str:
    gens = sorted(summary["by_generator"])
    short = {g: g.split("/")[1] for g in gens}
    L = [f"# Synthetic pilot `{summary['batch']}`: per-generator report", ""]
    L.append(
        'Built from the saved files in this folder (`make synth ARGS="report --batch '
        f'{summary["batch"]}"`). Versions: see `calls/*.json`. Teacher labels are finalized in code.'
    )
    L += [
        "",
        "## Yield",
        "",
        "| | " + " | ".join(short[g] for g in gens) + " |",
        "|---|" + "---|" * len(gens),
    ]
    bg = summary["by_generator"]

    def row(name: str, f) -> None:
        L.append(f"| {name} | " + " | ".join(str(f(bg[g])) for g in gens) + " |")

    row("cards", lambda r: r["cards"])
    row("chats kept", lambda r: _pct(r["kept"], r["generated"]))
    row("generation drops", lambda r: ", ".join(f"{k} {v}" for k, v in r["gen_drops"].items()) or "0")
    row("repairs", lambda r: ", ".join(f"{k} {v}" for k, v in r["repairs"].items()) or "0")
    row("labels kept", lambda r: _pct(r["labeled"], r["label_attempted"]))
    row("label drops", lambda r: ", ".join(f"{k} {v}" for k, v in r["label_drops"].items()) or "0")
    row(
        "card agrees with label",
        lambda r: _pct(r["card_agreement"]["all_agree"], r["card_agreement"]["labeled"]),
    )
    row(
        "disagreement types",
        lambda r: ", ".join(f"{k} {v}" for k, v in r["card_agreement"]["flags"].items()) or "0",
    )
    row(
        "card address used",
        lambda r: _pct(
            r["addresses"].get("card_address_used", 0), r["addresses"].get("cards_with_address", 0)
        ),
    )

    L += [
        "",
        "## Cost and tokens",
        "",
        "| | " + " | ".join(short[g] for g in gens) + " |",
        "|---|" + "---|" * len(gens),
    ]
    for stage, name in (("generation_usage", "generation"), ("label_usage", "labels (luna low)")):
        row(f"{name}: cost", lambda r, s=stage: f"${r[s]['cost_micros'] / 1e6:.4f}")
        row(f"{name}: per 1,000 chats", lambda r, s=stage: f"${r[s]['cost_per_1k_usd']}")
        row(
            f"{name}: tokens in (cached) / out",
            lambda r, s=stage: (
                f"{r[s]['input_tokens']:,} ({r[s]['cached_input_tokens']:,}) / {r[s]['output_tokens']:,}"
            ),
        )
        row(f"{name}: latency p50 ms", lambda r, s=stage: r[s]["latency_p50_ms"])

    L += [
        "",
        "## Style of the customer text",
        "",
        "| | " + " | ".join(short[g] for g in gens) + " |",
        "|---|" + "---|" * len(gens),
    ]
    for key in (
        "customer_messages_per_chat",
        "business_messages_per_chat",
        "words_per_customer_message",
        "share_lowercase_messages",
        "share_all_caps_messages",
        "share_messages_with_emoji",
        "distinct_openers",
    ):
        row(key.replace("_", " "), lambda r, k=key: r["style"].get(k))
    row(
        "top openers",
        lambda r: "; ".join(f"{k!r} {v}" for k, v in list(r["style"].get("top_openers", {}).items())[:3]),
    )
    for key in ("mean_nearest_similarity", "max_nearest_similarity", "distinct_3gram_share"):
        row(key.replace("_", " "), lambda r, k=key: r["diversity"].get(k))
    L.append("")
    L.append(
        "Nearest similarity: word 3-gram Jaccard of a chat's customer text with the most similar other chat from the"
        " same generator (lower = more varied; dedup drops ≥ 0.8)."
    )

    L += ["", "## Card agreement by scenario (agree / labeled)", ""]
    L += ["| scenario | " + " | ".join(short[g] for g in gens) + " |", "|---|" + "---|" * len(gens)]
    for scen, by in sorted(summary["agreement_by_scenario"].items()):
        L.append(
            f"| {scen} | "
            + " | ".join(f"{by[g]['agree']}/{by[g]['labeled']}" if g in by else "–" for g in gens)
            + " |"
        )

    L += ["", "## Labeled intents (primary)", ""]
    labels = sorted({k for d in summary["intents_by_generator"].values() for k in d})
    L += ["| intent | " + " | ".join(short[g] for g in gens) + " |", "|---|" + "---|" * len(gens)]
    for lab in labels:
        L.append(
            f"| {lab} | "
            + " | ".join(str(summary["intents_by_generator"].get(g, {}).get(lab, 0)) for g in gens)
            + " |"
        )
    L += ["", f"Audit sample: `audit.md` ({len(summary['audit_sample'])} chats, seed {AUDIT_SEED})."]
    return "\n".join(L) + "\n"


def render_audit(
    ids: list[str],
    convs: dict[str, SyntheticConversation],
    labels: dict[str, LabeledConversation],
    agreement: dict[str, dict],
    cards: dict[str, SynthCard],
) -> str:
    L = [
        "# Audit sample",
        "",
        "For each chat: the card, the chat, the teacher's finalized label, and the card check.",
        "",
    ]
    for cid in ids:
        c, s, lc, a = cards[cid], convs[cid], labels.get(cid), agreement.get(cid, {})
        L.append(f"## {cid}: {c.scenario.value}, {c.generator.split('/')[1]}, {c.business_id}")
        L.append(f"Card: {c.brief}")
        L.append(
            f"Card check: {', '.join(a.get('flags', [])) or 'agrees'}"
            + (
                f" (expected labels not found: {', '.join(a['missing_labels'])})"
                if a.get("missing_labels")
                else ""
            )
        )
        L.append("")
        intents = {i.message_index: i for i in lc.intents} if lc else {}
        for m in s.conversation.messages:
            tag = ""
            if m.index in intents:
                i = intents[m.index]
                tag = f" **[{i.primary.value}{' + ' + i.secondary.value if i.secondary else ''}]**"
            L.append(f"- {m.index} {m.role.value}: {m.text}{tag}")
        L.append("")
        if lc and lc.extraction:
            e = lc.extraction
            for it in e.items:
                what = it.menu_item_id or (
                    f"off-menu '{it.unmatched_text}'"
                    if it.unmatched_text
                    else "half " + " / half ".join(h.menu_item_id for h in it.halves or [])
                )
                mods = ", ".join(
                    f"{m.kind.value} {m.modifier_id or m.raw_text}"
                    + (f"→{m.replacement_modifier_id}" if m.replacement_modifier_id else "")
                    for m in it.all_modifications()
                )
                combo = ", ".join(f"{x.slot_id}={x.menu_item_id}" for x in it.combo_selections)
                L.append(
                    f"  - {it.line_id}: {it.quantity} × {what} {it.variant_id or ''} {mods} {combo}".rstrip()
                )
            L.append(
                f"  - fulfillment {e.fulfillment.method.value}, address {e.address.state.value}, payment"
                f" {e.payment.method.value}{' (claims paid)' if e.payment.customer_claims_paid else ''}, name"
                f" {e.customer_name.value or '–'}, decision {e.customer_decision.state.value}"
            )
            missing = ", ".join(f"{m.field.value}/{m.reason.value}" for m in e.missing_or_ambiguous)
            L.append(f"  - missing: {missing or 'nothing'}")
        elif lc:
            L.append("  - no order")
        else:
            L.append("  - label dropped")
        L += ["", "Audit: ☐ chat realistic ☐ card followed ☐ intents right ☐ order right. Notes:", ""]
    return "\n".join(L) + "\n"
