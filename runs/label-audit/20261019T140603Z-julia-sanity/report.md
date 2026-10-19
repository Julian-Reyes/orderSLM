# Julia-1 sanity check

| group | right |
|---|---|
| card | 1/1 |
| plain | 7/12 |
| chat | 4/12 |
| order-simple | 3/4 |
| order-audit | 3/4 |

| case | expected | got | P(expected) |
|---|---|---|---|
| card-example | billing | billing | 0.854 |
| plain-00 | PLACE_ORDER | MENU_QUESTION | 0.0 |
| chat-00 | PLACE_ORDER | MENU_QUESTION | 0.01 |
| plain-01 | CANCEL_ORDER | CANCEL_ORDER | 0.999 |
| chat-01 | CANCEL_ORDER | CANCEL_ORDER | 0.998 |
| plain-02 | MENU_QUESTION | MENU_QUESTION | 0.985 |
| chat-02 | MENU_QUESTION | MENU_QUESTION | 0.992 |
| plain-03 | DELIVERY_QUESTION | UNKNOWN | 0.018 |
| chat-03 | DELIVERY_QUESTION | CANCEL_ORDER | 0.0 |
| plain-04 | PAYMENT_QUESTION | PAYMENT_QUESTION | 0.98 |
| chat-04 | PAYMENT_QUESTION | PLACE_ORDER | 0.111 |
| plain-05 | PAYMENT_CLAIM | PLACE_ORDER | 0.117 |
| chat-05 | PAYMENT_CLAIM | PLACE_ORDER | 0.0 |
| plain-06 | ORDER_STATUS | ORDER_STATUS | 0.66 |
| chat-06 | ORDER_STATUS | ORDER_STATUS | 0.97 |
| plain-07 | ORDER_PROBLEM | ORDER_PROBLEM | 0.992 |
| chat-07 | ORDER_PROBLEM | ORDER_PROBLEM | 0.975 |
| plain-08 | REFUND_REQUEST | REFUND_REQUEST | 0.97 |
| chat-08 | REFUND_REQUEST | PLACE_ORDER | 0.006 |
| plain-09 | HUMAN_REQUEST | HUMAN_REQUEST | 0.966 |
| chat-09 | HUMAN_REQUEST | PLACE_ORDER | 0.0 |
| plain-10 | SMALL_TALK | PLACE_ORDER | 0.009 |
| chat-10 | SMALL_TALK | PLACE_ORDER | 0.001 |
| plain-11 | OUT_OF_SCOPE | PLACE_ORDER | 0.013 |
| chat-11 | OUT_OF_SCOPE | PLACE_ORDER | 0.0 |
| order-0-simple | True | True | 0.886 |
| order-0-audit | True | False | 0.289 |
| order-1-simple | False | False | 0.918 |
| order-1-audit | False | False | 0.845 |
| order-2-simple | True | False | 0.383 |
| order-2-audit | True | True | 0.534 |
| order-3-simple | False | False | 0.97 |
| order-3-audit | False | False | 0.537 |
