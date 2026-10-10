# Resource-accounting table

| Coordinate | Mathematical object / constructive bound | Converse status |
|---|---|---|
| Raw acquisitions | Main protocol uses its explicit N_raw; full-tail model T+2; finite-read model B+T+2, including preparation, every read/hold and terminal probe | Finite-read Phi uses the actual depth distribution at this budget; no optimal B/T policy claimed |
| Persistent state | At most M labels; finite-read code has 2^(m+2)-2 labels, already including mode and length | Actual-law checkpoint lower, ideal-score lower with acquisition variance, inherited exact/noisy continuation information lower |
| Auxiliary simulator | R internal states and paid source microsteps | R x M is a product upper, not universal necessity |
| Controller and clock | D_c and Q; B/T counters or externally provided schedule must be identified | No general optimal-controller/time converse |
| Temporary workspace | O(n_max+b_out) bits for word/report/arithmetic routines, erased across cuts | Not identified with persistent labels; surviving bits enlarge state in the information lower |
| Program description | Ratio schedule, depths, calibrated parameters and transition/readout code | Description length counted separately; no shortest-program theorem |
| Calibration | Local numerical allowances in common metric; finite-read model additionally has an unobserved terminal sign +/-delta | Exact delta^2 ambiguity floor in that same raw model; not a learned-kernel calibration theorem |
| Numerical output | Certified center error or unbiased dyadic rounding mesh 2^-b | At most 2^-2b/4 additional variance for ideal unbiased rounding; not a universal lower floor |
| Input precision | Full-tail Borel model reads a charged finite prefix; finite-read model physically acquires B initial bits and <=6 new bits per active report | Full and truncated raw reports are not declared TV-equivalent |
| Physical time | All raw waits retained; bit reads and arithmetic charged; O((n+b_out)^3) conservative deterministic center arithmetic | Exact rational rejection sampling has finite expected, not automatic worst-case time; truncation charges tail defect |
| Causal deficiency | Complete interactive common-task TV defect, controller/task compatible | Adds at most epsilon for loss in [0,1]; a matched lower needs separate alternatives |

Serial implementation uses M_tot >= M R D_c Q only as a declared feasible upper. A regulator/simulator state that is distinguished by executable continuation may carry an information lower, but not because it appeared in an implementation diagram. Algebraic and calibrated-real parameter access is never an uncharged universal computation model.
