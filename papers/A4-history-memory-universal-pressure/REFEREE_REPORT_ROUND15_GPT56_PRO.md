# Independent Referee Report — Round 15

**Manuscript:** A4 — *History, Memory, and Universal Pressure*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence and submission integrity

No Round-Fifteen A4 source is present in the submitted tree, and none was recoverable from the surviving truncated payload. The paper still inputs `ROUND14_POSITIVE_CLOSURE.tex`. I therefore review the actual controlling manuscript. The claim that a Round-Fifteen revision has been published is not supported by the branch contents.

## Executive assessment

Replacing impossible total-variation minorization on the complete past by a discounted metric is the right conceptual move. The manuscript, however, does not prove the global contraction it states; its Feynman–Kac source set is not a well-defined analytic Banach neighborhood; and the continuous-time renewal/memory theorem omits essential domain and forcing issues. These are load-bearing, not cosmetic.

## Decisive objections

### 1. Summable past variation does not give the stated pure contraction

The proof combines maximal coupling of the new symbol with the fact that old discrepancies are shifted into exponentially discounted coordinates. This may yield a weak-Harris estimate for a carefully patched distance-like function and on Lyapunov sublevels.

It does not establish the manuscript's global inequality in the raw \(d_\beta\) metric with no additive Lyapunov term. When newest symbols fail to couple, the distance can jump to order one even when \(d_\beta(x,y)\) is arbitrarily small. Summable variation controls the failure probability, but a complete contraction proof requires an explicit small-distance estimate, a large-distance Lyapunov coupling, and a patched metric.

### 2. The multiplier “neighborhood” is not a normed analytic chart

The set

\[
|V(h)|\le c_V+\eta\log W(h)
\]

with finite Lipschitz norm is described as a neighborhood of zero, but no Banach norm controlling \(c_V\), \(\eta\), and the weighted Lipschitz seminorm is specified. Analyticity of

\[
V\mapsto P(e^V\cdot)
\]

requires a fixed open set in one Banach space and uniform multiplier estimates on a fixed pair of weighted spaces. Changing to a “slightly heavier weight” with the source is not an operator-norm analytic family unless all inclusions and radii are fixed.

### 3. The renewal-resolvent estimate is imported from A2 without a valid unsmoothed theorem

A4 claims integrable vertical bounds for the returned resolvent from A2. The recoverable Round-Fifteen A2 candidate obtains very-high-frequency integrability only after a smooth physical-time test is inserted. That is insufficient for the raw suspension resolvent and its derivatives. Thus the Bromwich inversion and exponential memory bound have no established input.

### 4. The projected Volterra equation omits unresolved forcing

For a Mori–Zwanzig decomposition, the projected observable generally satisfies a resolved drift plus a memory convolution plus an orthogonal-dynamics forcing term depending on the unresolved initial component. The corollary states that

\[
x(t)=P_{\mathcal R}\mathcal U_t^VA
\]

satisfies a causal generalized Langevin equation determined by the memory distribution, but it does not state the forcing term or assume \(A\) lies in the resolved range.

A Schur-complement identity for the compressed resolvent does not erase the unresolved initial condition.

### 5. Domain assumptions for the compression are insufficient

The manuscript uses

\[
P_{\mathcal R}L_VP_{\mathcal R}
\]

and a large-\(z\) expansion through \(D(L_V^2)\). It must prove that the chosen resolved subspace lies in a common operator domain, that the projection preserves the relevant domain, and that the compressed inverse is defined away from a controlled singular set. These conditions are not consequences of a weighted Lipschitz spectral gap.

### 6. The descriptor theorem still assumes uniform inverse bounds

Even after taking pole–zero cancellation in the final Schur complement, vertical bounds for \(C_V(z)\) do not automatically give comparable bounds for \(C_V(z)^{-1}\). Small singular values away from isolated zeros can amplify the inverse. A quantitative lower bound on the minimum singular value is required on the Bromwich contours; it is not proved.

### 7. The rough-path theorem is mostly cited machinery

The text asserts uniform predictable-bracket convergence, conditional Lindeberg, second-level tightness, an area anomaly, suspension inversion, and terminal-residual control in a few paragraphs. The needed moment estimates and topology are not stated with sufficient precision, and the argument depends on A3's unproved stopped LDP.

## Required reconstruction

Prove a precise weak-Harris theorem in a patched weighted distance, define one fixed multiplier Banach algebra, and establish an unsmoothed suspension resolvent theorem. State the full forced Mori–Zwanzig identity with common domains and quantitative inverse bounds. Only then can descriptor extraction and rough-memory limits be considered.

## Recommendation

**Reject.** There is no Round-Fifteen A4 manuscript in the branch, and the controlling Round-Fourteen text does not establish its weighted spectral, renewal, or memory interfaces.
