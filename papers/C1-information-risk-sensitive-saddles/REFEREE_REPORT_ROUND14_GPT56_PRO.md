# Independent Referee Report — Round 14

**Manuscript:** C1 — *Information and Risk-Sensitive Saddles*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `83705e15bd30bb5e6a019c6cb77ab2a64b040acb8baff06ae7a1b8c54317fb4e`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 cleanly separates positive posterior measures from oriented geometric currents, uses a genuine product blow-up rather than collapsing zero-evidence directions, and replaces a fixed finite moment claim by growing bounded-Lipschitz coordinates. These are appropriate repairs.

The basic belief transition is nevertheless not a probability kernel: the displayed integral over observations omits the observation-density weight. The Feller hypothesis is then claimed to follow from a local asymptotic coefficient theorem that applies only to a narrow prepared model, not to the exact kernel on all beliefs. Repeated noiseless observations also leave the density class used by the coarea formula. The dynamic program and statistical conclusions therefore have no established state transition.

## Decisive objections

### 1. The displayed belief transition is not a probability kernel

The observation marginal has density `g_{nu,u}(y)`. Hence the observation `y` must be sampled with law

\[
g_{\nu,u}(y)\,dy.
\]

The manuscript instead defines the transition as

\[
(r,\nu)\longmapsto
\int \delta_{(r g_{\nu,u}(y),\nu_{u,y})}\,dy.
\]

This integrates Dirac masses against bare Lebesgue measure. Its total mass is the Lebesgue measure of `Y`, not one; it may even be infinite. The correct probability kernel would have the form

\[
\int g_{\nu,u}(y)
\,\delta_{(r g_{\nu,u}(y),\nu_{u,y})}\,dy,
\]

with any additional risk-sensitive weight separately normalized.

This is a direct algebraic defect in the object used by every subsequent DPP and Feller statement.

### 2. The blow-up represents only masses in `[0,1]`

The point `(r,nu)` is said to represent the finite measure `r nu`, but the radial coordinate is restricted to `0<=r<=1`. An unnormalized risk-sensitive belief or Feynman–Kac weight can have arbitrary positive mass. No normalization such as

\[
r={Z\over1+Z}
\]

is defined, and the transition `r -> r g(y)` can leave `[0,1]` even when `r<=1` because an observation density can exceed one.

Thus the proposed compact state is not invariant under its own update.

### 3. The exact coarea state is not closed under repeated noiseless observations

The coarea representation assumes that the current belief has densities `f_S` with respect to Hausdorff measure on a finite Whitney stratification. After a noiseless observation, the posterior is supported on a fiber of lower dimension. After repeated observations, intersections of fibers and collision strata create new dimensions and singular measures.

The paper says lower-rank strata are included, but it does not construct a recursively closed stratification or prove that the prediction step returns these singular posteriors to the declared density class. Rokhlin disintegration exists abstractly; the displayed coarea density need not.

### 4. The Feller theorem assumes the principal estimate

The theorem assumes

\[
\|g_{\nu,u}-g_{\tilde\nu,u}\|_{L^1}
+
\int g_{\nu,u}(y)
W_1(\nu_{u,y},\tilde\nu_{u,y})dy
\le L W_1(\nu,\tilde\nu).
\]

This is a very strong stability theorem for Bayesian disintegration. It fails near observations with small evidence unless one has uniform lower bounds or uses an integrated filter metric tailored to the kernel. The proof merely applies the assumed inequality.

The manuscript later says B1/A2 inserted coefficients prove it. Those are asymptotic local-limit statements for one prepared reference family and regular central observations. They do not imply an exact finite-volume Lipschitz inequality uniformly over every belief in `K_M`.

### 5. The inserted coefficient does not cover the dual class needed for Feller continuity

The coefficient theorem is uniform for `G` in a fixed finite-history Lipschitz class and for additive finite-dimensional observations. The Feller estimate requires control of the full posterior law in Wasserstein distance, i.e. all bounded-Lipschitz tests on the complete microstate/history space and arbitrary beliefs in the compact set.

A central insertion affecting finitely many coordinates cannot establish that global dual estimate.

### 6. The “compact weighted microstate set” is not the exact state space

B2 compact containment gives, at best, high-probability compact subsets or compact rate sublevels. It does not replace the microscopic/path state by one fixed compact set `E` on which the exact process lives. The exact belief can assign positive mass outside every selected compact set.

The paper alternates between an exact DPP and a compact containment truncation without introducing a cemetery/tail coordinate or estimating the truncation error.

### 7. The growing-coordinate construction is conditional on an unproved kernel Lipschitz constant

For a genuinely compact belief set, a finite determining family can approximate `W1`, and the reconstruction idea is reasonable. But the error propagation

\[
3\epsilon L_V\sum_{j=0}^{N-1}L^j
\]

requires the exact belief transition and reward to be Lipschitz with the same uniform `L`. That is precisely the unproved hypothesis above. The lemma cannot close the model by itself.

### 8. The reduced coordinates do not define a canonical controlled Markov kernel

The reconstruction `R_epsilon` is merely measurable and generally discontinuous. Pushing the belief kernel through `C_epsilon` and then reconstructing can destroy Feller continuity and strategy measurability. A measurable selector suffices for existence of some kernel, not for the uniform value comparison and continuity asserted.

### 9. The Bernstein–von Mises theorem assumes nearly all substantive hypotheses

The paper assumes:

- exact finite-centered LAN;
- uniform identifiability;
- positive information;
- uniformity over an informative strategy class;
- exponential posterior tightness; and
- the inserted coefficient normalization.

Once these hold, the Gaussian posterior conclusion is standard. The manuscript does not derive these hypotheses from the hard-sphere model, and B1/B3 do not currently prove them.

### 10. The exact game still depends on unresolved upstream objects

Prediction is delegated to B2/B4, the inserted observation coefficient to B1, and the score limit to B3. All three inputs remain mathematically open in Round 14. C1 therefore cannot be a closure theorem by composition.

## Required reconstruction

A credible paper should first construct one exact filtering model with:

1. a correctly normalized joint observation/posterior kernel;
2. an invariant unnormalized-belief state space with an explicit radial compactification;
3. a recursively closed class of singular posteriors;
4. a proved integrated filter-stability estimate; and
5. only then a finite-coordinate approximation and statistical limit.

## Recommendation

**Reject.** The revision contains useful state-typing ideas, but its central displayed transition is not a probability kernel and the Feller/DPP conclusions rely on an assumed stability theorem not supplied by the cited asymptotics.