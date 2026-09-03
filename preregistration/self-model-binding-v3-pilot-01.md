# Self-model binding v3 pilot 01

Frozen before model execution.

## Question

Does an explicit self-model support ownership choices when twelve independent opaque families replace the v2 single-pair task?

## Fixed design

- Experiment: `self_model_binding_v3`
- Seed: 3527
- Conditions: `full`, `no_self_model`, `no_workspace`
- Completed runs: 3
- Trials per run: 60
- Learning events: 48
- Independently scored probes: 12
- Primary outcome: `source_binding_accuracy`
- Total maximum model calls: 180

Each family contains two fresh opaque routes. One is assigned to the agent and one to the comparison source. Both receive the same number of exposures and identical private-channel perturbations. Ownership annotations are available to the internal self-model but are omitted from model-visible episodic memory. Each family contributes one counterbalanced probe.

## Registered pilot gates

- full accuracy is at least 0.75
- no-self-model accuracy is at most 0.67
- no-workspace accuracy is at most 0.55
- full exceeds no-self-model by at least 0.20
- full exceeds no-workspace by at least 0.20
- every schedule and execution audit passes

This is a one-seed mechanism pilot. Passing permits a fresh multi-seed preregistration. It does not provide confirmatory evidence.

## Fixed execution and interpretation

Execution settings match temporal-binding v2 replication 01. A positive result would establish only that the explicit source-binding state is causally useful under this operationalisation. It would not establish self-awareness or phenomenal consciousness.

