# Round 52 — Harsh referee report on the frozen Round 51 revision

## Recommendation: Reject at the requested Annals–Inventiones–JAMS–Acta standard

**Manuscript:** *Single-Atom Boundary Identification with Retained State and Logarithmic Physical Depth*  
**Author named in the manuscript:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/round51-single-atom-response-transfer-2026-09-05`  
**Frozen reviewed commit:** `f991a17a5d99bf0cce9f1e457df91097e69dcd8a`  
**Frozen reviewed tree:** `608bd9fa2b4272c79d0063dd795e1425ac15fee0`  
**Round 51 mathematical/source commit:** `f1393cdb21121f6a95faff99672003370ecca853`  
**Controlling Round 50 report commit:** `a7b9ffcfd79d2f8cd5179238db9124486c1d9f0a`  
**New review branch:** `review/round52-gpt6-astra-pro-harsh-round51-2026-09-05`  
**Date:** 5 September 2026  
**Reviewer:** GPT-6 Astra Pro, at the repository user's request.

This is an independently reasoned, AI-generated referee-style assessment, not a journal appointment, commissioned external report, or editorial decision of any named journal. Its mathematical conclusions and editorial judgment are distinguished below.

## 中文结论

**按用户指定的数学四大刊标准，本报告建议拒稿。拒稿不等于主定理已被推翻。** 本轮没有找到足以撤回当前对数深度恢复主定理的反例，也没有发现其核心证明链中已被证实的致命错误。不能为了满足 harsh review 的形式而把成立的条件定理说成错误。

Round 51 已实质回应上一轮：单原子表述、扩大成功事件、全符号加权能量、较快的余项衰减、有限响应到物理系数的化简，以及当前可执行源码，均确实存在。审稿人取得了与 Git blob 一致的作者程序和测试文件，实际重跑了 **66 项作者测试，全部通过**。因此，不再沿用上一轮“当前程序未取得”的批评。

本轮有新的、可复现的否定证据。`diameter_certified` 只检查若干数值半径，不绑定观测函数、采样时钟及完整滞后网格。把 `outer_boxes` 对错误观测网格返回的半径交给该函数，可得到 `True`，尽管保留的前缀集合直径为 **1**，而目标仅为 **1/8**。不仅零观测如此；一个非零、极短时刻的阶跃响应观测，以及重复 61 次的同一非零观测，也能复现。这是**无条件认证接口与条件定理之间的缺口**，不是正文明确要求“sampled-pulse grid”的定理反例。

另一项主要意见来自原始文献核对。Sarkar–Rakhlin–Dahleh 的 Algorithm 1 的确写了高斯输入，但 Assumption 1 允许各向同性次高斯输入，其误差证明也明确按次高斯输入展开。Rademacher 输入满足这一输入条件。因此，不能仅以该伪代码使用高斯采样，就将有界输入当作理论层面的实质障碍。当前稿件没有宣称所有既有方法必然失效；本报告也不把既有 FIR 定理直接冒充为整个新主定理。真正还需比较的是不规则时长、块间反馈、物理反演常数及完整后验。

独立审稿程序另执行了 **10 组、88 项有限检查**（其中包含 2 项源码身份检查），全部通过，并复现上述 **3 个接口反例**。程序成功退出的含义是“局部核查通过且缺口复现”，绝不是“实现已被认证正确”。报告还给出两条有证明的正面改进：当 `rho<1` 时不必要求探索律本身有原子；利用实际时钟范数可进一步改进几何余项及误差指数。这些属于改进，不是把保守正确的界判成错误。

---

## 1. Decision and classification

The paper now presents a coherent theorem, rather than merely a collection of closure assertions. I nevertheless do not find an adequate case for exceptional mathematical significance at the requested four-journal standard. Its strongest remaining feature is an explicit synthesis: a local sampled-channel inverse, a tail-uniform Jacobi inverse, and a chronological complete-posterior argument. That synthesis merits serious specialist consideration; its correctness does not by itself establish the requested publication threshold.

| ID | Finding | Classification and consequence |
|---|---|---|
| R52-C1 | The exposed diameter predicate does not bind its input radii to the observable map required by the theorem | Major verification-interface defect; three concrete unsafe-composition witnesses; does not refute the conditional analytic theorem |
| R52-M1 | The closest-comparison discussion omits the comparator's sub-Gaussian input assumption and proof scope when emphasizing Gaussian-input incompatibility | Material contribution-comparison issue; not a proof that prior literature contains the entire main theorem |
| R52-M2 | Exceptional depth and significance remain unestablished after the synthesis is decomposed | Principal editorial objection; no claim that all originality is absent |
| R52-Q1 | With positive nonexploration probability, the exploration law need not itself have an atom | Proven generalization, not a correctness defect |
| R52-Q2 | The actual clock norm gives a stronger rational geometric remainder and a better sufficient error exponent | Proven quantitative refinement, not a false printed bound |
| Scope | Fast chosen clock, block commitment, summably transient nuisance, non-sharp joint rate region | Genuine declared limitations, not concealed counterexamples |

The negative recommendation is not based on a fabricated no-go theorem. It also does not revive issues demonstrably repaired since Round 50.

## 2. What was actually reviewed and executed

I read the active TeX root and all nine inputs in its declared order: introduction, model/inverse, sampled generator, likelihood, blocks, response transfer, enclosures, optimality, and references. I read the Round 50 response and review index, the current literature audit, the controlling report's substantive assessment and requests, the complete current implementation and test source, and the verifier source. The inherited moment/Gram source is explicitly identifiable by its unchanged blob. I did not audit every historical manuscript or every repository branch. [M0–M12]

The Git comparison from the controlling Round 50 commit to the frozen Round 51 head reports `ahead_by=2`, `behind_by=0`, with Round 50 as the merge base. This review branch starts at the exact reviewed Round 51 commit. Historical sources and author files are not rewritten by this review.

The implementation and test files were reconstructed locally from the connector's complete text reads and verified against Git's blob hash before execution:

| File | Verified Git blob | Independently computed SHA256 |
|---|---|---|
| `tools/round51_certificates.py` | `6eda73359c1999027394062f2edb1532e0bed21f` | `c7284fb651146181c8e6264a11579b76b08864102e9dda6b84878f2e171a3001` |
| `tests/test_round51.py` | `2a6999afad296310a633d77c81a96950e45cf4d5` | `65e26cee191e5b59ef602767a2327d4acca142de3eef8fa1586d3dcd17789c35` |

The actual author-suite execution used Python 3.13.5: 66 tests, zero failures, zero errors, zero skips. The receipt is [AUTHOR_TEST_REPLICATION.json](reviews/round52/AUTHOR_TEST_REPLICATION.json).

The independent program [independent_checks.py](reviews/round52/independent_checks.py) performs ten groups and 88 finite checks, including source identities, all-sign energy, equality cases of weighted Cauchy–Schwarz, first affected diagonal and edge jets, finite-section locality, damped moment reconstruction, event probabilities, posterior/remainder arithmetic, improved clock-tail prefactors, and repaired input/resource guards. It separately reproduces three certification-interface witnesses. Its actual output is [INDEPENDENT_CHECKS.json](reviews/round52/INDEPENDENT_CHECKS.json).

**Not executed in this review:** the whole-checkout 18-source verifier, the three-pass LaTeX build, posterior simulation, or a proof assistant. I inspected the verifier source but do not relabel inspection as successful execution. I reviewed the article's TeX, not an independently rendered article PDF. The author's build receipts are not this referee's build results. The current executable-source objection is resolved; complete artifact reproduction is not claimed.

## 3. Audit of the mathematical chain

### 3.1 Common stability, product geometry and physical inversion

The pinned Jacobi box supplies a common positive lower form bound. The cross-term energy has uniform upper and lower comparisons with the state norm, and differentiating it cancels the mixed damping term. The resulting stable semigroup envelope is compatible with both the infinite chain and principal finite sections. Coordinate convergence gives strong convergence on finite-support vectors; bounded generators and the common integrable tail then give the stated response continuity. This is not an unjustified assertion of operator-norm compactness. [M1]

The moment identity follows from `A^2+cA=-diag(J,J)` with the stated derivative indexing. The inverse Gram representation uses monic-polynomial coefficients and positive norm ratios. In particular, the positive edge lower bound is essential when recovering `a_k` from a squared-edge ratio. The displayed exponential-in-depth conditioning estimate has a plausible and explicitly traceable derivation; I did not find a hidden quadratic-in-depth exponent in the assembled secant bounds.

The independent checks also verify the first changed step-response jet: changing `b_J` first appears at order `4J+4`; changing `a_J` first appears at order `4J+6`. Those checks support the locality bookkeeping, not the universal conditioning theorem by themselves. The conservative inverse `L=Q^{25(J+1)}` remains the main deterministic amplification cost.

### 3.2 The sampled pulse channel is corrected, not confused with an impulse

With `U=exp(Delta A)`, `X=U-I`, and `H=int_0^{Delta/2} exp(uA)du`, the selected clock puts all operators in the same convergent logarithm/square-root neighborhood. The identity

\[
F_r(X)H=A^{r-1},\qquad
F_r(x)=\Delta^{-r}\log(1+x)^{r-1}\frac{\log(1+x)}{x}(\sqrt{1+x}+1)
\]

correctly cancels the integrated-pulse channel. Removable scalar singularities are handled analytically. The polynomial transform is parameter-independent, and the row-sum bound survives expansion of `(U-I)^k`. I find no branch-selection or integrated-input error here. [M2]

The new `16^{-N}` remainder is justified by the displayed Cauchy estimate and tail summation. The weighted budget

\[
\mathcal W=\max_r\sum_{l=0}^N\frac{T_{rl}^2}{N+1-l}
\]

is the correct dual squared norm for the block-energy weights. Its positivity follows from the nonzero first transform row; `W<=A^2` is valid. Section 7.2 below improves the remainder again, but does not invalidate the current one.

### 3.3 Block information and chronology

On a successful fast block, commitment is what makes the intercept independent of every current block sign. Expanding the full convolution and averaging all signs yields exactly

\[
E_S\sum_k f_{b,k}^2
=\sum_k P_{b,k}^2+a^2\sum_k(m-k)d_k^2.
\]

The probability `p_*^m`, not a one-stage probability, multiplies that block floor. The event is generated by exogenous action randomizers, and the unsuccessful patterns contribute nonnegative energy. Crucially, this calculation does not condition the actual posterior on block success or discard other likelihood factors. [M4]

The wider lower-bound policy class and the narrower attaining block-committed class are logically compatible. Conversely, this argument does not authorize arbitrary within-block response-dependent feedback. The manuscript correctly retains the distinction.

### 3.4 Complete working posterior and the transient nuisance

The score exponential martingale is formed in the readout chronology, where the input-induced contrast is predictable before the fresh noise. The grouped-square exponential argument requires bounded nonnegative block increments, not independent blocks. The deterministic response-metric cover interpolates both realized squares and their conditional expectations. I did not find terminal-design conditioning disguised as a fixed-design proof. [M3]

The nuisance integral is bounded uniformly before integration over the working law. Its support need not contain the true initial state because every permitted transient decays under the common stability envelope and the positive stage gap. The numerator/denominator arithmetic is consistent:

\[
-97/512+13/256+1/32=-55/512\le-1/16.
\]

With `q=a^2 kappa/m`, the entropy and prior costs are of order `log(n)^2`; the stated strict exponent inequality gives a polynomial margin over these costs and the growing group factor. The medians argument needs joint prefix mass above one half, which the theorem supplies; it is not an unjustified union of coordinatewise marginal statements.

This is a credible complete-posterior argument under the declared assumptions. Its robustness is nevertheless to a **summably decaying initial-state discrepancy**, not to a persistent misspecification of the physical response, forcing law, or noise mechanism. That distinction matters when evaluating significance, even though the manuscript's literal working-law statement is correct.

### 3.5 Response estimation and finite sections

The finite response-net estimator obeys the stated minimum-residual triangle inequality. Its finite ordering resolves measurable tie breaking. The confidence-set diameter follows from pairwise response separation, provided the measured quantities really are the required pulse coefficients. [M5]

For the sign-centered estimator, removing the first signed pulse leaves a bounded-input trajectory. Conditional on the block-start history, successful duration pattern and other signs, the remaining intercept is independent of that first sign. Its bound and the Gaussian noise give the advertised sub-Gaussian proxy. The count/deviation proof uses an exponential supermartingale and a lower-tail success-count bound, not Gaussianity conditional on a terminal random count. The union over lags does not require their independence.

The finite-section bias uses a deliberately non-sharp word-locality order, so its factorial estimate is conservative. The same form bounds survive a principal cut, and the geometric sum of response magnitudes is uniform in cut size. Thus the reduction to a logarithmic-size finite section at polynomial response tolerance is genuinely established. It also weakens any rhetorical argument that infinite latent dimension itself creates a barrier to response-level estimation.

### 3.6 Outer sets and the all-policy lower bound

The analytic enclosure theorem correctly separates the original statistical band, represented band, spatial tail, mesh and Taylor errors. Its full-box completion assertion and existential projected-prefix witness have the right quantifiers. The diameter conclusion, however, explicitly assumes the sampled-pulse grid; this is exactly the hypothesis missing from the executable predicate discussed next. [M6]

The two-way propagation argument uses the first possible generator words from the boundary to site `J` and back. Duhamel gives the claimed first influence order, and splitting propagation into a short factorial part and a stable long-time part gives exponential spatial invisibility. At a common history the policy kernels cancel, so the chronological KL bound is legitimate even for adaptive selected finite readout times. The two-point risk statement proves logarithmic depth order, not the sharp joint depth/accuracy frontier. [M7]

An elapsed-time minimax statement must retain a sampling-rate or positive-gap restriction. The attaining stage design has such a restriction. The larger all-policy class allowing arbitrary finite readout times does not, by itself, bound the number of independent noisy observations in a fixed elapsed interval. The final time-order sentence should explicitly attach to the positive-gap experiment, rather than suggest an unrestricted all-policy elapsed-time theorem.

## 4. R52-C1 — An unbound arithmetic predicate is not an end-to-end diameter certificate

**Locations:** `tools/round51_certificates.py`, lines 310–314 (`diameter_certified`), the preceding `outer_boxes` return value, and the sampled-grid hypothesis in Theorem `thm:outer`. [M6, M10]

The predicate checks only

\[
L(2\mathcal A\max_q r_q+\mathcal E)\le\delta.
\]

It receives no observable map. It cannot check the clock, lag coverage, coefficient weights, compatibility of the model box, or whether the radii describe the same responses used by the inverse certificate. The outer result does not itself attach a verified sampled-grid identity. The author's test even exercises the predicate with a single-element list when the certificate has many lags; that is a test of scalar arithmetic, not coverage of the theorem's observation hypothesis.

### 4.1 Exact counterexample to unrestricted composition

Take the author's own admissible example box:

\[
c\in[1,2],\quad a_k\in[1/2,1],\quad b_k\in[3,4],\quad T=1.
\]

Set `J=0`, `delta=1/8`, `t0=1/2048`, `rho=1/2`, `w=1/4096`. The unmodified code returns `N=60`, `m=61` and `L E<=1/16`. Now use a legal observable `0*h(1/100)` with reference/represented band `[0,0]` and zero representation error. Invoke `outer_boxes` with `K=1`, `r=1`, `P=2`, `max_boxes=1`.

All observables and their observable-error radii are zero. The one full box is retained, and its prefix is

```text
c: [1,2], b0: [3,4], a0: [1/2,1].
```

Its actual `d_0` diameter is 1. Nevertheless,

```python
c.diameter_certified(out['outer_radii'], cert, Fraction(1, 8))
```

returns `True`. No fake certificate dictionary, floating-point rounding, partial enumeration or out-of-box parameter is used.

### 4.2 The issue is not confined to a zero observable or a short list

Let `t=10^{-100}` and use the nonzero observable `h(t)`. Since `ell B=0`, the generator bound gives

\[
|h_\beta(t)|\le\frac{\Lambda e^{\Lambda t}t^2}{2}
\le\frac{27t^2}{2}
\]

throughout this box: `Lambda=9`, `Lambda*t<1`, and `e<3`. Thus the exact rational band with radius `27t^2/2` contains **every** parameter. All five budgets remain accounted for in `outer_boxes`.

Both a single such observation and **61 repetitions of the same observation** return the entire prefix box and then yield `True` from the predicate. The repeated case has the nominal required number of observations; a length check alone would not fix it. The independent script executes all three witnesses against the frozen, hash-verified module.

### 4.3 Required repair and exact scope

This does **not** disprove Theorem `thm:outer`: the counterexamples violate its explicit sampled-grid hypothesis. It disproves interpreting the current predicate, when composed with the general outer-set routine, as an unconditional certified diameter decision. As a conditional arithmetic helper it may remain, but it should be named and documented accordingly, for example `radius_budget_satisfied`.

A genuine end-to-end wrapper must bind the result to a validated observable map and model/certificate identity. It should verify canonicalized pulse coefficients and times for every required lag, permit mathematically equivalent treatment of the known value `h(0)=0`, and reject missing, duplicated, wrongly scaled or wrong-clock observations before returning a diameter-certification status. Model bounds, `J`, `N` and `Delta` must agree as well. Add negative tests for all three witnesses and positive tests with the actual complete pulse grid.

Exact rational arithmetic establishes the correctness of arithmetic on its inputs. It does not establish that those inputs satisfy the inverse theorem's hypotheses. This is a material distinction in a manuscript advertising executable outer certificates.

## 5. R52-M1 — The closest comparison needs a theorem-level input audit

The revision is right that the Gaussian-input pseudocode of Algorithm 1 in Sarkar–Rakhlin–Dahleh is not literally a uniformly bounded policy. But the same preprint's **Assumption 1** permits isotropic sub-Gaussian inputs, and its **Section 11** develops the error analysis under a general sub-Gaussian input condition. The journal's Assumption 1 has the same input scope. I checked the preprint text and the journal PDF, including the rendered assumption page. [L1, L2]

For a scalar Rademacher variable `S`,

\[
ES=0,\qquad ES^2=1,\qquad
\sup_{p\ge1}p^{-1/2}(E|S|^p)^{1/p}=1.
\]

Thus bounded Rademacher excitation satisfies that input condition; the physical amplitude can be incorporated into the input operator. The distinction between literal Gaussian pseudocode and the proof's broader input class must be made explicit. The current literature audit lists Assumption 1 among checked materials but does not explain this point. [M9, M12]

Here is the concrete comparison the authors should perform. In the regular-duration, zero-baseline subexperiment, sampling at the readout endpoints gives a discrete stable linear system with transition `U=exp(Delta A)` and pulse input operator `aHB`, up to an innocuous indexing convention. A finite section has the same structure. The manuscript itself proves uniform stability and a dimension-uniform response-norm bound. Therefore a response-level comparison cannot stop at “Gaussian Algorithm 1 is unbounded.”

This observation does **not** transplant the full comparator theorem unchanged. Its initial-state and process-noise assumptions, the finite-section constants, irregular duration mixtures, and block-dependent baselines still require attention. In particular, a full-posterior conclusion is not a corollary of a frequentist FIR error bound. The author should identify those actual residual steps, including which proof estimates survive bounded inputs and zero process noise, rather than treating the choice of Gaussian excitation in a displayed algorithm as the decisive theoretical incompatibility.

The literature comparison is improved relative to Round 49 but still incomplete in a way that bears directly on the claimed contribution. This is not an accusation that the authors falsely quoted Algorithm 1; their narrow literal statement is true. The omission is the broader input assumption and proof scope in the same work.

Goldenshluger's institutional abstract confirms a genuine nonparametric predecessor: FIR estimation for stable transfer functions with polynomial or exponential response decay, nonasymptotic accuracy bounds, lower bounds and adaptation. I did not retrieve its full theorem-level paper and do not claim it already proves the present theorem. [L3] The deterministic dynamic Jacobi inverse lineage is likewise real, but does not alone provide this noisy chronological theorem. [L4]

## 6. R52-M2 — The paper has not established exceptional significance

The revised end-to-end decomposition is useful precisely because it exposes how much is now a modular composition. The deterministic response-to-physical theorem is a minimum-residual triangle inequality followed by two inverse bounds. The bounded-sign estimator is a cross-correlation estimator with a bounded intercept and a success-count argument. The complete-posterior theorem adds deterministic entropy control, a Gaussian score martingale and a summable nuisance potential. The sampled-channel identity is effective, but its analytic mechanism is local functional calculus in a deliberately small norm ball.

These observations are not dismissals of technical work. They identify where the paper's significance must reside: the quality, breadth or sharpness of the uniform physical inverse and the resulting statistical synthesis. At present, the model is uniformly pinned and damped, has bounded nearest-neighbor coefficients with a positive edge lower bound, uses a selectable fast clock, and excludes within-block readout-dependent feedback. None of these assumptions is hidden. Together they substantially simplify both propagation and the nuisance problem.

The lower bound establishes the same **order** of depth, but not a matching region. The sufficient inequality is `C_b*r+p_b*s<1`; the two-point obstruction is `8*vartheta*r+2*s>1`. The manuscript appropriately does not identify them. On the standard example above, the printed sufficient constants are approximately `C_b=575.681` and `p_b=3.249912`; the limiting fixed-accuracy inner depth coefficient is about `0.001737`, while the corresponding outer obstruction coefficient is about `366.968`. These are evaluations of deliberately loose bounds, not measurements of a true minimax threshold.

Likewise, for `J=0`, `delta=1/8` in that example, the simple certificate has `log10(1/kappa)` approximately `235.849`. This does not prove that the experiment actually needs an astronomical sample: a tiny lower bound on information is not an upper bound on information. It shows that the explicit envelope is not currently a calibrated account of statistical difficulty. The article claims neither practical efficiency nor sharp constants, so this is an assessment of the strength of the contribution, not an allegation of a false theorem.

The most distinctive posterior robustness is also narrower than general model misspecification: the working initial-state law can be wrong because its entire effect becomes summably small. The physical dynamics remain correctly specified. A self-contained theorem extracting a broader new posterior principle, a substantially more informative optimality theory, or a demonstrated new inverse mechanism would change the significance assessment. Merely adding more finite tests or changing another geometric base would not settle it.

I have not located a publication proving exactly the full Round 51 theorem under exactly its hypotheses. Accordingly, I do not assert a priority counterexample or absence of all originality. My judgment is that the submission has not established the exceptional depth or breadth required by the requested journals. This is a judgment on the current submission, not a mathematical prohibition on the research program.

## 7. Two further deductions from the current proof

These deductions are offered as rigorous improvements, not as newly invented acceptance conditions or correctness objections.

### 7.1 R52-Q1: the exploration distribution may be atomless when `rho<1`

Fix any `rho<1` and choose a sufficiently short nonexploration duration `t0` and gap `t0`. Let the exploratory duration law be any probability on `(0,T]`, including an atomless one. Count only blocks in which every stage is nonexploratory. Their probability is

\[
(1-\rho)^m>0.
\]

On those blocks the sampled response grid is exactly the one used in the manuscript. The sign-energy proof, complete-likelihood argument and entropy/nuisance estimates therefore go through with `p_*=1-rho`. The same form of logarithmic-depth region follows after substituting that value in the constants.

Thus a positive atom in the **exploration law itself** is not needed when the design already inserts fast probes with positive probability. For `rho=1`, this argument supplies no successful blocks and does not remove the atom assumption. The current sufficient theorem remains true; this extension clarifies that the mechanism is recurring fast excitation, not a necessary atomic property of the exploration distribution.

### 7.2 R52-Q2: a stronger clock-dependent rational remainder

Put `x=Delta*Lambda<=1/64`. The elementary series estimate

\[
e^x-1\le\frac{x}{1-x}
\]

gives

\[
\|X\|\le\frac{x}{1-x},\qquad
\tau=\frac{2x}{1-x}\le\frac{2}{63}<\frac1{16}.
\]

Keep the author's coefficient estimate `|c_rk|<=6 Delta^{-R} 2^k` and `||H||<=Delta`. The difference of two tails is at most

\[
12\Delta^{1-R}\frac{\tau^{N+1}}{1-\tau}
=\Delta^{-R}\tau^N\frac{12\Delta\tau}{1-\tau}
\le\Delta^{-R}\tau^N,
\]

because `12 Delta tau/(1-tau)<=24 Delta/61<=1`. Hence the same transform and row-sum budget admit the sharper remainder

\[
\mathcal E_\tau=\Delta^{-R}\tau^N.
\]

At rational model/clock inputs, `tau` is rational. Choosing `N` using `log(1/tau)` instead of `log(16)` preserves the proof structure and yields the sufficient error exponent

\[
p_b(\tau)=2+\frac{\log(1/p_*)+\log16}{\log(1/\tau)},
\]

with the corresponding depth constant obtained by the same ceiling accounting. Even the universal `tau=2/63` gives approximately `2.803652` when `p_*=1`, rather than 3.

Across designs allowing successively smaller fast durations while retaining positive success mass, this exponent tends to 2. The depth constant also changes, and can worsen as the clock shrinks; this is not a proof of the sharp joint frontier at fixed positive depth coefficient. It does show that the displayed accuracy exponent contains avoidable clock-estimate losses. The current `16^{-N}` result is valid but not an intrinsic rate barrier.

## 8. Disposition of the previous report and requirements for a response

| Round 50 item | Round 52 disposition |
|---|---|
| R50-M1: current executable source unavailable | Resolved for the new implementation and its test suite; both were retrieved, blob-verified and executed. The historical missing Round 49 programs are not retroactively recovered. |
| R50-Q1: enlarged event and all-sign energy | Resolved in the theorem and weighted certificate, not merely in the response prose. |
| R50-Q2: single-atom formulation | Resolved; Section 7.1 above gives a further optional extension. |
| R50-M2: finite-response comparison and contribution | Substantially improved by the explicit reduction, estimator and uniform cut bound; still incomplete for the reasons in Sections 5–6. |
| R50-E1: standalone exposition | Substantially improved. The active root has a coherent dependency order and does not use old publication receipts as proof premises. |

A response should first close the observable-map certification contract and add adversarial regression tests. It should then correct and complete the sub-Gaussian-input comparison, separating literal algorithm compatibility from applicability of the proof. Finally, it should address the central contribution judgment with a precise theorem-level significance argument, rather than citing the number of revision rounds or passing tests.

The two refinements in Section 7 can strengthen the statement and constants; they are not a demand to abandon the current positive result. The hypotheses limiting the clock, feedback, nuisance and elapsed-time interpretation must remain explicit.

**Final recommendation:** reject at the requested four-journal standard. The central logarithmic-depth result survives this examination under its stated assumptions; the unbound executable diameter interface does not yet support unconditional certification, and the exceptional-significance case remains unpersuasive. No journal acceptance, formal proof certification or universal impossibility conclusion is implied.

---

## Source map and reproducibility

All manuscript links below are pinned to the reviewed commit. The theorem labels in the report refer to those sources, not a moving branch.

- [M0: active root](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/ROUND51_REVISION.tex) and [introduction](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/introduction.tex).
- [M1: model and inverse](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/model_inverse.tex).
- [M2: sampled generator](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/sampled_generator.tex).
- [M3: likelihood](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/likelihood.tex).
- [M4: blocks](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/blocks.tex).
- [M5: response transfer](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/response_transfer.tex).
- [M6: enclosures](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/enclosures.tex).
- [M7: optimality](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/optimality.tex).
- [M8: references](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/references.tex).
- [M9: author response](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/AUTHOR_RESPONSE_ROUND50.md).
- [M10: implementation](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/tools/round51_certificates.py), [tests](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/tests/test_round51.py), and [verifier](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/tools/verify_round51.py).
- [M11: review index](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/ROUND51_REVIEW_INDEX.md) and [controlling Round 50 report](https://github.com/TrillionniumFoundation/theta-theory/blob/a7b9ffcfd79d2f8cd5179238db9124486c1d9f0a/REFEREE_REPORT_ROUND50_GPT6_PRO_HARSH.md).
- [M12: current literature audit](https://github.com/TrillionniumFoundation/theta-theory/blob/f991a17a5d99bf0cce9f1e457df91097e69dcd8a/round51/LITERATURE_AUDIT.md).
- [L1: Sarkar–Rakhlin–Dahleh, arXiv:1902.01848v6](https://arxiv.org/html/1902.01848v6), Assumption 1, Algorithm 1, Theorem 5.1, Proposition 5.1, Corollary 5.1 and Section 11. The input assumption/proof comparison, not a complete re-proof of that article, was checked.
- [L2: Sarkar–Rakhlin–Dahleh, JMLR 22(26), 2021](https://jmlr.org/papers/volume22/19-725/19-725.pdf), printed page 8, Assumption 1; rendered page inspected.
- [L3: Goldenshluger, 1998, institutional publication record and abstract](https://cris.haifa.ac.il/en/publications/nonparametric-estimation-of-transfer-functions-rates-of-convergen/), DOI 10.1109/18.661510. No full theorem-level access claimed.
- [L4: Mikhaylov–Mikhaylov, 2019, publisher record](https://www.aimsciences.org/article/doi/10.3934/ipi.2019021?viewType=HTML), DOI 10.3934/ipi.2019021. Used for the deterministic inverse lineage, not a claimed subsumption of this paper.

From this review branch, the two executed finite suites can be rerun with:

```sh
python tests/test_round51.py --json-out reviews/round52/AUTHOR_TEST_REPLICATION.json
python reviews/round52/independent_checks.py
```

The second command intentionally asserts that the frozen interface witnesses are reproducible. A future repaired implementation should not be substituted silently: the script checks the reviewed source blobs before running. The receipts record finite executions only; all infinite-dimensional and asymptotic judgments in this report rest on the written mathematical arguments and their stated scope.
