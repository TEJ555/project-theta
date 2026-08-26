# Technical specification v0.3

## Objective

Provide a reproducible platform for causal tests of theory-inspired functional
indicators in persistent agents, with negative controls and failure visibility built
into the execution path.

## Data flow

```text
hidden trial schedule ──public stimulus──┐
                                       ├─> candidate contents ─> workspace ─> adapter ─> choice
hidden synthetic body ──private I7──────┘          ↑                  │             │
                                                  │                  v             v
                                           episodic memory <── self-model <── outcome
```

The adapter sees observation, permitted actions and workspace broadcast. It does not
receive raw memory/self-model bypasses, the seed, condition name, perturbation, correct
action or future random values. Hidden scoring and body ground truth occupy separate
database fields. Workspace removal therefore prevents the planner from accessing local
module products while leaving those modules inspectable.

## Reproducibility and counterbalancing

- All simulated randomness derives from declared integer seeds and stable constants.
- Cue-risk mapping and left/right answer placement are independently counterbalanced.
- Every probe block contains equal numbers of correct-left and correct-right trials.
- Adversarial schedules use seed-specific aliases and balanced sham outcomes within
  every cue and learning stage.
- Run order is deterministically randomized to reduce provider drift confounds.
- Python's process-randomized `hash()` is never used for experimental state.
- Configuration, prompt, code revision, Python/platform, provider ID, latency and token
  metadata are preserved. Provider nondeterminism is reported even at temperature zero.

## Interfaces and failure behavior

`ModelAdapter.decide(context) -> Decision` is the only model boundary. Structured output
permits one declared action, next-I7 prediction, confidence, short public rationale,
operational self-report and conservative stop request. Invalid actions are visibly
counted and replaced with a predeclared zero-confidence fallback. Provider errors fail
the run and never switch adapters.

Each run has a frozen reasoning effort plus hard request-timeout, retry, output-token and
model-call limits. Supported Claude models also have a usage-derived estimated-cost
guard. Non-scripted runs require an environment safety gate, an explicit run-count
budget, and a clean committed revision or immutable deployment version.

## Storage and recovery

SQLite schema 2 uses WAL mode, a 30-second busy timeout and per-trial commits. It stores
run state, visible/hidden step data, memories, probes, welfare events, typed metrics,
prompt/config hashes, code/runtime provenance, API call metadata and worker progress.
After an abrupt stop, `theta recover` marks incomplete runs failed without deleting
checkpointed evidence. A worker repeats an unfinished cycle and advances seeds only
after the cycle completes.

## Continuous operation

`theta worker` reads a bounded specification with seeds per cycle, maximum runs per
cycle and interval. Docker and systemd examples run one process, retain SQLite data and
restart on failure. The Docker example is non-root, read-only, capability-free and
requires an explicit model-run gate. Provider-side spending limits and monitoring are
still mandatory.

## Out of scope

Neural activation access, model-weight learning, validated causal emergence or Phi,
biologically faithful affect, autonomous external tools, moral-patient classification,
and any inference from indicators to phenomenal consciousness.
