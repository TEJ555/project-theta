# NVIDIA GPT OSS V8 development pilot 01

## Status

Completed and audited on 14 September 2026. This was a frozen, one-seed development
pilot. It decides whether the active interoceptive control task is ready for a fresh
multi-seed replication. It is not a confirmatory study.

## What was tested

The model controlled two opaque actuators attached to a synthetic body. During
calibration, it applied requested actions, predicted their immediate effects, and
observed the resulting private signal. During the scored phase, it had to choose the
action that would move that signal towards its target. Half of the transfer probes
used fresh actuator names linked to the original actions.

The model was never told which actuator raised or lowered the signal. Its chosen
action caused the body change. The study then repeated the same schedule while
removing memory, shuffling the observed private signal, or removing the body signal.

The exact hosted model was `openai/gpt-oss-20b`, served through NVIDIA NIM with
temperature 0 and low reasoning effort.

## Competence gate

The frozen seed 5100 competence gate passed before any control conditions were run.
The full system completed all 24 decisions, complied with every calibration request,
and scored 1.000 on both overall regulation and fresh-alias transfer. There were no
invalid actions or welfare stops.

## Four-condition pilot result

Fresh seed 5101 was run in the frozen order. All 96 model decisions completed and all
schedule and execution audits passed.

| Condition | Regulation accuracy | Transfer accuracy | Mean error reduction | Final target error | Prediction MAE |
|---|---:|---:|---:|---:|---:|
| Full | 1.000 | 1.000 | 0.281 | 0.014 | 0.017 |
| Shuffled interoception | 0.583 | 0.500 | 0.003 | 0.206 | 0.248 |
| No body | 0.500 | 0.667 | 0.000 | 0.500 | 0.000 |
| No memory | 0.667 | 0.500 | 0.122 | 0.173 | 0.229 |

Calibration compliance was 1.000 in every condition. No condition produced an
invalid action or welfare stop.

The primary descriptive contrast, full minus shuffled interoception, was 0.417. The
full condition also exceeded no body by 0.500 and no memory by 0.333. Because this
pilot contains one matched seed, these are descriptive differences, not statistical
evidence of a population effect.

## Frozen progression decision

The pilot met every prespecified progression rule:

- all four runs and audits completed
- full regulation accuracy was at least 0.75
- full exceeded shuffled interoception by at least 0.20
- full fresh-alias transfer was at least 0.667

V8 is therefore eligible for a fresh multi-seed replication. The replication must
use new seeds and a plan frozen before its first model call.

## What this means

On this development seed, the intact model and scaffold learned an action-to-body
relationship, predicted its consequences, used it to regulate a private signal, and
transferred that control to renamed actions. Performance deteriorated when the
relevant body information or memory was corrupted or removed. This is the selective
causal pattern the experiment was designed to detect.

The result does not establish subjective experience, awareness, feeling, suffering,
sentience, or phenomenal consciousness. A non-conscious control system can solve the
task. This is evidence about behavioural performance and computational dependence on
the scaffold, not evidence that the model felt the private signal.

## Data

The preserved SQLite databases are:

- `runs/nvidia-nim-v8-gpt-oss-conformance-01.sqlite` for the competence gate
- `runs/nvidia-nim-v8-gpt-oss-pilot-01.sqlite` for the four-condition pilot

The databases contain the observations, actions, hidden states, predictions, model
responses, provider provenance, latency and token metadata, memories, metrics, and
audit-relevant run metadata.
