# External top-four referee report on A2-DYN revision 56

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v56-referee-response-2026-10-09`, `revision/a2-dyn-v56-referee-copy-2026-10-09`  
**Reviewed commit:** `4292877a5100c4c22975d9d563a1c54793139db4`  
**Reviewed repository tree:** `b9946833417b83fb66e3d6dbeb57e3756b7e9041`  
**Ordinary source payload tree:** `53ef371e695c2930a8d67433292eaeb76ddb00c8`  
**Active manuscript directory:** `papers/A2-DYN-v56-referee-response`  
**Active mathematical source:** one hundred twenty numbered core modules; revision 56 retains all one hundred eighteen revision-55 modules and adds modules 119--120  
**Frozen revision-55 author baseline:** `32866de446dd83c3036c04544ce4da66b019a990`  
**Frozen revision-55 complete paper tree:** `752682f2cc874aafa60c2e59581cc0e29ddccd89`  
**Controlling external report:** `reviews/a2-dyn-v55-external-top4-review-2026-10-09/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `38cfd6796d9146b9dcf30fb2f614731801edb53c` / `304f5b638c0cb2d61d934bbb864d48ea43039f90`  
**Date:** 9 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 56 is a genuine theorem-bearing advance over revision 55. Its contribution is not another fixed-window consequence of the local `L^1` theorem and not a rephrasing of the weak `L^{145/144}` endpoint. It proves that the two remaining positive physical sources—incidence and clearance—admit one common uncentered roof maximal envelope. Outside a quantitatively controlled open set, this envelope simultaneously controls

- the almost-everywhere height of each positive component;
- every average over every positive-length roof interval containing the same good anchor;
- every bounded source insertion through one common disintegration;
- the scalar raw error;
- the bounded-Lipschitz-dual path-valued raw error;
- exact conditional roof laws on arbitrarily short anchored intervals;
- the same-roof collision bridge at good roofs;
- and, through the inherited integrated clock transfer, both the collision and actual-return bridges on a common qualitative good set.

At a fixed reconstruction band `B`, the paper chooses

\[
\varepsilon(B)=A_0B^{-1/12},
\qquad
\lambda_B=B^{-1/384}.
\]

The positive physical remainder has local mass of order

\[
\varepsilon(B)^{1/16}=B^{-1/192}.
\]

The maximal weak `(1,1)` estimate therefore gives an exceptional roof set of length

\[
O(B^{-1/384}).
\]

The positive raw-error representation then improves the original-source mass of this same set to the same ordered exponent after the collision-count limsup. On the complement, every anchored interval average of the scalar and collision-path raw errors is `O(B^{-1/384})` in the ordered limit, with no lower restriction on the interval length.

I audited the new modules

- `core/119_maximal_physical_layers.tex`;
- `core/120_resolution_uniform_roof_laws.tex`;

and their use in the revised front matter. I also checked the precise inherited inputs from modules 104--118, the weak endpoint conversion, the positive raw-error identity, the source normalization, the path-measure normalization, the positive-part arithmetic reference, the common disintegration statements, the actual-return transfer, and the exact-source qualification records.

I found no decisive counterexample, exponent error, normalization error, Fourier-sign error, collision/return endpoint mismatch, false arithmetic cancellation, or invalid substitution of a collision-count-dependent frequency band into a fixed-band spectral theorem in the new text.

The new real-variable chain is internally coherent. In particular:

1. the maximal covering lemma is proved at finite count and before any interval is selected;
2. the weak `L^{145/144}` source-weight exponent is correctly converted to `1/145`;
3. the same open set controls both positive physical components and every bounded insertion;
4. the sharper `B^{-1/384}` source-mass estimate uses the exact positive raw-error representation and is not inferred from weak integrability alone;
5. the path-valued estimate uses a common positive path remainder and one countable norming class;
6. replacing the signed finite-count kernel `G` by `G_+` in posterior normalization does not increase the positive path-measure discrepancy;
7. the exact denominator and total-variation constants are consistent;
8. the pointwise likelihood conclusion retains a pointwise arithmetic floor, not merely positive integrated mass;
9. the actual-return theorem uses its own qualitative integrated error and does not inherit an unsupported band exponent;
10. the manuscript repeatedly states that a small exceptional set need not be empty.

The negative recommendation is nevertheless forced by the endpoint which still governs the title and the raw-inversion architecture. Revision 56 does **not** prove

\[
\sup_{R,n,k}
\operatorname*{ess\,sup}_{u\,\mathrm{central}}
\left|m^2p_{n,R}(k,m,u)
      -\mathcal L_{m,R}(k_1,k_2,u,n)\right|
\longrightarrow0.
\]

The incidence or clearance density may still form an arbitrarily high, arbitrarily narrow positive spike entirely inside the exceptional set. The new theorem localizes every such spike simultaneously across all roof resolutions and proves that both its Lebesgue size and its original-source probability are small. It does not bound the spike's essential height.

Consequently the following remain unproved:

- central-scale essential-height smallness of the incidence source;
- central-scale essential-height smallness of the clearance source;
- the complete two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof uniform collision and return bridges;
- unrestricted forward essential-likelihood convergence;
- the strong endpoint `L^{145/144}` statement;
- the unmodulated specialization unless the concrete section residue criterion is separately verified;
- and independent specialist certification of the inherited continuum chain.

The maximal argument is useful and exact in its scope, but it is classical real-variable analysis applied to an already constructed model-specific source. At the requested benchmark, a manuscript of this size, specificity and title should either close the positive-height obstruction or extract a substantially broader theorem whose independent significance no longer depends on that unfinished endpoint. Revision 56 does neither yet.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`4292877a5100c4c22975d9d563a1c54793139db4`.

The repository tree at that commit is

`b9946833417b83fb66e3d6dbeb57e3756b7e9041`.

The active article is

`papers/A2-DYN-v56-referee-response`.

The ordinary source payload tree recorded in the manifest is

`53ef371e695c2930a8d67433292eaeb76ddb00c8`.

The author commit has the revision-55 external-report commit

`38cfd6796d9146b9dcf30fb2f614731801edb53c`

as its parent. The chronology is therefore correct: revision 56 begins from the frozen external assessment rather than modifying the previously reviewed revision-55 author source in place.

The source manifest records:

- all one hundred eighteen inherited core modules retained byte-for-byte;
- all one hundred fifty-five inherited Python files retained byte-for-byte;
- the bibliography and compiled appendices retained;
- every inherited mathematical label retained;
- two new modules, 119 and 120;
- `maximal_boundary_localization_proved: true`;
- `all_anchored_interval_resolutions_proved: true`;
- `ordered_exceptional_length_exponent: 1/384`;
- `ordered_exceptional_source_exponent: 1/384`;
- `good_roof_likelihood_proved: true`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`;
- `pointwise_roof_conditioned_bridge_proved: false`;
- `arithmetic_factor_identically_one_proved: false`;
- and `independent_human_review: false`.

The preservation strategy is consistent with the stated revision process. The former front matter and status documents are archived under provenance, while the inherited mathematical modules remain present and compiled. The new article does not remove the old pointwise target or replace the actual first-return record by a different observable.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v56-external-top4-review-2026-10-09/`.

No author manuscript source, prior review, workflow, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-source qualification workflows completed successfully on both reviewed author refs:

- response branch run `37903942132`;
- referee-copy branch run `37903952642`.

The runs bind the build and finite diagnostics to the exact reviewed SHA. According to the validation record, the verifier checks

- the frozen revision-55 paper tree;
- the controlling revision-55 report blob;
- all older frozen reports required by the source archive;
- inherited core, script, bibliography and appendix byte identity;
- every compiled core and mathematical label;
- the ordinary-source Merkle identity;
- the read-only workflow hash;
- agreement of normal and optimized finite diagnostics;
- native TeX compilation;
- and theorem-label-based rendering of the new proof pages.

The new finite checks cover interval-cover triples, rational exponents, simultaneous anchored averages, exact conditional denominators, total-variation factors, two-point path inequalities and good-anchor likelihood normalizations. Negative controls retain narrow spikes and zero arithmetic classes as counterexamples to overclaiming.

These are useful source, algebra and bookkeeping checks. They do not certify

- the inherited physical thin-layer multiplier;
- the all-depth first-physical-defect source decomposition;
- the complete occupation-torus spectral theory;
- the moving spectral branches;
- the protected flow-box and critical-collar geometry;
- the path-valued positive raw-error representation;
- the actual-return clock transfer;
- or the missing incidence and clearance essential-height estimates.

The manuscript and its validation files state this limitation accurately.

## 4. Scope of this review

I did not attempt to re-prove all one hundred twenty core modules. The substantive audit concentrates on the chain that can alter the revision-55 assessment:

1. the definition and measurability of the uncentered roof maximal function;
2. the finite greedy interval cover;
3. the weak `(1,1)` constant and weak-`L^p` improvement;
4. interpolation of maximal functions from first mass and a weak endpoint;
5. conversion of a small roof set to small original-source mass;
6. the common exceptional set for incidence and clearance;
7. the use of one common disintegration for bounded insertions;
8. the exact exponent calculations `1/145`, `1/192` and `1/384`;
9. the sharper ordered source estimate from `P=G+V+e`;
10. simultaneous control of every interval containing a good anchor;
11. the path-valued positive remainder and bounded-Lipschitz dual norm;
12. replacement of signed `G` by `G_+` in conditional posteriors;
13. exact denominator, total-variation and conditional-mean constants;
14. pointwise good-roof bridge and likelihood bounds;
15. probability of the common exceptional set under both true and reference roof laws;
16. the qualitative diagonal in the reconstruction band;
17. maximal transfer to the actual-return bridge;
18. the distinction between deterministic families of intervals and adaptive selection events;
19. source preservation and qualification evidence;
20. the unchanged positive-height endpoint.

The inherited revision-55 and earlier continuum chain is treated as a source-pinned baseline, not as independently certified mathematics.

## 5. The interval maximal lemma

For a nonnegative integrable function `f` supported on a mother interval `I`, the manuscript defines

\[
\mathcal M_I f(u)
 =\sup_{J\ni u}\frac1{|J|}\int_J\mathbf 1_I(v)f(v)\,dv,
\]

where `J` ranges over all bounded positive-length intervals in the real line.

This is the appropriate object for the claimed simultaneous conclusion. It is not a maximal function over a preselected sequence of interval lengths. A good anchor therefore controls every subinterval of the mother interval which contains that anchor, including one-sided intervals and intervals whose lengths depend on the collision count.

The proof of openness of

\[
O_\lambda=\{\mathcal M_I f>\lambda\}
\]

is standard and correct. A witnessing interval with average strictly larger than `lambda` can be enlarged slightly while preserving the strict inequality. These enlarged intervals form an open cover.

For a compact subset of `O_lambda`, the proof selects an interval of greatest length, deletes all intervals which meet it and repeats. The selected intervals are disjoint. Every deleted interval has length no greater than its selected parent and meets that parent, so it is contained in the concentric triple of the selected interval. This gives

\[
|O_\lambda|
 \le \frac3\lambda\int_I f.
\]

The finite selection and inner-regularity passage are legitimate. The numerical constant three is not important, but the proof records it consistently.

The stronger weak-`L^p` estimate is obtained by splitting

\[
f=f\mathbf 1_{\{f\le\lambda/2\}}
  +f\mathbf 1_{\{f>\lambda/2\}}.
\]

The maximal function of the first term is at most `lambda/2`. The tail assumption

\[
|\{f>L\}|\le D L^{-p}
\]

therefore gives

\[
\int_{\{f>\lambda/2\}}f
 \le C_pD\lambda^{1-p},
\]

and the weak `(1,1)` estimate applied to the second term gives

\[
|O_\lambda|\le C_pD\lambda^{-p}.
\]

I find no error in this truncation argument.

Finally, integrating the minimum of

\[
3\delta/\lambda
\quad\text{and}\quad
C_pD\lambda^{-p},
\qquad
\delta=\int_I f,
\]

in the distribution formula gives

\[
\int_{\mathbb R}(\mathcal M_I f)^q
 \le C_{p,q}
 D^{(q-1)/(p-1)}
 \delta^{(p-q)/(p-1)},
 \qquad 1<q<p.
\]

The crossing scale and the exponents are correct. The integral near zero is finite precisely because `q>1`; the manuscript does not claim a global strong `L^1` estimate for the maximal function.

This lemma is classical rather than novel, but its explicit proof is useful because the later quantifiers depend on applying it before selecting an interval resolution.

## 6. Source-weight conversion

The first source-weight estimate begins with a nonnegative density `P` satisfying

\[
|\{P>L\}|\le D L^{-p}.
\]

For a measurable roof set `E`, integrating

\[
\min\{|E|,DL^{-p}\}
\]

and splitting at

\[
L=(D/|E|)^{1/p}
\]

gives

\[
\int_EP
 \le \frac p{p-1}D^{1/p}|E|^{1-1/p}.
\]

The constant and exponent are correct.

At the manuscript's endpoint

\[
p_c=\frac{145}{144},
\]

one has

\[
1-\frac1{p_c}=\frac1{145}.
\]

This is the origin of the finite-count exceptional-source exponent. The paper does not confuse it with the sharper ordered exponent derived later.

The second source-weight estimate is genuinely different. If

\[
P=G+f+e,
\qquad f\ge0,
\qquad \|G\|_\infty\le C_G,
\qquad \|e\|_\infty\le\eta,
\]

then

\[
\int_EP
 \le (C_G+\eta)|E|+\int_If.
\]

This uses the bounded controlled part and the exact positive remainder. It is not a consequence of the weak endpoint. The manuscript maintains that distinction, and this distinction is essential for the later `B^{-1/384}` original-source bound.

## 7. The finite-count physical exceptional set

The new physical densities are

\[
V_{\varepsilon,\mathrm{inc}}
 =m^2b^{\varepsilon,\mathrm{inc},1}_{n,k,m,R},
\qquad
V_{\varepsilon,\mathrm{clr}}
 =m^2b^{\varepsilon,\mathrm{clr},1}_{n,k,m,R},
\]

and

\[
V_\varepsilon
 =V_{\varepsilon,\mathrm{inc}}
  +V_{\varepsilon,\mathrm{clr}}.
\]

All three are nonnegative and bounded above by the complete normalized density

\[
P=m^2p_{n,R}(k,m,\cdot).
\]

The theorem defines one set

\[
O_{\varepsilon,\lambda}
 =\{\mathcal M_IV_\varepsilon>\lambda\}.
\]

This is the right choice for simultaneous control. Separate incidence and clearance sets would lose the statement that one anchor works for both physical defects and every bounded insertion.

The inherited finite-count thin-source estimate gives

\[
\int_IV_\varepsilon
 \le C(1+h)\varepsilon^{1/16}.
\]

The inherited weak endpoint for `P` also applies to `V_epsilon` because

\[
0\le V_\varepsilon\le P.
\]

Applying the two maximal estimates gives

\[
|O_{\varepsilon,\lambda}|
 \le C(1+h)
 \min\left\{
       \frac{\varepsilon^{1/16}}\lambda,
       \lambda^{-145/144}
      \right\}.
\]

This formula is correct. For the later band choice, the first term is the useful one; the weak-endpoint term is included for the finite-count theorem and for maximal `L^q` interpolation.

Applying the source-weight lemma to `P` and this set yields

\[
\int_{I\cap O_{\varepsilon,\lambda}}P
 \le C(1+h)
 \min\left\{1,
   \left(\frac{\varepsilon^{1/16}}\lambda\right)^{1/145}
 \right\}.
\]

The factor `(1+h)` is consistent: the powers of the weak endpoint constant and the set length add to one. The alternative bound by one uses the uniform local first moment of `P`.

By Lebesgue differentiation,

\[
V_\varepsilon(u)\le\mathcal M_IV_\varepsilon(u)
\]

for almost every `u` in the mother interval. Thus, outside `O`, both positive physical components have height at most `lambda` almost everywhere. For every such good anchor and every positive-length subinterval `J` of `I` containing it,

\[
\frac1{|J|}\int_JV_{\varepsilon,j}\le\lambda.
\]

This is a true all-resolution statement. It does not arise from differentiating a fixed-window asymptotic theorem.

The maximal `L^q` estimate is also consistent. With

\[
p_c-1=\frac1{144},
\]

one obtains

\[
\frac{1}{16}\frac{p_c-q}{p_c-1}
 =9(p_c-q).
\]

Hence

\[
\int(\mathcal M_IV_\varepsilon)^q
 \le C_q(1+h)\varepsilon^{9(p_c-q)},
 \qquad 1<q<p_c.
\]

The power of `(1+h)` is again one because the interpolation exponents sum to one.

## 8. Common versions and bounded insertions

The theorem claims that one exceptional set works for every bounded source insertion. This requires more than saying that each inserted density is individually dominated almost everywhere, because separately selected density versions could have insertion-dependent null sets.

The manuscript addresses this point by fixing a regular disintegration of the finite positive physical source over the roof and defining every bounded insertion through that one kernel. In that common version,

\[
|V^w_{\varepsilon,j}(u)|
 \le M V_{\varepsilon,j}(u),
 \qquad |w|\le M,
\]

for the same almost-everywhere roof set.

This is the correct measure-theoretic formulation. Its validity remains contingent on the inherited construction of the positive source and the common disintegration, but the new maximal argument does not introduce an uncountable union of exceptional null sets.

The final article should keep this common-version statement near every theorem that quantifies over roof-dependent source or path tests. It is easy for a reader to misread the result as a separate-version assertion.

## 9. The ordered reconstruction-band localization

For a fixed large reconstruction band, the manuscript sets

\[
\varepsilon(B)=A_0B^{-1/12}
\]

and

\[
\lambda_B=B^{-1/384}.
\]

The inherited positive-error theorem gives

\[
\limsup_{m\to\infty}
\eta_{B,m}
 \le CB^{-1/192},
\]

where

\[
\eta_{B,m}
 =\sup_{R,n,k}
 \|P-G-V_B\|_\infty.
\]

The exponent ledger is correct:

\[
\varepsilon(B)^{1/16}=B^{-1/192},
\]

and therefore

\[
\frac{\varepsilon(B)^{1/16}}{\lambda_B}
 =B^{-1/384}.
\]

The maximal weak `(1,1)` estimate gives the finite bound

\[
|O_{B,m,R}^{n,k,I}|
 \le C(1+h)B^{-1/384}
\]

uniformly in every collision count, radius and exact label.

For the original-source mass, the paper does not use only the weak endpoint, which would produce the much weaker power `1/145` of this length. It uses the exact representation

\[
P=G+V_B+e_B,
\qquad
\|e_B\|_\infty\le\eta_{B,m},
\]

and the uniform boundedness of `G`. This gives the finite estimate

\[
\int_{I\cap O}P
 \le C(1+h)
 \left\{(C_G+\eta_{B,m})B^{-1/384}
           +B^{-1/192}\right\}.
\]

Taking the collision limsup at fixed `B` yields

\[
\limsup_m\sup_{R,n,k,t}
\int_{I\cap O}P
 \le C(1+h)B^{-1/384}.
\]

This use of the positive representation is legitimate and is mathematically stronger than the finite weak-endpoint conversion.

At a good anchor,

\[
|P-G|\le V_B+\eta_{B,m}.
\]

Averaging over every surrounding subinterval and using the maximal bound gives

\[
\sup_{J\subset I:\,u\in J}
\frac1{|J|}\int_J|P-G|
 \le \lambda_B+\eta_{B,m}.
\]

Lebesgue differentiation gives the analogous almost-everywhere pointwise estimate on the same complement.

The order of limits is correct:

1. fix `B`;
2. use the finite maximal inequality for every `m`;
3. take `m` to infinity in the fixed-band discrepancy;
4. only then let `B` tend to infinity.

No spectral estimate is evaluated at a band chosen as an explicit function of `m`.

## 10. Meaning and limitation of the exceptional set

The new set has three important strengths.

First, it is chosen before an interval resolution is selected.

Second, it is chosen from the sum of the two positive physical sources, so it controls incidence and clearance simultaneously.

Third, after the collision limsup its original-source probability has the same `B^{-1/384}` order as its Lebesgue length.

It nevertheless has three equally important limitations.

First, it depends on the radius, exact labels, collision count and mother interval.

Second, the theorem controls only anchors outside the set; it does not provide a deterministic exceptional set independent of the target family.

Third, the set may contain a positive spike of arbitrarily large essential height.

The manuscript states all three limitations. A small open set cannot be replaced by the empty set, and vanishing probability cannot be replaced by uniform pointwise convergence.

## 11. The path-valued all-resolution theorem

Let `bold P(u)` be the positive collision-path measure at roof `u`, `bold b_B(u)` the positive physical path remainder and `W_R` the Gaussian bridge law. Their masses are `P(u)` and `V_B(u)`.

The inherited path positive-error theorem gives

\[
\eta^{\rm path}_{B,m}
 =\sup_{R,n,k}
  \operatorname*{ess\,sup}_u
 \|\mathbf P(u)-G(u)\mathsf W_R-\mathbf b_B(u)\|_{\mathrm{BL}^*}
\]

with

\[
\limsup_m\eta^{\rm path}_{B,m}\le CB^{-1/192}.
\]

For a positive finite path measure, the bounded-Lipschitz dual norm equals its mass because the constant function one belongs to the unit class. Hence

\[
\|\mathbf b_B(u)\|_{\mathrm{BL}^*}=V_B(u).
\]

It follows that

\[
\|\mathbf P(u)-G(u)\mathsf W_R\|_{\mathrm{BL}^*}
 \le V_B(u)+\eta^{\rm path}_{B,m}.
\]

The same scalar physical maximal set therefore controls the path-valued error. Outside it, every anchored interval average is bounded by

\[
r_{B,m}=\lambda_B+\eta^{\rm path}_{B,m},
\]

and

\[
\limsup_m r_{B,m}\le CB^{-1/384}.
\]

This is a clean use of a **common positive path remainder**. The set is not selected separately for each path test. A countable norming class fixes common roof versions, and measurable roof-dependent unit bounded-Lipschitz tests are then dominated by the dual norm.

The topology remains bounded-Lipschitz dual in the path variable. The theorem does not prove path-space total variation or an essential-supremum estimate in an unbounded path metric.

## 12. Replacing the signed transition kernel by its positive part

For conditional roof laws the manuscript defines

\[
F_J=\int_JP,
\qquad
H_J=\int_JG_+.
\]

The use of `G_+` is necessary because the finite transition kernel can be signed at finite count.

The path estimate was initially written with signed `G`. The manuscript observes correctly that replacing `G` by `G_+` does not increase the discrepancy.

If `G(v)\ge0`, nothing changes.

If `G(v)<0`, then

\[
\mathbf P(v)-G(v)\mathsf W_R
 =\mathbf P(v)+|G(v)|\mathsf W_R
\]

is a positive measure, whose bounded-Lipschitz dual norm is

\[
P(v)+|G(v)|.
\]

Replacing `G` by zero gives the smaller positive measure `bold P(v)` of norm `P(v)`.

Consequently

\[
\int_J|P-G_+|
 \le r|J|,
\]

and

\[
\int_J
\|\mathbf P-G_+\mathsf W_R\|_{\mathrm{BL}^*}
 \le r|J|.
\]

This positive-part passage is correct.

## 13. Exact interval posteriors

Assume

\[
H_J\ge d|J|
\]

and `r<d`. The scalar estimate gives

\[
|F_J-H_J|\le r|J|
\]

and hence

\[
F_J\ge(d-r)|J|.
\]

For the true and reference roof laws

\[
d\pi_J=P\mathbf 1_Jdu/F_J,
\qquad
dQ_J=G_+\mathbf 1_Jdu/H_J,
\]

adding and subtracting `G_+/F_J` gives an unnormalized variation mass at most

\[
2r|J|/F_J.
\]

The manuscript uses the convention

\[
d_{\rm TV}(\pi,Q)=\frac12\int|d\pi-dQ|.
\]

Therefore

\[
d_{\rm TV}(\pi_J,Q_J)
 \le\frac r{d-r}.
\]

The factor is correct.

For the joint roof-path law, normalizing the path-valued discrepancy and paying the denominator difference yields

\[
\frac{2r}{d-r}
\]

against functions measurable in the roof and unit bounded-Lipschitz in the path.

The conditional-mean bridge bound uses the pointwise inequality

\[
P(v)d_{\rm BL}(\mathsf Q^v,\mathsf W_R)
 \le2\|\mathbf P(v)-G(v)\mathsf W_R\|_{\mathrm{BL}^*}.
\]

When `G\ge0`, this follows by adding and subtracting `P\mathsf W_R` and using the constant test to bound `|P-G|`. When `G<0`, the right side is at least `2P` while the bounded-Lipschitz distance is at most two. Integration and division by `F_J` again give

\[
\int_Jd_{\rm BL}(\mathsf Q^v,\mathsf W_R)\,\pi_J(dv)
 \le\frac{2r}{d-r}.
\]

I find these normalization constants consistent.

The intervals may have arbitrarily small positive length and may depend on `m`. This conclusion is possible because the maximal estimate is finite and simultaneous in the interval family. It is not obtained by substituting a shrinking interval into a fixed-window asymptotic theorem.

## 14. The good-roof collision bridge

At a good roof, the unnormalized path error is at most `r`. The scalar positive-error representation gives

\[
P(u)\ge G(u)-\eta^{\rm path}_{B,m}.
\]

If

\[
G(u)\ge d
\]

and `eta_path<d`, the same pointwise path inequality yields

\[
d_{\rm BL}(\mathsf Q^u,\mathsf W_R)
 \le
\frac{2r_{B,m}}{d-\eta^{\rm path}_{B,m}}.
\]

This denominator is correct. It uses the smaller raw representation error in the denominator and the maximal raw error in the numerator.

The conclusion is explicitly almost everywhere on the good set because regular conditional path laws and density representatives are only fixed almost everywhere. The paper does not assign a positive probability to the equation `T_n=u`.

## 15. Good-roof likelihood

For a pointwise likelihood statement the manuscript assumes the stronger condition

\[
G\ge d>0
\]

almost everywhere on the interval. An integrated lower bound would not suffice.

The exact likelihood ratio is

\[
r_J(u)=\frac{H_JP(u)}{F_JG(u)}.
\]

The identity

\[
r_J(u)-1
 =\frac{H_J(P(u)-G(u))}{F_JG(u)}
   +\frac{H_J-F_J}{F_J}
\]

is correct.

At a good roof, `|P-G|\le r`. If `r\le d/2`, then

\[
H_J/F_J
 \le1+\frac r{d-r}
 \le2.
\]

The two displayed terms are each bounded by `2r/d`, giving

\[
|r_J(u)-1|\le4r/d.
\]

The theorem correctly restricts this essential bound to good roofs. It does not claim a forward essential-likelihood estimate on the entire interval.

## 16. Probability of bad anchors

On a mother interval with

\[
\int_IG_+\ge dh,
\]

the inherited local `L^1` law implies that the true denominator is eventually at least `dh/2`. This follows because replacing signed `G` by `G_+` does not enlarge the scalar discrepancy against the nonnegative density `P`.

Dividing the ordered original-source exceptional mass by the true denominator gives

\[
\pi_I(O_B)\le C_{h,d}B^{-1/384}
\]

in collision limsup.

For the reference law, the bounded transition kernel gives

\[
\frac{G_+}{\int_IG_+}
 \le \frac{C_G}{dh},
\]

so the Lebesgue length estimate gives the same order for `Q_I(O_B)`.

No independence assumption between the exceptional set and either measure is used. This is important because the set is defined from the same physical source.

## 17. The qualitative growing-band diagonal

The paper derives sequences

\[
B_m\to\infty,
\qquad
a_m\to0,
\]

for which the good-set errors and exceptional measures tend uniformly to zero.

The construction is legitimate. One first chooses a deterministic sequence `B_j` so that

\[
CB_j^{-1/384}\le2^{-j}.
\]

For each fixed `B_j`, the uniform fixed-band limsup supplies an index `M_j` beyond which the path discrepancy and normalization errors are small. One then sets

\[
B_m=B_j
\quad\text{for}\quad
M_j\le m<M_{j+1}.
\]

The all-interval maximal inequality is already finite at each pair `(B,m)`, so no additional diagonal over interval lengths is required.

This is a qualitative diagonal only. It does not provide a polynomial collision-count rate and does not estimate fixed-band spectral constants as the band grows. The manuscript says so explicitly.

## 18. Adaptive interval selection

The theorem is uniform over a deterministic family of all subintervals containing a good anchor. This means that for each fixed source and target, every member of that family satisfies the displayed estimate.

It does **not** imply that conditioning on the output of an adaptive interval-selection rule produces the same conditional law. If a random or data-dependent procedure chooses an interval, the selection event can carry additional information and can change the conditioning sigma field.

The manuscript includes this caveat. It should remain prominent in the final statement because “uniform over all intervals” is otherwise easy to overinterpret.

## 19. Maximal transfer to the actual-return bridge

The collision bridge has a quantitative ordered-band positive remainder. The actual-return bridge is available through an inherited integrated clock-transfer theorem without a collision-count rate.

The manuscript correctly treats the two situations separately.

It defines

\[
E_m^{\rm ret}(v)
 =\|P(v)\mathsf R^v-G(v)\mathsf V_R\|_{\mathrm{BL}^*},
\]

and

\[
E_m^{\rm col}(v)
 =\|\mathbf P(v)-G(v)\mathsf W_R\|_{\mathrm{BL}^*}.
\]

From the inherited integrated theorems it chooses a deterministic decreasing envelope `e_m` such that

\[
\int_I(E_m^{\rm ret}+E_m^{\rm col})
 \le(1+h)e_m.
\]

With

\[
\ell_m=\sqrt{e_m}+m^{-1},
\]

it defines

\[
O_m^{\rm both}
 =\{\mathcal M_I(E_m^{\rm ret}+E_m^{\rm col})>\ell_m\}.
\]

The weak `(1,1)` estimate gives

\[
|O_m^{\rm both}|
 \le C(1+h)e_m/\ell_m.
\]

The weak endpoint for `P` then gives

\[
\int_{I\cap O_m^{\rm both}}P
 \le C(1+h)(e_m/\ell_m)^{1/145}.
\]

Since `e_m/ell_m` tends to zero, both exceptional quantities vanish.

At a good anchor, every interval average of each path error is at most `ell_m`, and differentiation gives the same almost-everywhere pointwise bound. The constant path test supplies `|P-G|\le ell_m`, so the same exact denominator and posterior arguments apply.

This is a valid qualitative maximal transfer. It would be incorrect to assign the collision-envelope exponent `1/384` to this theorem, and the manuscript does not do so.

## 20. Exact labels and physical conventions

Revision 56 retains the original exact return source. It does not average the return index, collision count or displacement labels.

The normalization remains

\[
\nu_R^*=c^{-1}\nu|_{Y_R^*},
\]

and the factor `1/c` is not inserted a second time in the new maximal estimates.

The occupation convention remains half-open at collision times

\[
0,1,\ldots,m-1.
\]

Clearance of flight `j` is still read at collision `j+1`. The maximal argument acts on the resulting positive roof density and does not continue a trajectory through a grazing or competing-hit seam.

These conventions are preserved correctly in the new text.

## 21. Arithmetic modulation

The uniform main term remains the finite transition kernel

\[
\mathcal L_{m,R}.
\]

At a fixed radius and on central compact sets it reduces to

\[
c\,\mathfrak a_R(k,n,m)g_{\Omega_R}(Z).
\]

Revision 56 does not prove that the concrete section phase masses are uniform. It therefore does not prove that

\[
\mathfrak a_R(k,n,m)=1
\]

on every class.

This is mathematically honest. The posterior theorems use `G_+`, and the pointwise likelihood theorem assumes a positive arithmetic floor. Zero transition classes are not assigned likelihoods or conditional Gaussian laws.

A final paper should embrace this arithmetic modulation as intrinsic unless the concrete zero-residue criterion is separately proved.

## 22. What revision 56 closes

Relative to revision 55, the new manuscript closes the following real issues.

- One positive envelope now controls incidence and clearance simultaneously.
- One set works for every bounded source insertion through a common disintegration.
- The good set is chosen before the roof resolution.
- All positive-length intervals containing a good anchor are controlled simultaneously.
- The scalar and path-valued raw errors share the same physical exceptional set.
- The exceptional Lebesgue length is explicitly `O(B^{-1/384})`.
- The original-source probability has the same ordered exponent.
- Exact roof posterior total variation is uniform over arbitrarily short anchored intervals.
- The collision same-roof bridge is uniformly controlled at positive-reference good roofs.
- The true and reference mother-window roof laws assign vanishing probability to bad anchors along a qualitative diagonal.
- The actual-return and collision bridges admit a common qualitative maximal good set.

These are mathematically meaningful refinements of the topology and quantifiers of the earlier results.

## 23. What revision 56 does not close

The principal endpoint remains unchanged.

The manuscript has not shown that

\[
O_{B,m,R}^{n,k,I}=\varnothing
\]

for large `m` and `B`, nor that the physical density is small inside this set.

It has therefore not proved

\[
\lim_{B\to\infty}\limsup_{m\to\infty}
\|m^2b^{\varepsilon(B),\mathrm{inc},1}_{n,k,m,R}\|_{\infty,M}=0
\]

or

\[
\lim_{B\to\infty}\limsup_{m\to\infty}
\|m^2b^{\varepsilon(B),\mathrm{clr},1}_{n,k,m,R}\|_{\infty,M}=0.
\]

Consequently it has not proved

- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- a uniform essential-supremum same-roof bridge at every positive-reference roof;
- unrestricted forward essential likelihood;
- or a pointwise roof-conditioned path theorem at every prescribed roof representative.

The new results show that any obstruction is concentrated on a small open set which is small under both Lebesgue and original-source measures. They do not remove the obstruction.

## 24. Why small exceptional measure is not enough

A density spike can have height `H` and width much smaller than `H^{-1}`. Its total mass may tend to zero while its essential supremum diverges.

The weak `L^{145/144}` endpoint restricts the allowed relation between height and width, but it does not bound the height.

The maximal theorem adds the strong conclusion that every interval average around a good anchor is small. A spike remains compatible with that conclusion if all points of the spike lie in the exceptional set.

The original-source estimate shows that a conditioned trajectory is unlikely to have a roof inside the exceptional set. It does not prove the pointwise density theorem at those roofs.

Thus none of the following implications is valid:

- small exceptional length implies empty exceptional set;
- small source probability implies small essential height;
- all-resolution control outside the set implies pointwise control inside it;
- roof-mean bridge convergence implies a bridge at every prescribed roof;
- good-set likelihood control implies forward essential likelihood on the whole window.

The manuscript correctly avoids these implications.

## 25. Novelty and relation to prior methods

The maximal covering and weak-tail interpolation arguments are classical real-variable tools. Their value here lies in their application to a highly nontrivial source already constructed by the manuscript:

- the original four-coordinate return record;
- exact return and collision indices;
- a complete roof density;
- finite arithmetic residues and transition branches;
- a positive incidence/clearance source decomposition;
- a path-valued positive remainder;
- and an actual-return clock transfer.

The new theorem is not obtained by differentiating an interval local limit from the Lorentz-process, billiard mixing-local-limit or suspension-flow literature. It uses the manuscript's exact positive source and raw-error representation.

Nevertheless, the genuinely difficult dynamical inputs remain specific to one triangular finite-horizon Lorentz family. The new abstraction does not supply a second independent singular-hyperbolic application, and the interval maximal lemma itself is not a new spectral or dynamical theorem.

This limits the additional top-four significance of revision 56 even though the internal advance is real.

## 26. Generality and editorial significance

The combined A2-DYN program now contains a technically impressive collection of results:

- stationary physical microscopic local laws;
- parameter-family action estimates;
- finite occupation resonance classification;
- exact-index arithmetic interval laws;
- uniform transition kernels through arithmetic changes;
- local variation of the complete raw density;
- a one-sided pointwise lower law;
- weak and subcritical higher-integrability endpoints;
- endpoint Orlicz laws;
- path-valued raw inversion;
- same-roof finite-Wasserstein transport in mean;
- forward and reverse entropy conclusions;
- and now all-resolution localization outside small common physical exceptional sets.

This is substantial specialist mathematics if the inherited continuum chain withstands expert scrutiny.

At the requested four-journal benchmark, however, four factors remain decisive:

1. the title and architecture still center the unproved unrestricted pointwise raw endpoint;
2. the hardest inputs remain highly model-specific;
3. the article remains extraordinarily long and dependency-heavy;
4. no independent billiards/anisotropic-spaces audit has been obtained.

A focused paper centered on the complete local `L^q` law, positive-source maximal localization and conditional transport could plausibly be strong specialist-journal work. The present top-four submission architecture remains premature.

## 27. Independent specialist verification

No independent human specialist audit has been obtained. The following inherited points remain especially load-bearing:

1. the physical thin-layer multiplier through every homogeneity strip;
2. the image-side incidence and clearance transversality;
3. the next-collision clearance convention on all matched branches;
4. the full occupation-torus power bounds;
5. the moving spectral peak decomposition;
6. the physical peripheral representations;
7. the exact first-physical-defect source partition;
8. the all-depth marked local upper bound;
9. the protected flow-box height estimate;
10. the critical-collar geometry and one-time charging;
11. the complete band-limited arithmetic inversion;
12. the scalar positive raw-error identity;
13. the common positive path-remainder identity;
14. the common roof disintegration and countable norming class;
15. the actual-return clock transfer;
16. the uniform boundedness of the finite transition kernel;
17. exact normalization by the section mass `c`;
18. half-open occupation at the terminal collision;
19. preservation of exact labels in every positive upper comparison;
20. parameter-uniformity through arithmetic transitions.

For the new modules themselves, a specialist should check

- that the finite physical source used in the disintegration is exactly the source appearing in the inherited positive representation;
- that all maximal sets are formed from common roof versions;
- that the mother-window and central-target enlargements are sufficient for every inherited path estimate;
- that the true and reference denominators are uniform in the stated classes;
- and that no hidden dependence on the selected interval enters the fixed-band constants.

The exact-source workflows and finite diagnostics do not replace this audit.

## 28. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 28.1 Control the incidence height

Prove

\[
\lim_{B\to\infty}\limsup_{m\to\infty}
\sup_{R,n,k}
\operatorname*{ess\,sup}_{\mathrm{central}\ u}
 m^2b^{\varepsilon(B),\mathrm{inc},1}_{n,k,m,R}(u)=0.
\]

The estimate must hold on the present exact labels and original source, not after deleting the exceptional set.

### 28.2 Control the clearance height

Prove the analogous estimate for the complete competing-hit clearance source without continuing an orbit through a physical seam or replacing the word by a nearby regular word.

### 28.3 Complete the two-sided arithmetic raw theorem

Combine the two positive-height estimates with the already proved positive-error representation and the finite transition kernel.

The arithmetic factor must remain unless the section residue theorem is separately proved.

### 28.4 Deduce unrestricted same-roof bridges

Use the already isolated scalar-to-path implication to prove the collision and actual-return bridges at every positive-reference roof in the appropriate almost-everywhere version, without deleting a target-dependent exceptional set.

### 28.5 Resolve the arithmetic presentation

Either prove the concrete zero-residue criterion or state the finite arithmetic transition kernel and fixed-radius residue as permanent parts of the principal theorem and title-level summary.

### 28.6 Obtain independent specialist review

The physical multiplier, protected critical geometry, occupation spectrum, moving peaks, source decomposition and clock transfer require external human verification.

### 28.7 Extract a broader dynamical theorem

If top-four breadth is sought, formulate a reusable theorem for singular hyperbolic systems with positive boundary sources and verify it in more than one genuinely different system. The classical maximal lemma alone does not supply this breadth.

### 28.8 Reduce the proof burden

Present the shortest complete route to one principal endpoint. Historical pipelines, duplicated theorem hierarchies, validation ledgers and unfinished alternative endpoints should not dominate the journal article.

### 28.9 Sharpen the literature comparison

Explain theorem by theorem which exact-label, arithmetic, raw-density, path-valued and all-resolution conclusions are unavailable from existing Lorentz-process, billiard endpoint-LLT and suspension-flow LLT frameworks after checking their hypotheses.

## 29. Technical and presentation comments

1. Keep the mother interval `I`, anchored subinterval `J`, reconstruction band `B`, auxiliary spectral band, protection width `epsilon`, threshold `lambda` and collision count `m` visibly distinct.
2. State in every principal theorem that the exceptional set depends on the exact labels, collision count and mother interval.
3. Retain the phrase “almost everywhere on the good set” for pointwise density and bridge statements.
4. Do not call the good-set theorem an unrestricted essential-supremum theorem.
5. Keep `G` signed in raw inversion and use `G_+` only when defining a probability reference.
6. Keep the integrated denominator condition `H_J>=d|J|` distinct from the pointwise floor `G>=d`.
7. Preserve the exact total-variation convention with its factor `1/2`.
8. Keep the conditional-mean bridge constant `2r/(d-r)` separate from the roof TV constant `r/(d-r)`.
9. State that the likelihood bound `4r/d` holds only at good roofs.
10. Preserve the qualitative nature of the diagonal `B_m`; do not attach an unproved polynomial collision-count rate.
11. Do not import the collision-band exponent into the actual-return clock-transfer theorem.
12. Keep the common-disintegration construction adjacent to the assertion uniform over bounded insertions.
13. Distinguish a deterministic family of all intervals from an adaptive interval-selection event.
14. Keep bounded-Lipschitz path dual norm distinct from path-space total variation.
15. Keep finite-Wasserstein roof-mean convergence distinct from pointwise bridge convergence.
16. Preserve the weak `L^{145/144}` versus strong-subcritical distinction.
17. Do not infer source-height control from source-mass control.
18. Keep the exact factor `1/c` and avoid applying it twice.
19. Retain clearance at collision `j+1` and occupation at times `0,...,m-1`.
20. State the central-target enlargement across a mother window in the actual-return transfer.
21. Use `G_+` when defining `Q_J` and do not assign a law to a zero arithmetic denominator.
22. Keep the fixed-radius arithmetic factor in every specialization.
23. Do not describe the maximal lemma as a new spectral theorem.
24. Preserve the distinction between the finite weak-endpoint source-mass exponent and the sharper ordered `1/384` exponent.
25. State when an estimate is finite in `m` and when it holds only after a fixed-band collision limsup.
26. Keep source qualification, finite diagnostics and PDF rendering separate from proof certification.
27. Retain the status flags for the unrestricted endpoint and independent review.
28. Consider moving extensive provenance and validation material outside the main journal narrative.

## 30. Final assessment

Revision 56 is a serious and mathematically coherent response to the revision-55 report.

It proves a self-contained maximal interval principle, applies it to the actual positive incidence and clearance sources, constructs one common good-roof set for all interval resolutions and bounded insertions, and derives exact scalar, path and conditional consequences without changing the physical record or exact labels.

The exponent bookkeeping is consistent:

\[
\varepsilon(B)^{1/16}=B^{-1/192},
\qquad
\lambda_B=B^{-1/384},
\qquad
\frac{\varepsilon(B)^{1/16}}{\lambda_B}=B^{-1/384}.
\]

The weak-endpoint source conversion correctly uses

\[
1-1/(145/144)=1/145,
\]

while the sharper ordered original-source estimate correctly uses the positive raw-error representation instead.

The normalization of the exact interval posteriors, collision bridge, likelihood and actual-return transfer appears internally sound. I found no decisive error in modules 119--120.

The advance is nevertheless a localization theorem, not closure of the pointwise endpoint. The exceptional sets have small length and small probability, but they may still contain positive physical spikes of unbounded height. The unrestricted two-sided arithmetic raw-density theorem, unrestricted same-roof bridges and forward essential likelihood therefore remain open.

The manuscript also remains highly model-specific, extraordinarily large and dependent on continuum inputs which have not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist-journal paper built around the complete local `L^q` theory, positive-source maximal localization and conditional transport could be significant if the inherited proof chain survives expert audit. A future top-four submission should return only after closing the positive incidence and clearance heights or after extracting and independently validating a substantially broader theorem.