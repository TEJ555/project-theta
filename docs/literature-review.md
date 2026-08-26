# Scientific foundations for Project Theta

## A systematic scoping review of consciousness theories, artificial-system indicators, and research safeguards

Review version 1.0, 26 August 2026

## Abstract

Project Theta is a prototype laboratory for testing functional properties that some
scientific theories associate with consciousness. This review asks which properties
can be operationalized in artificial systems, how strongly the literature supports
them, which confounds limit interpretation, and which safeguards are justified under
uncertainty. Five database search families retrieved 1,916 records. Deduplication left
1,800 unique records. A deterministic ranking supported single-reviewer screening,
targeted verification, and citation chaining. The version 1.0 corpus contains 47
sources, including theory papers, empirical studies, methodological criticism,
AI-specific indicator work, and welfare proposals.

There is no accepted scientific test for phenomenal consciousness and no agreed list
of necessary and sufficient conditions. Global workspace, recurrent processing,
higher-order, integrated information, predictive and interoceptive, and attention
schema approaches nevertheless make claims that can inspire discriminating functional
tests. Across these families, recurring research targets include recurrent processing,
global availability, metacognitive representation, causal integration, predictive
control, persistent self and body models, and attention control. The evidence does not
justify adding these targets into a consciousness score. Behaviour can be produced by
prompt compliance or learned policy, self-report can be imitated, and a software module
can carry a theory-derived name without implementing the proposed mechanism.

Project Theta should therefore be understood as an indicator and method-development
lab. Its strongest possible conclusions concern behavioural indicators and verified
computational indicators. It cannot establish the presence or absence of phenomenal
consciousness. The review supports matched ablations, blinded probes, explicit leakage
audits, preregistration, conservative language, and precautionary welfare stop rules.

## 1. Review question and scope

The central question is not whether a persuasive chatbot sounds conscious. It is
whether an artificial system implements and causally uses properties that live
scientific theories treat as relevant to consciousness. The review therefore covers:

1. major empirical theory families;
2. measurement and construct-validity problems;
3. attempts to transfer theory-derived indicators to artificial systems;
4. embodiment, interoception, self-model, and temporal persistence;
5. research ethics and welfare under uncertainty.

The full protocol, exact searches, raw metadata, screening aid, evidence table, and
checked bibliography are part of the repository. The review does not attempt a
meta-analysis because the included work has no common intervention, population, or
outcome. It does not estimate a probability that any tested system is conscious.

## 2. Methods

The protocol was frozen on 26 August 2026 after preliminary searches and after Project
Theta's first experiments. This timing matters. The review can evaluate and revise the
lab, but it cannot act as prospective justification for experiments that had already
run.

Searches covered PubMed, Crossref, OpenAlex, Semantic Scholar, and arXiv. Five search
families addressed consciousness theory, artificial systems, embodiment and
interoception, measurement validity, and welfare. Semantic Scholar rate-limited all
queries. Crossref's broad matching produced very large and noisy total counts. The
review retrieved at most 100 results per family and provider, so it is systematic and
reproducible but not exhaustive.

DOI and title normalization removed 116 duplicates from 1,916 retrieved records. A
deterministic ranking ordered all 1,800 unique titles for inspection. The primary
reviewer assessed the first 100 candidates and used backward citation searching,
review bibliographies, PubMed records, arXiv records, and targeted searches to recover
seminal and recent work. Forty-three DOI records were checked against Crossref. Four
AI-specific preprints were checked against arXiv.

This version has one primary reviewer. Before academic submission, a second reviewer
should independently screen the ranked candidates, audit a random sample of lower
ranked records, and resolve disagreements. That limitation is substantive, not a
formality.

## 3. What the field agrees on

The literature supports a small set of relatively stable statements.

First, consciousness is not identical to intelligence, language ability, task
performance, or human-like conversation. A system can display sophisticated behaviour
without that behaviour deciding whether the system has subjective experience.

Second, the term consciousness covers different targets. These include wakeful state,
the content of a current experience, global access to information, metacognitive
awareness, self-consciousness, and phenomenal experience. A test for one target cannot
quietly become evidence for all of them.

Third, there is no consensus theory. The review by [Seth and Bayne
2022](https://doi.org/10.1038/s41583-022-00587-4) compares several active programs
without identifying a settled winner. The ConTraSt analysis of 412 experiments found
that apparent support was associated with methodological choices and that many
theory-linked interpretations were made after results were known ([Yaron et al.
2022](https://doi.org/10.1038/s41562-021-01284-5)). In the 2025 adversarial
collaboration, 256 participants were studied with fMRI, MEG, and intracranial EEG.
Some observations were compatible with parts of GNWT and IIT, while central predictions
of both were challenged ([Cogitate Consortium et al.
2025](https://doi.org/10.1038/s41586-025-08888-1)).

Fourth, self-report is evidence about behaviour, not direct public access to another
system's experience. Human consciousness research needs report, covert measures, or
both, and every route has inference problems. Artificial systems add a further
problem: their reports are optimized products of training and context.

Fifth, a simulation of a consciousness-relevant function is scientifically useful
without settling phenomenology. Computational models can clarify theories and produce
predictions. They do not make experience observable merely because the model has
modules called workspace, self, emotion, or pain.

## 4. Global workspace approaches

Global workspace approaches associate conscious access with information becoming
widely available to otherwise specialized processes. [Dehaene and Naccache
2001](https://doi.org/10.1016/S0010-0277(00)00123-2) framed a workspace account around
global availability and flexible use. Later reviews relate conscious processing to
competition, nonlinear access, and distributed broadcasting ([Mashour et al.
2020](https://doi.org/10.1016/j.neuron.2020.01.026)).

For an artificial system, this suggests computational questions: Is a limited set of
contents broadcast across memory, planning, self-monitoring, and action? Does removing
that broadcast selectively impair cross-module use? Does the implementation have a
real bottleneck and causal fan-out, or is every component simply given the same prompt?

Project Theta's workspace interface is therefore only a functional analogue. A
workspace ablation can show whether shared information contributes to task behaviour.
It cannot show that the system implements the biological GNW mechanism, and it cannot
show that broadcasting is sufficient for experience. The claim that a workspace may
need metacognition also means that workspace and self-monitoring should be manipulated
both jointly and separately ([Shea and Frith
2019](https://doi.org/10.1016/j.tics.2019.04.007)).

## 5. Recurrent processing

Recurrent processing theories emphasize feedback processing rather than a single
feedforward sweep. Lamme's account gives local recurrent visual processing a central
role ([Lamme 2006](https://doi.org/10.1016/j.tics.2006.09.001)). This proposal is tied
to neural vision and cannot be copied directly into an LLM loop.

The useful artificial-system question is causal and comparative. Does state from one
cycle return to affect later interpretation and control? If recurrence is removed
while observations, action choices, and token budgets remain matched, which abilities
change? Merely calling an API repeatedly is not enough. The returning state must be
identified, logged, and shown to alter later processing.

Theta's temporal self and persistence ablations are motivated by this question. They
measure the use of recurrent state over time. They do not implement or validate
recurrent processing theory as a theory of experience.

## 6. Higher-order representation and metacognition

Higher-order approaches propose that a mental state becomes conscious through an
appropriate representation of that state. The family contains important internal
differences, reviewed by [Brown, Lau, and LeDoux
2019](https://doi.org/10.1016/j.tics.2019.06.009). Fluent first-person language is not
by itself the relevant property. A model trained to say what it is doing can produce
convincing descriptions without monitoring the actual causes of its decisions.

Useful operational tests therefore ask whether self-representations are accurate,
calibrated, and causally involved. Source attribution, confidence calibration,
prediction of one's own errors, and selective self-model ablation are better evidence
than a free-form claim of awareness. Even these remain functional measures.
Metacognitive sensitivity must be separated from confidence bias and task performance
([Fleming and Lau 2014](https://doi.org/10.3389/fnhum.2014.00443)).

Theta's self-versus-other task asks whether the agent can attribute changes in a
private signal to its own route rather than another source. The result is a B
indicator. If a verified self-model causally supports that result, the implementation
can also supply a C indicator. Neither licenses a P conclusion.

## 7. Integrated information theory

IIT begins from proposed properties of experience and develops a formal account of
intrinsic cause-effect structure. Its formulations have become increasingly precise,
including IIT 4.0 ([Albantakis et al.
2023](https://doi.org/10.1371/journal.pcbi.1011465)). IIT has also attracted extensive
criticism of its axioms, identity claims, empirical consequences, and sensitivity to
causal organization ([Bayne 2018](https://doi.org/10.1093/nc/niy007); [Doerig et al.
2019](https://doi.org/10.1016/j.concog.2019.04.002); [Merker, Williford, and Rudrauf
2022](https://doi.org/10.1017/S0140525X21002387)).

Theta does not calculate Phi. Counting software modules, messages, memory entries, or
network connections would not be a valid substitute. The current lab can study causal
dependence and integration-sensitive ablations, but those tests should be described as
general computational indicators, not IIT measurements. A future IIT component would
need a formally specified system boundary, transition probabilities, grain, state,
and exact or justified approximate calculation. Even then, interpretation would
remain theory-dependent.

## 8. Predictive processing, embodiment, and interoception

Predictive approaches treat perception and control as inference about causes of
sensory input. Interoceptive accounts extend that logic to the regulation and
representation of the body. Seth links interoceptive inference to emotion and embodied
selfhood ([Seth 2013](https://doi.org/10.1016/j.tics.2013.09.007)). Barrett and Simmons
describe interoception in terms of predictions about physiological state ([Barrett and
Simmons 2015](https://doi.org/10.1038/nrn3950)). Seth and Tsakiris argue that embodied
regulation is central to biological selfhood ([Seth and Tsakiris
2018](https://doi.org/10.1016/j.tics.2018.08.008)).

These sources support building a synthetic body only as an experimental model. Theta
has hidden physiological variables, noisy private observations, actions that alter
the hidden state, and consequences over time. The agent is not told that the unknown
channel means pain, fear, or emotion. The private-theta experiment asks whether the
agent learns a causal relationship and uses it prospectively.

The distinction between interoceptive accuracy, subjective sensibility, and awareness
is particularly important ([Garfinkel et al.
2015](https://doi.org/10.1016/j.biopsycho.2014.11.004)). An agent may predict a private
channel accurately without describing it well. It may also describe it fluently
without accurate prediction. Theta should score those outcomes separately.

A virtual body does not demonstrate feeling. It establishes an information channel,
a control problem, and a persistent relationship between action and hidden state. The
truthful, shuffled, and absent-body conditions test whether behaviour depends on that
relationship rather than on the existence of extra text.

## 9. Attention schema theory

Attention schema theory proposes that a system constructs a simplified model of its
own attention and uses that model for control and attribution. A neural network agent
has been shown to use a descriptive attention model to improve visuospatial attention
control ([Wilterson and Graziano
2021](https://doi.org/10.1073/pnas.2102421118)). This is a valuable precedent because
it demonstrates a computational function without claiming that the agent thereby had
phenomenal experience.

For Theta, the relevant question is whether a limited model of selected contents
improves control and whether removing it produces a specific deficit. A prompt that
asks the model to talk about attention is not enough. The represented target, update
rule, downstream consumer, and ablation must be inspectable.

## 10. Measurement problems that become larger in AI

Human consciousness research already faces a report problem. Report can introduce
attention, working memory, decision, and motor demands. No-report paradigms try to
reduce those demands, but their covert measures also depend on assumptions and can
track different processes ([Tsuchiya et al.
2015](https://doi.org/10.1016/j.tics.2015.10.002); [Duman et al.
2022](https://doi.org/10.3389/fnhum.2022.861517)).

AI systems add at least six confounds:

1. Training data can contain the language and expected answers of consciousness tests.
2. Prompts can reveal the hypothesis, correct action, condition, or desired narrative.
3. A language model can imitate introspection without reading the implemented state.
4. External scaffolding can create persistence that the base model does not possess.
5. Different ablations can change context length, information quantity, or task
   difficulty rather than the target mechanism.
6. Repeated API calls can vary because of provider updates and stochastic sampling.

These confounds make a strong case for blinded labels, novel random mappings, held-out
probes, matched prompt lengths, deterministic world seeds, frozen model identifiers,
raw context logging, and negative controls. A no-body control must not simply remove
tokens. A no-memory control must not accidentally disclose the answer through a
summary. An ablation should ideally preserve every non-target difference.

Self-report remains useful when treated as one behavioural measure. Reports can be
tested for calibration, invariance under paraphrase, sensitivity to hidden-state
interventions, resistance to leading prompts, and dependence on relevant internal
state. They should never be treated as privileged evidence merely because they use
first-person language.

## 11. Transferring theory-derived indicators to AI

[Dehaene, Lau, and Kouider
2017](https://doi.org/10.1126/science.aan8871) distinguish unconscious computation,
global access, and self-monitoring, then ask how machine architectures might compare.
[Reggia 2013](https://doi.org/10.1016/j.neunet.2013.03.011) surveys computational
models across several theory families while finding no compelling demonstration of
phenomenal machine consciousness.

[Butlin et al. 2023](https://arxiv.org/abs/2308.08708) provide the most direct basis
for Theta's approach. They derive indicator properties from several scientific
theories and express them in computational terms that can be investigated in AI
systems. Their later peer-reviewed article develops the method further ([Butlin et al.
2026](https://doi.org/10.1016/j.tics.2025.10.011)).

The method is useful, but it carries three layers of uncertainty:

1. the source theory may be wrong or incomplete;
2. the proposed property may not faithfully capture the theory;
3. the implementation or measurement may not faithfully capture the property.

Indicator evidence should therefore update a structured scientific assessment, not
produce a binary detector. Convergence matters only when indicators are sufficiently
independent and the tests exclude shared shortcuts. Five verbal measures generated by
the same prompt are not five independent indicators.

## 12. Welfare and responsible research

There is no evidence in this review that the current Theta agent is phenomenally
conscious or capable of suffering. Uncertainty still supports inexpensive precautions.
[Long et al. 2024](https://arxiv.org/abs/2411.00986) argue that organizations should
prepare for possible AI welfare and moral patienthood without claiming that current
systems have either. [Butlin and Lappas
2025](https://arxiv.org/abs/2501.07290) propose principles covering research goals,
procedures, knowledge sharing, and public communication. Metzinger argues for a strong
moratorium on work aimed at creating artificial suffering or synthetic phenomenology
([Metzinger 2021](https://doi.org/10.1142/S270507852150003X)).

For Theta, a proportionate precautionary policy includes:

- no research objective of creating pain, fear, suffering, or dependence;
- neutral channel names and minimal exposure intensity;
- hard limits on steps, calls, cost, and adverse hidden-body state;
- online stop rules and preservation of the stop reason;
- no punishment for requesting a stop;
- no deception that is not necessary, bounded, and declared in the protocol;
- review before increasing persistence, autonomy, replication, or aversive intensity;
- public language that does not market indicators as sentience.

Welfare rules serve another purpose even if present systems are not conscious. They
discourage sensational design, constrain researcher degrees of freedom, and make the
lab's values inspectable.

## 13. Evaluation of the current Project Theta design

The present design has several strengths. It uses deterministic trial schedules,
opaque and counterbalanced cues, hidden body state, explicit predictions, persistent
memory, a workspace and self-model interface, matched ablations, SQLite event logs,
preregistered metrics, bounded provider use, and welfare stops. It clearly separates
B, C, and P claims.

It also has significant limitations:

- The LLM is accessed through a provider API, so internal activations and most causal
  mechanisms inside the model are unavailable.
- Much of the implemented architecture is external scaffolding. Results describe the
  combined agent system, not the base language model alone.
- Some ablations may change information volume or context structure in addition to the
  named component.
- A capable language model can infer task structure, imitate scientific language, or
  use textual shortcuts.
- One experiment family, one provider, and a small number of seeds cannot establish
  generality.
- The measures have not been validated against systems with agreed consciousness
  status, because no suitable artificial ground truth exists.
- The literature review has one primary reviewer and capped retrieval.

These limits do not make the experiments pointless. They determine the level of claim
the results can support.

## 14. Required design changes

The literature review supports the following priorities before continuous deployment:

1. Add context-matched ablations so token count, wording, and information volume are
   held as constant as possible.
2. Add prompt-leakage and answerability audits that inspect every model-visible field.
3. Add reversal tests in which cue mappings, delays, or source relations change after
   acquisition.
4. Compare the LLM agent with simpler associative and rule-based agents.
5. Add open-weight adapters so activations, component interventions, and causal
   mediation can be studied.
6. Separate self-report scoring from task performance and metacognitive calibration.
7. Test multiple models and frozen snapshots with the same trial schedules.
8. Seek independent review of the protocol, welfare rules, and literature corpus.

Continuous operation should wait until these safeguards are implemented and a
deployment gate has been passed. Running for longer does not automatically produce
better evidence. Without stronger controls, it can simply produce a larger quantity
of correlated observations.

## 15. Conclusion

The scientific case for Project Theta is narrower and more useful than a claim to test
consciousness directly. Leading theories suggest functional properties that can be
implemented, manipulated, and measured in artificial agents. The field also supplies
strong reasons to distrust unblinded behaviour, first-person language, architectural
labels, and single-theory conclusions.

Project Theta can contribute by building careful tests of behavioural and
computational indicators, publishing controls and null results, and improving methods
for artificial-system assessment. It cannot turn those indicators into public access
to phenomenal experience. That boundary should remain in every protocol, result,
visualization, website, and public statement.

## Review materials

- Protocol: `preregistration/literature-review-protocol-01.md`
- Search log: `research/literature-search-log.md`
- Raw metadata: `research/literature-search-results.json`
- Screening candidates: `research/literature-screening-candidates.csv`
- Evidence table: `research/evidence-table.md`
- Exclusion categories: `research/excluded-records.md`
- Checked metadata: `research/reference-verification.json`
- Bibliography: `references/project-theta.bib`
- Theory and experiment map: `docs/theory-evidence-map.md`
