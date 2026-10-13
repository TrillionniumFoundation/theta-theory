# Response to the external report on A2-DYN revision 85

**Author:** Qian Qi. **Revision:** 88, 12 October 2026.

**Controlling report:** `reviews/a2-dyn-v85-external-top4-review-2026-10-12/REFEREE_REPORT.md`, commit `af90a4e75bb4262cf16e64ff5e62a688bc21c007`, blob `86ecdfdf87d9ad7f6ecbe20c97f10cc75967eec5`.

**Immediate author baseline:** the already completed v87 revision at `44785327cc0331d994d5d1de371710615cfd6b93`, paper tree `086086bf42a833b241422b0b8a145fa5771a6f2d`. The latest visible external report at task initialization was v85. This revision continues its response on top of v86 and v87; those author revisions are not represented as new external reports or overwritten. All 204 inherited cores and the complete v87 article are preserved.

We thank the referee for requiring complete sources and a pre-limit treatment of collapsing residence. The new proof integrates the **entire negative residence moment at finite collision count**, including the spectrally small remainder. It then uses a whole-segment trace identity to estimate the actual outgoing surface with no positive residence or gradient cutoff. The resulting theorem is in an explicitly finite weak norm. Combined with the original positive remainder, it establishes local-norm convergence for the original unaveraged exact-label density. The pointwise essential-supremum objective, model, original guard, section, normalization and full arithmetic reference remain unchanged.

## 19.1. Fractional optical concentration

The optical trace estimate now integrates the angular-density variation over the whole actual segment before taking the roof norm. If a segment has roofs `(a,b)`, total residence `ell`, and density `A=omega/(4 pi c_* chi)`, Tonelli gives a factor `u-a` in the variation term. Radial growth bounds this factor divided by `z(u)` by `C ell^((1+eta)/2) z(u)^(-eta)`. This pays the first inverse-gradient singularity with the already proved actual fractional volume source, without importing an untruncated first inverse-gradient moment or selecting an initial positive gradient.

Theorem `thm:v88-weighted-trace` records the complete inequality before taking the collision limit. It includes the change of both omega and chi. It does not prove the old fractional essential-height charge zero. Instead, it supplies the surface estimate needed for a new complete raw-density norm theorem. The original stronger pointwise proof obligation is retained explicitly.

## 19.2. Zero residence concentration

Module 205 proves a count-independent physical cap `bar-nu{ell<=s} <= C sqrt(s)`. The proof is on the original collision source: incidence layers have invariant mass O(w^2), section-edge layers have mass O(w), and the true clearance upper envelope has area O(w), by its explicit backward-line coordinates. The geometrically tapered depths sum to a constant; no factor counting physical words is used. Dropping the endpoint tests on this positive upper comparison costs only the original normalization once.

Combine this cap with the retained finite-count exit-localization estimate on the **whole positive probability**, using `x<=A+D` and `x<=V` to infer `x<=A+min(D,V)`. The capped remainder can then be integrated against the negative-residence layer cake. The result is an actual untruncated moment of order upsilon for every `0<upsilon<1/32`, with leading thin-source gain `s^(1/32-upsilon)` and a retained exponentially small finite-count remainder. The whole layer cake is completed before either limit. This is not a list of fixed-positive-cutoff theorems.

Module 206 next estimates all short outgoing traces by this volume moment plus the paid fractional variation. Its interval-pulse lemma is valid for arbitrary overlaps: it sums physical traces before taking the measurable-set supremum. For every `1<q<32/31`, the complete first-exit surface, with **all** positive residences, satisfies a local weak-Lq bound decaying as `r^(1/q-31/32)`. For q=64/63 the power is 1/64. No lower residence cutoff remains in this theorem.

This is a genuine new complete-source norm estimate; it does not set the zero-residence essential-height charge to zero. No finite weak norm is relabeled as essential height.

## 19.3. The scalar pointwise theorem and downstream laws

Theorem `thm:v88-bad-source` proves a complete weak-local-norm bound for the original unaveraged bad density, with the same epsilon^(1/16) gain. Every initial momentum, every total residence and every exact label is retained. The intermediate averages occur only in the proof; the left side is not a smoothed density.

The positive scalar remainder then gives convergence of the actual normalized raw density to the unchanged full arithmetic reference in local weak Lq for `1<q<32/31`, uniformly on all fixed-length roof windows and exact labels. It gives strong local Lp convergence for every `1<=p<32/31` as well. The theorem includes all arithmetic zero classes in its unnormalized form. It does not automatically extend to roof windows growing with the collision count.

The primary pointwise objective is not replaced by this intermediate conclusion. Its original-source criterion remains the v87 criterion in the complete archive, and its charge-zero assertion is not marked proved. A finite local norm does not justify uniform positive denominators or unconditional same-roof ratios. The path, clock and likelihood conclusions retain their scalar-first conditions.

## 19.4. Independent specialist verification

The complete controlling v85 report and complete v87 response were read. The new proofs were checked against the image-clearance envelope in module 105, all-contact exit localization, the common Borel segment map in module 196, the v83 finite exit and surface identities, the actual fractional source and the exact v87 original-source criterion. The source archive preserves all older derivations.

Load-bearing checks for independent specialists are: the invariant area cap for the backward clearance envelope; the normalized cap on the full positive probability; the two residence layer-cake exponents; the weighted whole-segment trace and its radial factor; incident-component multiplicity one; the arbitrary-overlap pulse inequality; and the exact order of width, band and collision limits. The existing Demers–Pene–Zhang paper was consulted as primary background on anisotropic billiard local limits, not treated as proving the repository's four-record or new residence/trace statements.

No independent human specialist audit or formal continuum proof certificate is asserted. Finite diagnostics explicitly include a shrinking-spike example to prevent promotion of finite-norm convergence to essential-height convergence.

## 19.5. Reusable theorem and explicit parameters

Lemma `lem:v88-pulse` is an interval-pulse theorem on an arbitrary measure space and allows all overlaps. The geometric weighted trace in `thm:v88-weighted-trace` isolates the exact hypotheses needed for its physical use: a measurable maximal-segment bijection, the full angular-density variation, radial growth and actual positive volume moments. All parameter dependence and the finite-count cap appear before their limiting corollaries.

The physical negative moment has the strict range upsilon<1/32. Writing q=1/(1-upsilon) explains the strict upper endpoint q<32/31. No endpoint estimate at q=32/31 or at infinity is asserted. The explicit q=64/63, decay r^(1/64), is a convenient admissible example, not an optimality claim.

## Expository comments 20.1–20.10

The active article distinguishes a theorem with no cutoff in a finite norm from the retained positive-cutoff essential-height theorem. The moment exponent is upsilon, distinct from the angular coordinate vartheta; endpoint roofs remain a_j,b_j. The common null-set convention is stated at first use. The complete layer cake and segment sum are formed before the collision limsup, rather than summing infinitely many separate limiting estimates.

The historical critical-band exponents, paired assignments and the two older sufficient charge pairs are retained in the archive. The current pointwise criterion is identified by its precise theorem label. The corrected offset convention and the superseded module-189 notice are preserved. A new dependency guide supplies actual proof-page references in the newly assembled supplement. Build and finite-fixture records remain outside the mathematical argument and are not described as proof certification.

The title, exact-label pointwise target and intended journal benchmark are unchanged. The abstract states both the new complete raw-density local-norm theorem and the remaining pointwise requirement.

## Qualification and publication status

The v88 contract pins the exact v87 paper tree and the controlling v85 report blob, verifies all inherited files and root snapshots, compares normal/optimized diagnostics, builds the article and complete supplement, and checks all 207 core modules in the recorder union. A local archive build is not remote checkout qualification. No v87 successful run or local PDF is represented as a v88 remote run. Actual publication and validation state is recorded in the separate delivery record.
