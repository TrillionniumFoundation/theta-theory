# General Theta Foundations I — Revision 85

## Finite-Use Geometry and Learning of Ordered Quantum Measurements

This is a new R54 response on the exact completed v84 head `9ee14476f539a38f2f45f9bd4ed99a658a7eb14d`. Both controlling reports are frozen verbatim. The four-leading-general-journal objective, the topic, and every inherited mathematical section are retained. The primary remains separate from its complete binary supplement, independent structural article, and historical preservation edition.

## New theorem: smooth curves through the measurement boundary

Let `E(t)` be any fixed two-sided `C²` curve of ordered measurements, `E=E(0)`, and `H=E'(0) != 0`. No constant-rank or smooth exact Kraus-factor assumption is imposed. With support projections `P_j`, define

```
Gamma_E(H) = (i/2) sum_j [P_j,H_j],
W_E = sum_j P_j H_d P_j.
```

Theorem `thm:curveclassification85` proves, for every integer `N>=1` and all sufficiently small two-sided `t`,

```
D_N(E,E(t)) ~ min(1,sqrt(N)|t|)   if Gamma_E(H) belongs to W_E,
D_N(E,E(t)) ~ min(1,N|t|)         otherwise.
```

Both comparison constants and the angle interval belong to the fixed curve. The square-root lower is a repeated product-input experiment. The linear lower uses a known-pair logical-qubit code and recovery on the actual classical label and a retained reference of dimension at most `2d` per call. It does not turn a pair-specific code into a common unknown-device learner.

The proof constructs a normalized horizontal *surrogate* with the same first derivative, then budgets its `O(Nt²)` deviation from the actual curve. For the linear branch, a normalized first-order Kraus realization identifies the corrected logical derivative `-i[Gamma_L,.]` without factoring the actual rank-changing curve. The exact one-cycle remainder is at most `kappa t²`, with `kappa=L/2+2||Gamma||op²` and a stated effect-curvature bound `L`. A projective binary measurement opening to full rank at every nonzero angle illustrates a case beyond fixed unitary orbits.

A zero first derivative is not classified as stationarity. One-sided rank openings and uniform arbitrary-pair midpoint equivalence are different questions. The established metrological exponents and error-correction principle are credited to Zhou–Jiang and Knill–Laflamme. The submitted addition is the direct finite-pair support-coordinate proof for general two-sided `C²` effect curves and its finite error accounting.

## Certified controls and exact first-order decisions

Theorem `thm:controlstability85` gives the achieved classical separation with certified preparation, encoding, recovery and readout errors:

```
2 |sin(m t Delta/2)| - m kappa t² - 2e_0 - 2e_f - 2 sum_r nu_r,
```

truncated below at zero. All channel errors are uniform unhalved diamond bounds under both hypotheses. At the specified call number, `nu_r<=|t|Delta/(8pi)` and `e_0+e_f<=min(1,N|t|Delta)/(16pi)` suffice to preserve a positive constant fraction of the linear scale. This is a conditional robustness theorem, not a gate-synthesis or hardware certificate.

`curve_geometry.py` decides exact first-order realizability and the support branch on Gaussian-rational input. It checks every missing-support block `Q_j H_j Q_j=0`, computes the support generator and its Hilbert–Schmidt projection, and rejects incomplete or tampered certificates. The prescribed normalized-factor construction proves that these first-order conditions are also sufficient. The procedure does not infer curvature bounds or synthesize the recovery.

## Review and reproducibility entry points

| File | Role |
|---|---|
| `quantitative.tex` / `paper.pdf` | Primary article, including the complete finite Bernoulli premise and new curve/control proofs |
| `supplement.tex` / `BINARY_SUPPLEMENT.pdf` | Complete inherited binary boundary, learning, coding and control corpus |
| `structural.tex` / `STRUCTURAL_PAPER.pdf` | Independent unchanged structural proof graph |
| `main.tex` / `COMPLETE_REVISION.pdf` | Entire preserved mathematical development |
| `sections/72-finite-product-prerequisite.tex` | Self-contained finite Bernoulli product lower |
| `sections/73-smooth-boundary-curves.tex` | Support generator, first-order realizability, smooth-curve theorem, rank-opening example |
| `sections/74-certified-control-stability.tex` | Implemented-control error ledger and exact first-order decision |
| `RESPONSE_TO_REFEREE.md` | R01–R15, D01–D30, all 42 pipeline gates and 14 risks |
| `PROOF_AUDIT.md` / `CURVE_SCHEMA.md` | Proof dependencies and exact executable scope |
| `LITERATURE_AUDIT.md` / `LITERATURE_RETRIEVAL.json` | Current full-text covariant-learning comparison and retrieval identity |
| `evidence/BUILD_RECEIPT.json` | This revision's actual source, four PDFs, tests and reconstruction |

The main article now identifies precisely which results import a supplement theorem. The support/orbit/smooth-curve classification has its probability, covariance and correction premises in the primary. The learning consequences still use the explicitly linked current binary supplement.

The full text of Yoshida–Okigami–Posta–Grinko, arXiv:2609.39280v1, was retrieved and read. The current comparison distinguishes invariant-state and covariant-channel parameter dimensions, the two one-use losses, parallel-query bounds, nonmatching general diamond accuracy exponents, and the specialized Hayashi gate construction. No independent human priority judgment is inferred from this author-side comparison.

```sh
python build_revision.py --check-source
python curve_check.py
python curve_geometry.py examples/curve-rank-opening.json > curve-certificate.json
python curve_geometry.py examples/curve-rank-opening.json --verify curve-certificate.json
python build_revision.py --preflight       # not publication qualification
python build_revision.py --isolated        # from an actual native-source Git commit
python build_revision.py --verify-published
```

All 22 inherited suites run anew, followed by the curve suite, under ordinary and optimized Python. The new suite contains 313 positive checks, 17 negative controls, 150 exact finite Bernoulli cases and 20 unitary specializations. These checks do not establish continuum theorems or physical execution.

The v84 baseline has 529 native files and 891 complete-edition labels; its quantitative primary and supplement have 402 labels jointly, and its structural article 116. Every inherited mathematical section remains byte-identical and active in its previous edition. Changed entry/audit/build files have exact originals under `predecessor-v84-audit/`. Earlier directories and review branches are untouched. Source qualification, publication and final-head reconstruction use new v85 receipts. Independent human priority, arbitrary-pair full-boundary equivalence/entropy, growing-outcome minimax, general efficient recovery/dictionary/readout synthesis and the independent A/B/C/D aggregate programme are not claimed complete.
