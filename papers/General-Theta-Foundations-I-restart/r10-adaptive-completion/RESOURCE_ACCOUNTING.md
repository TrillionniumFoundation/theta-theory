# Resource accounting

| Resource | General completion | Finite implementation / joint construction |
|---|---|---|
| Raw acquisitions | preparation + ≤n binary calls + audit | N=n+2; early erased-bit extension N=n+3 |
| Persistent states | all internal and terminal nodes ≤2m−1≤M | early-channel extension 1+3L≤M; no omitted controller |
| Clock / phase | none publicly supplied or consulted by autonomous machine | node identity controls depth and stop; interpreter entry/program head resets at cuts |
| Predictor readout | leaf mean, same bounded task | coordinate-wise rational approximation, write-only output |
| Controller | policy action in read-only node record; current node retained | primitive instruction ID, action execution cost separately charged |
| Simulator | absent in base proof | S simulator states multiply the predictor/controller alphabet; other actual interface states counted |
| Read-only program | separate from M; arbitrary Borel constants not a finite-bit claim | O(M(log(M+1)+log(K+1)+d(p+1))+log(n+1)) under finite global primitive alphabet |
| Temporary workspace | discarded before each information cut | O(log(M+1)+log(K+1)+log(d+1)+p+1) with sequential scans |
| Numerical precision | exact Borel label model distinct from finite arithmetic | p fractional bits; task error u gives u² at fixed leaf means |
| Calibration | known-kernel certificate vs unknown offset kept distinct | fixed-leaf error composes in root norm; attained unknown sign δ gives δ² in joint model |
| Physical time | raw calls and their physical durations declared | bit-operation scan upper plus separately charged action/audit time |
| Offline planning | exact finite Bellman recursion may be exponential | rational Markov moments and comparisons effective; planning not free or claimed optimal |

The table gives matching acquisition/persistent-state risk and an explicit feasible program/workspace/time implementation. It does not give matching general lower bounds for program length, scratch, planning time or minimum simulator state. A read-only table is not secret extra persistent data: it is fixed before the run and parameter independent.
