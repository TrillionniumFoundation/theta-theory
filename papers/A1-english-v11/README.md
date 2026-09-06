# A1 v11 — certified memory across exponent collisions

**Manuscript:** [main.pdf](main.pdf) · [English TeX](main.tex)  
**Revision branch:** `revision/a1-english-v11-referee-response-2026-09-06`  
**Controlling report:** [`1aa4599eedca650d34c3778a00f3ad854c2bc9d7`](../../reviews/a1-english-v10-effective-finite-memory-2026-09-06/REFEREE_REPORT.md)  
**Reviewed submission:** `d9f48fe08fd694e636c287be7646ae7d723ce3b8`

This revision is based on the effective-finite-memory v10 review, not the separate shared-memory-composition v10 branch. The old submission, review and historical files remain unchanged. The English manuscript uses theorem–proof exposition in `amsart`; revision logistics and execution counts are outside the paper.

## Mathematical changes

The complete collision profile and its original persistent-state converse remain in force. Section 7 adds ten proved results:

* A separated-chain floor, attributed to the referee technical note, gives sufficient precision `log2(M+1)/d0 + O(1)` and program size `O(M^(1+J/d0) log(M+1))`, where `d0=(r-1) floor(N/2)`.
* A two-sided certificate from approximate feasible histories selects its own mesh. With `e` the largest true M-centre covering radius, the finite sample radius satisfies `max(0,r/2-h) <= e <= r+(A+2)h`. Stopping at `r >= 4(A+2)h` gives `h ~ e` without knowing e or a collision stratum.
* The complete profile determines the selected precision `b = (1/2) log2(1/Xi) + O(1)` and the sufficient program bound `O(M Xi^(-J/2) log(M+1))`. The four-cell, five-trial example inherits three corresponding resource phases.

Numerical precision and program size are sufficient resource statements, not matching lower bounds. The matching converse concerns M persistent labels. Fixed horizon, known calibration, the original arbitrary full-support prior classification, and the effective-data interface are distinguished explicitly.

## Referee response and evidence

[Point-by-point response](RESPONSE_TO_REFEREE.md) covers P10.1–P10.5 and the editorial/novelty objections. [Historical derivation map](HISTORICAL_DERIVATION_MAP.md) and [proof/resource ledger](PROOF_LEDGER.md) record dependencies and provenance.

`build.py` verifies the ten inherited body-file Git hashes, all **49** complete v10 proof blocks, and all **52** v10 named-result labels. The compiled manuscript contains **59** complete proofs, with all source references resolved. This is source-preservation verification, not automated proof checking.

`certified_compiler.py` adds finite input-error, transition and decoder certificates and adaptive refinement. The unchanged `finite_compiler.py` retains the one-field runtime machine. The new tests use an independent exponent-keyed truth algebra rather than the compiler's formal-label evaluator.

Local execution passed **8,207** new finite checks. They check all **495** stored query entries in nine physically perturbed-input programs, detect all **495** zeroed outputs and all **444** separately corrupted nonconstant entries, check **5,184** off-grid physical query outputs and **864** state recurrences, and test the adaptive certificate against exact interval covering radii. The largest physical query certificate is approximately **0.433271**, below one half; the largest observed query error is approximately **0.003355**. The physical off-grid fixtures use a specified neighbourhood of the eight command vertices; they are not a mesh of the whole cube at that tolerance. The separate adaptive fixtures cover their full command interval.

Fresh legacy reruns are stored separately: **7,904** original author checks and **36,960** independent referee checks. The original zero-output mutation again passes the old author suite; that historical diagnostic failure is reproduced, not hidden. No assertion count certifies continuum entropy, optimal program length, exhaustive priority, or acceptance by a journal.

## Reproduction

From this directory:

```sh
python3 validate.py
```

The script uses Python's standard library and `pdflatex`/`pdfinfo`. It checks the source manifest, runs both legacy suites and their original mutation control, runs the new suite, compiles three times without shell escape, and writes `validation/REVISION_VALIDATION.json`. From a source-only checkout, `python3 build.py --prepare-only` performs the proof-preservation and reference checks without TeX. The parent v10 and controlling review directories are required for the full legacy rerun.

The publication workflow runs only on this new revision branch, verifies before committing generated PDF/receipts, and never force-pushes. It changes no review branch, main branch, protection rule, member permission, or old manuscript. `SOURCE_MANIFEST.json` pins the readable v11 source files. The compressed transport source, when present under `.github/revision-sources/`, is only a reproducible installation input; this directory contains the actual readable manuscript and code.
