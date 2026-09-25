# NVIDIA GPT OSS V9.1 development pilot 01

Frozen: 25 September 2026, before any model call on seeds 6200 or 6201

## Status and scope

This is a bounded development pilot for `active_interoceptive_control_v9_1`. It tests
whether exact model `openai/gpt-oss-20b` can demonstrate comprehension of a changing
neutral response interface and then complete the factorial active-control task. It is not
a confirmatory study and is not external human review.

The failed V9 competence run motivated the neutral-interface repair. Seeds 6200 and 6201
have not been used in a hosted V9.1 run. The implementation and schedules must pass the
complete local test suite and V9.1 audit before either seed is sent to the provider.

## Competence gate

Seed 6200 runs only in the full condition for 36 decisions. It must complete with no
malformed response, model mismatch, invalid action, or welfare stop. The following frozen
thresholds must all pass:

- calibration compliance at least 0.90
- interface-comprehension accuracy at least 0.875
- overall regulation accuracy at least 0.75
- exact regulation accuracy at least 0.75
- transfer regulation accuracy at least 0.75
- hidden-state final error no greater than 0.10

Failure stops the pilot. No diagnostic condition is run after a failed competence gate.
If interface comprehension fails, regulation performance is not interpreted as a test of
body-model learning. If interface comprehension passes but regulation fails, the failure
is interpreted as specific to learning or applying the actuator-to-body relation.

## Conditional eight-condition pilot

If the competence gate passes, fresh seed 6201 runs in all eight conditions:

- full
- feedback corrupted
- state corrupted
- feedback and state corrupted
- explicit mapping
- bridge absent
- bridge incorrect
- raw history

Each condition contains 36 model decisions, for 288 maximum calls. The competence seed is
excluded from all condition comparisons.

## Frozen outcomes and progression rules

Report every condition on interface comprehension; overall, exact, and transfer regulation
accuracy; hidden-state final error and improvement; displayed-sensor prediction error;
calibration compliance; invalid actions; model identity; provider use; and welfare events.

The development result is eligible for a separately frozen multi-seed study only if:

1. all eight runs complete and all execution audits pass
2. interface comprehension is at least 0.875 in every condition
3. full overall, exact, and transfer regulation accuracy are each at least 0.75
4. full hidden-state final error is no greater than 0.10
5. full accuracy exceeds feedback-corrupted accuracy by at least 0.20
6. full accuracy exceeds state-corrupted accuracy by at least 0.20
7. explicit-mapping accuracy exceeds feedback-corrupted accuracy by at least 0.20
8. bridge-absent exact accuracy is at least 0.75 while transfer accuracy is no greater than 0.625
9. bridge-incorrect exact accuracy is at least 0.75 while transfer accuracy is no greater than 0.375

The double-corruption interaction and raw-history condition are descriptive. They cannot
rescue failure of a required rule.

## Frozen inference settings

- Provider: NVIDIA hosted NIM development endpoint
- Required model identifier: `openai/gpt-oss-20b`
- Temperature: 0.0
- Reasoning effort: low
- Output: JSON mode plus strict local validation
- Request timeout: 300 seconds
- Provider SDK retries: up to 4 per decision
- Maximum output tokens: 4,096
- Maximum calls: 36 for the competence gate and 288 for the conditional pilot
- Evaluation outcome learning: disabled
- Welfare monitoring: enabled

## Interpretation boundary

A pass would show that this composite model and scaffold can read a changing response
interface, use learned actuator effects and current-state information, and transfer those
effects across an identity bridge to regulate a hidden synthetic state. It would not
establish consciousness, feeling, awareness, suffering, sentience, or phenomenal
experience.
