# Round-Eight Independent Referee Report — GPT-5.6 Pro

**Manuscript:** B1 — *Microcanonical Preparation and Exponential-Scale Ensemble Transfer for Deterministic Hard Spheres*  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**  
**Reviewed revision branch:** `revision/round8-referee-positive-closure-11paper-2026-08-31`  
**Reviewed branch head:** `ad2b5106678b29b7d9ffb3824f61ddbd141ac4b8`  
**Reviewed tree:** `00d7ef9edcddda26fc88962e206677f9b399bebe`  
**Active controlling module:** `ROUND8_POSITIVE_CLOSURE.tex`, blob `b88d781a0ebf2edf8d3e68f7000d8855e9aa1e5c`

## Executive assessment

Round eight correctly abandons the false claim that a one-particle momentum–energy mark has a full-dimensional density. It also introduces explicit rank assumptions and a plausible regenerative mechanism: a typical large compound-Poisson sample contains linearly many disjoint smooth convolution blocks, while the low-particle sectors are exponentially small.

That argument proves, at best, a local-limit theorem for an ideal independent compound-Poisson mark sum. The paper is about a source-decorated grand-canonical hard-sphere law, whose logarithm contains connected hard-core and dynamical clusters. Round eight removes the connected remainder from the theorem rather than controlling it. The “exact finite saddle” is then simply assumed. Moreover, the displayed shell coefficient is incorrect for the allowed widths `w_mu=o(sqrt(mu))`: undoing a nonzero saddle tilt contributes an exponential factor varying across the shell, which cannot be pulled out as one constant unless the width is `o(1)` or that factor is retained inside the integral.

## Genuine repairs recognized

The revision should retain:

- explicit affine-span and submersion assumptions on the constraint marks;
- recognition that the one-particle law is singular;
- good-block regeneration rather than treating one smooth component as the whole convolution;
- explicit retention of empty and low-particle sectors;
- use of the exact finite-volume saddle in principle;
- distinction between extensive and normalized shell variables.

## Major mathematical objections

### 1. The theorem analyzes a compound-Poisson proxy, not the hard-sphere pressure

The normalized pressure is replaced by

\[
Q(\lambda)=\int(e^{\lambda\cdot X(v)}-1)d\nu(v),
\]

which is the exact logarithmic pressure of independent Poisson marks. The actual prepared hard-sphere numerator includes:

- hard-core exclusion correlations;
- path and actual-contact sources;
- connected collision clusters from B2;
- source-dependent changes in those connected terms.

Previous versions at least wrote a connected remainder and attempted to bound its frequency derivatives. Round eight omits it entirely. The good-block Bernoulli indicators are independent only under the ideal product/Poisson law; they are not independent under a general source-decorated connected cluster law.

No comparison theorem shows that the omitted term is negligible at the coefficient scale, uniformly in complex frequency and source derivatives.

### 2. The finite saddle is introduced without a finite hard-sphere theorem

The text says “let `(lambda_mu,theta_mu)` be the unique exact finite saddle.” Existence, uniqueness, compactness, and analytic source dependence are not proved for the actual finite hard-sphere pressure.

The covariance lemma concerns the limiting ideal compound pressure. It does not control the Hessian of the finite source-decorated pressure after connected corrections. Thus the saddle on which the shell coefficient rests is an assumption.

### 3. The relative shell formula omits the variation of the saddle likelihood across the shell

After tilting at a saddle `lambda_mu`, undoing the tilt gives, schematically,

\[
\mathbb P\{Y-y_\mu\in w_\mu B\}
=e^{-\mu I_\mu}
\mathbb E_{\rm tilt}
\left[e^{-\lambda_\mu\cdot(Y-y_\mu)};
Y-y_\mu\in w_\mu B\right].
\]

The manuscript replaces the expectation by an unweighted Gaussian integral. That is valid only if

\[
\sup_{z\in w_\mu B}|\lambda_\mu\cdot z|=o(1),
\]

for example `w_mu=o(1)`, or if the exponential factor is kept inside the integral.

The stated condition is only

\[
w_\mu=o(\sqrt\mu),
\]

which allows `w_mu=mu^{1/4}`. For a nonzero multiplier, the likelihood varies by `exp(O(mu^{1/4}))` across the shell. It is subexponential at speed `mu`, but it destroys the claimed relative coefficient `(1+o(1))`.

The theorem could support a logarithmic `o(mu)` shell cost under a much wider regime; it does not support the displayed sharp coefficient.

### 4. The good-block construction needs a rigorous randomized decomposition

The proof introduces an “independent partition coin” to assign a cutoff label. It does not define the joint law of that coin and the marks or prove that, conditional on being good, each block has the stated uniformly normalized `W^{k,1}` density. Overlapping cutoff patches require a partition of unity whose normalization depends on the sample and source.

This can likely be repaired for an independent product law, but it is not written as a theorem and it becomes substantially harder after connected hard-sphere reweighting.

### 5. High-frequency decay of the ideal law is not enough for the mixed coefficient

The estimate

\[
Ce^{-c\mu}+C_k(1+|\xi|)^{-k}
\]

is stated only for the compound continuous characteristic function. A mixed lattice–continuous inversion also requires:

- exact lattice span and exclusion of all other dual-lattice points;
- uniform small- and intermediate-frequency estimates;
- source derivatives of the full characteristic function;
- a density theorem on the target chart, including the connected correction.

These are not proved.

### 6. The admissibility assumption is not verified for the preparation observables

The paper now correctly excludes redundant constraints, but it does so by declaring admissibility. It does not show that the actual collection of energy, momentum, and additional moments used elsewhere in the series satisfies the product submersion condition on a positive-activity patch uniformly over the source chart.

The result is therefore conditional even at the ideal compound level.

### 7. The prepared LDP does not follow from the stated coefficient theorem alone

The final proof invokes “the finite-source Laplace principle” and exponential tightness. A full conditional empirical-measure LDP additionally needs compatible lower bounds on a separating source family, boundary points of the moment set, and a topology in which the conditioned effective domain is closed. None is developed in this module.

### 8. The dependency on B2 remains circular unless the full complex remainder is upstream

B1 is used to transfer B2-GC to B2-MC. It may use the already established B2-GC pressure as an input, but then it needs the B2 pressure with all mixed constraint frequencies on the exact complex domains used here. The current B2 theorem does not supply that coefficient packet, and B1 silently replaces it by a pure compound law.

## Required reconstruction

A valid B1 theorem must start from the exact finite B2-GC source-decorated pressure and prove a decomposition

\[
Q_\varepsilon=Q_{\rm singleton}+R_\varepsilon
\]

with frequency and source-derivative estimates strong enough for mixed inversion. The regenerative smoothing can control the singleton factor, but the connected factor must be retained. The finite saddle must then be proved for the full pressure. Finally, the shell theorem must either include the factor `exp(-lambda_mu z)` inside its Gaussian integral or restrict to a genuinely local extensive width.

## Recommendation

**Reject.** The regenerative idea is promising for the independent singleton sector, but the manuscript no longer proves a coefficient theorem for the actual hard-sphere law, and the displayed sharp shell asymptotic is false in the allowed width regime.