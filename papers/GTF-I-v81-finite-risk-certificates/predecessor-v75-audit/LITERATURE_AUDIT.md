# Theorem-level literature comparison — Revision 75

Primary sources checked on 4 October 2026. This is a targeted author-side comparison. Independent specialist priority review remains pending: no outside reviewer was contacted or commissioned, and neither this file nor an automated check represents external clearance. The preceding comparison is preserved verbatim in `predecessor-v74-audit/LITERATURE_AUDIT.md`; earlier comparisons remain in the inherited audit directories.

## Fiurášek–Mičuda: the two-use adaptive antecedent requested by r48

J. Fiurášek and M. Mičuda, *Optimal two-copy discrimination of quantum measurements*, Physical Review A **80** (2009), 042312. [Preprint](https://arxiv.org/abs/0909.2940), [full text](https://arxiv.org/pdf/0909.2940), [DOI](https://doi.org/10.1103/PhysRevA.80.042312).

Sections I, III and IV study two uses of a pair of projective single-qubit measurements. The admissible strategies decide from the two unknown-device outcomes and exclude additional ancillary measurements. The paper compares fixed product probes, adaptive product probes, entangled probes, and entangled probes with feed-forward. Equation (16) gives the adaptive-product success probability; equations (27)–(30) give the entangled/feed-forward perfect-discrimination construction. This is a direct antecedent for the finite-use adaptive measurement-discrimination interface. Its restricted ancillary interface must be kept explicit when comparing it with the 2021 parallel-optimality theorem below. It does not state the finite-use metric or covering law for noisy or biased binary-qubit families. `FM75` is present in both active bibliographies and the focused comparison discusses its premise directly.

## Sedlák–Ziman: unequal-visibility single-shot reduction

M. Sedlák and M. Ziman, *Optimal single-shot strategies for discrimination of quantum measurements*, Physical Review A **90** (2014), 052312. [Preprint](https://arxiv.org/abs/1408.0934), [full text](https://arxiv.org/pdf/1408.0934), [DOI](https://doi.org/10.1103/PhysRevA.90.052312).

Section VI, Example 4, equation (37), explicitly permits two different white-noise visibilities. The spin-flip symmetry reduces the one-use fixed-failure problem to discriminating two mixed qubit states. Theorem 1 separately characterizes perfect single-use discrimination of arbitrary binary measurements. Thus unequal visibility and the one-use state-discrimination reduction are established antecedents. Example 4 remains unbiased: its effects have trace one. It supplies neither a family-uniform multi-use processor/seizer for varying axes nor the biased-body result. The retained `SZ74` reference identifies the example rather than reducing its scope to equal-visibility circles.

## Puchała–Pawela–Krawiec–Kukulski: single-shot projective distance

Z. Puchała, Ł. Pawela, A. Krawiec and R. Kukulski, *Strategies for optimal single-shot discrimination of quantum measurements*, Physical Review A **98** (2018), 042103. [Preprint](https://arxiv.org/abs/1804.05856), [full text](https://arxiv.org/pdf/1804.05856), [DOI](https://doi.org/10.1103/PhysRevA.98.042103).

Theorem 1, equation (19), identifies the diamond distance between two von Neumann measurements with the minimum unitary-channel distance over diagonal phases. The theorem concerns a single use and projective effects. It is the direct source for that projective distance representation; it does not identify the adaptive distance of arbitrary noisy or biased effects with a chosen unitary-channel distance. `PPKK74` remains separate from the multiple-use citation.

## Puchała–Pawela–Krawiec–Kukulski–Oszmaniec: all-use projective endpoint

Z. Puchała, Ł. Pawela, A. Krawiec, R. Kukulski and M. Oszmaniec, *Multiple-shot and unambiguous discrimination of von Neumann measurements*, Quantum **5** (2021), 425. [Publisher](https://quantum-journal.org/papers/q-2021-04-06-425/), [preprint](https://arxiv.org/abs/1810.05122), [full text](https://arxiv.org/pdf/1810.05122), [DOI](https://doi.org/10.22331/q-2021-04-06-425).

Corollary 1 gives the exact finite-use parallel distance in terms of the phase-optimized spectral arc, with value two at the perfect-discrimination threshold. Theorem 2 proves parallel optimality among general networks using the projective measurement N times. This model allows ancillary systems and a final ancillary measurement, unlike the restricted comparison in the 2009 paper. `PPKKO72` therefore supplies an exact projective endpoint, with no asserted parallel optimality for all noisy or biased POVMs. It provides neither a covering law for the entire binary-qubit effect body nor a supplied-description codec.

## The mathematical distinction introduced by bias

Write a legal ordered binary-qubit effect as

```text
E = ((1+b) I + x·sigma)/2,       |b| + |x| <= 1.
```

The qubit spin flip changes the sign of `x` and fixes the identity coefficient. Hence `Gamma(E) - (I-E) = b I`. The symmetry used in the unbiased single-shot example holds precisely on the section `b=0`. This direct calculation identifies the extra proof obligation in the biased extension.

Equivalently, write `E = p P_u + q (I-P_u)` with `0 <= q <= p <= 1`. Both eigenvalues are now target data. At `p=q`, the axis is unobservable, but the scalar coin remains observable. At `p=1,q=0`, the measurement is projective. Thus adding one scalar coordinate to the old isotropic weight would miss the distinct spectral and angular scales. The metric comparison in `thm:biasedmetric75` must be checked against these degeneracies, rather than inferred from parameter dimension or Fisher information.

The inherited v74 inference chain remains active: radial Bernoulli support cutoff and angular blocks give a cancellation-free metric on the unbiased ball; local operational balls give weighted coverings on regular identifiable subsets; the depth distribution produces the contact trichotomy and the disk logarithm. The corresponding joint rational code charges visibility and direction together. Those results and their hypotheses are preserved.

## Claimed increment and established ingredients

The new comparison in Section 51, `thm:biasedmetric75`, concerns the complete four-dimensional body of ordered binary-qubit effects. Its spectral part uses finite Bernoulli product bounds and a controlled two-row representation for commuting effects. The angular upper bound constructs pairwise dilations with scalar cross overlap. The lower bound combines a product Bernoulli witness with common bias-removing processing followed by finite entangled blocks. These complementary witnesses control both endpoint probabilities uniformly. Eigenvalue extremality and monotonicity provide noncancellation for arbitrary axes. The covering conclusion then uses a direct analysis of the resulting anisotropic operational balls, including the scalar collapse and the projective corner. These are the theorem-level objects for priority comparison.

Section 52, `thm:biasedcover75`, proves covering order `N² log(N+2) delta^(-4)` for every `N>=1` and `0<delta<=delta_0`, with an absolute positive error cap. The lower bound allows arbitrary legal centres. The upper bound is realized by the exact rational spectral/angular construction of `thm:biasedcodec75`; its one-index capacity charges both eigenvalues and the axis. The proof counts a lattice with finite-use cutoff and packs separated projective-corner boxes. Each geometric depth scale contributes order `N² delta^(-4)`, yielding the logarithm. This is a direct covering proof; no nonsingular global coordinate chart is assumed at scalar effects.

Classical programme contraction, binary product testing, adaptive measurement discrimination, separated nets, weighted local volume and exact rational charts have established antecedents. No claim of invention is made for those ingredients. The asserted addition is their proved finite-use metric and covering consequence for the stated body. It is not an exact adaptive optimization formula for every noncommuting pair, a common-estimator theorem, unknown-device learning, a mutable-workspace lower bound, or a physical finite-classical-message simulation theorem.

## Independent review still required

An independent expert should compare the full biased-body metric and its covering consequence, together with the inherited unbiased-ball contact theorem, against quantum measurement discrimination and local channel statistical geometry. Particular attention should be paid to equivalent spectral-coordinate formulations and finite-use boundary regularization. The targeted search did not identify a directly matching all-pair, all-horizon biased-body theorem; that search outcome does not establish absence of prior work. No publication-level priority judgement or general-journal acceptance is inferred from this audit.
