# Self-model binding v4 no-provider red-team

Date: 6 September 2026

Status: passed the declared local checks. No Claude or paid-provider calls were made.

## Scope

The audit generated 400 fresh deterministic schedules using seeds 10000 through 10399.
Public-metadata rules were fitted on the first 200 schedules and evaluated only on the
remaining 200 schedules, containing 2,400 held-out probes.

The audit also ran full, generic-table, misattributed-table and permuted-table scripted
conditions on five fresh seeds.

## Results

- Best held-out public-metadata rule: character position 3 lexical comparison.
- Best held-out accuracy: 0.5275.
- Progression ceiling: 0.60.
- Old index-plus-seed parity diagnostic: 0.5050.
- Fixed-left and fixed-right accuracy: 0.5000 each.
- Learned probe-position accuracy: 0.5125.
- Forbidden model-visible fields found: none.
- Full and generic probe contexts: byte-identical for all five checked seeds.
- Full scripted accuracy: 1.000 for all five seeds.
- Generic-table scripted accuracy: 1.000 for all five seeds.
- Misattributed-table scripted accuracy: 0.000 for all five seeds.
- Probe-only accounting: 12 model calls and 48 skipped acquisition calls per run.

Permuted-table accuracy ranged from 0.0833 to 0.5833. This is expected to vary because a
permutation may preserve some bindings by chance.

## Interpretation

The repaired schedule defeats the tested public-order, fixed-side, lexical, character,
checksum and token rules on held-out schedules. This does not prove that every possible
shortcut has been removed. It establishes a reproducible red-team baseline for an outside
reviewer to extend.

Full and generic equality is an information-equivalence result. It is not evidence that a
specialised self-model has a causal behavioural effect. These measurements are behavioural
and computational indicators only and do not establish phenomenal consciousness.
