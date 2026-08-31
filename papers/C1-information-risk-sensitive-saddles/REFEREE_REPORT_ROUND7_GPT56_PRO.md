# Round-Seven Independent Referee Report — GPT-5.6 Pro

**Manuscript:** C1 — Information States, Risk-Sensitive Saddles, and Controlled Kinetic Values  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision:** `revision/round7-referee-positive-closure-11paper-2026-08-31@b1e3d17f59ca9bb1a04d4ac9157f10dc333f9607`  
**Controlling module:** `ROUND7_POSITIVE_CLOSURE.tex`, blob `2e82692a301515b7e05f9e516a165de43fc1e927`

## Executive assessment

The paper now acknowledges that exact noiseless observations produce singular posteriors, includes the new observation in the Bayes update, keeps the complete belief state before proving reduction, and preserves the corrected KL/Chernoff distinction and exact finite LAN centering.

The proposed coarea-current state is not covered by B2's measure–trace semigroup, and its normalized posterior norm cannot be uniform in the observed value without a lower bound on the observation density. The conditional block ratio theorem is not obtained from transversality, and the claim that all beliefs with the same one-particle mean become value-equivalent is false for correlated hard-sphere preparations. The control/filtering theorem therefore remains unproved.

## Major mathematical objections

### 1. Coarea normalization can blow up at perfectly regular observations

For a noiseless observation, the posterior is normalized by

\[
Z(y)=\int_{O^{-1}(y)}gJ_O^{-1}\,d\mathcal H^{D-r}.
\]

The lower bound \(J_O\ge j_*>0\) controls the coarea Jacobian, not \(Z(y)\). Even when every \(y\) is a regular value, the marginal observation density \(Z(y)\) may be arbitrarily small or vanish near the edge of its support. Dividing by it can make the posterior-current norm arbitrarily large.

A simple example is projection onto one coordinate under a smooth density whose marginal tends to zero at a boundary point. The observation map is a submersion everywhere, yet the normalized conditional density is not uniformly bounded in \(y\).

Thus the claimed estimate

\[
\|\Pi_{k+1}\|_{m pc}\le C\|\Pi_k^{m pred}\|_{m pc}
\]

uniformly in the observed value is false without a quantitative lower bound on the observation density. Rare regular observations need not be superexponentially small; they can have exactly the exponential probabilities relevant to the risk-sensitive game.

### 2. B2's state space does not include arbitrary observation currents

B2 introduces interior measures and incoming collision-boundary measures. A coarea posterior for an \(r\)-dimensional observation is a codimension-\(r\) current on an arbitrary level set. After it intersects a collision face, one obtains codimension \(r+1\) currents; repeated exact observations generate further strata.

These are not the interior/binary-flux pairs on which the B2 renewal equation was stated. No hierarchy over arbitrary observation codimensions, no compatibility traces, and no operator estimate are constructed. The sentence “B2 acts on every such current” is a type assertion unsupported by B2.

### 3. Critical observation sets are unrelated to billiard singularities

The proof says that the bad nontransverse observation set is contained in the B2 grazing/singularity shield. For a control-dependent map \(O_k^u\), critical points of \(DO_k^u\) can occur in the smooth interior of a chronological cell and have no relation to grazing collisions. Calling a channel “admissible” may exclude them by assumption, but then the paper must state and verify this assumption for the proposed observation families. The B2 shield cannot do it automatically.

### 4. The conditional ratio theorem requires a new high-frequency theorem

Inserting an exact observation by a coarea delta and Fourier inversion introduces unbounded imaginary frequencies in the observation variable. B2 proves, at most, pressure convergence for bounded particle/contact sources. A submersion theorem does not give a source-uniform local limit coefficient at speed \(\mu_arepsilon\), nor does it control the numerator and denominator uniformly over singular posterior currents.

The claim that “the same coarea denominator cancels” presupposes the asymptotic coefficient theorem. It does not prove it. A quenched conditional local-limit theorem is a major independent result and is absent.

### 5. One-particle means are not asymptotically sufficient for arbitrary reachable beliefs

Theorem r7-c1-sufficiency takes a supremum over all posterior currents with the same resolved mean and claims their controlled values become equal. Higher correlations can change imminent collision probabilities and contact rewards at order one while leaving the one-particle mean unchanged. For example, one belief can pair particles in near-contact incoming configurations and another can decorrelate them, with identical one-particle marginals.

Propagation of chaos can erase certain correlations for specially prepared chaotic families; it is not uniform over the announced posterior-current ball, especially after exact conditioning. The displayed bound

\[
\|\mathfrak h_j(\Pi_{k+1})\|\le Cho^j\mu_arepsilon^{1-j}+\cdots
\]

is asserted without derivation and is generally false for arbitrary singular beliefs. Consequently the reduced kinetic DPP does not follow.

### 6. Feller belief transitions are not established

Coarea conditional laws need not depend continuously on the observed value near changes of level-set topology, even when values are regular on individual cells. Removing exceptional values “by a common compact exhaustion” does not produce a global Feller kernel or measurable minimax selectors on the original belief space. The normalization problem above also destroys continuity.

### 7. The statistical conclusions inherit unproved B2/B3 inputs

The exact finite score centering and local denominator form are correct ideas. But the BvM theorem uses B3's unproved Gaussian process/covariance and pressure gaps inherited from B2. It cannot serve as an independent closure theorem.

## Required reconstruction

Either add observation noise with densities uniformly bounded above and below on the relevant compact sets, or build a genuine stratified-current filtering theory with observation-density lower bounds and operator estimates at every codimension. Prove a quenched local-limit/ratio theorem for exact observations. Any density-only reduction must be restricted to a quantitatively chaotic belief class and proved, not taken uniformly over all beliefs sharing a mean.

## Recommendation

**Reject.** The coarea formula types individual posteriors, but it does not provide uniform normalized bounds, a closed transition state, or asymptotic sufficiency. The controlled kinetic limit remains unsupported.
