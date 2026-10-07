// Thin client for orderslm.app.main. Shapes mirror the Pydantic contracts (docs/SCHEMA.md);
// gold extraction is edited as JSON and validated by the server, so it stays loosely typed here.

export type Json = null | boolean | number | string | Json[] | { [k: string]: Json };

export interface Meta {
  splits: string[];
  test_locked: boolean;
  labels: Record<string, string>;
  urgency: Record<string, string>;
  references: Record<string, string>;
  scenarios: string[];
  styles: string[];
}

export interface Variant { id: string; name: string; price_delta_cents: number }
export interface Modifier { id: string; name: string; group: string; price_cents: number }
export interface MenuItem {
  id: string;
  name: string;
  category: string;
  base_price_cents: number;
  variants: Variant[];
  default_variant_id: string | null;
  ingredient_ids: string[];
  addon_ids: string[];
  splittable: boolean;
  combo_slots: { id: string; name: string; choices: string[] }[];
}
export interface Menu {
  business_id: string;
  name: string;
  timezone: string;
  opens_at: string;
  closes_at: string;
  held_out: boolean;
  modifiers: Modifier[];
  items: MenuItem[];
}
export type Menus = Record<string, { version: string; menu: Menu }>;

export interface Message { index: number; role: "customer" | "business"; text: string; sent_at: string }
export interface Conversation {
  id: string;
  business_id: string;
  language: string;
  split: string;
  source: string;
  messages: Message[];
}
export interface Decision {
  primary: string;
  secondary?: string | null;
  urgency: string;
  flags: { refers_to: string; asks_for_human: boolean };
}
export interface Annotated {
  conversation: Conversation;
  scenarios: string[];
  style: string;
  gold_extraction: Json;
  gold_routing: { message_index: number; decision: Decision }[];
  annotator: string;
  annotation_notes?: string | null;
}
export interface Row { id: string; business_id: string; scenarios: string[]; style: string; messages: number; annotator: string }
export interface Finding { code: string; message: string; blocking: boolean }
export interface CheckResult {
  valid: boolean;
  findings: Finding[];
  derived_missing?: { field: string; reason: string; line_id: string | null }[];
  template_question?: string | null;
  pricing?: Json;
}

async function call<T>(method: string, url: string, body?: unknown): Promise<T> {
  const r = await fetch(url, {
    method,
    headers: body === undefined ? {} : { "Content-Type": "application/json" },
    body: body === undefined ? undefined : JSON.stringify(body),
  });
  const data = await r.json().catch(() => ({}));
  if (!r.ok) {
    const d = (data as { detail?: unknown }).detail;
    throw new Error(typeof d === "string" ? d : JSON.stringify(d ?? data));
  }
  return data as T;
}

export const api = {
  meta: () => call<Meta>("GET", "/api/meta"),
  menus: (split: string) => call<Menus>("GET", `/api/${split}/menus`),
  list: (split: string) => call<Row[]>("GET", `/api/${split}/conversations`),
  get: (split: string, id: string) => call<Annotated>("GET", `/api/${split}/conversations/${id}`),
  check: (split: string, a: Annotated) => call<CheckResult>("POST", `/api/${split}/check`, a),
  save: (split: string, a: Annotated, change_reason?: string) =>
    call<{ saved: string }>("PUT", `/api/${split}/conversations/${a.conversation.id}`, { annotated: a, change_reason }),
  stats: (split: string) => call<{ stats: Json; near_duplicates: [string, string, number][] }>("GET", `/api/${split}/stats`),
  relabelList: () => call<{ ids: string[]; not_before: string; done: string[] }>("GET", "/api/relabel"),
  relabelGet: (id: string) => call<{ conversation: Conversation }>("GET", `/api/relabel/${id}`),
  relabelSave: (a: Annotated) =>
    call<{ saved: string }>("PUT", `/api/relabel/${a.conversation.id}`, { annotated: a }),
};
