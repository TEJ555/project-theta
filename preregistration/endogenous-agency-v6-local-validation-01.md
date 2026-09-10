# Endogenous agency v6 local validation 01

Frozen: 8 September 2026, before the 100-seed validation

## Scope

This is deterministic engineering validation with no provider calls. It tests schedule construction, state plumbing, diagnostic controls and declared shortcut baselines. It cannot establish empirical model performance or phenomenal consciousness.

## Frozen design

- Protocol: `endogenous_agency_v6`
- Seeds: 2100 through 2199 inclusive
- Conditions: `full`, `evidence_only`, `journal_only`, `permuted_journal`, `neutral_journal`
- Runs: 500
- Decisions per run: 18
- Scripted intervention-aware positive control: 9,000 decisions
- Pooled-correlation negative control: 200 additional journal-only seeds, 2300 through 2499
- Provider calls: 0

## Required deterministic expectations

- Full exact and transfer accuracy: 1.000.
- Evidence-only exact and transfer accuracy: 1.000.
- Journal-only exact and transfer accuracy: 1.000.
- Neutral-journal exact and transfer accuracy: 1.000.
- Permuted-journal exact and transfer accuracy: 0.000 for the journal-following positive control.
- Authored-state accuracy: 1.000 for the intervention-aware control.
- Pooled-correlation journal-only exact, transfer and authored-state accuracy: 0.500, 0.500 and 0.000 respectively.
- All V6 schedule and shortcut audits pass.

Passing these expectations validates code paths only. A provider pilot will require a separate frozen plan and fresh seeds.
