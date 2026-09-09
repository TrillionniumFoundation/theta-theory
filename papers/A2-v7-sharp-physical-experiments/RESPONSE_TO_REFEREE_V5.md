# Response to the A2 v4 referee report

Author: Qian Qi. Revision: A2 v5, September 9, 2026.

Controlling report: review commit `ec861ecfcdd83a81880c1a9082becc19b0c76977`, `reviews/a2-v4-nonlinear-boundary-laws-harsh-independent-2026-09-09/REFEREE_REPORT.md`. Reviewed author commit: `68bbf5b841a66dcc2b85f4d76ce66b1ae8b9782f`.

The report recognizes the relative half-line factorization and physical fixed-offset law as substantive and mathematically coherent, and gives an unfavorable venue assessment rather than a fatal counterexample. We preserve their full proofs and address the importance question by resolving two further inverse problems and extending the nonlinear geometric realization. We do not treat the addition of a formula, a diagnostic count, or a longer manuscript as an editorial acceptance criterion.

## NBL-R1: nonlinear information and the one-flight comparison

The requested comparison is now Proposition `prop:v5-one-flight` in `v5/20_contact_rigidity.tex`. It gives the diagonal at every even jet order, not only at order four. For the existing geometric fiber, the one-flight derivative is 8/9 and the limiting derivative is sqrt(3)/2. The introduction, abstract, and comparison section distinguish nonlinear information from information exclusive to long records.

The new positive result is Theorem `thm:v5-jets`. For identical even facing graphs, the coefficient of d^(m-1) is affine in q_(2m), with the strictly negative diagonal in `eq:v5-diagonal`. The proof separately differentiates the stationary action, the relative determinant, and the physical residual-time integral. It includes the finite-jet dependence needed to turn a diagonal computation into a recursive inverse. Every fixed finite jet has a locally Lipschitz inverse and an exponentially convergent finite-bridge approximation.

Corollary `cor:v5-analytic-rigidity` reconstructs the analytic contact germ from probabilities and leading normalization, and determines each participating connected analytic boundary in its contact frame by an explicit arclength-continuation argument. It does not reconstruct an unknown lattice or obstacles absent from the channel. Theorem `thm:v5-realization` realizes arbitrarily many finite jet coordinates by actual analytic obstacles at exactly fixed area, gap, curvatures, and leading metrics. Its area compensator affects none of the selected jets, and the support-to-graph triangular diagonal is calculated directly. These statements extend the previous one-parameter fiber without changing the general hypotheses of the boundary-law theorem.

The one-flight nonlinear inverse is also triangular. We therefore do not describe the new rigidity as a strictly increasing inverse-information hierarchy in flight number. The long theorem establishes the limiting physical law and its relative, uniformly differentiated convergence on a common collar.

## NBL-R2: a positive sharp pairwise inverse

Theorem `thm:v5-pairwise` in `v5/40_pairwise_inverse.tex` proves the full nearby pairwise estimate, including multiplicities, from C1,C2,C3,C4. Its proof first uses the elementary symmetric coefficients of the three radius deviations, not separately labelled roots. The count map extends analytically to a full coefficient neighborhood by the contour formula `eq:v5-contour`. Its four-dimensional Jacobian, including the unknown area normalizer, has the strictly positive Wronskian `eq:v5-wronskian`. The inverse-function theorem gives Lipschitz recovery of area and polynomial coefficients; a multiplicity-preserving Rouche argument gives matching root error of order delta^(1/3).

This allows area to be a nuisance parameter in an ambient observation model. In the actual fixed-gap support-function family it remains the constrained symmetric function printed in the inherited area identity. We do not introduce a spurious independent fourth shape parameter.

Theorem `thm:v5-sharpness` proves that 1/3 is optimal even in the weighted infinite-sequence norm with a strict exponential margin. It derives the report's two-sided physical path, the nonzero cubic coefficient, and sorted matching distance. The circular-reference 1/2 theorem is retained unchanged, with its different quantifiers explained alongside the pairwise theorem. Thus the response contains both the constructive pairwise inverse and its exact sharpness mechanism, not only an obstruction.

## NBL-R3: calibration and the raw preparation cost

Proposition `prop:v5-harmonic` gives the nonzero timing derivative -v H_m/h + O_m(1) for the previous normalization. The known-gap and timing theorems remain active and unchanged.

The new calibration experiment is Lemma `lem:v5-calibration` and Theorem `thm:v5-self-calibration` in `v5/50_self_calibration.tex`. At m+1 nearby programmed windows, square-root probabilities have a simple onset zero. The unknown area and rarity prefactor multiply the polynomial and do not affect its zero. A finite-degree Taylor/Lagrange argument gives root error O_m(h^(m+1)+h epsilon) from relative probability error epsilon. Importantly, it uses only positive nodal offsets, not a fictitious negative-offset physical probability.

Independent preparations stopped after a prescribed number of successes provide the probability estimates. The negative-binomial/binomial duality supplies both concentration and preparation cost. Fresh independent records are then collected for endpoint extrapolation. The combined procedure gives fine gap error O_m(h^(m+1)/j), curvature error O_m(h^m), and expected and high-probability preparation order e^(j gamma) h^(-2m-2) times the confidence logarithm.

The pilot root is constrained to a safe interval, with a zero fallback if the fit has no unique admissible root. Consequently every second-stage physical offset remains at least h/4 on every pilot outcome, not only on its successful event. This is needed for the unconditional expected-cost statement. The experiment presupposes the explicit coarse bracket |j(g-g0)| <= h/4; its acquisition cost is not charged or silently assumed solved. Fine calibration, unlike that initial coarse localization, is included. No minimax or successive-impact independence claim is made.

## Further analytical and bibliographic requests

`v5/15_differentiated_operators.tex` records the uniform Green operator norms, differentiated perturbation trace norms, and their precise use in differentiating logarithmic determinants. Only the zeroth-order product must have operator norm below one; its derivatives need bounded trace norms, not smallness. The same subsection explicitly states that parameter derivatives moving gamma can raise the principal pole order while the remainder stays holomorphic on smaller common domains.

The active bibliography adds De Simoi--Kaloshin--Leguil, Inventiones Mathematicae 233 (2023), 829--901, DOI 10.1007/s00222-023-01191-8. `v5/60_comparison.tex` distinguishes its analytic, symmetric/generic, no-eclipse marked-length problem from the present normalized statistical datum. The other Hill, marked-length, Prony, enriched-spectrum, return-time, and statistical comparisons remain, with separate hypotheses and observations. No exhaustive priority certificate is claimed.

## Organization, retained material, and verification

The main article is a complete native English manuscript with the central chain of geometry, relative factorization, physical law, and contact inverse. Referee correspondence and validation metadata are separate from the paper. All earlier mathematical proof chapters and circular appendices remain in the active article; the companion and historical Round 33 source are preserved. The general boundary-law setting has not been replaced by the symmetry assumptions of its specialized inverse application.

The independent diagnostic script has no repository imports or network access and uses explicit failure exceptions, including under python -O. The initial local run passes 175 finite checks: 136 exact and 39 ordinary floating non-interval. The latter include actual one-flight length/twist integrations for a sixth-jet perturbation, rather than evaluation of the asserted coefficient formula alone. The observed slopes converge toward -1/972. Build scripts separately audit the native source graph, compile both documents, and retain logs and hashes. None of these finite computations substitutes for a proof or an independent referee's assessment.
