# Response to the independent referee on A2 revision 75

**Revision 76 — September 17, 2026**  
**Manuscript:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Author:** Qian Qi

The report addressed here is `reviews/a2-v75-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`, frozen at repository commit `ab44ba96a9fceeaa69bf4dbc98e5bfdd33b0cb5c`. Its mathematical baseline is the source commit `89d5a3aa3e9f00a806d48f19f6f6831770184d76`, manuscript tree `8a1a76ffba5009a6c3d9ed2e3c93e48a59f3ac1d`. Connected comparison found no manuscript changes between that source and the review head.

We thank the referee for distinguishing a concrete narrative inconsistency from correctness and from the separate question of significance. This revision corrects that inconsistency, adopts the integrated conditioning discussion, and extracts two precise statements from the central mechanism. One of these gives a phase-dependent improvement of the sufficient smooth inverse order. The marked local theorem, its complete proofs, the normal-incidence protocol, and the full technical programme remain present. We do not equate compilation, preservation, or the number of new statements with resolution of the placement judgment.

## R75-P1: principal transitions and the quadratic inverse

**Addressed.** The active principal copies are now `journal/core/periodic_relative_v76.tex`, `periodic_contact_v76.tex`, and `positive_curvature_v76.tex`.

The contact section promises exactly what it proves: action extraction and signed finite-jet factorization for actual smooth boundaries. It identifies the analytic function-space inverse as an extension in the full manuscript, rather than a theorem about to be proved in the principal slice. The next section is titled **Global identification of the positive quadratic parameters**. Its opening explains that the Schur contraction establishes quadratic image, global uniqueness, and residual control; actual smooth germ identification follows in the smooth-contact section. No appeal to a nonexistent preceding analytic theorem remains. The relative-law opening and conclusion now direct the reader to the general periodic smooth route and name alternating, analytic and lattice results as full-manuscript extensions.

The three inherited mathematical proof bodies are unchanged. Their former core files are retained at their original paths. The former `main.tex` and `rigidity.tex` are also retained byte-for-byte in `archive/v75-before-v76/`. The six full-entry reference aliases remain comparison/extension links, not hidden premises.

## R75-C1: inverse order, observation conditioning, and budget

**Adopted.** The new section `article/10m_conditioning_budget_v76.tex` puts the following dependencies together:

1. The strict scalar condition is `m > log(7)/(-log(a))`; the least permitted integer is `max(3, floor(log(7)/(-log(a)))+1)`. The inverse prefactor is `2/(1-theta_m)`. Choosing a target tail margin is distinguished from choosing the smallest admissible order.
2. The report's order examples are derived and independently recomputed: for `a=1/2,9/10,99/100`, the minimum orders are `3,19,194`; at `s=1` the accepted-mark exponents are `1/9,1/41,1/391`. A tail margin at most `1/2` requires orders `4,25,256` and bounds this particular inverse prefactor by four. This can increase the required regularity and worsen the sampling exponent.
3. The phase-weighted refinement below replaces `a` by the geometric mean of **common per-phase bounds on the whole interpolation class**, not by a product evaluated at one reference table. Its unweighted cost includes the ratio of the largest and smallest phase weights.
4. The section derives the separated-offset denominator and inverse derivative, identifies the obliquity/slice floors for the one-law route, and displays the nonsymmetric affine moment inverse. The affine example is an algebraic model, not an asserted positive-curvature realization.
5. The same section carries the accepted-mark estimate through exponentially rare acceptance, returning-flight rounding, and the exact finite-area sensitivity. It retains the count and bandwidth conditions, bounded readout error only after exact acceptance, the finite-flight defect, and the factor `1+N` in logarithmic area error.

These are sufficient upper bounds, not a weak-hyperbolicity impossibility theorem, a sharp lower bound, or a computational efficiency guarantee. The report is credited here for requesting the integrated discussion and for its scalar-order examples; the displayed calculations are proved in the paper and tested independently.

## R75-E1 and E3: the reusable mechanism

**Addressed mathematically, without claiming to settle placement.** The revision adds two statements in the existing proof route, not a new observational task.

### Relative determinants

`article/10k_relative_decoupling_v76.tex`, Proposition `prop:v76-determinant`, separates a perturbation into two diagonal end blocks and an off-diagonal coupling. With a common operator-norm margin, the first off-diagonal variation of `log det(I+T)` vanishes. The exact second-variation identity bounds the coupling by the square of its Hilbert--Schmidt norm, with no matrix-dimension factor. Each fixed-order parameter estimate retains two differentiated coupling factors. A separate trace-norm error accounts for deleting the middle or changing the end blocks.

This is an explicit refinement of the retained trace-transport mechanism, not a claim that trace-ideal estimates or logarithmic determinants are new. The application states which localization and Green estimates provide its hypotheses. The adjacent conditioning corollary shows why an arbitrarily small reference mass cancels before forming the conditional law. It does not divide an absolute error by a rare-event probability.

### Actual-function envelopes and a phase-dependent sufficient order

`article/10l_phase_weighted_envelope_v76.tex`, Proposition `prop:v76-envelope`, treats the actual integrated stationary envelope as a componentwise inequality `H <= alpha_*^{-1} G + K_m H`. The entries of the nonnegative matrix `K_m` sum the weighted visits to each phase. When its spectral radius is less than one, iteration gives the explicit bound `(I-K_m)^{-1}`. This is a comparison between actual candidates, not an algorithm pretending that its pair-dependent coefficients are observed.

For periodic visits with common one-step bounds `a_hat_i`, the matrix is exactly `6 A_m(I-A_m)^{-1}`, where `(A_m z)_i=a_hat_i^m z_(i+1)`. Its positive cyclic weight conjugates `A_m` to `a_bar^m` times a cyclic permutation, where `a_bar=(product a_hat_i)^(1/r)`. Consequently the sufficient condition is `6 a_bar^m/(1-a_bar^m)<1`. The weighted constant is `2/(1-theta_m)`; the ordinary norm includes `kappa(w)`.

Corollary `cor:v76-phase-stability` carries this refinement through the already proved finite-jet alignment and polynomial comparison. The common bounds must hold on the enlarged positive class containing those alignments. The graph prior remains `C^(m+3)`, and all small-error and observation floors remain. No curvature control is inferred from a final `C^0` estimate. The original worst-phase theorem is retained as a special sufficient condition.

The finite checker includes a positive heterogeneous Jacobi/visit fixture where the refined order is three while the scalar maximum bound requires nineteen. It is explicitly **not** offered as a geometrically realized table or a universal conditioning improvement. The actual billiard corollary follows from the proved one-step composition and stationary envelope, not that fixture.

These results clarify how the relative physical limit and the smooth inverse fit together, and give a quantitative strengthening inside the same theorem. They do not reconstruct supplied marks or remote arcs, remove the exact-gate premise, or solve an unreset-orbit problem. Whether this suffices for the requested general-journal placement remains a substantive question for the next referee.

## R75-E2: comparison with existing inverse problems

The corrected planar Noakes–Stoyanov theorem, the analytic marked-length result of De Simoi–Kaloshin–Leguil, and the enriched-spectrum Sinai result of Finamore–Leguil retain their distinct data, classes, and conclusions in the introduction. We make no same-data dominance or exhaustive priority claim. The new abstraction is not used to erase those distinctions. The low-rank moment identity remains attributed to the classical mechanism and subordinate to the physical-to-smooth theorem.

## R75-M1–M6: interfaces retained for renewed review

| Examined interface | Revision-76 disposition |
|---|---|
| M1: exact transfer/cofactor and relative normalization | All original proofs retained; the dimension-free off-diagonal estimate supplements, not replaces, them. |
| M2: residual clock, adjacent-flight window, measured coordinates, Liouville normalizer | Unchanged, including phase/flight distinction and actual endpoint Jacobians. |
| M3: two-offset extraction and global positive quadratic inverse | Mathematical bodies unchanged; principal opening corrected. |
| M4: signed finite jets and actual smooth inverse | Unchanged original route, including flat differences and polynomial alignment; phase-dependent strengthening added with proof and class requirements. |
| M5: locality, one-law offset, complete finite record | Actual remote completions, oblique-only single-law hypothesis, finite-clock correction, same-gate exact area anchor and logarithmic twist sensitivity retained. |
| M6: moment compression and charged estimation | Nonsymmetric inverse, paired weights, nonzero finite-flight rank defect, actual-table selection, full KDE terms, charged failures and normal-incidence two-offset appendix retained. |

## Preservation and verification boundary

`verification/v76-baseline-preservation.json` records all 1,017 inherited source files, including exact locations for the two archived changed entrypoints. `verification/v76-inherited-labels.json` records all 1,435 inherited active labels. The new checker verifies their continued reachability in the three-entry union, all principal references, unchanged inherited core proof bodies, exact phase/Jacobi and determinant identities, and conditioning arithmetic. Its assertions remain active under `python -O`.

The inherited source checks remain enabled, with their own stated scopes. `tools/build_revision_v76.py` builds the companion, full manuscript, and principal manuscript in isolated source-matched trees and records dependencies and PDF hashes. The native-delivery ledger identifies the actual source commit and build results; source text does not pre-announce an unrun CI result. Finite checks, compilation and sampled visual inspection are not formal proof verification or editorial acceptance.
