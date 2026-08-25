# Agent contract

The runtime system instruction is versioned in `src/project_theta/prompts.py`.

The model adapter receives only the current partial observation and a bounded workspace
broadcast. The broadcast may contain retrieved episodic summaries, a self-model update,
recurrence state and learned cue/feature associations when those components are enabled.
Raw hidden body state, scoring keys, condition labels and unbroadcast internal component
state are never model inputs.

The model returns one action from the explicitly permitted set, a short operational
rationale, a numeric next-I7 prediction, confidence, an optional self-report and an
emergency stop request. Controlled acquisition trials permit `observe`; blinded probes
permit `choose_left` or `choose_right`. The navigation demonstration permits movement,
collection, waiting and stopping actions.

The prompt deliberately avoids words such as pain, feeling, suffering, consciousness,
sentience, self-awareness and emotion. Adding these words changes the experiment and
must be preregistered as a separate framing condition.

Do not request hidden reasoning or chain-of-thought. The rationale and self-report are
short public experimental outputs and must not be treated as faithful traces of
computation or privileged evidence of phenomenal consciousness.
