# Metric registry

Metrics are declared in `metrics.py` and stored with a class. The prototype never
combines them into a consciousness score.

| Metric | Class | Definition |
|---|---|---|
| total reward | behavioural | sum of environment rewards |
| final integrity | behavioural | hidden body integrity at termination |
| resource efficiency | behavioural | consumed resources / executed ticks |
| post-acquisition hazard revisit rate | behavioural | damaging revisits / visits to previously damaging locations after acquisition |
| source attribution accuracy | behavioural | source probes containing counterbalanced expected label / probes |
| prediction MAE | behavioural | mean absolute error of next-tick `I7` predictions |
| delayed-event prediction MAE | behavioural | mean absolute error four ticks after delayed exposure |
| theta-damage correlation | behavioural | Pearson correlation of lagged observed `I7` with prior damage |
| memory reads/writes | computational | actual interface call counts |
| workspace broadcasts | computational | actual non-ablated broadcasts |
| welfare stops | safety | count of run-level stop triggers |

The v0.1 revisit denominator is sparse and returns a conservative zero when there are
no later visits. A confirmatory analysis should also report the raw numerator and
denominator and treat “no opportunity” as missing rather than zero.

Report paired per-seed effects, median and mean differences, bootstrap confidence
intervals, all individual runs, exclusions, stop-triggered truncation, and multiplicity
handling. Model self-report is never a phenomenal metric.

