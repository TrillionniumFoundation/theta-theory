# Response to the controlling v40 report — consolidated revision v42

**Manuscript:** Scalar collision laws and recognition of periodic dispersing billiards.
**Controlling report:** `24baf07cf2952668d61881c727cc6417e952c76e`.
**Reviewed author source:** v40, `c5593b05546889f436ce858c327670d080aae204`.
**Continuation base:** v41, `d81e4053bfba1703c4086ea8f9c69ed32c3537b6`.
**Date:** October 4, 2026.

We thank the referee for recognizing the two-fixed-command joint inverse and
for requesting explicit continuum arguments, quantitative contracts and a
closer literature comparison. Version 41 was already on the remote when this
revision began. We therefore continue that source rather than overwrite it or
repeat its work under a new name. Every active v41 proof body is retained; in
particular all 92 proof bodies of the reviewed v40 manuscript remain present.
The complete primary and supplement are supplied, not just this response.

## 11.1. Closest prior work

The theorem-level comparison `core/28_theorem_comparison.tex` and bibliography
are retained. They compare data, factor assumptions and conclusions, rather
than only keywords. In particular, the joint unknown-noise theorem of Gassiat,
Le Corff and Lehericy requires independence of two noise coordinate blocks;
its entire-transform dependence condition is not a nonvanishing real Fourier
assumption. Our stationary planar launch law need not split into independent
coordinates. The geometrical support literature supplies relevant identifiability
and Wasserstein results, but its passive additive observations are not supplied
as collision observations here.

The new acquisition theorem now constructs the required linear moment data from
actual two-bit collision records, rather than treating additive samples as free.
The collision-specific identity and the additional signed-measure decomposition
remain the source of the geometric separation. Fourier uniqueness, support-measure
calculus, polynomial approximation, concentration, and transportation duality are
identified as classical tools, not claimed as inventions. The scoped primary-source
recheck and version-sensitive theorem numbering are recorded in `V42_AUDIT.md`.
No exhaustive priority certificate is claimed.

## 11.2. Singular-law supports and component matching

The standalone lemmas in `core/24_measure_support.tex` and their application in
`core/21_two_field_rigidity.tex` remain in the primary. Supports are supports of
nonnegative measures `F(x) dx`. Positivity on neighborhoods and Tonelli's theorem
handle arbitrary compact launch probabilities, including atoms and lower-dimensional
supports. The strip boundary can be discarded only as a planar null set before
convolution, with the resulting equality justified almost everywhere. Convex
support gives connected components; the separation margin gives matching.
Almost-everywhere changes do not alter the finite translated occupation class
or its measure support. The physical endpoint identity remains pointwise.

The new `lem:protected-linear-prefix` uses the physical identity even at boundary
atoms. It replaces an unknown occupation-zero endpoint by a certified one: the
first exit from an outer polygon is outside the selected component and within
less than the component gap of it, hence cannot enter another component. Its
coefficients depend only on rational polygon membership, never on hidden starts.

## 11.3. Nonsmooth strict convexity

The primary retains `core/25_nonsmooth_curvature.tex`: the arc-support identity
is proved using the convex and concave section endpoint functions, not a
parametrization requiring a differentiable boundary. The surface-area atom at
a normal equals the length of the exposed segment. Strict convexity therefore
excludes atoms even when there are corners or singular-continuous curvature.
The negative part of the signed measure is exactly the pair of chord atoms.
Neither smoothness nor a positive curvature-radius bound is inserted into the
exact theorem. The later smooth assumptions belong only to the finite theorem.

## 11.4. Exact uniqueness and finite stability

The abstract, roadmap, exact Fourier factorization and finite moment section
continue to distinguish these mechanisms. Exact quotient recovery uses the
dense set where the compact obstacle transform is nonzero and then
continuity; it does not assert stable division through its zeros.

The new `thm:linear-moment-sampling` estimates all unnormalized component moments
through degree n with tolerance tau from a shared sequence of bounded signed
records. The proof exhibits a finite dyadic mesh, two fresh independent hidden
launches per record, a uniform boundary-cell quadrature estimate, and the
simultaneous concentration bound. Positivity is imposed only by the subsequent
rational probability fitting problem, not by clipping signed records.

Consequently `cor:linear-joint-budget` replaces the separated acquisition term
`C m^2 a_m^(-4) log(Cm/(a_m delta))` by
`C a_m^(-2) log(Cm/delta)`. The geometric term `N_geom(c a_m,delta/2)` and the
conditioning of the positive moment factorization remain. Thus the established
exponential sufficient joint bound remains valid. No optimal or parametric
joint rate is inferred from the conditional moment bound. The original all-node
proof is retained as a deterministic alternative.

## 11.5. Primary and technical supplement

The primary includes the exact proof, finite geometry/law/prediction results,
the new linear acquisition section and the expanded technical appendices.
The supplement retains the earlier preparation, directional-germ, calibration
and period arguments. The stable interface in `core/29_supplement_interface.tex`
prints all imported hypotheses and outputs and points to the precise supplement
proofs. No reader is required to reconstruct the Git revision history to use
an auxiliary statement. Qualification checks actual source openings, auxiliary
imports and unique ownership of labeled mathematics between the two documents.

## 11.6. Resources

The new theorem states its own attempted-bit bound with an explicit ceiling,
`2 ceil(8 |W|^2 K^2 tau^(-2) log(2 binom(n+2,2)/delta))`.
Every block has two attempted bits, including zero-coefficient blocks, solid
starts and misses. Available mesh sites are not counted as observations unless
selected. All moments share the same observations. Polygon arithmetic, random
choice generation, moment evaluation/storage, optimization, movement, calibration
and physical coordinate realization are not silently included in the bit bound.
The joint theorem retains the finite output, command and coordinate-description
contracts. Independent coordinate choices for the controller do not alter the
unknown stationary launch law.

## 11.7. Independent specialist review

This request is not represented as completed. No independent human specialist
has been recruited, and no human proof certificate or journal decision is
claimed. The existing specialist brief gives the five requested audit tracks.
For this revision the reviewer should additionally check the protected exit
margin, exact rational stopping, independent two-bit expectation, singular-law
quadrature and the conditional union of the geometry and sampling events.

The finite diagnostic suites and exact-source document workflow assist that
review. Their successful execution, if recorded for the current SHA, certifies
only the stated source and finite checks. It does not certify all continuum
arguments. The revised paper is submitted for another substantive proof review
with its positive results and original research topic intact.
