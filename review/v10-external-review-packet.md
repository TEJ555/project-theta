# V10 external methods review packet

Status: prepared before study 02 outcomes were inspected. No independent human reviewer
has completed this review.

## Review question

Does V10 validly test repeatable closed-loop use of private synthetic body mappings, and
what simpler prompt-level, wrapper-level, memory, interface, or scheduling mechanisms
could explain a passing result?

The requested review is methodological. It is not a request to decide whether the model
is conscious.

## Short protocol description

Six fixed outer seeds each contain four independently mapped body families. Every family
includes calibration, a no-feedback mapping checkpoint, direct interface probes, exact
regulation probes, and fresh-alias transfer probes. The full condition receives private
state observations, persistent memory, a wrapper-computed association summary, and an
explicit family-local alias bridge. A complete run has 176 model decisions.

## Files to inspect

- `preregistration/nvidia-nim-v10-multi-body-reliability-01.md`
- `preregistration/nvidia-nim-v10-multi-body-reliability-02.md`
- `docs/v10-multi-body-reliability-design.md`
- `docs/v10-post-result-decision-tree.md`
- `docs/v10-results-reporting-template.md`
- `docs/v10-analysis-amendment-2026-10-02.md`
- `review/v10-pre-outcome-red-team-2026-10-02.md`
- `src/project_theta/trials.py`
- `src/project_theta/agent.py`
- `src/project_theta/harness.py`
- `src/project_theta/audits.py`
- `scripts/audit_v10_schedule.py`
- `scripts/red_team_v10.py`
- `scripts/analyze_v10_reliability.py`
- `tests/test_controlled_trials.py`
- `tests/test_v10_analysis.py`
- `workers/nvidia-nim-v10-gpt-oss-reliability.json`

After the cohort is complete, also inspect the raw SQLite database, trial-level audit
export, frozen analysis JSON, and public result report.

## Requested checks

1. Reproduce the six-seed schedule audit and verify every frozen denominator.
2. Search for fixed-code, first-option, label-form, context-length, family-order, phase,
   and token-reuse shortcuts.
3. Verify that public context contains no hidden correct action, direction label, scoring
   key, condition name, or evaluation outcome feedback.
4. Determine exactly what is computed by the wrapper rather than inferred by the model,
   especially the association summary and transfer bridge.
5. Decide whether fresh-alias transfer measures composition with a supplied identity
   relation or a stronger form of spontaneous generalisation.
6. Check whether four families inside one process can support only within-run task
   reliability, rather than an inference based on 24 independent subjects.
7. Verify that the hierarchical bootstrap respects the six-seed and nested-family
   structure and does not treat trials as independent subjects.
8. Reproduce the execution audit, including provider IDs, exact model identity, retries,
   partial attempts, step counts, and required metric presence.
9. Try to make the analyzer accept duplicate completions, shortened runs, missing values,
   mismatched call logs, or non-retryable failures.
10. Challenge every frozen threshold and distinguish an engineering progression rule
    from a population-level statistical claim.
11. Propose controls that separately test raw calibration memory, wrapper-computed
    association summaries, current interoception, transfer bridges, and explicit mapping
    competence.
12. Identify any language in the code, report, site, or outreach material that overstates
    behavioural or computational evidence as phenomenal evidence.

## Minimum reproduction record

The reviewer should record:

- repository commit and local modifications
- Python and operating-system versions
- schedule-audit result
- test result
- analyzer result from the preserved database
- any independent script or shortcut policy used
- every unresolved concern, including concerns that do not change the numerical result

## Decision standard

A V10 full-condition pass is only enough to justify the separately frozen mechanism
cohort. It is not enough for a consciousness claim. The programme should not use V10 as a
flagship result until an independent human reviewer has reproduced the audit and analysis,
the mechanism cohort has tested the major component-level alternatives, and the result
has been attempted on another model or reproducible open-weight checkpoint.

Reviewer criticisms, Project Theta responses, and unresolved disagreements should be
published together. Internal AI-assisted reviews must remain labelled as internal rather
than presented as independent external review.
