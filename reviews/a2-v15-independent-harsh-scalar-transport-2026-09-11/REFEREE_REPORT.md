# Independent harsh referee report on A2 v15

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.

**Date:** 11 September 2026. **Requested evaluation standard:** Annals of Mathematics, Acta Mathematica, Inventiones Mathematicae, and Journal of the American Mathematical Society.

**Status:** author-requested, AI-assisted, source-pinned referee-style assessment. This report is not commissioned by any journal, is not an editorial decision, and is not a formal proof certificate.

## 1. Frozen version and recommendation

The reviewed revision branch is `revision/a2-v15-intrinsic-scalar-transport-2026-09-11`. The authoritative author commit is **`627c16b951994fa65acfbf3a621d0e4306131db3`**, with repository root tree **`5f17c9f2038a67b050bba74e2ce857cbb4c4c5f6`**. The author commit is dated 10 September 2026 at 22:02:04 UTC, which is 11 September in Amsterdam. Branch enumeration and both manuscript indexes identify this as the latest A2 revision inspected for this report.

Unless a different location is specified, manuscript paths below are relative to [`papers/A2-v15-intrinsic-scalar-transport`](https://github.com/TrillionniumFoundation/theta-theory/tree/627c16b951994fa65acfbf3a621d0e4306131db3/papers/A2-v15-intrinsic-scalar-transport) at that commit. TeX labels identify results; unverified typeset theorem or page numbers do not.

The preceding report is frozen at `0c523413ef7ffa2dedd1ab471ce58b3275896a93`, in `reviews/a2-v14-independent-harsh-intrinsic-density-2026-09-11/REFEREE_REPORT.md`. It reviewed author commit `e136929b120912586266fb78e0ae7b3c9d43bfd6`. I have read its findings and the present point-by-point response, but have independently examined the arguments and written the diagnostic code accompanying this report.

**Recommendation: reject the present submission at the requested four-journal level.**

The reason is the weight and significance of the demonstrated contribution, not a newly established fatal mathematical error. **I found no fatal error in the new scalar-product lemma, its physical determinant identification, or the principal inherited arguments inspected below.** This is a scoped mathematical finding, not approval of every historical appendix or a certificate for the entire research programme.

The two concrete v14 corrections are closed. V15 has made the classical comparison explicit, proved the claimed smooth-family statement, unified the relevant multiplier notation, and printed both directions of the width/profile equivalence. It would be unfair to describe this as failure to answer the referee. It would also be misleading to infer four-journal acceptance from successful completion of requests which the previous report explicitly said were not its principal publication objection.

There is substantial, potentially publishable mathematics in the physical relative law and the independent-contact inverse. My negative recommendation does not assert that the whole paper is already known, that it has no original result, or that the programme is obstructed. It does mean that I cannot recommend this version to the specified venues merely because another layer of correct interpretation has been added to the existing theorem package. I do not recommend an indefinite sequence of nominally technical major revisions with an unstated acceptance condition.

## 2. Disposition of the preceding requests

| Previous request or issue | Finding in v15 |
| --- | --- |
| C14-1: distinguish classical scalar smooth linearization from identification of the physical amplitude | **Closed.** `lem:v15-scalar-product` supplies the normalized product construction with mixed derivatives, and `cor:v15-determinant-product` identifies it with the physical Fredholm expression. The surrounding text and acknowledgments expressly disclaim a new scalar linearization mechanism. |
| C14-2: separate the single-flight factor, return multiplier, curvature ratio, and first-hit derivative | **Closed in the inspected relevant sections.** `eq:v15-multiplier-convention` uses `varrho`, `lambda`, `mathfrak r_b`, and `r_b` consistently in the hyperbolic and two-contact calculations. I checked the formulas, but did not independently verify the author's byte-for-byte historical alpha-renaming claim. |
| Width as an equivalent representation, not a second recovered invariant | **Closed.** `eq:v15-width-equivalence` gives the inverse weighted derivative and the leading width normalization. The asymmetric-branch limitation is retained. |
| Earlier restrictions on finite physical families, exact-germ normalization, and paid smooth-class calibration | **Retained in the inspected statements and proofs.** These are not new outstanding defects. The abstract restricts the two-flight observation assertion to the constructed locally full-rank families. |

The old objections concerning formal Taylor series being substituted for smooth uniqueness, free derivative observations, an uncharged calibration oracle, or a curvature-difference denominator are not supported by the current passages. I do not reinstate them.

## 3. The new scalar lemma survives the mixed-derivative audit

**Sources:** `article/16a_scalar_linearization.tex`, especially `lem:v15-scalar-product`, `eq:v15-scalar-product`, `eq:v15-scalar-iterates`, and `eq:v15-finite-product`.

The hypotheses are adequate for the stated conclusion. The family is jointly smooth on an open neighborhood of a compact parameter set, the fixed point is common to the family, and

$$
R_\xi(0)=0,\qquad R_\xi'(0)=\lambda_\xi,\qquad
0<\ell\le R_\xi'(u)\le q<1.
$$

These are not decorative assumptions. A common fixed point implies that every pure parameter derivative of $R_\xi$ vanishes there. A positive lower derivative bound controls logarithms and differentiated powers of the parameter-dependent multiplier. Compactness supplies the finite-order bounds used in the induction. The statement does not assume a smooth two-dimensional normalizing chart.

For $x_n=R_\xi^n(u)$, the highest mixed derivative in the differentiated orbit equation is multiplied by $R_\xi'(x_n)$. All forcing terms either contain a lower orbit derivative, or a pure parameter derivative of $R_\xi$ evaluated at $x_n$. The latter is $O(|x_n|)$, not an uncontrolled constant. Induction therefore gives a polynomial in $n$ times $q^n$ at each fixed order. The same argument applies to

$$
h_\xi(x_n)=\log\frac{R_\xi'(x_n)}{\lambda_\xi},
$$

because $h_\xi(0)=0$ throughout the family, including after pure parameter differentiation. The asserted termwise differentiated summability follows. There is no unjustified exchange of an infinite sum with arbitrary-order differentiation: the order is fixed first and the constants may depend on it.

Shifting the series yields the density cocycle, and integration yields the linearizer. The uniqueness argument uses differentiability at the fixed point correctly. If the conjugated competing coordinate satisfies $H(\lambda x)=\lambda H(x)$ and $H'(0)=1$, iteration towards zero forces $H(x)=x$. Smoothness of the competing coordinate is unnecessary.

The sharper iterate rate follows from the exact conjugacy, rather than from dividing a preliminary $q^n$ estimate by $\lambda^n$. Writing the normalized inverse as $x+x^2A_\xi(x)$ gives

$$
\lambda_\xi^{-n}R_\xi^n(u)-\mathfrak z_\xi(u)
=\lambda_\xi^n\mathfrak z_\xi(u)^2
 A_\xi(\lambda_\xi^n\mathfrak z_\xi(u)).
$$

Each fixed parameter derivative introduces at most a polynomial factor in $n$. One additional endpoint derivative supplies the density estimate. Hence the printed bound with every fixed $\sigma>\lambda_+$ is justified. This is a genuine mixed-family argument, not only a calculation for a fixed map.

The classical positioning is appropriate. The primary source [L1] recalls the one-dimensional hyperbolic smooth-linearization theorem before treating failures at lower regularity. Those lower-regularity failures do not challenge the smooth hypotheses here. V15 now separates that classical fact from the billiard amplitude identification. My verification of the particular uniform product proof above is independent of transferring a theorem from that source.

### 3.1 An independent check: the strict exponential margin is necessary

The following elementary example is a benchmark for the revised statement, **not a counterexample to it**. On a common small interval take

$$
R_{\lambda,a}(u)=\frac{\lambda u}{1+a(1-\lambda)u},\qquad
z_a(u)=\frac{u}{1+au},\qquad B_a(u)=\frac1{(1+au)^2}.
$$

For compact positive multiplier intervals inside $(0,1)$ and sufficiently small endpoint/parameter intervals, this family satisfies the lemma's hypotheses. Direct calculation gives

$$
R_{\lambda,a}^n(u)=\frac{\lambda^n u}{1+a(1-\lambda^n)u},
\qquad
\lambda^{-n}(R_{\lambda,a}^n)'(u)
=\frac1{[1+a(1-\lambda^n)u]^2}.
$$

In particular, the finite product multiplied by $B_a(R^n(u))$ equals $B_a(u)$ exactly. The normalized iterate error is

$$
\lambda^{-n}R_{\lambda,a}^n(u)-z_a(u)
=\frac{a\lambda^n u^2}
 {[1+a(1-\lambda^n)u](1+au)}.
$$

At $a=0$ its mixed derivative is

$$
\partial_\lambda\partial_a
 [\lambda^{-n}R_{\lambda,a}^n(u)-z_a(u)]
=n\lambda^{n-1}u^2.
$$

At the maximal multiplier of a compact parameter interval, division by $\lambda_+^n$ leaves a factor proportional to $n$. Thus replacing the printed strict-margin mixed-norm estimate by $C\lambda_+^n$ would be false in general. V15 does **not** make that replacement. The exact rational mixed-jet diagnostics test the orbit, conjugacy, and finite density remainder through total derivative order three, with the multiplier itself among the differentiated variables.

## 4. The physical determinant identification is correct and noncircular

**Sources:** `article/16_hyperbolic_coordinates.tex`, `thm:v14-intrinsic-density`; `article/16b_determinant_transport.tex`, `cor:v15-determinant-product`; `v4/10_boundary_layers.tex`, `eq:v4-half-amplitude` and `thm:v4-factorization`.

The relevant physical object is not an arbitrary scalar density. It is the normalized amplitude already constructed from the half-line edge product and interior Hessian:

$$
B_b(u)=\frac{\exp U_b(u)}{\det(I+G^{(b)}\Delta H_b(u))}.
$$

The first-flight stationary equation gives

$$
\varphi_b'(u)=
\frac{-\ell_{b,12}(u,\varphi_b(u))}
 {\ell_{b,22}(u,\varphi_b(u))+S_{1-b}''(\varphi_b(u))}>0.
$$

The proof uses exact finite Schur concatenation before taking a normalized limit. For a tail starting at $o=1-b$, the reference ratio is

$$
\frac{d^0_{j,o}}{d^0_{j+1,b}}
=\sqrt{a_o/a_b}\,
 \frac{\sinh((j+1)\gamma)}{\sinh(j\gamma)}
\longrightarrow r_b^{-1}.
$$

After cancellation of the positive terminal factor, this gives

$$
B_o(\varphi_b(u))\varphi_b'(u)=r_bB_b(u),
\qquad r_b=\sqrt{c_b/c_o}\,e^{-\gamma}.
$$

The placement of $r_b$ is correct. Composing two flights yields the return cocycle with $\lambda=e^{-2\gamma}$. The quotient of this positive normalized physical density and the scalar density is invariant under the contracting return and equals one at zero. It is therefore identically one. This proves the newly printed determinant/product identity.

The finite logarithmic remainder is also exactly as stated:

$$
\log B_b(u)-\sum_{i=0}^{n-1}
 \log\frac{R_b'(R_b^i(u))}{\lambda}
=\log B_b(R_b^n(u)).
$$

The mixed-norm estimate follows by writing $\log B_b(\zeta_b^{-1}(x))=xC_b(x)$ and applying the same differentiated conjugacy estimate. No estimate for a small absolute twist is divided by an exponentially small reference at this step.

The dependency is important. The finite physical relative theorem identifies the amplitude entering the probability. Classical scalar uniqueness then identifies that amplitude's dynamical meaning. The new scalar lemma is not being used to prove the physical theorem which is then invoked to prove the lemma. Conversely, a scalar contraction alone would not supply the physical selected event, the two-ended bridge, or its residual-time integration.

This is a sound identification. As an increment over the inspected v14 cocycle, however, the explicit infinite product and its telescoping remainder are consequences of an already normalized cocycle plus classical uniqueness. V15 itself largely acknowledges this. They clarify the main result; they do not supply a second independent physical rigidity result.

## 5. Audit of the inherited forward mechanism

**Sources:** `article/01_introduction.tex`, `thm:v8-main-relative`; `v4/10_boundary_layers.tex`, `lem:v4-halfline`, `thm:v4-factorization`, and `thm:v4-law`; the analytic comparison in `article/16_hyperbolic_coordinates.tex`.

The half-line Green kernel has the reflected exponential form required by the fixed left boundary. Locality of the tridiagonal nonlinear perturbation and decay of the stationary half-line imply trace-class control by the sum of the absolute entries. This is a dimension-independent estimate, not the false substitution of operator-norm smallness for trace-norm smallness on an increasingly long bridge.

The gluing proof controls the difference between the finite stationary segment and the sum of the two endpoint layers in the $\ell^1$ norm. The averaged Hessian is uniformly strictly diagonally dominant. Symmetry gives an $\ell^1$ inverse bound from the $\ell^\infty$ bound. Differentiating the difference equation leaves the same invertible operator on the highest derivative. The action estimate and its quadratic vanishing at the origin then follow with a strict exponential margin.

For the twist, the finite cofactor identity is normalized before taking logarithms and comparing determinants. Retaining the first and last $\lfloor j/3\rfloor$ sites leaves a trace-norm-small middle tail. The compressed finite Green kernels converge to their half-line counterparts, and their cross blocks are exponentially small at the retained separation. Telescoping powers bounds the difference of logarithmic determinants in trace norm. Differentiated trace series retain a trace-class factor. I found no new defect in these estimates.

The integration step uses common Morse domains. The inverse coordinate maps and transformed amplitudes depend on the action in fixed norms, with a finite loss of derivatives allowed by smoothness. Odd Taylor terms disappear after integration on the common disk. This justifies offset derivatives at zero and avoids unproved differentiation of a moving sharp sublevel boundary. The limiting endpoint density is not claimed to be a product probability: its two factors remain coupled by the residual-energy constraint.

The analytic comparison is also internally consistent. Its canonical mixed flux is

$$
T_n=\frac{\Delta(I)^n}{1-nI\Delta'(I)/\Delta(I)},
\qquad I=st\Delta(I)^n,
$$

and the physical flux is $|T_n/\det D\Phi_n|$, not $T_n$. With the billiard projection and $j=2n$, the exact origin value is $a_b/\sinh(2n\gamma)$. The reference denominator is retained. Parameter differentiation of the normalized expression uses its identity at the parameter-dependent origin, rather than discarding derivatives of the multiplier.

For comparison, [L2] discusses the local analytic hyperbolic normal form separately from the symmetry hypotheses of its geometric inverse problem. That supports the relevance of the analytic benchmark; it does not establish A2's full smooth, parameter-uniform, selected-event probability theorem. The latter remains the strongest forward contribution submitted here. This report has not newly checked every finite-bridge localization lemma in the older source tree; the precise reading boundary is recorded in [SOURCE_AUDIT.md](SOURCE_AUDIT.md).

## 6. What is, and is not, geometrically determined

### 6.1 Independent even contacts

**Sources:** `article/23_two_contact_rigidity.tex`, `thm:v12-two-contact`; `article/24_physical_image.tex`, `thm:v12-realization`.

At fixed labelled gap and curvatures, the limiting last-jet block is

$$
-\begin{pmatrix}P_m&Q_m\\Q_m&P_m\end{pmatrix}
 \operatorname{diag}(K_{m,0},K_{m,1}),
\qquad
K_{m,b}=\frac4{2^m(m+1)(m!)^2a_b^m}.
$$

I checked the action and determinant contributions separately. The unequal-curvature factor in the opposite-contact column is essential; the identity $K_{m,b}\mathfrak r_b^{2m}=K_{m,1-b}$ puts it in the displayed form. The antisymmetric eigenvalue is

$$
P_m-Q_m=m\tanh((m-1)\gamma)-(m-1)\tanh(m\gamma)>0.
$$

Strict concavity of $\tanh$ proves this without any separation between the two curvatures. The degree bookkeeping explains why lower jets cannot alter the last-jet coefficient. Recursive inversion is consequently justified at every fixed finite order. No bound uniform in the order is promised.

The support-function realization is genuinely physical. The separate parameters begin at the intended orders at the two horizontal normals; the area compensator begins beyond the retained jets and has nonzero area derivative. Positivity of the curvature radius, separation, and the first-hit channel persist on a small neighborhood. The graph-jet Jacobian has own-contact entry $-(2m)!\kappa_b^{2m}$ and zero opposite-contact entry at that order. This proves a local physical finite-dimensional image, not merely freedom to prescribe abstract profile coefficients.

The global continuation conclusion is restricted to connected real-analytic participating boundaries in their contact frames. It does not infer a smooth graph from its Taylor series, determine unobserved obstacles, or reconstruct the lattice. These restrictions are mathematically appropriate.

### 6.2 The two-flight comparison matters to the contribution accounting

**Source:** `article/29_two_flight_benchmark.tex`, `thm:v13-two-flight`, `cor:v13-jet-coordinates`, and `thm:v13-two-flight-observation`.

With $z=c_0c_1-1$, the finite last-jet block is

$$
-\begin{pmatrix}(1+2z)^m&1+2mz\\1+2mz&(1+2z)^m\end{pmatrix}
 \operatorname{diag}(k_mL_0^m,k_mL_1^m),
$$

where $L_b=g/(2c_bz)$ and $k_m=4/[2^m(m+1)(m!)^2]$. The other-contact twist variation supplies the $2mz$ term. Omitting it would change the inverse problem; the present proof does not omit it. The separating eigenvalue is the positive binomial remainder, and the printed quartic example has antisymmetric magnitude $1/48$.

The fixed-family observation theorem has an actual nonsingular nodal design at two flights. The proof obtains two-sided Lipschitz control by closeness to one fixed invertible Jacobian on a convex ball, not by pointwise nonsingularity alone. Its lower bound uses nearby physical tables, fixed positive probability margins, and conditional entropy for adaptive choices among the stated windows. Its scope is that finite-window experiment.

Consequently the limiting and two-flight coefficient vectors recover the same fixed-order even geometry. This limits the novelty that can be assigned to long bridges for that particular task. It does not identify the complete law functions or prove equivalence of noisy infinite-dimensional experiments. The manuscript now observes that distinction; the referee must do so too.

### 6.3 Width does not create additional information

**Sources:** `cor:v14-width`, `eq:v15-width-equivalence`, and `article/20_boundary_compatibility.tex`.

The two identities

$$
\mathcal W_b(E)=\int_0^E x^{-1/2}\mathcal V_b(x)\,dx,
\qquad
\mathcal V_b(E)=\sqrt E\,\mathcal W_b'(E)
$$

show that the width and the energy profile are the same complete datum in different coordinates. The leading term $2\sqrt E$ follows from $\mathcal V_b(0)=1$. The change $x=\zeta_b(u)$ removes the physical density, so the interpretation as an intrinsic stable-action sublevel width is legitimate.

For asymmetric contacts, the difference of two inverse branches does not specify their midpoint. This elementary information loss is not a constructed family of billiard counterexamples, and I do not portray it as one. V15 does not assert unrestricted asymmetric graph reconstruction. Its even-contact inverse requires the additional geometry and its explicit block calculation. Calling the width intrinsic does not enlarge that conclusion.

## 7. Full-profile inversion and the paid experiment

**Sources:** `article/20_boundary_compatibility.tex`, `article/21_abel_stability.tex`, `article/28_regularized_observation.tex`, and `lem:v11-calibration` in `article/27_profile_calibration.tex`.

The complete-profile uniqueness proof is stronger than formal recovery of Taylor coefficients. With $k=x^{-1/2}V$ and $\ell=x^{-1/2}W$, equal convolution squares imply $(k+\ell)*(k-\ell)=0$. Convolution once more with $x^{-1/2}$ yields a second-kind Volterra equation with leading constant $2\pi$. Its remaining kernel has bounded derivative; Gronwall proves uniqueness on the collar.

Deautoconvolution is a familiar inverse structure, but importing an unrelated uniqueness theorem without its function-space assumptions would not be legitimate. For example, the abstract of [L3] concerns compactly supported $L^2$ unknowns. A2's normalized kernel $x^{-1/2}V(x)$ with $V(0)=1$ is not in $L^2$ at zero. The elementary weighted argument printed here is therefore material. I do not cite [L3] as a proof of A2's theorem.

The Abel transform is linear and has precisely the affine nullspace stated in the paper. The physical integrated flux has zero value and zero slope at onset, so that ambiguity disappears on its actual image. The inverse estimate is in this specified transformed norm, not in uniform error of raw probabilities.

The regularization proof keeps three errors separate. Two integrations give the limiting flux two additional derivatives. Positive-node interpolation exploits that gain for an approximation error $h^{m-1/2}$. A structured smooth bridge error is controlled in $C^3$ without an inverse mesh power. Unstructured nodal sampling noise is amplified by $h^{-5/2}$. Choosing $t$ of order $\varepsilon h^{5/2}$ and $h$ of order $\varepsilon^{1/(m-1/2)}$ produces the power

$$
2+\frac6{m-1/2}+\frac\gamma{|\log\tau|}.
$$

The sum of the allocations includes ceilings and failed preparations. Compact ordered dictionaries and first-index tie breaking supply measurability. Dictionary elements need not themselves be physically realizable for this upper-bound argument.

The calibration pilot really estimates unknown smooth leading coefficients from positive offsets. Its one-sided bracket has a deterministic budget even on erroneous histories. The choice $s\asymp\xi^{1/m}$, $\rho\asymp\xi s$ balances extrapolation, gap translation, and Bernoulli noise, giving cost of order $\xi^{-(2+2/m)}$ up to the stated logarithm. Projection onto positive supplied boxes makes the inverse normalization maps Lipschitz and bounds subsequent allocations.

Most importantly, the post-pilot conditional mean is

$$
R H_{j,b}(d+\Delta),\qquad
\Delta=j(\widehat g-g),\qquad
R=\frac{\widehat A}{A}
 \frac{\sinh(j\widehat\gamma)}{\sinh(j\gamma)}.
$$

Translation is handled before division by $d^2$. The extra collar and $C^{3,1}$ assumption justify the $C^3$ shift estimate down to zero. There is no fictitious small-offset singularity in this processing, and no free exact-law oracle. The pilot's smaller power is absorbed by the profile-stage budget as stated.

These are useful and correctly distinguished results. The full-profile preparation bound is nevertheless explicitly sufficient, depends on supplied smoothness and convergence certificates, and is not a minimax information law. A finite-dimensional $N^{-1}$ risk theorem or an abstract profile instability example does not establish optimality for this different physical experiment. I found no such false inference in the inspected text.

## 8. Why the four-journal recommendation remains negative

The objection is not that a paper must contain an error before it can be rejected. Nor is a long proof automatically insufficient merely because the final object admits a classical interpretation. The question is what exceptional advance the whole paper demonstrates after its dependencies and restrictions are accounted for.

The strongest candidate is the uniform smooth physical relative theorem: it starts with obstacle graphs, retains exact phase normalization, controls a genuinely rare selected event on a nonshrinking collar, and transports all fixed mixed derivatives through integration. This deserves the most weight. I have not found a source that automatically subsumes that entire statement. Still, the submitted explanation largely refines a local hyperbolic endpoint mechanism, and the v15 scalar construction makes its classical component more explicit without increasing the physical scope or revealing a further dynamical phenomenon.

The strongest geometric component is the independent even-contact block inverse together with its physical realization, including equal curvatures. It is a real improvement over a single identical-contact calculation. But the finite two-flight calculation already gives the same fixed-order coordinates. The passage to long bridges contributes a separated smooth invariant; it cannot also be counted as indispensable for the finite-order geometric inverse.

For general smooth contacts, the recovered object is a symmetrized weighted profile, equivalently the normalized stable-action width. Its complete recovery is more than a jet result, but it is not a complete invariant of unrestricted contact geometry. The new product and width interpretation do not resolve that different identification problem. The observation theory makes the stated recovery operational under its certificates; its regular parametric result and sufficient nonparametric rate do not provide a separate sharp statistical principle.

In my assessment, these contributions amount to a technically substantial local programme rather than the exceptional conceptual reach I would require for a positive recommendation to the requested four journals. Another expert might assign greater significance to the uniform physical theorem. This is an editorial assessment of demonstrated weight, not a mathematical proof of lack of novelty.

I do **not** demand arbitrary asymmetric boundary reconstruction, a global classification, an optimal full-profile exponent, or an infinite-dimensional physical realization theorem as missing lemmas of the present claims. They would be different research results. Adding unrelated theorems, repeating closed calculations, or increasing finite check counts would not by itself answer this assessment. V15 has correctly addressed the concrete v14 requests; the remaining disagreement should not be disguised as noncompliance.

## 9. Specific remaining requests and submission readiness

**C15-1 — Integrated submission build; readiness issue, not a theorem defect.** The native README expressly reports only an isolated 18-page revised-section smoke build, with inherited references intentionally unresolved in that wrapper. Before an actual journal submission, the complete `two_collision.tex` and `main.tex` input graph should be compiled and the resulting cross-references, bibliography, and pagination checked. I did not run that build here. I cannot infer a full-build failure from the absence of a claimed successful full build; the present disclosure is honest. This request does not change the significance recommendation.

**C15-2 — Preserve the contribution hierarchy; presentation only.** The statements now properly separate physical factorization, classical scalar consequences, fixed-order even geometry, complete smooth profiles, and charged observation. That distinction should remain the organizing principle of a submission, including its abstract and cover letter. The explicit product is not a new independent linearization theorem and the width is not an additional invariant. The present source already makes these points; no further theorem proving is demanded by this comment. Repetition of review history and preserved older procedures should not be used as evidence of mathematical weight. Historical material can remain in the repository without altering any mathematical claim.

**No new mandatory mathematical correction is asserted in the inspected v15 additions.** I do not convert a negative venue assessment into an invented fatal defect. Nor do I certify uninspected auxiliary claims by silence.

## 10. Independent executed diagnostics

I wrote [verify_review.py](verify_review.py) for this review without importing author or previous-referee scripts. Both ordinary Python and `python -O` passed **3,318 explicit finite checks**. Their recorded JSON outputs, [diagnostics.normal.json](diagnostics.normal.json) and [diagnostics.optimized.json](diagnostics.optimized.json), are byte-identical. The check function raises an exception explicitly; optimization does not remove the tests.

The exact calculations include 2,880 rational Taylor-coefficient equalities for the scalar orbit, conjugacy, and finite density remainder, with mixed total order at most three. They also check alternating first-flight identities, wrong-normalization negative controls, the strict-margin example, contact-block formulas at orders two through nine, and the width/profile monomial identity. These are specified identities and coefficient tests, not thousands of independent theorem verifications.

The floating-point calculation uses actual local Euclidean flight lengths

$$
\ell_b(u,v)=\sqrt{(g+\psi_b(u)+\psi_{1-b}(v))^2+(u-v)^2},
$$

with cubic and quartic contact terms, for both an unequal-curvature asymmetric model and an equal-curvature asymmetric model. It solves stationary bridges, checks Hessian pivots, compares a logarithmic cofactor formula with a direct Schur complement, and checks the exact origin normalization at even and odd flight numbers. The maximum reference discrepancy was $7.11\times10^{-15}$, and the maximum cofactor/Schur relative discrepancy was $4.67\times10^{-15}$.

For the tested nonzero endpoints, the normalized two-boundary separation defect at 32 flights was at most $1.44\times10^{-14}$. A five-return derivative product with a 32-flight terminal tail agreed with the corresponding finite normalized bridge expression to $2.23\times10^{-16}$. This last comparison is a finite concatenation and truncated stable-branch diagnostic. It is **not** an independent certified computation of the infinite Fredholm determinant. The code and audit describe that distinction despite the diagnostic group's abbreviated name.

These are double-precision consistency measurements, not rigorous numerical error bounds. The local graphs were not completed into a global periodic table, no trajectory-based empirical probability experiment was run, and no interval arithmetic certified an infinite tail. The exact mixed-parameter derivative tests concern the explicit scalar family, not all mixed derivatives of the nonlinear Euclidean family. The analytic proofs, rather than these samples, are the basis for the all-order claims inspected above.

I did not rerun the author's advertised 10,549 checks or the preceding referee's 3,216 checks. I did not compile the full article, validate all historical retention counts, run remote CI, or independently re-referee every auxiliary appendix. The author may accurately report earlier executions, but those are not executions performed in this review. [SOURCE_AUDIT.md](SOURCE_AUDIT.md) records the actual reading and execution scope.

## 11. Conclusion

V15 answers the preceding concrete corrections and supplies a mathematically coherent scalar/physical identification. The independent mixed-derivative benchmark supports, rather than undermines, its strict-margin formulation. The inspected determinant, inverse, and paid-observation arguments do not justify an accusation that the principal claims have been disproved.

My recommendation remains **rejection at the requested four-journal level on significance grounds, with the v14 technical corrections closed and no newly established fatal error in the inspected core**. This is a reasoned negative evaluation of the present contribution, not an instruction to abandon the programme or a demand to remove its substantive mathematics.

## Primary sources used for the comparisons

**[L1]** H. Eynard-Bontemps and A. Navas, *On the failure of linearization for germs of C1 hyperbolic vector fields in dimension one*, [arXiv:2212.13646v2](https://arxiv.org/html/2212.13646v2). The introduction was inspected for the classical smooth one-dimensional comparison and the distinction from lower-regularity failures. It is not cited as a billiard probability theorem.

**[L2]** J. De Simoi, V. Kaloshin, and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/html/1905.00890v4). The local analytic normal-form discussion and its separation from the symmetry-dependent geometric inverse were inspected. This is a comparator, not a claim that its global inverse theorem has A2's data or hypotheses.

**[L3]** B. Hofmann, F. Werner, and Y. Deng, *On uniqueness and ill-posedness for the deautoconvolution problem in the multi-dimensional case*, [arXiv:2212.06534](https://arxiv.org/abs/2212.06534). Only the abstract-level statement of the L2 setting was used; no full-paper theorem audit or direct transfer to A2's singular weighted kernel is claimed.

These sources were consulted on 11 September 2026. This was a targeted primary-literature comparison, not an exhaustive priority survey. Repository evidence is pinned above, and the new calculations are supplied in this review directory.
