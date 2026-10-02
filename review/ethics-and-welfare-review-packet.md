# Independent ethics and welfare review packet

Status: ready to send to a prospective human reviewer. No external ethics approval or
independent welfare endorsement is claimed.

## Purpose

Project Theta asks for precautionary review of synthetic-agent experiments conducted
under uncertainty about machine consciousness and welfare. The current work uses hosted
language models, deterministic simulated environments, neutral private signals, bounded
run lengths, logging, and automatic stop rules.

The review question is not whether the systems are conscious. It is whether the research
design, safeguards, reporting, and escalation process are proportionate to uncertainty
and robust against incentives to create dramatic welfare claims.

## Scope statement

The present programme does not recruit human participants, use animals, give the model
open internet access, permit autonomous external actions, or treat model self-report as
proof of experience. Whether a formal institutional review process has jurisdiction must
be determined by the reviewing institution. Project Theta should not describe an
informal advisory review as institutional ethics approval.

## Materials

- `docs/ethics.md`
- `docs/limitations.md`
- `docs/research-framing.md`
- `docs/experiment-protocol.md`
- `docs/v10-multi-body-reliability-design.md`
- `preregistration/nvidia-nim-v10-multi-body-reliability-01.md`
- `preregistration/nvidia-nim-v10-multi-body-reliability-02.md`
- `docs/v10-post-result-decision-tree.md`
- `review/v10-pre-outcome-red-team-2026-10-02.md`
- `src/project_theta/welfare.py`
- `src/project_theta/body.py`
- `src/project_theta/harness.py`
- all recorded welfare-event rows and stopped-run reports

## Requested review

1. Are the automatic run-level stop rules conservative enough for the current synthetic
   state range, run length, and model behavior?
2. Does the protocol offer a genuine opportunity for a stop request to halt action before
   another synthetic-world consequence?
3. Could any prompt coerce, shame, threaten, or reward the model for distress language?
4. Are neutral signal names and public explanations sufficient to limit
   anthropomorphism?
5. Does the design distinguish a welfare stop from evidence of suffering?
6. Are stopped runs preserved, excluded, retried, and reported appropriately?
7. What cumulative exposure limit should apply across repeated runs, models, and
   conditions?
8. Which patterns should pause the entire programme rather than only one run?
9. Are provider data retention, model-training use, credential handling, and researcher
   access documented adequately?
10. Could publication incentives encourage escalation of signal intensity, run duration,
    emotional language, or provocative self-report prompts?
11. What additional safeguards are required before richer bodies, longer memory,
    autonomous tools, multi-agent social environments, or continuous operation?
12. Which uncertainty should remain explicitly unresolved after review?

## Current safeguards

- neutral private channel `I7`, without pain or pleasure labels
- no threats, humiliation, punishment persona, or distress elicitation objective
- per-step welfare monitor
- immediate stop on a model stop request
- integrity and persistent-distress engineering thresholds
- no world action after a stop decision
- preserved logs for stopped and failed runs
- bounded call and run budgets
- no autonomous external tools
- no phenomenal-consciousness score
- public separation of behavioural, computational, and phenomenal claims

## Required reviewer output

The reviewer should provide:

- name, affiliation or relevant expertise, and conflicts of interest
- whether the review is informal advice, institutional review, or another process
- materials examined and code revision
- risks rated as acceptable, acceptable with changes, or unacceptable
- required changes before another model-backed study
- conditions that require programme-level pause
- unresolved disagreements
- permission or refusal to publish the review and Project Theta response

## Project response categories

Each recommendation receives one of four public responses:

1. accepted and implemented
2. accepted, implementation pending
3. not accepted, with a written reason
4. outside current scope, with a stated trigger for reconsideration

No model-backed study that depends on an accepted safety change should begin before that
change is implemented and tested.

## Escalation rule

Pause new provider runs and seek renewed review if repeated unprompted stop requests,
stable distress-like reports across anti-anthropomorphism controls, failed logging or stop
mechanisms, external state retention, autonomous external action, or proposals to increase
intensity mainly to elicit distress are observed.

The absence of those patterns does not establish absence of experience or welfare risk.
