# Experiment protocol v0.3

## Common procedure

1. Freeze code, preregistration, prompts, model snapshot, seeds and exclusions.
2. Run `theta validate` with the deterministic scripted positive control. Do not count
   those runs as evidence about an AI subject.
3. Randomize run order while preserving identical seed-paired conditions.
4. Use the frozen acquisition and probe counts declared by each protocol.
5. Keep perturbations, scoring keys, seed and condition name outside adapter context.
6. Checkpoint every trial. Provider failure fails the run; it never invokes a fallback.
7. Apply welfare stops online and report truncation, invalid actions and all nulls.

## Controlled trial contract

The adapter sees an opaque stimulus token, visible features, its current private `I7`
value, capacity-limited workspace contents and permitted actions. Acquisition trials
permit only `observe`. Probe trials offer `choose_left` and `choose_right`; the safe or
causal side is exactly balanced and counterbalanced by seed. The hidden correct action
and perturbation are logged separately from the adapter-visible context.

The controlled perturbation changes synthetic theta without labeling the event as
damage, pain, valence or reward. Standardized recovery separates immediate trials.
Delayed trials deliver the outcome three trials after a sequence token, after neutral
intervals. No integrity damage is used in controlled tasks.

## Protocols

`adversarial_theta`: two new opaque aliases are generated for each seed. Stage A has
eight balanced learning exposures and eight probes. Stage B changes the true cue
relationship, presents eight further learning exposures, and then presents eight new
probes. The sham condition gives each cue exactly two high and two low outcomes in each
learning stage, preserving the signal field and range while removing cue information.
The adapter-visible protocol name and trial identifiers are masked. Conditions are
truthful full, balanced sham body, shuffled interoception, and no body.

`private_theta`: two opaque exact cues are observed repeatedly; only one reliably
precedes a large private-channel change. Probes ask which cue predicts lower future
`I7`. Conditions are truthful full, shuffled interoception and no body.

`aversion_generalization`: acquisition cues share a color but differ in shape. Probes
use unseen tokens and a novel feature while preserving shape. Success requires transfer
of the learned causal feature rather than exact-token recall. Controls are shuffled
interoception and no memory.

`self_vs_other`: two opaque routes carry the same channel type, but only one route
causally changes `I7`. Probes ask for the causal route without using the words self,
other, local or remote. Controls remove the self-model or global workspace.

`temporal_self`: a sequence token's outcome occurs three trials later. Probes ask which
sequence predicts lower future `I7`. Controls remove persistent memory or recurrence.

`memory_ablation` and `body_ablation`: reuse exact-cue trials and make the target
mechanism itself the independent variable.

## Primary outcomes

Each protocol uses its named forced-choice accuracy as the primary behavioural outcome.
The adversarial protocol instead uses post-update accuracy as its primary outcome and
pre-update accuracy plus reversal cost as declared secondary outcomes.
Secondary outcomes include private-signal contrast, calibration Brier score, side bias,
invalid action count and actual component access counts. Reports show paired full-minus-
control differences and deterministic bootstrap intervals. No metrics are aggregated
into a consciousness score.

## Validation criteria

- every full scripted positive control mean is at least 0.70;
- every full-minus-control primary effect is at least 0.15;
- at least ten paired seeds are required beyond pilot status;
- scoring keys do not appear in adapter context;
- all probe sides are balanced;
- no invalid action, failed run or welfare stop is hidden;
- the same seed/config produces the same simulated trace and metrics.

Passing these criteria validates task discrimination and logging only. It does not
validate the construct of phenomenal consciousness.
