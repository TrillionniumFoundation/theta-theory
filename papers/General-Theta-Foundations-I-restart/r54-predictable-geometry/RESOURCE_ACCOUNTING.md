# Resource accounting

| Resource | Main theorem | Explicit finite implementation |
|---|---|---|
| Real raw acquisitions | sum c_t; c_t>=c_star; all failures retained | gate and acquisition each cost one; dyadic mean <=402653184/1017871<400 |
| Acquisition navigator | B live labels | gate G and productive A: B=2 |
| Terminal dictionary | m distinct fixed outputs | one output 1/2 in the three-state dyadic example |
| Total persistent alphabet | B+m, lower M-b_phys under common mandatory contexts | three labels encoded in two bits; no external clock |
| Program description | NOT bounded for arbitrary Borel routing | three 15-bit thresholds =45 bits, fixed ISA and exact output additional; general cell table O(m k p) |
| Temporary workspace | separate from persistent labels; erased between calls | two 15-bit digitized-coordinate registers plus fixed comparison bits; general O(kp+log m) |
| Coordinate/parameter precision | effective input certificate required | p=14 fractional bits, deterministic error <=2^-14, clipped [0,1] |
| Execution time | per-call time certificate summed over actual occupation | <=400[t_raw(14)+14 C_cmp] in the declared digitizer contract |
| Raw hidden state | physical experiment, not writable/free observer memory | classical hidden sign or physical qubit; observer cannot retain arbitrary information there |
| Randomness | fresh routing coins independent of future audit, no retained seed | deterministic dyadic acceptance; stochastic hidden physical reports |
| Simulator state | predictor and simulator alphabets multiply S M | all retained phase and seed registers counted |
| Preparation / audit | separate until a total budget is declared | joint task N=N_core+2; early bit call and final vector audit paid |
| Calibration | deterministic output approximation changes squared loss by <=2D delta+delta^2; actual hidden sign gives delta^2 lower | sigma is absent from every pre-audit kernel |
| Deficiency | complete stopped scored-law TV, plus separate physical-cost certificate | actual early erasure probability 2 epsilon; exact defect epsilon |

Dictionary size is not total bit complexity. A static mathematical coefficient may have infinite description unless a finite certificate is supplied. The construction does not claim optimal program, workspace, time or simulator complexity. Generic additive costs need explicit weights; no silent sum of bytes, seconds and acquisitions is performed.
