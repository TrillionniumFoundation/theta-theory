# Referee Report

**Manuscript:** C1 — Information and Risk-Sensitive Saddles  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

This manuscript collects standard facts about log-Laplace dynamic programming, posterior-state sufficiency, deterministic full observation, and the Schur-complement derivative of an optimized value. These facts are useful typing reminders, but they are not new hard-sphere or billiard theorems.

Two claimed control results are also mathematically inconsistent: the block preparation-error accounting does not close under the stated scaling, and an initial preparation game is replaced by a pointwise-in-time Isaacs Hamiltonian that permits dynamic switching not present in the model.

## Major objections

### 1. The fixed-phase risk-sensitive recursion is generic backward induction

Once a history kernel \(K_\Psi\) is given and player II observes player I’s action, the displayed
\[
\sup_u\inf_v\log\int e^{c+V}dK_\Psi
\]
recursion is standard finite-horizon dynamic programming. The theorem needs measurable-selection hypotheses and a precise policy class, but even after repair it contains no new billiard mathematics. The kernel itself comes from A4’s tautological complete-history Markovization.

### 2. The prepare–act error calculation does not support the theorem

The proof assigns a slow-variation error \(O(\varepsilon m_\varepsilon^2)\) per block and says there are
\(O((\varepsilon m_\varepsilon)^{-1})\) blocks. Summing the displayed per-block errors gives
\[
O(\varepsilon m_\varepsilon^2)\,
O((\varepsilon m_\varepsilon)^{-1})
=O(m_\varepsilon),
\]
which diverges because \(m_\varepsilon\to\infty\).

The condition \(\varepsilon m_\varepsilon^2\to0\) controls only a single block. It does not control the accumulated error claimed in the proof. A normalization or cancellation may change the accounting, but none is stated. The theorem therefore does not follow from its own estimates.

The additional assertion that each controlled block law is \(O(\rho_*^{m_\varepsilon})\) from its stationary information projection also requires uniform mixing under all action-dependent tilts and uniform control of initial distributions—precisely the missing A2/A3 spectral/tower input.

### 3. The posterior state is defined tautologically

The posterior law of the future given observations is, by definition, sufficient for bounded future payoffs. This is not a filtering theorem. To obtain the claimed total-variation contraction and “uniform moment ball,” the paper must specify:

- the observation kernel and dominating measure;
- the refresh mechanism;
- the moment function;
- the transition on infinite histories;
- the minorization constants after Bayes normalization.

A deterministic history shift generally does not satisfy a Doeblin condition merely because an informal “refresh” occurs.

### 4. The full-observation no-go theorem is elementary

If the complete deterministic microstate is known, the future trajectory is known outside the singular null set. This is correct but immediate. It cannot carry a standalone top-journal paper.

### 5. The saddle Hessian is a generic implicit-function calculation

Under a smooth interior saddle and invertible signed Hessian,
\[
D^2W=G_{\phi\phi}-G_{\phi z}G_{zz}^{-1}G_{z\phi}
\]
is the standard envelope/Schur-complement formula. The hard part is proving existence, uniqueness, interiority, smooth dependence, and the correct infinite-dimensional differentiability for the actual path-pressure game. The manuscript assumes all of these.

There is also an internal mismatch between finite/discrete preparation choices and a Fréchet-smooth interior saddle. A finite action set has no such Hessian.

### 6. Initial preparation games do not yield the displayed dynamic Isaacs equation

The paper says preparation is chosen before deterministic evolution. Optimizing an initial preparation means taking one outer \(\sup\inf\) over the already constructed semigroup. The equation
\[
\partial_tU+\sup_u\inf_v
\mathbb H^{u,v}(f,\delta U/\delta f)=0
\]
instead allows \(u,v\) to be reselected at each time/state. That is a different adaptive-control model.

For path-work controls on a fixed phase, actions affect rewards but not the kernel; the Hamiltonian must reflect that distinction. For controls that change preparation, a controlled transition law and switching cost are required. The manuscript supplies neither. The “typed controlled closure” is therefore false as a unifying statement.

## Editorial recommendation

**Reject.** The paper is mostly a collection of textbook identities, and its two genuinely model-dependent control claims are not proved. These observations could become a short typing appendix to another paper, not a top-journal article.
