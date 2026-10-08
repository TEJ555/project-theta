# NVIDIA Nemotron V12 cross-model replication 01

Frozen before any V12 provider call.

## Motivation and research question

V11.1 passed every frozen execution and mechanism gate on NVIDIA-hosted
`openai/gpt-oss-20b`. V12 asks whether the same selective computational pattern
replicates on a genuinely different model family rather than reflecting one model's
training or output habits.

The required model is `nvidia/nemotron-3-super-120b-a12b`, an NVIDIA-developed hybrid
Mamba-2, mixture-of-experts and attention model with 120B total and 12B active
parameters. The hosted endpoint, exact identifier and free-endpoint availability were
verified in NVIDIA's public model catalogue before this document was frozen.

## Fixed design

- Experiment engine: `multi_body_mechanism_v11`
- Provider route: NVIDIA hosted NIM development endpoint
- Required model: `nvidia/nemotron-3-super-120b-a12b`
- Reasoning mode: disabled
- Temperature: 1.0, following the model provider's documented serving recommendation
- Seeds: 7500, 7501, 7502, 7503, 7504 and 7505
- Conditions: full, shuffled interoception, incorrect association summary, raw history,
  incorrect bridge and explicit mapping
- Runs: 36 paired seed-condition runs
- Decisions per run: 176
- Maximum completed study calls: 6,336
- Evaluation outcome learning: disabled
- Welfare monitoring: enabled
- Maximum attempts per seed-condition job: 2

Task geometry, controls, scoring denominators and progression thresholds are identical
to V11.1. Fresh seeds generate new opaque labels. V11.1 and V12 are analyzed separately.

## Bounded compatibility check

After this design is committed and pushed, one non-study provider call may test exact
model identity, JSON-object support, local schema validation and provider-ID presence.
Its prompt contains no study schedule or scoring key. Its response content is discarded;
only a provenance receipt is retained. Failure stops V12 before the study database is
created and does not justify switching models without a new preregistration.

## Execution validity

The cohort is interpretable only if:

1. exactly one completed 176-step run exists for every planned seed-condition pair;
2. exactly 6,336 completed provider calls are present;
3. all completed provider identifiers are present, unique and aligned between step and
   call records;
4. every completed call reports exact model `nvidia/nemotron-3-super-120b-a12b`;
5. all required metrics and invalid-action counts reproduce from raw trial rows;
6. no shortened denominator, duplicate completion or unreported failure exists; and
7. no more than one declared infrastructure recovery attempt exists for a pair.

The only retryable preserved failures are an interrupted local worker, the already
defined Windows cleanup or timeout failures, or the exact NVIDIA empty-completion error.
Failed attempts remain in the database and contribute no outcome evidence. An invalid
model action is a scored study result, not an infrastructure failure.

## Frozen progression gates

Cross-model replication passes only if every gate passes:

1. Execution validity passes.
2. Full-condition pooled regulation is at least 0.750, median seed regulation is at
   least 0.750, and every full seed is above 0.500.
3. Shuffled-interoception pooled regulation is at most 0.650; full minus shuffled is at
   least 0.150; and the paired difference is positive in at least five of six seeds.
4. Under the incorrect bridge, pooled exact accuracy is at least 0.750, pooled transfer
   accuracy is at most 0.550, exact minus transfer is at least 0.200, and the paired
   within-seed difference is positive in at least five of six seeds.
5. Explicit-mapping pooled and median regulation are each at least 0.750.
6. Across all 36 runs, pooled interface comprehension is at least 0.900 and at least 30
   runs score at least 0.875.
7. There are no more than six invalid actions overall and no run contains more than one.
8. There are zero welfare stops and all validity checks pass.

Failure of any gate blocks the cross-model claim. Seeds, thresholds and conditions will
not be replaced or expanded to rescue an unfavorable result.

## Analysis and shortcut controls

`scripts/analyze_v12_cross_model.py` reconstructs outcomes from raw trials and enforces
the exact provider identity. Deterministic 10,000-resample seed-level bootstrap intervals
are descriptive. The frozen schedule audit checks family balance, isolation, blinding,
mapping-direction balance and chance-level fixed-action shortcuts. A held-out red team
fits public-metadata rules on seeds disjoint from both study cohorts and must remain at or
below 0.55 accuracy.

## Welfare and interpretation boundary

The existing online stop monitor remains active. A welfare stop ends the affected run
and blocks progression; it is never silently retried as infrastructure.

A pass would support cross-model replication of a selective computational dependence in
this wrapper and benchmark. It would not establish awareness, feeling, suffering,
sentience or phenomenal consciousness. A non-conscious controller can produce the target
pattern.
