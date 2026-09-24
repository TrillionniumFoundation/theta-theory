# Resource ledger — revision 26

A state count is a cardinality, not an implicit number of bits. A multicut profile is not its minimum or its maximum. An offline optimizer is not a runtime register. Read-only constants may not depend on the unknown true parameter.

| Construction | Preparation and persistent-state accounting | Randomness / precision |
|---|---|---|
| Controlled routing | Two training preparations; profile `(1,K,m,3,6,3)`. The K-state decision cut selects a branch-specific experiment; the chosen action is held in the separately charged m-state buffer. | Fresh stochastic encoder/decoder rows; no free persistent policy selector. A cyclic mixture can require up to mK decision labels. K is not the uniform peak. |
| Exact original marked U2 | Two candidate training, one candidate validation, one target validation. Profile `(1,2,3,3,4,5,5,5,10,12,10,10,7,3)`; five frozen event labels, peak twelve. | One atomic Bernoulli row with algebraic probability tau. This is an exact stochastic-kernel realization, not an exact finite fair-coin implementation. |
| Dyadic marked U2 | Same four preparations; peak at most `max(12,6(b+1)+5)` under sequential fair-bit implementation. | At most b fair bits; score loss at most `(5/16)2^(-b)`. The comparator phase, origin and comparison flag are charged. |
| Revelation | At most N training preparations; K decision labels. Reveals update the label directly, with no revelation flag. | State initialization is a charged stochastic label, not a stored external seed. K=2 yields an atomic full validation peak of four. |
| Offline finite-profile recursion | The actual architecture contains only its declared finite labels and observable rows, including stop/design/event labels. | The parameterwise occupation bundle is a mathematical design variable, never retained by the controller. Reused autonomous rows are chosen once. |
| Acquired calibration and simulation | `N_cal` pilot preparations plus every source preparation used by the simulator. At cut t, at most `C_cal R_t M_t K_t` states. | C_cal retained calibration labels, R_t simulator states, M_t representative states and K_t controller states are all charged. |
| Categorical pilot | r0 rows, n samples per row, `N_cal=r0*n`; histogram labels at most `(n+1)^(r0*(d-1))`. | With coordinate tolerance z, all-row TV error at most dz/2 except probability at most `2*r0*d*exp(-2*n*z^2)`. A clocked schedule is assumed; autonomous phases cost additional states. |
| Repeated confidence consumer | R blocks, 4R preparations; `W_b(2R+1)` states including the running score sum. | At most bR fair bits. A whole-audit simulation defect is added once to the event error bound; independence is not assumed after a shared calibration is introduced. |

The exact two-preparation score on W>=12 does not establish that twelve states are necessary. The old decision-width-three longer audits remain valid and are not erased. The original collision width-3-through-11 frontier is distinct from both the routing K-cut law and the revelation K-cut law. The stationary autonomous theorem retains its original atomic versus sequential-bit conventions.
