# Independent Referee Report — Round 15

**Manuscript:** B2 — *Collision Clusters and Dynamic LDP*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence and submission integrity

The folder continues to declare and input Round Fourteen. No materialized Round-Fifteen B2 module, author response, or certificate exists in the branch. The surviving payload does not contain a complete B2 candidate. This is not a reviewable Round-Fifteen submission.

## Executive assessment

The manuscript has correctly abandoned a genealogy-uniform Łojasiewicz exponent and tries to use fixed-genealogy convergence plus a factorial majorant. That strategy could be viable. The particular transverse map is not defined on a physical family: the proof removes the surplus-contact equation while retaining the reflection and all later dynamics. Off the contact manifold there is no such hard-sphere collision. The lower-bound “Hodge repair” also does not preserve positivity.

These are fatal to the grand-canonical actual-contact theorem, which is the root of the entire B-series.

## Decisive objections

### 1. The surplus pseudo-orbit is not a hard-sphere trajectory

At the first surplus contact, the manuscript removes the equation

\[
|x_a(t_*)-x_b(t_*)|=\varepsilon
\]

but says it retains the reflection and the future trajectory. Once the equation is removed, nearby parameter values generally place the particles away from contact. There is then:

- no physical collision normal determined by relative position;
- no specular reflection at \(t_*\);
- no post-collisional velocity;
- no resulting hard-sphere future.

Thus the map whose transverse position derivative is computed is not defined by the deterministic hard-sphere flow on an open neighborhood.

A legitimate coarea proof must define a smooth **pre-contact** map on an open parameter domain and impose contact as its zero set. The reflection and post-contact chronology can be introduced only on that zero set, with a separate implicit-function construction. The current pseudo-orbit does neither.

### 2. The alleged witness does not prove the prescribed chronology exists

The proof places subsequent creation contacts in a short interval and a final free-flight interval of length \(L\), then chooses normals and velocities “generically.” Collision times, positions, normals, and velocities are constrained by the entire prior hard-sphere chronology. They cannot be assigned independently.

To prove a nonzero analytic minor, one must exhibit an actual regular solution of all flight and collision equations for the specified labelled graph and verify strict time ordering, absence of unintended collisions, and non-grazing incidence. No such construction is given.

### 3. Fixed-genealogy domination is not established by the displayed majorant

The factorial majorant includes velocity factors and combinatorial counts but does not prove domination uniform over the grazing/velocity truncations used in the transverse estimate. Passing those truncations by “monotone convergence” is not valid for signed or complex source-decorated activities, and incoming flux does not automatically control every inverse Jacobi denominator.

### 4. The positive lower recovery is false as written

The kinetic Hodge repair solves an \(L^2\)-type equation and sets

\[
\delta\Gamma=(\Delta r)A_f.
\]

Lax–Milgram controls \(\Delta r\) in \(L^2(A_f)\); it does not bound its negative part pointwise. Therefore it does not imply

\[
q+\Delta r>0.
\]

Adding a small Maxwellian background before solving does not dominate an unbounded negative correction. The repaired object may be a signed measure and cannot define a contact intensity or microscopic likelihood.

### 5. Exposure by a bounded source is not shown for the full regular class

Given \(q=d\Gamma/dA_f\), the source relation

\[
\psi=\log q-\Delta p
\]

is bounded only under strong bounds on \(q,q^{-1},p\). Solving the forward biased Boltzmann equation and backward adjoint does not prove that an arbitrary smooth balanced target pair arises from such a bounded source. The argument reverses the control problem without establishing surjectivity.

### 6. Bounded-source pressure does not automatically give the full entropy rate

A local complex source ball identifies the entropy dual only for bounded \(\log q\). Extending to every finite-action pair requires monotone source exhaustion, exponential compactness, and a recovery theorem stable as the source radius grows. Those steps are asserted in one paragraph and depend on the invalid positivity repair.

### 7. Corner and multiple-contact support is not closed by codimension counting alone

A codimension-two geometric set can carry a singular limiting measure even when every prelimit simple-flux measure gives it zero mass. To conclude that finite action excludes all corner mass, one needs lower semicontinuity of the entropy against the correct reference measure on a topology that sees those strata. The graph construction and entropy functional are not shown to provide this.

## Dependency impact

B1's canonical coefficient, B3's Gaussian tangent, B4's nonlinear semigroup, C1/C2, and D1 all require B2-GC. Until the physical pre-contact transversality and positive lower recovery are proved, none can treat the actual-contact Hamiltonian or LDP as an established input.

## Required reconstruction

Define the full pre-contact evaluation map on a genuine open trajectory parameter space, prove a nonfocusing/submersion theorem for its zero set, and only then sum fixed genealogies. For the lower bound, use positivity-preserving controls or a nonlinear projection onto balanced positive intensities rather than an unconstrained \(L^2\) correction.

## Recommendation

**Reject.** The submitted branch contains no Round-Fifteen B2 manuscript, and the controlling root theorem differentiates an off-contact reflection that does not exist.
