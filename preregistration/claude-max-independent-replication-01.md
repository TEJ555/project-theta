# Claude Max Independent Theta replication 01

## Administrative record

- Frozen: 27 August 2026, before any model call on the five replication seeds
- Registration revision: the Git commit containing this document
- Prior diagnostic: seed 509, inspected before this registration
- Experiment: `independent_theta`
- Access route: locally authenticated Claude Code Max subscription
- Experimental subject: Claude Code routed system, requested model alias `sonnet`
- Fresh replication seeds: 607, 719, 823, 937, and 1049
- Conditions: full, matched sham, and shuffled interoception
- Runs: 15
- Trials and maximum subscription prompts: 60 per run, 900 total
- Console API key budget: $0.00
- Reasoning effort: low

The diagnostic seed passed its progression gate with post-update scores of 6 of 6 in
full, 3 of 6 in matched sham, and 4 of 6 in shuffled interoception. Because that result
caused this replication to be run, seed 509 is excluded from fresh-cohort effect
estimates. A separate six-seed contextual summary may be reported and clearly labelled.

## Frozen execution order

Each seed is kept as a complete paired bundle. Within each bundle, the committed
deterministic randomizer gives this order:

| Seed | First | Second | Third |
|---:|---|---|---|
| 607 | Full | Shuffled interoception | Matched sham |
| 719 | Matched sham | Shuffled interoception | Full |
| 823 | Shuffled interoception | Full | Matched sham |
| 937 | Shuffled interoception | Matched sham | Full |
| 1049 | Full | Matched sham | Shuffled interoception |

The worker skips a job only when exactly one completed, non-stopped run already exists
for its seed and condition. An interrupted attempt is preserved as failed and may be
retried once after explicit recovery. A second failure blocks that job. Duplicate
completed jobs, welfare stops, malformed responses, authentication changes, and audit
failures stop the workflow for review.

## Subscription and isolation rules

Every call must record Claude.ai Max authentication, the exact Claude Code version,
the subscription billing route, requested and routed model identifiers, provider usage,
and the CLI dollar-equivalent estimate. Console API credentials and alternate Bedrock,
Vertex, or Foundry routes must be absent from child calls. Tools, plugins, skills, MCP,
Chrome integration, repository access, and session persistence remain disabled.

The dollar-equivalent CLI field is not treated as a Console API invoice. Account-level
usage credits are controlled in Claude settings and are outside the local adapter. A
subscription limit or billing prompt stops the noninteractive worker and preserves
completed jobs for later resumption.

## Outcomes and analysis

The primary outcome is seed-level post-update accuracy across six independent stage B
families. Fresh seeds are the inferential units. The following are reported for full,
matched sham, and shuffled interoception:

- condition means and ranges;
- seed-paired full minus control differences;
- deterministic bootstrap 95 percent intervals;
- exact two-sided sign tests with zero differences omitted;
- the number of seeds with a positive paired full advantage;
- stable, reversed, and reassigned post-update accuracy;
- pre-update accuracy, signal contrast, side bias, calibration, invalid actions,
  welfare stops, provider usage, routed models, latency, and billing provenance.

Five fresh pairs remain a small replication. P values are descriptive and no claim
depends on crossing 0.05.

## Replication progression gate

Every criterion is required across the five fresh seeds:

- mean full post-update accuracy is at least 5 of 6;
- mean full minus matched-sham post-update accuracy is at least 2 of 6;
- mean full minus shuffled post-update accuracy is at least 2 of 6;
- full has a positive paired advantage over each control in at least 4 of 5 seeds;
- mean full accuracy is at least 0.75 in each of the stable, reversed, and reassigned
  transition categories;
- all 15 planned runs complete without a welfare stop;
- all schedule, context, protocol identity, call-count, subscription, and leakage audits
  pass.

Failure blocks mechanism-attribution claims and triggers task or scaffold review. A
pass permits a separately preregistered mechanism-ablation study. It does not establish
consciousness.

## Interpretation boundary

The strongest permitted conclusion is that the scaffolded Claude Code system used
truthful private-signal information more successfully than the registered noncausal
controls in this task. Choices, rationales, memory use, workspace broadcasts, and
self-reports remain behavioural or computational observations. No result establishes
feeling, awareness, sentience, suffering, or phenomenal consciousness.
