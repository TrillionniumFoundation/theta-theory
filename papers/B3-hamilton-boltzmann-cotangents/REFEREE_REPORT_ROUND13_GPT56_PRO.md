# Independent Referee Report — Round 13

**Manuscript:** B3 — *Hamilton–Boltzmann Cotangents*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `6ec4571b1e00c1270022d94aee62db3e6006e3420a041c88d18a641ec83fc25f`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 13 correctly identifies the joint collision-noise coefficient as `Delta p + psi`, restores the pure-contact diagonal variance, retains the microscopic `h/mu` term in fourth moments, and places the inverse covariance on `Ran Sigma^{1/2}`. These are important corrections.

The process-tightness theorem nevertheless contains a direct contradiction with deterministic hard-sphere dynamics. It conditions on the complete microscopic state at a stopping time and then asserts a Poisson-type small-interval conditional fourth-moment bound. Given the complete state, the next collision time is already known. A stopping time can be chosen just before that collision, making one contact occur with conditional probability one. For intervals much shorter than `1/mu`, the resulting fourth moment is of order `mu^{-2}`, while the claimed upper bound is arbitrarily smaller. Thus the Aldous input is false on the stated filtration. The covariance-kernel and second-epi-derivative identifications also rely on unproved closed-range and full-LDP results from B2.

## Decisive objections

### 1. The conditional stopping-time estimate is false for a deterministic flow

The manuscript states, conditional on `F_tau`,

\[
 \mathbb E\left[
 |Z_{\tau+h}^\varepsilon-Z_\tau^\varepsilon|^4
 \mid\mathcal F_\tau\right]
 \le C\left(h^2+{h\over\mu_\varepsilon}\right)
\]

for every bounded stopping time. Its proof explicitly says to condition on the microscopic state at `tau` and restart the deterministic flow.

But the complete hard-sphere state determines the next regular collision time exactly. Fix a small deterministic `h` and let `tau` be the first time at which the remaining free-flight time to a regular collision equals `h/2`, stopped inside a compact non-grazing moment set. This is a stopping time for the full-state filtration. Conditional on `F_tau`, exactly one collision occurs in `[tau,tau+h]` with probability one.

A single contact contributes a jump of order

\[
 \mu_\varepsilon^{-1/2}
\]

to the centered contact fluctuation. Its conditional fourth moment is therefore of order

\[
 \mu_\varepsilon^{-2}.
\]

Choose `h=mu_epsilon^{-3}`. The claimed right side is of order

\[
 h^2+{h\over\mu_\varepsilon}
 =O(\mu_\varepsilon^{-4}),
\]

which is smaller by a factor of order `mu_epsilon^2`. This is a direct contradiction.

Poisson conditional moment estimates are valid when future contacts retain stochastic conditional intensity. They are not valid after conditioning on a deterministic microscopic state that reveals the future collision schedule.

### 2. The filtration is therefore incorrectly typed

If `F_tau` is intended to be a coarser empirical or observation filtration, the proof may not condition on the full microscopic state, and a new conditional cluster theorem is needed. If it is the complete microscopic filtration used in the proof, the estimate above is false.

This distinction is decisive for Aldous tightness, optional projections in C2, and the interpretation of the limiting Gaussian martingale. The manuscript cannot move between the two filtrations without an explicit conditional-disintegration theorem.

### 3. B2 pressure derivatives do not automatically yield the conditional estimate

B2's trajectory expansion is an ensemble average over random initial data. Restarting a deterministic trajectory from a Dirac microscopic state removes that averaging. Uniformity of an unconditional cluster expansion on compact moment sets does not imply a conditional estimate for every individual state, especially states lying immediately before a collision face.

The proof therefore invokes B2 outside the domain of its stated result.

### 4. The perturbative regular chart is assumed rather than obtained

The manuscript says that restricting the B2 real-source ball places every exposed phase in

\[
 cM\le f\le CM,
 \qquad
 \|f-M\|_{W^{2,\infty}(M^{-1})}
 +\|q-1\|_{W^{1,\infty}_w}\le\delta.
\]

Local uniform convergence of first and second pressure derivatives does not imply pointwise Maxwellian comparability or `W^{2,infinity}` regularity of the resulting kinetic path. These require a separate nonlinear regularity theorem for the biased Boltzmann equation. No such theorem appears in B2 or B3.

Thus the energy estimate is proved only after assuming the strongest regularity and smallness properties that the microscopic tilt is supposed to produce.

### 5. Forward energy estimates do not identify the full covariance kernel

The theorem asserts that the residual zero-variance annihilator is exactly a closed endpoint/transport coboundary, citing the closed range of the weak balance operator. The preceding forward well-posedness estimate does not by itself prove closed range of the adjoint constraint map or an observability inequality for all endpoint sources.

A complete proof needs the backward equation, endpoint trace estimates, constraint qualifications, and a theorem identifying the annihilator in the declared dual topology. These are summarized in one sentence.

### 6. The contact random measure and its symmetry quotient are not fully specified

The actual-contact measure carries exchange symmetry, incoming orientation, and the pre/post involution. An isonormal random measure on the unreduced collision space can double count the same physical collision. The paper must define the quotient collision measure, its intensity, and the exact factor in the bracket before the formula

\[
 \int q(\Delta p+\psi)(\Delta p'+\psi')\,dA_f
\]

is a theorem. The corrected coefficient is conceptually right, but the measure space is not constructed.

### 7. The second epi-derivative theorem inherits the unproved full LDP

Finite-dimensional analytic convex duality identifies inverse Hessians only on regular exposed projections. Passing to the full process rate requires the good B2/B1 LDP, projective consistency, equicoercivity, and a proof that finite cylinder projections form a core for the action tangent.

B2 has not proved its lower bound or its physical transversality. Conditional expectations of the proposed Gaussian process cannot substitute for Mosco convergence of the deterministic action.

### 8. Process convergence is not rescued by vanishing jump size alone

It is plausible that jumps of size `mu^{-1/2}` vanish and that an unconditional Gaussian limit may hold. That would require a correct tightness argument based on deterministic-time cumulant bounds, compensator-free martingale approximation, or a coarse filtration. The false conditional estimate is the only Aldous input supplied, so the theorem as written is not proved.

## Genuine improvements recognized

The joint coefficient `Delta p+psi`, the contact diagonal variance, the `h/mu` microscopic term, exact finite centering, and the Cameron–Martin square-root domain should all be retained.

## Dependency assessment

B3 remains conditional on B2's actual-contact LDP and B1's shell theorem, neither of which is established. B4, C1, C2, and D1 cannot use the stated process Gaussianity, covariance kernel, or inverse action form as closed inputs.

## Required reconstruction

The authors must first choose the filtration. For the full microscopic filtration, replace the false conditional moment estimate by a deterministic-schedule tightness argument. For a coarse filtration, prove a genuine conditional cluster/compensator theorem. Only then can the joint Gaussian process and optional-projection results be stated.

## Recommendation

**Reject.** The corrected covariance formula is valuable, but the process theorem rests on a stopping-time estimate directly contradicted by deterministic future knowledge, and the infinite-dimensional kernel/Mosco identifications remain conditional on unproved upstream results.
