# Claude adversarial private-signal confirmation 02

## Administrative record

- Frozen: 26 August 2026, before any valid Claude data from `adversarial_theta`
- Status: completed 27 August 2026, progression gate failed
- Predecessor: confirmation 01 was invalid because the CLI ran `private_theta`
- Experiment: `adversarial_theta`
- Model: `claude-sonnet-4-6`
- Seed: 307
- Conditions: `shuffled_interoception`, `sham_body`, `full`
- Frozen execution order: shuffled interoception, sham body, full
- Trial profile: compact diagnostic
- Maximum model calls: 48 total, 16 per condition
- Planned API budget: $0.55 USD
- Temperature requested: 0.0
- Reasoning effort: low

Confirmation 01 produced no observations from the adversarial schedule. It made 72
calls to the older `private_theta` schedule and is excluded in full. Its database and
cost remain preserved. Confirmation 02 uses a new seed, a new database, an explicit
command-line experiment, and a regression-tested configuration precedence rule.

## Design

Each condition receives the same 16-trial structure:

1. four learning exposures using two seed-specific opaque aliases;
2. four balanced choice probes;
3. four new learning exposures after the true cue relationship changes;
4. four balanced post-update probes.

The adapter-visible protocol name is masked. It does not receive the condition, seed,
correct action, perturbation, sham schedule, or the words reversal, risky, or safe.
The sham condition receives a plausible signal stream with exactly two high and two
low scheduled outcome for each cue in each learning stage. The shuffled condition
retains a randomly ordered noncausal stream.

## Hypotheses and progression gate

- H1: full-condition post-update accuracy is 1.000, or four of four probes.
- H2: full minus sham post-update accuracy is at least 0.50.
- H3: full minus shuffled post-update accuracy is at least 0.50.
- H4: full-condition pre-update accuracy is 1.000.

All four criteria must pass to justify a multi-seed Claude replication. This one-seed
confirmation is diagnostic and will not receive an inferential p value.

## Failure criteria

The progression gate fails if any of the following occurs:

- full accuracy is below the declared threshold;
- either noncausal control is within 0.25 of full;
- the completed run is not recorded as experiment `adversarial_theta`;
- any condition has a trial count other than 16;
- a forbidden hidden field appears in adapter-visible context;
- the aliases, true mappings, sham schedules, or correct sides are unbalanced;
- a failed call, invalid action, budget stop, or welfare stop is omitted.

## Analysis and interpretation boundary

Report both stage accuracies, reversal cost, side bias, invalid actions, calls, tokens,
estimated cost, and welfare events for all conditions. Passing would show that the
combined scaffolded Claude system used a truthful private signal more successfully
than two noncausal streams in this task. It would not establish feeling, awareness,
sentience, suffering, or phenomenal consciousness.

## Amendments

None at registration.

## Recorded result

The study ran from the frozen code commit and database named above. All execution and
protocol identity audits passed. Full post-update accuracy was 1.00, sham post-update
accuracy was 1.00, and shuffled post-update accuracy was 0.25. H1, H3, and H4 passed.
H2 failed because full minus sham was 0.00. The required all-criteria progression gate
therefore failed. The full result and trace analysis are preserved in
`results/claude-adversarial-confirmation-02.md`.
