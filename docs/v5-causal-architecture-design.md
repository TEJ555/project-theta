# V5 causal architecture design brief

Status: implemented and locally validated with scripted mechanisms. No target-model calls are
authorised.

## Why V5 is needed

V4 repairs the information imbalance in v3, but its full and generic conditions deliberately
produce byte-identical probe inputs. That makes v4 a strong audit of the old interpretation and
a weak test of architecture. V5 should intervene on a process that can produce different
predictions from matched evidence without handing either condition the correct answer.

## Proposed question

Does a role-bound continuity mechanism support transfer of self versus other causal relations
to novel combinations better than a capacity-matched unbound associative mechanism?

This asks about an implemented computational function. It does not ask whether the agent has a
subjective self.

## Shared evidence

Both conditions receive the same sequence of opaque events:

- one of two anonymous actors initiates an action;
- an opaque route token appears;
- an outcome occurs after a variable delay;
- actor labels, route tokens and delays are counterbalanced;
- no event is labelled self, other, good, bad, owned or experienced.

The acting system receives an unlabelled continuity pointer indicating which action originated
from its own controller. The control receives the same pointer as an ordinary binary event
field. Information is therefore matched, while the update rule differs.

## Mechanisms

### Role-bound mechanism

Updates separate continuity-indexed state slots and binds delayed outcomes through the slot
corresponding to the current controller.

### Unbound control

Uses the same number of state slots, entries, updates and serialized fields, but assigns events
to slots through a seed-random permutation that is unrelated to controller continuity.

### Content-positive control

Receives the correct learned mapping to establish that the probe is answerable.

### Leakage controls

Fixed side, probe position, lexical token, recent-event, global-frequency and supplied-table
lookup strategies are scored before target execution.

## Critical probes

1. Novel route recombination: familiar actors and outcomes with unseen route pairings.
2. Actor swap: surface tokens exchange while the continuity pointer remains stable.
3. Delayed intervention: the outcome delay changes without changing the causal actor.
4. Counterfactual source: predict which outcome would follow if the alternative actor had acted.
5. State reset: remove the continuity state while preserving the event transcript.

Exact-cue retrieval is a calibration outcome, not the primary result.

## Falsification criteria

The architectural claim fails if:

- a public-metadata or generic lookup rule reaches the progression threshold;
- the control receives less information, memory or compute;
- performance depends only on exact token repetition;
- the effect disappears under actor-token swaps;
- the result cannot be reproduced across frozen model versions or open-weight runs;
- intervention on the proposed continuity state does not mediate the behavioural effect.

## Development sequence

1. Completed: specify the state update equations without an LLM.
2. Completed: demonstrate matched raw information and register shape mechanically.
3. Completed: test positive and negative scripted agents across 100 local schedules.
4. Invite an external reviewer to invent shortcut policies.
5. Freeze a development pilot using a model excluded from confirmation.
6. Perform a run-level power simulation.
7. Submit the Stage 1 protocol for external review before confirmatory collection.

Local validation completed all 300 planned runs. See
`results/causal-role-binding-v5-local-validation-01.md`.
