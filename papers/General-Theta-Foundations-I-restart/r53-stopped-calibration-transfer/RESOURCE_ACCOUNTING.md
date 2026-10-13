# Resource accounting

| Resource | Counting convention / bound |
|---|---|
| Core raw acquisitions | Every allowed call including failures/rejections, sum c_ia; gate identity kappa(p)x_A |
| Checkpoint terminal values | m fixed responses; all-history sensing is a separate architecture |
| Autonomous persistent labels | L live + m terminal; no external mode/clock register |
| Necessary live labels | Mandatory modes with pairwise disjoint action sets; gate needs two |
| Stored label bits | ceil(log2(L+m)); not total bit complexity |
| Read-only program | Center precision + action/routing/coin descriptions + mode transition table |
| Temporary workspace | W_tmp(b), cleared or explicitly retained/charged; no hidden report tape |
| Computation/physical time | T_eval(b) E tau plus preparation/planning/audit; waiting p stays explicit |
| Simulator state | Direct product at most R M labels; own clock and actions must match |
| Numerical error | Killed potential W controls duration, U controls same loss; feasible reference slack |
| Calibration | Actual hidden fixed alternative for lower term; numerical tolerances separate |
| Total attained-error task | N-2 raw core calls after early call and final audit; 1+3(2+m) labels |

No free persistent random seed is allowed. Fresh coins are allowed. The qubit and hidden sign are protected physical systems, not memory registers at the observer's disposal. No optimality of program/workspace/time upper bounds is claimed.
