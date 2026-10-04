# Focused literature audit for the A2 v35 rereview

This note records the information-category comparisons used in the referee report. It is a focused theorem/mechanism audit, not an exhaustive priority search.

## 1. Active smooth-boundary estimation

### Locatelli–Carpentier–Kpotufe

A. Locatelli, A. Carpentier and S. Kpotufe, *An Adaptive Strategy for Active Learning with Smooth Decision Boundary*, PMLR 83 (2018), 547–571.

The paper studies adaptive active learning with a smooth decision boundary. Its algorithmic comparison to A2 v35 is the use of spatially adaptive line searches followed by smooth interpolation. The observation models are different:

- their controller queries a feature point and receives a classification label under the stated active-learning model;
- A2 v35 receives a collision bit that does not reveal whether the start was solid or whether a free flight missed;
- A2 v35 first manufactures an approximate membership query through a reciprocal pooled-mean identity and a killed Bellman inverse;
- A2 v35 targets laboratory `C^2` convex geometry and primitive-period recognition rather than excess classification risk.

Thus the active bisection/interpolation architecture is established background. The collision-level reduction and its calibration/sample accounting are the manuscript-specific contribution.

### Castro–Nowak

R. M. Castro and R. D. Nowak, *Minimax Bounds for Active Learning*, IEEE Transactions on Information Theory 54 (2008), 2339–2353, DOI 10.1109/TIT.2008.920189.

This is the broader minimax active-learning comparison for boundary-fragment classes and binary labels. It supports the referee report's conclusion that adaptively concentrating samples near a smooth boundary and deriving metric-entropy lower bounds are classical statistical mechanisms. Its loss and sensor do not contain the reciprocal collision experiment, unknown launch footprint or periodic reconstruction.

## 2. Noisy convex-support estimation

V.-E. Brunel, J. M. Klusowski and D. Yang, *Estimation of Convex Supports from Noisy Measurements*, Bernoulli 27 (2021), 772–793; arXiv:1804.09879.

This work estimates a convex body from continuous random vectors contaminated by additive Gaussian or nearly Gaussian noise. It analyzes Hausdorff loss, gives an estimator avoiding direct Fourier deconvolution and proves rate bounds in that observation model.

A2 v35 is not an instance of the same statistical experiment:

- it observes Bernoulli collision outcomes rather than noisy locations;
- its compact launch noise is controlled through active nominal centers and reciprocal commands;
- the unknown density is eliminated through the positivity support of a blurred occupation;
- the new two-scale theorem separates obstacle and footprint supports by Minkowski support addition.

The comparison is nevertheless important because it places “recover a convex support in the presence of nuisance noise without estimating the entire nuisance density” in an established inverse-statistical category. No rate equivalence between the Gaussian continuous-output model and the collision-bit model is implied.

## 3. Convex geometry

R. Schneider, *Convex Bodies: The Brunn–Minkowski Theory*, second expanded edition, Cambridge University Press, 2014.

The following ingredients are classical convex geometry and should not be presented as abstract novelties:

- support-function addition under Minkowski sums;
- homothetic support scaling;
- Steiner points and their continuity;
- parallel-body and symmetric-difference estimates;
- inner rolling bodies and erosions in their valid range;
- Brunn–Minkowski concavity of overlap quantities.

The v35 contribution is their use inside the specified reciprocal collision experiment, not the underlying identities themselves.

## 4. Binary information and stopping

C. E. Shannon, *A Mathematical Theory of Communication*, Bell System Technical Journal 27 (1948), 379–423 and 623–656.

The prefix-code/expected-length inequality, conditional mutual-information chain rule and Fano-type decoding bound belong to classical information theory. Version 35 includes a direct proof tailored to adaptive stopping. The manuscript-specific point is the preceding geometric estimate that forces every allowed Bernoulli mean into an interval of length `O(h^s)` under one common stationary noise law.

The one-step inequality

`I(V;Y) <= max_v p_v - min_v p_v`

is an elementary threshold/erasure comparison. Its stopped use is clean and useful, but it is not a new general coding theorem.

## 5. What appears distinctive in v35

The focused audit did not identify a cited theorem that already contains the complete combination of:

1. reciprocal pooled collision-bit forcing;
2. recovery of blurred positivity components by a fixed-aperture killed inverse;
3. blind separation of an unknown convex footprint and obstacles from two exact homothetic scales;
4. primitive periodic reconstruction after support subtraction;
5. a common-stationary-noise expected-attempt lower bound for the same collision sensor.

This combination is mathematically meaningful. The top-four assessment in `REFEREE_REPORT.md` is nevertheless negative because the combination remains strongly calibrated and prior-relative, and because its principal stationary upper and lower exponents do not match.

## 6. Scope limits

No exhaustive search of the active-learning, stochastic-geometry, geometric tomography, deconvolution, sequential-design or billiard-rigidity literatures was performed. This note does not establish priority, equivalence, journal acceptance or the absence of unpublished related work.