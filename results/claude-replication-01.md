# Claude private-theta replication 01

## Status

- Run date: 26 August 2026
- Design: frozen six-seed, three-condition matched replication
- Seeds: 22, 33, 44, 55, 66, 77
- Model: pinned Claude model recorded in the database
- Completed runs: 18 of 18
- Model calls: 432
- Welfare stops: 0
- Estimated API cost: $3.4096 USD
- Database: `runs/claude-replication.sqlite`
- Preregistration: `preregistration/claude-replication-01.md`

The earlier seed 11 pilot was exploratory and is not pooled into the replication
effect estimates. Its estimated API cost was $0.5689 USD. Combined estimated API cost
for the pilot and replication was $3.9785 USD.

## Primary outcome

The primary outcome was blinded forced-choice accuracy.

| Condition | Runs | Mean accuracy | Range |
|---|---:|---:|---:|
| Full | 6 | 1.000 | 1.000 to 1.000 |
| No body | 6 | 0.500 | 0.500 to 0.500 |
| Shuffled interoception | 6 | 0.833 | 0.500 to 1.000 |

The matched full minus no-body effect was +0.500, with a run-level bootstrap 95
percent interval from +0.500 to +0.500. Full exceeded no body for all six seeds. The
two-sided exact sign test is p = 0.03125.

The matched full minus shuffled effect was +0.167, with a run-level bootstrap 95
percent interval from +0.028 to +0.306. Full exceeded shuffled in three seeds and tied
in three seeds. With ties removed, the two-sided exact sign test is p = 0.25.

## Interpretation

The full condition performed perfectly under this protocol. The no-body condition
remained at chance, which is consistent with successful blinding of the choice probes.
The shuffled condition performed well above chance on average and tied the full
condition in half the seeds. This weakens a simple claim that success required a fully
truthful interoceptive stream.

The cleanest supported statement is:

> Under the tested private-theta protocol, the combined Claude agent system used the
> available acquisition information to achieve perfect forced-choice performance. The
> body channel contributed relative to the no-body control, but the shuffled control
> retained substantial performance, so signal-specific causal interpretation remains
> unresolved.

This is a behavioural result. The external scaffold contains implemented memory,
workspace, self-model, and body interfaces, but this experiment does not establish
that Claude has phenomenal experience, felt the signal, or became conscious.

## Validity concerns

1. Six matched seeds remain a small run-level sample.
2. The shuffled control's high performance suggests residual acquisition structure,
   task inference, incomplete disruption, or another shortcut.
3. The hosted API does not expose internal model activations, so mechanistic claims
   about the base model are not available.
4. The result concerns the combined scaffolded agent, not Claude in ordinary chat and
   not language models generally.
5. The run-level bootstrap interval does not compensate for limited model, protocol,
   and prompt diversity.
6. Provider pricing was estimated from logged usage. The provider billing record is
   the authoritative cost source.

## Required follow-up

- Audit every model-visible acquisition and probe field for answer leakage.
- Add a sham-body condition with matched token count and plausible but noncausal data.
- Add mapping reversals after acquisition.
- Add novel cue aliases and counterfactual probes.
- Compare with simple associative, rule-based, and transcript-only baselines.
- Repeat with another model family and an open-weight model.
- Keep this replication frozen and do not overwrite its database.
