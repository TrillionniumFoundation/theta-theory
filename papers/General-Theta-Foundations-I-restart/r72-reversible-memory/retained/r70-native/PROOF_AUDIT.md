# Author proof audit — R70

This is an author-side audit, not an external referee report. All valid R69 and earlier proofs remain inherited; accepted closures are not reopened for appearance. The original title and research target remain unchanged.

| Statement | Load-bearing proof | Quantifiers and boundaries | Audit status |
|---|---|---|---|
| `lem:r70-core` | Positive initial and output paths bound every active matrix entry by the actual decaying response; a stochastic recurrent remainder must exist | Nonzero response, limit zero, pure initial label, decoder in [0,1]; initial output itself may be zero | Full proof; exact core and degeneracy checks |
| `prop:r70-relative-spectrum` | A visible rational pole lies in one irreducible active block; Perron normalization there plus stationary-row mixing changes its modulus to the actual decay scale | Not a global scaling of a reducible matrix; invisible states cannot set a false decay rate | Full proof; explicit negative control for global scaling |
| `thm:r70-leakage` | Relative spectral necessity + killed minimal unattenuated construction | Nonreal phase, positive contrast and internal retention, strict positive leakage survival; exact extra live state | Matching lower and upper, including infinite case |
| `cor:r70-rates` | Substitute the exact increment into inherited R69 rates | Old fixed-phase arithmetic condition is retained; not assumed for (3+4i)/5 | Inherited rates transported, not new spectral theorem |
| `thm:r70-physical` | Explicit CP trace-preserving mixture; trace contraction from Jordan decomposition; raw protected-block recurrence | Hidden sink, not observer input; infinite-memory claim specifically at irrational internally undamped phase | Full physical proof and raw Kraus/audit diagnostics |
| `thm:r70-finite-tests` | Known denominator orders give cross-polynomial degree <=M+r-1; M+r zeros force identity | Tests only M-label candidates; finite family grows with M; no finite-data inference for arbitrary full-history kernels | Full proof; exact interpolation and negative control |
| Algebraic fixed-M gap | Compact stochastic controller space; no exact equality; polynomial resolvent graph | General elimination is proved, not executed for every M; no efficient-complexity claim | Positive attained computable gap; M=1 solved exactly |
| `thm:r70-background` | Finite exceptional prefix and two bounded-decoder suffix realizations; choice stored in counted labels | Positive background; fixed leakage in logarithmic upper; no matched background lower rate | Full constructive proof and exact complete-response checks |
| `prop:r70-degenerate` | Explicit 1/2/3-label realizations and active-core lower | Zero contrast, zero internal retention, zero leakage survival, no leakage and full background separated | Full proof and finite exact checks |
| `prop:r70-one-label` | Two endpoint affine lower bounds intersect; remaining nodes verified rationally | Exactly four parameter pairs and one live label | Exact global value, not local optimizer output |

An initial draft phrased the strict fixed-memory risk gap too broadly. Before source sealing, it was explicitly restricted to the irrational internally undamped case; strictly internally damped targets do admit finite exact realizations. No changed theorem is hidden behind a numerical test. The complete predecessor bytes are untouched.

The Perron, rational interpolation and positive-realization ingredients are classical. The main text supplies their proofs in the form needed and the priority ledger credits their ancestry. The current new mathematical assertions concern exact bounded-decoder state accounting and physical task consequences. Their top-four significance remains a question for independent assessment.

Remaining questions include general multi-command boundary control, exact or matched general-M squared-sign risk, a sharp background-dependent lower memory rate, intrinsic geometric exactness and matching program/precision/sampling/workspace/time resources. The finite tests and native build do not prove continuum statements by sampling and do not certify earliest priority.
