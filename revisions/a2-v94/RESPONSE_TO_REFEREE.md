# Response to the referee on A2 revision 93

Revision 94 — 19 September 2026

**Controlling report:** `reviews/a2-v93-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md`, commit `7d5e9d80a6033399afe633da21b44e4d6f435a2f`.

**Reviewed manuscript:** v93, commit `2832f7a7060217f6c8110688b66b73b9b946d13a`.

**New branch:** `revision/a2-v94-germ-newton-stochastic-intersection-2026-09-19`.

**Complete entrypoint:** `papers/A2-v17-boundary-information-coarsening/rigidity_v94.tex`.

We thank the referee for separating the success of the affine rational theorem from the missing geometry of the stochastic admissible germ. This revision follows Option 1 of the report. Its main result is a full-germ Newton law, and its principal application is a spectrally identifiable stochastic rank-loss intersection. The previous affine rational, global additive, quotient, statistical, and common-flag results remain active in the appendices. No inherited source file or report is overwritten.

The mathematical claims below are accompanied by proofs in the manuscript. Finite diagnostics and a local typesetting check are recorded separately; neither is presented as universal proof verification or as a successful complete native build.

## 1. Major objection I: compose with the actual admissible germ

**New sources:** `article/v94/germ_newton.tex`, Theorems `thm:germ-newton-v94` and `thm:composed-jets-v94`.

The central theorem no longer assumes an affine numerator slice. Let X be the compact semialgebraic admissible parameter space, F its observation map, and A_x the monic spectral polynomial. Assume only that the spectral polynomial is constant on the entire exact observation fibre. After analytic factorization into the separated base-root clusters, write the cluster coefficients as c_{r,a}(x). For the actual Hellinger ball B_P(t), set

    b_{r,a}(t) = max_{x in B_P(t)} |c_{r,a}(x)|,
    alpha_P = min_{r,a} ord_0 b_{r,a} / (m_r-a).

This is a finite collection of coefficient envelopes, not an optimization over an arbitrarily selected tangent space. The simultaneous rescaling of all cluster coefficients gives a compact joint limiting fibre C_0. Its image under the cluster-root maps supplies the exact leading diameter:

    omega_P(t) = C_P t^{alpha_P} + o(t^{alpha_P}).

The proof establishes boundedness, Hausdorff convergence of the joint coefficient sets, uniform root-multiset convergence, strict positivity of the leading diameter, and the rigidity alternative. The dependence among coefficients is retained in C_0; replacing it by the product of its coordinate projections would generally give the wrong constant.

For the closed stochastic model we use A_theta = product_b f_b, rather than det K. Thus the construction remains meaningful when a channel loses rank and det K vanishes identically. The full exact observation fibre is included throughout. No injective Jacobian, channel-rank condition, positive cell floor, or tau condition is imposed by this general theorem.

The earlier v92 result already established existence of a semialgebraic modulus and a Puiseux exponent. We do not count that existence statement again as the new result. The additional content is the finite cluster-coefficient Newton formula, its joint leading coefficient object, the exact root-multiset variational constant, and the composition with actual model constraints.

On an immersed analytic chart, the second theorem gives an explicit homogeneous-jet formula after composing the determinant with the whole coefficient map. In particular, its second-order term contains both

    D det(M)[E_2]  and  (1/2) D^2 det(M)[E_1,E_1].

Once any nonzero candidate edge is found, the proof gives a sufficient finite jet cutoff for the leading exponent and constant. There is no assertion of a universal cutoff for arbitrary analytic germs; local rigidity requires an identity, not a fixed finite list of vanishing derivatives. When the observation Jacobian is singular, the full-germ theorem replaces the Fisher-ellipsoid formula.

Proposition `prop:curved-cancellation-v94` gives a family whose complete determinant is g(z)(z^m+x^q), while its affine tangent determinant is g(z)(z^m-x^2). The first predicts q/m and the second 2/m; deleting x^q gives local rigidity with the same tangent. This directly addresses the referee's warning about higher model jets. The example is explicitly a positive rational experiment, not a claimed stochastic factorization.

## 2. Major objection II: an identifiable intersecting stochastic singularity

**New source:** `article/v94/stochastic_intersection.tex`, Lemma `lem:cubic-pencil-v94` and Theorem `thm:stochastic-intersection-v94`.

Take the original binary cubic model on [0,1], at seven or more clocks above one. For 0<r<1 and s=2r/3, choose

    f(z)=z(z-r)^2,    g(z)=(z-s)^3.

The first channel has two equal strictly positive columns, hence rank one. The second channel is strictly positive and invertible, and the weights are strict. The datum has positive cells, a channel-rank defect, an internal double root, an internal triple root, and an endpoint root. Its ambient coefficient observation Jacobian is not injective.

Nevertheless, its *entire* closed-model exact spectral fibre is a singleton. The proof does not fix the channels of competitors. It first establishes tau(P)>0 directly from the second marginal and coprimality. The rank-two second-marginal coefficient matrix then forces every competitor component polynomial into the monic affine pencil h_c=(1-c)f+cg. The identity

    disc(h_c)=-(4r^6/27)c(1-c)^2

together with the endpoint and real-root variance constraints implies that this pencil meets the permitted real-rooted interval set only at c=0 and c=1.

The local upper estimate is also a whole-model estimate. A quantitative form of the pencil lemma gives coefficient distance O(delta), not merely exact identification. Near its triple-root endpoint, the depressed-cubic inequality |b| <= 2(-a)^{3/2}/(3 sqrt(3)) is essential; the discriminant inequality alone would give an insufficient bound. The second-channel inverse is controlled uniformly over nearby closed-model competitors using the rank-two marginal coefficient matrix. Anchored real-rooted extraction then gives omega_P(t) <= C sqrt(t).

For the lower bound, keep the channels and weights fixed and replace g by

    g_u(z)=(z-s)((z-s)^2-u^2).

These are actual admissible stochastic alternatives. Their target displacement is |u|, whereas their Hellinger distance is gamma u^2+o(u^2), with gamma>0. Consequently the intrinsic exponent is 1/2. The main germ theorem gives the exact leading variational constant, and the statistical corollary gives shrinking-observation-ball squared risk of order N^{-1/2}.

This is not the nonidentifiable binary full-collapse example from v92-v93, nor an affine numerator perturbation declared stochastic without a factorization argument. It is an identifiable rank-loss intersection in the original closed model. The square-root value is not advertised as a new scalar root exponent: the new point is that the whole-model law holds despite the singular ambient coefficient inverse, because the nonlinear admissible set removes its kernel directions. The boundary constraint is part of the example and is not hidden as an interior assumption.

## 3. Major objection III: metric transport under left-right changes

**New source:** `article/v94/metric_transport.tex`, Proposition `prop:metric-transport-v94`.

We separate the algebraic and statistical assertions. For T(M)=AMB, the determinant changes by the nonzero scalar det(A)det(B), so its root exponents are algebraically invariant. The exact metric constant is invariant only when the observed experiment is transported as well:

    h_tilde(Q,Q') = h(T^{-1}Q,T^{-1}Q').

With vectorized T and Fisher matrix H, this gives

    H_tilde = T^{-T} H T^{-1},    J_tilde = T J,
    J_tilde^T H_tilde J_tilde = J^T H J.

The proof therefore transports both the ellipsoid and the full observation balls, not only the determinant. The convention is stated explicitly as a hypothesis of the retained v93 invariance assertion. Arbitrary transformed entries are not reinterpreted as probability cells. The historical v93 source remains byte-for-byte available; the operative additional hypothesis and its proof occur in the new main text before that appendix.

## 4. Major objection IV: intrinsic means image-germ intrinsic

The new theorem is formulated on the joint image of the actual observation map and spectral polynomial map. Analytic or semialgebraic changes of admissible coordinates preserving that image germ leave its coefficient envelopes, joint limiting set, and leading diameter unchanged. The assertion does not assume that the parametrization itself is injective.

The three notions requested by the referee are now separate: linear basis invariance of an affine slice; linear scalar-gauge covariance; and invariance of the full admissible observation germ. In an analytic chart, nonlinear changes require composition of *all* relevant jets; the theorem explicitly makes that composition.

## 5. Classical ingredients and contribution accounting (report Sections 8 and 10)

The introduction continues to credit rational interpolation, matrix-polynomial root perturbation, semialgebraic elimination and Puiseux preparation, latent factor identification, and inverse-modulus inference. Neither reciprocal unstructured pole orders nor existence of a semialgebraic Puiseux law is presented as new in isolation. The v93 compact eta comparison is retained as a compactness proposition, not as the conceptual centre of the article.

## 6. Two-scale boxes and local-to-uniform quantifiers (Sections 9 and 13)

The v93 two-scale result remains a coefficient-box statement. Changing the interpolation operator shears its coordinates and requires transporting those boxes. We do not identify its bidegrees with two independently observed statistical errors.

The global common-flag theorem and its uniform constants are preserved. The exact germ constants are datum-dependent. This revision does not claim the optional local-to-uniform degeneration theorem described as Option 3 in the report; it takes Option 1 instead. No pointwise pole order is inserted into a boundary-uniform theorem with its former constants unchanged.

## 7. Binary refactorization and fibre distinctions (Section 11)

The successful v93 binary refactorization proof remains active and unchanged. Its selected pointed collapse, its nontrivial intrinsic exact fibre, and the new identifiable cubic rank-loss datum are kept distinct. No spectral multiplicity of an arbitrary latent representative is assigned to an observation whose exact fibre changes that multiplicity.

## 8. Statistical integration (Section 15)

Corollary `cor:germ-risk-v94` applies to the new full-germ law, including the stochastic intersection. On radius c/sqrt(N) observation balls, it gives explicit two-sided leading risk bounds proportional to C_P^2 c^{2 alpha_P} N^{-alpha_P}. It is a minimax rate statement with an explicit constant sandwich, not an unproved exact decision constant. This is the same experiment and Hellinger convention used in the existing two-point argument.

## 9. Manuscript architecture and preservation (Section 14)

The main text now develops one principle: the intrinsic Newton geometry of the observed admissible germ. It contains the model and additive theorem, the full-germ and composed-jet proofs, the stochastic intersection, and the metric-transport theorem. The global normalization, clock design, quotient charts, regular Fisher inference, earlier singular forms, algorithms, statistical lower constructions, common-flag bounds, and affine rational results are all active in the appendices.

All twenty-two previously active proof and bibliography modules are imported without byte changes. Both historical v93 wrappers are retained in the repository, although the new entrypoint uses the new introduction. The active v94 graph has twenty-seven TeX inputs. The original report is inherited from the new branch's base commit and is not paraphrased in place of its source.

## 10. Smaller points (Sections 12 and 17)

The new metric section explicitly specifies complex root multisets, complex Euclidean modulus, and the conjugate constraints for real coefficients. The local affine competitor set includes a fixed sufficiently small coefficient neighbourhood in its formal definition. The scalar interpolation operator is denoted T_P(e), with the old notation identified as an operator, not multiplication. The infinity-exponent case is accompanied by the algebraic divisibility explanation.

The active v94 diagnostics use the corrected analytic-first-variation failure message. The historical v93 verifier is not edited. Positive rational examples remain explicitly distinguished from stochastic alternatives. The new abstract centres the full-germ theorem and its original-model application instead of listing every inherited theorem family.

## 11. Verification, provenance, and limits of this delivery (Section 16)

`SOURCE_MANIFEST.json` records the controlling review, reviewed source head, complete active TeX graph, and SHA256 identities of the new sources. The verifier obtains the actual commit and tree at runtime, checks GITHUB_SHA in Actions, compares every historical active v93 source with the controlling review commit, and rejects any changed or removed inherited path. Only additions in the declared v94 scope are permitted.

The branch-scoped workflow has no path filter. It runs the exact-source audit and finite diagnostics, compiles the complete inherited manuscript, checks the final log, and packages an artifact named for the actual HEAD. Successful source checks are not substituted for successful TeX compilation.

The recorded local result is six passing finite diagnostic groups and an eleven-page typesetting check of the new core with no overfull boxes. That local check deliberately omitted inherited appendices; its inherited cross-references were therefore unresolved. It is not the complete submission PDF. The full native result must be read from the exact-head workflow conclusion and artifact receipt. A queued or incomplete workflow is not a successful build.

The revision offers proved mathematical responses for renewed referee scrutiny. It does not certify acceptance by a journal, formal verification of all proofs, or a classification of every possible stochastic singular stratum.
