# External top-four referee report on A2-DYN revision 46

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v46-referee-response-2026-10-08`, `revision/a2-dyn-v46-referee-copy-2026-10-08`  
**Reviewed commit:** `fb16f06fb2bd205322d4a15979aef5a9a83d4970`  
**Reviewed repository tree:** `4169e573ae17131e3e85ae99500b1448331225e7`  
**Ordinary source payload tree:** `300154d700b4884795f45dd3eea5010230fa1e67`  
**Active manuscript directory:** `papers/A2-DYN-v46-referee-response`  
**Active mathematical source:** ninety-nine numbered core modules; revision 46 adds modules 98--99  
**Frozen revision-45 author baseline:** `5ab781065787b1aca00ff5182a62da49f847d2e4`  
**Controlling external report:** `reviews/a2-dyn-v45-external-top4-review-2026-10-08/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `0ada8feead815b267b530a92ed4e14f5445867f2` / `d9169afd510d4acb97bf79da6d811c2af0a04f9a`  
**Date:** 8 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 46 is a genuine mathematical advance over revision 45. It addresses, rather than merely reformulates, the largest unresolved part of the preceding report inside the smoothly protected source.

The new work extends the endpoint-continuation and relative-distortion mechanism from normal-to-normal critical words to arbitrary protected regular histories. It constructs an explicit graded source guard whose weak endpoint derivative is independent of the collision-word length. On the high-gradient part of that guarded source, the flow of

```text
grad F / |grad F|^2
```

translates the roof exactly while preserving the original displacement, collision count, return index, center word, and all section decisions. The resulting positive flow box compares a roof-level density with a fixed positive roof-window probability at the same exact integer labels. Combining this comparison with the already proved arithmetic fixed-window theorem produces an actual `W^{1,infinity}` density estimate and a common-band approximate-identity bound for the noncritical signed inverse.

The revision then completes every protected small-gradient source point to an actual protected normal-to-normal critical center and invokes the revision-45 critical-cluster estimate. This yields control of the entire smoothly protected correction, not only its shrinking critical collars. For each fixed protection parameter, the paper obtains

```text
limsup_m sup m^2 ||D_B^epsilon||_infinity <= C B^(-1/2)
```

whenever `B >= C epsilon^(-12)`, and it separately proves convergence for every diverging bandwidth sequence with the protection parameter fixed.

Finally, the paper proves that the complementary original source has total mass `O(epsilon)`, uniformly in the collision count, and gives an exact full-source reduction: the remaining pointwise arithmetic obstruction is the signed correction of the positive collapsing-margin source.

I audited the new modules

- `core/98_noncritical_window_transport.tex`;
- `core/99_protected_raw_reduction.tex`;

as well as their front-matter formulation, response to the preceding report, proof ledger, specialist audit map, source manifest, publication status, validation protocol, and exact-source workflow evidence.

Within the scope of this audit, I found no decisive counterexample, collision/return-label mismatch, missing section-normalization factor, Fourier-sign error, illicit substitution of a growing band into a fixed-band spectral theorem, or incorrect replacement of the arithmetic transition kernel by an unmodulated Gaussian.

The exponent ledger is internally consistent. The endpoint collar has radius `O(epsilon^3)`. The roof-translation width is `O(epsilon^3 delta^2)`. The regular derivative budget contributes

```text
B^(-1) [L delta^(-1)
         + M epsilon^(-3) delta^(-1)
         + M delta^(-2)],
```

while the near-critical contribution is `O(M delta^2)`. Choosing `delta=B^(-1/4)` produces `O((M+L)B^(-1/2))`, provided `B >= C epsilon^(-12)`. This is the correct condition for the term `epsilon^(-3)B^(-3/4)` to be absorbed by `B^(-1/2)` and for the critical-completion restriction `delta < c epsilon^3` to hold.

The negative recommendation is nevertheless unavoidable. The manuscript still does not prove the estimate that closes its advertised raw pointwise theorem. With the ordered protection scale

```text
epsilon(B)=A B^(-1/12),
```

the full law is reduced to the signed correction

```text
b^epsilon - K_B * b^epsilon
```

of a positive source whose incidence, clearance, or section-decision margins collapse. The manuscript proves only

```text
sum_{n,k} ||b^epsilon_{n,k,m,R}||_1 <= C epsilon.
```

It does not prove

```text
lim_{B->infinity} limsup_{m->infinity}
  sup m^2 esssup |b^epsilon - K_B*b^epsilon| = 0.
```

This remaining source includes precisely the near-grazing, competing-hit, and section-decision histories where pointwise concentration is most plausible. Small total mass, the inherited exponential fixed-count height bound, and the qualitative count-dependent diagonal do not imply the required central-scale pointwise estimate.

Thus revision 46 closes the protected noncritical inverse and localizes the unresolved term much more sharply, but it does not close the full arithmetic raw-density theorem.

The concrete section residues also remain part of the answer. At fixed radius the candidate singleton main term still carries `mathfrak a_R`; through radius-dependent arithmetic transitions the correct uniform main term remains `mathcal L_{m,R}`. The manuscript treats this correctly, but no unmodulated radius-uniform exact-index theorem is proved.

At the requested venue level, a paper organized around raw local inversion must either prove the remaining collapsing-margin correction estimate, with the arithmetic main term retained, or present a broader conceptual theorem whose independent importance does not depend on this unfinished endpoint. Revision 46 does neither yet, although it is a substantial advance toward the first alternative.

## 2. Frozen source, chronology, and qualification

Both reviewed author branches resolve to

`fb16f06fb2bd205322d4a15979aef5a9a83d4970`.

The repository tree at that commit is

`4169e573ae17131e3e85ae99500b1448331225e7`.

The active manuscript is

`papers/A2-DYN-v46-referee-response`.

The ordinary source payload tree recorded in the source manifest is

`300154d700b4884795f45dd3eea5010230fa1e67`.

The branch chronology is correct. Revision 46 begins from the frozen revision-45 external-review commit and adds a new author manuscript tree. The two author branches point to the same final author SHA. The revision preserves all ninety-seven inherited core modules and all one hundred nineteen inherited Python scripts byte-for-byte while adding modules 98 and 99, revised front matter, proof maps, provenance, diagnostics, and a new exact-source workflow. The bibliography, inherited mathematical labels, and compiled A--X synopsis are retained.

The exact-source workflows completed successfully at the reviewed SHA:

- response branch run `37778372692`;
- referee-copy branch run `37778409609`.

These workflows establish source identity, inherited-file preservation, manifest consistency, normal/optimized finite-check agreement, native TeX compilation, stabilized references, and theorem-page rendering. They do not certify the arbitrary-endpoint continuation, graded guard, flow-box Jacobian, distributional derivative, near-critical completion, clearance transversality, inherited anisotropic spectrum, or the missing collapsing-margin pointwise estimate.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v46-external-top4-review-2026-10-08/`.

No author manuscript source, prior report, workflow, or unrelated repository path is intentionally modified.

## 3. Scope of this review

I did not attempt to re-prove all ninety-nine modules. The substantive audit concentrates on the new chain that could alter the revision-45 assessment:

1. extension of endpoint continuation from critical words to arbitrary protected regular histories;
2. lower and upper reduced-action Hessian bounds at nonnormal endpoints;
3. logarithmic source-density distortion with possibly small endpoint incidences;
4. the explicit graded source guard;
5. its word-length-independent weak endpoint derivative;
6. its zero extension at physical and section-decision boundaries;
7. the fixed-window budget obtained from the arithmetic transition theorem;
8. exact roof translation by `grad F/|grad F|^2`;
9. preservation of all exact labels and section decisions under that flow;
10. weighted flow Jacobian and flow-box injectivity;
11. conversion of positive window mass to pointwise density control;
12. distributional integration by parts and absence of boundary measures;
13. the `W^{1,infinity}` noncritical derivative estimate;
14. the common-band approximate-identity estimate;
15. completion of small-gradient protected points to actual critical centers;
16. combination with protected critical-cluster deconcentration;
17. the `B^(-1/2)` protected-correction modulus;
18. the arbitrary diverging-band statement at fixed protection;
19. the one-flight near-boundary estimates;
20. uniform `O(epsilon)` exhaustion in original source mass;
21. the ordered protection-bandwidth scale;
22. the exact arithmetic boundary-reduction criterion;
23. the qualitative count-dependent protection diagonal;
24. the precise distinction between mass exhaustion and pointwise closure.

The inherited load-bearing inputs include the physical contact second variation, endpoint injectivity, cross-Hessian source-density formula, revision-45 critical collars and cluster deconcentration, the full occupation-torus fixed-band spectrum, the physical peripheral projection formula, the uniform arithmetic transition kernel, and the complete fixed-count source density.

## 4. Overview of the new reduction

For an exact label

```text
(K_{n,R},N_{n,R})=(k,m),
```

the revision introduces a smooth graded guard `Xi_m,R^epsilon`. It is one when every incidence, section-decision distance, and nonincident-flight clearance exceeds twice its graded threshold and vanishes outside the corresponding once-thresholded protected set.

The full density is split exactly as

```text
p = f^epsilon + b^epsilon,
```

where `f^epsilon` is the original source multiplied by the guard and `b^epsilon` is the positive complementary source. No renormalization is performed and no integer label is changed.

The protected density is divided by a smooth gradient cutoff into:

- a high-gradient part, controlled by roof translation and a first-derivative estimate;
- a low-gradient part, completed to actual protected critical centers and controlled by positive critical collars.

The protected correction is therefore estimated without summing wordwise `W^{2,1}` norms and without selecting a component-dependent spectral bandwidth.

The complement has uniformly small total mass as `epsilon` tends to zero. The paper then chooses `epsilon(B)=A B^(-1/12)` and reduces the full raw theorem to a single signed correction of that complement.

This is a materially sharper reduction than the revision-45 decomposition.

## 5. Endpoint continuation at arbitrary protected regular histories

The extension from normal endpoints to arbitrary regular endpoints is plausible and important.

The internal contact matrix and its off-diagonal decay do not depend on endpoint normality. In an endpoint derivative, one internal incidence factor cancels against the endpoint--internal Hessian entry. The endpoint factors that remain are bounded above by one. Thus the geometric-decay estimate for internal contact response survives.

For an `epsilon`-protected history, the same continuation argument gives an endpoint square of radius proportional to `epsilon^3`, independent of the word length. All incidence, clearance, and section-decision margins remain at least half their initial lower bounds, and the exact return decisions remain unchanged.

The reduced action satisfies

```text
grad F = (-p_0,p_m).
```

The Schur-complement second variation remains positive. Its upper bound is controlled by the endpoint principal block of the full contact Hessian, and the lower bound depends only on the endpoint incidences. Since the protection threshold at each endpoint is of order `epsilon`, the stated lower bound of order `epsilon` is consistent.

The physical source density in endpoint coordinates retains the factor

```text
(4 pi R c)^(-1),
```

with `c=nu(Y_R^*)`. At arbitrary endpoints the logarithmic derivatives of the two endpoint cosine factors cost at most `O(epsilon^(-2))`; the internal potential remains the larger `O(epsilon^(-3))` contribution. Thus

```text
|grad log w| <= C epsilon^(-3)
```

is consistent with the preceding critical calculation.

I found no normalization contradiction in this extension.

The argument nevertheless remains load-bearing. A specialist should verify the endpoint-coordinate conventions, the Schur upper bound, the cross-determinant formula away from normality, and the claim that the continuation glues globally over the stated endpoint square without an unnoticed multiplicity.

## 6. The graded guard

The guard is the product of three kinds of factors along the physical history:

1. incidence factors;
2. distances from section-decision boundaries;
3. nonincident-flight clearances.

Their thresholds decay geometrically with distance from the two endpoints. When one factor is differentiated in its transition region, the protected margins supplied by all nonzero factors and the endpoint-response estimate give a derivative of size

```text
C epsilon^(-2) q^(d/2).
```

There are at most two contacts at each endpoint distance `d`, so the sum over all differentiated factors is geometric. This yields

```text
|grad Xi_m,R^epsilon| <= C epsilon^(-2)
```

with no factor depending on `m`.

This is the correct mechanism for avoiding an exponential or linear word-length loss.

The proof uses weak derivatives of distance and minimum-clearance functions. This is acceptable in principle, but the following details require direct audit:

- the collision-cylinder distance near rectangle corners;
- the medial axes where the identity of the closest nonincident disk changes;
- the endpoint-coordinate derivative of the full collision state;
- the claim that no extra inverse-incidence factor occurs in the section-distance or clearance derivative;
- the zero extension near every genuine physical-word and section-decision boundary.

I did not identify a decisive failure in the stated Lipschitz argument, but these points should not be treated as routine bookkeeping.

## 7. The fixed-window budget

The paper defines

```text
Q_m(h) = m^2/(2h) sup P{|T_n-t|<h,
                        K_n=k, N_n=m}.
```

For each fixed `h>0`, the revision-41 uniform transition theorem and boundedness of its finite Gaussian peak sum imply

```text
limsup_m Q_m(h) <= C_0.
```

The constant in the limiting upper bound can be chosen independently of the fixed value of `h`; the convergence threshold may depend on `h`. This is exactly the level of uniformity used later.

The manuscript does not insert a shrinking window into that theorem. Every use fixes `h` before sending `m` to infinity. This respects the required quantifier order.

The upper bound sums all arithmetic branches and does not require a positive denominator. It is therefore appropriate for the later density estimate.

## 8. Positive roof-flow comparison

On the high-gradient source the vector field

```text
V = grad F / |grad F|^2
```

satisfies `VF=1`. Its flow therefore changes the physical roof by exactly the flow time.

For

```text
h = c_1 epsilon^3 delta^2,
```

the endpoint displacement is of order `epsilon^3 delta`, which stays inside the protected endpoint square. The Hessian bound keeps the roof gradient above `delta/2`. Hence the center itinerary, all section decisions, displacement, collision count, and return index are preserved.

The weighted divergence obeys

```text
|div_w V| <= C(delta^(-2)
                + epsilon^(-3)delta^(-1)).
```

Multiplication by the flow time gives `O(epsilon^3+delta)`, so the physical Jacobian ratio can be bounded between two fixed positive constants.

The map from a regular roof level times the flow interval is injective: the roof value identifies the flow time and uniqueness of the flow identifies the initial level point. Different physical words remain disjoint because the continuation stays inside the corresponding physical domains.

Coarea then converts the positive window mass to a pointwise level-density upper bound without a word-count factor.

This is the conceptual heart of revision 46. It is a genuine dynamical estimate rather than another Fourier reconstruction certificate.

The proof should nevertheless receive specialist scrutiny at the following points:

- global existence of the flow for the full stated interval;
- the first-exit argument simultaneously preserving the gradient and every graded margin;
- injectivity at chart seams and across the collection of endpoint charts;
- the exact weighted coarea Jacobian;
- disjointness of the flowed word domains;
- the use of almost-everywhere levels when the final norm is an essential supremum.

Within the written argument I found no immediate contradiction.

## 9. Distributional density derivative

The guarded high-gradient source is

```text
a Xi_m,R^epsilon H_delta nu_R^*.
```

The insertion is required to have a supremum bound and a weak endpoint-gradient bound on protected endpoint charts. The guard vanishes near physical and section-decision boundaries, while the gradient cutoff vanishes near critical points.

The integration-by-parts identity

```text
int g psi'
 = - sum_words int div(a Xi H_delta w V) psi(F)
```

therefore has no physical-domain boundary term. The density of the derivative measure is dominated by the pushforward of the same positive protected source multiplied by

```text
L delta^(-1)
+ M epsilon^(-3)delta^(-1)
+ M delta^(-2).
```

Applying the positive flow-box bound again gives

```text
m^2 ||g'||_infinity
 <= C T_epsilon,delta(M,L) Q_m(h).
```

This directly supplies a `W^{1,infinity}` estimate with no exponential word-count loss.

The manuscript correctly restricts the differentiable weighted class. Uniformly Lipschitz initial and terminal collision-state functions fit the theorem. An arbitrary measurable path selector does not.

The absence of boundary distributions is a load-bearing point. In particular, a future specialist audit should verify the zero traces of the full guarded product at every word-domain boundary, the cancellation of periodic arclength seams, and the treatment of nondifferentiable distance functions by Lipschitz approximation.

## 10. Common-band noncritical inversion

For a `W^{1,infinity}` function,

```text
|g(t)-g(t-s)| <= ||g'||_infinity |s|.
```

The first absolute moment of the fixed Schwartz approximate-identity kernel therefore gives

```text
m^2 ||g-K_B*g||_infinity
 <= C B^(-1) T_epsilon,delta(M,L) Q_m(h).
```

This estimate is independent of any componentwise second-derivative budget. It also remains valid for an arbitrary diverging sequence `B_m`, once `epsilon` and `delta` are fixed, because the spectral input was used only to bound a fixed positive roof window.

The paper is explicit that this is not a growing-band transfer-operator theorem. That distinction is correct.

## 11. Completion of the low-gradient source

On the protected low-gradient source,

```text
|grad F| <= 2 delta.
```

The two endpoint tangential velocities are therefore small. In a protected endpoint square the reduced Hessian becomes uniformly positive because the endpoint cosines remain bounded away from zero. Strict convexity gives a unique interior normal-to-normal minimum at distance `O(delta)` from the original source point and roof excess `O(delta^2)`.

If `delta < c epsilon^3`, the continuation remains inside the endpoint square and the critical center is `epsilon/2`-protected with the same exact integer labels. Thus the low-gradient source lies in the actual protected critical collars already controlled in revision 45.

This is a clean bridge between the new noncritical theorem and the inherited critical-cluster theorem. I found the scale `delta < c epsilon^3` consistent with the endpoint-collar radius and the `O(delta^2)` roof excess.

## 12. The protected correction modulus

The protected source is split into the high-gradient and low-gradient pieces. The first is controlled by the derivative estimate; the second by the critical-cluster density estimate.

After taking the collision limsup at fixed `epsilon`, `delta`, and `B`, the bound is

```text
C [ B^(-1)(L delta^(-1)
             + M epsilon^(-3)delta^(-1)
             + M delta^(-2))
    + M delta^2 ].
```

The choice `delta=B^(-1/4)` gives:

- `B^(-1)delta^(-2)=B^(-1/2)`;
- `delta^2=B^(-1/2)`;
- `B^(-1)delta^(-1)=B^(-3/4)`;
- `epsilon^(-3)B^(-3/4)<=C B^(-1/2)` when `B>=C epsilon^(-12)`.

The same bandwidth condition guarantees `delta<c epsilon^3`.

Thus the asserted modulus

```text
C(M+L) B^(-1/2)
```

is algebraically correct.

The bandwidth and protection are fixed in the collision limsup. The text does not claim a rate in `m`.

## 13. Diverging bandwidths at fixed protection

For an arbitrary deterministic sequence `B_m->infinity`, the proof does not substitute `B_m` into the fixed-band limsup modulus.

Instead it fixes `epsilon` and `delta` in the finite-time inequality. The high-gradient term tends to zero because `Q_m(h)` is eventually bounded and `B_m` diverges. The low-gradient term has collision limsup `O(delta^2)`. Letting `delta` tend to zero after taking the limsup gives zero.

This is a valid diagonal-free argument for fixed protection. It supplies no quantitative convergence rate in the collision count, and the manuscript says so.

## 14. Uniform mass of the unprotected source

The complement of the guard is estimated by summing one-flight bad-margin probabilities.

For incidence,

```text
nu{cos(phi)<s}=O(s^2).
```

For the moving finite-rectangle section, a boundary neighborhood has mass `O(s)`.

For a regular flight passing within distance `s` of a nonincident disk, the closest point lies in the interior when `s` is below the fixed inter-disk gap. The line-to-center distance has an angular derivative uniformly separated from zero because the initial point is at least `53/100` from the candidate center while the radius is at most `47/100`. Hence the angular set has measure `O(s)`.

Collision invariance applies these estimates at every time. The graded thresholds form two geometric tails from the endpoints, so their sum is bounded independently of `m`. Consequently

```text
int(1-Xi_m,R^epsilon) dnu_R^* <= C epsilon.
```

The exact-label events are disjoint at a fixed collision count, giving the corresponding summed component mass bound.

This is a meaningful and correctly normalized source-exhaustion result. It uses no independence or mixing.

The near-clearance transversality and the finite candidate-disk list are, however, geometric inputs requiring direct verification. In particular, the exclusion of endpoint minima and the relation between capped clearance and physical first-hit selection should be checked by a billiards specialist.

## 15. Ordered protection and arithmetic reduction

The choice

```text
epsilon(B)=A B^(-1/12)
```

makes the protected-correction condition `B>=C epsilon^(-12)` valid for each fixed sufficiently large `B`. Therefore, after the collision limsup,

```text
protected correction = O(B^(-1/2)).
```

The complementary source has total mass `O(B^(-1/12))`.

The paper emphasizes that these estimates are in different norms.

The exact source split gives

```text
D_B(full)=D_B(protected)
          + [b^epsilon-K_B*b^epsilon].
```

Using the fixed-band transition theorem, the full arithmetic pointwise law is equivalent to vanishing of the second term in the ordered limits

```text
m->infinity, then B->infinity.
```

The converse is also correct: if the full raw law holds, the full correction tends to zero at every fixed band, and subtracting the protected part bounds the boundary correction by `O(B^(-1/2))` after the collision limsup.

This criterion is extraction-independent and retains the correct arithmetic main term.

It remains a criterion, not a proof of the criterion's hypothesis.

## 16. The decisive unresolved estimate

The remaining source is

```text
(1-Xi_m,R^epsilon) nu_R^*.
```

It consists of histories having at least one collapsing incidence, section-decision margin, or nonincident clearance. Its exact-label roof density is `b^epsilon`.

The full theorem now requires

```text
lim_{B->infinity} limsup_{m->infinity}
 sup_{R,n,k} m^2 esssup_{central t}
 |b^{epsilon(B)}-K_B*b^{epsilon(B)}| = 0.
```

Revision 46 does not establish this.

The mass bound

```text
sum ||b^epsilon||_1 <= C epsilon
```

is insufficient. A source of small mass may concentrate on roof intervals much shorter than the local scale. A finite jump retains its pointwise height under support localization. A noncritical residual may have a large derivative or high-frequency inverse. Near-grazing and competing-hit geometry can create precisely such concentration.

The inherited complete fixed-count height bound is exponential in `m`, not `O(m^(-2))`, and therefore cannot combine with the `O(epsilon)` mass estimate at the stated ordered scale. The qualitative count-dependent diagonal merely chooses an increasingly permissive protected source; it does not bound the pointwise correction of its complement.

This is now the sole explicitly isolated unweighted pointwise obstruction, but it is still the central obstruction.

## 17. The qualitative count-dependent protection diagonal

For a prescribed diverging sequence `B_m`, the manuscript chooses a sequence `epsilon_m->0` slowly enough that the protected correction tends to zero. The complementary source mass also tends to zero.

This diagonal is logically valid. It makes no claim about a prescribed rate for `epsilon_m`.

It does not prove the raw LLT because the complement is controlled only in total variation. In particular, the two conclusions

```text
m^2 ||D_{B_m}^{epsilon_m}||_infinity -> 0,
sum ||b^{epsilon_m}||_1 -> 0
```

do not imply pointwise smallness of the full correction.

The paper records this limitation accurately.

## 18. Arithmetic structure

The revision preserves the correct arithmetic objects.

At fixed radius, the exact-index candidate main term is

```text
c mathfrak a_R(k,n,m) g_{Omega_R}(Z),
```

or equivalently `mathfrak a_R g_{D_R}` in return normalization.

Uniformly through changes of arithmetic type, the candidate main term is the finite Gaussian transition sum `mathcal L_{m,R}`.

The protected estimates sum all surviving resonant branches and do not require the section residues to be trivial. The boundary-reduction theorem retains the same transition kernel.

The concrete section phase masses are still not proved uniform. Therefore the manuscript does not prove an unmodulated radius-uniform singleton theorem, and it should continue to avoid presenting one.

## 19. Weighted consequences and conditioning

The new regular derivative theorem covers insertions with both a supremum bound and a weak endpoint-gradient bound. In particular, products of uniformly Lipschitz initial and terminal collision-state functions are included.

The protected critical part still admits arbitrary bounded measurable insertions by domination, and the complementary source has the same total-variation mass bound for arbitrary bounded weights.

What is not proved is the pointwise signed-correction estimate for the complete weighted boundary source. Arbitrary path selectors need not possess the endpoint derivatives required by the regular theorem. The fixed-interval bridge and phase-posterior theorems therefore do not become pointwise roof-conditioned bridge statements.

A completed conditioning program would require a boundary estimate for the relevant weighted numerators and denominators, not only the unweighted criterion.

## 20. Mathematical significance at the requested benchmark

The paper now contains a substantial collection of completed results:

- a stationary physical singleton local law;
- compact-family extensions and an explicit nonelliptic family;
- actual-return diffusive-window and arbitrarily slowly diverging-window laws;
- exact-index fixed-interval arithmetic local laws;
- parameter-uniform arithmetic transition kernels;
- exact-event Gaussian return bridges;
- arithmetic endpoint posteriors;
- complete finite-count density height bounds;
- exclusion of divergent physical germs;
- jump--cusp separation;
- pointwise removal of continuous cusp contributions;
- deconcentration of protected coalescing critical clusters;
- pointwise removal of shrinking protected critical sources;
- a count-compatible complete-component correction;
- coefficient-first pointwise reconstruction;
- a protected noncritical `W^{1,infinity}` estimate;
- control of the entire smoothly protected signed correction;
- uniform source-mass exhaustion by graded protection.

These are technically substantial results.

At the four-journal benchmark, however, the current architecture remains centered on an unproved title-level endpoint. The newest result reduces that endpoint to one positive boundary source, but the pointwise estimate for that source is absent. The paper also remains highly specialized to one finite-horizon triangular billiard family and contains ninety-nine core modules, many of which preserve historical conditional interfaces rather than support a single completed theorem.

Subject to specialist verification, the completed results could support a strong focused dynamics/probability paper. They do not yet establish the complete arithmetic raw local inversion theorem or the breadth expected at the requested four-journal level.

## 21. Independent specialist verification

The following claims require direct human expert audit:

1. the exact contact second variation inherited from the critical analysis;
2. arbitrary-endpoint continuation with graded margins;
3. the reduced-action Schur Hessian bounds;
4. the cross-Hessian source-density formula away from normal endpoints;
5. the `epsilon^(-3)` logarithmic distortion budget;
6. the endpoint-coordinate derivatives of incidence, section distance, and clearance;
7. weak differentiation of minimum-distance guards at medial axes;
8. zero extension at every physical and section-decision boundary;
9. existence and exact label preservation of the roof-translation flow;
10. weighted flow Jacobian and coarea comparison;
11. flow-box injectivity over all physical words;
12. the distributional derivative and absence of boundary measures;
13. completion of small-gradient points to protected critical centers;
14. the inherited critical-cluster theorem;
15. the one-flight nonincident-clearance transversality estimate;
16. the full occupation-torus anisotropic spectral theorem;
17. scalar projection continuity through arithmetic transitions;
18. the uniform transition fixed-window theorem;
19. the complete finite-graph density at singular and decision boundaries;
20. the remaining collapsing-margin correction.

The successful workflows and finite models do not settle these continuum questions. The manuscript and validation protocol accurately distinguish source qualification from proof certification.

## 22. Required work for a subsequent revision

A subsequent revision seeking the same benchmark should address the following in priority order.

### 22.1 Prove the collapsing-margin boundary criterion

Establish

```text
lim_{B->infinity} limsup_{m->infinity}
 sup m^2 esssup |b^{epsilon(B)}-K_B*b^{epsilon(B)}| = 0
```

on central exact-index sets, with the arithmetic transition kernel retained.

This is the decisive remaining item. A further equivalent formulation or a smaller mass estimate will not change the recommendation.

### 22.2 Decompose the boundary source by its first bad margin

A promising route is to split the complement according to the earliest or most severe failure among:

- grazing incidence;
- competing-hit clearance;
- section-decision distance.

For each class, construct a label-preserving coordinate or flow adapted to the bad margin and prove a pointwise density or signed-correction estimate. The current protection flow cannot be applied where the relevant margin is already collapsing.

### 22.3 Control finite jumps on the boundary source

Revision 44 paid all continuous positive-exponent cusp terms, and revisions 45--46 control the protected regular jumps. The remaining boundary finite jumps must be shown to be `o(m^(-2))`, included in a correct additional main term, or canceled by an explicit paired source.

Small source mass does not control a jump coefficient.

### 22.4 Control the boundary noncritical inverse

Develop a replacement for the protected roof-flow argument near singular and decision boundaries. Possibilities include one-sided flow boxes, stratified coarea coordinates, direct oscillatory cancellation, or a quantitative boundary transfer theorem. The complete residual inverse must be treated, not only its total mass.

### 22.5 Supply prescribed count-dependent thresholds

If the final proof uses `epsilon=epsilon_m`, provide an explicit rate and estimates valid at that rate. The present qualitative diagonal cannot be inserted into a uniform local theorem.

### 22.6 Complete the weighted boundary theory

Extend the final boundary correction estimate to the endpoint and path insertions required for pointwise conditioning. Distinguish Lipschitz endpoint weights from arbitrary measurable path selectors.

### 22.7 Retain the arithmetic theorem in its correct form

State the final pointwise result with `mathfrak a_R` at fixed radius and `mathcal L_{m,R}` uniformly, unless a separate proof establishes triviality of every nontrivial concrete section residue.

### 22.8 Obtain independent specialist review

The collision geometry, graded continuation, flow-box proof, finite-graph preparation, anisotropic spectrum, resonance transitions, and bridge arguments should be checked by specialists before publication claims are made.

### 22.9 Reduce the central route

A top-four submission should present a completed principal theorem through a concise dependency chain. The historical ninety-nine-module pipeline is useful as an archive, but unresolved interfaces should not dominate the main article.

## 23. Technical comments

1. Keep `m` for collision count and `n` for return index in every formula and supremum.
2. Keep `B` for roof bandwidth and use distinct notation for derivative entries and intrinsic jumps.
3. State whenever `epsilon`, `delta`, `h`, and `B` are fixed before the collision limit.
4. Do not infer a shrinking-window theorem from the fixed-window bound for `Q_m(h)`.
5. Do not substitute `B_m` into the fixed-band collision-limsup modulus; retain the separate finite-time argument.
6. Keep the distinction between the weak derivative of the guard and pointwise differentiability of distance functions.
7. List all genuine word-domain boundaries at which the zero extension is used.
8. Preserve the original section factor `(4 pi R c)^(-1)` in the source density.
9. Keep the lower Hessian bound's dependence on endpoint incidence visible outside the near-normal region.
10. Do not call the `W^{1,infinity}` approximate-identity estimate a growing-band spectral theorem.
11. The constant in the fixed-window limsup is independent of fixed `h`; the finite-time threshold need not be.
12. Keep the support and derivative conditions on admissible weighted insertions explicit.
13. Do not infer pointwise smallness of `b^epsilon` from its `O(epsilon)` total mass.
14. Do not combine the exponential fixed-count height bound with the boundary mass as though it gave an `m^(-2)` estimate.
15. Preserve the exact arithmetic transition kernel in every radius-uniform target.
16. A zero arithmetic residue corresponds to an exactly null class; do not attach a conditional law to a zero denominator.
17. Keep the right-trace convention at finite jumps.
18. A finite packet average does not identify a prescribed singleton.
19. The pointwise roof-conditioned bridge remains unproved.
20. Source qualification and finite diagnostics remain distinct from continuum proof certification.

## 24. Overall assessment

Revision 46 is a serious and constructive response to the revision-45 report.

It extends the protected geometry to arbitrary regular histories, constructs a word-length-independent graded guard, proves a positive label-preserving roof-flow comparison, obtains a genuine `W^{1,infinity}` noncritical density estimate, and controls the common-band noncritical inverse without summing unknown second-derivative budgets. It completes small-gradient points to the already controlled critical collars and thereby proves a `B^(-1/2)` collision-limsup modulus for the entire smoothly protected correction. It also proves a uniform `O(epsilon)` mass exhaustion of the original source and isolates one extraction-independent collapsing-margin boundary correction.

I found no decisive error in modules 98--99 within the scope of this review.

The paper nevertheless remains short of the theorem governing its title and central architecture. The signed correction of the collapsing-margin source is not shown small at the local scale; its mass estimate is not a density estimate; boundary jumps and boundary noncritical inverses remain; the prescribed-rate weighted theory remains open; and the concrete arithmetic residues are not proved trivial.

Subject to independent specialist verification, the completed stationary, interval, arithmetic, bridge, posterior, full-source reconstruction, height, cusp, critical-cluster, and protected-inverse results could support a strong focused paper. They do not yet constitute a complete top-four raw local inversion theorem.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
