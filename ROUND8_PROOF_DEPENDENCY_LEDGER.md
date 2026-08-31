# Round-Eight Proof Dependency Ledger

The dependency graph is acyclic and is enforced by `tools/verify_round8_referee.py`.

- A1 is independent.
- A2 is independent of A1 at theorem level.
- A3 uses the A2 finite-source coefficient and spectral packet.
- A4 uses A2 for Gibbs/transfer estimates and A3 for the prepared path phase state.
- B2-GC is the hard-sphere dynamic base.
- B1 uses the B2 bounded-source pressure only for dynamic marks; its regenerative coefficient theorem is otherwise independent.
- B2-MC uses B1 after B2-GC.
- B3 uses B2 and B1.
- B4 uses B2 compactness/recovery and B3 covariance typing.
- C1 uses B2, B1, B3, and B4.
- C2 uses A4 for past optional kernels and B3/B4 for kinetic cotangents.
- D1 consumes already-proved phase-specific A2/B1/B2/C1 inputs and never supplies an upstream proof to them.
