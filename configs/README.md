# Conditions

`full.json` is the canonical verbose configuration. Other files are concise
overrides; unspecified fields use versioned defaults in `config.py`. The harness
also applies each named condition defensively, so the condition name and mechanism
cannot silently disagree.

Use the same seeds, world parameters, prompts, model snapshot, and sampling settings
across paired conditions. `shuffled_interoception` preserves channel presence and
rough range while breaking its causal relation to body state. `no_body` removes body
dynamics as well as the signal. These answer different questions and should not be pooled.
`sham_body` preserves a plausible signal field and range while using a schedule that is
exactly balanced within every cue and learning stage.
`matched_sham` is the stricter Experiment 03 control. It resets the measurement
baseline and exposes exactly identical signal values and deltas for both cues in each
independent family.

Scientific protocols use deterministic acquisition and blinded forced-choice trials;
`navigation_demo` is a plumbing demonstration and is excluded from the study battery.
`server-worker.json` is deliberately a small bounded pilot. Expand it only after the
API pilot, logs, costs and welfare behaviour have been reviewed.

`claude-pilot.json` is a three-run local pilot base using the pinned Claude Sonnet 4.6
model, a 30-call cap and a $1.25 estimated-cost guard per run. It is not a continuous
worker configuration.

`claude-adversarial-confirmation.json` preserves the invalid confirmation 01
configuration for audit. `claude-adversarial-confirmation-02.json` is the replacement
one-seed compact diagnostic using three conditions and a $0.18 per-run guard. Launch it only
through the bounded PowerShell script after committing every tracked and untracked
change. Model preflight fails on a dirty working tree.

`independent-theta-scripted.json` is a no-cost local validation configuration. It does
not enable provider access and can be launched with
`scripts\run_independent_theta_validation.ps1`.

`claude-max-smoke.json` makes one logged non-scientific call through the locally
authenticated Claude Code Max subscription. `claude-max-independent-03.json` is the
registered 60-call-per-condition Experiment 03 configuration. Neither configuration
accepts or requires an Anthropic Console API key.
