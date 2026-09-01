# Independent Referee Report — Round 14

**Manuscript:** D1 — *Deterministic Theta Contractions*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `a2af75268483c0342458155712582ac7f32043d0a5e433188ff14129c80d3823`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject; remove as a standalone submission**

## Executive assessment

Round 14 replaces the invalid spectral-projection labels by honest positive measurable basin events, keeps a boundary label, regularizes component rates from inside each basin, and correctly recognizes that nonlinear values aggregate through log-sum-exp rather than linear averaging.

The paper is still not a closure theorem. Its own restricted-pressure definition has the sign of the phase weight wrong; the phase label is defined from a full path/order parameter and is not shown adapted or consistent across time horizons; conditional component LDPs and zero-free charts are assumed through basin recovery and real rate gaps that do not provide the required complex/operator estimates; and the dynamic “phase state” is anticipative. The manuscript remains a conditional bookkeeping note downstream of all unresolved platform theorems.

## Decisive objections

### 1. The unnormalized restricted pressure has the wrong sign

The manuscript defines

\[
\widetilde Q_{n,j}(F)
={1\over n}\log E[e^{nF(X_n)}\mid J_n=j]
\]

and

\[
\alpha_{n,j}=-{1\over n}\log w_{n,j}.
\]

Therefore

\[
\begin{aligned}
Q_{n,j}^{un}(F)
&={1\over n}\log E[e^{nF(X_n)};J_n=j]\\
&={1\over n}\log w_{n,j}+\widetilde Q_{n,j}(F)\\
&=-\alpha_{n,j}+\widetilde Q_{n,j}(F).
\end{aligned}
\]

The manuscript instead writes

\[
Q_{n,j}^{un}
=-{1\over n}\log w_{n,j}+\widetilde Q_{n,j},
\]

which equals `+alpha_{n,j}+tilde Q`. This is the opposite sign. Later log-sum-exp formulas use the correct `-alpha` convention, so the paper is internally inconsistent at its central normalization.

### 2. The label is not shown consistent across horizons

`J_n` is defined from the full path variable `X_n` and its order parameter. The statement that the same label survives every finite observable projection is true only for projections of one fixed `n`-horizon sample.

A dynamic semigroup requires labels compatible when the horizon changes from `n` to `m`, and adapted to the current filtration. A basin label determined by the completed future empirical path is generally not measurable at an intermediate time. The paper does not construct a single latent process `J_t` or prove that `J_n` is invariant under restriction to subintervals.

Consequently one cannot simply “retain the phase weights as a state coordinate” in a causal dynamic program.

### 3. Conditional LDPs do not follow from the stated assumptions alone

The theorem assumes the phase weight exponent exists and introduces the basin-internal l.s.c. envelope `I_j`. For the conditional upper bound one needs exponential control of neighborhoods of the basin boundary; for the lower bound one needs recovery sequences that remain in the basin at the microscopic level.

The recovery lemma delegates this to A3 and B2, neither of which proves the required platform LDP. Even abstractly, a macroscopic recovery path lying in an open basin does not automatically admit microscopic approximants whose order parameter remains in that basin with the same exponential cost unless the recovery is exponentially localized.

The component theorem is therefore conditional on the principal result it claims to provide.

### 4. The boundary component has no proved interior recovery theorem

The proof says the same argument applies to the boundary label using “its own interior in the labelled topology.” A Voronoi boundary band may have empty interior in the original topology, contain ties between phases, or consist of several geometrically unrelated pieces. No labelled topology or boundary-interior recovery construction is defined.

Thus `I_partial` and the conditional boundary LDP are not established.

### 5. A real rate gap does not give a zero-free complex partition function

The component chart proof uses an interior real rate gap and concludes that the localized finite-volume partition function is zero-free on a complex source neighborhood by Rouché's theorem. To apply Rouché one needs a uniform complex relative-error estimate with respect to a nonvanishing analytic leading term.

A real exponential bound on the complement does not control complex cancellations, and a positive basin indicator does not define an invariant simple-eigenvalue transfer operator. The claimed “positive killed operator” and its isolated Perron root are not constructed from the path-level basin event.

### 6. The dynamic component semigroups are not defined on basin-conditioned laws

Even if the finite-horizon conditional laws are valid, evolution of a law conditioned on a terminal/full-path basin does not preserve that basin under time splitting. The conditional component at time `s` depends on the remaining horizon and future event. It is therefore a two-parameter bridge/conditioning kernel, not an autonomous component semigroup.

The manuscript's log-sum-exp identity is correct for a fixed finite mixture at one horizon. It does not construct an augmented nonlinear semigroup across horizons.

### 7. The derivative statement at coexistence is incomplete

For a maximum of smooth component values, the convex hull of active derivatives describes a subdifferential under suitable local uniformity. The manuscript additionally says finite-volume subleading weights select subsequential mixtures. This requires asymptotic expansions of phase weights and component coefficients on a common scale. The platform papers do not provide such uniform expansions at coexistence or on the boundary label.

### 8. Shell weights inherit all unresolved component coefficients

The formula

\[
w_{n,j}c_{n,j}(a)e^{-nI_{j,C}(a)}
\]

is algebraically natural. It is a theorem only if each component has a uniform shell local limit and the boundary component is controlled on the same scale. A2 and B1 do not currently prove those results, and D1 adds no independent estimate.

### 9. The headline theorem assumes “proved platforms” that are not proved

The final statement begins with every regular finite-phase chart “of the proved Sinai or hard-sphere platform.” The upstream A2/A3/A4 and B1/B2/B3/B4 theorems remain open. D1 cannot turn them into established inputs by restating their desired consequences.

### 10. Standalone novelty is insufficient

The exact positive decomposition is the law of total probability, the component-rate normalization is standard conditional-LDP bookkeeping under strong assumptions, and the nonlinear aggregation is the elementary finite log-sum-exp principle. These ideas belong in a phase section of a future platform paper, not in a separate top-four submission.

## Required reconstruction

The correct future use of this material would be:

1. define a horizon-consistent, adapted positive phase label supplied by one platform;
2. prove its component LDP and local coefficient within that platform;
3. correct the restricted-pressure sign convention;
4. distinguish fixed-horizon log-sum-exp from causal component dynamics; and
5. incorporate the resulting theorem into the principal platform manuscript.

## Recommendation

**Reject; remove as a standalone submission.** The revision repairs the positivity and nonlinear aggregation language, but it contains a central sign error and assumes rather than constructs the component laws, analytic charts, and dynamic phase process.