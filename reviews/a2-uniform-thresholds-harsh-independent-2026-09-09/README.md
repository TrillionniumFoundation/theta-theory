# Independent review of the A2 uniform-threshold revision

Read [REFEREE_REPORT.md](REFEREE_REPORT.md) first. This review is pinned to `500cf06faccb6eadd6c122abeb63c60a0cb7522e` on `revision/a2-uniform-collision-thresholds-2026-09-09`.

**Disposition:** reject at the requested top-four-journal level as presented; no fatal in-scope error was established in the new main theorems. The report recognizes the new collision-order-uniform argument and retires obsolete objections to the old one-roof note. The remaining objections concern demonstrated significance, the information content of the inverse application, the closest literature comparison, and precise full-record response scope. This is an independent AI-assisted review, not a journal decision.

## Files

- `REFEREE_REPORT.md`: complete English report, proof audit, four graded objections, analytical refinements, previous-review disposition, and primary references.
- `diagnostics.py`: independent finite rational, ray-reflection, nonlinear-twist, and quadrature checks. No repository imports or network calls.
- `verification.json`: frozen source Git blobs, executed environment, checks by kind, selected measurements, script/output hashes, and explicit limitations.

## Reproduce the independent checks

From this directory, with Python and the dependencies available:

```sh
python diagnostics.py > diagnostics.json
python -O diagnostics.py > diagnostics.optimized.json
cmp diagnostics.json diagnostics.optimized.json
sha256sum diagnostics.py diagnostics.json diagnostics.optimized.json
```

The executed environment was Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0, and mpmath 1.3.0. Both executions passed 125/125 checks and produced byte-identical output. Exact reproducibility of numerical bytes across different library versions is not claimed. Full generated JSON is not committed; the verification receipt records its SHA-256 and the supplied script regenerates it.

Finite checks are not a proof of all radii, all collision orders, all source functions, or all derivative orders. A discarded, unjustified cap in an early referee harness is disclosed in the report and receipt; it is not a counterexample to the manuscript.

Only this new review directory is added on the review branch. No manuscript or old report is replaced, no merge is performed, and no permissions or branch-protection settings are changed. PDF rebuilding, the author's separate 411-case suite, remote CI, and formal proof certification are not part of this review.
