# Historical derivation audit — A2 v49

## Frozen starting point

Latest report and its reproduction record: `reviews/a2-v48-independent-harsh-top4-2026-09-14/`, commit `a512f70ca77d711bd6c9ee61988f1e8dd4dba790`. Reviewed mathematical source: `fe21046e47a89ec3b3df8493f4d885b087e3ad7f`. The complete v48 native source archive has SHA-256 `8e6968aa48d0eca3e0844c80bdab57c2c3d1c727be2dfecb4722477df98b06ff`; the Actions ZIP has digest `bee6a759c375a030a4b9540e23ec887374e01d336706e89302f781639efeab07`.

The report and its full audit record were read. Historical inputs below were examined at the proof interfaces used for this revision. This is not a claim to have independently re-proved every LAN, Poisson, deficiency, deconvolution, weighted-operator, auxiliary or companion theorem in the entire corpus.

## Actual derivation path used

| Source | Role and scope in v49 |
|---|---|
| `article/01c_geometric_setup_v43.tex` | Actual signed, channel-centered fixed-offset relative theorem and parameter conventions. Kept unchanged; now begins the core proof immediately after the introduction. |
| `v4/10_boundary_layers.tex` | Weighted half-line orbit, moving reference Green kernel, subtracted trace-class perturbation, edge sum, relative amplitude and determinant gluing. Read for the exact functional-family differentiation interface, especially the amplitude and trace-series arguments. Kept unchanged. |
| `article/23a_signed_endpoint_rigidity_v27.tex` | Terminal-envelope control and actual smooth finite-remainder factorization before homogeneous isolation. The finite truncation is differentiated before its limit, and the remainder argument permits flat differences. Kept unchanged; not replaced by a formal-series computation. |
| `article/23f_single_offset_law_inverse_v42.tex` and `article/23c_analytic_continuation_v23.tex` | Signed four-density action inverse and entire analytic images in separate contact frames. These steps do not need obstacle asymmetry. Kept unchanged. |
| `article/23b_intrinsic_multichannel_rigidity_v28.tex`, `article/23b1_signature_rigid_rerooting_v40.tex`, `article/23d_rank_two_lattice_recovery_v43.tex` | General incidence/gluing framework, root conventions and unknown marked lattice. All remain active without edits. |
| `article/23j_generic_finite_channel_rigidity_v45.tex` | Clear-skeleton existence, proper-symmetry Fourier criterion, exact asymmetric theorem, and displacement cochain. Read for the symmetry count and completeness of the new finite-branch construction; all original statements and proofs are byte-identical. |
| `article/23m_differential_rigidity_v48.tex` | Forward derivative, signed finite-jet kernel, analytic support variation and geometric gauge. Expanded only at moving-reference differentiation and noncircular local registration; the finite-coordinate argument remains. |
| `article/23k_quantized_law_stability_v46.tex`, `article/23l_calibrated_histograms_v47.tex` | Quantified whole-table histogram inverse and charged same-flight calibration. Both byte-identical; moved as complete inputs into the physical-acquisition part. |
| `article/25c_analytic_variation_bundles_v25.tex` | Historical compatible fixed-contact finite-jet and information-design result. Retained unchanged; not relabelled as a whole-table moving-lattice theorem. |

The report's Section 4 supplies the noncircular differential suggestion and the disk-lattice control. The revised article credits these suggestions. It additionally proves the finite exact reconstruction-branch theorem by combining the recovered entire images, finite symmetry torsors, a channel-incidence tree, and the existing cochain formula. This is a finite classification for exact function-valued data, not an assertion of globally unique phase on symmetric obstacles.

## Avoided invalid shortcuts

The derivative of the moving Green reference is retained. Trace-norm summability is obtained after subtraction, not by multiplying a nondecaying bound by the number of sites. The density normalizer is differentiated separately. The contact inverse is used at each finite actual-smooth order, and analyticity is applied to the controlled variation itself.

A nonzero harmonic determines angular velocity on the *actual continuously followed* congruence branch. A base symmetry need not persist when symmetry is broken; no arbitrary base branch is presumed to extend. Global exact alternatives are enumerated instead of being silently removed. The integer gain matrix need not be unimodular, and period scale and Gram form remain reconstructed quantities. The circular example concerns precisely its two-channel design, not every possible experiment.

## Active preservation and organization

`history/v48-review-baseline/active-source-manifest.json` is the actual v48 native manifest. Five edited active originals are archived there at their original relative paths: `main.tex`, `article/00_structural_introduction_v48.tex`, `article/01_introduction_v41.tex`, `article/23m_differential_rigidity_v48.tex`, and `v5/references_v43.tex`. The materializer rejects mismatched old SHA-256 values and unexpected edits. It is idempotent.

All 105 inherited inputs and their old labels remain in the active recursive main/companion graph; 100 inputs remain byte-identical at their original paths. The one new active input is `article/23n_finite_symmetry_v49.tex`. The new graph contains 106 inputs. The combined baseline includes 89 theorem, 74 lemma, 40 proposition, 40 corollary, five definition, 22 remark, one structural-theorem and 239 proof environments; their counts remain, with only the four new proved environments added.

The complete old detailed introduction and revision overviews now appear in compiled Appendix A.1. They have not been deleted or replaced by links to an external archive. The main structural introduction is rewritten around the same recovered object and its exact/differential symmetry distinction. Part I contains the core geometric proof in dependency order; Part II the local information experiments; Part III finite-resolution and physical acquisition. The full companion and all auxiliary derivations remain.

## Evidence classification

`tools/check_revision_v49.py` verifies preserved inputs/labels/environment counts, the intended top-level permutation, the finite determinant derivative and a missing-reference negative control, finite cyclic stabilizers and strictly convex Fourier examples, the symmetry-breaking branch distinction, the synthetic tree-assignment count, and exact disk-lattice/clearance identities. It also reruns the earlier finite differential and calibration functions. These are exact finite controls, not a machine proof or a realized generic-table inverse.

The complete native-build driver remains unchanged. Source freezing, imported companion auxiliary data, PDF products and post-push artifact verification are recorded separately. The final review-ready ledger gives actual run, source and product identifiers and sampled visual coverage. A1, unrelated research workstreams, prior reviews, the default branch and repository permissions are not modified by this revision.
