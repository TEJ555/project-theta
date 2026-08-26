# API cost ledger

Provider token usage is converted using the rates frozen in the adapter. These are
estimates, not invoices. Provider billing records and currency conversion are
authoritative.

| Study | Status | Calls | Estimated cost USD |
|---|---|---:|---:|
| Initial Claude pilot, seed 11 | Exploratory, completed | 72 | $0.568926 |
| Claude replication, six seeds | Completed | 432 | $3.409557 |
| Adversarial confirmation 01 | Invalid wrong-protocol execution | 72 | $0.581088 |
| Total spent through confirmation 01 |  | 576 | $4.559571 |

Confirmation 02 is not included because it has not run. Its compact 48-call design has
a hard study guard of $0.55. Based on confirmation 01's observed cost per call, it
would cost approximately $0.387. That would bring the estimated cumulative total to
approximately $4.947.

The projection is below $5 but close enough that provider billing differences or
currency conversion could still trigger a $5 workspace limit. The provider limit
remains authoritative.
