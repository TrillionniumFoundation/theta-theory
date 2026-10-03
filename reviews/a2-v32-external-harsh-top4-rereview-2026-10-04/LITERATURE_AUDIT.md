# Literature audit for A2 v32

## Scope

This is a focused comparison for the new v32 adaptive upper bound and binary-information lower bound. It is not an exhaustive priority search. The retained v31 and earlier literature ledgers continue to cover reciprocal hit functionals, random-set capacity functionals, killed random-walk potential theory, billiard inverse problems, period recognition, and the earlier uniform-grid construction.

The present audit asks a narrower question: how close are the new adaptive radial-search and metric-entropy arguments to established active boundary-estimation results?

## 1. Castro and Nowak

R. M. Castro and R. D. Nowak, *Minimax Bounds for Active Learning*, IEEE Transactions on Information Theory 54 (2008), 2339–2353.

Their experiment permits adaptive feature queries and observes a binary class label. The principal losses are classification/excess-risk quantities under boundary-fragment and regression-noise assumptions. The paper establishes upper and lower rates for that model.

The relevant similarity is structural: a smooth boundary is sampled by adaptively chosen binary queries, and boundary dimension rather than ambient grid dimension controls the attainable order.

The differences are material:

- the A2 collision bit is not a membership label;
- solid starts and free misses have the same output;
- reciprocal pooled commands and a killed Bellman calculation are first used to construct an approximate-membership label;
- the A2 target is laboratory `C^2` geometry and primitive periodic recognition, not excess classification risk;
- the A2 upper bound explicitly charges all attempted collision bits and requires scale-dependent physical calibration.

No Castro–Nowak exponent is transplanted into A2. The v32 lower bound is proved independently by a physical support-function packing and a binary-leaf argument.

## 2. Locatelli, Carpentier and Kpotufe

A. Locatelli, A. Carpentier, and S. Kpotufe, *An Adaptive Strategy for Active Learning with Smooth Decision Boundary*, Proceedings of Machine Learning Research 83 (2018), 547–571.

This is the closest algorithmic comparison among the sources audited. Their membership-query procedure uses line searches and smooth interpolation to recover a decision boundary, and it addresses adaptation to unknown regularity and noise parameters.

The v32 radial-search layer has the same broad active-estimation architecture:

1. find a coarse interior/exterior configuration;
2. run one-dimensional searches normal or radial to the boundary;
3. interpolate a smooth boundary from separated samples.

The v32 contribution is not a new general bisection or interpolation principle. Its additional work is the reduction from reciprocal collision bits to an approximate membership query with controlled calibration bias, the handling of solid starts and misses in the denominator, conversion to physical `C^2` convex-body loss, and the subsequent periodic arithmetic.

Unlike Locatelli–Carpentier–Kpotufe, v32 assumes the smoothness exponent is known and does not adapt to unknown smoothness.

## 3. Lawler and Limic

G. F. Lawler and V. Limic, *Random Walk: A Modern Introduction*, Cambridge University Press, 2010.

The killed-compass portion of v32 uses standard random-walk tools: a stopped quadratic martingale, finite mean exit, geometric survival from block iteration, and a killed resolvent/Bellman representation. The manuscript proves the finite bounds it needs and does not claim a new abstract potential-theory theorem.

## 4. Novelty boundary

The focused search did not identify a cited source proving the complete v32 combination:

- reciprocal endpoint cancellation for the collision sensor;
- finite dependency-diamond evaluation of approximate membership;
- adaptive `C^2` reconstruction of periodic convex components;
- exact bounded-denominator period relations under a known patch margin;
- a physical support-function packing with a matching binary-output power.

This combination is a meaningful synthesis. It should not be conflated with novelty of its individual engines, which are classical or closely parallel established active boundary estimation.

## 5. Editorial relevance

The literature comparison strengthens the mathematical positioning of v32 and answers the explicit request in the v31 report. It also sharpens the top-four assessment: after the reciprocal reduction, the rate improvement and lower bound are governed by the familiar one-dimensional smooth-boundary entropy `1/(s-2)`. The technically new content lies in implementing that active-estimation paradigm within the stipulated collision experiment and coupling it to periodic reconstruction.

No acceptance, exhaustive novelty result, or equivalence with passive billiard spectra is inferred from this audit.
