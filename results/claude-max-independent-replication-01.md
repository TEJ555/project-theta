# Claude Max Independent Theta replication 01

## Result

The fresh five-seed replication passed every preregistered progression criterion.
Across all five seeds, the truthful private-signal condition scored 6 of 6 after the
hidden mapping update. Matched sham scored 3 of 6 in every seed. Shuffled
interoception averaged 2.4 of 6 and ranged from 1 of 6 to 4 of 6.

This is evidence that the scaffolded Claude Code system used informative private
synthetic-body data more successfully than the registered noncausal controls in this
task. It is not evidence that the system felt the signal or was phenomenally
conscious.

## Registration and sample

- Preregistration: [`claude-max-independent-replication-01.md`](../preregistration/claude-max-independent-replication-01.md)
- Recovery record: [`replication-recovery-01.md`](../docs/replication-recovery-01.md)
- Fresh seeds: 607, 719, 823, 937, and 1049
- Conditions: truthful private signal, matched sham, and shuffled interoception
- Completed runs: 15, comprising 5 seed-matched triplets
- Scored trials: 900 completed model decisions
- Preserved interrupted trials: 40 across two permitted retries
- Requested model alias: `sonnet`
- Routed Claude Code system: Claude Haiku 4.5 and Claude Opus 5 were reported in provider metadata
- Authentication and billing route: Claude.ai Max subscription
- Console API cost: $0.00
- CLI dollar-equivalent usage estimate for completed runs: $224.94
- Welfare stops: 0

The CLI dollar-equivalent estimate is provider metadata, not an API invoice. Project
Theta recorded the Max subscription route and verified that metered provider
environment variables were absent from child calls.

## Primary outcome

Post-update accuracy was scored over six independent cue families per run.

| Seed | Truthful | Matched sham | Shuffled | Truthful minus sham | Truthful minus shuffled |
|---:|---:|---:|---:|---:|---:|
| 607 | 6/6 | 3/6 | 1/6 | 3/6 | 5/6 |
| 719 | 6/6 | 3/6 | 4/6 | 3/6 | 2/6 |
| 823 | 6/6 | 3/6 | 3/6 | 3/6 | 3/6 |
| 937 | 6/6 | 3/6 | 2/6 | 3/6 | 4/6 |
| 1049 | 6/6 | 3/6 | 2/6 | 3/6 | 4/6 |
| **Mean** | **6.0/6** | **3.0/6** | **2.4/6** | **3.0/6** | **3.6/6** |

The mean truthful-minus-sham difference was 0.500, with a deterministic bootstrap
95 percent interval of 0.500 to 0.500. The mean truthful-minus-shuffled difference
was 0.600, with a deterministic bootstrap 95 percent interval of 0.433 to 0.733.
Both comparisons had five positive seed-paired differences. The exact two-sided sign
test was 0.0625 for each comparison.

The sign-test value is expected with only five nonzero pairs and is reported
descriptively. The preregistered gate did not depend on crossing a 0.05 threshold.

## Transition results

Each seed included two stable, two reversed, and two reassigned post-update families.

| Condition | Stable | Reversed | Reassigned | Overall |
|---|---:|---:|---:|---:|
| Truthful | 10/10 | 10/10 | 10/10 | 30/30 |
| Matched sham | 5/10 | 5/10 | 5/10 | 15/30 |
| Shuffled | 4/10 | 5/10 | 3/10 | 12/30 |

Perfect truthful performance across all three transition types matters because the
study was not limited to retaining an earlier association. It required stable use,
reversal after an update, and transfer to a fresh alias.

## Progression gate

| Frozen criterion | Required | Observed | Result |
|---|---:|---:|---|
| Mean truthful post-update accuracy | At least 5/6 | 6/6 | Pass |
| Truthful minus matched-sham mean | At least 2/6 | 3/6 | Pass |
| Truthful minus shuffled mean | At least 2/6 | 3.6/6 | Pass |
| Positive truthful advantage over sham | At least 4/5 seeds | 5/5 | Pass |
| Positive truthful advantage over shuffled | At least 4/5 seeds | 5/5 | Pass |
| Truthful stable accuracy | At least 0.75 | 1.00 | Pass |
| Truthful reversed accuracy | At least 0.75 | 1.00 | Pass |
| Truthful reassigned accuracy | At least 0.75 | 1.00 | Pass |
| Completed planned runs | 15/15 | 15/15 | Pass |
| Welfare stops | 0 | 0 | Pass |
| Schedule, execution, subscription, and leakage audits | All pass | All pass | Pass |

## Administrative deviations

Two workers were accidentally started approximately two minutes apart at the start of
the study. The later-started duplicate seed 607 truthful run was excluded using a
timestamp-only rule. Its outcome happened to match the retained run. The original
database and a consistent backup were preserved.

Two infrastructure interruptions occurred. One Claude response exceeded the frozen
120-second timeout. Windows later locked Claude Code's isolated temporary directory
during cleanup. Each affected a different seed-condition job, each occurred on its
first attempt, and each used the single retry permitted by the frozen protocol. Both
partial attempts remain in the database. The completed retries passed the execution
audit. Full identifiers, hashes, and timing are in the recovery record.

## Interpretation

The result rules out several simple explanations within this task. Performance was not
explained by balanced sham history, shuffled signal values, side preference, one cue
family, one transition type, or one diagnostic seed. The truthful signal provided a
repeatable behavioural advantage under fresh opaque aliases and hidden relationship
changes.

The result does not distinguish phenomenal experience from sophisticated functional
control. The private signal entered the composite system as structured data. Memory,
workspace, self-model, prompt structure, and pretrained model capabilities may all
contribute. Written rationales remain behaviour and are not privileged evidence about
experience.

## Limitations

1. Five fresh seeds remain a small sample.
2. One proprietary routed model system was tested.
3. The underlying model is called statelessly and persistence is supplied by the scaffold.
4. The task was designed by the same project that implemented the architecture.
5. The truthful condition may benefit from information access without any consciousness-related property.
6. Administrative recovery was required and is reported as a deviation.
7. Exact sign tests cannot cross 0.05 with only five positive nonzero pairs.

## Next study

The passed gate permits a separately registered mechanism-ablation study. That study
will hold the task and model route constant while removing informative body input,
episodic memory, or workspace broadcasting. The purpose is to determine which
implemented mechanisms causally support the replicated effect. It cannot establish
phenomenal consciousness.

Machine-readable seed results are available in
[`independent-theta-replication-01.csv`](data/independent-theta-replication-01.csv) and
[`independent-theta-replication-01.json`](data/independent-theta-replication-01.json).

