# Execution evidence and limits — A1 v15

`python3 validate.py` executes all tests anew and builds the complete manuscript in three LaTeX passes. The current receipts are in `validation/`; archived v14 descriptions in `history/` are not counted as present execution. An absent or failed receipt must not be interpreted as a successful run.

The expected unchanged author suites are v10: 7,904; v11: 8,207; v12: 26,158; v13: 12,944; v14: 7,400, totaling 62,613. The new v15 circular suite contains 5,868 assertions. The current six-suite total is 68,481. The driver checks result status, exact count, test source hash, output hash, source preservation, PDF build status and source hashes again after execution.

`tests/test_v15.py` uses the Python standard library, exact fractions and Gaussian-rational Laurent arithmetic. It imports no existing author helper. The checks include 72 finite history configurations; exact product evidence and conjugate symmetry; physical repeated-query probabilities; cyclic Fourier orthogonality; normalized acquisition and double attenuation; exact weighted causal updates; 15 finite full-Jacobian configurations and their initial harmonic flags; paired exterior-volume powers; and exact adjacent phase crossings.

The negative controls intentionally omit the update's contrast-squared coefficient (162 detections), the evidence normalization (45 detections), or the acquisition attenuation (3 detections). Their failure is the desired diagnostic outcome. These altered formulas are not formulas asserted by the manuscript.

The sampled Jacobians do not establish uniformity over a contrast interval. That argument uses the central elementary-symmetric Jacobian and a uniform derivative bound in the written proof. The diagnostics do not prove minimax optimality, all-prior assertions, priority, or journal-level significance. All new diagnostics are author-designed, even though they are independent of the older implementation modules.

With a full repository checkout, `python3 validate.py --prior-review` also runs the **unchanged original v14 reviewer script** on **unchanged v14 source**, expecting 21,691 assertions over 60 configurations. This replay checks the predecessor baseline; it is neither a new independent review of v15 nor a test of the circular theorem. Its execution flag and result are recorded separately. The standalone local run need not have the neighboring baseline or review directory.

The source-preservation check compares all 77 complete v14 proof blocks and all 80 complete named statements by byte hash and multiplicity. It is not formal proof verification. The three compiler modules and all v10–v14 test sources also remain byte-identical. The new PDF is built from the current source, not copied from v14. Layout inspection is described separately in `VISUAL_INSPECTION.md`.
