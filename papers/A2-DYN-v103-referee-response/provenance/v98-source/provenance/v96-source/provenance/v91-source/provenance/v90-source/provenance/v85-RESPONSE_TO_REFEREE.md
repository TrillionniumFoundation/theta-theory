# Response to the external report on A2-DYN revision 84

**Author:** Qian Qi. **Revision:** 85, 12 October 2026.

**Controlling report:** `reviews/a2-dyn-v84-external-top4-review-2026-10-12/REFEREE_REPORT.md`, commit `ef77954a0faa2677028edf971327edca35051ead`, blob `29a2d3e77b637e34b107d8b9638fea51bc104e64`.

**Frozen author baseline:** v84 at `f94ff549308db3fbba2087be0852c3f1e4d0739a`, paper tree `ddae47df392cc5ca659cdef8250f96a0ff33fcab`. This revision starts at the controlling review commit. All 195 inherited cores and the entire preceding article are preserved.

We thank the referee for distinguishing a paired-trace difference from the height of a positive trace, and a uniform positive-cutoff bound from an untruncated endpoint. The new article proves actual essential-height estimates on every positive residence scale, including all critical and nongrazing endpoint types. Consequently the *full* surface, with any previously fixed positive residence cutoff, has height `C r^(1/32)` with a leading constant independent of that cutoff. The critical short part has the sharper `C r^(129/256)(1+|log r|)` height bound in the same ordering. The complete zero-residence tail is kept separately rather than removed by an exchange of limits.

The original title, Lorentz family, actual-return record, pointwise objective, section, guard, source normalization, exact labels, terminal test and all arithmetic classes are unchanged. The organizing pointwise theorem is not replaced by a local-mass or smoothed law.

## 1. Paired short nongrazing height — report 19.1

Theorem `thm:v85-band-height` estimates the complete occupancy trace of every band `s<l<=2s`, where `l` is the actual maximal regular residence. At any roof inside one such segment, the whole segment lies within distance `2s`, and its width-`4s` exit kernel is at least one half throughout that segment. Integrating over the *same physical faces* yields a pointwise persistence inequality. The existing local surface-mass theorem therefore gives essential height `C s^(1/32)` on the entire band, not merely an outgoing-minus-incoming difference.

For any fixed residence cutoff `delta>0`, only finitely many dyadic bands are needed below `2r`. Their leading numerical bounds form a summable geometric series, uniformly in the number of retained bands. Theorem `thm:v85-cutoff-surface` obtains `C r^(1/32)` for the complete surface at that cutoff. The audited transfer inequality then gives the same bound for the full paired incoming assignment at that cutoff. No word count or incoming-face deletion is used.

The qualification is explicit: each positive `delta` is fixed before the collision limit. The full zero-residence tail is not controlled by taking `delta` to zero afterwards in a finite-count assertion. The original untruncated paired-height request is advanced, not marked closed.

## 2. Short critical surface height — report 19.2

The band argument also gives a genuine height estimate for a critical outgoing restriction. On each complete band it proves

`height(B_s^[b]) <= C b^alpha + C_eta s^((1+eta)/2) b^(alpha-eta)`,

as well as the unrestricted `C s^(1/32)` bound. At the natural band threshold `b~sqrt(s)`, this gives `C s^(129/256)` height for every incoming type, including critical and grazing ends. It is a height theorem derived by persistence, not the earlier critical-mass exponent renamed.

For the original critical threshold `b_r~sqrt(r)`, summing the smaller band bounds gives `C r^(129/256)(1+|log r|)` for the whole critical short surface with any fixed positive residence cutoff. The logarithmic finite head and geometric numerical tail are written out. The leading constant is independent of the cutoff. The complete zero-residence tail still remains; no untruncated critical-height flag is promoted.

## 3. Canonical microscopic charge — report 19.3

The fractional charge is retained with the original order of limits. Module 198 additionally defines the actual outgoing occupancy trace of segments with `l<=delta`. Its complete normalized height is taken before `delta` tends to zero. The new theorem proves

`B_M <= F_M^all(r) <= B_M + C r^(1/32)`,

so the limiting full surface height is exactly one zero-residence charge. This is obtained from the newly proved complete positive-scale height estimates, not from fixed-count almost-everywhere convergence.

A further source-level comparison identifies what this boundary concentration measures. Let `q_delta` be the original collision source restricted to actual maximal segments of residence at most `delta` and with nongrazing forward exit. The difference between the outgoing trace and this actual volume-fiber density is bounded by the complete fractional optical potential of width `delta`. Both angular factors and the true first-exit selection are retained. Thus when the fractional charge is zero, the surface charge equals the short-segment collision-source charge.

These are exact comparisons, not proofs that either microscopic charge vanishes. The final pointwise budget contains the fractional charge and the zero-residence charge, or equivalently a sufficient pair of actual volume-source charges after paying the optical comparison. A finite-count uniform-integrability estimate is still required; shrinking an outer width alone does not establish it.

## 4. The no-word-count map — report 19.4 and comment 3

Theorem `thm:v85-segment-map` supplies a named Borel parametrization. It selects the first rational roof in each maximal segment, then disjointizes its transverse representatives in countably many angular charts. This gives a Borel bijection with explicit Borel inverse from `(sheet,angle,interior roof)` to the original regular collision event. All endpoint types and original physical components remain visible.

The theorem states the exact density `omega/(4 pi c_* chi)` and proves its full pushforward identity for every nonnegative Borel selector. It then identifies the nongrazing endpoint map and its flux measure. Two coincident geometric endpoints on different incident components remain distinct; on a single incident component backward-flow uniqueness gives the same maximal segment. Angular-chart seams are only Borel assignments, not physical exits. Fiber identities use a common determining algebra, and the null-set convention is stated before taking parameter suprema. This makes the transfer summation auditable without an informal multiplicity assertion.

## 5. Cutoff uniformity — report 19.5 and comment 4

Proposition `prop:v85-cutoff` reproduces the finite-count layer-cake computation from the exact retained critical-volume inequality. Its leading coefficient is at most

`(1+1/(alpha-1)) b^(alpha-1) = 129 b^(1/128)`,

independent of the positive lower gradient cutoff. Its finite-count remainder is at most `2 C_B (1+B|J|) m^2 c^(-1/2) rho_B^(m/4)`. The contrast is printed in the theorem, not hidden in a preceding paragraph. Splitting above a fixed gradient threshold proves the full positive-cutoff source bound with one leading constant. The audited transfer corollary repeats that constant when it invokes the estimate at `c_r=2 sqrt(Lambda r)`.

This verifies the dependence algebraically from the stated inherited spectral input. It does not claim an independent re-proof of that spectral input or permit `c=0` before the collision limit.

## 6. Independent audits — report 19.6

No independent human specialist audit has been obtained or inferred from software checks. The updated audit map identifies the rational-roof representative construction, the endpoint component convention, the exact angular density, restricted critical mass comparison, the lower-cutoff finite-count remainder and both microscopic charge limits. The cited Demers–Pene–Zhang work remains primary background on billiard local limits; it is not represented as a proof of the repository's four-record or new surface assertions.

## 7. Downstream statements — report 19.7

The scalar-first order is unchanged. The organizing pointwise LLT, pointwise roof-density theorem, unrestricted same-roof bridges and forward likelihood remain unpromoted while the microscopic vanishing statements are unproved. Positive arithmetic reference classes alone are normalized; no zero class is discarded from the unnormalized target.

## 8. Presentation and dependency map — report 18 and comments 1–8

The focused article opens with the two new complete positive-residence-cutoff height theorems. The long-residence symbol is now `R_r`, distinct from the arithmetic reference. The negative dyadic-shift domain is displayed inside the active formula. Critical mass and height are distinguished at each use, and the abstract and final theorem identify the two remaining microscopic requirements.

A compact supplement table maps each indispensable input to its original theorem, exact equation and proof page. Page numbers resolve in the current native build. The original 195 cores, all inherited code, appendices, bibliographies and provenance are unchanged; the full v84 article is included before the older archive. The historical module-189 superseded-notation notice remains present exactly once. Source receipts and finite diagnostics remain outside the journal narrative.

## Exact-source qualification

The new workflow pins the v84 paper tree and the controlling v84 report blob, checks all inherited files and v84 root snapshots, compares ordinary and optimized finite diagnostics, builds both the journal and full supplement, and verifies the recorder union of all 198 cores. Earlier successful runs are baseline evidence only. New run IDs and conclusions must be read at the final v85 author SHA. Finite regressions, source hashes and typesetting are not continuum proof certification.
