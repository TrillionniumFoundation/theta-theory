# Resource-accounting table

| Resource | Core external geometric | Core internal geometric | Joint bit/calibration external |
|---|---|---|---|
| dynamic labels | 1+m | 1+2m (halt copies charged) | 1+3(1+m)=3m+4 |
| dynamic bits | ceiling log2(1+m) | ceiling log2(1+2m) | ceiling log2(3m+4) |
| physical acquisitions, pathwise | tau+2 | tau+2 | tau+3 |
| mean acquisitions | 1/s+2 | 1/s+2 | 1/s+3 |
| deterministic cap | none | none | none |
| auditor stop resource | specified independent Bernoulli primitive | own fresh coin and halt labels | specified independent Bernoulli primitive |
| program constants | codepoints, action probabilities, readouts, raw primitive and partition code | same plus halt map | three copies or shared read-only code with lane labels |
| finite precision | certified p and actual boundary/failure envelopes | same plus hazard primitive | same plus bit/readout calibration |
| workspace | current report, arithmetic, sampling scratch; erased before next call | same | same |
| time | per-call certified time times actual count, plus initialization/audit | same | plus early bit call |

Hard cap H uses H+2 core / H+3 joint pathwise calls and an auditor counter. It is not a free internal hard deadline. Geometric terminal means calibrate only at the actual request, not each call. A noncomputable real hazard or program coefficient is not a finite-bit object. Exact Borel and certified finite-bit models are explicitly separate.

A simulator with R states and an M-label observer has a direct RM-state realization; this is an upper, not optimality of the product. Workspace, program, raw call map and physical time compose separately. Per-call mismatch eta gives complete-law error at most eta/s; readout error v gives a task-norm perturbation. Calibration delta and attained deficiency epsilon have a jointly realized matching law only in the explicit independent-bit/sign experiment.
