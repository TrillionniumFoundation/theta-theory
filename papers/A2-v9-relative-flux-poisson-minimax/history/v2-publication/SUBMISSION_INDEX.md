# Current A2 submission index

## Current article

`main.tex`: *Geometric stability and curvature identification for uniform collision thresholds* (25 pages).

Theorems 1.1–1.2 give the full-preparation, collision-order-uniform geometric and marked laws. Their new proof is in Sections 9–11. Theorem 12.1 establishes nonredundant contact-curvature recovery in an exact equal-gap family. Section 13 specifies record metrics, smooth response tests and a differentiated moving physical cut. Section 14 compares stationary, variational, inverse and periodic rare-event results. Sources are organized under `v2/` and the retained `sections/`.

## Complete circular specialization

Sections 2–8 of the same article retain the entire former main mathematical development. The original `sections/01_results.tex` through `sections/08_comparison.tex` files are all byte-identical; the current main selects an expanded comparison module. No former theorem or proof has been replaced by a summary. The original main entrypoint is preserved in `history/v1/main.tex`.

## Unchanged companion

`two_collision.tex`: complete regular two-collision response theorem and proof (seven pages), blob `df44402b17031525c087d39dfedf8dac3ada611d`. It is compiled before the main to supply real external references. Its hypotheses and fixed-window regime remain separate from the new uniform geometric hierarchy.

## Historical A2 target

`history/round33_A2.tex`: arithmetic separation and a conditional Fourier-inversion budget, blob `2213344f8efa895b4674f818d404c5d4a9af9da1`. The threshold hierarchy is not a substitute for unrestricted characteristic-function estimates, stable-curve operators or an integrated central Edgeworth remainder. The historical proof is preserved as a distinct programme component, not deleted or promoted to a proved billiard theorem.

## Review and reproduction

Controlling report: `review-basis-uniform-thresholds/REFEREE_REPORT.md`, original blob `d368c50000cbd02d750f4150ab76da5ff269d9e9`, from review commit `14aaea8937f8b2d373bc642f3568d7280dcbbbd7`. The earlier report and response are retained at their prior paths.

Current response: `RESPONSE_TO_REFEREE_V2.md`.  
Current dependencies: `PROOF_LEDGER_V2.md`.  
Current build: `python build.py`.  
Current receipts: `verification-v2/`.  
The intended new branch is `revision/a2-geometric-thresholds-curvature-2026-09-09`.
