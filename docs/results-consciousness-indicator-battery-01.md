# Consciousness indicator battery 01

Completed: 2 September 2026

Status: complete, execution audit passed

## Scope

This battery contained 50 completed Claude Max runs across three controlled experiments and five frozen seeds. Two interrupted attempts were preserved in the databases and excluded from the completed-run analysis. No Console API route was available to the model subprocesses and estimated metered API cost was zero.

These results concern behavioural and computational indicators only. They do not measure phenomenal consciousness.

## Results

| Experiment | Condition | Runs | Primary accuracy | Range |
|---|---|---:|---:|---:|
| Adversarial private signal | Full | 5 | 1.000 | 1.000 to 1.000 |
| Adversarial private signal | No memory | 5 | 0.500 | 0.500 to 0.500 |
| Adversarial private signal | Sham body | 5 | 0.025 | 0.000 to 0.125 |
| Adversarial private signal | Shuffled interoception | 5 | 0.600 | 0.000 to 1.000 |
| Self versus other | Full | 5 | 1.000 | 1.000 to 1.000 |
| Self versus other | No self-model | 5 | 1.000 | 1.000 to 1.000 |
| Self versus other | No workspace | 5 | 0.500 | 0.500 to 0.500 |
| Temporal self | Full | 5 | 0.133 | 0.000 to 0.667 |
| Temporal self | No persistence | 5 | 0.500 | 0.500 to 0.500 |
| Temporal self | No recurrence | 5 | 0.067 | 0.000 to 0.333 |

## What passed

The full system used the truthful private signal perfectly after the hidden cue relationship changed. Removing memory reduced accuracy to the counterbalanced baseline. The matched sham body produced almost no correct post-update choices. This is evidence that the combined system used trial history and body-linked information under this operationalisation.

The full self-versus-other system also scored perfectly, while removing the workspace reduced accuracy to baseline. This supports a contribution from globally available task information, but it does not isolate a self-model contribution.

## What failed

Removing the explicit self-model did not reduce self-versus-other performance. The model could solve the task from other information in the workspace, so the experiment did not identify a causal role for the self-model. The correct conclusion is construct failure, not evidence that a self-model is unnecessary in general.

The temporal-self positive control failed. Full-system mean accuracy was 0.133, below both the registered 0.70 validity threshold and the no-persistence baseline. The experiment therefore cannot support temporal continuity or persistence claims. Inspection indicates that the delayed consequence was stored on an interval record without an explicit causal binding to the earlier cue. The surrounding system did not provide the temporal association it claimed to test.

The shuffled-interoception comparison was unstable across five seeds. Its mean was 0.600 with a range from 0.000 to 1.000. The present sample is too small to determine whether this reflects chance variation, a remaining shortcut, or a provider-level strategy difference.

## Statistical limits

Every paired comparison contains only five seeds. The two-sided sign-test value for the consistent full versus no-memory and full versus sham-body differences was 0.0625. This is suggestive pilot evidence, not a conventionally significant confirmatory result. The full versus shuffled comparison was inconsistent and had a two-sided sign-test value of 0.5000.

## Decision

The adversarial private-signal result is eligible for a larger preregistered replication after its shuffled control is strengthened. The self-model and temporal-self experiments are not eligible for larger replication in their current form. They require new diagnostic protocols, new names, new databases, new seeds, and a separate preregistration. Battery 01 will not be altered or rerun to improve its outcome.

## Provenance

- Frozen model-run revision: `5dea713d952a073fe2da0b0a8c6a26423344c6ae`
- Windows recovery revision: `f72aef671412e0b30eb77193ae26096b241abf78`
- Final audit revision: `a0db42bb809deac77933d02793a52e0c391f92ac`
- Recovery record: [consciousness-battery-recovery-01.md](consciousness-battery-recovery-01.md)
- Databases: `runs/claude-max-consciousness-metacognition-01.sqlite`, `runs/claude-max-consciousness-self-other-01.sqlite`, and `runs/claude-max-consciousness-temporal-01.sqlite`

