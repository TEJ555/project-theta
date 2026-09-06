# External methods review packet

Status: ready for a human reviewer. No reviewer has been contacted.

## Review question

Can any condition in self-model binding v4 be solved through public ordering, option position, token form, context length, supplied labels or another shortcut that bypasses the intended information-matched comparison?

## Files to inspect

- `docs/methods-correction-2026-09-06.md`
- `preregistration/self-model-binding-v4-development-01.md`
- `src/project_theta/trials.py`
- `src/project_theta/agent.py`
- `src/project_theta/audits.py`
- `tests/test_controlled_trials.py`

## Requested checks

1. Reproduce the schedule audit across at least 200 fresh local seeds.
2. Invent additional metadata-only and deterministic lookup strategies.
3. Verify that full and generic conditions receive byte-identical probe contexts.
4. Check whether wrong-content controls preserve context structure, amount of information and compute.
5. Challenge the primary outcome and proposed seed-level analysis.
6. Identify any dependence between within-run probes that rules out item-level inference.
7. Confirm that the probe-only pathway does not remove a welfare opportunity or state transition relevant to the research question.
8. Recommend a sample-size method before any confirmatory registration.

## Success criterion

The protocol is ready for confirmation only when an outside reviewer can reproduce the local validation and cannot identify an obvious information-access or scheduling shortcut. Reviewer disagreements and unresolved issues will be published.
