# Round-Five Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — *Nonlinear Kinetic Semigroups from Deterministic Hard-Sphere Hierarchies*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round5-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `557c88ef447ab8c693b11e1c072efe97b4452556`  
**Active controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `c18b1ea8cc9b7e57ee46122ccc52ab32d554bcb0`  
**Unmaterialized round-five candidate:** `revision/round5-referee-final/B4_LAW_STATE_BBGKY_BOUNDED_INCREMENT.tex`, blob `42dfaee02d5db2aa68220b23fa53c7a78fc7eb4b`

## Source-control verdict

The active B4 manuscript is unchanged from round four. It still treats a class of linear hierarchy functionals as an algebra, uses a formal fixed-level corrector construction, and claims comparison on an energy state space which does not control the exponential collision Hamiltonian.

The round-five candidate correctly distinguishes deterministic microstate flow, law states, and correlation coordinates, and restricts the collision increment to a bounded core. It is not materialized. Its exact-state theorem is largely tautological, while the generator, compactness, and comparison arguments remain false or incomplete.

## Audit of the proposed round-five replacement

### 1. The “exact law-state tower” is not the nonlinear log-Laplace tower needed later

The candidate defines

\[
(\mathbf V_\varepsilon(t)\Phi)(\rho)
=\Phi((\Phi_t^\varepsilon)_\#\rho).
\]

This is simply deterministic composition on the space of probability laws. It is an exact semigroup for every deterministic flow, but it is not a conditional risk-sensitive value operator and supplies no nonlinear Markov closure for empirical density.

The exponential cylinder

\[
\mathbf E_{\varepsilon,F}(\rho)
=\mu_\varepsilon^{-1}\log\int e^{\mu_\varepsilon F(\pi(Z))}\rho(dZ)
\]

is one particular functional transported by this trivial semigroup. This observation does not establish the microscopic-to-kinetic nonlinear generator convergence claimed in the remainder of the paper.

### 2. The triangular BBGKY corrector construction is formal

The packet defines a corrector at level `j+1` using free transport of an “uncancelled defect” and then asserts that repeated substitution produces the complete time-ordered BBGKY operators. It does not define the functional domains, hard-sphere boundary traces, or the exact nonlinear generator acting on these cumulant functionals.

The estimate

\[
|R_{K,\varepsilon}|
\le C_F(\rho^K+\varepsilon^\alpha)
\]

is simply imported from the proposed B2 tree norm. No proof tracks the factorial combinatorics, boundary operators, source derivatives, and accumulation of lower-level correctors. This is the load-bearing perturbed-test theorem, and it is not supplied by a schematic recursion.

### 3. Finite hierarchy truncations are not order-preserving

The proof of relaxed upper and lower generator convergence says that positivity of factorial moment functionals permits approximation from above and below by finite hierarchy truncations. Truncating a factorial/cumulant expansion is not generally monotone. Coefficients and connected corrections have signs, and an arbitrary finite hierarchy vector need not correspond to a positive probability law.

Thus one corrected sequence with a norm estimate has not been constructed, and the two viscosity inequalities do not follow.

### 4. The declared energy sublevel is not compact in the topology used

The candidate equips the density state with weak convergence augmented by convergence of the second moment and declares

\[
\mathcal E_M=\{f:\int(1+|v|^2)f\le M\}
\]

compact. This is false. Consider

\[
\mu_n=(1-n^{-2})\delta_0+n^{-2}\delta_n.
\]

The measures converge weakly to `delta_0`, all have second moment one, but the limit has second moment zero. No subsequence converges in the topology requiring second-moment convergence. A bounded second moment does not give uniform integrability of the second moment itself.

One needs a higher-moment or exponential-tail bound, or a weaker topology. The compact-containment and action-sublevel arguments built on `E_M` therefore fail.

### 5. The bounded-increment test core is not shown to be compatible with comparison penalties

Restricting to cotangents with bounded collision increment is the right way to make

\[
\int(e^{\Delta p+\psi}-1)dA_f
\]

finite under only energy bounds. However the doubled-variable proof differentiates finite coordinate penalties constructed from an arbitrary convergence-determining family `phi_j`. It does not show that these derivatives belong to the bounded-increment core. If the core is narrowed enough to guarantee bounded `Delta p`, it may no longer generate the claimed state topology or separate all directions required for comparison.

The containment function handles the conserved energy direction only; it does not repair the other penalty cotangents.

### 6. Action compactness is not established

Energy and collision entropy can control mass and some collision tails, but compactness in the declared second-moment topology requires uniform integrability beyond the second moment. The balance equation also gives time equicontinuity only for a specified compact test class. The proof’s one-paragraph appeal to Prokhorov does not establish compact sublevels of the full density–contact action.

### 7. The Hamiltonian continuity modulus is incomplete

For bounded collision increments, the exponential factor is controlled, but continuity of `A_f` in a topology based only on weak convergence plus second moments still requires careful treatment of the product `f f_*`, relative velocity, and possible concentration. The packet does not prove uniformity over the entire energy sublevel.

### 8. All model-specific conclusions inherit B2 and B3

The Lax–Oleinik action, regular recovery paths, microscopic Laplace principle, and Gaussian tangent rely on B2’s unproved joint actual-contact LDP and B3’s invalid process Gaussian theorem. The exact law-state composition cannot replace those inputs.

## Genuine improvement

The candidate correctly stops calling the hierarchy vector a random state, uses the full law as the exact finite object, and restricts the kinetic cotangent so the collision exponential can be finite without high-order velocity exponential moments. These are important typing corrections. They do not prove the claimed hierarchy corrector, compactness, comparison, or convergence theorems.

## Required reconstruction

A viable paper must choose a state topology with genuinely compact Lyapunov sublevels, construct one exact perturbed-test sequence in the domain of the full BBGKY generator, and prove comparison using penalties that remain inside the bounded-increment core. It should then derive semigroup convergence from a separately proved B2 LDP rather than presenting deterministic law composition as closure.

## Recommendation

**Reject.** The active paper remains invalid. The unmaterialized candidate improves the state typing but contains a false compactness theorem, an unsupported order argument for hierarchy truncations, and only a formal BBGKY corrector construction. Every kinetic conclusion remains downstream of unproved B2/B3 interfaces.