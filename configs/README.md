# Conditions

`full.json` is the canonical verbose configuration. Other files are concise
overrides; unspecified fields use versioned defaults in `config.py`. The harness
also applies each named condition defensively, so the condition name and mechanism
cannot silently disagree.

Use the same seeds, world parameters, prompts, model snapshot, and sampling settings
across paired conditions. `shuffled_interoception` preserves channel presence and
rough range while breaking its causal relation to body state. `no_body` removes body
dynamics as well as the signal. These answer different questions and should not be pooled.

Scientific protocols use deterministic acquisition and blinded forced-choice trials;
`navigation_demo` is a plumbing demonstration and is excluded from the study battery.
`server-worker.json` is deliberately a small bounded pilot. Expand it only after the
API pilot, logs, costs and welfare behaviour have been reviewed.

`claude-pilot.json` is a three-run local pilot base using the pinned Claude Sonnet 4.6
model, a 30-call cap and a $1.25 estimated-cost guard per run. It is not a continuous
worker configuration.
