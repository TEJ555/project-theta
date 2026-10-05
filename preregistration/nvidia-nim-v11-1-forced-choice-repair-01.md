# NVIDIA GPT OSS V11.1 forced-choice repair 01

Frozen before any V11.1 provider call.

## Status and motivation

V11 completed all 36 runs and passed every scientific contrast, but one of 6,336 model
responses abstained from a forced choice. The frozen analyzer then detected both the
nonzero invalid-action count and the fact that the raw trial record contained only the
substituted fallback action. V11 remains formally failed and does not unlock cross-model
replication.

V11.1 is one targeted protocol repair with fresh data. It is not an added V11 tranche,
and V11 and V11.1 outcomes will not be pooled.

## Research question

Does the V11 mechanism pattern replicate when forced-choice compliance and raw action
provenance are measured without loss?

## Fixed design

- Experiment engine: `multi_body_mechanism_v11`
- Provider route: NVIDIA hosted NIM development endpoint
- Required model: `openai/gpt-oss-20b`
- Temperature: 0.0
- Reasoning effort: low
- Seeds: 7400, 7401, 7402, 7403, 7404 and 7405
- Conditions: full, shuffled interoception, incorrect association summary, raw history,
  incorrect bridge and explicit mapping
- Runs: 36 paired seed-condition runs
- Decisions per run: 176
- Maximum completed model calls: 6,336
- Evaluation outcome learning: disabled
- Welfare monitoring: enabled
- Maximum attempts per seed-condition job: 2

All task geometry, causal manipulations, scoring denominators and scientific thresholds
are identical to V11. New opaque labels are generated from the fresh seeds.

## Frozen repair

Every controlled item is explicitly described as forced choice. The model must choose the
better permitted action and may not abstain. Each trial preserves the raw model action and
an invalid-action flag. If an action is invalid, the harness uses its declared
deterministic fallback only for simulation continuity and scores the response incorrect.

The forced-choice compliance gate passes only if there are no more than six invalid
actions across all 6,336 calls and no run contains more than one. This bound was chosen
after the V11 failure and is tested only on fresh V11.1 data. Invalid responses are never
removed, retried, replaced for scoring, or treated as infrastructure failures.

## Frozen execution validity

The cohort is interpretable only if:

1. exactly one completed 176-step run exists for every planned seed-condition pair
2. exactly 6,336 completed provider calls are present
3. all provider response identifiers are present, unique and aligned between step and
   call records
4. every completed call reports exact model `openai/gpt-oss-20b`
5. all required metrics, including invalid-action counts, reproduce from raw trial rows
6. no silently shortened denominator, duplicate completion or unreported failure exists
7. the forced-choice compliance bound passes

## Frozen progression gates

Cross-model replication is unlocked only if every gate passes:

1. Execution validity passes.
2. Full-condition pooled regulation is at least 0.750, median seed regulation is at
   least 0.750, and every full seed is above 0.500.
3. Shuffled-interoception pooled regulation is at most 0.650; full minus shuffled is at
   least 0.150; and the paired difference is positive in at least five of six seeds.
4. Under the incorrect bridge, pooled exact accuracy is at least 0.750, pooled transfer
   accuracy is at most 0.550, exact minus transfer is at least 0.200, and the paired
   within-seed difference is positive in at least five of six seeds.
5. Explicit-mapping pooled and median seed regulation are each at least 0.750.
6. Across all 36 runs, pooled interface comprehension is at least 0.900 and at least 30
   runs score at least 0.875.
7. Forced-choice compliance passes.
8. There are zero welfare stops and all validity checks pass.

Failure of any gate blocks progression. No failed seed or condition will be replaced.

## Frozen summary classifications

Incorrect-summary interference and summary necessity use the exact V11 definitions. They
are classifications, not progression gates.

## Analysis

`scripts/analyze_v11_1_repair.py` independently reconstructs outcomes and invalid-action
counts from raw trial rows. Seed-level bootstrap intervals use 10,000 deterministic
resamples and are descriptive. Trials are not treated as independent organisms or human
participants.

## Registered infrastructure deviation after launch

After 13 completed runs, the first attempt for seed 7402 raw history stopped at step 164
because NVIDIA returned an empty completion. The database, partial attempt and provider
failure were preserved. The frozen worker specification allowed two attempts per job, but
the worker's retry classifier did not yet include this exact NVIDIA infrastructure error.
The adapter also passed the configured retry count only to the HTTP client, so a
successful HTTP response with empty content was not retried.

Before the permitted second attempt, the control plane was changed only to classify the
exact empty-completion error as retryable and to apply the already configured maximum of
four retries to empty completion content. Provider-attempt count is recorded on the final
successful call. No task geometry, prompt, condition, seed, scoring rule, threshold,
analysis rule or completed outcome changed. Runs before and after this patch retain their
exact code versions. This deviation will be reported with the result and is not grounds
to replace any scientific failure.

## Interpretation boundary

A pass would support a selective computational dependence claim for this model, wrapper
and benchmark after the measurement repair. It would not establish awareness, feeling,
suffering, sentience or phenomenal consciousness. A non-conscious controller can produce
the target pattern.

## Post-completion audit compatibility amendment

Added 5 October 2026 after outcomes were available. The generic execution audit and the
V11.1 analyzer recognised `interrupted_before_completion` as a preserved retry but did
not recognise the exact NVIDIA empty-completion failure documented above. Consequently,
they rejected the database despite exactly one completed run for every planned pair.

The audit is amended to accept only the exact preserved stop reason
`AdapterError: NVIDIA NIM returned an empty completion.` under the existing limit of no
more than one failed recovery attempt per seed-condition pair. The failed attempt remains
in the database, contributes no outcome rows or completed-call identifiers, and is not
pooled with the successful attempt. Other provider failures, a second recovery failure,
duplicate completions, missing calls and all scientific failures remain disallowed. This
post-completion amendment changes no prompt, seed, condition, denominator, metric,
threshold or observed result.

