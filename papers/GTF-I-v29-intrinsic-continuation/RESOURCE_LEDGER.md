# Resource ledger — revision 29

| Result | Persistent state and input convention | Exact scope |
|---|---|---|
| Intrinsic realization | All charged elementary cuts; no free seed or data-dependent clock; fixed row tables; action before its next report | Complete finite causal arrays; time-indexed rows; additional autonomous sharing not automatically preserved |
| Componentwise-simplex profile | `s_t = sum_j (affdim R_(t,j)+1)` | Lower against arbitrary stochastic generators; one matching causal machine at all cuts |
| Product continuation | Whole independent joint output law required | Capacity multiplication is not inferred from marginal correctness or additive payoff |
| Full-support product barrier | n q-ary inputs acquired before any release; output-order information and labels cannot be reread by the machine | Exact peak q^n for nonzero channel signal; output buffers included |
| Weak binary-query experiment | n bits read once, atomic query after acquisition, output sampled on that query update | t+1 labels after t bits; peak n+1 for `0<eta<=1/n^2`; only final decoder uses eta |
| Strong binary-query experiment | Same interface; all adaptive acquisition/scheduling memory must pass through query-cut state | Peak 2^n for `eta>1-1/n`; full retention matches |
| Query-free zero signal | One query-cut state; emitted bit held in two states if a held-output cut is charged | No claim that a held binary output needs only one state |
| Physical marked audit | Specified Brownian target; exact target-dependent atomic stochastic row | Five decision states and minimum twelve over fixed declared validation clocks retained |
| Acquired physical target | Finite calibration counters, row-precision workspace and downstream state products | Approximate-score theorem retained; not same exact five/twelve count for unknown target |

The online barycentric construction stores a vertex **index**. Vertex coordinates are fixed program constants, not an uncharged evolving real register. It uses no externally retained acquisition transcript. Atomic arbitrary stochastic rows are not silently implemented by a bounded number of fair bits. A bit-serial query interface would require a new query-buffer ledger.
