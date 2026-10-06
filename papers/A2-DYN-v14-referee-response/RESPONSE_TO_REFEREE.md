# Response to the referee: A2-DYN revision 14

**Article:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Revised directory:** `papers/A2-DYN-v14-referee-response`  
**Controlling report:** `reviews/a2-dyn-v13-external-top4-review-2026-10-06/REFEREE_REPORT.md`  
**Report commit / blob:** `014dbfa28501551a30388b44c0509fb7fbfbc444` / `0b505155503326568196c422034107cbfa8fc5ed`  
**Reviewed author baseline:** `47d2430dc14c4d98a9e80db6fd573b049be8808c`  
**Date:** 6 October 2026

We thank the referee for the detailed review of the unsmoothed moment, actual covariance and scalar nondegeneracy arguments. The principal addition in this revision is a proof of uniform positive definiteness of the entire four-dimensional return covariance. This addresses request A in Section 13 of the report. The proof does not evaluate a measurable transfer function on a prescribed periodic orbit and does not infer joint nondegeneracy from positivity of the count component.

The title, triangular Lorentz family, actual return section, joint displacement/count/flight-time record, and raw mixed-density endpoint are unchanged. Every inherited core module and theorem label remains. The new result is stated as Theorem E in the introduction and proved in full in Sections 25 and 26. The scalar count proof remains as an independent elementary argument.

## A. Full covariance nondegeneracy

**New conclusion.** Theorem `thm:joint-uniform-nondegeneracy` proves constants `0<d_0<=D_0<infinity` with `d_0 I_4 <= D_R <= D_0 I_4` for every radius in the original interval. It handles every real joint direction, including the discontinuous section contribution. The actual finite-return covariance inherits a uniform lower bound for sufficiently large return count, and the three-dimensional physical-time fluctuation covariance is uniformly positive definite as well.

The proof has three geometric and two cohomological steps.

### A.1. Exact collision action

Lemma `lem:exact-collision-action` derives `d tau_R = T_R*theta_R-theta_R`, where `theta_R=R p d alpha`, directly from the Euclidean flight length. The arrival tangential velocity equals the outgoing tangential velocity after reflection. Lattice labels are fixed on a regular branch and have zero derivative there. Summation gives forward and backward arc identities with their signs explicit.

### A.2. Measurable holonomy on positive-measure product sets

The only added geometric input is the qualitative local product structure for finite-horizon dispersing billiards, including homogeneous curves, contraction, positive-area product sets and absolute continuity. The exact source and its hypotheses are recorded in `GEOMETRIC_INPUT_MAP.md` and Lemma `lem:regular-collision-product`.

For a measurable unit-modulus phase, the proof disintegrates the restricted collision probability over stable curves and draws two conditionally independent points. Both pair marginals equal that restricted probability and hence are bounded by a fixed multiple of the full invariant measure. Smooth approximation therefore bounds the endpoint error after any iterate by the original `L1` approximation error, independently of the iterate. Contraction removes the smooth endpoint difference. The same construction works backwards on unstable curves.

This proves the phase holonomy identities for almost every stable and unstable pair. Product measure-class equivalence and Fubini then permit their multiplication around almost every quadrilateral, not around a preselected measure-zero orbit. The resulting identity forces the phase of `t` times the symplectic area to be an integer multiple of `2 pi`. Arbitrarily small nondegenerate quadrilaterals contradict this when the roof coefficient `t` is nonzero. Proposition `prop:measurable-roof-rigidity` thus excludes nonzero roof frequency without a pointwise Livsic representative.

No uniform local product or measurable-regularity constant in the radius is claimed. Pointwise positivity will be made uniform only through the already proved continuity of `D_R` and compactness of the parameter interval.

### A.3. Rotation products and a finite physical cover

The physical sixty-degree rotation acts on lattice coordinates by `A=[[0,-1],[1,1]]`. The exact identities `A^3=-I` and `I+A^2+A^4=0` cancel displacement phases in products of two and three rotated phase functions. Collision mixing then forces both `exp(2 i s)` and `exp(3 i s)` to be one; therefore `s` is an integer multiple of `2 pi`. This is Theorem `thm:physical-phase-rigidity`.

For a real spatial coboundary in direction `w`, rotation supplies a second equation in direction `wA`. Their determinant is `-(w_1^2-w_1 w_2+w_2^2)`, which is nonzero for every nonzero `w`. Hence both lattice coordinates would be real coboundaries. The physical billiard on the torus modulo twice the lattice would then possess the nonconstant invariant function `exp(i pi(H_1(x)+ell_1))`. Ergodicity of this finite-horizon four-scatterer billiard excludes that possibility. The enlarged torus is a real Euclidean billiard, not an artificial independent-sheet model; a rectangular eight-scatterer cover is also specified to avoid an affine change of the reflection law.

### A.4. Exact removal of the discontinuous section

For a zero-variance direction `(w,a,b)`, the inherited actual `L2` kernel theorem gives

`w.kappa_R + a + b tau_R - zeta eta_R = B-B o T_R`, with `zeta=(a+b mean(tau_R))/c*`.

When `zeta` is nonzero, exponentiation by `2 pi i/zeta` removes the integer-valued `eta_R` exactly. Physical phase rigidity forces `b=0` and `a/zeta` integral, whereas `a/zeta=c*` lies strictly between zero and one. This is a contradiction.

When `zeta=0`, exponentiation of the remaining physical identity first forces `b=0`; then `a=0`. The real spatial obstruction forces `w=0`.

This exhausts all joint directions. Importantly, the rotations act only after the section term has disappeared. No rotational invariance of the chosen return section is presumed.

### A.5. Uniformity and consequences

The continuous symmetric covariance has no nonzero kernel at any radius. Compactness supplies a positive lower eigenvalue over the original interval. The proof gives existence of this constant, not a numerical value. Theorem D's actual covariance rate transfers it to finite-return covariance matrices. The Gaussian density involving `det D_R` and `D_R^{-1}` is now unconditionally defined for this family.

## B. Complete complementary-frequency region

The new phase theorem excludes exact measurable collision phases at nonzero roof frequency and at nonintegral constant phase. This is a useful qualitative obstruction, but the manuscript does not turn it into an unproved norm estimate for approximate spectral vectors or an induced high-frequency resolvent.

Uniform ellipticity also gives an explicit Gaussian tail: the rescaled Gaussian integral outside `n^(1/200)` is at most `C exp(-c n^(1/100))`. This discharges the Gaussian-tail and covariance parts of the existing central inversion argument. It does not bound the complementary transform of the physical record or its edge-subtracted residual.

The physical central radius remains `2 n^(-99/200)`, with rescaled radius `2 n^(1/200)`. The annulus up to a possible `n^(-2/5)` outer regime, nonzero torus frequencies, growing roof frequencies and far roof tail still require the complete quantitative estimate requested by the referee. These regions are not omitted or declared covered by the new qualitative result. The covariance premise has been removed from the existing initial and marked inversion interfaces; their complementary-transform hypotheses remain explicit.

## C. Complete critical/singular raw branch decomposition

All exact raw-edge calculations, local inversion formulas and absolute residual-sum criteria are retained. The new proof does not differentiate a many-return coarea density and supplies no estimate for its second distributional derivative sum. Every regular critical word, grazing or competing-root boundary and dynamically generated image boundary still belongs in the full extraction. The true return-count growth of the resulting residual norm must be used in the frequency splice.

This revision removes the covariance obstruction in that same synthesis. It does not replace the required raw branch sum with a collision moment or initial-coordinate BV bound.

## D. Weighted conditioning and exact physical observations

Theorems C and D and their same-event conditional corollaries remain unchanged in their mathematical estimates. Their matrix is now known to be uniformly positive definite. The normalization remains the restricted collision measure for the complex insertion, with the section probability obtained by `a=s_R`.

The weighted complementary tails, edge estimates, and relative event replacement required for an exact physical observation are not consequences of nondegeneracy. Single marked-state events, terminal return-state insertions, multiple-time path events and exact lattice/time observations remain distinct. No indicator or denominator is changed in this revision.

## E. Independent specialist review and proof imports

The new qualitative billiard input is identified explicitly rather than labeled a consequence of an unspecified measurable Livsic theorem. The regular product set, conditional-pair approximation, four-corner Fubini argument, action-form sign, rotation symmetries and finite-cover realization are appropriate focal points for the next specialist review. No independent human specialist review is claimed here.

The source-to-norm appendix and the inherited Demers--Zhang collision-space import remain intact. The new proof uses their established mixing and covariance-kernel consequences, but introduces no unbounded induced twist on those spaces. The analytic part of phase rigidity is proved in the paper; the local product geometry and finite-horizon cover ergodicity are the stated external inputs.

## Presentation comments 1--10

The abstract now distinguishes the retained scalar count argument from the newly proved full covariance theorem. Theorems A--D keep their original statements; Theorem E supplies the stronger conclusion, and cross-references in the inversion and final-synthesis sections are reconciled accordingly. The count proof now explicitly states both `|q|=1` and `2 pi c*=91/5000`, and includes the two-factor `L2` approximation inequality requested in comment 4.

The distinct `n^(-1/6)` actual covariance/stopping rate and `n^(-2/9)` characteristic stopping rate are retained. Every induced correlation conclusion continues to say Cesaro where appropriate. Measure conventions and the event distinctions are unchanged. `INHERITED_EDITS.json` records every exact replacement in the inherited manuscript; the verifier replays those changes rather than relying on a blanket preservation statement. Publication metadata and dynamic execution receipts make no journal-acceptance or formal-certification claim.

## Source qualification

The source verifier includes all 33 core modules and retains all inherited mathematical labels. Twenty-three inherited core files, every inherited Python file and the bibliography are byte-identical; eight core files have precisely listed changes. New exact algebra checks cover the rotation identities, determinant, constant-phase cancellation, action-form sign and finite-cover cancellation. Independent high-precision finite physical calculations check 96 action partial derivatives and 240 rotation identities on 48 regular states. These computations test the implemented formulas, not continuum product structure, ergodicity or proof completeness.

The workflow checks out and archives the event SHA, runs normal and optimized diagnostics, compiles the complete article and emits an exact-run receipt and PDF hash. The static response does not predeclare the result of a future run. The new source and the additional nondegeneracy proof are offered for substantive re-review of the same raw mixed-density problem.
