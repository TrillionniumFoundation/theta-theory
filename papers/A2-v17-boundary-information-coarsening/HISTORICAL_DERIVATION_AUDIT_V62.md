# A2 revision 62 — historical derivation audit

## Frozen inputs

The latest located A2 report is `reviews/a2-v61-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md` at review head `9ec2004a18cccc69ed473685bdf94c91f0b25d4d`. Its reviewed source is `71e0bd6306f54466728c2e6e781bb0f422c5cfb0`. The v61 native artifact `10426471183` was downloaded through the authorized GitHub connector. Before editing, all 753 frozen source files were verified against their recorded lengths, SHA-256 values and Git blob identities. The manuscript subtree is `ee2d39dbce4dce4d972ec1a281af1df9aaf44d4a`.

## Historical proof interfaces read and used

| Material | Role in the revision | Treatment |
|---|---|---|
| v61 referee report, both recommendation and detailed mathematical findings | Correctly identifies no mandatory core repair; distinguishes finite-flight inverse, realized separation, and significance. | Report retained unchanged in the source branch ancestry. Every numbered item answered. |
| `journal/00_principal_introduction_v61.tex`, structural statements, v61 response/history/dependencies | Establishes the observation conventions and existing scope; warns against another nominal importance repair. | All unchanged. A short separate overview introduces the genuinely added result. |
| `article/01c_geometric_setup_v43.tex` | Uniform selected-channel geometry, normalized phase preparation, fixed-offset convention and relative error. | Unchanged. New sampling model explicitly fixes calibrated time rather than programming unknown alternative gaps. |
| `v3/10_geometry_action.tex`, `v3/20_integration.tex`, `v4/10_boundary_layers.tex` | Nonlinear stationary action, relative cofactor normalization, density integration, half-line limits and acceptance scale. | Unchanged. New lemma uses their finite-order endpoint bounds, exact acceptance formula and positive-offset normalizers. |
| `article/23a_signed_endpoint_rigidity_v27.tex`, `article/23a2_analytic_contact_inverse_v59.tex` | Actual-smooth versus analytic inverse, full lower-coupling inversion, protected domains. | Unchanged. No diagonal-only or formal-jet substitute is introduced. |
| `article/23a3_conditional_observation_inverse_v60.tex` | Bounded analytic prior, real-density-to-inner-disc estimate, two-realizable-law comparison and all-coefficient control. | Entire theorem and proof read; unchanged. This is the substantive inverse input for v62. |
| `article/23f_single_offset_law_inverse_v42.tex` | Exact density factorization and fixed-order finite-flight inverse. | Unchanged. Its finite-order conclusion is distinguished from the new complete analytic target. |
| `article/23k_quantized_law_stability_v46.tex` | Cell observations, interpolation, global quantified reconstruction and charged experiments. | The relevant observation/confidence interfaces read; unchanged. New cell-density fit avoids multiplying a fixed-order inversion constant through a growing jet order. |
| `article/23l_calibrated_histograms_v47.tex`, `article/25a_common_observables_v25.tex`, `article/25b_augmented_global_reconstruction_v26.tex` | Offset amplification, hard categories, observable signed calibration and explicit pilot cap. | Relevant calibration/cost interfaces read; unchanged. New cellwise tube bound exposes `r_c/h`, with the inherited pilot imported substantively. |
| `v4/20_nonlinear_information.tex` and the report's independent quartic calculation | Preserves the realized leading-data separation and both action/amplitude terms. | Unchanged. Not treated as a statistical lower bound for the new experiment. |

## New proof chain

`exact finite phase density -> positive normalizer and acceptance lower bound -> finite-law comparison -> conditional analytic inverse -> complete-germ deterministic estimate`

and

`fixed raw-attempt budget -> binomial success control -> cell-density concentration -> measurable realizable-law fit -> complete-germ confidence bound -> explicit even-flight/grid balance`.

For estimated calibration, the additional chain is

`observable pilot -> fixed programmed post-pilot experiment -> offset error j*v_g+v_t + cell-boundary displacement r_c/h -> conditional confidence bound -> explicit pilot cap O((j+1) exp(Gamma*j) epsilon_pil^(-3) log(C/alpha)) -> epsilon_pil proportional to h^4 -> total-budget exponent vartheta*omega/(12*omega+Gamma)`.

The pilot's dependence is explicitly estimated, producing a slower power in the complete budget with a squared logarithmic loss. Its integer grid and ceiling terms are retained in the proof. This new result has a local analytic target. It does not replace the original smooth theorem, the global exact finite-fiber theorem, unknown-origin laws, the immersed-model coordinate theorem, or the existing full-table acquisition theorem.

## Preservation and coverage

The only amended inherited manuscript files are `main.tex`, `rigidity.tex` and `README.md`; their exact originals are archived under `history/v61-review-baseline/`. All inherited proof modules and both old introduction inputs remain byte-identical. The new reference-route file includes the entire original route before adding the three explicit pilot/acquisition aliases. No existing mathematical source is made inactive.

The audit concentrates on the interfaces above and the newly written finite-experiment proof. It is not a new line-by-line certification of the entire previous 420-page delivery, every global matching proof, the complete local-experiment catalogue, or the companion. Native compilation, file preservation, finite algebra controls and sampled visual inspection are distinct checks and are reported separately.
