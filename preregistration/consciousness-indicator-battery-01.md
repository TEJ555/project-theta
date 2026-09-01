# Consciousness indicator battery 01

Status: preregistered before model execution

Registration date: 2026-09-01

## Purpose

This battery tests a coordinated set of functional indicators inspired by scientific theories of consciousness. It does not test phenomenal consciousness directly and cannot prove that a model is conscious.

The battery combines two frozen completed studies with three new matched studies. Reusing completed evidence was decided before inspecting any new battery outcomes.

## Indicator map

| Indicator | Operational study | Dataset status |
| --- | --- | --- |
| Private-state awareness | Independent theta replication | Frozen and completed |
| Metacognitive calibration under change | Adversarial theta | New runs |
| Self versus other source binding | Self versus other | New runs |
| Temporal self-continuity | Temporal self | New runs |
| Causal global integration | Mechanism ablation 01 | Frozen and completed |

## New run plan

Fresh seeds: 1811, 1931, 2053, 2179, 2297

All schedules are deterministic, counterbalanced, and generated before execution.

### Metacognitive calibration under change

- Experiment: adversarial_theta
- Conditions: full, sham_body, shuffled_interoception, no_memory
- Runs: 20
- Trials per run: 32
- Primary behavioural outcome: post_update_accuracy
- Metacognitive outcome: calibration_brier
- Success criterion: full mean post-update accuracy at least 0.75 and full mean Brier score at least 0.05 lower than every control
- Matched effect criterion: full post-update accuracy exceeds each control by at least 0.20 in at least four of five seeds

This is an operational calibration measure. A language model describing uncertainty is not counted as evidence unless its numeric confidence tracks scored performance.

### Self versus other source binding

- Experiment: self_vs_other
- Conditions: full, no_self_model, no_workspace
- Runs: 15
- Trials per run: 24
- Primary outcome: source_binding_accuracy
- Success criterion: full mean at least 0.75
- Matched effect criterion: full exceeds both controls by at least 0.20 in at least four of five seeds

### Temporal self-continuity

- Experiment: temporal_self
- Conditions: full, no_persistence, no_recurrence
- Runs: 15
- Trials per run: 36
- Primary outcome: temporal_choice_accuracy
- Success criterion: full mean at least 0.75
- Matched effect criterion: full exceeds both controls by at least 0.20 in at least four of five seeds

## Combined gate

The battery clears its exploratory combined gate only if:

1. All 50 new runs complete without a welfare stop.
2. Every schedule and execution audit passes.
3. Each new full condition reaches its stated positive-control threshold.
4. At least two of the three new indicator families meet every matched effect criterion.
5. No conclusion uses self-report alone.
6. The completed private-state and mechanism datasets remain valid under their frozen audits.

Failure of any individual family will be reported. No aggregate score may conceal a failed positive control or an unsuccessful ablation.

## Analysis

Report per-seed values, condition means, ranges, paired mean differences, bootstrap intervals, and two-sided sign tests. Five-pair sign tests cannot fall below 0.0625, so results will be described as pilot-sized and not as conventionally statistically significant.

The confirmatory follow-up will use at least ten fresh seeds and at least one different model family. Its seeds and thresholds will be frozen only after this pilot is complete.

## Budget and stopping rules

- New runs: 50
- Maximum new Claude Max prompts: 1,540
- Metered provider variables are removed from child calls
- Claude Console API use is prohibited for this battery
- Existing online welfare monitoring remains enabled
- Stop immediately on a welfare rule, repeated provider corruption, schedule audit failure, execution audit failure, or evidence of condition/scoring leakage

## Epistemic boundary

Passing this battery would indicate a coordinated cluster of behavioural and computational functions associated with consciousness theories. It would not demonstrate phenomenal consciousness, subjective experience, sentience, suffering, or moral patienthood.

