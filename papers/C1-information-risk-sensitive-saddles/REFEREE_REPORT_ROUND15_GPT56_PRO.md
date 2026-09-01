# Independent Referee Report — Round 15

**Manuscript:** C1 — *Information and Risk-Sensitive Saddles*  
**Submitted revision branch:** `revision/round15-referee-positive-closure-11paper-2026-09-01`  
**Locked branch commit:** `e25e565cc15ae65693c87eda37fd3a1f29357ecd`  
**Locked tree:** `d3c54fc19f0881ce3d38253f62ca3215fbf5000c`  
**Actual controlling module at review lock:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Recoverable registered Round-Fifteen candidate:** `C1_POSITIVE_SLICE_FILTER_GROWING_STATE.tex` from the truncated checksum-pinned payload  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *Journal of the AMS*  
**Recommendation:** **Reject**

## Evidence boundary

The controlling manuscript is still Round Fourteen. The complete C1 Round-Fifteen candidate was recoverable from the truncated payload and is reviewed as supplemental material. It is not part of the built paper.

## Executive assessment

The candidate repairs the missing observation-density factor in the transition kernel, keeps positive posterior measures separate from oriented currents, and abandons fixed finite-moment sufficiency. Those changes are correct. The key Feller theorem is nevertheless false under its stated topology: disintegration is not continuous under weak convergence of joint laws. The proof assumes exactly the integrated posterior-Lipschitz estimate it must derive, and the inserted local coefficient theorem cannot supply it for the full belief class.

## Decisive objection: posterior disintegration is not weakly continuous

Let \(Y\) be uniform on \([0,1]\). Define

\[
X_n(y)=1_{\{\sin(2\pi n y)>0\}}
\]

and let \(J_n\) be the joint law of \((X_n,Y)\). The rapidly oscillating graphs converge weakly to the product law

\[
J=\operatorname{Bernoulli}(1/2)\otimes\operatorname{Leb}.
\]

For every \(n\), however, the posterior of \(X_n\) given \(Y=y\) is a Dirac measure:

\[
\pi_{n,y}=\delta_{X_n(y)}.
\]

Hence the law of the posterior random measure converges to

\[
\tfrac12\delta_{\delta_0}+\tfrac12\delta_{\delta_1}.
\]

For the weak limit \(J\), the posterior is constant:

\[
\pi_y=\tfrac12(\delta_0+\delta_1),
\]

so its posterior-law is

\[
\delta_{\frac12(\delta_0+\delta_1)}.
\]

These two limits are different. Thus the map

\[
J\longmapsto \text{law of the conditional measure }J(dx\mid y)
\]

is not continuous for weak convergence, even on compact spaces with perfectly positive probability kernels. A Lyapunov moment bound does not cure the problem.

### 2. The manuscript assumes the missing stability estimate

The Feller theorem requires an integrated bound comparing posterior kernels:

\[
\int W_1(\pi_y,\tilde\pi_y)\,\lambda(dy)
\le C\,d_{\rm BL}(\bar\Lambda,\bar{\tilde\Lambda}).
\]

This is a strong filter-stability/dominated-density assumption, not a consequence of the coupling argument given. A coupling of two joint laws does not pair their regular conditional probabilities at the same observation value with such a bound.

The proof simply invokes the assumption, so the theorem does not derive Feller continuity for the hard-sphere or Sinai models.

### 3. The inserted local coefficient is far too local to close the gap

The coefficient theorem concerns a compact regular source/observation chart, finite history cylinders, and positive shell denominators. It does not control:

- arbitrary beliefs in the Lyapunov sublevel;
- singular or nearly singular observation laws;
- rapidly oscillating conditional densities;
- zero-evidence boundary directions; or
- iterative growth of the filter Lipschitz constant.

Therefore it cannot justify the global Feller hypothesis subsequently used for the DPP and finite-coordinate reduction.

### 4. The iterated current-slice construction is not fully typed

The text states that repeated coarea/Rokhlin slices form “positive normal currents.” Geometric slicing of oriented currents can be signed and dimension-dependent. Positivity belongs to coefficient measures, not automatically to the oriented current component. The product state and push-forward maps require a precise category of measures/currents and compatibility across codimension changes.

### 5. The finite-coordinate construction assumes an unjustified enumeration property

The candidate takes the first \(K\) bounded Lipschitz tests of a dense sequence and chooses \(K(\varepsilon)\) so that they resolve a \(2^{-K}\)-net. Density of the whole sequence does not imply that the **first** \(K\) tests have this property at a stated rate. One must choose a finite determining family depending on the tolerance, then construct a measurable reconstruction and prove the induced transition is stable.

### 6. The BvM theorem assumes all hard inputs

Uniform LAN, global identifiability, posterior testing, positive information, and a uniform inserted coefficient over adaptive strategies are the theorem-specific work. They are placed among the hypotheses or imported from B1/B3, whose underlying coefficient and Gaussian theorems remain open. The final result is therefore conditional, not a proved hard-sphere statistical theorem.

### 7. Zero-evidence compactification does not repair positive-evidence instability

Keeping a projective direction at zero mass can make the boundary topologically honest. It does not address discontinuity of normalized posteriors when evidence is small but positive, nor does it make the disintegration map continuous along oscillatory regular sequences.

## Required reconstruction

Restrict the observation model to a dominated class with densities bounded above and below and prove an integrated filter-stability theorem in a topology strong enough to control disintegration. Define finite determining coordinates adaptively for each tolerance. Keep zero-evidence and singular observation strata outside the regular Feller chart unless separately proved.

## Recommendation

**Reject.** The candidate fixes the normalization of the observation kernel but its main continuity theorem is contradicted by elementary oscillatory disintegrations.
