# Excluded record categories

This file documents exclusion logic for literature review version 1.0. It does not
claim that every excluded record received dual human review.

## Automated relevance screen

The deterministic ranking retained the first 100 of 1,800 unique records for primary
manual inspection. Lower-ranked records were not added to the evidence corpus unless
they were recovered through citation chaining or targeted verification. The common
reasons were:

- consciousness appeared only as a metaphor or incidental term;
- the record concerned clinical awareness without bearing on the review questions;
- the record concerned generic AI ethics without consciousness, sentience, welfare,
  moral patiency, or research governance;
- the record concerned active inference, embodiment, or metacognition without a clear
  link to consciousness or self-representation;
- the work proposed an implementation but provided no assessable mechanism, evidence,
  criticism, or safeguard;
- a later peer-reviewed version superseded the preprint;
- metadata was incomplete, duplicated, or clearly misclassified by a database.

## Records inspected but not included

The ranked candidate file is retained as
`research/literature-screening-candidates.csv`. Candidate records that were not added
to the final corpus commonly fell into these groups:

| Exclusion category | Example rationale |
|---|---|
| Superseded version | A preprint duplicated a later journal article in the corpus. |
| Peripheral application | The paper used a consciousness theory in a clinical or engineering application without testing the theory. |
| Speculative architecture | The proposal asserted machine consciousness without a discriminating test or causal evidence. |
| Insufficient relevance | The main subject was emotion, attention, AI capability, or ethics with no direct answer to a review question. |
| Correction or interview | The record did not contain a separate study or argument. |
| Metadata error | The search provider matched unrelated work because of author names or broad keywords. |

## Audit requirement

Before external academic submission, a second reviewer should independently screen
the 100 ranked candidates and a reproducible random sample of at least 10 percent of
the other 1,700 records. Any missed eligible record should trigger a wider audit and a
dated protocol amendment.
