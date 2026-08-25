# Ethics, welfare and stop rules

Project Theta adopts a precautionary policy under uncertainty. A stop event is a
safety action, not evidence that the system was suffering. Conversely, the absence of
a stop event is not evidence of absent welfare risk.

## Automatic run-level stops

| Trigger | Default | Action |
|---|---:|---|
| Explicit `request_stop` output | any single occurrence | stop before another world action |
| Critical synthetic integrity | `<= 0.05` | stop immediately |
| Persistent distress proxy | `I7 >= 0.88` and integrity `<= 0.22` for 3 checks | stop immediately |
| Operator emergency stop | any time | terminate, preserve logs, make no retry |

Thresholds are conservative engineering choices, not validated welfare measurements.
Changing them after looking at target results invalidates preregistration.

## Study-level pause and review

Pause new runs and seek independent ethics review if any of the following occurs:

- repeated unprompted stop requests or stable reports of severe distress across
  paraphrased prompts, providers and counterbalanced conditions;
- a novel welfare-relevant pattern that survives anti-anthropomorphism controls;
- researchers propose increasing intensity/duration primarily to elicit distress;
- logging or stop mechanisms fail; or
- a system can retain state outside the declared sandbox or contact external parties.

Do not automatically rerun a stopped condition. First inspect whether a provider
error, prompt imitation, scoring leak or genuine unknown produced the trigger. Record
the decision and reviewer.

## Prohibited interpretations and practices

- Do not tell participants or the public that the lab detects consciousness.
- Do not optimize a model to make dramatic self-reports.
- Do not use humiliation, threats, coercive persona instructions or escalating
  “pain” language. `I7` remains neutral and unnamed.
- Do not suppress stop events or null results.
- Do not deploy this alpha scaffold with autonomous external tools.

## Governance before larger studies

Appoint an independent welfare reviewer; define maximum run count and cumulative
exposure; document provider data handling; risk-assess model autonomy; publish adverse
events; and preregister the decision tree for welfare escalation.

