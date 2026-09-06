# Review record

The 6 September 2026 Astra review was produced by an AI coding and methods reviewer. It is valuable adversarial review, but it is not an independent academic peer review or external ethics review.

- `astra-methods-review-2026-09-06.md` contains the review.
- `reproduce_review.py` reproduces the reported schedule and table-reader diagnostics against the historical checkout and databases described in the review.
- `evidence.json` is the machine-readable output from that review.
- `external-review-packet.md` defines the questions for a future human methods reviewer.

Historical reproduction should use the frozen revision named in the review. The current code contains the later repair and will not reproduce the old schedule generator by design.
