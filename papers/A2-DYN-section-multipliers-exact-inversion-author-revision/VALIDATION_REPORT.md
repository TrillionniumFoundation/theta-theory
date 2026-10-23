# Validation report for the A2-DYN author revision

## Actual result and exact scope

The final **publication-local** source check, four mathematical verification programs and three-pass native LaTeX build completed successfully. The delivered manuscript has **271 pages**. These are actual execution and document records, not simulated qualification, a new referee report, or a proof that the raw pointwise local limit theorem or full four-coordinate inverse is complete. Both final mathematical completion flags remain false.

This report describes a **local, pre-push packaging snapshot**. Remote publication and a workflow for this new source have not yet occurred at this snapshot. Historical successful CI runs are recorded separately and are not transferred to this revision.

| Identity | Actual value |
|---|---|
| Build record used | `build/publication-local`, reproduced in `evidence/local/publication-local/` |
| Mathematical source SHA-256 | `a1b162cec833de28f138c2ba1e353b39be9a6d1d21a4398480afa8c7b38f9bd2` |
| Delivered PDF | `evidence/local/A2-DYN-manuscript.pdf` |
| PDF SHA-256 | `eadbce178543727a68058aa85f94c8f02b5e6a1e3879a392b85a7bfc46a185e6` |
| PDF size / pages | 2,118,501 bytes / 271 pages |
| Execution began | `2026-10-23T05:24:57.359511+00:00` |
| Execution finished | `2026-10-23T05:25:08.665881+00:00` |
| Detailed current summary | `evidence/local/VALIDATION_SUMMARY.json` |
| Current execution archive | `evidence/local/ACTUAL_LOCAL_EXECUTION.tar.gz` |
| Archive SHA-256 | `48cfe4ddd9afd6cd1b3a33c3d14f14e01254057be233946aa9d4a75f1b022f3a` |

The previous `final-local` candidate had mathematical source hash `5883bacfae0f46540aea50fb2bd00e4e5e6e7588afaa0a63938bd6b3a25b5121` and PDF hash `98d6ed0e207170678fc10a8e740e94c6c6e291f2ce81877d10bf1fc7458e26a5`. Its exact prior packaged receipts and PDF are preserved under `evidence/local/superseded-final-local/`. They are not the current validation. The final change made the original radius, occupation and lattice ranges explicit in the raw bridge; the current receipts were generated after that change.

## 1. Source identity, preservation and complete native closure

The final source check records **87 native closure files, 76 native core files and 1171 compiled labels**. It verifies **82 inherited active files unchanged**, including all **73 inherited core bodies 260–332**, and verifies the canonical identities of **660 unique historical native TeX objects**, totaling **7,303,280 bytes**. The historical object archive and census retain the original proof bodies, conditional statements, counterexamples and failed approaches. Identity and closure checks establish what was retained and built; they do not establish the truth of every theorem.

The final recorder lists 87 actual native inputs. The three additional active core modules are 333–335. `PROOF_NAVIGATION.md` gives final printed numbers and pages for their statements and the relevant retained inputs; `evidence/local/PROOF_INDEX.json` contains the complete 1171-label index and 49 new-module labels. The manifest and proof/dependency ledgers remain separate from this execution report.

The complete predecessor is the localized-clearance manuscript at source commit `9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761`, carried by `e84c06c758bed5b2dc09222ad725cfe0ba0d58dd`. The controlling report is `f01482035a0b945b50f1f9c30f30ef35077558dc`, which expressly examined `31792379408c5ace2c09284c2eb22d2331023433` through native 270–276. It is not described as a review of later continuation or as independent journal acceptance.

## 2. Four actual mathematical-program executions

All four programs ran with Python 3.12.14, optimization level 0, and exit code 0. The receipts preserve each exact command, working directory, timestamps, script hash, output and log hash. They are copied without rewriting into `evidence/local/publication-local/`; summaries are in `evidence/local/mathematical-checks.json`.

| Program | Actual checked content | Outcome and limits |
|---|---|---|
| `verify_section_constants.py` | Exact rational bounds for the physical defining polynomial and root bracket, root/section derivatives, momentum cap, coordinate motion, cone conversion, partition/arc counts and single source normalization; 100 explicit rational norm-parameter instances | PASS. In particular the recorded upper bound for the polynomial derivative is `-6710711/2500000<-2`, the momentum cap is below 5/6, and the moving horizontal-side bound is below 11. The finite parameter examples do not prove dynamical cone invariance or the full external spectral hypotheses. |
| `verify_exact_interval_inversion.py` | Symbolic piecewise tail, original `m^2/|I|` normalization, four-coordinate Fourier factor, actual-denominator ratio identity, analytical spike diagnostic, and finite-peak Gaussian constants; 60 closed-box integral comparisons at 90 decimal digits | PASS. The largest recorded numerical error/bound ratio is approximately 0.6404705763. Those 60 comparisons are auxiliary formula checks, not a proof for every physical orbit, interval or spectral frequency. The spike diagnostic is an abstract test of an invalid inference, not a substituted billiard model. |
| `verify_endpoint_kernel_algebra.py` | 20,100 exact collision/reversal-index cases, 200 guard/transient-sum cases, 630 determinant-one reversal matrices, 6 single-conditioning checks, and rejection of a false normalized-closure inference | PASS. These finite cases check index identities and normalization transcription. The native first-image, renewal, reversal and critical-sector proofs carry the continuum claims. |
| `check_historical_analytic_arithmetic.py` | 25 exact scalar/rational checks of inherited endpoint/localization exponents, outer-width balances, two-cap moment powers and fixed-positive-residence arithmetic | PASS. No spectral theorem, uniform physical source bound or exchange of limits follows merely from these calculations. |

The actual script hashes are:

- `verify_section_constants.py`: `8988cd26e549539745f58a22e863f12aa51ae395a81d402931ba9097b9185f38`.
- `verify_exact_interval_inversion.py`: `65106ec2d8cff1f9b10766d1aa7b03e54701fae34c83d4cad62f8ca9d2163d86`.
- `verify_endpoint_kernel_algebra.py`: `7175c26b162e8bf408adf9158e99b1001f48dd66fdd6ad267e55dff7b0473c20`.
- `check_historical_analytic_arithmetic.py`: `711432c5c1c21e8ca5496b9840930a983a4c262991c14aaf0b465a7f6f558c9f`.

The normalization checks retain the original entrance measure and its single factor, exact collision and occupation indices, genuine reversal and the actual roof-interval length. The programme results do not silently upgrade a weak tested operator to a strong operator, a total-variation budget to normalized roof height, or a finite leading critical coefficient to a complete local remainder estimate.

## 3. Actual native compilation

Three `pdflatex` passes ran with `-no-shell-escape`, `-interaction=nonstopmode`, `-halt-on-error`, `-file-line-error` and `-recorder`; every pass returned 0. The final native record reports no forbidden diagnostics and 271 pages. The exact per-pass commands/logs, final TeX log, recorder, auxiliary data, contents, bookmarks and extracted text are in the current execution archive. `pdftotext` also completed and its actual command record is retained.

Compilation verifies a readable build closure and reference assembly. It is not mathematical verification of continuous geometry, singular-source exhaustion, pressure, an ordered limiting remainder or the inverse Jacobian.

## 4. Final visual inspection: 24 pages, not 271

`evidence/local/FINAL_VISUAL_QA.md` and its JSON report cover pages **1–8, 239–253, 271**, totaling **24**. All 24 were directly inspected in the preceding 271-page candidate. Both PDFs were then rendered using identical settings and compared by exact pixel buffers: only page 246 changed. Publication pages 245–253 were additionally viewed directly, including page 246's final explicit parameter ranges. Thus the unaffected coverage is supported by verified pixel identity, not by the filename.

No clipping, unreadable mathematical glyphs, overlapping equation numbers, obscured headers, broken tables or material margin defects were observed in the covered pages. Pages **9–238 and 254–270 were not visually inspected**. The report makes no all-page claim and no independent human specialist certification. The final page PNGs, per-image identities and pixel-comparison record are preserved in `evidence/local/visual-qa/`; the root renderer's independent page record is also retained there.

## 5. Actual complete-baseline reproduction and preserved failed attempts

Before the new continuation, the complete 255-page predecessor was reconstructed locally with mathematical source SHA-256 `cecca59e06fc83d0e3bab89e41e347b6c831c50dd78e7603d63377ca4be4feb0`. The successful record contains **74 executions of 37 mathematical scripts**, once normally and once with optimization; all 74 returned 0. Its native PDF hash is `47b72ad61cebce137f5f63f21eb7e67eb3b51aa5a416f04b9a1ebaed8af1b822`. The full baseline phase began `2026-10-23T04:54:29.307678+00:00` and finished `2026-10-23T04:55:24.356147+00:00`. Its records are in `evidence/baseline/`, with 224 actual reproduction records in `ACTUAL_REPRODUCTION_LOGS.tar.gz`.

The earlier incomplete/failed attempts were not deleted or relabeled successful. `evidence/baseline/INITIAL_ATTEMPTS_DIAGNOSTICS.tar.gz` retains 448 diagnostic entries, including missing-`sympy` failures in the initial environment and proof-navigation failures caused by an output directory outside the expected article path. The successful later execution is a distinct record. The diagnostic archive hash is `9fcd33ba833347dc846528ab685433a3b473c370da2a5ab0f384806af3076c8d`; the successful reproduction archive hash is `575f8baa756024f40f871dbbb9d890b4fd3e9757f2787d66113d5402c6ccbf80`.

The 74 baseline executions and four current executions are separately identified; neither count is a count of independently proved theorems. No baseline or historical file was rewritten during the current packaging.

## 6. Deterministic current execution archive

`ACTUAL_LOCAL_EXECUTION.tar.gz` contains exactly **31 non-PDF files** copied byte for byte from the actual `build/publication-local` execution. Its PDF is supplied once separately as `A2-DYN-manuscript.pdf`. The copied open directory and top-level summary pointers use the same current bytes.

The archive uses sorted USTAR members, fixed file mode 0644, zero owner/group IDs, empty owner/group names, zero archive timestamps, and gzip with an empty filename and zero modification time. Execution timestamps **inside the original receipts are retained unchanged**. Two independent in-memory constructions produced identical compressed bytes. The packaged archive was reopened and every member's content hash compared with its actual execution source. `ACTUAL_LOCAL_EXECUTION.manifest.json` records all 31 member paths, sizes and hashes, the archive identity and the separate PDF identity.

This is deterministic packaging of these actual recorded bytes; rerunning TeX or the verification programs later may produce different timestamps or platform metadata and is not claimed to reproduce the whole archive byte for byte.

## 7. Historical CI and current remote status

The separately retained GitHub evidence reports completed/success for predecessor source run 39712256295 at `9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761` and carrier run 39714539054 at `e84c06c758bed5b2dc09222ad725cfe0ba0d58dd`. Their run/job/artifact identities remain distinct. The API/job-log audit does not claim independent reconstruction of downloaded artifact bytes.

At this packaging snapshot the new branch is **not yet pushed**, its source commit has not been assigned in this record, and its remote CI is **not yet executed**. `PUBLICATION_STATUS.json` intentionally records that scope. A later actual push or workflow receipt must name its real head commit; neither historical success nor this local build may be transferred to an untested commit by assertion.

## 8. Mathematical status preserved by the evidence

The current author proofs retain the full original physical system and inherited fixed-band spectral/arithmetic results. Module 333 is a quantitative reconstruction of the existing section interface. Module 334 supplies the direct exact-interval application and, using native 87, evaluates the fixed-analysis-window scalar comparison and reference modulus; it leaves the complete normalized local derivative charge as a sufficient open physical condition on that route. Module 335 completes the first-image/all-flight endpoint kernel and positive-width critical-coefficient tightness in the norms stated. Native 322's zero-clearance all-flight normalized fan and native 329's deep-clearance normalized payment remain inherited results.

The original same-pool shortage, or a valid sufficient alternative on the complete physical density, still requires a real closing mechanism. Conditional microscopic masses and the local inverse/Jacobian consequences retain their actual hypotheses. No finite check, archive hash, PDF build, visual check or CI success is presented as the missing continuum proof, expert reconstruction or full raw pointwise closure.
