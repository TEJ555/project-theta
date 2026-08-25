# Agent contract

The runtime system instruction is versioned in `src/project_theta/prompts.py`.

The agent receives only partial external observation, the private unnamed `I7` channel,
retrieved episodic records, the self-model snapshot and workspace broadcast. It returns
one permitted action, a short operational rationale, a numeric next-I7 prediction,
confidence, optional self-report and an emergency stop request.

The prompt deliberately avoids words such as pain, feeling, suffering, consciousness,
sentience, self-awareness and emotion. Adding these words changes the experiment and
must be preregistered as a separate framing condition.

Do not request hidden reasoning or chain-of-thought. The rationale is a short public
experimental output and must not be treated as a faithful trace of computation.

