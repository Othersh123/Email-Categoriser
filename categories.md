# Categories

Every email gets exactly one label. These definitions are the spec: the eval set is labelled against them, and the classifier prompt is written from them. If a case is ambiguous, decide it here first, then update the eval set and prompt to match.

Each rule has to be decidable from the email itself (sender, subject, body), because that's all the model sees.

## Labels

| Label | Counts | Doesn't count |
|---|---|---|
| **Spam** | Deceptive or junk email: phishing, scams, fake prizes, impersonating a bank or brand, pressure to click a link or share details. | Real marketing, even from a brand I never signed up with (Promotions). |
| **Statements** | Periodic account statements from banks: monthly savings account statements and credit card statements. | One-off transaction alerts or payment reminders (Important). Bank offers and rewards (Promotions). |
| **Important** | Needs my attention or action: a real person writing to me, payment reminders, security alerts, account changes, deliveries, order confirmations and receipts. | Marketing that only *sounds* urgent ("Last chance!", "Action required to claim your discount"). |
| **Podcasts and blogs** | Something to listen to or read: new podcast episodes, show notes, Substack posts, blog updates, editorial newsletters. | Brand marketing written like an article (Promotions). |
| **Promotions** | Marketing from any company: sales, discount codes, new products, bank offers. Includes brands I never signed up with. | Anything deceptive or scammy (Spam). |
| **Other** | Fits none of the above, e.g. LinkedIn and X notifications. | Don't use this to dodge a hard call between two real labels. |

## Tie-breaking rules

When an email fits more than one label, the first match wins:

1. **Spam**. A fake "your statement is ready, log in here" email is Spam, not Statements.
2. **Statements**. A statement that also shows the payment due date is still a Statement.
3. **Important**
4. **Podcasts and blogs**
5. **Promotions**
6. **Other**

## Decisions log

- 2026-10-17: Dropped "Credit card rewards" (rare in my inbox). Added "Statements" for bank and card statements.
- 2026-10-17: Renamed "Brand offers" to "Promotions".
- 2026-10-17: Merged "Podcast links" and "Blog posts" into "Podcasts and blogs".
- 2026-10-17: Order confirmations and receipts are Important.
- 2026-10-17: LinkedIn and X notifications are Other.
- 2026-10-17: Sales from brands I never signed up with are Promotions, not Spam. The model can't know who I signed up with, so Spam is about deception, not consent.
