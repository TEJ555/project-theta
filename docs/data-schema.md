# Data and logging schema

SQLite schema version 2 is created and migrated non-destructively by `storage.py`.

- `runs`: condition, seed, adapter/model, configuration, status and stop reason.
- `run_artifacts`: SHA-256 config/prompt hashes, immutable code revision and runtime.
- `steps`: agent-visible observation/context/decision plus separately stored hidden
  trial/body/scoring state and provider response ID.
- `api_calls`: per-trial token, latency, conservative cost estimate and provider metadata
  when available.
- `memories`: exact records made available to episodic memory.
- `probes`: hidden expected action and observed structured response.
- `welfare_events`: trigger, tick and state at conservative termination.
- `metrics`: typed behavioural/computational/quality/safety/cost values.
- `worker_state`: completed cycles and last seed for resumable continuous execution.
- `schema_info`: migration version.

WAL mode, a busy timeout and per-trial commits preserve completed evidence across
ordinary process interruption. `theta recover` marks unfinished runs failed; it does
not delete or disguise partial data.

JSON uses sorted compact encoding and timestamps use UTC ISO 8601. Raw chain-of-thought
is neither requested nor stored. API keys are never written to configuration/logs.
Before publication, lock the database read-only, calculate a file digest, publish the
analysis code/data dictionary and apply a documented retention/redaction policy.
