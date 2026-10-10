# External top-four referee report on A2-DYN revision 65

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v65-referee-response-2026-10-10`, `revision/a2-dyn-v65-referee-copy-2026-10-10`  
**Reviewed commit:** `04f38424177533db60dfd13c3052381dc0adb481`  
**Reviewed repository tree:** `972435fc257661abd14b2fa8bbb1e01beb95c862`  
**Ordinary source payload tree:** `3b9e9b95a45bf6ad9a1c88476715b83285116f15`  
**Active manuscript directory:** `papers/A2-DYN-v65-referee-response`  
**Active mathematical source:** one hundred thirty-nine numbered core modules; revision 65 retains all one hundred thirty-six revision-63 modules and adds modules 137--139  
**Preserved author baseline:** revision 63, commit `ae14ecbfa39d0d9005574155de86acecd2e8a166`  
**Frozen revision-63 complete paper tree:** `0d019a183d79d8de977bd705aa4ab1e228d6cc17`  
**Controlling external report:** `reviews/a2-dyn-v62-external-top4-review-2026-10-10/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `0ed5b59fdcf9e4f38e621307da4a864cc5a83c8b` / `4d0a4e354df2b7f7b14667332b0a40c2c959160f`  
**Date:** 10 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 65 contains genuine and technically interesting new mathematics on the original Lorentz source. It also incorporates the revision-63 additions, which were landed after the last formal external report and were not separately reviewed. I have therefore treated the five-module chain

- `core/135_effective_buffered_caustics.tex`;
- `core/136_effective_positive_localization.tex`;
- `core/137_reversible_critical_weights.tex`;
- `core/138_simple_caustic_density_profile.tex`;
- `core/139_affine_caustic_label_profiles.tex`

as the substantive new packet relative to the revision-62 report.

Revision 63 replaces the unspecified finite-count semialgebraic constants of revision 62 by explicit, though extremely large, budgets. It constructs a buffered weak-first-hit critical overcover, proves effective separation from that overcover, and gives an effective vertical tube estimate. The source localized near the overcover remains an original positive Lorentz source; the overcover itself carries no probability.

Revision 65 then enters part of the retained caustic source rather than merely estimating the size of its roof support. It identifies the intrinsic quadratic coefficient of a normal-to-normal half-word with a reversible square-root determinant,

\[
 J_z=\frac{1}{R c_*\sqrt{|\det(I-P_z)|}}
     =\frac{1}{R c_*}
       \frac{\lambda_z^{-1/2}}{1-\lambda_z^{-1}},
\]

and calculates the actual local roof density inside a simple clearance seam. The leading profile is an arcsine transition with one-sided limit `J_z/2`. The final new module extends the calculation to several simultaneous clearance seams and section-boundary coincidences, retaining affine offsets and the complete exact-label vector.

I found no decisive counterexample, missing factor of two, erroneous section normalization, wrong image mark, false primitive-period quotient, missing polar Jacobian, invalid label-count multiplier, or replacement of the original physical source in these calculations. The following points are internally coherent.

1. The reversible closure uses the first half-word only for its original labels and the doubled word only to calculate a linear weight.
2. The generating-function signs give `det(I-P_z)=-4bc`.
3. The roof-density coefficient involves the square root of the periodic determinant, not the ordinary inverse determinant.
4. Polar coarea cancels the radial Jacobian and gives the stated arcsine profile.
5. The original smooth first-clearance guard is bounded by the physical strips at its own two widths.
6. Coincident critical values are added as positive weights rather than separated artificially.
7. The affine comparison is uniform in the guard widths and keeps nonzero margin offsets.
8. Exact section occupation uses collisions `0,...,m-1`, with terminal membership treated separately.
9. The sum over exact output labels incurs no label-count factor because each input sign pattern carries at most one label.
10. Every unanalysed source component remains in an explicit positive complement.

These are meaningful improvements. In particular, the manuscript now knows the local height of a nontrivial roof-critical clearance source, rather than only its mass or the size of a containing tube.

The negative recommendation is nevertheless unavoidable because the manuscript still does not close the ordered long-count problem which governs its title and pointwise architecture.

The revision-63 budgets are

\[
 E_m=\left\lceil 2^{C_0(m+1)^{16}}\right\rceil,
 \qquad K_m=2^{E_m}.
\]

Their localization theorem requires

\[
 4K_m\varepsilon\le(\chi h)^{E_m},
 \qquad 0<\chi,h\le1.
\]

For every fixed reconstruction band `B`, the physical width
`epsilon(B)>0` is fixed before the collision-count limit. Since the
right side is at most one and `K_m` diverges, the displayed threshold
fails for all sufficiently large `m`. Thus the effective finite-count
localization is not merely quantitatively weak: in the required fixed-band
collision limit, it eventually becomes inapplicable. Choosing `B` as a
rapid function of `m` would reverse the order of limits established by
the spectral argument and is not licensed by the manuscript.

The revision-65 local formulas avoid this particular determinant
threshold, but they introduce two other unproved long-count inputs:

- uniform coverage of all relevant original-source caustic points by
  Morse neighborhoods whose radii, incidence bounds, gradient bounds
  and finite-jet constants remain usable at fixed `epsilon(B)` as
  `m` tends to infinity; and
- concentration of the positive reversible atomic measure on shrinking
  roof intervals at the normalized `m^2` scale.

The manuscript states the second input explicitly as

\[
 \lim_{h\downarrow0}\limsup_{m\to\infty}
 \sup_{R,n,k,t}m^2\mathfrak T_{B,n,k,m,R}([t-h,t+h])=0,
\]

but does not prove it. Individual decay

\[
 J_z\le C(47/53)^{m-2}
\]

is not enough: the number and clustering of critical half-words may
grow exponentially, and coincident or near-coincident roof values are
exactly what the required concentration estimate must control.

Moreover, the local neighborhoods do not cover the complete positive
boundary source. The remaining source still includes, among other
pieces,

- the complete first-incidence source;
- selected grazing contacts;
- noncritical-roof rank degeneracies;
- clearance caustic points outside the verified neighborhoods;
- regions where selected incidences or scalar margin gradients have no
  count-uniform lower bound; and
- the positive complement in the exact first-defect decomposition.

Consequently revision 65 still does not prove

- the ordered central-scale incidence height;
- the ordered central-scale complete clearance height;
- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof collision/return bridges;
- forward essential-likelihood convergence; or
- the unrestricted pointwise roof-conditioned path theorem.

These are not presentation details. They are the mathematical endpoint
around which the title, the positive-error identity, and a substantial
part of the one-hundred-thirty-nine-module article are organized.

At the requested benchmark, the article would need either

1. a proof of the two ordered Lorentz height estimates, including the
   required uniform neighborhood coverage and reversible-weight
   concentration; or
2. a substantially broader theorem whose independently verifiable
   hypotheses apply to several genuinely different singular-hyperbolic
   systems and whose significance does not depend on the unfinished
   Lorentz endpoint.

Revision 65 provides neither yet. Its new local formulas are useful and
apparently correct, but they reduce the remaining problem to a weighted
critical-cluster theorem rather than proving that theorem. No independent
human specialist audit has been obtained.

My assessment is therefore positive about the local geometric progress
and negative about readiness for *Annals*, *Acta*, *Inventiones*, or
*JAMS*.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`04f38424177533db60dfd13c3052381dc0adb481`.

The repository tree at that commit is

`972435fc257661abd14b2fa8bbb1e01beb95c862`.

The active article is

`papers/A2-DYN-v65-referee-response`.

The ordinary source payload tree recorded in the manifest is

`3b9e9b95a45bf6ad9a1c88476715b83285116f15`.

The latest prior formal report is the revision-62 report at

`0ed5b59fdcf9e4f38e621307da4a864cc5a83c8b`.

After that report, revision 63 landed at

`ae14ecbfa39d0d9005574155de86acecd2e8a166`.

It added modules 135--136. The branch named revision 64 was an alias for
that revision-63 source rather than a distinct theorem-bearing manuscript.
Revision 65 starts from a checkpoint whose parent is the revision-63
commit and then adds modules 137--139.

The current source manifest records

- all 136 inherited core modules byte-identical;
- all 187 inherited Python files byte-identical;
- all compiled appendices retained;
- all 1809 inherited mathematical labels retained;
- an append-only bibliography change;
- three new modules, 137--139;
- `lorentz_buffered_caustic_separation_budget_proved: true`;
- `lorentz_effective_caustic_tube_budget_proved: true`;
- `lorentz_reversible_critical_weight_identity_proved: true`;
- `lorentz_simple_seam_local_profile_proved: true`;
- `lorentz_affine_exact_label_local_profile_proved: true`;
- `uniform_reversible_critical_trace_concentration_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- `unrestricted_same_roof_pair_bridge_proved: false`;
- and `independent_human_review: false`.

These status declarations accurately distinguish the new local theorems
from the unproved ordered endpoint.

The present review branch begins directly from the reviewed author SHA
and adds only this report under

`reviews/a2-dyn-v65-external-top4-review-2026-10-10/`.

No author source, workflow, prior report, historical manuscript, or
unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA revision-63 qualification completed successfully on both
revision-63 author refs:

- response run `38025616388`;
- referee-copy run `38025623447`.

The revision-65 qualification completed successfully on the response
branch:

- response run `38044059239`.

At the time of this report, the repository API returned no separate
workflow run for the revision-65 referee-copy branch. Both v65 branches
point to the same exact commit, so this does not create a source-identity
ambiguity; it does mean that the claimed two-ref execution evidence is
not literally present for v65.

The v65 validation protocol checks

- the pinned revision-63 paper tree;
- all 136 inherited core files;
- all 187 inherited Python files;
- all 139 compiled core modules;
- all 1809 inherited mathematical labels;
- every retained appendix;
- sixteen provenance snapshots;
- append-only bibliography changes;
- exact workflow and ordinary-payload hashes;
- normal and optimized finite diagnostics;
- native TeX compilation; and
- theorem-label-based page rendering.

The new finite fixtures test reversible matrices, a one-flight contact
Hessian, the determinant square root, angular threshold profiles,
affine exact-label cases, parallel and quadrant cones, affine offsets,
label variation, and an invalid limit interchange.

These are useful source, algebra, and typesetting checks. They do not
certify

- the inherited anisotropic transfer-operator theory;
- the physical collision-graph and first-defect constructions;
- the effective real-algebraic format claims;
- the local diffeomorphism and positive-incidence hypotheses at every
  long word;
- count-uniform Morse neighborhoods;
- the reversible atomic concentration theorem;
- the complete ordered incidence or clearance height; or
- the unrestricted pointwise local limit theorem.

The manuscript and its validation files state this limitation accurately.

## 4. Scope of this review

I did not attempt to re-prove all 139 core modules. The substantive audit
concentrates on the mathematics which can change the revision-62
assessment:

1. the fixed-format weak-first-hit critical overcover;
2. the finite-fiber and horizontal-strip component bounds;
3. the effective one-variable lower modulus;
4. the buffered-cap separation inequality;
5. the effective vertical tube estimate;
6. insertion of these estimates into the original positive source;
7. the exact order-of-limits consequence of the resulting budgets;
8. reversible closure of a normal-to-normal half-word;
9. generating-function signs and the factor four in the periodic
   determinant;
10. the original source normalization of the Morse coefficient;
11. individual critical-weight decay and crossing measures;
12. physical-side interpretation at a competing-hit seam;
13. the angular threshold lemma;
14. the simple seam arcsine density profile;
15. comparison with the original smooth first-clearance guard;
16. positive critical-cluster bounds;
17. the conditional ordered trace transfer;
18. width-uniform affine guard comparison;
19. the finite margin and exact-label description;
20. the full affine exact-label profile;
21. the explicit finite-jet error budget;
22. the multiple-seam angular trace;
23. source coverage and remaining positive complements;
24. source preservation and workflow evidence; and
25. the unchanged top-four endpoint.

The inherited modules 1--134 are treated as a source-pinned baseline,
not as independently re-certified mathematics. Their load-bearing
continuum assertions remain subject to the specialist-audit requests in
prior reports.

## 5. The weak-first-hit critical overcover

Module 135 introduces an algebraic overcover

\[
 \widehat{\mathcal K}_{m,\eta}
\]

of the capped physical collision graph. It keeps contact and reflection
equations, selected root signs, first jets, uniform flight bounds, the
incidence cap, and the selected-witness envelope. Only strict first-hit
inequalities are weakened.

The associated critical image is

\[
 \widehat{\mathcal C}_{m,\eta}
 =\{(R,F(X)):Z(X)^2=R^2,\ \det D(F,Z)(X)=0\}.
\]

The physical caustic is contained in this set, but equality is neither
claimed nor used. No source measure is assigned to the additional
points. This is the correct distinction: an algebraic overcover may be
used to define a distance or a tube without being interpreted as a
physical orbit space.

The format bookkeeping retains `O(m)` continuous variables and
fixed-degree polynomial equations per word. There are exponentially many
words and polynomially many marks. Coefficient bit lengths are stated to
be `O(m^2)` after clearing rational denominators. The one algebraic
coefficient `sqrt(3)` is handled by an auxiliary equation.

I found no immediate inconsistency in this encoding. A specialist should
still verify that every reciprocal variable needed for the first jets is
uniformly bounded on the capped compact graph and that no hidden
elimination of intermediate collisions raises the degree or coefficient
height beyond the stated format.

## 6. Finite fibers of the buffered critical image

At fixed radius, the selected-witness derivative satisfies

\[
 \partial_\varphi Z=L_d>0.
\]

Thus `dZ` is nonzero on the seam. On the rank locus
`dF wedge dZ=0`, so `dF` is proportional to `dZ`. Along a fixed-radius
seam component, `dZ` vanishes on tangent vectors; hence `dF` vanishes as
well. The roof is therefore constant on each connected semialgebraic
component.

This argument is sound at the formal level. It gives a finite list of
roof values per fixed-radius component, and the sign-component bound
makes the list exponential in `m` after summing the words and marks.
The horizontal-strip image is a finite union of intervals and points.

The proof correctly keeps different word copies disjoint and does not
require differentiability across a change of selected word. It also uses
the weak graph only as an overcover. These qualifications should remain
explicit.

## 7. Effective real-algebraic modulus

The manuscript invokes a fixed-block quantifier-elimination estimate to
obtain output polynomials whose degrees and coefficient bit lengths are
bounded by

\[
 2^{C(m+1)^{12}}.
\]

It then proves an elementary lower-root estimate for a positive
single-valued semialgebraic function and enlarges the budget to

\[
 E_m=\left\lceil2^{C_0(m+1)^{16}}\right\rceil,
 \qquad K_m=2^{E_m}.
\]

The scalar polynomial step is internally coherent. Once `delta` is
smaller than an explicit coefficient-dependent threshold, the first
nonzero integer coefficient of the constant term dominates its tail.
For larger `delta`, monotonicity supplies a uniform lower bound.

The most delicate input is not that scalar step but the claimed
first-order descriptions of the relevant infima with at most a fixed
number of quantifier blocks, `O(m)` variables per block, controlled
coefficient heights, and no unrecorded dependence on the exponentially
large disjunction. I did not identify a direct contradiction, but this is
a theorem-level real-algebraic input and should be checked against the
pinned quantifier-elimination statement by a specialist.

Even granting the estimate completely, its output is only a finite-count
modulus. The enormous size of `E_m` and `K_m` is mathematically decisive
for the later limit.

## 8. Buffered separation

The buffered distance is taken from a source graph capped at `chi` to a
reference critical image capped at `chi/2`. The buffer is used to pass to
limits without assuming continuity of an unbuffered cap-dependent
critical set.

The resulting inequality is

\[
 (\chi d_{m,\chi}(X))^{E_m}
       \le K_m\bigl(||Z(X)|-R|+|\mathcal J(X)|\bigr).
\]

At an original first-clearance point this gives, under

\[
 4K_m\varepsilon\le(\chi h)^{E_m},
\]

a determinant lower bound outside the `h`-neighborhood of the reference
set.

The logical use of the cap buffer is correct. The theorem does not
place source measure on the overcover and does not replace the selected
physical witness.

The limitation is immediate: because `chi,h<=1`, the right side of the
threshold is at most one. For any fixed positive `epsilon`, the factor
`4K_m epsilon` eventually exceeds one. Hence the theorem supplies no
large-count information in the fixed-band regime.

## 9. Effective vertical tube length

The tube estimate reads

\[
 \sup_R\bigl|\{t:\operatorname{dist}((R,t),
       \widehat{\mathcal C}_{m,\chi/2})<h\}\bigr|
 \le K_m\chi^{-1}h^{1/E_m}.
\]

The proof avoids integrating an arbitrary semialgebraic function. It
defines a minimal tube radius capable of covering a horizontal interval,
expresses the interval inclusion by a fixed-block first-order formula,
and applies the scalar modulus. Component count then converts the bound
to total vertical length.

This is a legitimate strategy. The final absorption of component counts,
`mT_0`, and small Euclidean thickenings into the already enormous budgets
is plausible.

Again, the estimate is not useful in the ordered central limit. For large
`E_m`, the power `h^{1/E_m}` is close to one unless `h` is fantastically
small, while `K_m` is enormous. The theorem quantifies a finite-count
fact; it does not show shrinking support in the collision limit.

## 10. Positive localization on the unchanged source

Module 136 partitions the original first-clearance source into

- a later low-incidence part;
- a retained source near the buffered critical overcover; and
- a determinant-controlled part away from that overcover.

The later low-incidence part is paid by the inherited inverse-incidence
density. The determinant-controlled part is paid by the physical area
formula. Exact labels are removed only for a positive upper bound and
then restored through their disjoint partition. The source normalization
`c_*^{-1}` occurs once.

The resulting height estimate outside the retained source is

\[
 C M A^m\left((m+1)\chi+
        K_m\varepsilon(\chi h)^{-E_m}\right).
\]

The mass of the retained source is bounded using the tube estimate and
the inherited weak `L^{145/144}` law.

The partition and normalization are coherent. The manuscript correctly
does not convert this mass estimate into an essential-height estimate.
The retained source remains exactly the obstruction.

## 11. Consequence of the v63 budgets for the ordered problem

The required raw-inversion order is

1. fix the reconstruction band `B`;
2. let the collision count tend to infinity;
3. enlarge `B` only afterwards.

For fixed `B`, the width `epsilon(B)` is a fixed positive number. The
threshold for module 136 cannot hold for all sufficiently large counts,
and the explicit error contains factors larger than exponential.

Therefore revision 63 does not yield a diagonal or subsequence within
the proved theorem. A choice of `B=B_m` large enough to offset `K_m`
would require spectral estimates at that growing band. The manuscript
has repeatedly and correctly refused to claim such estimates.

The value of revision 63 is consequently structural and reproducible:
it shows that the unspecified constants can be made explicit. It does
not provide a quantitative route to the title-level ordered limit.

## 12. Reversible closure of a normal-to-normal half-word

Module 137 starts from a critical point of the reduced endpoint action.
The endpoint momenta vanish. Reversal gives

\[
 P_z=S M_z^{-1}S M_z,
 \qquad S=\operatorname{diag}(1,-1),
\]

for the doubled regular orbit on the collision quotient.

The generating-function conventions are

\[
 p_0=-F_u,\qquad p_m=F_v.
\]

They lead to

\[
 b=-h_{01}^{-1},\quad
 a=-h_{00}/h_{01},\quad
 d=-h_{11}/h_{01},\quad
 c=-\det H_z/h_{01}.
\]

Direct multiplication gives

\[
 P_z=
 \begin{pmatrix}ad+bc&2bd\\2ac&ad+bc\end{pmatrix},
 \qquad \det(I-P_z)=-4bc.
\]

I checked these algebraic identities and found them correct. The period
need not be primitive, and no division by the word length belongs in the
coefficient.

The manuscript also correctly separates two roles of the doubled orbit.
The original displacement, occupation, return index, roof, and arithmetic
class are those of the first half-word. The doubled orbit supplies only
a reversible linearization.

## 13. The intrinsic quadratic coefficient

The endpoint source density is

\[
 w_z=|h_{01}|/(4\pi R c_*).
\]

The two-dimensional Morse pushforward coefficient is

\[
 J_z=\frac{2\pi w_z}{\sqrt{\det H_z}}
     =\frac{1}{2R c_*\sqrt{bc}}.
\]

Since `|det(I-P_z)|=4bc`, this gives

\[
 J_z=\frac{1}{R c_*\sqrt{|\det(I-P_z)|}}.
\]

For hyperbolic eigenvalues `lambda_z,lambda_z^{-1}`, this becomes

\[
 J_z=\frac{1}{R c_*}
       \frac{\lambda_z^{-1/2}}{1-\lambda_z^{-1}}.
\]

The square root is essential. An ordinary inverse periodic determinant
would have the wrong density scaling. The normalization in the text is
consistent with the common collision measure and the section factor.

## 14. Individual critical-weight decay

The manuscript proves

\[
 J_z\le C(47/53)^{m-2}
\]

for each regular critical word, without requiring a lower bound on all
interior incidences.

The estimate uses the off-diagonal endpoint Hessian entry and the
Neumann bound for the internal contact matrix. I found no immediate
algebraic error.

This result is useful but must not be overinterpreted. It is an
individual bound. The number of physical critical words and the number
which can share a short roof interval may grow exponentially. The base
`47/53` is not compared with a sharp critical-word entropy, and no
weighted cancellation is available because the measure is positive.
Thus the estimate alone gives no concentration of the sum.

## 15. Normal crossing weights

The crossing weight is

\[
 W_z=|\partial_u p_m(u,0)|_z^{-1}=|c|^{-1}.
\]

The relation

\[
 J_z=\frac{\sqrt{\det H_z}}{2R c_*}W_z
\]

is consistent with the generating-function matrix. The fixed-count
small-square trace follows by changing variables from `(u,p_0)` to
`(p_0,p_m)`.

This identifies a useful normal crossing measure. It does not establish
an interchange between the small-square limit and the long collision
limit. The manuscript states that restriction correctly.

## 16. Physical-side boundary interpretation

At a competing-hit seam the global billiard map can change its selected
first hit and need not be differentiable. The manuscript instead extends
the selected simple-root contact equations from the physical side and
uses their limiting Hessian and symplectic generating data.

This is the correct formulation. The matrix `P_z` at such a seam is a
branch expression, not the derivative of a globally defined singular
map. No source is placed on a nonphysical continuation.

A specialist should verify that every contact root used in this boundary
argument remains simple under the stated positive selected-incidence
hypothesis and that the endpoint curvature bounds persist up to the
physical-side closure.

## 17. The angular threshold lemma

For a perturbed linear form on the circle, the manuscript compares

\[
 q_r(\theta)=a\cdot\omega_\theta+O(r)
\]

with its linear part. The symmetric difference is contained in thin
neighborhoods of two cosine levels. Uniformly in the threshold, such a
neighborhood has angular measure `O(sqrt(r))`, including at the extrema
of cosine.

This gives the needed transition-uniform estimate. A linear error would
not be available at the endpoint `lambda=|a|`, so the square-root loss is
natural.

## 18. The simple seam density profile

Near a nondegenerate roof minimum, Morse coordinates give

\[
 F(\Phi(y))=t_z+|y|^2/2.
\]

The transformed source density at zero is `J_z/(2pi)`. If the physical
clearance side is `0<g<s`, polar coarea gives

\[
 b_{z,s}(t_z+h)
 =\int_0^{2\pi}\widetilde w(r\omega_\theta)
       \mathbf 1_{\{0<g(\Phi(r\omega_\theta))<s\}}\,d\theta,
 \qquad r=\sqrt{2h}.
\]

The radial Jacobian cancels the derivative of `r^2/2`; there is no
missing factor `r^{-1}`. The leading angular measure is

\[
 2\arcsin\min\{1,s/(\kappa_z\sqrt{2h})\}.
\]

Thus

\[
 b_{z,s}(t_z+h)
 =\frac{J_z}{\pi}
   \arcsin\min\{1,s/(\kappa_z\sqrt{2h})\}
   +O_z(J_z h^{1/4}).
\]

For fixed `s`, the one-sided limit is `J_z/2`. I found the coefficient,
transition scale, and error exponent internally consistent.

## 19. The original smooth first-clearance guard

The actual guard is zero below one scaled width and one above twice that
width. On a neighborhood where all other margins are strict, the
original first-clearance source is therefore bounded between the
positive strips

\[
 0<g<\varepsilon e'_j
 \quad\hbox{and}\quad
 0<g<2\varepsilon e'_j.
\]

Applying the local profile to these two strips gives a genuine bound on
the original source. The word, witness, image collision `j+1`, and exact
labels are not changed.

This is stronger than a tube-mass estimate: it identifies the local
height at a roof-critical seam.

## 20. Positive critical clusters

For disjoint source neighborhoods the local upper bounds sum with their
actual positive coefficients. The manuscript packages those coefficients
as the atomic measure

\[
 \mathfrak T_{n,k,m,R}
 =\sum_z\frac{\lambda_z^{-1/2}}{1-\lambda_z^{-1}}\delta_{t_z}.
\]

The local cluster estimate is

\[
 b^{\varepsilon,\mathcal S}(t)
 \le\frac{1/2+\delta}{R c_*}
        \mathfrak T_{n,k,m,R}([t-r,t]).
\]

This is the correct positive summation. Coincident critical values are
added rather than removed. There is no factor equal to the number of
words because the atomic measure already contains their weights.

The formula also identifies the remaining theorem precisely: a
normalized short-interval concentration estimate for this positive
atomic measure.

## 21. The conditional ordered transfer

The manuscript proves that a fixed-band local height would follow if
both of the following held uniformly at large collision count:

1. the selected neighborhoods covered the relevant original source and
   remained valid for the fixed width `epsilon(B)`, with shrinking Morse
   radii and controlled local errors; and
2. the reversible atomic measures satisfied the normalized shrinking-
   interval concentration estimate.

This implication is logically correct and respects the order of limits.
It is conditional, not a new Lorentz theorem.

Neither premise is supplied. In particular, a fixed band does not imply
`epsilon(B)<epsilon_z` uniformly over long words. The admissible local
width may shrink faster than any available control. Likewise, no theorem
connects the existing annular spectral averages or periodic arithmetic
to the positive measure `mathfrak T` at a specified collision count and
exact label.

## 22. Width-uniform affine guard comparison

Module 139 keeps the affine offset

\[
 \beta+r a\cdot\omega
\]

rather than replacing every active margin by a homogeneous linear form.
This matters when a nonzero margin is small compared with the physical
guard width.

The Stieltjes representation of the monotone guard reduces its difference
to threshold disagreements. The circle-level estimate is uniform in the
threshold, so the final error is independent of the width and offset.
Products, minima, and Boolean formulas are paid by the sum of the scalar
input errors.

This argument is sound. It avoids an unjustified assumption that fixed
`epsilon` is smaller than every nonzero margin of a long word.

## 23. Physical margins and exact labels

The local disk retains a finite list of near-clearance margins and
section-edge margins. Each retained scalar margin is assumed to have a
nonzero individual gradient. No determinant formed from two different
boundary gradients is required.

The exact label is reconstructed from

- initial section membership;
- section visits at collisions `0,...,m-1`;
- terminal section membership at collision `m`;
- the selected displacement word; and
- the physical first-hit signs.

For every sign pattern, at most one pair `(n,k)` is assigned. This remains
true for affine sign patterns which are not physically realized; no
measure is assigned to those auxiliary patterns.

A specialist should verify the claim that composition of every section
edge function with the selected regular collision branch has nonzero
gradient in the chosen endpoint/Morse coordinates. This follows if the
intermediate-state map used there is indeed a local diffeomorphism on the
whole disk, but that dependency should be stated at theorem level.

## 24. The full affine exact-label profile

The angular reference profile is an explicit integral of the affine
margin signs and the inherited smooth guard. The main estimate is

\[
 \sum_{n,k}\left|b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+h)
  -\frac{J_z}{2\pi}\mathcal A_{z,n,k}(\varepsilon,h)\right|
 \le C_zJ_zh^{1/4}.
\]

The absence of a label-count factor is justified. On the set where an
input sign differs, both the original and affine output vectors are zero
or a single unit vector; their `ell^1` distance is at most two.

The explicit local error budget

\[
 C_z=C\left(1+W_z+
          \sum_f\sqrt{L_f/A_f}\right)
\]

makes the finite-jet dependence visible. This is preferable to hiding it
inside an unspecified local constant.

The estimate remains local. No lower bound for `A_f`, upper bound for
`L_f`, or relative density derivative is given uniformly over all words
as the collision count grows.

## 25. Multiple-seam angular traces

At fixed positive width, zero margins are replaced in the limit by the
signs of their linear parts, while nonzero margins retain their constant
sign. Dominated convergence gives

\[
 \lim_{h\downarrow0}
 b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+h)
 =\frac{J_z}{2\pi}|\mathcal C_{z,n,k}|.
\]

The angular sets may be empty. Coincident or parallel gradients are
allowed, and no inverse determinant of a boundary-gradient matrix is
introduced. A simple seam gives one half; a quadrant gives one quarter.

This is a useful exact local description of the retained caustic source.
It does not classify all physical caustic germs or establish count-uniform
coverage.

## 26. What revision 65 closes

Relative to the revision-62 report, the combined v63/v65 packet closes
or clarifies the following finite-count matters.

- The semialgebraic separation and tube constants are replaced by
  explicit collision-count and cap budgets for a specified buffered
  overcover.
- The overcover/source distinction is made precise.
- The intrinsic roof-critical coefficient is identified by reversible
  monodromy with the correct square root and original normalization.
- An individual critical weight has a uniform exponential upper bound.
- The actual density inside a simple roof-critical clearance seam is
  calculated across the width-to-roof transition.
- The original smooth first-clearance guard is controlled by the local
  profile.
- Coincident critical values are organized by a positive atomic measure.
- Several simultaneous clearance seams and section junctions receive an
  affine exact-label vector profile.
- The finite-jet error and exact-label bookkeeping are explicit.
- The extra long-count inputs needed for an ordered transfer are isolated
  in theorem form.

These are genuine advances in the local geometry of the original source.

## 27. What revision 65 does not close

The following title-level matters remain open.

### 27.1 The incidence height

The first-incidence source still has only a finite-count estimate with an
exponential count factor. The reversible clearance coefficient does not
bound the complete incidence source at the normalized pointwise scale.

### 27.2 The complete clearance height

Only selected roof-critical germs are evaluated. The complete positive
clearance source includes uncovered germs, selected grazing, noncritical
roof-rank degeneracy, and regions without count-uniform local constants.

### 27.3 Critical-weight concentration

No theorem bounds

\[
 m^2\mathfrak T_{B,n,k,m,R}([t-h,t+h])
\]

uniformly in the exact labels, radius, and long collision count as
`h` tends to zero after the collision limit.

### 27.4 Uniform neighborhood coverage

The Morse radii, guard admissibility widths, incidence caps, scalar
gradient lower bounds, and finite-jet constants are not controlled over
all relevant long words.

### 27.5 The unrestricted pointwise theorem

Without the two positive height limits, total variation, local `L^q`,
weak endpoint, all-resolution good-set results, and local caustic profiles
do not imply

\[
 \sup_{R,n,k}
 \operatorname*{ess\,sup}_{u\text{ central}}
 |m^2p_{n,R}(k,m,u)-\mathcal L_{m,R}(k_1,k_2,u,n)|\to0.
\]

A positive spike can have a known local shape and small mass while the
sum of many such spikes still has uncontrolled height.

### 27.6 Pointwise conditional consequences

Unrestricted same-roof bridges, pointwise roof-conditioned paths, and
forward essential likelihood still require a positive pointwise
reference denominator and the complete scalar height theorem.

## 28. Arithmetic modulation

The canonical finite arithmetic kernel remains the reference. At a fixed
radius, the finite residue and its zero classes remain. Revision 65 does
not prove that the arithmetic factor is identically one.

This is mathematically honest and should not be changed. A zero
arithmetic class must not be assigned a conditional Gaussian law or a
likelihood. The new local geometry neither removes nor alters the
arithmetic modulation.

## 29. Relation to existing methods and significance

The manuscript appropriately identifies the general ingredients as
classical or standard:

- reversible Hill-type determinant identities;
- Morse coordinates and polar coarea;
- one-dimensional angular threshold estimates;
- semialgebraic component bounds;
- effective real quantifier elimination; and
- layer-cake conversion of weak integrability to mass bounds.

The paper-specific achievement is their implementation on the original
Lorentz first-defect source with its exact labels, half-open occupation,
image-side witness, section normalization, finite arithmetic kernel, and
positive complements.

This is substantial specialist work if the entire inherited continuum
chain withstands expert scrutiny. It is not yet a persuasive top-four
package. The strongest new theorem is local and finite-word. The global
pointwise theorem remains conditional on a new concentration principle
which is neither proved nor realized in another comparable singular
system.

The article also remains extraordinarily long and dependency-heavy. Its
one-hundred-thirty-nine-module architecture includes many valuable
integrated and model theorems, but the editorial claim continues to be
governed by an unproved endpoint. At a top-four venue, either that endpoint
must be completed or the paper must be reorganized around a smaller set
of complete theorems of independently compelling breadth.

## 30. Independent specialist verification

No independent human specialist audit has been obtained. The following
new and inherited points remain especially load-bearing.

1. The exact collision-graph encoding and first-jet equations on capped
   weak-first-hit overcovers.
2. The stated quantifier-block, degree, atom, and coefficient-height
   bounds in module 135.
3. Application of the pinned effective quantifier-elimination theorem to
   the infimum graphs used for separation and tubes.
4. Compactness and finite-fiber arguments through weak first-hit seams.
5. The physical area formula and multiplicity bound for the unchanged
   first-clearance source.
6. The endpoint generating-function signs in module 137.
7. The factor four and square-root determinant in the reversible weight.
8. Uniform endpoint Hessian bounds without an interior incidence margin.
9. The physical-side branch interpretation at a competing-hit seam.
10. The Morse coordinate density and polar coarea normalization.
11. Uniform angular estimates at the arcsine transition.
12. The original guard sandwich and first-defect ordering.
13. Nonvanishing of every retained clearance and section margin gradient.
14. Exact occupation and terminal-membership bookkeeping in the Boolean
    label formula.
15. The common source versions used when summing vector-valued density
    profiles.
16. The complete inherited positive raw-error identity.
17. The missing uniform neighborhood coverage theorem.
18. The missing reversible atomic concentration theorem.
19. The relation of those positive weights to the existing peripheral
    spectral and periodic arithmetic information.
20. The complete ordered incidence and clearance limits.

The exact-source workflows and finite fixtures do not replace this audit.

## 31. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the
following matters.

### 31.1 Prove uniform source coverage

Give a theorem covering every relevant first-clearance caustic point at
fixed reconstruction band and all sufficiently large collision counts.
The theorem must quantify Morse radii, admissible guard widths, selected
incidence bounds, scalar-gradient lower bounds, second-jet bounds, and
relative source-density derivatives.

### 31.2 Prove reversible-weight concentration

Establish

\[
 \lim_{h\downarrow0}\limsup_{m\to\infty}
 \sup_{R,n,k,t}m^2
 \mathfrak T_{B,n,k,m,R}([t-h,t+h])=0
\]

for every fixed band, or prove a stronger statement which directly pays
the complete critical cluster. Individual word decay is insufficient.

### 31.3 Cover the positive complement

Handle selected grazing, noncritical-roof rank degeneracy, multiple
contacts not satisfying the local hypotheses, and every source component
outside the verified neighborhoods. No small-mass deletion is permitted
in a pointwise height theorem.

### 31.4 Complete the incidence height

Prove the ordered normalized first-incidence height on the same exact
labels and original source. The current finite-count exponential estimate
is not enough.

### 31.5 Complete the clearance height

Combine the local profiles and the remaining geometric pieces into the
ordered normalized complete-clearance estimate without reversing the
fixed-band limit.

### 31.6 Derive the unrestricted pointwise theorem

Only after the two positive heights are controlled should the paper state
the unrestricted two-sided arithmetic raw-density theorem and its
pointwise conditional consequences.

### 31.7 Connect geometry and dynamics

If the reversible atomic measure is to be controlled by existing spectral
or periodic information, state and prove the exact bridge. Mean-square
annular averages, an averaged return count, and a specified positive
critical trace are different objects and cannot be identified without a
new theorem.

### 31.8 Normalize qualification metadata

Trigger and record the exact-SHA workflow on both final author refs if
two-ref qualification is claimed. The current response ref succeeded;
no separate v65 copy-ref run was returned by the repository API.

### 31.9 Obtain independent expert review

The collision geometry, anisotropic operator theory, semialgebraic
complexity, reversible determinant, and local coarea chain require human
specialists.

### 31.10 Reduce the journal proof burden

Present the shortest complete route to one principal theorem. Extensive
historical pipelines, validation ledgers, conditional endpoint routes,
and model realizations may remain in companions or appendices, but should
not obscure which theorem is actually complete.

## 32. Technical and presentation comments

1. Keep the reconstruction band, physical guard width, roof distance,
   incidence cap, Morse radius, and collision count visibly distinct.
2. State on every use whether the source is physical, an algebraic
   overcover, or a physical restriction defined by distance to an
   overcover.
3. Preserve the cap buffer `chi` versus `chi/2` in module 135.
4. Do not describe the effective budgets as useful asymptotic rates.
5. Note explicitly that the v63 threshold fails eventually for fixed
   positive width.
6. Keep the square root in the reversible determinant.
7. Keep the original half-word labels separate from the doubled orbit.
8. Do not divide the reversible weight by a primitive period or a cyclic
   multiplicity.
9. At singular seams, call `P_z` a physical-side branch expression, not
   the derivative of the global billiard map.
10. Keep the distinction between the full quadratic coefficient `J_z`
    and its one-sided fraction.
11. Retain the exact arcsine transition rather than replacing it by its
    far-tail approximation near the threshold.
12. State that local density identities hold for coarea representatives
    almost everywhere in the roof.
13. Keep the original two guard widths `epsilon e'_j` and
    `2 epsilon e'_j` separate.
14. Keep coincident critical values in the positive atomic measure.
15. Do not infer cluster concentration from single-word decay.
16. State every local constant which can depend on the word.
17. Preserve affine offsets in the multiple-margin theorem.
18. Do not impose a determinant condition between two boundary gradients
    when only their individual nonvanishing is proved.
19. Keep initial, occupation, and terminal section decisions separate.
20. Retain the `ell^1` label-vector argument which avoids a target-count
    factor.
21. Do not convert the angular profile into a probability; it is a
    coefficient in an unnormalized source density.
22. Keep tube mass, source mass, essential height, and atomic trace as
    four different objects.
23. State the conditional nature of the ordered trace transfer in every
    theorem-level summary.
24. Do not choose a reconstruction band depending on the collision count
    unless a new growing-band spectral theorem is proved.
25. Keep the finite arithmetic factor and zero classes in the main term.
26. Do not assign conditional laws on zero reference classes.
27. Keep probability total variation, variation mass, and path
    bounded-Lipschitz dual norms distinct.
28. Preserve the image mark `j+1` for clearance.
29. Keep all later incidences after a first clearance in the physical
    source partition.
30. Separate source qualification and finite fixtures from continuum
    proof certification.
31. Record that the v64 branch was an alias rather than a separate
    theorem-bearing revision.
32. State clearly which parts of the article are complete results and
    which are conditional transfer routes.

## 33. Final assessment

Revision 65 is a serious mathematical response to the revision-62
report.

Revision 63 makes the finite-count caustic constants explicit through a
buffered algebraic overcover and effective real quantifier elimination.
Revision 65 calculates the physical density inside part of the retained
caustic source. It derives the reversible square-root weight with the
correct original normalization, proves a transition-uniform arcsine
profile, controls the original smooth guard, organizes critical clusters
as a positive atomic measure, and gives an affine exact-label profile for
multiple seams and section junctions.

I found no decisive algebraic, coarea, normalization, or exact-label
error in modules 135--139. Subject to specialist verification, these are
credible and useful finite-word theorems.

They do not, however, close the manuscript's principal endpoint. The
v63 budgets are unusable in the fixed-band collision limit. The v65
formulas require uniform long-word neighborhood coverage and a normalized
critical-weight concentration theorem which remain unproved. The complete
incidence source and substantial positive clearance complements also
remain outside the local profiles.

The unrestricted pointwise raw-density law, unrestricted same-roof
bridges, and forward essential likelihood therefore remain open. The
article is still highly model-specific, extraordinarily large, and
without independent expert certification.

**Final recommendation: reject in the present form at the requested
four-journal benchmark.**

A focused specialist-journal article centered on reversible caustic
weights, the local arcsine/affine profiles, and the effective finite-count
localization could be valuable if the geometric chain survives expert
audit. A new top-four review of the unified paper should begin only after
the long-count source-coverage and critical-cluster concentration
problems have been solved, or after the work has been reorganized around
a different complete theorem of comparable breadth.
