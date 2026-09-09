# Independent referee report: A2 v7, critical-boundary experiments

## Recommendation

**Reject in its present form at the requested top-four general mathematics-journal level.** The adverse recommendation concerns the demonstrated significance and comparative positioning of the results, not an identified fatal error in the new proof chains. This is a substantive revision. In particular, the fixed-bracket acquisition theorem really does charge the previously missing search and control unsuccessful histories. Repeating the earlier objection that its count reconstruction receives an accuracy-dependent bracket for free would now be wrong.

There is a concrete new reason for requesting a sharper statistical comparison. In the explicitly specified analytic physical family, four fixed positive-offset binary-count windows admit a locally nondegenerate inverse, including the unknown gap. The accompanying `FIXED_OFFSET_COMPARISON.md` derives a curvature-acquisition order **\(\varepsilon^{-6}\log(1/\eta)\)** without positions, channel labels, a supplied exact gap, or an uncontrolled extrapolation-order limit. This does not contradict the submitted shrinking-design lower bound or reproduce its finer simultaneous gap target. It does mean that the headline curvature cost \(\varepsilon^{-(6+6/m)}\) should not be assessed without the exact-model, fixed-offset benchmark.

The other central reservation is equally specific: the new critical testing profile is obtained in a regime which makes the accumulated nonlinear-to-quadratic error vanish. It is a valid operational consequence of uniform local estimates, but it does not establish a sharp testing law for the genuinely nonlinear fixed-positive-offset experiment. The latter relative law is the manuscript's most substantial analytical achievement and remains the part whose exceptional general mathematical significance must carry the submission.

**Date:** September 9, 2026, Asia/Singapore.  
**Reviewer:** GPT-6 Astra Pro, acting as an independent AI referee-style reviewer at the repository owner's request. This is not a journal-commissioned review, editorial decision, human referee endorsement, or formal proof certificate. The earlier report and the parallel revision were consulted; this is not a blinded assessment.

## 1. Source identity: two parallel v7s, not one moving submission

**Repository:** `TrillionniumFoundation/theta-theory`.  
**Principal reviewed branch:** `revision/a2-v7-critical-boundary-experiments-2026-09-09`.  
**Frozen submission commit:** `fc2f0599f5b6d905859722891265232dc7ef3c5b`.  
**Root tree:** `9098043d58e8e292b23cdcdc757bc2c81b3d32cd`.  
**Repository commit timestamp:** September 9, 2026, 11:00:00 UTC / 19:00:00 Singapore.  
**Manuscript directory:** `papers/A2-v7-critical-boundary-experiments/`.  
**Article:** *Relative boundary laws and statistical reconstruction in periodic dispersing billiards*, Qian Qi.  
**New review branch:** `review/a2-v7-critical-boundary-harsh-independent-2026-09-09`.  
**Review directory:** `reviews/a2-v7-critical-boundary-harsh-independent-2026-09-09/`.

The parallel branch `revision/a2-v7-sharp-physical-experiments-2026-09-09` has the later head `e3f5cba851f6216e879d1effa13fa171d92861b7`, timestamp 11:02:39 UTC. That head changes delivery documentation. Its mathematical-source parent `781b91da1b7af41c7c1528ccb44cd0681d564e0d` is timestamped 10:53:38 UTC, earlier than this principal revision. Thus the latest branch head and the latest substantive mathematical revision are different objects. Both have been reviewed separately. Neither report imports a theorem from the sibling and silently credits it to the other submission.

Both substantive revisions descend from the controlling v6 review commit `f1728f5d96ea01b1326daf9a6a36352b2e270be1`. That report reviewed author commit `4ca186258c92dcbc75accc4eb576e307cc612189`, whose complete manuscript subtree is `50f7fdb275a23d7a74234f4e1347c4934be8b8b8`. The older `sharp-experiments-econometrica` branch was identified as a source-packet commit, not treated as a newer complete mathematical manuscript.

Unless another source is explicitly named, the paths and LaTeX labels below refer to the principal directory at the frozen commit. Labels are the controlling locators; PDF theorem numbers and page counts stated by the author have not been independently verified here. This review adds review material only.

## 2. Disposition of the preceding requests

| Request in the controlling v6 report | Disposition in this committed v7 |
|---|---|
| V6-R1: observations, side information, varying parameters, cost, and uniformity in one place | **Closed.** `v7/00_scope.tex` distinguishes five experiments, including the new fixed-bracket procedure. It does not confuse selected positions with unlabelled Bernoulli reports. |
| V6-R2: statistical benchmarks with correct quantifiers | **Closed at the claimed scope.** `thm:v7-exact-tv`, `lem:v7-tangent`, `thm:v7-critical`, and `thm:v7-lower` provide actual statements and proofs. The wider fixed-bracket design is explicitly excluded from the shrinking-design optimality claim. |
| V6-R3: explain what long bridges add, given one-flight germ identification and fixed-J reconstruction | **The requested explanation is supplied.** The introduction states those limitations adjacent to its motivation. The adequacy of the significance case remains an editorial judgment, not an unchanged proof omission. |
| V6-R4: measurable reconstruction and separate reproducibility claims | **Closed in the source.** `lem:v7-selection` handles compact metric parameter sets and the root-or-zero pilot rule. The verification record distinguishes local author execution, rendering, remote CI, and proof. |

The earlier distinctions between actual and effective curvatures, a constrained physical three-amplitude inverse and an independent-normalizer four-amplitude inverse, finite jet order and infinite analytic continuation, and a selected horizontal hierarchy and all channels remain necessary and are not undone by this revision. This report does not recycle the historical unmaterialized-v6 finding against an actual v7 manuscript.

## 3. Mathematical audit

### 3.1 The uniform geometric and relative-flux mechanism

**Locators:** `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative`; `v3/20_integration.tex`, `lem:g-radial`; `v4/10_boundary_layers.tex`; `v5/15_differentiated_operators.tex`.

The common collar is not obtained by iterating a small neighborhood that shrinks with the number of flights. Each complete flight has length at least the minimum gap. Small total excess therefore makes each flight short, and separated near-normal outgoing states force reversal along the same alternating channel. The clearance argument excludes a third obstacle along a shortest segment. This is a legitimate local construction around an arbitrary positively curved separated periodic configuration, not a near-circle argument disguised as a general theorem.

For unequal facing curvatures, the alternating Jacobi scaling is essential. With \(c_b=1+g\kappa_b\), \(c=\sqrt{c_0c_1}\), and \(\gamma=\operatorname{arcosh}c\), the printed endpoint Schur complement agrees with the finite quadratic action. Its endpoint eigenvalues stay uniformly positive, while its mixed derivative contains \(\operatorname{csch}(j\gamma)\). The independent exact checks below test both parities and genuinely unequal contacts; they are not merely equal-curvature checks.

The weighted Green argument controls the stationary bridge by two summable endpoint layers. In the cofactor identity

\[
 -W_{uv}=\frac{\prod_i[-\ell_{i,uv}]}{\det H_{\rm int}},
\]

the logarithmic edge product is summable. The perturbation of the interior Hessian has bounded trace norm because it is tridiagonal and its entries inherit those endpoint weights. The relative determinant series retains one trace-class factor, including after differentiation; the addendum correctly does not assume differentiated factors remain small. Thus the proof controls the exponentially small twist relatively rather than dividing an absolute action error by it.

The half-line construction specifies its determinant normalization. The two-block comparison separates the endpoint perturbations before replacing finite Green kernels by half-line kernels, and estimates discarded entries in trace norm. Fixed polynomial derivative losses are absorbed by a strict exponential margin. This is the substantive analytical work in the paper; it should not be equated with the subsequent product-measure inequality.

The physical measure \((-W_{uv})\,du\,dv\,dr/(2\pi A)\) and the residual interval are retained. The preceding roof does not truncate the interval in the stated collar. Uniform Morse coordinates use the positive endpoint Hessian, not the small twist as an inverse bound. Fixed-domain radial integration explains smooth right offset derivatives. I found no fatal defect in these inspected arguments under the printed compact-family and local-channel hypotheses. This is a source audit, not a proof-assistant certification.

### 3.2 Unequal-contact support overlap and erasure equivalence

**Locator:** `v7/10_critical_experiments.tex`, `thm:v7-exact-tv`.

The whitening identity is correct. The half-line Hessians are

\[
 a_b=\frac{c\sinh\gamma}{g c_{1-b}},
\]

so the Jacobi formula indeed gives \(H_j=D M_jD\), with \(D=\operatorname{diag}(\sqrt{a_0},\sqrt{a_{j\bmod2}})\), and \(H_\partial=D^2\). The determinants agree for both parities. A common change of coordinates therefore reduces the comparison to a disk and an equal-area ellipse with reciprocal eigenvalues. The polar-overlap computation yields

\[
 \delta_j=\frac2\pi\arcsin(e^{-j\gamma}).
\]

For heterogeneous independent products, equality of the two densities on their common support gives the product of common masses, not merely a union-bound upper estimate. Restoring the failure atom gives \(1-\prod_i(1-p_i^0\delta_{j_i})\). No Gaussian or square-root sample accumulation is justified for this support-changing pair.

The two-way erasure randomizations are valid for the stated **simple binary pair at a fixed table**. The common restriction is the same measure under both hypotheses, and each exclusive restriction identifies the hypothesis. The reverse kernel may depend on the known table and design; the manuscript says so. It is not a universal simulator for an unknown geometry. That distinction is closed, not a fresh objection.

### 3.3 Actual positive offsets and growing sample sizes

**Locators:** `v6/10_experiment_transfer.tex`; `lem:v7-tangent`, `thm:v7-critical`.

The uniform tangent error is proved in the appropriate topology. In the general case, the scaled action error is \(O(\sqrt d\,|z|^3)\) and the amplitude error is \(O(\sqrt d\,|z|)\). Both residual intervals start at zero, so their symmetric-difference length is bounded by the action error. Coercivity confines all integrations to a fixed bounded set. Normalization then gives a conditional \(O(\sqrt d)\) bound; multiplication by the actual physical prefactor and restoration of failure mass gives \(O(p^0\sqrt d)\). Evenness of both graphs, without equality of the graphs, improves these to \(O(d)\) and \(O(p^0d)\).

The product comparison follows by telescoping and the reverse triangle inequality. Its hypotheses include the accumulated remainder condition, even when the limiting effective sample size is infinite. Under those hypotheses the proof is correct. There is no unlicensed interchange of growing sample size and small offset.

It is important to interpret the result exactly. At a finite nonzero critical value, \(k_jq_j\to b>0\) and \(k_j\sqrt{d_j}\to0\) imply \(d_j=o(q_j^2)\); in the even class the corresponding implication is \(d_j=o(q_j)\). Thus both physical hypotheses become asymptotically indistinguishable from their respective quadratic experiments at the entire experiment level. The resulting erasure profile is genuinely physical, but asymptotically tangent. The paper already states that its nonlinear fixed-offset rate \(\tau\) is not proved sharp. My significance reservation must not be relabelled as a missing assumption or false theorem.

An optional improvement is available from the sibling's projection argument. In either regularity class, the condition \(\omega(d_j)/q_j\to0\), with \(\omega=\sqrt d\) or \(d\), suffices for the full zero/finite/infinite effective-sample transition: for an infinite effective sample size, project onto approximately \(B/q_j\) successes, or \(B/(p_j^0q_j)\) raw preparations, prove the finite-B limit, and let \(B\to\infty\). This removes the need for the original full-sample accumulated error to vanish in that case. It is a useful refinement, not a condition of correctness or a new independent basis for a top-four recommendation.

### 3.4 Count indistinguishability, stopping, and confidence

**Locator:** `v7/30_count_lower_bounds.tex`.

The alternatives \(\beta=\pm s,\alpha=\zeta=0,R=1/4\) are physical and have the same gap. Rotation invariance annihilates the linear parameter differential of the normalized finite-offset count probability. Taylor expansion consequently gives \(|p(s)-p(-s)|\le Cd^2|s|^3\), while both probabilities are comparable to \(d^2\). This is a statement about complete finite-offset count probabilities, not only a leading-amplitude surrogate.

The radii separation, its conversion to curvature matching distance, and the Bernoulli entropy inequality give the stated weighted-exposure lower bound. Conditioning on a common history and independent randomization leaves the same next query in both alternatives; padding with stop symbols and passing from finite histories to the full transcript justifies adaptive stopping. The expected-risk bound and the fixed-confidence lower bound have the appropriate quantifiers.

The extension to a confidence logarithm is immediate from the entropy estimate and binary data processing, and is proved explicitly in the sibling. Its absence here is not a mathematical error: this submission says its matching power is apart from confidence logarithms. It should not be counted as another large conceptual advance when added.

### 3.5 Fine calibration and acquisition from a fixed initial interval

**Locators:** `v5/50_self_calibration.tex`, `v6/40_count_only_acquisition.tex`, and `v7/40_fixed_bracket_acquisition.tex`.

The inherited pilot extrapolates the zero of square-root probabilities, not the probability function at negative offsets. Its Lagrange interpolation proof controls both values and derivatives on the root interval. Clipping the root-or-zero rule gives an all-outcome gap bound; the enlarged second-stage safety margin prevents a failed pilot from programming a nonpositive actual offset when the supplied bracket is correct. The timing normalization error is explicitly charged as \(O(|\widehat g-g|/h)\).

The new search deals with the missing supplied bracket. On an interval of width \(w\), a success at the midpoint safely lowers its upper endpoint. A no-success update can discard the true gap only if the queried excess exceeds \(w/4\), and the quadratic lower onset bound controls that probability. Widths contract by either \(1/2\) or \(3/4\). The all-history estimate \(\sum w^{-2}\le C h^{-2}\) is valid by summing backwards from the last nonterminal interval; a union bound controls the first incorrect discard. The resulting \(h^{-2}\log((2+\log(W/h))/\delta)\) cost is correctly absorbed in the later fixed-m cost.

The caps on all pilot waiting times are not cosmetic. An incorrect initial search could put a window below onset and make an uncapped waiting time infinite. On the correct-search event the lower success-probability bound controls the probability of hitting a cap; on other histories the deterministic cap still controls cost. Fresh preparations justify conditional application of the inherited theorem. The final amplitude sample size is deterministic and its estimator has a compact fallback. The sum of the allocated failure probabilities is correct.

Accordingly `thm:v7-fixed-bracket` earns its all-history preparation bound and its independence from an accuracy-dependent supplied bracket. The wider initial queries place it outside the shrinking-collar lower-bound class. The manuscript explicitly acknowledges this; no global optimality misstatement is alleged.

### 3.6 Measurability and the finite-dimensional inverse

The closed-ball minimizing selection works on the stated compact metric parameter space. Values minimized over each fixed compact intersection are Borel, selected indices are Borel, and the nested compact minimizer sets have diameter tending to zero. The pilot's unique-root-or-zero convention is separately shown Borel, including degenerate polynomials. These proofs resolve the formal estimator issue without claiming computational efficiency.

The physical area identity and all twelve entries of the three-amplitude derivative table were independently recomputed. The determinant at the circle agrees with the displayed nonzero expression. The inverse-function argument is in a full symmetric-coefficient neighborhood before restriction to real roots, which is the correct way to handle coalescence. The companion comparison supplies the additional analytic descent needed for **finite-offset**, rather than only leading-amplitude, inversion; that step should not be omitted when considering its conclusion.

## 4. Principal requirements for another submission

### C-R1 — Major comparative issue: distinguish the exact parametric model, smooth nuisance robustness, and the loss being optimized

Read the accompanying fixed-offset comparison as a concrete test of the statistical significance case. Its four means use \((j,t)=(1,g_*+a),(1,g_*+2a),(2,2g_*+a),(3,3g_*+a)\), with a fixed small \(a\). Exact finite-offset probabilities are symmetric analytic functions of the three radius increments in the printed family and descend to coefficient coordinates. After a row difference and scaling the gap column by \(a\), the derivative tends to a block matrix of determinant \(C_1\det D_e(C_1,C_2,C_3)\ne0\). Thus neither the true gap nor contact positions are supplied.

The resulting \(\varepsilon^{-6}\log(1/\eta)\) curvature cost is a baseline within a sufficiently small fixed known physical neighborhood. It does not contradict an optimal rate in a design forced to shrink its offsets, and it does not match the extrapolation theorem's finer simultaneous gap error. It should therefore lead to a clear comparison of three different questions: curvature loss in a known exact family; joint curvature and finer timing accuracy; and reconstruction robust to unspecified higher-order smooth probability terms.

A satisfactory response may establish and discuss this comparison, identify a precise failure in its proof, or formulate the larger nuisance experiment for which the extrapolation method has a genuine robustness advantage. Merely repeating that the lower bound is design-restricted is logically correct but does not assess the natural exact-model alternative. No deletion of the fixed-bracket theorem or weakening of the broad smooth forward theorem is requested.

### C-R2 — Major significance issue, not a proof defect: identify the independent nonlinear advance

The new erasure profile is useful and its unequal-contact formulation is clean. Nevertheless, its proof reduces the entire compared experiment to tangent laws under the printed small-offset conditions. The precise positive-offset statement should receive credit without being counted as a sharp law for the nonlinear fixed-offset problem.

The strongest genuinely nonlinear result remains the common-collar relative determinant law and its differentiated physical integration. The manuscript should make a focused case for what mathematical problem this mechanism resolves beyond standard hyperbolic boundary-value localization, determinant identities, and the finite-dimensional consequences. A new global rigidity or arbitrary-itinerary theorem is **not** imposed as an acceptance condition. Nor would a sharper fixed-offset theorem automatically settle the venue judgment. The issue is the significance of the actual contribution, not a demand to expand scope indefinitely.

### C-R3 — Major exposition issue: organize an article, not an accumulated revision dossier

The active source still juxtaposes many inherited consequences with the new testing and acquisition material. The abstract lists relative analysis, testing, jets, analytic rigidity, realizations, coalescence, calibration, and lower bounds. The reader needs a sharper hierarchy of principal results and logically separate applications, not another layer of revision chronology.

Preserving every historical source file is good repository practice. It does not require every prior exposition to stay in the active article in its historical order. Reordering, combining duplicate motivation, and placing complete secondary proofs in a properly organized appendix can preserve all mathematical content. This request is not a page-count cutoff and not a claim that a long paper cannot meet the requested standard.

### C-R4 — Submission control and evidence

Designate one canonical next revision. This principal v7 has unequal-contact/general-smooth testing and fixed-bracket acquisition; the sibling has a stronger supercritical formulation and an explicit high-confidence stopped-design lower bound. They are complementary, not interchangeable. A revised response should state exactly which are included rather than refer ambiguously to “v7.”

Keep author build evidence, independent source review, executed diagnostic results, and remote CI separate. This revision's `VERIFICATION_V7.json` reports a local 72-page article and seven-page companion build and rendering. This reviewer inspected the record, not those PDFs, and did not rerun the build. The sibling instead explicitly records that its PDF build did not execute. Neither status is a mathematical counterexample, and they must not be merged into a single unqualified “verified v7” claim.

## 5. Targeted primary-literature comparison

The primary records below were checked online during this review. This is a targeted comparison, not an exhaustive priority search or a reproof of the cited works.

Bolotin and Treschev's *Hill's formula* relates action Hessians and monodromy for discrete and continuous Lagrangian systems [1]. It is relevant predecessor structure, but the inspected record does not establish that it contains this manuscript's common-collar nonlinear relative physical flux estimate. No duplication finding is made.

Zelditch's localized wave-trace calculations and analytic-domain inverse results use spectral observations and their own symmetry and nondegeneracy setting [2]. De Simoi, Kaloshin, and Leguil study marked lengths for analytic open billiards under non-eclipse, symmetry, and genericity hypotheses [3]. Finamore and Leguil's specified preprint concerns an enriched marked length spectrum and finite-horizon Sinai billiards [4]. These are different observations and geometric determination problems. Neither “our probabilities are different” nor a superficial analogy proves greater significance or containment in either direction.

Batenkov and Yomdin analyze accuracy in confluent Prony systems [5]. The manuscript's physical realization, specific amplitude Jacobian, and acquisition constraints require their own proofs; the universal phenomenon of singular coefficient-to-root conditioning is not itself new. The fixed-offset comparison accompanying this report is derived from this manuscript's explicit family and nonzero Jacobian, not attributed to the cited Prony paper.

## 6. Executed checks and limits of this review

The accompanying `independent_checks.py` completed **179 named checks: 156 exact symbolic/rational checks and 23 ordinary floating-point checks**. It was executed normally and with `python -O`; the two JSON outputs were byte-identical. Explicit exceptions enforce failures. The script imports no author or previous referee diagnostic module and makes no network calls.

Exact checks include unequal-contact endpoint Schur complements for both parities, determinant and flux ratios, the physical radius permutation action and area constraint, all twelve three-amplitude derivatives and their determinant, the four-window limiting Jacobian, heterogeneous product overlaps, coalescence matching on exact sample points, extrapolation identities, and exhaustive memoized all-outcome bracket-width recursions. Floating checks independently integrate disk/ellipse overlap and test sample entropy and critical-limit identities. These are diagnostics, not 179 proofs of the nonlinear theorem.

Executed environment: Python 3.13.5, SymPy 1.14.0, SciPy 1.17.0. Script SHA-256: `b55033e929cce883577dfeb28d7936395ebf5c326e8d1eea27ca287fd9714d5c`. Complete diagnostic-output SHA-256 in both modes: `c73ae356f017d14047161502c6be5da4fdc6241c54df8749e0fdff70fe1241da`. `VERIFICATION.json` records the source identities and evidence categories.

Direct source review covered all new v7 mathematical files and the scope table, both main entry points and responses, the principal geometric/Jacobi/relative-determinant/half-line/integration/transfer dependencies, calibration and count acquisition, the physical support family and three-amplitude inverse, and the specified previous review. The inherited contact-jet, global analytic-continuation, full record-response, circular appendix, and independent companion arguments were **not independently re-audited line by line in their entirety in this round**. Their historical disposition is not a new proof certificate. This report does not claim an audit of all eleven papers, every historical derivation, or every branch.

No physical nonlinear billiard simulation, exact finite-offset probability evaluation, interval arithmetic, formal proof assistant, manuscript PDF compilation, PDF visual inspection, or remote CI verification was performed by this reviewer. Author-reported build and diagnostic results are identified as such. The companion fixed-offset result rests on its written analytic and inverse arguments; its finite determinant check alone does not prove that result.

## 7. Final disposition

The revision should not be described as mathematically empty, unmaterialized, or nonresponsive. Its new unequal-contact tangent comparison, actual positive-offset limit, measurable reconstruction, physical stopped-design lower bound, and fully charged fixed-bracket count procedure survive this targeted audit without an identified fatal error.

I nevertheless do not recommend the present manuscript for the requested venue. The fixed-offset parametric benchmark makes the remaining statistical comparison more precise, and the tangent nature of the critical limit prevents it from settling the significance of the nonlinear common-collar mechanism by itself. These are reasons to revise the mathematical positioning and article architecture, not instructions to lower the general forward assumptions, erase correct proofs, or abandon the program. Satisfaction of a further checklist would still not constitute automatic acceptance; the next assessment should again be of its exact committed mathematics.

## References and immutable sources

[1] S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257. DOI: 10.1070/RM2010v065n02ABEH004671. Primary author record: https://arxiv.org/abs/1006.1532.

[2] S. Zelditch, *Inverse spectral problem for analytic domains, II: Z2-symmetric domains*, Annals of Mathematics 170 (2009), 205–269. DOI: 10.4007/annals.2009.170.205. Publisher: https://annals.math.princeton.edu/2009/170-1/p06.

[3] J. De Simoi, V. Kaloshin and M. Leguil, *Marked length spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae 233 (2023), 829–901. DOI: 10.1007/s00222-023-01191-8. Primary record: https://arxiv.org/abs/1905.00890.

[4] D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983, first submitted October 21, 2025. Primary record: https://arxiv.org/abs/2510.18983. No assertion of journal publication or exhaustive latest-version review is made.

[5] D. Batenkov and Y. Yomdin, *On the accuracy of solving confluent Prony systems*, SIAM Journal on Applied Mathematics 73 (2013), 134–154. DOI: 10.1137/110836584. Publisher: https://epubs.siam.org/doi/10.1137/110836584.

Frozen principal manuscript: https://github.com/TrillionniumFoundation/theta-theory/tree/fc2f0599f5b6d905859722891265232dc7ef3c5b/papers/A2-v7-critical-boundary-experiments.

Frozen parallel manuscript: https://github.com/TrillionniumFoundation/theta-theory/tree/e3f5cba851f6216e879d1effa13fa171d92861b7/papers/A2-v7-sharp-physical-experiments.

Controlling previous report: https://github.com/TrillionniumFoundation/theta-theory/blob/f1728f5d96ea01b1326daf9a6a36352b2e270be1/reviews/a2-v6-relative-transfer-harsh-independent-2026-09-09/REFEREE_REPORT.md.
