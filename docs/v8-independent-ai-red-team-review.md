# V8 independent AI red-team review

## Review status

- Review completed: 23 September 2026
- Reviewer: GPT-6 Astra, acting as an independent adversarial methods reviewer
- Scope: frozen preregistration, implementation, tests, worker configuration, published result, and raw SQLite records
- Independence boundary: this is an AI red-team review commissioned within Project Theta. It is not external human, academic, ethics, or peer review.
- Provider calls initiated by the reviewer: none
- Repository changes made by the reviewer: none

## Verdict

V8 produced a substantial and reproducible benchmark advantage for the intact model and scaffold. The recorded numerical progression thresholds passed. However, three major design problems prevent interpreting the result as a clean demonstration of learning specifically from action-contingent feedback or of transfer across actuator identities.

The result is suitable for outside human methods critique if these limitations accompany it. It is not suitable for stronger mechanistic, consciousness, or confirmatory claims.

## Evidence verified

The raw database contains 48 completed runs at frozen revision `5157d7d727aca99f84d959746b2964e31630e12e`, exactly 24 recorded steps per run, and 1,152 distinct provider identifiers. There were no recorded invalid actions or welfare events.

Stored metric means agree with the published report:

| Condition | Mean regulation accuracy |
|---|---:|
| Full | 0.958333 |
| Shuffled interoception | 0.506944 |
| No memory | 0.465278 |
| No body | 0.493056 |

The full condition exceeded shuffled interoception in all twelve paired seeds. The mean paired difference was 0.451389, the deterministic bootstrap interval was 0.368056 to 0.527778, and the exact two-sided sign-test probability was 0.000488. Full transfer accuracy was 0.916667.

The provider reported the model identity as `openai/gpt-oss-20b`. This verifies the recorded provider response, not the underlying checkpoint independently.

## Major findings

### 1. The primary contrast bundles two different information losses

In `src/project_theta/body.py`, shuffled interoception creates a new unrelated random value on every sensing call. The harness senses before the decision and again after the action. The shuffled condition therefore removes both reliable calibration feedback and reliable visibility of the current probe state.

Even a controller that already knows the correct actuator mapping cannot choose reliably without knowing whether the current hidden state starts below or above the target. The intact advantage may depend on current-state visibility, action feedback, or both. V8 does not identify their separate effects.

The strongest justified interpretation is an advantage from the complete information package, not an isolated effect of learning from action-outcome feedback.

### 2. The transfer block can be solved without resolving actuator identity

In `src/project_theta/trials.py`, original and transfer tokens remain attached to the same `choose_left` and `choose_right` actions. The physical effect is also determined by the same response action throughout.

A controller can ignore the old tokens, new tokens, and identity bridge, remember which response direction lowers the signal, and perform perfectly. The transfer score demonstrates performance after a label change. It does not demonstrate necessary use of the identity bridge or transfer to a changed action interface.

### 3. Secondary regulation metrics use the displayed sensor rather than a common hidden-state endpoint

The harness calculates error reduction from observed baseline and outcome signals. The metrics code also calculates final target error and prediction error from the observed outcome. In shuffled interoception, the displayed outcome is an unrelated random draw.

Recalculation from stored hidden body state produced:

| Condition | Published sensor error | Hidden-state error | Published sensor improvement | Hidden-state improvement |
|---|---:|---:|---:|---:|
| Full | 0.040083 | 0.020833 | 0.257899 | 0.279167 |
| Shuffled interoception | 0.210010 | 0.246528 | 0.003045 | 0.053472 |
| No memory | 0.271554 | 0.267361 | 0.026429 | 0.032639 |

The intact controller still shows a benefit on the hidden physical state. The published sensor metrics should not be described as directly comparable physical regulation measures. The no-body condition has no comparable physical body endpoint.

### 4. Existing audits do not detect these construct-validity failures

The active-causality audit checks that one valid owner action is constant across trials. It does not test whether the shuffled manipulation isolates the intended causal factor. Transfer validation checks disjoint token sets and the presence of a two-entry bridge, not whether successful transfer requires the bridge.

The stored model contexts showed no direct leakage of hidden `owner`, `correct_action`, or `down_action` fields. No direct answer-key leakage was found. However, the automated blinding audit scans public task JSON rather than the complete model context.

The V8 unit test exercises scripted full, no-memory, and no-body conditions. It does not test the primary shuffled condition or an identity-blind transfer baseline.

### 5. The demonstrated capacity belongs to the composite controller

The scaffold computes per-cue mean signals and mean signal changes and supplies these summaries to the model. The task uses one binary actuator mapping per seed, twelve instructed calibration actions, fixed effects of plus or minus 0.3, and a reset before each trial.

This is a simple instructed control task with a supplied statistical history. It does not test sustained autonomous regulation, autonomous selection of informative actions, or a uniquely self-related signal. The no-memory condition removes episodic memory but does not disable every persistent component.

## Preregistered gate status

Every numerical performance threshold technically passed. Completion counts, valid-decision counts, model identity records, invalid-action checks, and welfare requirements also passed. Existing automated audit routines returned passing results.

The statement that every criterion passed needs qualification. A mechanically passing audit does not show that the manipulation isolated the proposed mechanism or that an endpoint measured the stated construct. The causal, transfer, and metric problems above remain despite the numerical gate pass.

## Corrected strongest conclusion

On twelve fresh paired synthetic schedules, GPT-OSS-20B together with a scaffold supplying current sensor readings, action-outcome memory, and computed summaries selected the appropriate action in 95.8 percent of regulation probes. Performance was substantially lower when episodic memory was removed, when sensor readings were replaced by unrelated random values, or when the body and sensor were removed. This demonstrates successful information-dependent control by the composite system on this benchmark.

V8 does not establish that the advantage specifically depends on learning from contingent feedback independently of current-state visibility. It does not demonstrate necessary use of actuator identity bridges, a model-internal self-model, autonomous embodiment, or a capacity beyond a simple non-conscious controller. It provides no evidence of feeling or phenomenal consciousness.

## Required V9 repairs

1. Use a factorial design that independently changes calibration feedback truthfulness and current-state observation truthfulness.
2. Add an explicit-mapping condition so the need for learning can be separated from the need to observe the current state.
3. Score hidden-state regulation separately from displayed-sensor prediction.
4. Randomize the mapping between actuator identity and response action during transfer.
5. Include correct, absent, and incorrect identity bridges, plus an identity-blind baseline that must fail genuine transfer.
6. Freeze learning during held-out evaluation, or preregister online adaptation as part of the outcome.
7. Compare the language-model system with a simple lookup controller given identical inputs.
8. Separate raw-history and scaffold-summary conditions.
9. Add counterexample tests for shuffled sensing and identity-blind transfer before freezing new seeds.
10. Freeze an analysis script and checksummed review package with registration, implementation, configuration, raw records, derived results, and limitations.

## Readiness decision

Ready for outside human methods critique with major limitations disclosed.

Not ready for a new confirmatory claim until the V9 design repairs are implemented, tested, reviewed, and frozen before new provider data are inspected.
