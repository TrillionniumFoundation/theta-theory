# Response to the referee on A2 revision 88

**Author:** Qian Qi  
**Revision:** 89, 19 September 2026  
**Controlling report:** `reviews/a2-v88-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md` at `47fd795b7e4d80f9fe81e9798e73a05efc7fa8f7`  
**Reviewed manuscript:** v88 at `777a9c951d5ca94a5261a6585ab6548d267e21e4`  
**New manuscript:** `papers/A2-v17-boundary-information-coarsening/rigidity_v89.tex`  
**Review branch:** `revision/a2-v89-observable-polynomial-quotient-2026-09-19`

We thank the referee for identifying the structural separation between the polynomial normalization theorem and the observable affine inference theory. The present revision addresses that separation directly. The principal change is an observable joint-coefficient construction in every degree, together with its additive inverse and sharp statistical consequences. It is not a new unrelated observation regime. All results of v88 remain either in the principal article or in the unchanged source history; none has been removed to make the new claims easier to state.

The references below use stable theorem labels, so they remain unambiguous if final pagination changes.

## 1. What v88 fixed; the central structural objection

The polynomial gcd/nullity theorem, positive local fibres, worst-case clock obstruction, channel-coordinate additive estimate, affine residue invariant, explicit estimator, honest inference and both affine least-favourable families are retained. The new organizing result is **Observable polynomial inverse** (`thm:joint`, `article/v89/observable.tex`). It replaces the latent-only polynomial certificate by an observable one, rather than merely renaming the latent conditioning parameter.

## 2. Normalization defect and the collision argument

The proof of `lem:defect` is retained. The proof of `lem:local-fibre` now uses continuous tracked root paths: a continuous path taking values in a fixed finite root set must be constant. This handles cross-component collisions without assuming a positive gap between components. Weight renormalization, positive brackets, the fixed-channel property and the contradiction from a nonzero normalization direction remain explicit.

## 3. Worst-case clocks versus full functional complexity

The arbitrary-capacity construction in `prop:clocks` now displays

`P(T) = A + (D_0 - s_bar A)(g(T)-f(T))/q(T)`.

The matrices `E_b=U_:b V_:b^T` are linearly independent by the channel inverses. Since the chosen `s_b` are not all equal, `D_0-s_bar A` is nonzero; since `g-f` is a nonzero lower-degree polynomial, the scalar curve is nonconstant. The low-functional-rank nature of this worst-case example is stated in the introduction and theorem.

We also prove a stronger result rather than relying on that qualification alone. **Full polynomial span** (`prop:full-span`, `clock_complexity.tex`) gives

`rank N_P <= min{d, (s-1)(ell-d-1)}`, where `s=dim span{f_b}`.

When `s=d+1`, every `d+2` admissible distinct clocks identify the normalization; `d+1` do not. Positive interior full-span examples are constructed for every `k>=d+1`. This separates two sharp counts for two different complexity classes. No generic intermediate-span formula is inferred from a dimension upper bound.

## 4. Classical root perturbation and the new contribution

`lem:roots` now spells out the contour selection, constancy of the argument-principle count with algebraic multiplicity, disk-component matching and fixed-permutation limit when disks touch. The linear case is expressly described as semisimple cross-component stability.

The introduction and the theorem-level comparison in `general_quotient.tex` identify the spectral exclusion/counting mechanism as classical. The new observation-level step is the joint-projector normalization gauge in `thm:joint`. The revision does not attribute classical perturbation through semisimple multiplicities to this paper.

## 5. A fully observable condition in degree d

After recovering `q,K`, reduce into orthonormal frames and write `M(z)=sum M_j z^j`, `A_0=M_d`. The matrices `C_j=M_j A_0^{-1}` form a commuting semisimple algebra. For each distinct **complete component polynomial** `f`, take its joint projector `E_f` and put

`W_f=A_0^{-1}E_f`, `B_d=sum_f ||W_f||`, `eta_d=(B_d+tau^{-1})^{-1}`.

This is a finite observable construction. A separating linear combination of the coefficient matrices constructs the joint projectors, independently of the separating combination. Theorem `thm:joint` proves frame and representation invariance, the positive set, lower semicontinuity of `B_d`, upper semicontinuity of `eta_d`, continuity on fixed complete-polynomial grouping strata, and reduction to the affine residue condition.

The key identity is

`Mbar_r(z)^(-1) = sum_f W_f / (f(z)+I_d(r f/q)(z))`, with `r=q'-q`.

The coefficients `W_f` are unchanged by the normalization gauge. This proves an additive spectral scale `delta(B_d+tau^{-1})`, not `delta B_d/tau`. The same proof applies in the estimated singular subspaces of the direct estimator. Singular competitors are included through the invertible-leading-coefficient rank argument. The exponent is `1/d`, improved to `1/m` for separated clusters of at most `m` roots per scalar component, and to one for internal simple roots.

## 6. Exact local conditioning, not an inflated interpretation of eta

**Two-sided local conditioning** (`thm:exact-condition`, `local_condition.tex`) identifies the exact infinitesimal inverse modulus on strictly positive, full-rank, regular-normalization coefficient charts with pairwise distinct component polynomials and internal simple roots. Cross-component root collisions are allowed.

With forward derivative `J` and continuously labeled root derivative `G`, the exact condition in product Euclidean observation norm is

`c_2(P)=max_a sqrt([G(J^T J)^(-1)G^T]_aa)`.

The proof constructs the smooth observable inverse from joint projectors and stochastic normalization, proves injectivity of `J`, accounts for all nearby representations by compactness, treats equal aggregate root groups explicitly, and constructs a maximizing admissible path. It also gives the weighted/Fisher-metric version and the comparison `c_2 <= C_nu/eta_d`.

We do not identify `eta_d` itself with this exact condition, a distance to a discriminant, or the local risk at every singular point. The residue jump example is retained; it does not contradict the metric theorem on its stated charts.

## 7. The estimator and computational scope

The direct estimator and its full proof are retained in `algorithm.tex`. Its polynomial guarantee is strengthened in `thm:joint` using `B_d` rather than supplied latent channel conditioning. The introduction explicitly states the exact-arithmetic scope before the algorithm is reached. The procedure remains least squares, interpolation, SVD and matrix-polynomial roots. No finite-precision threshold or bit-complexity theorem is claimed without proof. Confidence-region optimization remains information-theoretic, separately from the explicit point estimate.

## 8. Sharp inference beyond degree one

Three results in `polynomial_statistics.tex` now supply the missing polynomial inference.

**Observable polynomial inference** (`thm:poly-inference`) gives whole-closed-model honesty and risk/diameter upper bounds in `eta_d`, including the cluster exponent `1/m`.

**Sharp semisimple signal classes** (`thm:poly-sharp`) proves squared-risk order `min{1,(Ns^2)^(-1)}` and the corresponding honest-diameter order on `eta_d>=s` classes with internally separated simple roots, in every fixed degree and admissible capacity. The new positive family uses `f_1=F+lambda G`, `f_2=F-lambda G`, other `f_b=F`, where `G` is a nonzero small constant and `F` is monic degree d. Thus `q=F` and the visible denominator genuinely has degree d; no common factor is attached to an affine model. Its two observed marginals are fixed, its observation difference is exactly proportional to the product of channel contrasts, and its `eta_d` is comparable to that product. All ranges are chosen before the testing displacement. The conditional KL chain rule proves the lower bound for adaptive clocks as well.

**Multiplicity-dependent local minimax exponents** (`thm:multiplicity`) proves neighbourhood squared-risk order `N^(-1/m)` and diameter order `N^(-1/(2m))` at an internally m-fold root, with regular normalization and distinct complete polynomial tuples. The real-rooted lower bound uses two moving alternatives `u^m H((z-x)/u)a(z)` and `u^m(H((z-x)/u)+c)a(z)`, where both `H` and `H+c` have only simple real roots. Their root displacement is order u and their coefficient difference order `u^m`. This avoids the false inference that an arbitrary constant perturbation of an m-fold real root remains real-rooted.

The assertions are respectively signal-class and neighbourhood minimax theorems. They do not claim a complete classification at all intersections of normalization cancellation and channel-rank loss. The exact singular limits of the two affine families remain proved and included.

## 9. Rational realization, Loewner and matrix GCDs

Anderson--Antoulas (1990), Beckermann--Labahn (2000), and Mayo--Antoulas (2007) have been added to the article and compared directly, together with the existing vector-interpolation and matrix-polynomial references. **The rational interpolation module** (`thm:rational-module`) states the exact scalar-denominator bounded-degree specialization of the interpolation space. It is expressly treated as a classical algebraic specialization, not as a new algorithm.

The distinction is then mathematical: minimal rational realization removes a common factor; the specified original numerator spectrum changes with that factor. The stochastic theorem realizes the ambiguity by positive fixed-channel parameters, while the joint coefficient algebra supplies the additive observation modulus. The literature audit records which source material was verified and does not make an unsupported exhaustive-priority claim.

## 10. Beyond the simultaneously diagonalizable model

`thm:rational-module` allows arbitrary rectangular polynomial numerators and independent monic scalar denominators; it assumes neither stochastic channels, positivity nor simultaneous diagonalization. Its kernel is `(q/h) R[z]_{<deg h}`, with `h=gcd(q, entries K)`.

**General quotient resolvent bound** (`prop:general-bound`) handles regular square numerators with possibly noncommuting and nondiagonalizable coefficients, using observable Laurent coefficients and the largest inverse pole order. It separates the ordinary coefficient susceptibility from the normalization-direction susceptibility. We do not extend the diagonal model's stronger normalization constant to arbitrary matrix curves without proof.

## 11. Quantitative degree, dimension and clock dependence

`prop:explicit` gives a concrete deterministic bound with Lagrange coefficient norms, the clock denominator bounds, degree d, capacity k and the measured `B_d,tau` displayed. Its prefactor is `2kd-1`; evaluation contributes an explicit `R^d` factor. There is no additional hidden ambient matrix-dimension factor in that Frobenius-to-operator estimate. This is quantitative dependence, not an assertion that interpolation remains uniformly stable as degree grows or weights vanish.

## 12. Individual proof comments

12.1 is repaired by the finite-valued continuous root-path argument. 12.2 is repaired by the explicit nonconstant affine-line formula and independence of the `E_b`. 12.3 is addressed by full contour and touching-disk multiplicity counting. 12.4 is addressed by explicitly naming semisimple cross-component collisions. 12.5 is addressed by separating the global certificate from the exact local metric theorem. 12.6 is addressed by stating exact-arithmetic scope at the outset and not claiming unproved numerical complexity. 12.7 is addressed by the new degree-d upper and matching lower theorems, with their precise class and neighbourhood quantifiers.

## 13. Reproducibility and preservation

Every path inherited from the controlling review commit is unchanged. The four retained principal modules (`residues`, `algorithm`, `statistics`, `relations`) are copied into v89 with their original Git blobs. The v88 article, v87 companion, earlier derivations and all referee reports remain untouched. Native build evidence is distinct from finite mathematical diagnostics; neither certifies the proofs formally.

Ten groups of exact symbolic/numerical diagnostics were run locally. The script upload was blocked by the connector's safety determination; the response does not claim that script is in the repository or that the new diagnostic suite ran in Actions. The local results are recorded separately. The branch's native workflow uses the inherited v88 verification suite and compiles the complete v89 source. Its actual run status and artifact, not the existence of its YAML, determine whether an independent build can be credited.

## 14–15. Structural advance and renewed review

The six requested directions are addressed by distinct, connected statements: the observable polynomial inverse, exact local metric theorem, rational-module comparison, sharp polynomial inference, general quotient theorem and explicit constants. The centre of the article remains one observation inverse, with the affine theory as a fully retained specialization. We submit these proofs and their stated hypotheses for renewed independent referee examination. Mathematical correctness, originality relative to the full literature and the journal-level editorial assessment remain matters for that examination; no acceptance conclusion is assigned by this response.
