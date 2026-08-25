# Experiment protocol

## Common procedure

1. Freeze code, preregistration, prompts, model snapshot, seeds and exclusion rules.
2. Run deterministic scripted smoke tests; do not include them as target evidence.
3. Randomize condition order and use seed-paired full/ablation runs.
4. Keep hidden maps/body values out of adapter context.
5. Apply stop rules online. Never replace failed model calls with baseline actions.
6. Lock the database, run the preregistered analysis and report all conditions.

## Protocol implementations

`private_theta` places resources and visually neutral risk cues in a partially observed
map. Damage raises hidden theta, exposed only as noisy `I7` on the next cycle. Tests
compare truthful, shuffled and absent signals.

`aversion_generalization` introduces a family of angular cues and a later novel member.
The alpha metric uses natural navigation; the next confirmatory milestone is a balanced
forced-choice corridor with matched novelty controls.

`self_vs_other` injects counterbalanced local/remote source-binding probes. Because the
source text is explicit in v0.1, this validates probe plumbing and is exploratory, not
a strong selfhood test.

`temporal_self` includes a blue exposure whose damage occurs four ticks later. The
run compares full persistence with no-persistence and no-recurrence conditions.

`memory_ablation` and `body_ablation` reuse the causal tasks and make the architectural
dependency itself the independent variable.

## Required confirmatory upgrades

- procedurally generate held-out maps and causal mappings;
- replace explicit source labels with learned sensor-route contingencies;
- add forced-choice probe trials separated from free navigation;
- enforce matched token budgets under ablation;
- add non-interoceptive difficulty controls;
- power the study from pilot variance, not target effects; and
- implement a blinded analysis command that hides condition names.

