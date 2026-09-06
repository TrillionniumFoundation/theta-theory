# A1 v10: independent referee-style review

**Submission:** `d9f48fe08fd694e636c287be7646ae7d723ce3b8`  
**Revision branch:** `revision/a1-english-v10-effective-finite-memory-2026-09-06`  
**Review branch:** `review/a1-english-v10-effective-finite-memory-harsh-2026-09-06`  
**Recommendation:** Reject at the requested Annals / Inventiones / JAMS / Acta level in the present form.

This is an owner-requested AI-assisted assessment, not a report commissioned by a journal. The recommendation concerns the mathematical significance demonstrated by this submission. No blocking counterexample to the principal classification or finite-compilation theorem was found in the examined proofs.

Read [REFEREE_REPORT.md](REFEREE_REPORT.md) for the submission-specific assessment and claim audit. [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md) proves a stronger sufficient numerical-precision and program-size bound using the submission's own compiler, without a collision oracle.

The execution evidence distinguishes three things: the unmodified author suite passes 7,904 assertions; a deliberate all-zero-output mutation also passes that suite; the referee's additional output checks detect the mutation and confirm the original tables on the tested fixtures. Separately, an independent standard-library program passes 36,960 exact assertions. These counts include elementary bookkeeping and do not certify continuum theorems or journal merit.

## Reproduction

From the repository root, with Python 3.10 or later:

```sh
REVIEW=reviews/a1-english-v10-effective-finite-memory-2026-09-06
OUT=/tmp/a1-v10-referee-reproduction
mkdir -p "$OUT"
python papers/A1-english-v10/tests/test_v10.py "$OUT/AUTHOR_TEST_RERUN.json"
python "$REVIEW/referee_checks.py" "$OUT/INDEPENDENT_DIAGNOSTICS.json"
python "$REVIEW/mutation_checks.py" papers/A1-english-v10 "$OUT"
```

The mutation program verifies the two pinned author Git blob hashes before executing, and does not modify the author files. All mutation is in memory. Its extra all-query output assertions are separate from the original author's assertion counter.

The JSON receipts and [EXECUTION_REPORT.json](EXECUTION_REPORT.json) record what was actually executed and what was not. This review does not claim a fresh LaTeX build, PDF inspection, GitHub Actions run, exhaustive priority search, or a re-audit of all legacy appendices and all eleven planned papers. Only new files in this review directory are added; the reviewed manuscript is not revised here.
