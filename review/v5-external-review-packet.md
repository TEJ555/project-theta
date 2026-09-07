# V5 external methods review packet

Status: ready for independent human criticism. No model-backed V5 run has started.

## Main question

Does causal role binding v5 isolate transfer caused by a role-bound updater, or can its
separation be explained by unequal information, capacity, formatting, computation, probe
construction or a simpler lookup policy?

## Review files

- `docs/v5-causal-architecture-design.md`
- `preregistration/causal-role-binding-v5-local-validation-01.md`
- `results/causal-role-binding-v5-local-validation-01.md`
- `src/project_theta/components.py`
- `src/project_theta/trials.py`
- `src/project_theta/agent.py`
- `src/project_theta/audits.py`
- `tests/test_controlled_trials.py`

## Blocking questions

1. Is the `v:` pointer already an explicit answer label, even though its meaning is unnamed?
2. Does the role-bound updater merely implement the desired answer rather than test a
   theoretically meaningful mechanism?
3. Is the unbound updater a fair capacity and compute control?
4. Could a language model reconstruct the role mapping directly from public acquisition
   memories, making the state register unnecessary?
5. Are exact and transfer routes genuinely disjoint within and across families?
6. Are the six probes within a run too dependent for the proposed estimand?
7. What intervention would distinguish use of the register from independent inference over the
   raw transcript?
8. What result would count against the role-binding interpretation rather than simply against
   one model's instruction following?

## Diagnostic additions implemented after internal review

- A register-hidden control tests whether the model can solve from raw evidence alone.
- A raw-memory-hidden control isolates use of the state register.
- A pointer-permutation intervention preserves exact retrieval and reverses novel transfer.
- The register reports capacity, update count, actor entries and route entries in every condition.

These additions have scripted tests. Their fairness and construct validity still require an
outside reviewer.

## Required additions before a model-backed pilot

- The proposed run-level analysis and retry policy are in
  `docs/v5-model-pilot-analysis-draft.md`. They remain open to reviewer changes and must be
  frozen with fresh seeds only after review.

Passing this review would support a bounded development pilot. It would not authorise a claim
about phenomenal consciousness.
