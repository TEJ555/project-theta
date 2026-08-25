# Changelog

## 0.2.0 - 2026-08-25

- Replaced under-stimulating free navigation as the scientific battery with
  deterministic acquisition and blinded, counterbalanced forced-choice trials.
- Added private-signal, generalization, source-binding, temporal, memory and body
  protocols with matched ablations and scripted positive controls.
- Added paired analysis, bootstrap intervals, exact sign tests and validity warnings.
- Added schema-v2 provenance, API-call metadata, checkpoints and interrupted-run
  recovery without discarding completed observations.
- Added bounded OpenAI Responses API and Ollama adapters with explicit opt-in gates,
  timeouts, retries and call budgets.
- Added preflight checks, a resumable worker, Docker Compose and systemd deployment
  examples, expanded tests and a worked infrastructure preregistration.
- Retained the grid world as `navigation_demo`, outside the scientific study battery.

## 0.1.0 - 2026-08-25

- Initial deterministic prototype with grid world, synthetic body, private I7 signal,
  memory, self-model, workspace, adapters, SQLite logging and welfare stop rules.
