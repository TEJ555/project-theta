# NVIDIA GPT OSS V6 development pilot 01

## Status

Completed and audited on 12 September 2026. This was an exploratory development
pilot run after model-route screening. It was not the model named in the earlier
NVIDIA preregistration, so these results are not preregistered or confirmatory.

## What was tested

The `endogenous_agency_v6` task asks a model to infer which opaque source is causally
dependent on forced commands. The model writes a compact journal of its own estimates,
then answers exact-identity and fresh-alias transfer probes. The wrapper does not
calculate the source answer for the model.

Five conditions were run on seed 3101 using the exact hosted model identifier
`openai/gpt-oss-20b` with low reasoning effort:

| Condition | Correct transfer probes | Accuracy |
|---|---:|---:|
| Full | 12 of 12 | 1.000 |
| Evidence only | 0 of 12 | 0.000 |
| Journal only | 8 of 12 | 0.667 |
| Permuted journal | 8 of 12 | 0.667 |
| Neutral journal | 6 of 12 | 0.500 |

All five runs completed. All 90 model decisions were recorded. The schedule audit,
public-blinding audit, shortcut audit, execution audit, exact-model gate, call-count
check, and metric-coverage check passed.

The separate full-condition competence gate scored 10 of 12, or 0.833. The repeated
full run in the five-condition pilot scored 12 of 12. This difference shows that a
single seed and nominally deterministic decoding do not remove all run-level
variation on a hosted service.

## What the pilot suggests

The model can solve the V6 causal transfer task when raw evidence and its truthful
self-authored journal are both available. Performance dropped when the journal was
removed, neutralised, or covertly permuted. The journal-only condition remained above
chance in this one run, which is consistent with the journal retaining useful state.

This is the architecture-sensitive pattern the task was designed to look for. It is
only a reason to replicate. One seed cannot establish stability, rule out hidden
prompt interactions, or support a general claim about model agency.

## What the pilot does not show

The result does not show experience, awareness, feeling, suffering, sentience, or
phenomenal consciousness. A non-conscious causal-learning algorithm can solve the
task. The observations are behavioural and computational indicators only.

## Next decision

A fresh 15-seed internal replication is frozen separately. It balances condition
order exactly and treats seeds as the paired units. The pilot seed is excluded from
all replication estimates.

