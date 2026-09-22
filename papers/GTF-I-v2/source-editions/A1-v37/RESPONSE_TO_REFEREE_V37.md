# Response to the independent referee report on A1 v36

**Manuscript:** *Attainable information and causal compression at exponent collisions*, publication revision v37.  
**Author:** Qian Qi.  
**Date:** 9 September 2026.  
**Controlling report:** `reviews/a1-english-v36-harsh-independent-2026-09-08/REFEREE_REPORT.md`, commit `1e7af61f0812638d00ee0efad8fc9a68e2776c3c`, blob `326d00cd68f03d91318e4181cb45786bf14fd7b8`.  
**Reviewed manuscript:** `8f074b8027627a71a81a362b9d15f47975e1f3ae`.  
**New branch:** `revision/a1-english-v37-publication-2026-09-09`.

We thank the referee for the detailed examination and favorable recommendation. The report closes the two preceding requests, recommends acceptance of the main article, and makes no further mathematical revision mandatory. The present edition therefore preserves the mathematical text that was assessed. It does not introduce an unrelated theorem, remove a result, or change the experiment in response to a requirement that the report does not make.

## 1. Disposition of the remaining requests

**R35.1: common normalization.** Corollary 13.3 and its proof remain unchanged. The three total horizons use one normalization H = 16 and one fixed L >= 8. The bound 245/16 < 16 applies throughout the original calibration square. Thus their normalized two-trial future nodes and Fourier matrices are literally the same at a fixed calibration. Acquisition still imposes the different cutoffs 3, 6 and 9. The report explicitly closes this request; no additional restriction has been introduced in v37.

**R35.2: crossover interpretation.** Remark 13.4 remains unchanged, including its explicit sentence that the crossover orders belong to the comparison envelope and are not exact optimizer transition thresholds. The two exponential orders and the path-free determinant argument are retained. The report closes this request as well.

**Closer literature comparison and production.** The report also confirms that the full-spectrum and superresolution comparisons are answered, and independently reproduces the complete v36 native build. We retain those comparisons and their proofs in full. Its independent execution remains a historical referee result, separate from the current author-side production verification described below.

No new R36 mathematical request is supplied by the report. We have therefore not invented additional numbered objections or claimed to repair an error that it does not identify.

## 2. The assessed mathematical contribution is preserved

The principal theorem remains the jointly calibration-and-budget-uniform attainable collision law. Its proof still proceeds through the feasible monomial tangent, strict mixed-moment and complete confluent pairings, minorization under the actual command-and-report law, whole-image anisotropic covering, and one reachable raw-moment transducer charged after each report. Every integer budget, additive collision stratum, and stated mean or worst-history conclusion is retained with its original quantifiers.

The supporting finite-cell realization, Blackwell postprocessing description, zero-evidence and zero-occupancy arguments, purification, scalarized polyhedral realization, compatibility, precision and exact-example results remain active. The full spectral comparison and both clarified consequences retain their existing roles. The complete companion and the historical derivations are preserved in the new Git subtree.

The source check compares the full 80-file native input closure with the pinned v35/v36 manifests. Seventy-nine inputs are byte-identical. In `main.tex`, the sole change is the edition date from 8 to 9 September 2026. All 222 theorem-like blocks and all 210 proof blocks are verbatim. The abstract, introduction, mathematical prose, formulas, theorem labels, references and native input selections are unchanged. These preservation checks establish a textual fact, not a new proof certificate.

## 3. Current source-pinned native build

The publication source was first committed as `616904c0f151b51e75b8a09fb98c25b65209975a`. The complete native pair was then built with that actual commit identifier. The later evidence commit does not change any active TeX input. Thus the current receipt identifies an existing source commit rather than an uncreated future commit or a floating branch.

The build produces a **42-page main article and 159-page companion**. All six compiler invocations return zero; actual external-label exports converge after three paired cycles. The final logs contain no unresolved references or citations, changing or multiply defined labels, or overfull boxes. The TeX recorder agrees with the declared 80-file input closure. The builder uses neither external-reference stubs nor substitute theorem statements.

`verification-v37/NATIVE_BUILD_V37.json` retains the compiler, source commit, pass and log hashes, converged exports, PDF hashes and reconstructible source manifest. The full execution receipt and compiler stdout logs are included in the downloadable native package. `build.py` uses the same content-verified native builder as the reviewed edition, with the output edition changed to v37.

## 4. Output equivalence and regression checks

All 201 PDF pages were compared with the supplied v36 PDFs. The only text change is the main-article date on page 1. At the recorded 72-dpi RGB rendering scale, all other **200 pages are pixel-identical**; all companion pages are text-identical as well. This is a specified output comparison, not a claim that PDFs with different metadata are byte-identical or that all graphical scales were compared.

All 42 main pages were inspected at coarse contact-sheet scale. Main pages 1, 38 and 39 and companion page 80 were additionally inspected enlarged. No apparent clipping, overlap or missing glyphs was found in those views. The visual record distinguishes these samples from a full-resolution proofread of every equation.

The four current, source-pinned mathematical diagnostic programs were replayed in ordinary and optimized Python. Their outputs match one another and the recorded v36 hashes. The new preservation/replay wrapper was also run in both modes with identical output. These are finite regression checks. We do not reattribute the additional referee-only checker to this edition or claim a new global controller optimization, formal proof-assistant run, or originality certificate.

## 5. Publication and subsequent review

The new directory contains the complete inherited Git source tree, the original controlling report, this response, the proof-preservation ledger, the source diff, and current verification records. The old entrypoint, README and build wrapper are retained under `history/`; the original review and revision branches are not overwritten. The downloadable package contains all 80 native TeX inputs, both PDFs, executable verification tools and complete current build logs. The full inactive historical tree remains available in the repository rather than being repackaged wholesale.

The referee recommendation concerns the main article and the scope examined in that report. It is not an acceptance decision by a named journal or a certificate for all eleven planned papers. We submit the preserved publication edition for the next assessment without changing its mathematical claims.
