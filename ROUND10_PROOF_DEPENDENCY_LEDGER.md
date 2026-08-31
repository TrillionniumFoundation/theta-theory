# Round-Ten Proof Dependency Ledger

## Non-circular order

### Independent benchmark

`A1`

A1 uses only its explicit baker family, mapping-torus construction, and
one-sided transfer operators.

### Sinai chain

`A2 -> A3 -> A4 -> C2 -> D1`

- A2 supplies the parameter-uniform vector/roof spectral, arithmetic, UNI,
  and density local-limit packet.
- A3 uses A2 only for finite-cylinder pressure and clock coefficients; its
  marked-flow state, projective LDP, and recession theorem are proved in A3.
- A4 uses A3's prepared path law and A2's regular phase spectrum to build the
  past kernel, Doob semigroup, rough tangent, and memory.
- C2 uses the A4 past filtration and the A2 common transfer bundle.
- D1 uses only already constructed phase components and component LDPs.

### Hard-sphere chain

`B2-GC -> B1 -> B2-MC -> B3 -> B4 -> C1/C2 -> D1`

- `B2-GC` consists of the closed trace graph, integrated first-surplus
  estimate, all-contact expansion, and source-uniform one-block theorem.
- B1 conditions that grand-canonical source pressure at the exact finite
  saddle and proves the shell coefficient.
- `B2-MC` uses B1 only in the final microcanonical transfer; the grand-
  canonical lower bound is proved before it.
- B3 uses B1's prepared initial covariance and B2's marked cumulants/Green
  graph; it does not define covariance through its own action Hessian.
- B4 uses the already proved B1--B2 good rate and B3 tangent.  B4 does not
  prove an upstream LDP by its Hamilton--Jacobi equation.
- C1 operates on the prediction/filtering state supplied by B2 and the
  reachable-chaos class it constructs itself.
- C2 and D1 use only completed component interfaces.

## Forbidden cycles

The structural verifier rejects any source claiming one of the following:

- B1 uses B2-MC;
- B2-GC uses B1;
- B3 covariance is defined as the inverse of an assumed coercive B3 action;
- B4 comparison proves B2 lower recovery;
- C1 observation coefficients are imported from C1 itself;
- D1 phase components are merely exponential tilts whose mixture creates a
  new law.

## Merge gates

1. Eleven registered Round-Ten sources materialize byte-identically.
2. Every theorem-like environment has a proof and every local reference
   resolves.
3. Paper-specific counterexample regressions pass.
4. The dependency graph is acyclic and the forbidden cycles are absent.
5. All eleven papers clean-build with no undefined references or citations.
6. The exact mathematical commit is separated from publication metadata and
   the old main is archived before an atomic main/tag update.
