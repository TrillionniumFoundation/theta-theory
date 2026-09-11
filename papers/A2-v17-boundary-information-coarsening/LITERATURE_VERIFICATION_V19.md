# Literature verification and novelty audit — A2 v19

## Purpose and method

This audit responds to C18-E4. It is organized by mechanism rather than by keyword alone: nonregular endpoint estimation, parameter-dependent support and limits of experiments, recent optimal testing, multidimensional support-dependent information bounds, support-boundary recovery, and billiard/inverse rigidity. Publisher/author metadata were preferred when available. The purpose is to delimit the manuscript's novelty claim, not to assert that no uncatalogued paper could contain a related calculation.

## 1. Classical one-dimensional nonregular endpoint models

### Akahira (1975a,b)

The two papers on nonregular location estimation are retained as early background for nonstandard rates and bounds on asymptotic distributions. Their bibliographic data are recorded in the manuscript bibliography through the records exposed by later official literature.

### Ibragimov--Has'minskii

*Statistical Estimation: Asymptotic Theory* provides the general asymptotic framework for regular and singular statistical experiments. It is background for local likelihood methods, not a source of the billiard coefficient.

### Richard L. Smith, Biometrika 72 (1985), 67--90

Official Oxford Academic metadata and abstract were rechecked. Smith studies densities which are zero below a parameter-dependent endpoint and behave as a power at the endpoint. He explicitly identifies the linearly vanishing case (`alpha=2`) as asymptotically normal and efficient at a nonstandard rate, including models with additional unknown parameters.

**Consequence for v19.** The manuscript does not claim that a logarithmically modified normal regime for a one-dimensional linearly vanishing endpoint is new.

## 2. Parameter-dependent support and limits of experiments

### Keisuke Hirano and Jack R. Porter, Econometrica 71 (2003), 1307--1338

The Wiley record was rechecked. The paper studies efficient estimation in parametric structural models whose support depends on the parameter, explicitly using Le Cam limits of experiments and local asymptotic minimax efficiency. It shows that the standard MLE can be inefficient and derives efficient procedures in its model class.

**Consequence for v19.** Parameter-dependent support, use of a limit experiment, and local asymptotic minimax reasoning are not claimed as novel mechanisms.

## 3. Recent optimal testing for nonregular parameter-dependent support

### Yuya Shimizu and Taisuke Otsu, *Optimal testing in a class of nonregular models*

The current arXiv record is `arXiv:2403.16413`; the authors' current research pages describe the paper as under revision / revise-and-resubmit at *Econometric Theory*. It develops asymptotically optimal tests from a limit experiment for nonregular models with parameter-dependent support.

**Consequence for v19.** Optimal hypothesis testing in generic nonregular parameter-dependent-support models is not claimed as a new subject of this paper. The v19 testing formula is used to characterize the particular hypersurface/billiard experiment and to compare physical coarsenings.

## 4. Multidimensional support-dependent information bounds

Work on Cramér--Rao--Leibniz bounds, including multidimensional parameter-dependent-support variants (e.g. Lu--Bar-Shalom--Willett--Palmieri and later survey work), relaxes the usual parameter-independent-support regularity condition and derives covariance bounds with boundary terms.

This literature is adjacent but mathematically different from the v19 theorem. The v19 matrix is the coefficient of a *logarithmically divergent Hellinger/LAN boundary layer* for a density which vanishes linearly on a smooth moving hypersurface:

`J_Sigma = integral_Sigma a_0 V V^T / |grad w_0| d sigma`.

The theorem then gives the triangular-array LAN likelihood, the Gaussian-shift local experiment, an efficient score estimator, and the sharp local quadratic minimax value at the `n p delta^2 log(1/delta)` scale. The manuscript does not identify a classical Cramér--Rao inequality with this statement.

## 5. Nonparametric support-boundary recovery

The literature on support estimation / support-boundary recovery (including adaptive low-density estimation and Bayesian support-boundary models) studies an unknown geometric support as an infinite-dimensional object, typically under Hölder or related regularity. Its minimax rates and loss functions are different from the finite-dimensional local moving-hypersurface experiment in v19.

**Consequence for v19.** The paper does not claim a new general minimax theory of nonparametric support recovery. Its function-valued billiard inverse is treated separately by the Abel/profile regularization results; the new LAN theorem is finite-dimensional.

## 6. Billiard and spectral rigidity literature

The manuscript retains the comparisons with De Simoi--Kaloshin--Leguil, Finamore--Leguil and Zelditch. These works recover billiard/domain geometry from marked-length, enriched marked-length or spectral information under their own geometric hypotheses. The v19 data are selected near-onset *physical endpoint records* in a labelled collision channel.

The new signed-endpoint theorem is therefore positioned as a local contact-rigidity result from a different information set. It does not claim recovery of unobserved obstacles, the lattice, or the full global table from one local channel.

## 7. Novelty claim retained after this audit

The active manuscript restricts its novelty claim to the following coupled statements proved in the paper:

1. the uniform nonlinear relative boundary law for the selected dispersing-billiard channel after normalization by the exponentially small physical flux;
2. recovery of the *unsymmetrized* half-line actions from the support of signed endpoint laws, and the resulting all-order labelled contact-jet block with determinant one, removing individual evenness and supplied-curvature assumptions from local contact rigidity;
3. the intrinsic regular-hypersurface logarithmic information coefficient and its vector matrix form `J_Sigma` for a linearly vanishing moving-support density with an independent retained failure atom;
4. the explicit billiard realization of the support velocity, nonsingularity of a finite positive-offset information design on every fixed finite labelled contact-jet family, and transfer of the LAN/minimax experiment to actual long finite bridges;
5. the exact three-level physical observation hierarchy for complete records, endpoint-only records and success indicators in the fixed-table finite-versus-boundary comparison.

The manuscript explicitly does **not** claim priority for parameter-dependent support, nonregular asymptotic normality, the one-dimensional linearly vanishing endpoint rate, generic Le Cam experiment methods, generic optimal testing for nonregular models, or generic support-boundary estimation.

## Verification record

Checked on September 11, 2026 against, among other sources:

- Oxford Academic: Richard L. Smith, *Maximum likelihood estimation in a class of nonregular cases*, Biometrika 72 (1985), 67--90, DOI 10.1093/biomet/72.1.67.
- Wiley Online Library: Keisuke Hirano and Jack R. Porter, *Asymptotic Efficiency in Parametric Structural Models with Parameter-Dependent Support*, Econometrica 71 (2003), 1307--1338, DOI 10.1111/1468-0262.00451.
- arXiv `2403.16413` and current author research pages for Yuya Shimizu and Taisuke Otsu, *Optimal testing in a class of nonregular models*.
- the parameter-dependent-support Cramér--Rao--Leibniz literature and recent survey records, used only to delimit the covariance-bound neighborhood of the claim.
- the inverse-billiard and spectral references already cited in the manuscript.

This audit is revision evidence. The mathematical novelty claim itself is the one stated in the active introduction and must stand or fall with the proofs, not with a search result.
