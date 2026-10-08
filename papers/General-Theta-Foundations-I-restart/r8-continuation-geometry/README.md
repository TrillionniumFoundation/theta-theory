# General Theta Foundations I — restart R8

**Acquired Geometry and Causal Resource Transfer** — continuation-geometry revision, 7 October 2026.

The main source is `main.tex`; all nine mathematical sections and the bibliography are ordinary source files in this directory. New continuation and noisy-regression proofs are integrated into the article before the retained acquisition and filtering realizations. This is a revision of the restart paper, not a realization rebranded as foundations, and not v97.

The full singular and typed-transcript proofs are supplied as **Supplement S**, an integral part of this submission. `build.py` rebuilds the unchanged R6 technical source at its pinned sibling path and attaches the source-controlled `supplement_cover.tex.in`. The supplement is not a separately published article. The retained R7 and R6 sibling trees remain unchanged.

## Mathematical additions

- Exact one-cut functional distortion; two-sided comparison under bounded common-channel domination; conditional localization when global domination is zero.
- Raw finite-report/common-density and joint-regeneration constructions, with actual submeasure mass.
- A sequential continuation-chart class theorem: the optimal recursively executable risk and actual continuation width are equivalent in order, allowing correlated prefix reports and unbounded acquired tails with controlled moments.
- A noisy regression theorem with correlated-prefix extension and continuous future query: the same binary task has online excess of order M^(-2/d) and terminal checkpoint excess of order M^(-2).
- An explicit numerical common-task upper for that realization, retaining the distinction between an allowed defect and an attained lower term.

## Build

Requires Python 3, pdfLaTeX, pdfinfo, and pypdf 5.9.0. Run `python refresh_manifest.py` only while intentionally editing source. For a fixed source tree run:

```sh
python verify.py
python regression.py
python -O regression.py
python build.py --source-sha FULL_SOURCE_COMMIT --output /tmp/theta-r8-products --receipt /tmp/theta-r8-receipt.json
```

A full build executes two isolated three-pass main builds, two isolated three-pass retained-technical-text builds and two isolated three-pass supplement-cover builds. The supplement attachment checks every retained page's text and is repeated byte-for-byte. Source hashes, recorder inputs, labels, references, and both Python modes are checked. These checks are not mathematical proofs.

`REFEREE_RESPONSE.md` maps all eight major and thirty technical R7 comments. `PROOF_LEDGER.md`, `THEOREM_MAP.md`, `ASSUMPTION_MATRIX.md`, `COUNTEREXAMPLE_LEDGER.md`, `RESOURCE_ACCOUNTING.md`, `PIPELINE_DERIVATION.md` and the audits delimit exactly what is proved. Source SHA, artifact SHA and final read-only verification SHA are recorded separately in `evidence/` after they exist.
