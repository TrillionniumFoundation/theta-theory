# Response to the A1 English-v3 referee report

**New submission:** English revision 4.0, 6 September 2026, Qian Qi.

**Controlling report:** `reviews/a1-english-v3-2026-09-05/REFEREE_REPORT.md`, review commit `574f2315a136d8b401644d8a3eeeb93c87887010`.

**Reviewed source:** submission `025a9b3fdfd9ffa86e6ae2924f8b5e5b1b58ddd6`, A1 source tree `ec09fa385c5fdcc5f2aece59a6b7f0806bfbb8ea`.

This response adds structural and performance theorems to the complete valid apparatus/filter/control chain. It does not answer the significance objection by changing the target to a weaker claim, dropping the failure record, removing the continuous-state lower bound, or labeling the broader program impossible. Editorial significance remains for a referee to assess from the new results; an author response is not an acceptance certificate.

## M1 — Smooth dynamics do not regularize an arbitrary Borel terminal report

**Action:** Corrected in `sections/A_scope_repairs.tex`, Theorem A.3 (`thm:transport-prep`).

The dynamical conclusion now concerns event times, event states, and the terminal **state**. Report regularity requires a specified jointly C^r map with uniform bounds. For distribution-valued response the report lives in a fixed smooth reporting manifold or a specified fixed ambient torus; the dimension in s>d/2+r is explicitly the dimension of the Sobolev reporting space. The first and higher report derivatives include the parameter dependence of that report map.

The no-event counterexample x'=a, x(0)=0, Y=1{x(1)>0} remains a regression example. It is a valid measurable experiment, but it does not satisfy the smooth-report clause. It is not misrepresented as a counterexample to the separately integrated polynomial detector kernel.

The historical companion's state/readout distinction was consulted directly. Its complete source is preserved. Current Appendix A is the sharpened statement when comparing editions. Transported and weighted preparations, all normalizer derivatives, and integrable jet envelopes remain in the theorem; no restriction to fixed preparation replaces them.

## M2 — Five coordinates are not always five intrinsic dimensions

**Action:** Corrected in the abstract, Theorem 1.1, and Section 5. The body is a compact moment body **in R^5**, of intrinsic dimension **at most five**.

Theorem 8.1's range argument also identifies the affine dimension of a general gate moment body as the rank of its integrand Gram matrix. In the report's lambda=0, G=1 example the continuation coordinate belongs to the span of the four likelihood moments, giving dimension four in the nondegenerate mode. The separate sharp 3n likelihood-state theorem is retained, with its open-family and continuous-encoding hypotheses unchanged.

**Additional A.2 clarification:** Dotted bulk derivatives are explicitly Eulerian, at fixed spatial position. An outward-normal outer-boundary flux is written explicitly when the outer boundary moves. Both internal density traces remain. Fixed outer domains are the zero-outer-flux special case, not an implicit double count of material derivatives.

## E1 — An engineered cubic detector needs a structural class theorem

**Action:** Added Sections 8 and 10; the collision geometry and exact cubic kernel remain intact.

The apparatus can indeed evaluate a known firmware function on the measured impact radius. Cubic closure is an observation design property, not a consequence forced by chaos or mechanics alone. Section 10 states this separation before constructing the more general detector.

**Theorem 8.1 (`thm:rank-criterion`)** gives a necessary and sufficient coefficient-Gram condition for a full-dimensional attainable failure family. It provides the explicit parameter-independent gate g_z=1/2-h^T Gamma^{-1}z, a realizable coefficient ball of radius (1/2-eta)lambda_min(Gamma)/||h||_infinity, and a quantified perturbation margin within the normalized degree-q apparatus class. Rank-deficient constraints are characterized at the factor-family level without asserting an unjustified dimension theorem for their products.

**Theorem 10.2 (`thm:smooth-surrogate`)** addresses nonpolynomial physical detector changes rather than coefficient roundoff. Bernstein interpolation of a positive normalized mark family remains positive, normalized, and physically realizable by the same prepared-coordinate inverse CDF. The placement and collision masses are retained exactly. Its degree-(m+1) raw kernel has positive Bernstein coefficients and an exact (m+1)N+1 coefficient likelihood state. Uniform mark Lipschitz or second-derivative bounds give one-step TV errors p_max L1/(4 sqrt(m)) or p_max L2/(16m), and explicit whole-policy regret and degree bounds. The payoff oscillation and its possible horizon dependence are printed; no horizon-uniform complexity claim is hidden in big-O notation.

These results supply an open same-degree class theorem and a constructive approximation theorem for a larger smooth physical class, rather than presenting one chosen cubic as a universal algebraic law.

## E2 — Bernstein arithmetic, beta mixtures, and the actual novelty burden

**Action:** Expanded the theorem-level comparison in Section 1 and the bibliography; added Theorems 8.1–8.2.

The Bernstein convolution is explicitly identified as established polynomial arithmetic, with Farouki–Rajan cited. No blanket numerical-conditioning guarantee is inferred from positivity. The beta-mixture identity is compared with Petrone–Wasserman's Bernstein-density posterior work; that density-estimation problem is distinguished from a finite-budget static-radius likelihood. The paper does not claim either classical identity as its central advance.

The general intrinsic lower bound is qn, obtained only after the physical gate family's full rank has been verified. An explicit right inverse produces the open family, the coprime-product differential gives rank qn+1 before normalization, and a local section plus invariance of domain gives the continuous-encoding lower bound. A full-support prior is still necessary for the stated posterior version. When degree elevation from q to m is required for positive arithmetic, the mn+1 stored coefficients are redundant; mn is not claimed as a sharp intrinsic lower bound.

The closest-work comparison is targeted, not an exhaustive priority search. Farouki–Rajan, Petrone–Wasserman, Kulik–Tymoshkevych, and Feinberg–Kasyanov–Zgurovsky were checked through their primary publication/institution/preprint records. In particular, the expected-total-cost POMDP result is not substituted for a proof of the present multiplicative objective.

## E3 — Policy structure and quantitatively certified performance

**Action:** Added Section 9 and the fully specified Section 11 example.

**Theorem 9.2 (`thm:two-arcs`)** solves the last-cartridge gate optimization explicitly by first selecting the common censoring decision and then comparing accepted and censored continuation envelopes. Under tagwise accepted rewards, the hit component is a convex envelope of affine functions of cos(y-theta) minus an affine function. Its nonpositive set is an interval, hence a high-acceptance set of at most two circle arcs. The theorem permits an arbitrary compact terminal-decision space, not only finitely many decisions. It does not assert a finite boundary count at every longer horizon.

**Theorem 9.3 (`thm:lookup-rate`)** gives an explicit finite-endpoint lookup error. With J cells per circle, angular Lipschitz constants L_k,L_r, and c=|lambda|B, the loss is at most

    2 N G_+ exp(Nc) (2 L_k + K |lambda| L_r) (2 pi/J).

Its proof controls the accepted integrand and the unnormalized failure measure, so rare or null failures do not introduce a posterior denominator. A finite-cube convexity argument gives endpoint lookup values. Mode-net errors and the exponential menu size are printed separately; this is not called a polynomial-time Bellman solver.

**Theorem 11.1 (`thm:adaptive-advantage`)** establishes strict adaptive value over the entire nonadaptive class. The instance has two counted cartridges, accepted multiplier 99/100, censoring multiplier 1, continuous terminal payoffs 2-t and 1+t, and mode family {1/20} x [0,1/20] x S^1. Its prior is

    (1-1/10000)[(2/5) delta_l + (3/5) delta_u] + (1/10000) Uniform(I).

First, at zero amplitude and the two-point reference prior, the angle is conditionally parameter-independent. All Borel gates reduce exactly to three acceptance fractions; convexity covers the complete nominal nonadaptive class by 64 vertex pairs. The nominal adaptive policy accepts only no-collision reports first, repeats that gate after acceptance, and censors everything after failure. All trials still consume a cartridge. Exact rational interval arithmetic gives:

    nonadaptive value: (1.600432377967011, 1.600432377967012)
    adaptive value:    (1.602586453549804, 1.602586453549805)
    nominal advantage: (0.002154075582792, 0.002154075582793)

Then a uniform complete-policy model-error bound and prior perturbation bound transfer the separation to **all modes and Borel gates** of the nonzero-amplitude cubic family with the full-support prior. The resulting lower-bound expression lies in

    (0.001171773732645, 0.001171773732646),

so the final advantage is strictly greater than **11/10000**. The interval shown here encloses the proved lower-bound expression, not the unknown exact final optimum difference. The comparison includes precommitted randomized commands. It is not a claim that a finite menu sampled in the cubic model exhausts all gates. The current full-rank state theorem applies to this final instance.

## Referee Section 7 — Endpoint gates

The homogeneous-continuation/layer-cake argument is included as Theorem 9.1 with explicit credit to the referee-derived consequence. It is not represented as a new priority claim. The right-continuity argument justifies the fixed one-half threshold of the jointly Borel gate representative, rather than assuming a measurable choice of an almost-everywhere good threshold. The additional two-arc, lookup, and strict-advantage results carry the new control strengthening.

## S1 and referee Section 8 — Model error versus arithmetic error

The smooth perturbation epsilon R^2+delta sin R remains a valid physical detector and still destroys the exact cubic derivative cutoff. Its fourth derivative and exact one-step TV distance are retained. The elementary chronological bound proposed by the referee is proved and sharpened to 1-(1-e0)^N in Theorem 10.1; it yields a value error of payoff-oscillation times that bound and twice that for transferred-policy regret.

This is explicitly different from Section 7's coefficient-relative-error bounds. The constructive smooth-family surrogate theorem then provides finite-state implementation of the perturbed apparatus itself. Neither TV closeness nor value stability is claimed to imply derivative convergence or uniform posterior control at rare histories.

## Preserved results and execution record

Every original principal proof-bearing label is retained. Four complete mathematical source files are byte-identical to v3; the control proof receives only the required dimensional wording changes, and the coefficient-stability mathematics remains unchanged with a historical-execution qualifier. The full foundation tree, all reviewed-source trees, and previous manuscript directories are preserved. The current 35-page principal source is independently compilable.

The newly executed suite contains 24 checks, including a full exact-rational adaptive certificate. All 24 passed. The certificate includes every nonadaptive pair, every adaptive first gate, the selected continuation comparisons, the enclosing constants, and the script digest. The current PDF was compiled, checked for unresolved references and overfull boxes, rendered, and visually inspected as recorded separately. Earlier authors' and referees' execution counts are not reused as current results; the preserved foundation companion was not rebuilt in this execution.

The submission invites a fresh assessment of these proofs and their mathematical significance. It does not equate passing finite diagnostics, page count, or this response's disposition labels with an independent favorable review.
