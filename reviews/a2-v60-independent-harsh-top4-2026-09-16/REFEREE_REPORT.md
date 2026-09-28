# Independent referee report on A2, revision 60

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted referee-style assessment. It is not commissioned by any journal, is not an editorial decision, and is not a formal proof certificate. Correctness, reproducibility, originality, and exceptional significance are separate questions.

## 1. Recommendation, frozen object, and coverage

**Recommendation: decline at the requested highest general-journal level on the present exceptional-significance case.** I do not establish a new fatal mathematical error in this revision. In the scoped examination below, Proposition 12.13, Lemma 12.14, and Theorem 12.15 withstand scrutiny. In particular, the new theorem really does obtain an all-order local contact estimate from real density error, with an explicit analytic prior and loss of radius. It would be incorrect to repeat the v59 criticism that the complete analytic inverse has no real-observation consequence without acknowledging this new, conditional conclusion.

The adverse recommendation is therefore not a claim that these three statements are false. Equally, checking these statements and their principal interfaces is not certification of all 418 delivered pages. The significance judgment in Section 6 is reassessed on the stronger result rather than automatically inherited from the previous report.

| Object | Immutable identity |
|---|---|
| Review-ready branch | `revision/a2-v60-review-ready-2026-09-16` |
| Review-ready head | `80ad74228001e8d2c3228ff57aff6f9fb8fc0c39` |
| Actual compiled mathematical source | `1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5` |
| Manuscript subtree reconstructed from the frozen archive | `f8e130592a601e000be4ed7be76c9843c8603318` |
| Source branch | `revision/a2-v60-conditional-real-observation-2026-09-16` |
| Manuscript directory | `papers/A2-v17-boundary-information-coarsening/` |
| Native workflow / attempt / artifact | `35039952221` / `1` / `10424981887` |

The principal article has **117 pages**, the full technical manuscript **294 pages**, and the companion **seven pages**. The historical directory name does not identify the current revision. The GitHub comparison from the compiled source to the review-ready head contains three delivery commits and no intervening change to a compiled mathematical input. The new source file was also read directly at the compiled commit; its Git blob is `6e313047140dc9a8033124a1482fe28d282be935`, matching the downloaded source. [D1]

### Scope of this round

The complete new module, `article/23a3_conditional_observation_inverse_v60.tex`, lines 1–319, was read and checked. The audit follows its dependencies through the retained full analytic inverse, the same-type density-ratio inverse, and the variable-leading-coordinate splitting. It also re-examines the half-line and relative determinant argument, the principal headline statements, the older histogram interpolation route, and the current acquisition declaration. The current response, historical audit, dependency ledger, and literature note were read as provenance and claims to check, not as substitutes for proofs. [S1–S7]

This is not a fresh line-by-line verification of the complete principal article plus technical corpus. In particular, the entire earlier finite-action/full-phase construction, every global matching and moving-family proof, all support-coordinate conversion prerequisites, the full acquisition/calibration and stopped-experiment catalogue, and the companion's mathematical argument are not freshly certified here. Prior scoped assessments of those topics are not silently converted into a complete certification. The reproduction exercise covers every delivered page mechanically, which is a different assertion.

## 2. Disposition of the preceding report

The preceding v59 report is frozen at `f480cf1d099128c0c84df1ed149cff9b75e6ba2d`; its mathematical source was `b56282439324435668ae80be90207fe7f5eebbf2`. [R1]

| Earlier point | Present disposition |
|---|---|
| Complete action inverse versus merely bounded diagonal blocks | The complete inverse remains in place. No regression to a diagonal-only argument was found. |
| R59-E2: isolate the contracted-evaluation structure | Satisfactorily implemented by Proposition 12.13, with both directions of the criterion and a quantitative inverse bound. |
| R59-S1: real finite-order error does not control the same-disc analytic norm | Still true, and not contradicted. The new theorem instead assumes an outer analytic neighborhood and estimates on a smaller disc. |
| Real-observation significance of the complete inverse | Improved: Theorem 12.15 now provides a conditional all-order consequence from real density error, and a weaker-metric consequence with an additional real Lipschitz prior. |
| Explicit acquisition dependency and anchored-coordinate qualifications | Retained. These are closed corrections, not newly rediscovered gaps. |
| Highest-level significance | Reassessed below; not settled by source preservation or by the absence of a new error. |

The v59 report did not establish a mandatory core error requiring this new theorem. The author has extended a valid local inverse rather than repaired a theorem previously shown false. The old monomial example is a topology warning, not a counterexample to the new conditional estimate. [R1–R2]

## 3. Detailed assessment of the new mathematics

### R60-M1. The contracted-evaluation criterion is correct, including necessity

Proposition 12.13, principal pp. 54–55, considers a bounded holomorphic invertible multiplier and a sum of component-dependent contracted evaluations on the order-q vanishing subspace of a bounded-holomorphic function space. The source does not assume compactness without demonstrating it. Higher-order Schwarz gives

$$\|K|_{X_n}\|\le W\rho^n/(1-\rho^n),$$

so one fixed sufficiently high vanishing subspace has an invertible restriction of L=A+K by a Neumann series. The low Taylor quotient is finite-dimensional and lower triangular; its diagonal blocks are exactly the displayed B_n. These facts prove sufficiency by solving the quotient and then the tail. [S1]

The converse deserves attention. An invertible operator preserving a subspace need not, without further information, have an invertible quotient. Here the restriction to the tail has already been proved surjective. If a nonzero polynomial class p has Lp in that tail, solve Lt=Lp within the tail. Then p-t is a nonzero kernel vector of L. This proves necessity without assuming that the full inverse preserves the tail in advance.

The compactness proof is also valid: Taylor truncation is evaluated only at arguments strictly contracted into the disc. The number of independent source coefficients is d(n-q), irrespective of the number of visits, and the operator-norm error tends to zero. The proof does not require convergence of Taylor partial sums in the full-disc H-infinity norm. The last inverse-function step is standard; the specifically billiard-related work remains the earlier construction of the actual stationary derivative.

An independent scope control illustrates why the finite nonresonance condition cannot be omitted. On the unit disc and X_3, put

$$Lf(z)=(1+z/4)f(z)-8(1+z/8)f(z/2).$$

The multiplier is invertible, the argument contracts, and the high tail is small, yet f(z)=z^3/(1+z/4) is a nonzero kernel vector. Its degree-three block vanishes. With the admissible majorants a^{-1}=4/3, W=9, rho=1/2 and m=7, the tail bound is 12/127<1. This supports, rather than contradicts, the printed criterion. It is an abstract operator example, not a billiard counterexample. [D2]

### R60-M2. The interpolation lemma has the correct constants and integer balance

Lemma 12.14, p. 56, assumes

$$0<s<r<\varrho<R,\qquad r+2s<\varrho,$$

and uses A_0=2(r+s)/s, b_0=(r+s)/(varrho-s)<1 and

$$\vartheta=\log(1/b_0)/\log(A_0/b_0).$$

At the Chebyshev roots, the monic nodal polynomial satisfies

$$|P_n'(x_k)|\ge n(s/2)^{n-1}.$$

The n basis polynomials therefore give the first error bound epsilon A_0^{n-1}, not an unaccounted factor n times that quantity. The contour lies strictly within the holomorphic domain, and the product estimates for P_n give the second error term. Thus

$$\|F\|_r\le\epsilon A_0^{n-1}+\frac{\varrho}{\varrho-r}M b_0^n.$$

For x=log(M/epsilon)/log(A_0/b_0) and n=ceil(x), the inequalities n-1<=x and n>=x bound the two terms by their respective constants times M^{1-vartheta} epsilon^{vartheta}. The separate treatments of epsilon=0, epsilon=M and M=0 are consistent. I find no rounding error, illicit boundary contour, or missing exponential factor here. [S1]

The lemma is an elementary explicit instance of conditional propagation of smallness, not a new general analytic-continuation principle. Trefethen's primary paper discusses precisely the distinction between unrestricted continuation and continuation with a complex-domain bound; the present manuscript supplies its own interpolation proof rather than attributing its exact constants to that paper. [L1]

### R60-M3. The two-disc inverse construction is not circular

Theorem 12.15, pp. 56–58, requires two compatible constructions: a forward action map on an outer disc, and a complete inverse on an inner disc. Simply restricting an inverse originally constructed on the larger disc would not, by itself, prove an inverse estimate in the smaller-disc norm. The source instead applies the local inverse theorem at the base on a smaller disc and chooses the input neighborhood before examining observational errors. [S1–S2]

The joint map is (g,psi) -> (g,S_g(psi)). The finite leading-coordinate extension of v59 supplies its inverse when the gap and action Hessians are retained. Splitting the action into its Hessian and order-three tail is bounded on the inner disc, since |S_b''(0)|<=2 r^{-2}||S_b||_r. Thus those Hessians can be extracted from the action, rather than supplied as additional observations. There is no hidden assumption that the curvatures agree.

The neighborhood is the intersection of the outer forward neighborhood with the restriction preimage of one inner inverse ball, then shrunk to a bounded ball. Local continuity of the forward map gives a common outer action bound. The actions from the two constructions agree on a small real collar by physical half-line uniqueness, then agree holomorphically on the inner disc. This is an actual compatibility argument, not a claimed gain of analytic radius by the inverse.

The order of choosing radii is consistent: r<R/4, varrho=R/2, s_+<r/2 and s<s_+ imply r+2s<varrho. The physical positive-density square can be made smaller without affecting this conclusion. The analytic neighborhood is additional geometric information; it is not inferred from a small data residual.

### R60-M4. Real density extraction tolerates different nonanalytic recording factors

For the stipulated recorded density

$$f(u,v)=cU(u)V(v)\{d-S(u)-S(v)\},$$

the separate factors and c cancel in the four-density ratio. With t=S/(d-S), the ratio is 1-t(u)t(v). The positive scalar anchor is t(a), and the signed action is recovered by t -> dt/(1+t). Positive density and anchor margins control the necessary divisions uniformly. The denominator q_f+q_tilde_f in the difference of the two square roots is bounded below. This proves the real C0 action estimate using no derivatives or complex extensions of U and V. [S1, S3]

Importantly, the comparison is between two admissible endpoints of the argument. It does not require every density on the line segment joining them to satisfy the factorization. Odd action coefficients are retained. The gap is observed separately; d, origins, signs, and units are fixed here.

Applying the scalar restriction lemma to the bounded holomorphic action difference and then the inner inverse gives

$$\|\psi-\widetilde\psi\|_r\le C\{e_g+e_\infty^{\vartheta}\}.$$

Cauchy's coefficient bound then yields the stated simultaneous weighted sum from degree two onward. The constant is independent of truncation order in this analytic weighted sense, not in the maximum norm of unweighted derivatives. This does remove the growing-order real differentiation cascade from the local estimate. The argument is a valid conditional observational consequence of the complete inverse.

### R60-M5. The weak-metric exponent and histogram bias are correctly qualified

With a common Lipschitz bound on a larger positive square, convolution on the interior square gives

$$e_\infty\le C_H h+C h^{-2}e_1.$$

The choice h=h_0 e_1^{1/3}, with h_0 below the collar distance, yields the exponent 1/3. The action inverse therefore receives exponent vartheta/3. The proof keeps the smoothing kernel inside the larger square, and handles e_1=0 by a limit. The convention e_1<=2 TV for the full probability laws is correct. [S1]

For grid cells of side at most delta, each density differs from its cell average in L1 by at most sqrt(2) H |Q_+| delta. Adding both errors gives exactly the stated bias term. The outside category makes the observation vector a probability vector, although the proof only uses the interior cells. A fixed nonzero mesh does not produce exact all-order recovery merely because the cell-mass residual vanishes.

The regularity assumption has real content. For generic two-dimensional Lipschitz functions, the tent h(1-|x|/h)_+(1-|y|/h)_+ has supremum h and integral h^3, with a uniformly bounded Lipschitz constant. The unscaled tent has supremum one and integral h^2, but an unbounded Lipschitz constant as h tends to zero. These are scope checks for the interpolation step, not a minimax lower bound within the constrained billiard-law class. Similarly, positive sinusoidally perturbed densities can have identical masses on one grid but nonzero L1 difference of order delta under a fixed Lipschitz bound. That general-density example is not being passed off as a pair of realized billiard tables. [D2]

## 4. What remains of the analytical core and the older conclusions

### R60-C1. The relative determinant mechanism is still the substantive forward step

Re-reading the half-line and two-ended argument confirms that the source works with the exact normalized cofactor identity before taking a long-flight limit. The perturbation is localized near both ends, its discarded tails are estimated in trace norm, and the compressed finite Green operator is compared with a direct sum of half-line operators. Remote reflections and cross-end blocks have exponential margins. The logarithmic determinant comparison uses telescoping powers with a trace-class factor, not a dimension-times-operator-norm shortcut. [S4]

The action and relative twist estimates are distinct. A small absolute action error cannot simply be divided by the exponentially small reference twist. The source avoids that mistake. The common-domain Morse integration likewise precedes the offset differentiation. The new observation theorem depends on this forward mechanism but does not replace it.

The retained v59 analytic argument has a different purpose: the stationary envelope is an invertible initial multiplier plus contracted later visits. The initial graph derivative is not evaluated at an unprotected boundary argument, and the terminal orbit term is removed only after its norm decay. Proposition 12.13 is a useful abstraction of that mechanism, not an independent source of physical stationarity. [S2]

### R60-C2. The comparison with the older histogram result is meaningful but local

The older quantified-law section obtains a fixed-order C^m density estimate of the form eta^{1/(m+3)}, then propagates finite jets with order-dependent inverse constants and separately controlled global continuation. The new argument instead obtains one real action estimate, propagates it into an inner analytic disc, and invokes the complete inverse there. Hence all local contact coefficients are controlled together with one fixed exponent and only a first-order density prior in the weak-metric clause. That is a real improvement in the form and local scope of the conclusion. [S1, S6]

It is not a replacement for the older whole-table theorem: it assumes one selected local analytic inverse neighborhood and does not control continuation around an obstacle, select a matching branch, register noisy unknown origins, or give a uniform charged acquisition budget. These are printed limitations. They should not be relabeled hidden gaps, but they delimit the contribution.

### R60-C3. The global and acquisition scopes have not silently expanded

The principal global datum remains a finite list of function-valued conditional laws, gaps, and marked channel/incidence/deck information. Its exact global conclusion has finite alternatives for noncircular obstacles and uniqueness under proper asymmetry. Its finite-scalar conclusion is local to an immersed finite-dimensional model. The v60 theorem does not identify these three information regimes. [S5]

Corollary 19.9 still explicitly imports full Theorem F.47.3 and its analytic-family, chart, sensor, calibration and charged-preparation hypotheses. The pilot records planar endpoints, the clock, and preparation outcomes in its specified frames. That is not a transverse-histogram-only pilot. The compact family is contained in one persistent asymmetric design neighborhood. Reading this dependency is not a fresh proof of the full acquisition theorem. No new acquisition input is used by Theorem 12.15. [S7]

Conditional-law accuracy alone does not bound preparation cost when both recording efficiencies can be scaled toward zero. Revision 60 continues to keep this distinction explicit. There is no basis in the new subsection for reopening the previously closed dependency objection.

## 5. Literature and attribution

The targeted primary-source check was refreshed. Trefethen supplies established conditional-continuation context; the printed elementary lemma and composition with the action inverse must be judged for their particular role here, not promoted into a new general continuation theory. [L1]

Finamore–Leguil's finite-horizon Sinai result uses an enriched marked length spectrum. De Simoi–Kaloshin–Leguil treats analytic open billiards with non-eclipse and stated symmetry/genericity hypotheses. Neither record establishes an equivalence between its observation and the present conditional endpoint-law datum. Osius supplies association-model context for eliminating marginal factors, not the billiard relative determinant or action inverse. Florio–Leguil's version-5 notice removes an affected geometric open-billiard spectral-rigidity assertion; it is not an available competing theorem or premise. [L2–L5]

This is a scope and attribution check, not an exhaustive priority search or a proof audit of those papers. I do not claim that the principal theorem is already known. The manuscript appropriately attributes the structural/Fredholm suggestion to the author-requested v59 memorandum without describing that memorandum as commissioned journal review.

## 6. Highest-level significance and editorial disposition

### R60-E1. The stronger observation theorem deserves credit, but is not an independent second breakthrough

The strongest current mathematical case is a coherent chain: relative long-bridge normalization retains nonlinear local actions; actual-smooth stationary factorization identifies the contact filtration; the complete analytic action map has a local inverse; and an analytic prior now yields conditional all-order local stability from real laws. The last arrow was missing as an established conclusion in v59 and is supplied in v60. It cannot fairly be dismissed as a source-counting exercise.

Nevertheless, once the v59 inverse and the exact density identity are available, the new proof consists of an elementary conditional-continuation estimate and standard interior interpolation, composed with that inverse on a correctly chosen smaller disc. The technically delicate part is compatibility of hypotheses and radii, which the author handles. The final functional analysis, scalar continuation, and smoothing steps should not each be counted as separate exceptional innovations. Their usefulness is not the same question as their independent depth.

My highest-level placement reservation therefore remains. The paper's proposed exceptional significance still rests chiefly on the relative boundary/action mechanism in a deliberately selected, marked alternating-channel observation model. The global registration and lattice conclusions are genuine outputs, not supplied geometry; however, much of the later reconstruction is exact analytic propagation, finite congruence matching, and a displacement cochain once the local images are known. The conditional local estimate strengthens the mechanism without establishing a comparably stronger global or acquisition theorem.

Rich function-valued observations are not inherently disqualifying, nor is a 117-page principal article. The concern is the demonstrated reach and concentrated mathematical depth of this particular mechanism relative to the requested general-journal placement. I remain unconvinced by the present case. This is a reviewer judgment, not evidence that the results lack novelty or an assertion that a specialist must agree. The targeted literature check does not justify a stronger claim of redundancy.

### R60-E2. A further routine repair-only iteration is not the response requested by this report

No new mandatory core proof repair is established here. It would be misleading to label another small lemma, an extra finite diagnostic, or a new preservation certificate as closure of this placement assessment. In particular, proving a different unmarked inverse problem, ordinary marked-length rigidity, or globally finite-information recovery is not imposed as a correctness repair to the stated theorems.

The principal and complete technical entries should remain distinct. Arbitrary deletion of mathematical content is not requested. The new structural explanation is useful and already implemented; another abstraction section is not needed merely to answer this report. Any subsequent independent editorial assessment should focus on why the relative/action mechanism itself constitutes an exceptional advance, with the conditional observation consequence credited at its actual strength.

## 7. Disposition codes

**R60-D1 — New mathematics:** Proposition 12.13, Lemma 12.14, and Theorem 12.15 are accepted within the stated scoped examination. No new mandatory core repair or realized counterexample is established. This is not a certificate for every theorem in the delivery.

**R60-D2 — Updated contribution:** retire the unqualified objection that the complete inverse has no real-observation consequence. The new conditional inner-disc result is valid; the unconditional same-disc implication remains unclaimed.

**R60-D3 — Preserve distinctions:** retain the a priori local analytic neighborhood, radius loss, fixed contact conventions, density and anchor margins, extra Lipschitz hypothesis, grid bias, and separation from global acquisition. These are correctly implemented assumptions and restrictions, not outstanding repairs.

**R60-D4 — Recommendation:** decline at the requested highest general-journal level on the present exceptional-significance case, rather than invite another nominal technical-repair round. An alternative positive placement judgment would need to engage the core mathematical mechanism, not revision numbers or delivery certificates.

## 8. Reproduction and evidence limits

The native artifact SHA-256 is `cc1d87a5454d2dd2637a8f3f741ee00cdb7e379f1b2138a02fb20649ecdcafc8`. Independent verification checked lengths, SHA-256 values and Git blob identities for **739 frozen files**, reconstructed the manuscript subtree in Section 1, checked **123 distinct active inputs**, and verified **45 build-report evidence entries**. The per-entry active counts are 113 full, 44 principal, and one companion. Comparing the v59 and v60 frozen active sources independently found **114 unchanged inherited paths and eight changed inherited paths**; the new subsection is the additional active path. This is a byte-level comparison, not a semantic census of distinct theorems. [D1]

Fresh builds of all three entries succeeded with shell escape disabled and regenerated auxiliary files. All **418 pages** match the native PDFs in extracted text and same-renderer 72-dpi RGB arrays. PDF bytes differ. The final full-manuscript log has three underfull-box notices; the principal and companion have none. No undefined-reference/citation, missing-character, overfull-box or LaTeX-error match was found in the final logs. Actual visual inspection covered principal pp. **54–58** at 108 dpi; no clipping or unreadable formula was observed there. All-page computational parity is not all-page visual inspection. [D1]

The new independent diagnostic imports no author checker. It verifies an exact 12-dimensional nonlinear weighted-composition quotient and the resonant kernel control; 246 interpolation rounding choices; 2,460 Chebyshev nodal-derivative inequalities; 300 exact-norm monomial cases; 729 rational four-density identities and 81 signed action recoveries, including positive nonanalytic nuisance factors; and general weak-norm/grid-bias controls. Ordinary and optimized Python emit identical JSON. The scripts do not certify a complex Banach contraction, an infinite-dimensional inverse, an infinite trace-class limit, global continuation, or a statistical risk theorem. The author's own finite/preservation checker was not rerun. [D2]

## Source keys

All S-keys refer to compiled source `1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5` under the manuscript directory in Section 1. [Immutable source root](https://github.com/TrillionniumFoundation/theta-theory/tree/1a55bfb1102c3eab9cdcd6a292c5ef9070ea14a5/papers/A2-v17-boundary-information-coarsening).

- **S1:** `article/23a3_conditional_observation_inverse_v60.tex`, lines 1–319; Proposition 12.13, Lemma 12.14, Theorem 12.15, principal pp. 54–58.
- **S2:** `article/23a2_analytic_contact_inverse_v59.tex`, especially protected-domain construction, envelope operator and lines 249–354, including the joint leading-variable inverse. This inherited module is byte-identical.
- **S3:** `article/23f_single_offset_law_inverse_v42.tex`, especially lines 1–125; exact four-density identity, scalar anchor and fixed-order norm conventions.
- **S4:** `v4/10_boundary_layers.tex`, lines 1–390; half-lines, normalized determinant comparison and common-domain physical law. Earlier full-phase prerequisites are not freshly certified.
- **S5:** `rigidity.tex`; `journal/00_principal_introduction_v56.tex`; `journal/01_structural_statements_v56.tex`; principal observation and headline scope. The full global proof catalogue is not freshly recertified here.
- **S6:** `article/23k_quantized_law_stability_v46.tex`, especially lines 1–160; quantified classes and older fixed-order histogram interpolation. This comparison is not a new audit of every global continuation estimate.
- **S7:** `article/23j_generic_finite_channel_rigidity_v45.tex`, lines 492–549; `journal/DEPENDENCY_LEDGER_V60.md`. Explicit acquisition application and additional hypotheses.
- **R1:** [Previous v59 report](https://github.com/TrillionniumFoundation/theta-theory/blob/f480cf1d099128c0c84df1ed149cff9b75e6ba2d/reviews/a2-v59-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md).
- **R2:** `RESPONSE_TO_REFEREE_V60.md`, `HISTORICAL_DERIVATION_AUDIT_V60.md`, and `LITERATURE_CHECK_V60.md` at the compiled source.
- **D1:** `AUDIT_LEDGER.md` and `AUDIT_RESULTS.json` in this review directory; independent rerun of the v59 `verify_delivery.py`, retained at the R1 commit. The full repository tree was not independently reconstructed; the manuscript subtree was checked against the pinned native record, with direct GitHub checks of the new module and source-to-ready comparison.
- **D2:** `independent_checks.py` in this review directory. Full emitted diagnostic JSON SHA-256 in this environment: `ec5e8f7ea182118cc498407be47a33dee71de9aca1cba3cc8ab55215efafa5b6`.
- **L1:** Lloyd N. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, [arXiv:1908.11097](https://arxiv.org/abs/1908.11097), especially the bounded-domain formulation on p. 2; primary PDF and record checked September 16, 2026.
- **L2:** Douglas Finamore and Martin Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, [arXiv:2510.18983](https://arxiv.org/abs/2510.18983), primary record and its enriched-datum description checked September 16, 2026.
- **L3:** Jacopo De Simoi, Vadim Kaloshin and Martin Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, [arXiv:1905.00890v4](https://arxiv.org/abs/1905.00890v4), primary record checked September 16, 2026; related DOI 10.1007/s00222-023-01191-8.
- **L4:** Gerhard Osius, *Asymptotic inference for semiparametric association models*, Annals of Statistics 37 (2009), 459–489, [arXiv:0903.0702](https://arxiv.org/abs/0903.0702), DOI 10.1214/07-AOS572; primary record checked September 16, 2026.
- **L5:** Anna Florio and Martin Leguil, *Smooth conjugacy classes of 3D Axiom A flows*, [arXiv:2010.04120v5](https://arxiv.org/abs/2010.04120v5), including its correction notice; primary record checked September 16, 2026.
