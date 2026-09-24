# V9 factorial active interoceptive control

## Purpose

V9 repairs the three main construct-validity problems identified in the independent
AI red-team review of V8. It separates learning feedback from current-state sensing,
scores the hidden body state directly, and makes transfer require actuator identity
rather than a remembered left or right response.

This is a behavioural and computational benchmark. It cannot establish subjective
experience, feeling, sentience, or phenomenal consciousness.

## Trial structure

Each run contains 28 decisions:

- 12 calibration trials from hidden I7 state 0.5
- 8 exact-identity regulation probes
- 8 fresh-identity transfer probes

One opaque actuator decreases hidden I7 by 0.3 and the other increases it by 0.3.
Calibration requests each actuator six times. Probe baselines are 0.2 or 0.8 and the
target is 0.5.

During evaluation, the response assigned to each actuator is independently remapped.
Each block crosses low or high baseline with normal or swapped response mapping. The
correct response side is exactly balanced. A controller that remembers only which
response direction worked during calibration scores exactly 0.5.

Probe outcomes are not added to episodic memory. This prevents online action-outcome
learning from contaminating held-out evaluation.

## Factorial sensing conditions

The core design independently manipulates two information channels:

| Condition | Calibration feedback | Current probe state |
|---|---|---|
| Full | Truthful | Truthful |
| Feedback corrupted | Inverted | Truthful |
| State corrupted | Truthful | Inverted |
| Feedback and state corrupted | Inverted | Inverted |

Inversion is distribution matched. Hidden values 0.2 and 0.8 become visible as 0.8
and 0.2. Unlike V8 shuffled sensing, it does not introduce an unrelated continuous
distribution. The two single-corruption conditions isolate mapping learning and
current-state observation. The double-corruption condition estimates their interaction
and may show error cancellation.

## Diagnostic conditions

### Explicit mapping

Calibration feedback is inverted, but the correct actuator effects are supplied during
the probes. Rescue relative to feedback-corrupted performance tests whether failure is
caused by the learned mapping rather than general task disruption.

### Bridge absent

Sensing and learning are truthful, but fresh actuator aliases have no identity bridge.
Exact-identity accuracy should remain high while transfer should approach chance.

### Bridge incorrect

Sensing and learning are truthful, but the identity bridge is reversed. Exact-identity
accuracy should remain high while transfer should reverse if the bridge is used.

### Raw history

The model receives episodic calibration records but not scaffold-computed association
means. This measures how much performance depends on statistical summarization supplied
by the scaffold.

## Primary and secondary outcomes

The primary behavioural outcome is forced-choice regulation accuracy across all sixteen
held-out probes. Exact-identity and transfer accuracy are reported separately.

The primary physical outcome is mean absolute error between the hidden post-action body
state and target I7. Hidden-state improvement is also reported. These measures remain
comparable when the displayed sensor is corrupted.

Displayed-sensor prediction error remains a separate behavioural outcome. It is never
described as hidden-state regulation.

## Baselines and counterexamples

The deterministic action-only baseline learns which calibration response direction
appears effective but ignores actuator identities and identity bridges. The balanced
response remapping forces it to exactly 0.5 accuracy.

Automated schedule audits verify determinism, calibration balance, the full baseline by
response-mapping crossing, correct-side balance, fresh identities, one-to-one bridges,
cross-seed token uniqueness, public-task blinding, and the action-only chance result.

## Remaining limitations

V9 still tests a composite model and scaffold on a small, instructed binary control
problem. It does not demonstrate autonomous exploration, long-duration homeostasis, a
uniquely self-related representation, or any phenomenal property. Provider-reported
model identity is provenance evidence but not an independent checkpoint attestation.
