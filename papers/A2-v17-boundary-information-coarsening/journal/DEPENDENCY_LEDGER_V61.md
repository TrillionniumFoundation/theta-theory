# A2 v61 — dependency declaration

The theorem/proof inputs and classifications in `DEPENDENCY_LEDGER_V60.md` remain unchanged. Revision 61 adds no theorem and changes no proof dependency. That retained ledger is the detailed declaration for the proof corpus; the present note records the one expository input replacement.

`rigidity.tex` now reads `journal/00_principal_introduction_v61.tex` instead of `journal/00_principal_introduction_v56.tex`. All mathematical environments of the former principal introduction are present verbatim in the revised text, and the old file remains in the source tree. The added prose points to existing results: the relative factorization, the actual-smooth finite-jet factorization, the complete analytic inverse, conditional inner-disc real-observation stability, the fixed-order finite-flight inverse, and the realized leading-data comparison. It introduces no new premise for the principal theorems.

In particular, Corollary `cor:v45-physical-chart` continues to import full Theorem `thm:v25-global-physical-reconstruction` (F.47.3) substantively, including its analytic-family, chart, sensor, calibration and charged-preparation requirements. It is not reclassified as a comparison. The application is not used in the local relative theorem or the principal exact global theorems. The conditional contact estimate is not promoted into global registration, noisy unknown-origin calibration or a uniform acquisition theorem.

The source-preservation checker validates the explicit input replacement and unchanged proof modules. This declaration is reading-based; a syntax check is not a proof of complete semantic dependency closure. Statement numbers are unchanged; page numbers may move with the revised introduction.
