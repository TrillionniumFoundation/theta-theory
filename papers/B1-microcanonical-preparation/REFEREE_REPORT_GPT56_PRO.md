# Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — Microcanonical Preparation  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject without invitation to revise**  
**Review object:** SHA-256-pinned eleven-paper source archive `566335121763abaa7ed8ed2280a3b4345877777e8bedbd80f4eef0a6b48745e2`  
**Role in the series:** foundational input for B2, B4, and D1.

## Executive assessment

The central theorem asserts that the extensive path/collision log-Laplace functional under a fixed-particle, fixed-energy, fixed-momentum, moment-conditioned hard-sphere shell is asymptotically equal to the corresponding functional under a fixed grand-canonical/canonical law with one-particle density \(f_a^0\), uniformly over the declared bounded source class.

That theorem is false. The failure occurs already at time zero, before any hard-sphere dynamics or recollision analysis enters. Conditioning a macro observable and then exponentially tilting by that same observable is not equivalent, at speed \(N\), to evaluating the tilt under the zero-source canonical information projection. The source changes the saddle in the conserved/macro variables, producing an order-\(N\) discrepancy.

Because the false transfer is the principal bridge from physical preparation to the later dynamic theory, this is a fatal series-level obstruction.

## Decisive counterexample

Let \(\chi\) be one bounded macro observable used in the preparation and suppose the shell conditions on

\[
\frac1N\sum_{i=1}^N \chi(z_i)\in[a-\delta_N,a+\delta_N],
\qquad \delta_N\to0.
\]

Choose the allowed bounded path source

\[
h(z(\cdot))=t\,\chi(z(0)).
\]

Under the conditioned law, the exponent satisfies

\[
tN(a-\delta_N)
\le
 t\sum_{i=1}^N\chi(z_i)
\le
 tN(a+\delta_N)
\]

for \(t>0\) (with the inequalities reversed for \(t<0\)). Hence

\[
\frac1N\log E_{\mathrm{mc},\,\chi\approx a}
\exp\left(t\sum_i\chi(z_i)\right)
\longrightarrow ta.
\]

Under the fixed product/canonical law with one-particle density \(f_a^0\),

\[
\frac1N\log E_{f_a^0}
\exp\left(t\sum_i\chi(z_i)\right)
=
\log\int e^{t\chi}f_a^0.
\]

Since \(\int\chi f_a^0=a\), strict convexity gives, for small nonzero \(t\),

\[
\log\int e^{t\chi}f_a^0
=
 ta+\frac{t^2}{2}\operatorname{Var}_{f_a^0}(\chi)+o(t^2)
>
 ta
\]

whenever the variance is nonzero. Therefore the difference is order \(N\), i.e. order of the claimed Boltzmann–Grad large-deviation speed, not \(o(N)\).

Hard-core excluded-volume corrections are lower order in the dilute scaling used in the manuscript and cannot cancel this convexity gap. Short-time dynamics is irrelevant because the counterexample is supported at time zero.

## Further major objections

### 1. The source-dependent constrained saddle is omitted

The correct microcanonical scaled cumulant generating function is a constrained variational pressure. When a source is introduced, the multipliers for particle number, energy, momentum, and the prepared moments must generally be reoptimized. Equivalently, one must extract a source-dependent Fourier/Laplace coefficient from the grand-canonical partition function.

The manuscript freezes the zero-source information projection \(f_a^0\) and substitutes it into a source-decorated pressure. The counterexample shows exactly why this step is invalid.

### 2. Ordinary equivalence of ensembles is being used at the wrong scale

Equivalence for fixed local observables, law-of-large-numbers quantities, or finite marginals does not imply equality of extensive log-Laplace functionals. Exponential tilts probe a new variational saddle. The paper repeatedly moves from local ensemble equivalence to an exponential-scale identity without proving the required source-uniform coefficient extraction.

This is not a technical strengthening of a standard theorem; it is a different theorem and, on the stated source class, a false one.

### 3. Static excluded-volume estimates do not establish a dynamical inversion theorem

The observation that a crude hard-core volume correction is subleading at the target speed does not prove uniform complex Fourier–Laplace inversion of a dynamical partition function with path and collision sources. A valid theorem would require:

- analytic control in all saddle variables and sources;
- a nondegenerate Hessian after conservation-law quotients;
- contour deformation and tail estimates;
- fixed-\(N\) coefficient extraction;
- control uniform in the shrinking shell widths; and
- a proof that exceptional hard-core configurations remain negligible after tilting.

None is supplied.

### 4. The conditional information projection itself needs a complete LDP

The exponential-family formula for \(f_a^0\) does not prove existence and uniqueness on the entire announced parameter set. The paper needs a conditional empirical-measure LDP for the hard-core microcanonical shell, an admissible moment set, global existence of multipliers, and a precise window regime. Invertibility of a local covariance matrix is only a local condition.

### 5. “Preparation occurs before dynamics” strengthens rather than removes the objection

Because the preparation is genuinely microcanonical, its constraints remain present under later exponential evaluation. The manuscript's fixed-parameter transfer discards the very correlations created by the preparation at the same speed used for the LDP. The conceptual narrative and the theorem are therefore in direct tension.

## Consequences for the series

B2's prepared initial rate, B4's microcanonical diagonal semigroup limit, and D1's deterministic microcanonical-to-theta hierarchy cannot use B1 as a valid bridge. Any downstream theorem depending on an \(o(\mu_\varepsilon)\) transfer for arbitrary bounded sources is invalid until replaced by a source-dependent constrained pressure.

## Correct replacement

A plausible corrected object has the schematic form

\[
Q_{\mathrm{mc}}(h,\psi;a)
=
\inf_{\lambda}
\left\{Q_{\mathrm{gc}}(h,\psi;\lambda)-\lambda\cdot a\right\}
-C(a),
\]

with the sign convention determined by the coefficient extraction and with all conserved quantities included. A simpler fixed-saddle formula can hold only for a source class orthogonal/invariant to the conditioned constraints, which must be stated explicitly.

## Recommendation

**Reject without invitation to revise.** The main theorem is disproved by an allowed time-zero source. The manuscript requires a new central theorem, not a repair of exposition or estimates.
