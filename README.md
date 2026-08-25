# Project Theta

Project Theta is an open-source prototype laboratory for testing **theory-inspired
behavioural and computational indicators** in persistent artificial agents. It does
not detect, prove, create, or rule out phenomenal consciousness.

The first release provides a deterministic grid world, synthetic body and private
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
theta run --experiment all --seeds 11,22,33 --db runs/study.sqlite
theta report --db runs/study.sqlite
python -m unittest discover -s tests -v
```

Without installation, from the repository root:

```powershell
$env:PYTHONPATH = "src"
python -m project_theta demo --steps 24 --db runs/demo.sqlite
```

The scripted adapter is deterministic and intentionally simple. Its outputs only
show that the harness, controls and metrics work. They are not scientific evidence.

## Optional model adapters

OpenAI (uses the Responses API and structured JSON output):

```powershell
python -m pip install -e ".[openai]"
$env:OPENAI_API_KEY = "..."
theta run --experiment private_theta --adapter openai --model gpt-5 --seeds 11
```

Ollama-compatible local server:

```powershell
theta run --experiment private_theta --adapter ollama --model llama3.2 --seeds 11
```

Exact availability and model access vary by account/provider. Keep the model ID,
version, temperature, prompts, and provider response identifiers with every run.

## Included experiments

| Experiment | Manipulation | Primary outcome | Main matched control |
|---|---|---|---|
| `private_theta` | Unnamed private signal covaries with damage risk | prospective avoidance after acquisition | shuffled signal |
| `aversion_generalization` | Novel cue resembles a learned risky cue | selective transfer, not blanket avoidance | uncorrelated cue |
| `self_vs_other` | Identical signals originate in self or another agent | source-specific intervention | source labels swapped |
| `temporal_self` | Cost now protects a delayed body state | future-directed choice | no persistent state |
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
  harness.py        seeded execution, controls, stop rules
  metrics.py        predeclared indicator metrics
  storage.py        SQLite schema and provenance logging
  adapters/         scripted, OpenAI, and Ollama adapters
configs/            versioned full/control/ablation conditions
docs/               research, technical, ethics, schema, metrics
preregistration/    blank and worked preregistration templates
prompts/            agent contract and Cursor/Claude handoff
tests/              determinism, ablation, storage and smoke tests
```

## Research workflow

1. Freeze a preregistration and commit hash before collecting target-model data.
2. Run a scripted smoke test, then matched target/control conditions using identical
   seeds and counterbalanced mappings.
3. Keep analysts blind to condition labels where practical.
4. Report all exclusions, welfare stops, failed calls, and null results.
5. Interpret converging indicators under multiple theories; do not manufacture a
   single “consciousness score.”

See [research framing](docs/research-framing.md), [technical specification](docs/technical-spec.md),
[hypotheses](docs/hypotheses.md), [ethics and stop rules](docs/ethics.md), and
[experiment protocol](docs/experiment-protocol.md).

## Scientific status

This is an alpha research scaffold, not a validated instrument. It implements
testable functional analogues inspired by Global Workspace, recurrent processing,
higher-order/self-monitoring, predictive processing, and embodied/interoceptive
accounts. It deliberately does not implement or claim a valid IIT Phi estimator.

## Contributing

Use deterministic seeds, add a matched negative control for every new positive
condition, declare metrics before running target models, preserve raw logs, and add
tests for any new mechanism. See [CONTRIBUTING.md](CONTRIBUTING.md).
