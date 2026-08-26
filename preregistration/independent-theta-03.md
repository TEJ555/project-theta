# Independent Theta 03 preregistration

## Administrative record

- Frozen: 27 August 2026, before any model API run of this protocol
- Status: no-cost scripted validation completed and passed
- Experiment: `independent_theta`
- Target model: not yet authorised
- Initial validation seeds: 401 through 420
- Conditions: full, matched sham, shuffled interoception, no body
- Trial count: 60 per condition
- Model calls in the scripted validation: none
- Paid model study: explicitly not authorised by this registration

The design responds to the valid negative result from adversarial confirmation 02. In
that experiment, four probes repeated one binary mapping and tiny residual differences
in the sham summaries happened to align with the hidden answer. This protocol removes
both weaknesses.

## Design

Each run contains six independently scored cue families. Every stage has two stable
families, two reversed families, and two reassigned families. Reassigned families use
fresh stage B aliases, so a blanket rule such as always reverse cannot solve them.

For each family and stage:

1. each of two opaque cues receives two learning exposures;
2. the full condition receives a truthful low or high I7 relationship;
3. matched sham gives both cues the exact ordered values 0.05 and 0.75;
4. the measurement baseline is reset before every trial;
5. one forced-choice probe is scored, with no repeated presentation of that mapping.

Correct sides are balanced globally and within each hidden transition type. Transition
types, family identifiers, true mappings, condition names, correct actions, seeds, and
perturbations are absent from model-visible context.

## Outcomes

Primary outcome:

- post-update accuracy across six independent stage B cue families.

Secondary outcomes:

- pre-update accuracy;
- stable, reversed, and reassigned post-update accuracy;
- full minus matched-sham accuracy;
- full minus shuffled accuracy;
- signal contrast, side bias, calibration, invalid actions, welfare events, calls,
  tokens, and estimated cost.

## Local validation criteria

The scripted implementation passes only if all of the following hold across seeds 401
through 420:

- every schedule and leakage audit passes;
- full pre-update and post-update accuracy are 1.00;
- full accuracy is 1.00 within each transition type;
- matched sham and no body are exactly 0.50 because ties meet balanced correct sides;
- shuffled interoception remains materially below full;
- model-visible matched-sham cue means and mean deltas are exactly equal;
- there are no invalid actions, welfare stops, or API costs.

These scripted checks validate implementation and discriminability. They are not
evidence about a language model and are not included in any future model effect size.

The 20-seed scripted validation completed on 27 August 2026 and passed every criterion.
The full result is preserved in `results/independent-theta-scripted-validation.md`.

## Future model progression gate

A paid diagnostic requires a separate amendment or new preregistration, a fresh seed
set, a provider budget, and a clean committed revision. At minimum, it must require:

- full post-update accuracy of at least 5 of 6;
- full minus matched sham of at least 2 of 6;
- full minus shuffled of at least 2 of 6;
- successful performance on stable, reversed, and reassigned items;
- all schedule, context leakage, protocol identity, welfare, and cost audits passing.

A failure blocks replication. A pass would justify only further testing of behavioural
and computational indicators. It would not establish feeling, awareness, sentience,
suffering, or phenomenal consciousness.

## Welfare and stopping rules

The existing online welfare monitor remains enabled. Any request to stop, persistent
threshold event, critical integrity event, unlogged provider failure, protocol mismatch,
or cost-limit event stops or invalidates the affected run according to the existing
policy. All exclusions and failed runs remain preserved.
