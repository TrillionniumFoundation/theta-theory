# Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C1 — Information and Risk-Sensitive Saddles  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**  
**Review object:** SHA-256-pinned eleven-paper source archive `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`

## Executive assessment

The paper collects several valid generic observations: log-Laplace backward induction, posterior-state sufficiency, determinism under complete observation, and the Schur-complement formula for the Hessian of a smooth optimized value. These are useful typing reminders, not new billiard or hard-sphere theorems.

The two model-dependent claims fail on their own terms. First, the stated per-block preparation error accumulates to a divergent total under the chosen scaling. Second, an initial one-time preparation game is replaced by a dynamic Isaacs Hamiltonian that allows the controls to be reselected at every time and state. That is a different control problem.

## Major mathematical objections

### 1. The fixed-phase risk-sensitive recursion is standard backward induction

Once a measurable kernel and admissible action classes are supplied, a recursion of the form

\[
\sup_u\inf_v\log\int e^{c+V}\,dK
\]

is textbook finite-horizon dynamic programming. The manuscript still owes measurable-selection, policy, and information-pattern hypotheses, but satisfying them would not create a top-journal contribution.

Moreover, the kernel is inherited from A4's complete-history Markovization. Retaining the complete past makes the recursion exact but does not solve memory reduction or identify a tractable sufficient statistic.

### 2. The prepare–act block error does not close

The proof states a slow-variation error of order

\[
O(\varepsilon m_\varepsilon^2)
\]

per block and uses

\[
O((\varepsilon m_\varepsilon)^{-1})
\]

blocks. Summation gives

\[
O(\varepsilon m_\varepsilon^2)
\,O((\varepsilon m_\varepsilon)^{-1})
=
O(m_\varepsilon),
\]

which diverges because \(m_\varepsilon\to\infty\). The condition \(\varepsilon m_\varepsilon^2\to0\) controls a single block, not the total horizon.

A normalization, telescoping cancellation, martingale structure, or sharper per-block estimate might alter the conclusion, but none is stated or proved. The theorem therefore contradicts its own error accounting.

### 3. Uniform re-equilibration under controlled tilts is assumed

The claim that every action-dependent block law lies within \(O(\rho_*^{m_\varepsilon})\) of its stationary information projection requires a uniform spectral gap/mixing theorem over the entire controlled family, plus uniform moment and initialization control. These are precisely the unresolved A2/A3-type inputs.

The manuscript cannot use “prepared phase” as a substitute for a quantitative, action-uniform mixing theorem.

### 4. Posterior sufficiency is tautological; posterior contraction is not proved

The conditional law of the future given the observations is sufficient for bounded future payoffs by definition. A substantive filtering theorem would establish finite-dimensional closure, stability, or contraction for a specified observation model.

The announced total-variation contraction and invariant moment ball require an observation kernel and dominating measure, a precise refresh mechanism, a Lyapunov/moment function, a transition on the history space, and minorization constants stable under Bayes normalization. None is provided. A deterministic shift does not become Doeblin merely because a “refresh” is mentioned.

### 5. The complete-observation no-go statement is elementary

Outside singular sets, complete observation of a deterministic microstate determines the future trajectory. This is correct and useful as a modeling warning. It is immediate, however, and cannot carry a standalone research paper.

### 6. The saddle Hessian is a generic envelope calculation whose hard hypotheses are assumed

Under a smooth interior saddle with invertible signed Hessian,

\[
D^2W
=
G_{\phi\phi}-G_{\phi z}G_{zz}^{-1}G_{z\phi}
\]

is the standard implicit-function/Schur-complement formula. The actual work would be to prove existence, uniqueness, interiority, smooth dependence, and Fréchet differentiability for the relevant path-pressure game. The manuscript assumes those properties.

There is also a typing inconsistency: finite or discrete preparation choices do not possess a smooth interior Hessian of the kind used in the theorem.

### 7. An initial preparation game is not the displayed dynamic Isaacs problem

If the players choose a preparation once before deterministic evolution, the value has one outer \(\sup\inf\) applied to the already constructed phase-dependent semigroup. In contrast,

\[
\partial_tU+\sup_u\inf_v
\mathbb H^{u,v}\left(f,\frac{\delta U}{\delta f}\right)=0
\]

allows \(u,v\) to be reselected continuously as time and state change. This enlarges the admissible strategy class and changes the value.

To justify the Isaacs equation, the authors would need a genuinely adaptive controlled transition law, nonanticipative strategies, switching rules/costs, and a comparison theorem. None is part of the stated preparation model. The proposed “typed controlled closure” is therefore false.

### 8. Reward control and preparation control are conflated

On a fixed phase, actions that affect only running/terminal work change the reward but not the transition kernel. Actions that change preparation alter the law itself. These two cases lead to different dynamic programming equations. The manuscript merges them into one Hamiltonian without specifying how controls enter.

## Dependency assessment

C1 cannot provide a controlled closure for D1 or other papers. Its fixed-phase recursion is generic; its multiscale preparation theorem does not close; and its Isaacs equation solves a different game.

## Minimum viable reconstruction

The paper should be reduced to a precise modeling note separating three cases: one-time preparation, reward-only control on a fixed phase, and genuinely adaptive law control. For any multiscale theorem, the accumulated error must be recomputed and a uniform controlled mixing theorem supplied.

## Recommendation

**Reject.** The paper is mostly textbook structure, while both nontrivial model-dependent conclusions are mathematically unsupported—one by divergent error accumulation, the other by changing the game being solved.
