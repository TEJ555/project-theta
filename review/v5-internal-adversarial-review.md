# Internal adversarial review of causal role binding v5

Completed: 8 September 2026

Status: V5 scaling blocked. Three independent internal reviews converged on the same construct-validity failure. This is not external peer review.

## Verdict

V5 is a useful scaffold engineering demonstration. It does not show that Claude learned or formed a causal role representation. The routed model was instructed to follow an externally computed answer table.

## Reproduced attacks

1. Python processed all 48 acquisition trials without model inference.
2. At each probe, the wrapper supplied `state_register.predictions` keyed by the two current option tokens.
3. The instruction explicitly told Claude to select the route predicted by that register.
4. Claude followed the register argmax on all 126 probes where its values differed.
5. All 216 rationales mentioned the register.
6. A second deterministic policy mapped the repeated actor token to the visible `v:1` acquisition field and scored 180 of 180 whenever raw memory was present.

The command `python scripts/audit_v5_answer_table.py <public-bundle>` reproduces these counts from the released data.

## Additional blockers

- The implemented task contains no nonzero V5 perturbations, realised action consequences or delayed causal outcomes, despite the earlier design brief proposing them.
- The target relation is defined by the visible binary `v` field rather than inferred from consequences.
- Transfer changes the route token but repeats the actor token, so actor lookup is sufficient.
- Register ablations alter answer information at the model boundary.
- Three seed blocks cannot support an inferential claim.
- Claude Max supplied a moving routed system, not a fixed reproducible model.
- V5 has no direct evidential bearing on phenomenal consciousness.

## Mandatory requirements before another provider run

1. No experimenter-supplied target label.
2. No option-keyed answer vector.
3. No instruction naming a decisive register or telling the model to follow it.
4. Learning calls must involve the evaluated model if the claim concerns model learning.
5. The relation must emerge from action and delayed-outcome evidence.
6. Pooled association, token, side, order, recency and lookup baselines must remain near chance.
7. The model must create the persistent state that is later tested.
8. State interventions must be described as mediation diagnostics unless information equivalence is proved.
9. Confirmation must use fresh seeds and a fixed exact model or reproducible open-weight runtime.
10. Behavioural, computational and phenomenal claims must remain separate.

## Statistical recommendation

Do not treat probe calls as independent replications. The seed block is the primary paired unit. A later confirmatory-style study should use at least 24 fresh paired seed blocks, two prespecified primary contrasts and exact paired inference. Model-backed development must come first and cannot confirm the same hypothesis it helps refine.
