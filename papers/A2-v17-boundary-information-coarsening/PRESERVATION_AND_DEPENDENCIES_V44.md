# A2 v44 — preservation and historical dependency audit

## Frozen baseline

The addressed report is `reviews/a2-v43-independent-harsh-top4-2026-09-14/REFEREE_REPORT.md` at `6f7de242000a7db2bf473276b8e1792104c7cd42`. Its native source is `22d9b930a426cdb2c62984a5a3e5875e95e05e79`, and its products commit is `edd95683ee57965ff8cd82cee1462a478d06ae39`. The revision descends from the report commit and does not modify that report or any historical branch.

## Exact preservation

`tools/check_revision_v44.py` reads the already committed v43 active-source manifest. All 95 baseline entries (94 main, one companion) are checked by Git blob identity. The only replaced native TeX file is `main.tex`; its exact baseline bytes are retained as `history/v43-review-baseline/main.tex`. The checker reverses precisely the declared revision metadata, abstract addition and two new inputs and requires the result to equal the archived baseline. The remaining active source files stay byte-identical at their original paths. Direct input order and complete recursive input closure are checked.

The complete current main has 96 recursive TeX files; the companion has one. The 212 inherited theorem-style environments remain: 79 theorems, 59 lemmas, 34 propositions, 35 corollaries and five definitions. This is a preservation count, not a count of independently novel or independently re-proved results. Four environments are added: one theorem, two propositions and one corollary. No whole part, auxiliary proof, bibliography item, statistical experiment or physical construction is deleted.

The old root README, old paper README and complete old main are archived by their original Git blob identities. Earlier failed-build ledgers and the incorrect v43 retention receipt remain historical evidence. The A1 and other programme workstreams are not edited.

## Sources consulted and their role

The current introduction and proof architecture, v43 geometric setup, signed contact inverse, complete single-offset inverse, analytic continuation, intrinsic signature/symmetry classification, rerooting lemma, rank-two reconstruction, global physical reconstruction setup and analytic support-variation construction were consulted. The v32 historical audit, v42 preservation record and v43 report's source map were also used. This is a dependency audit and targeted proof examination, not a fresh line-by-line certification of the 222-page predecessor.

| New argument | Inherited dependency and reason |
|---|---|
| Uniform contact collars and signed limiting laws | `v3/10_geometry_action.tex`, `v3/20_integration.tex`, `v4/10_boundary_layers.tex`, and `article/01c_geometric_setup_v43.tex`: positive curvature, gap and third-obstacle clearance for the selected channels |
| Actions from the eight laws | `article/23f_single_offset_law_inverse_v42.tex`: the amplitude-cancelling density ratio with a nonzero scalar anchor |
| Both contact jets | `article/23a_signed_endpoint_rigidity_v27.tex`: smooth finite remainders and the homogeneous determinant-one block inverse, not merely formal polynomial jets |
| Complete curve images | `article/23c_analytic_continuation_v23.tex`: analytic germ globalization |
| Intrinsic incidence and one common frame | `article/23b_intrinsic_multichannel_rigidity_v28.tex`, `article/23b1_signature_rigid_rerooting_v40.tex`, and `article/23d_rank_two_lattice_recovery_v43.tex`: signature uniqueness, rerooting and marked rank-two holonomy |
| Physical realization on compact subfamilies | `article/25a_common_observables_v25.tex` and `article/25b_augmented_global_reconstruction_v26.tex`: observable pilots, finite separating tests, fresh long-flight stages and charged preparation caps |
| Analytic-neighborhood comparison | `article/25c_analytic_variation_bundles_v25.tex`: earlier support-function variations; the new proof supplies a simultaneous globally periodic family and explicit clearance/symmetry margins |

## Fresh proof content and its boundary

The new proof derives support parametrization, curvature and free-area formulas, the all-lattice separation and clearance bounds, nonsymmetry, nondegenerate closest contacts and uniform gates. It then checks the same-frame cycle and spanning conditions together, derives two-harmonic registration from recovered images, computes the exact lattice Gram form and proves analytic persistence. Those arguments, rather than numerical experiments, establish the new mathematical statements.

The finite diagnostic receives complete curve-image invariants at its registration stage. It does not purport to reconstruct analytic boundaries from a finite number of empirical endpoint samples. Its checks cannot certify the all-order forward law, smooth-remainder theorem, analytic continuation, Poisson comparison kernels or physical complexity bounds. Existing assumptions and non-effective compact-class conclusions remain explicit.

The current primary-source notices for Florio–Leguil (arXiv:2010.04120v5), Finamore–Leguil (arXiv:2510.18983), and Meister–Reiß (arXiv:1101.5248) were checked for consistency with the retained introduction. No new priority or reduction claim is made, and this is not an exhaustive literature certification.
