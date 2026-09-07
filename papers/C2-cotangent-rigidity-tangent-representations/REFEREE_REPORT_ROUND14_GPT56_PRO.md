# Independent Referee Report — Round 14

**Manuscript:** C2 — *Cotangent Rigidity and Tangent Representations*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `7732463d3abb1b908a145cde978e4c58d59192a0572298e533094248bce54af4`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 correctly separates the weighted strict topology used for Radon duality from the stronger Hölder/anisotropic/graph spaces used for response. It also corrects the constant direction in the invariant-integral quotient and uses the real coercive part of a sectorial form.

The principal common-form theorem is still not well typed. The Hilbert pairing varies with the parameter, yet the resolvent derivative omits its derivative; the resolved subspace is assumed only to lie in the form domain while the memory formula uses the unbounded operator compression `P L P`; and the uniform form equivalence is simply imported from A4/B4, where it has not been proved. The rigidity and likelihood sections likewise assume their main model-specific interfaces.

## Decisive objections

### 1. The dual pullback is not automatically an embedding

The continuous inclusion

\[
\iota_m:\mathscr A_W^m\to C_W(E)
\]

induces a pullback

\[
\iota_m^*:C_W(E)^*\to(\mathscr A_W^m)^*.
\]

This map is injective only if the image of `iota_m` is dense enough to separate all Radon measures. Continuity alone does not make it an embedding. The manuscript does not prove density of the strong cylinder algebra in the weighted strict space on the graph-completed path state.

Without injectivity, distinct invariant Radon cotangents may become the same strong functional, invalidating the claimed functorial crossing between the two topologies.

### 2. Rational-time annihilation does not automatically give full flow invariance

A measure annihilating all rational-time coboundaries is invariant under rational times. Extending this to every real `t` requires strong continuity of

\[
U\mapsto U\circ\Theta_t
\]

in the weighted strict topology and continuity of the weighted moment under the flow. These hypotheses are not stated or proved on the graph-completed, possibly singular path space.

The Radon quotient theorem may be repairable, but the proof as written omits a necessary dynamical continuity interface.

### 3. Full pressure-functional equality is not connected to the claimed hard-sphere quotient

For the Sinai symbolic phase, equality of equilibrium Gibbs measures can imply a Hölder coboundary theorem under a precise Livšic hypothesis. For the finite-time hard-sphere source problem, the manuscript instead invokes B3's covariance kernel.

Equality of the complete nonlinear perturbation functional is stronger than equality of its first two derivatives, while B3 identifies only a local Gaussian covariance kernel and an asserted balance annihilator. The proof does not show that all higher source variations vanish exactly on the same quotient or that the pressure is strictly convex modulo that gauge on the full source neighborhood.

Thus the hard-sphere rigidity conclusion does not follow from the stated B3 input.

### 4. The common form domain is assumed rather than constructed

The section begins with “Assume the estimates proved in A4/B4” and writes uniform equivalence of the real form norms. A4 constructs a linear Doob suspension generator; B4 constructs a nonlinear Nisio semigroup. B4 does not supply a sectorial linear form family comparable to A4's form.

No common cylinder core, closability theorem, sector bound, or uniform coercivity proof is given for either platform family. The main theorem is therefore conditional on the central assertion it advertises.

### 5. Differentiating the resolvent omits the derivative of the Hilbert pairing

The weak equation is

\[
z(u,v)_{H_\eta}+a_\eta(u,v)=\langle f,v\rangle.
\]

The Hilbert spaces `H_eta` and their inner products vary with `eta`. Differentiating this equation produces a term

\[
z\,D_\eta( u,v)_{H_\eta},
\]

in addition to the derivative of `a_eta`. The displayed formula

\[
D(z-L_\eta)^{-1}
=(z-L_\eta)^{-1}(DL_\eta)(z-L_\eta)^{-1}
\]

is valid only after all operators have been transported to one fixed ambient Hilbert space with the metric derivative included in `DL_eta`. The manuscript does not construct such a transport.

A common form domain is not the same as a common Hilbert pairing.

### 6. The memory compression is undefined on the stated resolved space

The resolved family is assumed to satisfy

\[
R_\eta\subset V,
\]

where `V` is the form domain. The memory formula then uses

\[
P_\eta L_\eta P_\eta.
\]

For a sectorial form, membership in the form domain does not imply membership in the operator domain `D(L_eta)`. Thus `L_eta P_eta g` need not exist for a resolved observable `g in V`.

The compression must be written at the form level or the resolved family must be proved to lie in a common operator domain. Neither is done.

### 7. The inverse compressed resolvent needs a uniform singular-value theorem

The derivative of

\[
C_\eta(z)^{-1}
\]

is controlled only where `C_eta(z)` is invertible with a quantitative lower singular-value bound. Avoiding the discrete poles of the final Schur complement on a compact set is not enough for a uniform Bromwich estimate on an unbounded vertical line.

The paper imports A4's vertical theorem but does not prove that the inverse and its parameter derivative preserve the required integrable bounds.

### 8. The likelihood theorem assumes its conclusion-level hypotheses

The theorem begins by assuming A4 conditional-kernel rough convergence and a B3 uniform `L^(1+delta)` likelihood bound. Neither is proved in the cited papers. Stable convergence of filtrations and optional projections is itself delicate; finite-dimensional path convergence plus uniform integrability is insufficient without a theorem on convergence of conditional expectations.

The proof says to approximate by finite-history cylinders and remove the approximation “using kernel convergence,” but no uniform approximation statement for the complete filtration is given.

### 9. The Brownian optional projection need not retain the stated terminal representation without identification of the filtration

A positive martingale in a Brownian filtration can be represented as a stochastic exponential under suitable strict positivity and integrability. The paper must prove that the limiting resolved filtration is genuinely Brownian and has the martingale representation property. “Nondegenerate resolved Brownian filtration” is inserted as an assumption, not derived from the contraction.

### 10. The synthesis remains dependency driven rather than theorem driven

The Radon quotient and source/state chain rules are abstract functional analysis. The substantive model-specific claims—pressure rigidity, common form response, memory differentiation, and likelihood convergence—are all imported from A2–A4 or B2–B4, whose interfaces remain open.

## Required reconstruction

A credible paper must:

1. prove density before calling the dual pullback an embedding;
2. establish full-time continuity of the weighted flow action;
3. transport every form to one fixed Hilbert space and include the metric derivative;
4. place resolved observables in a common operator domain or use a purely form-level memory formula;
5. prove quantitative inverse bounds for the compressed resolvent; and
6. state a genuine filtration-convergence theorem for optional projections.

## Recommendation

**Reject.** The two-topology distinction is correct, but the common-form and memory constructions remain ill typed, and the likelihood theorem assumes the unresolved model-specific convergence it is meant to synthesize.