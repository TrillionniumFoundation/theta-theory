# Literature audit — Revision 35

This is a targeted primary-source comparison, not independent exhaustive priority clearance. Sources were inspected on 25 September 2026. Full-text inspection below refers to the specified relevant sections, not a claim to reproduce each entire proof. Search hits unrelated to the mathematical query were excluded.

## Direct additions requested by r19

**Reingold–Steinke–Vadhan, 2013.** Full primary preprint arXiv:1306.3004v2, especially Sections 1.1–1.2 and Theorem 1.4. The model definition and principal theorem pages were rendered. The main article maps its layer conventions to our stochastic rows and separates width from total size. Link: https://arxiv.org/pdf/1306.3004

**Steinke–Vadhan–Wan, 2017.** Final primary article, Theory of Computing 13, article 12, 1–50, especially the abstract, Section 1.1, principal Fourier-growth statement and program model. Model/diagram page rendered. DOI 10.4086/toc.2017.v013a012. Link: https://theoryofcomputing.org/articles/v013a012/v013a012.pdf

**Lee–Pyne–Vadhan, 2022.** Primary LIPIcs version, Definitions 3–5, Theorem 6, and Section 1.2.3 on generalized group products. Theorem 6 page rendered and compared. DOI 10.4230/LIPIcs.APPROX-RANDOM.2022.2. Link: https://drops.dagstuhl.de/storage/00lipics/lipics-vol245-approx-random2022/LIPIcs.APPROX-RANDOM.2022.2/LIPIcs.APPROX-RANDOM.2022.2.pdf

**Berkes–Borda, 2023.** Full primary preprint arXiv:2204.00274, especially the introduction, main convergence statement and Fourier/arithmetic setup. Theorem 1 page rendered. Journal reference: J. London Math. Soc. 108, 409–440. Link: https://arxiv.org/pdf/2204.00274

## Exact comparison performed in the article

The target is an ordered matrix product with two real terminal columns. For a fixed queried column, one terminal stochastic accepting row gives Boolean acceptance probabilities on the same internal alphabet. The complex combination does not require a joint two-answer sample. The Boolean Fourier coefficient is written explicitly as a product of half-sum/half-difference matrices. The conditional past-phase centroid and its nonlinear norm are different objects.

We do not argue that randomness makes all previous methods inapplicable: resolving random tables and applying convexity transfers some general deterministic inequalities. Regularity, however, is a real missing hypothesis for arbitrary stochastic rows; a common reset matrix fails uniform-law preservation. The compared stated Fourier-growth/PRG theorems are not being used as an unproved hidden-width theorem. The new proof establishes a separated-packet contraction directly, with arbitrary starting centroids and endpoint assignments.

Likewise, the harmonic multiplier of an uncompressed biased Bernoulli circle walk is classical. The new packets instead have a uniform active count and correlated internal bits. Only different packets are independent. Their use is licensed by wordwise correctness, not an asserted new mixing rate of the fair walk.

## Positive realization, geometry and comparison of experiments

Heller (1965), Vidyasagar (2011), Benvenuti–Farina (2004), and Monras–Winter (2016) remain inherited background references whose relevant positive-realization/rotation and accessible-space distinctions were documented in v32–v34. No new full-source independent audit of every classical theorem is asserted here. The current paper reproduces the upper construction it needs and independently proves its all-hidden lower theorem. A stationary peripheral-spectrum obstruction does not replace the proof allowing a different transition at every epoch.

Sphere-cap estimates, finite spherical nets, convex decompositions and quantization are classical geometric ingredients. The elementary needed bounds are proved in the article. The compact-group theorem is a statement about conditional compression in a specified orthogonal representation; it is not a claim to have invented orbit quantization or Haar measure.

Blackwell's finite garbling and Torgersen's one-sided comparison framework are inherited classical references, not new results. The manuscript distinguishes an actual terminal-error minimum from an accumulated sum of local deficiency certificates. It gives a lower bound, not a complete dynamic-deficiency classification.

Wegener's 2000 monograph is a standard bibliographic reference for terminology; the operational model comparison is based on the directly inspected branching-program primary papers above rather than a claimed new full reading of that monograph. Prior Norberg/PRFA priority boundaries are not silently marked cleared. The current theorem does not depend on claiming historical primacy for residual-state minimization.

## Repository sources

The r19 report was read through its final assessment at `6016075083626f7c94cfb07912c49fa256fcf9e0`. The exact v34 artifact and native source chain were retrieved. Its Fourier budget, rotation consequences, common-row deficiency, symmetry/autonomy and history audit were checked. The v33 resonant construction is reproduced with attribution. The frozen Round-Seventeen ledger was read through the GitHub connector. None of these internal reviews is independent external peer-review validation.
