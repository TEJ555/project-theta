# Project Theta review, 6 September 2026

**Recommendation: prioritise a shortcut-resistant, information-matched experiment before scaling the programme. Then validate a cheaper execution protocol and obtain external replication.** The foundation is useful, but current positive results admit much simpler explanations than the intended architecture claims.

This review inspected the research code at revision `837b88e`, preregistrations, reports, two completed SQLite datasets, relevant task history, and the website source. All 48 existing unit tests passed. No provider calls were made, no research source or historical data was changed, and no active experiment was interrupted. Website SEO work was already underway in the separate task “Build Project Theta scaffold.” This is a source and evidence review, not a full browser or deployment audit.

Research checkout: `C:/Users/jason/Documents/Codex/2026-08-25/referenced-chatgpt-conversation-this-is-an/outputs/project-theta`.

## 1. Highest priority: remove a demonstrated answer-position shortcut

`src/project_theta/trials.py:92` assigns the correct answer side using `(index + seed) % 2`. The public task includes the indexed trial ID (`trials.py:47,103`). All ten registered self-model v3 confirmation seeds are odd. Consequently, **choose right on even-numbered probes and left on odd-numbered probes** scores **120/120** across those ten planned schedules, without using the body, memory, self-model, cue meanings, or model inference.

The same rule scores **72/72** across the six registered temporal-binding v2 replication schedules. These are offline schedule checks, not new model results. The v3 schedule audit nevertheless returns `pass`. The assignment rule was also present in the first-tranche frozen revision `3131694`.

This demonstrates an available shortcut. It does **not** establish that Claude exploited it, or erase the observed differences between conditions. It does prevent treating the task as successfully ruling out metadata-only strategies.

Recommended next change: use a separately seeded, shuffled balanced side schedule whose answer assignment is independent of public probe index and acquisition ordering. Hide unnecessary schedule identifiers from model input. Hiding IDs alone is insufficient if tick or order reveals the same pattern. Add parity, alternation, order, token and metadata-only strategies to the audit. Test these over a large fixed set of local seeds before spending model calls.

Preserve the current data and original preregistrations; record this limitation in their interpretation. Do not silently repair the task mid-study or merge a repaired task into the existing confirmation. Defer additional large runs under the affected design until this issue is addressed.

## 2. Distinguish supplied answers from architectural benefit

The self-model receives the simulator's `owner` annotation via `harness.py:269`. `SelfModel.update()` converts it into a numeric per-cue `source_bindings` table (`components.py:94 to 98`). The LLM receives that table through the workspace and is instructed to select the self-associated route. Removing the self-model removes the informative table.

A deterministic lookup of the highest source-binding value, using only logged model-visible context, scores **60/60** on the full condition's completed tranche-one probes. The same reader defaults to the left option when the table is absent and scores **30/60** in each ablated condition. Actual Claude scores were full **1.000**, no self-model **0.417**, and no workspace **0.500**, each over five runs.

Thus an ordinary table reader reproduces the major separation. The finding supports successful use of supplied source information; it does not yet show an advantage of a specialised self-model over another representation of the same information. This is an intentional implemented pathway, not evidence of accidental raw-owner exposure in the public memory.

Recommended next comparison:

- Full architecture with the current source representation.
- The same source information available through a generic table or memory representation, with access, context length, and computation matched as closely as possible.
- A representation of equal size with source associations permuted, to test dependence on correct content.
- A deterministic lookup/associative baseline, clearly identified as a computational baseline.

If the question is whether the agent can *infer* ownership, provide ambiguous action/outcome evidence and test new mappings rather than directly supplying ownership labels. Treat that as a new task with new predictions.

Workspace ablations have a related limitation: average logged context size in tranche one was **9,303 characters** for full and **869** for no workspace. Removing the workspace removes most accumulated information. Padding alone would address size, but not informational access. A generic information-matched channel is the more decisive control.

## 3. Largest speed opportunity: avoid unnecessary inference in a new protocol

The completed self-model tranche contained 15 runs × 60 calls = **900 calls**:

| Phase | Calls | Median call latency | Total recorded call time |
|---|---:|---:|---:|
| Acquisition / observation | 720 | 24.62 seconds | 5.14 hours |
| Scored probes | 180 | 24.91 seconds | 1.24 hours |

Acquisition has only one permitted action, `observe`. The simulator controls the perturbation and Python builds the memories and source bindings. Each call launches a fresh Claude Code process with session persistence disabled. This makes observation-only inference the strongest optimisation candidate.

A probe-only version would reduce this tranche's calls from **900 to 180: 80% fewer calls**, with an idealised inference-time reduction of about fivefold at these measured latencies. This is a design estimate, **not a measured end-to-end speedup**. Subscription pauses, startup work and failures are excluded from the timing totals.

Skipping calls is not automatically equivalent. Acquisition decisions include predictions and stop requests; previous predictions can enter later context. A new protocol must explicitly define which state updates, welfare opportunities and measured outcomes change. Compare retained probe inputs and outcomes on development seeds, preserve relevant safeguards, and freeze the new protocol before collecting its target data. Do not retrofit it into the running confirmation.

Further priorities: report calls per scored probe, successful-call latency, retry waste and elapsed wall time automatically; shorten unnecessary output fields only in a new protocol; benchmark a direct, version-pinned model adapter after compatibility checks. Add bounded parallelism only across independent runs once checkpoint ownership and provider limits are understood. Parallelism reduces waiting but does not reduce total calls or improve validity.

## 4. Fix model identification before cross-model claims

The worker requests the alias `sonnet`. In all 900 completed tranche-one calls, the stored `actual_models` list contains both `claude-haiku-4-5-20251001` and `claude-opus-5[1m]`. The temporal replication reports the same two entries in its 648 calls. The adapter records `temperature_applied: null`, even though the requested setting is zero.

These are reported usage identifiers; the logs alone do not establish the exact role each model played. Describe this evidence as **the recorded Claude Code routed system**, and disclose requested selector, returned model entries, CLI version, reasoning settings and unapplied temperature. Do not present it as a verified isolated Sonnet-at-temperature-zero experiment.

For a future comparison, require an approved actual-model identity or flag a deviation before continuing. Prefer exact model versions where the provider supports them. Claude's documentation confirms that aliases select current models and distinguishes them from full model names: [CLI reference](https://code.claude.com/docs/en/cli-usage).

## 5. Make the public research record current and reproducible

The website source still describes the 50-run indicator battery as running, although `docs/results-consciousness-indicator-battery-01.md` records completion on 2 September. That report contains scientifically important failures: self-model removal initially did not matter, and the first temporal positive control failed. The homepage also calls mechanism attribution passed while a later paragraph describes that same study as the next experiment. Its test count is 40; the current suite has 48.

Publish the failed controls and revisions alongside the positive stories. Maintain one dated study registry feeding both README and website: protocol version, status, number of completed seed pairs, actual backend, report, deviations and reproducible data location. SEO metadata alone will not correct contradictory research status.

Raw databases are intentionally ignored by Git. That is sensible for working files, but the reviewed tree lacks a complete public analysis bundle for the recent studies. Create a reviewed export containing per-seed outcomes, appropriate model-visible inputs/responses, failure records, code and prompt hashes, frozen analysis, and data checksums. Verify that another person can regenerate the tables without making model calls. Do not publish raw provider metadata without checking it for identifiers or sensitive content.

The website and research code live in different folders and repositories. Add a short root-level project map and one current decision log so future work starts from the right checkout and latest evidence. A complete engineering reorganisation is unnecessary.

## Suggested order of work

1. **Now:** record the shortcut and interpretation limits; preserve all existing results; reconcile the public status. Review the active study's continuation in its owning task rather than silently changing it here.
2. **Next development cycle:** repair schedule predictability, add adversarial baselines, design the information-matched comparison, and validate a reduced-call protocol locally.
3. **Next model pilot:** test whether the revised question is discriminating on fresh development seeds. Keep failures and redesign history separate from confirmation.
4. **Before scaling:** ask an external methods reviewer to attack the protocol and reproduce the exported analysis. No outreach was sent during this review.
5. **Then:** freeze a confirmatory sample size and analysis around a meaningful effect; test a second independent model family on the corrected task. Keep development/model-selection data separate from confirmation. Analyse seed pairs as clusters rather than treating every within-run probe as an independent model replication.

Defer a larger simulation world, more indicators, a hosted commercial platform, and large batches of additional models until one central claim survives these checks. A clear null result against an information-matched baseline is also a useful outcome.

The next meaningful milestone should be: **an outside reviewer can reproduce one well-defined finding and cannot explain it using an obvious information-access or scheduling shortcut.** That is a stronger basis for a paper, collaboration or funding pitch than a larger count of completed calls.

The theory-inspired framing remains appropriate. Butlin and colleagues formulate computational indicators derived from consciousness theories, rather than a behavioural proof of experience: [Consciousness in Artificial Intelligence](https://arxiv.org/abs/2308.08708). Nothing in this review turns the current task effects into evidence of subjective experience.

## Reproduction and limits

`review/reproduce_review.py` reproduces schedule shortcuts, the existing audit result, completed-run summaries, call timings, model entries and the source-table baseline. `review/evidence.json` contains this review's output. It opens only the two completed databases, refuses databases with WAL files or running rows, and does not invoke providers. The second tranche's planned schedules were checked, but its active database and incomplete outcomes were not analysed.

The parity strategy is a diagnostic discovered during review, not a preregistered baseline or evidence of the model's actual reasoning. The lookup strategy evaluates recorded contexts rather than simulating a new agent trajectory. Public dataset availability and deployed website behaviour were not independently verified. Findings about website content refer to the inspected local source, which another task was editing concurrently.
