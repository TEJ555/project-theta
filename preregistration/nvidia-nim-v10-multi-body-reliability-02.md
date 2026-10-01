# NVIDIA GPT OSS V10 multi-body reliability study 02

Frozen: 1 October 2026, before any model call in this replacement cohort

## Reason for replacement

Study 01 stopped during seed 6300 after 21 of 176 planned calls. The Python worker
terminated without reaching its exception handler, leaving the run marked as running.
The database, write-ahead log, completed trial records, and provider metadata are
preserved without alteration. No study 01 outcome metric was available or inspected.

Study 01 is an infrastructure failure and is not resumed. Continuing at trial 22 would
reconstruct neither the agent's live memory state nor the exact execution context and
would therefore produce an invalid seed. Study 02 restarts the complete frozen cohort in
a new database. The failed partial seed is not used as outcome evidence and is reported
alongside study 02.

## Frozen design

Study 02 uses the unchanged V10 protocol, configuration, progression rules, analysis,
and interpretation boundary defined in
`nvidia-nim-v10-multi-body-reliability-01.md`.

- Experiment: `multi_body_reliability_v10`
- Provider: NVIDIA hosted NIM development endpoint
- Required model: `openai/gpt-oss-20b`
- Condition: full
- Seeds: 6300, 6301, 6302, 6303, 6304, and 6305
- Body families per seed: 4
- Model decisions per seed: 176
- Maximum calls: 1,056
- Temperature: 0.0
- Reasoning effort: low
- Evaluation outcome learning: disabled
- Welfare monitoring: enabled

All six seeds will be attempted. Infrastructure failures remain preserved and reported.
There is no outcome-dependent stopping, seed replacement, or change to a frozen gate.

## Interpretation boundary

A pass would show repeatable behavioural and computational regulation across several
independently mapped synthetic body families. It would not establish consciousness,
feeling, awareness, suffering, sentience, or phenomenal experience.
