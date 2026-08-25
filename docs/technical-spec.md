# Technical specification

## Objective

Provide a small, reproducible platform for causal tests of theory-inspired functional
indicators in persistent agents. The platform must make negative controls easier than
post-hoc storytelling.

## Cycle

```text
hidden world ──external observation──┐
                                    ├─> candidate contents ─> workspace ─> adapter ─> action
hidden body ──private I7 signal──────┘          ↑                  │             │
                                               │                  v             v
                                        episodic memory <── self-model <── consequences
```

At tick *t*, the adapter sees only the partial observation, private signals,
capacity-limited broadcast, retrieved memory and self-model. It never sees hazard
coordinates, body variables, experiment scoring keys, or future random values. The
harness logs both visible context and hidden ground truth in separate fields.

## Reproducibility contract

- All simulated randomness derives from the declared integer seed.
- Counterbalancing (map reflection and source order) derives from seed parity.
- Python's process-randomized `hash()` is never used for experimental state.
- The full condition, model ID, temperature, adapter, schema version and prompt are
  preserved. Formal runs should add immutable provider snapshot/version metadata.
- Provider nondeterminism must be reported even at temperature zero.

## Interfaces

`ModelAdapter.decide(context) -> Decision` is the only generative-model boundary.
The `Decision` schema permits one action, rationale, next-I7 prediction, confidence,
operational self-report and conservative stop request. Invalid actions become `wait`;
provider errors fail the run and are never silently replaced by a baseline.

`EpisodicMemory`, `SelfModel`, and `GlobalWorkspace` expose small replaceable APIs.
Their ablations remove the mechanism rather than merely telling the model to ignore it.

## Threat model

Primary threats are prompt leakage, memorized human narratives, fixed spatial rules,
unmatched token/context budgets, adapter retry differences, experimenter degrees of
freedom, and selecting only models that “look conscious.” Mitigations include opaque
signal names, randomized causal mappings, held-out seeds/maps, matched contexts,
negative controls, preregistration and full reporting.

## Out of scope for v0.1

Neural activation access, mechanistic interpretability, learning model weights,
validated causal emergence or Phi measures, multi-agent theory of mind, rich physics,
biologically faithful affect, and claims about moral patienthood.

