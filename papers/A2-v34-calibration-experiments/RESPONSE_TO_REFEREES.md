# Response to the v33 referee report

**Paper:** Qian Qi, *Scalar collision laws and recognition of periodic dispersing billiards*  
**Report:** `3d825951afb2c2bd1da258de8648287c046cdc13`, blob `0acfac285985da9babdc8721a87dcef608b4c7d0`  
**Reviewed author source:** `245a2bf5d13b72d81ef85b784e9fcb2dd88ca490`  
**Revision:** A2 v34, 4 October 2026

We thank the referee for distinguishing mathematical correctness, experimental scope and editorial significance. We retain the scalar collision problem and every active v33 result. The response to the calibration objection is not only a qualification: Section 9 proves reconstruction for an unknown stationary density with a fixed calibrated support, without shrinking the random launch spread or observing the realized starts. This complements rather than contradicts the table-dependent bounded-error converse.

## 8.1 — Uncertainty quantifiers

Theorem 8.2 now displays (8.4). For every sufficiently small error radius there exist two physical tables and two admissible measurable implementation maps, fixed for the two worlds, that induce the same complete transcript law for every admissible short-command controller. The maps may differ and use the nominal command and draw. They are not one shared known noise device. The transcript explicitly excludes unobserved actual positions. The pointwise construction already proves this controller-uniform order; the revision makes it visible in the theorem, overview and abstract.

## 8.2 — Boundary convention

Section 1.2 and Lemma 8.1 state the convention: solids and sweeps are closed; a solid-boundary start is zero and a swept-boundary start outside every solid is one. On a disagreement the forced-zero start is moved strictly into its solid or strictly outside all sweeps before evaluation. On agreement the nominal start and the same closed convention are retained. The proof is pointwise, including tangencies; the convention is not justified solely by dismissing a null set.

## 8.3 — Descriptions versus physical precision

The original dyadic theorem and separate resource table remain active without altered bounds. The abstract puts finite digital descriptions next to the separate physical tolerance. The stationary-noise theorem also states nominal dyadic precision and the known numerical representations of K, b0 and gamma. Its random footprint does not narrow, but its nominal command accuracy and probability accuracy are refined. We do not equate a short command word with manufacturing its launch distribution, calibrating the footprint, or a bound on apparatus travel and energy.

## 8.4 — Scope of the calibration converse and a new positive theorem

The old converse is headed “Minimax resolution under table-dependent bounded errors.” It remains valid for its original broad adversarial implementation class. The positive contrast is Theorem 1.4/9.6. All commands use one fresh stationary additive draw with support K, t+diam(K)<d0, and density j(z)>=b0 dist(z,partial K)^gamma. The density is unknown, may be nonsymmetric and need not have mean zero; no upper or derivative bound and no evaluation oracle for j is assumed.

The reciprocal identity still yields g=(T-I)v. Separated positive components and stopped comparison recover v. Its positive components are precisely C+(-K), so known support subtraction recovers C without density deconvolution. Lemma 9.2 proves the quantitative depth bound v>=c e^(gamma+3/2) by rolling-disk overlap, concavity of the square root of intersection area and a small erosion of K. Proposition 9.3 then gives a uniform inverse modulus even when the two compared nuisance densities differ.

For finite acquisition, Lemma 9.4 bounds forcing and update errors by the aperture Green function instead of the number of iterations. The lattice clipped to the fixed aperture has only a prior-bounded number of states per target. A query at depth scale e costs at most C e^(-(2gamma+3)) log(C/epsilon) attempts. Applying the retained radial reconstruction at e proportional to h^s and h proportional to nu^(1/(s-2)) proves the displayed finite sample bound. The footprint support and random spread stay fixed. All solid starts and misses remain charged.

The theorem requires calibrated support, a known boundary-mass lower bound, reciprocal stationarity, exact nominal commands apart from certified rounding, and the existing geometric and period margins. It does not cover an unknown shift of the footprint, arbitrary extra bounded errors, unbounded jitter, observed metrology or long-flight controls. No new minimax claim is made. Thus the paper establishes a positive fixed-spread inverse in a defined common-noise experiment, rather than extending the adversarial lower bound beyond its quantifiers.

## 8.5 — Submission architecture

The journal package is now one self-contained article. All ten v33 proof chapters and all old labels remain active; the new overview and stationary chapter are additional. The complete reviewed v33 tree and every nested historical document remain byte-for-byte in `archive/v33/` and in their pre-existing repository paths. No historical result has been deleted. The journal ZIP contains only the current primary and its active TeX inputs, with no nested Supplement R/S naming obligations. `SUBMISSION_MAP.md` separates the journal reading route from the repository provenance route.

## Conceptual comparison and evidence

Section 10 distinguishes direct active classification, convex-support estimation from noisy continuous vectors, and the present pooled collision sensor. Support addition, Brunn–Minkowski concavity, stopped-walk comparison and coding are credited as classical. The new result is their explicit realization in this sensor with an unknown fixed-spread nuisance density, plus a finite controlled reconstruction and inverse modulus. Neither literature priority nor journal significance is inferred from a sample exponent or diagnostic count.

The v33 exact-source sixteen-document build succeeded; we do not reopen it as a delivery defect. The new v34 validator has its own pins, a one-document manifest, archive-tree integrity checks, normal/optimized new and retained tests, and a read-only exact-triggering-SHA workflow. Its actual local receipt records source-content execution only. It passed 5,886 new diagnostics and 21 new contract tests, reran the stated v33/v32 suites, and built the 28-page primary without final TeX diagnostics. Hosted qualification must be judged from the actual v34 run, not the old successful build. No physical sensor, formal proof assistant or independent journal referee was executed by these checks.
