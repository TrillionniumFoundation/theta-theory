# A1 v36 — revision and proof-preservation ledger

**Basis:** v35 manuscript `02a19f2ddb83cf68bfbf8361c137613e2ffd3925`; v35 independent report `30ea5daf9c1f5cf345061f940b55bd559e2e1686`.

## Local mathematical dependencies

R35.1 uses the normalization condition in `v35/introduction.tex` and the original detector square and two-trial exponent list in `text/collision_consequences.tex`. On that unchanged square, the maximum one-step exponent is 49/16. Multiplication by the largest of the three horizons gives 245/16 < 16. Consequently the common choice H = 16 is allowed for horizons 3, 4 and 5. The two-trial formal node list divided by 16, together with a single fixed L >= 8, defines literally the same Fourier matrix. The acquired cutoffs and risk laws are then exactly those of the existing Corollary 13.3. Its old argument is preserved after the added admissibility calculation.

R35.2 uses only the envelope in the inherited two-parameter corollary and the flat-path substitutions in the existing Remark 13.4. Balancing the first two terms gives rho^(-6); balancing the last two gives rho^2*tau^(-8). The local sentence identifies these as envelope comparison orders, not an exact optimizer partition. It adds no hypothesis to the path-free determinant theorem.

## Unchanged proof architecture

The exact-information and acquired-tangent sources remain `text/exact_information.tex` and `core/03_transversality.tex`. Positive pairings and global-covering inputs remain in `text/analytic_inputs.tex`; acquired confluent flags and their actual command-and-report mass remain in `text/collision_flags.tex`. The checkpoint and one-common-filter proofs remain in `text/collision_direct.tex`, with the principal theorem in `text/main_classification.tex` and the memory consequences in `text/collision_consequences.tex`.

The full finite-cell realization module remains `v35/moment_controllers.tex`. The complete compatibility, precision and exact-instance proofs remain the selected `v33/` sources. The entire companion and its structural, exact-kernel, uncertainty, effective, graph, occupation and regenerative developments are unchanged. Their distinct hypotheses and resources are not imported into the main theorem with stronger quantifiers.

This revision checks the report and the affected historical arguments; it does not claim a fresh line-by-line proof audit of every companion result or every paper in the program. Whole-source preservation is checked separately from analytical review.

## Source preservation

The new native repository directory is constructed from the entire v35 native tree, so inactive historical sources remain present. The new main selects `v36/comparison.tex`, which differs from `v35/comparison.tex` only in its input of `v36/spectral_comparison.tex`. The latter contains the two local clarifications and explicit normalization calculation. The old modules remain untouched. Entry points and metadata replaced in the new directory have v35 copies under `history/`.

There are 80 active TeX inputs, 222 theorem-like blocks and 210 proof blocks before and after revision. There are 220 verbatim statement blocks and 209 verbatim proof blocks. The two extended statements have labels `cor:v35-fixed-future` and `rem:v35-flat-path`; the one extended proof belongs to the former. All original conclusions, all equation labels and all original proof text remain. The supplied companion and the current companion have identical text on all 159 pages.

## Verification artifacts

`verification-v36/PRESERVATION.json` records the source comparison. `NATIVE_BUILD_V36.json` records the current full native build and reconstructible source hashes; `BUILD_RECEIPT.json` in the downloadable review package retains the full input list and logs. `EXECUTION_RECORD.json` records ordinary and optimized runs of the new exact clarification checker and three inherited regression programs. `VISUAL_INSPECTION.json` specifies sampled pages and render hashes. None of these records is a proof-assistant certificate or a journal decision.
