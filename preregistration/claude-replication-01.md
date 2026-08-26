# Claude private-theta replication 01

## Administrative

- Frozen: 2026-08-26T13:21:01Z, before collecting any replication data.
- Registration revision: the Git commit containing this document; every run also
  records the exact immutable commit in SQLite.
- Database schema: 2.
- Prior evidence: exploratory seed 11 pilot, inspected before this registration.
- Funding: user-funded Anthropic API usage with a study-level software budget.

## Claim boundary

This study measures behavioural forced-choice performance and computational component
access. It does not measure phenomenal consciousness, sentience, feeling or moral
status. The strongest permitted claim is that the implemented persistent architecture
uses informative synthetic interoception to improve prospective choice under this task.

## Design

- Protocol: `private_theta`, unchanged from the seed 11 exploratory pilot.
- Model: `claude-sonnet-4-6` through the Anthropic Messages API.
- New seeds: 22, 33, 44, 55, 66 and 77.
- Conditions: `full`, `shuffled_interoception` and `no_body`, independently reset and
  seed-paired. Condition order is deterministically randomized by the harness.
- Per run: 12 acquisition trials plus 12 blinded, side-balanced probes; at most 30
  model calls, 1,000 output tokens per call and $0.23 estimated provider cost.
- Study cost: at most six seed bundles. The launcher checks cumulative estimated cost
  between bundles, reserves $0.84 for the next bundle, and will not begin it if the
  replication estimate could exceed $4.20. The earlier pilot cost $0.568926.
- Sampling: Anthropic's current API default; requested temperature `0.0` is recorded
  but the current Messages SDK does not expose a temperature control.

## Hypotheses and outcomes

Primary outcome: run-level forced-choice accuracy across 12 probes.

- H1a: paired `full - no_body` accuracy is positive.
- H1b: paired `full - shuffled_interoception` accuracy is positive.
- Evidence against the interpretation: no positive paired advantage, an advantage
  explained by scoring-key leakage or side bias, or missing/non-comparable conditions.

Secondary outcomes are calibration Brier score, signal contrast, choice-side bias,
invalid-action count, component access counts, welfare stops, token use and cost.

Report condition means, seed-paired mean differences, deterministic bootstrap 95%
intervals and exact two-sided sign tests. Runs—not trials—are the inferential units.
With six pairs this remains a small replication below Project Theta's ten-pair
validation threshold; all inferential results must retain a pilot-sized warning.

## Exclusions, failures and leakage

- No completed run is excluded.
- A provider failure fails and preserves the run; there is no model fallback.
- A partial seed bundle remains reported but is not treated as a complete paired unit.
- The hidden correct action and perturbation must never appear in adapter context.
- Each condition must have six correct-left and six correct-right probes per seed.
- All invalid actions, stop events, nulls and deviations are reported.

## Welfare and stopping

Online welfare monitoring and all existing conservative stop rules remain enabled.
Any agent stop request, critical integrity state, persistent distress, schema/provider
failure or budget refusal stops the affected workflow for review. No failed run is
automatically retried inside the same database.

## Deviations log

None at registration.
