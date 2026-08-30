# Round-three proof-dependency ledger

**Base:** `main@970d88ae41faf601ae609d833b48288f213e5c5c`  
**Working branch:** `revision/round3-full-positive-closure-11paper-2026-08-30`  
**Policy:** positive reconstruction only; no no-go substitution, no silent restriction of a headline theorem, and no theorem credit for a compiler without its model packet.

## 1. Non-circular construction order

The hard-sphere series is rebuilt in the following order.

1. **B2-GC:** source-decorated real-trajectory cumulants under a grand-canonical hard-core law.  This step uses only the microscopic flow and the trajectory-cluster geometry; it does not use B1.
2. **B1:** finite-dimensional source-dependent conditioning of B2-GC.  The constraint multiplier is reoptimized for every path/collision source.  A tilted-law concentration argument replaces the false fixed-saddle transfer.
3. **B2-MC:** transfer the marked cumulant and the joint density/actual-collision LDP to the microcanonical shell by B1.
4. **B3:** construct the full balance-adjoint gauge quotient, Orlicz path duality, and joint Gaussian tangent from B2-MC and the prepared initial covariance from B1.
5. **B4:** construct the kinetic nonlinear semigroup by a correlation-hierarchy perturbed-test theorem, not by asserting finite-volume density closure.
6. **C1/C2/D1:** compose only the typed outputs proved in A1--A4 and B1--B4.

The Sinai series is rebuilt in the following order.

1. **A2:** a moving-cut anisotropic atlas, vector/roof complex spectrum, temporal non-integrability, higher-block twists, and a uniform lattice--nonlattice local limit theorem.
2. **A3:** an explicit finite-connector Young code, singularity-frequency estimates with a complexity ledger, and a two-clock extended contraction with complete upper and lower bounds.
3. **A4:** a weighted history Feller semigroup and a compressed-resolvent memory kernel which does not assume generation of `QLQ`.
4. **C2/D1:** use only maps living on the same platform, or an explicitly proved scaling map between platform-labelled components.

A1 is reconstructed independently as an exact Hamiltonian impact-network benchmark on one common symbolic path space.

## 2. New proof tools introduced in round three

### 2.1 Source-dependent shell tilting

For a grand-canonical pressure `Q(H,lambda)` and target constraint `a`, define `lambda_H` by

`partial_lambda Q(H,lambda_H)=a`.

The shell log-Laplace functional is proved by changing measure to the `H,lambda_H` law.  The shell has subexponential probability under this law because its mean is exactly `a`, its covariance is `O(mu^{-1})`, the continuous windows satisfy `sqrt(mu) delta_mu -> infinity`, and the exact particle-number coefficient has a uniform lattice local limit.  This proves the constrained pressure without a fixed zero-source saddle or an unproved complex contour gap.

### 2.2 Edge-rooted marked recollision recursion

Every actual collision receives its source mark.  Collision genealogies are decomposed into a creation skeleton and ordered cycle edges.  Deleting the first cycle exposes the independent geometric constraint used in the hard-sphere recollision estimate.  Iteration yields a source-uniform exponential generating bound for all collision marks; recollisions are never bounded by pretending that they introduce a new label.

### 2.3 Moving-cut spectral bundle and temporal UNI

The radius-dependent billiard spaces are treated as a finite Banach bundle.  Local pullbacks identify stable-curve test distributions while preserving physical branch pairings.  A concrete temporal-distance rectangle supplies a derivative bounded away from zero uniformly in the radius, giving the high-frequency roof estimate.  Medium frequencies are handled by compactness and periodic obstruction; low frequencies give the joint Gaussian expansion.

### 2.4 Shielded marked-clock contraction

The Young-code factor is truncated simultaneously in return length, singularity distance, path-window depth, and clock residual.  The number and measure of bad singularity pieces are kept in one ledger.  The lower bound is proved by a clock-surgery lemma which concatenates typical marked blocks and changes only a sublinear terminal segment to hit a deterministic collision or physical horizon.

### 2.5 Compressed-resolvent memory

For a finite-dimensional resolved projection `P`, the exact transfer function is defined directly from the compressed Koopman resolvent,

`M(z)=zP-PLP-[P(z-L)^{-1}P]^{-1}`.

This construction is independent of whether `QLQ` generates a semigroup.  The causal memory distribution is obtained by inverse Laplace transform; on the Sinai spectral class the transform continues to a left half-strip and gives an exponentially decaying kernel.

### 2.6 Correlation-state perturbed tests

The exact hard-sphere state is represented by its correlation hierarchy.  A density cylinder is lifted by recursively constructed correlation correctors.  The BBGKY generator acting on the corrected cylinder cancels correlation and recollision defects and converges to the Boltzmann exponential Hamiltonian.  This supplies nonlinear-generator convergence without claiming that a smooth one-particle density is an exact finite-volume state.

### 2.7 Balance-adjoint gauge complex

The dual pair `(p,psi)` is quotiented by the closed range of

`r -> (r,-Delta r)`

with the transport endpoint contribution included through the exact weak balance.  The invariant combination is `Delta p+psi`; uniqueness is asserted only for this quotient class.  A weighted kinetic Poincare estimate supplies closed range after constants and collision invariants are fixed.

## 3. Paper-level closure gates

| Paper | Gate that must be proved before merge |
|---|---|
| A1 | common-path typing; Hamiltonian impact realization; process bridge; calibrated-cocycle uniqueness; defined response arrays |
| A2 | uniform geometric atlas; vector/roof multiplier theorem; UNI/aperiodicity; higher-block spectrum; joint local limit and ratio conditioning |
| A3 | finite-connector code; marked level-2 exponential tightness; singularity shield; collision/physical clock upper and lower bounds; finite-rate support; closed coboundary quotient |
| A4 | weighted-history Feller/core theorem; compressed-resolvent identity; exponential memory on the proved spectral class; short-memory tangent |
| B1 | source-dependent multiplier; shell concentration/local coefficient; uniform hard-core transfer; constrained initial rate and covariance |
| B2 | exact orientation/balance; all-contact marked cluster bound; grand-canonical HJ; source-uniform lower bound; microcanonical transfer; good joint rate |
| B3 | complete function spaces; integral Fenchel dual; exact gauge quotient; multiplier qualification; prepared joint fluctuation limit |
| B4 | exact correlation-state semigroup; corrected-cylinder generator convergence; compact containment; comparison; lifted microcanonical saddle; Gaussian tangent |
| C1 | three non-conflated games; vanishing block error without an artificial change of game; discrete versus smooth saddle calculus; comparison for adaptive law control |
| C2 | platform-labelled parent; continuity or exponential approximation of each contraction; strict-dual cotangent space; spectral/cluster differentiability; typed likelihood and memory diagrams |
| D1 | correct speed normalization; explicit maps for every contraction; joint likelihood-ratio tangent; dependency hashes and commutative diagrams |

## 4. Fail-closed merge rules

The branch may update `main` only after all of the following hold.

1. Every paper's controlling `main.tex` includes its round-three proof module.
2. No round-three theorem contains `assume the main gate`, `imported packet`, `reviewer must verify`, `conditional on`, `no theorem credit`, or an equivalent placeholder for its own principal assertion.
3. Every displayed main theorem has a proof, and every cross-paper import resolves to a theorem already earlier in the dependency order.
4. All eleven papers build from a clean checkout.
5. A mechanical grep verifies corrected normalization, source-dependent saddles, full gauge notation, platform labels, and absence of the superseded fixed-saddle formulas.
6. The exact revision commit is subjected to a fresh harsh internal rereview before the main ref is moved.

Build success is necessary but not mathematical certification; the proof audit is a separate mandatory gate.
