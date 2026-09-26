# Response to r29 and continuation beyond the published v44 revision

**General Theta Foundations I — Revision 46**  
**Certified Positive Realization of Numerical Word Experiments**  
27 September 2026

The controlling report is `reviews/general-theta-foundations-i-v43-word-profiles-arithmetic-fluctuations-harsh-top4-r29-2026-09-26/REFEREE_REPORT.md`, frozen at `6e8a9504a1a0820e6195317df885d99aed06c878`. No later report was found in the initial remote branch survey. The report concerns v43, not v44 or v45. We inspected the complete published v44 source and artifact and retain its response achievements explicitly rather than presenting them as discoveries of v46. A separate v45 work branch was still staged/queued. Its files are inherited unchanged in the base tree, but are not part of the mathematical claims assessed here.

## 11.1 — the finite-type minimum

The sharper `min{1/2,r(1+h)/(2r+1+h)}` remains in `metric-width.tex`, unchanged from v44. There is a logical distinction worth retaining: from `L <= min(a,b)` one may always infer the weaker bound `L <= b`. Thus the report's example `b=3/5 > 1/2` does not disprove that weaker inequality. Retaining the minimum is preferable exposition and removes the ambiguity without a false confession of a counterexample. All subsequent limiting exponents remain as before.

## 11.2 / Sections 5 and 6 — exact realization and whole-run compatibility

The v44 normalized Hankel characterization, one-row separation dual, and constant separate planar ranks are retained with complete proofs in `hankel-compatibility.tex`. The v44 distortion-rate/enclosure inequality remains in `distortion-rate.tex`. Neither is attributed to this revision.

The new `thm:gram46` makes the whole numerical task finitely certifiable without introducing the exponential suffix table. Its augmented target/candidate matrices use the execution-order transpose explicitly. A Gram recursion equals the sum of squares of all seed/word/query residuals. Exact zero, not a floating-point small number, means every numerical probability agrees. The backwards Gram recursion also constructs an actual failing word when the proposed machine is not exact. Stochastic normalization, decoder bounds and all seed rows are checked separately. Ordinary signed low rank is not substituted for positive realizability.

With the displayed horizon and width profile as finite input, the same equations form a polynomial-size existential-real exact feasibility system. Auxiliary Gram variables are constrained by their recurrence, so arbitrary positive semidefinite matrices cannot be substituted for them. No hidden-state observability or rank-minimality hypothesis is used. Existence over real algebraic data yields an algebraic machine by real-closed-field sampling. This is a decidability/representation-size result, not polynomial-time synthesis or a rational exact-witness theorem.

## A stronger finite-error objective

The new `thm:moments46` concerns the actual optimum over all legal machines, not accumulated local deficiencies. For `Q=|X||A|^N D`, globally minimized even moments obey `ell_p <= E <= Q^(1/p) ell_p`. The first bounds increase and running minima of the second bounds decrease to the same true optimum. A minimizer of the p-moment is used as a candidate for the sup-error minimum; there is no illicit min/max exchange. Symmetric-power recurrences make each moment finite without word enumeration. A finite root certificate bounds a given candidate, but a numerical local optimization cannot certify the globally minimized ell_p.

The new `thm:grid46` supplies an alternative finite two-sided certificate by exhaustive rational row grids, with an explicit TV rounding budget and the same available boundary profile. A strictly positive margin allows dyadic approximation. Equality at the optimal boundary need not allow rational coefficients. The exact optimum is 1-Lipschitz in the specified numerical target, so strict feasibility/infeasibility margins survive bounded perturbations.

The finite planar example `prop:smallfront46` has an actual exact error frontier: rho/2, rho/4, 0 for one, two and at least three command-boundary labels. The proof bounds every affine two-state segment, and the code supplies matching rational rows and exhaustive finite grid optima. The zero-command example is not advertised as a new growing-horizon exponent; identity-only horizons use the narrowest cut. The held answer remains a separate two-label cut.

## Literature and complexity boundary

The classical nature of the Gram/tensor mechanism is explicit. Tzeng's 1992 equivalence result is a primary antecedent; Balle–Panangaden–Precup's Theorem 2, Theorem 11 and Section 5 already relate weighted series, Hankel rank and squared-error constructions. Their all-length weighted approximation does not impose the present stochastic and bounded-decoder feasible set or the finite worst-word objective. These differences identify the task; they do not justify claiming the Gram trick itself as new.

Ohta's reachable/null-space tensor reductions and Finesso–Grassi–Spreij's divergence-based HMM realization are compared in their stated stationary/probabilistic settings. The inherited positive-cone comparison with Benvenuti–Farina remains. A new categorical-output proposition transfers Shitov's Theorem 2 and Corollary 3 through an explicit stochastic normalization. The underlying hardness and field distinction are external mathematics, with the normalization proved here. This categorical variant is not silently identified with selected binary coordinate queries, and the hardness conclusion is not asserted for the fixed-dimensional orthogonal subclass.

The finite-input representation, exponential word/sign systems when used, fixed-dimension symmetric-power condition, and absence of a polynomial-time global optimizer are stated adjacent to the claims. The primary-source audit distinguishes full parsed papers and inspected theorem pages from metadata-only access.

## 11.3–11.7 and minor comments

The title retains the requested series prefix and gives a subject-specific subtitle. The abstract immediately specifies nonuniform clocked atomic-row label width. The inherited uniform finite-bit theorem still separately charges the horizon, arithmetic, random words and scratch space. The two-label answer cut and distinction between fixed-length and anytime tasks remain explicit. Every v44 finite-bit proof and the actual integer-interval compiler are unchanged.

The fixed alpha, r, delta, rho and epsilon dependence remains in the arithmetic statements. Bugeaud–Laurent supplies the ordinary/dual terminology; the DGLPS comparison remains version-pinned. Unit-circle center restrictions, the Gamma=1 impossibility case, natural logarithms, rational s0 approximation, and finite phase-tag costs are retained. No new independence assumption is imposed within packets.

The existing profile comparison remains one-sided. The moment theorem characterizes a finite optimized error through a convergent hierarchy, not equality of distortion and enclosure profiles. We do not announce a new sharp noncommutative nongapped exponent, a Liouville limsup, or a closed formula for every finite width.

## Pipeline and preservation

The r29 report, the frozen Round-Seventeen dependency ledger, the complete v44 native sources and its source-bound artifact, and its inherited v43 mathematical modules were consulted. The main analytic DAGs still require their own Fourier/local-limit, stopped-LDP, global-kernel, nonlinear-semigroup, graph-core, filtering and optional-projection arguments. None is inferred from finite matrix recurrences. We do not claim to have re-proved every archived page.

All v44 mathematical proof modules are retained; current changes are additive apart from the title/abstract, explicit new-contribution prose and bibliography. The complete v44 PDF is preserved byte-for-byte, and its cumulative volumes remain optional archives. The r29 review and all v44/v45 paths and branches are untouched. There is no claim that an independently produced v45 draft was reviewed or superseded mathematically.

The next referee can inspect `thm:gram46`, `thm:moments46`, `thm:grid46`, `prop:smallfront46`, and the clearly delimited `prop:hard46`. The program checks exact candidates and four fully enumerated one-cut grids; generic real quantifier elimination, large-degree global minimization and independent priority certification were not executed. Build receipts state only operations actually performed. A successful build is not an external mathematical endorsement or a journal decision.
