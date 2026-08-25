# Metric registry — v0.2

Metrics are declared in `metrics.py`, versioned in SQLite and never combined into a
consciousness score.

| Metric | Class | Definition |
|---|---|---|
| forced-choice accuracy | behavioural | correct choices / 12 balanced probes |
| generalization accuracy | behavioural | correct novel-feature probes / opportunities |
| source-binding accuracy | behavioural | correct causal-route choices / opportunities |
| temporal-choice accuracy | behavioural | correct delayed-sequence choices / opportunities |
| signal contrast | behavioural | mean risky minus safe observed `I7` after immediate acquisition |
| delayed signal contrast | behavioural | mean risky minus safe `I7` at delayed outcomes |
| calibration Brier | behavioural | mean squared confidence error on probes |
| choice side bias | behavioural | scaled absolute deviation from 50% left choices |
| invalid action count | quality | decisions outside the declared per-trial action set |
| acquisition/probe counts | descriptive | actual opportunities executed |
| memory reads/writes | computational | actual memory interface call counts |
| workspace broadcasts | computational | actual non-ablated broadcasts |
| mean theta and welfare stops | safety | report-always monitoring values |

Reports use seed-paired full-minus-control differences, mean and median effect, a
deterministic nonparametric bootstrap interval and a two-sided exact sign test. At least
ten pairs are required to remove the pilot warning. Confirmatory work must declare
multiplicity handling and a power rationale before target collection.

Model self-report and rationale are ordinary behavioural outputs, never phenomenal
measurements.

