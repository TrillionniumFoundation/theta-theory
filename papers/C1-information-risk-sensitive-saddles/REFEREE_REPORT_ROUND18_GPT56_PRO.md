# Referee Report — Round 18 (Independent Harsh Review)

**Paper:** C1 — *Typed Control, Information, and Saddle Envelopes for Kinetic Cotangent Phases*  
**Version reviewed:** `revision/round17-referee-positive-closure-11paper-2026-09-01@d13b48757f85d9ec1c6998f89c861845094891fa`  
**Controlling source:** `ROUND17_POSITIVE_CLOSURE.tex` (`C1_REGULAR_FILTER_QMD.tex`)  
**Date:** 1 September 2026  
**Editorial recommendation:** **REJECT**  
**Present mathematical status:** The filter chart, belief-state DPP, LAN, and Bernstein–von Mises conclusions are not proved.

## 1. Overall assessment

The manuscript correctly acknowledges a basic obstruction that earlier versions did not: disintegration is not continuous under arbitrary weak convergence of joint laws. Restricting continuity claims to dominated positive-evidence charts is the right strategy. It is also reasonable to retain an unnormalized kernel/evidence object rather than normalize before treating zero-evidence strata.

The proposed implementation is not mathematically complete. The one-step belief kernel is not fully specified, the regular chart assumes domination and Sobolev regularity that the upstream models do not provide, the zero-evidence blow-up is not constructed as a measurable state space, and the dynamic-programming hypotheses are not verified. Most importantly, quadratic-mean differentiability plus an asserted score CLT is promoted directly to triangular-array LAN and a strategy-uniform Bernstein–von Mises theorem. Those implications require substantial additional uniform likelihood and posterior-concentration arguments that are absent.

## 2. Decisive mathematical objections

### 2.1. [FATAL] The filtering model and unnormalized kernel are incompletely defined

The paper writes

\[
\Lambda^a_\pi(dx,dy)=\pi(dx)K^a(x,dy)
\]

and calls this a one-step joint kernel. A filtering transition normally involves a hidden-state transition from `x` to `x'` and an observation conditional on the new or current state. The object above is only a joint law of the **old** state and an observation unless `K^a` secretly includes both transition and observation and returns a measure on `(x',y)`. The notation and subsequent posterior update do not say which state is being conditioned.

The proof later speaks of “prediction followed by observation” and of exact microscopic transition kernels, but neither the transition operator nor the composition with the observation kernel is written. Without this, the belief update, Markov property, control timing, likelihood increments, and DPP are not well defined.

### 2.2. [FATAL] The regular chart assumes a common dominating structure that is not part of its definition

The chart is described through densities `k_\pi^a(x,y)` with respect to a reference observation measure `\nu`, with

\[
c\le k_\pi^a(x,y)\le C,
\qquad
\|k_\pi^a\|_{W_y^{s,1}(C^1_{W,x})}\le M.
\]

The dominated-disintegration proof then embeds both joint kernels in a fixed dominating measure `m_0(dx)\nu(dy)` and estimates an `L^1_W` difference of their densities. No such `m_0` appears in the chart definition. Beliefs in `\mathcal P_W(E)` can be mutually singular, so the factor `m(dx)` cannot be absorbed into one fixed density without an explicit domination hypothesis.

Even if each observation law is dominated in `y`, posterior measures in `x` may remain singular relative to one another. The displayed pointwise estimate compares `j(x,y)m(dx)` with `\tilde j(x,y)\tilde m(dx)` as though both had densities against `m_0`; this is an additional strong condition. The theorem therefore does not apply to the global belief class stated in the paper.

### 2.3. [FATAL] The “model-derived regular filter chart” is not derived from A2/B1/B2

Theorem `thm:r17-c1-chart` claims that all relevant Sinai and hard-sphere observations enter a chart with `W_y^{s,1}` regularity for `s>\dim Y`, a uniform positive lower density, `C^1` weighted dependence on the hidden state, and compactness on every source/control compact set.

The cited upstream results do not supply these properties:

1. A2's claimed LLT concerns a four-dimensional vector/return/roof density in a central window, not arbitrary finite-cylinder path observations with hidden-state derivatives.
2. B1's coefficient theorem concerns selected finite constraint vectors, not all particle/contact observation kernels.
3. B2's formal marked pressure gives source derivatives, not Sobolev derivatives of a finite-volume observation density with respect to `y`.
4. Uniform lower bounds hold, at best, on carefully chosen central windows after normalization; they are not global in `x`, belief, control, and observation.
5. The active upstream manuscripts only claim finitely many low-order derivatives. If `\dim Y` is four or larger, the requirement `s>\dim Y` already exceeds the available derivative order.

The statement that derivatives follow by differentiating “the common source kernel before inversion” conflates derivatives with respect to a source parameter and spatial/Sobolev derivatives with respect to the observed value. A Fourier inversion theorem must explicitly control moments of the Fourier transform to yield the latter.

### 2.4. [FATAL] The exponentially good smoothing assertion is unsupported

Atomic finite-volume observations cannot literally lie in an `L^1` density chart. The paper proposes convolution at a vanishing scale and says the smoothing error is exponentially negligible at the governing LDP speed. Approximation in a weak observation metric is not enough for exponential equivalence of posterior kernels or controlled values.

One must prove, uniformly over the source/control class,

\[
\limsup_{\varepsilon\to0}a_\varepsilon^{-1}
\log P(d(Y_\varepsilon,Y_\varepsilon^{\rm sm})>\eta)=-\infty
\]

or an appropriate exponentially good approximation statement, and then show stability of the filter and risk-sensitive value under that approximation. No coupling between the atomic and smoothed observations is constructed. A “singularity shield” or coefficient lower bound does not imply superexponential smoothing error.

### 2.5. [MAJOR] The claimed compactness of chart subsets is not a consequence of Rellich alone

Rellich compactness in the observation variable can give compactness from `W^{s,1}_y` into a weaker `L^1_y` space on a bounded domain. Here the functions take values in a weighted hidden-state function space, the observation domain is not specified as bounded, and the `C^1_{W,x}` bound need not be compact in `L^1_W` over a noncompact state space. Uniform tail control in both `x` and `y`, a compact vector-valued embedding, and closure of the evidence lower bound are required.

The statement “bounded subsets are compact” is therefore false without additional localization and tightness hypotheses. This compactness is later used for measurable selection and uniform finite-coordinate approximation.

### 2.6. [FATAL] The zero-evidence/projective boundary is not a defined measurable state space

The paper says that when the unnormalized coefficient measure has zero mass, the state stores a “projective direction in the positive cone.” The zero measure has no projective direction. To create a blow-up at zero one must choose a topology and an equivalence class of approach directions; there is no canonical direction determined by a zero kernel.

The disjoint union `\mathcal Z` of regular charts and the blown-up singular boundary is not shown to be standard Borel or Polish. Overlapping charts may assign different representations to the same belief, and no transition maps or quotient relation are given. The proof of `thm:r17-c1-dpp` therefore cannot invoke a jointly measurable disintegration or measurable maximum theorem on this undefined space.

The claim that adjoining a projective direction “makes the update Borel also at zero evidence” is especially problematic: observations of zero predictive probability occur only on null sets under the current model, and choosing a posterior there is inherently nonunique. A Borel convention can be fixed, but it must be explicit and shown compatible with the control/DPP; projectivization does not solve this automatically.

### 2.7. [FATAL] The measurable-selection and DPP hypotheses are not verified

Theorem `thm:r17-c1-dpp` invokes compact relaxed controls, lower semicontinuity of the transition action, and the measurable maximum theorem. The manuscript does not define:

- the relaxed-control space and its topology;
- the admissible-control correspondence at each belief;
- the measurable graph of that correspondence;
- the one-step transition kernel on `\mathcal Z` as a function of control;
- continuity or semicontinuity of the risk-sensitive reward/cost;
- whether the same control must be used across latent/model components;
- integrability needed for the exponential criterion.

A universally measurable transition alone is not sufficient for a Feller selector theorem. Exact posterior DPPs for risk-sensitive partially observed control require careful timing and an augmented state containing all quantities on which future likelihoods depend. The proof is a generic verbal template, not a verification for the proposed kinetic experiments.

### 2.8. [MAJOR] The finite-coordinate value approximation requires invariance and stability not shown

Proposition `prop:r17-c1-finite` correctly observes that a compact metric set admits finite separating coordinates at a chosen tolerance. But the conclusion about controlled values requires more than reconstructing an individual belief:

1. the compact set `K` must be forward invariant, or all reachable beliefs over the horizon must lie in a common compact set;
2. transition kernels and rewards must be uniformly continuous uniformly in controls;
3. repeated reconstruction errors must be stable under the filter;
4. the risk-sensitive Bellman operator is not generally a contraction in the ordinary sup norm without normalization/discounting.

The proof says “backward induction and the contraction of the risk-sensitive Bellman operator,” but no contraction coefficient or horizon-dependent error estimate is given. The metric reconstruction lemma does not establish the control approximation theorem.

### 2.9. [FATAL] The QMD statement is not established uniformly for the triangular array

Theorem `thm:r17-c1-lan` concerns exact finite-volume densities `p_\vartheta^\varepsilon` and then takes local shifts of order `\mu_\varepsilon^{-1/2}`. QMD for each fixed `\varepsilon` as `h\to0` is not enough. One needs a **uniform triangular-array** expansion at `h/\sqrt{\mu_\varepsilon}`, including a remainder that is `o(1)` after summing the effective information scale.

The manuscript says that two `L^1` source derivatives and one dominated third derivative, together with lower/upper density bounds, give QMD. To justify the square-root Taylor expansion uniformly, one needs bounds on derivatives relative to the density and control of the region where the density is small. The claimed uniform positive lower bound is only on a regular observation window and cannot hold on the entire observation space for a normalized density on a noncompact domain.

It is also not shown that the parameter is finite-dimensional, identifiable, differentiable through the controlled dynamics, or that the score covariance scales as `\mu_\varepsilon I_\vartheta`.

### 2.10. [FATAL] QMD plus a score CLT does not automatically imply the claimed LAN

LAN requires the full log-likelihood-ratio expansion

\[
\log\frac{dP_{\vartheta+h/\sqrt{\mu_\varepsilon}}^\varepsilon}
{dP_\vartheta^\varepsilon}
=h^T\Delta_\varepsilon-	frac12h^TI_\vartheta h+o_{P_\vartheta}(1)
\]

uniformly on bounded `h`, together with contiguity. A central limit theorem for one score statistic and convergence of its covariance do not control the quadratic remainder of the exact likelihood. One needs local asymptotic quadraticity, a Lindeberg condition or differentiability-in-quadratic-mean theorem adapted to the triangular array, and uniform information convergence.

The references “A2 or B3 gives its Gaussian limit” are also insufficient: A2 is a local limit theorem for selected Sinai observables, while B3's process CLT is itself unproved. Neither is formulated as the score CLT of the exact experiment in this theorem.

### 2.11. [FATAL] The Bernstein–von Mises conclusion is essentially unproved

A prior with positive continuous density does not by itself yield Bernstein–von Mises. One additionally needs posterior concentration at the local rate, uniformly powerful tests or a suitable likelihood-ratio bound away from the local chart, control of nuisance/control parameters, nonsingular information, and a prior-thickness/tail argument.

The paper asserts “uniform tests follow from compact identifiability and the coefficient large-deviation bound,” but no tests are constructed and no uniform separation theorem is stated. Strategy-uniform BvM is even stronger: if the strategy is adaptive, the experiment and information can be random or policy dependent, and uniform LAN plus posterior concentration must hold over the strategy class. A one-sentence Laplace argument cannot establish this.

## 3. Dependency consequences

C1 depends on A2/B1/B2/B3/B4, all of which fail independent review. It also fails internally through the missing dominated chart, state-space, DPP, LAN, and BvM arguments. Its filter and statistical conclusions cannot be used by C2 or D1.

## 4. Minimum requirements for reconsideration

A future submission would need:

1. a fully specified hidden-state transition/observation model and exact belief update;
2. a chart with explicit common domination, evidence bounds, Sobolev norms, and model-specific verification;
3. a rigorous exponentially good approximation theorem for atomic observations;
4. a Polish/standard-Borel global belief state, including an explicit null-observation convention;
5. complete admissible-control, measurable-selection, and risk-sensitive DPP hypotheses;
6. a forward-invariant compact set and quantitative finite-coordinate value approximation;
7. uniform triangular-array QMD/LAQ and contiguity;
8. a separate posterior-concentration and testing proof for any BvM theorem, with the strategy class precisely delimited.

## 5. Recommendation

**Reject.** The manuscript correctly identifies why weak disintegration is insufficient, but does not construct the dominated alternative it needs. The statistical section then jumps from local density differentiability to LAN and Bernstein–von Mises without the required triangular-array and posterior arguments. The central results are not established.