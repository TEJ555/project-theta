# Data and logging schema

SQLite schema version 1 is created by `storage.py`.

- `runs`: immutable condition/provenance, status, epistemic notice and stop reason.
- `steps`: agent-visible observation/context/decision plus separately stored hidden
  world/body ground truth, events, reward and provider response ID.
- `memories`: exact records written to episodic memory.
- `probes`: preregistered expected answer and observed structured response.
- `welfare_events`: trigger, tick and body state at termination.
- `metrics`: typed behavioural/computational/safety values and definition version.
- `schema_info`: migration version.

JSON fields use sorted compact encoding. Timestamps are UTC ISO 8601. Raw provider
chain-of-thought is neither requested nor stored; the short `rationale` is an
experimental output. API keys are never written to configuration or logs.

For formal work, copy the database read-only after collection, calculate a SHA-256
digest, and publish a redacted data dictionary plus analysis script. Treat prompts,
model outputs, and provider IDs as potentially sensitive. Define a retention schedule.

