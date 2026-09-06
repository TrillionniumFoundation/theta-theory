# Corrected complete foundation companion (English edition 2.1)

This directory is a complete copy of the 35-blob English-v2 source tree `900059b847980a27be4866d495b00eeb96562dc5`, with the three controlling mathematical scope corrections applied in place. All twenty numbered source sections and all four appendices remain available. The new principal research manuscript, response letter, executed checks and build receipt are in the parent directory.

## Corrections

- `sections/04_selection.tex`, Proposition 4.4: retain bounded bias B and minimize D(Q||P)-QB; identify the bias-free special case explicitly.
- `sections/12_response.tex`, Theorem 12.2: retain both branch density traces and the normalized shape derivative.
- `sections/13_hybrid.tex`, Theorem 13.3: separate trajectory regularity from fixed or transported weighted preparation; retain transport, weight and normalizer derivatives.

`main.tex` identifies the edition and marks the inherited verification appendix as historical. Other mathematical sections, including the complete equilibrium collision-tube proof, are retained from the frozen source. The frozen review directory itself is unchanged.

## Build status

This corrected foundation companion has not been compiled in the current revision execution. Its historical testing/build tools are retained for reproducibility, not claimed as newly run. In particular, neither the old 53-page report nor the old validation files certify this edition. The parent manuscript is independently self-contained and its own actual build receipt records 22 pages and the executed tests.

To compile the companion from this directory: `pdflatex -interaction=nonstopmode -halt-on-error main.tex` (repeat for references). Use the parent `build_and_verify.py` for the new principal manuscript; it deliberately does not claim to build this companion.
