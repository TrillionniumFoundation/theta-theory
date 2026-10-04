# A2 v19 — intrinsic network and period descent

Qian Qi · 28 September 2026

Primary article: **Intrinsic marked boundary laws and rigidity of periodic dispersing billiards**, `main.tex` (15 pages in the actual local build). The controlling report is the v18 report at `e727a7ac9b73b6928ecc194d74628125159d49cf`, not the earlier v16 report. The reviewed author checkpoint is `0708f67908355e9881d1993b42bcc698b0c350c6`.

## Main revision

Theorem 1.2 recovers the incidence graph and geometric cycle displacements from an unlabelled collection of local density pairs when the analytic obstacle representatives are asymmetric and pairwise noncongruent. No obstacle identities, cross-channel registrations, relative edge signs or integer lattice-copy labels are supplied. The free-area normalization and recovered obstacle areas give the period covolume. A finite-index lattice classification bounds the candidates by the divisor sum of the recovered index; index one gives unique reconstruction. Proposition 3.4 constructs open primitive physical families; Proposition 3.5 constructs exact physical finite-index ambiguities.

Theorem 1.3 gives conditional finite-histogram recovery on uniform analytic classes with shape and symmetry margins. Lemma 4.4 locks the recovered integer structure by comparing admissible physical candidates, not by taking integer spans of noisy real vectors. The local inverse and physical C3 hypotheses are in Section 2; the closest boundary-distance, lens and obstacle travelling-time comparisons and the two retained regularizations are in Section 5. Two windows always mean two density functions or two growing histograms, not two scalar observations.

The title, billiard-boundary-law topic and requested mathematical-journal target are retained. Neither a minimax claim nor an exact analytic count-only result is inferred.

## Submission volumes and preservation

`retained/v18/main.tex` is **Supplement R**, the complete reviewed v18 article with every input unchanged, native tree `3c558d7799e9e49812e7bab98320d3a98e7f7418`. It retains all 14 v18 core files, including the moment inverse, registered symmetric-table theorem, both older regularizations, count fibers and physical experiments. These are supplied results, not deleted or demoted to unavailable history.

`complete/main.tex` and `complete/two_collision.tex` are **Supplement S** and its auxiliary document. The exact tree is `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`, also preserved within Supplement R. `SUPPLEMENT_MAP.md` gives the reading map. Previous repository papers and review paths are unchanged.

## Reproduction and evidence

Python 3.10+, NumPy, SciPy, latexmk, a LaTeX installation with amsart/Latin Modern/microtype, and Poppler pdfinfo are needed. Run:

```sh
python3 tools/validate_v19.py
# In an actual checkout of this revision, including retained volumes:
python3 tools/validate_v19.py --all-volumes --require-checkout
```

The actual local primary-only run passed **43,864 finite checks**, with identical normal and optimized Python output. Its 90 nonlinear stationary-ray curvature comparisons had maximum absolute error `1.2312545871751013e-08`. The 15-page primary build had no final TeX warnings, undefined references, or overfull/underfull boxes. The mathematical/tool source manifest was unchanged. All 15 rendered pages were inspected.

That local execution was **source-content execution, not an authenticated Git checkout**. It did not rebuild Supplement R or S. `verification/local/receipt.json` retains null commit/run fields and records the actual commands, exits and digests. `SOURCE_PINS.json` binds every new mathematical/tool source to its actual SHA-256. The published core and tools trees are content-identical to the locally checked ones.

The separate read-only GitHub workflow checks out its exact triggering commit, checks retained tree identities, reruns the new and retained diagnostics, and builds the primary and all three retained documents. It uploads actual logs, receipts and PDFs, including failures. Its existence or a queued run is not a successful hosted build. No hosted success is asserted here. The preserved v18 checkpoint's broken historical validator is not used or rewritten; the new v19 validator has its own complete pins and schema.

Finite diagnostics and compilation do not certify all proofs, establish literature priority or constitute a journal decision.
