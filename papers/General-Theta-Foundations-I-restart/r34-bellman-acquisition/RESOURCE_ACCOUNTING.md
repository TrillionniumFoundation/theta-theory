# Resource-accounting table

| Resource | Core theorem | Post-control joint theorem / implementation |
|---|---|---|
| Preparation | One physical call | One physical call |
| Core acquisitions | Exactly n calls, adaptive finite action family | Exactly n calls; all actions finish before new bit |
| Side acquisition | None | One freshly prepared bit report; no core action afterwards |
| Audit | One protected terminal physical call | One protected product audit |
| Physical total N | n+2 | n+3 |
| Dynamic persistent states | `1+sum m_t <= M`, every phase/action/halt included | `1+sum_{t<n}m_t+4m_n <= M` for the constructive code |
| Feasibility | `M>=n+1` | `M>=n+2=N-1` |
| Lower bottleneck | Last width at most `M-n` | Pre-bit width at most `M-n-1=M-N+2` |
| Finite programme | Action, halt, grid and centroid tables; description bits separately charged | Additional bit labels/readouts; programme not identified with log M |
| Temporary workspace | Current report precision plus evaluator/integration workspace certificate | Same, plus bounded bit handling |
| Clock | Carried by disjoint phase labels | Carried by disjoint core/bit/terminal roles |
| Calibration | No unknown core parameter in theorem | Actual invisible fixed sign ±delta scored in product task |
| Numerical error | Programme action slack gamma; rounded readout delta_out²; mismatch probability budget | Same certificate, independent of physical attained calibration |
| Causal deficiency | Complete-law parameter-independent simulation | Actual early-completion bit deficiency epsilon=a/2 at post-control interface |
| Simulator state | R states multiply M to RM | No hidden simulator history or quantum workspace |
| Physical/CPU time | n raw calls plus primitive evaluation and offline planning, all stated separately | One extra paid report; no free retries/audit peek |

The checkpoint has unrestricted acquisition memory and pays only for the final checkpoint labels. It must not be advertised as a total-memory implementation.

`benchmark.py` contains exact rational descriptions of 779 thresholds and 30 scalar codepoints for a 61-label binary machine. Logarithm evaluation and real-report comparison require the numerical certificate. The diagnostic trace is for inspection, not part of the finite-state machine.

M counts configurations, not total bit complexity. Programme and workspace upper estimates are not a proved joint computational optimum. In the same-task perturbation propositions, errors add (with the explicit bounded-loss factor) while independent simulator/controller configurations multiply. Full infinite-horizon or LDP transfer is not inferred.
