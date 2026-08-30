# Round-Four Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — *Microcanonical Excess-Pressure Semigroups and Kinetic Theta-Generators*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round4-referee-positive-closure-11paper-2026-08-30@cbee394d6ee33db471b63420131314bd05909a0f`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `c18b1ea8cc9b7e57ee46122ccc52ab32d554bcb0`

## Overall assessment

The revision correctly abandons the nonintegrable high-order velocity Lyapunov source from the previous circulation and moves to an energy/subquadratic topology. It also recognizes that the exact finite state is the complete correlation hierarchy rather than the one-particle density.

The new hierarchy functional “algebra” is not an algebra, the exact nonlinear tower is ill typed, and the corrected-generator construction does not address the BBGKY coupling to higher marginals at the required domain level. More decisively, finite second energy does not make the exponential collision Hamiltonian finite for the declared subquadratic cotangents. The Hamiltonian continuity and comparison theorem therefore fail on the stated state space.

## Major objections

### 1. The declared hierarchy functional space is not closed under multiplication

The manuscript defines

\[
\mathcal F(G)=\sum_{k\ge0}\frac1{k!}\langle F_k,g_k\rangle
\]

and calls the collection an algebra closed under multiplication. Pointwise multiplication gives

\[
\mathcal F(G)\mathcal G(G)
=
\sum_{k,l}\frac1{k!l!}
\langle F_k,g_k\rangle\langle G_l,g_l\rangle,
\]

which is quadratic in the hierarchy coordinates. It is not generally representable as another linear series `sum <H_n,g_n>` on an arbitrary correlation state. Such a representation would require factorization relations between `g_{k+l}` and `g_k tensor g_l`, which do not hold for correlated laws.

Thus `mathfrak A_{alpha,beta}` is not the claimed algebra, and the assertions about closure under exponentiation, conditional expectation, and the nonlinear semigroup domain do not follow.

### 2. The exact hierarchy tower mixes a deterministic law state with a random microstate

A correlation hierarchy `G` determines the ensemble law and evolves deterministically under the BBGKY/Liouville semigroup. The expression

\[
\mathscr S_\varepsilon(t)\mathcal F(G)
=\mu_\varepsilon^{-1}\log
\mathbb E_G e^{\mu_\varepsilon\mathcal F(G_t)}
\]

is therefore ambiguous. If `G_t` is the deterministic evolved hierarchy, the expectation is redundant and the logarithm equals `mathcal F(G_t)`. If `G_t` denotes a random empirical hierarchy of a microstate, that object and its relation to the deterministic correlation hierarchy are not defined.

The risk-sensitive tower naturally acts on functions of the microscopic state, or on conditional laws/history states. It is not obtained by simply treating an unconditional correlation hierarchy as both a state variable and a random observable. Proposition `prop:r3-b4-hierarchy` is consequently not a well-typed exact identity.

### 3. The “exact connected `j`-particle propagator” ignores BBGKY coupling

The finite `j`-particle BBGKY component is not a closed semigroup: its evolution couples to the `(j+1)`-particle marginal through the collision boundary. The manuscript introduces

\[
\mathscr U_{\varepsilon,j}^{\rm conn}(t)
\]

as an exact `j`-particle connected propagator and uses it to solve a backward Duhamel equation cancelling the complete order-`j` defect. No operator, domain, boundary condition, or closure theorem for this propagator is given.

A connected cluster coefficient can be represented by a Duhamel series, but it is not an autonomous hard-sphere semigroup at fixed label number in the manner asserted. Therefore the recursive correctors are formal, and the claim that they belong to the nonlinear generator domain is unproved.

### 4. Choosing `K(epsilon)` does not establish convergence of the corrected tests

The bound

\[
\|\mathfrak c_j[F]\|\le C_F(CT)^{j-1}
\]

is stated in an unspecified hierarchy norm and does not include the dependence on `epsilon`, derivative order, or analytic-radius loss. The finite-volume coefficient carries factors `mu_epsilon^{1-j}`, but the functional evaluation on `g_j` may scale with the density and combinatorics. The proof does not show that the infinite corrector sum converges to zero uniformly on the microscopic state space or that the generator error remains uniform as `K(epsilon)->infinity`.

The perturbed-test theorem is therefore not established.

### 5. Energy compactness does not make the exponential Hamiltonian finite

The state space controls only

\[
\int(1+|v|^2)f(dv)<\infty.
\]

The test class allows a “subquadratic” collision increment, for example growth like

\[
\Delta p\sim |v|^{2-\delta}.
\]

Finite second moment does not imply

\[
\int e^{c|v|^{2-\delta}}f(dv)<\infty.
\]

A probability density can have a polynomial tail with finite second moment and infinite exponential moment of every positive subquadratic power. For such an `f`, the collision Hamiltonian

\[
\int ff_*B\left(e^{\Delta p+\psi}-1\right)
\]

may be infinite.

Hence the Hamiltonian is not finite or continuous on the declared energy sublevels and cylinder-cotangent class. The proof's statement that “energy uniform integrability controls every tail” is false for an exponential of a subquadratic function.

One must either restrict cotangents to bounded collision increments or impose uniform stretched-exponential velocity moments on the state domain.

### 6. The Hamiltonian continuity lemma is false as stated

Weak convergence with a uniform second-moment bound controls integrals of functions growing strictly below quadratic, but not their exponentials. The difference-of-exponentials estimate used in the proof has no uniform integrable majorant. Therefore

\[
|\mathbb H(f,p,\psi)-\mathbb H(g,q,\psi)|
\le C_M(d_{2-\delta}(f,g)+\cdots)
\]

cannot hold on all energy sublevels.

This invalidates the doubled-variable comparison proof and the asserted uniqueness of the HJ equation.

### 7. The containment proof conflates path compactness with energy conservation

Quadratic energy conservation controls the one-time velocity tails, but compact containment of the empirical path in a Skorokhod/weak topology also requires a quantitative time modulus for all convergence-determining tests. The proof invokes collision mass and exact balance without deriving an exponential modulus estimate uniform over complex sources.

Moreover, a complex tilted “law” is not a probability measure, so statements about probabilities uniformly under a compact complex source ball are not meaningful without passing to absolute weights and normalizing real parts.

### 8. The action semigroup uses a rate not proved by B2

The Lax--Oleinik formula is formally correct if B2 supplies a good additive action with compact sublevels and recovery sequences. B2 does not prove that theorem. The present paper simply imports lower semicontinuity, compactness, and action-dense smooth pairs.

Even abstractly, the supremum over balanced paths must specify the terminal density topology and show that concatenation preserves all integrability conditions. These details are absent.

### 9. The comparison proof is not an infinite-dimensional comparison theorem

A finite-coordinate doubling penalty approximates the weak metric, but the Hamiltonian depends quadratically on the full density and exponentially on the collision increment. Passing `J -> infinity` requires uniform approximation of all Hamiltonian terms, not only the metric tail. No containment of the dual gradients or coercive penalization in the source topology is shown.

The proof is a template, not a comparison theorem.

### 10. The microcanonical constraint surface is misstated for nonconserved preparation observables

The manuscript says `C(f)=a` may include “any exactly conserved initial constraints,” then restricts the dynamic path to remain in `E_a`. The macro observables `chi_j` used in B1 need not be conserved by hard-sphere flow. If they are merely preparation moments, the path should not remain on their initial constraint surface.

Thus the claimed equivalence between the constrained semigroup and the B1 source-dependent initial saddle is valid only for actual collision invariants, not for arbitrary prepared moments. The statement must distinguish static initial constraints from dynamically conserved quantities.

### 11. The Gaussian semigroup conclusion is downstream of an unproved process CLT

B3 does not presently establish process-level Gaussian convergence. Expanding a limiting semigroup and saying higher cumulants vanish is insufficient to prove convergence of transition semigroups uniformly over initial states. The quadratic theta generator remains formal.

## Status of previous objections

The revision genuinely fixes the impossible positive `|v|^m`, `m>6`, exponential source and uses exact quadratic energy as a Lyapunov quantity. This removes one direct error. It does not provide the additional exponential velocity integrability needed for the nonlinear collision Hamiltonian on unbounded cotangents.

## Minimum viable reconstruction

A rigorous paper should:

1. define the exact nonlinear semigroup on microscopic states or conditional hierarchy laws, not an unconditional deterministic hierarchy;
2. construct a genuine functional algebra closed under the required operations;
3. prove a perturbed-test theorem using the full BBGKY/Duhamel hierarchy with domains;
4. restrict the HJ test core to bounded collision increments, or strengthen the state space to uniform stretched-Gaussian moments;
5. prove compact containment and comparison in those compatible spaces; and
6. treat initial preparation moments separately from conserved dynamic constraints.

## Recommendation

**Reject.** The revised energy topology is better chosen, but the exact finite-state tower, nonlinear-generator convergence, Hamiltonian continuity, and comparison theorem are not valid on the declared spaces.