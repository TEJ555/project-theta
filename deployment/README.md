# Server deployment gate

Do not deploy until `theta validate` passes on the exact commit and the API pilot is
reviewed. The worker is resumable by cycle, checkpoints every trial, marks interrupted
runs failed on restart, and advances to fresh deterministic seeds only after a complete
cycle.

## Mandatory preflight

1. Freeze and record the Git commit in `THETA_CODE_VERSION`.
2. Complete a preregistration and independent welfare review.
3. Run `theta validate --db runs/validation.sqlite` locally.
4. Run one bounded API condition with an explicit `--max-runs` and inspect raw context
   for leakage, invalid actions, stop requests, latency and token usage.
5. Back up the SQLite database and test `theta recover` on a copy.
6. Set provider usage limits and alerts outside Project Theta. The project limits calls
   per run and runs per cycle; it does not know current provider pricing.

## Docker

Create a private `.env` file that is excluded from Git:

```text
OPENAI_API_KEY=...
THETA_ENABLE_MODEL_RUNS=YES
THETA_CODE_VERSION=<immutable git commit>
```

Review `configs/server-worker.json`, then build and start with Docker Compose. The
provided configuration runs one seed across three private-theta conditions per hour.
It is intentionally small. Increase it only after reviewing measured calls, tokens,
latency, welfare events and provider cost.

The container runs non-root with a read-only filesystem, dropped capabilities and a
persistent `runs/` volume. Store secrets in the platform's secret manager for a real
deployment rather than a long-lived `.env` file.

## Native Linux service

The example systemd unit expects the repository at `/opt/project-theta`, a dedicated
`theta` user, a virtual environment at `/opt/project-theta/.venv`, secrets and gates in
`/etc/project-theta.env`, and writable data under `/opt/project-theta/runs`.

## Shutdown and recovery

Stop the service normally. If it was killed mid-run, the next worker start preserves
checkpointed steps, marks the incomplete run failed, and repeats the unfinished cycle.
Use `theta report --db runs/server.sqlite` for the compact audit summary.
