# Independent referee-style assessment of A1 English v25

This is an owner-requested AI-assisted assessment, not a report commissioned by a journal or a formal proof certificate.

**Reviewed submission:** `8a84075ee518035069d38fd9262bd455aff4ac86` on `revision/a1-english-v25-adaptive-graph-width-2026-09-07`.

**Review branch:** `review/a1-english-v25-harsh-independent-2026-09-07`, created from that exact submission. This package adds review files only; it does not revise the manuscript or merge a branch.

## Read the assessment

[REFEREE_REPORT.md](REFEREE_REPORT.md) contains the recommendation, controlling-request dispositions, direct scalar and new adaptive-proof audit, star calculation, significance assessment, concrete corrections, and evidence limits.

The requested four-journal recommendation is **reject on mathematical significance**. No false principal theorem or unresolved central gap was found in the inspected proof route. The genuinely new adaptive extension is acknowledged; the earlier closed architecture and early-example requests remain closed. These are review conclusions, not a theorem certificate or an acceptance prediction.

Corrections E25.1–E25.3 concern the incorrect cutwidth bibliography, the absent relative proof ledger invoked by the response, and weak diagnostic negative controls. The report distinguishes these from its venue judgment.

[REVIEW_SCOPE.json](REVIEW_SCOPE.json) pins the source commits and blob identifiers, records what was and was not read or executed, and describes the scope of each finding.

## Reproduce the independent finite checks

From this directory, with Python 3.10 or newer:

```sh
python independent_diagnostics.py > /tmp/a1-v25-referee-normal.json
python -O independent_diagnostics.py > /tmp/a1-v25-referee-optimized.json
cmp /tmp/a1-v25-referee-normal.json /tmp/a1-v25-referee-optimized.json
cmp /tmp/a1-v25-referee-normal.json DIAGNOSTICS.json
```

[independent_diagnostics.py](independent_diagnostics.py) was executed during this assessment. It imports no author implementation and uses exact rational arithmetic. [DIAGNOSTICS.json](DIAGNOSTICS.json) records **4,789 passed checks** and the executed script's SHA-256. Ordinary and optimized Python produced byte-identical outputs. The GitHub-reported script blob matches the locally executed bytes.

Finite checks do not prove the continuum theorem. No native checkout, LaTeX build, submitted-PDF visual inspection, fresh GitHub Actions success, exhaustive companion audit, or exhaustive literature-priority search is claimed. Those limitations are recorded rather than replaced by older validation receipts.
