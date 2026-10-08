# General Theta Foundations I — restart R7

**Acquired Geometry and Causal Resource Transfer**

Native manuscript: `main.tex`; final PDF is built under `artifacts/General_Theta_Foundations_I_restart_r7.pdf`. The complete retained R6 article is rebuilt as `artifacts/General_Theta_Foundations_I_technical_companion.pdf`. No v96 manuscript was copied into this native article.

The central theorem couples the existing block construction to a new dominated-continuation-cut converse for the same terminal task. Further results prove a matched adaptive acquisition/state law on nonhomogeneous anisotropic binary cylinders, a common erasure/calibration risk law, finite-bit implementation bounds, and the ordinary categorical filtering-loss consequence of the primitive Gaussian certificate. The older nonreset singular realization remains a second direct block-theorem realization, with its complete proof in the companion and its attachment in the native appendix.

Read `REFEREE_RESPONSE.md`, `PROOF_LEDGER.md`, `THEOREM_MAP.md`, `ASSUMPTION_MATRIX.md`, `RESOURCE_ACCOUNTING.md`, `PIPELINE_DERIVATION.md`, `LITERATURE_COMPARISON.md`, `SCOPE_AUDIT.md`, and `HISTORY_COVERAGE.md` before reviewing novelty or coverage. Neither tests nor successful PDF builds establish the mathematical claims. The necessary-and-sufficient classification of all acquired geometries and optimal workspace/program/time region are not asserted.

Build from a checkout containing the unchanged sibling `../r6-operational-transfer`:

```sh
python3 verify.py
python3 regression.py
python3 -O regression.py
SOURCE_COMMIT=$(git rev-parse HEAD) python3 build.py
```

`build.py` performs two isolated three-pass builds of the native article and two of the full retained companion, normal/optimized regressions for both, reference/label/source-inventory checks, and a source-mutation check. It writes only the new subtree's artifacts and receipt. The receipt binds the source SHA and native source tree; a separate artifact commit and subsequent read-only verification are required before referee readiness. Scope is this complete native article and retained R6 companion, not every unrelated paper or historical version in the repository.
