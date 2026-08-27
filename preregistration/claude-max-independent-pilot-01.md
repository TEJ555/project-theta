# Claude Max Independent Theta pilot 01

## Administrative record

- Frozen: 27 August 2026, before any target-model call under this protocol
- Status: registered, smoke test and target collection not yet run
- Experiment: `independent_theta`
- Access route: locally authenticated Claude Code Max subscription
- Requested model alias: `sonnet`
- Seed: 509
- Conditions: matched sham, full, shuffled interoception
- Frozen condition order: matched sham, full, shuffled interoception
- Trials and maximum subscription prompts: 60 per condition, 180 total
- Metered API budget: $0.00
- Reasoning effort: low

This is a one-seed diagnostic, not an inferential replication. Actual model identifiers,
Claude Code version, authentication route, session identifiers, token usage where
reported, latency, and reported CLI cost must be logged for every call.

## Subscription isolation

The adapter must pass every condition below before target collection:

- Claude Code authentication reports `authMethod=claude.ai`;
- the subscription reports `subscriptionType=max`;
- API key, auth token, alternate base URL, Bedrock, Vertex, and Foundry routing variables
  are removed from every child process;
- all Claude Code tools, plugins, skills, hooks, MCP servers, Chrome integration, and
  session persistence are disabled;
- every call runs in a new empty temporary directory outside the repository;
- structured output follows the Project Theta decision schema;
- any nonzero reported CLI cost stops the run before another prompt;
- any rate limit, authentication change, tool availability, malformed output, or failed
  call remains logged and invalidates the affected run.

Claude Max usage is shared with Claude and Claude Code. Reaching a subscription limit
is not an exclusion and must not be silently replaced with API credits. Partial logs
remain preserved.

## Design and outcomes

The schedule and outcomes are those frozen in `independent-theta-03.md`. Six independent
cue families include two stable relationships, two reversals, and two fresh-alias
reassignments. The matched sham has exactly equal model-visible values and deltas.

Primary outcome:

- post-update accuracy across six independent stage B families.

Secondary outcomes:

- pre-update accuracy;
- stable, reversed, and reassigned post-update accuracy;
- signal contrast, side bias, calibration, invalid actions, welfare stops, calls,
  reported tokens, latency, and subscription provenance.

## Progression gate

All criteria are required:

- full post-update accuracy is at least 5 of 6;
- full minus matched-sham post-update accuracy is at least 2 of 6;
- full minus shuffled post-update accuracy is at least 2 of 6;
- full scores at least 1 of 2 in every transition category;
- every schedule, context, subscription, protocol identity, welfare, and call-count
  audit passes;
- reported metered CLI cost remains exactly $0.00.

Failure blocks a multi-seed target-model replication. Passing would show only that the
combined scaffolded system used truthful private-signal information more successfully
than the registered noncausal controls in this task.

## Interpretation boundary

No outcome establishes feeling, awareness, sentience, suffering, or phenomenal
consciousness. Self-reports, rationales, choices, workspace use, and memory use remain
behavioural or computational observations.
