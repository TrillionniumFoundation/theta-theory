# Referee Report

**Manuscript:** B1 — Microcanonical Preparation  
**Recommendation:** **Reject**  
**Standard applied:** Annals / Acta / Inventiones / JAMS  
**Review target:** pinned eleven-paper clean-main tree, SHA-256 `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`.

## Overall assessment

The paper’s key claim is an exponential-scale transfer from a conditioned fixed-\(N\), fixed-momentum, fixed-energy hard-sphere shell to a hard-core grand-canonical ensemble with one-particle density \(f_a^0\), uniformly for bounded path and collision sources. This theorem is load-bearing for B2–D1.

As stated, it is false. Ordinary equivalence of ensembles does not imply equality of extensive log-Laplace functionals under arbitrary sources. At exponential scale, a source changes the saddle in the conserved/macro variables. The proof fixes the zero-source information projection and thereby misses an order-\(\mu_\varepsilon\) contribution.

## Decisive counterexample to the transfer theorem

Take one of the bounded macro observables \(\chi\) used in the preparation and, for simplicity, one scalar constraint
\[
\frac1N\sum_{i=1}^N\chi(z_i)\approx a.
\]
Choose an allowed bounded path source that depends only on time zero:
\[
h(z(\cdot))=t\,\chi(z(0)).
\]

Under the conditioned microcanonical law, the empirical mean of \(\chi\) lies in a window \(\delta_\varepsilon\to0\). Hence
\[
\frac1N\log
E_{\mathrm{mc},\,\chi\approx a}
\exp\!\left(t\sum_i\chi(z_i)\right)
\longrightarrow t a
\]
(up to the vanishing window error).

Under the fixed canonical/product law with one-particle density \(f_a^0\),
\[
\frac1N\log
E_{f_a^0}
\exp\!\left(t\sum_i\chi(z_i)\right)
=
\log\int e^{t\chi}f_a^0,
\]
which is strictly larger than \(ta\) for small nonzero \(t\) whenever
\(\operatorname{Var}_{f_a^0}(\chi)>0\). The discrepancy is order \(N\sim\mu_\varepsilon\), not \(o(\mu_\varepsilon)\).

Hard-core exclusion contributes only a lower-order correction in the Boltzmann–Grad dilute regime and cannot cancel this elementary convexity gap. The counterexample already exists at time zero, so short-time cluster analyticity is irrelevant.

Thus the asserted uniform equivalence for arbitrary bounded single-particle path sources fails on the manuscript’s own source class.

## Additional major objections

### 1. The correct source-dependent saddle is missing

A microcanonical scaled cumulant generating function is generally a constrained variational pressure. Its canonical representation requires reoptimizing the multipliers for momentum, energy, particle number, and the \(\chi\)-constraints as the source varies, or taking an explicit Legendre/Fourier coefficient of the source-dependent grand-canonical pressure.

The paper instead substitutes the zero-source saddle \(f_a^0\) into the source-decorated pressure. This is exactly the invalid step exposed by the counterexample.

### 2. Static hard-core volume estimates do not prove dynamical ensemble transfer

The estimate \(N^2\varepsilon^3=O(\varepsilon^{-1})=o(\varepsilon^{-2})\) is a crude static excluded-volume bound. It does not establish uniform complex Fourier–Laplace inversion of a dynamical partition function with path and collision sources. One needs source-uniform analyticity in all saddle variables, a nondegenerate Hessian after quotienting conservation laws, contour/tail estimates, and control of the fixed-\(N\) coefficient extraction.

None is supplied.

### 3. The shell and information projection require a complete large-deviation statement

The paper writes down \(f_a^0\) as an exponential family but does not prove the conditional empirical-measure LDP for the hard-core microcanonical shell, uniqueness on the admissible moment set, or the precise role of the shrinking windows. Nonsingularity of a covariance matrix is only a local condition; it does not guarantee global existence or uniqueness for all declared \(a\).

### 4. “Preparation before dynamics” does not repair exponential nonequivalence

The conceptual insistence that the physical preparation is microcanonical is reasonable. But this makes it more—not less—important to retain the constrained pressure under subsequent exponential tilts. The paper’s transfer erases precisely the correlations induced by the preparation at the scale on which the later LDP is formulated.

## Consequences for the series

B2’s prepared initial cost, B4’s diagonal semigroup limit, and D1’s “microcanonical-to-theta” chain all invoke this theorem. They cannot be considered closed while B1 remains false.

## What a correct replacement would look like

The authors should derive a source-dependent microcanonical pressure of the form
\[
Q_{\mathrm{mc}}(h,\psi)
=
\inf_{\lambda\ \text{for conserved constraints}}
\bigl[Q_{\mathrm{gc}}(h,\psi;\lambda)-\lambda\cdot a\bigr]
-\text{normalization},
\]
with the correct min/max convention and a rigorous coefficient-extraction theorem. Only source classes invariant under the conditioned constraints could admit a simpler fixed-parameter transfer.

## Editorial recommendation

**Reject.** The main theorem is disproved by an allowed time-zero source. This is a foundational, not repair-level, defect.
