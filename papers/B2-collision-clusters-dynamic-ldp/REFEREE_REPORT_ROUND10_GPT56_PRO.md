# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** B2 — Collision Clusters and Dynamic LDP  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `a8bf65a2b25be63ede058d2b701c24d917299f6f5713216dccb4abf1261a27e2`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

The revision makes worthwhile structural changes. It defines the collision trace as part of a closed transport graph, retains the true reflected future, abandons the QR-reset argument, and places the first-surplus estimate in an integrated flux formulation. It also correctly orders the grand-canonical theorem before B1's microcanonical transfer.

The central hard-sphere theorem is still absent. The proof of the integrated Jacobi estimate makes an invalid leap from “a real-analytic minor is not identically zero” to a sublevel exponent uniform in genealogy depth. The one-block error contains a mesh-independent recollision term that cannot be sewn uniformly over vanishing partitions. The proposed conservative regularization reduces an infinite-dimensional balance defect to a finite incidence equation without proof. Consequently the all-contact pressure and full joint LDP remain formal.

## Major mathematical objections

### 1. Nonzero analytic minors do not give a depth-uniform Łojasiewicz exponent

The key lemma asserts

\[
\mathfrak m_m\{s_{\min}(J_\lambda)<\rho\}
\le C^m\rho^\beta
\]

with one \(\beta>0\) independent of genealogy depth \(m\). Its proof says that determinant minors are nonzero analytic functions and invokes quantitative analytic sublevel estimates.

That inference is false without a uniform bound on analytic complexity and vanishing order. The elementary family

\[
f_m(x)=x^m
\]

consists of nonzero real-analytic functions on a fixed interval, but

\[
|\{x:|f_m(x)|<\rho\}|\asymp\rho^{1/m}.
\]

No positive exponent \(\beta\) works uniformly in \(m\), and multiplying the constant by \(C^m\) does not repair the exponent.

Compositions of \(m\) free flights and specular collision maps have analytic complexity and possible vanishing order growing with \(m\). The “first separating fork” proves at most that a suitable minor is not identically zero; it does not bound its order of vanishing. This is the exact estimate needed to make the surplus gain independent of depth.

### 2. Semi-dispersing hard-sphere geometry is not reduced to a positive two-volume argument

Hard-sphere flows have neutral directions, simultaneous/symmetric collision degeneracies, and long products of incidence factors. Symplecticity preserves total phase-space volume, not the smallest singular value of the projected map from selected fork variables to two physical contact coordinates.

The paper must identify a specific minor, control all grazing and multiple-collision singularities, and prove a flux-weighted inverse-moment estimate. The one-paragraph statement that independent translations cannot remain focused does not establish rank two at the surplus contact or an integrable inverse Jacobian.

### 3. The first-surplus theorem collapses if \(\beta\) depends on depth

The optimization

\[
\rho=\varepsilon^{2/(\beta+2)}
\]

gives \(\varepsilon^{2\beta/(\beta+2)}\) only for a fixed \(\beta\). If the actual sublevel exponent is \(\beta_m\to0\), the \(\varepsilon\)-gain degenerates with genealogy depth and cannot be absorbed by a factor \(C^m\) or by the time simplex.

Thus the asserted \(\alpha_0>0\) uniform over all connected genealogies has not been proved. This is the load-bearing estimate for every later source and LDP statement.

### 4. The one-block estimate cannot be sewn uniformly over vanishing meshes

The block error contains

\[
C_R\bigl(h\varepsilon^\eta+arepsilon^{\alpha_0}+h^2\bigr).
\]

A horizon \(T\) partitioned into \(T/h\) blocks accumulates the middle term as

\[
C_RT\varepsilon^{\alpha_0}/h.
\]

This does not vanish uniformly over partitions with mesh \(h\downarrow0\). One may take the iterated limit \(\varepsilon\to0\) at fixed \(h\), followed by \(h\to0\), or impose a diagonal condition \(h\gg\varepsilon^{\alpha_0}\). The theorem instead claims source-uniform partition refinement and partition independence without declaring such an order of limits.

Chapman–Kolmogorov does not cancel a norm error of fixed size per block.

### 5. The hierarchy is an analytic scale, not a semigroup on one declared Banach space

The creation operator is bounded from \(\mathfrak X_\alpha\) to \(\mathfrak X_{\alpha'}\) only for \(\alpha'<\alpha\). Picard iteration with a loss of radius can construct a short-time analytic-scale evolution, but it is not a strongly continuous semigroup on one fixed Banach space without an Ovsyannikov-type theorem and explicit radius budget. The manuscript calls it a generated semigroup without supplying that theorem.

This matters for the operator norms and repeated products used in the sewing argument.

### 6. The “exact conservative regularization” is not constructed

The proof proposes to truncate velocity by a radial retraction on each energy–momentum shell, convolve in space and time, and repair the remaining defect by a finite cell incidence matrix. Several nontrivial requirements are skipped:

- a radial truncation cannot in general preserve total momentum and energy pointwise for an arbitrary multi-particle distribution;
- the weak kinetic balance defect is a function/distribution of continuous variables, not a finite-dimensional vector merely because space-time is partitioned into cells;
- a signed contact correction must satisfy collision kinematics, pre/post symmetry, positivity, and absolute continuity with respect to \(A_{f_h}\);
- a bounded right inverse uniform under mesh refinement is not established; and
- adding a small Maxwellian background need not dominate a correction whose norm blows up as the mesh shrinks.

The lower-bound extension to all finite-action paths therefore rests on an unproved density theorem.

### 7. A bounded local source expansion does not yield the full entropy LDP

The cluster expansion is established only on a bounded complex source ball. The full Poisson entropy action requires exposing collision ratios \(q=d\Gamma/dA_f\) with arbitrarily large \(\log q\), detecting singular currents, and separating every failure of the balance constraint. The manuscript does not prove a global real-source exhaustion or a monotone approximation compatible with the one-block estimates.

Convex duality on a neighborhood of zero gives a local rate branch, not the full good path-space LDP claimed in the main theorem.

## Dependency and editorial assessment

B2-GC is the first gate in the hard-sphere chain. Since the depth-uniform Jacobi/coarea theorem is not proved, B1's dynamic source input, B2-MC, B3, B4, C1, C2, and D1 remain conditional.

A publishable paper should focus on the integrated first-surplus theorem itself, with a rigorously typed trace space, a uniform inverse-Jacobi estimate, and a source-uniform connected expansion. The current manuscript states all of these and proves none at the required level.

## Recommendation

**Reject.** The central depth-independent recollision gain rests on an invalid analytic-sublevel inference. The subsequent sewing, regularization, and full LDP do not close independently.
