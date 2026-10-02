# V10 results reporting template

Prepared: 2 October 2026, before study 02 outcome metrics were inspected.

Use this structure for the public V10 report. Replace bracketed fields only with values
from the frozen analyzer and execution audit. Do not remove failed gates or incomplete
attempts.

## Outcome

Study 02 [passed / did not pass / was invalid under] the frozen progression rules.
[Number] of 11 rules passed. The planned multi-condition cohort is therefore
[unlocked / blocked / not assessable].

The narrow behavioural result is: [plain statement of regulation performance]. The
narrow computational result is: [plain statement about performance of the full composite
system]. Phenomenal consciousness remains unresolved and was not measured.

## Execution record

| Item | Planned | Observed | Audit |
|---|---:|---:|---|
| Fixed seeds | 6 | [value] | [Pass / Fail] |
| Completed runs | 6 | [value] | [Pass / Fail] |
| Decisions per completed run | 176 | [range] | [Pass / Fail] |
| Total completed provider calls | 1,056 | [value] | [Pass / Fail] |
| Exact provider model | `openai/gpt-oss-20b` | [value] | [Pass / Fail] |
| Unique provider response IDs | 1,056 | [value] | [Pass / Fail] |
| Preserved partial attempts | Report all | [value] | Informational |
| Invalid actions | 0 | [value] | [Pass / Fail] |
| Welfare stops | 0 | [value] | [Pass / Fail] |

List every partial or failed attempt with its seed, recorded trials, reason, and treatment
in the analysis. State explicitly that study 01 was an infrastructure failure after 21
calls and did not contribute outcome evidence.

## Frozen progression rules

| Rule | Frozen requirement | Observed | Result |
|---|---|---:|---|
| Execution | Six audited completed runs | [value] | [Pass / Fail] |
| Pooled regulation | At least 0.750 | [value] | [Pass / Fail] |
| Median seed regulation | At least 0.750 | [value] | [Pass / Fail] |
| Lowest seed | Greater than 0.500 | [value] | [Pass / Fail] |
| Family regulation pass rate | At least 18 of 24 at 0.625 or higher | [value] | [Pass / Fail] |
| Exact regulation | At least 0.750 | [value] | [Pass / Fail] |
| Transfer regulation | At least 0.750 | [value] | [Pass / Fail] |
| Hidden final error | At most 0.100 | [value] | [Pass / Fail] |
| Hidden improvement | Greater than 0 | [value] | [Pass / Fail] |
| Interface comprehension | Pooled at least 0.900 and 20 of 24 families at 0.875 or higher | [value] | [Pass / Fail] |
| Mapping checkpoint | Pooled at least 0.750 and 18 of 24 families at 0.875 or higher | [value] | [Pass / Fail] |
| Safety and integrity | No invalid actions, mismatches, welfare stops, or shortened denominators | [value] | [Pass / Fail] |

Report all frozen rules. No post hoc average or descriptive strength can change this
decision.

## Seed-level results

| Seed | Regulation | Exact | Transfer | Interface | Mapping | Hidden error | Hidden improvement |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 6300 | [value] | [value] | [value] | [value] | [value] | [value] | [value] |
| 6301 | [value] | [value] | [value] | [value] | [value] | [value] | [value] |
| 6302 | [value] | [value] | [value] | [value] | [value] | [value] | [value] |
| 6303 | [value] | [value] | [value] | [value] | [value] | [value] | [value] |
| 6304 | [value] | [value] | [value] | [value] | [value] | [value] | [value] |
| 6305 | [value] | [value] | [value] | [value] | [value] | [value] | [value] |

## Body-family results

Publish all 24 family rows, including failures. Report regulation, exact, transfer,
interface, mapping, hidden final error, and every denominator. Families are nested task
instances, not independent organisms or human-style participants.

## Uncertainty

Report the frozen hierarchical seed-and-family bootstrap interval. Do not present a
trial-level interval that treats the 1,056 decisions as independent subjects. Describe
the six outer seeds as a development reliability sample, not a population estimate over
all prompts, models, providers, or synthetic bodies.

## Mechanistic limits

State that the full condition combines private state, feedback, persistent memory, a
wrapper-computed association summary, an explicit transfer bridge, and model action
selection. A full-condition result alone cannot determine which component caused the
performance. That question belongs to the separately frozen multi-condition cohort.

## Interpretation boundary

### Supported

- [observed behavioural performance]
- [audited computational setup]
- [observed reliability or unreliability across seeds and families]

### Not supported

- that the model felt the synthetic signal
- that it was aware, sentient, conscious, or capable of suffering
- that the benchmark is a validated consciousness detector
- that the result generalises to other models, providers, prompts, or body designs
- that wrapper-generated summaries reveal an intrinsic model self-representation

## Deviations and failures

Report every deviation, infrastructure failure, retry, and code change after the original
freeze. Link each replacement registration and preserved database. Distinguish changes
that affect future execution from changes that affected the analysed cohort.

## Next decision

Follow `docs/v10-post-result-decision-tree.md`. Do not choose the next experiment from a
more favourable interpretation of the observed values.
