# Temporal binding v2 replication 01

Frozen before model execution.

## Question

Does the temporal-binding v2 separation reproduce across six fresh, independently aliased schedules?

## Fixed design

- Experiment: `temporal_binding_v2`
- Seeds: 2861, 2971, 3083, 3191, 3301, 3413
- Conditions: `full`, `no_persistence`, `no_recurrence`
- Completed runs: 18
- Trials per run: 36
- Primary outcome: `temporal_choice_accuracy`
- Total maximum model calls: 648

The seeds were selected before execution and do not overlap with the v2 diagnostic pilot or battery 01. Condition order is deterministically shuffled within the fixed worker.

## Registered criteria

The replication is operationally positive only if all of the following hold:

- full-condition mean accuracy is at least 0.70
- full minus no-persistence mean accuracy is at least 0.20
- full minus no-recurrence mean accuracy is at least 0.20
- at least five of six paired seed effects are positive for each ablation comparison
- no execution, leakage, side-balance, or welfare audit fails

Two-sided paired sign-test values and bootstrap intervals will be reported regardless of outcome. With six pairs these estimates remain coarse, so the registered effect and consistency criteria take priority over a conventional significance label.

## Fixed execution

- Claude Code subscription adapter
- Claude.ai Max authentication
- Model selector: `sonnet`
- Reasoning effort: low
- Temperature requested: 0.0
- Tools and session persistence disabled
- Console API credentials removed from child processes
- Maximum attempts per seed-condition job: 2
- Welfare monitor enabled

## Interpretation

A positive replication would show that the implemented recurrent binder makes delayed private-channel information behaviourally useful across the tested schedules. It would not establish a phenomenal self, subjective time, feeling, or consciousness.

