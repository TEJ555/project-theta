# Methods correction: answer-position and information-access confounds

Published: 6 September 2026

Status: all affected studies are retained as development evidence. No additional runs will be added under the affected design.

## What was found

A model-assisted methods review identified a deterministic relationship between the public probe identifier and the hidden correct answer side. In the registered self-model v3 schedules, a rule that chose right for even-numbered probes and left for odd-numbered probes scored 120 out of 120. The same rule scored 72 out of 72 in the registered temporal-binding v2 schedules.

This does not show that Claude used the shortcut. It shows that the design did not rule it out.

The review also showed that the full self-model condition received a source-binding table built from simulator ownership annotations. A deterministic table lookup reproduced the main separation between full and ablated conditions. Removing the self-model or workspace also removed task-relevant information and substantially shortened the context.

The supported conclusion is therefore narrower than previously stated: the routed Claude system used supplied source information successfully. The study does not isolate a benefit from a specialised self-model and does not show that ownership was inferred from experience.

## Affected record

- Self-model binding v3 pilot and confirmation are development studies.
- Confirmation tranche one remains complete and unchanged.
- Confirmation tranche two stopped after eight of fifteen planned runs. The eight completed runs are retained. The remaining seven will not be collected.
- Temporal-binding v2 and other earlier forced-choice studies using the same public identifier and answer-side generator require the same limitation when interpreted.
- Original preregistrations, databases, reports and code revisions remain preserved.

Nothing in these studies is evidence of phenomenal consciousness.

## Repair

Version 4 is a new protocol with new seeds and a new database. It:

- removes trial identifiers from model-visible tasks;
- uses a separately seeded, shuffled and balanced answer-side schedule;
- audits fixed-side, public-order parity, lexical and token-length strategies over 2,400 probes;
- gives full and generic conditions byte-identical model-visible binding-register inputs;
- adds misattributed and permuted wrong-content controls with the same schema and entry count;
- uses model inference only for the twelve scored probes;
- keeps protocol-defined acquisition updates and welfare checks on all sixty steps;
- records model calls and skipped inference separately; and
- can fail a confirmatory run when the provider-reported model identity differs from a frozen requirement.

## Remaining limitation

V4 still supplies wrapper-computed ownership associations. It tests representation and information-access explanations. It does not yet test whether an agent can infer ownership from ambiguous action and outcome evidence. That inference task is a separate future protocol and requires its own predictions and validation.

The Claude Max route must be described as a Claude Code routed system. It is suitable for development, but not for a claim about one isolated model version. Confirmation should use an exact provider model version or a reproducible open-weight runtime.
