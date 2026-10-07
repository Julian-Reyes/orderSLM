import { useEffect, useMemo, useRef, useState } from "preact/hooks";
import {
  api,
  type Annotated,
  type CheckResult,
  type Conversation,
  type Decision,
  type Json,
  type Menu,
  type Menus,
  type Meta,
  type Row,
} from "./api";

type Mode = "label" | "relabel" | "stats";
type Evidence = { message_index: number; quote: string };

// ---------------------------------------------------------------- helpers

/** "+05:30"-style offset of `timeZone` at `at`, so sent_at is timezone-aware in the menu's zone. */
function tzOffset(timeZone: string, at: Date): string {
  const part = new Intl.DateTimeFormat("en-US", { timeZone, timeZoneName: "longOffset" })
    .formatToParts(at)
    .find((p) => p.type === "timeZoneName")?.value;
  const m = part?.match(/GMT([+-]\d{2}):?(\d{2})?/);
  return m ? `${m[1]}:${m[2] ?? "00"}` : "+00:00";
}

function localIso(timeZone: string, at: Date): string {
  const f = new Intl.DateTimeFormat("en-CA", {
    timeZone,
    year: "numeric",
    month: "2-digit",
    day: "2-digit",
    hour: "2-digit",
    minute: "2-digit",
    second: "2-digit",
    hourCycle: "h23",
  }).formatToParts(at);
  const v = (t: string) => f.find((p) => p.type === t)?.value ?? "00";
  return `${v("year")}-${v("month")}-${v("day")}T${v("hour")}:${v("minute")}:${v("second")}${tzOffset(timeZone, at)}`;
}

function laterIso(iso: string, seconds: number): string {
  const offset = iso.slice(19);
  const base = new Date(iso);
  if (Number.isNaN(base.getTime())) return iso;
  const shifted = new Date(base.getTime() + seconds * 1000);
  const sign = offset.startsWith("-") ? -1 : 1;
  const [h, m] = offset.slice(1).split(":").map(Number);
  const local = new Date(shifted.getTime() + sign * (h * 60 + (m || 0)) * 60000);
  return local.toISOString().slice(0, 19) + offset;
}

function emptyGold(): Json {
  return {
    items: [],
    fulfillment: { method: "unknown", requested_time: { state: "not_mentioned" } },
    address: { state: "not_mentioned" },
    payment: { method: "unknown" },
    customer_name: { state: "not_mentioned" },
    missing_or_ambiguous: [],
  };
}

const defaultDecision = (): Decision => ({
  primary: "PLACE_ORDER",
  urgency: "normal",
  flags: { refers_to: "draft", asks_for_human: false },
});

function syncRouting(a: Annotated): Annotated {
  const byIndex = new Map(a.gold_routing.map((r) => [r.message_index, r.decision]));
  const gold_routing = a.conversation.messages
    .filter((m) => m.role === "customer")
    .map((m) => ({ message_index: m.index, decision: byIndex.get(m.index) ?? defaultDecision() }));
  return { ...a, gold_routing };
}

function blank(split: string, menu: Menu | undefined, annotator: string): Annotated {
  const tz = menu?.timezone ?? "America/New_York";
  const now = new Date();
  return syncRouting({
    conversation: {
      id: `${split}-${now.toISOString().slice(0, 10).replaceAll("-", "")}-${String(now.getTime()).slice(-5)}`,
      business_id: menu?.business_id ?? "",
      language: "en",
      split,
      source: "human",
      messages: [{ index: 0, role: "customer", text: "", sent_at: localIso(tz, now) }],
    },
    scenarios: [],
    style: "texting",
    gold_extraction: emptyGold(),
    gold_routing: [],
    annotator,
  });
}

const store = {
  get(key: string): string | null {
    try {
      return localStorage.getItem(key);
    } catch {
      return null;
    }
  },
  set(key: string, value: string | null) {
    try {
      if (value === null) localStorage.removeItem(key);
      else localStorage.setItem(key, value);
    } catch {
      /* private window: drafts just aren't kept */
    }
  },
};

const money = (c: number) => `$${(c / 100).toFixed(2)}`;

// ---------------------------------------------------------------- app

export function App() {
  const [meta, setMeta] = useState<Meta | null>(null);
  const [split, setSplit] = useState("dev");
  const [mode, setMode] = useState<Mode>("label");
  const [menus, setMenus] = useState<Menus>({});
  const [rows, setRows] = useState<Row[]>([]);
  const [current, setCurrent] = useState<Annotated | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [annotator, setAnnotator] = useState(() => store.get("orderslm:annotator") ?? "julian");

  useEffect(() => {
    api.meta().then(setMeta).catch((e) => setError(String(e.message ?? e)));
  }, []);

  const refresh = () => {
    if (mode === "relabel") return;
    api.list(split).then(setRows).catch((e) => setError(e.message));
  };

  useEffect(() => {
    setCurrent(null);
    api.menus(split).then(setMenus).catch((e) => setError(e.message));
    refresh();
  }, [split]);

  useEffect(() => store.set("orderslm:annotator", annotator), [annotator]);

  // ?open=<id> deep-links to a conversation in the current split.
  useEffect(() => {
    const id = new URLSearchParams(location.search).get("open");
    if (id && rows.some((r) => r.id === id) && !current) open(id);
  }, [rows]);

  const open = async (id: string) => {
    setError(null);
    const draft = store.get(`orderslm:draft:${split}:${id}`);
    if (draft && confirm("You have unsaved edits for this conversation. Restore them?")) {
      setCurrent(JSON.parse(draft));
      return;
    }
    setCurrent(syncRouting(await api.get(split, id)));
  };

  if (!meta) return <div class="boot">{error ?? "Loading…"}</div>;
  const firstMenu = Object.values(menus)[0]?.menu;

  return (
    <div class="shell">
      <header class="top">
        <strong class="brand">OrderSLM</strong>
        <span class="muted">annotation</span>
        <nav class="tabs">
          {meta.splits.map((s) => (
            <button class={s === split ? "tab on" : "tab"} onClick={() => setSplit(s)}>
              {s}
              {s === "test" && meta.test_locked ? " (locked)" : ""}
            </button>
          ))}
        </nav>
        <nav class="tabs">
          {(["label", "stats", ...(split === "test" && meta.test_locked ? ["relabel"] : [])] as Mode[]).map((m) => (
            <button class={m === mode ? "tab on" : "tab"} onClick={() => setMode(m)}>
              {m === "relabel" ? "blind relabel" : m}
            </button>
          ))}
        </nav>
        <label class="annotator">
          annotator <input value={annotator} onInput={(e) => setAnnotator(e.currentTarget.value)} />
        </label>
      </header>
      {error && (
        <div class="banner err" onClick={() => setError(null)}>
          {error}
        </div>
      )}
      {notice && (
        <div class="banner ok" onClick={() => setNotice(null)}>
          {notice}
        </div>
      )}
      {mode === "stats" ? (
        <Stats split={split} />
      ) : mode === "relabel" ? (
        <Relabel menus={menus} meta={meta} annotator={annotator} onError={setError} onNotice={setNotice} />
      ) : (
        <div class="body">
          <aside class="side">
            <button class="primary wide" onClick={() => setCurrent(blank(split, firstMenu, annotator))}>
              New conversation
            </button>
            <ul class="list">
              {rows.map((r) => (
                <li class={current?.conversation.id === r.id ? "on" : ""} onClick={() => open(r.id)}>
                  <div class="id">{r.id}</div>
                  <div class="muted small">
                    {r.business_id} · {r.messages} msg · {r.style}
                  </div>
                  <div class="chips">
                    {r.scenarios.map((s) => (
                      <span class="chip">{s}</span>
                    ))}
                  </div>
                </li>
              ))}
              {!rows.length && <li class="muted small">No conversations in {split} yet.</li>}
            </ul>
          </aside>
          {current ? (
            <Editor
              key={current.conversation.id}
              split={split}
              meta={meta}
              menus={menus}
              initial={current}
              locked={split === "test" && meta.test_locked}
              save={async (a, reason) => {
                const r = await api.save(split, a, reason);
                store.set(`orderslm:draft:${split}:${a.conversation.id}`, null);
                setNotice(`Saved ${r.saved}`);
                refresh();
              }}
              onError={setError}
            />
          ) : (
            <main class="empty muted">Pick a conversation or start a new one.</main>
          )}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------- editor

interface EditorProps {
  split: string;
  meta: Meta;
  menus: Menus;
  initial: Annotated;
  locked: boolean;
  blindConversation?: boolean; // relabel: messages are read-only
  save: (a: Annotated, changeReason?: string) => Promise<void>;
  onError: (e: string) => void;
}

function Editor({ split, meta, menus, initial, locked, blindConversation, save, onError }: EditorProps) {
  const [a, setA] = useState<Annotated>(initial);
  const [goldText, setGoldText] = useState(() => JSON.stringify(initial.gold_extraction, null, 2));
  const [goldError, setGoldError] = useState<string | null>(null);
  const [check, setCheck] = useState<CheckResult | null>(null);
  const [evidence, setEvidence] = useState<Evidence | null>(null);
  const [reason, setReason] = useState("");
  const [saving, setSaving] = useState(false);
  const timer = useRef<number | undefined>(undefined);
  const menu = menus[a.conversation.business_id]?.menu;
  const draftKey = `orderslm:draft:${split}:${a.conversation.id}`;

  // Debounced server check on every edit; unsaved work is kept in localStorage.
  useEffect(() => {
    if (!blindConversation) store.set(draftKey, JSON.stringify(a));
    window.clearTimeout(timer.current);
    timer.current = window.setTimeout(() => {
      (blindConversation ? api.check("test", a) : api.check(split, a))
        .then(setCheck)
        .catch((e) => onError(e.message));
    }, 500);
  }, [a]);

  const update = (f: (a: Annotated) => Annotated) => setA((prev) => syncRouting(f(prev)));
  const conv = a.conversation;
  const setConv = (c: Partial<Conversation>) => update((p) => ({ ...p, conversation: { ...p.conversation, ...c } }));
  const setMessages = (messages: Conversation["messages"]) =>
    setConv({ messages: messages.map((m, i) => ({ ...m, index: i })) });

  const setGold = (gold: Json) => {
    setGoldText(gold === null ? "null" : JSON.stringify(gold, null, 2));
    setGoldError(null);
    update((p) => ({ ...p, gold_extraction: gold }));
  };
  const onGoldText = (text: string) => {
    setGoldText(text);
    try {
      const parsed = JSON.parse(text) as Json;
      setGoldError(null);
      update((p) => ({ ...p, gold_extraction: parsed }));
    } catch (e) {
      setGoldError(String((e as Error).message));
    }
  };

  const gold = a.gold_extraction as Record<string, Json> | null;

  const addItem = (itemId: string, variantId: string, quantity: number) => {
    if (!gold || !evidence) return;
    const items = (gold.items as Record<string, Json>[]) ?? [];
    const used = new Set(items.map((i) => String(i.line_id)));
    let n = items.length + 1;
    while (used.has(`L${n}`)) n++;
    const line: Record<string, Json> = { line_id: `L${n}`, menu_item_id: itemId, quantity, evidence: [evidence] };
    if (variantId) line.variant_id = variantId;
    setGold({ ...gold, items: [...items, line] });
  };

  const applyRules = () => {
    if (!gold || !check?.derived_missing) return;
    setGold({
      ...gold,
      missing_or_ambiguous: check.derived_missing as unknown as Json,
      clarification_question: check.template_question ?? null,
    });
  };

  const onSelect = (index: number, el: HTMLTextAreaElement) => {
    const quote = el.value.slice(el.selectionStart, el.selectionEnd);
    if (quote.trim()) setEvidence({ message_index: index, quote });
  };

  const doSave = async () => {
    setSaving(true);
    try {
      await save(a, locked ? reason : undefined);
    } catch (e) {
      onError((e as Error).message);
    } finally {
      setSaving(false);
    }
  };

  return (
    <main class="editor">
      <section class="col">
        <h2>Conversation</h2>
        <div class="grid2">
          <label>
            id
            <input value={conv.id} disabled={blindConversation} onInput={(e) => setConv({ id: e.currentTarget.value })} />
          </label>
          <label>
            business
            <select
              value={conv.business_id}
              disabled={blindConversation}
              onChange={(e) => setConv({ business_id: e.currentTarget.value })}
            >
              {Object.entries(menus).map(([id, m]) => (
                <option value={id}>
                  {m.menu.name}
                  {m.menu.held_out ? " (held out)" : ""}
                </option>
              ))}
            </select>
          </label>
          <label>
            style
            <select value={a.style} onChange={(e) => update((p) => ({ ...p, style: e.currentTarget.value }))}>
              {meta.styles.map((s) => (
                <option value={s}>{s}</option>
              ))}
            </select>
          </label>
          <label>
            annotator
            <input value={a.annotator} onInput={(e) => update((p) => ({ ...p, annotator: e.currentTarget.value }))} />
          </label>
        </div>
        <div class="chips pick">
          {meta.scenarios.map((s) => {
            const on = a.scenarios.includes(s);
            return (
              <button
                class={on ? "chip on" : "chip"}
                onClick={() =>
                  update((p) => ({ ...p, scenarios: on ? p.scenarios.filter((x) => x !== s) : [...p.scenarios, s] }))
                }
              >
                {s}
              </button>
            );
          })}
        </div>
        <p class="muted small">Select text in a customer message to use it as evidence.</p>
        {conv.messages.map((m, i) => (
          <div class={`msg ${m.role}`}>
            <div class="msghead">
              <span class="idx">#{i}</span>
              <button
                class="link"
                disabled={blindConversation}
                onClick={() =>
                  setMessages(
                    conv.messages.map((x, j) =>
                      j === i ? { ...x, role: x.role === "customer" ? "business" : "customer" } : x,
                    ),
                  )
                }
              >
                {m.role}
              </button>
              <input
                class="time"
                value={m.sent_at}
                disabled={blindConversation}
                onInput={(e) =>
                  setMessages(conv.messages.map((x, j) => (j === i ? { ...x, sent_at: e.currentTarget.value } : x)))
                }
              />
              {!blindConversation && conv.messages.length > 1 && (
                <button class="link danger" onClick={() => setMessages(conv.messages.filter((_, j) => j !== i))}>
                  remove
                </button>
              )}
            </div>
            <textarea
              rows={2}
              value={m.text}
              readOnly={blindConversation}
              onInput={(e) =>
                setMessages(conv.messages.map((x, j) => (j === i ? { ...x, text: e.currentTarget.value } : x)))
              }
              onMouseUp={(e) => onSelect(i, e.currentTarget)}
              onKeyUp={(e) => onSelect(i, e.currentTarget)}
            />
          </div>
        ))}
        {!blindConversation && (
          <button
            onClick={() => {
              const last = conv.messages[conv.messages.length - 1];
              setMessages([
                ...conv.messages,
                { index: conv.messages.length, role: "customer", text: "", sent_at: laterIso(last.sent_at, 20) },
              ]);
            }}
          >
            + message
          </button>
        )}
        <label class="block">
          annotation notes (every judgment call)
          <textarea
            rows={2}
            value={a.annotation_notes ?? ""}
            onInput={(e) => update((p) => ({ ...p, annotation_notes: e.currentTarget.value || null }))}
          />
        </label>
        {menu && <MenuRef menu={menu} />}
      </section>

      <section class="col">
        <h2>Routing</h2>
        <table class="routing">
          <thead>
            <tr>
              <th>#</th>
              <th>primary</th>
              <th>secondary</th>
              <th>urgency</th>
              <th>refers to</th>
              <th>human</th>
            </tr>
          </thead>
          <tbody>
            {a.gold_routing.map((r, k) => {
              const set = (d: Partial<Decision>) =>
                update((p) => ({
                  ...p,
                  gold_routing: p.gold_routing.map((x, j) => (j === k ? { ...x, decision: { ...x.decision, ...d } } : x)),
                }));
              const d = r.decision;
              return (
                <tr title={conv.messages[r.message_index]?.text}>
                  <td>{r.message_index}</td>
                  <td>
                    <select value={d.primary} title={meta.labels[d.primary]} onChange={(e) => set({ primary: e.currentTarget.value })}>
                      {Object.keys(meta.labels).map((l) => (
                        <option value={l} title={meta.labels[l]}>
                          {l}
                        </option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <select value={d.secondary ?? ""} onChange={(e) => set({ secondary: e.currentTarget.value || null })}>
                      <option value="">—</option>
                      {Object.keys(meta.labels).map((l) => (
                        <option value={l}>{l}</option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <select value={d.urgency} title={meta.urgency[d.urgency]} onChange={(e) => set({ urgency: e.currentTarget.value })}>
                      {Object.keys(meta.urgency).map((u) => (
                        <option value={u}>{u}</option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <select
                      value={d.flags.refers_to}
                      onChange={(e) => set({ flags: { ...d.flags, refers_to: e.currentTarget.value } })}
                    >
                      {Object.keys(meta.references).map((u) => (
                        <option value={u}>{u}</option>
                      ))}
                    </select>
                  </td>
                  <td>
                    <input
                      type="checkbox"
                      checked={d.flags.asks_for_human}
                      onChange={(e) => set({ flags: { ...d.flags, asks_for_human: e.currentTarget.checked } })}
                    />
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>

        <h2>
          Gold extraction{" "}
          <label class="inline small">
            <input type="checkbox" checked={gold === null} onChange={(e) => setGold(e.currentTarget.checked ? null : emptyGold())} />{" "}
            no order (null)
          </label>
        </h2>
        {gold !== null && (
          <>
            <div class="evidence">
              {evidence ? (
                <>
                  evidence: <code>#{evidence.message_index}</code> “{evidence.quote}”
                  <button class="link" onClick={() => navigator.clipboard?.writeText(JSON.stringify(evidence))}>
                    copy JSON
                  </button>
                </>
              ) : (
                <span class="muted">no evidence selected</span>
              )}
            </div>
            {menu && <AddItem menu={menu} disabled={!evidence} onAdd={addItem} />}
            <div class="row">
              <button onClick={applyRules} disabled={!check?.derived_missing}>
                Fill missing info + question from the rules
              </button>
            </div>
          </>
        )}
        <textarea class={goldError ? "json bad" : "json"} rows={22} spellcheck={false} value={goldText} onInput={(e) => onGoldText(e.currentTarget.value)} />
        {goldError && <div class="err small">JSON: {goldError}</div>}

        <CheckPanel check={check} />

        <div class="savebar">
          {locked && !blindConversation && (
            <input class="grow" placeholder="reason for changing locked gold (logged)" value={reason} onInput={(e) => setReason(e.currentTarget.value)} />
          )}
          <button class="primary" disabled={saving || !check?.valid || !!goldError || (locked && !blindConversation && !reason.trim())} onClick={doSave}>
            {saving ? "Saving…" : "Save"}
          </button>
        </div>
      </section>
    </main>
  );
}

function AddItem({ menu, disabled, onAdd }: { menu: Menu; disabled: boolean; onAdd: (i: string, v: string, q: number) => void }) {
  const [itemId, setItemId] = useState(menu.items[0]?.id ?? "");
  const [variant, setVariant] = useState("");
  const [qty, setQty] = useState(1);
  const item = menu.items.find((i) => i.id === itemId);
  useEffect(() => setItemId(menu.items[0]?.id ?? ""), [menu.business_id]);
  return (
    <div class="row additem">
      <select value={itemId} onChange={(e) => (setItemId(e.currentTarget.value), setVariant(""))}>
        {menu.items.map((i) => (
          <option value={i.id}>{i.name}</option>
        ))}
      </select>
      {!!item?.variants.length && (
        <select value={variant} onChange={(e) => setVariant(e.currentTarget.value)}>
          <option value="">{item.default_variant_id ? `default (${item.default_variant_id})` : "size not stated"}</option>
          {item.variants.map((v) => (
            <option value={v.id}>{v.name}</option>
          ))}
        </select>
      )}
      <input type="number" min={1} max={99} value={qty} onInput={(e) => setQty(Number(e.currentTarget.value) || 1)} />
      <button disabled={disabled} title={disabled ? "select evidence text in a message first" : ""} onClick={() => onAdd(itemId, variant, qty)}>
        + item line
      </button>
    </div>
  );
}

function MenuRef({ menu }: { menu: Menu }) {
  const [q, setQ] = useState("");
  const needle = q.toLowerCase();
  const items = useMemo(
    () => menu.items.filter((i) => !needle || i.id.includes(needle) || i.name.toLowerCase().includes(needle)),
    [menu, needle],
  );
  const mods = new Map(menu.modifiers.map((m) => [m.id, m]));
  return (
    <details class="menuref">
      <summary>
        Menu: {menu.name} · {menu.opens_at.slice(0, 5)}–{menu.closes_at.slice(0, 5)} {menu.timezone}
      </summary>
      <input placeholder="filter items" value={q} onInput={(e) => setQ(e.currentTarget.value)} />
      {items.map((i) => (
        <div class="menuitem">
          <code>{i.id}</code> {i.name} <span class="muted">{money(i.base_price_cents)}</span>
          {i.splittable && <span class="chip">half-and-half</span>}
          {!!i.variants.length && (
            <div class="small">
              variants: {i.variants.map((v) => v.id).join(", ")}
              {i.default_variant_id ? ` (default ${i.default_variant_id})` : " (no default)"}
            </div>
          )}
          {!!i.ingredient_ids.length && <div class="small">includes: {i.ingredient_ids.join(", ")}</div>}
          {!!i.addon_ids.length && (
            <div class="small muted">
              add-ons: {i.addon_ids.map((id) => `${id} (${mods.get(id)?.group})`).join(", ")}
            </div>
          )}
          {i.combo_slots.map((s) => (
            <div class="small">
              slot <code>{s.id}</code>: {s.choices.join(", ")}
            </div>
          ))}
        </div>
      ))}
    </details>
  );
}

function CheckPanel({ check }: { check: CheckResult | null }) {
  if (!check) return <div class="check muted">checking…</div>;
  const pricing = check.pricing as { ok?: boolean; data?: { total_cents?: number; lines?: { display_name: string; quantity: number; line_total_cents: number }[] }; error?: { message?: string } } | undefined;
  return (
    <div class="check">
      <div class={check.valid ? "status ok" : "status bad"}>{check.valid ? "valid: ready to save" : "not valid yet"}</div>
      {check.findings.map((f) => (
        <div class={f.blocking ? "finding bad" : "finding warn"}>
          <code>{f.code}</code> {f.message}
        </div>
      ))}
      {check.derived_missing && (
        <div class="small">
          rules say missing: {check.derived_missing.map((m) => `${m.field}${m.line_id ? `(${m.line_id})` : ""}`).join(", ") || "nothing"}
          {check.template_question && <div class="muted">template question: “{check.template_question}”</div>}
        </div>
      )}
      {pricing && (
        <div class="small">
          {pricing.ok && pricing.data ? (
            <>
              quote:{" "}
              {pricing.data.lines?.map((l) => `${l.quantity}× ${l.display_name} ${money(l.line_total_cents)}`).join("; ")} · total{" "}
              {money(pricing.data.total_cents ?? 0)}
            </>
          ) : (
            <span class="muted">can't price yet: {pricing.error?.message}</span>
          )}
        </div>
      )}
    </div>
  );
}

// ---------------------------------------------------------------- stats and relabel

function Stats({ split }: { split: string }) {
  const [data, setData] = useState<{ stats: Json; near_duplicates: [string, string, number][] } | null>(null);
  const [err, setErr] = useState<string | null>(null);
  useEffect(() => {
    api.stats(split).then(setData).catch((e) => setErr(e.message));
  }, [split]);
  if (err) return <main class="pad err">{err}</main>;
  if (!data) return <main class="pad muted">Loading…</main>;
  const s = data.stats as Record<string, Json>;
  return (
    <main class="pad stats">
      <h2>
        {split}: {String(s.conversations)} conversations, {String(s.customer_messages)} customer messages
      </h2>
      <div class="statgrid">
        {Object.entries(s)
          .filter(([, v]) => v && typeof v === "object")
          .map(([k, v]) => (
            <div class="card">
              <h3>{k.replaceAll("_", " ")}</h3>
              {Object.entries(v as Record<string, number>).map(([name, n]) => (
                <div class="statrow">
                  <span>{name}</span>
                  <b>{n}</b>
                </div>
              ))}
              {!Object.keys(v as object).length && <div class="muted small">none yet</div>}
            </div>
          ))}
      </div>
      <h3>Near-duplicates (customer text, Jaccard ≥ 0.8)</h3>
      {data.near_duplicates.length ? (
        data.near_duplicates.map(([x, y, sc]) => (
          <div>
            {x} ~ {y} ({sc})
          </div>
        ))
      ) : (
        <div class="muted">none</div>
      )}
    </main>
  );
}

function Relabel({
  menus,
  meta,
  annotator,
  onError,
  onNotice,
}: {
  menus: Menus;
  meta: Meta;
  annotator: string;
  onError: (e: string) => void;
  onNotice: (n: string) => void;
}) {
  const [listing, setListing] = useState<{ ids: string[]; not_before: string; done: string[] } | null>(null);
  const [current, setCurrent] = useState<Annotated | null>(null);
  const load = () => api.relabelList().then(setListing).catch((e) => onError(e.message));
  useEffect(() => void load(), []);
  const open = async (id: string) => {
    const { conversation } = await api.relabelGet(id);
    setCurrent(syncRouting({ conversation, scenarios: [], style: "texting", gold_extraction: emptyGold(), gold_routing: [], annotator }));
  };
  return (
    <div class="body">
      <aside class="side">
        <p class="small muted">Blind relabel: earlier labels are hidden. Label from scratch.</p>
        <ul class="list">
          {listing?.ids.map((id) => (
            <li class={current?.conversation.id === id ? "on" : ""} onClick={() => open(id)}>
              <div class="id">
                {id} {listing.done.includes(id) && <span class="chip on">done</span>}
              </div>
            </li>
          ))}
        </ul>
      </aside>
      {current ? (
        <Editor
          key={current.conversation.id}
          split="test"
          meta={meta}
          menus={menus}
          initial={current}
          locked={false}
          blindConversation
          save={async (a) => {
            await api.relabelSave(a);
            onNotice(`Relabel saved for ${a.conversation.id}`);
            load();
          }}
          onError={onError}
        />
      ) : (
        <main class="empty muted">Pick a conversation from the relabel sample.</main>
      )}
    </div>
  );
}
