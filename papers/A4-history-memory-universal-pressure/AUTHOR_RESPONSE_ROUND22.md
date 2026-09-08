# Author response to Referee Round Twenty-Two — A4

The referee's two algebraic contradictions are accepted.  The former transmission-zero construction and the false high-frequency cancellation have been removed, not patched by terminology.

## A4.1 — history minorization

The active proof uses three distinct scales.  A Lyapunov weight controls mark size, stable hyperbolicity controls the influence of remote marks on the future kernel, and a bounded history metric controls topological truncation.  On a Lyapunov sublevel a remote mark can retain order-one Lyapunov mass, but its effect on the kernel is bounded by a geometric factor `(theta/rho)^n`.  The synchronized small-set proof uses this influence bound and a finite connector cover; it never asserts uniform smallness of the Lyapunov tail.

## A4.2 — rough paths

The observable is required to lie in the same weighted Lipschitz Banach space on which the spectral gap is proved, in addition to a `2+epsilon` moment.  The Poisson solution, martingale-coboundary decomposition, and second level are therefore typed and bounded.

## A4.3 — renewal factorization

Entry, exit, residual-flight, and history-return operators now have explicit source and target spaces.  The renewal resolvent is proved by a first/last-return decomposition and then continued meromorphically.

## A4.4 — exact memory algebra

For a closed block generator the active kernel is

`K(t)=PLQ exp(t QLQ) QLP`,

with transform

`Khat(z)=PLQ (z-QLQ)^{-1} QLP`.

Its generic expansion begins with `z^{-1} PLQLP`, exactly as the report computes.  Exponential time decay follows from the orthogonal semigroup.  For absolutely integrable vertical inversion, the explicit term `PLQLP/(z+omega)` is subtracted and inverted separately; the remainder is `O(z^{-2})`.

The paper no longer adjoins the residue of a holomorphic full resolvent.  Genuine poles are handled only by genuine Riesz projections.  The compressed resolvent is related to the full generator by the exact Schur--Feshbach identity on declared domains.

The positive history pressure, rough-path, renewal, and forced-memory results are retained with the corrected definitions and algebra.
