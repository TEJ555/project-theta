# V10 multi-body reliability design

## Purpose

V10 asks whether active synthetic-body regulation is reliable across independently mapped
body families and fresh outer seeds. It follows the V9.1 result, where direct interface
comprehension was perfect but full-condition regulation changed from 0.938 on the
competence seed to 0.625 on the conditional-pilot seed.

V10 is not designed to produce a stronger headline by making the task easier. Each body
family retains V9.1's calibration quantity, neutral response remapping, exact probes,
fresh-alias transfer probes, hidden-state endpoint, and frozen evaluation learning.

## Sampling structure

Each run contains four independently generated body families. Every family has:

- a fresh opaque body identity
- two fresh calibration actuator identities
- an independently assigned increasing and decreasing actuator
- two fresh transfer aliases
- a family-local identity bridge
- independently remapped neutral response codes and display order

The four hidden actuator directions are exactly balanced within each seed. Tokens never
repeat across bodies or seeds. Transfer bridges never cross body boundaries.

The synthetic dynamics are standardized across families. Each scored trial begins from a
controlled state, as in V9.1. The independent sampling concerns the identity and causal
mapping that must be learned, not a claim that four persistent organisms exist.

## Trial structure

Each family contributes 44 decisions:

- 12 calibration trials
- 8 no-feedback body-mapping checkpoints
- 8 direct interface-comprehension probes
- 8 exact-identity regulation probes
- 8 fresh-alias transfer probes

A complete run therefore contains 176 decisions. Trials are shuffled across body families
within each phase. The phase order is calibration, mapping checkpoint, interface check,
exact regulation, and transfer regulation.

The mapping checkpoint directly asks which calibrated actuator increased or decreased I7.
It gives no correctness or outcome feedback and is not written to episodic memory. It
separates failure to retain the learned causal map from failure to apply the current state
or response interface.

## Reliability metrics

The primary regulation outcome remains accuracy across exact and transfer probes. V10 also
reports:

- regulation accuracy for every body family
- the fraction of body families scoring at least 0.625
- the lowest body-family regulation accuracy in each seed
- interface and mapping-checkpoint pass rates by family
- exact and transfer accuracy separately
- hidden-state final error and improvement
- seed-level means and a hierarchical seed-and-family bootstrap interval

No family is silently excluded for failing an interface or mapping checkpoint. Its
regulation result remains in the primary estimate and is labelled for interpretation.

## Why there is no single-seed gate

The V9.1 passing gate seed overstated performance on the next fresh seed. V10 therefore
freezes all six outer seeds in advance. All are attempted regardless of intermediate
scores. There is no replacement of an unfavourable seed and no score-dependent decision to
continue.

## Interpretation boundary

A V10 pass would support a narrow claim that the composite system can repeatedly learn and
use several private action-to-body mappings under controlled remapping and transfer. It
would still be compatible with non-conscious control and reasoning mechanisms. It would
not establish subjective experience or phenomenal consciousness.

## Execution recovery

Provider execution uses the fixed worker rather than the direct multi-run command. Each
seed and condition is an explicit job. A completed job is skipped on recovery, while an
interrupted attempt is preserved as failed and may be retried once from the beginning.
The worker blocks duplicate completions, non-retryable failures, a third attempt, an
unclean code revision, and recovery while an active lock exists.

Recovery never continues from the middle of a synthetic body sequence. The agent's live
memory and execution context cannot be reconstructed exactly from a partial database, so
the interrupted attempt remains evidence of an infrastructure failure and the affected
job restarts from trial zero.
