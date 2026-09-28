# Independent referee report on A2 v85

**Review date:** 18 September 2026  
**Reviewed branch:** `revision/a2-v85-finite-noisy-geometric-rigidity-2026-09-18`  
**Reviewed head:** `4f3d2ab5259b8deda67e1ec6ea9a6151a405ddd4`  
**Principal manuscript:** `papers/A2-v17-boundary-information-coarsening/rigidity_v85.tex`  
**Previous controlling report:** `reviews/a2-v84-independent-harsh-top4-2026-09-18/REFEREE_REPORT.md`

## Editorial recommendation

**Not suitable in the present form at the requested four-leading-general-mathematics-journal level.**

This is nevertheless a substantially stronger revision than v84. I do not see a short counterexample that invalidates the principal new theorems. My recommendation is based primarily on conceptual scale, theorem architecture, and the distinction between genuinely new hard mathematics and a careful synthesis of established mechanisms.

The revision closes several important objections from v84: it gives a finite structural result for rational-derivative detector spaces, connects finite categorical records to a quantitative metric certificate, gives confidence sets valid at singular channels, realizes the missing-clock ambiguity by actual simple metrics, and treats raw failed acquisitions explicitly.

## 1. Polar classification: correct-looking, but too narrow for the claimed scale

Theorem `thm:v85-polar` reduces regular separation to two finite obstruction families after differentiation: integer simple-pole residue vectors for secants and one/two-point double-pole directions for tangents. The proof by uniqueness of partial fractions and realization of the allowed residue vectors is clean. I found no immediate defect.

However, the conceptual step is modest. In the rational category, once the secant and tangent expressions are differentiated, the possible moving poles are already extremely rigid. Corollary `cor:v85-maximal` becomes still more elementary after imposing principal-part saturation, because that hypothesis makes the obstruction coordinatewise.

For the requested editorial level I would want a broader intrinsic theorem: for example a classification in a natural meromorphic/Chebyshev-type category, a sharp intrinsic sampling invariant, or a structural theorem from which the present rational examples follow as corollaries.

## 2. The pole clock budget is only a sufficient count

Theorem `thm:v85-budget` gives the sufficient number
[
N=D+6+b(E).
]
The Rolle/degree argument is internally consistent. But the result is not shown to be minimal, approximately minimal, or controlled by an invariant known to characterize optimal clock complexity.

The paper now has three clock-count mechanisms: the sharp polynomial (q+3) result, the generic analytic (d+5) result, and this pole-degree budget. What is missing is a theorem explaining them through one intrinsic complexity parameter and giving matching lower bounds.

## 3. “No supplied signal floor” should not be confused with uniform informative recovery

Theorem `thm:v85-confidence` makes a mathematically important distinction. Coverage is valid over the full compact forward class, including rank-deficient channels, while interval contraction requires the true parameter to lie in a regular class (mathfrak K_kappa).

This is correct. But the rate constant and contraction threshold still depend on unknown conditioning. Near singular channels the confidence interval may remain essentially the full action range.

Thus the theorem is adaptive in validity, not a uniform adaptive recovery theorem. A deeper statistical result would characterize the singular transition, establish honest locally adaptive diameter bounds, or prove the corresponding impossibility boundary.

## 4. The finite noisy metric theorem is mainly a composition theorem

Theorem `thm:v85-geometric` is the most important addition and genuinely closes a gap in v84. The logic is now complete:
[
	ext{finite records} 	o 	ext{action intervals} 	o
	ext{sampled boundary distances} 	o C^0	ext{ distance error}
	o C^2	ext{ metric error modulo gauge}.
]

Under its hypotheses, the proof is sound in outline. But the hard geometric step is imported from Stefanov--Uhlmann. The new contribution is the compatibility of the selective observation model with that local stability theorem, together with the elementary boundary-net interpolation bound.

The geometry remains local near a simple metric with s-injective ray transform, under a high regularity bound, and only modulo a boundary-fixing diffeomorphism. Those qualifications are now stated correctly. They also show why this is not a new boundary-rigidity theorem.

At the target level, a more consequential result would move one of the hard geometric boundaries: partial data, a larger global class, a non-simple setting, weaker regularity, or a genuinely new rigidity/stability mechanism.

## 5. The metric reconstruction remains set-valued

The object
[
widehat{mathcal G}
={g'inmathcal G: a_i^-le d_{g'}(z_i)le a_i^+}
]
is a valid confidence/feasibility set, and the theorem proves a small diameter modulo gauge.

This is not yet an effective inversion algorithm on an infinite-dimensional metric class. The finite dictionary corollary requires a supplied dictionary with certified boundary-distance approximation. Constructing such a dictionary is outside the theorem.

The manuscript should consistently call the result a stability/confidence certificate unless an effective geometric reconstruction procedure is added.

## 6. The parametric (N^{-1}) theorem is statistically standard once regularity is fixed

Theorem `thm:v85-parametric-risk` is correct-looking. The upper bound combines a finite-dimensional geometric design, root-(n) empirical probability error, and local inverse stability. The lower bound is a standard two-point KL/total-variation argument.

This establishes the correct (N^{-1}) squared-risk order for a regular finite-dimensional family, but that rate itself is not a deep new statistical phenomenon. The more interesting problem is the selective/singular regime: efficiency with unknown nuisance, degeneration of channel rank, or nonregular limit experiments.

## 7. The geometric clock threshold is sharp only for a very flexible nuisance class

Theorem `thm:v85-geometric-clock` is a real improvement over a purely scalar ambiguity argument. The scaling family (g_t=(1+t)^2g_0) produces actual non-boundary-isometric metrics, while endpoint-dependent reference delays and detector polynomials preserve the (q+2)-clock observations.

I do not see a short algebraic defect in the construction.

But the lower bound permits the reference delay and detector polynomial to vary independently at every boundary pair. That freedom is exactly what allows the scalar fibre to be pasted pointwise into geometry.

A much stronger result would establish a comparable threshold under structured nuisance: constant reference delay, a low-dimensional shared reference family, common detector coefficients, or quantitative smoothness coupling across boundary pairs.

## 8. The paper is coherent, but still lacks one invariant controlling the whole theorem stack

The manuscript now contains several distinct mechanisms: latent projective factorization, scalar action fibres, rational pole classification, generic analytic design, confidence sets, covering reconstruction, exact lift compatibility, boundary rigidity, parametric testing, and raw-attempt thinning.

The logarithmic quotient unifies the scalar layer well. It still does not generate the whole stack from one structural theorem.

At the requested editorial level, the paper needs a principle that makes several of these modules inevitable consequences rather than a sophisticated accumulation of compatible arguments.

## 9. Literature positioning remains incomplete

The new comparisons with Sontag, Alberti--Santacesaria, blind calibration, synchronization, Stefanov--Uhlmann, and standard minimax theory are useful. They are not yet sufficient for claims spanning finite analytic evaluation, rational/Chebyshev interpolation, nonlinear finite-measurement inverse problems, nuisance calibration, singular confidence sets, and boundary rigidity.

Every principal theorem should have a closest-predecessor paragraph stating precisely what abstract result was already known and what additional mathematical statement is new here.

## 10. Source-level audit

I checked the new proofs at theorem level.

- `thm:v85-polar`: no immediate defect found; the residue realization and tangent double-pole argument are consistent.
- `cor:v85-maximal`: correct-looking within the explicitly stated principal-part saturation class.
- `thm:v85-budget`: the degree/Rolle count is consistent; significance is limited by lack of optimality.
- `thm:v85-confidence`: coverage and regular-subset contraction are internally coherent. The observable-rank-to-latent-regularity step should be isolated as a lemma in a polished version.
- `prop:v85-grid`: valid finite exhaustive implementation; no efficiency conclusion follows.
- `thm:v85-geometric`: the boundary-net estimate and transfer to the imported metric stability theorem are correct in form.
- `cor:v85-budget-rate`: the exponent balance is correct.
- `lem:v85-geometric-design`: a standard but valid use of s-injectivity and the inverse function theorem.
- `thm:v85-parametric-risk`: the (N^{-1}) upper/lower order is correct-looking under the stated regularity/interior hypotheses.
- `thm:v85-geometric-clock`: the metric scaling fibre is plausible and consistent with the earlier complete scalar fibre theorem.
- `thm:v85-raw`: conditioning on observed retained counts preserves coverage; the positive acceptance lower bound enters only the rate.

I therefore do not base the recommendation on a discovered fatal proof error.

## 11. Reproducibility status

The branch records a passed algebra-only verification run, including charge-vector checks, saturated-space masks, scaling-fibre tests, forward-model checks, and a finite geometric derivative design. These are useful diagnostics but not proof certification.

At the reviewed head, the branch documentation itself states that the full source check and native TeX builds had not yet completed. The latest branch-specific manuscript workflow was still pending at the time of this review; an earlier run had been cancelled.

A final submission package should have successful source validation, native compilation, resolved references/citations, and rendered-PDF inspection. CI success would improve source readiness, not alter the mathematical recommendation by itself.

## 12. What would justify another review at this level

A further review would be justified by at least one change of mathematical scale, such as:

1. a detector-space theorem substantially broader than rational partial fractions, with intrinsic and near-sharp clock complexity;
2. a sharp geometric threshold under structured/shared nuisance rather than endpointwise free nuisance;
3. a genuinely new geometric rigidity or stability theorem rather than transfer to an existing boundary-distance theorem;
4. singular statistical theory describing the rank-degenerate regime and honest adaptive confidence diameter;
5. a single structural invariant that controls several currently separate modules.

## Final assessment

Revision 85 is the strongest and most coherent A2 version in this sequence. It materially closes several objections from v84, and its new principal proofs appear substantially more mature.

The remaining issue is not that the manuscript lacks results. It is that the results still decompose into relatively classical mechanisms whose synthesis is stronger than any individual conceptual advance. The polar theorem is narrow, the clock budget is only sufficient, the finite noisy geometry theorem imports the hard rigidity step, the parametric rate is regular (N^{-1}), and the sharp clock lower bound relies on endpointwise flexible nuisance.

For those reasons, my editorial recommendation remains: **not suitable in the present form at the requested four-leading-general-journal level.**
