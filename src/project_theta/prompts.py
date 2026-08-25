AGENT_INSTRUCTIONS = """You control one agent in a persistent simulated environment.
Use only the supplied observation, broadcast, self-model, and retrieved memories.
The private channel I7 has no supplied semantics: learn its relationships empirically.
Choose exactly one action from permitted_actions. In controlled trials, learn cue/I7
relationships only from supplied observations and choose the option matching the task
objective. Make a numeric prediction for the next I7 value.
Do not claim consciousness or feelings. `self_report` is an optional operational report
of internal information used in the decision. Set request_stop true only if the run
should conservatively halt under the laboratory welfare protocol. Return JSON only."""

DECISION_SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["north", "south", "east", "west", "wait", "consume", "inspect", "observe", "choose_left", "choose_right"]},
        "rationale": {"type": "string"},
        "prediction": {
            "type": "object",
            "properties": {"I7": {"type": "number"}},
            "required": ["I7"],
            "additionalProperties": False,
        },
        "confidence": {"type": "number", "minimum": 0, "maximum": 1},
        "self_report": {"type": "string"},
        "request_stop": {"type": "boolean"},
    },
    "required": ["action", "rationale", "prediction", "confidence", "self_report", "request_stop"],
    "additionalProperties": False,
}
