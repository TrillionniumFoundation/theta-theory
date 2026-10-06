# General Theta Foundations I — Revision 83

## Finite-Use Geometry and Learning of Ordered Quantum Measurements

Revision 83 responds to both R52 reports on the exact completed v82 object `57937576a6f413594589d0509a6816ca4ea3a83e`. The reports are frozen verbatim and identified in `CONTROLLING_REPORTS.json`. The four-leading-general-journal objective is retained. The paper's topic and every inherited proof section are preserved.

### New mathematical results

On the complete body `E_j >= 0`, `sum_j E_j = I_d`, define the normalized covariance on zero-sum Hermitian tuples by

```
S_E(K) = sum_j E_j K_j,
(C_E K)_j = (E_j K_j + K_j E_j - E_j S_E(K) - S_E(K)^* E_j)/2.
```

It is positive, polynomial and concave in the measurement. It vanishes identically precisely at projection-valued measurements. With midpoint `M`, difference `H` and `Qcal_N² = N <H,(C_M + Id/N)^(-1)H>`, the new theorem proves

```
D_N(E,F) <= min(2, 2 sqrt(k+1) Qcal_N(E,F))
```

for all integer `d,N >= 1`, `k >= 2`, including zero effects, changing rank, and noncommuting supports. A regularized horizontal-energy identity proves the path bound, and operator concavity gives the midpoint formula. The restriction to two outcomes is exactly twice the squared binary Sylvester modulus. The unregularized dual energy contracts under classical output processing.

Uniform outcome noise of size `epsilon` creates the scale `N/sqrt(1+N epsilon)`. A rotating projective family gives a matching fixed-k lower bound. This is a full-body adaptive **upper** certificate and a sharp crossover on a specified family, not a claimed two-sided classification or entropy theorem on the whole multi-outcome boundary.

The covariance modulus is evaluated by exact rational linear algebra in `(k-1)d²` variables, with the nonorthogonal basis Gram matrix included. A separate guarded affine repair

```
A_j = B_j + (I - sum_i B_i)/k,
L_a(B)_j = (A_j + 4a I)/(1+4ka)
```

legalizes balanced component estimates with error at most `4a`. This gives polynomial-bit legalization with no grid enumeration, preserving the joint fixed-k learning and description orders. Public dictionaries and general collective-readout synthesis remain separate, potentially exhaustive resources.

### Article organization

The quantitative article now starts with finite-outcome geometry, coding and learning, followed by the closed-body covariance and affine repair. Its front matter includes theorem-level Mele–Bittel and Zambrano–Ramos-Calderer–Kueng substitutions with an explicit legality step. The complete binary prerequisite graph follows in appendices. The structural article remains independent and unchanged. The complete research edition retains its entire existing structure and adds the new proofs.

| Entry | Role |
|---|---|
| `quantitative.tex` / `paper.pdf` | Primary article, finite-outcome first with full binary appendices |
| `structural.tex` / `STRUCTURAL_PAPER.pdf` | Unchanged, independently complete structural companion |
| `main.tex` / `COMPLETE_REVISION.pdf` | Complete mathematical preservation edition |
| `sections/67-coupled-boundary-covariance.tex` | Closed-body covariance, horizontal energy, noise crossover, exact evaluation |
| `sections/68-affine-legalization.tex` | Polynomial guarded legalization and retained learning orders |
| `RESPONSE_TO_REFEREE.md` | All 15 required revisions, 30 detailed comments, 24 gates and 10 risks |
| `PROOF_AUDIT.md` / `PROOF_STATUS.json` | Proof dependencies, exact hypotheses and evidentiary boundaries |
| `COVARIANCE_SCHEMA.md` | Exact evaluator and verification contract |
| `evidence/BUILD_RECEIPT.json` | Actual native-source qualification, fresh regressions and page reconstruction |
| `evidence/JOURNAL_PACKAGE.zip` | Self-contained quantitative and structural source graphs |
| `evidence/RESEARCH_PACKAGE.zip` | Full native corpus, three PDFs and verification evidence |

### Reproduction

```sh
python build_revision.py --check-source
python covariance_check.py
python covariance_metric.py examples/covariance-noncommuting.json --horizon 3 > pair-certificate.json
python covariance_metric.py examples/covariance-noncommuting.json --horizon 3 --verify pair-certificate.json
python build_revision.py --isolated          # actual committed native source
python build_revision.py --verify-published # exact publication or metadata-only final head
```

`--preflight` checks uncommitted sources without qualifying publication. The production builder runs all 20 inherited suites again plus the new covariance/repair suite under ordinary and optimized Python. The new suite has 140 positive checks and 17 negative controls, covering exact noncommuting identities, singular cases, binary reduction, Gram-matrix accounting, noisy limits, scalar product laws, and guarded repair. Finite checks are not proofs of continuum theorems. No general physical learner is represented as executed.

The source baseline has 465 native files and 827/329/116 complete/quantitative/structural labels. Every predecessor mathematical section is byte-identical and remains active in its original edition. The reordered introduction's labels remain active in the quantitative guide appendix. Changed entry, audit and build files have exact original copies under `predecessor-v82-audit/`. All previous revision directories and all review branches remain unchanged.

Independent human specialist priority clearance is not supplied by this author-side revision or by CI. Growing-k minimax sharpness, a matching full-boundary multi-outcome entropy theory, and general efficient dictionary/readout synthesis remain separate questions. The five independent A/B/C/D aggregate flags remain false. Current publication and exact-head receipts, not earlier revision evidence, establish this revision's execution status.
