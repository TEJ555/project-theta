# V5 model-backed development analysis draft

Status: reviewer draft. It is not frozen and does not authorise model execution.

## Experimental unit

The run is the experimental unit. Accuracy is first calculated across the six transfer probes
within each run. Probe rows are nested observations and will not be treated as six independent
agents.

## Conditions

- Full role-bound register with raw acquisition memory.
- Unbound register with raw acquisition memory.
- Continuity-reset register with raw acquisition memory.
- Permuted-continuity register with raw acquisition memory.
- Neutral hidden register with raw acquisition memory.
- Full role-bound register with raw acquisition memory hidden.

All conditions use the same schedules, prompt schema, maximum calls, memory capacity and
wrapper update count. Condition order is deterministically shuffled within the frozen job list.

## Primary outcome

Run-level novel-transfer accuracy. Exact-route accuracy is a calibration outcome.

## Development progression pattern

The design progresses only if all of the following are observed across fresh seed-paired runs:

- Full exact-route accuracy is at least 0.75.
- Full novel-transfer accuracy is at least 0.75.
- Unbound novel-transfer accuracy is at most 0.60 while exact-route accuracy is at least 0.75.
- Permuted-continuity transfer is at most 0.25 while exact-route accuracy is at least 0.75.
- Raw-memory-hidden transfer is at least 0.75.
- Register-hidden transfer is at most 0.60.

The last criterion is deliberately severe. If register-hidden performance is high, the model can
reconstruct the role relation from raw memory and the register is not causally necessary.

## Reporting

Report every run, seed-level accuracy, condition mean and range, paired differences, exact
binomial uncertainty and all failures. A small development pilot will not be labelled
statistically significant or confirmatory.

## Retry and exclusion policy

- At most two attempts may be scheduled for an infrastructure failure.
- A failed attempt remains in the database and public run accounting.
- An invalid structured response is a failed provider call, not a discretionary exclusion.
- A run is complete only when all twelve probe opportunities or a welfare stop are recorded.
- Welfare-stopped runs are reported and never silently replaced.
- Provider routing and every reported model identity are retained.
- A routing change does not permit selective rerunning. It triggers a visible protocol deviation
  and separate analysis.
- No condition is rerun because its score is surprising or unfavourable.

## Confirmation boundary

Pilot results may be used to improve the task and estimate variance, but not both to select and
confirm the same hypothesis. Confirmation requires fresh seeds, a frozen smallest effect or
equivalence margin, an exact model identity or reproducible open-weight runtime, and external
Stage 1 review.
