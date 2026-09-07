# Causal role binding v5 diagnostic controls local validation 02

Status: frozen for scripted engineering validation only. No target-model execution is
authorised by this document.

## Frozen validation

- Seeds: integers 8200 through 8299 inclusive.
- Conditions: full, permuted continuity, register hidden and raw role memory hidden.
- Scripted adapter with probe-only inference.
- Maximum 400 runs and 4,800 scripted decision calls.
- The schedule and primary transfer outcome are unchanged from local validation 01.

## Expected diagnostic pattern

| Condition | Exact-route accuracy | Novel-transfer accuracy |
|---|---:|---:|
| Full | 1.00 | 1.00 |
| Permuted continuity | 1.00 | 0.00 |
| Register hidden | 0.50 | 0.50 |
| Raw role memory hidden | 1.00 | 1.00 |

Register entry count, update count, capacity, actor entry count and route entry count must be
identical across conditions. Every run must record 12 scripted calls and 48 skipped acquisition
calls.

This deterministic pattern validates the interventions. It is not a model result, an effect-size
estimate or evidence of phenomenal consciousness.
