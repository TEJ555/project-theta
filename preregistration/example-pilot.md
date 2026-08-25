# Example pilot preregistration - v0.2 infrastructure validation

- Date: 2026-08-25
- Code: Project Theta v0.2.0; schema 2; exact commit recorded at execution
- Adapter: deterministic scripted positive control, not a research subject
- Seeds: 101 through 120, paired across every registered condition
- Scope: six controlled protocols; 340 total runs
- Claim boundary: validates laboratory behaviour only and produces no evidence about
  AI consciousness or about a target model.

## Question

Do the controlled schedules guarantee acquisition opportunities, keep scoring keys
hidden, counterbalance choice sides, and produce the predeclared positive-control
differences when required components are available versus ablated?

## Primary outcomes

- `private_theta`, `memory_ablation`, `body_ablation`: forced-choice accuracy
- `aversion_generalization`: generalization accuracy on held-out cue tokens
- `self_vs_other`: causal source-binding accuracy
- `temporal_self`: delayed temporal-choice accuracy

## Acceptance criteria

- every protocol has 12 blinded probes per seed with six correct-left and six
  correct-right mappings;
- full scripted conditions have mean primary accuracy at least 0.70;
- each predeclared full-minus-control paired effect is at least 0.15;
- each comparison has 20 seed pairs and no missing primary outcomes;
- no scoring key appears in the public task, agent observation, memory event or prompt;
- named ablations remove their mechanism and provenance is complete;
- no failed runs, invalid actions, welfare stops or silent adapter fallbacks.

## Analysis

Report condition means, seed-paired mean differences, deterministic bootstrap 95%
intervals, exact two-sided sign tests and all validity warnings. Do not combine outcomes
into a consciousness score. A failure pauses target-model testing and triggers a code or
protocol review; it is not excluded post hoc.

## Interpretation

Passing this preregistration means the scripted positive control can discriminate the
implemented mechanisms under deterministic conditions. It does not validate the tasks
as measures of phenomenal consciousness and does not establish that a language model
uses the same mechanisms.
