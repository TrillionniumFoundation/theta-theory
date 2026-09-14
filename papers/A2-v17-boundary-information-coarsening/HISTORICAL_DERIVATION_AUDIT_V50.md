# Historical derivation audit — A2 revision 50

September 15, 2026. The review baseline is `5051b7789a424656a558179922607d8b55061b28`, containing the complete v49 report and reproduction record. Its reviewed mathematical source is `a003c1c69585f09f0b8fcc9fe03eb330cd6d57b7`, delivered as the 259-page main and seven-page companion. The v49 source archive and source-matched active manifest are the starting bytes, not the old directory's version number.

## Materials read for this revision

The complete latest report, including its Section 4 example and final disposition, and its `AUDIT_AND_REPRODUCTION.md` were read through the connected GitHub interface. The complete current main entry, structural introduction and finite-symmetry section were examined. The local source inspection focused on `v4/10_boundary_layers.tex` (half-line construction, normalized determinant gluing and physical limiting law); `article/23a_signed_endpoint_rigidity_v27.tex` (weighted inverse, terminal envelope, actual smooth finite remainders and order-by-order contact blocks); and `article/23f_single_offset_law_inverse_v42.tex` (amplitude-free density identity, scalar anchor and finite-order inversion). The analytic continuation, clear-skeleton and lattice-cochain sources were checked at the interfaces used by the exact-fiber example, and the current differential section and calibration hypotheses were compared with the latest report.

The v49 author response, historical audit, active manifest and preservation code were read as provenance and navigation, not treated as proofs. This round does not claim a fresh line-by-line reproof of every historical transfer-operator, LAN, Poisson, deficiency, deconvolution, physical reconstruction or companion theorem. Their active-source identities are preserved and their hypothesis boundaries are not changed.

## Derivation route retained

| Source | Role | Treatment |
|---|---|---|
| `v3/10_geometry_action.tex`, `v3/20_integration.tex` | Stationary action, cofactor twist and common-domain phase integration | Unchanged |
| `v4/10_boundary_layers.tex` | Two nonlinear endpoint layers; trace-norm relative gluing; fixed-offset conditional law | Unchanged; exact scale and cofactor identity displayed in the introduction |
| `article/23a_signed_endpoint_rigidity_v27.tex` | Weighted half-line inverse, finite terminal term and actual-smooth jet factorization | Unchanged; finite remainder bound and determinant-one block displayed in the introduction |
| `article/23f_single_offset_law_inverse_v42.tex` | Four-density nuisance cancellation and signed scalar-anchor inverse | Unchanged; continues to recover every fixed finite contact jet without supplied amplitudes |
| `article/23c_analytic_continuation_v23.tex` | Whole analytic images from recovered registered contact germs | Unchanged; no equality of arbitrary smooth germs asserted |
| `article/23j_generic_finite_channel_rigidity_v45.tex` | Clear skeleton, generic asymmetric exact uniqueness and marked cochain | Unchanged |
| `article/23n_finite_symmetry_v49.tex` | Finite congruence torsors, actual local branch, complete candidate enumeration and circular comparison | Entire file unchanged |
| `article/23m_differential_rigidity_v48.tex` | Moving-reference derivative, noncircular infinitesimal kernel, model-local scalar coordinates | Entire file unchanged |
| `article/23k_quantized_law_stability_v46.tex`, `article/23l_calibrated_histograms_v47.tex` | Full-class quantified inverse and hard-category acquisition with charged pilot | Both entire files unchanged; original observation and conditioning hypotheses retained |
| All other Part II/III and appendix inputs; complete companion | Observation-specific information, physical reconstruction and auxiliary arguments | All remain active; no inherited theorem or proof body rewritten |

The substantive new source is `article/23o_two_branch_example_v50.tex`. Its first proposition implements, with attribution, the referee's noncircular C4 example. It proves all-lattice disjointness and channel clearance, equality of the exact conditional laws, completeness of the two-element fiber and inequivalence of the marked lattices. Its second proposition shows that the mark (1,1) is a clear additional channel in both branches and its gap alone separates them. The new proof uses a radius tube about the center segment because the closest segment of that additional channel cannot simply be assumed radial.

The argument deliberately keeps four questions separate: exact recovery of full channel images; global discrete choices in their assembly; the local derivative kernel; and the information supplied by one extra marked observation. No example is misclassified as a counterexample to the valid theorem. No example-specific gap comparison becomes a general noisy reconstruction result.

## Content preservation

The exact v49 active manifest is archived in `history/v49-review-baseline/active-source-manifest.json`. The same directory retains exact originals of the three amended active inputs: `main.tex`, `article/00_structural_introduction_v48.tex` and `v5/references_v43.tex`. The amendments are version/date metadata, a brief abstract sentence, additive core-mechanism explanation, one new input and explicit attribution. Theorem A and its proof are unchanged verbatim. The old Part I ordering and compiled Appendix A.1 are unchanged.

The v50 checker verifies all 106 inherited inputs against SHA-256, byte length and Git blob identity; 103 remain identical in place. It checks all 518 inherited theorem-style/proof blocks verbatim, all old labels, and all active references. The new graph has 107 inputs and 1096 labels. All 243 inherited proof environments remain, with two new propositions and two new proofs. These are preservation invariants, not measures of significance or formal correctness.

No A1 file, other research paper, historical report, default branch, branch protection or collaborator permission is part of this revision's write scope. New author/product/review-ready branches retain the latest review ancestry.

## Scope of the additional checks

Exact SymPy controls check the curvature radius, original gaps, proper pair congruence, four relative assignments and two orientation-valid candidates, marked Gram difference, the determinant identities for every symbolic lattice mark, and the positive margins for the additional channel. A negative control records the nonzero support derivatives at its center directions, detecting the incorrect assumption that those directions must be contact normals. The preserved v49, v48 and v47 finite controls also run. None of these finite calculations substitutes for the written all-lattice geometry or the infinite-flight estimates.

The complete native build and final post-download checks are separate from proof review. Their exact source/product identities, retained warnings and actual sampled visual coverage are reported in the final v50 ledger.
