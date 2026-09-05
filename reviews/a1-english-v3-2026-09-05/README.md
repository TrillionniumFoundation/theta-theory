# A1 English-v3 independent referee review

Start with [REFEREE_REPORT.md](REFEREE_REPORT.md), then [CLAIM_AUDIT.md](CLAIM_AUDIT.md).

**Reviewed revision:** `revision/a1-english-v3-operational-closure-2026-09-05` at `025a9b3fdfd9ffa86e6ae2924f8b5e5b1b58ddd6`.

**Review branch:** `review/a1-english-v3-harsh-referee-2026-09-05`.

**Recommendation:** Reject at the requested four-leading-mathematics-journal level, while recognizing substantial improvement and a largely credible principal apparatus/filter/control chain. This is an independent AI-assisted assessment, not a journal appointment or official editorial decision.

The report contains a detailed principal-theorem audit, disposition of the previous review, two local scope corrections, three contribution objections, a proved endpoint-gate strengthening, and a detector-perturbation/model-value error analysis. The 13-entry claim audit distinguishes correctness, scope, significance and out-of-model diagnostics.

## Reproduce the independent finite checks

```bash
python -m pip install -r requirements.txt
python referee_checks.py rerun.json
```

The recorded final run passed 20/20 diagnostics under Python 3.13.5. [DIAGNOSTICS.json](DIAGNOSTICS.json) identifies exact, numerical and finite-analogue checks separately. Author tests were not rerun; LaTeX/PDF verification and proof-assistant verification were not performed. The report discloses an initial referee-harness Boolean-conversion error and its correction.

[REVIEW_MANIFEST.json](REVIEW_MANIFEST.json) records the reviewed identities and hashes of the report, audit, script and execution receipt. The [source/](source/) subtree is exactly Git tree `ec09fa385c5fdcc5f2aece59a6b7f0806bfbb8ea`, the full reviewed A1 directory, unchanged. This review adds files only under its new review directory; it does not edit the manuscript, the main branch or the revision branch.
