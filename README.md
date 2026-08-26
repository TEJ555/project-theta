# Project Theta

Project Theta is an open-source prototype laboratory for testing **theory-inspired
behavioural and computational indicators** in persistent artificial agents. It does
not detect, prove, create, or rule out phenomenal consciousness.

Requires Python 3.10 or newer.

Version 0.2.3 provides a deterministic grid world, controlled acquisition/probe engine, synthetic body and private
interoception, persistent memory, self-model and workspace interfaces, pluggable
model adapters, six experimental protocols, matched ablations, welfare stop rules,
SQLite/JSON logging, metrics, preregistration templates, tests, and a no-key demo.

## Epistemic boundary

Project Theta keeps three claims separate:

1. **Behavioural indicators**: observable performance such as avoiding a cause of an
   unknown internal signal or distinguishing self from other.
2. **Computational indicators**: inspectable mechanisms such as persistent memory,
   global broadcast, recurrent state updates, and a self-model used in control.
3. **Phenomenal consciousness**: whether there is anything it is like to be the
   system. No result produced here licenses that inference.

Passing a task can be caused by prompt imitation, learned verbal patterns, simple
control policies, leakage, or architecture-specific shortcuts. Self-reports are
logged as behaviour, not privileged access to phenomenal facts.

## Quick start (no API key)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -e .
theta demo --steps 24 --db runs/demo.sqlite
theta doctor --adapter scripted --db runs/doctor.sqlite
theta validate --db runs/validation.sqlite
theta run --experiment all --seeds 11,22,33 --db runs/study.sqlite --json runs/study.json
theta report --db runs/study.sqlite
python -m unittest discover -s tests -v
```

If installation fails, the `theta` command will not exist yet. Resolve the Python or
installation error first, reactivate the environment, and rerun `python -m pip install -e .`.

Without installation, from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m project_theta demo --steps 24 --db runs/demo.sqlite
```

The scripted adapter is deterministic and intentionally simple. Its outputs only
show that the harness, controls and metrics work. They are not scientific evidence.

## Optional model adapters

Anthropic Claude (recommended first bounded pilot):

```powershell
python -m pip install -e ".[anthropic]"
.\scripts\run_claude_pilot.ps1
```

The launcher prompts privately for the Console API key, runs preflight plus exactly
three matched conditions, prints the report and removes the key from its process. The
key is never written to the repository or database. If a prior default pilot database
exists, the launcher preserves it and automatically selects the next numbered filename.

The Claude pilot uses pinned `claude-sonnet-4-6`, at most 30 calls and an estimated
$1.25 USD guard per run. Three runs therefore have a planned guard of $3.75 USD, with
a possible one-call overshoot because the provider reports tokens after a response.

After reviewing the exploratory pilot, the bounded six-seed replication is launched
separately so it remains auditable:

```powershell
.\scripts\run_claude_replication.ps1
```

Its frozen design is in `preregistration/claude-replication-01.md`. The launcher runs
each matched three-condition seed as a bundle and checks a $4.20 cumulative replication
budget before beginning the next bundle.
The estimate uses frozen regular-input, output, cache-write and cache-read rates.
Configure a provider-side spending limit as the authoritative billing ceiling.

For isolation, create a dedicated `project-theta` workspace in the Claude Console, set
its monthly spend limit to $5 USD, and create the pilot key inside that workspace. Do
not use the unrestricted Default Workspace key and do not paste the key into chat.

OpenAI (uses the Responses API and structured JSON output):

```powershell
python -m pip install -e ".[openai]"
$env:OPENAI_API_KEY = "..."
$env:THETA_ENABLE_MODEL_RUNS = "YES"
theta doctor --adapter openai --db runs/api-doctor.sqlite
theta run --experiment private_theta --adapter openai --model gpt-5.6 --seeds 11 --max-runs 3 --db runs/api-pilot.sqlite
```

Ollama-compatible local server:

```powershell
$env:THETA_ENABLE_MODEL_RUNS = "YES"
theta run --experiment private_theta --adapter ollama --model llama3.2 --seeds 11 --max-runs 3
```

Exact availability and model access vary by account/provider. Keep the model ID,
version, temperature, prompts, and provider response identifiers with every run.
Model-backed execution is locked unless `THETA_ENABLE_MODEL_RUNS=YES` is set and
`--max-runs` is explicit. Both hosted adapters use schema-constrained output, record
usage/latency, freeze reasoning effort in the logged configuration, and fail rather than
silently substituting the scripted baseline. OpenAI response storage is disabled.

## Included experiments

| Experiment | Manipulation | Primary outcome | Main matched control |
|---|---|---|---|
| `private_theta` | Guaranteed neutral cue exposures produce informative or uninformative private signals | blinded forced-choice accuracy | shuffled/no body |
| `aversion_generalization` | Novel cues preserve a learned causal feature | selective transfer to held-out tokens | shuffled/no memory |
| `self_vs_other` | Opaque routes differ in whether they causally change the private channel | source-binding choice accuracy | no self-model/workspace |
| `temporal_self` | Sequence outcomes occur after three intervening trials | delayed forced-choice accuracy | no persistence/recurrence |
| `memory_ablation` | Memory available versus disabled | within-seed performance difference | full architecture |
| `body_ablation` | truthful body, no body dynamics, or shuffled interoception | within-seed performance difference | truthful body |

Run `theta list` for machine-readable protocol descriptions.

## Repository map

```text
src/project_theta/
  world.py          deterministic world and observations
  body.py           hidden physiology and private I7 signal
  components.py     memory, self-model, workspace interfaces
  agent.py          persistent perception-to-action loop
  experiments.py    protocol registry and probe schedules
  trials.py         blinded, counterbalanced controlled trial generator
  harness.py        seeded execution, controls, stop rules
  metrics.py        predeclared indicator metrics
  analysis.py       paired effects, bootstrap intervals and validity warnings
  storage.py        SQLite schema and provenance logging
  worker.py         resumable, bounded continuous-run worker
  adapters/         scripted, OpenAI, and Ollama adapters
configs/            versioned full/control/ablation conditions
docs/               research, technical, ethics, schema, metrics
preregistration/    blank and worked preregistration templates
prompts/            agent contract and Cursor/Claude handoff
references/         checked BibTeX bibliography
research/           raw searches, screening record, evidence table, verification
tests/              determinism, ablation, storage and smoke tests
deployment/         Docker/systemd examples and deployment gate
```

## Research workflow

1. Freeze a preregistration and commit hash before collecting target-model data.
2. Run a scripted smoke test, then matched target/control conditions using identical
   seeds and counterbalanced mappings.
3. Keep analysts blind to condition labels where practical.
4. Report all exclusions, welfare stops, failed calls, and null results.
5. Interpret converging indicators under multiple theories; do not manufacture a
   single “consciousness score.”

See the [full literature review](docs/literature-review.md), [evidence table](research/evidence-table.md),
[research framing](docs/research-framing.md), [technical specification](docs/technical-spec.md),
[hypotheses](docs/hypotheses.md), [ethics and stop rules](docs/ethics.md), and
[experiment protocol](docs/experiment-protocol.md).

The completed six-seed Claude study is documented in
[replication results](results/claude-replication-01.md). Public repository and website
work is organized in the [publication plan](docs/publication-plan.md).

The literature review is reproducible and its limitations are explicit. It has one
primary reviewer, capped database retrieval, and requires independent second-reviewer
screening before journal submission or a claim of exhaustive coverage.

## Scientific status

This is a pre-deployment research prototype, not a validated instrument. It implements
testable functional analogues inspired by Global Workspace, recurrent processing,
higher-order/self-monitoring, predictive processing, and embodied/interoceptive
accounts. It deliberately does not implement or claim a valid IIT Phi estimator.

The scripted validation is a positive-control test of the laboratory, not evidence
about AI subjects. Before a server deployment, follow the [deployment gate](deployment/README.md).

## Contributing

Use deterministic seeds, add a matched negative control for every new positive
condition, declare metrics before running target models, preserve raw logs, and add
tests for any new mechanism. See [CONTRIBUTING.md](CONTRIBUTING.md).
