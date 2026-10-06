# General Theta Foundations I — Revision 86

## Finite-Use Geometry and Learning of Ordered Quantum Measurements

This revision responds to the R55 reports on exact completed v85 `ca39533970c77a156cafe916ee6287c54c91fa00`. Both reports are frozen verbatim. The general mathematics journal objective and the complete prior mathematical corpus are retained.

### Finite neighborhoods, not only fixed curves

Fix a legal measurement E, a nonzero Hermitian zero-sum direction H, and a finite remainder bound Lambda. Write P_j=supp(E_j), Q_j=I−P_j and J_j=Q_j H_j Q_j. The exact one-sided tangent cone is J_j>=0. It is realized by a normalized rational matrix curve, including singular opening blocks and noncommuting cross-support terms. The complete covariance range is characterized by J_j=0 for every j together with Gamma_E(H)=(i/2)sum_j[P_j,H_j] in the real support span W_E.

The main finite-pair theorem holds for **every** legal F with

```
sum_j ||F_j-E_j-sH_j||op <= Lambda s^2.
```

For fixed E,H,Lambda, uniformly over this entire finite neighborhood, every integer N>=1, and every sufficiently small s>0, the adaptive order is `min(1,sqrt(N)s)` in the covariance range and `min(1,Ns)` otherwise. Constants and the interval are not uniform over base measurements or directions. No curve or smooth factorization of F is assumed.

The independent-product theorem separates three mechanisms:

| First-order geometry | Independent product probes | Arbitrary coherent adaptive tester |
|---|---|---|
| All J_j=0, Gamma in W_E | min(1,sqrt(N)s) | min(1,sqrt(N)s) |
| All J_j=0, Gamma outside W_E | min(1,sqrt(N)s) | min(1,Ns) |
| Some J_j nonzero | min(1,Ns) | min(1,Ns) |

The product class has one probe–reference pair per call, no entanglement between pairs and no feedback into later inputs; arbitrary collective final readout is allowed. It is **not** the class of all entangled parallel testers. The third row is witnessed by an output impossible at the base and therefore needs no coherent recovery. The second uses the known-pair code and actual-label/reference recovery. Established metrological and fidelity ingredients are credited in the theorem discussions.

### Higher-order and computational consequences

One-sided C2 curves with nonzero right derivative are included. So are families `E+t^q H+O(t^(2q))`, with fixed H nonzero. For the exact scalar family `((1-t^b)(1/2+t^a),(1-t^b)(1/2-t^a),t^b)`, relative to `(1/2,1/2,0)` and `1<=a<b<2a`, the proved order is `min(1,sqrt(N)t^a+Nt^b)`. This accounts for an intervening opening that is not covered by the quadratic-remainder corollary. A zero first jet alone remains undetermined.

A polynomial exact certificate checks one-sided realizability, its mechanism, and a supplied pair's componentwise rational remainder allowances. A nonzero opening yields an exact rational witness probability and its finite repeated-event bound. This does not compute the neighborhood interval, curvature of an unspecified curve, general recovery, or optimal adaptive distance. The conditional control ledger uses `kappa=Lambda+2||Gamma||op^2` and retains angle-dependent diamond budgets.

### Reading and reconstruction

| Entry | Role |
|---|---|
| `quantitative.tex` / `paper.pdf` | Journal-facing article, including the new finite-neighborhood and acquisition theorems |
| `supplement.tex` / `BINARY_SUPPLEMENT.pdf` | Complete current binary boundary, learning, coding and auxiliary proofs |
| `structural.tex` / `STRUCTURAL_PAPER.pdf` | Independently complete, unchanged structural proof graph |
| `main.tex` / `COMPLETE_REVISION.pdf` | Entire preserved mathematical development |
| `sections/75-one-sided-tangent-neighborhoods.tex` | Exact cone, all-input channel norm, finite-neighborhood dichotomy, one-sided curves and controls |
| `sections/76-independent-probes-and-higher-jets.tex` | Independent-product converse, higher-order and mixed-rate results, exact decision |
| `RESPONSE_TO_REFEREE.md` | All 15 required items, 8 minor comments, 42 pipeline gates and 16 risks |
| `PROOF_AUDIT.md` / `CONE_SCHEMA.md` | Written proof checks and exact executable boundary |
| `evidence/BUILD_RECEIPT.json` | Actual new native source, four PDFs, fresh tests and reconstruction |

```sh
python build_revision.py --check-source
python cone_check.py
python cone_geometry.py examples/cone-opening-pair.json > cone-certificate.json
python cone_geometry.py examples/cone-opening-pair.json --verify cone-certificate.json
python build_revision.py --preflight       # local checks, not source qualification
python build_revision.py --isolated        # actual committed native source only
python build_revision.py --verify-published
```

All 23 prior suites run anew, plus the cone/neighborhood suite, under ordinary and optimized Python. The new suite has 353 positive checks and 27 negative controls, including 56 complete finite classical laws and 8 direct full-covariance range checks. Finite checks do not prove continuum statements or execute a physical learner.

The baseline has 565 native files, 912 complete labels, 423 primary/supplement labels jointly and 116 structural labels. No inherited proof text is deleted. All original mathematical sections remain active; two sections receive editorial insertions specifying curvature and channel-norm conventions. `EDITORIAL_INSERTIONS.json` permits exact removal to restore the original section hashes. All other predecessor sections are byte-identical. Exact originals of changed files are retained in `predecessor-v85-audit/`.

The one-sided result does not reclassify the old two-sided theorem's hypotheses. Arbitrary-pair midpoint equivalence, complete-boundary entropy and common learning, growing-k minimax, unrestricted higher-order jets and efficient general dictionary/recovery synthesis remain separate questions. Independent human priority and physical execution are not claimed; the five independent A/B/C/D aggregate flags remain false. New receipts, not v85 successes, establish this revision's execution status.
