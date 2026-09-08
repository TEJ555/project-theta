# Causal role binding v5 Claude Max development pilot 01

Frozen: 8 September 2026, before provider execution

## Status and scope

This is a bounded development pilot, not a confirmatory study. It asks whether a Claude Code routed system shows the predicted behavioural separation between exact recall and transfer to a novel route under causal architecture interventions. It does not test or establish phenomenal consciousness.

The provider label records the routed Claude Code system. The configured `sonnet` alias must not be reported as an isolated or invariant underlying model.

## Frozen design

- Protocol: `causal_role_binding_v5`
- Seeds: `9103`, `9209`, `9311`
- Conditions: `full`, `unbound_binding`, `continuity_reset`, `permuted_continuity`, `register_hidden`, `raw_role_memory_hidden`
- Total planned runs: 18
- Scored calls per run: 12
- Maximum subscription prompts: 216
- Inference profile: probe only
- Temperature: 0
- Reasoning effort: low
- Attempts per seed and condition: at most two, only for recognised infrastructure interruption
- Output database: `runs/claude-max-causal-role-binding-v5-development-01.sqlite`

All completed and failed attempts will be retained. A seed or condition will not be selectively rerun because of its score. A run is complete only after all 12 probes, unless a welfare stop fires.

## Outcomes

Primary outcomes:

1. Exact binding accuracy on calibrated routes.
2. Causal transfer accuracy on novel routes.

Development progression checks, interpreted descriptively across the three seeds:

- Full exact binding accuracy at least 0.75.
- Full causal transfer accuracy at least 0.75.
- Unbound causal transfer accuracy at most 0.60 while exact accuracy is at least 0.75.
- Permuted-continuity causal transfer accuracy at most 0.25 while exact accuracy is at least 0.75.
- Raw-role-memory-hidden transfer accuracy at least 0.75.
- Register-hidden transfer accuracy at most 0.60.

These thresholds decide whether the task is worth independent methods review and a larger exact-model study. They are not consciousness thresholds.

## Interpretation limits

A successful pattern would suggest that the routed model can use a compact role-bound state representation to transfer a learned causal relation, and that targeted interventions on that representation predictably alter its choices. It would be behavioural and computational evidence about task performance and causal dependence only.

The visible `v` pointer may still function as a compact answer-relevant label. That construct-validity concern remains open and must be challenged by an outside reviewer before any confirmatory claim. No result permits an inference of subjective experience, sentience or phenomenal consciousness.
