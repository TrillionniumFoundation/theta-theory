# Round 50 — Independent harsh referee report on the frozen Round 49 revision

## Recommendation: Reject at the requested Annals–Inventiones–JAMS–Acta level

**Manuscript:** *Logarithmic-Depth Boundary Identification with Bounded Probes and Retained State*  
**Author named in the manuscript:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Revision branch reviewed:** `revision/round49-bounded-probe-retained-state-2026-09-05`  
**Frozen distribution commit:** `abae39b7efeec5f6995f85fcbe1cc1d10e27fba6`  
**Distribution tree:** `35dbf5ad7391a7d7a4d0f82a3fb896c28253d0f9`  
**Full-history source commit:** `2fde77007cdba64ba1ee57be7398d8f78a5d393b`  
**Full-history source tree:** `23846e9c23fe860ce57381d62fe7b39bb9b1313e`  
**Source-capsule commit identified by the publication record:** `370eaef4fe631396728442612d1d44e941917b2c`  
**Controlling Round 48 report commit:** `cd21a42e47faa8aee0979137da64bf77b016a201`  
**New review branch:** `review/round50-gpt6pro-harsh-round49-2026-09-05`  
**Review date:** 5 September 2026, Asia/Singapore  
**Reviewer:** GPT-6 Pro, at the repository user's request.

This is an independently reasoned, AI-generated referee-style assessment. It is not a report commissioned by, an appointment from, or an editorial decision of any of the four journals named above. A negative recommendation at that requested standard is not a declaration that the research program is impossible or that the main theorem is false.

### 中文结论

按所要求的数学四大刊标准，本报告建议拒稿，但必须准确说明拒稿依据：**本轮未发现推翻当前主定理的反例，也未定位到必须撤回其对数深度结论的致命证明漏洞。** Round 49 确有实质进展，不能继续用 Round 48 已经修复的问题否定它。

新稿将短脉冲的延迟响应、收敛的采样生成元反演、整块条件信息下界与完整工作似然的后验界连成了一条可信的证明链。在明确选择的快时钟及块内预承诺控制类中，原有有界时长抽样律能够实现对数深度恢复；全策略信息上界给出相应阶数障碍。抽样权重与置信分配混用、输入舍入扩张漏计这两处旧问题，当前文本均已修复。

本报告的主要否定意见是贡献定位和交付完整性，而不是伪造新的数学反例。现有证明实际上只需要一个足够短、具有正质量的诊断原子；多尺度抽样律的其余结构不是这项新深度定理的必要机制。并且，非探索阶段也使用该原子，因此成功块概率可由 `(rho*w0)^m` 严格改进为 `(1-rho+rho*w0)^m`。报告给出推导及算例，明确将其列为改进而非错误。对非参数脉冲响应估计等最近邻工作的比较仍不足以建立四大刊级别的突出贡献。与冻结 GitHub 版本匹配的三个作者程序没有在本次审查中取得，故作者报告的 43 项测试及双根构建没有被本审稿人重新执行。

本次独立执行了 **14 组、104 个有限案例**，其中 74 个为精确有理算术案例，30 个为 80 位 Decimal 数值案例，全部通过。它们支持局部代数核查，不构成无限维定理的形式化认证。审稿程序和实际结果随本报告一并落盘。

---

## 1. Executive assessment and classification of findings

The revision has crossed a meaningful mathematical threshold. It no longer needs an unbounded-duration law to exhibit logarithmic recoverable depth. It also supplies a genuinely different posterior argument: variance-sensitive control replaces the previous information-square cost by inverse-information cost. These are not cosmetic rewrites. [M3–M5]

The central conclusion supported by my examination is the following. For the chosen sufficiently small clock, bounded block-committed profiles, the stated product coefficient prior, and any working initial-state law on the declared ball, the full working posterior of completed blocks contracts through

\[
J_n=\lfloor r\log n\rfloor,\qquad \delta_n=n^{-s},\qquad C_b r+p_b s<1.
\]

The deterministic elapsed-time bound and the all-policy logarithmic-depth obstruction are compatible. This is an attainability result for a specified admissible design, not a theorem about every bounded-feedback policy or every externally imposed clock. The manuscript substantially says this already. [M5, M8, M11]

The findings below must not be conflated:

| ID | Finding | Classification and effect |
|---|---|---|
| R50-M1 | Matching executable implementation and verifier were not retrieved for this frozen submission | Material reproducibility/submission issue; not a counterexample to a written theorem |
| R50-M2 | The closest-comparison argument remains incomplete, especially for nonparametric impulse-response estimation | Major contribution-positioning objection; no established priority counterexample |
| R50-Q1 | The successful-block event can be enlarged without changing the implemented design | Proven quantitative refinement; the printed lower bound remains valid |
| R50-Q2 | The new depth argument only requires one sufficiently short atom | Structural clarification and broader corollary; not a logical defect |
| R50-E1 | Revision history and certification bookkeeping obscure the standalone mathematical contribution | Expository objection, not mathematical invalidity |
| Scope S1 | The positive theorem chooses the fast clock and excludes within-block readout-dependent control | Declared scope; not an undisclosed gap |
| Scope S2 | Inner and outer joint exponent regions do not coincide | Declared non-sharpness; not a failure of the order theorem |

**There is no newly demonstrated fatal correctness defect in this ledger.** My recommendation remains negative at the requested journal level principally because the exceptional-significance case has not been established after the new mechanism is separated from its classical and statistically standard ingredients. The distribution problem is an additional, repairable obstacle to independently evaluating the operational implementation claims. Neither issue licenses announcing that the principal theorem has been disproved.

## 2. Source freeze, actual work, and exclusions

I reviewed the main TeX root and all eleven `round49/` inputs, the retained supplement and its five Round 45 inputs, the author response, review index, source manifest, proof ledger, publication record and verification receipt. I examined the controlling report's mathematical criticisms and their stated repairs. I do not claim to have audited every historical branch or every earlier research document.

The Git comparison from `2fde770...` to `abae39b...` reports exactly one descendant commit, adding only `ROUND49_PUBLICATION.json`, `ROUND49_TESTS.log`, `ROUND49_VERIFICATION.json`, and `ROUND49_VISUAL_AUDIT.json`. It does not modify the manuscript. The fetched active input blob identities agree with those declared in the manifest. This supports a clean distinction between source and artifact publication; it is not an independent execution of the author's checkout verifier. [M13]

There is also a different, same-number **local-only** Round 49 package in the accompanying materials accessible during this review. Its title is *History Information and Logarithmic Depth in Bounded-Duration Boundary Identification*, its recorded local source commit is `cadf0e1775ee8802087f0a3b5d2aa135c711edf6`, and its publication record explicitly says that it was not pushed to GitHub. It reports a 22-page main article and 54 tests, rather than this submission's 16-page article and 43 tests. It discusses a different clustered-time construction without the same small-gap hypothesis. **It is excluded from this review.** It cannot repair or invalidate the frozen GitHub article merely because its filenames also say Round 49. This is a source-selection distinction, not an allegation of inconsistent mathematics within the frozen commit.

I independently wrote and ran `reviews/round50/independent_checks.py`. The corresponding `INDEPENDENT_CHECKS.json` records the actual execution: Python 3.13.5, 14 groups and 104 finite cases, all passed. The script uses the standard library only. Its SHA256 is

```text
dea7d7b2b65f28c6924df107a1b2f562d17f8e8fbe4cc53faefae686a3307871
```

The checks cover formal sampled-logarithm identities, finite coefficient bounds, factorial-normalized Vandermonde inverses, the damped moment identity, inverse Gram identities, coefficient reconstruction, first changed boundary jets, complete sign enumeration, the enlarged success probability, posterior exponent arithmetic, representation-error accounting, and representative resource inequalities. The Decimal cases are not interval-certified bounds. A finite check cannot establish a universal infinite-depth inequality.

**Not executed by this referee:** the author's 43-test suite, the author's source-bound verifier, either TeX build, or any proof-assistant formalization. I reviewed TeX sources, not a visually audited rendering of the two claimed PDFs. The manuscript's reported build successes remain author-provided evidence, not my replicated results.

## 3. Audit of the principal proof chain

### 3.1 Physical inverse, compactness and the earlier separation laws

The energy argument supplies common exponential stability under the stated strict pinning, damping and edge bounds. Product-topology compactness is compatible with the full-input response metric because finite boundary words are local and the stable tail is uniformly integrable. I find no illicit substitution of operator-norm compactness for product compactness. [M1]

The identity

\[
A^2+cA=-\operatorname{diag}(\mathsf J,\mathsf J)
\]

correctly yields the moment formula

\[
\mu_m=(-1)^m\sum_{k=0}^m\binom{m}{k}c^{m-k}v_{m+k}.
\]

The inverse Gram representation in monic orthogonal-polynomial coefficients preserves an exponential-in-depth estimate, rather than silently introducing a quadratic depth exponent. The positive edge lower bound supplies the required norm-ratio denominators. My examination of the assembled secant bounds supports the conservative certificate

\[
d_J(\beta,\gamma)\le Q^{25(J+1)}
\max_{r\le4J+8}|h_\beta^{(r)}(0)-h_\gamma^{(r)}(0)|.
\]

The independent finite identities supplement that argument; they do not replace it. [M1]

The factorial-normalized interpolation matrix has the relevant induced infinity-norm bound `2^N binom(2N,N) <= 8^N`. The compact-law grid uses existing labeled cells; the known value at zero is not a fictitious noisy observation. The finite-mean law and its mean `13u0/2` remain distinct from the bounded-duration law. I find no new defect in the retained sufficient separations `exp[-C_c j log(ej)] delta^12` and `exp[-C_infty j] delta^8`. [M2]

### 3.2 The sampled-generator bridge is mathematically substantive and appears sound

Put `U=exp(Delta A)`, `X=U-I`, and `H=int_0^{Delta/2} exp(uA) du`. The selected atom makes `Delta Lambda <=1/64`, so `||X||<=1/32`. The local logarithm and square-root series are therefore in a common convergent Banach-algebra neighborhood; there is no hidden choice among distant matrix-logarithm branches. [M4]

For

\[
F_r(x)=\Delta^{-r}[\log(1+x)]^{r-1}
\frac{\log(1+x)}{x}(\sqrt{1+x}+1),
\]

the cancellation with

\[
H=\Delta\,\frac{\sqrt{1+X}-1}{\log(1+X)}
\]

gives `F_r(X)H=A^(r-1)`, with removable singularities interpreted analytically. This is the key channel correction: a delayed short-pulse response is not simply the instantaneous impulse response, and the manuscript does not confuse the two. The transform is parameter-independent. [M4]

Cauchy estimates on `|x|=1/2`, the bound on `H`, and expansion of `(U-I)^k` give the displayed finite coefficient budget and remainder

\[
\mathcal A_{N,R}=8\Delta^{-R}4^N,\qquad
\mathcal E_{N,R}=16\Delta^{-R}8^{-N}.
\]

The remainder is conservative, but its decay is sufficient. Choosing `N` so that `L E <= delta/2` produces the asserted delayed-pulse separation. The constants in `m <= K_b j+v/log 8` and `kappa_b >= exp(-C_b j) delta^{p_b}` are consistent with the displayed logarithmic accounting. In particular, the whole-run probability is included, rather than the probability of one successful atom being reused for an entire run. [M4]

This bridge is the strongest new deterministic component. It deserves explicit recognition. Its correct proof is not diminished by the quantitative refinements in Section 5 below.

### 3.3 Retained-state blocks and conditional information

On a successful block, successive endpoints are separated by `Delta`. Conditional on the pre-block history, actions, committed profiles and the other signs, the first sign is still fresh. Consequently

\[
f_{b,k}(\beta)=P_{b,k}(\beta)
+aS_{b,0}\{b_{k,\beta}-b_{k,\beta_0}\}.
\]

Block commitment is doing real work: it prevents the intercept from depending on that sign through later within-block feedback. Squaring and averaging leaves a nonnegative intercept square. The group-start conditional floor is therefore valid. [M5]

Equally importantly, the proof does **not** replace the full likelihood by a likelihood conditional on block success. The success event is used to lower-bound an expectation of nonnegative squared contrasts; unsuccessful blocks remain in the likelihood. Revealing independent action randomizers for this calculation does not condition the Gaussian score on a terminal, response-dependent design. The usual objections to data-discarding or fixed-design conditioning do not apply here. [M3, M5]

The new attainable depth uses information from increasing lags of an old pulse, even though each individual probe is short. Thus a factorial obstruction for one fixed reset window does not contradict the result. The relevant observation age increases with the block length; the individual forcing duration need not increase. [M4, M5, M8]

### 3.4 Variance-sensitive posterior transfer

For a deterministic net point, the Gaussian exponential martingale controls the score relative to its own quadratic variation. The grouped squared contrasts are bounded nonnegative increments, so the exponential chord inequality controls their shortfall relative to group-start conditional expectations. The net is deterministic in the common full-input metric. Interpolation includes the conditional expectations as well as the realized squares. [M3]

I checked the resulting event

\[
|S_n|\le A_n/16+nq/64,\qquad
A_n\ge V_n/2-nq/32
\]

and the roles of `m M^2`, `sigma^2`, `e_q`, and the entropy term. The grouped square estimate does not require independent blocks; the Gaussian score remains in the original readout chronology. The construction is not just an unproved transfer of frequentist confidence contraction to a posterior. [M3]

The nuisance integral estimate is uniform over the working initial-state law because the entire transient potential is controlled by a summable envelope before integration. On the variance event, the numerator coefficient is `-97/512`; the denominator ball costs `13/256`; and the allowed nuisance difference adds `1/32`. Thus

\[
-97/512+13/256+1/32=-55/512\le-1/16.
\]

The direction of the prior small-ball estimate is correct. There is spare constant margin rather than an arithmetic gap. [M3]

For `q_b=a^2 kappa_b/m` and `m=O(log n)`, the decisive failure exponent has size at least `c n^(1-gamma)/(log n)^2`, where `gamma=C_b r+p_b s<1`. It dominates the `O((log n)^2)` entropy and prior-mass costs. Rounding to completed blocks costs `o(n)` readouts, and their deterministic clock is at most `(t0+T)n'`. The coordinate-median argument gives a genuine finite-prefix estimator. These steps support the announced sufficient region. [M3–M5]

### 3.5 The all-history obstruction and what is actually matched

For two parameters differing only in `b_J`, the two off-boundary propagators in Duhamel's formula each have their first possible word at degree `2J+1`. The resulting first changed step-response derivative is `4J+4`. In the independent exact examples the leading difference is `-delta product_{k<J} a_k^2`, as expected. Damping loops do not shorten the path. [M8]

The short-time factorial estimate plus the exponentially stable tail gives the all-time `L^1` response bound. At a common observed history the two candidate policies prescribe the same input function, so the chronological Gaussian KL chain rule applies to the full data record. The zero-initial-state pair is a legitimate subexperiment for a lower bound on uniform estimation over the larger initial-state class. [M8]

This supports logarithmic depth **order** at fixed accuracy. The displayed sufficient condition `C_b r+p_b s<1` and necessary obstruction `8 vartheta r+2s>1` are not a sharp common exponent curve. The manuscript explicitly distinguishes them. Demanding matching constants as a precondition for the correctness of an order theorem would be an invalid objection. A sharper curve could increase the contribution's significance, but it is additional research, not a missing lemma needed to validate the theorem as stated.

## 4. Disposition of the previous operational objections and retained results

### 4.1 R48-M1 is repaired in the current mathematics

`w_q` now denotes sampling probability, while `eta_q` denotes confidence allocation. The count lower bound uses `pi=rho min_G w_q`; the confidence logarithm uses `eta_min`; and `C_v=4/(alpha_c eta_min)`. The explicit visit budget retains the arbitrary allocation dependence. Making a grid's confidence allocation extremely small therefore increases the budget rather than contradicting it. The simultaneous coverage argument uses stopped exponential supermartingales, not an assertion that a selected sum is Gaussian conditional on its terminal visit count. [M6]

The block-pulse bands are separately justified, with one shared success count and correlated lag statistics. No independence across lags is required. The predetermined-grid count guarantee is not silently extended to a retrospectively selected grid. I consider the old text-level allocation objection closed, while leaving implementation replication to R50-M1. [M5, M6]

### 4.2 R48-M2 is repaired in the current mathematics

The input representation budget is now explicit:

\[
I_q\subset I_q^{\rm rat}\subset
[\widehat y_q-R_q-\epsilon_q,\widehat y_q+R_q+\epsilon_q].
\]

The outer radius is correspondingly `R_q+epsilon_q+2E_q`. The old example enclosing `[-10^-7,10^-7]` by `[-1,1]` requires `epsilon >=1-10^-7`; the current theorem no longer treats that enlargement as free. [M7]

The statement about a retained full box is universal over its admissible completions. The statement about a projected prefix is existential: a retained full-box witness must exist. Selecting separate witnesses for two prefixes is sufficient for the prefix diameter argument, because that distance ignores the further tail. This is the correct quantifier, not a claim that every tail attached to the projection is feasible. [M7]

The separate tail, mesh and Taylor errors appear conservative and compatible with the bounded generator and finite-word locality. The construction explicitly makes no practical or polynomial-time assertion. I do not label finite exhaustive enumeration an efficient algorithm that the author never claimed to have supplied.

### 4.3 Retained results are not new substitutes for the main theorem

The actual-information tracking result uses the original **stagewise** predictable information, not the grouped finite-block quantity. Uniform likelihood approximation, equicontinuity, compactness and full prior support supply the pathwise Laplace comparison and subsequential LDP statements. The probability-one assertion is for each chosen policy sequence and coupling, not an intersection over uncountably many policies. The weighted operator conclusion is a product-topology consequence, not unweighted operator-norm consistency. [M9]

The homogeneous supplement assumes strong uniform smoothness, summable nuisance derivatives, an interior truth, and a global quadratic contrast. Its random-information BvM follows from a relative Laplace argument under uniformly nondegenerate root-n information. The six-duration mechanical embedding and balanced-sign contrast supply those strong hypotheses in its separate model. The state and memory conclusions use bounded-Lipschitz Gaussian images of a five-dimensional parameter, not an unrestricted infinite-dimensional BvM. Strong filter jets are formulated in specified separable dual subspaces; the finite preparation weights are ordinary finite-component evidence ratios. I found no new contradiction in those arguments. They do not establish the new infinite-Jacobi theorem and should not be counted again as new Round 49 contributions. [M10]

## 5. R50-Q1 and R50-Q2: a stronger elementary certificate and the actual mechanism

### 5.1 Enlarge the successful-block event

**Location:** `round49/blocks.tex`, opening experiment definition and `lem:block-floor`; constants in `round49/sampled_generator.tex`.

The manuscript sets every **nonexploration** stage to `q0`, yet calls a block successful only when all stages explore and select `q0`. This is a valid but unnecessarily small event.

Let `E_b^*` mean that every stage either does not explore or explores and selects `q0`. Its conditional probability is

\[
\Pr(E_b^*\mid\mathcal F_{b,-})=p_*^m,
\qquad p_*=1-\rho+\rho w_0.
\tag{R50.1}
\]

It is determined by exogenous action randomizers and is independent of all block signs and noises. On this event the entire duration pattern is exactly the same fast pattern as on the printed success event. The same sign argument therefore gives

\[
\mathbb E\!\left[\sum_{i\in G_b}f_i(\beta)^2\mid\mathcal F_{b,-}\right]
\ge a^2p_*^m\sum_{k=0}^N(b_{k,\beta}-b_{k,\beta_0})^2.
\tag{R50.2}
\]

This statement does not require altering the exploration law or the likelihood. Additional labels coinciding in duration might enlarge the event further; they are not needed for (R50.1).

Consequently the block certificate can replace `(rho w0)^m` by `p_*^m`, and in the constants it can replace

\[
a_b=\log(1/(\rho w_0))+\log16
\quad\text{by}\quad
\widetilde a_b=\log(1/p_*)+\log16.
\tag{R50.3}
\]

The same `K_b` is retained, with `C_b` and `p_b` updated accordingly. For `rho<1` this strictly improves the displayed sufficient region. It also removes the artificial deterioration of this particular certificate as `rho` becomes small while the nonexploration design itself keeps using the diagnostic atom.

For the admissible box `c in [1,2]`, `a_k in [1/2,1]`, `b_k in [3,4]`, `T=1`, `rho=1/2`, the manuscript's definitions give `Lambda=9`, `Q=72`, `t0=1/2048`, `Delta=1/1024`, and `w0=1/4096`. The per-stage probabilities are respectively `1/8192` and `4097/8192`. The computed constants are

\[
(C_b,p_b)\approx(1411.411,7.666667),\qquad
(\widetilde C_b,\widetilde p_b)\approx(648.239,3.666549).
\]

These are illustrative evaluations, not sharp or practical sample-complexity claims. The improvement follows from the symbolic probability calculation, not from the numerical example.

**Classification:** quantitative refinement, not a false bound. It would be unfair to call a conservative information floor a contradiction. Nevertheless, a paper presenting explicit resource regions should either use this inexpensive improvement or state why it deliberately retains the smaller event.

### 5.2 All signs yield a stronger exact block-energy identity

Condition on the pre-block history, committed profiles and a fixed fast action pattern. Write `d_k=b_{k,beta}-b_{k,beta0}`. Linearity gives

\[
f_{b,k}=P_{b,k}+a\sum_{j=0}^k S_{b,j}d_{k-j},
\]

where `P` is independent of all block signs. Averaging all signs gives the exact identity

\[
\mathbb E_S\sum_{k=0}^{m-1}f_{b,k}^2
=\sum_{k=0}^{m-1}P_{b,k}^2
+a^2\sum_{k=0}^{m-1}(m-k)d_k^2.
\tag{R50.4}
\]

The printed first-sign floor is a valid consequence. Formula (R50.4) displays the underlying finite impulse-response regression geometry more transparently. It does not, by itself, prove that the final logarithmic factors or minimax constants can be removed. The independent script checks complete sign enumerations through block length seven; the displayed orthogonality argument is the general proof.

### 5.3 Only one sufficiently short positive-mass atom is needed

The proof of the new block theorem does not use the dense rational half of `omega`, nor its growing family of derivative grids, except to locate one atom satisfying the fast-clock condition. Once `t0`, its mass and the bounded duration cap are available, all subsequent steps use delayed responses of that same atom.

More generally, retain the coefficient box, prior, noise, block commitment and working initial-state assumptions. Let a bounded-duration exploration law have any atom of mass `w>0` at a duration `t>0` satisfying `2t Lambda<=1/64`. Choose gap `t` and the same nonexploration duration. The sampled-generator proof applies with `Delta=2t`, the block proof with that atom's mass, and the same entropy and nuisance arguments then yield a logarithmic-depth sufficient region with the corresponding constants. The remaining atoms need not form a multiscale or dense family for this **block** theorem.

This is a direct corollary of the manuscript's proof, not a prior theorem being asserted without a citation. The old multiscale structure still matters for the separately retained **one-stage**, unrestricted-feedback separation results. The revision should present these two roles distinctly.

**Why this matters for review:** the genuine new mechanism is a sampled short-pulse channel plus retained response history and chronological information transfer. It is not a newly necessary elaborate duration distribution. A clean one-atom formulation would improve the result's generality and expose the right literature comparison. This observation strengthens a possible revised paper while making its present novelty rhetoric more precise.

## 6. R50-M1: the operational implementation is not independently reproducible from the retrieved submission

**Locations:** `ROUND49_PUBLICATION.json`, `round49/SOURCE_MANIFEST.json`, the review index, and the implementation statements in the author response. [M12, M13]

The record is commendably explicit that the following programs were **not committed**:

```text
tools/round49_certificates.py
tests/test_round49.py
tools/verify_round49.py
```

Their SHA256 values are pinned, but a hash is not executable source. The publication record points to an accompanying `ROUND49_REVIEW_BUNDLE.tar.gz`, expected SHA256

```text
093718cc094f5f0cc82ee90979f1702326f884c7c1beed901ab02189033d4d6b
```

I searched the available accompanying-file records and inspected the same-number materials returned. I did not retrieve that matching bundle. The distinct local-only `ROUND49_REVIEW_PACKAGE.zip` described in Section 2 cannot be substituted: its source identity, title, test count and PDF records differ.

The proper conclusion is limited but important: **I cannot independently assess the three frozen implementation programs or reproduce the reported 43-test and double-build workflow from the material retrieved in this review.** This does not establish that the bundle never existed, that the author did not run the workflow, or that the recorded successes were fabricated. I make none of those accusations.

Before a submission claims independently reproducible executable outer certificates and source-bound validation, the exact matching programs should be made durably available with the frozen sources, or as a clearly retrievable, immutable associated artifact. The instructions should distinguish an ordinary repository checkout from a checkout augmented by that artifact. The existing explicit disclosure is necessary, but does not supply the missing bytes.

For mathematical acceptance, the distinction also runs in the other direction: a pure mathematical proof does not require numerical regression tests to become true. This delivery issue concerns evaluation of the promised implementation, not the logical necessity of a computer certificate for the analytic theorem. The independent Round 50 checks are different programs and must not be presented as a replacement execution of the author's suite.

## 7. R50-M2: the exceptional-contribution case is still underdeveloped

### 7.1 What the verified literature comparisons do and do not show

**Mikhaylov–Mikhaylov.** Their dynamic Jacobi inverse work establishes the deterministic boundary-response/moment reconstruction lineage. The present continuous-time damping, noisy chronological observation and quantitative depth statements are different ingredients. This reference prevents a priority claim for the response-to-Jacobi principle, but does not by itself prove the present statistical theorem. [L1]

**Sarkar–Rakhlin–Dahleh.** The finite-time LTI work studies unknown finite latent order, noisy input-output data and Hankel/finite-impulse-response estimation. In the cited preprint, Theorem 5.1 and Corollary 5.1 quantify Hankel-block and Markov-parameter errors. Its realization target has similarity ambiguity; this manuscript targets labeled infinite physical coefficients. Those are real differences. They do not eliminate the need to analyze whether a dimension-uniform finite-response estimation component can be combined with the physical inverse. [L2]

**Goldenshluger.** A closer nonparametric predecessor is missing from the current bibliography: *Nonparametric estimation of transfer functions: Rates of convergence and adaptation*, IEEE Transactions on Information Theory 44(2) (1998), 644–658. The author's institutional publication record describes nonasymptotic FIR least-squares bounds, lower bounds, adaptation, and families with polynomially or exponentially decaying impulse responses. Thus “the compared system-identification result has finite latent order” is not a complete comparison with the relevant estimation literature. I verified this bibliographic record and abstract, not a theorem-by-theorem reduction from its full text. It is a required comparison target, **not** a demonstrated theorem that already subsumes Round 49. [L3]

**Agapiou–Stuart–Zhang.** Their linear severely ill-posed Bayesian model yields logarithmic contraction rates under exponentially decaying spectral visibility; see Theorem 4.3. Its commuting Gaussian operator framework does not supply this nonlinear coefficient inverse or experimental design. The comparison nevertheless confirms that logarithmic behavior alone is not a novelty criterion. The current introduction appropriately acknowledges that limitation. [L4]

**Yue–Thunberg–Goncalves.** Their system-aliasing work concerns recovering continuous generators from sampled matrix exponentials and the difficulties caused by slow sampling. The manuscript avoids the relevant ambiguity by an explicit small-norm neighborhood, rather than solving a general aliasing problem. Its additional channel correction and infinite-chain inverse remain to be assessed on their own merits. [L5]

**Du–Nair–Janson.** Their Theorem 1 permits adaptive linear Gaussian information with potentially diverging condition number, subject to stated eigenvalue growth; Corollary 1 specializes policy uniformity to basis-vector designs. The homogeneous supplement here has nonlinear means but stronger smoothness and uniformly nondegenerate root-n contrast. Its random-information Gaussian approximation is not a resolution of the general anisotropic problem. The manuscript's separation of posterior approximation from frequentist coverage is correct. [L6]

### 7.2 The comparison the paper still needs

The revised introduction lists relevant references and disclaims exaggerated priority claims. That is progress, but a list of differing assumptions does not yet establish a deep new advance. The most useful comparison is a precise decomposition into: estimation of delayed pulse coefficients from a nonreset record; inversion of the sampled pulse channel; inversion to labeled Jacobi coefficients; and complete-posterior transfer with initial-state misspecification.

For each component, the authors should state what existing FIR/system-identification or inverse-stability result actually provides under compatible input, noise and stability assumptions, what uniformity would be lost in a finite-chain truncation, and which quantitative lemma must genuinely be added. This does not require asserting that an existing theorem applies when it does not. It requires identifying the obstruction to such a reduction rather than relying only on the words “infinite-dimensional” and “physical labels.”

My strongest positive assessment is that the sampled-channel lemma and the complete-record block transfer form a useful, potentially original synthesis with an explicit physical target. My negative assessment is that the present submission has not demonstrated the conceptual depth, breadth or exceptional significance needed for the four journals requested. The proofs use a strongly pinned, uniformly damped, bounded nearest-neighbor model; a selectable fast clock; committed blocks; and an exponentially conditioned finite-jet inverse. Once those assumptions are made explicit, the general statistical transfer is comparatively standard, and the new analytic identity is elementary though effective. A correct and useful synthesis is not automatically a four-journal contribution.

This is an editorial judgment, not an objective theorem about the value of the work. I have **not** located a prior publication proving the exact main theorem under exactly these hypotheses. I therefore do not accuse the manuscript of lacking all originality, and I do not turn an incomplete literature search into a priority verdict.

## 8. Scope discipline and presentation requests

The selected fast gap is an assumption of the attainable design. It should remain visible in the abstract, main theorem and any summary. The argument reviewed here does not establish recovery at every fixed positive externally imposed observation gap. Conversely, this report does not prove that such an extension is impossible. The excluded local manuscript is a different proposed approach, not part of the present evidence. [M4, M5, M11]

Similarly, arbitrary feedback **between** committed blocks is not arbitrary feedback **within** them. The separate unrestricted stagewise results should remain separately quantified. The all-policy lower bound and the narrower attaining upper-bound class can legitimately yield an order-optimal attainable depth; their policy classes need not coincide point for point. [M3, M5, M8]

The explicit constants are conservative certificates, not estimates of the actual minimax threshold. Section 5 shows that a sizeable part of their loss can be removed without new theory. This reinforces the manuscript's own warning against reading the displayed joint regions as a sharp frontier. A practical or polynomial-time solver, a matching leading constant, and arbitrary-clock recovery are possible further achievements, **not retroactive requirements for proving the stated order result**.

For a standalone submission, move Round-number narration, delivery disputes and proof-ledger status language out of the article and into the response or artifact documentation. Put the one-atom sampled-channel theorem and the posterior information theorem in a clean theorem map, with their constants collected once. Retained homogeneous results should remain visibly separate rather than inflating the list of new claims. These are R50-E1 presentation requests, not allegations that repository bookkeeping has been misrepresented as a formal proof.

## 9. Decision and requirements for a response

I would not recommend acceptance at the requested Annals/Inventiones/JAMS/Acta level. The rejection is **not** based on the old confidence-allocation or input-rounding defects, and it is **not** based on a demonstrated collapse of the new logarithmic-depth theorem.

A useful response should address three concrete matters. First, supply the exact matching implementation artifact and make the frozen reproduction path unambiguous. Second, either incorporate the enlarged successful event and one-atom formulation or explain the deliberate retention of the weaker certificate. Third, replace the current broad novelty contrasts by an explicit comparison with nonparametric response estimation and with a possible finite-response-to-physical-inverse reduction.

Those actions would improve rigor of presentation, reproducibility and contribution assessment. They do not promise acceptance, and they do not require pretending that all conceivable stronger theorems have already been proved. The mathematical result that survives this review should be retained: **bounded individual probes, a chosen fast clock, retained history, block commitment and a complete-likelihood argument do support an explicit logarithmic-depth recovery theorem in the declared model.**

---

## Source references

All manuscript references below are immutable links to the reviewed distribution commit, not moving branch heads. Equation/theorem labels in the report refer to the literal TeX labels in those files.

- **M1:** [Model, stability and physical inverse — `round49/model_inverse.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/model_inverse.tex).
- **M2:** [Earlier response laws, separation and chronology — `round49/separation.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/separation.tex).
- **M3:** [Variance-sensitive likelihood and posterior — `round49/likelihood.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/likelihood.tex).
- **M4:** [Sampled-generator inverse — `round49/sampled_generator.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/sampled_generator.tex).
- **M5:** [Retained-state blocks — `round49/blocks.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/blocks.tex).
- **M6:** [Confidence and visit budgets — `round49/confidence.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/confidence.tex).
- **M7:** [Certified outer sets — `round49/enclosures.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/enclosures.tex).
- **M8:** [All-policy lower bound and frontier — `round49/frontier.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/frontier.tex).
- **M9:** [Retained adaptive limits — `round49/retained_limits.tex`](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/retained_limits.tex).
- **M10:** [Retained supplement root](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/ROUND49_RETAINED_RESULTS.tex), with [triangular theorem](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round45/triangular.tex), [mechanical verification](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round45/lattice.tex), and [filter/memory/mixture results](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round45/filter_memory.tex).
- **M11:** [Introduction and main theorem](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/introduction.tex).
- **M12:** [Author response to Round 48](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/AUTHOR_RESPONSE_ROUND48.md); [controlling report at its frozen commit](https://github.com/TrillionniumFoundation/theta-theory/blob/cd21a42e47faa8aee0979137da64bf77b016a201/REFEREE_REPORT_ROUND48_GPT6_PRO_HARSH.md).
- **M13:** [Publication record](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/ROUND49_PUBLICATION.json), [source manifest](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/round49/SOURCE_MANIFEST.json), and [author verification receipt](https://github.com/TrillionniumFoundation/theta-theory/blob/abae39b7efeec5f6995f85fcbe1cc1d10e27fba6/ROUND49_VERIFICATION.json).

### Primary literature checked for the comparisons

- **L1:** A. S. Mikhaylov and V. S. Mikhaylov, *Dynamic inverse problem for Jacobi matrices*, Inverse Problems and Imaging 13 (2019), 431–447, [publisher page](https://www.aimsciences.org/article/doi/10.3934/ipi.2019021?viewType=HTML); related [moment-problem preprint, arXiv:1907.11153](https://arxiv.org/abs/1907.11153).
- **L2:** T. Sarkar, A. Rakhlin and M. A. Dahleh, *Finite Time LTI System Identification*, JMLR 22(26) (2021), 1–61, [journal record](https://jmlr.org/papers/v22/19-725.html). The theorem-numbered comparison was checked in [arXiv:1902.01848v6, Sections 3 and 5](https://arxiv.org/html/1902.01848v6); it is identified as that version rather than silently conflated with every numbering in the journal article.
- **L3:** A. Goldenshluger, *Nonparametric estimation of transfer functions: Rates of convergence and adaptation*, IEEE Transactions on Information Theory 44(2) (1998), 644–658, DOI 10.1109/18.661510; [author's institutional publication record and abstract](https://cris.haifa.ac.il/en/publications/nonparametric-estimation-of-transfer-functions-rates-of-convergen/). Review scope here is the verified record/abstract, not a complete audit of its full theorem hypotheses.
- **L4:** S. Agapiou, A. M. Stuart and Y.-X. Zhang, *Bayesian posterior contraction rates for linear severely ill-posed inverse problems*, Journal of Inverse and Ill-Posed Problems 22(3) (2014), 297–321; [arXiv:1210.1563v3, Theorem 4.3](https://arxiv.org/html/1210.1563v3).
- **L5:** Z. Yue, J. Thunberg and J. Goncalves, *Inverse Problems for Matrix Exponential in System Identification: System Aliasing* (2016); [arXiv:1605.06973](https://arxiv.org/abs/1605.06973). The comparison uses the stated problem and scope, not an assertion that its finite-matrix results already prove the present infinite-chain theorem.
- **L6:** K. Du, Y. Nair and L. Janson, *Bernstein–von Mises for Adaptively Collected Data* (2025); [arXiv:2511.06639v1, Theorem 1, Corollary 1 and Appendix F](https://arxiv.org/html/2511.06639v1).

### Independent review artifacts

[Referee's finite-check source](reviews/round50/independent_checks.py) and [actual results](reviews/round50/INDEPENDENT_CHECKS.json) accompany this report. They are not the author's programs. All review files are additions on the new review branch; this review does not request a merge, approve a pull request, or alter the frozen manuscript.
