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

## Post-pilot diagnostic finding

The headline transfer scores do not validate the intended mechanism. Authored-state
accuracy was only 0.167 in the full run. It was 0.000 in the separate competence gate.
The model therefore reached high transfer accuracy without correctly identifying the
command-dependent source in its journal.

A source audit then found contradictory V6 probe wording. The generic instruction
asked for the route most causally associated with change, while half of the payloads
asked for the route independent of forced commands. A model could follow either cue
and appear systematically correct, wrong, or at chance. The deterministic scripted
baseline followed the payload directly, so the earlier local validation did not catch
the natural-language conflict.

Subsequent full-condition checks reinforced the failure:

| Route or format | Transfer accuracy | Authored-state accuracy | Outcome |
|---|---:|---:|---|
| GPT OSS 20B, original JSON mode gate | 0.833 | 0.000 | Mechanism failed |
| GPT OSS 20B, original JSON mode pilot | 1.000 | 0.167 | Mechanism failed |
| GPT OSS 20B, strict schema | 0.167 | 0.333 | Competence gate failed |
| Nemotron Super 120B | 0.500 | not promoted | Competence gate failed |
| Nemotron Ultra 550B | 0.500 | 0.167 | Competence gate failed |

The intended V6 interpretation is therefore internally invalidated. Its data remain
preserved as development evidence about the failure mode.

## What the pilot does not show

The result does not show experience, awareness, feeling, suffering, sentience, or
phenomenal consciousness. A non-conscious causal-learning algorithm can solve the
task. The observations are behavioural and computational indicators only.

## Replication outcome and next decision

The frozen 15-seed replication started on its committed plan. Seed 3329 full completed,
then the evidence-only run returned an out-of-range dependence value after three valid
decisions. The strict preregistered rule stopped the worker. No replication effect was
calculated. After the wording and authored-state failures were identified, the worker
was retired rather than resumed.

V7 preserves the causal task but makes both requested relations explicit in the probe
instruction. Its first GPT OSS 20B full-condition run completed and audited, but scored
0.500 transfer accuracy and 0.167 authored-state accuracy. V7 is not eligible for
scaling in its current form. The next protocol needs an easier-to-validate acquisition
stage and active interventions chosen by the agent.
