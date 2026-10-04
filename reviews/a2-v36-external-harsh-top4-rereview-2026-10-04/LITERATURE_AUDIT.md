# Focused literature audit for the external A2 v36 rereview

This note records the information-category comparisons used in the referee report. It is a focused audit, not an exhaustive priority search. No publication, acceptance or equivalence claim is inferred.

## 1. Active smooth-boundary estimation

**R. M. Castro and R. D. Nowak**, *Minimax bounds for active learning*, IEEE Transactions on Information Theory **54** (2008), 2339–2353.

Their boundary-fragment framework is a classical antecedent for adaptive spatial queries, one-dimensional searches and smooth-boundary rates. The queried response is a class label, and the primary risk is classification risk. In A2 v36, a collision bit is not a membership label: a solid start and a free miss both return zero. The local-query reductions are therefore genuine additional work, while bisection, interpolation and metric-entropy counting are not new abstract principles.

**A. Locatelli, A. Carpentier and S. Kpotufe**, *An adaptive strategy for active learning with smooth decision boundary*, Proceedings of Machine Learning Research **83** (2018), 547–571.

This is the closest algorithmic comparison for radial line search and polynomial reconstruction of a smooth boundary. Their theorem adapts to unknown smoothness and noise parameters in a membership-query classification model. A2 v36 assumes the smoothness class and quantitative physical priors, targets laboratory `C^2` geometry, and first derives a usable boundary response from pooled collision commands. The manuscript correctly claims neither a new general bisection method nor unknown-smoothness adaptation.

## 2. Informative rare responses

**S. Yan, K. Chaudhuri and T. Javidi**, *Active learning from imperfect labelers*, Advances in Neural Information Processing Systems **29** (2016).

Their model contains an observed abstention response. Under informative-abstention assumptions, rare informative outcomes can lead to inverse-probability rather than inverse-squared-probability costs. This is an appropriate conceptual antecedent for the statistical gain in the v36 rare query.

The sensor in v36 has no abstention symbol. The paper instead constructs a one-sided event from the collision geometry itself. Shifted pooled commands and a conjunction over at most two outward compass candidates guarantee an exact exterior zero and a positive interior probability. That geometric reduction is specific to the manuscript's sensor. Once it is established, the finite-batch estimate is elementary binomial detection.

The comparison should not be weakened to “the occupation is small.” The two raw means in a reciprocal difference need not be rare even when their difference is small. The v36 improvement depends on the exact exterior-zero event for the commands actually sampled.

## 3. Noisy convex-support estimation

**V.-E. Brunel, J. M. Klusowski and D. Yang**, *Estimation of convex supports from noisy measurements*, Bernoulli **27** (2021), 772–793.

This work studies continuous random vectors from an unknown convex support observed with additive Gaussian or nearly Gaussian noise, and analyzes Hausdorff recovery. It is relevant because it shows that geometric support recovery under nuisance noise need not be framed only as full density deconvolution.

The observation model is nevertheless different. A2 v36 observes attempted collision bits at controlled nominal centers, not noisy continuous positions. Its compact-footprint positivity sets, reciprocal killed-walk inverse, homothetic support separation and periodic recognition are not supplied by that literature. Conversely, the manuscript's polynomial rates should not be compared numerically with Gaussian-support rates as if they belonged to one experiment.

## 4. Classical convex geometry

**R. Schneider**, *Convex Bodies: The Brunn–Minkowski Theory*, second expanded edition, Cambridge University Press, 2014.

Minkowski addition, support-function linearity, Steiner points, mixed area, parallel bodies, erosions and rolling-body facts are classical. The segment-sweep formula used by the direct scale normalization is Cavalieri's principle, equivalently a special mixed-area identity. The area-normalized quadratic is also standard convex algebra once the relevant scalar area is known.

The manuscript's observation-level contribution is to obtain the needed scalars from pooled collision data:

- an isolated integrated forward mean yields a coordinate-width sum;
- a killed-walk adjoint yields an occupation mass equal to obstacle area.

The subsequent two-by-two support inversion and smaller-root selection are not new abstract convex-geometric principles, but their use in this sensor model is mathematically meaningful.

## 5. Query precision and resource accounting

**P. W. Goldberg and S. Kwek**, *The precision of query points as a resource for learning convex polytopes with membership queries*, COLT 2000, 225–235.

This work treats the precision of query coordinates as an explicit computational resource. A2 v36 follows the same accounting principle in a different smooth and noisy setting: it separately bounds attempted observations, nominal-center occurrences and the binary description of centers, setting indices and repetition counts.

That accounting is welcome but remains digital. It does not measure apparatus travel, manufacturing, homothety certification, physical metrology or arithmetic running time. The referee report therefore does not treat the new bit-description theorem as an end-to-end physical complexity result.

## 6. Random-walk and information tools

**G. F. Lawler and V. Limic**, *Random Walk: A Modern Introduction*, Cambridge University Press, 2010, is the natural reference for killed-walk potential theory and stopped martingale mechanisms.

**C. E. Shannon**, *A mathematical theory of communication*, Bell System Technical Journal **27** (1948), remains the foundational information reference.

The manuscript proves the finite identities it needs, including the stopped binary-range bound and killed adjoint. These are clean applications, not claimed new general theorems in probability or information theory.

## 7. Novelty boundary and editorial implication

The focused search did not identify a cited predecessor containing the complete combination of:

- pooled reciprocal collision commands with solid starts and misses charged;
- a geometric conjunction producing an exact exterior zero;
- blind separation of an unknown footprint and an unknown homothety ratio;
- width and killed-area normalizations from collision bits;
- primitive-period recovery in the bounded periodic class.

That synthesis is a genuine contribution. It does not establish priority against uncited work, and it does not turn the component mechanisms into new universal principles.

The remaining top-four objection is therefore not that the paper merely copies one cited theorem. It is that the contribution remains tied to a highly calibrated active sensor, strong prior class and unresolved stationary minimax exponent. The same package can be significant for a specialist journal without meeting the exceptional conceptual threshold of *Annals*, *Acta*, *Inventiones* or *JAMS*.
