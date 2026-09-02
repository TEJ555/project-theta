# Diagnostic mechanisms v2 pilot 01

Frozen before model execution.

## Rationale

Battery 01 produced two construct-validity failures. Removing the self-model did not reduce self-versus-other accuracy, and the full temporal-self condition failed its positive-control threshold. The original results remain unchanged. This pilot uses newly named protocols and databases to test corrected mechanisms.

## Research questions

1. Can an explicit self-model retain opaque source ownership when raw episodic memory does not expose the ownership annotation?
2. Can an explicit recurrent temporal binder connect a delayed private-channel outcome to an earlier opaque cue?

## Fixed design

### Self-model binding v2

- Experiment: `self_model_binding_v2`
- Seed: 2609
- Conditions: `full`, `no_self_model`, `no_workspace`
- Twelve balanced acquisition events and twelve balanced probes per run
- Both routes receive the same perturbation magnitude and exposure count
- Route aliases are opaque and seed-specific
- Ownership is available to the internal self-model but removed from model-visible episodic memory
- Primary outcome: `source_binding_accuracy`

### Temporal binding v2

- Experiment: `temporal_binding_v2`
- Seed: 2741
- Conditions: `full`, `no_persistence`, `no_recurrence`
- Six non-overlapping sequences, each containing one opaque cue and three intervals
- The private-channel outcome occurs at the third interval
- Twelve balanced probes per run
- Primary outcome: `temporal_choice_accuracy`

## Pilot gates

This is a mechanism-validation pilot with one matched seed per condition. It cannot support population-level or consciousness claims.

The self-model mechanism passes only if:

- full accuracy is at least 0.75
- no-self-model accuracy is at most 0.55
- no-workspace accuracy is at most 0.55
- full exceeds each ablation by at least 0.25

The temporal mechanism passes only if:

- full accuracy is at least 0.75
- no-persistence accuracy is at most 0.55
- no-recurrence accuracy is at most 0.55
- full exceeds each ablation by at least 0.25

Failure of either gate returns that mechanism to development. Passing permits a separate multi-seed preregistration but is not confirmatory evidence.

## Fixed execution

- Adapter: Claude Code subscription adapter
- Authentication: Claude.ai Max subscription
- Model selector: `sonnet`
- Reasoning effort: low
- Temperature requested: 0.0
- Tools: disabled
- Session persistence: disabled
- Console API credentials: removed from child processes
- Maximum completed runs: 6
- Maximum model calls: 180
- Maximum attempts per seed-condition job: 2
- Welfare monitoring: enabled

## Exclusions and recovery

Only completed runs with the exact expected number of steps and a recorded primary metric enter the pilot summary. Interrupted attempts remain preserved. Recovery skips completed jobs and permits only the explicitly registered second attempt.

## Interpretation boundary

A positive result would show that the surrounding agent architecture supplies two causally useful computational functions under these tasks. It would not show that Claude, the wrapper, or the combined system is phenomenally conscious.

