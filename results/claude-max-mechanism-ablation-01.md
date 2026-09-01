# Claude Max mechanism ablation 01

Status: completed and execution-audited

Date completed: 2026-09-01

## Result

All 20 preregistered seed-condition runs completed. The full architecture scored 1.000 on post-update accuracy for every seed. Removing episodic memory, workspace broadcasting, or informative interoception reduced accuracy to 0.500 for every seed.

| Condition | Seeds | Mean | Range | Difference from full |
| --- | ---: | ---: | ---: | ---: |
| Full | 5 | 1.000 | 1.000 to 1.000 | reference |
| No memory | 5 | 0.500 | 0.500 to 0.500 | 0.500 |
| No workspace | 5 | 0.500 | 0.500 to 0.500 | 0.500 |
| No body | 5 | 0.500 | 0.500 to 0.500 | 0.500 |

For each matched comparison, the bootstrap 95 percent interval was 0.500 to 0.500. The two-sided sign-test value was 0.0625 because the preregistered study contained five pairs. There were no welfare stops and no metered API charges. The run used the authenticated Claude Max route.

## Interpretation

The result supports a narrow computational claim. Successful use of the private signal in this task depended causally on informative interoception, accessible memory, and workspace broadcasting. It did not establish consciousness, subjective experience, sentience, or feeling.

The exact 0.500 control scores are consistent with the counterbalanced forced-choice baseline. The clean separation is encouraging, but the sample remains pilot-sized and comes from one model route and one task family. Further tests must use different operational indicators and fresh schedules.

## Audit record

- Planned coverage: 20 of 20 runs
- Completed coverage: 20 of 20 runs
- Trials per run: 60
- Fresh seeds: 1181, 1301, 1423, 1549, 1693
- Conditions: full, no_memory, no_workspace, no_body
- Final execution audit: PASS
- Estimated metered API cost: USD 0.00

These results are behavioural and computational indicators only. They are not phenomenal evidence.

