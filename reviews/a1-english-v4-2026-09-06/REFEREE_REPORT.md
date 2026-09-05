# Referee report — A1, English revision 4.0

**Manuscript:** *A1: Realizable Mechanical Experiments, Path Selection, and Response — Attainable polynomial rank, structured adaptive control, and robust finite-budget inference in a Lorentz laboratory*  
**Author named in the submission:** Qian Qi  
**Review date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT at the requested general-mathematics-journal level in its present form.**

This is a fresh AI-assisted referee-style assessment commissioned by the repository owner, not a review commissioned by any of the named journals. “Independent” here means that the proofs and calculations were checked afresh rather than accepting the author's response or test receipts; it does not imply an independent human referee, an institutional appointment, or formal verification. The recommendation concerns this submission, not the viability of the research program.

## 1. Submission identification and review scope

The controlling source is:

```
repository:       TrillionniumFoundation/theta-theory
revision branch:  revision/a1-english-v4-structural-control-robustness-2026-09-06
submission commit:e4b10bf7acebf38dbcfb466b3ee4cf30bb77b381
repository tree:  e366cddd2950419489537004b1816a410fa4148f
principal source: papers/A1-english-v4/main.tex
previous review:  574f2315a136d8b401644d8a3eeeb93c87887010
previous source:  025a9b3fdfd9ffa86e6ae2924f8b5e5b1b58ddd6
```

Two v4 revision branches were present. The branch reviewed here was committed at **2026-09-05 17:48:14 UTC**, or **6 September 2026, 01:48:14 Singapore time**. The other branch, `revision/a1-english-v4-structural-robust-control-2026-09-06`, was at `78e9437b686f4b4ef8e2c47a48bcfa9c9c492022`, committed at 16:22:02 UTC. They are siblings with the same previous-review parent, not successive commits on a single manuscript branch. This report concerns the chronologically later submission, not a mixture of the two.

I read the entire current principal mathematical source: the main file, all eleven numbered section files, both appendices, and the bibliography. I also read the current response and proof ledger, the preceding v3 report, and the submitted exact adaptive-certificate program. The twenty-two proof-bearing labels are audited separately in [CLAIM_AUDIT.md](CLAIM_AUDIT.md).

The scope is the current principal paper, including its self-contained Appendix A. I did **not** freshly re-audit every theorem in the preserved foundation companion, the eleven-paper program, or every historical branch. The companion's preservation is not a new mathematical approval. Likewise, the author's 35-page build and 24 diagnostics remain author-reported: I did not compile LaTeX, inspect a PDF, or rerun that suite. Instead I wrote and executed a separate [39-check program](referee_checks.py), with [complete results](DIAGNOSTICS.json), including all 64 nominal nonadaptive comparisons and an independent binary-model ablation. None of the numerical decisions in that program uses floating-point comparisons.

All manuscript anchors below mean files under `papers/A1-english-v4/` at the pinned submission commit. The source is retained by ancestry of this review branch, without modifying or duplicating the manuscript. References to theorem numbers follow the submitted proof ledger; source labels are the controlling identifiers.

## 2. Executive judgment

**The revision has substantially answered the previous requests for additional mathematics. It has not, in my judgment, established a sufficiently deep or consequential central advance for the requested journals.** These are different conclusions, and the report must not conceal the first in order to make the second sound harsher.

The two local v3 defects are repaired. The new rank criterion has a valid explicit right inverse. The general degree-q dimension proof correctly separates intrinsic dimension from redundant degree elevation. The endpoint argument has a legitimate Borel implementation. The last-cartridge two-arc formula is correct under its tagwise-reward hypothesis. The approximation theorem preserves both normalization and physical flag masses. The adaptive example is not a sampled-menu comparison masquerading as an all-Borel theorem: its reduction and transfer argument cover the declared comparator classes, and its numerical bounds reproduce independently.

I found **no new blocking mathematical counterexample to the twenty-two printed principal statements under their stated ideal-apparatus and finite-budget hypotheses**. This is an assessment after reading their proofs, not a certificate that no error exists. In particular, I do not reject because the polynomial kernel is false, because rare failures are omitted, because the final gap is numerically fabricated, or because an arbitrary smooth perturbation allegedly preserves cubic closure. None of those accusations would be justified here.

The decisive objection is the contribution. The added structural results are, largely, finite-dimensional linear algebra and the polynomial-product argument already visible in v3. The added control results are consequences of a supremum-of-linear continuation functional and a single cosine coordinate. The smooth approximation theorem combines positive Bernstein averaging with a complete-policy coupling estimate. The strict performance example is an ordinary acceptance-cost-saving mechanism that survives unchanged after removing the billiard, the angular mark, the cubic factor family, and the continuum of parameter values from the nominal problem.

A coherent combination of correct ingredients can be valuable. What remains unestablished is why this particular combination changes a substantial mathematical problem, reveals a genuinely new obstruction, or proves a structural phenomenon whose significance goes beyond the engineered model. The manuscript currently demonstrates coexistence of mechanical realization, exact-state dimension, and adaptive value; it does not demonstrate that their interaction is essential to the advertised performance theorem.

I therefore recommend rejection rather than a routine minor or major revision. The missing item is not another correction of a displayed identity. It is a stronger central contribution. This does not require abandoning the setup, lowering the target, or proving a long-time billiard theorem outside the paper's declared scope.

## 3. Disposition of the v3 review

| Previous item | Current disposition | Assessment |
|---|---|---|
| M1: smooth dynamics versus arbitrary Borel report | **Closed in current principal A.3** | The report map must now be jointly C^r; the Sobolev reporting space and its dimension are specified. |
| M2: five coordinates versus five intrinsic dimensions | **Closed** | The body is stated to lie in R^5, with intrinsic dimension at most five. The rank-deficient example is explained. |
| A.2 Eulerian convention and outer flux | **Closed in the current statement** | Both density traces, the Eulerian bulk derivative, and moving-outer-boundary flux are explicit. |
| E1: need a structural class and physical robustness theorem | **Requested additions supplied; significance still disputed** | Sections 8 and 10 now contain such theorems. Their existence cannot be denied; their depth must be evaluated. |
| E2: distinguish established Bernstein arithmetic and intrinsic dimension | **Technical and attribution response substantially supplied** | The relevant arithmetic and beta-mixture references are added, and the qn/mn distinction is correct. |
| E3: specific policy structure and certified performance | **Requested additions supplied** | The two-arc formula, quantitative lookup bound, and full-class separation are real results. Their mechanism is assessed below. |
| Endpoint-gate and model-error suggestions | **Included with attribution** | They are not falsely claimed as newly invented by the revision. |
| Overall four-journal significance | **Unresolved; decisive editorial objection** | The additions do not yet establish the level of central mathematical advance requested. |

The previous report explicitly warned that adding the elementary endpoint and model-error consequences would not automatically settle significance. Conversely, it would be moving the goalposts to say that the author has supplied no structural theorem, no policy theorem, or no quantitative example. The correct criticism now concerns the actual strength and mechanism of those results.

## 4. Mathematical audit of the new results

### 4.1 The attainable-rank criterion is valid, but is a range theorem for a finite linear map

**Anchors:** `sections/08_structural_class.tex`, Theorem 8.1, `thm:rank-criterion`, `eq:rank-right-inverse`, `eq:rank-margin`.

Let h be the coefficient vector and let Gamma be its Gram matrix. The equivalence between independence of the coefficient functions and positive definiteness follows from

\[
v^\top\Gamma v=\int (v\cdot h(x))^2\,\nu(dx).
\]

If Gamma is singular, its null vector annihilates every attainable failure coefficient vector. If it is invertible, the gate

\[
g_z(x)=\frac12-h(x)^\top\Gamma^{-1}z
\]

satisfies `f(g_z)=f(1/2)+z`, and the displayed norm estimate keeps it inside the gate interval. The perturbation estimates correctly bound the change of polynomial values by `sqrt(q+1) xi` and the change of Gram matrices by `nu(X)(2 H0 xi+xi^2)`. The normalization assumption is retained rather than inferred from positivity. I find no error in these arguments.

Nevertheless, this is a finite-dimensional surjectivity criterion with a convenient explicit right inverse. “Physically realizable” adds that the permitted comparator can evaluate the constructed function; within the unrestricted measurable-gate class, there is no further implementation constraint in the proof. The result does not characterize a restricted family of finite circuits, noisy comparators, inaccessible mark coordinates, or bounded calibration resources. Those are not omitted hypotheses of the theorem; they are distinctions relevant to its significance.

The reported radius is a sufficient bound in a chosen coefficient norm, not an intrinsic optimal robustness radius. Nothing in the paper proves optimality of that constant, and the author correctly does not claim it. The principal mathematical content is the range computation, not a new general physical attainability principle.

### 4.2 The intrinsic dimension proof is sound; the full-rank case is not the natural frontier

**Anchors:** Theorem 8.2, `thm:q-dimension`; retained Theorem 4.3, `thm:dimension`.

An open family of admissible degree-q factors contains pairwise coprime, exact-degree factors. At such a tuple, the differential of multiplication has kernel

\[
\delta F_i=\lambda_i F_i,\qquad \sum_i\lambda_i=0.
\]

Its rank is `n(q+1)-(n-1)=qn+1`. Normalization removes one dimension. The local section supplies a continuous injection from an open qn-dimensional set into any alleged exact continuous encoding, and invariance of domain supplies the lower bound. The fixed known denominator and the full-support-prior qualification are handled correctly. The distinction between intrinsic qn coordinates and an elevated positive Bernstein array of mn+1 entries is important and now explicit.

This is a genuine lower bound, not merely a count of stored coefficients. But replacing cubic degree by q is an immediate extension of the v3 proof, and the same mechanism already treats a broad rank-deficient fixed-mode class. Section 7 below gives the stronger rank-dependent conclusion `n(r-1)` with its proof. This is a referee deduction, not a claim that the submission contains a false theorem. It shows that the submitted full-rank theorem stops before a natural structural formulation accessible to its existing method.

A separate limitation must remain explicit: this is a worst-case exact encoding bound across the known command family. It is not a lower bound for approximate inference, finite-bit decision quality, the reachable states of every fixed policy, or the particular policy that witnesses the adaptive gap. The manuscript generally states these quantifiers correctly. Its main narrative nevertheless places the state lower bound and performance example next to each other without proving a substantive dependence between them.

### 4.3 Endpoint control and the last-step two-arc theorem are correct

**Anchors:** `sections/09_policy_structure.tex`, Theorems 9.1–9.2, `thm:endpoint`, `thm:two-arcs`.

The homogeneous continuation functional is a supremum of fixed-policy linear integrals. It is convex, homogeneous, and Lipschitz in variation. The accepted contribution is linear in the gate; the failure contribution is convex. Layer cake therefore gives an optimal endpoint gate. The right-continuity argument is needed and works: a strict deficit at any threshold below one would persist on a right interval, contradicting almost-everywhere optimality. Thresholding the already jointly Borel representative avoids a new measurable-selection gap.

For the final cartridge, selecting the common failure decision first and optimizing the accepted decision pointwise is legitimate. For a fixed failure decision, the gate is obtained from a linear pointwise comparison. On the collision component, the accepted envelope is a supremum of affine functions of `cos(y-theta)` and the failure contribution is affine. Their difference is convex, so its positive set is at most two end intervals in the cosine coordinate, hence at most two arcs on the circle. Compact infinite decision sets are covered by the stated continuity and selection argument.

However, the last-cartridge restriction is unnecessary under the same tagwise current-reward hypothesis. One can freeze an optimal continuation policy on the failure branch instead of freezing only a terminal decision. The accepted envelope remains a supremum of affine functions. Section 8 below supplies the full finite-horizon consequence and the Borel construction. This is another useful result available from the same method, not a newly discovered obstruction to the printed theorem.

### 4.4 The lookup bound is valid, but it is not a tractable global-control theorem

**Anchor:** Theorem 9.3, `thm:lookup-rate`.

The proof correctly approximates integrals of the gate against a uniformly regular family, rather than claiming uniform L1 approximation of every measurable gate. The two circle components have total reference mass two. The accepted-integrand error and the unnormalized failure-measure error therefore give the stated one-step constant. Convexity on the finite cube permits an endpoint vertex with no worse objective. Bellman propagation contributes the remaining horizon factor.

The resulting error

\[
2N G_+ e^{N|\lambda|B}(2L_k+K|\lambda|L_r)\frac{2\pi}{J}
\]

is a legitimate sufficient bound. Its exponential payoff factor, exponential gate-menu size, and exclusion of global optimization and finite-bit arithmetic costs are printed. They are not hidden mistakes. They also mean that the theorem does not establish efficient decision computation in the sense suggested by a casual reading of “effective finite-budget inference.” The exact filter's arithmetic count and the optimal-control problem's complexity must continue to be separated.

### 4.5 The smooth surrogate is an actual normalized experiment, not just a polynomial fit

**Anchors:** `sections/10_robust_approximation.tex`, Theorems 10.1–10.2, `thm:model-stability`, `thm:smooth-surrogate`.

The Bernstein average of normalized mark densities remains normalized because its nonnegative basis sums to one. Multiplying it by the positive linear factor R preserves positive Bernstein coefficients; degree elevation accommodates the quadratic placement and no-hit components. Both physical flag masses remain unchanged. This repairs the specific danger that a polynomial approximation might cease to define an experiment.

The L1 approximation estimates follow from the binomial first absolute moment and second centered moment. The factors `1/(4 sqrt(m))` and `1/(16m)` correctly include the conversion from L1 distance to total variation and the probability of the hit component. The two-policy regret comparison correctly contributes a factor of two. Coupling common policies while their histories agree gives `1-(1-e0)^N`; it does not incorrectly compare two separately recomputed feedback actions at mismatched histories. Independent policy randomization can be coupled through a shared seed.

These proofs appear sound. Their significance is narrower than a general robust-response theorem: they control complete-policy values, not parameter derivatives or rare-history posterior errors. The author explicitly acknowledges that distinction. The exact cutoff in radius derivatives remains a property of the chosen polynomial channel. The approximation rates are sufficient rates of this positive construction; there is no optimality lower bound or demonstrated necessity of the degree-regret tradeoff.

## 5. The adaptive separation reproduces — and admits a decisive ablation

**Anchor:** `sections/11_adaptive_advantage.tex`, Theorem 11.1, `thm:adaptive-advantage`.

### 5.1 The full-class reduction is not a computational loophole

At zero amplitude and the two-point prior, the angle conditional on a raw tag is independent of the radius. A Borel gate therefore contributes only its three tagwise acceptance fractions to the posterior; its accepted angle may supply parameter-independent randomization, but randomization cannot outperform the best continuation at that posterior. At the last and adaptive first steps, the homogeneous continuation gives convexity in the three fractions. For a nonadaptive pair, the value is separately convex in the two gate vectors. Successively replacing each vector by a vertex cannot decrease its value. Shared exogenous randomization averages deterministic-pair values.

Consequently the 64 vertex pairs do cover the nominal nonadaptive class. This conclusion follows from the analytic reduction, not from enumerating 64 cases. For nonzero amplitudes the mark may be informative, but the manuscript does not improperly reuse the finite reduction there: it applies a uniform model comparison to the whole declared policy class. The prior mixture is genuinely full support, although it is overwhelmingly atomic. Full support is not the same as an absolutely continuous prior, and the theorem does not claim the latter.

### 5.2 Independent exact-rational recomputation

The independent program used a different Machin-series truncation and a finer square-root enclosure than the author's program. It checked every printed nonadaptive upper-table entry, all eight adaptive first-gate bounds, the selected continuations, and all four terminal posterior signs. It gives:

| Quantity | Independent outward enclosure |
|---|---|
| Nominal nonadaptive optimum | (1.600432377967011670, 1.600432377967011671) |
| Nominal adaptive optimum | (1.602586453549804595, 1.602586453549804596) |
| Nominal advantage | (0.002154075582792925, 0.002154075582792926) |
| Final transferred lower-bound expression | (0.001171773732645061, 0.001171773732645062) |

Thus the claimed final lower bound **greater than 11/10000 is reproduced**. The last interval encloses the lower-bound expression, not the unknown exact difference between the two final full-cubic optima. This distinction is correct in the author's response and must remain so.

### 5.3 Removing the mechanics, angular mark, and full-rank cubic family leaves the nominal gain unchanged

Define an ordinary binary experiment with parameter i in `{l,u}` and a single Bernoulli signal, with probability

\[
q_i=\frac{a_0-\pi R_i^2-2TR_i}{a_0}
\]

of signal 1. Signal 0 is the complement. Use the same prior weights `z_l=2/5`, `z_u=3/5`, acceptance multiplier `s=99/100`, and two terminal decisions with endpoint payoffs `(2,1)` and `(1,2)`.

There is no billiard in this experiment, no impact coordinate, no angular detector, no cubic likelihood requirement, and no continuum of parameter values. The four binary endpoint gates give 16 nonadaptive pairs. Repeating the convexity argument covers all fractional binary gates. Independent exact evaluation gives **the same two nominal optima above**. The optimum accepts signal 1 at the first step; after an accepted 1 it again accepts signal 1, whereas after censoring it accepts nothing. The best nonadaptive controller accepts signal 1 at both steps.

The equality is not merely a numerical coincidence. For these optimizing policies the original three-tag experiment uses only “no collision” versus its complement. Its selected-policy formulas therefore depend only on the two numbers q_l and q_u. The full 64-case and reduced 16-case upper bounds show that the identical selected policies are optimal in their respective nominal experiments.

Writing

\[
M=z_lq_l(1-q_l)+2z_uq_u(1-q_u),
\]

the common difference is exactly

\[
\Delta_*=(1-s)M.
\]

It comes from declining to pay for an accepted second report on a branch where that report would not change the optimal terminal decision. The second cartridge is still consumed. This is an **acceptance-cost advantage**, not a saving in the counted mechanical resource. At zero acceptance cost the corresponding fixed-source binary problem has no adaptive advantage.

The tag-only witness also ignores the nonzero-amplitude mark: integrating its cosine component gives zero, so its tag probabilities and payoff remain unchanged for every amplitude. The cubic family enlarges the competing class, and the uniform transfer bounds show that the enlargement cannot close the gap. That is a valid robustness result. It does not show that exploiting cubic angle information causes the gain, or that the sharp 3n-dimensional exact state is needed by the winning strategy.

This is the principal significance objection to Theorem 11.1. The theorem is true as stated, but the demonstrated mechanism does not depend on the combination of structures presented as the paper's central advance. A finite example embedded in a richer model is not thereby a performance theorem about the richer model's essential structure.

## 6. The mechanical realization still functions as a programmable channel realization

**Anchors:** `sections/02_laboratory.tex`, `eq:detector-map`; the opening construction of `sections/10_robust_approximation.tex`.

The short-window collision-tube calculation is coherent and should be preserved. The ambient preparation uses a radius-independent cell area, charges unsuccessful insertion, and obtains collision mass `2RT/a0`. The separate conditional equilibrium mass is not silently substituted. Separation and convexity justify the one-collision coverage argument without deleting a positive-mass grazing neighborhood.

At collision, however, the detector's internal coordinate satisfies `|z|=R`. For any chosen smooth positive normalized density q(r,y), the same allowed inverse-CDF firmware can turn that exact geometric coordinate into the channel q(R,y). The generalization is now explicitly stated in the manuscript. This is not logically circular: the apparatus measures a physical coordinate rather than receiving the unknown parameter from the controller. Nor is it a counterexample to its ideal apparatus model.

It means that the polynomial family and its rank are selected through programmable garbling of an internally exact measurement. The subsequent algebraic theorems are largely independent of the billiard. A substantial realization theorem can certainly be important, but here the allowed observation class already grants the main mechanism needed to realize the desired likelihood. A top-level contribution needs to show something more restrictive, unavoidable, or structurally explanatory than the existence of such a programmable realization.

The reviewer does not require a quantum model, energy accounting, noisy hardware, or a many-collision limit as an arbitrary additional hurdle. The issue can be addressed within the stated ideal finite-budget class, by proving a genuinely informative theorem about constrained attainable families or about the interaction between state geometry and decision performance. The current paper has not yet done that.

## 7. Referee-derived strengthening: the fixed-mode rank-deficient dimension

This section gives a positive mathematical consequence of the manuscript's method. It is **not** a claim of literature priority and is **not** an assertion that the author stated the wrong full-rank theorem.

**Proposition.** Let W be a real vector space of univariate polynomials, of dimension r, and let U be a nonempty relatively open subset of W consisting of polynomials strictly positive on a compact interval I. Fix `t0 in I`. For n factors in U, consider the normalized product

\[
(F_1,\ldots,F_n)\longmapsto
\frac{\prod_iF_i(t)}{\prod_iF_i(t_0)}.
\]

Its image contains a smooth local patch of dimension **n(r-1)**, and this is its generic local dimension. A continuous exact encoding of all these factor histories requires at least n(r-1) real coordinates; recording the n individually normalized factors gives a matching factor-history encoding. For r=1 the normalized product is fixed and the dimension is zero. A common known denominator and a full-support prior do not change the lower-bound argument.

**Proof.** Let G be a greatest common divisor of W, and set `W_hat=W/G`. Since U contains positive polynomials, G has no zero on I. Dividing every factor by G is an invertible linear operation on W and removes a fixed factor `G^n` from every product. The space `W_hat` has dimension r and no common complex zero.

For r at least two, let d be the maximum degree in `W_hat`. Choose an exact-degree polynomial in the relative-open image of U. Its roots are finite. At each root, evaluation is a nonzero linear functional on `W_hat`; otherwise that root would be common to the whole space. A second polynomial can therefore be chosen in the same open set outside the finite union of evaluation kernels and the leading-coefficient-zero hyperplane. Repeating this argument gives n pairwise coprime exact-degree factors `F_hat_i`. The nonvanishing conditions are open and dense.

At such a tuple, the differential on `W_hat^n` is

\[
(\delta F_1,\ldots,\delta F_n)\longmapsto
\sum_i\delta F_i\prod_{j\ne i}F_j.
\]

Reducing modulo F_i shows that F_i divides delta F_i. Both have degree at most d, so `delta F_i=lambda_i F_i`. The only remaining condition is `sum lambda_i=0`. Thus the differential has kernel dimension n-1 and rank

\[
nr-(n-1)=n(r-1)+1.
\]

Evaluation normalization removes one further scalar direction. This yields rank n(r-1). The rank is locally constant on the coprime exact-degree set, so the constant-rank theorem gives a local image patch and a local section of that dimension. Composing a proposed exact continuous encoding with the section gives a continuous injection, and invariance of domain excludes a smaller Euclidean dimension.

For the matching upper encoding, each `F_i/F_i(t0)` lies in a fixed affine hyperplane of W of dimension r-1. Store its coordinates for all n factors. This is a continuous exact factor-history representation with n(r-1) coordinates. It is not required to identify permutations of factors. If r=1 every normalized factor is the same, proving the zero-dimensional case. Multiplication or division by a fixed nonvanishing function changes neither injectivity nor local dimension; a full-support prior identifies positive continuous likelihoods up to normalization. This completes the proof.

**Application to the paper.** For a fixed mode, let W be the range of the linear map from gate perturbations to failure polynomials. Its dimension is the Gram rank r. The same right-inverse construction restricted to the range gives a relatively open attainable family around the half-gate failure polynomial. The proposition then applies even when the coefficient Gram matrix is singular in the full degree-q ambient space. Full rank gives `r=q+1` and recovers qn. Rank-deficient spaces with a common polynomial divisor are included after removing that divisor.

This does not assert the same formula for an arbitrary union of different mode-dependent spaces, or for a physically restricted gate class without relative interior. Those are different problems. It does show that the fixed-mode structural statement naturally depends on rank, not on the full-rank/no-full-rank dichotomy. The accompanying finite symbolic checks include a sparse space `span{1,t^2,t^5}` and a space with common factor `1+t^2`; their general justification is the proof above, not the finite checks.

## 8. Referee-derived strengthening: two arcs at every finite stage

Again, this is a deduction under the printed assumptions, not a priority claim and not an objection to the correctness of the narrower Theorem 9.2.

**Proposition.** In the Lorentz observation family, if the accepted reward at each stage is constant on each raw tag, an optimal finite-budget Borel feedback controller can be chosen so that, at every state and selected mode, the collision high-acceptance set consists of at most two arcs. The no-collision gate is angle-constant. Endpoint values are eta and 1-eta, including eta=0. The future continuation problem may have the original compact decision set and bounded observable rewards; tagwise regularity is needed at each stage to which the arc conclusion is applied.

**Proof at one stage with b remaining cartridges.** Fix a posterior pi and mode a. Let g* be an optimal fixed-mode gate, whose existence is already proved in Section 5. Set

\[
A(x)=e^{\lambda r_a(x)}\mathcal W_{b-1}(k_R^a(x)\pi(dR)).
\]

Choose an optimal remaining policy on the failure branch of g*, and denote its conditional expected future payoff by L(R). If that branch has zero mass, choose any admissible continuation. Such a policy exists by the same finite-horizon attainment theorem. Define

\[
C(x)=e^{\lambda r_a^\dagger}\int L(R)k_R^a(x)\pi(dR).
\]

For any alternative gate g, using this frozen failure continuation and the optimal accepted continuations gives the feasible value

\[
J(g)=\int\{g(x)A(x)+(1-g(x))C(x)\}\,\nu(dx).
\]

At g*, this value equals the optimal fixed-mode value. Maximizing J pointwise gives the endpoint gate that accepts highly exactly where A>C. Its feasible value is at least the optimal value already attained by g*, hence must equal it. Allowing the failure continuation to reoptimize cannot change that equality into a value above the optimum. Therefore this threshold gate is optimal for the original problem.

On a collision tag, put `z=cos(y-theta)`. The measure `k_R^a(1,y) pi(dR)` is affine in z. The functional W is a supremum of linear integrals, so A is a convex function of z when the current accepted reward is tagwise constant. The function C is affine. Thus A-C is convex on [-1,1], its nonpositive set is an interval, and its positive set pulls back to at most two circle arcs. On the no-collision tag both A and C are angle-constant.

For feedback measurability, use the manuscript's Borel selection of g*(state,a) and its Borel optimal continuation policy on the compact state strata. The failure posterior, extended arbitrarily on its common-null branch, is Borel. Starting the selected continuation from that posterior makes L(R,state,a) jointly Borel by finite chronological integration. The coefficients of C are therefore Borel, while A has the established continuity in its arguments. The set `{A>C}` is jointly Borel. No selection from an unspecified topological space of policies is needed. Backward induction gives the claimed controller at all finite stages.

The argument gives an existence and boundary-count statement, not a finite-bit solver, a uniformly simple state partition, or a bound on the computational effort required to find the arc endpoints. Those distinctions remain essential. Nevertheless, the natural full-horizon structure is available; the last-step restriction does not mark a genuine barrier of the present method.

## 9. Literature and presentation

The targeted primary-source checks support the comparisons below. They are not an exhaustive priority search, and I do not assert that any one cited paper already proves this entire manuscript.

**[R1] Farouki and Rajan, *Algorithms for polynomials in Bernstein form* (1988).** The primary publication record explicitly treats arithmetic and other algebraic procedures directly in Bernstein form and discusses limitations of broad conditioning claims. This supports classifying the positive multiplication identity as established arithmetic, not dismissing the submitted operational model as an identical prior theorem. Primary record: https://research.ibm.com/publications/algorithms-for-polynomials-in-bernstein-form

**[R2] Petrone and Wasserman, *Consistency of Bernstein Polynomial Posteriors*, CMU Technical Report 708.** The institutional abstract describes Bernstein densities as beta mixtures in Bayesian nonparametric inference. That is relevant background for the mixture identity, not a prior proof of the exact controlled-radius filter. Primary record: https://www.stat.cmu.edu/tr/tr708/tr708.html

**[R3] Smallwood and Sondik, *The Optimal Control of Partially Observable Markov Processes over a Finite Horizon* (1973), Operations Research 21, 1071–1088.** The publisher's abstract identifies a finite-horizon piecewise-linear convex value function in state probabilities. This is a closer comparison for the finite-state nominal example and its continuation-envelope geometry than an exclusively general discussion of predictive representations. Its setting is not silently substituted for the present continuous-parameter, multiplicative-payoff theorem. Primary record: https://pubsonline.informs.org/doi/10.1287/opre.21.5.1071

**[R4] Feinberg, Kasyanov and Zgurovsky, *Partially Observable Total-Cost Markov Decision Processes with Weakly Continuous Transition Probabilities*.** Their preprint discusses posterior-state continuity, optimality equations, and existence under expected-total-cost criteria. The manuscript appropriately proves its own multiplicative-payoff case; the reference is context, not an exact theorem identity. Primary record: https://arxiv.org/abs/1401.2168

**[R5] Ren, Johansson, Shi and Shi, *Quickest Change Detection in Adaptive Censoring Sensor Networks*.** This work studies feedback-dependent censoring and communication constraints, with asymptotic optimality under a different detection criterion. It confirms that adaptive censoring and report-cost tradeoffs are established topics. It does not settle the submitted finite-budget numerical example. Primary record: https://arxiv.org/abs/1503.04999

**[R6] Kulik and Tymoshkevych, *Lift zonoid and barycentric representation on a Banach space with a cylinder measure*.** This is relevant background for vector-integral bodies and their geometry, not evidence that the present five-coordinate Bellman reduction has already appeared verbatim. Primary record: https://arxiv.org/abs/1211.2927

The current bibliography is improved. The remaining problem is not cured by appending more citations: the introduction must identify a central advance after established mechanisms are subtracted. The internal review dialogue, preservation counts, branch histories, and test receipts also occupy too much of the principal paper's mathematical narrative. These records should remain available in the repository and supplement, but they should not serve as evidence of mathematical depth. This is a presentation concern, not a demand to delete proofs or erase history.

## 10. Requirements for a materially different editorial assessment

A further revision should not answer this report merely by adding the two referee deductions as additional numbered theorems and announcing another closed round. They are useful consolidations, but both follow relatively directly from the existing method. Nor should it abandon the valid lower-bound and failure-retention results to make the paper easier to describe.

The central task is to establish a result in which a nontrivial constraint on attainable experiments, the geometry of exact or approximate information states, and a decision-theoretic consequence are genuinely connected. A concrete test for the present performance narrative is whether removing the advertised structural feature changes the theorem's mechanism or its sharp bound. Section 5's binary ablation shows that the current example does not pass that test.

Within the existing finite-budget setting, a convincing development could characterize a substantively restricted attainable class and prove a matching state/performance obstruction or sharp control law that depends on that restriction. The quantifiers, comparator class, and resource being improved would need to be fixed in advance. This is a direction for strengthening the central theorem, not a requirement to solve every possible generalization, and not a promise that any particular added result will receive acceptance.

For the current paper, the exact-state lower bound, the preserved probability of failures, the complete common-policy comparisons, and the explicit ideal-apparatus assumptions should all remain. The distinction between a theorem's validity and its journal-level significance should remain equally explicit.

## 11. Reproducibility and final recommendation

The new diagnostic program completed **39/39 checks**. Its SHA-256 is:

```
1d8fb43c5d974ae44edf5d624f80d92ed80a6b0030c319e521d9726c9955f7c7
```

The count refers only to this review's execution. It does not reuse the author's older 39-check count, the current author's 24 checks, or the previous referee's 20 checks. The program imports no author test code. Its exact arithmetic independently confirms the nominal table and transfer inequality; its symbolic checks support the displayed algebra and finite-rank examples. General geometric coverage, Borel selection, all-budget dimension, and all-Borel comparator coverage are assessed through the analytic proofs, not inferred from finite tests. No PDF, CI run, proof assistant, human approval, or exhaustive originality clearance is claimed.

**Final recommendation: REJECT at the requested four-journal level.** The principal revision is mathematically coherent and substantially improved, and its explicit adaptive-gap certificate withstands independent recomputation. The reason for rejection is that the claimed structural and performance advance remains largely a combination of elementary mechanisms whose advertised interaction is not established. The binary ablation and the two referee-derived extensions make that judgment concrete. This is not a verdict of impossibility on the research program and not an assertion that the principal theorem has been disproved.
