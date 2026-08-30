# Revision-Round Referee Report — GPT-5.6 Pro

**Manuscript:** C1 — *Typed Control, Information, and Saddle Envelopes for Kinetic Cotangent Phases*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed source:** `main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`, manuscript blob `fc6f823263b7b74f5dec7be1d1efedfb6306d053`  
**Revision provenance:** no revised C1 manuscript is present on the repository's discoverable eleven-paper revision ref; the controlling `main` source is reviewed.

## Overall assessment

This revision makes one real improvement: the previous multiblock prepare–act theorem with an accumulated \(O(m_\varepsilon)\) error has been removed. The manuscript now distinguishes a fixed prepared law, a one-time preparation decision, and bounded path-work decisions, and it explicitly excludes adaptive control of microscopic collision geometry.

The remaining paper, however, consists mostly of generic envelope, posterior-sufficiency, and deterministic-observation facts. Its sole dynamic closure is still internally inconsistent: after declaring that preparation is chosen before evolution and that adaptive law control is excluded, it writes a pointwise-in-time Isaacs Hamiltonian that permits controls to be reselected as the state evolves. This solves a different game. The paper therefore does not contain a new top-journal theorem.

## Major objections

### 1. The saddle-envelope theorem is a standard implicit-function calculation

Under twice Fréchet differentiability, a unique interior saddle, and invertibility/coercivity of \(G_{zz}\), the formula

\[
D^2V
=
G_{\phi\phi}-G_{\phi z}G_{zz}^{-1}G_{z\phi}
\]

is the standard envelope/Schur-complement identity. At fixed \(z\), the Hessian of a log-Laplace functional is \(artheta\) times covariance. These are correct generic facts.

The actual mathematical work would be to prove, for the kinetic path-pressure game, existence and uniqueness of the saddle, interiority, Fréchet smoothness, closed-range properties, and invertibility of the infinite-dimensional signed Hessian. The manuscript assumes all of these. Thus the theorem is not a hard-sphere or kinetic contribution.

### 2. There is a mismatch between finite preparation choices and smooth optimizer response

The control section later defines a “fixed finite set of preparation choices,” while the saddle theorem differentiates a smooth interior optimizer \(z^*(\phi)\) and uses \(G_{zz}^{-1}\). A finite action set has no Fréchet derivative or interior Hessian of this kind.

The paper must choose between a discrete preparation game, where values are upper/lower envelopes and generally nonsmooth, and a smooth finite- or infinite-dimensional parameter manifold satisfying the implicit-function hypotheses. It currently combines incompatible models.

### 3. Posterior-history sufficiency is true by definition, not a filtering theorem

The conditional law of the future given the observations is sufficient for bounded future functionals by construction. The Bayesian tower is likewise automatic. This does not provide a finite-dimensional filter, stability estimate, contraction, or implementable state equation.

The manuscript now correctly says that finite-dimensional filtering requires a separate approximation theorem. With that qualification, the proposition is a modeling definition rather than a research result.

### 4. The complete-observation no-go theorem is elementary

For deterministic hard-sphere dynamics outside a null singular set, the future is a measurable function of the complete microstate. Hence conditional variance vanishes under full observation. This is correct and useful as a warning against artificial filtering noise, but it is immediate and cannot carry a standalone top-journal paper.

### 5. The controlled HJ equation changes the timing and admissible strategy class

The manuscript states that preparation decisions occur before deterministic evolution and that path-work decisions evaluate a fixed prepared phase. For such a one-time preparation game, the value should have the form

\[
\sup_u\inf_v S_t^{z(u,v)}\Phi,
\]

where each \(S_t^z\) is the already constructed semigroup for a fixed preparation. The optimization sits outside the evolution.

Instead, the paper writes

\[
\partial_tU+\sup_u\inf_v
\mathbb H^{u,v}\left(f,\frac{\delta U}{\delta f}\right)=0.
\]

This equation permits \(u\) and \(v\) to be chosen anew at each time and state. It is the dynamic programming equation for an adaptive controlled kinetic law, not a one-time preparation choice. The manuscript explicitly excludes precisely that model.

This is a statement-level contradiction, not a missing estimate.

### 6. Reward control and law control are conflated

A bounded path-work decision on a fixed prepared phase changes the running or terminal reward but not the transition law or kinetic Hamiltonian. A preparation decision changes the initial law or selects one fixed phase. An adaptive law control changes the generator/Hamiltonian through time. These produce three different dynamic programming structures.

The displayed \(\mathbb H^{u,v}\) merges them without specifying whether \(c^{u,v}\) is a reward, whether \(\Theta(z(u,v))\) changes the law once or continuously, or what policy class is admissible. “Typed” terminology does not resolve the mathematical distinction.

### 7. The kinetic phases imported into the game are not established

The fixed-phase semigroups, cotangents, and collision Hamiltonians used by C1 depend on B1–B4. B1 is false on its source class; B2's marked LDP is unproved; B3's cotangent uniqueness is false; and B4's density semigroup is not constructed. C1 cannot treat these phases as available state dynamics.

### 8. The paper has insufficient independent novelty

After deleting the inconsistent controlled HJ claim, the content is:

- a standard envelope theorem;
- posterior-law sufficiency;
- deterministic full-observation triviality; and
- a taxonomy of decision timing.

This could be a useful typing appendix or modeling note, but not an Annals/Acta/Inventiones/JAMS article.

## Status of prior objections

The removal of the divergent block-error theorem is a genuine correction and should be acknowledged. The revision also improves the taxonomy of control interfaces. It has not aligned the final Isaacs equation with that taxonomy, so the central control-theoretic inconsistency remains.

## Required reconstruction

The paper should be reduced to one precisely defined game. For a one-time preparation game, optimize outside fixed phase semigroups. For reward-only control, retain the fixed kernel and put controls in the cost. For a genuine adaptive kinetic game, define controlled transition laws, nonanticipative strategies, switching rules, compactness, and a comparison theorem. These models should not share one theorem without explicit equivalence.

## Editorial recommendation

**Reject.** The revision closes one prior defect, but the surviving dynamic equation solves a different game from the one the manuscript declares, and the remaining results are generic rather than top-journal contributions.
