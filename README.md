# theta-theory — Round 51 revision

The active submission is **Single-Atom Boundary Identification with Retained State and Logarithmic Physical Depth**, responding to the frozen Round 50 referee report.

Start with [ROUND51_REVIEW_INDEX.md](ROUND51_REVIEW_INDEX.md), the [main manuscript source](ROUND51_REVISION.tex), and the [point-by-point response](AUTHOR_RESPONSE_ROUND50.md).

The revision generalizes the retained-state bounded-probe theorem to any sufficiently short positive-mass atom, enlarges the successful-block event, uses all-sign weighted energy and a sharper sampled-channel remainder, and proves an explicit finite-response-to-physical reduction with a compatible estimator and dimension-uniform truncation bounds. The complete working posterior and logarithmic depth-order conclusion are retained and strengthened.

Current executable source is supplied directly in `tools/round51_certificates.py`, `tests/test_round51.py` and `tools/verify_round51.py`. Run `python tools/verify_round51.py --build` to verify the frozen active-source closure, execute the new finite tests and build the article. The review index specifies dependencies and distinguishes actual execution receipts from analytic proofs.

All previous manuscript roots, referee reports and historical derivations remain on this full-history revision branch. No prior branch is rewritten or merged. The new code is not represented as a recovered copy of the missing Round 49 programs. No journal acceptance or formal proof certification is claimed.
