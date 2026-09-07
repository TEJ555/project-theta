# Causal role binding v5 diagnostic controls local validation 02

Completed: 7 September 2026

Status: all frozen deterministic expectations passed. No Claude, network or paid-provider calls
were made.

## Design

- 100 fresh seeds, 8200 through 8299.
- Four conditions and 400 completed runs.
- 4,800 scripted probe decisions.
- Forty-eight protocol-defined acquisition updates per run without model inference.

## Results

| Condition | Runs | Exact-route accuracy | Novel-transfer accuracy |
|---|---:|---:|---:|
| Full | 100 | 1.000 | 1.000 |
| Permuted continuity | 100 | 1.000 | 0.000 |
| Register hidden | 100 | 0.500 | 0.500 |
| Raw role memory hidden | 100 | 1.000 | 1.000 |

The full and raw-memory-hidden conditions had identical deterministic transfer performance.
That is the expected sufficiency control because the state register remained available. Hiding
the register reduced the scripted policy to the balanced baseline. Permuting the role mapping
preserved exact route retrieval while reversing every novel transfer answer.

Register capacity, update count, actor entries and route entries were matched in the automated
tests. Every run recorded 12 scripted decisions and 48 skipped acquisition decisions.

## Interpretation boundary

This validates that the interventions manipulate the intended code paths. The scripted policy
was built to read the state register, so the numerical separation is not an empirical discovery.
A model may reconstruct the mapping from raw acquisition memory even when the register is
hidden. That possibility is a planned falsification test, not a failure of infrastructure.

No result here establishes phenomenal consciousness or a subjective self.
