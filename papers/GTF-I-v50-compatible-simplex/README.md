# General Theta Foundations I — Revision 50

**Compatible Simplices and Exact Stochastic Width**  
Author: Qian Qi. Date: 27 September 2026.

The manuscript positively addresses r31 by adding higher-width compatibility geometry, a rank-tight occupation budget and exact four-state frontier, an all-horizon invariant-simplex classification, an exact distortion/enclosure separation, and a rational noncommuting three-epoch orthogonal cubic optimum beyond every separate matrix flattening. Explicit output-size bounds and direct tensor-completion comparisons supplement the retained two-state alternative. All v49 theorem/proof content remains in the integrated paper.

Start with `paper.pdf`, `RESPONSE_TO_REFEREE.md`, and `evidence/THEOREM_LOCATIONS.json`. `evidence/REFEREE_PACKAGE.zip` is the compact submission package. It excludes the large historical archives, which remain unchanged in the v49 folder.

## Native build

From this directory, after installing Python 3.11+, SymPy 1.14.0, PyMuPDF 1.26.7 and a LaTeX distribution with amsart, lmodern, microtype, mathtools and hyperref:

    python build.py --check-core

The source-bound workflow supplies `GTF_SOURCE_COMMIT` and validates the exact native source commit. A local run without it is explicitly labelled `local-uncommitted-build`; it must not be represented as remote CI. `prepare.py` is only for initially copying the pinned v49 sources in a full repository; the published native files and standalone core archive already contain those copies. An isolated archive rebuild uses `build.py --core-only` and needs no predecessor files or network.

The build runs v50/v49/v47/v44 finite checks with ordinary and optimized Python, checks preservation, exercises the CLI's fail-closed limit, compiles three passes, checks every page, and rebuilds the source archive in isolation with all-page text and raster equality. The build does not independently certify universal proofs or novelty.

## Scope

The higher-width normal form is necessary at cuts of width equal to the D+1 Hankel rank, with spanning seeds and all coordinate queries. It is not asserted for arbitrary larger factorizations. The nine-dimensional cubic experiment instead has one designated coordinate query. The packet/enclosure separation is exact, but does not replace the retained arithmetic proofs. The four-state positive-error interval is qualitative. The full algebraic two-state optimizer is proved, not generically implemented. The resource model is nonuniform atomic-row width; exact algebraic sampling is not a claim about uniform finite-bit cost. See `PROOF_STATUS.json`, `RESOURCE_LEDGER.md`, `LITERATURE_AUDIT.md`, and `HISTORY_AUDIT.md`.
