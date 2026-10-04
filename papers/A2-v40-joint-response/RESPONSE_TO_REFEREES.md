# Response to the A2 v39 referee report

**Manuscript:** Qian Qi, _Scalar collision laws and recognition of periodic dispersing billiards_.

**Revision:** A2 v40, 4 October 2026.

**Controlling report:** [v39 report at `790654161f2f069fb4d1d1ee18bfe86ea5290d74`](https://github.com/TrillionniumFoundation/theta-theory/blob/790654161f2f069fb4d1d1ee18bfe86ea5290d74/reviews/a2-v39-external-harsh-top4-rereview-2026-10-04/REFEREE_REPORT.md).

**Reviewed author source:** `f815a7acdb5c03e03b9996fc7052b405db66936d`.

## 1. The principal change

The report identifies two central questions: whether joint recovery can be obtained from a materially smaller command family, and whether the exact inverse has finite counterparts for the unknown probability law and for response completion. The revision answers both questions with new proofs. It keeps the collision sensor and the geometric-periodic topic, and preserves the complete reviewed mathematics in a separately compiled technical companion.

The new primary theorem uses only the two fixed vectors `a = te` and `-a`, where `t > 0` is fixed. Both ordinary forward commands use the same unknown stationary launch law. The exact observations are still the full spatial fields `F_+` and `F_-`; they are not two real numbers. The primary abstract, introduction and theorem state this input explicitly. The angular family and the limit of command lengths to zero are absent from the new exact theorem and from its finite acquisition.

The proof also broadens the exact geometric and probabilistic class. Obstacles need only be strictly convex, with bounded diameter and positive separation. Boundary smoothness and positive curvature bounds are unnecessary for exact identification. The unknown compact probability may have atoms, a singular part, or a lower-dimensional convex support. The only size comparison is `t + diam(A) < d`. There is no obstacle-width condition and no requirement that one obstacle resolve two translated density copies.

The theorem identifies the complete canonical triple

\[
\bigl(\mathcal O-s(A),\ A-s(A),\ (z\mapsto z-s(A))_\#\mu\bigr),
\]

the full common-translation fiber, every finite-length forward response and the full period group. The finite theorems use the same two fixed commands and give explicit geometry, probability, density and predictive conclusions in their stated quantitative classes.

## 2. Smaller command data and a new geometric inverse

**Report, Sections 3–5 and Section 10(1):** the v39 inverse uses every center, every direction and arbitrarily short positive lengths; the separated-copy factorization becomes explicit after classical angular differentiation.

**Revision:** primary Section 2, especially `lem:two-field-prefix`, `lem:two-field-calibration` and `thm:two-field-rigidity` in [core/21_two_field_rigidity.tex](core/21_two_field_rigidity.tex).

First, the original endpoint bit identity gives

\[
r(x)=F_+(x)-F_-(x+a)=v(x+a)-v(x).
\]

With `M = floor((D + Delta)/t) + 1`, occupation has the finite inverse

\[
v(x)=\max_{0\le m\le M}
\left\{-\sum_{k=0}^{m-1}r(x+ka)\right\}.
\]

The expanded components have diameter at most `D + Delta` and gap greater than `t`. A chain leaves its current component within `M` steps and cannot jump straight to another, so a zero endpoint exists without being supplied. The formula is `M`-Lipschitz in the forcing values and `2M`-Lipschitz in the two mean fields. The finite-prefix argument has an explicit antecedent in the repository's v29 derivation; that inheritance is documented rather than claimed as new abstract inversion.

Second, let `P = C - A` be one recovered occupation component. The associated collision supports `K_+` and `K_-` can be matched to it because each meets `P` and no other occupation component. Their supports are the incoming strips plus `-A`. Their support functions satisfy the new collision identity

\[
H_C(u)=2h_P(u)-h_{K_+}(u)-h_{K_-}(u)+t|u\cdot e|
=h_C(u)-h_{L_C}(u).
\]

Here `L_C` is the chord joining the contacts with normals `e^perp` and `-e^perp`. This cancels the unknown footprint before geometric differentiation. If the chord has length `ell` and normal directions `±n`, then

\[
(\partial_\phi^2+1)H_C
=\mathsf S_C-\ell(\delta_n+\delta_{-n}).
\]

Strict convexity makes the positive surface-area measure nonatomic; the chord contributes the two negative atoms. The Jordan decomposition therefore identifies the chord and the obstacle, even if the positive measure has a singular continuous part. Steiner centering and support subtraction put all components and the footprint in the same canonical frame. One compact occupation component then determines the entire law by its Fourier transform on the dense nonzero set of the obstacle transform, followed by continuity and Fourier uniqueness.

The direction variable in the support function is a numerical geometric variable, not a new commanded flight direction. The proof uses no angular response derivative or length derivative. It does use the same-law endpoint comparison of the two opposite commands, with a known nominal translation; the text says precisely that no separately prescribed reciprocal preparation is supplied.

The final proposition in Section 2 records a complementary fact: one fixed orientation cannot identify even a single smooth strictly convex obstacle with a known law, despite all positive lengths being available. A support perturbation confined to the outgoing normal semicircle preserves the incoming arc and every corresponding collision bit. The proof includes tangencies and atomic laws. It is a statement about fixed-orientation spatial fields, not a statistical lower bound.

## 3. Finite geometry and the sufficient exponent

**Report, Sections 8–10:** the finite v39 theorem depends on strong priors, several vanishing acquisition scales and a large nonsharp sufficient exponent.

**Revision:** primary Section 3, [core/22_two_field_finite.tex](core/22_two_field_finite.tex), with complete proofs of the two-direction boundary test, the shared positive-record hull bound and stable contact-chord correction.

The quantitative class is stated separately. It retains known `C^{6,beta}` and positive-curvature bounds for obstacles and footprint, the lower boundary-mass condition

\[
j(z)\ge b_0\operatorname{dist}(z,\partial A)^\gamma,
\]

and `2t + Delta < d0`. The command length `t` and the two vectors `±te1` are fixed throughout the finite experiment. No density upper bound, density evaluation, continuity modulus or obstacle-width comparison is supplied.

There are three quantitative steps.

1. The finite occupation inverse gives coarse protected expanded components. A two-direction rare boundary test works even at tangency. A uniform outer tangent disk makes the shifted starting points free. The conjunction of at most two candidate marks is surely zero outside the component and succeeds with the required cap-mass probability inside it.
2. Positive records are **known nominal centers**, not unobserved collision locations. Every directional cap of a collision-support hull has positive-record probability at least `c epsilon^(gamma + 9/2)`. This follows from a strip area bound `c epsilon^3` and footprint cap mass `c epsilon^(gamma + 3/2)`. The same records estimate all support directions. Conditioning on the hidden displacement gives a rational-grid quadrature error `O(mesh)` without a density modulus.
3. A sine second difference locates the two negative curvature atoms to `O(epsilon)`. A signed plateau with vanishing moments estimates the chord length to `O(epsilon^((s-1)/s))`. Smoothing the corrected support, with the segment's distributional structure retained, yields `C2` error `O(epsilon^((s-2)/s))`.

Consequently

\[
N_\nu\le C\nu^{-Q_{\rm pair}}
\log(C/\nu)\log(C/(\nu\delta)),\qquad
Q_{\rm pair}=\frac{(\gamma+9/2)s}{s-2},\quad s=6+\beta.
\]

The old sufficient exponent is `3 Q_pair`. At `gamma = 0`, `s = 7`, the new power is **6.3**, compared with **18.9** in the reviewed theorem. The text calls both sufficient upper bounds. It does not transfer the companion's sharp known-uniform-disk rate to this joint unknown-law experiment. The required nominal grid, `nu^Q_pair` up to fixed factors, is stated and charged as coordinate description and physical precision.

## 4. Finite law recovery and response completion

**Report, Section 10(2) and (4):** exact density identification is separate from finite acquisition, and exact response completion is not a finite-cost extrapolation theorem.

**Revision:** primary Section 4, [core/23_two_field_law.tex](core/23_two_field_law.tex), provides those finite counterparts with complete acquisition and stability proofs.

An isolated occupation contribution, normalized by obstacle area, is the density of `X - Z`, where `X` is uniform on the recovered obstacle and `Z` has the unknown canonical law. The moment lemma acquires all moments through degree `4m` from a shared rational spatial grid and finite prefix queries. The proof conditions on each hidden shift and controls boundary cells of a translated convex body, so it does not assume continuity of occupation or of the unknown law.

The bivariate triangular convolution identities give the explicit moment conditioning bound `D_k <= 2 a 8^k k!`. A tensor Jackson approximation and transportation duality then imply

\[
W_1(\mu_0,\widehat\mu_0)\le C/m+a(Cm)^{Cm}.
\]

A finite rational linear programme fits a positive atomic law while allowing the error in the recovered obstacle moments. At `m` of order `epsilon^{-1}` and `a_m = exp[-C m log(Cm)]`, the theorem gives

\[
N\le N_{\rm geom}(c a_m,\delta/2)
+C m^2 a_m^{-4}\log\frac{Cm}{a_m\delta}
\le \exp\!\left(C\varepsilon^{-1}\log\frac C\varepsilon\right)
\log^2\frac C\delta.
\]

The output has `W1` law error and geometric error at most `C epsilon`, with probability at least `1 - delta`. The law stage itself applies to arbitrary compact probabilities once the required geometric estimates are given. Its composition with the finite geometric theorem uses that theorem's quantitative density and geometry class. The proof makes no assertion of uniform strong density recovery over unrestricted `L1` densities.

For every fixed bounded window `U` and maximum command length `T`, the same finite output predicts the whole family with

\[
\sup_{|b|\le T}\int_U|\widehat F_b(x)-F_b(x)|\,dx
\le C_{U,T}\varepsilon.
\]

This follows from collision-indicator variation, convex swept-body symmetric differences and coupling of the launch laws. The statement includes the bounded patch needed when estimated lattice vectors differ from the true ones.

There is also a strong density and uniform prediction theorem under the explicit additional prior `|D j0|(R2) <= V` for the zero-extended density. Acquire `W1` accuracy `c epsilon^2` and output the finite kernel mixture `rho_epsilon * mu_hat`. Then

\[
\|\widehat j-j_0\|_1\le C(V+1)\varepsilon,
\qquad
\sup_{\substack{x\in U\\|b|\le T}}
|\widehat F_b^{\rm dens}(x)-F_b(x)|\le C_{U,T,V}\varepsilon.
\]

The sufficient cost is `exp(C epsilon^{-2} log(C/epsilon)) log^2(C/delta)`. The density estimate uses the BV translation inequality; the raw-mean estimate uses planar `BV -> L2` and the geometric symmetric-difference bound. Thus density recovery and finite response completion now have explicit hypotheses, norms and costs, beyond the exact completion statement.

## 5. Hypotheses, periods and resource accounting

**Report, Section 10(3), (5) and (6):** different theorem classes must remain distinct, finite period decisions need their margin or complete aperture, and spatial sites cannot be conflated with commands, bits or physical controls.

The primary introduction states the periodic presentation bounds, the entire patch-defect definition and the geometric loss. Exact period recovery uses only the broad exact class and assumes no periodicity. Uniform finite primitive-period decisions use `B_eta` and its known positive nonperiod-patch margin. The finite-cloud corollary replaces periodicity by a known protected aperture containing all expanded components and their fixed query collars. A finite list is not treated as a complete configuration without that aperture condition.

The retained direct germ theorem, one-resolved-obstacle extension and finite regularization theorem remain separate in the companion. Their assumptions are not attached to the new fixed-pair theorem. Conversely, the new exact singular-law result is not presented as a finite statistical result without quantitative priors.

Every finite theorem distinguishes distinct nominal sites `S`, site-and-sign command occurrences `J`, and fresh attempted bits `N`, with `S <= J <= N`. It also records coordinate mesh, finite description length, aperture and the role of an unknown footprint origin. Numerical integration, finite LP arithmetic, movement and realization of coordinate precision are separate from bit counts. The experiment assumes conditionally independent fresh draws and exactly the same stationary law at all attempts.

## 6. Primary architecture and complete preservation

**Report, Section 10(7):** the 85-page primary retains 76 proofs and several previous programmes; substantial splitting or compression is warranted.

The new primary contains an introduction and three proof sections: the two-field exact inverse, finite geometry, and finite law recovery with prediction. It does not append the entire earlier programme to its main argument. The separately compiled technical companion retains **all 32 v39 core files byte for byte**, all **322** baseline mathematical labels, all **76** baseline proof bodies and all **79** baseline formal blocks. Its title and opening guide identify its role and link to the primary theorems.

The preservation contract is relative to the actual reviewed v39 closure, not merely to the older v38 closure. It checks both executed document input closures, every old proof body, unique ownership of labels and proofs, stable cross-references, and both TeX recorders. Shared preamble and bibliography are label-free; neither can conceal duplicated mathematical content. Final document counts and page totals are recorded by the qualification receipt.

All old paper and review trees remain in place. The new branches add a v40 paper directory and its own workflow. The companion and main share the same article identity and topic. The source-level split makes the new argument available for focused review without deleting the previous derivations.

## 7. Attribution and evidence for the next review

The primary credits classical support-measure and signed Minkowski-difference calculus, moment-to-transport comparison, and bounded-variation inequalities. [LITERATURE_AUDIT.md](LITERATURE_AUDIT.md) records the consulted primary sources and compares the observation models. [HISTORICAL_DERIVATION_AUDIT.md](HISTORICAL_DERIVATION_AUDIT.md) pins the v29 finite-prefix and v31 mean-exit antecedents and the reviewed v39 arguments. The new claim is the collision-specific support cancellation and the resulting complete two-command inverse, together with finite geometric, probability and predictive constructions.

The qualification workflow binds both PDFs and both source archives to the actual revision SHA. It runs finite diagnostics and contract checks under ordinary and optimized Python, requires stable clean TeX builds, and records failures as evidence rather than silently dropping them. These checks make the submission reproducible. The mathematical proofs, including all hypotheses used in each finite reduction, are provided for the next referee's substantive assessment.
