# Endogenous agency V7 development record

## Why V7 exists

V6 used a generic probe instruction that asked for the source most causally associated
with change. Half of the probe payloads instead requested the source independent of
forced commands. This conflict made model behaviour dependent on which part of the
prompt it followed. V7 preserves V6 unchanged for reproducibility and introduces a new
protocol identifier with relation-aligned wording.

Every V7 probe defines both permitted relations:

- `tracks_forced_commands` requests the source with stronger dependence on forced
  issued commands;
- `independent_of_forced_commands` requests the source with weaker dependence on
  forced issued commands.

The wording supplies the task definition, not the correct source or answer side.
Opaque labels, held-out aliases, counterbalanced sides, balanced requested relations,
delayed outcomes, and the hidden causal assignment remain unchanged.

## Validation

Three fresh schedule audits passed. The audit now contains an explicit
`relation_aligned_instruction` check so the contradiction cannot silently return.
The deterministic causal baseline scored 1.000 with truthful state and 0.000 when the
journal was covertly permuted.

The first exact-model development run used NVIDIA hosted `openai/gpt-oss-20b`, strict
JSON Schema output, low reasoning effort, seed 3101, and the full condition. It
completed all 18 decisions and passed the execution audit. Transfer accuracy was
0.500 and authored-state accuracy was 0.167. It failed the registered competence
threshold of 0.70 and was not scaled.

## Interpretation

Correcting the wording removed one validity threat but did not make the model learn
the intended causal state. The raw acquisition format still asks a language model to
aggregate a large nested table of delayed records in one call. Near-zero authored-state
accuracy means later choices cannot be interpreted as the use of a learned self-model.

V7 is therefore a useful negative development result. It is not evidence against
machine consciousness. It shows that this benchmark does not yet provide a reliable
measurement instrument for the proposed indicator.

## Requirement for the next protocol

The next protocol should expose causal evidence through sequential interaction rather
than a single arithmetic-heavy record table. The agent should choose interventions,
observe delayed changes in a private body variable, and demonstrate regulation in a
fresh environment. The analysis should separately score:

- acquisition of the action to body causal mapping;
- prospective prediction of private-state change;
- active regulation under perturbation;
- transfer to fresh action aliases;
- degradation under shuffled interoception, memory removal, and yoked actions.

Only a protocol with a reliable positive control and selective ablation effects should
advance to model-family replication or outside methods review.
