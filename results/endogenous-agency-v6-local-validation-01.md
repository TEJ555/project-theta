# Endogenous agency V6 local validation 01

Completed: 10 September 2026

Validated code revision: `83dc48d57c3255e714f9620da1925fee04936bea`

## Outcome

The deterministic engineering validation completed 700 no-provider runs. All 500
primary runs and all 200 pooled-correlation negative-control runs completed. The
100-seed schedule audit and the 500-run execution audit passed.

Both validation databases recorded the clean committed revision above for every run.

This validates schedule construction, blinding, model-authored-state plumbing,
diagnostic conditions and baseline behaviour. It is not evidence from an evaluated
language model.

## Primary positive-control results

Each condition contained 100 seeds and 1,800 decisions.

| Condition | Authored state | Exact probes | Transfer probes |
|---|---:|---:|---:|
| Full | 1.000 | 1.000 | 1.000 |
| Evidence only | 1.000 | 1.000 | 1.000 |
| Journal only | 1.000 | 1.000 | 1.000 |
| Neutral journal | 1.000 | 1.000 | 1.000 |
| Permuted journal | 1.000 | 0.000 | 0.000 |

The scripted intervention-aware positive control can solve the task from raw forced
evidence, can transfer through fresh aliases, can use its own stored journal without
raw evidence, and predictably follows the wrong mapping when that journal is covertly
permuted.

Full, evidence-only, journal-only and neutral-journal performance are identical for
this deliberately capable positive control. The generic report therefore emits weak
control-separation warnings. Those warnings are expected here and do not represent a
model result. The conditions are intended to diagnose a model's strategy in the next
phase, not to force separation in the scripted solver.

## Pooled-correlation negative control

Across 200 fresh seeds, the strategy that ignores forced-versus-passive structure
scored:

- authored-state accuracy: 0.000;
- exact-probe accuracy: 0.500;
- transfer-probe accuracy: 0.500.

This confirms that simple pooled command correlation cannot solve V6. The best tested
public metadata strategy scored 0.507 across 2,400 held-out probes.

## What changed from V5

V6 does not expose the V5 target label or option-level answer vector. The evaluated
model participates during acquisition, estimates which opaque source depends on
forced commands, and writes the persistent state that later conditions retain, hide,
neutralise or permute. Fresh transfer probes use new aliases linked only by an identity
bridge.

## Next step

Run the frozen one-seed NVIDIA NIM development pilot in
`preregistration/nvidia-nim-v6-development-01.md`. If it completes without a new
shortcut or capability failure, inspect raw contexts and decisions before allocating
fresh seeds. A credible confirmatory-style analysis remains at least 24 fresh paired
seed blocks away and requires outside methods review.

## Interpretation boundary

These results concern software behaviour and computational mechanisms. They do not
show phenomenal consciousness, subjective feeling or sentience.
