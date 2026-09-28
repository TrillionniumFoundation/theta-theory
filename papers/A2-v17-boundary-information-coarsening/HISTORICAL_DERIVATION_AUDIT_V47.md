# Historical derivation audit for A2 revision 47

Date: September 14, 2026. Review baseline: `45b42eee377c7fd3cff81c24c95acb91d6f46ab6`. Native mathematical baseline: `ab99196fadc20682c1ee44d6bb433a788c7274ab`.

## Sources examined and their use

The latest report was read in full, including its distinction between the favorable proof findings C1–C4, the minor calibration clarification P1, and the editorial assessment E1. Its independent finite-check script and the reviewed source identity were examined. The final native artifact for run `34838199154`, attempt 1, artifact `10345480046`, supplied the source archive used for local work. Its source ZIP and manuscript hashes were checked against its build report; the two inherited files to be edited also matched their Git blob identities in the review branch.

| Historical material | Role in the revision |
|---|---|
| `article/23k_quantized_law_stability_v46.tex`, complete section | Retained quantitative class, finite histogram interpolation, Bellman recursion, analytic continuation, registration, explicit accuracy prescription, conditional confidence and caps. The only edit in this module is the requested adjacent calibration clarification. |
| `article/23f_single_offset_law_inverse_v42.tex` | Checked the normalized single-offset law, the amplitude-free inversion interface and full-box finite-flight normalization needed for offset-uniform categorical bias. |
| `article/23a_signed_endpoint_rigidity_v27.tex`, finite smooth-remainder factorization, especially the argument corresponding to source lines 298–404 | Kept the actual functional finite-jet justification separate from truncated polynomial calculations. No replacement by formal Taylor algebra is made. |
| `article/25a_common_observables_v25.tex`, complete section | Reused the existing physical observation space, positive-offset normalization, measurable same-flight pilot, onset error multiplied by the final flight number, observable projection error, and fully charged pilot cap. |
| `article/25b_augmented_global_reconstruction_v26.tex`, complete section | Checked the prior choice of final even flight number before the pilot, the conditional uncapped-success construction, and the distinction between old bounded-Lipschitz tests and new hard categories. |
| `article/01_introduction_v41.tex`, quantitative overview v46, previous response and historical audit v46 | Preserved the observation-specific research architecture; added an acquisition overview instead of deleting the accumulated mathematical results or importing referee correspondence into the article. |
| Generic skeleton and registration material v45 and the report's audited registration interface | Retained the arbitrary finite asymmetry witnesses, unknown lattice, common-frame convention and zero-net-gain backtrack. The new proofs use the already stated quantitative registration theorem unchanged. |

The proof route is: normalized relative endpoint law; signed action and finite contact-jet inverse; finite support jet and analytic continuation; intrinsic registration and marked lattice recovery; quantized observation stability; then the new explicit timing and cell-edge error transfer. The existing position pilot is reused at the final flight number, not run at an earlier smaller number.

## Literature check

Primary-source records were checked on September 14, 2026. Trefethen, *Quantifying the ill-conditioning of analytic continuation*, BIT 60 (2020), 901–915, DOI `10.1007/s10543-020-00802-7`, is relevant background for conditional continuation, not a replacement for the manuscript's proof. Finamore–Leguil, arXiv `2510.18983`, uses an enriched marked length spectrum, not this endpoint-law observation. Florio–Leguil, arXiv `2010.04120v5`, explicitly removes the earlier geometric rigidity assertion affected by the stated error while retaining the dynamical results. The existing bibliography and these distinctions are unchanged. This was a targeted comparison, not an exhaustive priority search.

## Fresh proof and diagnostic scope

Fresh derivation covers the full new offset-continuity lemma, hard-cell coupling lemma with outer edges, calibration-aware confidence theorem, and explicit joint grid/pilot/sample prescription. The offset comparison is made on one fixed true boundary after the same estimated observable projection. It does not rely on total-variation continuity between ambient position laws on different curves. Concentration is applied before adding cap failure.

The finite diagnostics check the exact quadratic-cap offset identity, the flight-number amplification, exact rational category perturbations and a negative control for suppressing chart error, and every budget in a finite illustrative design prescription. The functional test maps are not claimed to be billiard realizations. Ordinary and optimized executions agree. The inherited v46 quantitative and adaptive/v32/v38 diagnostics are separately rerun, not presented as newly independent implementations.

Source preservation is checked against all 101 entries of the frozen main-plus-companion input manifest, including exact original Git blobs for the two amended files. New current inputs total 103. The complete native main and companion are compiled, not merely the new section. Successful source, finite algebra and build checks do not constitute a new line-by-line audit of every inherited operator estimate, Gaussian or Poisson experiment theorem, deconvolution result, auxiliary application, or companion proof. Their original complete texts remain available to the next referee.

No default-branch merge, historical-branch force update, permission change, membership change, or deletion of prior research material is part of this revision. Final publication identities and the scope of rendered-page inspection are recorded separately in the v47 delivery entry.
