# General Theta Foundations I — Revision 87

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

This revision responds to the R56 external report and proof/pipeline audit on exact v86 head `0a7d65923c12334ecc60ec42084bdd0c612e2e49`. Both are frozen verbatim with source identities in `CONTROLLING_REPORTS.json`. The general-mathematics journal objective is retained. The title now foregrounds discrimination; the measurement topic, all prior mathematical sections, binary supplement, learning consequences, structural article and complete archival edition are preserved.

### Main result: the missing parallel class and a uniform block-width law

Fix a measurement E, a nonzero one-sided direction H, and a finite remainder allowance Lambda. Write `||R||_Sigma=sum_j||R_j||op` and admit every legal F satisfying `||F-E-sH||_Sigma<=Lambda s²`. Let each independent probe–reference group use at most b calls, with arbitrary entanglement within that group, no input feedback, arbitrary final joint readout, and public mixtures. For all integers `1<=b<=N`, the new theorem gives:

| Direction | Block-b separation | Entangled parallel and adaptive separation |
|---|---|---|
| H in the covariance range | `min(1,sqrt(N)s)` | `min(1,sqrt(N)s)` |
| All missing-support blocks zero, support generator outside the support span | `min(1,sqrt(Nb)s)` | `min(1,Ns)` |
| Some positive missing-support block nonzero | `min(1,Ns)` | `min(1,Ns)` |

Both bounds and the small scale interval depend only on fixed E,H,Lambda, not on b,N or the permitted remainder. Setting b=N proves that entangled parallel acquisition has the same local order as adaptive acquisition. This is not equality of exact distances, perfect-discrimination thresholds, or fixed-pair asymptotic error exponents. The independent-product converse remains restricted to its original class.

The new upper uses a finite Bures bound for each entangled block and multiplies fidelities only between independent blocks. The lower prepares corrected logical GHZ blocks before any device call and recovers only after acquisition. Tensor telescoping retains the full `m kappa s²` remainder. A fixed binary readout, independent blocks and the finite Bernoulli lemma prove the sharp `sqrt(Nb)s` scale uniformly also when b grows.

### Nonempty neighborhoods

With `a>=max||H_j||op`, `E_j>=lambda P_j`, `a,lambda>0`, set `c=1+2a²/lambda`, `s*=min(1,lambda/(2a),1/a)` and `Lambda*=ck(1+2k)`. Then `(E_j+sH_j+cs²I)/(1+kcs²)` is legal throughout `[0,s*]` and has Sigma remainder at most `Lambda*s²`. Thus Lambda at least Lambda* guarantees nonemptiness for every small positive scale. The allowance is sufficient, not minimal; smaller allowances are not automatically infeasible. The rational-input executable constructs and checks these constants exactly. Its interval controls the explicit realization, not the discrimination theorem's small interval.

### Reading and reconstruction

| File | Role |
|---|---|
| `quantitative.tex` / `paper.pdf` | Primary discrimination article with the new block theorem and explicit nonemptiness |
| `supplement.tex` / `BINARY_SUPPLEMENT.pdf` | Complete retained binary foundation and learning prerequisites |
| `structural.tex` / `STRUCTURAL_PAPER.pdf` | Independent unchanged structural article |
| `main.tex` / `COMPLETE_REVISION.pdf` | Complete retained mathematical corpus |
| `sections/77-nonempty-tangent-neighborhoods.tex` | Constructive allowance and exact polynomial certificate |
| `sections/78-entanglement-width.tex` | Block upper, parallel corrected lower, width law and parallel/adaptive order comparison |
| `RESPONSE_TO_REFEREE.md` | All 15 requirements, 20 detailed comments, 28 gates and 16 risks |
| `PROOF_AUDIT.md` / `BLOCK_SCHEMA.md` | Proof constants, resource distinctions and exact executable scope |
| `evidence/BUILD_RECEIPT.json` | Fresh native-source qualification, PDFs and reconstruction |

```sh
python build_revision.py --check-source
python block_check.py
python block_geometry.py examples/entanglement-width-projective.json > certificate.json
python block_geometry.py examples/entanglement-width-projective.json --verify certificate.json
python build_revision.py --preflight        # no publication qualification
python build_revision.py --isolated         # from the committed native source
python build_revision.py --verify-published # exact publication or metadata-only final head
```

All 24 inherited suites execute again, plus the new suite, under ordinary and optimized Python. The new suite has 591 positive checks and 21 rejection controls, with 12 complete entangled parallel probability laws (one to four calls), exact nonemptiness checks, and integer block plans. These are exact finite regressions, not continuum proofs or physical execution.

The v86 baseline has 600 native files, 941 complete-edition labels, 452 primary/supplement labels jointly and 116 structural labels. All predecessor mathematical sections are byte-identical to v86 and remain active. The prior insertion registry is retained as historical evidence; v87 introduces no further edits to those sections. Changed entry/audit/build files have exact originals in `predecessor-v86-audit/`. Earlier directories and review branches are unchanged.

Independent human priority, global arbitrary-pair midpoint equivalence, complete multi-outcome boundary entropy and common learning, unrestricted higher-order approaches, growing-k minimax sharpness and efficient general quantum-control/dictionary synthesis are not claimed complete. The known cone, GHZ, fidelity and metrological mechanisms are credited. The independent A/B/C/D aggregate flags remain false.
