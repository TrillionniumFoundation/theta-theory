# Independent harsh referee-style report on A2 v16

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.

**Review date:** 11 September 2026. **Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society.

**Author branch:** `revision/a2-v16-integrated-submission-2026-09-11`.

**Immutable source reviewed:** `bd27ed3208cc869f6c7a6547453a2557bfcd03ed`, committed at 2026-09-11 02:37:39 UTC. The manuscript root is `papers/A2-v16-integrated-submission/`. Source paths below are relative to that root unless stated otherwise. The preceding v15 report is pinned at `a108adf17c4b9360e340a2d5708b20a375d69283`.

This is an author-requested, AI-assisted independent referee-style assessment. It is not a journal-commissioned report, an editorial decision, or a certification by one of the journals named above. The reading boundary and executed evidence are recorded in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). Statements about inspected proofs must not be expanded into a certification of every retained historical appendix.

## 1. Recommendation to an editor

**Recommendation: reject at the requested four-journal level.** I do not recommend acceptance, conditional acceptance, or a routine major revision with an implied path to acceptance.

The principal reason is the remaining gap between the manuscript's demonstrated mathematical contribution and the significance needed to justify this exceptionally demanding target. This is an editorial assessment, not a newly discovered contradiction in a theorem. The recommendation would remain negative if the complete native manuscript compiled cleanly today.

The revision is substantially more disciplined than a paper which confuses a classical scalar coordinate with a new rigidity invariant. It states the relevant restrictions, separates finite-jet recovery from the function-valued problem, preserves failed preparations, and treats adaptive stopping correctly in the new sections. I found **no demonstrated fatal mathematical error in the v16 additions or in the core proof chain examined here**. That conclusion is deliberately narrower than declaring the entire large retained manuscript verified.

There is a genuine technical paper here. Its strongest part is the smooth, physical, relatively normalized long-bridge theorem on a common nonshrinking collar, together with a specified observable boundary invariant. The independent-contact inverse and its physical realization also deserve mathematical credit. But v16's additional stopped-transcript and common-support calculations do not establish a new geometric rigidity mechanism or a sharp statistical principle. They mostly complete the operational consequences of the already established single-record estimate.

The full native main build remains unverified. This is an independent submission-readiness issue, not the mathematical basis for rejection. The author has not falsely advertised it as completed.

## 2. What changed, and what should not be reopened

The principal v16 additions are `article/17_adaptive_experiments.tex`, `article/31_adaptive_critical.tex`, and `article/16c_strict_margin.tex`; the fixed-design physical comparison is now explicitly part of the main route. The response and build driver are also new or updated components of this checkpoint.

| Item | Assessment in this review |
| --- | --- |
| Stopped adaptive physical transfer, `thm:v16-adaptive-transfer` | Correct under the printed bounded-cap, fresh-preparation, common-policy and admissible-collar assumptions. A useful consequence, not a new coupling principle. |
| Charged pilot comparison, `cor:v16-pilot-transfer` | The exceptional event and the valid fallback kernel are handled correctly; the boundary expression is not illicitly evaluated outside its collar. |
| Adaptive tangent overlap, `thm:v16-adaptive-critical` | The product is averaged under the normalized common-history process, and reverse randomization uses its product-weighted law. These distinctions are essential and are present. |
| Critical limit, `cor:v16-adaptive-critical-limit` | Correct for the stated convergence of the accumulated hazard under the auxiliary common-history law, together with the physical approximation error. |
| Strict-margin example, `prop:v16-strict-margin` | Correct; explicitly attributed to the previous review. It is not a billiard realization or a new linearization theorem. |
| Classical scalar linearization versus physical amplitude identification | The earlier distinction remains repaired. The Schur-concatenation argument identifies the physical amplitude rather than assuming the identification. |
| Curvature ratios, one-flight factors and two-flight multipliers | The repaired notation is retained. I do not reopen the old multiplier objection. |
| Full native main build | Still not verified; see Section 7. |

A severe review should not manufacture fresh errors merely because the requested recommendation is severe. Conversely, the absence of a new fatal error does not create an obligation to recommend publication at this level.

## 3. Audit of the strongest mathematical route

### 3.1 Localization, physical phase measure and relative normalization

The proof route in `v3/10_geometry_action.tex`, `v3/20_integration.tex`, and `v4/10_boundary_layers.tex` is materially stronger than a fixed-flight Taylor expansion.

The shortest-channel localization uses positive separation, strict convexity, and separation of the finitely many relevant outgoing normal states. A sum of flight lengths with total excess at most a fixed collar forces every individual flight into a short-channel neighborhood. Specular reflection then selects the reversed channel. The argument does not accumulate an error proportional to the number of impacts. The claim about a selected nonminimal channel is distinguished from exhaustion of an unselected count event.

The physical normalization is also not an arbitrary transverse ensemble. First variation and cancellation of the arclength factors yield

\[
 d\mu=\frac{-W_{j,uv}}{2\pi A}\,du\,dv\,dr.
\]

The small excess is less than the minimum roof, so the previous flight does not truncate the initial residual interval and another flight cannot fit after the selected last impact. The source's use of this full-phase measure is justified by the inspected local argument; finite horizon is not needed for this step. See `eq:g-full-flux` and the proof following `lem:g-radial`.

The decisive relative estimate is obtained from the exact cofactor identity

\[
 -W_{j,uv}=\frac{\prod_i[-\ell_{i,uv}]}{\det H_{\mathrm{int}}},
\]

normalized by its value at the normal orbit **before** approximation. Endpoint localization gives a dimension-independent trace-norm estimate for the nonlinear Hessian perturbation. The logarithmic determinant series retains a trace-class factor after every fixed number of differentiations. This avoids the invalid alternative of dividing a merely absolute action error by an exponentially small reference twist. See `eq:v3-cofactor`, `eq:v3-logdet`, and `eq:v4-finite-log`.

The two retained endpoint blocks in `thm:v4-factorization` are separated by a growing middle interval. Perturbation tails are estimated in trace norm, while the Green kernel compares each retained block with its half-line limit. The fixed strict exponential margin absorbs polynomial factors arising at each fixed derivative order. The constants may use higher boundary norms; the theorem is not a finite-regularity estimate with all constants controlled by one unspecified low norm.

Finally, `lem:g-radial` and `thm:v4-law` use uniformly positive endpoint Hessians to put the residual integrals on a common Morse domain. Odd Taylor terms vanish after integration, giving the smooth right-hand dependence on the offset. The source accounts for the additional endpoint derivatives needed by each fixed offset derivative. No differentiation of an uncontrolled moving indicator is required.

**Assessment:** this is the strongest part of the submission. I have not found a failure in the inspected argument, and I have not located a cited theorem which automatically supplies this whole smooth, uniform, phase-normalized package. It would be inaccurate to dismiss the entire result as already proved by a scalar linearization theorem.

### 3.2 What the classical comparison does and does not show

The analytic normal form in De Simoi–Kaloshin–Leguil, Section 2, provides the local model

\[
 N(s,p)=(\Delta(sp)s,\Delta(sp)^{-1}p).
\]

Their paper distinguishes this local mechanism from the additional symmetry and reconstruction steps of its marked-length inverse problem [L1]. The manuscript's `prop:v14-normal-form` performs the mixed-boundary calculation rather than attributing a physical probability theorem to that source. In particular, its physical flux is

\[
 J_n=\left|\frac{T_n}{\det D\Phi_n}\right|,
 \qquad T_n=\frac{\Delta(I)^n}{1-nI\Delta'(I)/\Delta(I)}.
\]

Dropping the projection determinant would change the physical amplitude. The source does not drop it. Its exact normal-orbit value also agrees with the alternating Jacobi formula after setting the number of flights to twice the number of returns.

In the smooth scalar problem, hyperbolic one-dimensional linearization is classical; the low-regularity counterexamples discussed by Eynard-Bontemps–Navas do not refute the smooth theorem used here [L2]. The elementary product proof in `article/16a_scalar_linearization.tex` is valid. The subsequent physical Schur identity in `article/16_hyperbolic_coordinates.tex` supplies the additional identification

\[
 B_{1-b}(\varphi_b(u))\varphi_b'(u)=r_bB_b(u).
\]

There is no circular claim that this scalar identity first proves the finite relative bridge law. The source obtains it from that law and exact concatenation.

The strict-margin family in v16 reinforces the distinction between a contraction multiplier and a uniform mixed-parameter rate. Direct differentiation gives

\[
 \left.\partial_\lambda\partial_a
 [\lambda^{-n}R_{\lambda,a}^n(u)-z_a(u)]\right|_{a=0}
 =n\lambda^{n-1}u^2.
\]

Thus a bound with a fixed constant times \(\lambda_+^n\) fails for that mixed derivative at the endpoint of the parameter box; every strictly slower exponential absorbs the polynomial. The independently executed rational checks agree with the source. This is a correct benchmark, not an additional rigidity theorem.

### 3.3 Geometry: real inverse content, but a restricted target

The all-order block in `thm:v12-two-contact` has an antisymmetric eigenfactor

\[
 m\tanh((m-1)\gamma)-(m-1)\tanh(m\gamma)>0.
\]

Strict concavity of the hyperbolic tangent gives the positivity. The unequal-curvature factors are not optional: the identity relating the two endpoint scales places them in the correct diagonal factor of the block. The inspected calculation includes the amplitude variation, not just the variation of the stationary length.

The two-flight proof in `article/29_two_flight_benchmark.tex` is particularly informative. Eliminating the intermediate impact gives the printed two-by-two Schur Hessian. Varying the opposite contact also varies the normalized twist; its contribution supplies the factor \(2mz\). The separating factor is

\[
 (1+2z)^m-(1+2mz)=\sum_{r=2}^m\binom mr(2z)^r>0,
 \qquad z=c_0c_1-1.
\]

I independently checked the Schur scales, the moment contribution, and the equal-curvature quartic block, whose antisymmetric magnitude is \(1/48\) at the printed normalization. Equal curvatures do not destroy this inverse.

The support-function construction in `thm:v12-realization` also has meaningful content. Opposite-normal perturbations begin at different orders, and the area compensator begins beyond the targeted jets. Consequently the selected gap, free area, and labelled curvatures can remain fixed while the targeted contact jets vary independently. This constructs finite-dimensional physical alternatives; it is not merely a formal jet example.

The limits of the conclusion are nevertheless important. The graph inverse assumes individually even contacts and supplied labelled leading geometry. It does not establish the analogous inverse for arbitrary asymmetric contacts. The analytic continuation argument determines participating analytic boundaries from exact germs; it is not a stability statement for distant boundary points under noise. The finite-window parametric lower bound is for the specified finite family and allowed windows.

The two-flight and limiting coefficients give equivalent **fixed finite-jet coordinates**. This defeats any argument that long records are necessary for that fixed finite-dimensional recovery. It does **not** prove equivalence of the complete noisy smooth experiments, and I do not use it to dismiss the function-valued boundary problem.

### 3.4 Complete profiles, inverse norms and acquisition

The full-profile uniqueness proof in `article/20_boundary_compatibility.tex` is a genuine smooth-function argument, not an identity theorem applied to formal Taylor series. With \(f=k-\widetilde k\) and \(a=k+\widetilde k\), equality of the self-convolutions gives \(a*f=0\). Convolution with \(x^{-1/2}\) and differentiation reduce this to a Volterra equation with bounded remainder kernel. Gronwall then yields uniqueness.

The Abel flux norm in `article/21_abel_stability.tex` is explicitly a linear transform seminorm whose affine nullspace disappears on the physical flux class. The weighted Volterra estimate establishes the stated two-sided control. It would be wrong to replace this norm by raw uniform probability error without regularization. The manuscript does not make that replacement.

In `article/28_regularized_observation.tex`, the limiting candidate flux gains two derivatives. The positive-node reconstruction consequently yields

\[
 \|\widehat V-V\|_\infty
 \le C\{h^{m-1/2}+\tau^j+t h^{-5/2}+\delta\}.
\]

The smooth bridge bias is treated in its \(C^3\) norm; only scalar sampling noise incurs the mesh amplification. Substituting \(h\asymp\varepsilon^{1/(m-1/2)}\), \(t\asymp\varepsilon h^{5/2}\), and the least admissible even \(j\) gives the printed sufficient exponent

\[
 2+\frac{6}{m-1/2}+\frac{\gamma}{|\log\tau|}.
\]

The plug-in calibration argument correctly translates the integrated flux before reconstruction; it does not introduce a spurious gap-error term divided by the offset. I inspected that argument and its use of the stated pilot lemma. I did **not** independently re-prove the entire inherited pilot lemma or all retained nuisance lower bounds; the audit records this boundary.

The geometric inverse and this profile inverse must not be merged into a stronger unproved statement. A symmetrized energy profile, equivalently the normalized stable-action width, does not by itself provide the manuscript with a theorem determining arbitrary asymmetric billiard contacts. Conversely, abstract nonuniqueness of two branches with prescribed width is not automatically a physically realized billiard nonuniqueness theorem. Neither direction may be asserted without its own argument.

## 4. Independent audit of the new adaptive mathematics

### 4.1 Why the stopped-kernel estimate is valid

Let \(D_i\) be the event that the first discrepancy in a sequential coupling occurs at observation \(i\). Before that discrepancy the histories, policy randomization, designs and stop decisions agree. Conditional maximal coupling bounds the next discrepancy by the one-step error. The common-history subprobability is dominated by the full physical-history law. Summing the disjoint first-discrepancy events therefore gives

\[
 \|P^\pi-Q^\pi\|_{\rm TV}
 \le \min\left\{1,\mathbb E_{P^\pi}
            \sum_{i\le T} e(a_i)\right\}.
\]

This is valid for the capped stopping rule; there is no need to pretend the adaptive observations are an independent product with deterministic factors. The reverse marginal version follows by the same construction. The measurable-coupling assumption is printed, and the physical models admit the density/common-part construction in their endpoint-time representation. Parameter dependence of a coupling used in a proof is not an observation of that parameter by the policy.

The event \(\{T\ge i\}\) and the chosen design are determined before the next fresh outcome. Thus

\[
 \mathbb E_P\sum_{i\le T}p(a_i)\tau^{j(a_i)}
 =\mathbb E_P\sum_{i\le T}Y_i\tau^{j(a_i)}.
\]

For \(j(a_i)\ge J\) and stopping no later than the kth success, the last sum is bounded pathwise by \(k\tau^J\). This does not make failures free: the raw preparation charge remains \(T\), and the source retains both failures and the stopping time in the transcript. It also does not justify an uncapped infinite stopping-time theorem without an additional limit argument.

The pilot corollary keeps the pilot exact in both experiments, uses the admissible comparison only on its good event, and bounds the remaining probability by the pilot failure allowance. The use of a specified valid kernel on bad histories is essential. I found no omitted charge or illicit boundary-model evaluation in this argument.

**Contribution assessment:** the nontrivial billiard input is the previously proved relative single-preparation error \(Cp\tau^j\). The passage to a stopped policy is an elementary but correctly executed coupling argument. Calling this passage a new general theory of adaptive experiments would overstate its content.

### 4.2 Why the adaptive overlap is not an ordinary product formula

For the fixed known binary tangent pair, let \(C_a\) be the equal common restriction, \(h(a)\) its missing mass, and \(R_a=C_a/(1-h(a))\). Running the policy under the common kernels produces an auxiliary transcript law \(R^\pi\). The actual common transcript measure is

\[
 Z\,dR^\pi,\qquad Z=\prod_{i\le T}(1-h(a_i)).
\]

Because an exclusive record remains in the full retained history, a transcript that has become exclusive cannot later become common again. Therefore

\[
 m_\pi=\mathbb E_{R^\pi}Z,
 \qquad \|P^{0,\pi}-Q^{0,\pi}\|_{\rm TV}=1-m_\pi.
\]

The reverse kernel for an erasure must draw from \(Z\,dR^\pi/m_\pi\), not from \(R^\pi\). The manuscript makes this distinction explicitly. The randomizations can depend on the known table and design, but not on the binary hypothesis. Hence the result is not a parameter-free equivalence between experiments for two unknown billiard tables.

The physical approximation uses separate stopped comparisons on the two sides of the binary pair and then the reverse triangle inequality. The two expectations in its error term need not be taken under the same physical marginal. They are correctly kept separate in the source.

### 4.3 A fresh exact negative control

The following example was constructed and checked for this review. It is a **negative control against a tempting shortcut, not a counterexample to v16**.

Each action has two common symbols, each of mass \((1-h)/2\), and one hypothesis-exclusive symbol of mass \(h\). The auxiliary common kernel is uniform on the two common symbols. Take three observations. The initial action has hazard \(1/5\). If its common symbol is the first symbol, use hazard \(1/10\) for both remaining actions; otherwise use hazard \(2/5\) for both.

Then

\[
 m=\frac45\frac{(9/10)^2+(3/5)^2}{2}
   =\frac{117}{250}.
\]

Multiplying the unconditional common masses instead would give

\[
 \frac45\left(1-\frac{1/10+2/5}{2}\right)^2
 =\frac9{20}\ne\frac{117}{250}.
\]

Conditional on a common transcript, the first common symbol has probability \(9/13\), not \(1/2\). The latter is its probability under the unweighted auxiliary law. Thus this one example separately checks the expectation-of-product issue and the reverse-randomization weight. The exact total variation and equal-prior testing error are respectively \(133/250\) and \(117/500\).

The source uses the correct formula. Replacing it by the shortcut would introduce an error that is not present in the submitted revision.

### 4.4 Critical scaling: the law under which the limit is taken matters

The logarithmic estimate used in the source is sufficient:

\[
 0\le -\log(1-x)-x\le\frac{x^2}{2(1-x)}.
\]

If the maximum hazard tends to zero and the sum of hazards converges in probability to a deterministic finite \(b\), both under the relevant common-history laws, then \(Z\) converges in probability to \(e^{-b}\). Boundedness of \(Z\) passes this to expectations. For \(b=\infty\), the upper bound \(Z\le e^{-\sum h}\) suffices. Together with the physical approximation error, this gives the printed critical profile.

A useful boundary of the statement is the random-hazard case. If instead the accumulated hazard converges in distribution to a finite nonnegative random variable \(B\), with the maximum hazard negligible, the same calculation gives a common-mass limit \(\mathbb E e^{-B}\), not generally \(e^{-\mathbb E B}\). This is an elementary extension/clarification, not a missing assumption in the manuscript: the manuscript specifies a deterministic limiting \(b\). Its importance here is to prevent an unjustified operational interpretation of the result as depending only on an average sample budget.

## 5. Why the four-journal significance objection remains

The author now states many of the qualifications correctly. The remaining objection is therefore not cured by printing the same qualifications again.

**First, the highest-value theorem is a uniform physical refinement of a well-understood local hyperbolic mechanism.** The relative normalization and simultaneous geometric/offset estimates are real work. But the present submission has not persuaded me that this refinement produces a sufficiently deep change in the broader understanding of billiard rigidity or local dynamics to carry the requested venue. This is a judgment about impact, not an assertion that a pointwise analytic normal form already proves every smooth-family estimate.

**Second, the geometric and function-valued targets have different strengths.** The strongest geometric reconstruction is restricted to even contacts with supplied labelled leading data. The unrestricted smooth invariant is a symmetrized weighted energy datum. The latter is complete for its defined observable target, not a complete classification of asymmetric contact geometry. A paper cannot obtain the force of a general geometric rigidity theorem by alternating between these two meanings of completeness. The revision is careful about this distinction, but the limitation still matters to significance.

**Third, the simpler finite experiment removes one possible claim of necessity.** Two flights already give the fixed-order even-contact inverse. The limiting coefficients are a second coordinate system on that finite-jet image. The long-bridge theorem must therefore earn its significance through its genuinely function-valued, uniform physical content, not through a claim that finite-jet recovery requires arbitrarily long records. The source accepts this point; it is not an unresolved proof objection.

**Fourth, the acquisition theorem is a sufficient construction, not an intrinsic information law.** Its exponent contains a supplied convergence certificate and changes when that certificate is weakened. The procedure has a finite dictionary and preparation guarantee, not a computation-time guarantee. The inspected finite-family parametric lower bound does not close the physical infinite-dimensional minimax problem. Sharp statistical optimality is not a universal prerequisite for a top-journal paper; it simply cannot be counted as a contribution of this one.

**Fifth, the v16 additions do not change these facts.** A sequential coupling lemma plus the existing \(Cp\tau^j\) bound yields the adaptive transfer. A common-submeasure decomposition yields the tangent erasure experiment. The strict-margin example is already attributed to the earlier review. These additions improve completeness and correctness of use, but do not by themselves supply the missing conceptual advance.

For comparison, the finite-horizon enriched marked-length rigidity setting of Finamore–Leguil is a different observation problem [L3]. It cannot simply be used as a theorem subsuming the present probability law, nor can the present local law be advertised as solving that global enriched-spectrum problem. My literature comparison is deliberately scoped and is not a claim to have proved the absence of all related work.

I do not demand that the authors delete mathematical content, abandon their program, or append an unrelated difficult theorem. A response may challenge this editorial assessment by explaining the significance of results already proved. What is not adequate is treating every added consequence, repaired convention, and additional test count as another independent breakthrough. The proposed venue must be justified by the contribution remaining after those dependencies are accounted for.

## 6. Disposition of earlier comments and current findings

| Identifier | Type | Disposition / required action |
| --- | --- | --- |
| C14-1, classical scalar comparison | Earlier positioning/correctness distinction | **Closed and retained closed.** The scalar theorem and the physical amplitude identification are separated. |
| C14-2, multiplier notation | Earlier mathematical presentation | **Closed and retained closed.** The curvature ratio, first-hit derivative and return multiplier are distinguished. |
| Earlier width-versus-profile concern | Earlier scope issue | **Closed and retained closed.** Width and profile are explicitly equivalent coordinates on one invariant. |
| C15-2, contribution hierarchy | Earlier exposition | **Substantially addressed as exposition.** The principal relative law, restricted geometry and observation consequences are separated. This does not settle significance. |
| C15-1 / C16-R1 | Submission readiness | **Open.** Produce and retain a successful complete native companion-first/main build from an identified source commit, with source manifest, final logs, reference checks and product hashes. |
| C16-R2 | Minor repository consistency | **Open.** The repository-root README at the reviewed commit still calls v15 the latest A2 author revision. Update the discovery pointer in a subsequent author revision; this review does not alter it. |
| C16-E1 | Editorial significance | **Decisive negative assessment at the requested level.** Address the contribution remaining after the classical mechanisms and dependent consequences are separated. This is not a finite checklist guaranteeing acceptance. |
| New v16 theorem-correctness blocker | Mathematical correctness | **None established in the inspected material.** Do not convert this statement into an all-appendix proof certificate. |

Adding an explanatory sentence about the random-hazard extension in Section 4.4 would be optional clarification only. It is not a condition for correctness of the current deterministic-limit corollary.

## 7. Build evidence: an unsuccessful workflow is not a demonstrated TeX error

The manuscript's `VERIFICATION.json` explicitly records `full_native_main_build.status = not_yet_verified` and `C15-1_closed = false`. The companion and finite diagnostics are separately described and are not passed off as a full-main build.

For the exact reviewed SHA, the independently queried GitHub Actions record is run **34555357324**, workflow `A2 v16 integrated submission`. Its `source-and-build` job is **103126782653**. The run and job report `conclusion: failure`; the job has an empty step list and runner ID zero. The artifact endpoint reports no artifacts. The recorded run was created at 02:37:54 UTC and updated at 02:39:13 UTC on 11 September 2026.

This evidence does **not** establish that LaTeX was started and failed. It does establish that this run does not provide a successful native-main product. I do not attribute an infrastructure cause that the record does not show.

The build driver was read. It is designed to traverse the native input graph, run finite diagnostics in ordinary and optimized modes, build the companion before the full main, scan final logs, and preserve products and hashes. A sound build driver is useful, but source for a driver is not an executed build.

I did not run the full native main build in this review. The source reads were performed through the private repository connector rather than a complete local checkout. Neither a shortened document nor a smoke test has been substituted. The old completeness objection therefore remains a precisely scoped readiness issue.

## 8. Independently executed evidence

The review includes [verify_review.py](verify_review.py), written independently for this review without importing the author's checker or earlier review checkers. It uses exact rational arithmetic from the Python standard library. It has explicit failure checks rather than relying on `assert`, so the checks remain active under `python -O`.

The following commands were actually executed:

```sh
python verify_review.py > diagnostics.normal.json
python -O verify_review.py > diagnostics.optimized.json
cmp diagnostics.normal.json diagnostics.optimized.json
```

Both runs passed and their outputs were byte-identical. They contain **461 checks**: 120 stopped-kernel cases, 36 success-budget cases, 18 common-history cases, 36 reverse-erasure cases, 162 scalar identities, 30 mixed-margin identities, 21 limiting contact-block cases, 4 Schur-scale cases, 25 two-flight checks, 4 profile-jet inversions, and 5 negative controls. These are finite cases and identities, not 461 independent theorems.

The tested stopping rules include deterministic caps, stopping at a prescribed success count, and history-dependent early termination. Generic raw kernels alter the failure mass as well as successful outcomes. The success-budget examples distinguish expected preparation cost from expected successes. The erasure checks compare the exact common restriction with the weighted auxiliary transcript law and reconstruct both hypothesis marginals.

Script SHA-256:

`0311268b464151d2e498ddd461d5f9c3b5ce0267f34ebf147745b49f8c7bbd9d`

Each executed output SHA-256:

`a85cffa174c243a60a51f07abadda1d8e129dab2d4799360afe7b7b1f0d6c3bb`

Case digest:

`bf4d53fbe8f6d97cf634d187e33aa63734f2518eee347cf53413f8a7275d4195`

The Git blob identities of the uploaded script and outputs were matched against the locally executed bytes. The outputs are retained as [diagnostics.normal.json](diagnostics.normal.json) and [diagnostics.optimized.json](diagnostics.optimized.json).

These checks do not certify the infinite-dimensional determinant argument, the complete smooth inverse theorem, a billiard realization for every abstract profile, or the full manuscript build. They are not a billiard simulation. The author's reported 1,539 checks and earlier reviews' counts have not been reused as independently executed evidence here.

## 9. What a substantive response should do

For source readiness, close C16-R1 with the complete native products, not another assertion that the source graph is present. Correct the minor discovery pointer in C16-R2. Preserve the mathematical qualifications and attribution already repaired.

For the mathematical editorial issue, identify precisely what the principal physical relative theorem enables that is not already supplied by its classical local mechanism and the simpler finite-jet inverse. The most defensible emphasis is its simultaneous smooth-family relative control and the complete physical boundary-profile experiment. Explain the mathematical reach of that result on its actual hypothesis class. Do not broaden the claim to arbitrary asymmetric geometry, unknown-table erasure equivalence, or an optimal preparation exponent without proving those statements.

A successful build and a polished response would improve submission readiness; they would not, by themselves, reverse this recommendation. Further rounds which merely append consequences of the same estimate are unlikely to change the significance assessment. This conclusion is not a no-go theorem for the research program, and it does not require reducing or deleting the existing mathematical material.

## 10. Source and literature references

All manuscript citations in this report refer to the immutable author commit specified at the top, not to a moving default branch. Source labels are used instead of invented PDF page numbers. The detailed reading boundary is in [SOURCE_AUDIT.md](SOURCE_AUDIT.md).

**[R15]** Previous author-requested review: `reviews/a2-v15-independent-harsh-scalar-transport-2026-09-11/REFEREE_REPORT.md` at commit `a108adf17c4b9360e340a2d5708b20a375d69283`. Used to track prior comments and attribution; not treated as an independent proof certificate for v16.

**[L1]** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, arXiv:1905.00890v4; Invent. Math. 233 (2023), 829–901. The current review inspected the introduction's separation of local dynamics from symmetry-dependent geometry and the normal-form discussion in Section 2. [Version-pinned text](https://arxiv.org/html/1905.00890v4).

**[L2]** H. Eynard-Bontemps and A. Navas, *On the failure of linearization for germs of C1 hyperbolic vector fields in dimension one*, arXiv:2212.13646v2, 5 November 2023. The introduction explicitly distinguishes classical smooth scalar linearization from the low-regularity failures studied in that paper. [Version-pinned text](https://arxiv.org/html/2212.13646v2).

**[L3]** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983v1, 21 October 2025. The abstract/version record was checked for the finite-horizon enriched-spectrum scope; the full proof was not re-refereed in this session. [Version record](https://arxiv.org/abs/2510.18983v1).

**Final verdict:** technically serious and improved, with no newly established fatal error in the inspected core; nonetheless not recommended for the requested four-journal venue. The remaining editorial objection is substantive contribution, and the separate complete-native-build objection is still open.
