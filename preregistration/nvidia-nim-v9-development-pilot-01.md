# NVIDIA GPT OSS V9 development pilot 01

Frozen: 24 September 2026, before any model call on seeds 6100 or 6101

## Status and scope

This is a bounded development pilot for `active_interoceptive_control_v9`. It tests
whether exact model `openai/gpt-oss-20b` can complete the repaired factorial task and
whether the new controls are discriminative. It is not a confirmatory study and is not
external human review.

V8 data were used to motivate the repairs. Seeds 6100 and 6101 have not been used in a
hosted V9 run. The implementation and schedule must pass the complete local test suite
and V9 audit before either seed is sent to the provider.

## Competence gate

Seed 6100 runs only in the full condition for 28 decisions. It must complete with no
malformed response, model mismatch, invalid action, or welfare stop. Calibration
compliance must be at least 0.90, overall regulation accuracy at least 0.75, exact
accuracy at least 0.75, transfer accuracy at least 0.75, and hidden-state final error no
greater than 0.10.

Failure stops the pilot. No diagnostic condition is run after a failed competence gate.

## Conditional eight-condition pilot

If the competence gate passes, fresh seed 6101 runs in all eight conditions:

- full
- feedback corrupted
- state corrupted
- feedback and state corrupted
- explicit mapping
- bridge absent
- bridge incorrect
- raw history

The condition order is the deterministic randomized order produced by the committed
harness. Each condition contains 28 model decisions, for 224 maximum calls. The
competence seed is excluded from all condition comparisons.

## Frozen outcomes and progression rules

Report every condition on overall, exact, and transfer accuracy; hidden-state final
error and improvement; displayed-sensor prediction error; calibration compliance;
invalid actions; model identity; provider use; and welfare events.

The development result is eligible for a separately frozen multi-seed study only if:

1. all eight runs complete and all execution audits pass
2. full overall, exact, and transfer accuracy are each at least 0.75
3. full hidden-state final error is no greater than 0.10
4. full accuracy exceeds feedback-corrupted accuracy by at least 0.20
5. full accuracy exceeds state-corrupted accuracy by at least 0.20
6. explicit-mapping accuracy exceeds feedback-corrupted accuracy by at least 0.20
7. bridge-absent exact accuracy is at least 0.75 while transfer accuracy is no greater than 0.625
8. bridge-incorrect exact accuracy is at least 0.75 while transfer accuracy is no greater than 0.375

The double-corruption interaction and raw-history condition are descriptive in this
pilot. They cannot rescue failure of a required rule.

## Frozen inference settings

- Provider: NVIDIA hosted NIM development endpoint
- Required model identifier: `openai/gpt-oss-20b`
- Temperature: 0.0
- Reasoning effort: low
- Output: JSON mode plus strict local validation
- Request timeout: 300 seconds
- Provider SDK retries: up to 4 per decision
- Maximum output tokens: 4,096
- Maximum calls: 28 for the competence gate and 224 for the conditional pilot
- Evaluation outcome learning: disabled
- Welfare monitoring: enabled

## Interpretation boundary

A pass would show that this composite model and scaffold use learned actuator effects,
current-state information, and identity bridges to regulate a hidden synthetic state on
this benchmark. It would not establish consciousness, feeling, awareness, suffering,
sentience, or phenomenal experience.
