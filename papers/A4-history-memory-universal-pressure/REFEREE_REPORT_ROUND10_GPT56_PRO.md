# Independent Referee Report — Round Ten (GPT-5.6 Pro)

**Manuscript:** A4 — History, Memory, and Universal Pressure  
**Reviewed revision:** `revision/round10-referee-positive-closure-11paper-2026-08-31@b45406b03ab45e70461d36da5d3ee64892a92c8f`  
**Controlling mathematical commit:** `101dc123e4bafbb8e140e658ac1390f7735dc67e`  
**Registered module SHA-256:** `ba482a13a4ee2d5ead8277b5aa8c4fc4a9d6fa4979df87793240c30abf6a8969`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject.**

## Executive assessment

The paper has corrected several earlier typing errors. It now conditions on a genuine symbolic past rather than a stable-leaf quotient, uses an eigenfunction Doob transform rather than statewise Feynman–Kac normalization, and writes the causal Volterra sign correctly.

However, the revised Poisson decomposition is still algebraically false. The displayed increment has conditional mean \(Pg\), not zero, and the claimed coboundary identity does not telescope. The memory theorem then assumes a common Hilbert realization and a meromorphic/vertical resolvent theory not supplied by A2, and it again infers exponential memory from insufficient transform information. The headline quenched rough limit and pressure–memory compatibility therefore have no valid foundation.

## Major mathematical objections

### 1. The proposed martingale difference is not centered

The paper defines

\[
h_g=\sum_{n\ge1}P^ng,
\qquad
m_g(H_k,H_{k+1})
=g(H_{k+1})+h_g(H_{k+1})-Ph_g(H_k).
\]

Since

\[
(I-P)h_g=Pg,
\]

one has

\[
P(g+h_g)=Pg+Ph_g=h_g,
\]

not \(Ph_g\). Therefore

\[
\mathbb E[m_g(H_k,H_{k+1})\mid\mathcal F_k]
=h_g(H_k)-Ph_g(H_k)=Pg(H_k),
\]

which is generally nonzero.

The proof explicitly writes the false identity

\[
P(g+h_g)=Ph_g.
\]

This is a direct algebraic contradiction, not a missing estimate. The repository hostile script checks for the presence of this string but does not verify the equality.

A correct choice is possible—for example, with \(h=\sum_{n\ge0}P^ng\), the increment \(h(H_{k+1})-Ph(H_k)\) is centered—but the theorem and every formula depending on the current \(m_g\) must be rewritten.

### 2. The claimed coboundary decomposition does not telescope

Summing the manuscript's increment gives

\[
\sum_{j=0}^{n-1}m_g(H_j,H_{j+1})
=
\sum_{j=1}^{n}g(H_j)
+
\sum_{j=1}^{n}h_g(H_j)
-
\sum_{j=0}^{n-1}Ph_g(H_j).
\]

The last two sums are not equal to \(Ph_g(H_n)-Ph_g(H_0)\). Hence the displayed identity for \(\sum g(H_j)\) is also false. The rough invariance principle cannot be invoked from a nonexistent martingale–coboundary decomposition.

### 3. Uniform quenched rough convergence is asserted rather than proved

Even after correcting the algebra, a locally uniform quenched rough invariance principle for a singular billiard suspension requires a precise family of conditional kernels, uniform Poisson estimates, bracket convergence, roof-time inversion, control of exceptional pasts, and second-level tightness. The proof cites “Feller coupling,” “ergodic theorem uniformly on compact history sets,” and an “A3 exponential shield,” none of which has been established at the required strength.

In particular, an ordinary ergodic theorem is not automatically uniform over initial histories. The claimed stable/quenched conclusion is a substantial theorem, not a paragraph-long corollary of spectral mixing.

### 4. The Hilbert realization and compressed resolvent are assumed

A2 constructs, at best, transfer operators on anisotropic Banach scales. A4 then introduces a “common Hilbert realization” of a generator \(L_\Psi\), a finite-rank orthogonal projection \(P\), and inverses of compressed resolvents. No theorem builds this Hilbert space, proves that the Doob dynamics is strongly continuous there, identifies domains of the block operators, or shows that \(C(z)\) is invertible on the required region.

Writing \(L\) as its own \(P/Q\) block matrix is tautological. It does not establish the spectral continuation or memory regularity later attributed to that block decomposition.

### 5. Meromorphic continuation does not yield the claimed residual-memory decay

The paper says that A2 provides finitely many principal parts in every closed strip and that removing them permits a Bromwich contour shift. Neither assertion follows from A2. Ruelle-type generators can have infinitely many resonances in an unbounded vertical strip. More importantly, meromorphic continuation alone gives no decay of the resolvent on vertical lines.

To deduce an exponentially integrable ordinary kernel one needs explicit vertical bounds and removal of all polynomial/instantaneous distributional terms. A transform such as \(\widehat K(z)=1\) is entire and bounded but corresponds to \(\delta_0\), not an exponentially integrable function. The revision does not state the hypotheses excluding this phenomenon.

### 6. The pressure-to-rough-limit passage has no declared scaling theorem

The potential \(\Psi\), the additive observable, time, and amplitude must be scaled consistently for a Feynman–Kac semigroup to converge to a Brownian risk-sensitive semigroup. The proof merely says that analytic perturbation passes \(\lambda_\Psi\) and \(h_\Psi\) through the scaling. It supplies no uniform source neighborhood, normalization, or convergence theorem for those eigen-data.

The memory coordinates are even more delicate: convergence of a path does not imply convergence of an unbounded convolution/resolvent functional without the very residual estimates that remain unproved.

## Dependency and editorial assessment

A4 relies on A2 and A3, both of which retain load-bearing gaps, but it also fails independently through the incorrect martingale algebra. C2 and D1 must not treat A4's optional projections, rough tangent, or memory realization as completed interfaces.

The paper should be split. A corrected past-kernel/Doob construction may form a useful abstract note. A separate model-specific paper would need to prove the quenched rough limit and the analytic memory theorem with complete operator domains and vertical resolvent estimates.

## Recommendation

**Reject.** The central martingale theorem is false by direct conditional expectation, and the model-specific rough and memory theorems are unsupported. The revision does not meet the correctness threshold for any journal, much less a top-four venue.
