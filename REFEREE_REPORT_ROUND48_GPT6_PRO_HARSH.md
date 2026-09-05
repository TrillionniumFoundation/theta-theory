# Round 48: Independent harsh referee report on the frozen Round 47 revision

## Recommendation: Reject at the requested Annals–Inventiones–JAMS–Acta level

**Manuscript:** *Sharp Depth Scales for Adaptive Boundary Identification of Infinite Damped Jacobi Lattices*  
**Author named in the manuscript:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Revision branch reviewed:** `revision/round47-sharp-boundary-depth-2026-09-05`  
**Frozen distribution commit:** `1d10fbf2d1c06e875b5124d39266c7dbb0dd8735`  
**Distribution tree:** `c0b5ebfe5ab2b2826c416fd0150ab76e73cadaef`  
**Underlying source commit:** `ce0e531d65974ca46642e374df61f4299fadf786`  
**Source tree:** `99b09e515f0f96ad35f3fa2ad075c6f61ed96b89`  
**Preceding report commit:** `0c2f4c9f10bcf7c9f5a37538d869061e6e0fbfb8`  
**New review branch:** `review/round48-gpt6pro-harsh-round47-2026-09-05`  
**Review date:** 5 September 2026, Asia/Singapore  
**Reviewer:** GPT-6 Pro, at the repository user's request.

This is an AI-generated, independently reasoned referee-style assessment. It is not a report commissioned by, an appointment from, or an editorial decision of any of the four journals named above. The recommendation is an assessment of this submission at the requested standard, not a declaration that the research program is impossible or should be abandoned.

### 中文结论

按所要求的数学四大刊标准，建议拒稿。但本轮必须承认实质进展：闭式矩反演、线性深度逆映射常数、过采样、有限平均时长设计以及全历史信息下界已经构成一条相当完整的主证明链。**本报告没有得到推翻当前对数级恢复深度主定理的反例，也不沿用上一轮已经修复的理由。**

本轮发现两个可以精确定位、局部修复的置信保证问题：访问预算把“抽样概率”与“置信误差分配权重”混用了；有理外包计算没有把输入区间的舍入扩张计入最终半径。前者在前文允许任意权重的量词下不成立；后者有已运行的精确有理算术反例。这些问题不直接推翻主后验定理。

拒稿的进一步依据是顶刊层面的贡献定位：对数深度的阶数结论现在确有根据，但“原始固定窗口、无洗脱实验”的最优深度及联合深度—精度边界仍未确定，相关系统辨识和严重病态统计反问题的比较也不完整。本报告明确区分已经证明的阶数最优性、尚未证明的更强边界，以及审稿人的价值判断。

---

## 1. Executive assessment

Round 47 is substantially stronger than Round 45. In particular, the principal quantitative objection in Round 46 cannot simply be repeated. The manuscript has not merely substituted one large constant for another. It uses oversampling to separate Taylor order from the depth-dependent jet order, obtains a fixed-window separation exponent of order `J log J`, constructs a fixed duration law with an exponential tail and finite mean, and combines this with an all-history testing obstruction at logarithmic depth. These are genuine additions. [M1–M7]

My examination supports the following narrower positive assessment. I found no counterexample to the displayed all-depth inverse estimate, the two response-separation certificates, the posterior-contraction sufficient regimes, or the order-logarithmic all-history lower bound. The arguments make appropriate distinctions between a conditional-information floor and actual information, between posterior Gaussian approximation and frequentist coverage, and between fixed reset experiments and observations of an unreset history.

There are nevertheless two present defects in the operational claims. **R48-M1** concerns an omitted dependence on the confidence-allocation weights in `prop:visits`. **R48-M2** concerns an omitted input-enclosure error in `prop:outer`. These are not objections to the soundness of a confidence sequence with its correct weights, nor to interval arithmetic relative to the intervals actually supplied. They are defects in the transition from those valid ingredients to the stated guarantees.

The additional, and more substantial, basis for my negative recommendation at the requested journal level is editorial rather than a demonstrated false main theorem. The exceptional-significance case is still not established after separating classical moment inversion, analytic interpolation, uniform likelihood concentration, compact Laplace arguments, and locality plus stability. The new result may be a useful original synthesis; this review does **not** establish that an existing paper already proves it. But the submission has not yet shown why this particular synthesis is a sufficiently deep advance for the four journals requested. Adding assertions of closure to a proof ledger would not answer that question.

## 2. Scope, source freeze, and what was actually verified

The active mathematical object reviewed is `ROUND47_REVISION.tex` and its twelve inputs under `round47/`. I also read the retained supplement's `round45/triangular.tex`, `lattice.tex`, `filter_memory.tex`, preamble, and references. Its homogeneous finite-dimensional Gaussian results are not dependencies of the new infinite-Jacobi depth theorem. I examined the author response, the relevant preceding-report arguments and requests, the manifest and publication record, the certificate implementation, verifier, and test source. I do not claim to have audited every historical branch.

The Git comparison from the source commit to the distribution commit has exactly one descendant commit and adds exactly four files: `ROUND47_LOCAL_VALIDATION.json`, `ROUND47_MAIN_BUILD_CHECK.json`, `ROUND47_PUBLICATION.json`, and `ROUND47_TESTS.log`. It does not alter the manuscript sources. The source/distribution distinction is legitimate. [M10]

The publication record reports 34 author tests and a local, three-pass, 16-page main-manuscript build. It expressly says that the retained-supplement build and complete-checkout verifier were not executed and that the main PDF was not committed. The referenced workflow run `33933500834` was still reported as `queued`, with no conclusion, when inspected for this review. None of this is evidence of a failed mathematical theorem or a fabricated success claim. [M10]

I did **not** rerun the author's entire 34-test suite, the complete-checkout verifier, or either TeX build. I did independently reconstruct the certificate module from the fetched text, verify its exact Git blob identity, and execute 16 independent checks, including the rounding counterexample below. The verified module has Git blob

```text
c1f30bc24637559b4c3798367da9b0c7c63ca551
```

The executable review checks and their actual output are in `reviews/round48/independent_checks.py` and `reviews/round48/INDEPENDENT_CHECKS.json`. A passing check may mean that an advertised identity held, or that a stated defect was successfully reproduced; it does not mean that the entire manuscript was verified. There is no proof-assistant certification.

## 3. What survives this review

### 3.1 The deterministic inverse and both sampling laws

The identity

\[
 A^2+cA=-\operatorname{diag}(\mathsf J,\mathsf J)
\]

correctly gives

\[
 \mu_m=(-1)^m\sum_{k=0}^{m}\binom{m}{k}c^{m-k}v_{m+k}.
\]

The inverse Gram representation by normalized monic orthogonal-polynomial coefficient vectors controls the matrix inverse exponentially, rather than with a quadratic depth exponent. The subsequent ratio estimates retain the lower bounds on the polynomial norms and on the positive off-diagonal coefficients. With `j=J+1`, I find the assembled jet bound `Q^(25j)` conservative but consistent, including depth zero. The finite checks are supplementary to this algebra, not its all-depth proof. [M2]

The interpolation matrix is normalized by factorials. Its induced infinity norm bound `2^N binom(2N,N) <= 8^N` is appropriate. In particular, the response at the origin is known, not an additional noisy diagnostic cell. Oversampling with `N` larger than the required jet order genuinely permits the Taylor remainder to be absorbed without the previous depth losses. I find no defect in the resulting sufficient bounds

\[
 D_\omega\ge e^{-C_cj\log(ej)}\delta^{12},
 \qquad
 D_\nu\ge e^{-C_\infty j}\delta^8.
\]

The long-law atom masses normalize correctly, including the label convention for duplicate times. Its mean is exactly `13u_0/2`; the geometric index also supplies an exponential moment. Consequently, the stated linear elapsed-time bound is not based on replacing an unbounded duration by an unjustified deterministic maximum. [M3, M4]

### 3.2 The probability arguments do not reuse the old gap

The controlling metric is an impulse-response `L^1` metric common to every bounded realized input history. The sign decomposition places the intercept before the fresh sign, and candidate likelihoods use the same realized actions. These are the correct quantifiers for feedback robustness. The forward-map entropy and prior-mass estimates do not smuggle in an inverse-modulus assumption. [M5]

The finite-net score and centered-square bounds are taken at their actual shrinking resolutions. The nuisance likelihood factor has a summable transient envelope, uniformly over the working initial-state law. The posterior exponent arithmetic is

\[
 -13/32+3/32+1/16=-1/4.
\]

I therefore do not find the former fixed-resolution-to-shrinking-resolution problem in the present proof. The stated posterior sufficient regimes follow from the displayed concentration bound. The actual-information tracking result also correctly follows `Q_n`, not merely its diagnostic floor. [M5, M6]

### 3.3 The testing obstruction and its limitation

Changing only `b_J` forces the first changed step-response derivative to occur at order `4J+4`. The two-way return-path calculation, factorial short-time tail, and all-time integral split are consistent. The Gaussian chronological likelihood calculation then bounds the KL divergence for the entire permitted observation record, not just for a fixed open-loop input. Restricting the lower-bound subexperiment to zero initial state is legitimate for a uniform impossibility claim over the larger class. [M7]

The distinction between experiments must remain explicit. The `J log J` upper obstruction is a fixed-window response statement, and its testing corollary is for reset, zero-state windows. The no-washout compact-law experiment contains history information that this reset bound does not control. The manuscript currently says so. I do not treat its deliberately restricted reset corollary as a false claim about unreset feedback experiments.

For the finite-mean long law and the larger bounded-input experiment class, the positive and negative results do establish **logarithmic depth order**. They do not establish an optimal leading constant or a matching joint depth–accuracy frontier. That distinction is substantive, but it does not falsify the order statement.

### 3.4 Retained results

The supplement's nonlinear adaptive quasi-BvM argument uses strong uniform smoothness, a global quadratic contrast, and information eigenvalues bounded above and below on a high-probability event. Its relative Laplace argument does not require information convergence. I did not find a new failure in its nuisance derivative budget, six-duration embedding, balanced-prefix contrast, or finite-preparation mixture.

The state and memory conclusions remain finite-dimensional Gaussian images; the strong filter estimates express deterministic forgetting after differentiating a normalized tilt. They are not an infinite-dimensional BvM in an unrestricted operator topology. These qualifications are already substantially respected and should not be discarded in a response to this report.

## 4. R48-M1: the visit budget silently changes the confidence-allocation weights

**Location:** `round47/operations.tex`, `eq:bands`, `thm:confidence`, and `prop:visits`.  
**Classification:** a false general implication under the preceding arbitrary-weight formulation; a local missing hypothesis, not a failure of the main posterior theorem. [M8]

The response-band construction permits **any** positive weights `p_q` summing to one, with the probe-law weights given only as an example. Its radius is

\[
 R_{q,n}^2=\frac{2v}{a^2m}
 \log\frac{2m(m+1)}{\alpha_c p_q},\qquad m=N_q(n)>0.
 \tag{R48.1}
\]

The following visit-budget proposition introduces a different quantity `p`: each selected label's **exploration-law mass**. It sets `pi=rho p` and `C_v=4/(alpha_c p)`. Its proposed observation budget does not contain the arbitrary confidence weight `p_q`. The proof's upper bound on the radii therefore needs the additional assumption `p_q=p` on the selected labels, or a suitable lower bound on those weights. Neither is stated there.

This is not merely a request for a more detailed proof. It has an elementary counterexample for **every** proposed finite budget that is independent of the confidence weights.

Fix a certificate grid `G`, a radius `delta` smaller than the box's `d_J` diameter, and an integer `n` satisfying the printed budget. For every visited label, since `1 <= m <= n`,

\[
 R_{q,n}^2\ge\frac{2v}{a^2n}
       \log\frac{4}{\alpha_c p_q}.
 \tag{R48.2}
\]

Choose the weights of all labels in `G` sufficiently small in advance, distributing the remaining mass positively among the other diagnostic labels. The right side of (R48.2) can be made arbitrarily large without changing `n`, the sampling probabilities, or the count-error bound. This choice is made before the data, not retrospectively.

For completeness, this can invalidate the claimed diameter itself, not just the proof's radius test. Put `H_*=C_*/lambda_*`, so that `|h_beta(t)| <= H_*`. For any `zeta>0`, the bounded signal and Gaussian noise give a deterministic finite `M_Y` with

\[
 P\{\max_{i\le n}|Y_i|\le M_Y\}\ge1-\zeta.
\]

For example, the signal bound used in the band proof permits

\[
 M_Y=B_*+aH_*+\sigma\sqrt{2\log(2n/\zeta)}.
\]

On this event, `|hhat_{q,n}| <= M_Y/a` whenever `m>0`. Choose the confidence weights so that every lower bound in (R48.2) exceeds `(H_*+M_Y/a)^2`. Then every parameter in the box satisfies every selected band. An unvisited label imposes no constraint either. With the permitted choice `Q_n=G`, the confidence set is the whole box with probability at least `1-zeta`, and its diameter is larger than `delta`. Taking `zeta` small contradicts the claimed high-probability diameter guarantee. The simultaneous **coverage** theorem itself remains valid.

**Required repair.** Distinguish the sampling mass `w_q` from the confidence allocation `eta_q`. For equal sampling mass `p` on the grid, retain `pi=rho p`, but replace

\[
 C_v\quad\hbox{by}\quad
 \frac4{\alpha_c\eta_{\min}},
 \qquad \eta_{\min}=\min_{q\in G}\eta_q.
 \tag{R48.3}
\]

Alternatively, explicitly specialize to `eta_q=w_q` before stating the proposition. The count Chernoff bound still uses `p`; the confidence logarithm uses `eta_min`. A regression should prevent these quantities from being silently interchanged again. The independent script supplies an exact algebraic illustration of (R48.2); the all-finite-budget counterexample is the argument above, not a Monte Carlo experiment.

## 5. R48-M2: certified input enclosure error is absent from the outer-radius guarantee

**Location:** `round47/outer_algorithm.tex`, input-representation paragraph, `eq:outer-errors`, and `prop:outer`; implementation `outer_confidence`.  
**Classification:** an incorrect bridge from outward-enclosed inputs to the original statistical radius; locally repairable. [M9]

The implementation accepts rational intervals containing the real statistical bands. This is a sensible interface. But the proposition's claimed radius is still the original `R_{q,n}+2E`, and `E` contains only tail, mesh, and Taylor errors. It contains no error from the outward enclosure of the band endpoints.

Write the original band as `I_q=[hhat_q-R_q,hhat_q+R_q]`, its represented interval as `I_q^rat`, and assume

\[
 I_q\subset I_q^{\rm rat}
 \subset[\widehat h_q-R_q-\epsilon_q,
         \widehat h_q+R_q+\epsilon_q].
\]

If the computed interval `[H_q-E,H_q+E]` intersects `I_q^rat`, the triangle inequality yields

\[
 |h_\beta(t_q)-\widehat h_q|
 \le R_q+\epsilon_q+2E,
 \tag{R48.4}
\]

not `R_q+2E`. The missing term cannot be removed by refining the parameter mesh or increasing the Taylor order.

### An executed exact-arithmetic witness

Use rational bounds

\[
 c\in[1,1001/1000],\quad
 a_k\in[1/2,501/1000],\quad
 b_k\in[3,3001/1000],
\]

which satisfy strict diagonal dominance. Set `J=0`, `t=1/100`, `K=4`, mesh half-width bound `r=1/1000`, and Taylor order `P=6`. Take the original band `[-10^-7,10^-7]` and the valid but deliberately coarse outward enclosure `[-1,1]`.

The SHA-verified author implementation examines one box and retains it. Exact rational computations, with decimals shown only for readability, give

\[
\begin{aligned}
 H&=4.983242104554987\times10^{-5},\\
 E&=6.324865031791793\times10^{-7},\\
 H-E&=4.9199934542370696\times10^{-5},\\
 R+2E&=1.3649730063583584\times10^{-6}.
\end{aligned}
\]

The exact rational inequality `H-E > R+2E` is tested, not inferred from rounded decimal output. The center's admissible infinite completions, and indeed the completions covered by this uniform error bound, lie outside the original band enlarged by `2E`. Supplying the original narrow rational band directly instead returns an empty union, as it should.

This example attacks neither the validity of the tail/mesh/Taylor error bounds nor interval arithmetic relative to the **supplied** interval. It attacks precisely the assertion that an arbitrarily outward-enclosed input still yields the original statistical radius plus `2E`. The deterministic construction statement must account for input representation even on data records for which the original confidence set is empty; coverage is a separate probabilistic event.

**Required repair.** Carry an explicit `epsilon_q` budget and replace the diameter condition by

\[
 \max_{q\in G}(R_{q,n}+\epsilon_q+2E)
 \le\frac{\delta}{4LA}.
 \tag{R48.5}
\]

Equivalently, redefine and expose the represented band's center and radius, and use that enlarged radius consistently. The output should report the statistical, representation, tail, mesh, and numerical budgets separately. Also distinguish completions of a retained full `K`-box from arbitrary completions of its projected prefix: the latter need only have a witnessing retained full box for the diameter argument. Universal feasibility of every tail appended to a projected prefix is unnecessary and should not be implied.

## 6. What the existing bounds already say about joint depth and accuracy

The following deductions sharpen the interpretation of the submitted results. They are not counterexamples to weaker sufficient statements, and they do not require a new observation law.

### 6.1 The confidence budget has order `kappa^-1`, not `kappa^-2`

Specialize the confidence allocation to the sampling law, repairing R48-M1. On a certificate grid,

\[
 \kappa=\frac{p\delta^2}{4L^2A^2},\quad
 r_*^2=\frac{\delta^2}{16L^2A^2},\quad\pi=\rho p.
\]

Consequently the nontrivial term defining `B_v` is exactly

\[
 \boxed{\frac{16v}{a^2\pi r_*^2}
       =\frac{64v}{a^2\rho\kappa}.}
 \tag{R48.6}
\]

For no washout, the remaining factors in the visit budget are logarithmic at the depth and accuracy scales under discussion. The count-only term is no larger in polynomial order, since `p^-1 <= kappa^-1` for these certificates. Thus the corrected confidence construction permits a strictly larger sufficient region than the particular uniform-Hoeffding posterior proof.

Take `J_n=floor(r log n)` and `delta_n=n^-s`, with `r,s>0`. The analytic long-law certificate has

\[
 \kappa_n\ge C n^{-(C_\infty r+8s)}.
\]

Choosing confidence and count error probabilities tending to zero polynomially adds only logarithmic factors. Equation (R48.6) and `prop:visits` then give confidence coverage tending to one and diameter at most `delta_n` whenever

\[
 \boxed{C_\infty r+8s<1.}
 \tag{R48.7}
\]

This statement concerns the theoretical confidence sets, or the corrected outer construction with sufficiently small additional enclosure errors. It is not a claim that the existing capped exhaustive algorithm efficiently reaches such depths. The displayed posterior proof uses `n kappa_n^2` and only gives the smaller sufficient region `C_infinity r+8s<1/2`. Both statements can be true simultaneously.

### 6.2 The compact-law sufficient statement can also be strengthened immediately

With `J_n=floor(r log n/log log n)` and `delta_n=n^-s`, one has

\[
 (J_n+1)\log(e(J_n+1))=r\log n\,[1+o(1)].
\]

The manuscript's own posterior calculation therefore permits

\[
 C_cr+12s<1/2,
 \tag{R48.8}
\]

rather than only stating the smaller little-oh depth regime. The corrected confidence budget similarly permits `C_c r+12s<1`. These are direct corollaries of the submitted inequalities, not a new optimality theory.

### 6.3 A matching joint frontier is still not proved

Let `theta` denote the positive propagation exponent in the manuscript's all-time bound. Applying that bound to two parameters separated by a fixed multiple of `delta_n` at site `J_n` gives

\[
 \mathrm{KL}\lesssim
 n\delta_n^2e^{-4\theta(2J_n+1)}
 =O(n^{1-2s-8\theta r}).
\]

Thus uniform recovery at accuracy `n^-s` is impossible in the region

\[
 8\theta r+2s>1.
 \tag{R48.9}
\]

The boundary case is not settled by this calculation. The sufficient regions and this necessary obstruction are far from matching. At fixed accuracy they agree on logarithmic **order**, which is real progress. They do not determine a common leading constant, the optimal accuracy exponent at a given depth, or the value of feedback. The paper explicitly declines some of those stronger claims; the title and summary should continue to honor that restriction.

## 7. Originality and significance: the case required by the requested venue is incomplete

The Round 46 demand for an actual depth obstruction has been substantially answered. It would be unfair to move the goalposts by pretending that every paper must solve every design problem. My objection is instead that the manuscript still does not isolate the conceptual advance after the following comparisons.

**Dynamic Jacobi inversion.** The comparison with Mikhaylov and Mikhaylov is materially better: their discrete-time boundary/moment reconstruction differs from this continuous-time, noisy, damped experiment. Their moment-problem paper already connects dynamic data, moments, and finite-block reconstruction. The present statistical and elapsed-time conclusions are not supplied merely by that observation. The revision properly acknowledges the deterministic lineage. [P1]

**Adaptive BvM.** Du, Nair and Janson's Theorem 1 treats adaptive linear Gaussian data without a deterministic limiting information matrix; their Corollary 1 is a policy-uniform **basis-vector/bandit** statement, not a general-design uniform nonlinear theorem. Their Appendix F discusses weaker parametric regularity. The retained result here has nonlinear means and nuisance transients, but also a uniformly nondegenerate root-`n` information regime and strong smoothness. That is not a general resolution of the anisotropic or weak-regularity difficulties in their paper. The comparison should identify both the additional model structure and the stronger hypotheses. The distinction between Gaussian posterior approximation and frequentist validity must remain. [P2]

**Finite-time partially observed system identification.** Sarkar, Rakhlin and Dahleh study stable discrete-time systems of unknown **finite** latent order; their Section 3 assumptions and Theorem 5.1/Corollary 5.1 concern noisy Hankel and finite-impulse-response estimation. An infinite Hankel matrix is not the same thing as an infinite-dimensional physical state. Their realization problem also differs from recovery of labeled Jacobi coefficients. Consequently their results do not automatically subsume this manuscript. Nevertheless they are an important missing benchmark for the proposed route from finite noisy input-output data to a data-supported structural depth. A comparison should distinguish prediction/realization error, similarity ambiguity, and physical-coordinate error. [P3]

**Severely ill-posed statistical inversion.** Agapiou, Stuart and Zhang derive logarithmic contraction behavior for linear inverse problems with exponentially decaying singular values under commuting Gaussian assumptions. That is a different model, and it does not prove the present nonlinear coefficient result. It does demonstrate why an exponential loss of visibility producing a logarithmic recoverable index is not, by itself, an unfamiliar statistical mechanism. The new contribution must be the model-specific uniform geometry and experiment/resource result, not the word “logarithmic.” [P4]

After these distinctions, the most promising contribution is the combination of a physical coefficient inverse, two-way damped locality, and finite-cost observation design robust to arbitrary allowed baselines. The proof is coherent, but its components remain relatively direct in this uniformly bounded, uniformly pinned, common-damping Jacobi box. I am not persuaded that the present breadth and depth justify one of the four requested journals. This is a significance judgment, not a claim of plagiarism, a complete priority search, or a theorem that no such contribution could be sufficiently important.

One substantive way forward would be a sharp characterization of the original fixed-window **unreset** experiment, or a substantially tighter resource–depth–accuracy theorem that explains what the random duration law and feedback actually change. An alternative would be a genuinely useful general structural theorem beyond this single box model. These are possible mathematical directions, not a requirement to deliver all of them or an excuse to dismiss the present valid results.

## 8. Presentation, verification, and acceptance conditions

The root `README.md` still advertises Round 45. At the reviewed head there is no `ROUND47_REVIEW_INDEX.md`, although the Round 47 sources and publication record are present. A reader should not have to infer the active submission from branch history. Add a short current index pointing to the main manuscript, retained supplement, response, source freeze, and actual verification scope. This is a navigation defect, not a false mathematical theorem.

The new verifier really does resolve a named commit, check ancestry and manifest coverage, and compare source bytes with Git objects. That is a substantive repair of the previous regex-only SHA check by code inspection. It should not be criticized as if the old verifier were still active. Conversely, fixture tests and a main-only build are not a successful full-checkout run; the publication record correctly refrains from claiming one. A future complete build should cover both declared roots and report its actual outcome.

Before any positive correctness recommendation, R48-M1 and R48-M2 need explicit textual and implementation repairs, together with negative tests demonstrating the old failure mode and the corrected budgets. The main proofs should remain intact unless a new defect is actually established. For a renewed four-journal significance assessment, the manuscript additionally needs a precise contribution comparison and a clearer account of what frontier it has, and has not, identified. Merely renaming the sufficient constants or adding more routine consequences would not resolve that assessment.

## 9. Reproducible checks and source anchors

Run from the repository root:

```sh
python3 reviews/round48/independent_checks.py --output /tmp/round48-checks.json
```

The script first rejects a certificate module whose Git blob differs from the reviewed one. The 16 checks cover the block identity; moment inversion through order eight; Gram identities of sizes one through six; first changed derivatives at depths zero through five; interpolation matrices of orders one through twelve; exact compact and long grid certificates; law masses and mean duration; finite secant inequalities; posterior exponent arithmetic; the allocation-radius obstruction; the rounding witness; rejection with the original narrow band; the corrected input-error inequality; inverse-`kappa` confidence-budget scaling; and refusal to return a partial capped search. These are finite algebraic and implementation checks, not empirical adaptive-policy coverage experiments or all-depth formal proofs.

All manuscript anchors below refer to the frozen distribution commit, not a moving branch.

| Anchor | Frozen source and principal relevance |
|---|---|
| M1 | `ROUND47_REVISION.tex`; `round47/introduction.tex`: title, advertised regimes, experimental distinctions |
| M2 | `round47/inverse.tex`: closed moment inversion, Gram inverse, `eq:jet` |
| M3 | `round47/compact_window.tex`: interpolation, `eq:compact-certificate`, compact separation |
| M4 | `round47/finite_mean.tex`: `eq:long-certificate`, mean duration and `eq:clock-tail` |
| M5 | `round47/statistics_geometry.tex`: common metric, conditional sign floor, entropy and prior mass |
| M6 | `round47/statistics_bounds.tex`; `round47/information_limits.tex`: finite-n posterior, information tracking, weighted consequences |
| M7 | `round47/frontier.tex`: return-path lower bounds, reset restriction, all-history testing |
| M8 | `round47/operations.tex`: `eq:bands`, `thm:confidence`, `prop:visits`, `eq:visit-budget` |
| M9 | `round47/outer_algorithm.tex`; `tools/round47_certificates.py`: represented inputs, `prop:outer`, finite exact implementation |
| M10 | `ROUND47_PUBLICATION.json`; `round47/SOURCE_MANIFEST.json`; `tools/verify_round47.py`; source/distribution comparison |

Canonical manuscript: <https://github.com/TrillionniumFoundation/theta-theory/blob/1d10fbf2d1c06e875b5124d39266c7dbb0dd8735/ROUND47_REVISION.tex>.

Operational source: <https://github.com/TrillionniumFoundation/theta-theory/blob/1d10fbf2d1c06e875b5124d39266c7dbb0dd8735/round47/operations.tex>.

Outer-construction source: <https://github.com/TrillionniumFoundation/theta-theory/blob/1d10fbf2d1c06e875b5124d39266c7dbb0dd8735/round47/outer_algorithm.tex>.

Source/publication comparison: <https://github.com/TrillionniumFoundation/theta-theory/compare/ce0e531d65974ca46642e374df61f4299fadf786...1d10fbf2d1c06e875b5124d39266c7dbb0dd8735>.

### Targeted primary literature

**P1.** Alexander Mikhaylov and Victor Mikhaylov, *Dynamic inverse problem for special system associated with Jacobi matrices and classical moment problems*, arXiv:1907.11153 (2019). Targeted comparison of the dynamic-data/moment reconstruction setting; not an assertion that its statistical experiment equals this one. <https://arxiv.org/abs/1907.11153>.

**P2.** Kevin Du, Yash Nair and Lucas Janson, *Bernstein–von Mises for Adaptively Collected Data*, NeurIPS 2025; arXiv:2511.06639. Theorem 1, Corollary 1, and Appendix F were consulted for the distinctions above. <https://arxiv.org/html/2511.06639v1>.

**P3.** Tuhin Sarkar, Alexander Rakhlin and Munther A. Dahleh, *Finite Time LTI System Identification*, Journal of Machine Learning Research 22(26) (2021), 1–61. Section 3, Theorem 5.1, and Corollary 5.1. The targeted comparison used the publisher's parsed text; attempted web PDF screenshots were unavailable. <https://www.jmlr.org/papers/v22/19-725.html>. <https://www.jmlr.org/papers/volume22/19-725/19-725.pdf>.

**P4.** Sergios Agapiou, Andrew M. Stuart and Yuan-Xiang Zhang, *Bayesian Posterior Contraction Rates for Linear Severely Ill-posed Inverse Problems*, arXiv:1210.1563. The abstract/model description is used only for the stated exponential-singular-value/logarithmic-contraction comparison. <https://arxiv.org/abs/1210.1563>.

---

## Final recommendation

**Reject at the requested four-journal level.** The order-logarithmic main result has survived this review's checks and is a genuine improvement over the preceding submission. Two subsidiary confidence guarantees are not correct under the input and weighting freedoms currently stated, and they require the specific local repairs above. The further obstacle to a positive four-journal recommendation is the demonstrated significance of the contribution, not an invented fatal failure of the main theorem. A response should preserve the valid mathematics, correct the two guarantees, and address the remaining substantive comparison and frontier questions without treating numerical tests or a proof ledger as substitutes for proofs.
