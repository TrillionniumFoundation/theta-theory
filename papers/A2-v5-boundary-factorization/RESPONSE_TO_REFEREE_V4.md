# Response to the independent referee: A2 v4

**Manuscript:** *Uniform collision thresholds and nonlinear boundary laws in periodic dispersing billiards*  
**Author:** Qian Qi  
**Revision branch:** `revision/a2-v4-nonlinear-boundary-laws-2026-09-09`  
**Controlling report:** `26b05bf0c6483a326d078c99393f4a34434bcc18`, `reviews/a2-geometric-thresholds-v3-harsh-independent-2026-09-09/REFEREE_REPORT.md`  
**Reviewed manuscript:** `3f8ad0a5b718818a22c0e2e47378d4d6c93473a1`, `papers/A2-geometric-thresholds-v3-observability/`.

We thank the referee for distinguishing the correctness of the established uniform threshold and endpoint-observation results from the separate question of their depth and significance. This revision does not treat the report as a request to withdraw those theorems or to reduce the geometric class. It retains the general smooth periodic setting, the complete physical normalization and nonlinear estimates, the exact unlabelled inverse, the record-response results, the circular appendices, and the unchanged two-collision companion. The principal change is mathematical: the uniform finite-bridge analysis now leads to a nonlinear two-boundary limit, with an explicit geometric separation from the entire leading hierarchy.

The new complete article has 44 pages in the recorded native build, followed separately by the unchanged 7-page companion. The page count is a build fact, not an argument for significance. The new results and their proofs are part of the article, rather than promises in this response. The referee's venue recommendation remains a matter for a further independent assessment.

## OBS-R1 — leading-data saturation and a consequence of the nonlinear calculus

### The saturation statement is now explicit

Proposition 8.1 (`prop:v4-saturation`) proves the factorization through one-flight data. At known gap, the one-flight probability amplitude and the two endpoint variances determine the full leading selected-channel hierarchy. In particular,

\[
 A_j=A_1\frac{\sinh\gamma}{\sinh(j\gamma)},\qquad
 v_{j,b}=v_{1,b}\frac{\coth(j\gamma)}{\coth\gamma}
 \quad(j\text{ odd}).
\]

The full endpoint matrix at either parity follows from the already established Hessian formula. Increasing the flight number is not described as producing additional leading inverse coordinates. This observation is integrated into the introduction, the acquisition section, and the comparison section.

### Two semi-infinite boundary layers replace an unspecified large-j remainder

Section 5 (`v4/10_boundary_layers.tex`) constructs half-line stationary segments by a weighted contraction using an explicit half-line Green inverse. Lemma 5.1 defines their convergent boundary actions. The corresponding normalized boundary amplitudes are defined by the convergent edge-product logarithm and a trace-class Fredholm determinant. The latter is specified by its logarithmic series, including normalization and differentiated convergence; it is not an unnamed infinite determinant.

Theorem 5.2 proves exponentially accurate factorization of both the nonlinear action and the **relative** twist:

\[
 W_j-jg=S_0(u)+S_{j\bmod2}(v)+O_{C^k}(\tau^j),\qquad
 \frac{-W_{j,uv}}{-W_{j,uv}(0,0)}
 =B_0(u)B_{j\bmod2}(v)+O_{C^k}(\tau^j).
\]

The proof has two distinct parts. First, it glues the two half-line segments, bounds the interior residual in a summable norm, and uses strict diagonal dominance to estimate the exact nonlinear correction. Second, it truncates the Hessian perturbation to two endpoint blocks in **trace norm**, compares the compressed finite Green inverse with the direct sum of the half-line inverses, and controls the logarithmic determinant under those trace-class perturbations. A remote-boundary or off-diagonal Green term has a strict exponential margin, and fixed derivative orders add only polynomial factors absorbed in that margin. No dimension-dependent determinant bound and no division of an absolute action error by the small reference twist is used.

Theorem 5.3 then proves smooth convergence, including at offset zero, of the normalized actual probability at a **fixed positive offset**. Its limiting conditional law retains both endpoints and the first residual time. The proof uses the common constructive Morse maps and radial cancellation, so it does not differentiate a moving indicator without justification. The two endpoint amplitudes factor, but the limiting probability does not: the common residual-energy constraint couples the ends.

Corollary 5.4 supplies the fixed-positive-offset weights at equal metric thresholds, which were not supplied by the former leading-amplitude selection statement. Corollary 5.5 gives a meromorphic continuation of the actual onset series beyond its first convergence circle and computes the positive pole residue from the nonlinear boundary laws. This series is still a sequence of specified onset windows; it is not substituted for the characteristic function of an unrestricted long record.

### A geometric family not separated by any leading endpoint statistic

Section 6 (`v4/20_nonlinear_information.tex`) makes the new information concrete. The family is

\[
 h_{s,z}(\theta)=1+s\sin^4\theta+z\sin^6\theta
\]

on the lattice `3 Z x 4 Z`, with an analytic area compensation `z=z(s)`. Its horizontal gap is exactly one, its free area is exactly `12-pi`, and **both contact curvatures are exactly one**. Thus not only the entire leading count hierarchy but every leading endpoint covariance matrix is fixed for all flight numbers.

The fourth graph derivative is `q_s=3-24s`. Proposition 6.1 computes the quartic derivative of the nonlinear boundary coefficient directly from the half-line action and determinant:

\[
 \partial_q\mathcal R_\infty(0)
 =-\frac{\cosh(2\gamma)+2}{12a^2\sinh(2\gamma)},\qquad
 a=\sinh\gamma/g.
\]

Theorem 6.2 gives the resulting nonzero physical derivative

\[
 \left.\partial_s\mathcal R_\infty^{(s)}(0)\right|_{s=0}=\sqrt3/2.
\]

It proves local recovery of the family parameter from this nonlinear coefficient. At every sufficiently small fixed positive offset, the nonlinear limiting probability also changes. This is stronger than the retained earlier scalar-product fiber: that fiber was already separated by the leading endpoint metric, whereas this new one is not. The article includes a finite-length quartic formula as an independent normalization check, not as a replacement for the half-line proof.

We do not claim global shape rigidity or that higher jets first entered inverse billiard theory here. The comparison now includes Osterman's analytic marked-length work, alongside the retained length-spectrum and periodic-rare-event antecedents, and identifies the different observations and conclusions. The positive addition is the proved nonlinear physical boundary law and its explicit separation of otherwise identical leading statistical data.

## OBS-R2 — the infinite-sequence topology and a matching positive theorem

### The referee's sequence estimate is incorporated with its strict margin

Theorem 10.2 (`thm:v4-sequence-stability`) works in

\[
 \|D\|_a=\sup_{j\ge1}e^{aj}|D_j|,\qquad 0\le a<\gamma_-.
\]

Along the specified coalescing path it proves the differentiated exponential estimate
`|C_j''(s)| <= B(1+j)^2 exp(-gamma_- j)` and then
`||C(s)-C(0)||_a <= B_a s^2`. The curvature matching distance is comparable to `|s|`. The loss of a Lipschitz inverse is therefore not presented as merely a finite-truncation issue, and exact identification is not conflated with quantitative conditioning. The strict exponential margin is stated; relative error in arbitrarily small amplitudes is not silently substituted for this norm.

### A three-amplitude statistic gives a sharp positive reference-point estimate

Theorem 10.1 (`thm:v4-radial-stability`) adds the matching positive conclusion. From the first three amplitudes define

\[
 m=2C_2/C_1,\quad J=C_3/C_1-f(m),\quad f(x)=x^2/(4-x^2).
\]

With `x_r=sech(gamma_r)` these are a weighted mean and a Jensen gap, with positive weights bounded away from zero. The proof computes the strictly positive second derivative of `f`, obtains two-sided comparison of `J` with the weighted variance of the `x_r`, and deduces

\[
 \max_r|\kappa_r-\kappa_*|
 \asymp |m-x_*|+\sqrt J.
\]

Consequently the distance to the fixed circular reference is bounded by the square root of the first-three-amplitude error, and hence by the square root of the infinite sequence error in the displayed norm. Combined with the explicit coalescing path, this proves that the one-half exponent is sharp **relative to the circular reference**.

That qualifier is essential. The revision does not assert a pairwise one-half-Hoelder inverse for arbitrary noncircular triples near coalescence, nor recovery of an arbitrary triple from three numbers. The full exact Moebius/Prony identification, multiplicities, normalizer formula, and area dependence remain intact in Section 9. The endpoint-record observation is still identified as richer data rather than a regularization of the same unlabelled vector.

## OBS-R3 — accuracy, raw preparation cost, and timing

The original independent-preparation estimator and its exponentially growing raw acquisition cost remain in Proposition 7.2. Section 8 now makes the requested accuracy interpretation explicit: the single-offset procedure has sufficient cost of order

\[
 e^{j\gamma}\epsilon^{-4}\log(C/\eta)
\]

for curvature accuracy `epsilon`. Long collision order is not described as an acquisition advantage.

Theorem 8.2 supplies a further consequence of the all-order uniform remainder. At any **fixed** extrapolation order `m`, measurements at the offsets `h,2h,...,mh` are combined with the exact polynomial weights
`(-1)^(l-1) binom(m,l)`. The bias is `O_m(h^m)`. Pairwise position concentration and the existing compact-image inverse give a quantitative curvature error. A binomial waiting-time estimate gives a high-probability bound on the number of raw preparations, in addition to its expectation. The sufficient accuracy-cost order is

\[
 C_m e^{j\gamma}\epsilon^{-(2+2/m)}\log(C_m/\eta).
\]

For example, order two gives the sufficient exponent three instead of four. Constants depend on the fixed order, and the exponential rarity factor is unchanged. There is no assertion of optimality, uniformity as `m` tends to infinity, independence of successive impacts, or unmodelled measurement noise.

Proposition 8.3 treats the actual programmed window. If its supplied gap has error `Delta g`, the true offset at level `l` is `lh-j Delta g`; normalization by the programmed offset produces a term bounded by `C_m j|Delta g|/h`, in addition to the ordinary gap error in the inverse. Preserving an `O(h^m)` bias requires the sufficient calibration `|Delta g|=O_m(h^(m+1)/j)`. The old `m=1` tolerance is exactly of order `h^2/j`. That calibration is an assumption with a displayed cost in the error estimate, not a free timing correction.

## Preservation, execution, and the boundary of verification

All 123 labels in the reviewed article's active source closure remain in the new closure; 53 labels are added. The original 29 theorem/lemma/proposition/corollary environments have counterparts, with 12 additional results. The original native sources are retained, and changed publication entrypoints are archived. The entire controlling-review repository tree remains the base of this branch. No old manuscript, review, circular appendix, or historical derivation is deleted. The original companion source is unchanged and its seven extracted PDF page texts agree exactly after recompilation.

Four finite diagnostic suites were executed in ordinary and optimized Python, with each pair giving byte-identical JSON: the new suite has 252 checks; the three retained suites have 257, 328, and 411. The new suite separates exact rational/symbolic identities from floating nonlinear gluing, finite quartic coefficients, and actual residual-time quadratures. These are not interval certificates, full-equilibrium simulations, or continuum proofs. The referee's separate 594-check suite was read through its report but is not claimed to have been replayed.

The complete native article and companion were built with real cross-references and recorder-verified input closures; their final logs have no unresolved references, multiply defined labels, or overfull boxes. All 44 main-article page thumbnails and enlarged samples were inspected. The builder and exact input hashes are recorded. The analytical proofs, not check counts or page counts, support the theorems.

A temporary read-only GitHub source-export workflow was attempted before local source recovery; run `34296978029` failed before returning job steps or an artifact. No remote CI success is claimed, and that temporary workflow is removed from the delivered tree. The build and diagnostic executions reported here are actual local executions against content-addressed native sources. The new mathematical conclusions remain available for independent referee scrutiny.
