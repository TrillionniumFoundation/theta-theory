# Resource accounting

| Coordinate | Exact meaning / bound | Accounting rule |
|---|---|---|
| N | Number of real raw calls, including mandatory preparation/reset calls | External evaluation horizon, not an internal free clock. |
| tau | One complete charged cycle length | Actual controlled law; uniform tail envelope supplied for all programs. |
| M | Entire persistent classical observer alphabet, including distinguished reset state | No external seed/counter/history survives. Log2 M alone is not total bit complexity. |
| Physical reset | Joint new physical preparation and observer overwrite | Mandatory experimental protocol; count its calls/time. Not derived from mixing. |
| Lifetime clock | Part of a stated physical experiment, possibly unbounded | Not observer memory; a simulator reproducing it must pay its own resources. |
| Program description | Probability table: at most [M|A|+M^2 sum J_a] ceil(log2(Q+1)) bits, plus classifier/code/readouts | Distinct from runtime labels. General Borel exact rows need not be computable. |
| Workspace | Report parsing, random sampling, output arithmetic | Charged separately; no optimal lower bound is proved for it. |
| Q / rho | Probability denominator / readout approximation | Row TV and loss modulus enter effective error separately. |
| Calibration delta | General approximation uses its certified task modulus; the explicit hidden-sign task attains delta^2 | An upper tolerance alone is not an unavoidable lower error. |
| epsilon | Complete scored-cycle causal defect under fixed timing/task/reset interface | Tail-dependent average modulus chi(epsilon), not universally linear. |
| Simulator S | Full internal simulator state, action/report lift, reset/clock/readout compatibility | Combined predictor/simulator labels <=MS; serial counts multiply. |
| Physical time | Actual preparation, sensing, reset and audit duration | Per-target-call value is not automatically per-source-time value. |
| Offline work | All finite tables, model net, interval integrations | Exhaustive certificate, not efficient synthesis. |

The matching joint example uses 3 floor(M/3)<=M labels. No extra reset label is needed because its zero-score preparation reuses one existing label. This is a sufficient construction, not a proof of the least possible observer or simulator size. Audit marks are performed marked-kernel outputs; a laboratory implementation using separate audit calls must add those calls to its ledger. No free audit is inferred from an abstract symbol.
