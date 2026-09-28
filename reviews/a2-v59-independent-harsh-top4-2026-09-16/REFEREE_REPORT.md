# Independent referee report on A2, revision 59

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted referee-style assessment, not a commissioned journal report, an editorial decision, or a formal proof certificate. The mathematical assessment is based on the frozen sources and actual delivered manuscripts, not on the response letter's assurances. Correctness, reproducibility, and exceptional significance are separate questions.

## 1. Recommendation and the object reviewed

**Recommendation: do not accept at the requested highest general-journal level on the present case for exceptional mathematical significance.** This is not a rejection based on a newly demonstrated fatal mathematical error. Within the examination specified below, the new Lemmas 12.10–12.11 and Theorem 12.12 withstand scrutiny. In particular, revision 59 does prove a local inverse for the **complete** analytic action map in its stated fixed-disc norm. Describing this revision as merely a diagonal conditioning estimate would be incorrect.

The new theorem is a substantive advance over revision 58. It changes the mathematical assessment of the local inversion mechanism, even though it does not, in my judgment, establish a sufficiently compelling overall case for the requested journals. Neither the previous adverse placement judgment nor the number of revisions is evidence against the new theorem.

| Object | Frozen identity |
|---|---|
| Review-ready branch | `revision/a2-v59-review-ready-2026-09-15` |
| Review-ready head | `c75b58f58e34cf56d6d4bf674a907b4b979a3940` |
| Actual compiled mathematical source | `b56282439324435668ae80be90207fe7f5eebbf2` |
| Manuscript subtree | `d9417e5fafc9ee2ad7f9cf70f98809d4c31a2ff8` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Source branch | `revision/a2-v59-analytic-contact-inverse-2026-09-15` |
| Native workflow / attempt / artifact | `34985144445` / `1` / `10403013663` |

The principal article has **113 pages**, the full technical manuscript **290 pages**, and the companion **seven pages**. The historical directory name does not identify the revision. The preparation commit is not the compiled source. Comparing the compiled commit with the review-ready head reveals no intervening modification of a compiled mathematical input. Page references below are to the principal article unless stated otherwise. [D1]

### Scope

The fresh reading covers the complete new analytic-inverse module; the principal statements and proof organization; the two-ended relative normalization and half-line construction; the actual-smooth factorization and highest-degree contact calculation; the admissible-block estimate; the single-offset density inverse; the interior-window theorem and its geometric transfer; the clear-skeleton argument; the complete finite-congruence fiber proof; and the main moving-family, registration, and finite-coordinate arguments. The current response, historical derivation audit, and dependency ledger were checked against these sources. [S1–S9]

This is **not** a fresh line-by-line verification of all 410 pages. The complete earlier finite-action/full-phase derivation, every prerequisite of physical calibration, the full adaptive and stopped-experiment catalogue, and the companion's mathematics are not certified here. In particular, checking the declaration of the acquisition dependency is not a fresh proof of that acquisition theorem. The all-page reproduction exercise has a different scope from mathematical review.

## 2. Disposition of revision 58

The preceding report is frozen at `464209b66aad6ff48b63f054711396fbfd759b64`; it reviewed actual mathematical source `92a6d946c98e19c33ebff15997c0116ac158b89d`. [R1]

| Earlier point | Disposition in the present review |
|---|---|
| Uniform admissible highest-degree blocks, R58-M1/M2 | Retained and still accepted within the stated scope. |
| A diagonal estimate does not bound all lower-triangular couplings, R58-M3 | Correct as a logical warning, but no longer describes the strongest analytic result. The new envelope representation supplies additional structure and a complete local inverse. |
| Actual smooth representatives, not just formal jets | The finite-remainder argument remains in place; the new analytic theorem does not replace it. |
| Anchored contact equalities versus functional collar bounds | Remains closed. |
| Explicit substantive acquisition dependency, previously R56-C1 | Remains closed; the new inverse does not remove the additional acquisition assumptions. |
| Exceptional significance | Must be reassessed on the stronger result, not automatically inherited from the preceding report. My reassessment remains adverse for the reasons in Section 6. |

There was no demonstrated mandatory core error in the v58 report that required the author to prove an unrelated stronger inverse problem. Revision 59 should be credited as a substantive extension, not misrepresented as a repair of a theorem previously shown false. [R1–R2]

## 3. The new analytic inverse

### R59-M1. The fixed-disc holomorphic construction handles the derivative-loss issue

Lemma 12.10, pp. 51–52, works in the affine Banach space

$$\psi^*+\mathscr X_R,\qquad \mathscr X_R=\{\eta\in H^\infty(D_R;\mathbb C^2):\eta_b^{(k)}(0)=0,\ 0\le k<3\}.$$

The gap and quadratic contact jets are fixed at this stage. Let $t=e^{-\gamma}$ and $\lambda_b=\mathfrak r_b t$. Positivity of both contact curvatures gives $\lambda_b<1$, not merely $\lambda_0\lambda_1=t^2$. Consequently the linear half-line visits can be bounded by $\lambda_*^i|u|$, where $\lambda_*<1$. The weighted construction chooses

$$\lambda_*<\beta<\rho<\sigma<1.$$

The reference Green bound is valid in the weighted sequence norm. For example, its scalar majorant satisfies the explicit uniform estimate

$$\sum_{k\ge1}t^{|i-k|}\beta^{k-i}\le \frac1{1-t/\beta}+\frac{t\beta}{1-t\beta},$$

because $t<\beta<1$. Thus the displayed choice of weights is consistent with the alternating reference dynamics. [S2–S3]

The serious issue is not this geometric sum but the dependence on arbitrary bounded holomorphic perturbations. Differentiation is not a bounded operation from $H^\infty(D_R)$ to itself. The source avoids using such an operation: at the uncontracted initial endpoint $x_0=u$, the stationarity equation uses the graph's **value**, whereas differentiated graphs occur only at internal arguments lying in a protected smaller disc. Factoring $\eta(z)=z^3v(z)$ and applying Cauchy estimates there gives the needed bounds on the differentiated nonlinear residual.

On the weighted ball the residual is $O(R^2)$ and its Lipschitz constant is $O(R)$. The Schwarz estimate for the correction gives

$$|x_{b,i}(u)|\le (\lambda_*^i+C_0R\beta^i)|u|\le\rho^i|u|.$$

The sufficient condition $\lambda_*/\rho+C_0R\beta/\rho<1$ works uniformly in $i$. It also protects the arguments throughout the fixed-point ball, rather than only after a solution has been found. Uniform convergence of the Banach-valued holomorphic iterates and the summable action terms then supplies the claimed holomorphic map. This is more than pointwise analyticity for a finite-dimensional family. [S2]

I find no unresolved derivative-loss obstruction in this construction. The restriction to a smaller real physical collar is appropriate: bounded holomorphic perturbations on the open disc need not have controlled derivatives at its boundary. The lemma does not assert that every perturbation extends to an entire periodic obstacle. That is a limitation of the statement, not a contradiction within its local setting.

### R59-M2. The complete envelope derivative has the required multiplicities and compact remainder

Lemma 12.11, p. 52, proves

$$ (L_\psi\eta)_b(u)=\alpha_b(u)\eta_b(u)+\sum_{i\ge1}v_{b,i}(u)\eta_{b+i}(x_{b,i}(u)),\qquad L_\psi=A_\psi+K_\psi.$$

Here the initial flight contributes once, each internal visit contributes twice through adjacent flights, and $|\alpha_b|\ge a_*>0$. The finite stationary differentiation retains the terminal orbit term before passing to the limit. Its bound is a constant times $\rho^{N-1}\beta^N\|\eta\|_R$, so it vanishes in the function norm. The direct variations are norm summable because the perturbation vanishes to order three. There is no unexplained removal of the endpoint term. [S2]

For a variation vanishing to order $m$, higher-order Schwarz gives

$$\|K_\psi|_{\mathscr X_{R,m}}\|\le\frac{2W\rho^m}{1-\rho^m},\qquad \|A_\psi^{-1}\|\le a_*^{-1}.$$

Both operators preserve the vanishing filtration. Taylor truncation in the contracted evaluations gives a finite-rank approximation of rank at most $2(m-3)$ with error

$$\frac{2W\rho^m}{(1-\rho)(1-\rho^m)}.$$

This is a valid same-space compactness argument even though Taylor partial sums need not converge in the $H^\infty$ norm on the full disc: the partial sums are used only at the contracted arguments. No extension of the weights or orbits beyond $D_R$ is required. Neither compactness nor this estimate makes the complete derivative a radius-improving operator.

Independent finite stationary-chain controls, including unequal curvatures and odd graph terms, agree with the correctly counted envelope in 64 configurations. Deliberately doubling the initial contact is detected in all 64. These checks test a finite variational identity; they do not prove the holomorphic infinite-chain assertion. [D2]

### R59-M3. The complete inverse is actually established, including the quotient assertion

Theorem 12.12, pp. 53–54, does not infer full invertibility from the bounded diagonal. It chooses **one fixed finite** $m$ so that

$$q_m=\frac{2W}{a_*}\frac{\rho^m}{1-\rho^m}<1.$$

On the high-vanishing subspace a norm-convergent Neumann series inverts $L=A+K$. On the finite quotient of degrees $3,\ldots,m-1$, the actual contact-jet formula supplies an invertible lower-triangular map with diagonal blocks $M_3,\ldots,M_{m-1}$. These are separate ingredients: smallness is needed on the tail, not on the whole strictly lower-triangular part. [S2–S3]

The source then solves

$$\eta_{\rm low}=L_{\rm low}^{-1}P_my,\qquad \eta_{\rm tail}=L_{\rm tail}^{-1}(y-L\eta_{\rm low}).$$

The second argument belongs to the tail because its low Taylor projection vanishes. This proves bounded invertibility on actual functions. It does not contain an uncontrolled nilpotent sum whose number of factors grows with the reconstruction order.

There is also a useful independent qualitative check. The established decomposition makes $L$ an invertible multiplier plus a compact operator, hence Fredholm of index zero. If $L\eta=0$, the invertible triangular jet blocks successively force every Taylor coefficient of $\eta$ to vanish; analyticity then gives $\eta=0$. The Fredholm alternative therefore gives surjectivity and bounded invertibility. This standard argument is a cross-check, not a replacement for the source's quantitative low-order/tail construction and not a claim of a new general functional-analytic principle.

The nonlinear contraction is also correctly organized. Holomorphic dependence makes the nonlinear remainder's derivative small near the base. The lower Lipschitz estimate follows by closeness to one fixed invertible derivative on a convex ball, not from pointwise nonsingularity alone. Invariance of every vanishing tail under both $L$ and $L^{-1}$ justifies the induced finite-jet inverses, with norm bounds inherited from the parent operators. The bounds are uniform in jet order **in the quotient norms induced by the analytic norm**. They are not bounds in the maximum norm of unweighted derivatives. The coefficient estimate on each smaller disc is the appropriate Cauchy consequence. [S2]

Finally, the joint leading-variable extension uses the explicit local inverse from $(g,a_0,a_1)$ to $(g,\kappa_0,\kappa_1)$ and a block-triangular derivative. Positive branches near the base suffice. I find no missing infinite-dimensional inversion step in this proof.

### R59-S1. The stronger conclusion has a stronger topology, not a statistical interpretation

The new result must not be conflated with stability from a real-interval density norm. An elementary illustration in its declared function space is

$$h_N(z)=\varepsilon(z/R)^N,\qquad N\ge3.$$

Its $H^\infty(D_R)$ norm is $\varepsilon$, whereas, on every $[-r,r]$ with $r<R$, every fixed finite derivative norm tends to zero as $N\to\infty$. Indeed its derivative of order $j$ is bounded there by

$$\varepsilon\frac{N!}{(N-j)!}R^{-j}(r/R)^{N-j}.$$

Thus arbitrarily accurate fixed-order real data need not be accurate in the same-disc analytic norm. This is a topology comparison, not a counterexample to the theorem or an assertion of global periodic realization. It agrees with the source's express limitation. [S2, D2]

The radius and full inverse constants can depend on the base germ and its extension bounds. The uniform hyperbolic-margin estimate for the isolated $M_n$ does not make all constants in Theorem 12.12 uniform over arbitrary analytic tables. Nor does the theorem stabilize continuation around an entire obstacle, remove finite matching alternatives, or produce a uniform preparation budget. Those restrictions are properly printed. A future report should retain them without treating them as unacknowledged errors.

## 4. The inherited mechanisms still carrying the headline conclusions

### R59-G1. Relative normalization and the actual-smooth inverse remain substantive

The decisive forward issue is the exponentially small reference twist. An absolute bridge estimate divided by that twist would not establish the needed relative law. The two-ended proof instead begins with the exact normalized cofactor identity

$$\log b_j=\sum_i\log\{g[-\ell_{uv}(y_i,y_{i+1})]\}-\log\det(I+G_j\Delta H_j).$$

The endpoint perturbations are summable; two retained end blocks are compared to the half-line operators; reflected and cross-end terms decay exponentially. The proof does not replace a trace-norm estimate by the number of sites times a crude operator-norm estimate. The trace-series comparison uses the telescoping bound $m q^{m-1}\|T-\widetilde T\|_1$, with $q<1$. Fixed differentiation orders introduce only fixed polynomial losses absorbed by a strict exponential margin. This is the analytical interface that supports a nonlinear law at fixed excess time. [S4]

The finite-smooth argument likewise does real work. Interpolation of actual graph pairs with equal finite anchored jets, stationary cancellation, and control of the terminal term give an $O(|u|^{M+1})$ action difference before the affine jet recursion is used. Nonlinear corrections of the orbit do not affect the newly isolated homogeneous degree. Counting the initial and interior visits correctly yields the $\coth(n\gamma)$ and $\mathfrak r_b^n\operatorname{csch}(n\gamma)$ block. Smooth flat remainders are not a counterexample to this finite-order statement; equality of complete smooth germs is not asserted. [S3]

The new analytic theorem strengthens the inverse side but does not replace the relative probability theorem or retroactively make all smooth remainder constants order-uniform. No new fatal error was established in the examined relative/smooth interfaces.

### R59-G2. The law and window inverses do not secretly observe the boundary

On a positive square the density ratio satisfies

$$1-\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}=t(u)t(v),\qquad t=\frac{S}{d-S}.$$

A single nonzero anchor fixes a positive scalar square root; it does not require differentiating a pointwise square root at the degenerate minimum. This retains odd action coefficients. The finite-order stability statement assumes differentiable density control, positive density, and a nonzero anchor margin. [S5]

For a recorded interior window,

$$\partial_{xy}\log p(x,y)=-\frac{S'(x-\xi)S'(y-\eta)}{[d-S(x-\xi)-S(y-\eta)]^2}.$$

The unique vertical and horizontal zero lines locate the origins under the printed visibility assumptions. The local extension uses three extra derivatives and noncentral slices with simple roots. Both origins must lie inside the window; units, directions, and excess time remain specified. No unobserved cap boundary is used to replace these assumptions. Conversely, the complete-support fiber-width argument is correctly acknowledged: the interior interaction is not being sold as the only possible method of centering a fully observed cap. [S6]

### R59-G3. Finite global ambiguity, infinitesimal rigidity, and finite data are different assertions

The clear-skeleton construction is genuine: obstruction descent uses uniform separation and yields graph paths, not specular trajectories. A tree plus two independent gain edges gives $N+1$ channels; finite-translate bounds justify clearance persistence. The finite-fiber theorem enumerates incidence rotations, checks all centered image agreements, recovers the actual marked lattice through

$$L=(v_1\ v_2)M^{-1},$$

and then imposes nonsingularity, orientation, disjointness, and selected-contact admissibility. It does not assume that $M$ is unimodular or that a cochain solution is automatically realizable. Both inclusions in the fiber statement are supplied. Noncircularity gives finite ambiguity; proper asymmetry gives uniqueness. [S7]

The differential argument uses common-strip analyticity of the parameter variation, not pointwise analyticity of the family members alone. Its amplitude differentiation includes the moving reference operator and cancellation of nondecaying reference terms. At a finitely symmetric base it follows the actual local congruence branch; it does not require every base symmetry to persist after deformation. The finite-coordinate conclusion additionally requires an immersed finite-dimensional model. These distinctions survive revision 59. [S8]

The datum remains rich. A finite number of exact conditional laws is not a finite number of scalar observations. The local scalar-coordinate theorem is not one globally identifying finite vector for the whole infinite-dimensional analytic class. This is an observation-model distinction, not a mathematical objection to the correctly scoped theorem.

### R59-G4. The acquisition dependency is explicit and remains external to the core inverse

Corollary 19.9, pp. 93–94, imports full Theorem F.47.3, including its analytic-family, chart, sensor, calibration, and charged-preparation assumptions. The pilot records planar endpoint positions in a common frame for the two types of a channel, uses the clock, and charges failures. Its compact family lies in one persistent asymmetric skeleton neighborhood. The existence of a skeleton at each table does not produce a single common acquisition design across arbitrary unrelated neighborhoods. [S9]

Scaling both separate recording efficiencies by $\varepsilon$ leaves the normalized conditional law unchanged and scales recorded-success probability by $\varepsilon^2$. Exact conditional identification therefore cannot alone provide a uniform charged budget over vanishing efficiencies. This is acknowledged in the window discussion. Neither Theorem 12.12 nor the corrected dependency declaration proves the full acquisition theorem afresh. There is no demonstrated circular use of that downstream theorem in the examined proofs of the principal geometric results. [S6, S9]

## 5. What the literature check does and does not show

The targeted primary-record check was refreshed rather than inferred from overlapping titles. Finamore–Leguil treats finite-horizon Sinai billiards using an **enriched** marked length datum. It must not be cited as an ordinary marked-periodic-length theorem. De Simoi–Kaloshin–Leguil treats analytic open billiards under non-eclipse and stated symmetry/genericity assumptions. Their observation maps and table classes differ from the present selected conditional-law setting. No reduction between these data sets has been established by this review. [L1–L2]

Osius provides established association-model context for separating odds-ratio information from unrestricted marginals. That does not supply the billiard relative determinant theorem, physical realization, or complete contact inverse. The version-5 record of Florio–Leguil explicitly removes an affected geometric open-billiard spectral-rigidity assertion while retaining dynamical conclusions. The removed assertion should not be used as an established competing theorem. [L3–L4]

These are targeted bibliographic and observation-scope checks, not a proof audit of those papers or an exhaustive priority search. I make neither a first-priority claim for the present manuscript nor an allegation that its main theorem is already known.

## 6. Exceptional significance and presentation

### R59-E1. The stronger inverse improves the paper, but the placement case remains insufficient

The strongest case for this work is now a coherent chain: a two-ended relative law retaining nonlinear boundary information, a justified smooth contact filtration, and a same-disc local analytic coordinate map for the complete variational action. The unknown lattice and finite matching problem are real outputs, not supplied solutions. It would be unfair to dismiss the work as density-ratio algebra or to continue objecting that only the diagonal has been controlled.

Nevertheless, my recommendation remains adverse at the requested level. The observation is tailored to alternating clear-channel bridges and includes marked incidences and gains, calibrated signed transverse conventions, known offsets, and entire conditional laws. Rich data do not by themselves make a theorem unimportant; inverse and rigidity problems routinely have infinite-dimensional data. The concern here is that, once the difficult local relative/action mechanism is established, a substantial portion of the global construction consists of exact analytic propagation, finite congruence matching, a displacement cochain, and selection of a basis of test differentials. These consequences are coherent, but should not each be counted as an independently exceptional innovation. [S1, S5–S9]

Theorem 12.12 does overcome the complete local coupling issue in a natural strong topology. Its contribution is the stationary multiplier-plus-contracted-visits representation and the protected-domain construction, not a new inverse-function theorem. It does not show that this conditioning improvement is available in the real observation topology, and the manuscript correctly declines to claim that. Thus the improvement changes an important local analytical conclusion without yet establishing a comparably stronger global or observational conclusion.

For a highest-level general-journal recommendation, I remain unconvinced that the present paper demonstrates enough mathematical reach beyond this specially structured observation model, or enough independently compelling depth concentrated in the relative/action mechanism, to justify the proposed placement. This is an evaluative judgment, not an impossibility statement or a claim that the results lack novelty. A specialist could reasonably assess that mechanism more favorably. Such a recommendation would have to explain why this particular mechanism is an exceptional advance; another successful build or another revision number cannot do so.

I am **not** imposing the solution of ordinary marked-length rigidity, an unmarked inverse problem, or finite-information global recovery as a correction to the stated theorems. Those are different problems. Nor would an unrelated additional proposition be an adequate response to this placement reservation.

### R59-E2. Preserve the mathematical corpus; sharpen the conceptual emphasis

The principal article and full technical manuscript are now distinct entries, and the new proof is placed within contact inversion rather than as another detached probability section. That organization is appropriate. Length alone is not a rejection criterion, and arbitrary removal of proved material is not requested.

An optional useful refinement is to isolate, in the explanatory discussion, the reusable structural principle behind the new inverse: an invertible initial multiplier, strictly contracted later evaluations, and nonresonant finite jet blocks. The qualitative Fredholm check in R59-M3 makes this structure transparent; the printed constructive proof supplies its quantitative version. This could help readers see exactly which part is billiard-specific and which part is functional analysis. It is an expository suggestion, not a missing theorem or a required repair.

## 7. Required disposition

**R59-D1 — Mathematical status.** No new mandatory core proof repair is established within the stated coverage. Lemmas 12.10–12.11 and Theorem 12.12 are accepted by this scoped examination. This does not certify every statement in all three entries.

**R59-D2 — Preserve the actual advance.** Future summaries must distinguish the old diagonal estimate from the new full local analytic inverse. The latter is not refuted by an arbitrary ill-conditioned triangular matrix: the actual derivative has additional compact weighted-composition structure.

**R59-D3 — Preserve the scope boundaries and closed corrections.** Keep the fixed-disc analytic norm, smaller real collar, exact versus statistical distinctions, actual common-strip family hypothesis, finite matching alternatives, and explicit acquisition input. These are correctly implemented restrictions, not outstanding hidden errors.

**R59-D4 — Editorial disposition.** Do not treat the next step as another routine repair-only round. My recommendation is nonacceptance at the requested level on the current significance case, after crediting the stronger analytic result. The next substantive editorial assessment should concentrate on the relative/action mechanism and its mathematical importance, not on accumulating closure certificates.

## 8. Independent reproduction and evidentiary limits

The downloaded native artifact has SHA-256

`c62fd4e19677b48f6fd866a772ba4aa98a32d497c1b0e1d74f57b08496fb6f3a`.

An independent verifier checked the lengths, SHA-256 values, and Git blob identities of all **718 frozen files**, reconstructed the manuscript subtree stated in Section 1, checked **122 distinct active inputs**, and checked all **45 build-report evidence entries**. The active path counts are 112 for the full entry, 43 for the principal entry, and one for the companion; their union is smaller than their sum because inputs are shared. [D1]

Fresh builds with shell escape disabled succeeded for all three entries. All **410 pages** match the native delivery in extracted text and same-renderer 72-dpi RGB arrays. The rebuilt PDFs are **not byte-identical**. No undefined-reference/citation, missing-character, overfull-box, or LaTeX-error match was found in the checked final logs. The full manuscript retains two underfull-box notices; the principal and companion logs contain none. Actual visual inspection covered principal pp. **3, 51, 52, 53, and 54**. No clipping or unreadable formula was observed on those pages. All-page mechanical parity is not described as all-page visual inspection. [D1]

The separate independent mathematical diagnostic imports no author checker. It checks 180 exact rational weighted-Green rows, four tail-parameter choices, finite compactness majorants, the 64 stationary-chain envelope identities and their negative controls, and the analytic-versus-real topology illustration. Ordinary and optimized Python produce identical output. The worst relative error in the finite envelope comparison is approximately $1.59\times10^{-9}$ or smaller in this run. These are finite controls, not proofs of arbitrary-order inversion, trace-class convergence, global analytic continuation, or statistical risk bounds. [D2]

The author's preservation counts remain documented author diagnostics; this report does not convert source-block counting into an independent semantic census of distinct theorems. Reproducibility is necessary discipline, but it is not an argument for acceptance.

## Source keys and audit trail

All S-keys refer to the compiled source `b56282439324435668ae80be90207fe7f5eebbf2`, under `papers/A2-v17-boundary-information-coarsening/`. [Immutable source root](https://github.com/TrillionniumFoundation/theta-theory/tree/b56282439324435668ae80be90207fe7f5eebbf2/papers/A2-v17-boundary-information-coarsening).

- **S1:** `rigidity.tex`; `journal/00_principal_introduction_v56.tex`; `journal/01_structural_statements_v56.tex`. Principal statements, observation model, and proof map.
- **S2:** `article/23a2_analytic_contact_inverse_v59.tex`, lines 1–354. Complete new module; Lemmas 12.10–12.11 and Theorem 12.12, pp. 51–54.
- **S3:** `article/23a_signed_endpoint_rigidity_v27.tex`, actual-smooth factorization, terminal envelope and homogeneous isolation; `article/23a1_uniform_blocks_v58.tex`, lines 1–124. Proposition 12.9 and the distinction between diagonal and full inversion.
- **S4:** `v4/10_boundary_layers.tex`, lines 1–390. Half-line construction, relative normalization, two-ended comparison, and fixed-offset law. This is not certification of every earlier finite-action or full-phase prerequisite.
- **S5:** `article/23f_single_offset_law_inverse_v42.tex`, especially lines 1–205. Theorem 13.1, p. 55, and finite-order density inversion.
- **S6:** `journal/shared/23q_support_and_interior_windows_v52.tex`, lines 1–271. Theorem 14.6, p. 67; window geometry and recording-efficiency qualification.
- **S7:** `article/23j_generic_finite_channel_rigidity_v45.tex`, especially lines 1–194; `article/23n_finite_symmetry_v49.tex`, lines 1–243. Theorem 19.3, p. 89; Theorem 20.3, p. 95, with both fiber inclusions and the circular comparison.
- **S8:** `article/23m_differential_rigidity_v48.tex`, moving-reference differentiation, analytic propagation, local registration and finite-coordinate arguments. Theorems 21.5–21.6, p. 104. A separate complete re-audit of every graph-to-support prerequisite is not claimed.
- **S9:** `article/23j_generic_finite_channel_rigidity_v45.tex`, lines 492–549; `journal/DEPENDENCY_LEDGER_V59.md`. Corollary 19.9, pp. 93–94, and the declared full Theorem F.47.3 input.
- **R1:** [Previous v58 report](https://github.com/TrillionniumFoundation/theta-theory/blob/464209b66aad6ff48b63f054711396fbfd759b64/reviews/a2-v58-independent-harsh-top4-2026-09-15/REFEREE_REPORT.md).
- **R2:** `RESPONSE_TO_REFEREE_V59.md`, `HISTORICAL_DERIVATION_AUDIT_V59.md`, and `LITERATURE_CHECK_V59.md` at the compiled source. Responses and provenance, not substitutes for proofs.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, and `verify_delivery.py` in this review directory; native artifact 10403013663 and the source-to-review-ready comparison.
- **D2:** `independent_checks.py` and the mathematical-diagnostic summary in `AUDIT_RESULTS.json`. The script emits the full configuration records for reproduction.
- **L1:** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983](https://arxiv.org/abs/2510.18983), primary record accessed for this review.
- **L2:** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), related DOI 10.1007/s00222-023-01191-8.
- **L3:** Gerhard Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489, [arXiv:0903.0702](https://arxiv.org/abs/0903.0702), DOI 10.1214/07-AOS572.
- **L4:** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), including the version-5 correction notice.
