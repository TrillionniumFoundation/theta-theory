# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B4 — *Nonlinear Kinetic Semigroups from Deterministic Hard-Sphere Hierarchies*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `eefcbcf38e4764146767d8f63254795eae60f4c0`

## Executive assessment

Round eight fixes two genuine defects. Static preparation is removed from the transition action, restoring formal additivity, and the corrector is written as a terminal-value Duhamel equation with the correct sign. The manuscript also abandons the impossible “entire cutoff equal to one on an open box.”

The new semigroup theorem is still not established. The resolvent construction conflates a generator acting on states with a generator acting on nonlinear observables, and Stone–Weierstrass approximation does not give density in a `C_b^2` generator graph norm. The comparison argument restores coercivity by sending a slope bound `R` to infinity, but the Boltzmann Hamiltonian's continuity constants grow exponentially in `R`; a state mismatch of order `1/R` is not enough. The theorem assumes only continuity on each bounded cotangent ball, which is logically insufficient for the limit. The corrector summability and microscopic generator convergence are also asserted without the full BBGKY estimates they require.

## Genuine repairs recognized

The following changes should be retained:

- the transition action contains dynamic cost only;
- the terminal-value corrector has zero terminal remainder;
- the exact state includes the contact ledger;
- the weak-energy topology remains separate from moment convergence;
- nonanalytic cylinders are no longer declared analytic by fiat;
- the comparison proof acknowledges the bounded-gradient/coercivity tradeoff.

## Major mathematical objections

### 1. The resolvent core mixes the state generator and the observable generator

The manuscript writes

\[
J_{\lambda,\varepsilon}
=(I-\lambda\mathbb A_\varepsilon)^{-1}
\]

and then applies it to a state `z` inside

\[
F_{m,\lambda}(z)=
\phi(\Pi_mJ_{\lambda,\varepsilon}z).
\]

This treats `A_epsilon` as a generator on the linear law/hierarchy state. The claim that `F_{m,lambda}` belongs to the generator domain is a statement about the induced generator on nonlinear observables. Passing from one to the other requires a chain rule on the state space, differentiability of the flow, and domain stability. None is stated.

For a Markov generator, the product formula generally contains a carré-du-champ term; for a deterministic derivation, product stability has a different proof. The text alternates between these two settings.

### 2. Stone–Weierstrass does not prove graph-core density

Stone–Weierstrass gives uniform approximation of continuous scalar functions on a compact set. It does not give convergence of first and second derivatives, generator images, collision increments, or the `C_b^2` graph norm asserted in Lemma `r8-b4-core`.

Likewise, strong convergence `J_lambda -> I` on the state Banach space does not automatically make the nonlinear cylinder generators converge. A genuine graph core must be proved by a smoothing/commutator theorem for the actual augmented generator.

### 3. The finite corrector theorem assumes the entire triangular estimate

The theorem states the uniform summability

\[
\sum_j
(\|c_j^\varepsilon\|+
\|\mathbb A_\varepsilon c_j^\varepsilon\|)<\infty.
\]

The proof says that a `j`-ledger defect has factor `C^j/j!`. No definition of `D_j^epsilon`, no recursive cancellation formula, and no graph-norm estimate for the generator image are supplied. Connected BBGKY coefficients typically carry their own factorial and velocity/boundary losses; a ledger label count does not by itself give the displayed bound.

The terminal-value sign is correct, but the existence and normal convergence of the infinite corrector remain the missing theorem.

### 4. The two-scale comparison limit is invalid under the stated assumptions

At fixed `R`, the doubled cotangents have norm at most `R` and the states are separated by at most `C/R`. To pass `R -> infinity`, the proof needs a modulus satisfying

\[
\omega_R(C/R)\longrightarrow0,
\]

where `omega_R` is the Hamiltonian's state-continuity modulus on the radius-`R` cotangent ball.

The theorem assumes only continuity for each fixed `R`. That does not imply the displayed joint limit. For the actual collision Hamiltonian,

\[
H(f,p)\sim\int ff_*B(e^{\Delta p}-1),
\]

the Lipschitz constant in `f` grows like `e^{cR}`. The product

\[
e^{cR}\frac1R
\]

diverges. Thus the restored coercivity drives the cotangent into a region where continuity becomes exponentially worse.

“Exponential containment” controls the state tail; it does not control this local source-growth problem.

### 5. The metric penalty is not shown to generate admissible cotangents

The manuscript assumes a bounded compatible metric `d_B` and differentiates it. A general compatible metric on an infinite-dimensional weak topology is not smooth, and its subgradients need not be finite combinations of the bounded collision-increment tests defining the Hamiltonian core.

A Tataru/Ekeland comparison theorem requires an explicit variational distance or a smooth cylindrical approximation with quantified derivatives. None is constructed.

### 6. The action compactness and closure needed for the semigroup are not proved here

Formal time additivity is correct. But the Lax–Oleinik semigroup also requires compactness or recovery under concatenation, closure of the balance equation, and lower semicontinuity of the perspective entropy in the selected path topology. Round eight cites B2 for these facts, while B2's trace state and regularization are not valid.

### 7. Microscopic generator convergence is circularly reduced to upstream conclusions

The final proof invokes B2 compact containment and lower recovery, the graph core, and the infinite corrector. Those are exactly the unresolved interfaces. A half-relaxed-limit theorem cannot be applied until the upper and lower nonlinear generators and a comparison theorem are genuinely established.

### 8. The exact microscopic state remains underspecified

An augmented law/contact-ledger state is a sensible idea, but the paper does not define its Polish/Banach topology, the domain of the augmented BBGKY generator, or the relation between ledger correlations and the nonlinear path cylinders. The resolvent and coordinate projections therefore have no complete functional-analytic setting.

## Dependency assessment

B4 remains downstream of the unproved B2 dynamic LDP and B3 fluctuation geometry. C1's kinetic game and D1's dynamic commutation theorem cannot use the Round-8 semigroup or comparison labels as closed results.

## Required reconstruction

A viable proof must:

1. define the augmented state and its linear generator;
2. construct a common nonlinear observable graph core with genuine derivative/generator approximation;
3. prove the full triangular corrector estimates;
4. formulate comparison with a penalty whose coercivity and exponential source growth are quantitatively compatible; and
5. establish compact action sublevels and recovery independently of the desired semigroup limit.

## Recommendation

**Reject.** The static/dynamic accounting and corrector sign are repaired, but the graph core is not proved and the comparison argument fails at the `R -> infinity` limit for an exponential Boltzmann Hamiltonian.