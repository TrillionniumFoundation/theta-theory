# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** D1 — Deterministic Theta Contractions  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `198573ea45cc0a15e7440e53508c160ed8889a808fe6deefa14dca723cefc6a5`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject; remove as a standalone submission.**

## Executive assessment

The paper now acknowledges that phase components must be genuine pieces of the microscopic law, preserves exponentially small remainders, and no longer infers a nonconvex minimum rate from the conjugate of a maximum pressure. Those are substantial corrections.

The revised formulation is still internally inconsistent. The restricted partition function is unnormalized and already contains the phase weight \(w_{n,j}\), yet the physical pressure subtracts the phase cost \(\alpha_j\) a second time. Phase labels are allowed to change with the finite projection, so no projective labelled process has been defined. Most importantly, the existence and regularity of the phase basins, restricted LDPs, boundary recoveries, shell coefficients, and Gaussian tangents are simply assumed; the platform papers do not construct them. The manuscript therefore remains a conditional collection of standard mixture lemmas, not a closure theorem.

## Major mathematical objections

### 1. The phase cost is double counted in the pressure formula

The paper defines

\[
Z_{n,j}(\theta)
=\mathbb E_n[e^{n\theta\cdot X_n};B_{n,j}],
\qquad
Q_{n,j}(\theta)=n^{-1}\log Z_{n,j}(\theta).
\]

At \(\theta=0\),

\[
Q_{n,j}(0)=n^{-1}\log w_{n,j}\longrightarrow-\alpha_j.
\]

If \(Q_{n,j}\to Q_j\) as stated, then \(Q_j\) already includes the phase-weight cost. Since

\[
\mathbb E_n e^{n\theta\cdot X_n}
=\sum_j Z_{n,j}(\theta)+\text{remainder},
\]

the physical pressure is

\[
Q(\theta)=\max_j Q_j(\theta),
\]

not

\[
\max_j\{Q_j(\theta)-\alpha_j\}.
\]

The latter subtracts \(\alpha_j\) twice. If the authors intend \(Q_j\) to be the conditional pressure of \(\mathbb P_{n,j}\), then the definition of \(Q_{n,j}\) must be changed to divide by \(w_{n,j}\). The current theorem is algebraically inconsistent.

### 2. The phase basins are assumptions, not outputs of the platform papers

The opening paragraph assumes disjoint basins whose uncovered mass is superexponentially small and whose boundaries are subexponential under all compact real source tilts. It then says A2–A4 and B1–B4 construct these objects.

Those papers do not prove such a basin decomposition. An exposed tilted law or a local spectral branch is a change of measure, not a measurable component of the original finite-volume law. Metastable boundary conditions and Riesz projectors likewise do not automatically define disjoint positive events \(B_{n,j}\) with superexponential coverage.

This assumption is essentially the desired microscopic coexistence theorem.

### 3. The labels are not projectively consistent

For every finite projection \(m\), the paper introduces a possibly different finite family

\[
B_{n,1},\ldots,B_{n,J_m}.
\]

No refinement map relates labels at level \(m+1\) to labels at level \(m\). Without such compatibility, there is no joint labelled random variable on the projective path space, and the finite labelled rates cannot form a Dawson–Gärtner system.

“Exact contraction of each restricted law” does not solve the problem: contracting a basin defined in a finer projection need not equal any basin chosen at the coarser level.

### 4. The phase-local zero-free theorem assumes the dominant spectral representation

A measurable restriction to an event \(B_{n,j}\) is not generally represented by one transfer/cluster operator with a simple isolated eigenvalue. Sharp basin indicators introduce nonlocal boundaries and can destroy analyticity or produce cancellations in the restricted partition function. The assertion that a platform operator has a Riesz contour inside the basin is a new theorem requiring a construction of phase boundary conditions or projectors.

Subexponential basin-boundary probability does not imply a uniform zero-free complex neighborhood; complex cancellations are not controlled by positive real probability estimates.

### 5. The phase-wise face lower bound is delegated to an absent theorem

The projective proof says every boundary face is recovered by a phase-specific normal-source limit and local coefficient theorem. A source tending to infinity can leave the phase regularity chart, approach a singular support face, or change the dominant basin. Uniform local limits on compact source charts do not justify this limit.

The required microscopic recovery is exactly the hard part of a full LDP and cannot be inserted as a phrase in a synthesis paper.

### 6. Thin-shell conditioning needs compatible phase coefficients and boundaries

Even if each restricted law had a local coefficient, conditioning the original law requires control of shell intersections with basin boundaries. A boundary that is subexponential before conditioning can dominate a shell whose probability has a larger exponential cost. The stated superexponential uncovered mass does not by itself control every boundary contribution after a source-dependent thin conditioning.

The shell theorem also inherits the invalid A2 and B1 coefficient packets.

### 7. Differentiation does not commute automatically at coexistence

For a finite mixture of exponentials with tied phase pressures, derivatives of the total finite-volume logarithm depend on subexponential phase weights and can oscillate with \(n\). Phase-wise derivatives exist, but the physical derivative need not converge to a unique convex combination unless the weights themselves converge at the required scale.

The main theorem states a “compact convex set or mixture selected by the microscopic phase weights” without giving such a convergence hypothesis or topology.

### 8. The standalone content is standard conditional probability

Once genuine phase laws and their full LDPs are assumed, the finite-mixture rate

\[
\min_j(\alpha_j+I_j)
\]

and the corresponding conditional decomposition are elementary. The nontrivial mathematics lies in constructing the phase basins and proving the platform-specific LDP, coefficient, Gaussian, and semigroup theorems. D1 proves none of them.

## Dependency and editorial assessment

D1 is the terminal dependency hub. A2–A4, B1–B4, C1, and C2 all remain open or false in essential respects. A synthesis paper cannot close those gaps by assuming phase-wise versions of their conclusions.

The correct editorial action is to remove D1 as a standalone manuscript. Any valid finite-mixture lemma can be placed in a short appendix of a future platform paper after an actual microscopic phase decomposition is established.

## Recommendation

**Reject; remove as a standalone submission.** The pressure theorem double counts phase weights, the projective labels are undefined, and every model-specific hypothesis is assumed rather than proved. No independent top-four contribution remains.
