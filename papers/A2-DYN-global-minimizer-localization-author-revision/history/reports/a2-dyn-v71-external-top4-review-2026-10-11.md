# External top-four referee report on A2-DYN revision 71

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v71-referee-response-2026-10-11`, `revision/a2-dyn-v71-referee-copy-2026-10-11`  
**Reviewed commit:** `85152b57d47493e8d0ec2125e8365560aeb75cf0`  
**Reviewed repository tree:** `afb525d63d2c80455faa97515d3fb76b41a7be16`  
**Active manuscript directory:** `papers/A2-DYN-v71-referee-response`  
**Active mathematical source:** one hundred fifty-six numbered core modules; revision 71 retains all one hundred fifty-four revision-70 modules and adds modules 155--156  
**Frozen revision-70 author baseline:** `9eb04448ca20772c99c500b406a62bca1d2172c7`  
**Frozen revision-70 paper tree:** `6ac66c423de6b7705441cf346b927f04de9ad1a1`  
**Controlling external report:** `reviews/a2-dyn-v70-external-top4-review-2026-10-10/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `acf8568f8ce23f3067532f87d4264bdc41e3901b` / `17cc59fa6d9063db8dabf4b2dbaa6a81247198c6`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 71 is a genuine theorem-bearing advance over revision 70. The preceding report accepted the finite-scale overlap construction and the signed one-sided radial-current identity, but observed that the complete pointwise budget still contained three uncontrolled ordered heights:

1. the angular-loss component `d70` inside the selected disks;
2. the original physical outside source `e70`; and
3. the complete first-incidence source.

The present revision makes a mathematically meaningful improvement to the first item. Instead of treating every chart's angular loss separately, it pools the available receiving collar capacity over all active charts of the **same** collision count, radius, exact return/displacement label and roof value. It then reallocates a maximal scalar fraction of the old loss source back into the controlled source. The controlled component increases, the positive residual decreases, and the source remains the original physical source with no orbit coupling or label exchange.

The revision also replaces the previous death-only radial comparison by an exact two-sided bounded-variation balance. The new kernel counts positive births below the source roof and negative deaths above it, retains all radial jump atoms, translates every chart to the same roof, and takes the positive part only after the physical weights and all active charts of one exact label have been combined.

I audited the new modules

- `core/155_pooled_physical_collar.tex`;
- `core/156_two_sided_current_and_raw_budget.tex`;

and their direct inherited inputs in modules 149 and 152--154. I also checked the revised front matter, source manifest, proof ledger, specialist audit map, validation protocol, exact-SHA workflow records and the legal fixed-band order of parameters.

I found no decisive counterexample, missing section normalization, incorrect capacity algebra, false orbit transport, wrong sign in the BV kernel, lost jump atom, exact-label mixing, word-count multiplier, or illegal collision-count-dependent reconstruction band in the new scoped proofs.

In particular, the following points are internally coherent.

1. The pooled quantities `X`, `O` and `Y` are formed only from active charts carrying the same exact label and evaluated at one common roof.
2. The recovery coefficient lies in `[0,1]` and is maximal only for the displayed scalar capacity constraint; the manuscript does not misdescribe it as optimal transport.
3. The recovered and residual sources are complementary bounded weights on the unchanged positive source, not a fictitious partition into new physical events.
4. The controlled source satisfies `s71,K <= E_chi K Y` before any ordered limit is taken.
5. The inherited comparison-collar theorem bounds the pooled receiving average after summing all active centers, so no chart count or exact-label count appears.
6. The resulting ordered height is `O(K chi^6)` with `K`, `chi` and `epsilon` fixed before the collision-count limsup.
7. The two-sided BV identity has the correct triangular coefficients on both sides of the source roof.
8. The identity includes positive births below the source roof and negative deaths above it; a death-only current would miss the late-birth example exhibited in the text.
9. Distributional atoms of `DL` remain present.
10. The physical current is combined with the actual chart weights and common-roof translations before a positive part is taken.
11. At `K=1`, the residual capacity is exactly the positive part of the pooled signed current `X-Y`.
12. At general `K`, the residual is exactly represented by the positive part of `C-(K-1)Y`.
13. The fixed-band contribution `K(B) chi(B)^6` is correctly written as `K(B) B^{-1/4}`.
14. The manuscript does not claim an ordered current estimate, outside-source estimate, incidence estimate or unrestricted pointwise theorem.

These are real improvements. The negative recommendation is therefore not based on failure of the new algebraic and BV identities.

It is forced by the fact that the revision still does not prove any of the three unrestricted ordered estimates which govern the title-level endpoint.

The new raw budget is

```text
E_M <= C_M B^(-1/192)
       + C K(B) B^(-1/4)
       + C N_{chi(B)}(K(B))
       + H(b_inc)
       + H(e70).
```

Here `N_chi(K)` is the ordered essential height of

```text
[X - K Y]_+
 = [C - (K-1)Y]_+.
```

No bound tending to zero is proved for this quantity. The current theorem gives an exact geometric representation of the same residual; it does not estimate it. The complete first-incidence height and the outside-source height are unchanged and unproved.

Consequently revision 71 still does not establish

- complete ordered control of the selected-chart angular loss;
- complete ordered first-incidence height;
- complete ordered outside-source height;
- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof collision and actual-return bridges;
- forward essential-likelihood convergence; or
- the unrestricted pointwise roof-conditioned path theorem.

The reserve-class theorem is conditional: it proves the complete selected-source height under `X <= K Y`. The manuscript explicitly does not prove that the unrestricted Lorentz family satisfies this condition for any admissible `K(B)`. Scalar complementary-profile examples illustrate the mechanism but are not Lorentz realizations.

At the requested benchmark, the paper would need either

1. a quantitative theorem producing `K(B)` with
   `K(B)B^(-1/4) -> 0` and `N_{chi(B)}(K(B)) -> 0`, together with vanishing ordered incidence and outside heights, followed by the unrestricted pointwise theorem; or
2. a substantially broader theorem of independent significance, with quantitatively verifiable hypotheses and several genuinely different singular-hyperbolic realizations, so that the paper no longer depends editorially on the unfinished Lorentz endpoint.

Revision 71 supplies neither endpoint yet. No independent human specialist audit has been obtained.

My assessment is therefore positive about the new pooled-source identity and negative about readiness for *Annals*, *Acta*, *Inventiones* or *JAMS*.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`85152b57d47493e8d0ec2125e8365560aeb75cf0`.

The repository tree at that commit is

`afb525d63d2c80455faa97515d3fb76b41a7be16`.

The active paper is

`papers/A2-DYN-v71-referee-response`.

The immediate mathematical baseline is revision 70 at

`9eb04448ca20772c99c500b406a62bca1d2172c7`.

The source manifest records

- all one hundred fifty-four inherited core modules byte-identical;
- all two hundred six inherited Python sources byte-identical;
- all ten inherited appendices byte-identical;
- `references.tex` byte-identical;
- every inherited compiled input and mathematical label retained;
- the revision-70 opening retained in a compiled appendix;
- one hundred fifty-six active core modules;
- `lorentz_pooled_capacity_recovery_proved: true`;
- `lorentz_pooled_controlled_height_proved: true`;
- `lorentz_two_sided_signed_collar_identity_proved: true`;
- `lorentz_full_selected_reserve_class_height_proved: true`;
- `lorentz_pooled_net_current_height_proved: false`;
- `lorentz_outside_source_height_proved: false`;
- `lorentz_complete_first_incidence_height_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- `forward_essential_likelihood_convergence_proved: false`; and
- `independent_human_review: false`.

These flags accurately distinguish the new scoped results from the unproved full endpoint.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v71-external-top4-review-2026-10-11/`.

No author source, workflow, prior review, historical manuscript or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA revision-71 qualification workflows completed successfully on both reviewed author refs:

- response branch run `38069193232`;
- referee-copy branch run `38069197930`.

Both runs use the reviewed SHA

`85152b57d47493e8d0ec2125e8365560aeb75cf0`.

According to the validation protocol and workflow, the verifier checks

- the frozen revision-70 paper tree;
- the controlling revision-70 report blob;
- every inherited core, Python, appendix, bibliography, input and label byte;
- all one hundred fifty-six active core inputs;
- the inherited boolean status map;
- normal and optimized finite diagnostics;
- native TeX compilation without shell escape;
- stabilized references, warning-free typesetting and rendered proof pages; and
- the actual checkout SHA and active source tree.

The new finite diagnostics cover the scalar capacity allocation, the zero-capacity case, partial and full recovery, complementary profiles, late births, atomic deaths, signed-current cancellation, the fixed-band `K B^(-1/4)` tradeoff and negative controls against pooling different labels.

These checks are meaningful source, algebra and typesetting evidence. They do not certify

- completeness of the physical one-hot mask;
- common coarea versions through all pooled essential suprema;
- the inherited unguarded comparison collar theorem;
- the restricted-analytic description of every fixed-word physical angular set;
- collision-uniform control of the signed pooled current;
- the outside-source height;
- the first-incidence height;
- the unrestricted pointwise theorem; or
- independent human review.

The manuscript and validation files state this boundary correctly.

## 4. Scope of this audit

I did not attempt to re-prove all one hundred fifty-six modules. The substantive review concentrates on the new chain and its direct inputs:

1. the old overlap/loss decomposition `s70+d70`;
2. the exact physical angular fraction at one exact label;
3. the pooled capacities `X`, `O`, `Y`;
4. the scalar recovery coefficient;
5. source-level realization of the roof-dependent weight;
6. the inherited unguarded collar trace;
7. the `O(K chi^6)` height calculation;
8. the reserve-class corollary;
9. finite-word BV of the angular fraction;
10. the exact two-sided collar kernel;
11. the Jordan-part upper bound;
12. the physical reduced-boundary current;
13. common-roof translation of chart currents;
14. the identity `C=X-Y`;
15. the residual `C-(K-1)Y`;
16. the fixed-band pointwise budget;
17. the unchanged incidence and outside terms;
18. source preservation and exact-SHA evidence; and
19. the requested top-four significance standard.

The inherited anisotropic-operator, arithmetic, critical-geometry, source-partition and local-limit chains are treated as source-pinned inputs, not as independently recertified mathematics. Their earlier specialist qualifications remain in force.

## 5. The scalar recovery lemma

The abstract lemma starts with nonnegative numbers satisfying

```text
O <= min(X,Y),
S <= E O,
D <= E(X-O).
```

For `K>=1` it defines

```text
theta_K = min(1,(K Y-O)/(X-O))
```

when `X>O`, and `theta_K=1` when `X=O`.

The algebra is correct. Since `KY>=Y>=O`, the numerator is nonnegative. One has

```text
O+theta_K(X-O)=min(X,KY),
(1-theta_K)(X-O)=(X-KY)_+.
```

Thus

```text
S_K=S+theta_KD <= E min(X,KY),
D_K=(1-theta_K)D <= E(X-KY)_+.
```

When `X=O`, the hypothesis on `D` forces `D=0`, so the convention `theta_K=1` is harmless.

The monotonicity in `K` is also correct.

The manuscript carefully limits the optimality claim: `theta_K` is maximal for the displayed scalar capacity constraint. It is not claimed to be a physical transport optimum or a coupling between chart trajectories.

## 6. Pooled capacities on the original source

At a fixed collision count, radius, exact label and roof, the manuscript defines

```text
X = sum_z J_z L_z(u_z),
O = sum_z J_z average_v min(L_z(u_z),L_z(v)),
Y = sum_z J_z average_v L_z(v).
```

The active chart set is the same in all three sums. The exact label is not suppressed mathematically; it is only omitted typographically.

The inequalities

```text
0 <= O <= min(X,Y)
```

follow chartwise from the minimum.

The inherited physical profile bounds give

```text
s70 <= E_chi O,
d70 <= E_chi (X-O).
```

This step retains the actual nonconstant guard; only its upper bound by one is used.

The new sources

```text
s71,K = s70 + theta_K d70,
d71,K = (1-theta_K)d70
```

are legitimate bounded source weights. The coefficient `theta_K(t)` may depend on all active charts of the same exact record, but it is a measurable scalar function of the roof. Composing it with the original roof observable therefore defines a measurable insertion on the original probability space. No spectral regularity of this insertion is needed for the positive comparison.

The identities

```text
b_clr = s71,K + d71,K + e70,
s71,K >= s70,
0 <= d71,K <= d70
```

are exact.

A specialist should nevertheless verify that one common family of coarea representatives is used before forming `X`, `O`, `Y` and `theta_K`, so that version choices do not vary chart by chart. The manuscript explicitly adopts common coarea versions; the finite diagnostics cannot establish that continuum bookkeeping.

## 7. Ordered height of the recovered source

The scalar lemma gives

```text
s71,K <= E_chi K Y.
```

For each active chart,

```text
J_z average_{(0,j)} L_z
 <= exp(K_chi sqrt(2j)) q_hat_{z,j}.
```

At roof `t`, the active centers lie in `[t-h,t]`. The inherited comparison-collar theorem with atom interval length `h` and collar width `j=h/2` gives a bound proportional to

```text
h+j=3h/2.
```

Consequently

```text
H(s71,K)
 <= (3/2) C K h_chi
    exp((1+1/sqrt(2))K_chi r_chi)
 <= C' K chi^6.
```

The exponent calculation is correct because

```text
h_chi = r_chi^2/2,
r_chi = r_0 chi^3,
K_chi r_chi = O(chi).
```

No chart count or word count enters: the collar theorem is applied after summing the positive physical event.

This is the principal unconditional quantitative gain of revision 71. It is genuine, but it controls only the enlarged recovered source.

## 8. The receiving-reserve class

If

```text
X(t) <= K Y(t)
```

for almost every roof and uniformly in the stated large-count family, then

```text
d71,K=0.
```

The full selected-chart source is therefore controlled by the preceding `O(K chi^6)` estimate.

This corollary is correct. It is also strictly conditional.

The paper gives scalar complementary-profile examples in which one chart's late birth is compensated by another chart's receiving capacity. These examples show that the reserve condition is weaker than chartwise monotonicity or chartwise no-loss. They do not show that the unrestricted Lorentz chart family satisfies the reserve condition.

For editorial purposes this distinction is decisive. The corollary is a theorem about a stated subclass, not a theorem that the complete physical source belongs to that subclass.

## 9. The two-sided BV balance

Let `mu=DL` and let

```text
bar L = j^(-1) integral_0^j L(v)dv.
```

The kernel is

```text
k_j(u,s)=F_j(s)                 for s<u,
          -(1-F_j(s))           for s>u,
F_j(s)=min(s/j,1).
```

For a continuity point `u`, averaging the BV fundamental theorem over `v in (0,j)` gives

```text
L(u)-bar L = integral k_j(u,s)dmu(s).
```

The coefficients are correct:

- a point `s<u` is crossed by a fraction `min(s,j)/j=F_j(s)` of the receiving interval;
- a point `s>u` is crossed in the opposite direction by a fraction `(j-s)_+/j=1-F_j(s)`.

The kernel vanishes above `max(u,j)`, so no finite-variation assertion at the upper endpoint `h` is needed. The formulation also avoids artificial boundary atoms at zero and at `h`.

Taking the relevant Jordan parts yields

```text
(L(u)-bar L)_+
 <= integral_{s<u} F_j(s)dmu^+(s)
    + integral_{s>u}(1-F_j(s))dmu^-(s).
```

This inequality correctly retains upward jumps below the source roof and downward jumps above it. The late-birth example demonstrates why the older death-only formula cannot control the whole-disk comparison.

I find no sign error in this lemma.

## 10. The physically weighted pooled current

For each chart the inherited finite-perimeter theorem identifies

```text
mu_z = DL_z
```

with the radial projection of the signed reduced-boundary current of the actual Boolean physical angular set.

The manuscript defines

```text
C_lambda(t)
 = sum_{z active at t} J_z
     integral k_j(t-t_z,s)dmu_z(s).
```

Applying the scalar balance chart by chart gives the exact identity

```text
C_lambda(t)=X_lambda(t)-Y_lambda(t).
```

This is the correct common-roof combination. A positive part is taken only after all charts of the same exact label and their physical coefficients have been summed, preserving cancellations between births and deaths and between charts.

The manuscript is also correct to say what this object is **not**. Because the active chart set changes with `t`, `C_lambda` is not asserted to be the distributional derivative of a total source in the roof variable. No derivative of the moving active-set boundary is included. Thus the result is an exact scalar representation of the pooled capacity discrepancy, not a global conservation law or a factorized resolvent identity.

This limitation must remain explicit in any subsequent use of the word “current.”

## 11. The residual and the current height

The pooled recovery theorem gives

```text
d71,K(t)
 <= E_chi [X(t)-K Y(t)]_+
 = E_chi [C(t)-(K-1)Y(t)]_+.
```

The manuscript then defines

```text
N_chi(K)
 = limsup_m sup_{R,lambda}
     m^2 ||[C-(K-1)Y]_+||_infinity.
```

This is a useful isolation of the remaining selected-chart obstruction.

It is not an estimate of that obstruction.

At `K=1`, `N_chi(1)` is precisely the ordered essential height of the positive pooled current. For larger `K`, increasing the receiving reserve can reduce the residual, but the controlled source pays the factor `K`.

A future closure would need quantitative tail information for the physical ratio `X/Y` or a direct current estimate strong enough to choose `K(B)` while keeping

```text
K(B)B^(-1/4) -> 0,
N_{chi(B)}(K(B)) -> 0.
```

No such theorem is present in revision 71.

Finite variation of each fixed word is insufficient. The number and geometry of word boundaries can grow with the collision count, and the physical weights and roof translations must be retained before cancellation. The current identity correctly exposes this difficulty but does not solve it.

## 12. The revised raw budget

With

```text
epsilon(B)=A_0 B^(-1/12),
chi(B)=sqrt(epsilon(B)),
```

and `K(B)` chosen before the collision-count limit, the manuscript obtains

```text
E_M <= C_M B^(-1/192)
       + C K(B)B^(-1/4)
       + C N_{chi(B)}(K(B))
       + H(b_inc)
       + H(e70).
```

The order of limits is correct. No parameter is chosen as a function of the collision count.

The formula is sharper than the revision-70 budget because part of `d70` has been moved into a controlled source and the remaining part has an exact pooled-current representation.

It is nevertheless still a conditional criterion. The last three terms are not proved to vanish.

The first-incidence term retains only finite-count bounds with exponential collision-count constants. Those bounds cannot be inserted into a fixed-band collision limsup.

The outside source `e70` still contains failed taper, selected grazing, noncritical roof-rank pieces and physical states outside the chosen disks. Revision 71 does not change or estimate it.

## 13. What revision 71 closes

Relative to revision 70, the paper now proves the following.

- Same-label receiving capacity can be pooled before a positive deficit is taken.
- The recovered controlled source is a genuine source weight on the original probability space.
- The controlled source increases monotonically while the positive residual decreases.
- Its ordered height is `O(K chi^6)`.
- The full selected source is controlled on the explicit reserve class `X<=KY`.
- Radial births and deaths admit one exact two-sided BV balance.
- Atomic jumps are retained.
- Chart currents are translated to a common roof and physically weighted before cancellation.
- The remaining selected-chart source is exactly localized to the positive pooled-current excess.
- The fixed-band raw budget records the correct `K B^(-1/4)` tradeoff.

These are mathematically useful refinements of the physical source analysis.

## 14. What revision 71 does not close

The paper has not proved any one of the following unrestricted assertions.

1. `N_{chi(B)}(K(B)) -> 0` for an admissible reserve sequence.
2. Vanishing ordered height of the complete first-incidence source.
3. Vanishing ordered height of the outside clearance source.
4. The complete ordered clearance height.
5. The unrestricted pointwise arithmetic raw-density theorem.
6. Pointwise roof-density convergence on every central exact label.
7. Unrestricted same-roof collision/return bridge convergence.
8. Forward essential-likelihood convergence.
9. A pointwise roof-conditioned path theorem on every positive-reference class.
10. A collision-uniform total-variation bound for the pooled physical current.
11. A global distributional current identity for the total source.
12. A singular resolvent or transfer-operator closure of the boundary current.
13. Triviality of the finite arithmetic factor or elimination of zero classes.
14. Independent human verification of the inherited continuum chain.

The source manifest and publication-status files state these limitations accurately.

## 15. Why the current representation is not yet closure

The new identity is valuable because it places all selected-chart angular mismatch into one signed expression. It may permit cancellations which are invisible in the sum of wordwise Jordan variations.

However, an exact representation and a quantitative estimate are different statements.

A family of signed currents can have finite variation at every collision count while its positive common-roof sum has unbounded normalized essential height. The current can also oscillate between charts whose critical centers move with the word. Neither fixed-word definability nor the scalar reserve algebra controls this growth.

Moreover, since `C_lambda(t)` is not the distributional derivative of the full source in `t`, one cannot integrate by parts in the global raw Fourier inversion without additional active-set boundary terms and a compatible operator realization.

Accordingly, the new current should be viewed as a precise geometric target for the next estimate, not as a completed resolvent mechanism.

## 16. Incidence and outside sources remain independent blockers

Even a complete estimate of the pooled selected-chart current would not by itself finish the paper.

The first-incidence source and `e70` remain in the pointwise budget with positive sign.

The inherited inverse-incidence and finite-type/caustic calculations are finite-count results with collision-dependent constants. They do not supply the ordered fixed-band limits required here.

The outside source is not a negligible bookkeeping remainder. It contains physically distinct failures of the selected-chart construction. Any complete proof must either cover these states by a new positive comparison with collision-uniform constants or prove their ordered essential height directly.

The manuscript correctly keeps these sources visible.

## 17. Arithmetic and conditioning

The finite arithmetic transition kernel remains the correct uniform reference. Zero arithmetic classes are retained.

Revision 71 does not prove that the arithmetic factor is identically one and does not define conditional laws on a zero reference class.

The existing integrated record laws and mean bridge results retain their scope. The new scalar capacity recovery does not upgrade them to unrestricted same-roof statements. Such an upgrade still requires the pointwise source heights and a positive pointwise denominator.

## 18. Significance at the requested benchmark

The pooled recovery lemma and the two-sided BV balance are clean and useful. Their novelty lies in their application to an already elaborate exact-label Lorentz source, not in the scalar inequalities themselves.

The manuscript now contains a very large specialist programme:

- collision-space anisotropic spectral theory;
- exact section occupation and arithmetic transition kernels;
- global mixed total variation;
- bridge and postselection laws;
- pressure/contact comparisons;
- Markov and baker realizations;
- finite-type physical coarea;
- caustic localization;
- finite-scale overlap;
- and pooled radial-current recovery.

If the inherited continuum chain is correct, this represents substantial specialist mathematics.

At the requested four-journal level, however, the paper still has two structural problems.

First, the title and proof architecture are organized around an unrestricted pointwise raw-density endpoint which remains conditional on three unproved ordered heights.

Second, the new revision is incremental relative to that endpoint. It replaces one positive residual by a smaller positive residual with an exact current representation, but supplies no decay estimate for the new residual and no progress on the other two blockers.

A top-four submission should present a completed principal theorem of exceptional scope or a broadly reusable mechanism with independently verified applications. Revision 71 does not yet reach either standard.

## 19. Independent specialist verification

No independent human audit has been obtained.

The following new points require specialist checking.

1. Common coarea representatives before pooling all active charts.
2. Measurability of the global roof coefficient `theta_K` and its realization as a source insertion.
3. Exact-label and chart disjointness in the inherited comparison-collar event.
4. Absence of a hidden chart-count factor in the pooled `Y` estimate.
5. The finite-perimeter representation of every actual Boolean angular set.
6. Attribution of coincident interfaces exactly once.
7. The sign convention in the projected physical current.
8. Preservation of jump atoms in the BV balance.
9. Common-roof translation before positive-part extraction.
10. The distinction between the scalar current and a distributional derivative of the moving total source.
11. The unchanged contents of `e70`.
12. Compatibility of every exact-label restriction with the original section normalization.

The inherited anisotropic, arithmetic, critical-geometry, first-defect and path-transfer arguments remain separate audit obligations.

Native compilation and finite scalar fixtures do not discharge these continuum checks.

## 20. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 20.1 Prove a pooled-current tail theorem

Establish a quantitative estimate for

```text
N_chi(K)
 = limsup_m sup_{R,lambda}
   m^2 ||[X-KY]_+||_infinity
```

which is uniform in the legally ordered physical family.

It must be strong enough to choose `K(B)` with

```text
K(B)B^(-1/4) -> 0,
N_{chi(B)}(K(B)) -> 0.
```

A fixed-word BV statement or an unweighted interface count is not sufficient.

### 20.2 Control the complete first-incidence source

Prove the ordered essential-height estimate on the original exact labels and source. Do not choose the reconstruction band as a function of the collision count.

### 20.3 Control the outside clearance source

Cover or estimate failed taper, selected grazing, noncritical roof-rank and uncovered states with collision-uniform constants. The source may not be discarded by a small-mass or exceptional-set argument.

### 20.4 Close the unrestricted pointwise theorem

Insert the three new estimates into the positive raw-error identity and prove the two-sided pointwise arithmetic law with the finite transition kernel and zero classes retained.

### 20.5 Derive the pointwise conditional consequences

Only after the scalar theorem is closed should the manuscript claim unrestricted same-roof bridges, forward essential likelihoods or pointwise roof-conditioned path laws.

### 20.6 Clarify any future current/resolvent route

If the signed current is to enter Fourier inversion or a resolvent equation, construct the actual global distributional object, including terms created by the moving active-chart set, and prove the required operator or measure bounds.

### 20.7 Obtain independent expert review

The collision-space, physical-source, BV-current and arithmetic chains require independent specialists in dispersing billiards, anisotropic transfer operators and geometric measure theory.

### 20.8 Reduce the journal proof burden

A final journal article should expose one shortest complete theorem route. Extensive historical revision ledgers and incomplete alternative routes should not dominate the main narrative.

## 21. Technical and presentation comments

1. Keep `m,R,n,k,t` fixed when defining pooled capacities; do not suppress the exact-label restriction in theorem summaries.
2. State explicitly that pooling across different labels, radii or collision counts is forbidden.
3. Keep the scalar optimality claim separate from physical optimal transport.
4. Retain the distinction between complementary weights and disjoint events.
5. Preserve common coarea versions before defining `theta_K`.
6. At `X=O`, note explicitly that `D=0` and the value of `theta_K` is immaterial.
7. Keep `K` fixed before the collision-count limsup.
8. When `K=K(B)`, state the order: fix `B`, hence `K(B)`, then take the collision limsup, then let `B` grow.
9. Do not describe `N_chi(K)` as estimated; it is defined and geometrically represented.
10. State that the reserve theorem is conditional and that the scalar examples are not Lorentz realizations.
11. Preserve the exact formula for the two-sided BV kernel.
12. Retain atomic jumps and do not replace the distributional derivative by an almost-everywhere classical derivative.
13. Keep the physical weights `J_z` inside the common-roof sum.
14. Take the positive part only after summing the signed chart currents.
15. Do not call `C_lambda` the derivative of the total source in `t`.
16. Keep the contents of `e70` visible in every principal budget.
17. Do not insert the finite-count `C A^m epsilon` incidence estimate into the ordered fixed-band theorem.
18. Retain the finite arithmetic transition kernel and zero classes.
19. Do not infer pointwise conditioning from integrated total variation.
20. Keep probability total variation distinct from variation mass.
21. Preserve the source normalization `c_*^{-1}` exactly once.
22. Keep occupation at collisions `0,...,m-1` and terminal membership at collision `m`.
23. State that exact-SHA qualification is source evidence, not proof certification.
24. Move extensive provenance and validation records outside the final mathematical narrative where possible.

## 22. Final assessment

Revision 71 is a serious and mathematically coherent response to the revision-70 report.

It proves an exact same-label pooled-capacity construction, enlarges the controlled physical source while preserving the `O(K chi^6)` ordered height, and identifies the remaining selected-chart defect through a two-sided signed BV current which includes births, deaths, atoms and inter-chart cancellation at a common roof.

I found no decisive error in the scoped algebra, the BV kernel, the height calculation or the fixed-band exponent bookkeeping.

The advance nevertheless remains a **reduction**. The new pooled-current height is not proved small. The outside source and complete first-incidence source are untouched. Hence the unrestricted pointwise arithmetic raw-density theorem and its same-roof consequences remain open.

The manuscript is also exceptionally large and depends on a continuum proof chain which has not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist-journal paper built around the physical collar, angular overlap, pooled capacity and signed current could be valuable if the inherited geometric chain survives expert audit. A future top-four review should begin only after the pooled current, outside source and first-incidence source are all controlled in the legally ordered central regime and the title-level pointwise theorem is actually closed.
