# Actual validation of the localized-clearance author revision

This report describes the executed final reconstruction of native 327–332. The complete manuscript and current proof bodies were present before these checks ran. Earlier interrupted preparations and preflight PDFs are retained separately and are not used to certify the current source. All paths are relative to this article unless an original command receipt records its actual absolute working directory.

## Exact source and output identities

| Object | SHA-256 / identity |
|---|---|
| Mathematical/build input manifest, 140 files | `5745a5abe9bb95de6dc64d53d28e018549c41f330b2895fb3382d9019bb8ae55` |
| Shared mathematical source digest in the actual final phase receipts | `cecca59e06fc83d0e3bab89e41e347b6c831c50dd78e7603d63377ca4be4feb0` |
| Native `main.tex` | `251d44ddb3e56b4f88b277ff1f333946b668abaeb2be804e47694f0d48580f6b` |
| Final 255-page native PDF | `60b08184ad7bfa001aae76deb98d99062212cc647723a8e096485e89861df6f5` |
| Actual final LaTeX auxiliary file | `a70b100d598e8757d2ac139760a30d0337a65a5e7070739081bc78371184c56e` |
| Predecessor identity anchor | `ca3d5e4d2204230a21e3e3e6ed8439d5b79484a38a98ff3ab8456db03394ae6c` |

The manifest freezes inputs that affect the mathematical article and its build/check programs. It is distinct from later evidence, explanatory documents, publication receipts and output inventories; no circular self-hash is claimed. The complete Git commit and article tree, once published, identify the whole packet including those records.

## Executed phases

| Phase | Actual result | Retained evidence |
|---|---|---|
| Source preservation and closure | Passed: 5,938 predecessor files / 688,244,624 bytes; 69 unchanged active inherited proof/model inputs; recursive historical preservation gates; all 140 frozen current inputs | `evidence/current-execution/source/` |
| Mathematical auxiliary programs | Passed: 37 programs, 74 real normal/optimized commands, 65 successful comparisons | `evidence/current-execution/math/` |
| Native typesetting | Passed: three real `pdflatex` passes with recorder, actual `pdfinfo`, 255-page PDF | `evidence/current-execution/typeset/` |
| Actual native input closure and proof destinations | Passed: 84 reachable TeX files, all 73 core bodies 260–332, 1,125 unique labels, 807 distinct referenced labels, every label matched to a compiled record and PDF destination | `PROOF_INDEX.json`; `delivery/PROOF_NAVIGATION.md`; delivered-navigation receipt |
| Original historical assembly/build | Passed: original assembler and six real `pdflatex` passes in an isolated copy, producing the retained 26/883-page historical documents | `evidence/current-execution/historical/` |
| Visual inspection | All 255 pages inspected in layout overviews; 34 pages inspected in detail sheets, including all six new proof bodies and the revised introduction/dependency notes | `evidence/current-execution/visual/` |
| New remote exact-SHA CI | No success inferred from any local result; actual state is recorded separately | `PUBLICATION_STATUS.json` and any subsequent publication receipts |

The final mathematics phase used `tools/validate_revision.py math --output .../build/math-final-cli`; the final typeset phase used `typeset --output .../build/typeset-final-norm`. The frozen source phase used `source --output .../evidence/current-execution/source`. Their complete original command arrays, timestamps, exit codes and log hashes are retained. Output copies preserve original receipt paths as provenance of where the commands actually ran. The delivered PDF and auxiliary files were re-indexed at their retained paths after copying; that actual command is in `evidence/current-execution/delivered-proof-navigation.command.json`.

The isolated historical builder ran separately at 23:09 UTC on 21 October 2026. The final mathematics and native typeset completed at approximately 23:19 UTC. The phases share the frozen mathematical identity shown above where applicable. This report does not claim that the literal `bash build.sh` wrapper was run in this already populated workspace. That wrapper is provided for a clean checkout and dedicated CI. The historical repository-wide gate was **not executed**.

## Mathematical checks and what they establish

The 37-program suite executes every listed program twice, once normally and once with `python -O`. All 74 exit statuses were zero. There are 65 comparisons: 61 require byte-identical finite output and four compare mathematical JSON after removing only the declared execution metadata (`executed_utc` and `optimized`). The actual receipts, compared files and comparison decisions are retained. An author-internal read-only gate audit independently re-read those outputs, recomputed their hashes and reconstructed the 37-by-two tag set.

The three new programs contribute the following finite checks per execution:

| New program scope | Checks in each actual run |
|---|---:|
| Native 327–329 geometry, renewal, boundary indexing and normalized union | 1,478,574 |
| Native 330–331 full-label variation, return tail, positive kernel, four-frequency and normalization algebra | 74,071 |
| Native 332 Gauss/endpoint derivatives, tested norm and corrected coefficient scaling | 28,388 |

These counts describe finite exact identities, inequalities, index cases and diagnostic examples. They do not count reconstructed continuous trajectories or independently verified theorems. The native proofs supply the uniform physical-word arguments, singular exhaustion and required order of limits.

The substantive author-internal checks cover:

- The complete last-long renewal sum, including the terminal generation; genuine disjoint initial preimages; a single adapted/Euclidean metric conversion along a complete suffix.
- The actual clearance line-offset derivative, both impact signs, all candidate disks, true first-hit continuation, exact half-counts and incoming terminal Jacobi factor.
- Both terms in the two-half interval overlay, cap Jacobian cancellation before using selected mass, priority at simultaneous boundaries, and positive incoming critical traces.
- The complete singular multiplier with one conditioning factor, the fourth-root selected-interior loss, original guard widths, both geometric depth sums, original `m^2` payment and unchanged outer-limit order.
- Complete-label vector jump costs (two at an interior relabeling, one at an endpoint membership), with no label-cardinality multiplication.
- Conservative tower inequality without an ergodic-saturation premise; full restoration/payment of the removed positive collision tail.
- Positive kernel normalization, second moment, cubic transform, full three-dimensional mark torus and `(2pi)^(-4)` inversion convention.
- Normal and fixed-collision polynomial exponent calculations, arbitrary Borel observation scope, and division only by the actual selected-event denominator.
- The factor `H=e^T G^(-1)e` in the Gauss derivative, the exact `C^1` norm, localized chain derivatives without an artificial inverse-incidence factor, and bounded-label coefficient scaling.

The full dependency ledger identifies the inherited results used by these proofs. This internal reconstruction is neither a new external referee review nor independent human specialist reconstruction of the whole dynamical chain.

## Corrections found during integration

All replaced bytes and actual failed preparations remain under `audit/` and `evidence/preparation/`.

1. **General bounded label coefficients.** The first integrated version of native 332 omitted `sup_l |c_l|` from the translation bound for an arbitrary bounded coefficient family. The final statement and proof include this norm. A step-density scaling example gives a literal counterexample to the omitted-factor statement; six new finite checks retain that diagnostic. The corrected native 332 SHA-256 is `618aaa348f7ebe40cc62a54f26a458ee9863194364b7c84a000046f79a86e16d`. The diagnostic is not represented as a Lorentz trajectory.
2. **Verification command interface.** Two new analytical checkers use `--details` as a flag and accept the destination through `--output PATH`. The driver was corrected to that actual interface. The final 74-command run is after this correction; no failed command was relabeled as successful.
3. **Layout and notation.** Overfull displays in the preflight source were reformatted, a missing spacing command was corrected, and the new endpoint-test constants were distinguished from an inherited constant with a similar name. All old source bytes and real preflight logs/PDFs remain identifiable. The final source has no overfull box.

The relevant records are `audit/integration-proof-correction/`, `audit/integration-layout-correction/`, the three preserved preflight source directories, and `audit/integration-cross-checks/`. Component-stage source hashes and check counts describe their particular stage; the final manifest and final execution packet govern the delivered source.

## Typesetting and navigation

The final recorder's actual native TeX input set equals the declared complete 84-file closure. All core bodies 260–332 are loaded once. The 1,125 source labels have actual compiled records and named PDF destinations; the six new bodies contain 94 labels. Seven LaTeX auxiliary page labels differ from their actual destination page because of page breaking. The generated navigation records both values and uses the actual physical PDF page; it does not silently substitute an old page map.

The final log contains no fatal TeX error, undefined reference, duplicated label, missing font character or overfull box. Two `amsmath` advisories about inherited primitive `\\atopwithdelims` and `\\over` remain visible. They do not indicate a failed compile; unchanged historical proof text was not edited to suppress them.

The visual packet contains 15 actual rendered sheets. Pages 1–255 were rendered at 24 dpi for complete layout overview; pages 1–7, 215–237 and 252–255 at 90 dpi for detailed inspection. The inspected final PDF has no detected clipping, missing page or formula overflow at that stated scope. The overview resolution is not claimed to establish formula-level correctness of every historical page.

## Historical preservation and real rebuild

`CURRENT_SOURCE_ANCHOR.json` records every predecessor path, byte length, SHA-256, Git blob and mode. The reconstructed predecessor tree is exactly `3010c90e2363dfe1808101a3e992eb02643c28f1`. The source gate independently verifies the retained 5,938-file copy, all unchanged active mathematical inputs and the older recursive preservation gates. Original reports, proof bodies, counterexamples and execution records are retained rather than replaced by summaries.

The original 390-file historical source closure was copied to a new isolated build directory and its own assembler was executed. Six actual historical `pdflatex` commands produced:

| Delivered historical file | Bytes | SHA-256 |
|---|---:|---|
| `delivery/historical-main.pdf` | 529,089 | `d3fdacb4a020f165014f8790a184ae6d59aea5b95e48acd603a051b546c15688` |
| `delivery/historical-supplement.pdf` | 5,714,968 | `57b406b6642c94e79193f75c125e4c7820fe2ba4e7c6e46d05040936420e0bf6` |

The historical build summary, original command receipts and logs are retained. That successful rebuild does not make historical conditional or disproved assertions unconditional; their original scientific status remains traceable.

## Remote and mathematical limits

The inherited completed run `39526895726` tested source commit `6708e30d1e8511e6ed2f4e3a6247c09628bd3ea9`. Its artifact was independently reconstructed by 1,333 consistency checks, but it is a predecessor run. It is not the CI of native 327–332. The new workflow is limited to the new A2-DYN branch and article; its actual executed SHA, completion and conclusion require new receipts.

The present proof adds a genuine complete deep-clearance payment and actual-record analytical estimates. It does **not** prove vanishing of the full endpoint/shallow same-roof shortage, abundance of the original comparison pool there, a strong joint spectral/arithmetic expansion with all uniform errors, the required microscopic conditional denominator in every target case, or the final unrestricted raw pointwise/inverse conclusion. Their exact minimal closing statements are retained in the manuscript and proof ledger. No finite count, render, source hash, successful command or CI status is used to assert otherwise.
