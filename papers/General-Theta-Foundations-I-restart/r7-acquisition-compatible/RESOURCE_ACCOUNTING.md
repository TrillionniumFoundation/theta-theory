# Resource accounting

| Coordinate | Meaning | Proven account |
|---|---|---|
| N | Actual raw kernel calls including preparation, failed/missing/idle opportunities and terminal audit | Progressive N=n+2; erasure extension N=n+3; Gaussian T+2; retained dynamic singular B+T+2 |
| M | Entire data-dependent retained tuple at the stated prediction cuts | Block code M per declared fiber; progressive K<=floor(log2 M) exact bits; joint source 3*2^K'<=M |
| Q | Supplied or stored deterministic phase/clock | Separately counted; digital total persistent cardinality <=2^K Q, or 3*2^K' Q |
| R | Simulator internal states | Explicit serial upper in thm:morphism; not universally necessary |
| C_ctr | Controller state | All data-dependent retained controller state must fit M or be separately included in the cut tuple |
| W | Temporary writable bits | Digital <=C[p+log(K+d+2)]; erased before persistent cuts; not replaced by log M |
| L_prog | Read-only program/calibration/schedule description | Digital <=C(K+d)[p+log(K+d+N+2)] |
| p | Supplied coefficient/output precision | Root digital error Gamma=(K+1)2^-p; no arbitrary-real computability claim |
| delta | Inaccessible task calibration sign radius | Joint-family lower and upper delta^2; a generic allowance is only an upper |
| u | Certified local stable-metric numerical error | Must preserve the relation; adds to local root error before propagation |
| epsilon | Complete common-task stopped-law defect | Adds L_* epsilon; attained order and exact deficiency in the stated erasure pair |
| T_bit | Primitive computation | Padded sequential-tape upper C[N+d(K+d)(p+log(K+d+N+2))] |
| physical time | All actual acquisition and primitive computation | Digital <=N+T_bit in declared units; no parallel/unlimited precision convention hidden |

The matched multiscale law is for N, data-dependent label capacity M, delta and the attained epsilon interface on the displayed feasible digital region. It is NOT an optimal tradeoff for total program/scratch/time, nor does it erase the Q multiplier when total persistent state includes a stored clock. Raw terminal audit outcomes are revealed after prediction and cannot be used to manufacture pre-decision precision.
