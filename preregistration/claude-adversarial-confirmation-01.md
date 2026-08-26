# Claude adversarial private-signal confirmation 01

## Administrative record

- Frozen: 26 August 2026, before any Claude data from this protocol
- Status: registered locally, not yet run
- Experiment: `adversarial_theta`
- Model: `claude-sonnet-4-6`
- Seed: 209
- Conditions: `sham_body`, `full`, `shuffled_interoception`
- Frozen execution order: sham body, full, shuffled interoception
- Maximum model calls: 96 total, 32 per condition
- Planned API budget: $0.95 USD
- Temperature requested: 0.0
- Reasoning effort: low

The no-body condition is excluded from this bounded confirmation because the previous
Claude replication already placed it at chance and the immediate question concerns
truthful versus noncausal private streams. It remains present in local validation and
must return in a later multi-seed replication.

## Design

Each condition receives the same 32-trial structure:

1. eight learning exposures using two seed-specific opaque aliases;
2. eight balanced choice probes;
3. eight new learning exposures after the true cue relationship changes;
4. eight balanced post-update probes.

The adapter-visible protocol name is masked. It does not receive the condition, seed,
correct action, perturbation, sham schedule, or the words reversal, risky, or safe.
The sham condition receives a plausible signal stream with exactly two high and two
low outcomes for each cue in each learning stage. Its signal therefore contains the
same field and numerical range as the full condition but no cue-discriminating
relationship. The shuffled condition preserves the older random-signal control.

## Hypotheses

- H1: full-condition post-update accuracy is at least 0.875, or seven of eight probes.
- H2: full minus sham post-update accuracy is at least 0.25.
- H3: full minus shuffled post-update accuracy is at least 0.25.
- H4: full-condition pre-update accuracy is at least 0.875.

All four criteria must pass to justify a multi-seed Claude replication. This one-seed
confirmation is a diagnostic pilot and will not receive an inferential p value.

## Failure criteria

The confirmation fails its progression gate if any of the following occurs:

- full accuracy is below the declared threshold;
- either noncausal control is within 0.25 of full;
- a forbidden hidden field appears in adapter-visible context;
- the aliases or correct sides are unbalanced;
- a failed call, invalid action, budget stop, or welfare stop is omitted;
- implementation or prompt changes are made after observing a result without a dated
  amendment and a new confirmation database.

A failed gate is scientifically useful. It means the task still permits a shortcut,
the full signal is insufficient, or this operationalization does not discriminate the
conditions for this model.

## Analysis

Report all three condition accuracies for both stages, reversal cost, side bias,
invalid actions, calls, tokens, estimated cost, and welfare events. Inspect every
adapter-visible context for forbidden fields. Do not pool this seed with the earlier
pilot or replication.

## Interpretation boundary

Passing would show that the combined scaffolded Claude system used a truthful private
signal more successfully than two matched noncausal streams in this task. It would not
show feeling, suffering, awareness, sentience, or phenomenal consciousness.

## Amendments

None at registration.
