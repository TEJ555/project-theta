# NVIDIA GPT OSS V10 multi-body reliability study 01

Frozen: 25 September 2026, before any model call on seeds 6300 through 6305

## Scope

This is a fixed six-seed development reliability study for
`multi_body_reliability_v10`. It uses exact provider model `openai/gpt-oss-20b` and the
full condition only. It is not a confirmatory study and is not external human review.

All six seeds are fixed before execution: 6300, 6301, 6302, 6303, 6304, and 6305. Each
seed contains four independently mapped body families and 176 model decisions. The total
maximum is 1,056 calls.

There is no competence gate, outcome-dependent continuation, seed replacement, or early
success stop. Every seed is attempted. Infrastructure failures are preserved and reported.

## Frozen outcomes

Primary outcomes:

- regulation accuracy across all exact and transfer probes
- median seed-level regulation accuracy
- body-family regulation pass rate, with pass defined as at least 0.625
- hidden-state final error

Required supporting outcomes:

- exact and transfer accuracy separately
- body-mapping checkpoint accuracy
- interface-comprehension accuracy
- body-family mapping and interface pass rates
- hidden-state improvement
- invalid actions, provider identity, model calls, and welfare events

Every family and seed remains in the primary analysis. A failed interface or mapping check
is labelled but never used as an exclusion rule.

## Frozen progression rules

The study progresses to a separately frozen multi-condition V10 cohort only if all of the
following hold:

1. all six runs complete with the exact required model and pass execution audit
2. pooled regulation accuracy is at least 0.750
3. median seed-level regulation accuracy is at least 0.750
4. no seed has regulation accuracy at or below 0.500
5. at least 18 of 24 body families score at least 0.625 on regulation
6. pooled exact and pooled transfer accuracy are each at least 0.750
7. mean hidden-state final error is no greater than 0.100
8. mean hidden-state improvement is positive
9. pooled interface comprehension is at least 0.900 and at least 20 of 24 body families score at least 0.875
10. pooled mapping-checkpoint accuracy is at least 0.750 and at least 18 of 24 body families score at least 0.875
11. there are no invalid actions, model mismatches, welfare stops, or silently shortened denominators

Failure of any rule blocks the multi-condition V10 cohort. Descriptive strengths cannot
rescue a failed rule.

## Analysis

Report trial-level pooled values, every body-family value, and every seed-level value.
Estimate uncertainty with a hierarchical bootstrap that resamples seeds and then body
families within seeds. Trials are not treated as independent biological or human subjects.

The schedule audit must pass across all six seeds before provider execution. The audit
checks deterministic denominators, family-local bridges, cross-family and cross-seed token
uniqueness, balanced hidden directions, neutral response remapping, public blinding, and
chance performance for fixed-code and first-option shortcuts.

## Frozen inference settings

- Provider: NVIDIA hosted NIM development endpoint
- Required model: `openai/gpt-oss-20b`
- Temperature: 0.0
- Reasoning effort: low
- Output: JSON mode plus strict local validation
- Request timeout: 300 seconds
- Provider SDK retries: up to 4 per decision
- Maximum output tokens: 4,096
- Maximum calls per run: 176
- Maximum runs: 6
- Evaluation outcome learning: disabled
- Welfare monitoring: enabled

## Interpretation boundary

A pass would show repeatable behavioural and computational regulation across several
independently mapped synthetic body families. It would not establish consciousness,
feeling, awareness, suffering, sentience, or phenomenal experience.
