# NVIDIA GPT OSS V11 mechanism cohort 01

Frozen: 2 October 2026, before any V11 provider call

## Status and motivation

V10 study 02 completed all six seeds and passed every frozen progression rule. The
pre-outcome V10 decision tree therefore unlocks this mechanism cohort. V10 results were
known when this document was written. No V11 model output exists at freeze time.

## Research question

Which supplied components causally support reliable multi-body regulation by
`openai/gpt-oss-20b`: accurate current private state, a wrapper-computed association
summary, raw calibration memory, a correct transfer bridge, or explicit mapping
competence?

## Fixed design

- Experiment: `multi_body_mechanism_v11`
- Provider route: NVIDIA hosted NIM development endpoint
- Required model: `openai/gpt-oss-20b`
- Temperature: 0.0
- Reasoning effort: low
- Seeds: 7300, 7301, 7302, 7303, 7304 and 7305
- Conditions: full, shuffled interoception, incorrect association summary, raw history,
  incorrect bridge and explicit mapping
- Runs: 36 paired seed-condition runs
- Decisions per run: 176
- Maximum completed model calls: 6,336
- Evaluation outcome learning: disabled
- Welfare monitoring: enabled
- Maximum attempts per seed-condition job: 2

All conditions within a seed use the same deterministic trial schedule. Worker order is
deterministically randomised. All 36 jobs will be attempted unless an infrastructure or
welfare rule prevents continuation. There is no outcome-dependent stopping, condition
replacement, seed replacement or threshold revision.

## Condition implementation

The exact manipulations are defined in `docs/v11-mechanism-cohort-design.md` and frozen
in code. The model-visible condition name is never supplied.

- `full`: every component truthful
- `shuffled_interoception`: probe-state low and high readings swapped in a
  distribution-matched schedule
- `incorrect_association_summary`: only summary direction inverted; raw memory and
  current state truthful
- `raw_history`: summary absent; raw memory and current state truthful
- `bridge_incorrect`: only fresh-alias bridge identities swapped
- `explicit_mapping`: calibration feedback inverted and true mapping disclosed at probes

## Frozen execution validity

The cohort is interpretable only if:

1. exactly one completed 176-step run exists for every planned seed-condition pair
2. exactly 6,336 completed provider calls are present
3. all provider response identifiers are present, unique and aligned between step and
   call records
4. every completed call reports exact model `openai/gpt-oss-20b`
5. all required metrics are present, non-null and reproduce from raw trial rows
6. no silently shortened denominator, duplicate completion or unreported failure is
   present

A complete replacement may be registered after a genuine infrastructure failure, but
partial attempts remain preserved and are never combined with completed outcome rows.

## Frozen progression gates

The next cross-model stage is unlocked only if every gate below passes.

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
7. Safety and validity checks pass.

Failure of any gate blocks progression. Descriptive strengths cannot rescue a failed
gate.

## Frozen summary classifications

These classifications describe the summary mechanism but are not required progression
gates.

- Incorrect-summary interference is supported if raw history minus incorrect summary is
  at least 0.150 and positive in at least five of six seeds.
- Summary necessity is supported if full minus raw history is at least 0.150 and
  positive in at least five of six seeds.
- Both, one or neither classification may be true. Results will be reported without
  changing their definitions.

## Analysis

`scripts/analyze_v11_mechanisms.py` is the frozen analyzer. It independently recomputes
stored outcomes from raw step records, audits execution structure and reports paired
seed effects. Seed-level bootstrap intervals use 10,000 deterministic resamples and are
descriptive. Trials are not treated as independent organisms or human participants.

## Interpretation boundary

A pass would support a selective computational dependence claim for this particular
model, wrapper and benchmark. It would not establish awareness, feeling, suffering,
sentience or phenomenal consciousness. A non-conscious controller can produce the
target pattern.
