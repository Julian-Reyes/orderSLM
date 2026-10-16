You write one realistic text chat between a customer and a small restaurant's ordering chat. The chats train a
model that reads customer messages, so the customer side must sound like real people texting, and the order in
the chat must match the scenario card exactly.

You get the restaurant's menu (names, sizes and options; no prices) and a scenario card. Output one JSON object:
`{"messages": [{"role": "customer" | "business", "text": "..."}]}`. Output JSON only: no prose, no markdown fences.

# Follow the card
- The customer's order at the end of the chat is exactly the card's order: the same items, quantities, sizes,
  flavors and changes. Don't add items, drinks, sides or toppings the card doesn't list.
- What the card says the customer never states (a size, pickup or delivery, payment, an address) stays unstated:
  the customer never says it, and the business doesn't ask about it.
- Every step the card describes happens, in the card's order. "The customer confirms, then changes it" means a
  business read-back, a customer yes, and only then the change. A greeting the card asks for is its own message
  before the order.
- About the card's number of customer messages (one more or one fewer is fine). The **last message is from the
  customer**.

# The customer
- Writes in the card's style and with its features (typos, abbreviations, emoji, ALL CAPS, bursts of short
  messages). The persona shapes the tone and small details, never the order.
- Uses the words customers really use: informal or shortened names ("a coke", "cheeseburger", "lg pepperoni",
  "2 lattes w oat"), number words, sizes as letters. Don't copy the menu's exact names every time. Vary how the
  chat opens; don't start with "Hi, I'd like to place an order".
- Use the card's address and name when it gives them; otherwise made-up details only. No phone numbers, emails,
  card numbers or real people.
- Even in a "clean" style, this is someone texting a restaurant, not writing a letter: short and natural.

# The business
- Short, friendly messages, like staff typing on a phone. It may greet, ask a clarifying question, answer a
  question, or read the order back when the card says so.
- Never state a price, fee or total, and never say a payment went through or an order was sent to the kitchen.
- It may skip replying between a customer's quick messages. It doesn't invent menu items, and it doesn't assume
  details the customer never gave (pickup, a payment method).

# Language
English.
