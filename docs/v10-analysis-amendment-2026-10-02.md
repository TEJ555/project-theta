# V10 analysis integrity amendment

Recorded: 2 October 2026, while study 02 was running and before any V10 study 02
decisions, rationales, scores, or outcome summaries were inspected.

Status: post-freeze procedural amendment. This is not part of the original registration
and must not be described as if it had been frozen on 25 September 2026.

## Why an amendment was needed

The original V10 analyzer assumed one clean completed run per seed. It did not fully
implement the recovery rules already accepted by the execution audit, and it trusted the
stored metric table without independently comparing it with the raw trial log.

These are integrity defects rather than outcome-threshold choices. They were identified
without examining V10 outcome values.

## Changes

The hardened analyzer now:

1. reports every execution attempt
2. permits at most one preserved `interrupted_before_completion` attempt per seed
3. requires exactly one completed 176-step and 176-call run for every planned seed
4. excludes preserved partial attempts from scientific outcome estimates
5. rejects duplicate completions, non-approved failures, missing metrics, null metrics,
   and shortened denominators
6. verifies that every logged step has the same non-empty provider response ID as its
   matching API-call record
7. requires 1,056 unique completed provider response IDs from exact model
   `openai/gpt-oss-20b`
8. independently recomputes regulation, exact, transfer, interface, mapping, hidden
   final-error, and hidden-improvement metrics from the raw trial rows
9. rejects any disagreement between the recomputed values and stored metric table

## What did not change

- experiment prompts or trial schedule
- seeds or body-family mappings
- model, provider route, temperature, or reasoning setting
- condition or information shown to the model
- outcome definitions
- any progression threshold
- hierarchical bootstrap structure or seed
- interpretation boundary

No additional V10 model call is authorized by this amendment.

## Frozen prompt note

The NVIDIA adapter prompt used by study 02 contains the accidental phrase `Do not emit
All dependence and confidence values must be numbers`. The surrounding schema, example,
and validation still require numeric dependence values, but the sentence is malformed and
could confuse a model.

Study 02 remains unchanged. The exact frozen prompt hash and prompt text must be retained
with its report. The sentence is corrected only for future studies, which will therefore
have a different prompt hash. This correction cannot be used to rerun or replace any V10
study 02 seed.

## Reporting requirement

After study 02 completes, run both:

1. the analyzer from frozen commit `1894a0c`
2. the hardened analyzer from the later reviewed commit

Publish both machine-readable outputs. Their shared scientific estimates and frozen gates
should agree for a clean six-run cohort. If they disagree, stop and report the difference
before interpreting V10. The hardened execution and consistency checks may block a cohort
that the original analyzer would have accepted; they may not turn a failed frozen outcome
threshold into a pass.

The final report must label this as a post-freeze, pre-outcome integrity amendment and
include the exact commit identifiers for both analyzers.
