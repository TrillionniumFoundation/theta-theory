# External top-four referee report on A2-DYN revision 66

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v66-referee-response-2026-10-10`, `revision/a2-dyn-v66-referee-copy-2026-10-10`  
**Reviewed commit:** `e96761c0b12dbc46c187f4aeb4ee8d537863dec5`  
**Reviewed repository tree:** `cfd741f950117fa8d304843f14bf0179fa54740b`  
**Complete revision-66 paper tree:** `fdf737e94888a540c05d86c458d77b500895e713`  
**Ordinary source payload tree:** `7d397d8fe8b5dac3a6e08f461dab71b0483de3cf`  
**Active manuscript directory:** `papers/A2-DYN-v66-referee-response`  
**Active mathematical source:** one hundred forty-two numbered core modules; revision 66 retains all one hundred thirty-nine revision-65 modules and adds modules 140--142  
**Frozen revision-65 author baseline:** `04f38424177533db60dfd13c3052381dc0adb481`  
**Frozen revision-65 complete paper tree:** `897816d34b3d012fb93feaf532dcf64740723d83`  
**Controlling external report:** `reviews/a2-dyn-v65-external-top4-review-2026-10-10/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `8f5b4dd2b2b12b7454b3ebdfa0e41546ba7f6908` / `2b2f7798f7c6eefa23c9c0a27368fd53df907442`  
**Date:** 10 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 66 is a genuine theorem-bearing advance over revision 65. The preceding report identified two particularly sharp obstructions in the critical-source route:

1. the available local Morse charts did not have a collision-count-uniform radius and distortion budget on a sufficiently large part of the original physical source; and
2. the manuscript had not connected its local reversible coefficients to a dynamical concentration theorem without multiplying an individual coefficient estimate by an uncontrolled number of critical words.

Revision 66 substantially advances both points.

The new manuscript proves an incidence-normalized inverse estimate for the contact matrix,

\[
 |(A^{-1})_{ij}|\le C\min(c_i,c_j)q^{|i-j|},
 \qquad q=47/53,
\]

and uses it to construct selected-contact continuations with collision-count-uniform weighted jets under the tapered incidence condition

\[
 c_j\ge \chi q^{\min(j,m-j)/4}.
\]

The construction is allowed to cross clearance and section seams at the level of the selected contact equations, while the actual first-hit, section, occupation, terminal and exact-label decisions remain as zero-one masks in the original source integral. This is a conceptually appropriate separation between a smooth coordinate continuation and the physical orbit set.

The resulting Morse chart has radius

\[
 r_\chi=r_0\chi^3
\]

and relative density distortion

\[
 \left|\log\frac{2\pi\widetilde w_z(y)}{J_z}\right|
 \le C\chi^{-2}|y|,
\]

uniformly in the word length. The physical source is then evaluated by an exact nonlinear angular integral, without replacing first-hit or section decisions by their affine tangent cones and without dividing by a small physical-boundary gradient.

Most importantly, revision 66 constructs a positive finite-width physical collar trace

\[
 \mathcal Q_{m,s;n,k,R}
 =\sum_z\left(\frac1s\int_0^s
 b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+u)\,du\right)\delta_{t_z}
\]

and proves the ordered bound

\[
 \limsup_{m\to\infty}\sup_{R,n,k,t}
 m^2\mathcal Q_{m,s;n,k,R}([t-h,t+h])
 \le C(2h+s),
\]

for fixed widths before the collision-count limit. This estimate is obtained by a positive comparison with the inherited exact-label two-normal-endpoint local law. It permits coincident critical values and changing exact labels and does not introduce a word-count multiplier. This is a real geometry-to-dynamics bridge, not another finite-word coefficient estimate.

I audited the new modules

- `core/140_tapered_contact_continuation.tex`;
- `core/141_uniform_physical_angular_source.tex`;
- `core/142_physical_collar_trace_bridge.tex`;

and their use in the new front matter. I also checked the inherited contact matrix and source normalization, the reversible square-root coefficient, the exact-label partition, and the two-strip local theorem used in the collar comparison.

I found no decisive counterexample, missing section factor, incorrect image mark, invalid label averaging, erroneous polar-coarea factor, hidden word-count multiplier, or reversal of the proved order of limits in the new chain. In particular:

1. the Neumann-series estimate retains one endpoint incidence, and symmetry supplies the minimum of the two incidences;
2. the row-normalized internal Hessian has a collision-count-uniform inverse in the tapered weighted norm;
3. the nonlinear derivative exponents are summable under the stated taper;
4. the selected-contact continuation is not represented as a physical continuation across a seam;
5. the Morse transformation is exact and the density estimate is relative, so no lower bound for the exponentially small coefficient `J_z` is needed;
6. the first-clearance multiplier has a count-uniform Lipschitz bound after its geometrically tapered widths are included;
7. exact labels form a pointwise partition, so summing the profile errors does not cost the number of output labels;
8. in the collar comparison the two endpoint-strip widths are `O(sqrt(s))`, whose product supplies the required factor `s`;
9. the roof window has the correct length `2h+s`; and
10. the fixed-count zero-width limit is explicitly kept separate from the collision-count limit.

These are meaningful improvements, and the finite-width trace theorem appears internally coherent subject to specialist verification of the inherited continuum inputs.

The negative top-four recommendation is nevertheless unavoidable because revision 66 proves concentration for the finite-width trace `Q`, not for either of the two zero-width measures which govern the pointwise endpoint.

The physically observable zero-width trace is

\[
 \mathcal B_{m;n,k,R}
   =\sum_z J_z\theta_{z,n,k}\,\delta_{t_z},
\]

where `theta` is the exact physical and exact-label angular fraction. The manuscript proves only

\[
 \mathcal B_m(I)
 \le e^{C\chi^{-2}\sqrt{2s}}\mathcal Q_{m,s}(I)
       +\mathcal D_{m,s}(I),
\]

where `D` is the positive angular loss between the finite-radius nonlinear angular set and its tangent fraction. The required estimate

\[
 \lim_{s\downarrow0}\limsup_{m\to\infty}
 \sup_{R,n,k,t}m^2\mathcal D_{m,s;n,k,R}([t-1,t+1])=0
\]

is stated but not proved.

This is not a cosmetic remainder. At each fixed collision count, dominated convergence gives the tangent fraction. It gives no uniform rate as the number of physical and section decisions grows, their gradients become small, their tangent directions coalesce, or their nonlinear zero sets enter the shrinking circles. Uniform contact jets control the selected contact coordinates; they do not by themselves control the angular complexity of all physical masks. The angular-loss term records exactly the missing interchange between the zero-width and long-count limits.

Moreover, the verified charts do not cover the complete positive boundary source. The explicit outside source still includes tapered-incidence violations, selected grazing, noncritical roof-rank components, points not lying in the specified normal critical disks, removed chart annuli, and other first-defect pieces. The complete first-incidence height is also unchanged and unproved in the ordered central regime.

Consequently revision 66 still does not prove

- the complete ordered incidence height;
- the complete ordered clearance height;
- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof collision/return bridges;
- forward essential-likelihood convergence; or
- the unrestricted pointwise roof-conditioned path theorem.

These remain the endpoint around which the title, positive-error identity, and much of the one-hundred-forty-two-module article are organized.

At the requested benchmark, the article would need either

1. a proof of the angular-loss estimate together with ordered control of the chart complement and complete incidence source, thereby closing the unrestricted pointwise theorem; or
2. a substantially broader theorem, with independently verifiable hypotheses and multiple genuinely different singular-hyperbolic applications, whose significance does not depend on the unfinished Lorentz endpoint.

Revision 66 provides neither yet. No independent human specialist audit has been obtained.

My assessment is therefore positive about the new count-uniform coordinates and finite-width trace theorem, but negative about readiness for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`e96761c0b12dbc46c187f4aeb4ee8d537863dec5`.

The repository tree at that commit is

`cfd741f950117fa8d304843f14bf0179fa54740b`.

The active article is

`papers/A2-DYN-v66-referee-response`.

The ordinary source payload tree recorded in the manifest is

`7d397d8fe8b5dac3a6e08f461dab71b0483de3cf`.

The complete paper tree recorded by the revision index is

`fdf737e94888a540c05d86c458d77b500895e713`.

The immediate mathematical baseline is revision 65 at

`04f38424177533db60dfd13c3052381dc0adb481`.

The controlling report is the revision-65 report at

`8f5b4dd2b2b12b7454b3ebdfa0e41546ba7f6908`.

Revision 66 begins from the frozen review state and adds modules 140--142 together with new front matter, source manifests, validation material and provenance snapshots. The source manifest records

- all 139 inherited core modules byte-identical;
- all 191 inherited Python files byte-identical;
- the bibliography byte-identical;
- every inherited appendix retained;
- every inherited mathematical label retained;
- the old abstract and introduction compiled in `appendices/v65_frontmatter.tex`;
- the old complete main source retained in provenance;
- `lorentz_tapered_selected_contact_jets_proved: true`;
- `lorentz_tapered_uniform_morse_charts_proved: true`;
- `lorentz_nonlinear_physical_profile_proved: true`;
- `lorentz_ordered_physical_collar_trace_proved: true`;
- `lorentz_uniform_angular_loss_proved: false`;
- `lorentz_complete_source_coverage_proved: false`;
- `uniform_reversible_critical_trace_concentration_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- and `independent_human_review: false`.

These flags accurately distinguish the new finite-width theorem from the unproved zero-width and complete-source endpoints.

The present review branch begins directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v66-external-top4-review-2026-10-10/`.

No author manuscript source, workflow, prior review, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA revision-66 qualification completed successfully on both reviewed author refs:

- response run `38048022331`;
- referee-copy run `38048027247`.

Both runs identify the reviewed SHA

`e96761c0b12dbc46c187f4aeb4ee8d537863dec5`.

The validation protocol checks

- the frozen revision-65 complete paper tree;
- the controlling revision-65 report blob;
- all 139 inherited core files;
- all 191 inherited Python files;
- all 142 compiled core modules;
- every inherited appendix and mathematical label;
- the unchanged bibliography;
- the ordinary source payload and workflow hashes;
- normal and optimized finite diagnostics;
- native TeX compilation without shell escape;
- stabilized cross-references and warning-free typesetting; and
- theorem-label-based rendering of the new proof pages.

The new finite fixtures test the weighted tridiagonal inverse, tapered norms, clearance-guard products, polar coarea, positive angular-loss inequalities and source partitions. A deliberate negative control distinguishes bounded contact jets from a uniform angular-loss conclusion.

These are useful source, algebra and typesetting checks. They do not certify

- the inherited contact Hessian and endpoint-curvature formulas;
- the physical collision graph and first-hit encoding;
- the anisotropic transfer-operator and arithmetic local laws;
- the reversible square-root determinant identity;
- the count-uniform physical mask complexity;
- the angular-loss estimate;
- the complete incidence or clearance heights; or
- the unrestricted pointwise local limit theorem.

The manuscript and its validation files state this limitation accurately.

## 4. Scope of this review

I did not attempt to re-prove all 142 core modules. The substantive audit concentrates on the mathematics that can change the revision-65 assessment:

1. the refined inverse estimate for the tridiagonal contact matrix;
2. row normalization by frozen incidences;
3. the tapered weighted norm;
4. mixed endpoint and internal nonlinear estimates;
5. quantitative continuation in a dimension growing with the word length;
6. preservation of positive selected reflection signs;
7. construction of a count-uniform Morse disk;
8. relative, rather than absolute, source-density distortion;
9. interpretation of the reversible coefficient on the physical side of a seam;
10. exact physical masking of nonphysical continuations;
11. the first-clearance guard and its geometric depth weights;
12. the nonlinear angular coarea formula;
13. summation over exact labels without a label-count factor;
14. disjointness of the physical chart restrictions;
15. the positive outside-source partition;
16. construction of the finite-width trace `Q`;
17. the endpoint-strip comparison with the exact-label local theorem;
18. the order of the `m`, `h`, and `s` limits;
19. the fixed-count zero-width coefficient;
20. the physical angular fraction;
21. the positive atomic-to-collar comparison;
22. the unproved angular-loss input;
23. the distinction between traces `Q`, `B`, and `T`;
24. source preservation and workflow evidence; and
25. the unchanged top-four endpoint.

The inherited modules 1--139 are treated as a source-pinned baseline, not as independently recertified mathematics. Their load-bearing continuum claims remain subject to the specialist-audit requests in earlier reports.

## 5. The incidence-normalized contact inverse

Let `A` be the positive tridiagonal contact matrix used in the inherited endpoint action calculation, and write

\[
 A=D(I-K).
\]

The diagonal inverse satisfies

\[
 D_{jj}^{-1}\le \frac{R c_j}{2}.
\]

The matrix `K` is nonnegative, connects only neighboring indices, and has row sums at most

\[
 q=47/53<1.
\]

Therefore

\[
 (I-K)^{-1}=\sum_{r\ge0}K^r,
\]

and a path from index `i` to index `j` needs at least `|i-j|` steps. The manuscript obtains

\[
 |(A^{-1})_{ij}|\le Cc_jq^{|i-j|}.
\]

Since `A` is symmetric, the same bound holds with `c_i`; taking their minimum gives

\[
 |(A^{-1})_{ij}|\le C\min(c_i,c_j)q^{|i-j|}.
\]

Dividing the `i`th row by `c_i` gives

\[
 |(D_c^{-1}A^{-1})_{ij}|\le Cq^{|i-j|}.
\]

For weights

\[
 \omega_j=\sigma^{d_j},
 \qquad \sigma=\sqrt q,
 \qquad d_j=\min(j,m-j),
\]

the inequality

\[
 |d_i-d_j|\le |i-j|
\]

makes the corresponding weighted row sums geometric with ratio `q/sigma=sqrt(q)<1`. Thus

\[
 N=A D_c
\]

has an inverse uniformly bounded in the stated weighted norm.

I find this calculation correct, assuming the inherited decomposition `A=D(I-K)` and row-sum bound. It is a useful refinement because it replaces the product of inverse incidences by a single local incidence which is then removed by row normalization.

A specialist should nevertheless verify the precise convention for internal versus endpoint incidences and the identity

\[
 D_yE=D_c A D_c
\]

at every selected physical-side word. That identity is inherited and is load-bearing here.

## 6. Count-uniform selected-contact continuation

The stationary equation at contact `j` is divided by its frozen base incidence `c_j^0`. The resulting derivative in the internal contact variables is

\[
 D_yG=A D_c=N.
\]

The frozen choice is important: differentiating a variable normalization would produce additional terms not covered by the displayed inverse estimate.

Each unscaled stationary equation depends only on three adjacent contacts. Its fixed-order derivatives are bounded by the positive minimum flight length and do not divide by incidence. If the inputs have weighted norm one, division by the frozen incidence gives

\[
 \omega_j^{-1}|D^rG_j[v_1,\ldots,v_r]|
 \le C_r\chi^{-1}
 q^{((r-1)/2-1/4)d_j}.
\]

For every `r>=2` the exponent is nonnegative. This supplies collision-count-uniform nonlinear bounds. A contraction argument then gives

\[
 \|D^r y_j\|\le C_r\chi^{1-r}\sigma^{d_j},
 \qquad r=1,2,3.
\]

The theorem ultimately restricts the endpoint square to radius `a_0 chi^3`. On this smaller square, the incidence variation is bounded by

\[
 C\chi^3q^{d_j/2},
\]

while the base incidence is at least

\[
 \chi q^{d_j/4}.
\]

Their ratio is at most `C chi^2 q^{d_j/4}`, so reducing `a_0` preserves at least half of every selected incidence. This part of the scale choice is coherent.

The continuation solves the selected reflection equations only. It is not required to satisfy the physical first-hit inequalities or section decisions. The manuscript consistently assigns zero source weight to every nonphysical point later. I regard this as legitimate: one may use a smooth overchart for coordinates without placing physical probability on the continuation.

The principal specialist question is whether all mixed endpoint/internal derivatives invoked by the contraction have the stated weighted bounds uniformly in the growing dimension. The local support of the equations makes the claim plausible, but it should be checked directly against the selected contact convention.

## 7. Uniform Morse coordinates and the relative density

The endpoint reduced action has a uniformly positive definite Hessian on the selected continuation, using the inherited endpoint Schur-complement bounds. Contact jets through order three give endpoint-action derivatives through order four bounded by

\[
 C\chi^{-2}.
\]

The manuscript uses the exact quadratic construction

\[
 Q_z(x)=2\int_0^1(1-s)\nabla^2F_z(sx)\,ds,
 \qquad y=Q_z(x)^{1/2}x.
\]

Since

\[
 F_z(x)-F_z(0)=\frac12x^{\mathsf T}Q_z(x)x,
\]

this gives the exact identity

\[
 F_z(\Phi_z(y))=t_z+|y|^2/2.
\]

On an endpoint square of radius `O(chi^3)`, the derivative of the map remains uniformly close to its value at zero; this yields an image disk of radius `r_0 chi^3`.

The source coefficient

\[
 w_z=|F_{uv}|/(4\pi R c_*)
\]

may be exponentially small with the word length, so an absolute derivative estimate would be unsuitable. The manuscript instead differentiates `log w_z`. The refined diagonal inverse makes each incidence-potential term proportional to

\[
 |dc_j|/c_j,
\]

and the tapered derivative bounds give a summable series

\[
 C\chi^{-1}\sum_jq^{d_j/4}.
\]

Together with the Morse Jacobian this produces

\[
 |D\log\widetilde w_z|\le C\chi^{-2}.
\]

Hence

\[
 e^{-C\chi^{-2}|y|}\frac{J_z}{2\pi}
 \le \widetilde w_z(y)
 \le e^{C\chi^{-2}|y|}\frac{J_z}{2\pi}.
\]

This relative estimate is the correct topology for a coefficient which itself decays with the orbit length. I found no missing word-count factor in the logarithmic derivative calculation.

The identity

\[
 \widetilde w_z(0)=J_z/(2\pi)
\]

uses the inherited reversible determinant formula. The present report does not independently recertify that formula.

## 8. Exact physical masks and the clearance guard

The mask `B_{z,n,k}` is defined from the actual selected positions and velocities. It requires

- the selected word to be the actual first-hit word;
- the original initial section membership;
- the original terminal section membership;
- the original half-open occupation convention;
- and the exact return and displacement labels.

Pointwise,

\[
 0\le\sum_{n,k}B_{z,n,k}(y)\le1.
\]

Thus exact labels are not frozen to the singular center and no label-count factor appears when the vector profile is summed.

For `epsilon<=chi/4`, all selected incidence guard factors equal one throughout the common chart. The flight-`j` clearance has a Lipschitz constant of order

\[
 q^{d'_j/2},
 \qquad d'_j=\min(j,m-1-j),
\]

while its guard width is

\[
 \varepsilon q^{d'_j/4}.
\]

The corresponding guard Lipschitz constant is therefore

\[
 C\varepsilon^{-1}q^{d'_j/4}.
\]

Summation over the flights is a geometric series independent of `m`. Taking a minimum over a fixed candidate list does not increase the Lipschitz constant beyond the maximum of the individual constants. This gives the claimed count-uniform bound for the first-clearance multiplier.

If one competing clearance vanishes at the critical center, then on a sufficiently small physical disk the relevant flight guard is zero, the incidence guards remain one, and the complete first-defect telescoping sum equals one. This saturation argument is compatible with simultaneous seams and later defects because it uses the unchanged product identity rather than deleting tests.

I found this guard calculation coherent. A specialist should check that the candidate list used off the physical set remains uniformly finite on the selected continuation and that the inherited signed image-side clearance has exactly the stated endpoint-influence bound.

## 9. The nonlinear physical angular profile

The manuscript defines

\[
 A_{z,n,k}^{\varepsilon}(h)
 =\int_0^{2\pi}
 B_{z,n,k}(\sqrt{2h}\,\omega_\theta)
 D_z^\varepsilon(\sqrt{2h}\,\omega_\theta)\,d\theta.
\]

This is the actual nonlinear angular set, not an affine approximation. The pushforward density is

\[
 b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+h)
 =\int_0^{2\pi}
 \widetilde w_z(\sqrt{2h}\,\omega_\theta)
 B_{z,n,k}(\sqrt{2h}\,\omega_\theta)
 D_z^\varepsilon(\sqrt{2h}\,\omega_\theta)\,d\theta.
\]

The radial factor in planar polar area cancels the derivative of `r^2/2`, so no extra power of `h` is missing. Positivity and the relative density bound give

\[
 e^{-K_\chi\sqrt{2h}}
 \frac{J_z}{2\pi}A_{z,n,k}^{\varepsilon}(h)
 \le b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+h)
 \le e^{K_\chi\sqrt{2h}}
 \frac{J_z}{2\pi}A_{z,n,k}^{\varepsilon}(h).
\]

Since the exact-label masks form a pointwise partition,

\[
 \sum_{n,k}A_{z,n,k}^{\varepsilon}(h)\le2\pi.
\]

Therefore the summed vector error is at most

\[
 C K_\chi J_z\sqrt h.
\]

The product `K_chi r_chi` is bounded, so the exponential remainder is controlled on the whole common disk.

This theorem is a useful correction to the affine-profile route: it avoids dividing by an arbitrarily small boundary gradient. It deliberately leaves the angular integral unevaluated. That is mathematically honest, but it also identifies the remaining long-count problem.

## 10. Physical chart disjointness and the positive complement

At fixed collision count, different regular center words give disjoint itinerary events. For a selected word the normal critical point is unique by the inherited strict convexity argument. After assigning seam overlaps consistently, the physical chart restrictions can therefore be summed without a word-count factor.

The manuscript defines

\[
 b^{\varepsilon,\mathrm{clr}}
 =b^{\varepsilon,\chi,\mathrm{chart}}
  +b^{\varepsilon,\chi,\mathrm{outside}},
 \qquad b^{\varepsilon,\chi,\mathrm{outside}}\ge0.
\]

The outside source explicitly includes

- violations of the tapered incidence envelope;
- selected-grazing neighborhoods;
- noncritical roof-rank components;
- physical states outside the specified Morse disks;
- and annuli removed when a chart is shortened.

This partition is important. The new coordinate theorem does not silently treat its overchart as complete physical coverage.

No ordered essential-height estimate is proved for the outside source. This is one of the decisive remaining gaps.

## 11. The finite-width physical collar trace

For each physical chart and exact label, define

\[
 M_{z,n,k}(s)=\int_0^s
 b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+u)\,du.
\]

The trace

\[
 \mathcal Q_{m,s;n,k,R}
 =\sum_zs^{-1}M_{z,n,k}(s)\delta_{t_z}
\]

is positive. The atom at `t_z` is only bookkeeping; its coefficient is the average actual source mass in the roof collar.

If `t_z` belongs to `[t-h,t+h]`, the corresponding source collar has actual roof in

\[
 [t-h,t+h+s].
\]

The uniform Morse theorem bounds both endpoint tangential momenta by

\[
 C\sqrt s.
\]

The physical chart pieces are disjoint, their clearance weights are at most one, and the exact section and label indicators are unchanged. Hence

\[
 s\mathcal Q_{m,s;n,k,R}([t-h,t+h])
 \le \nu_R^*(E_{n,k,m,R}^{(C\sqrt s)}(t;[-h,h+s])).
\]

The inherited two-strip local theorem gives, for fixed `s,h` before `m` tends to infinity,

\[
 \limsup_m\sup_{R,n,k,t}
 m^2\nu_R^*(E^{(C\sqrt s)}(t;[-h,h+s]))
 \le C s(2h+s).
\]

Division by `s` yields

\[
 \limsup_m\sup_{R,n,k,t}
 m^2\mathcal Q_{m,s;n,k,R}([t-h,t+h])
 \le C(2h+s).
\]

This argument is correct in its order of limits. It does not evaluate a transfer-operator constant at a width depending on `m`. It does not count critical words or require their roof values to be separated.

This theorem genuinely closes the geometry-to-dynamics comparison for the specified finite-width physical trace.

## 12. The fixed-count zero-width coefficient

At a clearance seam, the first-clearance multiplier is saturated on a sufficiently small physical disk. For a fixed finite word, the remaining active first-hit and section margins have nonzero individual gradients. Their signs on the circle of radius `sqrt(2u)` converge, away from finitely many angular directions, to the signs of their linear parts.

Let `theta_{z,n,k}` be the corresponding angular fraction. Dominated convergence gives

\[
 \frac{A_{z,n,k}^{\varepsilon}(u)}{2\pi}
 \longrightarrow\theta_{z,n,k}
 \qquad(u\downarrow0)
\]

at each fixed collision count. The multiplicative profile then yields

\[
 \lim_{u\downarrow0}
 b_{z,n,k}^{\varepsilon,\mathrm{clr}}(t_z+u)
 =J_z\theta_{z,n,k}.
\]

The same coefficient is the limit of the collar average. Since only finitely many selected critical words occur at fixed `m`, summation commutes with this fixed-count limit.

The proposition is correctly limited to fixed count. It supplies no uniform rate in `m`.

## 13. The angular-loss obstruction

Define

\[
 a_{z,n,k}(u)=A_{z,n,k}^{\varepsilon}(u)/(2\pi)
\]

and

\[
 \mathcal D_{m,s;n,k,R}(I)
 =\sum_{z:t_z\in I}\frac{J_z}{s}
 \int_0^s(\theta_{z,n,k}-a_{z,n,k}(u))_+\,du.
\]

The elementary inequality

\[
 \theta\le a(u)+(	heta-a(u))_+
\]

and the lower multiplicative profile give

\[
 \mathcal B_m(I)
 \le e^{K_\chi\sqrt{2s}}\mathcal Q_{m,s}(I)
      +\mathcal D_{m,s}(I).
\]

This comparison is correct. It also shows precisely why the new trace theorem does not imply zero-width concentration.

The contact jets control the selected positions and velocities in a common chart. They do not provide a collision-count-uniform lower bound for the gradients of every active physical or section margin. Nor do they bound

- the number of nearly active margins;
- the minimum angle between their gradients;
- the order at which a nonlinear physical boundary departs from its tangent line;
- the clustering of those tangent directions;
- or the total reversible weight carried by words with poor angular convergence.

For each fixed word these issues disappear under dominated convergence. Uniformly over long words, they may generate an angular boundary layer whose physical weight is not controlled by the present estimates.

The manuscript states the needed assertion as

\[
 \lim_{s\downarrow0}\limsup_{m\to\infty}
 \sup_{R,n,k,t}m^2\mathcal D_{m,s;n,k,R}([t-1,t+1])=0.
\]

It is unproved. Without it, the passage from finite-width trace `Q` to physical zero-width trace `B` remains conditional.

This is now the sharpest new blocker inside the verified chart class.

## 14. Three distinct traces

The article contains three measures which must not be conflated.

### 14.1 The finite-width physical trace `Q`

Its atoms are collar averages of the actual positive Lorentz source. Revision 66 proves its ordered concentration.

### 14.2 The zero-width physical trace `B`

Its coefficient is

\[
 \beta_{z,n,k}=J_z\theta_{z,n,k}.
\]

It includes the physical and exact-label angular fraction. Its concentration is conditional on the unproved angular-loss estimate.

### 14.3 The full reversible trace `T`

Its coefficient uses the full reversible weight `J_z`, without the physical angular fraction. Revision 65 introduced this larger trace. Revision 66 does not prove its concentration.

The new theorem for `Q` therefore does not close the concentration input requested in the revision-65 report for `T`, and it does not yet close the physically relevant trace `B` either.

The source manifest and proof ledger state these distinctions correctly.

## 15. The complete incidence and clearance sources

Even if the angular-loss estimate were proved, the article would still need ordered control of the positive chart complement and of the complete first-incidence source.

The inherited inverse-incidence theorem gives finite-count bounds with exponential factors. Revision 66 uses incidence normalization to control the coordinate inverse, but does not convert that estimate into the complete exact-label incidence height in the fixed-band collision limit.

Likewise, the clearance chart theorem covers normal critical points satisfying the tapered incidence envelope. It does not cover selected grazing, every noncritical rank component, or every point outside the chosen disks. Those pieces remain in `b^{outside}`.

The complete positive raw-error identity requires the sum of all incidence and clearance pieces. Small mass, small support, a finite-width average, or a local chart formula for a positive subset cannot replace an essential-height estimate for the full source.

## 16. Consequences for the unrestricted pointwise theorem

The target remains

\[
 \sup_{R,n,k}\operatorname*{ess\,sup}_{|Z_{m,R}|\le M}
 \left|m^2p_{n,R}(k,m,t)-\mathcal L_{m,R}(k_1,k_2,t,n)\right|
 \longrightarrow0.
\]

Revision 66 does not prove this statement.

The complete integrated arithmetic record theorem, total-variation approximation, local `L^q` laws, positive lower law, good-set likelihoods, finite-width posteriors and coupled bridge theorems retain their existing scope. None upgrades an integrated or finite-width estimate to a uniform density-height estimate at a prescribed roof.

Therefore the following downstream statements remain unproved:

- unrestricted same-roof collision bridge convergence;
- unrestricted same-roof actual-return bridge convergence;
- forward essential likelihood convergence on the whole central window;
- unrestricted pointwise roof-conditioned path laws; and
- a title-level unconditional raw mixed-density LLT.

The arithmetic transition kernel and its zero classes also remain part of the theorem; no unmodulated Gaussian law is obtained.

## 17. Order of limits

The new ordered trace theorem uses the legitimate order

1. fix `chi`, `epsilon`, collar width `s`, and roof radius `h`;
2. let the collision count tend to infinity;
3. then let `h` and `s` tend to zero.

No growing reconstruction band is inserted into a fixed-band spectral estimate.

The fixed-count identity

\[
 \mathcal Q_{m,s}\to\mathcal B_m
 \qquad(s\downarrow0)
\]

has the opposite first limit and cannot be interchanged with `m->infinity` without a uniform estimate. The angular-loss term is exactly the cost of that interchange.

Any future revision must preserve this distinction. A diagonal `s=s_m` chosen after inspecting the fixed-count convergence would not by itself prove the ordered pointwise theorem.

## 18. Novelty and significance

The new weighted inverse and physical collar comparison are nontrivial and tailored to the original Lorentz source. The finite-width trace theorem is not obtained by differentiating a standard interval local limit: it depends on the exact critical collar geometry, exact labels, the positive source restriction and the inherited endpoint-selected arithmetic law.

Subject to specialist verification, this material could form a valuable focused paper on count-uniform critical charts and positive critical-cluster bounds for dispersing billiards.

At the requested top-four benchmark, however, the following factors remain decisive:

1. the title and architecture still center an unproved unrestricted pointwise endpoint;
2. the new theorem controls a finite-width auxiliary trace rather than the required zero-width physical source;
3. complete source coverage and incidence height remain open;
4. the full article contains 142 tightly interdependent modules;
5. the hardest continuum inputs remain highly model-specific; and
6. no independent expert audit has been obtained.

A top-four significance case would be materially stronger after the complete pointwise theorem is closed, or after the chart-and-trace mechanism is extracted as a general theorem with several independent singular-hyperbolic realizations.

## 19. Independent specialist verification

No independent human specialist audit has been obtained.

For the new modules, the highest-priority checks are:

1. the exact identity `D_yE=D_c A D_c` in the selected contact convention;
2. the row-sum estimate for `K` and the endpoint-incidence factor in the Neumann series;
3. mixed endpoint/internal nonlinear bounds in the tapered weighted norm;
4. contraction on weighted spaces whose dimension grows with `m`;
5. preservation of positive selected reflection signs;
6. interpretation of the selected continuation across a physical seam;
7. the endpoint Hessian lower bound on the continuation;
8. the logarithmic derivative of the determinant coefficient;
9. the quantitative Morse inverse and its Jacobian;
10. finiteness of the competing-disk candidate list on the continuation;
11. the Lipschitz clearance guard at a changing closest point;
12. exact first-defect saturation when one clearance vanishes;
13. disjointness of the physical chart pieces;
14. common coarea representatives for the exact masks;
15. the use of the inherited two-strip theorem with widths fixed before `m`;
16. the fixed-count tangent angular fraction;
17. the interpretation of the angular-loss measure; and
18. all inherited transfer-operator, arithmetic and source-normalization inputs.

The exact-source workflows and finite fixtures do not replace this audit.

## 20. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 20.1 Prove the angular-loss estimate

Establish

\[
 \lim_{s\downarrow0}\limsup_{m\to\infty}
 \sup_{R,n,k,t}m^2\mathcal D_{m,s;n,k,R}([t-1,t+1])=0.
\]

A valid proof must control the complete family of active physical and section masks, not merely the selected contact coordinates. It must retain exact labels and the original source.

### 20.2 Control the positive chart complement

Prove an ordered essential-height estimate for

\[
 b^{\varepsilon,\chi,\mathrm{outside}}.
\]

This includes tapered-incidence violations, selected grazing, noncritical rank components and physical states outside the normal critical disks. A mass or support estimate is insufficient.

### 20.3 Complete the first-incidence height

Use the incidence-normalized geometry, or a different argument, to prove the complete exact-label ordered incidence estimate required by the positive raw-error criterion. The finite-count exponential inverse-incidence bound does not suffice.

### 20.4 Complete the clearance height

Combine zero-width physical-trace concentration, outside-source control, transverse and finite-type coarea, and the caustic analysis into one complete ordered clearance estimate on the original source.

### 20.5 Deduce the unrestricted pointwise theorem

Insert the two complete positive-height estimates into the established raw-error identity. Retain the finite arithmetic transition kernel and zero classes unless a separate residue theorem is proved.

### 20.6 Derive the unrestricted same-roof consequences

Only after the pointwise theorem is proved should the paper claim unrestricted same-roof bridge convergence and forward essential likelihood.

### 20.7 Obtain independent specialist review

The contact-coordinate continuation, physical masking, angular-loss argument, inherited anisotropic spectral chain and positive source decomposition require expert human verification.

### 20.8 Reduce the proof burden

A journal submission should expose the shortest complete route to one principal theorem. Extensive historical front matter, validation ledgers and unfinished alternative routes should remain available in the repository without dominating the article's logical spine.

### 20.9 Sharpen the literature comparison

Explain theorem by theorem which count-uniform coordinate, exact-label, critical-cluster and pointwise conclusions are not available from existing Lorentz-process, endpoint-mixing or suspension-flow local-limit theorems after checking their hypotheses.

## 21. Technical and presentation comments

1. Keep `Q`, `B`, and `T` distinct in every theorem summary.
2. State whenever `chi`, `epsilon`, `s`, and `h` are fixed before the collision-count limit.
3. Do not abbreviate the fixed-count convergence `Q_{m,s}->B_m` as an ordered concentration theorem.
4. Keep the positive angular-loss term visible; it is not a signed remainder.
5. Retain the exact-label masks in the definition of the angular integral.
6. Keep initial membership, occupation at `0,...,m-1`, and terminal membership separate.
7. Preserve the image mark `j+1` for clearance.
8. Do not assign physical probability to the selected-contact continuation outside the first-hit set.
9. State that the Morse disk is a coordinate disk, not a physical disk.
10. Keep the tapered incidence condition in every uniform-chart statement.
11. State that selected grazing is excluded from the uniform chart theorem.
12. Do not infer complete source coverage from disjointness of the covered charts.
13. Keep the relative density estimate separate from an absolute lower bound for `J_z`.
14. Preserve the square root in the reversible determinant coefficient.
15. Do not divide by a primitive period.
16. Keep the original half-word labels; do not read labels from the doubled reversible orbit.
17. State that coincident critical values add positively.
18. Keep the two endpoint strip width `O(sqrt(s))` and roof width `2h+s` visible in the trace proof.
19. Do not introduce a word-count factor after the positive source comparison.
20. Keep the two-strip local theorem's fixed-width quantifier order explicit.
21. Distinguish common coarea representatives from pointwise values at exceptional roofs.
22. Keep the label sum under the pointwise partition bound rather than an output-cardinality estimate.
23. State that the first-clearance guard is saturated only on the physical part of the continuation.
24. Keep the outside source nonnegative and explicit.
25. Do not infer essential height from small support or small source mass.
26. Preserve the finite arithmetic factor and zero denominator classes.
27. Keep probability total variation distinct from variation mass and path bounded-Lipschitz dual.
28. Do not attach an unproved polynomial rate to the qualitative ordered limits.
29. Keep source qualification separate from proof certification.
30. Record both exact-SHA workflow runs, but do not describe them as independent mathematical reviews.

## 22. Final assessment

Revision 66 is a serious and mathematically coherent response to the revision-65 report.

It proves a refined contact inverse with a retained incidence factor, removes collision-count dependence from selected-contact jets under an explicit taper, constructs count-uniform Morse coordinates across clearance and section seams, and evaluates the original physical source through exact nonlinear angular masks. It then proves a clean ordered concentration estimate for a positive finite-width physical collar trace by comparing the disjoint collars with the exact-label two-endpoint local law.

I found no decisive error in modules 140--142. The trace theorem is a genuine advance and closes one previously missing geometry-to-dynamics step.

The advance nevertheless stops one limit short of the pointwise endpoint. The zero-width physical trace requires uniform control of the angular loss, the larger reversible trace remains uncontrolled, and the complete incidence and chart-complement sources remain outside the theorem. The unrestricted pointwise raw-density law and its same-roof consequences are therefore still open.

The manuscript also remains exceptionally large, highly model-specific and dependent on continuum inputs which have not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist-journal paper centered on the incidence-normalized contact inverse, uniform physical critical charts and the finite-width collar trace could be significant if the inherited geometric and spectral inputs survive expert audit. A renewed top-four submission should return only after the angular-loss and complete-source height problems are closed, or after the mechanism is extracted and verified as a substantially broader theorem.