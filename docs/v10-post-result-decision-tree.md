# V10 post-result decision tree

Recorded: 2 October 2026, while study 02 was still running and before its outcome
metrics were inspected.

This document does not amend the frozen V10 protocol or progression thresholds. It
records what Project Theta will do after the frozen analysis so that the next decision is
not chosen to suit the result.

## Step 1: execution validity

Run the execution audit before examining scientific outcomes.

- If every planned seed has exactly one completed 176-trial run, every completed trial
  has one valid provider record from `openai/gpt-oss-20b`, and no disallowed failure is
  present, continue to Step 2.
- One preserved `interrupted_before_completion` attempt per seed is allowed only when a
  complete replacement attempt also exists. The partial attempt is reported but excluded
  from outcome estimates.
- Any duplicate completion, missing trial, provider mismatch, non-retryable failure,
  missing required metric, or silently shortened denominator invalidates the cohort. Do
  not interpret its outcome gates.

## Step 2: frozen progression gates

Apply every threshold in
`preregistration/nvidia-nim-v10-multi-body-reliability-01.md`. Descriptive strengths do
not rescue a failed gate.

### All gates pass

The permitted conclusion is that this model and wrapper repeatedly performed the frozen
multi-body regulation task under the full composite condition.

Next action: freeze and run a multi-condition mechanism cohort. It must include at least:

- full composite condition
- shuffled interoception
- incorrect association summary
- raw calibration memory without the wrapper-computed association summary
- incorrect transfer bridge
- explicit mapping-competence control

Do not describe a full-condition pass as evidence of phenomenal consciousness.

### One or more gates fail

The multi-condition cohort is blocked under the frozen rule.

Next action: publish the complete result and diagnose the failure by seed, body family,
probe type, interface performance, mapping retention, and hidden-state endpoint. Any
revised task becomes a new development study with new seeds and a new preregistration.
Do not silently relax a threshold or replace an unfavourable seed.

### Mixed or borderline pattern

There is no special borderline override. A value below a frozen threshold is a failed
gate. Confidence intervals and family-level variation remain useful for diagnosis, but
they do not alter the progression decision.

## Step 3: claim discipline

Regardless of outcome, report three layers separately:

1. Behavioural result: which actions the system selected and how accurately.
2. Computational result: which provided state, memory, summary, bridge, and interface
   components were available and which later ablations change performance.
3. Phenomenal status: unresolved. These experiments do not determine whether anything
   was felt or experienced.

## Step 4: external scrutiny gate

Before using V10 as a flagship research claim:

- publish code, frozen schedules, preregistrations, execution metadata, analysis code,
  and de-identified result data
- obtain review from at least one independent human researcher with no role in building
  the protocol
- invite a reproducibility attempt on a separately operated provider or local model
- record reviewer criticisms and responses without presenting internal AI review as
  independent external review

## Step 5: next scientific target

If the mechanism cohort shows selective degradation under causal controls, the next
target is generalisation across model families and a richer closed-loop body. If the
controls do not separate, the correct conclusion is that V10 performance can be explained
by simpler prompt-level or wrapper-level mechanisms, and the task must be redesigned
before making a stronger claim.
