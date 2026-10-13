# Resource accounting

| Resource | General model / implementation | Not silently free |
|---|---|---|
| Acquisition | Each raw sensing action counts one; sup_theta E tau<=N | Rejected reports count; N is not a pathwise cap |
| Persistent state | Number of live plus terminal states <=M, the sets disjoint | Stop flag, saved seeds, phase, simulator states |
| State bits | At least ceil(log2(number of live plus terminal states)) for the label | Not equal to program or total physical complexity |
| Sharp constructor | One live plus m terminal, total m+1 | No saved exact posterior, history, or external clock |
| Program constants | Effective constructor: primitive description plus O(km[p+log m]) bits | Codebook, acceptance thresholds and action primitive |
| Numeric precision | p<=C+ceil(s^-1 log2(Nm)) under certified effective inputs | Bare Borel minimizer need not be computable |
| Temporary workspace | Current report, distance accumulator/index, arithmetic; erased before next call | It is charged separately, not retained between acquisitions |
| Physical time | Expected evaluations for all attempted calls plus preparation/audit | No deterministic latency guarantee or optimal-time lower claimed |
| Causal simulator | Product-state bound R M; source calls <=kappa N+c | Internal state, action lift, report/stop/audit compatibility |
| Error composition | Full stopped scored-law TV, root readout error; actual attained delta^2/epsilon in product | Report-marginal TV does not suffice; TV does not price unbounded duration |
| Attained product | One live, m bit-waiting labels, 3m terminal labels: 4m+1<=M | Bit query and protected audit after the committed core stop |
| Total physical calls in product | One preparation + core mean n + one bit query + one audit = n+3 | This convention is separate from the core's E tau<=n |
| Calibration data / known constants | Raw model family and verified comparison/net primitives are declared input | No theorem of free unknown-kernel learning or free discovery of nu |

An extra upper bound on any nonnegative linear primitive cost is allowed by the general occupation theorem while retaining the unit acquisition cap. Equality constraints on expected occupation cannot use invariant removal without additional proof.
