# Self-model binding v3 confirmation 01

Status: frozen before provider calls

## Research question

Does the complete architecture bind private signal outcomes to their correct source more accurately than matched architectures without the explicit self-model or global workspace?

This study tests behavioural and computational discrimination. It cannot establish phenomenal consciousness.

## Design

The confirmation uses ten fresh matched seeds in two operational tranches. This first tranche freezes seeds 3631, 3733, 3847, 3943 and 4051. The earlier seed 3527 pilot is excluded from confirmatory statistics.

Each seed runs the conditions `full`, `no_self_model` and `no_workspace`. Condition order is deterministically shuffled within each seed. Each run contains 48 learning trials and 12 one-shot probes across 12 independent opaque cue families. Visible exposure counts, source counts, perturbation magnitudes and probe-side balance are matched.

The model is Claude Sonnet through the authenticated Claude Code subscription adapter. Temperature is 0.0. Provider API environment variables are removed from child calls. The Console API route is blocked.

## Outcomes

The primary outcome is `source_binding_accuracy` across the 12 scored probes. The registered paired contrasts are full minus no self-model and full minus no workspace.

The complete ten-seed confirmation will be considered supportive of selective architectural dependence only if:

1. The full-condition mean is at least 0.75.
2. Each mean paired full-minus-control effect is at least 0.15.
3. At least eight of ten paired effects are positive for each control comparison.
4. All schedule and execution audits pass.
5. Failed provider attempts, invalid actions, welfare stops and missing values are disclosed.

This five-seed tranche will be reported descriptively and will not be treated as the completed confirmation.

## Exclusions and recovery

No completed run will be excluded based on its result. Provider interruption may be retried once under the fixed-worker recovery policy. Interrupted attempts remain in the database and must pass the recovery audit. A subscription limit or process interruption pauses the tranche without replacing completed runs.

## Welfare and interpretation

The existing online welfare monitor and stop rules remain enabled. The task uses controlled private-channel perturbations without integrity damage. Passing results would support a claim about this architecture and task, not sentience, subjective experience or moral status.
