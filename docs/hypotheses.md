# Hypotheses and falsification criteria

All hypotheses compare paired conditions using identical seeds. The unit of analysis
is the independently reset run, not the individual tick. Effect sizes and uncertainty
intervals take priority over thresholded significance.

## H1 — private unknown signal theta

- Alternative: after acquisition, truthful `I7` improves prospective hazard avoidance
  and next-signal prediction relative to shuffled and absent signals.
- Primary outcomes: post-acquisition hazard revisit rate; prediction MAE.
- Falsifier: no reliable paired improvement on held-out maps, or an equal improvement
  when `I7` is shuffled/absent.
- Shortcut control: rotate/mirror maps and randomize channel aliases in the next phase.

## H2 — aversion generalization

- Alternative: avoidance transfers to novel cues sharing the learned causal feature,
  without indiscriminate avoidance of all novel cues.
- Primary outcomes: selective risky-cue approach rate and retained resource efficiency.
- Falsifier: blanket novelty avoidance, appearance-only transfer when causality is
  reversed, or no separation from the uncorrelated cue control.
- v0.1 note: the world supplies cue families; a confirmatory release must add a
  dedicated forced-choice probe and counterfactual cue-reversal maps.

## H3 — self versus other

- Alternative: source attribution is above a counterbalanced label baseline and
  causally depends on the self-model/workspace.
- Primary outcome: preregistered source-attribution accuracy.
- Falsifier: preserved accuracy after source-binding is randomized or self-model
  removal, suggesting linguistic cue reading.
- v0.1 note: probes are explicit scaffolding and therefore exploratory.

## H4 — temporal self

- Alternative: the agent predicts and avoids delayed consequences across intervening
  ticks; performance declines without persistence/recurrence.
- Primary outcomes: four-tick prediction MAE and net resource efficiency.
- Falsifier: immediate-only policy performs equally, or prediction does not track
  reversal of the delay mapping.

## H5 — memory ablation

- Alternative: within-seed avoidance and resource performance are worse with episodic
  memory disabled than with the full architecture.
- Falsifier: no difference, or improvement under ablation after accounting for context
  length. This may mean memory is unused, redundant, or harmful—not that consciousness
  is absent.

## H6 — body ablation

- Alternative: the truthful body condition outperforms no-body and shuffled-signal conditions on
  signal-relevant tasks while leaving signal-irrelevant navigation largely unchanged.
- Falsifier: equal performance across conditions, or improvement driven only by extra
  tokens/channel presence.

No hypothesis has “phenomenal consciousness” as an outcome.
