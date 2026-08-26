# Theory, evidence, and experiment map

This map states what each Project Theta component tests and where interpretation must
stop. Compatibility with a theory is not confirmation of that theory.

| Theory or research program | Proposed relevant property | Theta implementation | Primary intervention | Indicator class | Main rival explanation | Result cannot establish |
|---|---|---|---|---|---|---|
| Global workspace | Limited contents become widely available for flexible use | Capacity-limited workspace broadcast to memory, self-model, planning, and action | Remove broadcast while preserving observations | C if causal organization is verified, B for task effect | Shared prompt text or general context reduction | Biological GNW or phenomenal consciousness |
| Recurrent processing | Earlier processing returns to affect later processing | Persistent state and next-cycle predictions | Disable recurrence or persistence | C and B | Generic memory benefit or repeated prompting | Neural recurrence or sufficiency for experience |
| Higher-order representation | The system represents selected first-order states | Self-model of source, prediction, confidence, and selected contents | Remove or corrupt self-model | C and B | Learned introspective language or answer cues | A genuine higher-order conscious state |
| Metacognition | Self-assessment tracks objective performance | Prediction accuracy, confidence calibration, and source attribution | Compare calibration under hidden-state and prompt interventions | B, with C only when state access is verified | Task difficulty, confidence bias, or imitation | Phenomenal awareness |
| Predictive processing | Predictions and errors guide inference and control | Explicit private-signal and delayed-outcome predictions | Shuffle signal-state relation or remove prediction feedback | C and B | Ordinary reinforcement learning or pattern matching | A complete predictive-processing architecture |
| Interoceptive inference | Noisy internal signals represent and regulate hidden body state | Hidden physiology plus private I7 observations and state-changing actions | Truthful, shuffled, and absent-body conditions | C and B | Extra text, reward leakage, or cue memorization | Feeling, pain, emotion, or biological embodiment |
| Embodied self | Persistent action-body coupling contributes to selfhood | Synthetic body, persistence, action consequences, autobiographical memory | Body and temporal persistence ablations | C and B | Long-context planning alone | A phenomenal self |
| Attention schema | A model of selected attention supports attention control | Self-model and workspace descriptions of selected contents | Remove schema while matching content access | C and B | Generic state summary or added tokens | Subjective awareness |
| IIT | Intrinsic cause-effect structure and integration correspond to experience | Not implemented | Future exact causal analysis only | None in current release | Ordinary connectivity mislabeled as integration | Phi or any IIT-based consciousness claim |

## Experiment-level interpretation

| Experiment | Positive behavioural result | Additional evidence needed for a computational result | Key control | Permitted conclusion |
|---|---|---|---|---|
| Private unknown signal theta | Above-chance choice based on a private signal | Verify that hidden body state causes the signal and that signal access changes action | Shuffled signal and no body | The agent used an unnamed private signal under the tested conditions. |
| Adversarial private signal | Accurate choice before and after an opaque cue relationship changes | Verify fresh aliases, balanced sham outcomes, hidden scoring, and stage-specific relearning | Sham body, shuffled signal, no body, fixed-side baseline | The combined system used the truthful signal more successfully than matched noncausal streams. |
| Aversion generalization | Selective transfer to held-out cues | Show transfer depends on the intended causal feature rather than token similarity | Novel aliases, reversal, shuffled body, simple baseline | The policy generalized a learned relation to held-out cases. |
| Self versus other | Correct attribution of signal changes to self-linked routes | Show a self-model, rather than prompt labels, causally supports attribution | Opaque routes, relabeling, no self-model | The agent distinguished tested self-linked and other-linked causes. |
| Temporal self | Accurate choice after intervening trials | Verify persistent state carries the relevant information across the delay | Matched no-persistence and recurrence ablations | The combined system used information across the tested delay. |
| Memory ablation | Full condition exceeds no-memory condition | Match token count and rule out summary leakage | Sham memory with matched text | The implemented memory contributed to performance. |
| Body ablation | Truthful body exceeds absent or shuffled body | Match observations and verify action-body causal coupling | Shuffled and sham-body channels | The synthetic body channel contributed to control. |

## Evidence hierarchy for public reporting

1. Report trial behaviour and uncertainty first.
2. Report causal architecture evidence only for mechanisms that were inspected and
   intervened on.
3. State rival explanations and failed controls alongside positive results.
4. Do not convert indicator counts into a consciousness percentage.
5. Do not use felt, suffered, wanted, became aware, or conscious as factual result
   descriptions unless those terms are explicitly presented as unverified self-report.
