# A2 revision 141 — native referee submission

**Intrinsic reconstruction from nonreduced failure schemes** — Qian Qi — 23 September 2026.

The principal mathematical chain is intrinsic coefficient extraction -> sharp finite reconstruction -> spectral geometry. A new, separately proved real theorem constructs totally real reciprocal likelihood fibres for every definite pencil, proving the assertion formulated as Fevola–Mandelshtam–Sturmfels Conjecture 4.5.

## Reading objects

`geometry.pdf` / `geometry.tex` is the principal article. `supplement.pdf` / `supplement.tex` retains the full boundary, collision, primary, relative, and historical technical material. `complete.pdf` / `complete.tex` combines both proof networks. Main/supplement references are cross-linked after the build.

Start with `RESPONSE_TO_REFEREE_V140.md` and `REFEREE_GUIDE_V141.md`. `LITERATURE_AUDIT_V141.md` gives the exact source comparisons and explicitly unverified documentary items. `PROVENANCE_MANIFEST_V141.json` and `NONDELETION_V141.json` bind sources and retained history. Executed checks and actual PDF/page counts appear in `evidence/BUILD_RECEIPT_V141.json`.

## Build

From this directory run `bash build.sh`. Requirements: Python 3 with SymPy, NumPy and PyMuPDF; a TeX Live installation containing AMS classes, Latin Modern, microtype, xr-hyper and hyperref. The workflow installs these dependencies and runs the same entry point. Seventeen scripts execute before the three native LaTeX builds and the source/layout audit.

The build removes and recreates only this revision's generated `evidence/` directory. It does not modify predecessor manuscripts. Native sources require no prior Actions artifact, transport decoding or unpublished file. `verify_v141.py` records `A2_SOURCE_COMMIT` when supplied, otherwise the actual Git HEAD when available, and otherwise the literal `local-preflight`.

## New proof locations

`parts/21-spectral-specialization.tex`: explicit sheaf-to-module/similarity and local-Artinian square-root lemmas.

`parts/22-relative-spectral-strata.tex`: universal actual finite-neighbourhood family, arbitrary base change, spectral Fitting readout and realization of all Segre closure intersections.

`parts/23-real-likelihood.tex`: separated-root score lemma, explicit data for every multiplicity pattern, omitted-axis exclusion, denominator check, Hessian and openness proof.

All earlier theorem statements and proof files remain. Changed predecessor files are archived exactly under `history/v140/`. A build receipt is finite reproducibility evidence, not a formal proof certificate or a journal decision. The Ballico full-text comparison and exhaustive contraction-priority clearance have not been falsely marked complete.
