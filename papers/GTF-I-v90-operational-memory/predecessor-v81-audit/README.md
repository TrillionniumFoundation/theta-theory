# General Theta Foundations I — Revision 81

This is the complete successor to published v80, responding to the latest deposited R51 reports on v77. The primary article remains **Finite-Use Geometry and Learning of Ordered Binary Quantum Measurements**. Its full-body geometry, boundary entropy, common learner, exact codes, joint interior learning laws and structural companion are retained.

## New result: finite rational risk certificates

`sections/64-finite-risk-certificates.tex` constructs Gaussian-rational collective readouts with an exactly checkable finite certificate. The proved parameter net and normalized Choi-record Lipschitz estimate transfer the certificate to every real effect in `I/4 <= E <= 3I/4`. A prescribed denominator and exhaustive finite search at successive dyadic query counts guarantee termination at the existing joint optimal call order:

\[
 M=O\!\left(N\delta^{-2}[d^2+d\log(1/\eta)]\right),\qquad
 B=(d^2/2)\log_2N+d^2\log_2(1/\delta)+O(d^2).
\]

The theorem takes integer `d,N>=1`, rational `0<delta<=2^-13`, and rational `0<eta<=1/8`. The calls are independent one-call Choi acquisitions; coherent processing uses only completed outputs. Finite trusted-control specifications preserve the original future-loss risk and confidence. All constants in these orders are absolute. The inherited lower bounds match both resource orders under their stated decoder conventions.

For a fixed readout, checking radius `a`, failure `alpha` on a proved `r`-net gives radius `a+r`, failure `alpha+m r` on the continuous target family. The proof accounts separately for the moving success labels, complete POVM legality, Gaussian-rational rounding, and probability error. Finite checks do not replace this analytic transfer.

## Reading and reconstruction

| Entry | Object |
| --- | --- |
| `quantitative.tex` / `paper.pdf` | Primary focused mathematical article |
| `structural.tex` / `STRUCTURAL_PAPER.pdf` | Independently complete structural companion |
| `main.tex` / `COMPLETE_REVISION.pdf` | Entire retained mathematical development |
| `RESPONSE_TO_REFEREE.md` | All 12 required revisions, 26 detailed comments, 32 pipeline gates and 10 risks |
| `FINITE_RISK_PROOF_AUDIT.md` | New soundness, rationalization, termination and control proofs |
| `FINITE_RISK_SCHEMA.md` | Exact finite-certificate replay contract |
| `evidence/JOURNAL_PACKAGE.zip` | Both standalone article source graphs and submission materials |
| `evidence/RESEARCH_PACKAGE.zip` | Full native source, articles and core execution evidence |

Run `python build_revision.py --check-source` to check preservation and active inputs. Production from a committed native source uses `python build_revision.py --isolated`; the final committed publication is verified read-only with `python build_revision.py --verify-published`. The finite replay suite is `python finite_risk_check.py` and also runs under optimized Python.

The explicit search and certificate dimensions can be very large. Training calls, reusable index bits, raw readout storage, verification work and trusted realization costs remain separately accounted. The finite implementation exercises described in the evidence do not claim execution of the general optimal learner. The external human priority task remains available in the specialist brief. The source pins, report recommendation and full historical pipeline are preserved.
