You read a customer's text chat with a restaurant, given the restaurant's menu (JSON) and the conversation so far.
Output one JSON object (no prose, no markdown fences) with:

- `intent`: the router label of the latest customer message: `primary`, and `secondary` only for a message with two
  requests. Labels: {label_codes}.
- `order`: the order after the latest message: items (menu ids, quantity, size, modifications, combo picks, notes),
  fulfillment and requested time, address, payment, customer name, customer decision, notes and ambiguity flags.

Use only ids from the menu. Take every value from what the customer wrote, with the exact words as evidence
(`message_index` + `quote`). Never output prices. Items about a past or placed order, or a request for staff, are
not a new order.
