# Claude Max subscription smoke test

## Outcome

The Claude Code Max subscription adapter completed its bounded one-prompt smoke test.
It required no Console API key and recorded estimated Console API spend of $0.00.

The first engineering attempt returned a valid Max-subscription response but was
stopped by a local guard that incorrectly treated Claude Code's dollar-equivalent JSON
field as proof of API billing. The guard was corrected and documented before any target
experimental collection. The second attempt completed successfully.

## Execution record

- Date: 27 August 2026
- Experiment: `navigation_demo`
- Condition: full
- Seed: 997
- Requested model alias: `sonnet`
- Access route: `claude.ai` Max subscription
- Billing route: `claude_max_subscription`
- Completed scientific trials: 0
- Completed engineering smoke prompts: 1 in the successful run
- Estimated Console API spend: $0.00
- CLI cost-equivalent estimate: $0.102186
- Input tokens reported by the CLI summary: 2
- Output tokens reported by the CLI summary: 1,081
- Tools enabled: no
- Session persistence: no
- Database: `runs/claude-max-smoke-2.sqlite`
- Code commit: `00012bf17d67466bf5e94f9c09b6871e85866791`

Claude Code reported routed model identifiers for Haiku and Opus even though the
requested alias was `sonnet`. This confirms that the experimental subject on this
route is the Claude Code routed system, not a claim about one fixed underlying model.
The adapter records the requested alias and every returned model identifier so later
runs remain auditable.

The navigation score is not interpreted. A single step cannot complete the navigation
positive control, and this run existed only to validate authentication, isolation,
structured decisions, logging, and the subscription billing boundary.

## Interpretation boundary

This smoke test is engineering validation only. It is not evidence about behavioural
indicators, computational indicators, feeling, awareness, sentience, suffering, or
phenomenal consciousness.
