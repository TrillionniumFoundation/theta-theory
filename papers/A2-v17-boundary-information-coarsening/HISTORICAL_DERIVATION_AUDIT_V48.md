# Historical derivation and preservation audit — A2 v48

## Pinned objects

The latest report is frozen at `757f2ee4e3bf766d2eb56d972e6d2f621b3fd2a6` on `review/a2-v47-independent-harsh-top4-2026-09-14`. Its actual v47 mathematical source is `219b39e94b14187561dc3b7e5bdbae49dbd92cc2`; native run `34843699559`, artifact `10347280538`. The 248-page main and 7-page companion in that artifact supplied the source archive and active-source manifest used for this revision. These identities are distinguished from the review-ready and product-attestation commits.

## Historical route used, and what is added

| Historical source | Role in the revised proof | Treatment in v48 |
|---|---|---|
| `v4/10_boundary_layers.tex`, `v5/15_differentiated_operators.tex`, `article/15_operator_comparison.tex` | Nonlinear relative law and finite-order parameter derivatives on a flight-independent collar | Unchanged; used to establish the new forward `C^1` lemma |
| `article/23a_signed_endpoint_rigidity_v27.tex` | Weighted half-line inverse, finite terminal-envelope control, functional smooth remainders, triangular signed contact inversion | Unchanged; differentiated only at fixed finite orders |
| `article/23f_single_offset_law_inverse_v42.tex` | Four-density amplitude cancellation, nonzero scalar anchor, explicit action and curvature recovery | Unchanged; new section displays the full differential of the ratio, anchor and action |
| `article/23c_analytic_continuation_v23.tex`, `article/23k_quantized_law_stability_v46.tex` | Exact analytic continuation, finite graph-to-support conversion and quantitative order-before-noise reconstruction | Unchanged; new kernel theorem applies analytic uniqueness to the controlled support variation, not a norm-bounded continuation inverse |
| `article/23b_intrinsic_multichannel_rigidity_v28.tex`, `article/23b1_signature_rigid_rerooting_v40.tex`, `article/23d_rank_two_lattice_recovery_v43.tex` | Proper incidence matching, common root, two marked independent cycle holonomies, unknown Euclidean lattice | Unchanged; new section differentiates a finite harmonic registration and the lattice cochain |
| `article/23i_nonsymmetric_periodic_realization_v44.tex`, `article/23j_generic_finite_channel_rigidity_v45.tex` | Explicit nonsymmetric realization, obstruction descent, clear skeleton, open dense proper asymmetry, `N+1` channels | Unchanged; no graph-mechanism count is promoted to a universal observation lower bound |
| `article/23k_quantized_law_stability_v46.tex`, `article/23l_calibrated_histograms_v47.tex` | Full analytic-class finite histogram inverse and same-flight calibration with timing and all-edge crossing control | Both active files byte-identical, including the resolved R46-P1 clarification |
| `article/25c_analytic_variation_bundles_v25.tex` | Compatible fixed-contact finite jets and finite collections of positive-offset information designs | Unchanged; explicitly distinguished from full-table single-offset infinitesimal rigidity with moving lattice |
| `article/18*`, `article/25*`, `article/29*` and recursive auxiliary inputs | Local information under coarsening, charged physical reconstruction, position benchmark, complete technical proofs | No inherited theorem or proof removed; physical pilot and intrinsic inverse retain different observation levels |

The new route is

`fixed-offset law derivative -> action derivative -> every finite signed graph-jet derivative -> analytic support variation -> differentiable incidence registration -> marked lattice derivative -> finite-dimensional scalar local coordinates`.

The potential invalid shortcuts are each avoided: exact injectivity is not substituted for a derivative-kernel proof; a formal series is not substituted for the smooth finite-jet factorization; analyticity of parameter slices is not substituted for analyticity of the derivative; uniform support stability is not silently upgraded to a bounded inverse of continuation; two-cycle gains are not assumed unimodular; and compactness is not treated as finite-dimensionality.

## Precise new sources and hypotheses

`article/00_structural_introduction_v48.tex` states Theorem A and separates exact, differential, finite-dimensional and quantitative conclusions for their respective classes. `article/23m_differential_rigidity_v48.tex` proves the forward derivative including moving normalization, local signed derivative kernel, analytic propagation, finite gcd-one harmonic registration, full periodic infinitesimal rigidity, and scalar local coordinates.

A common-strip `C^1` analytic-support family is a hypothesis of the new *differential* theorem only. Every inherited smooth finite-jet, exact analytic, compact quantitative, local statistical and physical theorem remains in its original form. Arbitrary finite-dimensional immersed models are allowed for the coordinate theorem, but no finite-dimensional model is imposed on the full analytic class.

## Preservation invariant

The starting active manifest has 103 distinct inputs. All are kept active in their original relative input order. Only `main.tex` and the first section heading in `article/01_introduction_v41.tex` are amended. Their exact originals are archived under `history/v47-review-baseline/`. The new main has a condensed abstract, new structural introduction, and a relocated Part I heading; all old detailed statements remain in the body. Every other inherited active input, including the bibliography and companion, is byte-identical.

The recursive graph therefore has 105 distinct active inputs. The combined inherited sources contain 87 theorem, 70 lemma, 40 proposition, 40 corollary, five definition, 22 remark and 232 proof environments. All survive. The new inputs add Theorem A, four lemmas, two theorems and seven proofs. Counts are audited by `check_revision_v48.py`; they are content-preservation checks, not an assessment of novelty or correctness.

No A1 file, other paper, default branch, branch protection, collaborator permission, or historical review is modified. The new branches preserve the latest review ancestry. Full native build/provenance evidence belongs to the actual v48 compiled source, not an earlier PDF.
