# CM2 Round261 Adaptive Common-Face Strict Separation

Round261 applies a breadth-first dyadic quadtree to all 5,120 Round260 residual faces. Each region/cell is classified as `MATCH`, `EXCLUDE`, or `UNRESOLVED`; strict opposite-sign `EXCLUDE` cells are permanently pruned.

- Accepted strict common-face patches: 3,280 (`3,056` Round208, `224` Round204).
- Strict-separation trees exhausted: 224 (`32` Round208, `192` Round204). These have no positive-area common patch and receive zero glue.
- Remaining fail-closed after depth 8: 1,616 (`1,528` Round208, `88` Round204), containing 182,072 unresolved depth-8 cells.
- All accepted patches have exact positive area and explicit strict 3D corridors on both sides; normal depth is at most 25.
- Exact patch-area sum: `186865401/53687091200000`.
- Exact two-sided corridor-volume sum: `8464695485090211/1844674407370955161600000`.
- Accepted evidence covers 224 external component pairs: 128 rank reductions and 96 redundant certified physical edges.
- Exact-key-pure quotient: `68,876 → 68,748`; all 53,968 occurrence rows and 116 key rows are rebuilt.

The independent verifier recomputes all 3,066,244 cell-side classifications with pinned Round204/208 verifier evaluator chains and does not import or execute the producer. Status is `PASS_INDEPENDENT_ROUND261`. Seeds `261071` and `261929` are byte-identical.

No maximality, fibre-exhaustion, global-disposition, Gate5, or CM2 promotion is issued. Gate5 remains `10/18`; CM2 remains `NO-GO_FOR_CLAIM`.

Next: continue adaptive refinement of the 1,528 Round208 and 88 Round204 depth-8 residuals, then audit pinned cross-chart transitions.
