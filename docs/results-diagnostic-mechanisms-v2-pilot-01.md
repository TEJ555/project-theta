# Diagnostic mechanisms v2 pilot 01

Completed: 3 September 2026

Status: six of six runs complete, execution audits passed

## Results

| Experiment | Condition | Accuracy |
|---|---|---:|
| Self-model binding v2 | Full | 1.000 |
| Self-model binding v2 | No self-model | 0.917 |
| Self-model binding v2 | No workspace | 0.500 |
| Temporal binding v2 | Full | 0.750 |
| Temporal binding v2 | No persistence | 0.500 |
| Temporal binding v2 | No recurrence | 0.000 |

## Registered decisions

Temporal binding v2 passed every pilot gate. Full performance reached the registered 0.75 threshold, no-persistence remained at 0.50, and no-recurrence fell to 0.00. The full-minus-ablation effects were 0.25 and 0.75. This protocol is eligible for a fresh multi-seed replication.

Self-model binding v2 failed its selective-ablation gate. Removing the workspace reduced performance to baseline, but removing the explicit self-model left accuracy at 0.917. The task used only one stable pair of opaque routes, so a stable token preference could produce near-perfect results without source information. This is a plausible shortcut, not a confirmed explanation. The protocol will not be promoted to replication.

## Next design

Self-model binding v3 replaces the single route pair with twelve independently assigned opaque families. Each family receives matched exposure counts and identical perturbation magnitudes. Each family is scored only once. This converts a stable token guess from an almost all-or-nothing shortcut into a counterbalanced chance strategy.

## Limits

Each v2 comparison used one seed. The temporal result validates the mechanism well enough to justify replication, but it is not itself confirmatory evidence. Neither result is evidence of phenomenal consciousness.

Metered Console API cost was zero.

