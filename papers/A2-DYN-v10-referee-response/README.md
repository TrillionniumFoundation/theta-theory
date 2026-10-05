# A2-DYN — revision 10

**Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas**  
Qian Qi — 5 October 2026

This is the complete revised article, not a response-only supplement. Its entry point is `main.tex`. The title, physical family, joint displacement/count/flight-time record, raw mixed-density endpoint, periodic arithmetic, critical-edge calculations, and all twenty-four mathematical core files of revision 9 are retained. The new files are included in the article.

## Controlling review and source

The revision starts from review commit `8448e718a22658c94dcb654b52c69b44f9889fe1`, which contains the report on author commit `872f8695670373a3ca67ff84841a1ea38ed64227`:

`reviews/a2-dyn-v9-external-top4-review-2026-10-05/REFEREE_REPORT.md`

The report's blob is `14539536556fc1d041cc30917296708084146259`. The revision-9 mathematical core tree is `c38e24f02fae423f231ccfa1389751abd8a51789`. The current response and source manifest use this report, not the superseded revision-8 report.

## New mathematical content

Theorem B and Theorem 21.3 establish a radius-uniform **integrated** Gaussian comparison on the growing rescaled ball `|v| <= 2 n^(1/200)`, with error `C n^(-3/280) sqrt(log(2+n))`. The record is the actual deterministic first-return record. The theorem includes complex initial insertions with uniformly bounded supremum and initial-coordinate BV norms. It is proved from a frequency-explicit collision estimate and exact stopping, without an induced spectral expansion or an independence assumption.

Corollary 21.4 inserts that proved central integral into exact raw inversion. Positive definiteness, the complementary residual integral and local edge corrections remain explicit hypotheses. In particular the new band's physical radius `n^(-1/2+1/200)` is smaller than the old `n^(-2/5)` cutoff; no unproved annulus estimate is hidden in the substitution.

Appendix A gives the finite candidate-center lemma, uniform semialgebraic slicing, chart gluing and smooth-density norm identification. Appendix B gives explicit chronological product errors, zero/short-block treatment, the complex fourth-derivative bound, coarse interpolation, and covariance-square-root continuity.

## Files and verification

- `RESPONSE_TO_REFEREE.md`: responses to every essential and technical comment.
- `PROOF_LEDGER.md`: dependencies, new conclusions and exact remaining boundaries.
- `SOURCE_MANIFEST.json`: source-pinned identities and byte-preservation hashes.
- `COLLISION_INPUT_MAP.md`: retained detailed collision-theory source map; Appendix A supplies the expanded norm proof.
- `VALIDATION.md`: local build and inspection record, with verification limits.
- `tools/verify_v10.py`: active preservation and finite-diagnostic entry point. Older verification scripts are preserved as historical dependencies, not renamed v10 entry points.

From this directory run `bash build.sh`. The result is `build/main.pdf`. Native local compilation produces **69 pages**, with **27** unique mathematical core inclusions, **91** proof environments and **266** labels. All **24** inherited core files are byte-identical to the reviewed v9 source. The exact-event-SHA GitHub workflow is `.github/workflows/a2-dyn-v10-qualification.yml`; its artifact contains the PDF, source archive, logs and machine-readable evidence. The workflow performs read-only qualification and does not modify repository source.

## Scope

The growing-band integral is an unconditional conclusion within the article's established collision input. The full raw LLT, uniform positive definiteness, induced high-frequency realization, all-branch residual estimates and exact-event conditioned limits are **not** claimed proved. Initial insertions are not arbitrary terminal or multiple-time insertions. No independent human dynamics review or journal acceptance is claimed. The manuscript remains directed at the original raw mixed-density problem; it is not recast as a different specialist paper.
