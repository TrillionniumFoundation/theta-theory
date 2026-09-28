# Independent referee report on A2 v14

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.

**Date:** 11 September 2026. **Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society.

**Status:** author-requested, AI-assisted, source-pinned referee-style assessment. This is not a journal-commissioned report, an editorial decision, or a formal proof certificate.

## 1. Version and recommendation

The author branch is `revision/a2-v14-intrinsic-boundary-normal-form-2026-09-10`. This report reviews the frozen commit **`e136929b120912586266fb78e0ae7b3c9d43bfd6`**, with root tree `235b06d8ed42d9697ef983367683bc97947f2dad`. Manuscript paths below are relative to `papers/A2-v14-intrinsic-boundary-normal-form` unless explicitly stated otherwise. TeX labels, rather than unverified printed numbering, identify the results authoritatively.

The parent is the latest v13 report at `b3f0ad5843782c221651c9189fc156d20865cab1`, which reviewed author commit `0e54099f079232df233316ae6fe7986fc51b7ea1`. I have read that report, the v14 response, the new section, and the principal supporting arguments identified in [SOURCE_AUDIT.md](SOURCE_AUDIT.md). This is a new assessment, not a restatement of the previous verdict.

**Recommendation: reject in the present form at the requested four-journal level.**

This recommendation is principally about significance, not a newly discovered false theorem. **I found no fatal mathematical error in the new analytic comparison, the smooth density cocycle, or the inspected inverse-and-observation chain.** That is a scoped finding, not certification of every inherited appendix result. The v13 report's two principal requests have been answered. I would not recommend another round of nominally technical major revision while leaving the author to guess an unstated acceptance condition.

V14 makes the paper more intelligible and its claims more accurate. It does not, in my assessment, supply the exceptional additional conceptual or geometric advance needed to change the venue recommendation. The new scalar linearizing density is a correct identification of an existing physical amplitude with a classical one-dimensional dynamical object. The new width is an invertible re-expression of the already recovered energy profile. Neither should be counted as an independent new rigidity phenomenon. The manuscript largely acknowledges these dependencies; the disagreement is about their resulting weight, not about whether the author has responded honestly.

There remains worthwhile mathematics: uniform relative control of a rare physical event, a transparent independent-contact jet inverse, physical finite-dimensional realization, and a genuinely charged observation procedure. I do not claim that the entire smooth physical theorem is already in the literature, that these results are unpublishable, or that the research programme is obstructed. I do not recommend acceptance at the specified level on the evidence in this revision.

## 2. Disposition of the preceding requests

| Request | Disposition in v14 |
| --- | --- |
| R13-1: compare the relative physical law with analytic hyperbolic normal forms, including physical projection and the smooth remainder of the contribution | **Closed as the requested comparison.** Proposition `prop:v14-normal-form`, the following billiard specialization, and the final subsection of `article/16_hyperbolic_coordinates.tex` provide the comparison, its hypotheses, and its limits. The normal-form calculation is attributed to the preceding referee memorandum. |
| R13-2: replace the abstract's universal finite-dimensional-family claim | **Closed.** The abstract now restricts to the locally full-rank physical finite-jet families constructed in the paper. This matches `thm:v13-two-flight-observation`. The remote-obstacle counterfamily is no longer a counterexample to the wording. |
| Earlier C13-1: distinguish exact-germ normalization from finite-sample calibration | **Closed in the inspected passage.** The paragraph following `eq:v13-finite-law` extracts the leading coefficient only from an exact supplied germ. The actual sampling experiment either supplies the fixed family data or uses the separately charged smooth pilot. |
| Earlier C13-2: make the current A2 revision discoverable | **Closed.** The frozen repository README points to v14 and its response; the manuscript README gives the reading and build map. This does not independently verify its advertised build and retention counts. |

The prior objections about missing two-flight twist variation, formal jets being substituted for smooth uniqueness, derivative observations, uncharged failures, and exact-family calibration oracles are not being reinstated. The inspected v14 source explicitly avoids those defects.

Closing these requests does not mechanically imply acceptance. Conversely, a negative significance assessment must not be disguised as failure to implement requests that have actually been implemented.

## 3. The new analytic benchmark is mathematically satisfactory

**Source:** `article/16_hyperbolic_coordinates.tex`, Proposition `prop:v14-normal-form`, especially `eq:v14-mixed-equation`, `eq:v14-exact-mixed-flux`, `eq:v14-physical-flux`, and `eq:v14-csch-normalization`.

For the normal form

$$
N(s,p)=(\Delta(sp)s,\Delta(sp)^{-1}p),\qquad \Delta(0)=\lambda\in(0,1),
$$

prescribing the initial stable coordinate and terminal unstable coordinate gives

$$
I=st\Delta(I)^n,\qquad p_0=t\Delta(I)^n,\qquad s_n=s\Delta(I)^n.
$$

The manuscript correctly differentiates the implicit equation rather than treating the invariant as independent of the prescribed endpoints. With

$$
D_n=1-nI\frac{\Delta'(I)}{\Delta(I)},
$$

both relevant canonical mixed derivatives equal

$$
T_n=\frac{\Delta(I)^n}{D_n}.
$$

The contraction is on a fixed small box. The derivative estimates retain a polynomial in the return number and absorb it into a strict exponential margin. The argument also addresses the cancellation at the parameter-dependent value of the multiplier: differentiating a normalized quantity is not the same as dividing an uncontrolled differentiated error by a small number.

The physical projection is indispensable and is now present. For

$$
\Phi_n(s,t)=\bigl(U(s,t\Delta(I)^n),V(s\Delta(I)^n,t)\bigr),
$$

canonicity gives

$$
du\wedge dP=T_n\,ds\wedge dt,
\qquad du\wedge dv=(\det D\Phi_n)\,ds\wedge dt.
$$

Thus the physical mixed flux is exactly

$$
J_n(u,v)=\left|\frac{T_n}{\det D\Phi_n}\right|,
$$

with the mixed coordinates evaluated at the inverse physical endpoint map. The proof establishes this inverse on a common inner box, not just pointwise at the orbit. Its limiting factors are the normalized inverse projection derivatives along the invariant axes.

The normalization at the billiard orbit also survives inspection. Here the multiplier is the **two-flight return multiplier**, $\lambda=e^{-2\gamma}$. If the canonical derivative has columns along $(1,-a_b)$ and $(1,a_b)$, canonicity gives $AB=(2a_b)^{-1}$. Consequently

$$
J_n(0,0)=\frac{2a_b\lambda^n}{1-\lambda^{2n}}
         =\frac{a_b}{\sinh(2n\gamma)}.
$$

This agrees with the exact Jacobi normalization, including its denominator. The action limit is then obtained from first variations with an explicit additive normalization. I found no missing sign or factor of two in these arguments.

The cited De Simoi–Kaloshin–Leguil text recalls the local analytic normal form separately from its global inverse-spectral hypotheses [L1]. V14 now makes the appropriate distinction. Neither that citation nor the calculation alone supplies A2's entire smooth, parameter-uniform physical probability theorem. I do not use the analytic benchmark as a fictitious citation for such a theorem.

## 4. The smooth first-flight cocycle is correct, but its novelty must be localized

**Source:** the same file, Theorem `thm:v14-intrinsic-density`, equations `eq:v14-Bellman` through `eq:v14-iterate-limits`.

Write $o=1-b$, let $\varphi_b$ be the first physical hit along the stable half-line, and put

$$
r_b=\sqrt{c_b/c_o}\,e^{-\gamma},\qquad
R_b=\varphi_o\circ\varphi_b,\qquad r_0r_1=\lambda=e^{-2\gamma}.
$$

The Bellman identity and the stationary equation give

$$
\varphi_b'(u)=
\frac{-\ell_{b,12}(u,\varphi_b(u))}
 {\ell_{b,22}(u,\varphi_b(u))+S_o''(\varphi_b(u))}>0.
$$

At the orbit this equals $r_b$. The positive denominator supplies the needed implicit-function estimates, and the first-hit maps contract a common smaller interval.

For a finite tail, exact stationary concatenation gives

$$
-W_{j+1,b,12}
 =\frac{-\ell_{b,12}}{\ell_{b,22}+W_{j,o,11}}
       [-W_{j,o,12}].
$$

The reference ratio is

$$
\frac{d^0_{j,o}}{d^0_{j+1,b}}
 =\sqrt{a_o/a_b}\,
       \frac{\sinh((j+1)\gamma)}{\sinh(j\gamma)}
 \longrightarrow r_b^{-1}.
$$

Normalizing before passing to the relative limit and cancelling the positive terminal factor proves

$$
B_o(\varphi_b(u))\varphi_b'(u)=r_b B_b(u).
$$

The placement of $r_b$, rather than its reciprocal, is correct. This is the important physical identification: the density previously defined by a half-line relative determinant obeys the dynamical transport law with the correct reference normalization.

Integration yields the normalized scalar coordinate

$$
\zeta_b(u)=\int_0^u B_b(x)\,dx,
\qquad \zeta_o\circ\varphi_b=r_b\zeta_b,
\qquad \zeta_b\circ R_b=\lambda\zeta_b.
$$

The uniqueness proof is valid even against other merely differentiable normalized linearizers. After conjugation, the commuting germ satisfies $h(\lambda x)=\lambda h(x)$ and $h'(0)=1$, so dilation toward zero forces $h(x)=x$.

The quantitative limits also follow legitimately from the exact conjugacy. Writing $\zeta_b^{-1}(x)=x+x^2h_b(x)$ gives

$$
\lambda^{-n}R_b^n(u)-\zeta_b(u)
 =\lambda^n\zeta_b(u)^2h_b(\lambda^n\zeta_b(u)).
$$

Endpoint differentiation yields the density limit. Fixed parameter derivatives introduce polynomial factors in $n$, absorbed by any fixed strict exponential margin above the maximum return multiplier. There is no need to assume a smooth two-dimensional symplectic normalizing chart for this step.

The dependency is not circular: the existing relative factorization is used to identify its amplitude, rather than supposedly being reproved from that identification.

### 4.1 A closer comparator for this new theorem is one-dimensional linearization

The distinction between analytic two-dimensional normal forms and arbitrary smooth billiards is important for the main forward theorem. It is not, by itself, evidence of new scalar linearization theory. Smooth hyperbolic germs on a line are classically smoothly linearizable; the primary research source [L2] explicitly recalls that regime before studying failures at lower regularity. Those low-regularity failures are not counterexamples to A2.

There is a short direct calculation in precisely the smooth contraction setting. For any smooth orientation-preserving contraction $R$ fixing zero with $R'(0)=\lambda$, define

$$
\widetilde B(u)=
 \exp\left\{\sum_{k=0}^{\infty}
    \log\frac{R'(R^k(u))}{\lambda}\right\}.
$$

On a sufficiently small interval the series and every fixed derivative converge. It satisfies

$$
\widetilde B(R(u))R'(u)=\lambda\widetilde B(u),
\qquad \widetilde B(0)=1.
$$

Its integral is the unique normalized scalar linearizer. Uniqueness also forces compatibility of the two first-flight charts. A complete proof, including the relevant smooth-family statement, is provided in [SCALAR_LINEARIZATION_AND_WIDTH_BENCHMARK.md](SCALAR_LINEARIZATION_AND_WIDTH_BENCHMARK.md).

Accordingly, the specifically physical content of Theorem 8.2 is the equality of the pre-existing determinant amplitude with this scalar density. Existence of a normalized scalar linearizer, its uniqueness, and the normalized iterate limits are not separate new dynamical mechanisms. The concatenation argument establishes the physical identification correctly. It does not make all of its classical consequences separate advances of equal weight.

This observation does **not** replace the finite-bridge determinant proof. A scalar germ alone does not specify a two-ended stationary bridge, its physical reference twist, first-hit event selection, or the residual-time probability integral. The distinction cuts both ways and must be retained.

## 5. The width is a useful interpretation, not additional recoverable information

**Source:** Corollary `cor:v14-width` and `eq:v14-width`; compare `article/20_boundary_compatibility.tex`, `eq:v9-energy-profile` and `thm:v9-compatibility`.

The change $x=\zeta_b(u)$ removes the density because $dx=B_b(u)du$. If $\widehat S_b=S_b\circ\zeta_b^{-1}$, the limiting law becomes the ordinary residual integral for $\widehat S_b$. Its normalized sublevel width is

$$
\mathcal W_b(E)
 =\sqrt{a_b/2}\,[\zeta_b(u_{b,+}(E))-\zeta_b(u_{b,-}(E))]
 =\int_0^E x^{-1/2}\mathcal V_b(x)\,dx.
$$

The constants agree with the earlier pushforward formula. Conversely, for positive energy,

$$
\mathcal V_b(E)=\sqrt E\,\mathcal W_b'(E).
$$

Thus the complete width and the complete energy profile encode the same datum. The leading width is $2\sqrt E$, since $\mathcal V_b(0)=1$. A separate curvature scale is unnecessary for the normalized width but is necessary to undo that normalization. These statements are correct.

For even contacts, the two intrinsic inverse branches are related by reflection. Without evenness, their difference does not specify their midpoint. The companion note gives explicit smooth, strictly convex abstract wells with unchanged width and different inverse-branch midpoints. That example is deliberately **not** asserted to be a family of Euclidean billiard contact actions. It is not a counterexample to A2's even-contact inverse, and the manuscript does not assert unrestricted asymmetric graph determination.

The corollary improves interpretation: it explains what the recovered profile measures in a preferred dynamical coordinate. It does not enlarge the information recovered by the earlier Volterra inverse. In particular, it does not close an additional physical geometric identification problem merely by changing from $\mathcal V$ to $\mathcal W$.

## 6. Audit of the principal inherited arguments

### 6.1 Relative determinant factorization

**Source:** `v4/10_boundary_layers.tex`, `lem:v4-halfline`, `eq:v4-half-amplitude`, and `thm:v4-factorization`.

The half-line Green kernel has the correct reflected exponential form. The local nonlinear Hessian perturbation has summable entries; the trace norm is controlled by those sums rather than by the number of sites. On the chosen small box, the logarithmic determinant series contains one trace-class factor and bounded remaining factors. Differentiation preserves the summability mechanism.

The two-ended comparison retains separated endpoint blocks, estimates the middle tail, and compares compressed finite Green kernels with the two half-line kernels. The off-diagonal kernels are exponentially small at that separation. Telescoping powers controls differences of logarithmic determinants in trace norm. Polynomial factors caused by any fixed derivative order are absorbed into a slower exponential rate. This is a genuine relative argument, not an absolute stationary-action estimate divided by an exponentially small flux.

I found no new error in this inspected factorization proof. Its finite-bridge existence, physical localization, and common-domain integration dependencies should remain explicit. This review is not a fresh line-by-line verification of every earlier geometric lemma or every collision-record appendix.

### 6.2 Independent-contact jet inversion and its physical image

**Sources:** `article/23_two_contact_rigidity.tex`, `article/24_physical_image.tex`, and `article/29_two_flight_benchmark.tex`.

The limiting two-contact block has positive antisymmetric factor

$$
m\tanh((m-1)\gamma)-(m-1)\tanh(m\gamma)>0.
$$

Strict concavity of $\tanh$ proves the inequality. The unequal-curvature column factors are accounted for, and no division by a curvature difference occurs. The theorem does not infer a general smooth graph from its formal Taylor series: the complete graph conclusion is made in the analytic even class.

The two-flight block is

$$
D_{q_m}\xi_{m-1}
 =-\begin{pmatrix}(1+2z)^m&1+2mz\\1+2mz&(1+2z)^m\end{pmatrix}
      \operatorname{diag}(k_mL_0^m,k_mL_1^m),
$$

where $z=c_0c_1-1>0$, $L_b=g/(2c_bz)$, and $k_m=4/[2^m(m+1)(m!)^2]$. The other-contact twist variation is essential to the term $2mz$. The action and amplitude variations, the two quadratic moment formulas, and the degree bookkeeping in the fixed Morse domain agree. Its antisymmetric factor is the strict binomial remainder. The explicit all-order triangular calculation, rather than only the displayed quartic example, establishes the inverse.

The support-function realization supplies actual analytic obstacles, not abstract profile coefficients. It preserves the selected support positions and curvature radii. The high-order area compensator has nonzero area derivative and does not change retained jets. The own-contact Jacobian entry is $-(2m)!\kappa_b^{2m}$; the opposite contact begins at higher order. The resulting finite-dimensional physical image is locally open in the stated jet coordinates.

These are among the more substantial geometric parts of the manuscript. The two-flight and limiting coefficient systems are locally equivalent **at fixed finite jet order**. That is not an equality of their complete smooth law functions, a uniform estimate as the jet order tends to infinity, or an equivalence of their noisy function-valued experiments. The current text correctly respects these limits.

### 6.3 Finite-window physical statistics

The corrected family restriction is essential. Within the constructed family, the nodal Jacobian is two Vandermonde blocks plus a higher-order remainder. Multiplication by the inverse Vandermonde leaves an error of order the fixed node spacing. The physical normalization multiplies rows by fixed positive constants, since the leading data are fixed in this family.

The proof restricts to a convex parameter ball on which the normalized Jacobian stays close to a fixed invertible matrix. Integrating along segments then proves bi-Lipschitz control; pointwise nonsingularity alone would not suffice. Ordered finite nets make the estimator measurable. The lower bound uses actual nearby physical tables, fixed probability margins, and conditional relative entropy for the allowed adaptive window choices.

The resulting $N^{-1}$ squared-risk order is correct for this regular finite-dimensional experiment. It is not evidence that the general smooth inverse has a sharp parametric rate. The manuscript now states that distinction properly.

### 6.4 Complete profiles, Abel inversion, and paid calibration

**Sources:** `article/20_boundary_compatibility.tex`, `article/21_abel_stability.tex`, `article/28_regularized_observation.tex`, and the calibration lemma in `article/27_profile_calibration.tex`.

The uniqueness argument for complete profiles is not merely formal deautoconvolution of Taylor series. With $k=x^{-1/2}V$ and $\ell=x^{-1/2}\widetilde V$, equality of their convolution squares gives $(k+\ell)*(k-\ell)=0$. Convolution with $x^{-1/2}$ and differentiation yield a second-kind Volterra equation with nonzero leading constant; Gronwall proves uniqueness on the collar.

The Abel transform is a linear operator, and its affine nullspace is removed only on the physical zero-value, zero-slope integrated-flux class. The stated two-sided inverse is in that specific differentiated data norm. Raw uniform probability error is not silently substituted for it.

The integrated flux gains two derivatives on the stated profile class. The positive-node reconstruction uses that gain for the approximation term, transports a structured smooth bridge error without mesh amplification, and amplifies scalar nodal noise by $h^{-5/2}$. Keeping these three errors separate yields the advertised sufficient accuracy exponent

$$
2+\frac{6}{m-1/2}+\frac{\gamma}{|\log\tau|}.
$$

The pilot really uses one- and two-flight bits with unknown smooth remainders. Its gap bracket is one-sided on the good event; its sample cost is bounded even on bad histories. Positive-node extrapolation estimates the leading coefficients rather than receiving them as an oracle. Projection onto supplied boxes controls subsequent allocations.

In the final experiment, the conditional mean of the scaled bit is exactly

$$
R H_{j,b}(d+\Delta),\qquad
\Delta=j(\widehat g-g),\qquad
R=\frac{\widehat A}{A}
       \frac{\sinh(j\widehat\gamma)}{\sinh(j\gamma)}.
$$

Translation is estimated before division by $d^2$, avoiding a false small-offset singularity. The pilot's smaller accuracy power is absorbed by the profile stage, with the stated upper multiplier bound. These steps address real statistical issues. I found no basis in the inspected proof for reopening an oracle, measurability, or uncharged-failure objection.

The rate is explicitly sufficient and depends on a supplied convergence certificate. It is not an intrinsic minimax information law. This limitation is not a correctness defect and does not become a requirement to prove an unrelated lower bound merely because a referee requests a demanding journal standard.

## 7. Why my four-journal recommendation remains negative

The manuscript now allows its mathematical contributions to be separated accurately.

The uniform smooth relative theorem is the strongest forward claim. It derives a physical two-ended limit from obstacle graphs rather than receiving canonical charts as input. The determinant method controls rare-event normalization and differentiated errors cleanly. However, the product structure has a local hyperbolic explanation, and the new density interpretation falls within scalar smooth linearization once the stable branch is constructed. V14 has clarified this relationship; it has not exhibited an additional dynamical phenomenon beyond it.

The independent-contact inverse is genuinely geometric in its stated even class, including equal curvatures. Its explicit last-jet blocks and physical realization deserve credit. The new v14 material does not strengthen that inverse. The finite two-flight result already recovers the same fixed-order geometry, so the long-bridge limit cannot be credited again as necessary for that finite-order determination.

The complete smooth invariant is more than a formal jet object, but its general conclusion is the recovery of symmetrized energy profiles, equivalently normalized stable-action widths. The Volterra and Abel structure explains both uniqueness and the observation topology. Recovering that well-defined invariant is useful. Calling it intrinsic does not turn it into a complete invariant of arbitrary asymmetric billiard geometry.

Finally, the statistical theorems respect the physical cost of observations and the unknown normalization. They complete the stated inverse experiment. The finite-dimensional rate is regular parametric behavior, and the full-profile exponent is a sufficient bound for a specified reconstruction. Neither supplies a separate sharp statistical principle in the current paper.

These are reasons to judge the **weight of the package**, not reasons to erase its components. My assessment is that the submission contains a technically substantial local programme but does not yet make a sufficiently compelling case for the exceptional conceptual depth or reach I would require to recommend one of the four requested journals. Another referee could weigh the smooth physical theorem more highly; this is not a theorem about journal suitability or a proof that no new result is present.

I specifically do **not** require unrestricted nonsymmetric boundary reconstruction, a global classification, an optimal full-profile minimax exponent, or an infinite-dimensional physical realization theorem as missing lemmas of this manuscript. They are different results. Nor do I recommend adding unrelated theorems or increasing verification counts to obtain a favorable verdict. The concrete v13 repair programme has been completed; the remaining negative judgment should be stated directly.

## 8. Specific corrections and presentation requests

**C14-1 — Scalar positioning and attribution; limited revision, not a correctness blocker.** In the subsection introducing `thm:v14-intrinsic-density`, add the one-dimensional smooth-linearization comparison. Distinguish the existence and uniqueness of the normalized scalar coordinate from the physically specific identification of the determinant amplitude. A citation and a concise product-formula explanation suffice. The companion note supplies a self-contained comparison, not a theorem to be advertised as a new independent discovery. This is an additional finding of the present review, not retroactive noncompliance with R13-1.

**C14-2 — Multiplier notation; minor.** Section 8 uses $\lambda=e^{-2\gamma}$ and $r_b=\sqrt{c_b/c_{1-b}}e^{-\gamma}$, whereas the two-contact section locally uses $\lambda=e^{-\gamma}$ and a ratio denoted $r_b$ without the exponential. The definitions make the formulas locally consistent, so this is not a mathematical contradiction. Nevertheless, in a long manuscript this is an avoidable source of wrong parity and normalization. A global convention such as $\rho=e^{-\gamma}$, $\lambda=\rho^2$, and distinct symbols for curvature ratios and first-flight contractions would improve the paper.

These changes would improve accuracy of positioning and readability. I do not claim that they alone would reverse the significance verdict. There is no request to delete historical material or to modify earlier author/review branches. Retaining proofs in the repository is compatible with making their dependency and contribution hierarchy explicit.

## 9. Independent diagnostics and their limits

I wrote and ran [verify_review.py](verify_review.py) without importing author or previous-referee code. Ordinary Python and `python -O` both passed **3,216 explicit checks**, and their JSON outputs were byte-identical. The check function raises explicitly rather than relying on removable Python assertions. [verification.json](verification.json) records the numerical results, cases, environment, and limitations.

The exact part contains **2,208 checks**: 90 two-type rational scalar-cocycle cases, exact normalized iterate identities through eight returns, 90 wrong-reciprocal negative controls, 99 positive rational two-flight block cases, direct quadratic Schur variances, and six abstract width-shear cases. These calculations test specified formulas; they do not prove the complete all-order billiard inverse.

The floating-point part contains **1,008 checks** using actual Euclidean local flight lengths

$$
\ell_b(u,v)=\sqrt{\bigl(g+\psi_b(u)+\psi_{1-b}(v)\bigr)^2+(v-u)^2}.
$$

It solves finite stationary boundary problems for equal-curvature even, unequal-curvature even, and unequal-curvature asymmetric graph patches. It compares a 64-flight determinant approximation to the half-line amplitude with the derivative along the truncated stable branch, and tests finite even/odd bridge factorization.

Across 24 endpoint/orientation cases, the maximum first-flight cocycle relative discrepancy was **$2.36\times10^{-14}$**. The maximum discrepancy of the normalized eight-return scalar derivative from the 64-flight determinant approximation was **$1.01\times10^{-11}$**. For the tested 20-flight bridges, the maximum normalized-flux factorization error was **$1.76\times10^{-11}$** and the action-separation error **$6.93\times10^{-13}$**.

These are double-precision consistency measurements, not certified error bounds. The 64-flight object is a truncation, not the exact infinite limit. The local graph patches were not completed into a global periodic table, and no physical trajectory simulation or empirical success-probability experiment was run. The abstract width examples are not asserted to be physically realizable. These restrictions are material, not boilerplate.

I did not rerun the author's advertised suites, compile the 129-page manuscript or its companion, verify all historical-retention counts, run remote CI, or independently re-referee every appendix theorem. The author reports those build/retention activities; they must not be presented as activities performed in this review. The source-pinned mathematical reading, the independent derivations, and the stated diagnostic runs are the basis of the present report.

## 10. Conclusion

V14 is a real and substantially successful response to the preceding report. The new proofs examined here do not justify an accusation of fatal mathematical invalidity. They do justify a more precise accounting of what is new: the physical amplitude is identified with a classical scalar density, and the existing complete energy invariant is interpreted as a normalized stable-action width.

My recommendation is therefore **negative for acceptance at the requested four-journal level, with the previous principal correctness/positioning requests closed**. The remaining dispute is the significance of the demonstrated package, not an unfulfilled instruction to repeat a repaired calculation. This report and its companion calculations should be used within that scope.

## Primary literature used for the present comparisons

**[L1]** J. De Simoi, V. Kaloshin, and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/html/1905.00890v4), especially the local normal-form discussion preceding Remark 1.8 and Section 2. This source supports the local analytic comparator; it is not cited as proving A2's probability theorem.

**[L2]** H. Eynard-Bontemps and A. Navas, *On the failure of linearization for germs of C¹ hyperbolic vector fields in dimension one*, [arXiv:2212.13646v2](https://arxiv.org/html/2212.13646v2), introduction, paragraphs distinguishing the classical smooth one-dimensional theorem from the low-regularity failures studied there. The scalar proof in the companion note is supplied independently; no low-regularity counterexample is transferred to A2's smooth setting.

Both sources were inspected in their versioned HTML form on 11 September 2026. This is a targeted comparison, not an exhaustive priority search or a new audit of every external paper in A2's bibliography.
