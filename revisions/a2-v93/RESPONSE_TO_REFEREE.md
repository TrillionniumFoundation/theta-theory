# Response to the referee: A2 revision 93

**Manuscript:** Projective polynomial observations: intrinsic geometry and additive normalization  
**Author:** Qian Qi  
**Date:** 19 September 2026  
**Controlling report:** `reviews/a2-v92-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md`  
**Report commit:** `37e03652f639930f5489dfee09150a7cba3964d7`  
**Reviewed v92 manuscript:** `d55c480f8cdf9f1327b4142bf1bb31a315f71b2b`  
**New branch:** `revision/a2-v93-constrained-newton-gauge-2026-09-19`

We thank the referee for distinguishing the results established in revision 92 from the remaining structural questions. The present revision takes Option B in Section 20 of the report as its principal task. It replaces the sufficient first-order exposure condition by a finite exact invariant of the full allowed polynomial perturbation space, proves the corresponding leading Hellinger-ball diameter, and transports this invariant through the unknown scalar normalizer. A positive family shows why the first-order filtration suggested in Section 7 must itself be enlarged: every first-order Laurent functional can vanish while a quadratic determinant term moves the spectrum.

The proofs, rather than the regression programs, carry these assertions. All twenty previously active proof and bibliography modules remain active and byte-for-byte unchanged. The new introduction reorganizes the contribution around global additive normalization and exact local constrained geometry. The earlier entrypoint and all historical derivations remain in the branch.

## 1. Exact constrained perturbation theory (report Sections 7, 14, 17 and Option B)

**Location:** `article/v93/constrained_newton.tex`, Theorem `thm:constrained-newton`, equations `eq:constrained-exponent` through `eq:exact-constrained-modulus`.

For a real linear space S of polynomial numerator perturbations, expand the determinant into its homogeneous parameter parts. At a root r of multiplicity m_r, write H_{r,j,a} for the coefficient of (z-r)^a in the homogeneous part of parameter degree j. The exact spectral exponent is

    alpha_r(S) = min { j/(m_r-a) : 1 <= j <= k, a < m_r, H_{r,j,a} is not identically zero }.

The complete spectral exponent is the minimum over the base roots. This is a finite coefficient calculation, not elimination over the original latent model and not merely an assertion that a Puiseux exponent exists. Polynomial-in-z perturbations are included in S from the outset.

The proof gives more than upper and lower orders. The local rational observation chart has an injective derivative because tau(P)>0. Its Hellinger ball pulls back, after division by t, to the Fisher ellipsoid of squared radius four. Retaining the terms on the minimizing Newton edge gives an explicit polynomial for each root cluster. The maximum bottleneck diameter of these cluster-root multisets over the ellipsoid is the constant C_S in

    omega_P^S(t) = C_S t^alpha + o(t^alpha).

Uniform root localization, the limiting-set assertion and positivity of C_S are proved in the text. The multiset metric takes the finite root-permutation quotient without differentiating a sorting map. Bases, numerator coordinates and the normalization functional are transported together.

### Why a linear visible-order test alone cannot classify the slice

The exterior-power identity in the same section gives

    alpha_r(S)^(-1) = max_j rho_{r,j}/j,

where rho_{r,j} is the pole order of tr(wedge^j(M^(-1) E_x)), considered as a homogeneous polynomial in the allowed parameters. The proposed first-order Laurent filtration is j=1. It can miss all the leading motion.

Proposition `prop:quadratic-exposure` constructs a strictly positive probability experiment for every m>=3. In suitable constant coordinates the base is diag(f,g), with f=z^m and g a monic polynomial having distinct positive roots away from zero. The fixed-total perturbations have upper-left entry zero, so their determinant is exactly

    f(g+h) - uv.

Every first-order trace is h/g and is analytic at zero for every allowed polynomial h. The term -u(0)v(0) nevertheless gives alpha=2/m. Allowing the monic normalizer to vary introduces a constant upper-left perturbation and gives alpha=1/m. The proof checks strict cell positivity, invertibility of the leading coefficient and tau>0. This family is in the declared positive rational experiment, not a claim about real-rooted stochastic alternatives.

## 2. Unknown normalizer and cancellations (report Sections 8, 12, 17 and Option C)

**Location:** Corollary `cor:free-normalizer-v93` and Propositions `prop:newton-gauge`, `prop:bigraded-gauge`.

For a free monic normalizer the allowed space is all degree-at-most-d numerator perturbations whose leading coefficient has zero entry sum. Constant rank-one perturbations are allowed. The exact local exponent is 1/nu, where nu is the actual pole order of the true resolvent. The proof does not require a flag, a first-order zero-sum exposure condition, or equality nu=nu_Q. In particular the retained 3-by-3 cancellation example has exponent 1/3 also in the full unknown-normalizer local experiment; its path-count certificate is 1/6.

This statement is deliberately distinguished from a uniform replacement in the earlier additive theorem. The inverse coefficient constant here depends on the fixed datum and can diverge with tau. We have not replaced nu_Q by nu in a boundary-uniform two-scale bound while silently retaining the old constants.

The scalar interpolation map gives a linear isomorphism

    E <-> (e, H),  E = H_e M + H,  e = entrysum(E),  entrysum(H)=0.

The complete determinant and its Hellinger metric are transported by this isomorphism. Its total homogeneous-degree invariant is therefore unchanged. A bidegree refinement gives the exact power along two-scale coefficient boxes: for scalar and zero-sum radii epsilon^A and epsilon^B, minimize (Ap+Bq)/(m_r-a) over the nonzero bidegree coefficients. This accounts for cancellations in the full gauge determinant, not individual triangular paths. Separate coefficient boxes must themselves be transported when the interpolation operator changes.

The older common-flag theorem is retained because it gives a different and stronger kind of uniform control. The new pointwise classification applies even to coefficient algebras without a common invariant flag; it does not purport to provide the same uniform additive certificate for that entire larger class.

## 3. Intrinsic and pointed singularities (report Sections 5, 6, 9, 16, 19.1--19.2)

**Location:** `article/v93/fibres_and_admissibility.tex`, opening paragraphs; new introduction, subsection on singular fibres and regular coefficient recovery.

The revision now separates three objects explicitly: the intrinsic observation germ using the whole exact fibre, the pointed latent germ (P,theta_0), and the strata inside the exact fibre. In the retained binary family, “the intersection a=b=x=0” denotes the selected pointed representative. Multiplicity and component equality do not label P_* intrinsically. Its whole-model spectral modulus remains exactly D-L; the monomial ideal describes transverse pointed arcs, not a vanishing intrinsic exponent.

The profiled quartic theorem is identified as a theorem about real-rooted root extraction after analytic coefficient recovery. The route for reconstructing its S is specified: normalizer, numerator coefficients, joint projectors and component tuples, then the profiled Fisher form, all modulo finite component relabelling.

The specific identifiable multi-defect stochastic normal form requested in Option A is not asserted to have been proved here. In particular the new rational theorem assumes tau>0 and does not fill that role by relabelling the totally nonidentifiable binary example. This revision instead supplies the definitive constrained-invariant theorem requested as the alternative Option B, including its scalar-gauge transformation. The original singular-fibre results and their proofs have not been removed or weakened.

## 4. Binary whole-model admissibility (report Section 10 and 19.4)

**Location:** Lemma `lem:binary-refactor-v93` and its application.

For K_epsilon=z A_epsilon-C_epsilon the normalized matrix is X_epsilon=C_epsilon A_epsilon^(-1). Its two simple real roots and projectors are analytic. The explicit formulas

    Q_b = (X - xi_(3-b) I)/(xi_b-xi_(3-b)),  W_b = Q_b A

give analytic rank-one coefficient matrices. Their base entries are strictly positive, so they remain positive on a base-dependent neighbourhood. Their total, row and column sums give the strict weights and stochastic columns. The lemma verifies the exact leading coefficient, constant coefficient, total numerator, weight sum, root interval and channel ranks.

The application to the zero-total binary moment perturbation recovers the exact determinant displayed in the report and both root derivatives -1/(2ab). The lower direction is consequently a tangent in the original stochastic model, not just in the space of algebraic pencils.

## 5. Fixed-margin comparison (report Section 11 and 19.7)

**Location:** Proposition `prop:compact-eta-v93`.

On compact regular classes with positive margins for cells, channel singular values, tau, weights, internal simple-root gaps, root intervals and complete-tuple separation, the exact Fisher condition and eta_d^(-1) are two-sided comparable. The proof uses continuity on the finite quotient and positivity of both quantities. Cross-component scalar collisions are allowed. This is a fixed-margin equivalence, not an exact identity or a bound uniform across the vanishing-cell counterexample. The proposition answers the positive compact-class question without claiming a maximality result for the margin conditions.

## 6. Editorial structure and relation to classical tools (report Sections 14--15, 19.3, 19.5, 19.8)

The title and general-journal objective are retained. The new abstract and introduction distinguish the stochastic closed model from the positive rational extension, the uniform certificate from a fixed-datum condition, and coefficient singularity from scalar root singularity. The main new result is one theorem with its exact leading constant; the gauge results and explicit examples are consequences or supporting propositions.

Resolvent expansions, exterior powers, Newton rescaling and root-counting arguments are treated as classical tools, with the existing primary references retained. The observation-specific statements concern the actual allowed numerator space, higher-order exposure, its Hellinger pullback, and the unknown scalar normalizer. The v92 “Exact cancellation test” remains an exact resolvent calculation in its original section; the new introduction explicitly distinguishes it from the complete constrained determinant classification proved here.

## 7. Source preservation, provenance and native audit (report Section 18)

The new revision is based on the exact v92 review commit. No old file is changed or deleted. The main input graph retains all twenty earlier active proof and bibliography modules, with two new proof modules and a new entrypoint/introduction.

The manifest separates `previous_review_commit`, `previous_revision_head` and `revision_source_commit`. The current `revision_head` is resolved from Git at execution and recorded in the audit receipt together with its tree; in Actions it must equal GITHUB_SHA. This avoids the impossible circular promise of storing a commit's own hash inside that commit. The manifest is the only intentionally self-unhashed metadata file. Every declared new source has byte count, SHA256 and Git blob identity. The pinned v92 manifest imports the exact old identities; the verifier checks all its active source identities, inherited blob declarations and verifier hashes, as well as preservation of the complete active graph.

The new workflow is limited to this revision branch and triggers on **every push**, without a paths filter. It fails on missing files, hash mismatches, unpinned additions, modifications of old files, unresolved TeX labels/citations, compilation errors, or overfull horizontal boxes. It emits an actual-HEAD receipt, complete manuscript PDF/log/text and source-response archive. It does not write to main or any other manuscript branch.

The local run has passed seven finite diagnostic groups: invisible first variations in degrees three and four; exact normalization rank; the 3-by-3 cancellation exponent; the scalar interpolation shear; the binary determinant and positive refactorization; and the Hellinger radius-two normalization. The new proof modules also pass a local TeX typesetting smoke test. A smoke test is not a compilation of the complete inherited manuscript. The remote exact-head workflow is the authoritative full-build check; its observed run status must accompany any delivery claim. Neither diagnostic success nor native compilation is a formal proof-verification claim.
