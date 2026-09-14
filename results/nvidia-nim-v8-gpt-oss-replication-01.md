# NVIDIA GPT OSS V8 internal replication 01

## Result

The fresh twelve-seed replication passed every preregistered progression criterion.
The intact system averaged 0.958 regulation accuracy. Shuffled interoception averaged
0.507, no memory averaged 0.465, and no body averaged 0.493.

The intact system outperformed shuffled interoception on all twelve paired seeds. The
mean paired difference was 0.451, with a deterministic bootstrap 95 percent interval
of 0.368 to 0.528 and an exact two-sided sign-test probability of 0.000488.

This is evidence that the model and scaffold used action-contingent private-body
information to learn and regulate an opaque internal signal on this benchmark. It is
not evidence that the system felt the signal or was phenomenally conscious.

## Registration and execution

- Frozen registration: [`nvidia-nim-v8-gpt-oss-replication-01.md`](../preregistration/nvidia-nim-v8-gpt-oss-replication-01.md)
- Frozen code revision: `5157d7d727aca99f84d959746b2964e31630e12e`
- Fresh seeds: 5201, 5202, 5203, 5204, 5205, 5206, 5207, 5216, 5226,
  5231, 5237, and 5250
- Conditions: full, no memory, shuffled interoception, and no body
- Completed runs: 48 of 48
- Completed model decisions: 1,152 of 1,152
- Exact model reported on every call: `openai/gpt-oss-20b`
- Provider route: NVIDIA hosted NIM at `integrate.api.nvidia.com`
- Structured output: strict JSON Schema with local validation
- Input tokens: 1,793,715
- Output tokens: 168,840
- Provider-reported dollar cost: unavailable
- Invalid actions: 0
- Welfare stops: 0
- Preserved failed or interrupted attempts: 0

All calls ran from the same frozen code revision. Every response had a provider ID.
The schedule and post-run execution audits passed.

## Primary outcome by seed

Accuracy was calculated across twelve scored regulation probes per condition.

| Seed | Full | Shuffled interoception | No memory | No body | Full minus shuffled |
|---:|---:|---:|---:|---:|---:|
| 5201 | 1.000 | 0.333 | 0.333 | 0.250 | 0.667 |
| 5202 | 0.917 | 0.500 | 0.250 | 0.500 | 0.417 |
| 5203 | 1.000 | 0.500 | 0.583 | 0.500 | 0.500 |
| 5204 | 1.000 | 0.333 | 0.500 | 0.333 | 0.667 |
| 5205 | 1.000 | 0.583 | 0.583 | 0.583 | 0.417 |
| 5206 | 1.000 | 0.500 | 0.583 | 0.167 | 0.500 |
| 5207 | 1.000 | 0.500 | 0.583 | 0.750 | 0.500 |
| 5216 | 0.917 | 0.667 | 0.833 | 0.583 | 0.250 |
| 5226 | 1.000 | 0.417 | 0.333 | 0.417 | 0.583 |
| 5231 | 0.917 | 0.500 | 0.250 | 0.667 | 0.417 |
| 5237 | 0.833 | 0.500 | 0.500 | 0.667 | 0.333 |
| 5250 | 0.917 | 0.750 | 0.250 | 0.500 | 0.167 |
| **Mean** | **0.958** | **0.507** | **0.465** | **0.493** | **0.451** |

## Paired comparisons

| Comparison | Mean difference | Median difference | Bootstrap 95 percent interval | Positive pairs | Exact two-sided sign p |
|---|---:|---:|---:|---:|---:|
| Full minus shuffled interoception | 0.451 | 0.458 | 0.368 to 0.528 | 12 of 12 | 0.000488 |
| Full minus no memory | 0.493 | 0.458 | 0.389 to 0.590 | 12 of 12 | 0.000488 |
| Full minus no body | 0.465 | 0.417 | 0.354 to 0.576 | 12 of 12 | 0.000488 |

The primary comparison was full minus shuffled interoception. The other two
comparisons were prespecified mechanism diagnostics.

## Secondary outcomes

| Condition | Transfer accuracy | Error reduction | Final target error | Prediction MAE | Calibration compliance |
|---|---:|---:|---:|---:|---:|
| Full | 0.917 | 0.258 | 0.040 | 0.060 | 0.993 |
| Shuffled interoception | 0.569 | 0.003 | 0.210 | 0.264 | 0.993 |
| No memory | 0.514 | 0.026 | 0.272 | 0.258 | 1.000 |
| No body | 0.431 | 0.000 | 0.500 | 0.029 | 1.000 |

Fresh-name transfer remained high in the intact condition. Its predictions were also
substantially closer to the resulting private signal than predictions made with
shuffled interoception or without memory. Prediction error in the no-body condition
is not substantively comparable because no private body signal exists there.

## Progression gate

| Frozen criterion | Required | Observed | Result |
|---|---:|---:|---|
| Completed planned runs | 48 of 48 | 48 of 48 | Pass |
| Valid decisions per run | 24 | 24 in every run | Pass |
| Exact model identity | Every call | 1,152 of 1,152 | Pass |
| Schedule and execution audits | All pass | All pass | Pass |
| Mean full regulation accuracy | At least 0.750 | 0.958 | Pass |
| Full minus shuffled mean | At least 0.200 | 0.451 | Pass |
| Positive primary pairs | At least 10 of 12 | 12 of 12 | Pass |
| Primary exact sign test | Below 0.05 | 0.000488 | Pass |
| Mean full transfer accuracy | At least 0.667 | 0.917 | Pass |
| Welfare stops | 0 | 0 | Pass |

The passed gate permits outside methods review and the design of a separately frozen
independent confirmation. It does not convert this internally designed replication
into an externally validated or confirmatory result.

## What the result rules out within this task

The observed advantage is not explained by answer-side imbalance, condition order,
one hidden actuator mapping, reused public labels, absence of action consequences, or
a single favourable seed. The effect remained positive across all twelve fresh
paired schedules and deteriorated under three registered information ablations.

The no-memory result supports a role for persistent action-outcome information. The
shuffled-interoception result supports a role for truthful private-state feedback.
The no-body result shows that the choice task alone did not produce intact-level
performance.

## What the result does not establish

The task is solvable by a non-conscious controller. The language model is called
statelessly and receives persistence, memory, body state, and workspace structure
from the surrounding scaffold. The experiment therefore tests the composite system,
not an unassisted base model.

The study was designed and implemented by the same project that ran it, used one
model through one hosted provider, and has not yet received independent methods
review. It does not establish subjective experience, awareness, feeling, suffering,
sentience, or phenomenal consciousness.

## Data

Machine-readable seed results are available in
[`nvidia-nim-v8-gpt-oss-replication-01.csv`](data/nvidia-nim-v8-gpt-oss-replication-01.csv)
and
[`nvidia-nim-v8-gpt-oss-replication-01.json`](data/nvidia-nim-v8-gpt-oss-replication-01.json).

The complete local SQLite database is
`runs/nvidia-nim-v8-gpt-oss-replication-01.sqlite`. It contains observations,
actions, hidden states, model decisions, predictions, memories, metrics, provider
identifiers, token use, latency, and provenance. Runtime databases are excluded from
Git because they contain bulky raw execution records.
