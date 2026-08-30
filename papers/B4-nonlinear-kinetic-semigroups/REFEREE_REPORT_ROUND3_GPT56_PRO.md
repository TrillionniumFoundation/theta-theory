# Round-Three Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — *Microcanonical Excess-Pressure Semigroups and Kinetic Theta-Generators*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round3-full-positive-closure-11paper-2026-08-30@6a31720e5b0b6ab156b575f947596f9b66f56efe`  
**Controlling module:** `ROUND3_POSITIVE_CLOSURE.tex`, blob `be18b04e57d6646ef4763819425903f82a43811d`

## Executive assessment

The paper now makes the correct conceptual distinction between the exact finite-volume state—the correlation/BBGKY hierarchy—and the limiting one-particle density. It also constructs a candidate action semigroup from the B2 density/collision rate rather than inferring density Markovianity from a generic history tower. These are important improvements.

The proposed proof does not work. The correlation correctors are asserted rather than constructed, the infinite-dimensional comparison theorem is only a formal doubled-variable outline, and the chosen weighted containment function is incompatible with the Gaussian velocity law. In particular, the paper chooses a polynomial moment of degree `m>6` and claims that a positive exponential source in that moment is controlled by the B2 Gaussian source expansion. A Maxwellian/Gaussian tail has no exponential moment of `|v|^m` for `m>2`. The key compact-containment lemma is therefore false.

The proof also says that elastic collisions conserve the polynomial weight `|v|^m`; they conserve only mass, momentum, and kinetic energy. This invalidates the Lyapunov estimate used in the comparison argument. The remaining semigroup and microcanonical conclusions depend on the unproved B1–B3 chain.

## Improvements relative to the preceding circulation

1. The exact finite state is no longer declared to be the empirical density.
2. The paper attempts a perturbed-test/corrector route from the hierarchy generator to the kinetic Hamiltonian.
3. The limiting semigroup is defined variationally from an additive density/collision action.
4. The preparation multiplier is retained as an augmented static coordinate rather than reoptimized at every time block.
5. The finite-volume covariance normalization is delegated to the corrected B3 theorem.

These are the correct architectural choices. They need a valid analytic implementation.

## Major mathematical objections

### 1. The exponential containment source does not exist for `m>2`

The paper fixes `m>6` and uses

\[
\Upsilon(f)=\langle1+|v|^m,f\rangle.
\]

It then claims that the B2 cluster theorem remains analytic after adding a small positive multiple of `1+|v|^m` to the particle source, and applies Chernoff’s inequality.

Under a Gaussian/Maxwellian velocity activity, for every `delta>0` and every `m>2`,

\[
\int_{\mathbb R^3}
\exp\{\delta|v|^m\}
\exp\{-\beta|v|^2\}\,dv
=
\infty.
\]

Thus even the one-particle exponential moment is infinite. No cluster expansion can create an analytic positive source where the underlying activity is nonintegrable. The B2 source class itself was quadratic in velocity, not degree `m>6`.

Consequently Lemma `r3-b4-containment`, the source-uniform moment estimate, and every later use of exponential compact containment in this topology are invalid.

### 2. Elastic collisions do not conserve the chosen polynomial moment

The proof of Hamiltonian continuity says that “elastic collisions conserve kinetic energy and the polynomial weight grows only through free transport.” For `m>2`,

\[
|v'|^m+|v_*'|^m
\neq
|v|^m+|v_*|^m
\]

in general. Only the quadratic energy is conserved. Higher moments can increase or decrease at a collision.

Therefore the asserted Lyapunov estimate

\[
\mathbb H(f,D\Upsilon,0)
\le C(1+\Upsilon(f))
\]

is not established. Worse, the Hamiltonian contains `exp(Delta D Upsilon)`, whose high-velocity growth is incompatible with Gaussian tails for a polynomial of degree above two.

This is a direct mathematical error in the comparison framework.

### 3. The proposed moment balls are not compact in the declared weighted topology

A bound on the `m`-th moment gives tightness in ordinary weak topology and uniform integrability for lower-order weights. It does not make

\[
\{f:\langle1+|v|^m,f\rangle\le M\}
\]

compact in a topology that tests functions growing like `|v|^m`. Mass can escape to larger velocities while preserving the moment bound and fail convergence against the top-order weight. One needs a strictly stronger moment, a superlinear de la Vallée–Poussin function, or a weaker topology.

The action semigroup, attainment argument, and doubled-variable maximum therefore lack the compact state set they use.

### 4. The recursive correlation correctors are not constructed

The key lemma claims correctors `c_j[F]` satisfying

\[
\mathscr H_\epsilon F_\epsilon^{(K)}
=
\mathbb H(g_1,\delta F/\delta f,\psi)
+O(\epsilon^\alpha+\rho^K).
\]

The proof says to order connected defects by label number and define each corrector as a negative time integral transported by the free hierarchy. This does not establish:

- a solvable cohomological/Poisson equation for each defect;
- symmetry and boundary compatibility at hard-sphere contacts;
- convergence of the infinite corrector series;
- independence of the observation horizon;
- control of derivatives produced by the exponential nonlinear generator; or
- the claimed uniform remainder on hierarchy moment balls.

A connected-cluster estimate for trajectories is not automatically a perturbed-test theorem for the BBGKY generator.

### 5. The “upper and lower generator convergence” proof is circular

The theorem obtains both inequalities by first letting `K→∞` in the unproved corrector lemma and then approximating arbitrary hierarchies by finite connected truncations. Positivity of factorial moments does not order nonlinear logarithmic generators, so it does not preserve upper and lower inequalities in the manner claimed.

No domain for the hierarchy generator, graph convergence, or recovery sequence is specified.

### 6. The exact hierarchy semigroup is not typed on a stable function class

`S_epsilon(t)F(G)` is introduced for terminal density cylinders via a factorial expansion. After one application it is a functional of the complete hierarchy, not generally another density cylinder. To write

\[
S_\epsilon(t+s)=S_\epsilon(t)S_\epsilon(s),
\]

the authors must define an operator on a class of hierarchy functionals closed under the evolution and exponential transform. “The correlations determine every expectation” proves a tower for the underlying law, but not the stated nonlinear semigroup on the declared domain.

### 7. The infinite-dimensional comparison theorem is only a template

The proof doubles finitely many coordinates, sends the number of coordinates to infinity, and invokes Hamiltonian continuity. It does not prove that maxima exist, that the cylinder penalties approximate the weighted metric uniformly on the relevant compact set, or that the exponential collision Hamiltonian satisfies the required continuity and coercivity under the cotangents generated by the penalty.

Because the containment function is invalid, the maximizers are not even confined to a valid compact moment set. The claimed uniqueness theorem therefore has no proof.

### 8. The Lax–Oleinik semigroup depends on B2’s unproved full action

The variational construction would be meaningful if B2 supplied a good additive density/collision rate with recovery sequences. B2 currently derives the full entropy action from a small source ball and does not prove the actual-collision lower bound. Compact sublevels, attainment, and stability of the action used here are therefore unavailable.

### 9. The lifted microcanonical multiplier is not fully justified

The formula retains an initial multiplier `lambda` as a static state and applies a terminal infimum. This is a plausible way to avoid blockwise reoptimization, but the paper does not define how `S_{s,t}^lambda` depends on `lambda` after the initial time, or prove that the augmented state is sufficient for conditional composition. Once a concrete density `f_s` is fixed, the transition action normally depends on `f_s`, not on the original grand-canonical activity label.

A disintegration theorem connecting the source-dependent initial saddle to intermediate conditional laws is required.

### 10. The Gaussian theta contraction is downstream of an unproved process CLT

B3 does not establish tightness of the joint density/collision fluctuation field. Expanding the limiting pressure to second order gives finite-dimensional Gaussian cumulants, not convergence of nonlinear semigroups or likelihood ratios on path space.

### 11. The controlling manuscript is not standalone

The active paper is a preamble plus one closure module. The hierarchy generator, hard-sphere boundary operator, source domains, B2 action, viscosity topology, and B1 saddle are not given at submission-level completeness.

## Editorial recommendation

**Reject.** The hierarchy-state and action-semigroup architecture is a genuine improvement, but the current analytic framework contains a direct nonintegrability error and a false collision-moment claim. A viable reconstruction should use a Gaussian-compatible quadratic/exponential weight or a carefully chosen lower-order polynomial topology, prove an actual hierarchy perturbed-test theorem, and establish comparison on a valid compact-containment space. It must remain downstream of completed B1–B3 theorems.