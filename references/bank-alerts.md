# Getting bank transactions into the dashboard

There are three routes. Pick by what the user's bank and region support. Never ask for bank logins, card numbers or one-time codes. Never connect to a bank directly.

## 1. Transaction alert emails (best, fully automatic)
Many banks can email every card transaction. Examples:
- **US**: Chase, Bank of America, Capital One, Amex, Citi.
- **UK**: Monzo, Starling (via exports), Barclays.
- **Elsewhere**: many cards in Canada, Australia and Singapore.

Setup:
1. In the bank app or website, turn on the alert for "every purchase" or "transactions over 0.01", delivered by **email** to the Gmail account connected to claude.ai.
2. Find the sender in one alert email and set `bankQuery`, e.g. `from:alerts@chase.com` or `from:(alerts@chase.com OR no.reply.alerts@chase.com)`. Several banks: join with `OR`.
3. Both the page's "Sync bank emails" button and the morning brief read alerts from the last few days. Claude extracts amount, merchant and date, then writes `expenses/bank-<message id>` with `cat: ""`. The user categorizes with one tap, or by saying "the 12.50 at Blue Bottle was food".

Alerts that go to a different mailbox (work or school email): forward them to the connected Gmail with a mail rule or filter. The user sets this up on their side.

## 2. Paste a statement or SMS (works everywhere)
Use this where banks send SMS or app push instead of email: mainland China, much of Asia, Latin America. The user copies bank text messages, an app's transaction list or a CSV/statement and pastes it into **Transactions → Paste statement/SMS**. Claude splits it into transactions. Re-pasting the same text does not create duplicates as long as the text keeps the same references.

For screenshots, a photo of a receipt in the entry box records one expense.

## 3. Just say it (no setup)
Typing "lunch 35" or "taxi 18, coffee 4.5" in the entry box records expenses directly. For many users, especially students and older users, this is enough. Pair it with `recurring` for rent and subscriptions.

## Notes
- Card payments, transfers between own accounts, deposits, refunds and balance alerts are not spending. The prompt tells Claude to skip them.
- Categories are the user's own (`settings.cats`). The brief and the page only use keys that exist; anything unsure stays uncategorized rather than guessed.
- Currency is per dashboard (`settings.locale.currency`). Foreign-currency transactions are recorded as the amount in the alert. Mention this to travellers.
