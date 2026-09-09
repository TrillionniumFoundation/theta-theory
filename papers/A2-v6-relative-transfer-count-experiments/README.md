# A2 v6: relative boundary laws and statistical reconstruction

**Author:** Qian Qi. **Date:** September 9, 2026.  
**Main source:** `main.tex`. **Local compiled length:** 63 pages.  
**Revision branch:** `revision/a2-v6-relative-transfer-count-experiments-2026-09-09`.

This is the materialized response to the v5 statistical-contact-rigidity report at `9975aa037d5d9eb1f339b9220f9cd21fb54c0876` and the later second report at `0421836a5868967f90093281c7ca43aab9815a0d`. It is based on the actual author manuscript at `1e57d9c024f90f0304e5572c0e320707bab88074`, not the earlier branch whose v6 name only pointed to a review snapshot.

## Referee entry points

Read `RESPONSE_TO_REFEREE_V6.md` for the point-by-point response, `PROOF_LEDGER_V6.md` for assumptions and dependencies, `SOURCE_PINS_V6.json` for provenance, and `VERIFICATION_V6.json` for executed commands and limits. The `V5` ledgers and prior source pins retained in this directory describe the previous revision, not the present verification run.

The new mathematical sections are `v6/10_experiment_transfer.tex` (total variation, raw rare-event mass and product-risk transfer), `v6/20_finite_jet_stability.tex` (all finite flights, fixed-order uniform inverse and sensitivity comparison), `v6/30_three_amplitudes.tex` (the constrained physical area model), and `v6/40_count_only_acquisition.tex` (Bernoulli counts through fine calibration to coalescing curvature recovery). The general nonsymmetric forward theorem, full relative-factorization proof, limiting contact inverse, four-amplitude inverse, selected-position acquisition and all active appendices remain.

## Build and checks

Install a TeX distribution with `latexmk`, `pdflatex`, AMS packages and the packages named in `preamble.tex`. From this directory:

```sh
python tools-v6/build.py
python tools-v6/verify_revision.py > revision-checks.json
python -O tools-v6/verify_revision.py > revision-checks-optimized.json
cmp revision-checks.json revision-checks-optimized.json
python review-basis-v5/independent_checks_second.py > referee-checks.json
```

The diagnostic scripts require NumPy, SciPy and SymPy; exact executed versions are in `VERIFICATION_V6.json`. They use explicit failure exceptions and make no network requests. The latest referee script is retained unmodified with its provenance. The build script compiles the complete article and the unchanged seven-page companion, and rejects undefined references and overfull boxes.

The source is committed to this branch. Compiled PDFs and the standalone active-source packet are delivered separately with the conversation; their hashes are recorded in the verification and delivery records. No remote CI success or journal acceptance is asserted. The standalone packet is sufficient to compile the active article; the Git branch additionally preserves all inactive inherited history and older verification materials.

## Observation models

Scalar leading amplitudes recover actual contact curvatures only when the two facing curvatures within each channel agree; otherwise the parameters are effective channel curvatures. The physical three-amplitude theorem is local near `R=1/4`; the four-amplitude theorem permits an independent normalizer. Exact contact germs, noisy coefficient vectors, conditional positions, and raw counts are distinct data.

The new count-only rate includes fine calibration but starts from a supplied coarse bracket. It is a sufficient rate, not a minimax assertion. The total-variation theorem concerns the specified endpoint/residual-time record and its failure atom, not a silently enlarged full growing collision array. All these distinctions are printed in the mathematical statements and proofs.
