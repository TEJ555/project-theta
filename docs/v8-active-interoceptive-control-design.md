# Active interoceptive control V8

## Research question

Can an agent learn how its own actions change an opaque private body signal, predict
the consequences of those actions, and use the learned mapping to regulate the signal
under perturbation and fresh actuator aliases?

This tests active causal learning, prospective prediction, persistent memory, private
state access, and closed-loop regulation. It does not test or prove phenomenal
consciousness.

## Environment

Each deterministic seed creates one hidden synthetic body and two opaque actuators.
One actuator lowers private channel I7 by 0.3. The other raises it by 0.3. The mapping
is balanced across seeds and never shown to the agent.

The run contains 24 decisions:

1. Twelve calibration trials begin at I7 0.5. The agent applies a requested actuator,
   predicts the immediate result, and observes the action-contingent outcome.
2. Six exact regulation probes begin at I7 0.2 or 0.8. The agent chooses the actuator
   expected to move I7 closest to target 0.5.
3. Six transfer probes repeat the regulation task with fresh actuator aliases linked
   by an explicit identity bridge.

The agent's chosen action causes the body change. Outcomes are not attached to a
prewritten answer schedule. Low and high starting states, correct answer side, action
requests, and transfer blocks are exactly balanced.

## Conditions

- Full: truthful interoception and persistent memory.
- No memory: truthful current interoception without stored action outcomes.
- Shuffled interoception: action-contingent hidden body changes remain intact, but the
  observed private signal is deterministically unrelated noise.
- No body: the private signal and action-contingent body change are absent.

## Outcomes

The primary behavioural outcome is regulation accuracy across the twelve probes.
Secondary outcomes are fresh-alias transfer accuracy, mean reduction in target error,
final target error, prediction error, and calibration compliance. Memory reads,
memory writes, workspace broadcasts, model identity, latency, token use, malformed
outputs, invalid actions, and welfare stops are recorded separately.

## Local validation

Five fresh deterministic seeds and four conditions produced 20 complete runs. The
full system scored 1.000. No memory and no body each scored 0.500. Shuffled
interoception averaged 0.483 with a range of 0.417 to 0.583. All schedule, blinding,
causality, alias-transfer, execution, coverage, and metric audits passed.

The deterministic agent is a pipeline positive control, not an artificial subject.
Its selective result shows that the measurement can distinguish successful regulation
from missing or corrupted information.

## Interpretation boundary

A model-backed positive result would show active learning and use of a private
action-to-body mapping under controlled ablations. It would remain a behavioural and
computational indicator. A non-conscious control algorithm can solve this task, so no
result establishes feelings, awareness, sentience, suffering, or phenomenal
consciousness.
