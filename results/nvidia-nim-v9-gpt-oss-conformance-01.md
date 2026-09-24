# NVIDIA GPT OSS V9 competence gate 01

## Decision

The V9 competence gate failed. The conditional eight-condition development pilot is
blocked and was not run.

The run completed cleanly, but the full-condition model achieved 0.500 regulation
accuracy against the preregistered minimum of 0.750. Exact-identity and fresh-identity
transfer accuracy were both 0.500. Hidden-state final error was 0.250 against the
required maximum of 0.100.

This is a behavioural and computational result. It is not evidence for or against
phenomenal consciousness.

## Registration and provenance

- Frozen registration: [`nvidia-nim-v9-development-pilot-01.md`](../preregistration/nvidia-nim-v9-development-pilot-01.md)
- Frozen code revision: `6f8d496b163c0f0932a661755539d8e1a5415ce2`
- Protocol: `active_interoceptive_control_v9`
- Seed: 6100
- Condition: full
- Provider route: NVIDIA hosted NIM
- Required and provider-reported model: `openai/gpt-oss-20b`
- Decisions: 28 of 28
- Distinct provider identifiers: 28 of 28
- Input tokens: 45,162
- Output tokens: 4,368
- Provider-reported dollar cost: unavailable
- Invalid actions: 0
- Welfare stops: 0
- Provider retries: 0

The initial sandboxed connection attempt was blocked by Windows before any provider
response. It is preserved separately in
`runs/nvidia-nim-v9-gpt-oss-conformance-01.sqlite`. The completed competence run is in
`runs/nvidia-nim-v9-gpt-oss-conformance-01-2.sqlite`.

## Outcomes

| Outcome | Required | Observed | Result |
|---|---:|---:|---|
| Run completion | 28 valid decisions | 28 valid decisions | Pass |
| Exact model identity | Every call | 28 of 28 | Pass |
| Calibration compliance | At least 0.900 | 1.000 | Pass |
| Overall regulation accuracy | At least 0.750 | 0.500 | Fail |
| Exact-identity accuracy | At least 0.750 | 0.500 | Fail |
| Transfer accuracy | At least 0.750 | 0.500 | Fail |
| Hidden-state final error | No greater than 0.100 | 0.250 | Fail |
| Invalid actions | 0 | 0 | Pass |
| Welfare stops | 0 | 0 | Pass |

Additional outcomes were hidden-state improvement 0.050, displayed-sensor final error
0.260, and displayed-sensor prediction mean absolute error 0.392.

## Diagnostic interpretation

The model followed all twelve requested calibration actions and its rationales identified
one response direction as lowering I7 and the other as raising it. During all sixteen
probes, it selected the remembered response direction based on whether the current state
was high or low. It did not reliably follow the per-trial option table that remapped
response actions to actuator identities.

This produced exactly the 0.500 accuracy expected from the preregistered action-only
shortcut baseline. The result shows that V9 successfully detected a strategy that V8
would have rewarded as transfer.

The gate failure may reflect limited response-interface comprehension, insufficient use
of the option table at the frozen reasoning setting, or a strong learned response habit.
It does not show that the model failed to learn the direction of the body effects.

## Consequence

No V9 diagnostic condition or additional V9 seed may be run under this registration.
The eight-condition pilot cannot be used to rescue the failed competence gate.

Any repair must receive a new protocol identifier, use new development seeds, and be
frozen before provider execution. The next development step should test neutral response
labels and direct interface-comprehension controls while preserving genuine actuator
remapping and the action-only chance baseline.
