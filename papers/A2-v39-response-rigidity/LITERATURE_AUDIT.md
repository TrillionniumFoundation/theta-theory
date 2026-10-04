# Literature audit — A2 v39

This audit positions the current directional-germ inverse relative to primary sources. It concerns the mechanisms used in the manuscript and the information supplied by each experiment. It is not an exhaustive literature search or a priority determination. Classical angular inversion, convex support identities, first variations and regularization are credited separately from the collision-specific identification argument.

## 1. Planar angular inversion

A. K. Louis, M. Riplinger, M. Spiess, and E. Spodarev, *Inversion algorithms for the spherical Radon and cosine transform*, Inverse Problems **27** (2011), 035015. DOI: [10.1088/0266-5611/27/3/035015](https://doi.org/10.1088/0266-5611/27/3/035015).

The [author-hosted full text](https://www.uni-ulm.de/fileadmin/website_uni_ulm/mawi.inst.110/mitarbeiter/spiess/publications/inv-cos-rad.pdf), Section 4, Proposition 1, gives the planar sine-transform inverse \(f=(g+g'')/2\) for a twice differentiable pi-periodic datum; cosine inversion differs by a quarter-turn. The introduction and Section 2 formulate the even angular setting and its relation to directional distributions of line and fiber processes. The [author's institutional bibliography](https://www.uni-ulm.de/en/mawi/institute-of-stochastics/staff/evgeny-spodarev/publications/papers/) confirms the publication metadata.

The angular differential operator is therefore a classical ingredient. The present one-sided kernel has the explicitly proved normalization

\[
\bigl(\partial_\theta^2+1\bigr)(-\cos\theta)_+
=\delta_{\pi/2}+\delta_{-\pi/2}.
\]

It leaves an antipodal sum, not two individually labelled normal contributions. The current inverse uses the nominal-position variable to resolve the translated density copies. Their component supports and normalized masses determine the footprint and full centered density. This spatial identification is proved independently; it is not deduced by claiming cosine-transform injectivity on arbitrary nonsymmetric angular data.

## 2. Directional variation and stationary random sets

B. Galerne, *Computation of the perimeter of measurable sets via their covariogram. Applications to random sets*, Image Analysis and Stereology **30** (2011), 39–51. DOI: [10.5566/ias.v30.p39-51](https://doi.org/10.5566/ias.v30.p39-51).

The [primary journal record](https://www.ias-iss.org/ojs/IAS/article/view/22) states the relations between covariogram directional derivatives, directional variation, and perimeter, including random-set counterparts and expected perimeter density. It provides an antecedent for obtaining geometric boundary information from infinitesimal translated-set probabilities.

The present datum differs: it is a nominal-position-dependent family of forward first-collision means under one unknown stationary launch density. The weighted entering-boundary formula in `lem:single-boundary-flux` is proved by disintegrating the actual free-start strip and then using translation continuity in \(L^1\). The proof retains spatial location and gives a weak finite-length error. The covariogram identities alone do not give joint recovery of this density and the individual obstacles.

## 3. First variation of dilation volume

M. Kiderlen and J. Rataj, *Dilation volumes of sets of finite perimeter*, Advances in Applied Probability **50** (2018), 1095–1118. DOI: [10.1017/apr.2018.52](https://doi.org/10.1017/apr.2018.52).

The [publisher record](https://www.cambridge.org/core/journals/advances-in-applied-probability/article/dilation-volumes-of-sets-of-finite-perimeter/DD02FBCCEDC413C339DFAE5F9A6EFFD2) and [author institutional record](https://pure.au.dk/portal/en/publications/dilation-volumes-of-sets-of-finite-perimeter/) were consulted. The latter links the [open preprint](https://arxiv.org/abs/1708.09191).

The paper studies one-sided first variations of volumes dilated by finite structuring sets. The two-point case connects directional covariogram derivatives with the cosine transform of surface-area measures; the work also treats derivatives of stationary random-set contact distributions. These are established antecedents for the dilation/variation step. The present manuscript proves its spatially weighted collision identity directly and does not invoke those general statements as a black-box theorem for joint density/table identification. This audit verified the primary records and stated scope, rather than relying on an uninspected theorem number from the full article.

## 4. Convex normal coordinates and support cancellation

R. Schneider, *Convex Bodies: The Brunn–Minkowski Theory*, second expanded edition, Encyclopedia of Mathematics and its Applications **151**, Cambridge University Press, 2014.

The [publisher page](https://www.cambridge.org/core/books/convex-bodies-the-brunn-minkowski-theory/400F6173EE613859F144E9598DDD8BDF) and [publisher front matter](https://assets.cambridge.org/97811076/01017/frontmatter/9781107601017_frontmatter.pdf) verify the edition. The manuscript retains its established attribution of support addition, Steiner centering, rolling-body geometry, surface-area measures and Cauchy perimeter to convex geometry.

The new proof explicitly specifies its planar normal convention, boundary parametrization \(c=h n+h'\tau\), and curvature radius \(r=h+h''\). It proves the required separation and normalization rather than hiding them in a reference. The one-resolved-obstacle extension recovers occupation from the odd directional flux and then cancels the known footprint support from each expanded component. Neither support addition nor this cancellation identity is claimed as a new abstract convex-geometric principle.

## 5. Geometry with an unknown probe

J. S. Villarrubia, *Algorithms for scanned probe microscope image simulation, surface reconstruction, and tip estimation*, J. Res. Natl. Inst. Stand. Technol. **102** (1997), 425–454. DOI: [10.6028/jres.102.030](https://doi.org/10.6028/jres.102.030).

The [official NIST record](https://www.nist.gov/publications/algorithms-scanned-probe-microscope-image-simulation-surface-reconstruction-and-tip) and [full primary article](https://pmc.ncbi.nlm.nih.gov/articles/PMC4882144/) were read. The article represents scanned-probe imaging by dilation, uses erosion for reconstruction, and develops blind tip estimation from unknown image features. Its introduction explains the outer-bound character of blind reconstruction and the need to handle noise.

This is a relevant unknown-probe precedent. In the retained homothetic construction, collision deficits and support envelopes identify an unknown common summand. In the new single-law construction, angularly differentiated spatial responses contain density copies with recoverable supports, masses and centers. The proof consequently recovers the probability density as well as its support in the exact experiment. A morphological support constraint alone does not supply this additional conclusion.

## 6. What the single-law theorem proves

The exact data are raw forward means at all nominal centers, all commanded directions, and arbitrarily short positive command lengths. Directions are controlled input labels; the output remains one collision bit. No launch realization, collision position, or collision time is observed. This command family is richer than the retained pooled compass field, and it is not identified with a passive billiard invariant.

The flux exists in \(L^1_{\mathrm{loc}}\), locally uniformly in direction. Angular differentiation in the same function-space setting gives a positive sum of translated copies of the unknown density. With footprint diameter below the inter-obstacle gap and every obstacle width, spatial components separate all copies. Their masses remove curvature weights, and their Steiner points recover the complete obstacle boundaries. Equality is classified exactly by a common translation of obstacles and launch law. The recovered canonical triple determines every finite-length forward response and the full translation period group.

`thm:single-resolved-obstacle` strengthens this exact result. Only one obstacle needs diameter larger than the footprint diameter, while the footprint remains smaller than the inter-obstacle gap. A minimum-area angular support component identifies a pure copy without being supplied that obstacle. After identifying the density, the odd part of the germ gives the distributional gradient of occupation. Bounded continuity and zero infimum fix occupation uniquely; componentwise support cancellation then recovers obstacles whose antipodal copies overlap.

The distinction from classical angular inversion is precise. The angular operator resolves a symmetrized weighted normal measure. The spatial components, their minimum-area selection where necessary, their normalized masses, and the odd-flux occupation identity together establish joint geometric and probabilistic identification for this sensor. The manuscript supplies those arguments explicitly. This comparison makes no priority assertion.

## 7. Finite regularization and the exact-extension boundary

The finite theorem has stronger quantitative hypotheses than the one-resolved-obstacle exact extension. It requires a uniform gap between every angular density copy, bounded \(C^{6,\beta}\) obstacle and footprint geometry, positive curvature bounds, and a lower boundary-mass condition. It requires no density upper bound, smoothness, translation modulus, or density evaluation.

Positive spatial and angular kernels define a nonnegative comparison field. Integration by parts puts the angular derivatives on known kernels, as in approximate inversion. The manuscript then proves its sensor-specific bounds: weak flight bias uniform over the unknown density, finite spatial boundary quadrature, rational displacement rounding, averaged rare-collision variance, Bernstein sampling, and support acquisition. Thus a derivative of an exact response field is not treated as a free finite observation.

The explicit sufficient cost is

\[
N_\nu\le C\nu^{-Q_\gamma}\log\frac{C}{\nu\delta},
\qquad Q_\gamma=\frac{(3\gamma+27/2)s}{s-2},
\qquad s=6+\beta.
\]

This theorem estimates the centered footprint and obstacle geometry in \(C^2\), not an unrestricted \(L^1\) density in a strong norm. It does not claim a necessary or minimax exponent. Uniform finite periodic recovery retains the positive nonperiod-patch margin. The finite nonperiodic corollary uses a protected aperture that contains all expanded components and collars. The exact minimum-area argument is not assigned a uniform finite acquisition bound under its weaker one-body assumption.

## 8. Retained comparisons and statistical benchmark

The article retains its previous comparisons to active boundary estimation, informative rare outcomes, convex-support estimation and query precision in `core/05_comparison.tex`, and retains their references. It also retains the stopped-Poisson and occupation-measure background credited to Lawler–Limic and Altman. The current principal directional proof does not depend on a reciprocal occupation inverse; the latter remains useful under its different pooled observation model.

The matching stationary polynomial power remains a theorem about a fixed known uniform-disk law on the stated bounded smooth physical class, with centered \(C^2\) loss, fixed confidence and worst-case expected attempts. Its lower command class permits adaptive directions and lengths tending to zero; its upper construction uses a fixed pooled compass. One logarithmic factor remains. This result is not a minimax theorem for simultaneous unknown-density and unknown-footprint reconstruction.

The complete article therefore separates exact forward fields, reciprocal differences, raw flux normalizations, finite pointwise occupation, finite geometric recovery, and the known-law minimax comparator. Those distinctions are part of the mathematical statements, not editorial qualifications added after them.
