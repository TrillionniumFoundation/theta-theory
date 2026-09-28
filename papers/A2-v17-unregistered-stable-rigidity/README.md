# A2 v17 — unregistered rigidity and conditional whole-table reconstruction

**Qian Qi, 28 September 2026.** The primary manuscript is `main.tex`, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*. This is a substantive revision of A2 v16, responding to the external report frozen at `62c98e9178c5571a19afaccf8b5e67fc892c6c1e`. The Annals/Acta/Inventiones/JAMS mathematical target and the billiard-boundary-law topic are retained.

## Referee reading route

Read Theorem 1.1 for the complete result, Section 7 for the new unregistered theorem, and Section 8 for finite noisy-window reconstruction of the entire table. `RESPONSE_TO_REFEREES.md` maps all eight requested corrections to the text. `PROOF_LEDGER.md` separates assumptions, proofs, diagnostics, and remaining scope boundaries.

Theorem 7.2 reconstructs a labelled periodic table from independent edge reversal orbits, without supplied cross-channel arclength registration or relative signs, when the analytic obstacle images have trivial Euclidean isometry groups. For noncircular obstacles it gives a finite assembly bound. Proposition 7.4 constructs an open physical asymmetric class. The previous fully registered theorem remains available for symmetric obstacles; no old theorem is replaced by a weaker one.

Theorem 8.1 gives conditional whole-table reconstruction from finitely many noisy masses and endpoint moments. It estimates the unknown onset and leading geometry, recovers finite jets, controls analytic continuation on a uniform strip, synchronizes the images using quantitative asymmetry, and bounds the lattice error. Its constants depend on explicit analytic, geometric and symmetry margins. It is not a claim of an optimal inverse rate or of efficient exhaustive search.

## Source package and preservation

The locally built primary article has **29 pages**. `complete/main.tex` is the complete retained Supplement S; `complete/two_collision.tex` is its retained auxiliary document. Their entire tree is unchanged: `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`. `history/v16-reviewed` is the exact entire reviewed v16 paper tree, including its prior history and evidence. Seven active mathematical core files are reused byte-for-byte. Earlier repository papers and review branches are not edited.

## Reproduction

From this directory run `python3 tools/run_validation.py` for the primary article. In a real Git checkout run `python3 tools/run_validation.py --all-volumes` to check the preserved supplement tree and build all three documents. Requirements: Python 3.10+, `latexmk`, `texlive-latex-extra`, `texlive-fonts-recommended`, and Poppler `pdfinfo`.

The actual local source-content run passed 5,844 retained and 1,094 new finite diagnostics; normal and optimized Python outputs were identical. It built the 29-page primary with no final TeX warnings, undefined references, or overfull/underfull boxes, and did not change mathematical or tool sources. This was **not an authenticated Git checkout**, and Supplement S was **not rebuilt locally**. The receipt preserves null checkout/run fields rather than inventing them. Its source manifest is bound to the published Git blobs in `SOURCE_PINS.json`.

The separate read-only GitHub workflow checks out its exact triggering commit, builds the primary and both preserved supplementary documents, and uploads actual receipts and logs, including failures. A workflow definition or queued run is not a successful hosted build. Consult the run associated with the revision commit; no successful hosted conclusion is asserted by this README. Finite checks and compilation are not independent proof certification or a journal decision.
