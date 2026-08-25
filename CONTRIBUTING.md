# Contributing

Project Theta accepts falsifiable experiments, controls, adapters, metrics, and
documentation improvements. Contributions must preserve the distinction among
behavioural indicators, computational indicators, and phenomenal consciousness.

For every experiment change:

- state the theory-derived rationale without treating the theory as settled;
- include a shortcut/leakage analysis and at least one matched negative control;
- make randomness flow from an explicit seed;
- log enough provenance to replay the condition;
- specify exclusion and welfare-stop handling before data collection;
- add deterministic unit tests; and
- avoid composite “consciousness scores” unless each component and weighting is
  separately justified and sensitivity-tested.

Run `python -m unittest discover -s tests -v` before opening a pull request.

