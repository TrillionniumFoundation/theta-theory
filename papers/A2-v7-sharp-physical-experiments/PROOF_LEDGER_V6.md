# A2 v6 proof and dependency ledger

Source labels are controlling; numbering and pages refer to the delivered 63-page build.

| Claim | Location | Inputs and proof mechanism | Quantifiers and observation |
|---|---|---|---|
| General threshold law | Theorem 1.1; `v3/10_geometry_action.tex`, `v3/20_integration.tex` | Ground-channel localization, weighted Dirichlet bridge, cofactor formula, physical residual-time integration | Smooth periodic dispersing compact families; no symmetry or finite horizon; uniform in collision order |
| Relative two-boundary law | Theorems 5.2-5.3; `v4/10_boundary_layers.tex`, `v5/15_differentiated_operators.tex` | Half-line contraction, summable gluing error, localized trace-class determinant comparison, common Morse integration | Fixed derivative order; normalized twist rather than absolute small flux; both endpoint parities |
| Total-variation transfer | Theorem 6.1, Corollary 6.2; `v6/10_experiment_transfer.tex` | Zero value/gradient of action error gives quadratic vanishing; fibrewise moving-domain bound; amplitude normalization; product telescoping | Endpoints and first residual time; fixed physical design explanation; raw error retains rare-event mass; no TV assertion for full growing array |
| Limiting contact inverse | Theorem 8.1 and Corollary 8.2; `v5/20_contact_rigidity.tex` | Finite-degree action and determinant variations; triangular diagonal; analytic identity theorem | Identical even facing graphs; exact analytic uniqueness and fixed finite-order stability, not noisy global continuation |
| Physical independent jet coordinates | Theorem 8.3; `v5/20_contact_rigidity.tex`; Section 9.1 | Analytic area compensator above prescribed graph-jet order; triangular support-to-graph map | Full leading hierarchy of the selected horizontal ground channel, not every selected channel; vertical derivative check retained |
| Uniform finite-flight jet inverse | Theorem 9.1; `v6/20_finite_jet_stability.tex` | Positive summand diagonal; two endpoint terms bound it below uniformly in j; finite recursive inverse with uniform derivatives | Fixed recovered order M, arbitrary flight number j; coefficient noise, not raw probability noise |
| High-order diagonal comparison | Proposition 9.2; same file | Divide exact half-line and one-flight formulas; geometric-series asymptotics | Fixed lower jets and same absolute coefficient error; no full condition-number or minimax equivalence |
| Conditional-position acquisition | Theorem 12.3; `v5/50_self_calibration.tex` and preceding variance sections | Square-root onset pilot, safe fallback, paired conditional variance, Richardson extrapolation, waiting-time cost | Selected positions plus count pilot; local coarse bracket supplied; e^(j gamma) rarity charged |
| Ambient four-amplitude inverse | Theorems 15.1-15.2; `v5/40_pairwise_inverse.tex` | Contour extension in symmetric coefficients, positive four-function Wronskian, inverse-function theorem, root matching, physical cubic sharpness path | Independent area normalizer; equal facing curvatures for actual-curvature interpretation; otherwise effective parameters |
| Physical three-amplitude inverse | Theorem 16.1; `v6/30_three_amplitudes.tex` | Exact area constraint, printed derivative table and nonzero determinant at R=1/4; joint-gap coefficient inverse; root matching | Local physical family near R=1/4, includes multiplicities and nearby R; not global minimal-data claim |
| Bernoulli amplitude acquisition | Lemma 17.1; `v6/40_count_only_acquisition.tex` | Uniform threshold derivatives, finite extrapolation, Bernstein concentration with probability O(h^2) | Raw unlabelled counts, J=3 or 4, fixed extrapolation order; known gap for this lemma |
| Calibrated count-only curvature acquisition | Theorem 17.2; same file | Count-only j=1 square-root pilot; L=J+1 all-outcome safety; conditional fresh-count concentration; explicit timing error; three/four-amplitude inverse | Coarse local bracket supplied; fine timing fully charged; sufficient epsilon^(-(6+6/m)) cost, not minimax |
| Record responses and circular consequences | Section 18 and Appendices A-G | Original source-pinned proofs | Retained with original hypotheses; not replaced by new general-itinerary claims |

## Attribution of calculations

The first v5 report supplied the limiting/one-flight diagonal ratio, the physical three-amplitude determinant, and the known-gap count baseline. The later report supplied formula (F) for the finite-flight diagonal and the vertical-channel calculation (V). These contributions are acknowledged in the response. The new uniform-in-flight inverse follows from the explicit endpoint bound. The experiment-transfer theorem and locally calibrated count-only composition have complete proofs in the new sections. No exhaustive external novelty claim is made for any consequence.

## Preservation map

The new Git paper directory is derived from the complete reviewed v5 directory tree `6445f4fbefa574e575ac870d4987754bf8cf94fe`, not from a shortened reconstruction. The manuscript driver replaces the opening exposition, retains all existing active proof chapters, and inserts four new mathematical chapters. Targeted edits to `v5/20_contact_rigidity.tex` and `v5/40_pairwise_inverse.tex` correct the advertised channel/curvature interpretation; their proof chains remain. The comparison and bibliography are expanded.

The inherited directories have exact Git tree identities: `v2` = `7400fdf153b4a3fb2cb888c0f602afbc2c2ea203`; `v3` = `3074daddd6e19dcea3125699d774b3661d5a5f4d`; `v4` = `1f4135226cbb613db06a1ec79911f63f9cfc6fd0`; `sections` = `b1eade005465575f0d8356d384855f396125d516`. The preamble and two-collision source are unchanged. Original reviewed v5 text is copied into `history/v5-reviewed/` for comparison. No existing root-repository file is deleted or overwritten by this revision.

## Verification boundary

Finite symbolic checks test the exact derivative and area identities, rational Schur complements, extrapolation cancellations and safety margins. Ordinary floating checks test population pilot examples and a quadratic-law total-variation comparison. The unchanged referee script also checks nonlinear stationary chains. Neither suite proves a continuum theorem. The printed proofs, rather than a diagnostic count, carry the mathematical conclusions.
