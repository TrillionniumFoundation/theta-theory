# External top-four referee report on A2-DYN revision 43

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v43-referee-response-2026-10-08`, `revision/a2-dyn-v43-referee-copy-2026-10-08`  
**Reviewed commit:** `f3fb2858b2c10aa2f4f857d56132491a5ea25861`  
**Reviewed repository tree:** `94e973a4a4b13f213003869141d0e96cee51cc98`  
**Ordinary source payload tree:** `23929e85026d4b732f229941e2af22b47bd3853e`  
**Active manuscript directory:** `papers/A2-DYN-v43-referee-response`  
**Active mathematical source:** ninety-three numbered core modules; revision 43 adds modules 92--93  
**Frozen revision-42 author baseline:** `7e155f0fda2a7a5f77a061ed5b54cab5943fb24b`  
**Controlling external report:** `reviews/a2-dyn-v42-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `1d854ffbf468393c80e4f1bb744bfdadbb3e15a8` / `a41ef7c5d55ae4db201176892b286ba99ea84f31`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 43 is a real mathematical advance over revision 42. It does not merely relabel the guarded critical-packet result, and it does not infer a pointwise estimate from the small total mass of an omitted source. Instead, it returns to the complete finite-collision component at each exact label, extracts all one-sided constructible power--logarithm germs from that full component, allocates their localized mass against the exact component probability, and sums the resulting corrections over all actual collision labels. It then performs the discrete coefficient extraction before roof-frequency inversion and obtains a componentwise absolutely convergent inverse with a prescribed summed pointwise reconstruction error.

The revision also replaces the older unevaluated raw-closure interface by an exact smoothing identity whose central term is the already evaluated arithmetic transition kernel from revision 41. This is cleaner and more faithful to the actual exact-index arithmetic structure than an unmodulated Gaussian ansatz.

I audited the new modules

- `core/92_count_compatible_raw_correction.tex`;
- `core/93_complete_raw_inversion.tex`;

as well as their use in the abstract and article-level route, the response to the referee, proof ledger, specialist audit map, source manifest, publication status, validation record, and exact-source workflow evidence.

Within the scope of this audit, I found no decisive counterexample, sign error in the Fourier inversion, collision-label mismatch, missing section normalization, incorrect arithmetic residue replacement, or illegitimate interchange of the infinite label sum with the roof integral. The coefficient-first order is mathematically appropriate, and the manuscript is explicit that joint Fourier `L^1` integrability is neither assumed nor proved.

The negative recommendation is nevertheless forced by the central theorem that remains absent. The new exact decomposition is

```text
m^2 p_{n,R}(k,m,t)
 = L_{m,R}(k,t,n)
   + m^2 D_{B,n,R}(k,m,t)
   + o(1),
```

where `L_{m,R}` is the evaluated finite Gaussian transition kernel and

```text
D_{B,n,R} = p_{n,R} - K_B * p_{n,R}
```

is the full-source signed high-roof-frequency correction. Revision 43 does not prove

```text
m^2 D_{B,n,R} -> 0
```

on the central exact-index scale. It proves that this estimate is necessary and sufficient for the desired arithmetic pointwise local law and gives a finite integral certificate for it. That is a useful localization of the remaining task, but it is not the task's solution.

The adaptive component bandwidths likewise certify reconstruction, not asymptotics. They depend on the actual second-derivative budgets of the prepared residuals and can be arbitrarily large and discontinuous in the radius, label, and return count. No quantitative estimate connects those bandwidths to the fixed-band transfer-operator theory. The localized correction can have arbitrarily small total variation while retaining very large or divergent pointwise height near an integrable singularity. Consequently its mass estimate does not control the exact local-limit remainder.

The concrete section residues also remain nontrivial in the manuscript. At fixed radius the correct exact-index main term contains the arithmetic factor `mathfrak a_R`; uniformly through parameter transitions the correct main term is `mathcal L_{m,R}`. Revision 43 handles this correctly, but it does not prove the unmodulated singleton theorem for the concrete section.

At the requested benchmark, an article organized around raw local inversion must either prove the central-scale smallness of the complete signed correction, with the arithmetic main term retained, or present a broader conceptual theorem whose independent importance does not depend on that unfinished endpoint. Revision 43 does neither yet.

## 2. Frozen source, chronology, and qualification

Both reviewed author branches resolve to

`f3fb2858b2c10aa2f4f857d56132491a5ea25861`.

The repository tree is

`94e973a4a4b13f213003869141d0e96cee51cc98`.

The active manuscript is

`papers/A2-DYN-v43-referee-response`.

The ordinary source payload tree recorded by the source manifest is

`23929e85026d4b732f229941e2af22b47bd3853e`.

The branch chronology is correct. Revision 43 begins from the frozen revision-42 review commit and adds a new author manuscript tree. The two author branches point to the same final author SHA. The revision preserves all ninety-one inherited core modules and all one hundred seven inherited Python scripts byte-for-byte, while adding modules 92 and 93, revised front matter, provenance, validation records, and a new exact-source workflow.

The exact-source workflows completed successfully at the reviewed SHA:

- response branch run `37740172105`;
- referee-copy branch run `37740184792`.

The workflows establish exact source identity, inherited-file preservation, manifest consistency, normal/optimized finite-check agreement, native TeX compilation, stabilized references, and theorem-page rendering. They do not certify the constructible preparation argument, the complete finite-graph density theorem, the anisotropic spectral chain, the arithmetic transition theorem, or the remaining raw correction estimate.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v43-external-top4-review-2026-10-08/`.

No author source, prior report, workflow, or unrelated path is intentionally modified.

## 3. Scope of this review

I did not attempt to re-prove all ninety-three modules. The substantive audit concentrates on the new chain that could alter the revision-42 assessment:

1. the use of the complete exact-label finite graph rather than a guarded source;
2. the intrinsic one-sided power--logarithm germ expansion of a full component density;
3. localization of all terms of exponent at most one without changing their coefficients;
4. the zero-trace `W^{2,1}` residual after localization;
5. allocation of correction mass against exact component probabilities;
6. total-variation summability over all displacement and collision labels;
7. exact restriction compatibility under collision-count cutoffs;
8. exponential count moments and the complex frequency tube;
9. coefficient-first roof inversion;
10. the component Fourier `L^1` estimate;
11. adaptive bandwidth allocation and the summed essential-supremum certificate;
12. the long-return reconstruction ledger;
13. the fixed-band smoothing identity;
14. the evaluated arithmetic transition main term;
15. the necessary-and-sufficient full-source signed-remainder criterion;
16. the finite integral certificate for that remainder;
17. the exact boundary between reconstruction and a local-limit estimate.

The inherited results most directly used by this chain are the complete finite-count constructible density in module 40, the cumulative return tail, the revision-41 uniform transition theorem, the fixed-radius arithmetic interval theorem, and the covariance conversion between collision and return normalizations.

## 4. Summary of the new mathematical route

For fixed return index `n`, radius `R`, and exact discrete label

```text
ell = (k_1,k_2,m),
```

the full component density is denoted `f_ell`. Its reference mass is

```text
b_ell = P{(K_n,N_n)=(k,m)}.
```

A component with fixed collision count `m` is already complete when the finite collision graph is taken at cutoff `m`; increasing the cutoff cannot add trajectories with a different value of `N_n`. Revision 43 uses this elementary but important observation before choosing any singular localization.

For each nonzero component, the manuscript extracts every intrinsic one-sided term

```text
x^alpha (log x)^k,  -1 < alpha <= 1,
```

from every singular value of the whole component. The coefficients are unchanged. Only the support radii are shrunk so that the total variation assigned to the correction is at most a prescribed fraction of `b_ell`. The remainder then lies in `W^{2,1}` and has zero value and derivative traces at all extracted points.

Choosing the component budget `epsilon b_ell` gives

```text
mu^w = E^epsilon + Q^epsilon,
||E^epsilon||_TV <= epsilon,
||Q^epsilon||_TV <= ||w||_infty + epsilon.
```

The label series converge absolutely in total variation. The same component choices are used at every count cutoff, so the count-truncated corrections are literal restrictions of one common measure. Cumulative return tails yield exponential control of the count truncation and exponential count moments.

For each label, the `W^{2,1}` residual has an integrable roof transform. Instead of asserting that the full mixed transform is jointly integrable over all torus and roof frequencies, the proof first takes the torus coefficient, obtaining the exact component transform, and only then inverts the roof coordinate. This produces a valid pointwise reconstruction at each label.

Finally, a fixed smooth roof-frequency cutoff `chi(b/B)` defines a smoothing kernel `K_B`. The full signed correction is exactly

```text
D_B = p - K_B * p.
```

The revision-41 band-limited transition theorem evaluates `K_B*p`, so the raw pointwise theorem is reduced to smallness of `D_B` at scale `m^{-2}`.

## 5. Audit of the complete component construction

### 5.1 Fixing the count label before extraction

This is the conceptually strongest part of the revision.

For the event `N_n=m`, the cutoff `m` contains the complete physical graph relevant to that label. A larger cutoff changes neither the measure nor its density. By making this observation before selecting singular neighborhoods, the manuscript avoids the incompatibility that would arise if each global cutoff generated a fresh set of localized germs.

This justifies the projective identities

```text
E^{epsilon,L'} restricted to {m<=L} = E^{epsilon,L},
Q^{epsilon,L'} restricted to {m<=L} = Q^{epsilon,L}.
```

I found no count-label mismatch in this argument.

### 5.2 Intrinsic germ selection

The input from module 40 is that the real and imaginary parts of each compactly supported component density are constructible and analytic away from finitely many points. The one-variable preparation gives convergent Puiseux--logarithm expansions on one-sided intervals.

Revision 43 correctly distinguishes convergent expansions from merely formal asymptotics. It fixes a genuine interval of convergence before shrinking the localization radius. Equal roof values are combined before extraction, so no inverse separation factor appears when singular values coalesce.

Every exponent at most one is removed. Because the original density is integrable, all nonzero exponents exceed `-1`. After the finite jet is subtracted, the first remaining exponent is strictly greater than one. Two derivatives are therefore integrable, and the residual value and first derivative vanish at the extraction point.

Within the stated constructible framework, I found this logic coherent.

### 5.3 Arbitrarily small correction mass

The integral

```text
integral_0^d x^alpha |log x|^k dx
```

tends to zero for every `alpha>-1`. Consequently the support of a singular germ can be reduced until its `L^1` mass is as small as prescribed, without scaling its coefficient.

This is correct, but its interpretation is essential. The smallness comes from localization of support, not from small singular coefficients. It does not imply a small supremum, a small second-derivative norm, or a small high-frequency inverse.

The manuscript states this limitation accurately.

### 5.4 `W^{2,1}` residual and trace matching

The cutoff is chosen `C^2` with matching derivatives at its transition endpoints. Near each singular point it equals one, so the full low-order germ is removed. On the transition interval both the constructible density and the localized germ are smooth. The resulting residual has no jump in its value or first derivative; hence the second distributional derivative has no atom.

This supports the asserted `W^{2,1}` membership. It also makes the right-trace convention in the later pointwise inversion consistent.

### 5.5 Summation over labels

The allocation

```text
||e_ell||_1 <= epsilon b_ell
```

immediately gives absolute total-variation convergence because

```text
sum_ell b_ell = 1.
```

Likewise

```text
||q_ell||_1 <= (M+epsilon)b_ell.
```

The cumulative collision-count tail transfers directly to the correction and residual. This part of the proof does not hide word multiplicities or require uniform singular-value separation.

### 5.6 Exponential moments and holomorphic tube

The displacement and roof supports grow at most linearly with the collision count. Exponential count moments therefore dominate the component transforms in a nonempty complex tube. Polynomial factors produced by fixed-order frequency derivatives can be absorbed by choosing a slightly larger exponential moment below the cumulative-tail exponent.

The resulting domain can be chosen uniformly in the radius. The selected germ radii need not vary continuously in the radius for this conclusion, since only their mass and support bounds are used.

This is a valid output, but it is exponential control in the imaginary directions. It gives no decay as the real roof frequency tends to infinity.

## 6. Audit of coefficient-first inversion

### 6.1 Component Fourier norm

For a compactly supported `q_ell in W^{2,1}`, the manuscript uses

```text
|qhat_ell(b)| <= min(A_{0,ell}, A_{2,ell}|b|^{-2}).
```

Splitting at `sqrt(A_2/A_0)` gives

```text
integral |qhat_ell(b)| db <= 4 sqrt(A_{0,ell} A_{2,ell}).
```

The constant and the limiting zero-norm cases are correct. Absolute roof inversion therefore yields the continuous representative of `q_ell`.

### 6.2 Inversion order

The full residual transform has an absolutely convergent discrete-label expansion for each fixed roof frequency because the component `L^1` masses are summable. The proof takes the torus coefficient first and identifies it with `qhat_ell(b)`. Only then is the roof variable integrated, where the component Fourier norm is finite.

This avoids a false use of Fubini. Joint integrability on `T^3 x R` is not claimed. I regard this as an important correction to a common failure mode in raw local inversion arguments.

### 6.3 Adaptive component bandwidths

The tail estimate

```text
sup_t |q_ell(t)-q_ell^{Lambda}(t)|
 <= A_{2,ell}/(pi Lambda)
```

leads to

```text
Lambda_ell = max{1, A_{2,ell}/(pi delta b_ell)}.
```

The labelwise error is then at most `delta b_ell`, and summation gives the prescribed total essential-supremum error `delta`.

The proof handles null components separately. For a fixed finite set of labels, the maximum bandwidth can be used as a common band.

The statement is mathematically correct as an existence and reconstruction theorem.

### 6.4 Long-return reconstruction ledger

Choosing

```text
epsilon_n = delta_n = (1+n)^(-P-3)
```

gives a reconstruction error negligible after multiplication by `n^2`. The collision cutoff

```text
L_n = ceil(lambda n + (P+4)c_0^{-1} log(2+n))
```

contains every central collision label and makes the count-tail variation polynomially and exponentially negligible.

This closes the bookkeeping for exact reconstruction. It does not close the local-limit proof, because the required component bandwidths have no quantitative upper bound and the finite reconstructed high-frequency integral is not estimated.

## 7. Audit of the arithmetic smoothing identity

### 7.1 The fixed-band kernel

The kernel

```text
K_B(t) = (2pi)^(-1) integral e^{-ibt} chi(b/B) db
```

is real, even, integrable, and has total mass one. Positivity is not needed for the revision-41 complex band-limited test theorem.

The sign convention is consistent: convolution at target `t` is the exact test `K_B(T_n-t)`.

### 7.2 Extraction independence

Adding the explicit edge difference to the high-frequency inverse of the residual gives

```text
D_B = (e+q) - K_B*(e+q) = p-K_B*p.
```

Therefore `D_B` is independent of the chosen germ radii, the mass budget, and the particular complete extraction. This is an exact identity, not an asymptotic stability statement.

### 7.3 Evaluated central term

The revision-41 transition theorem applies to the fixed test `K_B` and gives

```text
m^2 (K_B*p)(k,m,t) = L_{m,R}(k,t,n) + o(1).
```

At fixed radius, `L_{m,R}` reduces on central compact sets to

```text
c mathfrak a_R(k,n,m) g_{Omega_R}(Z).
```

The manuscript correctly retains the arithmetic factor and does not replace a singleton by a finite packet.

### 7.4 Necessary and sufficient criterion

Combining the exact identity and the fixed-band expansion yields

```text
m^2 p = L_{m,R} + m^2 D_B + o(1).
```

Hence the pointwise arithmetic transition law holds if and only if `m^2 D_B` tends to zero uniformly on central sets. If this holds for one fixed band, it holds for every fixed band because two fixed-band smoothings have the same evaluated leading term.

This criterion is correct. It should, however, be described editorially as a precise reformulation of the missing estimate, not as a proof of that estimate.

### 7.5 Finite integral certificate

Truncating the component high-frequency inverse at the adaptive `Lambda_ell` changes the signed correction by at most `delta b_ell`, and the summed error is at most `delta`. This produces a finite integral whose smallness is equivalent up to a certified negligible tail.

Again, the finite integral is an exact physical quantity left to be estimated. No spectral estimate is evaluated at `Lambda_ell`.

## 8. The decisive unresolved estimate

The manuscript's raw endpoint requires

```text
sup m^2 esssup |D_{B,n,R}(k,m,t)| -> 0
```

on every central compact set.

Revision 43 does not provide any of the following:

- cancellation of the localized singular germs against the residual inverse;
- a uniform bound on the pointwise height of the complete correction;
- a summable bound for all component second-derivative norms;
- a polynomial or controlled exponential bound for `Lambda_ell`;
- a growing-band transfer-operator estimate reaching those bands;
- a direct oscillatory estimate for the finite full-source inverse;
- a classification proving that all central singularities lie outside the relevant target range;
- a theorem showing that the singular contribution itself is part of a non-Gaussian main term which should be retained.

The exact criterion therefore leaves the central analytic problem open.

## 9. Small mass is not pointwise smallness

The new correction can be made arbitrarily small in total variation because every integrable germ is supported on an arbitrarily short one-sided interval. This is useful for summability and count compatibility.

But a germ such as

```text
x^alpha,  -1<alpha<0,
```

has arbitrarily small `L^1` mass on a short interval and unbounded essential supremum there. Logarithmic germs and finite jumps similarly retain their intrinsic coefficient when localized.

Thus

```text
||E^epsilon||_TV <= epsilon
```

has no direct implication for

```text
m^2 esssup |E^epsilon|
```

or for the high-frequency signed correction. The manuscript acknowledges this. It is nevertheless the principal reason that the measure-level common correction does not complete the raw density theorem.

## 10. Intrinsic versus localized coefficient summability

Revision 43 proves absolute total-variation convergence of a series of **localized** complete-component germs. The support radii are chosen after the exact component is fixed and are allowed to shrink according to `epsilon b_ell`.

This is different from proving absolute summability of the intrinsic unlocalized coefficients or of the revision-42 exponential two-jet word series. A large coefficient can contribute very little total variation if it is supported on a sufficiently small interval.

The new theorem therefore establishes the existence of a common finite correction measure, not a canonical globally controlled pointwise correction profile. This distinction is correctly recorded in the manuscript and should remain explicit in any future statement.

## 11. Lack of quantitative parameter control

The correction mass estimates are uniform in the radius, but the selected singular points, germ partitions, localization radii, second-derivative norms, and adaptive bandwidths need not vary continuously or remain quantitatively bounded as `R` changes.

The extraction-independent identity `D_B=p-K_B*p` avoids a logical dependence on those choices. However, any proof using the finite certificate still requires uniform control of the actual component budgets. None is supplied.

A top-four uniform theorem would require one of two routes:

1. parameter-uniform preparation and derivative estimates strong enough to control the adaptive bands; or
2. a different dynamical/cancellation argument that estimates `D_B` directly and bypasses the prepared component constants.

Revision 43 presently provides neither.

## 12. Arithmetic residues remain part of the answer

The revision correctly accepts the conclusion of revisions 40--42: the exact-index fixed-radius interval law naturally carries

```text
mathfrak a_R(k,n,m),
```

and the radius-uniform transition statement is governed by

```text
mathcal L_{m,R}.
```

The concrete section phase masses are not proved uniform. Consequently an unmodulated Gaussian singleton theorem is not available without an additional zero-residue result.

The new raw criterion is stronger editorially because it is written with the correct arithmetic main term. This is progress. It also means that any final pointwise theorem must either retain the arithmetic factor and transition kernel or prove their nontrivial branches vanish.

## 13. Weighted insertions and conditional applications

Module 92 treats a bounded weight that is finite-record subanalytic at every finite cutoff. This includes the unweighted law and many finite Boolean endpoint events.

It does not automatically cover the full weighted insertion class appearing in the historical conditioning interface, especially arbitrary path-dependent or merely multiplier-bounded observables. The exact-event bridge and arithmetic phase posterior established earlier remain valid in their stated fixed-interval regimes, but the new raw correction theorem does not yet promote them to pointwise roof conditioning.

A complete raw-density program would need a parallel quantitative estimate for the weighted signed correction, not only an unweighted criterion.

## 14. Relation to the inherited residual theorem

The inherited theorem `thm:LLT` requires, among other things:

- an integrable residual transform with an `o(n^{-2})` complementary-frequency integral;
- a correction of total variation `o(n^{-2})`;
- pointwise central smallness of the correction density.

Revision 43 achieves a different and in some respects cleaner decomposition. It gives a common complete correction measure with arbitrarily small mass and a coefficient-first inverse even when the full mixed transform is not jointly integrable. It then identifies the exact signed smoothing correction that must vanish.

This does not verify the hypotheses of `thm:LLT`, nor does it replace them with a completed unconditional theorem. It replaces an overly global Fourier interface by a sharper remaining estimate.

## 15. Mathematical significance at the requested benchmark

The manuscript now contains several substantial completed results:

- the stationary physical singleton local law;
- compact-family extensions and nonelliptic examples;
- actual-return diffusive-window and arbitrarily slowly diverging-window laws;
- exact-index fixed-interval arithmetic local laws;
- radius-uniform arithmetic transition kernels;
- exact-event Gaussian return bridges;
- arithmetic endpoint posteriors;
- guarded regular critical packets;
- a count-compatible complete-component correction measure;
- coefficient-first pointwise reconstruction.

These results are nontrivial and potentially publishable after specialist verification.

At the four-journal benchmark, however, the current 286-page architecture remains dominated by an unproved endpoint. The newest two modules are mainly a representation and reduction theorem: they establish where the missing signed remainder lives and how it may be reconstructed, but they do not show it is asymptotically small.

The breadth required to compensate for that missing endpoint is also not yet demonstrated. The complete-component preparation is tied to this finite-horizon semialgebraic billiard graph, and the paper does not formulate a general theorem for broad singular hyperbolic systems with multiple independent applications.

## 16. Independent specialist verification

The following load-bearing claims require human expert audit:

1. the exact finite collision graph and constructible density for the actual moving section;
2. the use of the Cluckers--Miller integration and preparation results at singular and decision boundaries;
3. the claim that the complete one-variable density has the stated convergent one-sided Puiseux--logarithm germs;
4. intrinsic collection of all terms of exponent at most one;
5. zero-trace matching and the global `W^{2,1}` conclusion;
6. count-label exactness and cutoff compatibility;
7. cumulative-tail transfer to the correction and residual;
8. the coefficient-first extraction from the full transform;
9. the fixed-band transition theorem inherited from revision 41;
10. the full occupation-torus anisotropic inequalities and peripheral-spectrum classification;
11. the parameter-uniform resonance transition expansion;
12. the exact-event bridge moment estimates.

The successful workflows and finite tests do not resolve these continuum questions. The manuscript accurately says so.

## 17. Required work for a subsequent revision

A subsequent revision seeking the same benchmark should address the following in priority order.

### 17.1 Prove the signed correction estimate

Establish

```text
m^2 D_{B,n,R} -> 0
```

uniformly on central exact-index sets, with the arithmetic transition kernel as the main term.

This is the decisive item. Further reformulations without an estimate will not change the recommendation.

### 17.2 Control central singular contributions

For every singular and decision-boundary germ capable of entering a central target, prove one of:

- its coefficient is sufficiently small;
- its support misses the central region;
- its contribution cancels with another explicitly paired source;
- or it belongs to a non-Gaussian correction that must remain in the final theorem.

### 17.3 Close the adaptive-band ledger

Give quantitative bounds for

```text
A_{2,ell}/b_ell
```

on the relevant central labels, or replace the adaptive Fourier inversion by a direct oscillatory estimate. The present existence of `Lambda_ell` is not enough.

### 17.4 Supply a dynamical estimate beyond fixed bands

If the proof continues through Fourier truncation, establish a growing-band operator or cancellation theorem compatible with the actual required bandwidths. Fixed-band estimates cannot simply be evaluated at `Lambda_ell`.

### 17.5 Make the parameter-uniform mechanism explicit

Either construct uniform preparation neighborhoods and derivative budgets through radius changes, or prove the extraction-independent correction estimate directly without selecting parameter-continuous germs.

### 17.6 Resolve the arithmetic statement

State the final theorem with `mathfrak a_R` and `mathcal L_{m,R}`, unless a separate proof establishes that all concrete nontrivial section residues vanish.

### 17.7 Treat weighted sources

Extend the signed-correction estimate to the weighted endpoint/path class needed for the conditioning theorem. A pointwise unweighted LLT alone does not automatically give every weighted denominator and numerator.

### 17.8 Obtain independent expert review

At minimum, separate experts should audit:

- singular billiard geometry and finite graphs;
- anisotropic transfer operators;
- constructible preparation and coarea regularity;
- arithmetic resonance and stationary phase;
- conditional bridge tightness.

### 17.9 Reduce the central route

The article should distinguish completed principal theorems from the historical derivation archive. A top-four submission should not require the reader to navigate ninety-three core modules to determine which endpoint remains conditional.

## 18. Technical comments

1. Keep `B_m,C_m` reserved for collision derivative entries and use a distinct notation for roof-frequency bands.
2. State explicitly that the component bandwidth formula applies only when `b_ell>0`; null components are zero.
3. Retain the right-trace convention at finite jumps and avoid assigning finite values to divergent germs.
4. Do not describe `||E^epsilon||_TV<=epsilon` as a pointwise error estimate.
5. Do not describe absolute total-variation convergence of localized germs as absolute summability of intrinsic coefficients.
6. Keep the dependence of `A_{2,ell}` and `Lambda_ell` on `n,R,ell,w` visible.
7. The fixed-band transition theorem must always be applied with `B` fixed before the collision count tends to infinity.
8. The finite remainder certificate is a truncation certificate, not a proof that the finite inverse is small.
9. Preserve the distinction between the collision count `m` and return index `n` in every supremum.
10. Keep the exact normalization of `K_B` and the sign `K_B(T_n-t)` visible.
11. The statement that one-band smallness implies every-band smallness relies on the common transition main term; cite that step whenever reused.
12. Do not infer parameter continuity of germ radii from uniform mass estimates.
13. The complex tube controls imaginary-frequency growth, not real-frequency decay.
14. The phase factor must remain in the fixed-radius pointwise candidate main term unless the zero-residue criterion is verified.
15. A finite packet average does not identify a prescribed singleton.
16. The exact-event bridge remains conditioned on a fixed positive roof interval, not on a density value.
17. Weighted raw inversion requires its own correction estimate.
18. Source qualification and finite models should remain separated from proof certification.

## 19. Overall assessment

Revision 43 is a serious and constructive response to the revision-42 report.

It removes the guarded-source omission at the level of exact reconstruction. It builds one count-compatible correction from the complete component densities, includes singular and decision-boundary germs, proves absolute total-variation convergence and exact cutoff compatibility, obtains exponential count moments, and gives a valid coefficient-first pointwise inverse. It also writes the raw endpoint with the correct arithmetic transition kernel and isolates one extraction-independent signed correction.

I found no decisive error in the two new modules within the scope of this review.

The paper nevertheless remains short of the theorem governing its title and central architecture. The newly isolated signed correction is not shown small at the local scale; the adaptive bands have no usable long-time bounds; small correction mass does not control pointwise singular height; the concrete arithmetic residues are not proved trivial; and the weighted pointwise theory remains open.

Subject to independent specialist verification, the completed stationary, interval, arithmetic, bridge, posterior, and reconstruction results could support a strong focused paper. They do not yet constitute a complete top-four raw local inversion theorem.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
