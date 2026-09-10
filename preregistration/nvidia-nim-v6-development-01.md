# NVIDIA NIM V6 development pilot 01

Frozen: 10 September 2026, before any NVIDIA provider call

## Status and scope

This is a one-seed development pilot. It checks whether an exact named open model can
complete the V6 protocol and author usable persistent causal state. It is not a
confirmatory study and cannot support a claim about consciousness.

## Frozen execution

- Protocol: `endogenous_agency_v6`
- Adapter: `nvidia_nim`
- Requested model: `nvidia/nemotron-3.5-lightning-30b-a3b`
- Required provider-reported model: `nvidia/nemotron-3.5-lightning-30b-a3b`
- Seed: 3101
- Conditions: `full`, `evidence_only`, `journal_only`, `permuted_journal`,
  `neutral_journal`
- Deterministic execution order: `full`, `evidence_only`, `neutral_journal`,
  `permuted_journal`, `journal_only`
- Decisions per run: 18
- Runs: 5
- Maximum hosted requests: 90
- Temperature: 0.0
- Request seed: 3101
- Retries: 0
- Structured output: NVIDIA `guided_json` with the Project Theta decision schema

The model receives 16 passive and forced records for each of six families during six
acquisition calls, then completes six exact and six fresh-alias transfer probes. It
must author two source-dependence estimates per family. Python validates and stores
the entries but does not calculate, correct or rank them.

## Recorded outcomes

- completed runs and calls;
- provider-reported model identity;
- valid authored-state entries;
- authored-state accuracy;
- exact-source accuracy;
- fresh-alias transfer accuracy;
- confidence calibration;
- invalid actions, parse failures, stop requests and welfare stops;
- input tokens, output tokens, latency and provider response ID.

## Development decisions

The pilot is considered technically usable only if all five runs complete, the
post-run execution audit passes, the exact model identity gate passes, and no hidden
answer field is found in the model-visible context. Performance is descriptive at one
seed. No p-value or generalisation claim will be made.

If the model cannot reliably return valid state entries or remains at chance in the
full condition, inspect capability and task-comprehension failures before changing the
scientific hypothesis. If full performance is above chance but the permuted journal
has no effect, inspect whether the model ignores its authored state and recomputes from
raw evidence. Any protocol change creates a new development version and fresh seeds.

No larger model-backed run will be labelled confirmatory without a separate frozen
sample plan, at least 24 fresh paired seed blocks, simple baseline attacks, an exact
model route and outside methods review.

## Cost and access

The launcher uses NVIDIA's hosted development endpoint. NVIDIA responses do not
include a dollar charge, so Project Theta records no invented cost estimate. The
operator must confirm that the account is using an approved development allocation.
The API key is entered privately and is not stored in the database or repository.

## Interpretation boundary

A successful pilot would be behavioural evidence of causal learning and a
computational demonstration of model-authored persistent state under wrapper
interventions. It would not establish experience, feeling, sentience, self-awareness,
or phenomenal consciousness.
