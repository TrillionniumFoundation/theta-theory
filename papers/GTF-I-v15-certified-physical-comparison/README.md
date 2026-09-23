# General Theta Foundations I — v15

**Intrinsic Causal Deficiency and Physical Certification**

This revision addresses the independent v14-r2 report at `5c855fde40aa40bb3d79e7473b2a78a54e4e3d9f`. Its principal result is a same-budget certified interval for the original physical intrinsic deficiency, joining analytic approximation, actual report quantization, coherent rational marked trees and finite nonconvex testing. A constructive collision-chart graph core verifies the effective inputs for fixed-particle hard spheres with algebraic kicks and bounded computable data. Exact physical examples and task/witness bounds supplement this theorem. All v14 canonical mathematics and earlier complete development are retained.

## Manuscripts and review documents

- `paper.pdf` / `main.tex`: canonical full English article.
- `complete-development.pdf` / `development.tex`: same article plus all preserved predecessor mathematical bodies and historical introductions.
- `RESPONSE_TO_REFEREE.md`: E14-R2.1–E14-R2.8 and comments 14.1–14.8.
- `PROOF_LEDGER.md`: explicit hypotheses and proof locations.
- `HISTORY_AUDIT.md`, `PIPELINE_GRAPH.json`, `REPOSITORY_SNAPSHOT.json`: separately typed mathematical dependencies and frozen source observations.
- `PRESERVATION_DIFF.md`: exact inclusion/preservation policy.
- `LITERATURE_COMPARISON.md`: classical subtraction and the explicitly uncompleted Norberg/Paull–Unger full-text audit.

The new work is on `revision/general-theta-foundations-i-v15-certified-physical-comparison-2026-09-23`. The root referee entry will identify the final frozen branch, actual source build commit, publication commit and artifact. It must not be inferred from a version name alone.

## Reproduce

From the repository root, with all pinned inherited sources present:

```sh
python -m pip install -r papers/GTF-I-v15-certified-physical-comparison/requirements.txt
# Debian/Ubuntu: texlive-latex-extra texlive-fonts-recommended lmodern poppler-utils
OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 python papers/GTF-I-v15-certified-physical-comparison/build.py
```

`evidence/BUILD_RECEIPT.json` identifies the checkout actually built. `evidence/COMPILED_SOURCES.zip` contains all required pinned inputs, with no font files. A standalone source-archive rebuild is identified as such rather than assigned an invented commit. A later rebuild does not change the source identity of previously published PDFs.

The new exact examples can be reproduced by:

```sh
python papers/GTF-I-v15-certified-physical-comparison/certified_data.py --output /tmp/gtf-physical-data.json
python papers/GTF-I-v15-certified-physical-comparison/verify.py
python -O papers/GTF-I-v15-certified-physical-comparison/verify.py
```

The program computes exact finite rationalizations, the physical sign-table certificate through the unchanged v14 independent checker, and the nonzero analytic Gram constants. It does **not** implement general collision-chart exhaustion, arbitrary physical quadrature or real quantifier elimination. Those general constructions are mathematical algorithms proved in the manuscript, not misrepresented software features.

The general theorem is fixed-horizon, fixed-particle and input-effective where effectiveness is claimed. The historical nonlinear action-sublevel/Boltzmann–Grad target is preserved but not claimed solved by the new L2 certificate. No independent referee endorsement, formal proof certification or journal acceptance is asserted.
