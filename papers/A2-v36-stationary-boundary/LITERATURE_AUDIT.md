# Focused literature audit — A2 v36

Checked on 4 October 2026 against the primary sources listed below. This is a focused comparison of mathematical mechanisms and observation models, not an exhaustive priority search. The controlling manuscript is the v35 author source at `70c055e1ff090d58ecd61a5644e0fa62a7766f13`; the controlling report is `985d798e172d38c0a9df2a068fe414b2fd13bcbc`.

## 1. Active boundary estimation

**R. M. Castro and R. D. Nowak**, *Minimax bounds for active learning*, IEEE Transactions on Information Theory **54** (2008), 2339–2353, DOI [10.1109/TIT.2008.920189](https://doi.org/10.1109/TIT.2008.920189).

- [Publisher record](https://ieeexplore.ieee.org/document/4494677/)
- [Author-hosted full draft](https://nowak.ece.wisc.edu/IT_minimax.pdf)

Their boundary-fragment model supplies classical antecedents for adaptive one-dimensional searches, polynomial interpolation and metric-entropy lower bounds. The observations are directly queried classification labels, and their principal risk is classification excess risk. A collision bit in the present experiment does not distinguish a solid start from a free miss. The reduction from that physical bit to a boundary test, the laboratory `C^2` loss, and primitive-period recognition require separate arguments. The author-hosted document is a 2007 draft; the bibliography uses the final 2008 publication metadata.

**A. Locatelli, A. Carpentier and S. Kpotufe**, *An adaptive strategy for active learning with smooth decision boundary*, Proceedings of Machine Learning Research **83** (2018), 547–571.

- [Official record](https://proceedings.mlr.press/v83/locatelli18a.html)
- [Full paper](https://proceedings.mlr.press/v83/locatelli18a/locatelli18a.pdf)

This is the closest algorithmic comparison for the active line-search and smooth-interpolation layer. Their construction adapts to unknown boundary smoothness and noise parameters; its boundary supremum-norm rate is given in Theorem 1. The present paper assumes a known bounded smoothness class and proves an observation-level reduction to local boundary tests. It does not claim a new general bisection principle or adaptation to unknown regularity. Their response-probability threshold is `1/2`, whereas the new collision query uses an exterior probability equal to zero.

## 2. Informative rare responses

**S. Yan, K. Chaudhuri and T. Javidi**, *Active learning from imperfect labelers*, Advances in Neural Information Processing Systems **29** (2016).

- [Official record](https://proceedings.neurips.cc/paper_files/paper/2016/hash/dd77279f7d325eec933f05b1672f6a1f-Abstract.html)
- [Full paper](https://proceedings.neurips.cc/paper_files/paper/2016/file/dd77279f7d325eec933f05b1672f6a1f-Paper.pdf)

Their model includes an observed abstention symbol. Under informative-abstention assumptions, their Theorem 3 obtains an inverse-probability query cost, and their discussion distinguishes this gain from estimating a noisy difference whose variance stays positive. This is an appropriate antecedent for the statistical principle used in `core/12_rare_stationary.tex`.

The new geometric step in Proposition `prop:rare-query` is specific to pooled collision observations. Fixed-accuracy normal information selects at most two outward compass candidates. A conjunction of tests at translated centers includes a true support-maximizing candidate even at a compass tie. At an exterior target that candidate has exactly zero collision probability; at positive inner depth every candidate has success probability bounded below by a fixed multiple of the cap mass. Thus the original unobserved compass direction and all-attempt charging are preserved. The subsequent estimate for seeing no success in a fixed batch is an elementary binomial bound.

This distinction is essential: small occupation does not imply small variance for the two raw means in a signed reciprocal difference. The new rate follows from the proved exterior-zero event and inner cap mass for the commands actually sampled.

## 3. Support estimation with additive noise

**V.-E. Brunel, J. M. Klusowski and D. Yang**, *Estimation of convex supports from noisy measurements*, Bernoulli **27** (2021), 772–793, DOI [10.3150/20-BEJ1229](https://doi.org/10.3150/20-BEJ1229).

- [Publisher record](https://projecteuclid.org/journals/bernoulli/volume-27/issue-2/Estimation-of-convex-supports-from-noisy-measurements/10.3150/20-BEJ1229.short)
- [Final author-hosted PDF](https://klusowski.princeton.edu/sites/g/files/toruqf5901/files/documents/brunel2021estimation.pdf)

The bibliography now cites this final publication instead of only `arXiv:1804.09879v1`. Their observations are continuous vectors contaminated by Gaussian or nearly Gaussian noise, and their loss is Hausdorff distance. Their method shows that support recovery need not proceed by first estimating a full density through Fourier deconvolution. It does not supply the present reciprocal collision identity, compact-footprint positivity sets, homothetic matching or unknown-ratio calibration. Its rates and the present polynomial bounds concern different statistical experiments.

## 4. Classical convex geometry and the scale calibration

**R. Schneider**, *Convex Bodies: The Brunn–Minkowski Theory*, second expanded edition, Encyclopedia of Mathematics and its Applications **151**, Cambridge University Press, 2014.

- [Publisher record](https://www.cambridge.org/core/books/convex-bodies-the-brunnminkowski-theory/400F6173EE613859F144E9598DDD8BDF)

Minkowski support addition, homothetic scaling, Steiner points, mixed area, rolling-body arguments and parallel-body estimates are classical inputs. The segment-sweep identity used in Lemma `lem:unk-scale-flux` is Cavalieri's principle, equivalently a special mixed-area identity. The density cancellation in its integrated form uses Tonelli's theorem and normalization of a probability density.

The observation-level contribution in `core/13_unknown_scale.tex` is the isolation and measurement of that integral from pooled collision bits. Its value is an obstacle width sum. Combined with the two recovered positivity supports, this scalar determines the unknown operating ratio. The linear support formulas are not claimed as new abstract convex geometry.

The same section gives an independent normalization by component area. The identity `M_C = |C|` is Fubini's theorem. A finite killed-walk adjoint expresses the area as an integral of weighted reciprocal means; classical mixed-area algebra then selects the unique physical scale root. The two normalizations have different separation requirements and different exact data: the width construction uses a pooled forward mean in addition to the reciprocal differences, while the area construction uses the differences alone.

The identified quantities are the first physical footprint and the ratio of the two settings. A rescaling of an unobserved parameter footprint accompanied by inverse rescaling of both apparatus factors is a representation gauge. The common homothety origin remains a laboratory assumption.

## 5. Query precision and information accounting

**P. W. Goldberg and S. Kwek**, *The precision of query points as a resource for learning convex polytopes with membership queries*, Proceedings of the Thirteenth Annual Conference on Computational Learning Theory, Morgan Kaufmann, 2000, 225–235.

- [Author bibliography](https://www.cs.ox.ac.uk/people/paul.goldberg/publications.html)
- [Original paper](https://www.cs.ox.ac.uk/people/paul.goldberg/papers/colt00procs-GK.pdf)

They explicitly account for query-coordinate precision in exact membership learning of rational convex polytopes. The present theorem follows the general accounting principle in a different smooth, noisy observation model. Its digital bound includes the additional centers needed for the integral measurement as well as the fine boundary queries. A bound on binary descriptions does not itself price physical travel, manufacture or metrology.

**G. F. Lawler and V. Limic**, *Random Walk: A Modern Introduction*, Cambridge Studies in Advanced Mathematics **123**, Cambridge University Press, 2010, remains the random-walk reference.

- [Publisher record](https://www.cambridge.org/core/books/random-walk-a-modern-introduction/7DA2A372B5FE450BB47C5DBD43D460D2)

**C. E. Shannon**, *A mathematical theory of communication*, Bell System Technical Journal **27** (1948), 379–423 and 623–656, remains the foundational information reference.

- [First part](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb01338.x)
- [Second part](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb00917.x)

The killed Green identities, entropy chain rule, decoding bounds and binomial concentration are credited as established principles. The paper includes the specific proofs needed for its finite experiment. Its retained A2 v31 reference remains an unpublished repository manuscript.

## 6. Scope of the comparison

The focused search did not identify a cited predecessor containing the complete pooled-collision conjunction, stationary footprint inverse, unknown-ratio normalization and primitive-period reconstruction. This observation does not establish priority or exclude other related work. The manuscript claims the stated collision constructions and their proved resource bounds, not novelty of their elementary statistical or convex-geometric components.

For a fixed uniform-disk law the new stationary upper and retained lower exponents still differ by `s/(2(s-2))`. Neither exact stationary minimax optimality nor a passive billiard invariant is inferred from these comparisons.
