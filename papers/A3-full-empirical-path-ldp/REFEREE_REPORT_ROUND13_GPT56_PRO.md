# Independent Referee Report — Round 13

**Manuscript:** A3 — *Full Empirical-Path LDP*  
**Reviewed branch:** `revision/round13-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `5c8b71e67d62d4a63c53a5a59e7a10f1ccc0f688`  
**Reviewed tree:** `586de2e3cf8c547ca3cbfbc0cb0daba2fd05af59`  
**Controlling module:** `ROUND13_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `83d0101d56e965069cbf4eab1c177d5444ebab4fb4539d396b47aff524010ded`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 13 makes several conceptually correct changes: the horizon is deterministic, the last incomplete excursion is selected by the same controlled transition as the completed excursions, singularity exposure is retained rather than declared uniformly negligible under entropy controls, and collision and physical clocks are treated separately.

The paper still does not prove the announced path LDP. The displayed recurrent–recession rate is not a defined functional on a specified state space, and it contains no explicit cost for the terminal residual law even though that law is an argument of the reconstruction map. The key Foster–Lyapunov estimate is asserted from a stationary exponential return tail, which does not imply the required pointwise conditional drift. The proof also omits the mesoscopic-excursion regime and replaces a difficult Γ-convergence/recovery theorem by a paragraph of description.

## Decisive objections

### 1. The displayed rate does not charge the terminal residual law

The proposed rate is

\[
 I^c(z)=\inf\left\{
 (1-\alpha)\mathcal R_c(\eta)
 +\alpha\int J_c(\xi)\,\zeta(d\xi):
 \mathcal C_c(\eta,\alpha,\zeta,\rho)=z
 \right\}.
\]

The pointed terminal residual law `rho` appears in the reconstruction map, but it appears nowhere in the cost. The proof later says that when the terminal prefix carries a positive clock fraction it is “included in `rho` and paid by the same one-excursion cost.” No such term is present in the formula.

One must either make `rho` a deterministic marginal of `zeta` with a precisely stated compatibility constraint or add its clock fraction and recession cost explicitly. As written, two states with identical `(eta,alpha,zeta)` but terminal prefixes arising from branches with different exponential probabilities receive the same rate.

This is a defect in the theorem statement itself, not merely in its proof.

### 2. The recession functional is not mathematically defined

The definition uses

\[
 P\left(r(A_1)=\ell,
       \ell^{-1}K_{A_1}\in U\mid A_0\in C\right).
\]

Here `P(a,db)` was introduced as a transition kernel, not as a path law with a specified distribution of `A_0`, so conditioning on `A_0 in C` is undefined until an entrance distribution is fixed. Moreover `K_a` is a path in the graph-completed billiard state space; scalar multiplication `ell^{-1}K_a` has no defined meaning. Presumably the authors intend a normalized occupation/profile measure, but that object, its topology, and the neighborhoods `U` are not specified.

The outer `sup_U`, the limit/infimum in `ell`, and the superscript “lsc” do not repair an undefined underlying state variable. Consequently neither `J_c` nor the compactness of the rate sublevels is established.

### 3. A stationary exponential tail does not imply the stated pointwise drift

The proof of

\[
 PV(a)\le\rho V(a)+b1_C(a),
 \qquad V(a)=e^{\eta(r(a)+\tau(a))},
\]

appeals to the Young-tower return tail and bounded Gibbs distortion. An exponential tail under an invariant Gibbs law controls an average distribution. It does not imply a uniform conditional Foster–Lyapunov inequality for every current branch `a`.

A Markov chain can have an exponentially decaying invariant tail while high states are arbitrarily sticky, so that `PV(a)/V(a)` tends to one along a subsequence. The manuscript must prove a model-specific conditional estimate from the transition graph and Gibbs kernel. “Enlarging the connector set” does not by itself make the pointwise tail contraction smaller.

The drift estimate is then used for stopping-time entropy uniform integrability, compact containment, the complete-past kernel in A4, and the physical-clock theorem. It is a load-bearing unproved theorem.

### 4. The recurrent/recession decomposition omits mesoscopic escape regimes

The proof says that bounded entropy separates a vanishing number of excursions whose individual lengths are of order `n`. There is another possible regime: `sqrt(n)` excursions of length `sqrt(n)`, or more generally `m_n=o(n)` excursions with lengths tending to infinity and total clock of order `n`.

Such a family carries positive clock mass, has vanishing transition frequency, and is neither represented by a tight recurrent edge law nor by finitely many order-`n` excursions. It may converge to a recession profile measure, but proving the stated integral cost requires a triangular-array Γ-limit and control of connector/entrance distributions. The manuscript does not analyze this regime.

The assertion that finitely supported approximations of `zeta` and a diagonal argument provide every recovery sequence is precisely the theorem that must be proved.

### 5. The exact entropy formula does not identify the claimed rate

The Gibbs variational identity for a stopped path is a useful starting point. It does not automatically imply that all bounded-cost controls converge to the specific tuple `(eta,alpha,zeta,rho)` or that their entropy liminf equals the displayed additive formula.

A complete weak-convergence proof must establish:

- tightness of controlled transition flows and all unbounded clock/profile coordinates;
- identification of every possible concentration/escape measure;
- the entropy liminf for recurrent, mesoscopic, and terminal sectors;
- a measurable recovery control for every finite-rate state; and
- compatibility with the singular graph completion.

The current proof replaces these steps by a narrative description.

### 6. The physical-clock theorem repeats rather than proves the random-time analysis

The physical result says to “repeat” the collision proof with roof stopping. It must instead verify exponential tightness at speed `T`, control small/large controlled mean roofs, identify physical recession profiles, and construct the residual free-flight law. These do not follow formally from replacing `r` by `tau`, especially when the two clocks have different tail and arithmetic structures.

### 7. The contraction to physical paths is not established at singular states

The graph completion deliberately separates one-sided singular continuations. Forgetting that germ is discontinuous at a collision singularity in the ordinary path topology. The statement that every finite-rate law charging a multivalued continuation has infinite cost is asserted without a quantitative proof from `J_c`. It cannot substitute for the exponentially good approximation theorem needed by the contraction principle.

## Genuine improvements recognized

The deterministic stopped-control viewpoint, inclusion of the terminal branch in the entropy chain rule, explicit recession coordinates, and separation of collision and physical clocks are the correct architectural directions. They should be retained in a future proof.

## Dependency assessment

A3 remains the upstream gate for A4 and the Sinai part of C2/D1. Until the drift, Γ-limit, terminal cost, and physical-clock recovery are actually proved, those papers have no established full path rate or prepared history law.

## Required reconstruction

The paper should first define one Polish stopped-renewal state and one exact rate, including an explicit cost and compatibility law for the terminal residual. It must then prove a full controlled Γ-convergence theorem covering recurrent, mesoscopic, and one-big-excursion regimes. Only after that theorem should collision- and physical-time contractions be stated.

## Recommendation

**Reject.** The revised architecture is more honest, but the central rate functional is incomplete and partly undefined, and the weak-convergence proof omits the main compactness, liminf, and recovery arguments.
