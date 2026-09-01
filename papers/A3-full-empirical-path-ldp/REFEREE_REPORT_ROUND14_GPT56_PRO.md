# Independent Referee Report — Round 14

**Manuscript:** A3 — *Full Empirical-Path LDP*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `1e1b2fe5cf43fe66d4a08386d0fd953522ef77fcfe32d7e2d3b6c8f1d7f20e78`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 correctly stops trying to discard singularity exposure uniformly over finite-entropy controls. It also places the final incomplete excursion in the state and attempts to formulate collision-clock and physical-clock problems directly at deterministic horizons.

The central “exact” control representation is nevertheless false on the declared control class. The paper restricts each controlled transition to depend only on the current entrance state, whereas the Gibbs variational formula for an arbitrary functional of the stopped empirical state requires history-, time-, and accumulated-state-dependent predictable kernels. The proposed stationary-kernel rate therefore does not follow. Several coordinates and costs are also left undefined precisely where a macroscopic terminal excursion creates order-one effects.

## Decisive objections

### 1. The exact variational identity uses too small a control class

The manuscript defines a controlled trajectory through kernels

\[
Q_j(\cdot\mid y_j)\ll K(y_j,\cdot),
\]

depending only on the current entrance state. It then claims, for every bounded continuous functional `Phi` of the stopped empirical state,

\[
-{1\over n}\log E e^{-n\Phi}
=
\inf_Q E_Q\left[\Phi+{1\over n}\sum D(Q_j\Vert K)\right].
\]

The Gibbs/Donsker–Varadhan variational identity is exact when the disintegrated control at time `j` may depend on the full past, the current time/clock, and any accumulated statistic on which `Phi` depends. Restriction to `Q_j(.|y_j)` is not exact.

A two-step finite-state example already disproves the claim: take a trivial current state and a terminal payoff depending on whether the two successive symbols agree. The optimal second-step tilt depends on the first symbol. No current-state-only kernel can realize it.

One may recover exactness by enlarging the controlled state to include the accumulated empirical variables and residual clock, or by allowing general predictable kernels. The manuscript does neither.

### 2. The stopped state is not mathematically defined

The third coordinate is written as

\[
{1\over n}\operatorname{pref}_{a_n}(e_{N(n)}).
\]

A pointed path prefix is not a vector that can be multiplied by `1/n` unless it has first been encoded as an occupation measure/current with a specified topology. The paper does not define that encoding, its mass, or how it is combined with the first clock-weighted excursion measure.

This matters when the terminal excursion has length of order `n`: its prefix carries order-one clock mass and cannot be treated as an auxiliary endpoint decoration.

### 3. The uniform exponential kernel bound is unproved and implausibly strong

The lemma assumes

\[
\sup_y\int e^{\eta W(e)}K(y,de)<\infty.
\]

An exponential Young-tower return tail under the invariant Gibbs law does not by itself imply a uniform conditional exponential moment over every entrance state, especially near deep homogeneity/singularity states. The proof replaces this issue by “bounded distortion” and summation over branches, without a uniform entrance-state comparison.

This supremum is subsequently used for stopping-time truncation, compact containment, physical-clock inversion, and the history kernel in A4. It is a new load-bearing theorem and is not proved.

### 4. The stationary controlled-kernel rate does not follow from the exact problem

Even if the variational formula were corrected to allow predictable controls, the rate is then asserted to be an infimum over stationary kernels `bar Q` with invariant entrance law `pi`. No theorem is supplied that reduces arbitrary time-inhomogeneous, empirical-state-dependent, stopped controls to stationary Markov controls without loss.

For additive empirical measures of ordinary Markov chains such a reduction follows from a precise occupation-flow theorem. Here the stopping index is random, clocks are unbounded, one excursion may carry order-one mass, and the terminal prefix is part of the state. Those features require a new theorem, not the sentence “any convergent controlled sequence has a limit occupation measure.”

### 5. Macroscopic endpoint imbalance is not `O(1/n)`

The proof says that entrance and exit marginals agree because unmatched endpoints have `O(1/n)` clock mass. That is true for count-normalized transitions with bounded marks. It is false for a terminal or initial excursion of length comparable with `n`: its clock weight is

\[
{r(e)\over n}=O(1).
\]

Exactly these one-big-excursion states are retained by the manuscript. Their endpoint defect must be represented by an explicit defective-flow coordinate and cost. The phrase “ordinary and defective invariant controlled kernels” does not define such an object.

### 6. The terminal cost is only described in prose

The rate contains

\[
\mathfrak t(\rho\mid\pi,\bar Q),
\]

described as the entropy of the final excursion minimized over completions of the observed prefix. The paper does not specify:

- the reference conditional law of the completion;
- the terminal clock fraction;
- the topology on prefix laws;
- consistency with the complete-excursion control; or
- lower semicontinuity and compactness of this cost.

The rate is therefore not a defined functional on a defined state space.

### 7. The recovery proof does not cover mesoscopic and macroscopic controls

The proof treats a stationary bounded-`W` kernel, concatenates finitely many components, and then says that truncation and an entropy-moment estimate control all ordinary, mesoscopic, and macroscopic tails simultaneously. A `1/L` expectation estimate gives tightness; it does not construct recovery sequences for an arbitrary prescribed distribution of excursions on scales between `1` and `n`, nor does it identify the entropy cost of those scales.

The projective recession proposition cannot repair this: it contracts the already asserted good rate `I^c`. If `I^c` has not been proved on the enlarged state, Dawson–Gärtner only repackages the missing theorem.

### 8. The graph-to-physical contraction is not shown continuous at singular paths

Recording a signed distance and a one-sided label can select a continuation, but continuity of concatenation also requires compatible collision times, numbers of impacts, endpoint matching, and control of accumulation near grazing. The proof checks none of these. A local Skorokhod topology can still fail continuity when an impact is born, lost, or merged.

### 9. Physical-time inversion repeats the same unresolved interfaces

Replacing `r` by `tau` in the entropy formula does not automatically establish a physical-time LDP. One must prove compactness of the stopped roof occupations, lower semicontinuity of the residual-flight kernel, stationary/defective-flow reduction at physical speed, and recovery for macroscopic roof excursions. These are asserted by analogy.

## Dependency assessment

A3 remains the central unresolved bridge in the Sinai chain. A4 has no established complete-past kernel or physical-clock rough limit, while C2 and D1 have no proved parent path LDP from which to contract phases, cotangents, or memory.

## Required reconstruction

A credible revision must:

1. state the exact control formula over all predictable kernels on an explicitly enlarged stopped state;
2. define the terminal prefix as a measure/current coordinate;
3. prove an occupation-flow compactness and Markovization theorem with defective endpoint mass;
4. give a complete lower-semicontinuous terminal/recession cost; and
5. prove collision and physical clocks separately before contracting to path space.

## Recommendation

**Reject.** The revision retains the right phenomena, but the claimed full LDP is obtained from a false restricted-control identity and an undefined stationary/recession rate.