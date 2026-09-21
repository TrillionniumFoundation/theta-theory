# Preservation and proof dependencies: A2 v112

## Immutable baseline

This branch starts from the controlling R111 review commit `cafc6c1bd403dae4acc66177fb43feee54c02b1d`. The reviewed mathematical source is `1e21bcbe1741c9fb67a8b3fabe0f6bc20cfdb559`, with reviewed head `f7c55b929c8750a98c9219803863e746968a423d`. No main, historical revision, or review branch is edited.

All changes relative to R111 are new files under `article/v112/`, its branch-only workflow, and its root index. The source-bound verifier rejects modifications or deletions of inherited files, not only changes to a few selected manuscripts. It also pins historical principal and experiment blobs.

## Content retention

All 68 inherited LaTeX labels are retained. The complete files `02-global-geometry.tex`, `03-realization-stability.tex`, and `05-complements.tex` are copied byte-for-byte from v111. They retain the full c>=4 codimension proof, its small-case arithmetic, sharp native threshold and exact realization proofs, quantitative inverse estimates, spectral examples, classical maximal rank, monomial comparison, finite categorical and observed-exposure estimation, computed finite-offset encoding and independent-noise comparison, complete-contact ambiguity, three-site native relations, scalar query count, reciprocal design fibres, endpoint representations, and deterministic root costs.

The revised introduction changes the conceptual order, adds a precise literature comparison and states the new geometry. It retains both original introductory theorems and the complete contact/native derivations. The statistics part retains all earlier results and adds the quantitative proof, explicit moment control, deterministic finite precision, and the full exposure nuisance decomposition. No conclusion is deleted to avoid the review.

## New dependency graph

1. Classical Hankel exact-rank dimensions + relative isotropic dimension count -> the already proved full-range codimension theorem (Sections 1 and 4).
2. Strict endpoint gap in c>=8, k>=2c+1 -> only rank-two and full-rank incidences can dominate maximal components.
3. Unique secant hyperplane from a general first plane -> 2^(L-1) distinct birational signed incidences.
4. Nondegenerate isotropic incidence is smooth and irreducible and contains non-secant planes.
5. In expected codimension: maximal-minor grade -> Eagon--Northcott -> purity and Cohen--Macaulayness. Steps 2--4 identify the full-rank component and all possible components. Dimension of the projective annihilator fibre gives generic corank one.
6. For signed components: remove the two secant points -> residual saturation a>=b -> the OLD full-range theorem applied to (k-2,c-1) -> residual product span -> tangent dimension -> generic scheme smoothness. This is not an induction using the new theorem.
7. Generic scheme reducedness on every minimal component + Cohen--Macaulayness -> reducedness of the entire expected-codimension scheme. One component gives integrality. Thom--Porteous then computes its fundamental cycle.
8. Positive native incidence + birationality + loading submersion -> smooth real strata. Schur row and conormal coordinates -> local singular-value/distance comparison and local tube exponents.
9. Quantitative Poisson step-density L1 estimate -> raw/jittered Gaussian comparison in both deficiencies -> known-mark score experiment. Deterministic quantization, boundary mass control and cell-average reconstruction give the finite-precision alternative.

## What is not promoted to a theorem

No full low-dimensional component classification; no global reducedness claim in excess codimension; no normality or complete singularity classification; no dimension-uniform global random-design bound; no physical observation of distance jets; no automatic global sufficiency for unknown marks or an estimated centre. The prior sharp full-range results remain unchanged despite these limits on the new stronger conclusions.

## Reproducibility

`SOURCE_MANIFEST.json` lists mathematical-input SHA-256 hashes. The full build verifies the actual Git checkout and additions-only diff before writing a source-bound receipt. The inherited finite checks are rerun; new strict-gap and signed Jacobian checks are stress tests only. The five-volume build compiles the unchanged v111/v110/v109/v108 companions as well as v112. Logs and PDFs are bound to the source commit that produced them; a later evidence-only commit must not be confused with the mathematical source commit.
