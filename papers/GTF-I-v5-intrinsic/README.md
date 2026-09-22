# General Theta Foundations I — fifth intrinsic revision

Author: Qian Qi. Date: 22 September 2026.

Controlling review: `review/general-theta-foundations-i-v4-harsh-referee-2026-09-22`, commit `aba384e8bbadd36b4ce27a2c932c1a9cb5e63b53`, report `reviews/general-theta-foundations-i-v4-2026-09-22/REFEREE_REPORT.md` (Git blob `c702a64f74882a9c90597bb5f56d16dd3a0d3e72`).

Working branch: `revision/general-theta-foundations-i-v5-intrinsic-2026-09-22`.
Frozen handoff branch: `revision/general-theta-foundations-i-v5-intrinsic-referee-ready-2026-09-22` (created after publication verification).

## Two views, one mathematical source

`principal-paper.pdf` is the focused causal-memory article. It contains the intrinsic profile theorem, the pressure theorem, the dependent-acquisition comparison, and the complete general posterior-orbit and noisy expanding proofs they use. `paper.pdf` is the full Foundations I revision. It additionally contains every retained v4/v3/v2 quantitative proof and the first-edition foundational body. Both share `core.tex`; they are not divergent mathematical revisions. The build verifies identical numbers for every core label.

Start with the focused edition for the new argument, then the full edition for calibration, collisions, filtering, control and foundational cross-references. The full edition is the preservation record. No old file, theorem or proof is removed to obtain the focused edition.

## New argument

Separated C^(1+gamma) inverse branches + stationary Hölder Gibbs law -> mass-weighted orbit cylinder tree -> arbitrary-centre Hilbert quantization comparison -> exact suffix-closed finite-state realization -> two-pressure exponent. The finite profile is computed from cylinder masses and finite branch derivatives, not supplied as an unknown Hilbert quantization invariant.

For b branches and N leaves, the full greedy tree has exactly `(bN-1)/(b-1)` designated states; every suffix is already a vertex. In particular the binary implementation uses `2N-1` states, including the empty word. Conditional minorization then transfers the risk order to invariant acquisition kernels that retain hidden memory. No physical refresh coin is exposed to the observer.

## Rebuild

From a repository checkout containing the pinned inherited inputs:

```sh
python3 papers/GTF-I-v5-intrinsic/build.py
```

Alternatively extract `evidence/COMPILED_SOURCES.zip` into an empty directory and run the same command there. Required executables are Python 3, `pdflatex` and `pdfinfo`; TeX needs the standard AMS, geometry, hyperref, mathtools, enumitem, booktabs, microtype and Latin Modern packages used by the inherited preamble. On Ubuntu the workflow installs `texlive-latex-extra texlive-fonts-recommended texlive-science lmodern poppler-utils`.

The build checks hash-bound inputs, inherited source identities, retained labels, core numbering, normal/optimized diagnostic agreement and five negative controls, then compiles both views to stable references. In a Git checkout it also checks the review blob, preserved trees, source HEAD and new-path-only diff. It writes PDFs, a complete source archive and an execution receipt under `evidence/`.

These checks identify the submitted source and detect specified regressions. They are not formal proof verification or independent refereeing. New hypotheses, constants and proof dependencies are listed in `PROOF_LEDGER.md`; historical consultation and literature are audited separately. No journal endorsement or acceptance is claimed.
