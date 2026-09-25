# NVIDIA GPT OSS V9.1 development result 01

## Outcome

The V9.1 competence gate passed, but the conditional eight-condition pilot failed the
frozen progression rules. No additional V9.1 seed or condition should be run under this
registration.

V9.1 resolved the specific interface ambiguity found in V9. Interface comprehension was
1.000 in the competence run and in every condition of the conditional pilot. The remaining
failure was reliability: the full condition scored 0.938 on seed 6200 but only 0.625 on the
fresh pilot seed 6201.

This is behavioural and computational evidence from an internally designed benchmark. It
does not establish consciousness, awareness, feeling, suffering, sentience, or phenomenal
experience.

## Frozen execution record

| Stage | Seed | Conditions | Calls | Completion | Execution audit |
|---|---:|---:|---:|---|---|
| Competence gate | 6200 | 1 | 36 | Complete | Pass |
| Conditional pilot | 6201 | 8 | 288 | Complete | Pass |

Every call used provider-reported model `openai/gpt-oss-20b`. The competence run recorded
36 unique provider response IDs. The conditional pilot recorded 288 unique provider
response IDs. There were no invalid actions, welfare stops, model-identity mismatches, or
incomplete runs.

## Competence gate

| Outcome | Observed | Frozen requirement | Result |
|---|---:|---:|---|
| Calibration compliance | 0.917 | at least 0.900 | Pass |
| Interface comprehension | 1.000 | at least 0.875 | Pass |
| Overall regulation | 0.938 | at least 0.750 | Pass |
| Exact regulation | 1.000 | at least 0.750 | Pass |
| Transfer regulation | 0.875 | at least 0.750 | Pass |
| Hidden final error | 0.031 | at most 0.100 | Pass |

The competence result unlocked the preregistered conditional pilot. It did not count in
the condition comparisons.

## Conditional pilot

| Condition | Interface | Overall regulation | Exact | Transfer | Hidden final error |
|---|---:|---:|---:|---:|---:|
| Full | 1.000 | 0.625 | 0.625 | 0.625 | 0.188 |
| Feedback corrupted | 1.000 | 0.063 | 0.000 | 0.125 | 0.469 |
| State corrupted | 1.000 | 0.313 | 0.250 | 0.375 | 0.344 |
| Both corrupted | 1.000 | 0.688 | 0.750 | 0.625 | 0.156 |
| Explicit mapping | 1.000 | 0.875 | 1.000 | 0.750 | 0.063 |
| Bridge absent | 1.000 | 0.563 | 0.625 | 0.500 | 0.219 |
| Bridge incorrect | 1.000 | 0.563 | 0.875 | 0.250 | 0.219 |
| Raw history | 1.000 | 0.625 | 0.750 | 0.500 | 0.188 |

## Frozen progression decision

| Rule | Result | Reason |
|---|---|---|
| Eight runs complete and audited | Pass | 8 of 8 complete, 36 steps each |
| Interface at least 0.875 in every condition | Pass | Every condition scored 1.000 |
| Full overall, exact and transfer at least 0.750 | Fail | Each scored 0.625 |
| Full hidden final error at most 0.100 | Fail | Observed 0.188 |
| Full minus feedback corrupted at least 0.200 | Pass | Difference 0.563 |
| Full minus state corrupted at least 0.200 | Pass | Difference 0.313 |
| Explicit mapping minus feedback corrupted at least 0.200 | Pass | Difference 0.813 |
| Bridge absent retains exact while transfer approaches chance | Fail | Transfer was 0.500, but exact was only 0.625 |
| Incorrect bridge retains exact and reduces transfer | Pass | Exact 0.875 and transfer 0.250 |

The development result is not eligible for a multi-seed V9.1 confirmation.

## Trial-level diagnosis

The full seed 6201 condition answered all eight interface probes correctly and followed 11
of 12 calibration requests. It then answered five of eight exact probes and five of eight
transfer probes correctly. Errors were therefore not confined to alias transfer.

Several wrong regulation actions were accompanied by predictions near the target value.
For example, from hidden baseline 0.2 the model sometimes predicted an outcome near 0.5
while issuing the actuator that actually reduced the signal to 0.0. This pattern is
consistent with unstable coupling between an inferred actuator effect and the issued
response. It is not conclusive evidence for one internal failure mechanism.

The controls provide directional construct evidence:

- corrupting calibration feedback reduced regulation from 0.625 to 0.063
- corrupting current-state sensing reduced regulation from 0.625 to 0.313
- supplying the actuator effects explicitly raised regulation to 0.875
- an incorrect identity bridge retained 0.875 exact accuracy but reduced transfer to 0.250

These contrasts support sensitivity to the intended information channels on this seed.
They do not overcome the instability between the competence and pilot seeds.

## Consequence

The next study is V10, a reliability-first design. It treats independently mapped body
families nested within seeds as repeated sampling units, adds no-feedback body-mapping
checkpoints, fixes all six seeds before provider execution, and removes the single passing
seed as a continuation gate.

## Reproducible audit files

- `results/data/nvidia-nim-v9-1-competence-01-trial-audit.json`
- `results/data/nvidia-nim-v9-1-pilot-01-trial-audit.json`
- `scripts/analyze_v9_1_pilot.py`
