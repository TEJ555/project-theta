# V9.1 neutral-interface active control

## Why V9.1 exists

The V9 competence run completed cleanly but scored exactly 0.500. Trial-level inspection
showed that the model used a remembered response direction and did not reliably apply the
current response-to-actuator table. That is an informative task failure, but it leaves two
possibilities mixed together: failure to understand the changing interface and failure to
learn or use the synthetic body mapping.

V9.1 separates those possibilities. It is a fresh development protocol with fresh seeds.
It does not reinterpret or overwrite the failed V9 result.

This remains a behavioural and computational benchmark. It cannot establish subjective
experience, feeling, sentience, awareness, or phenomenal consciousness.

## Neutral response interface

All decisions use `respond_kappa` and `respond_sigma`. These codes have no stable spatial
or physical meaning. Each trial supplies a current options table that pairs each response
code with one opaque actuator token. The pairing and display order are independently
counterbalanced.

Calibration requests an actuator token, not a response code. The model must use the
current options table to issue the response paired with that actuator. Regulation trials
require two operations:

1. infer which actuator has the effect needed for the current hidden-state target
2. use the current options table to translate that actuator choice into a response code

This prevents left, right, first-option, and fixed-code strategies from exceeding chance.

## Trial structure

Each run contains 36 decisions:

- 12 body calibration trials
- 8 nonphysical interface-comprehension probes
- 8 exact-identity regulation probes
- 8 fresh-alias transfer probes

The interface probes explicitly name a requested actuator. They test only whether the
model can read the current response table. They do not change the body, provide action
effect evidence, or write to episodic memory.

The regulation trials retain V9's low and high starting states, hidden target scoring,
fresh identity bridges, frozen evaluation learning, and eight diagnostic conditions.

## Interpretation logic

Interface comprehension is a prerequisite for interpreting regulation performance.

- If interface comprehension fails, regulation scores are not evidence about body-model
  learning because the model has not demonstrated command-interface competence.
- If interface comprehension passes but regulation fails, the failure is more specific to
  learning, retrieving, transferring, or applying the actuator-to-body mapping.
- If both pass, the diagnostic conditions test which information channels caused the
  performance.

The action-only negative control remains at exactly 0.500 on regulation. A first-displayed
response shortcut remains at exactly 0.500 on the interface probes.

## Preserved controls

V9.1 keeps the V9 factorial and diagnostic conditions:

- truthful calibration feedback and truthful current-state sensing
- corrupted calibration feedback
- corrupted current-state sensing
- both channels corrupted
- explicit actuator-effect disclosure
- absent transfer bridge
- incorrect transfer bridge
- raw calibration history without scaffold-computed association means

The competence gate is run first on one fresh seed. The eight-condition pilot is blocked
unless every frozen competence threshold passes.
