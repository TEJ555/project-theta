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

Confirmation 02 completed below its $0.55 study guard. No further paid study is
authorised by its result because the preregistered progression gate failed.

The recorded estimate is below $5 but close enough that provider billing differences
or currency conversion could produce a different invoiced total. The provider billing
record and workspace limit remain authoritative.
