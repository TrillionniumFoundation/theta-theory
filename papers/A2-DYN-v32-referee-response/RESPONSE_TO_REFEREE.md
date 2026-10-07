# Response to the substantive referee: A2-DYN revision 32

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Active source:** `papers/A2-DYN-v32-referee-response`  
**Controlling report:** `reviews/a2-dyn-v31-external-top4-review-2026-10-07/REFEREE_REPORT.md`  
**Report commit / blob:** `ea8b02f156b1d99633443103ae5e88eb96a89fce` / `068e7f72d813f9ce2a558fb237af624d5cca90af`  
**Reviewed author baseline:** `c0b184a89ff3d38675d0bc90a9e60b584476e5c3`  
**Baseline ordinary paper tree:** `06d63ae32efec644d907a0d3d0118c54b8e74c4c`  
**Date:** 7 October 2026

We thank the referee for the detailed assessment of the transverse-field extraction and microscopic inversion. This revision retains the original triangular family, actual section, four-coordinate return record and raw mixed-density endpoint. It addresses the requested source-geometric details with standalone proofs and adds a positive finite-band reconstruction of microscopic event measures on the original trajectory space. The new result is Theorem W. No inherited theorem, label or proof is removed.

The principal mathematical advance concerns the weighted class. Instead of trying to differentiate each downstream path selector, we regularize the unweighted endpoint law once and construct a likelihood between zero and one on the original probability space. Its error is controlled in source total variation. Consequently the finite-band formula is uniform against every bounded measurable trajectory statistic, including indicators of multiple physical-time observations. This is a weighted finite-band reconstruction theorem, not a Gaussian evaluation of the remaining finite integral.

## 1. The actual finite complementary integral

Theorem `thm:positive-spectral-approximation` gives a nonnegative finite-band density of the full actual law, with no smoothing in any lattice coordinate. From a positive extraction `mu=Q+E`, removed mass `delta`, and the all-label second derivative budget `A_2`, it proves

`||mu-mu_B||_TV <= 2 delta + 6 A_2/B^2`.

The kernel is explicitly `k(t)=3/(8 pi) [sin(t/4)/(t/4)]^4`. Its Fourier multiplier is the compactly supported cubic spline in `eq:positive-kernel-transform`. Unit mass, zero signed first moment and second moment 12 are proved in the text. The second-order Taylor cancellation gives the `B^(-2)` global density error. The three lattice coordinates are preserved exactly.

This advances the sharp interval formula of Theorem V to a positive global mixed-L1 reconstruction. It does not evaluate the finite complement on balanced, compact nonzero, peripheral or growing roof frequencies. Those spectral estimates remain in the original raw synthesis. We have not relabeled a reconstruction kernel as a Gaussian main term.

## 2. The pointwise common correction

The new all-label interpolation lemma proves

`A_1 <= 2 sqrt(A_0 A_2)`, and `sum_ell ||q_ell||_infinity <= A_1/2`.

These bounds are for the regular residual, not for the removed density. They allow us to estimate the source probability of a roof-interval boundary crossing under a positive bandlimited likelihood. They do not turn small removed mass into a small essential supremum of the original density. The exact signed pointwise ledger in `eq:geometric-common-raw-ledger` is retained, as are both uncontrolled terms identified in the report. The new mixed-L1 estimate is explicitly distinguished from the local essential-supremum target.

## 3. Microscopic denominators and positivity

For an event `A={J_n in {ell} x I}`, Theorem `thm:all-selector-finite-band` defines a likelihood `lambda_{A,B}` on the original source and proves

`||1_A-lambda_{A,B}||_1 <= delta + 2 kappa_1 sqrt(A_2)/B`,

where `kappa_1 <= sqrt(12)`. The bound is independent of the interval length, including arbitrarily shrinking bounded intervals. A union of at most `J` intervals per lattice fibre pays only a factor `J` in the second term; lattice labels are not averaged.

The approximate denominator `p_{A,B}=E lambda_{A,B}` is nonnegative because the likelihood is nonnegative, not because a signed Fourier integral was assumed positive. Corollary `cor:positive-microscopic-posterior` gives two exact alternatives. If the actual denominator is larger than the error, the normalized conditional measures differ in total variation by at most twice the error divided by that actual denominator. If instead the finite-band denominator has been evaluated and exceeds the error, it supplies a rigorous positive lower bound for the actual denominator and the corresponding posterior bound.

This is a conditional-measure approximation and an a posteriori denominator inequality. It is not a proof of the desired microscopic Gaussian denominator. No numerical evaluation of the billiard's full finite complementary integral is claimed in this revision.

## 4. The original stationary physical space

Proposition `prop:stationary-geometric-extraction` extends the positive geometric extraction to the actual equilibrium return suspension. Its entrance marginal is `rho_R nu_R^*`, with `rho_R=c* tau_R^*/mean(tau_R)`, not the bounded current-collision density. The latter is not substituted for the former.

The discarded mass is bounded by

`C [ exp((a n-c L)/2) + (L+1)^(1/2) epsilon^(1/32) ]`.

The one-return exponential moment controls the L2 norm of the roof bias. On each retained source piece the first-return roof is a finite collision sum, so the same zero-extension and divergence proof supplies

`A_2 <= C exp(C(L+1) log(C/epsilon))`.

The age coordinate and the entire physical path remain on the same suspension. Thus every bounded physical-path statistic may be used in the new weighted finite-band formula. The endpoint record is explicitly the return record from the actual preceding section origin. The theorem does not identify that return event with the original microscopic physical-time event. Their relative comparison at a Gaussian raw denominator remains a separate target, as the report requests.

## 5. Closing the bounded-selector class at the reconstruction stage

For every bounded measurable `W`, with no BV or finite-record requirement, the new estimate is

`|E(W 1_A)-E(W lambda_{A,B})| <= ||W||_infinity E_B`.

The second expectation is a finite Fourier integral of the full original weighted transform, with the same three lattice coordinates and the compact spline multiplier in roof frequency. The proof uses only the unweighted boundary-crossing estimate; it never differentiates the weighted pushforward and never treats an arbitrary path selector as an anisotropic multiplier.

The supremum over `|W|<=1` is exactly the variation norm of the two unnormalized measures on the original initial-state space. Hence the statement is uniform even for time-dependent or highly irregular bounded selectors. Intersecting with a further measurable physical-path event only decreases that unnormalized error. The corresponding selected posterior still requires its own positive denominator; the new corollary states this requirement and gives a finite-band lower-bound test for it. We do not infer a Gaussian denominator for arbitrary rare selectors.

For polynomial interval-fibre complexity and arbitrary prescribed polynomial accuracy, Theorem `thm:uniform-positive-microscopic-inversion` gives the explicit choices

`L_n=ceil(lambda n)`, `epsilon_n=epsilon_0 n^(-d)`,

`A_n=1+C exp(C(L_n+1)log(C/epsilon_n))`,

`B_n=n^(P+kappa+4) sqrt(A_n)`.

One may take `lambda>max(1,a/c)+1` and `d>32(P+5)`. Both the global mixed-L1 error and the unnormalized all-selector event error, multiplied by `n^2`, are `O(n^(-P))`. The bandwidth satisfies `log B_n=O(n log n)`; it is not claimed to be polynomial. Unlike sharp interval truncation, the positive-likelihood error has no logarithmic dependence on `B|I|`.

## 6. Self-contained geometry and specialist audit points

The new Section `sec:source-boundary-calculus` expands each geometric step singled out in the report.

- `lem:self-contained-collision-differential` derives the four entries from the differentiated flight equation and the incoming/outgoing tangential velocity, then proves determinant one and the action identity in the same block. No derivative formula is simply asserted from a distant reference.
- `lem:complete-first-hit-guard` defines the finite candidate set by the uniform horizon and disk radii. A positive root cannot pass through zero; two disk entry roots cannot tie at a positive point because the disks are disjoint. Every first-hit change must therefore meet one of the candidate discriminants.
- Four angular charts are specified. Their numerator degree, denominator bounds `[1,16]`, coordinate Jacobian bound and continuous positive coefficient minimum are shown explicitly. This supplies the uniformity needed for the existing polynomial sublevel estimate.
- `lem:source-partition-zero-extension` indexes the first forbidden collision or section decision. The corresponding earlier guard is identically zero on a two-sided neighborhood. Later, possibly undefined iterates are not differentiated or assigned an artificial smooth extension. The source vector-field products have the regularity needed for both distributional integrations by parts, and disjoint interiors prevent a symbolic multiplicity factor.

The fixed-table differential has also been checked against Section 3.1 of Stenlund--Young--Zhang. No new billiard theorem is imported. The stationary-bias extension uses the already proved suspension and exponential-tail identities. The positive kernel, interpolation, event operator and posterior estimates are proved here. Independent human specialist review has not been obtained in this author revision; the geometric null-set and zero-extension assertions remain explicit audit points rather than being certified by a script.

## 7. Presentation comments 1--7

1. The ambiguous abstract phrase has been replaced by the statement that the **logarithm** of the bandwidth is `O(n log n)`. The formulas and new theorem use `log B_n` consistently.
2. Differential, coordinate conversion, determinant and action are now in one self-contained lemma.
3. The complete first-hit guard and coefficient compactness argument have their own lemma.
4. A formal source-partition and zero-extension lemma precedes the stationary extension; the original extraction proof points to it.
5. The introduction separates Theorems V and W under a microscopic reconstruction heading, explicitly identifying them as approximations and reductions rather than the Gaussian raw LLT.
6. The main-text role diagram and updated final dependency guide collect the present status and distinguish section/equilibrium laws, L1/source-TV/local-Linfinity norms, and Gaussian results/finite-band reductions. Inherited proofs and meaningful scope statements are not arbitrarily removed.
7. The literature comparison now discusses the completed Gaussian, flow, conditional-path and source-regularization results relative to Szász--Varjú, Dolgopyat--Nándori and Baladi--Demers--Liverani. None is imported as a theorem for the full joint moving-section return record without checking its hypotheses.

## 8. Preservation and exact qualification

The baseline is the frozen ordinary v31 tree, including all 64 core modules and 67 Python files. All old mathematical labels and the bibliography are retained. The only changed inherited core files are the dependency guide and the two v31 modules, whose exact replacements are recorded in `INHERITED_EDITS.json`; all mathematical proofs in those two modules remain. Two new core files contain the added proofs. All inherited Python files are byte-identical.

The source verifier checks the entire old tree, replay of every declared edit, all old labels, every actual file hash and the read-only qualification workflow. The controlling report is frozen by its exact Git blob; a local validation without the report bytes records that boundary explicitly, while the exact remote qualification requires and verifies those bytes. Normal and optimized finite diagnostics, native typesetting and new-page rendering are separate from mathematical certification. No future workflow run is predeclared successful in this response.

The new proof is submitted for substantive re-review as progress on microscopic weighted reconstruction within the original raw mixed-density program. The unevaluated finite complement, pointwise common correction, Gaussian microscopic denominator and physical-event replacement are not silently declared closed.
