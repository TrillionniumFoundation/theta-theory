# Independent Referee Report — Round 14

**Manuscript:** B1 — *Microcanonical Preparation*  
**Reviewed branch:** `revision/round14-referee-positive-closure-11paper-2026-09-01`  
**Reviewed commit:** `dd9dbcb891076b7dbfe388bd8543d8342ba103c0`  
**Reviewed tree:** `c4492f8891e065201af70e68e6764ff5975f2137`  
**Controlling module:** `ROUND14_POSITIVE_CLOSURE.tex`  
**Registered module SHA-256:** `00de3561fed8db80b2c2ea73b6c1470ad556e8ccba744ea82ac239fa5840ce02`  
**Editorial standard:** *Annals of Mathematics*, *Acta Mathematica*, *Inventiones Mathematicae*, or *JAMS*  
**Recommendation:** **Reject**

## Executive assessment

Round 14 adopts the correct high-level order: extract exact particle number before Fourier inversion in the continuous constraints, and use separate source-dependent saddles in numerator and denominator. This removes the old grand-canonical empty-sector contradiction at the conceptual level.

The replacement coefficient theorem is not proved and is internally inconsistent. Its stated high-frequency bound contains a frequency-independent term on an infinite domain, so its claimed integral is infinite; the proof silently substitutes a stronger estimate not stated in the theorem. The “many regular components” lemma also treats a signed connected-polymer expansion as a positive probability measure and applies Chernoff's inequality without constructing such a measure. The shell scaling is inconsistent as written.

## Decisive objections

### 1. The high-frequency theorem contradicts its own integral conclusion

The theorem states, for `|u|>R`,

\[
|\varphi_{\varepsilon,N,H}(u)|
\le e^{-cN}+C_s(1+|u|)^{-s-c_0N}.
\]

The first term is independent of `u`. Therefore

\[
\int_{|u|>R} e^{-cN}\,du=\infty.
\]

It is impossible to conclude

\[
\int_{|u|>R}|\varphi_{\varepsilon,N,H}(u)|\,du
=o(N^{-d/2}).
\]

The proof notices the problem and says that the “actual bound” is

\[
C_s\left[e^{-cN}(1+|u|)^{-s}
 +(1+|u|)^{-s-c_0N}\right].
\]

That is a different theorem. A proof cannot repair a false displayed statement by replacing it in prose. The shell coefficient explicitly invokes the theorem as stated.

### 2. No positive polymer probability measure is constructed

The connected hard-core/trajectory polymer activities are generally signed, and on complex source charts they are complex. The lemma compares the total absolute weight of partitions with few regular components to “the total positive coefficient,” marks selected polymers by an auxiliary variable, differentiates a logarithm, and applies Chernoff's inequality.

This reasoning would be valid for a positive Gibbs measure on polymer partitions. The manuscript never constructs one. In a Mayer or connected-cluster expansion, the partition representation contains cancellations; the derivative of the logarithm of the final positive coefficient is not automatically the expectation of the number of marked connected components under a positive law.

The problem is especially visible for hard-core two-particle connected activities, whose basic Mayer factor has negative sign. The claim that singleton and collision-polymer activities are uniformly positive is not justified.

### 3. The “many regular components” conclusion does not follow from pressure analyticity

Even if a positive marked partition law existed, a lower bound on

\[
\partial_{\log v}p_N(1)
\]

only controls the mean marked count. An exponential lower-tail estimate uniform in `N`, source, and the exact-number coefficient requires a uniform logarithmic moment-generating bound in a real interval and convexity estimates. “The same polymer norm” does not supply the necessary positivity or coefficient-uniform constants.

### 4. Coarea on a positive patch does not give a globally smooth component law

The proof selects a compact submersion patch and concludes that the summed mark of a regular polymer type has a `C-infinity` density with rapidly decaying characteristic function. A local submersion gives a smooth absolutely continuous component. The complement of the patch can retain singular or critical-value mass unless the polymer type is explicitly restricted to the patch by a smooth positive partition and the remainder is separately controlled.

The Fourier factor used later is the characteristic function of the entire conditional component, not merely one smooth subcomponent. This gap repeats the smoothing error from earlier rounds in a coefficient-level form.

### 5. The exceptional coefficient class is not shown to contain a regular component

To fix the frequency-independent `e^{-cN}` term, the proof says that every exceptional partition still has one fixed regular component and hence obtains `(1+|u|)^{-s}` decay. That property is not part of Lemma `r14-b1-components`, which only says that the exceptional partitions contain fewer than `c_0N` regular components. “Fewer” includes zero.

Thus even the stronger prose bound is unsupported by the lemma on which it relies.

### 6. The complex activity saddle is only local and cannot support the global Fourier theorem

The coefficient saddle `z_{epsilon,H,u}` is proved only on a common complex neighborhood of `u=0`. The high-frequency theorem ranges over all `u in R^d`. Outside the local chart, no unique analytic activity saddle is defined, no contour deformation is justified, and no coefficient pressure is shown analytic.

The tail proof switches to a combinatorial partition argument, but its normalization and comparison with `Z_{N}(0;H)` still require coefficient estimates uniform in large `u`. Those estimates are not established.

### 7. The regular-shell scaling is inconsistent

The event in the shell theorem is

\[
\sqrt{\mu_\varepsilon}(C-a)\in\mathcal W_\varepsilon,
\]

and `g_epsilon` is the Gaussian mass of `W_epsilon` in these central-limit coordinates. The text then says that centered boxes with

\[
\delta_\varepsilon\downarrow0,
\qquad
\sqrt{\mu_\varepsilon}\delta_\varepsilon\to\infty
\]

are included and have `g_epsilon -> 1`.

If `delta_epsilon` is the half-width of `W_epsilon` in the displayed CLT coordinates, then `W_epsilon` shrinks and its Gaussian mass tends to zero, not one. If `delta_epsilon` is an unscaled physical shell width, then `W_epsilon` should be defined as the expanding box of half-width `sqrt(mu) delta_epsilon`. The theorem conflates the two coordinate systems.

### 8. The shell class is partly defined by the desired Fourier conclusion

A shell is called regular when smooth approximations have Fourier error

\[
r_\varepsilon=o(g_\varepsilon\mu_\varepsilon^{-d/2}).
\]

This is not a geometric shell hypothesis unless `r_epsilon` is independently defined and estimated. As written, the class incorporates the error scale that the theorem is meant to prove, making the result partly tautological.

### 9. Uniform covariance and the global mean map inherit the unproved component lemma

The lower Hessian bound, properness, and degree-one mean-map statement are all derived from the assertion that the exact-number coefficient contains linearly many full-rank positive components. Since that assertion has not been proved on a positive coefficient law, the finite saddle theorem and the Schur-complement covariance are not established.

### 10. The dependency on B2 is not a closed input

The coefficient expansion begins by importing B2's all-contact Kotecký–Preiss estimate and complex trajectory-polymer remainder. Round 14 B2 does not prove that theorem or its lower-recovery interface. B1 therefore cannot serve as the microcanonical bridge even if its own coefficient arguments were repaired.

## Correct direction

The number-first strategy should be retained, but a valid proof must:

1. construct a genuine positive canonical decomposition or avoid probabilistic statements about signed polymer partitions;
2. prove a global integrable characteristic bound with no unstated replacement;
3. isolate smooth mark blocks by an explicit positive partition of unity;
4. keep physical and CLT shell coordinates distinct; and
5. derive the shell error from checkable geometric hypotheses.

## Recommendation

**Reject.** The conceptual order is improved, but the principal Fourier theorem is false as displayed, and the positive-probability argument underlying all coefficient and covariance estimates does not exist.