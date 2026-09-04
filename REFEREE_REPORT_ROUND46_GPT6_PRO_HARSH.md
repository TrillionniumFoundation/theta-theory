# Round 46: Independent harsh referee report on the frozen Round 45 revision

## Recommendation: Reject at the Annals–Inventiones–JAMS–Acta level

**Manuscript:** *Effective Adaptive Boundary Identification of Infinite Damped Jacobi Lattices*  
**Author named in the manuscript:** Qian Qi  
**Repository:** `TrillionniumFoundation/theta-theory`  
**Revision branch reviewed:** `revision/round45-effective-adaptive-closure-gpt6pro-2026-09-05`  
**Frozen distribution commit:** `00fee70834ee5e2a1fadc55c5d118a23a4637477`  
**Distribution tree:** `6968bce021371e1940db17f8a6e147684e080381`  
**Underlying source commit:** `c67f80f34fc128ba3eaece0fd8ad4ea262aa9cd1`  
**Source tree:** `680b42ab3d0bfa7d5eac89f5150f19d56805d8c9`  
**Controlling preceding report commit:** `9417c8d9ed14f8a8c4ba538435bf29837630b0ae`  
**New review branch:** `review/round46-gpt6pro-harsh-round45-2026-09-05`  
**Review date:** 5 September 2026, Asia/Singapore  
**Reviewer:** GPT-6 Pro, at the repository user's request.

This is an AI-generated, independently reasoned referee-style assessment. It is not a report commissioned by, an appointment from, or an editorial decision of any of the four journals named above. The recommendation expresses the reviewer's assessment of correctness, originality, depth, and significance at the requested level.

### 中文结论

建议按所要求的数学四大刊标准拒稿，但**不能沿用上一轮“修正未落盘、浅层指数不成立、洗出导数缺项”等理由**。本轮源码与发布提交之间的区别是合理的；有限样本概率界、正时间网格和无洗出策略的共同度量都有实质补充。本次审查没有得到推翻当前主定理的反例。

拒稿的主要依据是贡献定位与定量深度，而不是制造一个不存在的致命错误。下面给出的独立推导，在同一参数盒、同一采样分布和同一统计论证下，将响应导数逆映射的界从二次深度指数改进为线性深度指数，并得到二次而非三次深度指数的响应分离界，进而支持更大的充分恢复深度。这说明现有定量主结果包含可以用初等结构消除的巨大损失。此外，直接相关的自适应 BvM 与 Jacobi 动态边界反演文献尚未得到实质比较。报告将已修复的证明问题、原创性判断及验证工具的剩余缺陷分别列明。

---

## 1. Executive assessment

Round 45 is a materially better submission than the Round 43 v2 object discussed in the preceding report. There is now a coherent active publication unit, a source freeze followed by an artifact-only publication commit, and actual finite-sample arguments where the preceding response required them. A severe review must acknowledge that progress.

I do **not** find a demonstrated fatal counterexample to the current principal theorem chain. In particular, the old failure of the composed inverse exponent has been repaired. The current posterior-separation arithmetic checks out. The no-washout argument now controls the full realized input through a deterministic compact metric rather than silently replacing an adaptive history by a fixed design. The confidence-set proof uses the correct stopped-supermartingale mechanism.

Nevertheless, I recommend **rejection at the requested four-journal level**. The manuscript has not established that its collection of regular likelihood arguments, classical inverse spectral identities, compact-space Laplace bounds, and conservative finite-map estimates constitutes a sufficiently deep new mathematical result. The most credible candidate for such a result is the quantitative connection between observable boundary data, depth, and physical time. That connection is not adequately benchmarked, and its advertised depth scale contains large avoidable losses.

This is not merely the generic objection that the constants are large. In Section 4 below I derive, under the manuscript's own assumptions,

\[
 d_J(\beta,\gamma)
 \le Q^{25(J+1)}
 \max_{0\le r\le4J+8}|h_\beta^{(r)}(0)-h_\gamma^{(r)}(0)|,
\]

in place of its \(Q^{64(J+1)^2}\) bound. With the **same multiscale sampling law**, the resulting response separation satisfies

\[
 D(\beta,\gamma)\ge
 \exp\{-1000F(J+1)^2\}\,\delta^{20(J+1)},
 \qquad d_J(\beta,\gamma)\ge\delta,
\]

where \(F=1+\Lambda T+|\log T|+\log Q\) is the manuscript's box quantity. Its own finite-sample statistical machinery then supports the sufficient regime

\[
 J_n=o(\sqrt{\log n}),
\]

rather than just \(J_n=o((\log n)^{1/3})\), with the same displayed form of shrinking coefficient radius. The derivation is given in full enough detail to audit, and finite exact-arithmetic checks are supplied separately.

**A stronger bound does not falsify a weaker sufficient theorem.** The authors explicitly disclaim optimality. My objection is that the quantitative centerpiece has not yet been analyzed deeply enough to carry the claimed level of significance. Simply replacing one inflated constant by another would not settle that editorial issue.

## 2. Exact scope and publication integrity

### 2.1 One active paper, not an eleven-paper retrospective

The active submission is `ROUND45_REVISION.tex` and its eleven inputs under `round45/`, including the preamble and bibliography. I read those active inputs, the response to Round 44, the proof ledger, historical-reuse map, manifest, verifier, tests, and publication receipt. Older rounds are provenance, not additional active submissions. This report is not a claim to have audited every derivation in the repository's historical branches.

All source references below refer to the frozen distribution SHA above. The source paths and theorem labels in Section 9 identify the evidence independently of changing page numbers.

### 2.2 The old failed-finalizer objection does not apply

The Git comparison from `c67f80f...` to `00fee708...` contains one commit and only seven added distribution artifacts: three build logs, the final TeX log, the PDF, the test log, and `ROUND45_VERIFICATION.json`. No manuscript source changed in that comparison. The workflow directory at the frozen head contains exactly one workflow, `verify-round45.yml`, with `contents: read` and disabled persisted checkout credentials. It does not rewrite the mathematics or push a generated revision.

The receipt names the source commit and reports nineteen checked files, three successful LaTeX passes, a successful six-test suite, and a 26-page PDF. It records the PDF SHA-256 as

```text
b5e520ec98d650373c106cc9e26dd21f7ad6c76b2bced81a04d93ce3f039a94f
```

These are **the author's recorded build results**, not a new build conducted by this reviewer. I checked the source/distribution relationship through GitHub, but did not independently download and hash the PDF or rerun the author's LaTeX build. The mathematical review is source-based, not a PDF layout inspection. The independent computations actually performed are specified in Section 8.

The author correctly states that regression tests and compilation are not proof-assistant verification. It would be unfair to attribute a stronger certification claim to this revision.

### 2.3 A remaining, narrower provenance defect

The verifier's `--source-sha` option is not actually bound to the checked source bytes. `tools/verify_round45.py` validates only that the argument matches forty lowercase hexadecimal characters and then copies it into the receipt. It never resolves the commit or compares the checked files with that Git object. Thus a nonexistent forty-digit SHA passes the argument-validation step; if the other local checks pass, the program has no further mechanism to reject that false source designation.

This is a defect in the **verification mechanism**, not evidence that the supplied `c67f80f...` designation is false: the latter is independently supported by the source/distribution comparison. The remedy is to resolve the source commit, compare each active input and the manifest against it, and require exact coverage of the active input graph. Artifact-only descendants should remain permissible; requiring the distribution HEAD itself to equal the source commit would be the wrong repair. Tests should reject both an invalid source designation and a manifest omitting an active input.

## 3. What has genuinely been repaired

The objection identifiers in the following table are those used by `AUTHOR_RESPONSE_ROUND44.md` and `round45/PROOF_LEDGER.json`.

| Prior obligation | Finding on the frozen Round 45 text |
|---|---|
| M1: composed inverse exponent | Repaired as a conservative bound. For \(j=J+1\ge1\), \(4(2j+1)^2+17j^2\le53j^2\le64j^2\). The old counterexamples at depths 0–3 do not apply. |
| M2: washout derivatives | Repaired. The ordered Duhamel argument retains \((1+\log(i+1))^{|\alpha|}\), then absorbs it using a strictly smaller positive summability margin. |
| M3: zero-time diagnostic cell | Repaired. The finite grid requires exactly \(R_J\) positive-time cells; the origin is known deterministically. |
| M4: finite-map condition audit | The current Gram solves, polynomial norms, quadratic forms, denominators, and ratio estimates are explicit enough to audit. They are excessively conservative, not the old missing calculation. |
| M5: shrinking-net likelihood control | Substantively repaired. A finite-n bound, interpolation mechanism, explicit transient budget, and prior-ball denominator are now supplied and used at the shrinking resolution. |
| M6: policy-uniform no-washout control | Substantively repaired through the \(L^1\) impulse-response metric and the chronological sign decomposition. The actual conditional information is correctly distinguished from its exploration floor. |

### 3.1 The finite-n posterior calculation is internally consistent

In `uniform_statistics.tex`, the score interpolation is controlled by a deterministic metric times the empirical absolute noise. The centered-square interpolation includes the conditional-expectation term. Conditional Gaussian exponential bounds are taken before future actions are observed. These are the right mechanisms for this policy class.

The posterior-separation theorem uses numerator exponent \(-13nq/(32\sigma^2)\), denominator lower exponent \(-3nq/(32\sigma^2)\), and a combined transient cost at most \(nq/(16\sigma^2)\). Their net value is exactly

\[
 -13/32+3/32+1/16=-1/4.
\]

The prior quantity is correctly an **upper** bound on minus log prior mass. The explicit entropy bounds then dominate the relevant shrinking nets under the stated sufficient depth regime. I do not see a fixed-resolution-to-shrinking-resolution interchange left unproved in this argument.

### 3.2 The adaptive statements have the right quantifiers

The no-washout decomposition holds the entire realized action record fixed when evaluating a candidate likelihood. The intercept is measurable before the fresh sign, so its cross term has conditional expectation zero. The convolution bound is common to all histories with the declared input bound. This is a genuine improvement over a policy-specific continuity argument.

The almost-sure assertion is made for each chosen sequence of policies and triangular coupling, using summable common finite-n bounds. It is not an intersection of probability-one events over an uncountable policy class. The Laplace-tracking result follows the complete conditional-information sequence; its cluster LDPs do not require that sequence to converge. Asking for a deterministic information limit would misread the current theorem.

### 3.3 The confidence and Gaussian-image claims are appropriately restricted

Stopping a nonnegative exponential supermartingale at the mth visit, followed by allocation \(\alpha p_q/[m(m+1)]\), is a valid way to handle adaptive visits. The proof does not condition on the terminal visit count and declare the selected errors Gaussian. The data-selected finite cell collection is covered by the underlying countable simultaneous event.

Likewise, the homogeneous BvM theorem approximates a posterior by a random Gaussian law. It does not by itself prove a sampling central limit theorem for its center. The current-state and memory laws are explicitly finite-dimensional Gaussian images, and the operator conclusion is explicitly exponentially weighted. These distinctions should be retained.

These positive findings are not formal certification of every assertion. They explain why the recommendation below is primarily about mathematical contribution, not a repetition of defects that the frozen text no longer contains.

## 4. Major objection R46-1: the quantitative centerpiece contains avoidable structural losses

This section is an independent referee derivation, not a modification of the submitted manuscript and not a claim of priority or minimax optimality. It uses exactly the common scalar damping and coefficient box already assumed in the infinite-Jacobi part.

Retain the manuscript's notation

\[
 B_0=\max\{1,b_++2a_+\},\quad \Lambda=1+c_++B_0,
 \quad Q=8\max\{2,\Lambda,T,T^{-1},a_-^{-1}\},
 \quad j=J+1.
\]

In particular \(Q\ge16\), \(\|A\|\le\Lambda\le Q\), \(1+c_+\le Q\), and \(1+B_0\le Q\). Matrix infinity norms below are induced row-sum norms; polynomial coefficient norms are one-norms.

### 4.1 The response-to-moment inverse has a closed formula

Write \(\mathsf J\) for the stiffness operator to distinguish it from the depth index. The block generator satisfies the exact identity

\[
 A^2+cA=-\operatorname{diag}(\mathsf J,\mathsf J).
\]

With \(v_r=\ell A^{r+1}B=h^{(r+2)}(0)\) and
\(\mu_m=\langle e_0,\mathsf J^m e_0\rangle\), it follows that

\[
 \boxed{\displaystyle
 \mu_m=(-1)^m\sum_{k=0}^m\binom{m}{k}c^{m-k}v_{m+k}.}
 \tag{R46.1}
\]

Indeed, multiply \((A^2+cA)^m\) by \(A\), expand the commuting powers, and apply \(\ell\) and \(B\). On the other hand, applying \(\ell A\operatorname{diag}(\mathsf J^m,\mathsf J^m)B\) gives \(\mu_m\). No analytic continuation or recursive propagation of earlier errors is involved.

For two admissible parameters put \(e=\max_{0\le r\le2M}|v_r-\widetilde v_r|\), with \(M\ge1\). Since \(c=-v_1\), the damping difference is at most \(e\). Also \(|v_r|\le Q^{r+1}\). Subtracting (R46.1) gives, for \(1\le m\le M\),

\[
 |\mu_m-\widetilde\mu_m|
 \le\big[(1+c_+)^m+m2^{m-1}Q^{2m}\big]e
 \le Q^{4m}e.
 \tag{R46.2}
\]

For the last step use \(m2^{m-1}\le4^m\le Q^m\) and
\(Q^m+Q^{3m}\le Q^{4m}\). Thus the moment map costs at most \(Q^{4M}\), not a quadratic exponent in \(M\). This improvement exploits a structural identity of the model, not a different observation assumption.

### 4.2 Orthogonality gives a substantially better Hankel inverse bound

Let \(H_{j-1}=(\mu_{r+s})_{0\le r,s<j}\). Pad the monic coefficient vector of \(p_k\), \(k<j\), with zeros to length \(j\). Orthogonality gives

\[
 \boxed{\displaystyle
 H_{j-1}^{-1}=\sum_{k=0}^{j-1}\rho_k^{-1}p_kp_k^T.}
 \tag{R46.3}
\]

To verify it, stack the padded vectors as the rows of a unitriangular matrix \(P\). Then \(PH_{j-1}P^T=\operatorname{diag}(\rho_0,\ldots,\rho_{j-1})\), and invert this identity.

The submitted proof already establishes \(\|p_k\|_1\le Q^k\) and
\(\rho_k=\prod_{r<k}a_r^2\ge a_-^{2k}\). Therefore

\[
 \|H_{j-1}^{-1}\|_\infty
 \le\sum_{k=0}^{j-1}\|p_k\|_1^2/\rho_k
 \le\sum_{k=0}^{j-1}Q^{4k}
 \le jQ^{4(j-1)}\le Q^{5j}.
 \tag{R46.4}
\]

The cofactor estimate in the manuscript throws away this orthogonal structure and generates an unnecessary quadratic exponent.

Now reuse the manuscript's valid secant identities for the Gram solve, the two quadratic forms, and the ratios, replacing its inverse bound by \(A'_j=Q^{5j}\). Its quantities can then be bounded as follows, for \(j\ge1\):

| Quantity | Valid upper bound |
|---|---:|
| \(S_j=\|p_j\|_1\) | \(Q^j\) |
| \(V'_j=jA'_j(1+jS_j)\) | \(Q^{9j}\) |
| \(R'_j=S_j^2+2B_0^{2j}S_jV'_j\) | \(Q^{13j}\) |
| \(T'_j=S_j^2+2B_0^{2j+1}S_jV'_j\) | \(Q^{14j}\) |
| \((T'_j+b_+R'_j)/a_-^{2j}\) | \(Q^{17j}\) |
| \((R'_{j+1}+a_+^2R'_j)/(2a_-a_-^{2j})\) | \(Q^{15(j+1)}\) |

For completeness, the intermediate exponents in the first three nontrivial rows are at most \(8j+1\), \(12j+1\), and \(12j+2\). The b-ratio is at most \(Q^{16j+1}\). In the a-ratio, cancellation of the factor two against the denominator gives \(Q^{15j+14}\). These imply the table for every \(j\ge1\). At coefficient index zero, \(b_0=\mu_1\) and the a-ratio costs at most \(Q^{14}/2\); no shallow-depth exception is omitted.

Consequently, through depth \(J\), the moment-to-coefficient map costs at most \(Q^{17(J+1)}\). Taking \(M=2J+2\) in (R46.2) and composing gives

\[
 \boxed{\displaystyle
 d_J(\beta,\gamma)\le Q^{25(J+1)}
 \max_{0\le r\le4J+8}|h_\beta^{(r)}(0)-h_\gamma^{(r)}(0)|.}
 \tag{R46.5}
\]

Derivatives only through \(4J+6\) are needed; retaining the manuscript's \(4J+8\) grid is harmless. The calculation applies to infinite operators because every identity used is a finite moment identity, with bounds uniform in the unspecified tail.

### 4.3 The finite-grid inverse also admits an exponential, not factorial, bound

For \(V_R=(k^r/r!)_{0\le k,r\le R}\), let \(C_R=\|V_R^{-1}\|_\infty\). The Lagrange polynomial at node \(k\) is

\[
 L_k(x)=\frac{\prod_{0\le l\le R,\ l\ne k}(x-l)}{\prod_{l\ne k}(k-l)}.
\]

Its contribution to the rth row of \(V_R^{-1}\) is \(r![x^r]L_k(x)\). Since \(r!\le R^r\), the absolute value of this contribution is at most

\[
 \frac{\prod_{l\ne k}(R+l)}{k!(R-k)!}
 \le\frac{(2R)!/R!}{k!(R-k)!}.
\]

The first inequality follows by evaluating the polynomial with absolute coefficients at \(R\); its coefficients have alternating signs before taking absolute values. Summing over \(k\) proves

\[
 \boxed{C_R\le2^R\binom{2R}{R}\le8^R.}
 \tag{R46.6}
\]

In particular, the submitted remainder constant obeys

\[
 H_R=\frac{C_R(2e^{\Lambda T}\Lambda^R)R^{R+1}}{(R+1)!}
 \le2e^{\Lambda T+1}(8e\Lambda)^R.
 \tag{R46.7}
\]

Here it is essential not to discard the factorial in the Taylor remainder before accounting for its cancellation.

### 4.4 Consequence for the existing sampling distribution and depth scale

Keep the submitted labels, weights, \(R=4J+8\), and \(\zeta_R=\min(1,T/(2R))\). Set \(L'_J=Q^{25j}\), and choose the least positive \(s\) such that
\(H_R\zeta_R2^{-s}\le\delta/(2L'_J)\). Every such cell already belongs to the manuscript's sampling law; this is not an alternative experiment.

Its own finite-grid argument gives

\[
 D\ge K'_J\delta^{2R+3},\qquad
 K'_J=\frac{2^{-J-4}}{R\zeta_R C_R^2(L'_J)^2(Z'_J)^{2R+1}},
 \quad Z'_J=\max\{2/\zeta_R,4L'_JH_R\}.
\]

Use the same \(F=1+\Lambda T+|\log T|+\log Q\) as the article. For \(j\ge1\), the preceding bounds imply

\[
 \log C_R\le8jF,\quad \log\zeta_R^{-1}\le jF,
 \quad \log H_R\le17jF,\quad \log Z'_J\le43jF.
\]

For example, \(\log\zeta_R^{-1}\le\log(16j)+|\log T|\le jF\), and
\(\log H_R\le F+R(1+\log8+\log\Lambda)\le17jF\). Dropping the nonpositive \(\log\zeta_R\) term in \(-\log K'_J\) yields

\[
 -\log K'_J
 \le12jF+16jF+50jF+(16j+1)43jF
 =(688j^2+121j)F\le809j^2F.
\]

Since \(2R+3\le20j\) and \(0<\delta\le1\), this proves the convenient bound

\[
 \boxed{D\ge e^{-1000Fj^2}\delta^{20j}.}
 \tag{R46.8}
\]

With an exploration floor bounded away from zero and the article's choice
\(\delta_n=\exp\{-\eta\log n/(80j_n)\}\), take
\(q_n=\rho_n a^2e^{-1000Fj_n^2}\delta_n^{20j_n}\).
If \(j_n^2=o(\log n)\), then

\[
 q_n\ge n^{-\eta/4-o(1)},\qquad
 nq_n^2\ge n^{1-\eta/2-o(1)}.
\]

Both required entropy and negative-log-prior-mass terms remain \(O((\log n)^2)\). Thus the already-proved finite-n posterior inequality yields shrinking coefficient recovery for \(J_n=o(\sqrt{\log n})\). No new probabilistic lemma is necessary.

This is a sufficient improvement, not an optimality theorem. It nevertheless changes the depth exponent without changing the assumptions or the sampling law. An account of the genuine depth obstruction is therefore essential to the paper's significance. The authors should not present the cubic-depth audit as the culmination of the available structure.

## 5. Major objection R46-2: the closest relevant literature is not compared

The active bibliography has four entries. Those entries are pertinent, and the introduction correctly acknowledges several classical ingredients. The problem is not the number four as such; it is the omission of directly relevant comparisons.

Du, Nair and Janson, *Bernstein–von Mises for Adaptively Collected Data* (NeurIPS 2025; arXiv:2511.06639), already establish an adaptive Gaussian posterior approximation in linear regression without the usual stability assumption needed for frequentist validity. Their Theorem 1 allows a random design and imposes growth conditions on its information eigenvalues rather than a deterministic limiting information matrix. Their distinction between posterior Gaussian approximation and frequentist coverage is directly relevant here. **This does not subsume the submitted nonlinear mechanical theorem with its uniform nuisance treatment.** It does mean that “adaptive BvM without information convergence” cannot serve as an unqualified conceptual novelty claim. The manuscript needs a theorem-by-theorem account of what its nonlinear, policy-uniform, and transient-robust formulation adds. [P1]

Mikhaylov and Mikhaylov's *Dynamic inverse problem for Jacobi matrices* treats reconstruction of semi-infinite Jacobi matrices from discrete-time boundary dynamics. Their related work on Jacobi dynamics and classical moment problems connects finite dynamic response data, moments, Hankel-type matrices, and finite-block reconstruction. **Their discrete-time deterministic setting differs from the present continuous-time damped, noisy, adaptive experiment.** These papers do not by themselves dispose of the present statistical contribution, but they are much closer comparisons for the claimed response–moment–Jacobi mechanism than a general inverse-spectral textbook alone. [P2, P3]

The manuscript already cites Vollmer for transferring regression results through inverse stability, Shalizi for dependent-data Bayesian asymptotics, and Howard and coauthors for confidence sequences. I am not asking the authors to pretend those citations are absent. The additional obligation is to isolate the genuinely new theorem after accounting for these existing ingredients and the closer comparisons above.

This targeted search is not an exhaustive priority investigation. I make no allegation of copying or deliberate omission. The present novelty case is simply inadequate for the venue standard requested.

## 6. Major objection R46-3: the paper does not yet identify the substantive inference frontier

The most interesting result is the no-washout mechanism: a fresh sign retains a response-information floor despite arbitrary bounded predictable baselines, and the complete input is controlled through an impulse-response metric. That could anchor a focused contribution. In the present submission it is surrounded by many consequences whose mathematical novelty is limited once that mechanism and a uniform likelihood estimate have been established.

The compact posterior LDP is a useful consequence, but the proof is an elementary Laplace argument after uniform likelihood tracking. The cluster-LDP extension correctly handles nonconvergent information, yet is largely a consequence of equicontinuity and compactness. The strong filter-jet estimates arise from exponential deterministic forgetting combined with derivatives of a normalized tilt. The memory posterior is a smooth image of five-dimensional regular inference, not a new infinite-dimensional Gaussian limit. The article now states these restrictions honestly; honesty about scope does not itself make the consequences deep new theorems.

The weighted operator result is also correct in its stated topology. On the uniformly bounded Jacobi box, the metric
\(\|W_\tau(\mathsf J_\beta-\mathsf J_\gamma)W_\tau\|\)
induces the product topology of the Jacobi coefficients: weighted norm convergence implies entrywise convergence by testing fixed basis vectors, and entrywise convergence implies weighted norm convergence by a finite-prefix/tail split. Damping must be included separately. Thus this is a useful quantitative repackaging of coefficient recovery, not an independent strengthening to ordinary operator-norm identification.

A compelling centerpiece would need to explain a real limitation or capability of boundary inference. For example, how does distinguishability deteriorate with depth and elapsed physical time under the allowed forcing? Which part of that deterioration is unavoidable, and which is created by the multiscale allocation or monomial coordinates? Does feedback improve achievable depth, or does the theorem merely guarantee robustness to it? What changes when one asks for a matching actual information rate rather than a floor? The current paper does not resolve these questions.

I do not impose a universal rule that every top-journal paper must contain a minimax theorem, simulations, or an optimal controller. Here, however, once the classical identities and regular posterior arguments are separated out, the quantitative depth claim is the principal proposed source of exceptional significance. Section 4 shows that its current form is not a reliable description of the underlying frontier. A new result addressing that frontier, or another comparably substantive advance, is needed; adding more routine corollaries is not a substitute.

## 7. Required changes before the work can be reassessed on its merits

**First, rebuild the mathematical positioning.** State precisely what is new relative to adaptive random-information BvM results and dynamic Jacobi boundary reconstruction. Separate the classical deterministic engine, the regular posterior machinery, and the model-specific adaptive inference theorem. Do not claim that the comparison papers prove the same theorem when they do not.

**Second, replace the avoidably weak condition analysis and investigate what remains.** Equations (R46.1)–(R46.8) provide a concrete audit target. Verify or improve them independently, propagate the corrected geometry through the rates and confidence thresholds, and explain whether any resulting depth scale reflects information limits rather than bookkeeping. This is not a demand to declare the existing sufficient theorem false.

**Third, make the operational content explicit.** For a selected depth and coefficient radius, give an interpretable finite observation/physical-time requirement using the declared probe law and the actual probability bound. For confidence cylinders, distinguish simultaneous coverage, sufficient shrinking diameter, and computational construction of the set. The current implicit set is mathematically legitimate; it is not automatically an implemented finite algorithm.

**Fourth, harden source-bound verification.** Resolve the named source commit and compare the active input graph and all relevant blobs to it. Preserve the valid separation between source freeze and artifact publication. Keep exact finite tests explicitly subordinate to written analytic proofs.

For a specialist venue, a substantially sharper and better-positioned paper centered on policy-uniform no-washout boundary identification might merit a different assessment. That is not a prediction of acceptance. For the four journals requested, the current revision does not establish the requisite case, and I would not recommend acceptance or a merely cosmetic revision.

## 8. Independent checks actually performed

The accompanying `reviews/round46/independent_checks.py` is a standalone standard-library Python program. It imports no author test module and does not modify manuscript files. Its recorded output is `reviews/round46/INDEPENDENT_CHECKS.json`.

The executed checks all passed:

- Twelve rational coefficient/damping configurations verify the block identity and the closed moment formula through moment order 12 and response-jet index 24.
- Twenty-eight exact Hankel cases, with matrix dimensions 1–7, verify the orthogonal-polynomial inverse identity, the product norms, and coefficient reconstruction.
- Exact inversions for \(R=1,\ldots,16\) verify the sharper Vandermonde row-sum bound.
- Polynomial coefficient certificates check the relevant all-depth exponent comparisons after substituting \(j=z+1\); the old Round 43 failure depths are retained explicitly and distinguished from the repaired Round 45 inequality.
- Exact fractions check the current posterior exponent arithmetic and the telescoping confidence-error allocation.

Reproduce from the review branch with:

```sh
python3 reviews/round46/independent_checks.py --output /tmp/round46-checks.json
```

The script SHA-256 is:

```text
ed7a7b6f915a54c767d602947d574a649e04d9b4f19b2bad983e3d4e7b02be3e
```

Finite examples are regression checks, not proofs for all depths. The exact polynomial certificates establish the specified polynomial inequalities, not the entire analytic argument. The all-depth identities and estimates are justified in Section 4. No adaptive-policy simulation, empirical coverage experiment, author test-suite rerun, or independent PDF compilation is claimed.

## 9. Source anchors and primary references

### Frozen manuscript anchors

Every path in this table is relative to `TrillionniumFoundation/theta-theory` at commit `00fee70834ee5e2a1fadc55c5d118a23a4637477`.

| Path | Relevant labels or content |
|---|---|
| `ROUND45_REVISION.tex` | Title, abstract, complete active input graph |
| `round45/introduction.tex` | Advertised inverse bound, growth rate, scope, and novelty discussion |
| `round45/triangular.tex` | `ass:triangular`, `lem:nuisance-budget`, `lem:sobolev-score`, `thm:abstract-bvm` |
| `round45/lattice.tex` | `thm:jet-embedding`, `prop:balanced-contrast`, `thm:lattice-bvm` |
| `round45/filter_memory.tex` | `lem:strong-pushforward`, `thm:filter-jets`, `cor:memory-posterior`, `thm:preparation-mixture` |
| `round45/uniform_statistics.tex` | `prop:finite-n-field-concentration`, `lem:finite-n-exact-correction`, `thm:finite-n-posterior-separation`, `thm:adaptive-laplace-tracking` |
| `round45/infinite_jacobi.tex` | `eq:jacobi-parameter`, `thm:jacobi-reconstruction`, `lem:washout-derivatives`, `thm:jacobi-rate` |
| `round45/inverse_stability.tex` | `lem:response-moment-triangularity`, `prop:effective-gram-reconstruction`, `lem:effective-response-jet`, `lem:finite-grid-certificate`, `thm:effective-jacobi-stability` |
| `round45/linear_time_protocol.tex` | `eq:policy-controlling-metric`, `lem:predictable-intercept-information`, `thm:linear-time-adaptive-jacobi` |
| `round45/growing_depth_uncertainty.tex` | `lem:jacobi-boundary-locality`, `thm:growing-depth-recovery`, `cor:weighted-operator-recovery`, `thm:honest-jacobi-cylinders` |
| `round45/references.tex` | The four-item active bibliography |
| `AUTHOR_RESPONSE_ROUND44.md`, `round45/PROOF_LEDGER.json` | Claimed repairs and their M1–M6 identifiers |
| `round45/SOURCE_MANIFEST.json`, `ROUND45_VERIFICATION.json` | Source manifest and author publication receipt |
| `tools/verify_round45.py`, `tests/test_round45.py`, `.github/workflows/verify-round45.yml` | Actual verification scope and the unbound source-SHA argument |

Canonical source entry: <https://github.com/TrillionniumFoundation/theta-theory/blob/00fee70834ee5e2a1fadc55c5d118a23a4637477/ROUND45_REVISION.tex>.

### Primary literature used for the targeted comparison

**[P1]** Kevin Du, Yash Nair, Lucas Janson, *Bernstein–von Mises for Adaptively Collected Data*, NeurIPS 2025. Theorem 1 and the discussion distinguishing posterior approximation from frequentist validity. arXiv:2511.06639. <https://arxiv.org/abs/2511.06639>. Official proceedings: <https://papers.nips.cc/paper_files/paper/2025/file/a3086f0efcb7221f8de434c21e0bab6b-Paper-Conference.pdf>.

**[P2]** A. S. Mikhaylov and V. S. Mikhaylov, *Dynamic inverse problem for Jacobi matrices*, Inverse Problems and Imaging 13(3) (2019), 431–447. DOI: 10.3934/ipi.2019021. <https://www.aimsciences.org/article/doi/10.3934/ipi.2019021>.

**[P3]** Alexander Mikhaylov and Victor Mikhaylov, *Dynamic inverse problem for special system associated with Jacobi matrices and classical moment problems*, arXiv:1907.11153, version 1, 2019. Sections 2–3, including the dynamic-data/moment relationship and finite reconstruction. <https://arxiv.org/html/1907.11153v1>.

The four references already cited by the manuscript remain relevant: Teschl's Jacobi-operator monograph; Vollmer, arXiv:1302.4101; Shalizi, DOI 10.1214/09-EJS485; and Howard, Ramdas, McAuliffe and Sekhon, DOI 10.1214/20-AOS1991. This report does not treat acknowledged background as an undisclosed contribution.

---

## Final recommendation

**Reject at the requested Annals–Inventiones–JAMS–Acta level.** Round 45 has repaired substantial correctness and publication defects, and this review does not establish that its current main conclusions are false. What remains insufficient is the demonstrated originality and depth of the central contribution. The sharpenings above show that the advertised quantitative scale is not yet the product of a sufficiently searching analysis. A stronger mathematical centerpiece and a precise comparison with the nearest prior work are required, not another assertion that a proof ledger has closed every question.
