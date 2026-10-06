# Resource account and lower-bound responsibility

Full implementation ledger: (N_raw, m, R, D_c, Q, W, P, b_cal, b_num, tau). Fused ledger: (N_raw, M, W, P, b_cal, b_num, tau). Risk expressions keep the full vector. M=m*R*D_c*Q is a constructive direct-product capacity, not a universal identity for optimal machines.

| Coordinate | Counted data/cost | Bound proved |
|---|---|---|
| N_raw | All physical calls, pilot/failure calls and one actually executed terminal probe | Pathwise affine morphism map; robust class N_raw=n+3; prediction-only N maps to N_raw>=N+1 |
| m / M | Observation-dependent state at cuts | Anisotropic predictive-label lower; growing-tag fused-state lower at floor(M/L) |
| R,D_c,Q | Actual simulator/controller/internal-clock capacity | Constructive products; mandatory L=R0*D0*Q0 only when semantic tokens independently challenged |
| W | Temporary current reports, candidate indices, guard bits; cleared each call | Explicit O_d(B) feasible upper for robust grid scan; no general optimal lower |
| P | Readonly code and parameter/grid descriptions | Procedural P0+O_d(log budgets+log b); arbitrary center table instead O(mdB) |
| b_cal | Calibration input interface | Propagated state error; delta^2 lower only for compulsory indistinguishable alternatives |
| b_num | Numerical input precision, not all arithmetic guard bits | Common-cell 2^(-2b) lower; guard bits charged to W |
| tau | Calls plus elementary bit operations; emitted tag cost | Explicit padded O_d(N_raw*(m+1)*B^2) feasible upper; not optimal-runtime lower |

Pathwise is default. Expected N/tau composition requires conditional per-call bounds uniformly over calling histories. Tail composition uses joint good events and union bounds. Memory/workspace/program capacities remain pathwise.

Independent immutable randomness is not an observation tape. Any data-dependent pointer is retained. A free public clock is the exogenous protocol call index; adaptive timing is charged. Robust arithmetic can be padded to the stated uniform bound, so runtime is not an uncounted later observation.

The robust upper stores L tag states, three bit states, and m+1 geometric states (including unresolved): 3L(m+1)<=M. The converse is for fused M and does not presuppose this architecture. The tag challenge is a machine output, not a new physical probe; its bit-output operations are charged. Only one terminal soft-task probe executes.
