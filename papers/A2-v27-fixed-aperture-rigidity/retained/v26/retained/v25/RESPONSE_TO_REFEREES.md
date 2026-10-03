# Response to the v24 referee report

**Paper:** Qian Qi, *Reference-free certification from intrinsic boundary laws*  
**Report:** 3aeea88879dbba28a7564e3c5787ce293e3a45c8, 3 October 2026  
**Report blob:** 81646493b2011abb8edfa95b4eef795208ef7c0e  
**Reviewed author:** f5754f7eacc5b2bde9450de154a4e4c0093b3e23  
**Revision:** A2 v25, `papers/A2-v25-effective-local-recognition`

We thank the referee for separating the proved local acquisition mechanism from the remaining effectivity and information-category questions, and for identifying the stopping-exponent inconsistency. The response is mathematical rather than a change of journal target or subject: we make finite recognition effective from numerical prior bounds and replace derivative and arclength queries by certified local values. We retain the complete previous mathematical development and its successful source qualification without presenting it as qualification of the new source.

## 1. Compactness, changes of representatives and lattice walls

New Lemma 2.1 (`lem:presentation-compactness`) supplies the missing parameter-space statement. For each of the finitely many possible type counts, it keeps all bounded lattice presentations rather than choosing a discontinuous reduced basis. Steiner centers lie in closed coordinate parallelograms. Centered support functions converge uniformly on every narrower complex strip; this implies convergence of every fixed derivative. The physical and quantitative margins are closed conditions.

Bounded bridge length bounds the integer target label. On each fixed label stratum, strict convexity gives a unique closest pair, compactness gives continuity of that pair, and the positive contact Hessian gives smooth/analytic-chart continuity through each fixed derivative. The frame is defined using the quarter-turn of the normal, without an angular branch cut. Representative changes relabel k by k+m_i-m_j; basis changes act by U^{-1}k. At cell faces and reduction walls both presentations are kept. Equivalence is constant on a pair of fixed discrete-label strata. This closes the topology details used in the retained compactness proof.

## 2. Computing the fingerprint, not assuming usable constants

Theorem 3.4 (`thm:effective`) replaces the non-effective calibration step. Its numerical inputs are the explicitly stated support-strip and graph-disk bounds, curvature, diameter, bridge-length, physical separation, shape-separation and asymmetry margins. It requires no separate oracle for K_* or chi.

Lemma 3.1 proves an explicit real-interval-to-strip modulus by equispaced interpolation and a chain of three-circles estimates. With J=ceil(4/a), its exponent is 2^{-(J+3)}. Lemmas 3.2 and 3.3 convert small contact-graph values to close complete pair images and then use the positive physical separation to lock the actual translated target. Equations (3.3)–(3.8) give a finite recipe for the jet order, separation and sampling length. In particular, with P=m0*2^{J+3}, E_*=B*2^{-P} and chi_*=E_*/8, the required tail and mesh inequalities are explicit.

`tools/calibrate_fingerprint.py` implements exact rational bounds and symbolic integer expressions for this recipe. It does not round a tiny threshold to zero or pretend that an exponentially long fingerprint has been measured. The supplied example is an arithmetic input example, not a claimed physical realization of all of those numbers. The constants can be extremely conservative; the theorem supplies computability, not sharpness or a practical complexity guarantee.

## 3. Removing high-order derivative and arclength queries

The same theorem gives a second fingerprint S_N consisting only of the gap and the two graph values on a finite symmetric grid. A first-derivative bound fills the spaces between grid points; no high derivative is inferred from those values. Reversal permutes the grid coordinates. The retained registry proof therefore gives exactly the same class and coherent-sign decisions under arbitrary certified errors.

Theorem 5.2 (`thm:value-gates`) then implements the local record procedure with height-value and distance-to-solid enclosures. Its access model states chart coverage, coordinate directions, nonverticality and a numerical C3 bound. Lemma 5.1 gives certified first- and second-difference inequalities and uniform C2 reconstruction from O(nu^{-1}) height values at accuracy c*nu^3. A contraction test encloses the normal contact; the existing clearance test remains; intrinsic arclength is obtained by certified integration. Ambiguous cases are rejected, while protected inputs have a fixed slack and succeed under a finite budget.

This is a genuine sensor reduction, not a passive-trajectory claim. Local Cartesian coordinate access and distance to all solid in the permitted neighborhood remain additional observations. We neither infer them from endpoint laws nor assume away the work of producing them. Their costs are now displayed as a function of a value-query cost V.

## 4. The fixed a=6 inconsistency

Theorem 1.1 now uses a chosen a>=6 in both its quantifiers and its displayed tail. Its expected generic probe-work statement requires a>4+s, consistently with the unchanged schedule in Section 7. Section 5.2 explicitly notes that a=6 only proves that expectation bound for s<2; at s=2 the upper-bound series is harmonic. We do not infer actual infinite cost merely from divergence of that bound.

For the value-access implementation, V(epsilon)<=C epsilon^{-s_v} gives P_val(nu)<=C nu^{-(1+3s_v)}. The sufficient choice is a>=6 and a>5+3s_v. Launch count, square-range growth and statistical powers are unchanged; local measurement cost remains distinct from fitting, travel, setup and bit complexity. The exact tests include both the borderline failure of the fixed choice and the corrected inequalities.

## 5. Rich data, generic priors and classical ingredients

The abstract and Theorems 1.1–1.2 retain numerical analytic, shape, symmetry and geometric margins. Two endpoint windows remain two density functions or two growing histograms, not two numbers. The local values are an acquisition/recognition sensor; they are not relabelled as count observations. The global inverse still uses normalized probabilities, including failure outcomes, so unseen area is not lost by conditioning on success.

Section 8 separates this information set from boundary-distance, lens and exterior travelling-time data. It also records the general planar union-of-obstacles lens-rigidity result, not merely the constructive two-obstacle comparison. Interpolation, three-circles, finite differences, concentration and error spending are credited as classical mechanisms. The new claim is their explicit calibration for coexisting bridge recognition and the local value-access implementation, not a new general theorem of analytic continuation or concentration.

No minimax claim, passive discovery theorem, exact analytic count-only rigidity/nonrigidity result, or conventional marked-length theorem is inferred. A journal's significance judgment is not settled by changing terminology or by passing numerical checks.

## 6. Preserving the earlier paper while focusing the contribution

The primary remains theorem-led. Its new Theorem 1.2 identifies the effective/value-access refinement; Sections 3 and 5 contain its complete arguments. All six prior chapters remain active. Three chapters—local acquisition, the intrinsic inverse/completion certificate, and noisy stopping—are byte-identical to v24. The compactness chapter is expanded; the setting receives the necessary exponent correction and new theorem; the comparison is expanded.

The entire reviewed v24 paper, including all its source, historical companions, failed-run history and successful qualification, is retained as the exact native tree `3d729a1fe93e2250cd68494d149fbb6e90b4096e` under `retained/v24`. The original complete Supplement S tree is also unchanged. No previous manuscript or review path is edited. This preserves every prior result rather than using a shorter source package to hide omissions.

## 7. Source qualification and limits of this execution

The referee correctly closes the old source-delivery objection: v24's exact-SHA run 37107483439 succeeded, following the recorded layout failure at 37106889506. Those are historical facts about v24, not newly run v25 evidence.

The new independent v25 driver verifies its complete source pins, runs the new finite diagnostics in ordinary and optimized Python, builds the primary, and records actual commands, exits and digests. In full-package mode it requires an exact clean checkout, checks both retained native trees, and invokes the unmodified v24 driver as a nested requalification under the current SHA. Its historical raw diagnostics and reversible staged-only layout wrappers are retained, not silently suppressed.

The actual local source-content run passes 5,490 finite checks with identical normal/optimized output and compiles the 22-page primary without final TeX warnings. All rendered primary pages were inspected. The local run is not a Git checkout, does not execute a physical sensor and does not rebuild the retained volumes. The read-only hosted workflow must provide its own current-SHA result. Neither its definition nor its queue state is reported as success. Finite checks and compilation are not proof certification or referee acceptance.
