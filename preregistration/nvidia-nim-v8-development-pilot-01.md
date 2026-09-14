# NVIDIA GPT OSS V8 development pilot 01

Frozen: 14 September 2026, before any model call on seeds 5100 or 5101

## Scope

This is a bounded development pilot for `active_interoceptive_control_v8`. It evaluates
whether exact model `openai/gpt-oss-20b` can complete the active task and whether the
registered information ablations change behaviour. It is not confirmatory.

## Competence gate

Seed 5100 runs in the full condition for 24 decisions. It must complete with no
malformed response, model mismatch, invalid action, or welfare stop. Calibration
compliance must be at least 0.90, overall regulation accuracy at least 0.75, and fresh
alias transfer accuracy at least 0.667.

Failure stops the pilot. No control condition is run after a failed competence gate.

## Conditional four-condition pilot

If the competence gate passes, fresh seed 5101 runs in deterministic order: full,
shuffled interoception, no body, then no memory. Each condition contains 24 model
decisions, for 96 maximum model calls. The competence seed is excluded from the
four-condition effect estimates.

The primary descriptive comparison is full minus shuffled interoception on active
regulation accuracy. Full minus no memory and full minus no body are mechanism
diagnostics. Report every condition, exact and transfer accuracy, regulation
improvement, prediction error, calibration compliance, invalid actions, model identity,
provider use, and welfare events.

The pilot is eligible for a fresh multi-seed replication only if all four runs and
audits complete, full regulation accuracy is at least 0.75, full exceeds shuffled
interoception by at least 0.20, and full transfer accuracy is at least 0.667.

## Frozen inference settings

- Provider: NVIDIA hosted NIM development endpoint
- Required model identifier: `openai/gpt-oss-20b`
- Temperature: 0.0
- Reasoning effort: low
- Output: strict JSON Schema plus local validation
- Request timeout: 300 seconds
- Provider SDK retries: up to 4 per decision
- Maximum output tokens: 4,096
- Welfare monitoring: enabled

## Interpretation boundary

A pass would be evidence of active causal learning and private-state regulation in
this scaffold. It would not be evidence of phenomenal consciousness.
