# A2 v4 — hypotheses, proof dependencies, and preservation

The controlling review is `26b05bf0c6483a326d078c99393f4a34434bcc18`; the reviewed manuscript is `3f8ad0a5b718818a22c0e2e47378d4d6c93473a1`. The native revision is `papers/A2-v4-nonlinear-boundary-laws/` on `revision/a2-v4-nonlinear-boundary-laws-2026-09-09`.

## Unchanged geometric and physical foundation

The positive-curvature periodic configuration is arbitrary within the local compact-family formulation. Neither finite horizon, congruent obstacles, central symmetry, nor proximity to a circle is introduced as a new premise of the general theorems. The finite channel selection, separation and clearance, specular reversal, and full-event localization are proved in the retained geometry section. The exact first-residual-time measure is `-W_uv du dv dr/(2 pi A)`. This is the full equilibrium preparation, not an imposed endpoint ensemble.

The retained Dirichlet lemma has a common contact box, weighted coordinate decay, uniform endpoint Hessian, and **relative** twist error. The trace-class perturbation and logarithmic determinant are essential. They control an exponentially small twist without pretending that a uniform absolute error is relative. The retained smooth radial lemma cancels odd terms even for nonsymmetric graphs. It proves uniform right-smooth offset remainders for probabilities and physical variances.

## Lemma 5.1 and Theorem 5.2: the half-line objects and their coupling

`v4/10_boundary_layers.tex` gives the half-line Green kernel explicitly. Its weighted convolution bound gives a uniformly contracting nonlinear half-line equation. Uniqueness among small bounded stationary segments follows from strict diagonal dominance, not just from an ansatz in the weighted space. Summability defines the boundary action; its quadratic derivative is computed by first variation.

The half-line Hessian perturbation is trace class because it is tridiagonal with summable endpoint weights. The boundary amplitude is the exponential edge-product sum divided by the Fredholm determinant defined through its absolutely convergent logarithmic series. Its normalization is one at zero. Every fixed derivative retains at least one trace-class factor.

For finite-to-infinite comparison, glue the left and reversed right half-lines, correct endpoint values, and bound the stationarity residual in `ell^1`. A symmetric uniformly diagonally dominant averaged Hessian gives a uniform `ell^1` inverse. Differentiation controls the full correction. For the determinant, retain two blocks of length `floor(j/3)`, bound discarded perturbation entries in trace norm, and compare the compressed finite Green matrix with the two half-line compressions. The remote reflection and block interaction are exponentially small. The logarithmic determinant is locally Lipschitz in trace norm with all fixed differentiated versions. Polynomial index factors are absorbed in a strict exponential margin. This proves the normalized-twist factorization independently of an absolute action convergence estimate.

## Theorem 5.3 and Corollaries 5.4–5.5: physical nonlinear limits

The reference determinant has parity-dependent value `sqrt(a_0 a_p)`, independent of length at fixed parity. Common Morse coordinates depend locally Lipschitz-continuously on uniformly positive actions. Their difference vanishes at zero. Applying radial cancellation on the fixed disk controls the normalized probability and every fixed right offset derivative, including zero. The limiting law has product boundary amplitude but a shared energy constraint; no independence of the ends is asserted.

The conditional-law comparison uses common latent coordinates, `L^1` density comparison, and scaled endpoint-map coupling. Its metric is bounded-Lipschitz, not total variation of singularly embedded full records. A fixed number of end collisions may be included. The tied-channel weights use a finite positive sum. The meromorphic onset series uses coefficient errors with a strict exponential margin; it is not an unrestricted pressure or characteristic function. Positive and possible negative pole residues are derived from the even/odd boundary coefficients.

## Proposition 6.1 and Theorem 6.2: information not present in any leading endpoint metric

`v4/20_nonlinear_information.tex` treats identical even contact graphs for the explicit coefficient calculation, not for the general half-line theorem. Stationarity makes the quartic action coefficient equal to its broken-action quartic term on the linear bridge. Its graph-fourth-jet derivative is `coth(2 gamma)`. In the relative determinant the quartic jet changes only the diagonal quadratic Hessian term; the mixed edge twist has no corresponding quadratic contribution. The half-line diagonal Green sum gives the amplitude derivative. Residual-time integration combines the two terms, yielding the displayed quartic sensitivity.

The actual analytic support family is `1+s sin^4(theta)+z(s) sin^6(theta)` on the rectangular lattice. Area compensation has nonzero derivative `5 pi/8`. The gap, support points, and second contact jets remain fixed exactly, while the graph fourth derivative is `3-24s`. Curvature positivity, separation from other lattice translates, and clearance persist on a small open parameter interval. At the disk the nonlinear coefficient derivative is `sqrt(3)/2`. The local inverse is one-dimensional and has nonzero derivative; no arbitrary-boundary rigidity is inferred. Every leading count coefficient and endpoint covariance matrix really is fixed along this family.

## Proposition 8.1 and Theorem 8.2: saturation and bias reduction

The one-flight leading inverse determines all leading higher-order selected-channel quantities. This is stated before any acquisition claim. The new acquisition theorem uses fixed-order polynomial extrapolation, not a claim of new leading information at large length. The variance remainder is right-smooth with uniform derivatives, so the exact binomial weights give `O_m(h^m)` bias. Paired independent successful preparations yield bounded unbiased summands. A union concentration bound and compact-image projection give the curvature error even when the extrapolated vector is outside the observation image.

For raw cost, the actual success probability is comparable to `(lh)^2 exp(-j gamma)`. Negative-binomial expectations and a binomial lower-tail estimate give expected and high-probability costs. Constants depend on fixed extrapolation order, and no minimax claim is made. Proposition 8.3 propagates actual-window error through both offset normalization and the supplied-gap inverse. Its sufficient timing calibration is explicit; gap estimation itself is not charged as a free operation.

## Theorems 10.1–10.2: positive circular-reference stability

The first three amplitudes produce a weighted mean of `sech(gamma_r)` and a Jensen gap for `x^2/(4-x^2)`. Positive curvature boxes bound all weights below, and strict convexity compares the gap to the variance. This gives a two-sided observable measure of distance to the fixed circular configuration and a positive one-half-Hoelder estimate. It is a reference-point theorem, not a pairwise inverse at all nearby triples.

On the explicit coalescing path, the first derivative of each amplitude is zero. Differentiating its hyperbolic expression yields `C(1+j)^2 exp(-j gamma_-)`; the strict norm margin `a<gamma_-` makes the bound uniform over the entire sequence. The path proves optimality of the circular-reference exponent, while the positive three-amplitude theorem proves its attainability. The exact retained Moebius/Prony identification and area dependence are not weakened.

## Historical derivations and architecture

The complete reviewed v3 native foundation, v2 geometric proof files, original circular sections, fixed-window companion, and original response/ledger files remain available in the repository. The Round 33 arithmetic/Fourier chapter was read at blob `2213344f8efa895b4674f818d404c5d4a9af9da1`. Its algebraic separation estimate and conditional Fourier compiler remain distinct from the present onset series. No unrestricted billiard frequency envelope is inferred from the half-line construction.

The main article integrates the new results before the retained observation, inverse, response and comparison material. All 123 previously active labels remain; the new active closure has 176. The environment counts change from 8 theorems, 10 lemmas, 7 propositions and 4 corollaries to 14, 11, 10 and 6. The original companion source and extracted page texts are unchanged. The source closure and per-file hashes are recorded in `verification-v4/PRESERVATION.json` and `verification-v4/NATIVE_BUILD.json`.

## Verification boundary

The 44+7-page native build has resolved references, stable auxiliary files, a recorder-matched real input closure, and no overfull boxes. Four finite suites, each executed normally and with `-O`, pass with pairwise identical JSON: 252 new checks and 257/328/411 retained checks. Exact finite algebra is separated from floating quadrature and finite nonlinear gluing. A finite half-line cutoff and a finite amplitude prefix are labelled as such. They do not certify an infinite operator, a continuum family, or an equilibrium trajectory simulation. All main-page thumbnails and selected enlarged pages were visually inspected; full-size inspection of all pages is not claimed. No remote CI pass, formal proof-assistant verification, exhaustive priority survey, or journal acceptance is claimed.
