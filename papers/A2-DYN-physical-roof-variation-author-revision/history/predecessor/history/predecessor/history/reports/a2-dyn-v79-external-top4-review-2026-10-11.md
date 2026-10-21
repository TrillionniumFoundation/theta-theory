# External top-four referee report on A2-DYN revision 79

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v79-referee-response-2026-10-11`, `revision/a2-dyn-v79-referee-copy-2026-10-11`  
**Reviewed commit:** `be7d5f2c076b73b3da254d36b1268d3cb842ea6a`  
**Reviewed repository tree:** `4465ab4bb0c7241bbe239414c17820b1ca793e83`  
**Active manuscript directory:** `papers/A2-DYN-v79-referee-response`  
**Active mathematical source:** one hundred eighty-two numbered core modules; revision 79 adds modules 180--182  
**Frozen revision-78 author baseline:** `5af5cbc845bfe1f73d835fee2f65fffddc7c0e55`  
**Frozen revision-78 paper tree:** `0239ebffad6c3b6e75f070e29dd1bfc59c97491e`  
**Controlling report:** `reviews/a2-dyn-v78-external-top4-rereview-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `e3cd829a662db368b9dbc6db1fb9f0a1be5f60c3` / `cb19ddee147ba0978c638e4792d03a8d951272e7`  
**Additional v78 report considered:** commit `44dc4675d03488b404c0d3269b3bac63f3fd1144`, blob `ebc04c596d8e071dbd7abcb5715ab7fd77104a19`  
**Exact-source qualification runs:** response `38134473944`; referee-copy `38134479434`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, optical-geometry, geometric-measure-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 79 is a genuine and mathematically substantive response to the revision-78 reports. The earlier source had reduced the remaining geometric obstruction to two positive components: true exits from the original exact event and physical coarea-volume loss on surviving same-label trajectories. It had not separated the angular contribution to the physical Jacobian from the inverse optical twist, and its available third-derivative estimates were local in the regular word.

Revision 79 makes three real advances.

First, it proves a collision-uniform third-derivative estimate for the reduced roof on every regular physical word. The key stationary-action identity cancels all terms containing second derivatives of the internal contact map. The resulting estimate uses only first contact derivatives, which decay geometrically with distance from the two endpoints, and uniformly bounded third derivatives of individual flight lengths.

Second, it factors the physical Jacobian of the canonical endpoint-momentum flow into an inverse-twist ratio and an angular Hessian ratio, and it proves that the complete angular part contributes at most `C sqrt(r)` in the required ordered `m^2` normalization. Thus the previously unspecified interior volume loss is genuinely reduced to the inverse-twist loss.

Third, it gives a positive optical sensitivity formula, controls the complete optical loss on a specified incidence corridor, and derives an exact first-exit boundary formula with the initial source weight and the inverse forward Jacobian. This corrects the tempting but invalid identification of original starting mass with unweighted physical boundary flux.

I audited the new modules

- `core/180_uniform_cubic_reduced_action.tex`;
- `core/181_separated_physical_volume_budget.tex`;
- `core/182_optical_sensitivity_and_exit_flux.tex`;

and their immediate dependence on modules 174 and 177, the inherited fixed-width source estimates, the v78 reports, the revised opening, response, proof ledger, source manifest, specialist-audit document and exact-SHA qualification records.

Within that scope, I found no decisive counterexample, missing exact label, reversed endpoint convention, illegal growing-band substitution, sign error in the Jacobian factorization, or hidden claim that the remaining positive defects have already been proved small.

The negative recommendation is nevertheless forced by the manuscript's own final reduction. Revision 79 proves

```text
E_M <= C_M B^(-1/192)
       + X_{epsilon(B),M}(r)
       + O_{epsilon(B),M}(r)
       + C (1+epsilon(B)^(-1)) sqrt(r),
```

where `X` is the ordered height of the averaged true-exit mass and `O` is the ordered height of the averaged inverse-twist loss. It does **not** prove a decay estimate for either complete quantity.

The regular optical theorem controls only the incidence corridor. Its complement is dominated pointwise by the unchanged bad source `b^(C delta)`, whose pointwise roof height is precisely of the type still unavailable. The first-exit theorem is an exact flux representation, not a collision-uniform roof-height estimate for the pulled-back flux. Therefore the organizing exact-label pointwise local limit theorem remains open.

At the requested benchmark, proving the angular factor and identifying the exact boundary and optical mechanisms are important advances. They are not substitutes for proving the two remaining positive defects small.

## 2. Frozen source and qualification

Both reviewed author branches resolve to

`be7d5f2c076b73b3da254d36b1268d3cb842ea6a`.

The repository tree is

`4465ab4bb0c7241bbe239414c17820b1ca793e83`.

The active journal source is

`papers/A2-DYN-v79-referee-response/main.tex`,

and the complete inherited article is assembled by

`papers/A2-DYN-v79-referee-response/supplement.tex`.

The source manifest records one hundred seventy-nine inherited core modules and one hundred eighty-two active modules. The additions are exactly modules 180--182. It records byte preservation of inherited cores, Python sources, appendices, bibliographies and provenance, and it keeps the complete revision-78 article in the supplement.

The exact-source qualification workflows completed successfully at the reviewed author SHA on both refs:

- response branch run `38134473944`;
- referee-copy branch run `38134479434`.

These runs establish exact checkout identity, preservation of the frozen baseline and controlling report, normal/optimized finite-fixture agreement, native journal and supplement compilation, recorder coverage and PDF geometry checks. They do not certify the continuum stationary-action calculation, optical normalization, target-direction coarea covariance, boundary exhaustion, inherited spectral inputs, or the two missing endpoint estimates.

The source manifest is appropriately conservative. It marks as proved the stationary cubic cancellation, the uniform reduced-roof third derivative, angular Jacobian motion, complete angular-volume comparison, positive optical sensitivities, regular optical contribution, thin-source domination and initial-weight first-exit identity. It leaves false the flags for complete true-exit roof-height decay, complete inverse-twist roof-height decay, the full raw return LLT, the pointwise roof-density LLT, unrestricted same-roof conditioning, forward essential-likelihood convergence, independent human review and formal proof certification.

The present review branch starts directly from the final author SHA and adds this report only under

`reviews/a2-dyn-v79-external-top4-review-2026-10-11/`.

## 3. Scope of this review

The complete supplement contains a long historical pipeline. I have not attempted to re-certify all one hundred eighty-two core modules. The substantive audit concerns:

1. the stationary-action cubic identity;
2. the uniform sum of per-flight third derivatives;
3. the distinction between a pointwise derivative bound and a common continuation neighborhood;
4. the angular Hessian ratio along the canonical flow;
5. the physical Jacobian factorization;
6. target-direction coarea covariance on the complete exact-label source;
7. the separated endpoint budget and criterion;
8. the positive optical recursion and its sensitivities;
9. the incidence-corridor optical estimate;
10. domination of the thin optical complement by the original source;
11. the initial-weight first-exit formula and inverse Jacobian;
12. the fixed-count monotone exhaustion;
13. the relationship of these results to the original scalar endpoint; and
14. source identity and qualification evidence.

The inherited fixed-width complete-source bound, positive scalar remainder, optical inverse estimate, all-contact first-derivative decay, exact arithmetic reference, path remainder and collision-to-return transfer are treated as source-pinned inputs. This report does not independently re-prove those historical chains.

## 4. Stationary cubic cancellation

Module 180 begins with a general stationary-action lemma. If

```text
partial_z S(q,z(q)) = 0,
F(q) = S(q,z(q)),
U_u = (u,Dz(q)u),
```

then it proves

```text
D^3 F(q)[u,v,w] = D^3 S(q,z(q))[U_u,U_v,U_w].
```

This identity is correct at the formal differential level. Differentiating the stationary equation gives

```text
D^2 S[U_u,(0,zeta)] = 0
```

for every internal vector `zeta`. When the formula for `D^2 F` is differentiated, the derivatives of the lifted vectors are purely internal and are annihilated by this identity. Thus no bound on `D^2 z` or on the inverse internal Hessian enters the cubic formula.

This is a useful observation in the present billiard problem. Near an internal grazing collision, the smooth continuation neighborhood can shrink and second derivatives of the contact map can diverge, while the first derivative along an actual regular trajectory may remain controlled after the incidence normalization. The lemma correctly separates these issues.

The statement is local, and the manuscript does not claim continuation through a singularity. I found no circular use of the desired third-derivative bound in this cancellation.

A specialist should nevertheless verify the coordinate conventions carefully: the internal variables use oriented arclength, the endpoint variables use angles, and the physical Hessian is `D_c A D_c`. The proof is valid only if the stationary equations and the lifted contact derivatives are written in one consistent mixed coordinate system. The manuscript appears to do this, but this is a load-bearing geometric check.

## 5. The uniform reduced-roof third derivative

For an individual flight of length at least `tau_-`, the manuscript bounds the first three derivatives of the Euclidean norm and combines them with the first three derivatives of a circular arclength parametrization. It obtains a fixed per-flight cubic constant

```text
C_3 = 6/tau_-^2 + 3/(R_- tau_-) + 1/R_-^2.
```

The lifted endpoint direction at contact `j` is bounded by

```text
|U_j| <= C_Q q_0^(d_j) |u|.
```

Each flight joins contacts whose depths are at least the associated flight depth. Since at most two flights occur at any depth, the sum of cubic contributions is bounded by a geometric series. This yields one constant `T_*` independent of collision count, radius, exact labels, positive internal incidences and positive clearances.

The mechanism is mathematically plausible and materially stronger than a wordwise local estimate. In particular, it does not sum absolute constants over exponentially many words: the theorem is proved pointwise on every actual regular word and is then used through the complete-source transport comparison.

I found no missing factor growing with the collision length in the printed depth sum. The most important independent checks are:

- the all-contact first-derivative estimate from module 177 must apply to the same reduced action and the same endpoint variables;
- the per-flight third derivative must include all mixed derivatives coming from the two moving contacts;
- tangent orientation changes must not alter the absolute derivative bound;
- the minimum flight bound must hold on every regular physical word in the stated family; and
- no endpoint-angle factor of `R` may be lost when passing between arclength and angle coordinates.

Subject to those checks, the theorem appears coherent.

## 6. Angular Hessian motion

Along the canonical flow, the direction of the endpoint momentum gradient is constant. In dimension two the angular Jacobian is

```text
chi = (e_perp)^T K e_perp,
```

where `K=D_q^2 F`. The new cubic bound therefore gives

```text
|chi(Phi_h x)-chi(x)| <= C sqrt(h).
```

The lower bound for `chi` converts this to a logarithmic ratio estimate. The flow is conjugate by `(F,vartheta)` to translation in the roof coordinate, and the endpoint-coordinate Jacobian is

```text
J_h^q = chi(x)/chi(Phi_h x).
```

This part of the argument is internally consistent. The square-root scale comes from the inherited endpoint-curve length estimate, not from a Hölder assumption on the Hessian.

The result closes the specific issue left open in revision 78: the angular part of the physical Jacobian no longer carries an unquantified reduced-roof third derivative.

## 7. Physical Jacobian factorization

The original collision measure is constant in `(alpha_0,p_0)` coordinates. Passing to endpoint-angle coordinates introduces the density

```text
omega = |partial_{p_0} alpha_m|^(-1).
```

Combining this density ratio with the endpoint-coordinate Jacobian gives

```text
eta_h = omega(Phi_h x)/omega(x),
J_h   = eta_h * chi(x)/chi(Phi_h x).
```

This is the correct structural factorization: `eta_h` is the inverse-twist contribution and the `chi` ratio is the angular contribution.

The comparison

```text
|[1-eta_h k_h]_+ - [1-eta_h]_+|
    <= eta_h |1-k_h|
```

is valid because the positive-part map is one-Lipschitz. Since the `chi` ratio is uniformly comparable to one, `eta_h` is bounded by a fixed multiple of the physical Jacobian `J_h`.

Target-direction coarea covariance then gives

```text
int_{S_h(t)} J_h dmu_t <= p(t+h).
```

Averaging over `0<h<r` and using the inherited fixed-width estimate for the unweighted density yields the ordered `C sqrt(r)` bound.

I found no sign reversal or source/target density inversion in the displayed factorization. This is one of the strongest new results of the revision.

The specialist issue is measure-theoretic rather than algebraic. The source uses many regular physical words and only joint almost-everywhere coarea versions. The proof should be checked for a single common measurable decomposition, no double counting at word interfaces, and compatibility of the source and target fiber versions before the collision supremum is taken. The inherited interface ledger and exact-event partition are intended to provide this, but finite fixtures cannot establish it.

## 8. The complete angular-volume estimate

Let `V_h` be the positive physical volume loss and `O_h` the positive inverse-twist loss. Revision 79 proves

```text
|bar V_r(t)-bar O_r(t)| <= C sqrt(r) A_r p(t)
```

before any collision limit. The unweighted fixed-width source theorem then gives

```text
limsup_m sup_{R,n,k} m^2 ||bar V_r-bar O_r||_infinity
    <= C sqrt(r)
```

for every previously fixed width.

This is a complete-source estimate. It does not multiply a per-word estimate by the number of words and does not require a pointwise bound on `p`. The order of limits is legal: `r` and all auxiliary spectral parameters are fixed before the collision limit.

The conclusion is exactly as strong as the proof supports. It says that the positive physical volume defect is equivalent, up to a controlled angular error, to the positive inverse-twist defect. It does **not** say that either defect is small by itself.

## 9. The separated endpoint theorem

The new endpoint budget reads

```text
E_M <= C_M B^(-1/192)
       + X_{epsilon(B),M}(r)
       + O_{epsilon(B),M}(r)
       + C_Theta (1+epsilon(B)^(-1)) sqrt(r).
```

The source-shift inequality preceding this estimate retains

- the full original source;
- every exact displacement and occupation label;
- true exits;
- the physical volume defect;
- the original guard mismatch; and
- the complete finite arithmetic reference.

No positive source is deleted by the signed occupation-current identity. No arithmetic zero class is normalized away.

The proof also records a sufficient pair of estimates

```text
X_{epsilon,M}(r) <= C_M epsilon^(-q_X) r^(beta_X),
O_{epsilon,M}(r) <= C_M epsilon^(-q_O) r^(beta_O),
```

and a legal choice of `r` as an outer power of `epsilon(B)`.

This theorem is useful because it separates mechanisms that require different tools. It is, however, a conditional closure theorem. The two displayed estimates are explicitly proof obligations.

The stated qualitative criterion is mathematically correct but should not be confused with an independent advance toward proving the criterion. Necessity follows because, if the scalar pointwise theorem is already known, both positive defect sources are bounded by the already small original bad source. Sufficiency follows from the separated endpoint budget. Thus the criterion accurately identifies the endpoint; it does not estimate it.

## 10. Positive optical recursion

Module 182 writes the incidence-normalized optical matrix as the standard tridiagonal matrix with

```text
A_ii = t_{i-1}+t_i+V_i,
A_i,i+1 = -t_i,
t_i = 1/ell_i,
V_i = 2/(R c_i).
```

The recurrence

```text
y_0=0, f_0=1, y_1=ell_0,
f_i=f_{i-1}+V_i y_i,
y_{i+1}=y_i+ell_i f_i
```

produces a polynomial `y_m` with nonnegative coefficients which is separately affine in each flight length and internal potential. The manuscript identifies

```text
y_m = (product ell_j) det A,
omega = R c_0 c_m / y_m.
```

For a positive separately affine polynomial, each logarithmic sensitivity lies in `[0,1]`. The resulting differential of `log omega` retains each inverse-incidence term with a coefficient between zero and one.

I found the recurrence, positivity and separate-affineness argument coherent. It is important that the theorem does not claim the inverse incidences disappear. Positivity controls their coefficients; it does not make the complete source integral finite or small.

The normalization `omega=R c_0 c_m/y_m` and the cancellation of internal incidence squares in the endpoint Schur complement are specialist-level identities and should be checked independently. No inconsistency is apparent from the printed recurrence and the low-dimensional cases.

## 11. The regular optical corridor

On trajectories satisfying

```text
c_i(Phi_s x) >= delta q_0^(d_i/2)
```

for all internal contacts and all `0<=s<=h`, the logarithmic derivative of `omega` is bounded by `C delta^(-1)` along the endpoint curve. For `r<=c delta^2`, the manuscript obtains

```text
limsup_m sup_{R,n,k} m^2
 ||bar O_r^(epsilon,reg(delta))||_infinity
    <= C delta^(-1) sqrt(r).
```

This estimate is internally coherent and uses only the fixed-width unweighted source bound after target coarea covariance.

It controls the complete regular part: no physical word satisfying the corridor is omitted. It also preserves the correct quantifier order.

## 12. The thin optical complement

If the corridor fails at some time before `h`, the inherited margin-motion estimate implies that the starting incidence is at most a constant multiple of

```text
delta q_0^(d_i/2).
```

The corresponding factor in the original guard with auxiliary parameter `C delta` is zero, so the thin starting set is dominated by the original positive source `b^(C delta)`. This gives

```text
bar O_r^(epsilon,thin(delta))(t) <= b^(C delta)(t).
```

This is a correct pointwise source domination. It is also where the closure stops.

The manuscript has only a fixed-width estimate for `b^(C delta)`, not a collision-uniform pointwise height estimate. Choosing `delta` small does not by itself make

```text
limsup_m sup_{R,n,k} m^2 ||b^(C delta)||_infinity
```

small. A positive density can concentrate in a narrow roof interval while every previously fixed average remains controlled.

Thus the regular optical theorem cannot be combined with thin-source domination to prove the complete optical height without a new concentration estimate. This is not a technical afterthought; it is one of the two central unresolved terms.

## 13. The first-exit flux formula

For a relatively compact regular domain `D`, module 182 derives

```text
E_{D,h}^epsilon(t)
 = integral_{Gamma_D^+}
   1_{0<L(y)-t<=h, L(y)-t<tau_D^-(y)}
   W^epsilon(x_{t,y}) / J_{L(y)-t}(x_{t,y})
   d zeta_D(y).
```

The formula has three essential features.

1. The weight is evaluated at the **initial** point, not at the exit.
2. The inverse forward Jacobian converts physical boundary flux back to initial source mass.
3. The backward lifetime selects the first forward exit rather than a later re-entry.

These features are correct in flow-box coordinates. If the physical source has density `a(u,theta) du dtheta`, the exit flux is `a(b(theta),theta)dtheta`, while the starting fiber mass is `a(t,theta)dtheta`; their ratio is exactly the inverse physical Jacobian.

This also explains why vanishing unweighted boundary density at a grazing exit does not imply vanishing initial exit mass: the inverse Jacobian may diverge.

I found no sign or orientation error in the stated formula. The principal specialist checks are the construction of the regular flow-box domains, the treatment of tangential and lower-dimensional boundary strata, measurable summation without multiplicity, and the common almost-everywhere versions in `(t,h)`.

## 14. Fixed-count exhaustion

For an increasing regular exhaustion `D_l` of the full regular exact event, the manuscript proves

```text
E_h^epsilon(t)
 = lim_l { initial mass outside D_l + E_{D_l,h}^epsilon(t) }.
```

The bracketed quantities are nonnegative and decrease. Pointwise in the starting state, they are the indicator that the forward segment of length `h` is not contained in `D_l`. Their limit is the indicator of a true exit from the full regular event.

This is the correct source-level limiting statement. The manuscript also correctly fixes the collision count before taking the exhaustion limit. It does not claim total-variation convergence uniformly in collision count.

Again, the result is a representation theorem. It does not estimate the roof-localized height of the pulled-back flux.

## 15. The two remaining endpoint estimates

After revision 79, the unresolved scalar problem is cleaner than before, but it remains substantial.

### 15.1 Complete true-exit height

The first-exit identity must be converted into a bound of the form

```text
X_{epsilon,M}(r) <= C_M epsilon^(-q_X) r^(beta_X)
```

or an equally strong qualitative decay in the legal outer limit.

This requires collision-uniform control of

- grazing exits;
- competing-hit and third-obstacle exits;
- true section-decision exits;
- exact-event boundary exits;
- simultaneous first failures;
- the inverse physical Jacobian in the boundary pullback; and
- concentration of the resulting flux in the roof variable.

Total exit probability, phase-space thickness of the exit layer, or unweighted physical boundary flux is not enough. The estimate is an `m^2`-normalized essential roof-height statement at the original exact labels.

### 15.2 Complete inverse-twist height

The regular incidence corridor is controlled, but the thin complement remains dominated by `b^(C delta)`. Closing this term requires either

- a pointwise concentration theorem for the thin original source;
- a direct weighted inverse-twist estimate which gains enough incidence factors before the roof pushforward; or
- a genuine singular/surface spectral insertion theorem applicable to this source.

None of these is supplied by the current manuscript. The bounded volume-multiplier theory in the inherited spectral chain does not automatically apply to inverse-incidence or boundary insertions.

## 16. Why the new formulas do not imply smallness

The principal danger at this stage is to confuse structural exactness with quantitative decay.

- A uniform per-word third derivative does not control the mass of words near a physical boundary.
- A Jacobian factorization does not bound the inverse-twist ratio on near-grazing sources.
- A positive sensitivity formula does not remove inverse incidences.
- A source domination by `b^(C delta)` does not bound its pointwise roof height.
- A first-exit flux formula does not control concentration of that flux after projection to the roof.
- A fixed-count monotone exhaustion does not commute automatically with the collision-normalized limsup.
- An exact necessity-and-sufficiency criterion does not prove either side of the criterion independently.

The manuscript generally respects these distinctions. They are exactly why the two endpoint flags remain false.

## 17. Downstream path and likelihood conclusions

The retained positive path-remainder theorem equates the ordered scalar endpoint error with the bounded-Lipschitz path-numerator error once the scalar endpoint is closed. The collision-to-return clock transfer and forward likelihood statements also remain downstream of scalar closure.

Revision 79 does not alter this logical order. It correctly restricts normalization to positive reference classes and never divides by an arithmetic zero class.

Therefore no unconditional same-roof collision bridge, actual-return bridge, or forward essential-likelihood theorem follows from the new geometric identities alone.

## 18. Significance at the requested benchmark

The stationary-action cancellation, complete angular-volume comparison and correct first-exit pullback are nontrivial contributions. They make the endpoint obstruction more intrinsic and remove an important unquantified geometric term.

Nevertheless, the article's organizing theorem remains the exact-label pointwise raw local limit theorem, and that theorem is still unproved. The current main article is commendably shorter than the complete supplement, but the mathematical narrative is still a sequence of reductions ending in two positive estimates stated as obligations.

At the level of *Annals*, *Acta*, *Inventiones* or *JAMS*, one needs either

1. closure of both remaining endpoint estimates and hence the original pointwise theorem; or
2. a general theorem of independent breadth, with verifiable hypotheses and several genuinely different singular-hyperbolic realizations, whose significance does not depend on the unfinished Lorentz endpoint.

Revision 79 supplies neither completed endpoint nor such a broader theorem yet.

Subject to specialist verification, the new geometric results may be valuable components of a strong specialist paper or technical companion. They do not make the present combined claim top-four ready.

## 19. Required changes before another top-four review

A further revision should address the following points.

1. **Prove the complete true-exit roof-height estimate.** Use the initial-weight flux formula, including the inverse Jacobian, to obtain collision-uniform `m^2`-normalized essential-height decay at the original exact labels.
2. **Prove the complete inverse-twist roof-height estimate.** Control the thin incidence source rather than merely dominating it by another original bad source.
3. **Keep the two mechanisms separate.** Do not infer one estimate from the other or absorb a positive exit into a signed occupation current.
4. **Preserve the legal order of limits.** Every width, guard parameter and auxiliary Fourier band must be fixed before the collision limit; the outer band is enlarged last.
5. **Audit the mixed-coordinate cubic calculation.** Verify endpoint angles, internal arclengths, the physical Hessian and all factors of `R` in one consistent convention.
6. **Audit target-direction coarea covariance.** Supply one common measurable word/interface decomposition and joint almost-everywhere fiber versions for the complete source.
7. **Audit the optical normalization.** Check the continuant identity, endpoint Schur complement and `omega=R c_0 c_m/y_m` directly in the physical collision convention.
8. **Audit the exit exhaustion.** Construct the increasing regular flow-box domains explicitly enough to justify the boundary stratification and monotone first-exit limit.
9. **Obtain independent specialist review.** Experts in dispersing billiards, optical Jacobi fields, coarea transport and anisotropic transfer operators should inspect the load-bearing continuum arguments.
10. **Maintain the journal/supplement separation.** The focused article is an improvement; historical proof archives and source receipts should remain outside the main narrative.

## 20. Final assessment

Revision 79 is a substantive advance over revision 78.

It proves a uniform reduced-roof cubic estimate, removes the angular Hessian ratio from the unestimated physical volume defect, gives a useful positive optical sensitivity formula, controls the regular optical corridor, and derives the correct initial-source first-exit flux with inverse Jacobian and first-exit selection. I found no decisive mathematical error in these new statements within the audited scope.

The remaining problem is no longer an unspecified geometric remainder. It is the sum of two explicit positive roof-height defects:

- complete true-exit mass; and
- complete inverse-twist loss, including the thin incidence source.

Neither defect is proved small in the required collision-uniform order of limits. The exact-label scalar pointwise theorem and its unconditional path and likelihood consequences therefore remain open.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
