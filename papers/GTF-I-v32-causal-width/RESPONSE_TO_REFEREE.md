# Response to the sixteenth pipeline-aware referee report

**General Theta Foundations I — Revision 32**  
**Causal Width Beyond Cutwise Positive Rank**  
25 September 2026

Controlling report: `reviews/general-theta-foundations-i-v31-compatible-memory-pipeline-harsh-top4-r16-2026-09-25/REFEREE_REPORT.md`, frozen at `0e69fdcfc11067a7de9a6122fc603f6a5e2253d8`. Reviewed v31 publication: `90dc2c8f0c75e2cfbb95cc61b247ce4d5e216eb9`; native v31 source: `ca4982c728168e9e25bc86fe85e0fd7fae455192`.

The report accepts the two-cut example but asks for unbounded incompatibility, an arbitrary-horizon obstruction and natural composition. This revision develops all three. It does not present another constant-size counterexample as the main result. It also centralizes the machine conventions and directly compares the rotation mechanism with the classical stationary positive-realization examples.

Stable theorem labels below refer to the native source. The executed build writes the actual numbers and pages in `evidence/THEOREM_LOCATIONS.json`. The retained program title does not assert an editorial outcome or that independent analytic gates follow from these finite-state theorems.

## Main advance: separate minima three, simultaneous width unbounded

`thm:headline` studies a family with four initial seed symbols, two command symbols, two final queries and a binary output. These alphabet sizes do not grow with the horizon. For a fixed planar rotation R, the specified means are `e_j^T R^(sum c_t) x/10`. Every conditional probability stays in the fixed interval `[(1-sqrt(2)/10)/2,(1+sqrt(2)/10)/2]` at every horizon. There are no support zeros or diminishing-signal hypotheses in this example.

`prop:static-three` proves that every internal cut has both ordinary normalized residual rank three and separate positive minimum three. The entire future array from any prefix is a mixture of three legal rotated-triangle continuations. Such a separate factorization embeds in a complete machine when its other registers are unrestricted, so the claim is not only about an amputated matrix.

Nevertheless, for the golden-angle rotation,

```
max(3, log2(N/24000000)/6) <= W_N
                          <= min(3*(N+1),4*ceil(sqrt(N+1))).
```

The lower bound is against all clocked stochastic transducers with the declared inputs, including arbitrary hidden state continuations and arbitrary changes of rows with time. The upper bound realizes each conditional probability exactly. Thus the ratio of minimum simultaneous width to the maximum separate positive minimum tends to infinity. The logarithmic lower and square-root upper bounds are not claimed sharp.

The rational rotation `[[3,-4],[4,3]]/5` gives a second family with all entries rational and the same uniformly positive support. Its simultaneous width also tends to infinity, with effective algebraic excluded-horizon certificates and an exact rational `3*(N+1)`-state upper machine. The explicit logarithmic constant is stated for the golden angle, not silently transferred to the rational angle.

## Sections 4 and 10.5 — a reusable temporal obstruction

**Addressed by `lem:lift`, `thm:volume` and `thm:quantitative`.**

The lower proof must not assume that every hidden state has a well-defined continuation in the observed affine plane. A small positive realization can have unobservable directions. Given its reachable state distributions E_h, we therefore form

```
H_t = aff{E_h},        Q_t = H_t intersect Delta_(K_t),
P_t = pi_t(Q_t),
```

where pi_t reads terminal means after the remaining commands are idle. The common stochastic update maps Q_t into Q_(t+1), and the observable intertwining identity holds on H_t by affine extension from actual prefixes. It follows that `P_t union R P_t subset P_(t+1)`.

A section of the K_t-label simplex can have more than K_t vertices. We explicitly retain the safe `2^K_t` vertex bound rather than assuming an unlifted realization. This point is tested by a small affine-prefix counterexample and is central to the all-hidden-state quantifier.

For a full-dimensional seed hull S, bounded observation domain D and determinant-one command maps, define delta_M by minimizing the volume increase `vol(conv(union L P))-vol(P)` over all polytopes between S and D with at most M vertices. It is a geometric quantity without a selected witness list or a proposed machine. Compactness and absence of an invariant polygon make it positive. Every realization satisfies

```
sum_(t<N) delta_(2^K_t) <= vol(D)-vol(S).
```

For the golden angle, an elementary Fibonacci orbit covering, a polygon support deficit and a triangular area estimate prove

```
delta_M >= 1/(6000000*M^6),
sum_(t<N) 2^(-6*K_t) <= 24000000.
```

This is an arbitrary-horizon multi-cut budget, not another two-cut feasibility reformulation. It is unchanged in normalized form under invertible affine recodings. In particular it bounds how many epochs may have small width, even when other epochs have arbitrarily larger registers.

The rational case supplies a finite real-algebraic procedure for delta_M: list at most M vertices, partition by hull order and determinant signs, write polygon areas, and apply quantifier elimination. The input representation is specified, and no efficient algorithm in a succinct horizon is claimed. The procedure is proved, not reported as numerically executed for enormous M.

## Sections 4 and 10.5 — exact closure and a growing Pareto frontier

**Addressed independently by `thm:tagged-sum` and `cor:pareto-sum`.**

When a branch tag is supplied initially, never repeated as a free future input, and must be recovered exactly at the end, the complete feasible-profile set is the Minkowski sum of the component profile sets. A state shared by two branches would have to output two different tags with probability one on the same suffix. Thus their reachable state sets are disjoint at every cut, and all common rows restrict to genuine component realizations. This proves both directions for arbitrary horizons and arbitrary stochastic encoders.

For m copies of the v31 primitive, the result is the exact region

```
K1 >= 3*m,       K2 >= 3*m,       K1+K2 >= 7*m.
```

The minimum peak is `ceil(7*m/2)`, while either cut alone needs `3*m`. The full primitive proof is included in Appendix A and explicitly credited to v31. The tag has structural zeros, so this family is not advertised as full support. The rotation family separately provides the stronger fixed-alphabet, uniformly full-support unbounded ratio. Nonnegative scalar direct-sum additivity is classical; the new statement used here is addition of the complete compatible profile regions.

## Sections 5 and 10.2 — theorem-level literature comparison

**The closest rotation and quotient precedents are read directly and made explicit.**

The revised main text cites Benvenuti–Farina, Theorems 2–3 and Example 4, and Monras–Winter, Theorem 6, Example 2/Lemma 7 and Section 4/Theorem 9. Irrational rotation preventing a finite stationary positive realization is classical. The accessible-space/observable-quotient construction is also classical. Neither is claimed as a discovery of this revision.

The finite comparison is different: every finite horizon here has a positive realization; the lower bound permits a new machine for every horizon, with unrelated stochastic rows at different epochs; every separate positive rank is three. The expanding-section budget is what rules out a uniformly bounded *clocked* width. A peripheral-spectrum argument for one repeated positive matrix is not substituted for this proof.

We also inspected the relevant portions of the August 2026 paper of Lumbreras–Ma–Thompson–Gu, including Section IV.2 and its same-update mechanism. Its infinite-horizon decision-error and quantum-simulation conclusions are distinguished from our finite exact classical width claims. It is cited rather than omitted because of its recent date.

Gillis–Glineur's restricted/nonrestricted distinction is used to explain why a section-and-projection argument is needed. Denis–Esposito's residual generation does not restrict our competing states. Qi–Comon–Lim's nonnegative tensor direct-sum result is acknowledged in the profile composition section. Basu–Pollack–Roy supplies the real algebraic decision procedure. The literature record distinguishes full texts inspected from publisher-only or inherited background citations; an exhaustive independent priority certification is not claimed.

The weighted replacement step in v31 is explicitly identified with weighted reservoir sampling, with the direct algorithm in Pharr–Jakob–Humphreys, Appendix A.2, as a primary reference. It is not a new sampling claim or part of the present novelty summary. The old additive implementation and critical-simplex results are preserved, not deleted.

## Sections 7, 10.3 and 11 — the exact machine conventions

**Centralized in `def:machine` and Section 2.**

The paper fixes the finite horizon, full external input alphabet, initialization E, stochastic command rows T, decoder D, and product formula. The seed and query are atomic inputs, the commands are externally supplied, and equality is required for every complete word. Only the updated register persists; no past seed, random tape, input transcript or schedule record is free. The external time index and known row table are free in this positive-realization model. Available labels are counted, so padding has a precise meaning. Zero-probability and unreachable rows are legal normalized rows.

All lower bounds permit phase-dependent rows. The polygon upper construction actually has the same command matrices at each training epoch, since successive radii have constant ratio; its final decoder depends on N. This is not a single unchanged machine for all horizons and not autonomous input-length recognition. Rational fair-bit implementation has a separate workspace ledger inherited from v31. No finite-denominator implementation is asserted for the computable-real golden-angle rows.

The v31 dummy-label clarification is stated explicitly: when preceding mixture weight is zero, choose the dummy in the existing label alphabet. The retained published v31 PDF is not silently edited; this clarification appears in the new article and response.

## Sections 8, 10.1, 10.4 and 10.6 — focus, preservation and pipeline

The main paper retains one principal theorem spine: the complete transducer model, reachable-section geometry, the cumulative volume obstruction, explicit realization, and the fixed-rank unbounded family. A short independent profile-composition section gives the exact frontier; its inherited primitive is proved in an appendix. A contribution table labels inherited and classical ingredients. No leading entropy exponent or known critical simplex is counted as new mathematics.

The work descends additively from r16. The entire v31 article remains byte-identical as `supporting-results.pdf`; its cumulative mathematical and development volumes are appended unchanged in the new archival volumes. The small `REFEREE_PACKAGE.zip` excludes those large archives and contains the focused article, response, and core reproducibility sources. Preservation is not used as evidence of depth.

We re-read the frozen Round-Seventeen dependency ledger and the v31 source arguments that enter this revision. The A2/A3/A4/C2/D1 and hard-sphere chains retain their Fourier/LLT, stopped-LDP, common-domain, nonlinear semigroup and optional-projection gates. The present theorem is not represented as an independent analytic gate solved in those manuscripts. Fully adaptive collision validation, a complete arbitrary-positive-realization classification and sharp second-order query streaming remain separate objectives. The requested research progress is the explicit unbounded causal incompatibility and its geometric multi-cut law, not a fabricated pipeline edge.

## Status for the next review

The article contains full analytic proofs of the all-hidden-state lift, volume budget, explicit logarithmic bound, exact square-root construction, rational effective variant and tagged profile identity. Finite tests verify identities and representative implementations; they do not prove the uniform optimization claims, settle priority, or determine a journal decision. The principal remaining quantitative question is the gap between the logarithmic lower and square-root upper widths. The latest report's demand for an unbounded gap and an arbitrary-horizon obstruction is answered without asserting that every proposed direction has been closed.
