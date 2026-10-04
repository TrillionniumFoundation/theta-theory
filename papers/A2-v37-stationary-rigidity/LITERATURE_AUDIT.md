# Focused literature audit — A2 v37

Checked on 4 October 2026 against the primary sources below. This audit compares mathematical mechanisms and observation models. It does not establish priority.

The controlling report is the v36 rereview on review/a2-v36-external-harsh-top4-rereview-2026-10-04, commit 3c6b195c183df2c52e58e25cf59f7e3fcba07fc3, review tree 525207754a23a6f70f0e7034cc41f13ead111522. It reviews author commit 2559749a038fd2b5ec46d7cc74fdb4bd844b266a, repository tree 46ad6437731b81ffe439c48fe9ede8b2fbc1d194, paper tree 3cc6234334105c6e9be005e19d05df696aa1d923, and core tree 18974801d85e6d5760adb71d9ec15fa7da8ede4f. The previous audit remains at its original v36 path. The present audit retains its applicable comparisons and adds global inversion, blind morphology and random-cap precedents.

## 1. Potential theory and recovery without a supplied aperture

**G. F. Lawler and V. Limic**, *Random Walk: A Modern Introduction*, Cambridge Studies in Advanced Mathematics **123**, Cambridge University Press, 2010.

- [Publisher record](https://www.cambridge.org/core/books/random-walk-a-modern-introduction/7DA2A372B5FE450BB47C5DBD43D460D2)
- [Author-hosted full text](https://www.math.uchicago.edu/~lawler/srwbook.pdf)

Proposition 6.1.1 gives the martingale obtained by subtracting accumulated generator values; Proposition 6.1.2 gives bounded harmonic Liouville; Theorem 6.2.1 gives the stopped Dirichlet representation; Proposition 6.2.3 gives killed-Green inversion of the discrete Poisson equation. Optional sampling is stated in Theorem 12.2.3. These remain classical inputs when their elementary proofs are supplied.

The new core/14_global_response.tex uses the collision identity g=(T-I)v, positivity, bounded expanded components and separation preventing jumps between components. These conditions give a uniform exit-time bound. The positive-obstacle iteration recovers occupation from the forcing without a supplied component or killing aperture. Translation covariance and convex cancellation then identify the full period group of an arbitrary locally finite configuration. The contribution concerns this collision realization and removal of geometric inputs; the stopping and Poisson mechanisms themselves are established.

The exact response field is an active input-output datum. Its constructive finite-field approximation does not, on its own, count the collision attempts needed to estimate the field values.

## 2. Geometric blind-probe reconstruction

**J. S. Villarrubia**, *Algorithms for Scanned Probe Microscope Image Simulation, Surface Reconstruction, and Tip Estimation*, Journal of Research of the National Institute of Standards and Technology **102** (1997), 425–454, DOI [10.6028/jres.102.030](https://doi.org/10.6028/jres.102.030).

- [Official NIST record](https://www.nist.gov/publications/algorithms-scanned-probe-microscope-image-simulation-surface-reconstruction-and-tip)
- [Full text](https://pmc.ncbi.nlm.nih.gov/articles/PMC4882144/)

This is a close geometric antecedent for inference with an unknown physical probe. Scanned-probe imaging is expressed as dilation by a reflected tip. Blind reconstruction combines constraints from separated image features and obtains an outer envelope, or bluntest tip consistent with the image. The paper relates this to the earlier *Morphological Estimation of Tip Geometry for Scanned Probe Microscopy*, Surface Science **321** (1994), 287–300; an [official NIST record](https://www.nist.gov/publications/morphological-estimation-tip-geometry-scanned-probe-microscopy) is available.

The present experiment uses additional data: two labelled physical settings with homothetic footprint supports and raw pooled collision fluxes. Component-independent width deficits identify the scale ratio. Envelopes of Steiner-centered component supports eliminate the common unknown obstacle collection without matching its members. The conclusion is exact geometric reconstruction with independent setting translations under the stated convexity and separation hypotheses. The NIST work is relevant prior blind morphology with a different observation and conclusion.

## 3. Classical convex geometry and unknown homothety

**R. Schneider**, *Convex Bodies: The Brunn–Minkowski Theory*, second expanded edition, Encyclopedia of Mathematics and its Applications **151**, Cambridge University Press, 2014.

- [Publisher record](https://www.cambridge.org/core/books/convex-bodies-the-brunnminkowski-theory/400F6173EE613859F144E9598DDD8BDF)

Minkowski support addition, homothetic scaling, Steiner centering, mixed area, rolling-body arguments and parallel-body estimates are classical. The segment-sweep width identity is Cavalieri's principle, equivalently a special mixed-area formula. Its density-independent integral uses Tonelli's theorem and normalization of a probability density.

The retained core/13_unknown_scale.tex realizes two normalizations from collision observations. Integrated forward flux measures an obstacle width sum. Integrated occupation measures its area; a killed-walk adjoint expresses the latter through reciprocal differences, and mixed-area algebra selects the physical scale root.

The v37 global extension removes the supplied common origin and component correspondences. A pointwise infimum over centered component supports is an envelope, not necessarily a support function. Its common-addend cancellation is elementary once the ratio is identified. The mathematical work recovers the geometric collections and scalar invariants from collision fields and identifies the residual translation freedom.

Direct width calibration uses raw forward means as well as reciprocal differences. The retained area route uses differences alone. Exact homothety and labelled physical settings remain assumptions. Exact identification at distinct scales does not imply uniform conditioning as the scale gap vanishes.

## 4. Active smooth-boundary estimation

**R. M. Castro and R. D. Nowak**, *Minimax bounds for active learning*, IEEE Transactions on Information Theory **54** (2008), 2339–2353, DOI [10.1109/TIT.2008.920189](https://doi.org/10.1109/TIT.2008.920189).

- [Publisher record](https://ieeexplore.ieee.org/document/4494677/)
- [Author-hosted draft](https://nowak.ece.wisc.edu/IT_minimax.pdf)

Their boundary-fragment model supplies antecedents for adaptive searches, interpolation and metric-entropy lower bounds. They directly query classification labels and chiefly study classification excess risk. The present bit does not distinguish a solid start from a free miss. A physical boundary query, centered component C^2 loss, and translation-period reconstruction require separate arguments. The linked draft is dated 2007; the bibliography uses the final 2008 metadata.

**A. Locatelli, A. Carpentier and S. Kpotufe**, *An adaptive strategy for active learning with smooth decision boundary*, Proceedings of Machine Learning Research **83** (2018), 547–571.

- [Official record](https://proceedings.mlr.press/v83/locatelli18a.html)
- [Full paper](https://proceedings.mlr.press/v83/locatelli18a/locatelli18a.pdf)

This is the closest algorithmic comparison for active line search and smooth interpolation. Their Theorem 1 gives a boundary supremum-norm rate with adaptation to unknown regularity and noise parameters. The present finite theorem assumes its bounded smoothness class and proves the collision-level reduction. Their classification threshold is 1/2; the retained rare collision query uses an exterior probability equal to zero. Neither bisection nor interpolation is claimed as a new principle.

## 5. Informative rare responses and weighted cap mass

**S. Yan, K. Chaudhuri and T. Javidi**, *Active learning from imperfect labelers*, Advances in Neural Information Processing Systems **29** (2016).

- [Official record](https://proceedings.neurips.cc/paper_files/paper/2016/hash/dd77279f7d325eec933f05b1672f6a1f-Abstract.html)
- [Full paper](https://proceedings.neurips.cc/paper_files/paper/2016/file/dd77279f7d325eec933f05b1672f6a1f-Paper.pdf)

Their observed abstention symbol can be informative. Under their assumptions, Theorem 3 gives inverse-probability query cost. Their discussion distinguishes this from estimating a noisy difference with nonvanishing variance. This precedes the retained rare-event statistical principle.

In core/12_rare_stationary.tex, fixed-accuracy normal information selects at most two outward compass candidates. The conjunction includes a support maximizer at compass ties. That candidate has exactly zero exterior collision probability, while every selected candidate has a cap-mass lower bound at positive inner depth. The direction stays hidden and all attempts are counted. The no-success estimate is elementary binomial concentration. The exterior statement remains local to a protected bracket and requires 2t+D_*<d_0.

**V.-E. Brunel**, *Uniform behaviors of random polytopes under the Hausdorff metric*, Bernoulli **25** (2019), 1770–1793, DOI [10.3150/18-BEJ1035](https://doi.org/10.3150/18-BEJ1035).

- [Author manuscript](https://arxiv.org/pdf/1503.01504)
- [Author publication list](https://vebrunel.fr/publications/)

Theorem 1 and Corollary 1 convert cap mass of order epsilon^alpha into an iid convex-hull Hausdorff rate of order (log n/n)^(1/alpha). Proposition 3 gives alpha=gamma+(d+1)/2 for a rolling convex support and density bounded below by a boundary-distance power gamma. In the plane this is gamma+3/2. This is a direct predecessor for weighted cap geometry and inverse rare-mass detection. Its observed spatial points and loss differ from hidden-launch actively commanded collision bits; the result does not by itself prove the full collision minimax exponent.

**W. Härdle, B. U. Park and A. B. Tsybakov**, *Estimation of Non-sharp Support Boundaries*, Journal of Multivariate Analysis **55** (1995), 205–218, DOI [10.1006/jmva.1995.1075](https://doi.org/10.1006/jmva.1995.1075).

- [Author-institution publication record](https://researchportal.ip-paris.fr/en/publications/estimation-of-non-sharp-support-boundaries/)

The record describes optimal piecewise-polynomial support-boundary estimation for iid spatial observations when density vanishes at the boundary. Its rate combines smoothness and density decay. This is an earlier non-sharp boundary model, with a different observation and loss.

## 6. Support recovery with additive measurement noise

**V.-E. Brunel, J. M. Klusowski and D. Yang**, *Estimation of convex supports from noisy measurements*, Bernoulli **27** (2021), 772–793, DOI [10.3150/20-BEJ1229](https://doi.org/10.3150/20-BEJ1229).

- [Publisher record](https://projecteuclid.org/journals/bernoulli/volume-27/issue-2/Estimation-of-convex-supports-from-noisy-measurements/10.3150/20-BEJ1229.short)
- [Final author-hosted PDF](https://klusowski.princeton.edu/sites/g/files/toruqf5901/files/documents/brunel2021estimation.pdf)

The final publication replaces the earlier arXiv-only bibliographic form. Their continuous-vector observations have Gaussian or nearly Gaussian noise, and their loss is Hausdorff distance. Their method illustrates that support recovery need not first estimate a full density by Fourier deconvolution. Compact-footprint positivity, reciprocal collision identities and homothetic calibration use different information.

**M. Reiß and J. Schmidt-Hieber**, *Posterior contraction rates for support boundary recovery*, Stochastic Processes and their Applications **130** (2020), 6638–6656.

- [Publisher record](https://www.sciencedirect.com/science/article/pii/S0304414920303057)
- [Author-institution full text](https://ris.utwente.nl/ws/files/250258159/2020_Reiss_Schmidt_Hieber_Posterior_contraction_rates.pdf)

Section 2.1 gives Hellinger affinity exp(-n ||f-g||_1/2) for its Poisson support-boundary experiment and explains its one-sided likelihood geometry. It illustrates the need to use the actual information geometry of a boundary model. It supplies no automatic Hellinger contraction for blurred collision indicators. Any sharper collision converse must establish that contraction for every command in its stated design class.

## 7. Query precision and information accounting

**P. W. Goldberg and S. Kwek**, *The precision of query points as a resource for learning convex polytopes with membership queries*, Proceedings of the Thirteenth Annual Conference on Computational Learning Theory, Morgan Kaufmann, 2000, 225–235.

- [Author bibliography](https://www.cs.ox.ac.uk/people/paul.goldberg/publications.html)
- [Original paper](https://www.cs.ox.ac.uk/people/paul.goldberg/papers/colt00procs-GK.pdf)

They account for coordinate precision in exact membership learning of rational convex polytopes. The present digital account applies that general principle to smooth noisy observations. It includes center occurrences for normalization, boundary queries, settings and repetitions. Binary description length does not measure physical travel, manufacture or metrology.

**C. E. Shannon**, *A mathematical theory of communication*, Bell System Technical Journal **27** (1948), 379–423 and 623–656.

- [First part](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb01338.x)
- [Second part](https://onlinelibrary.wiley.com/doi/10.1002/j.1538-7305.1948.tb00917.x)

Entropy chain rules and decoding inequalities are established principles. The manuscript supplies the stopped-experiment argument in its physical model. The broad-design stationary converse allows direction control and concerns worst-case expected attempts; the retained finite upper theorem uses pooled compass commands and a deterministic confidence bound. The new all-short-command Hellinger estimate closes the polynomial gap without restricting that lower-bound command class. The final minimax comparison uses the same physical class, common disk law, confidence and worst-case expected-cost criterion for both designs. The retained A2 v31 item remains an unpublished repository manuscript.

## 8. Response to the controlling report

Report sections 6.1–6.6 require exact distinctions between raw means and differences, local and global conclusions, center occurrences and sites, separation designs, supplied and learned calibration, and upper/lower experiment classes. These distinctions remain in force.

The section-7 response is the global positive-occupation inverse, equality of response and configuration period groups without a periodicity prior, homothetic reconstruction with unregistered origins and no component correspondence, and the sharp common-disk stationary minimax power. Lemmas lem:effective-collision-boundary and lem:all-short-hellinger supply the collision-specific estimate uniformly over centers, directions and lengths tending to zero. Theorems thm:sharp-stationary-lower and cor:stationary-minimax combine it with the physical packing and stopped information chain. The shrinking-layer controller leaves one logarithmic factor between the upper and lower bounds; no sharp logarithmic or confidence dependence is asserted. Classical ingredients remain credited. This focused search identifies related predecessors; it establishes no priority for the elementary principles or the broad problem of unknown-probe reconstruction.
