# Author proof audit — R69

This is author-side proof analysis, not a new independent report. The original title and Annals / Acta / Inventiones / JAMS aim remain unchanged.

| Result | Load-bearing proof | Adversarial boundary check |
|---|---|---|
| Exact spectral response criterion | Three-mode characteristic recurrence in the lower; maximal-modulus eigenvector normalized at the counted initial state in the upper | Arbitrary reducible Q; arbitrary phase; nonzero contrast; legal decoder range; no free initialization |
| Stochastic sector lemma | Poisson stochastic semigroup; convex eigenvector polygon; inward edge velocity; strict log-cos concavity | Zero lies in polygon interior even for reducible Q; consecutive angular gaps < pi; all factors positive; equality forces all M distinct vertices |
| First-sector optimizer | Explicit convex mixture of I, directed cycle and uniform matrix | Global lower for every Q; exact endpoint; no symmetry assumption in lower; cyclic controllability fixes decoder |
| Worst-phase exact count | Polygon inradius upper; preceding-sector midpoint lower | Adverse phase depends on alpha; integer threshold equality handled; K=3 separately by rank |
| Fixed-phase cubic-root law | Global c/k arithmetic lower plus elementary pigeonhole approximation; power-sector lower and denominator-sensitive polygon upper | Same fixed phase at every noise; explicit constants; not numerical scaling; no statement for phases without this arithmetic certificate |
| Original algebraic phase lower | Nonzero Gaussian-integer numerator plus the same power-sector estimate | Uses irrationality of (3+4i)/5 only, not an unproved badly-approximable property; logarithmic lower is not matched |
| Degenerate cases | Explicit two-state real eigenmode and nonconstant-response lower | alpha=0, gamma=0, lambda=-1,0,1; no invalid three-mode rank argument |
| Physical squared-task consequence | Inherited actual three-outcome POVM and unique optimal response in thm:r67-embedding | Fixed dictionary; first call paid; protected dimension four is not observer memory; known prepared phase rather than an unknown phase oracle |

The sector inequality and its Type-0 equality classification are classical and explicitly credited. The full Karpelevic boundary theorem is not a hidden premise of the rate proof. The only number-theoretic tool needed is proved by pigeonhole; the quadratic example has a direct integer-polynomial global certificate. Numerical checks do not stand in for any of these steps.

The new independent diagnostics include a noncirculant stochastic matrix whose maximal eigenvector coordinate is not the original first coordinate, exact all-time intertwining certificates, physical POVM/loss calculations, endpoint realizations, Gaussian-integer bounds, scalar degeneracies, raw damped Bloch dynamics, and actual directional circulant rows. The tested powers/parameters remain finite. Ordinary and optimized execution must agree, with every failure raising an exception rather than relying on assert statements.

The prior R68 instrument-wide state-positive theorem, weighted stopping criterion, robust tied face and all other current inherited results retain their separate proof audits under retained/r68-native. No previously closed issue is reopened merely to increase the revision count. No full archival mathematical reproof or independent human approval is claimed.

The finite-spectral-mixture theorem additionally treats a fixed finite collection of nonzero phase modes on a higher-dimensional protected carrier. Its lower retains every spectral obstruction and the full 2r+1 Hankel rank; its upper counts the initial mixture label and any constant tail block. It yields the same matched cubic-root exponent for certified fixed phase lists, not a universal theorem for arbitrary multi-frequency positive realizations.
