# Independent reviewer checklist

This checklist is for a reviewer who has had no role in producing target-model results.
It is not satisfied by an internal or model-generated review.

## Independence

- Declare prior involvement, financial interests and relevant collaborations.
- Confirm that no Project Theta target-model v4 results were provided.
- State whether the review is paid and confirm that payment is not outcome-dependent.

## Reproduction

- Check out the frozen commit in a clean environment.
- Run the unit suite and the continuous-integration workflow.
- Run `python scripts/red_team_v4.py` with at least 200 fresh seeds.
- Record the operating system, Python version, commit and complete command output.

## Method checks

- Attempt to predict answer side from every model-visible field except the binding content.
- Verify that full and generic-table probe contexts are byte-identical.
- Verify that wrong-content controls preserve schema, entry count and inference budget.
- Check whether any hidden simulator annotation reaches the model through memory or logs.
- Treat seed, run and condition as the experimental units where appropriate. Do not treat
  twelve within-run probes as twelve independent agents.
- Challenge the chosen effect size, equivalence margin and sample-size calculation.
- Check that model routing, versions, sampling controls and failed calls are reported.
- Check that welfare monitoring remains active during acquisition when inference is skipped.

## Required conclusion

Classify each issue as blocking, important but non-blocking, or editorial. A passing review
means no obvious flaw was found after reasonable effort. It does not certify the experiment
as a detector of phenomenal consciousness.
