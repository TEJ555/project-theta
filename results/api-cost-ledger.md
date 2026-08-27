# API cost ledger

Provider token usage is converted using the rates frozen in the adapter. These are
estimates, not invoices. Provider billing records and currency conversion are
authoritative.

| Study | Status | Calls | Estimated cost USD |
|---|---|---:|---:|
| Initial Claude pilot, seed 11 | Exploratory, completed | 72 | $0.568926 |
| Claude replication, six seeds | Completed | 432 | $3.409557 |
| Adversarial confirmation 01 | Invalid wrong-protocol execution | 72 | $0.581088 |
| Adversarial confirmation 02 | Valid, progression gate failed | 48 | $0.339075 |
| Total spent through confirmation 02 |  | 624 | $4.898646 |

Two engineering prompts were sent through an authenticated Claude Max subscription
while developing and validating the subscription adapter. One was stopped by a local
post-response guard and one completed the smoke test. Neither used a Console API key,
so they do not change the estimated Console API total above. Claude Code's separate
dollar-equivalent usage estimate is retained in the smoke record.

The completed Independent Theta Max diagnostic added 180 subscription prompts. Every
call recorded the Claude Max billing route and no metered provider variables. Its CLI
dollar-equivalent estimate was $48.608463, while estimated Console API spend remained
$0.00. It therefore does not change the Console API total above.

Confirmation 02 completed below its $0.55 study guard. No further paid study is
authorised by its result because the preregistered progression gate failed.

The recorded estimate is below $5 but close enough that provider billing differences
or currency conversion could produce a different invoiced total. The provider billing
record and workspace limit remain authoritative.
