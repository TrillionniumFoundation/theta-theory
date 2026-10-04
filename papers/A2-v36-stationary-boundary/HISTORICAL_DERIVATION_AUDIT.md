# Historical derivation and source audit — A2 v36

## 1. Controlling review and author source

The controlling report is the complete A2 v35 referee package on

`review/a2-v35-external-harsh-top4-rereview-2026-10-04`

at commit

`985d798e172d38c0a9df2a068fe414b2fd13bcbc`.

Its report, source audit, literature audit and verification record were read. It reviews the author branch

`revision/a2-v35-self-calibrated-stationary-2026-10-04`

and its equivalent referee-copy alias at author commit

`70c055e1ff090d58ecd61a5644e0fa62a7766f13`.

The reviewed repository tree is `052f994e14452cc42a39ab23c8dae33a468c6495`; the manuscript subtree at `papers/A2-v35-self-calibrated-stationary` is `80780f2590aec6d471985835b1b334774b23675f`. These are the controlling mathematical sources. The earlier divergent branch `revision/a2-v35-self-calibrated-footprint-2026-10-04` at `7125ed358a6c3da9fef0cd0011cca0710ad0aab4` is not substituted for them.

The new revision starts from the controlling review head and preserves the reviewed manuscript, report and earlier repository paths.

## 2. Immediate proof dependencies

The active v35 manuscript and its proof and historical ledgers were consulted. The dependencies used in the new arguments are:

| Retained source | Mathematical input used in v36 |
| --- | --- |
| `core/01_local_queries.tex` | All-attempt reciprocal balance, separated positive components, stopped occupation comparison and fixed-aperture reconstruction |
| `core/02_adaptive_boundary.tex` | Coarse acquisition, interior centers, isolated radial brackets, relaxed bisection and smooth radial reconstruction without a derivative loss |
| `core/03_period_recognition.tex` | Protected-patch period tests, bounded-denominator locking and primitive discrete data |
| `core/04_information_bound.tex` and `core/07_sequential_gauge.tex` | Physical bump packing, laboratory gauge and expected-stopping information accounting |
| `core/06_finite_precision.tex` and `core/08_calibration_resolution.tex` | Finite command descriptions, dyadic implementation and the distinction between digital precision and physical calibration |
| `core/09_stationary_jitter.tex` | Unknown stationary density, positivity support, rolling-cap mass, uniform Green error and the earlier signed-mean boundary query |
| `core/10_unknown_footprint.tex` | Strict-nesting correspondence, support separation at two known scales and convexity of reconstructed support functions |
| `core/11_stationary_information.tex` | A common stationary-noise contraction and the expected-attempt lower bound |

The v34 and v32 proof and historical ledgers were also read to distinguish the origins and scopes of the Green estimate and adaptive interpolation. No independent recertification of every older volume is claimed.

## 3. Earlier rate arguments inspected directly

Two historical proof files were read in addition to their ledgers. Their native blob identities at the controlling review commit are:

| Historical proof file | Git blob |
| --- | --- |
| `papers/A2-v11-abel-stable-boundary-profiles/article/26_abel_acquisition.tex` | `ba2f96ff0234b1770a9621c1fe9e58d590c71e26` |
| `papers/A2-v5-statistical-contact-rigidity/v5/50_self_calibration.tex` | `ff812da7bced2c22abde7ea770885d377a5031bb` |

The v11 source retains the integrated flux before normalization. In the notation of that source, `H = c_j p = d^2 F` and the variance of its empirical estimate is at most `c_j M d^2/N`. A Bernstein allocation exploits the small physical success probability. This supplies a useful methodological precedent: stochastic estimation should respect the event actually observed. The v11 labelled finite-flight model is not imported as the stationary pooled observation model.

The v5 source proves negative-binomial concentration and `E T_r = r/p`, and checks that clipped pilot outputs keep subsequent physical windows positive even on failed pilot events. This is useful history for charging every preparation and distinguishing unconditional expected cost from conditional successful-pilot cost. Version 36 uses deterministic batch sizes in its fine boundary test; it does not invoke an unbounded wait at a location whose success probability might be zero.

The v11 profile-calibration source was also consulted for independent pilot stages, conservative numerical bounds and explicit calibration charges. Those principles inform the organization of the new experiment; the older contact/profile inverse theorems are not asserted for the new stationary sensor without proof.

## 4. New derivations

### Pooled rare-collision tests

The new `core/12_rare_stationary.tex` first obtains fixed-accuracy normal information from the retained reciprocal queries. It then selects a finite set containing every support-maximizing compass vertex. At most two translated pooled tests suffice. Their conjunction has a deterministically negative exterior outcome and a cap-mass lower bound at positive inner depth, including normals at which compass maximizers tie.

The collision event identity is new to this revision; the final binomial no-success bound is elementary. This avoids treating a small difference of two potentially nonrare means as a rare observation. With the stated stronger, fixed separation design, the local cost is `e^(-(gamma+3/2))` up to a confidence logarithm. The retained radial reconstruction then gives attempted-bit upper exponent `((gamma+3/2)s+1)/(s-2)`. All directions remain pooled, and every solid start and miss is counted.

### Identification of the unknown operating ratio

The new `core/13_unknown_scale.tex` gives two independent normalizations.

The first isolates one obstacle's complete forward-response support in a domain computed from coarse observations. Integrating its pooled mean removes the unknown density and measures `t/2` times the sum of the obstacle's coordinate widths. Width additivity and the two expanded supports then determine the unknown ratio and the first physical footprint. A finite unbiased continuous-location experiment, followed by a controlled dyadic quadrature, gives a calibration charge of `O(nu^-2 log(C/delta))`, which is below the new boundary exponent on the stated smoothness range.

The second normalization recovers obstacle area from integrated occupation by a finite killed-walk adjoint. Mixed-area algebra gives the unique physical root and its stability. This argument uses only the reciprocal differences and proves exact identifiability under the weaker separation condition stated in that theorem.

These arguments recover the physical first footprint and the ratio, not an arbitrary additional normalization of an unobserved parameter footprint. Exact homothety about the common laboratory origin and the quantitative priors remain assumptions.

## 5. Preservation and presentation

The stationary inverse, rare boundary query, unknown-ratio normalization and common-noise converse form the principal narrative. The localized, finite-control, calibration and period-recognition arguments remain in full appendices of the same manuscript. They are not replaced by references to a mandatory external proof volume.

The source-retention check for this draft keeps all 117 labels and all 33 proof environments of the reviewed active manuscript reachable. These are preservation counts, not a count of independently certified theorems. The original v35, v34, v33 and earlier sources remain at their established repository paths.

The revised literature audit distinguishes the borrowed statistical and convex-geometric principles from their collision realization and updates the Brunel–Klusowski–Yang reference to its final Bernoulli publication. It also records the relevant active-abstention and query-precision antecedents.

This audit concerns mathematical dependencies, historical reuse and source identity. It makes no claim of a new hosted build, journal acceptance, physical apparatus validation or formal proof certification.
