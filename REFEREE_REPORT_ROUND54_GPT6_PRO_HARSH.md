# Round 54 — Harsh referee report on the frozen Round 53 revision

## Recommendation: Reject at the requested Annals–Inventiones–JAMS–Acta standard

**Manuscript:** *Boundary Identification from Recurring Fast Probes: Energy-Robust Posteriors and Bound Observable Certificates*  
**Author named in the manuscript:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Reviewed revision branch:** `revision/round53-bound-certificates-energy-robust-posterior-2026-09-05`  
**Frozen reviewed commit:** `7f1bc9a42ba27615aea61afb9a417ef076e2c6e1`  
**Frozen reviewed tree:** `5758267cbe13a276f5c12026a535117b4e17960b`  
**Controlling Round 52 review HEAD / revision parent:** `8e3e6f663fde9942384298eb9c60cf217a926bac`  
**New review branch:** `review/round54-gpt6pro-harsh-round53-2026-09-05`  
**Date:** 5 September 2026  
**Reviewer:** GPT-6 Pro, at the repository user's request.

This is an independently reasoned, AI-generated referee-style assessment. It is not a journal appointment, commissioned external report, or editorial decision of any named journal. The recommendation is the reviewer's assessment of this submission at the requested standard. It is not an assertion that the research program is impossible.

## 中文结论

**本报告按用户指定的数学四大刊标准建议拒稿，但不宣称已经推翻当前的对数深度恢复主定理。** 主文、两个继承证明文件及当前实现经过审查后，本轮没有找到已证实足以否定核心收缩结论的致命数学错误。Round 53 的累计平方能量扰动定理确实超出了上一轮仅处理指数衰减初始态的范围；这一进展应予承认。

本轮发现并实际复现了新的认证缺口。`validate_certificate` 用数值相等来代替精确类型校验：将证书中的有理数 `A` 换成数值完全相等的 `float(A)`，仍能通过重算校验，随后完整的 `certify_outer` 会进入浮点计算。对于同一完整观测网格、同一组有理数区间和同一非空枚举集合，精确证书返回 `enclosed`，浮点版本却返回 `certified`，尽管精确的充分界严格超过目标 `1/8`。这里没有修改作者程序、伪造返回对象或绕过入口。

**这个反例的边界必须说清楚：它证明“精确预算判据被错误接受”，不证明实际保留集合的物理直径超过目标。** 所用正向接口夹具的真实前缀直径为 `2/10^180`，小于 `1/8`。因此这不是解析外包定理或主收缩定理的反例，而是本轮声称已绑定的精确认证接口仍存在的实际缺陷。

报告还给出一条新的、带有限样本常数的比较命题：同一个互相关响应估计器，在允许与符号相关的可预测扰动时，用 Cauchy–Schwarz 控制偏差，同样达到主文印出的累计能量容忍区域及多项式扰动区域。无偏性并非必要。该结论不替代完整后验收缩，但说明新增能量容忍指数不能被当作后验方法独有的显著突破。

作者新增的 **44 项测试已在 Git blob 校验后独立重跑，全部通过**；另有 **170 项独立有限检查**通过，并复现上述两种错误接受路径。“检查通过”在此包含“缺陷成功复现”，不表示实现已经被证明正确。本报告没有把作者的 110 项总测试记录或三遍 LaTeX 构建记录冒充为审稿人的实际执行。

---

## 1. Decision and classification

Round 53 is a substantive revision. The previous observable-grid witnesses are rejected by the new entry point, the exploration hypothesis is broader, the actual-clock remainder is used consistently, and the complete posterior is extended to a genuinely larger discrepancy class. I withdraw the corresponding superseded objections rather than reproducing them under new labels.

Nevertheless, I recommend rejection at the requested four-journal standard. There is a new, reproducible failure of the advertised exact certification contract. Separately, the manuscript still has not made a persuasive case for exceptional mathematical significance. The latter judgment is not inferred from a programming defect: repairing that defect would leave the contribution assessment to be addressed on its own merits.

| ID | Finding | Classification and consequence |
|---|---|---|
| R54-C1 | Numerically equal floating certificate fields pass recomputation validation and cause an over-budget instance to be accepted by the unmodified certifying endpoint | Major runtime exact-arithmetic contract defect; not a counterexample to the analytic theorem or to actual set diameter |
| R54-M1 | The manuscript's own response estimator admits the same printed cumulative-energy region by a direct, bias-aware argument | Missing natural contribution comparison; a new referee deduction, not a contradiction of a printed theorem |
| R54-M2 | The enlarged posterior theorem remains a relatively direct perturbation of the existing proof, while quantitative optimality and theorem-level positioning remain insufficient for the requested exceptional threshold | Principal editorial objection; not a claim that the complete theorem already exists in the literature |
| R54-Q1 | The current sufficient constants remain very far from the lower-bound constants | Quantitative context, not an incorrect bound, actual sample lower bound, or newly imposed requirement of sharp constants |

The core conditional mathematical claims survive this examination, subject to the usual limitations of an unaided written-proof audit. That is different from formal verification, a finding of complete correctness, or a positive editorial recommendation.

## 2. Frozen scope, source identity and actual execution

The review targets the single active Round 53 article, not every historical paper stored in the repository. I read the complete 791-line root `ROUND53_REVISION.tex`, both explicitly included mathematical sources `round51/model_inverse.tex` and `round51/likelihood.tex`, the itemized response to Round 52, the review index, the current source manifest and literature audit, the active implementation, its inherited implementation dependency, the new test suite, the verifier source, and the controlling report's substantive findings and requests. The report's theorem references use source labels to avoid ambiguity between generated numbering and source files. [M0–M8]

The revision is one commit ahead of the controlling review, with that review as its parent. This review branch starts at the exact frozen revision commit. The review adds only its own report, independent program and execution receipts; it does not rewrite historical reports, author sources, or `main`.

The executable files used locally were checked against the Git blob identities returned by the connector before execution:

| File | Verified Git blob | SHA256 of executed bytes |
|---|---|---|
| `tools/round51_certificates.py` | `6eda73359c1999027394062f2edb1532e0bed21f` | `c7284fb651146181c8e6264a11579b76b08864102e9dda6b84878f2e171a3001` |
| `tools/round53_certificates.py` | `6a80f4fb264ab29958ebc3f6ea1ab5c2a06e62fb` | `24b7010cbebe84aa8d371d80370d67049f8c6a6f75488ae9f72e34ebcafc1d28` |
| `tests/test_round53.py` | `5fd6b0f474eec22b9a6a3be589ff9dd3f3aeef83` | `b27ae0154ee8d45de9caee80ee410284e2b24638ff3a0f151515356e9cbc6048` |

The actual author-suite execution used Python 3.13.5: **44 tests, zero failures, zero errors, zero skips**. Its receipt is [AUTHOR_ROUND53_TEST_REPLICATION.json](reviews/round54/AUTHOR_ROUND53_TEST_REPLICATION.json).

The independent program performs **170 finite assertions** in ten groups: source identity (3), actual-clock inequalities (64), all-sign energy (5), first affected jets (8), moment reconstruction (12), energy-transfer arithmetic (20), robust response bounds (11), arithmetic-predicate witness (4), endpoint-band coverage (36), and full-endpoint witness (7). Its actual receipt is [INDEPENDENT_CHECKS.json](reviews/round54/INDEPENDENT_CHECKS.json). Assertion counts are bookkeeping, not a measure of mathematical proof strength.

**Not independently executed:** the inherited 66-test Round 51 suite, the complete 12-source manifest verifier, the three-pass TeX build, a PDF rendering, posterior simulations, or a proof assistant. The author reports 110 total tests and a 14-page build; those remain author receipts, not this referee's executions. Reading the TeX source and verifier is not equivalent to executing or visually checking a PDF build.

External comparison was targeted, not exhaustive. I checked the primary LTI preprint's input assumptions and the 2026 posterior paper's observation model and principal contraction statements. I did not independently re-prove those external papers. No complete priority search is claimed. [L1–L2]

## 3. Disposition of the controlling Round 52 report

| Round 52 item | Round 54 disposition |
|---|---|
| C1: unbound observable-map predicate | The original defect is repaired at the new endpoint: the complete canonical pulse grid, model identity, band ordering and enumeration are bound. The old witnesses are rejected. The distinct exact-type defect in Section 5 remains. |
| M1: Gaussian pseudocode versus sub-Gaussian analysis | Corrected in Section 7.1 of the article. The new discussion no longer treats bounded signs as a theoretical exclusion from the comparator's input class. |
| M2: exceptional significance | The new energy theorem is a real strengthening, but the comparative and editorial issue is not resolved; see Sections 6–7 below. |
| Q1: atomless exploration when nonexploration recurs | Incorporated into the principal theorem through `p=1-rho+rho*w>0`, including `w=0` when `rho<1` and the case `rho=0`. |
| Q2: actual-clock remainder | Incorporated into the proof, constants and executable constructor; the standard example changes from `N=60` to `N=41`. |
| Elapsed-time scope | Correctly made conditional on a positive sampling gap for comparison policies. The unrestricted theorem is explicitly in readout count. |

These are substantive closures, not merely changes of terminology. In particular, the current report does not repeat the old zero-observable example as though the new entry point accepted it. The independent failure below uses the correct complete grid and a nonempty exhaustive outer set.

## 4. Audit of the core mathematical chain

### 4.1 Stability, response geometry and the labeled inverse

The pinned coefficient box gives a uniform positive form bound on the Jacobi operator. Differentiating the displayed cross-term energy cancels the mixed damping term and yields the stated common exponential stability envelope. The upper and lower comparisons of that energy with the state norm are compatible with the given choices of constants. Principal finite cuts retain the necessary form bounds. [M1]

The continuity assertion is based on strong operator convergence from coordinate convergence, not on an unjustified claim of operator-norm compactness. Uniformly bounded generators give convergence on finite time intervals, and the common stable tail gives continuity of the boundary response in `L1`. Product compactness then supplies compact response geometry.

The damped moment identity has the correct derivative indexing. The Gram inverse representation, monic-polynomial norm bounds, positive edge lower bound, and secant estimates support the exponential-in-depth constant `L=Q^(25(J+1))`. I did not find a hidden quadratic-in-depth loss in the assembled exponents. The finite checks reproduce the moment identity and labeled coefficients for several depths; they also verify that changing `b_J` first changes the step-response jet at order `4J+4`, and changing `a_J` first does so at `4J+6`. These checks supplement, rather than replace, the written uniform-in-tail argument.

### 4.2 The pulse channel and actual-clock inversion

The corrected transform genuinely compensates for the integrated input channel. With `U=exp(Delta*A_beta)`, `X=U-I`, and `H=int_0^(Delta/2) exp(u*A_beta)du`, the scalar identity gives

\[
F_r(X)H=A_\beta^{r-1},\qquad
F_r(z)=\Delta^{-r}[\log(1+z)]^{r-1}
\frac{\log(1+z)}{z}(\sqrt{1+z}+1).
\]

The small common norm ball justifies the chosen analytic branches and removable quotient. Expanding `(U-I)^k` yields a parameter-independent finite transform. The actual-clock ratio

\[
\tau=\frac{2\Delta\Lambda}{1-\Delta\Lambda}\le\frac2{63}
\]

and the prefactor inequality `12*Delta*tau/(1-tau)<=1` justify the pairwise remainder `E=Delta^(-R)*tau^N`. The weighted norm `W` is the correct dual squared norm for the block multiplicities. Its positivity and the bound `W<=A^2` are valid. [M0, labels `lem:sampled`, `prop:envelope`]

The resource constants account for the entire successful-block probability `p^m`, not just the probability of one short probe. Smaller clock choices may improve the accuracy exponent while worsening the depth constant; the article correctly refrains from identifying this sufficient tradeoff with a sharp frontier.

### 4.3 Chronology, complete likelihood and block information

The likelihood compares candidates at a common realized history. Parameter-independent action kernels cancel in that chronological comparison; the proof does not condition on the final adaptive design as if it were fixed. The contrast is predictable before each fresh Gaussian noise. Deterministic response-metric covers control contrast differences uniformly over histories. The grouped-square argument uses bounded nonnegative increments and their conditional means, not independence of the groups. [M2]

On a successful fast block, within-block commitment makes the intercept independent of all current block signs. Sign orthogonality then yields the exact weighted energy identity. Multiplication by `p^m` is justified by the exogenous durations, and unsuccessful patterns contribute nonnegative conditional energy. An additive predictable observation discrepancy may affect later block commitments, but does not change this algebra at a fixed block-start history. [M0, label `lem:block-floor`]

This is why the stronger discrepancy model does not invalidate the information floor. It is also why the argument does not prove the same assertion for arbitrary readout-dependent feedback within the block. The manuscript states the restriction; it is not a concealed defect.

### 4.4 The new cumulative-energy posterior theorem

Theorem `thm:energy` is a genuine extension, and its displayed finite constants are consistent. Completing Gaussian squares introduces the additional term `sum d_i*f_i`. The deterministic inequality

\[
\left|\sum_i d_if_i\right|\le A_n/16+4D
\]

is enough to control it. The working initial-state integral is bounded uniformly before integration. Cauchy–Schwarz gives its new cross term `sqrt(R2*D)`, so the law integrated by the working likelihood still need not charge the true initial state. [M0, Section 5]

On the simultaneous score and square event, the upper numerator coefficient on the separated set is `-41/256`, and the lower denominator coefficient on the radius-`sqrt(q)/4` prior ball is `-7/128`. Their difference is `-27/256`. Consequently the stated posterior exponent

\[
\mathcal P(\sqrt q/4)-\frac{27nq}{256\sigma^2}
 +\frac{8D}{\sigma^2}+2B_{n,D}
\]

follows with the declared nuisance envelope. The special budgets give

\[
-27/256+8/1024+2/64=-17/256\le-1/16.
\]

The weighted Gaussian-modulus bound used for `B_(n,D)` does not require a false independence assertion about adaptive contrasts. The relevant noise variables remain fresh in the filtration.

At logarithmic depth, `n'q` has a polynomial margin over the covering and prior costs, while the grouped-square exponent loses only another logarithmic factor. Thus the condition `D_n=o(n^(1-gamma)/log n)` is sufficient for the printed region. The polynomial-discrepancy corollary correctly allows nonsummable squared-energy envelopes when `0<alpha<=1/2` and `gamma<2*alpha`. The conclusion is not restricted to an exponentially dying initial response.

These are positive findings. They do not establish that the perturbation argument is a deep new general posterior principle. Section 6 explains a relevant comparison that the response has not made.

### 4.5 Response transfer, outer enclosures and the lower bound

The finite response-net estimator uses the correct minimum-residual triangle inequality and deterministic tie-breaking. The nonreset sign estimator's noise bound is chronological; it does not assume Gaussianity conditional on the final random success count. The finite-section locality estimate is conservative, and common stability makes its response bound uniform in cut dimension. [M0, Section 7]

The analytic outer theorem has the right quantifiers. A retained projected prefix has a full-box witness; the completion claim concerns that full box, not arbitrary tails attached to the projected prefix. Statistical, representation, spatial, mesh and Taylor errors are separately charged. The diameter implication requires the complete pulse grid and a valid exact budget. The new grid validation closes the old missing hypothesis; Section 5 identifies a different runtime failure. [M0, Section 8]

The all-policy lower bound uses two-way propagation, a rank-one diagonal perturbation, an `L1` response bound, and the chronological Gaussian KL chain rule. The selected readout times do not defeat the argument because the mean difference is bounded uniformly in time at a common history. The positive-gap elapsed-time corollary now correctly charges the number of readouts. The lower bound establishes the logarithmic order at fixed accuracy, not the sharp joint depth/error region. [M0, Section 9]

## 5. R54-C1 — Recomputed numerical equality does not enforce exact arithmetic

### 5.1 The precise entry-point defect

**Locations:** `tools/round53_certificates.py`, lines 55–68 (`PulseCertificate`), 103–108 (`validate_certificate`), and 194–209 (`certify_outer`). The arithmetic-only helper is at lines 142–149. [M4]

The certificate dataclass is frozen but has no runtime field-type validation. Its validator recomputes a canonical certificate and compares the supplied and recomputed objects using dataclass equality. Equality of numerical values is weaker than equality of exact representations: a binary floating-point power of two compares equal to the corresponding `Fraction`.

The certifying endpoint then continues to calculate with the **supplied** certificate, rather than the recomputed canonical one. A floating `A` therefore passes validation and silently changes the final budget calculation to floating arithmetic. The stated float-rejection and exact-rational contract is not enforced at this input boundary.

This is not an attack on an already returned object. The witnesses call the unchanged public certifying function and let that function construct its own result. No monkey-patching, mutation of frozen fields, subclass trick, or external outer-set substitution is used. The only noncanonical input is an ordinary `PulseCertificate` made with `dataclasses.replace`.

The analytic theorem assumes exact rational data, so it is not contradicted by a noncanonical input. The defect is that the advertised runtime validator accepts that input and emits a successful certificate without maintaining the promised arithmetic domain. Type annotations alone do not implement the rejection claim.

### 5.2 An exact-threshold witness for the arithmetic helper

Use the standard example

\[
[c_-,c_+]=[1,2],\quad [a_-,a_+]=[1/2,1],\quad
[b_-,b_+]=[3,4],\quad T=1,
\]

with `J=0`, `delta=1/8`, `t0=1/2048`, `rho=1/2`, and `w=1/4096`. The exact certificate has `N=41`, `m=42`, and `A=2^165`.

```python
cert = c.certificate(spec)
mixed = dataclasses.replace(cert, A=float(cert.A))
c.validate_certificate(mixed)  # succeeds
```

Let

\[
r_* = \frac{\delta/L-\mathcal E}{2\mathcal A},\qquad
r=r_*(1+10^{-16}).
\]

All radii supplied to the helper are the exact rational `r`. Algebraically,

\[
L(2\mathcal A r+\mathcal E)
=\delta+(\delta-L\mathcal E)10^{-16}>\delta.
\]

The strict inequality follows from `L*E<=delta/2`. Nevertheless, the actual floating calculation rounds to `0.125`. The exact certificate returns `False` from `radius_budget_satisfied`; the numerically equal mixed-type certificate returns `True`. This is a strict exact-threshold crossing, not merely the observation that some intermediate quantity has a different type.

### 5.3 The same defect reaches the full certifying endpoint

It would be insufficient to attack only the explicitly conditional arithmetic helper. The independent program therefore constructs the complete pulse grid and calls `certify_outer` twice on identical data.

Use the author's positive-fixture scale `h=10^(-180)` and the admissible narrow box

\[
c\in[1-h,1+h],\quad a_k\in[1/2-h,1/2+h],\quad
b_k\in[3-h,3+h],\quad T=1.
\]

Keep the other specification values above. For this different box the exact certificate has `N=35`, `m=36`, and `A=2^153`. Take spatial depth and Taylor order `K=P=80`, mesh radius `h`, and `max_boxes=1`. There is one full box, not a partial enumeration.

Compute each exact Taylor center `H_q` and its declared deterministic error `E_q` using the frozen implementation. Define `r_*` and `r` as above using this box's certificate, and set

\[
R_q=r-2E_q,\qquad
I_q=I_q^{\rm rat}=[H_q-R_q,H_q+R_q],\qquad \epsilon_q=0.
\]

The program checks `R_q>E_q>0` for all 36 rows. Thus the bands cover the narrow full box under the same deterministic enclosure argument; the outer radii are exactly `r`. The grid, model, bands, resource cap and full-box witnesses agree in both executions. Only the type of the otherwise equal field `A` changes.

The actual outputs are:

| Property | Canonical exact certificate | Numerically equal certificate with floating `A` |
|---|---|---|
| Validator outcome | Accepted | Accepted |
| Complete enumeration | Yes, one box | Yes, one box |
| Retained full boxes | One | The identical box |
| Exact sufficient bound | Strictly greater than `1/8` | The same mathematical bound |
| Returned bound type | `Fraction` | `float` |
| Returned numerical bound | Strictly greater than `1/8` | `0.125` |
| Returned status | `enclosed` | `certified` |

**Limitation of the witness:** the actual prefix diameter is `2/10^180`, which is below `1/8`. The witness does not prove an incorrect physical recovery set. It proves that the specified exact sufficient-budget decision is wrong and that the public endpoint can return a non-exact bound while purporting to enforce an exact-rational contract. The report does not infer a larger mathematical counterexample from this evidence.

### 5.4 Why the existing tests miss it, and the required repair

The field-modification tests in `tests/test_round53.py`, lines 217–224, replace values by `value+1`. That checks value mismatch, not a numerically equal change of arithmetic representation. The positive fixture, lines 149–172, uses only canonical certificates. Both sets of tests can pass while this failure remains, as the independent execution confirms. [M5]

The repair should make exact arithmetic an invariant of the validated computation. One sound approach is strict field validation: genuine integer orders, no booleans, and canonical rational derived fields with a clearly specified input policy. Another is to have validation return the recomputed canonical certificate and use **only that object** in all subsequent calculations and in the returned provenance, rejecting noncanonical input when the documented interface promises rejection. Merely adding another value-equality comparison is not a repair.

Add regression tests for numerically equal floating fields, for an exact bound immediately above the threshold, and for the complete endpoint with matching nonempty grids. Assert that returned budget quantities remain exact. A disclaimer about authenticity of arbitrary user-created output objects does not address an output produced by the unmodified advertised entry point after its own validation.

This defect is fixable. Its correction should not require weakening the mathematical result. Conversely, it should not be reported as already fixed merely because the previous 44 tests still pass.

## 6. R54-M1 — The same printed energy region holds for the elementary response estimator

### 6.1 What the manuscript does and does not claim

The revision correctly avoids claiming that its sign estimator is unbiased under arbitrary sign-correlated discrepancies. It does **not** state a theorem that robust frequentist estimation is impossible. I do not attribute such a claim to it.

The missing comparison is different: unbiasedness is unnecessary. The very same estimator admits a deterministic bias bound that, after the manuscript's own inverse, gives the same conservative energy-tolerance region printed for the posterior. This is particularly relevant because the new discrepancy class is the principal mathematical response to the previous significance objection. [M0, labels `thm:main-drift`, `thm:response-estimator`; M3]

### 6.2 Referee proposition: finite response bound with predictable drift

Retain the experiment, committed blocks, bounded physical initial state and Gaussian noise assumptions of the response-estimator theorem. Add arbitrary predictable readout errors `d_i` with pathwise cumulative squared energy at most `D`. Alternatively, use zero external initial state and include its entire response in `d_i`.

Write `pi=p^m`, let `B` be the number of completed blocks, and let `M_B` count successful blocks. For `M_B>0`, use exactly the manuscript's estimator

\[
\widehat b_k=\frac1{aM_B}\sum_{b\le B:E_b}S_{b,0}Y_{b,k}.
\]

With the manuscript's `v_*`, for every `e>0`,

\[
\begin{split}
\mathbb P\bigg\{M_B<B\pi/2\ \text{or}\
\|\widehat{\mathbf b}-\mathbf b_N(\beta_0)\|_\infty
>e+\sqrt{\frac{2D}{a^2B\pi}}\bigg\}
\le e^{-B\pi/8}+2m\exp\left\{-\frac{a^2e^2B\pi}{4v_*}\right\}.
\tag{R54.1}
\end{split}
\]

**Proof.** Subtract the actual discrepancy from each readout only for the purpose of the proof. The physical response and Gaussian noise along the realized input still satisfy the same block sign-martingale estimate. Contaminated earlier histories may change the next committed baseline, but conditional on that history the baseline is fixed, the current signs are fresh, and the physical intercept has the same deterministic bound. Thus the manuscript's stochastic deviation and count estimates apply to this drift-subtracted score under the actual experiment; no comparison of two different feedback histories is needed.

For each lag, the remaining drift contribution satisfies, pathwise,

\[
\left|\frac1{aM_B}\sum_{b:E_b}S_{b,0}d_{b,k}\right|
\le\frac1a\sqrt{\frac{\sum_{b:E_b}d_{b,k}^2}{M_B}}
\le\frac1a\sqrt{\frac D{M_B}}.
\]

On `M_B>=B*pi/2` this is the additional term in (R54.1). A union bound over lags proves the result. The selected sums need not be independent, the discrepancy need not be centered, and no conditional Gaussian law at the final success count is asserted. QED.

The Cauchy–Schwarz cost is not purely an artifact of allowing an unrealistically independent error. For example, at the final lag of a block take `d_(b,N)=c*S_(b,0)*1_(E_b)` and other discrepancies zero. Success and the first sign are known before that final readout, so the error is predictable. The resulting drift bias is `c/a` whenever successes occur, and the selected energy is `c^2*M_B`; the displayed Cauchy–Schwarz bound is attained. A deterministic envelope is `c^2*B`.

### 6.3 Explicit physical transfer and the printed asymptotic region

Use the simpler, unweighted certificate, and define its finite information quantity

\[
\mathcal I=n'q
=\frac{a^2B\pi\delta^2}{4L^2\mathcal A^2},\qquad n'=Bm.
\]

Choose stochastic tolerance and response-net mesh

\[
e=\eta=\frac{\delta}{12L\mathcal A},
\]

and retain `L*E<=delta/2`. Apply the manuscript's response-to-physical transfer to (R54.1). On its success event,

\[
\begin{split}
d_J(\widehat\beta,\beta_0)
&\le L\left\{\mathcal A\left(2e+\eta+
2\sqrt{\frac{2D}{a^2B\pi}}\right)+\mathcal E\right\}\\
&\le\frac{3\delta}{4}+\delta\sqrt{\frac{2D}{\mathcal I}}.
\tag{R54.2}
\end{split}
\]

In particular, `D<=I/32` suffices for physical error at most `delta`, with failure at most

\[
e^{-B\pi/8}+2m\exp\{-\mathcal I/(144v_*)\}.
\tag{R54.3}
\]

Under the article's printed sufficient region `gamma=C_tau*r+p_tau*s<1`, the information `I` is bounded below by a constant times `n^(1-gamma)/log n`. Consequently

\[
D_n=o(n^{1-\gamma}/\log n)
\]

also suffices for this frequentist estimator. Discrepancies bounded by `C*i^(-alpha)` give the same strict condition `gamma<min(1,2*alpha)` after the same energy summation. A bounded initial-state response can either stay in the physical intercept or be charged to the finite-energy envelope.

This proves equality of the **printed conservative asymptotic regions**, not equality of every finite bound. In particular, it does not claim to match a better finite certificate obtained from `W` in place of `A^2`.

### 6.4 Consequence for the contribution assessment

The complete posterior theorem remains more than a point-estimation theorem: it uses all completed readouts and controls mass for the working nonlinear posterior with an integrated nuisance law. A robust estimator does not imply those assertions. Nothing in (R54.1)–(R54.3) proves Bayesian uncertainty calibration either.

Nevertheless, the energy tolerance and the nonsummable polynomial examples are not, by themselves, posterior-specific phenomena in this experiment. They already follow from the existing response estimator, one pathwise Cauchy–Schwarz inequality, and the existing inverse. The manuscript should present this comparison or identify an error in the explicit derivation, rather than treating potential sign-correlated bias as a reason to stop the comparison at the correctly specified estimator.

This is a constructive comparative result, not a demand to abandon the positive logarithmic-depth theorem. Its purpose is to identify more accurately what remains distinctive about the posterior result.

## 7. R54-M2 — Exceptional significance remains unestablished

### 7.1 The improvement is real; the new mechanism is limited

The Round 52 report specifically invited a broader posterior principle as one possible way to strengthen the submission. Round 53 takes that direction and genuinely enlarges the discrepancy class. I credit that response. It would be unfair to continue describing the current theorem as covering only exponentially transient initial-state uncertainty.

What has changed in the proof, however, is chiefly an additional contrast cross term and its control by Young's inequality, plus the corresponding nuisance cross term. The deterministic covers, grouped information, score martingale, prior-ball denominator, and physical inverse are inherited. The standalone formulation is useful, but isolating a portable lemma does not automatically make its mechanism a substantial new principle.

The distinctive content must therefore lie in the strength and reach of the quantitative physical inverse, the chronological synthesis, or a genuinely informative optimality theory. At present the model remains uniformly pinned and damped, edges stay bounded away from zero, the clock is selected inside a small analytic norm ball, and within-block feedback is excluded. These assumptions are not hidden and are not errors. They are relevant to the breadth of the contribution.

I have not found a publication that proves the full present theorem under exactly its hypotheses. I therefore make no priority counterexample, plagiarism allegation, or claim of zero originality. The narrower editorial judgment is that the submission has not demonstrated the exceptional mathematical depth or breadth needed for a positive recommendation at the requested standard.

### 7.2 The LTI comparison is corrected, but cannot carry the novelty argument

Sarkar–Rakhlin–Dahleh's primary preprint allows isotropic sub-Gaussian inputs in Assumption 1, while also making explicit initial-state and noise assumptions. A Rademacher input meets the input condition. Round 53 now correctly distinguishes that scope from the Gaussian pseudocode. [L1]

The article's regular-duration recurrence and finite-section bounds identify a real response-level comparison. They do not automatically transfer an entire external theorem to irregular durations, block feedback, labeled infinite-chain coefficients or the complete working posterior. Those residual tasks are appropriately distinguished. The corrected comparison should be retained, not undone to manufacture an artificial obstruction.

For the new robustness issue, the most direct comparator is now internal: Section 6 proves a robust response front end for the exact experiment under discussion. It avoids claiming applicability of an external FIR theorem without checking all its assumptions.

### 7.3 The new posterior reference deserves a precise, limited comparison

Seizilles–Siebel's primary text uses independent random-design Gaussian regression, proxy variances and a proxy forward map, with rescaled Gaussian priors. Theorem 3.12 gives surrogate-posterior contraction under quantitative misspecification conditions; Theorem 3.17 transfers it through an inverse modulus. Corollary 3.15 explicitly connects slower approximation to slower contraction, and Appendix B develops related M-estimation tools. These statements are more relevant than an abstract-only acknowledgment. [L2]

They do not directly subsume the present predictable block design, product coefficient priors, or integrated transient law. Those differences prevent an automatic theorem transplant; they do not establish exceptional novelty by themselves. A useful comparison should identify the exact hypothesis or proof step needed to pass from one setting to the other. My inspection is of the observation model and named statements, not an independent verification of that entire paper.

### 7.4 R54-Q1: current constants and the actual strength of the optimality claim

For the standard box and clock in Section 5.2, direct numerical evaluation of the current formulas gives approximately

\[
C_\tau=512.009405,\qquad p_\tau=2.859439,
\]

with sufficient fixed-accuracy intercept `1/C_tau=0.001953089`. The intercept from the displayed lower-bound obstruction is `1/(8*vartheta)=366.968047`. At `J=0`, `delta=1/8`, the simple certificate has

\[
\log_{10}(1/\kappa)\approx207.253571.
\]

These are descriptive floating evaluations of the article's formulas, recorded separately from the exact checks. They are not certified numerical estimates of a minimax threshold. In particular, a tiny proved information floor is **not** proof that the experiment actually requires its reciprocal number of observations.

The article honestly claims order matching rather than a sharp joint frontier. I do not turn its non-sharp constants into a false-theorem objection. They do show why the existing lower bound adds less quantitative substance than a matching rate region would: the sufficient inequality and the obstruction leave a very large unresolved region. Improving another conservative base or reporting more regression tests would not, by itself, resolve the editorial significance issue.

## 8. Requirements for a technically credible response

A response should address the new evidence without reopening settled matters.

**Exact certification.** Repair the representation/type boundary or replace caller-supplied derived fields with a canonical recomputation that is actually used. Reproduce both witnesses before the repair and show rejection or exact recomputation afterwards. Preserve complete-grid, nonempty-output and resource-completeness tests. Do not describe the present witness as a physical-diameter counterexample; equally, do not dismiss it as output forgery when it passes through the unmodified certifying endpoint.

**Robustness comparison.** Incorporate or carefully rebut (R54.1)–(R54.3), including predictable sign-correlated discrepancies, baseline chronology, the deterministic drift bound, and the distinction between the unweighted printed region and weighted finite improvements. Explain the residual benefit of full posterior contraction after this comparator is included. Merely observing that the estimator is biased does not answer the argument.

**Contribution and literature.** Compare the precise statistical ingredients with the named primary results, without either claiming automatic subsumption or treating different terminology as proof of novelty. State which new quantitative mechanism, breadth or optimality content bears the exceptional-significance claim. A programming repair is necessary for the advertised executable contract, but is not a promise of acceptance at the requested journals.

**Scope and evidence.** Retain the now-correct qualifications on working likelihoods, coverage of supplied bands, block commitment, chosen clocks, exhaustive computational cost, and positive-gap elapsed time. Keep actual executions separate from source inspection and author receipts. The narrow positive fixture is useful as an interface test, but its a priori diameter already lies below the target and it is not an empirical demonstration of informative recovery on a wide box.

These requests do not require weakening the positive theorem or replacing it with a no-go statement. They require an accurate certification interface and an honest account of the strength of the mathematical contribution.

**Final recommendation:** reject at the requested four-journal standard. The core logarithmic-depth and energy-robust posterior conclusions survive the present written-proof audit under their declared hypotheses. The exact runtime certification claim still fails in a reproducible way, and the exceptional-significance argument remains unpersuasive after the stronger frequentist comparison is made explicit.

---

## Source map and reproduction

All repository source links below are pinned to the reviewed commit. The independent checks deliberately refuse to run against substituted source blobs. Historical programs remain unchanged.

- **[M0]** [Active article, `ROUND53_REVISION.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/ROUND53_REVISION.tex). Relevant labels: `lem:sampled`, `prop:envelope`, `thm:energy`, `lem:block-floor`, `thm:response-estimator`, `thm:outer`, `thm:global`, `cor:time`.
- **[M1]** [Inherited model, stability and physical inverse](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/round51/model_inverse.tex).
- **[M2]** [Inherited chronological likelihood, covers and grouped-square proof](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/round51/likelihood.tex).
- **[M3]** [Itemized response to Round 52](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/AUTHOR_RESPONSE_ROUND52.md).
- **[M4]** [Active certificate implementation](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/tools/round53_certificates.py) and [unchanged rational core](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/tools/round51_certificates.py).
- **[M5]** [Author's new 44-test suite](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/tests/test_round53.py).
- **[M6]** [Review index](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/ROUND53_REVIEW_INDEX.md), [source manifest](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/round53/SOURCE_MANIFEST.json), and [verifier source](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/tools/verify_round53.py).
- **[M7]** [Current literature audit](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/round53/LITERATURE_AUDIT.md).
- **[M8]** [Controlling Round 52 report](https://github.com/TrillionniumFoundation/theta-theory/blob/7f1bc9a42ba27615aea61afb9a417ef076e2c6e1/REFEREE_REPORT_ROUND52_GPT6_ASTRA_PRO_HARSH.md).
- **[L1]** T. Sarkar, A. Rakhlin and M. A. Dahleh, *Nonparametric Finite Time LTI System Identification*, [arXiv:1902.01848v6](https://arxiv.org/html/1902.01848v6), particularly Assumption 1 and the finite-response setup. The input-scope comparison is not a claim that this paper proves the complete Round 53 theorem.
- **[L2]** F. Seizilles and M. Siebel, *Posterior contraction under misspecification and heteroscedasticity in non-linear inverse problems*, [arXiv:2603.28177v1](https://arxiv.org/html/2603.28177v1), Section 2.3, Theorems 3.12 and 3.17, Corollary 3.15, and the stated role of Appendix B. Primary text accessed 5 September 2026; targeted statement-level comparison, not a full proof audit.

From a checkout of this review branch:

```sh
python tests/test_round53.py --json-out reviews/round54/AUTHOR_ROUND53_TEST_REPLICATION.json
python reviews/round54/independent_checks.py
```

The second command checks the three source blobs, performs the finite assertions, and writes `reviews/round54/INDEPENDENT_CHECKS.json`. Successful exit intentionally includes reproduction of the two exact-budget contract defects. A later repaired implementation must not be substituted silently into this frozen-source witness. No result here is labeled formal proof certification, a complete artifact build, or journal acceptance.
