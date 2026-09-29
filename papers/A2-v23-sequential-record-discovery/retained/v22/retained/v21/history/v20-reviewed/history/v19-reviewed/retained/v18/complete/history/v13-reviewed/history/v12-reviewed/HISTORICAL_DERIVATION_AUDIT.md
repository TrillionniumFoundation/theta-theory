# Historical derivation audit for A2 v12

## Authenticated source

The latest reviewed author commit is `c8af2cf4201deae5b447b490d44e3cba1aaa8ae0`; its native manuscript tree is `35a9fad03d7f1ee41f2c8661ee3c7aa58047bbad`. The independent review is `bcde40b514e4dc00a3252f2d0710002a2caeac7b`. Its report blob is `75f604f50085fc2e2824f46288892a2ed1a80089`. The review ref was read again before publication and still pointed to that commit.

The matching archived source packet was materialized for local compilation. Every one of the 110 native files was checked against its recorded Git blob and SHA-256, and the complete native tree was reconstructed to the live reviewed tree SHA. The packet was not trusted merely because its filename said v11. All earlier sources remain on the parent branch; the new paper is added in a new directory. The v11 front matter, metadata and changed tooling are also retained under `history/v11-reviewed`.

## Mathematical chain consulted

| Historical source | Content used in the revision | Consequence |
| --- | --- | --- |
| `v3/10_geometry_action.tex` | Localized alternating channel, exact endpoint Hessian, period-two scaling, finite Green matrix, normalized mixed derivative | Supplies unequal-curvature factors and an independent finite-bridge benchmark for the new block |
| `v3/20_integration.tex` | Full-phase flux, physical residual time, common Morse coordinates and exact leading selected probability | Supplies normalized residual-time moments and the physical means used by both observation theorems |
| `v4/10_boundary_layers.tex` | Half-line stationary orbit, action, Green diagonal, edge product and relative determinant; fixed-order geometric convergence | Supplies separate contact-type action and amplitude sums and the finite-window derivative approximation |
| `v5/15_differentiated_operators.tex` | Trace-norm derivative bounds without a growing dimension factor | Preserves the physical derivative control; no stronger bridge smoothness is inferred from the new flux gain |
| `v4/20_nonlinear_information.tex` | Earlier quartic variation and fixed-leading physical family | Retained benchmark; not claimed as the new independent-contact theorem |
| `v5/20_contact_rigidity.tex` | Shared even-contact triangular inverse, graph-jet realization and one-flight comparison | Recovered as the diagonal restriction of the new two-contact block; its antisymmetric direction is separately proved |
| `article/20_boundary_compatibility.tex` | Symmetrized weighted energy pushforward and exact integrated convolution | Defines the general target and yields the two-derivative gain |
| `article/21_abel_stability.tex` | Linear Abel discrepancy, affine nullspace, two-sided inverse, mixed derivative estimate | Remains unchanged and controls the higher-order positive-node regularizer |
| `article/25_profile_acquisition.tex`, `article/26_abel_acquisition.tex` | Compact sum-norm class, positive dictionaries, global interpolation and full preparation accounting | Complete earlier proofs remain active; the stronger approximation uses two more nodes on the same profile class |
| `article/27_profile_calibration.tex` | Translated physical integrated mean and charged smooth-class one-/two-flight pilot | Actual calibration values remain removable with the improved profile-stage rate |
| `article/60_smooth_remainders.tex`, `article/65_envelope_minimax.tex` and count appendices | Distinct finite-dimensional smooth-nuisance experiments | Preserved with their own alternatives, hypotheses and losses; not transferred to the full-profile minimax problem |
| `history/`, `two_collision.tex` and collision-response sections | Earlier derivation record and full auxiliary physical calculations | Retained without a new claim of exhaustive proof certification |

## New work and attribution

The new contact block, its strict antisymmetric coefficient, the two independent support bases, the finite-order physical fibre statement and the fixed finite-window observation theorem are proved in `article/23_two_contact_rigidity.tex` and `article/24_physical_image.tex`. The integrated-flux gain, the improved sufficient rate and the conditional modulus were supplied in Section 5 of the v11 report; `article/28_regularized_observation.tex` credits the report and provides the complete revised observation proof and self-calibration consequence.

The independent finite diagnostics compare the limiting block against finite Dirichlet Green sums and full quadratic-ellipse moments, rather than checking only a re-expression of the claimed limit. They are algebraic benchmarks, not nonlinear billiard simulations or proofs of convergence.

## Scope

This audit concerns the latest A2 report and the historical derivation chain needed for the revision. It is not an exhaustive audit of every theorem in every historical branch, the A1 program, or all eleven proposed papers. The preserved formal statements and proofs are checked byte-for-byte; their retention does not by itself certify their correctness. The source tree, clean builds, tests, and explicit written proofs are distinct forms of evidence.
