# External top-four referee report on A2-DYN revision 92

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v92-referee-response-2026-10-12`, `revision/a2-dyn-v92-referee-copy-2026-10-12`  
**Reviewed author commit:** `f1288a14908a08197365b3f3d83a7e6d59e5a676`  
**Reviewed repository tree:** `8af035016ba10d4536db4ebb79bf08a07f033b9f`  
**Active manuscript directory:** `papers/A2-DYN-v92-referee-response`  
**Canonical revision identity:** `a2-dyn-v92-one-sided-pointwise-and-positive-conditioning-2026-10-12`  
**Active mathematical source:** 219 numbered core modules; revision 92 adds modules 217--219  
**Immediate author baseline:** revision 91 at `5c7512a4341d8277101d9c0b609dc7d2cda1512a`  
**Frozen revision-91 paper tree:** `5637513690e13d4abf1a46eedb568327648a0b1f`  
**Controlling external report:** `reviews/a2-dyn-v91-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `6cd33d53851905266893e5b42fbb7c75b7f1bea2` / `abce658e6c17f1cbcc0337ff5323c46808dce7cf`  
**Qualification status at report freeze:** no workflow run was discoverable for the response ref; referee-copy run `38256067445` was queued with no conclusion  
**Date:** 12 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, probability, information-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 92 is mathematically nontrivial and, at its stated topology, internally coherent subject to the inherited scalar, critical, and positive path-remainder inputs. The new manuscript makes one useful conceptual separation and derives several genuine downstream consequences:

1. it reactivates the already proved one-sided pointwise lower law and makes explicit that a physical denominator floor on `G>=d>0` does not require the missing pointwise upper estimate;
2. it converts unweakened critical weak convergence of the raw error into convergence of the bounded reciprocal error in every finite roof `L^p` norm;
3. under the retained positive path-remainder theorem, it proves finite-roof-norm convergence of the exact same-roof collision kernels in bounded-Lipschitz distance;
4. it obtains all finite posterior moments for the original critical-or-short-residence union on positive-reference roofs;
5. it proves stability under arbitrary moving measurable roof selections with fixed positive reference floor and fixed positive reference-mass floor; and
6. it proves both directions of relative-entropy convergence for the resulting one-dimensional roof marginals.

I found no decisive sign error, exponent error, normalization error, missing Jacobian in the diffusive window, illicit normalization of an arithmetic zero class, or unjustified claim of path-space total variation or path-space entropy in modules 217--219. The weak-to-strong real-variable lemma, the positive-measure mixture identities, the posterior powers, and the roof-marginal entropy estimates are mutually consistent.

The negative recommendation is nevertheless decisive for two reasons.

First, revision 92 does not solve the governing theorem retained by the paper. The unrestricted pointwise exact-label raw local limit remains open. The manuscript itself keeps

```text
original_critical_residence_source_charge_zero_proved = false
full_raw_return_LLT_proved = false
primary_referee_request_closed = false
```

and explicitly states that the upper essential-height charge has not been proved zero.

Second, the principal new arguments in revision 92 are downstream normalization consequences of previously established inputs. The one-sided lower law is historical module 108, not a new pointwise theorem. The path/scalar discrepancy comparison is inherited from the earlier positive path-remainder architecture. The moving-conditioning and entropy results are useful but largely real-variable and measure-normalization deductions once those strong inputs are granted. They do not supply the collision-uniform spike-persistence or superlevel geometry requested in the revision-91 report.

At the requested benchmark, a paper whose title, introduction, and source architecture remain organized around unrestricted pointwise raw inversion must prove the missing upper half. Revision 92 clarifies what already follows without it, but does not close it.

## 2. Frozen source, chronology, and source identity

Both reviewed revision-92 author refs resolve to

`f1288a14908a08197365b3f3d83a7e6d59e5a676`.

The repository tree at that commit is

`8af035016ba10d4536db4ebb79bf08a07f033b9f`.

The active article is

`papers/A2-DYN-v92-referee-response`.

The source manifest identifies revision 91 as the immediate baseline:

`5c7512a4341d8277101d9c0b609dc7d2cda1512a`,

with frozen paper tree

`5637513690e13d4abf1a46eedb568327648a0b1f`.

The revision-92 author commit has the controlling revision-91 review commit as parent. The complete revision-91 source is additionally snapshotted at

`papers/A2-DYN-v92-referee-response/provenance/v91-source`.

The active packet preserves 216 inherited core modules and adds exactly:

- `core/217_one_sided_pointwise_inversion.tex`;
- `core/218_positive_disintegration_and_posterior_stability.tex`;
- `core/219_moving_roof_conditioning_and_entropy.tex`.

Both distinct revision-88 variants remain separately preserved. The revision does not silently merge their incompatible modules or replace the weak-Lp lineage by the parallel optical-moment lineage.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v92-external-top4-review-2026-10-12/`.

No author manuscript, author revision branch, workflow, prior review, preserved variant, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The revision-92 workflow is

`.github/workflows/a2-dyn-v92-qualification.yml`.

At report freeze, the GitHub Actions branch query returned no workflow run for

`revision/a2-dyn-v92-referee-response-2026-10-12`.

The referee-copy branch had one run:

`38256067445`,

with status `queued` and `conclusion=null` at the reviewed SHA.

I therefore do not describe revision 92 as having completed fresh exact-SHA remote qualification on both author refs.

The declared validation contract is meaningful. A completed run is designed to verify:

- the frozen revision-91 paper tree;
- the complete revision-91 snapshot;
- the controlling revision-91 report blob;
- byte and mode preservation of all inherited sources;
- preservation of both revision-88 variants;
- normal and optimized finite-diagnostic agreement;
- native compilation of the focused article and full supplement;
- recorder coverage of all 219 core modules;
- stabilized references and warning gates; and
- PDF word geometry and selected renders.

These checks would establish source identity, finite algebraic consistency, and reproducible assembly. They would not certify the inherited continuum coarea identities, common disintegrations, four-record spectral theorem, positive path remainder, or the missing upper-spike exclusion theorem. The manuscript states this limitation correctly.

## 4. Scope of this audit

The complete source contains 219 core modules and a supplement exceeding seven hundred pages. I have not independently reconstructed every historical theorem.

The substantive review concentrates on:

1. the exact requests made in the revision-91 external report;
2. the historical positive scalar remainder and one-sided lower law as invoked in module 217;
3. the bounded weak-to-strong lemma and its endpoint logarithm;
4. the positive-reference denominator and reciprocal-density theorem;
5. the positive path-remainder input used in module 218;
6. the path/scalar discrepancy comparison;
7. the exact original-guard mixture and posterior interpretation;
8. the same-roof collision-kernel bounded-Lipschitz estimate;
9. the posterior exponent arithmetic for all finite `p`;
10. the moving roof-selection normalization in module 219;
11. the joint roof--path bounded-Lipschitz test class;
12. the two entropy inequalities and both directions of roof-marginal relative entropy;
13. preservation of exact labels, physical source, original guard, normalization, and arithmetic zero classes;
14. the distinction between lower pointwise control and upper essential-height control; and
15. the requested top-four completeness, novelty, and significance standard.

The inherited positive scalar remainder, unweakened critical weak theorem, original-union critical estimate, positive path remainder, common conditional kernels, and finite-peak reference bound are treated as source-pinned inputs. Their interfaces with the new deductions are audited here. This report does not convert those inherited inputs into independently verified theorems.

## 5. The governing pointwise assertion

The retained target remains the uniform pointwise raw local limit

```text
sup_{R, 1<=n<=m, k in Z^2}
esssup_{t in C_{m,R,n,k}(M)}
|m^2 p_{n,R}(k,m,t) - L_{m,R}(k_1,k_2,t,n)| -> 0.
```

Writing

```text
P = m^2 p,
G = L,
f = P-G,
```

revision 92 proves the negative-part statement

```text
[G-P]_+ -> 0
```

uniformly in essential supremum.

It does not prove

```text
[P-G]_+ -> 0
```

in essential supremum.

Thus the remaining obstruction is now cleanly one-sided, but it is still exactly the missing pointwise theorem. The new reciprocal, posterior, kernel, and entropy conclusions are compatible with fixed-height positive pulses on roof sets whose measures shrink to zero.

The example retained by the authors,

```text
G = 1,
P_j = 1 + 1_(0,delta_j),
delta_j -> 0,
```

has the pointwise lower law, all finite reciprocal conclusions, roof-marginal entropy convergence, and finite-norm kernel analogues, while

```text
||P_j-G||_infinity = 1.
```

This topology test is decisive: revision 92 does not bridge the final gap.

## 6. Audit of module 217: the historical one-sided lower law

### 6.1. Exact sign argument

For each fixed reconstruction band `B`, the retained scalar identity is

```text
P-G = b_B + e_B,

b_B >= 0,

limsup_m sup_{R,n,k} esssup |e_B|
    <= C_M B^(-1/192).
```

Therefore

```text
[G-P]_+ <= |e_B|.
```

Taking the collision limsup first and the reconstruction band to infinity last gives

```text
sup_{R,n,k} esssup [G-P]_+ -> 0.
```

This argument is correct. It is genuinely pointwise and does not use a false embedding from weak `L^(32/31)` into `L-infinity`.

The historical credit is also now accurate: this lower law is already Theorem `thm:v51-positive-error`, equation `eq:v51-lower-local-law`, in retained module 108. Revision 92 restates and exploits it; it does not newly discover it.

### 6.2. Positive-reference denominator

On

```text
D_m(d) = C(M) intersect {G>=d},
```

with fixed `d>0`, the lower law yields eventually

```text
P >= G-d_m >= d/2.
```

Hence

```text
[G/P-1]_+ <= 2 d_m/d.
```

The constants and quantifiers are correct. The fixed floor `d` is indispensable. The theorem is not uniform over all roofs with merely `G>0`, and no ratio is assigned on `G=0`.

This is a useful correction to an overly broad reading of the earlier downstream restriction: denominator existence on a fixed positive-reference class does not require the missing upper pointwise theorem.

It does not, however, provide a two-sided pointwise ratio theorem.

## 7. Audit of module 217: bounded weak-to-strong conversion

The manuscript uses the measurable-set norm

```text
N_q(u;J)
 = sup_{E subset J} |E|^(-1+1/q) int_E |u|.
```

If `0<=u<=H` and `N_q(u;J)<=A`, testing on `{u>lambda}` gives

```text
|{u>lambda}| <= min(L,(A/lambda)^q).
```

Integrating the distribution function yields:

- for `1<=p<q`,

```text
||u||_p
 <= (q/(q-p))^(1/p) A L^(1/p-1/q);
```

- for `p>q`,

```text
||u||_p
 <= (p/(p-q))^(1/p) A^(q/p) H^(1-q/p);
```

- and at `p=q`,

```text
||u||_q^q
 <= A^q (1+q log(H L^(1/q)/A)).
```

The constants and exponents are correct. In the supercritical case, the exact distribution integral contains a negative lower-end correction, so the printed upper bound is valid. At the endpoint, the logarithm is unavoidable at this level of information.

The consequence is also correct: bounded functions tending to zero in weak `L^q` converge strongly in every finite `L^p`, including `p>=q`.

This is an elementary real-variable lemma, not a new billiard estimate. Its role is nevertheless appropriate because the reciprocal and posterior variables are bounded even though the raw error is not.

## 8. Audit of module 217: reciprocal-density convergence

On `D_m(d)`, define

```text
r_m = |1-G/P|.
```

The denominator floor gives

```text
r_m <= 2|P-G|/d.
```

Moreover:

- if `P>=G`, then `r_m=1-G/P<=1`;
- if `P<G`, the one-sided lower law gives `r_m<=2d_m/d<=1` eventually.

Thus

```text
0<=r_m<=1
```

and

```text
N_Q(r_m;J)
 <= (2/d) N_Q((P-G)1_C(M);J),
Q=32/31.
```

Applying the bounded weak-to-strong lemma to the revision-91 unweakened critical weak convergence proves every finite local `L^p` limit. The same pointwise inequality in rescaled coordinates gives the complete central-window result in measure `dt/sqrt(m)`.

The proof is correct at its stated scope.

Importantly, it does not prove strong `L^Q` convergence for the unbounded raw error. The active status correctly leaves

`strong_critical_LQ_convergence_proved = false`.

## 9. Audit of module 218: path/scalar discrepancy comparison

Let

```text
mathbf P = P Q_t,
```

and let `G W_R` be the retained Gaussian bridge reference measure on the same roof. The positive path remainder input states, for fixed `B`,

```text
mathbf P - G W_R =mathbf b_B +mathbf E_B,

mathbf b_B >= 0,
||mathbf b_B||_(BL*) = b_B,
||mathbf E_B||_(BL*) <= eta_B.
```

Because the constant test belongs to the bounded-Lipschitz class,

```text
|P-G| <= ||mathbf P-GW_R||_(BL*).
```

Conversely,

```text
||mathbf P-GW_R||_(BL*)
 <= b_B+eta_B
 <= |P-G|+2 eta_B.
```

The second inequality follows from

```text
|P-G| = |b_B+mathbf E_B(1)| >= b_B-eta_B.
```

Therefore the nonnegative gap between the path numerator discrepancy and the scalar absolute discrepancy tends uniformly to zero after the legal outer limit.

This deduction is correct. It is, however, an additive restatement of the inherited positive path theorem, not a new construction of the path comparison.

Its critical-norm consequence follows because the uniform additive error has weak norm bounded by its height times the fixed window factor.

## 10. Audit of module 218: the exact original-guard mixture

The input includes the positive submeasure relation

```text
0 <=mathbf b_B <=mathbf P.
```

Hence

```text
mathbf A_B =mathbf P -mathbf b_B
```

is positive and has mass

```text
A_B = G +mathbf E_B(1).
```

On `G>=d`, after choosing `B` large and then `m` large,

```text
A_B >= d/2.
```

Normalizing the two positive restrictions gives the exact mixture

```text
Q_t
 = (1-beta_B) Q_good + beta_B Q_bad,

beta_B = b_B/P.
```

The good-kernel estimate

```text
d_BL(Q_good,W_R) <= 4 eta_B/d
```

follows from

```text
Q_good-W_R
 = (mathbf E_Bmathbf - E_B(1)W_R)/A_B.
```

The full mixture estimate

```text
d_BL(Q_t,W_R)
 <= 2 beta_B + 4 eta_B/d
```

uses only that the bounded-Lipschitz distance between probability measures is at most two in the stated convention.

Finally,

```text
beta_B
 = 1-G/P -mathbf E_B(1)/P,
```

so

```text
|beta_B-(1-G/P)| <= 2 eta_B/d.
```

These identities and constants are correct. The mixture uses the original guard and its physical complement; no transported surrogate source or new normalization is inserted.

## 11. Audit of module 218: same-roof collision kernels

Writing

```text
mathfrak d_m
 = ||mathbf P-GW_R||_(BL*),
```

one has

```text
P(Q_t-W_R)
 = (mathbf P-GW_R) + (G-P)W_R.
```

After division by `P`, the numerator comparison gives

```text
d_BL(Q_t,W_R)
 <= min(2, 2|1-G/P| + 2 rho_m/d),
```

where `rho_m` is the uniform path/scalar discrepancy gap and `rho_m->0`.

The factor two in front of the reciprocal error is correct: one copy comes from the path numerator and one from the scalar mass correction.

The reciprocal theorem then yields convergence in every finite local roof `L^p` norm and on the complete diffusive window.

The theorem correctly keeps the following distinctions:

- the bounded-Lipschitz supremum over path tests is already taken at each roof;
- the roof exceptional set is not selected separately for each path observable;
- the conclusion is not path-space total variation;
- the conclusion is not roof essential-supremum convergence;
- the conclusion is not an actual-return clock theorem; and
- the conclusion is restricted to the quantified positive-reference class.

Subject to the inherited positive path-remainder theorem and common-kernel measurability, the argument is correct.

## 12. Audit of module 218: posterior powers

For the original weighted exceptional union, the posterior mass is

```text
pi = H_(a,delta)^epsilon / P
```

on `D_m(d)` and zero outside. Since `H_(a,delta)^epsilon` is a positive restriction of the total source,

```text
0<=pi<=1.
```

It is dominated by

```text
min(1, 2 m^2 U_(a,delta)/d),
```

where `U_(a,delta)` is the unweighted original union. The revision-91 input gives, at

```text
a=h^(1/8),
delta=h^(1/4),
```

an ordered weak-critical bound

```text
N_Q(upper function)
 <= C h^(31/4096).
```

Applying the bounded weak-to-strong lemma yields:

- for `p<Q`,

```text
||pi||_p <= C h^(31/4096);
```

- for `p=Q`,

```text
||pi||_Q
 <= C h^(31/4096)(1+|log h|)^(1/Q);
```

- for `p>Q`,

```text
||pi||_p
 <= C h^(1/(128p)).
```

The last exponent is correct because

```text
(31/4096)(Q/p)
 = (31/4096)(32/(31p))
 = 1/(128p).
```

The same unweighted upper selector dominates every smaller cutoff pair and every original weight without requiring monotonicity of `W^epsilon` in `epsilon`.

No `p=infinity` conclusion follows, and none is claimed.

## 13. Audit of module 219: moving roof selections

The local window has measure `L`; the complete central window uses `dt/sqrt(m)` and has uniformly bounded measure. Let

```text
E_m subset K_m intersect {G>=d},

H_E = int_(E_m) G d lambda_m >= zeta>0.
```

The actual and reference masses are

```text
F_E = int_(E_m) P d lambda_m,
H_E = int_(E_m) G d lambda_m.
```

Because the integrated scalar error over the ambient window tends uniformly to zero,

```text
|F_E-H_E| <= a_m -> 0,
```

uniformly over arbitrary measurable `E_m`. Therefore `F_E>=zeta/2` eventually and `F_E/H_E->1` uniformly.

For joint roof--path laws, subtracting the unnormalized finite measures before normalization gives the test bound

```text
(v_m+|F_E-H_E|)/F_E
 <= (2/zeta)(v_m+a_m).
```

Here the path section of the test is in the unit bounded-Lipschitz class, while no regularity in the roof variable is imposed. The common-kernel and countable-norming-class assumptions make the integrated discrepancy measurable.

The scalar version gives total variation convergence of the roof marginals. The result is uniform over all moving sets satisfying the two fixed floors.

This is correct. The mass floor `zeta` cannot be removed: conditioning on reference masses collapsing to zero could amplify errors arbitrarily. The active status correctly records that uniform conditioning on arbitrarily small reference masses is not claimed.

The joint conclusion is an integral probability metric with arbitrary Borel roof dependence and bounded-Lipschitz path sections. It is not total variation on path space.

## 14. Audit of module 219: two-sided roof entropy

### 14.1. Elementary entropy inequalities

For `1<p<2`, the manuscript uses

```text
x log x - x + 1 <= C_p |x-1|^p,
```

for `x>=0`, and

```text
x-1-log x <= C_p |x-1|^p,
```

for `x>=1/3`.

These inequalities are correct.

Near `x=1`, both left sides are quadratic and are dominated by `|x-1|^p` because `p<2`. On bounded sets away from the singular endpoint the ratios are continuous. For large `x`, the first grows like `x log x` and is dominated by `x^p` for `p>1`; the second grows linearly and is also dominated by `x^p`.

The lower cutoff in the second inequality is necessary because reverse entropy is singular as `x` approaches zero.

### 14.2. Likelihood control

The roof likelihood is

```text
R_E
 = (P/G)(H_E/F_E).
```

On `E_m subset {G>=d}`:

```text
P/G >= 1-d_m/d,
```

and

```text
H_E/F_E -> 1
```

uniformly. Hence `R_E>=1/3` eventually, with no upper bound imposed.

Moreover,

```text
|R_E-1|
 <= (2/d)|P-G| + (2/zeta)a_m.
```

Using `G<=D_M`, `H_E>=zeta`, the bounded ambient window measure, and Hölder to control `a_m^p`, one obtains

```text
int |R_E-1|^p dG_E
 <= C int |P-G|^p d lambda_m.
```

Choosing any fixed

```text
1<p<Q=32/31
```

is possible. Unweakened weak `L^Q` convergence implies strong `L^p` convergence on the fixed local or rescaled window, so the right side tends to zero.

### 14.3. Both entropy directions

Since

```text
int R_E dG_E = 1,
```

one may write

```text
KL(P_E^roof || G_E^roof)
 = int (R_E log R_E - R_E + 1) dG_E,
```

and

```text
KL(G_E^roof || P_E^roof)
 = int (R_E - 1 - log R_E) dG_E.
```

The two elementary inequalities therefore prove both entropy limits.

The proof is correct at the stated roof-marginal level. It neither assumes nor proves an upper essential-likelihood bound. It cannot be transferred to path space because the actual collision-path law and Gaussian bridge reference may be singular there.

## 15. Response to the revision-91 report

Revision 92 addresses some secondary points accurately but does not answer the primary mathematical request.

### 15.1. Pointwise lower half and denominator existence

**Clarified and correctly credited.** The historical lower law is made explicit, and a fixed positive-reference denominator floor is separated from the unproved upper pointwise estimate.

### 15.2. Bounded reciprocal topology

**Addressed.** The bounded reciprocal variable converges in every finite roof `L^p` norm, including at and above the critical exponent. This does not upgrade the raw error.

### 15.3. Same-roof conditional kernels

**Addressed in finite roof norms, conditional on the inherited positive path remainder.** The topology is bounded-Lipschitz on path space and finite `L^p` in the roof, not uniform roof convergence or path total variation.

### 15.4. Moving positive-mass conditioning

**Addressed.** Arbitrary measurable moving roof selections are stable when both a pointwise reference floor and a total reference-mass floor are fixed.

### 15.5. Roof-marginal entropy

**Addressed.** Both entropy directions are proved without an upper likelihood bound, but only for one-dimensional roof marginals.

### 15.6. Quantitative upper-spike persistence

**Not addressed.** No theorem forces a high positive value of `P-G`, or of the original exceptional source, to persist on a roof interval of collision-uniform positive width or capacity.

### 15.7. Genuinely pointwise maximal closure

**Not addressed.** The revision adds normalization consequences after weak convergence. It does not strengthen the revision-91 weak maximal theorem into a pointwise estimate with a prescribed non-collapsing scale.

### 15.8. Above-threshold regularity with vanishing norm

**Not addressed.** No new Sobolev, Besov, BV, oscillation, or derivative estimate reaches a space embedded into `L-infinity` with a norm tending to zero.

### 15.9. Direct superlevel geometry

**Not addressed.** The maximal-segment geometry, radial monotonicity, angular density, endpoint classification, and prefix structure are not used to obtain a lower bound on the width of high upper-error components.

### 15.10. Independent specialist verification

**Not supplied.** The manuscript preserves sources and diagnostics but does not provide an independent reconstruction of the load-bearing scalar, spectral, coarea, or path-remainder inputs.

Thus revision 92 is an accurate downstream clarification, not a closure of the revision-91 referee request.

## 16. Exact theorem-bearing contribution of revision 92

Subject to the inherited inputs, I regard the following as the genuine contribution of this revision:

1. an explicit separation of the historical one-sided pointwise lower law from the missing upper pointwise theorem;
2. a uniform denominator floor on each fixed positive-reference class;
3. a bounded weak-critical-to-all-finite-`L^p` principle applied to the reciprocal density;
4. an additive identification of path numerator discrepancy with scalar absolute discrepancy under the positive path remainder;
5. an exact original-guard posterior mixture with quantitative good-kernel control;
6. finite-roof-norm convergence of exact same-roof collision kernels in bounded-Lipschitz distance;
7. all-finite posterior moment bounds for the original exceptional union;
8. stability under arbitrary moving measurable roof selections with fixed positive floors; and
9. two-sided relative-entropy convergence of the selected roof marginals.

Items 2--9 are useful consequences. Their novelty, however, is downstream and conditional. The primary billiard-local-limit obstruction is not advanced beyond the revision-91 upper-spike formulation.

The historical lower law and path comparison must continue to be credited as inherited results rather than revision-92 discoveries.

## 17. Claims that remain unproved

The manuscript correctly leaves unproved:

- zero essential-height charge for the original exceptional source;
- the upper pointwise half `[P-G]_+ -> 0`;
- the unrestricted pointwise exact-label raw local limit theorem;
- strong raw `L^(32/31)` convergence;
- a finite-norm implication to essential height;
- a uniform roof bounded-Lipschitz kernel theorem;
- path-space total variation convergence;
- path-space relative entropy convergence;
- uniform conditioning on reference masses tending to zero;
- a forward essential-likelihood theorem;
- unrestricted same-roof ratios on all merely positive reference values;
- normalization of arithmetic zero classes;
- an unnormalized growing-window theorem;
- independent human specialist approval; and
- a formal proof certificate.

The active status files represent these boundaries accurately.

## 18. What a successful next revision must prove

The next revision should return to the only remaining scalar obstruction. Further bounded normalizations, posterior moments, entropy inequalities, or finite-`p` kernel consequences will not close the pointwise theorem.

### 18.1. Quantitative persistence of upper excess

Prove that if

```text
P(t)-G(t) >= lambda
```

at a Lebesgue point, then the positive excess or the corresponding original exceptional source remains above a fixed fraction of `lambda` on a roof set whose measure is bounded below by an explicit function of `lambda`, uniformly in collision count, exact labels, billiard radius, and legal cofinal cutoffs.

Combined with the established critical-norm decay, such a theorem would force the upper essential height to vanish.

### 18.2. A prescribed-scale pointwise maximal inequality

A sufficient estimate would bound the source value by an average over a radius that cannot collapse arbitrarily with collision count, plus a remainder tending uniformly to zero in the legal outer limit.

The radius must be tied quantitatively to physical geometry, source height, or a collision-uniform regularity modulus. Another weak-type superlevel-measure estimate is not enough.

### 18.3. Source-specific regularity above the one-dimensional embedding threshold

A Sobolev, Besov, bounded-variation, or oscillation route must control the positive upper source in a topology embedded into `L-infinity`, and the relevant norm must tend to zero. A bounded norm, or a vanishing norm below the embedding threshold, still permits collapsing fixed-height pulses.

The bounded reciprocal is not suitable for this step because dividing by `P` suppresses the amplitude information of a large positive spike.

### 18.4. Direct geometry of superlevel components

The existing maximal-segment and endpoint architecture should be used to show that high source values cannot live on arbitrarily short roof components. Relevant structures may include:

- monotone radial growth along the exact field;
- the full angular density and its physical derivative;
- two-sided endpoint classification;
- complete residence bands;
- prefix representations of exact events; and
- collision-uniform control of the number and geometry of superlevel components.

The output must be a lower-width or lower-capacity theorem, not only an integrated crossing estimate.

### 18.5. Preserve the exact limit order

Any new pointwise mechanism must continue to respect:

1. finite-count formation of the positive physical source;
2. fixed auxiliary spectral bands before collision limits;
3. complete physical scale summation before limsup where required;
4. auxiliary-band enlargement only after the collision limit;
5. cofinal cutoffs fixed before each collision limit; and
6. the reconstruction band as the outermost limit.

A roof scale or frequency band chosen directly as a function of collision count would not prove the stated theorem.

### 18.6. Promote downstream pointwise laws only after scalar closure

Revision 92 shows that finite-roof-norm conditional kernels and roof entropy already follow on fixed positive-reference classes. The next revision should not relabel these as uniform path inversion.

Only after the scalar upper essential-height charge is proved zero should the manuscript consider:

- uniform roof kernel convergence;
- forward essential-likelihood convergence;
- unrestricted same-roof ratios; or
- actual-return point-conditioned laws.

### 18.7. Independent specialist verification

A submission of this breadth needs independent audits of the inherited positive scalar remainder, four-record spectral theorem, physical coarea/disintegration, and positive path remainder. Source preservation and finite diagnostics are not substitutes for specialist reconstruction.

## 19. Exposition and architecture

The focused article is concise and clearer than the full archive, but several editorial points remain important.

1. The abstract should state even more prominently that the one-sided pointwise law is historical and that the new results are conditional consequences on `G>=d`.
2. The phrase "unconditional normalization theorem" should be avoided unless immediately qualified by the fixed reference and reference-mass floors and the inherited path input.
3. The distinction between raw-error topology, reciprocal topology, roof topology, and path topology should remain explicit in every theorem summary.
4. The joint moving-set metric should be named as an integral probability metric with arbitrary Borel roof dependence and bounded-Lipschitz path sections, not informally called total variation.
5. The reverse entropy theorem should continue to display where the lower likelihood floor enters.
6. Historical module 108 and the inherited path comparison should be cited in the theorem statements, not only in the proof ledger.
7. The response-branch qualification asymmetry should be resolved before any reproducibility claim is made.
8. Archive-facing provenance material should remain in supplementary documentation rather than carrying the main mathematical narrative.

These changes would improve precision but would not alter the recommendation.

## 20. Significance and venue assessment

Revision 92 contains a clean positive-reference conditioning package. The separation between denominator existence and upper pointwise inversion is conceptually useful. The moving roof-selection theorem and two-sided roof-marginal entropy result may also be of interest in a specialized treatment of conditional local limits.

However, most of the new mathematics is an application of:

- a historical one-sided lower law;
- the revision-91 unweakened critical weak theorem;
- an inherited positive path-remainder theorem; and
- elementary bounded-function and entropy inequalities.

It does not add the new billiard geometry or regularity mechanism demanded by the remaining pointwise problem. Consequently the revision-92 increment, taken by itself, does not meet the novelty and central-theorem threshold of the requested four journals.

If independently verified and reorganized around positive-reference conditional limits rather than unrestricted pointwise inversion, some of these results could support a specialized paper or a downstream companion paper. The current manuscript, however, retains the unrestricted pointwise raw theorem as its organizing objective and retains its decisive upper charge as open.

## 21. Final recommendation

Revision 92 is careful about scope and contains several correct deductions:

- the historical lower law gives a physical denominator on `G>=d`;
- the bounded reciprocal converges in every finite roof norm;
- the positive path remainder yields finite-norm same-roof kernel stability;
- the original exceptional union has quantitative finite posterior moments;
- moving positive-mass roof conditioning is stable; and
- both roof-marginal entropy directions converge.

I found no decisive internal error in modules 217--219 at their stated topology, conditional on the inherited inputs.

Nevertheless, revision 92 does not prove the manuscript's governing pointwise theorem and does not answer the revision-91 demand for collision-uniform upper-spike persistence or an equivalent source-specific `L-infinity` mechanism. The main obstruction is unchanged, and the new contribution is predominantly downstream normalization rather than closure of the primary billiard problem.

**I therefore recommend rejection in the present form at the requested Annals/Acta/Inventiones/JAMS benchmark.**

This recommendation does not deny the value of the positive-reference conditioning results. It reflects the mismatch between the theorem the manuscript continues to organize around and the theorem it currently proves, together with the limited top-four novelty of the revision-92 increment once its inherited inputs are separated from its new deductions.
