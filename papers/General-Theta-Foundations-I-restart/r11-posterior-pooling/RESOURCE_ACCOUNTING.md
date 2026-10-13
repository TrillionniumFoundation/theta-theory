# Resource-accounting table

| Coordinate | New bound / rule | Explicit caveat |
|---|---|---|
| Raw sensing calls n | Exactly n controlled transitions/reports | Preparation and scored audit additional |
| Persistent state | 1+sum_t L_t | Includes initial state, phase, action instruction and terminal label |
| Persistent bits | ceil(log2(1+sum L_t)) | Does not include immutable programme or scratch |
| Hybrid singular states | 1+sum_t(vertices+sum_s L_t,s) | Stratum identity not a free register |
| Early bit + sensor state | 1+3(1+nL)=4+3nL | Safe sufficient count, not minimal status merging |
| Simulator state and clock | M S Q | Only genuine extra clock/interface states multiplied |
| Programme | Explicit finite table bound in Section 5 | Known constants cannot depend on acquired data or true unknown parameter |
| Temporary workspace | Kernel/arithmetic/table-scan buffer | Erased at each persistent cut; not hidden posterior memory |
| Physical time | Certified kernel durations plus execution scans | No unit-cost random access or free arithmetic |
| Bellman comparison gamma_t | Adds sum gamma_t risk | Offline certificate; planning need not be polynomial |
| Coefficient/report/arithmetic beta_t | Adds O(rho beta_t/h_t) mismatch | Distinct from output precision |
| Terminal readout u | Adds u^2 | Forecast projected into simplex |
| Physical kernel calibration zeta_t | Adds 2 sum zeta_t in categorical task | Conditional joint law, not report marginals only |
| Scored-law deficiency epsilon | Adds L_loss epsilon via certified lift | Lower transfer needs reverse coverage |
| Attained sign/erasure experiment | delta^2 + epsilon/2 squared risk | Same actual scored task and early deadline |

For fixed n, matching excess in the joint example is M^(-2/d)+delta^2+epsilon. Displayed n dependence is retained. This is not a matched region for all programme, workspace, planning, execution and simulator coordinates.
