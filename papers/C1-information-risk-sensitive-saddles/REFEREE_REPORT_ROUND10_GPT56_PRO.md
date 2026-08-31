# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** C1 — Information and Risk-Sensitive Saddles  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `85d4b58081ccaa7e786b6abc7939c32092b5c60ba9ab031a58f080ccef23a856`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

The paper now distinguishes full belief control from a later reachable-chaos reduction, carries unnormalized evidence explicitly, and permits observation strata distinct from billiard grazing strata. Those are correct modeling improvements.

The mathematical filtering state is still not constructed. Coarea “restriction” of an arbitrary measure to a zero-measure level set is not the formula written in the paper; the state space excludes the zero-evidence boundary while claiming continuity as evidence tends to zero; and the joint coefficient theorem applies B1's additive good-block mechanism to general path/contact observations without proving an additive regenerative representation. The reachable-chaos estimate and Bernstein–von Mises conclusion are then asserted on top of these missing interfaces.

## Major mathematical objections

### 1. The coarea update is not defined on the declared measure tower

The update is written as

\[
\mathcal O_{u,y}\Lambda
=\sum_S
1_{S\cap O_u^{-1}(y)}J_{O_u|S}^{-1}\Lambda|_S.
\]

For an absolutely continuous measure \(\Lambda\), the level set \(O_u^{-1}(y)\) has \(\Lambda\)-measure zero, so ordinary restriction gives zero. Coarea produces a disintegration or slice for almost every \(y\), not multiplication of an arbitrary finite measure by a level-set indicator.

To extend this operation to measure-valued currents one needs a precise theory of normal currents/slices, rectifiability, orientation, and continuity under the selected topology. The direct sum \(\bigoplus_r\mathcal M_W(\mathcal S_r)\) contains arbitrary measures for which such slices need not exist. Closing a graph after starting with smooth densities does not identify the resulting domain with the whole declared measure tower.

### 2. The state space has no zero-evidence boundary

The Feller state is

\[
\widehat{\mathfrak B}
=\{(\Lambda,z):\langle1,\Lambda\rangle=e^z,\ z\in\mathbb R\}.
\]

A sequence with evidence \(Z_n\downarrow0\) has \(z_n=\log Z_n\to-\infty\) and no limit in this space. The preceding lemma nevertheless claims continuity “including sequences with \(Z\downarrow0\).” That is topologically impossible without adjoining a boundary point \(z=-\infty\) and, if future decisions depend on normalized beliefs, a projective direction at zero mass.

Integrating zero-evidence observations with weight zero avoids defining a posterior exactly at \(Z=0\); it does not prove Feller continuity or compact containment near evidence escape.

### 3. The codimension tower is not shown to be closed under repeated observations

Repeated observation level sets can meet collision strata nontransversely, change rank, split into infinitely many components under the hard-sphere flow, and create corners of unbounded combinatorial complexity. The paper assumes a finite stratification on each chronological cell and then uses factorial codimension weights. It does not prove that the sequence of prediction/observation operations stays within a countable locally finite normal-current complex with uniform operator bounds.

Critical strata cannot simply be “promoted” without constructing their induced measures and transition maps.

### 4. The joint observation coefficient does not follow from B1 good blocks

The observation family consists of affine statistics of the full particle path and actual-contact measure. Such a statistic is additive at the empirical level, but its contribution from one initial spatial block is not conditionally independent of other blocks: future collisions join their genealogies. B1's local mark-sum submersion does not automatically extend to an arbitrary path/contact observation.

The paper must prove a source- and control-uniform high-frequency theorem for the augmented observation coordinates using the actual B2 trajectory expansion. The statement that one can “adjoin the observation coordinates to the B1 good-block sum map” assumes this theorem.

### 5. The ratio theorem conflates coefficient cancellation with evidence control

For a bounded insertion, numerator and denominator may share the same exponential saddle, but their polynomial coefficients need not be identical; the insertion can alter conditional expectations on the local Gaussian fiber. A valid ratio theorem requires a uniform inserted local limit theorem, not merely the uninserted coefficient.

For risk-sensitive or exponentially scaled posterior payoffs, the source changes the saddle altogether. The theorem does not distinguish these two cases.

### 6. The reachable-chaos class is circularly defined and not uniformly controlled

\(\mathfrak R_\varepsilon\) is defined as the smallest class closed under the very prediction and observation kernels whose estimates are at issue. The claimed supremum over that class includes rare exact observations with finite large-deviation cost. Conditioning on such observations can select phase mixtures or strongly correlated collision patterns, and an evidence factor does not automatically restore

\[
\|\kappa_j\|=O(\mu_\varepsilon^{1-j}).
\]

The proof says that normal convergence of a source pressure preserves cumulant scaling. This is valid only on a uniform analytic source chart and does not cover conditioning values approaching its boundary, critical strata, or nonunique phases.

### 7. The reduced game error is not summed through the dynamic program

Even if one-step higher-correlation errors are small, uniform \(o(1)\) for the game value requires stability under all admissible strategies, observation kernels, minimax selection, and the number of decision stages. The manuscript gives no quantitative Bellman Lipschitz estimate or error recursion.

### 8. The LAN and Bernstein–von Mises theorem lacks a statistical model

A Bernstein–von Mises theorem requires a finite-dimensional parameter, an identifiable likelihood family, a prior with specified local regularity, local asymptotic normality uniformly in local alternatives, and posterior tightness. None of these objects appears in the theorem statement. “A regular phase” and a covariance matrix are not sufficient hypotheses.

B3's Gaussian fluctuation theorem, even if valid, would not by itself imply a posterior theorem for an unspecified controlled observation model.

## Dependency and editorial assessment

C1 depends on the unproved B1, B2, B3, and B4 interfaces and fails independently at the definition of its coarea state. It cannot supply a filtering/game closure for C2 or D1.

A viable paper should choose a finite observation model, build the sliced-current state on a precise normal-current domain, adjoin an actual zero-evidence compactification, and prove one inserted local limit theorem. The current sweeping theorem package is not rigorous.

## Recommendation

**Reject.** Evidence lifting is conceptually correct, but the observation update is not defined on the stated space, the Feller state omits its boundary, and the statistical limit theorem has no complete hypotheses.
