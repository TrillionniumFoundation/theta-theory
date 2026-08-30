# Revision-Round Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject without invitation to revise**  
**Reviewed source:** `main@ae2fdc16bf1ad4a6b58cca6020a7b8b61236e2ad`, manuscript blob `977c19aba57823b32fcf4679f717ba5f64e34521`  
**Revision provenance:** no revised B1 source is materialized on the repository's discoverable eleven-paper revision ref. This report reviews the current controlling `main` source.

## Overall assessment

The abstract now says that the paper proves transfer to a “source-dependent information projection.” The actual theorem and proof do not do this. They still fix the zero-source one-particle density \(f_a^0\) and claim \(o(\mu_\varepsilon)\) agreement between conditioned microcanonical and fixed hard-core grand-canonical log-Laplace functionals uniformly over arbitrary bounded path and collision sources.

That theorem remains false. The contradiction occurs at time zero and uses an allowed source from the manuscript's own class. Consequently no dynamical cluster estimate, short-time restriction, hard-core correction, or diagonal choice can repair it. Since B1 is the preparation input for B2, B4, and D1, the defect propagates through the hard-sphere half of the series.

## Decisive counterexample

Let \(\chi\) be one of the bounded macro observables used in the preparation, and suppose the conditioned shell imposes

\[
\left|\frac1N\sum_{i=1}^N\chi(z_i)-a\right|\le\delta_N,
\qquad \delta_N\downarrow0.
\]

Choose the bounded single-particle path source

\[
h(z(\cdot))=t\,\chi(z(0)).
\]

This is an allowed time-zero path source. Under the conditioned microcanonical law,

\[
tN(a-\delta_N)
\le t\sum_{i=1}^N\chi(z_i)
\le tN(a+\delta_N)
\]

for \(t>0\), with the inequalities reversed for \(t<0\). Therefore

\[
\frac1N\log
E_{\mathrm{mc},\,\chi\approx a}
\exp\left\{t\sum_{i=1}^N\chi(z_i)\right\}
\longrightarrow ta.
\]

Under the fixed product/canonical representation with one-particle density \(f_a^0\),

\[
\frac1N\log
E_{f_a^0}
\exp\left\{t\sum_{i=1}^N\chi(z_i)\right\}
=
\log\int e^{t\chi}f_a^0.
\]

Since \(\int\chi f_a^0=a\),

\[
\log\int e^{t\chi}f_a^0
=
ta+\frac{t^2}{2}\operatorname{Var}_{f_a^0}(\chi)+o(t^2),
\]

which is strictly larger than \(ta\) for small nonzero \(t\) whenever the variance is positive. The difference is order \(N\asymp\mu_\varepsilon\), not \(o(\mu_\varepsilon)\).

The counterexample is independent of the hard-sphere dynamics. It already holds at \(T=0\). Static hard-core corrections of order \(o(\mu_\varepsilon)\) cannot cancel an order-\(\mu_\varepsilon\) convexity gap.

## Major objections

### 1. The abstract and theorem are internally inconsistent

The abstract advertises a source-dependent information projection. The theorem concludes that the technical density is \(f_a^0\), and the proof says that the nonsingular covariance gives a unique saddle with activity \(f_a^0\), after which source-decorated pressure is evaluated at that activity.

A genuinely source-dependent transfer would reoptimize the multipliers for particle number, momentum, energy, and the \(\chi\)-constraints as the source varies. That reoptimization is absent. Renaming the theorem does not change its mathematics.

### 2. Equivalence of ensembles is being used at the wrong scale

Local or macrostate equivalence does not imply equality of extensive log-Laplace functionals. An exponential source changes the variational saddle. The conditioned ensemble constrains the empirical \(\chi\)-mean, while the fixed canonical ensemble allows it to move under the source. This is exactly the mechanism exposed by the counterexample.

The paper needs a source-dependent constrained pressure, not a uniform fixed-saddle transfer.

### 3. The Fourier–Laplace inversion argument omits source-dependent saddle equations

A valid coefficient-extraction theorem would begin from the full source-decorated grand-canonical partition function and solve the saddle equations including the source. It would need:

- analytic dependence on all constraint multipliers and sources;
- a nondegenerate constrained Hessian after conservation-law quotients;
- contour and tail estimates uniform in the source ball;
- fixed-\(N\) coefficient extraction; and
- control of shrinking shell windows.

The proof merely states that the zero-source saddle remains usable and that substituting it changes pressure by \(o(1)\) per particle. The time-zero example proves that assertion false.

### 4. The static hard-core estimate is irrelevant to the main obstruction

The estimate

\[
N_\varepsilon^2\varepsilon^3=O(\varepsilon^{-1})=o(\mu_\varepsilon)
\]

may control a crude excluded-volume correction in the dilute regime. It does not establish source-uniform dynamical ensemble transfer, and it cannot correct the mismatch between a constrained and unconstrained empirical observable at order \(N\).

### 5. The conditional information projection itself is not fully established

The exponential-family formula for \(f_a^0\) is written under local covariance nonsingularity. The paper does not prove the hard-core conditional empirical-measure LDP, global existence of multipliers on the declared moment set, uniqueness beyond a local neighborhood, or the exact admissible window regime. These are additional gaps, although the direct counterexample is already decisive.

### 6. The correct replacement changes every downstream formula

A plausible microcanonical pressure must have a constrained variational or coefficient-extraction form, schematically

\[
Q_{\mathrm{mc}}(h,\psi;a)
=
\inf_{\lambda}
\{Q_{\mathrm{gc}}(h,\psi;\lambda)-\lambda\cdot a\}
-C(a),
\]

with all conservation and preparation constraints included and with the correct sign convention. Only special sources invariant under the conditioned constraints could admit a fixed-saddle simplification.

B2's initial cost, B4's diagonal semigroup limit, and D1's microcanonical-to-theta chain must all be reformulated around this constrained source-dependent object.

## Status of prior objections

The revised abstract recognizes the need for source dependence, which is conceptually correct. The theorem and proof, however, have not been changed to implement it. The decisive prior counterexample therefore remains fully applicable.

## Editorial recommendation

**Reject without invitation to revise.** The central theorem is false on the stated source class. A new manuscript would require a different theorem with a source-dependent constrained saddle, not a repair of estimates or exposition.
