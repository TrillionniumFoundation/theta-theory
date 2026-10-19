# External top-four referee report on A2-DYN revision 68

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v68-referee-response-2026-10-10`, `revision/a2-dyn-v68-referee-copy-2026-10-10`  
**Reviewed commit:** `c8268a608a971c6832bcfed2a827af951e84c577`  
**Reviewed repository tree:** `5ad306f9d52530e8a409a8e55f85dece72fab234`  
**Ordinary source payload tree:** `a7edcb2364f66f5808323e008a9fe1f943033071`  
**Active manuscript directory:** `papers/A2-DYN-v68-referee-response`  
**Active mathematical source:** one hundred forty-eight numbered core modules; revision 68 retains all one hundred forty-five revision-67 modules and adds modules 146--148  
**Frozen revision-67 author baseline:** `add4d884ec0902fd5c70c68e1a82065442eab58f`  
**Frozen revision-67 complete paper tree:** `266c432351a184e230b7e4df4f970c9d9f87208c`  
**Controlling external report:** `reviews/a2-dyn-v67-external-top4-review-2026-10-10/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `d3321f707ba556bd25bb586178eed89038133cc8` / `b6e34eb10fa505a97a800a5ef7bc0e99cc222609`  
**Date:** 10 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards/anisotropic-spaces audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 68 is a genuine theorem-bearing advance over revision 67. The preceding report identified two different failures in the physical clearance analysis. First, labels with zero tangent angular fraction could nevertheless be born nonlinearly at positive radius and therefore remained invisible to the zero-width atomic trace. Second, fixed-word exhaustion did not give collision-count-uniform control of either the old angular condition number or the complete positive complement.

Revision 68 resolves the first issue on every fixed radial-persistence stratum. It does so without imposing a uniform bound on the finite birth order.

The new source proves that, at every fixed selected circular-billiard word and exact label, the unguarded physical angular fraction has an analytic one-sided germ. It is either identically zero near the critical center or has the form

\[
 \ell_{z,\lambda}(r)
   =\eta_{z,\lambda}r^{d_{z,\lambda}}
      +O_z(r^{d_{z,\lambda}+1}),
 \qquad \eta_{z,\lambda}>0,
 \quad d_{z,\lambda}\in\mathbb N_0.
\]

Thus a label with zero tangent fraction but nonzero nonlinear source has a positive finite order of birth. The source then restores the original first-clearance guard, records a relative analytic remainder and a relative guard-Lipschitz budget, and defines a persistence number which also pays the certified analytic radius. On each fixed persistence stratum the actual source density is comparable to

\[
 \gamma_{z,\lambda}r^{d_{z,\lambda}},
 \qquad \gamma_{z,\lambda}=J_zg_z\eta_{z,\lambda},
\]

with multiplicative errors which are linear in the radius.

The main new device is a positive outer-annulus comparison. The value of the source on the inner collar `0 < u < H` is bounded by its own positive average on the single outer annulus `H < u < 2H`. Since the monomial `r^d` is nondecreasing for every `d >= 0`, the comparison constant has no dependence on the finite birth order. Combining this comparison with the inherited arbitrary-positive-subfamily collar theorem gives

\[
 \limsup_{m\to\infty}\sup_{R,n,k}
 m^2\|b^{\mathrm p,K,H}_{m;n,k,R}\|_\infty
 \le 6CH F_{\chi,K}(H),
\]

where

\[
 F_{\chi,K}(H)
 =e^{(2+\sqrt2)K_\chi\sqrt H}
   \frac{1+\sqrt2K\sqrt H}{1-2K\sqrt H}.
\]

At fixed `K`, `chi` and `epsilon`, this tends to zero with `H`. The theorem includes zero-tangent nonlinear sectors of every finite order on the stated stratum and also non-seam critical centers whose actual center guard is positive.

I audited the new modules

- `core/146_analytic_angular_germs.tex`;
- `core/147_relative_radial_persistence.tex`;
- `core/148_annular_height_and_full_source.tex`;

and their use in the revised front matter. I also checked the exact nonlinear profile in module 141, the arbitrary-positive-subfamily collar theorem in module 142, the revision-67 angular strata and complete-source partition in modules 143--145, the exact-label convention, the coarea normalization, the interval constants and the two exact-SHA qualification runs.

I found no decisive counterexample, missing factor of `2 pi`, missing radial coarea factor, incorrect annulus exponent, label-count multiplier, word-count multiplier, reversal of the proved limits, or hidden deletion of the original positive source in the new three-module chain. In particular:

1. dividing an active analytic margin by the radius produces an analytic function at `r=0`;
2. every active margin has exactly two simple angular root germs near zero;
3. after truly coincident germs are identified, their cyclic order is fixed on a sufficiently small one-sided interval;
4. the exact one-hot label is constant on each moving open arc because the complete primitive sign vector is constant there;
5. the angular fraction is a finite sum of analytic arc lengths and hence is analytic;
6. nonnegativity forces the first nonzero coefficient of a nonzero germ to be positive;
7. the persistence cutoff pays both the inverse certified radius and the relative angular and guard errors;
8. the physical coarea profile has no missing power of `r`, because the polar arclength factor cancels the derivative of `r^2/2`;
9. the annular comparison uses one common positive annulus and does not sum infinitely many dyadic scales;
10. the inherited collar theorem is stated for an arbitrary positive subfamily, so the persistence restriction creates no combinatorial multiplier;
11. the interval of critical centers contributing to one roof value has length `H`, while the inherited collar width is `2H`, giving the displayed factor `6`; and
12. the proof fixes every geometric cutoff before the collision-count limsup.

These are meaningful achievements. The negative recommendation is therefore not based on a failure of the new restricted theorem.

The recommendation is instead forced by the endpoint which still governs the title and the one-hundred-forty-eight-module architecture.

The new estimate controls only the source

\[
 b^{\mathrm p,K,H},
\]

a positive restriction to a fixed persistence stratum and to the shrinking inner collar `0 < F_z-t_z < H`. As `H` decreases, this controlled source shrinks and the positive complement expands. The exact partition is

\[
 b^{\varepsilon,\mathrm{clr}}
  =b^{\mathrm p,K,H}
    +r_{68}^{\varepsilon,\chi,K,H},
 \qquad r_{68}^{\varepsilon,\chi,K,H}\ge0.
\]

The complement still contains, among other classes,

- failed incidence taper;
- selected grazing;
- noncritical-rank components;
- uncovered physical states;
- zero-center-guard source, which may be infinitely flat;
- source outside a certified analytic-germ disk;
- large persistence numbers;
- outer portions of the same chart;
- omitted annuli;
- and the inherited outside source.

No ordered essential-height estimate is proved for this complement. Fixed-word finiteness of the persistence number does not imply weighted tightness after the supremum in the radius and exact labels and after the collision limsup. The old physical angular tail `E(K)` is also still unproved, and the new persistence number is explicitly not identified with the old angular condition number.

The complete first-incidence height remains open as a separate positive source. The finite-count inverse-incidence theorem has an exponential collision-count constant and does not provide the fixed-band ordered estimate needed by the raw-error criterion.

Consequently revision 68 still does not prove

- the complete ordered first-incidence height;
- the complete ordered clearance height;
- the unrestricted two-sided pointwise arithmetic raw-density theorem;
- unrestricted same-roof collision and actual-return bridges;
- forward essential-likelihood convergence;
- or the unrestricted pointwise roof-conditioned path theorem.

These are not cosmetic extensions. They are the title-level endpoint and the hypotheses required by the manuscript's own positive raw-error identity.

At the requested benchmark, the article would need either

1. complete ordered control of the physical persistence tail, the positive complement and the first-incidence source, followed by the unrestricted pointwise theorem; or
2. a substantially broader theorem with quantitatively verifiable hypotheses and several genuinely different singular-hyperbolic realizations, so that the paper's significance no longer depends editorially on the unfinished Lorentz endpoint.

Revision 68 supplies neither yet. No independent human specialist audit has been obtained.

My assessment is therefore positive about the new nonlinear component theorem and negative about readiness for *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`c8268a608a971c6832bcfed2a827af951e84c577`.

The repository tree at that commit is

`5ad306f9d52530e8a409a8e55f85dece72fab234`.

The active article is

`papers/A2-DYN-v68-referee-response`.

The ordinary source payload tree recorded in the manifest is

`a7edcb2364f66f5808323e008a9fe1f943033071`.

The immediate mathematical baseline is revision 67 at

`add4d884ec0902fd5c70c68e1a82065442eab58f`.

The controlling external report is the revision-67 report at

`d3321f707ba556bd25bb586178eed89038133cc8`.

Revision 68 begins after that frozen review state and lands a complete author source. The final source manifest records

- all 145 inherited core modules byte-identical;
- all 197 inherited Python files byte-identical;
- all seven inherited appendices byte-identical;
- the bibliography byte-identical;
- every inherited compiled input and mathematical label retained;
- the previous abstract and introduction compiled verbatim in `appendices/v67_frontmatter.tex`;
- the old complete main source and replaced metadata archived under provenance;
- 148 active core modules;
- `lorentz_analytic_angular_germ_classification_proved: true`;
- `lorentz_zero_tangent_all_order_strata_height_proved: true`;
- `lorentz_order_free_annular_comparison_proved: true`;
- `lorentz_positive_center_guard_nonseam_strata_height_proved: true`;
- `lorentz_angular_condition_tail_proved: false`;
- `lorentz_uniform_angular_loss_proved: false`;
- `lorentz_complete_source_coverage_proved: false`;
- `grazing_boundary_pointwise_smallness_proved: false`;
- `clearance_boundary_pointwise_smallness_proved: false`;
- `full_raw_return_LLT_proved: false`;
- `pointwise_roof_density_LLT_proved: false`;
- and `independent_human_review: false`.

These status flags accurately distinguish the new restricted theorem from the unproved complete-source endpoint.

The present review branch starts directly from the reviewed author SHA and adds only this report under

`reviews/a2-dyn-v68-external-top4-review-2026-10-10/`.

No author source, workflow, prior review, historical manuscript, or unrelated repository path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA revision-68 qualification workflows completed successfully on both reviewed author refs:

- response branch run `38057027567`;
- referee-copy branch run `38057036276`.

Both runs use the reviewed SHA

`c8268a608a971c6832bcfed2a827af951e84c577`.

This closes the submission-evidence defect noted in the revision-67 report, where only the response ref had a completed run at the time of audit.

According to the validation protocol, the revision-68 verifier checks

- the frozen complete revision-67 paper tree;
- the controlling revision-67 report blob;
- all 145 inherited core files;
- all 197 inherited Python files;
- all seven inherited appendices;
- the unchanged bibliography;
- all 148 active core inputs;
- all inherited mathematical labels and compiled inputs;
- the ordinary source payload and workflow hashes;
- normal and optimized finite diagnostics;
- native TeX compilation without shell escape;
- stabilized references and warning-free typesetting; and
- theorem-label-based rendering of the new proof pages.

The new finite fixtures cover analytic zero-angle births, high-order annular comparison, positive relative guard products, exact one-hot labels, coarea normalization and the final height constants. Negative controls distinguish

- finite jet agreement from analytic identity;
- zero-center infinitely flat guards from finite-order analytic birth;
- fixed-count exhaustion from ordered weighted tightness;
- and small mass from small essential height.

These checks are useful source, algebra and typesetting evidence. They do not certify

- completeness of the primitive physical margin list;
- the selected-contact analytic continuation;
- the arbitrary-positive-subfamily collar theorem;
- the continuum one-hot physical visit rule;
- the physical persistence tail;
- the complete incidence or clearance height;
- the unrestricted pointwise theorem;
- or independent human review.

The manuscript and its validation files state this boundary accurately.

## 4. Scope of this review

I did not attempt to re-prove all 148 core modules. The substantive audit concentrates on the new claims and the inherited statements which they use directly:

1. analyticity of the selected-contact graph;
2. analyticity of the specific matrix-square-root Morse coordinates;
3. completeness of the primitive physical and section margins;
4. nonvanishing differential of every active margin;
5. fixed inactive signs on a word-dependent disk;
6. analytic angular root germs;
7. fixed cyclic order after truly identical germs are identified;
8. exact one-hot labels on moving arcs;
9. analytic exact-label angular fractions;
10. positivity and finite order of the first nonzero coefficient;
11. the certified radius and relative Taylor remainder;
12. the original Lipschitz clearance guard and positive center value;
13. the relative weighted angular profile;
14. the unchanged physical coarea Jacobian;
15. the positive outer-annulus comparison;
16. the arbitrary-positive-subfamily collar theorem;
17. the center-interval argument converting trace mass to density height;
18. the exact positive complement;
19. the distinction between the old angular condition number and the new persistence number;
20. the fixed-band order of limits;
21. source preservation and workflow evidence; and
22. the remaining top-four endpoint.

The inherited modules outside this route are treated as a source-pinned baseline, not as independently recertified mathematics. Their load-bearing continuum claims retain the audit qualifications of the earlier reports.

## 5. Analytic primitive margins

The first new lemma asserts that, at a fixed normal critical word with positive selected incidences, the complete finite scalar-margin description can be chosen real analytic in the selected Morse coordinates.

For the circular table this is a plausible and structurally correct route. The selected contact equations are analytic. Positive incidence makes the selected roots simple. Invertibility of the internal derivative permits analytic implicit continuation of the contact graph. The manuscript also fixes a particular analytic Morse map rather than appealing only to a `C^2` Morse lemma: the positive-definite analytic matrix field is square-rooted analytically, and the resulting coordinate map has an analytic local inverse.

The treatment of the competing-disk clearance is also correctly formulated. The minimum itself need not be analytic. The proof instead retains the finite list of signed analytic candidate tests separately and fixes the sign of the nonzero perpendicular coordinate before forming the clearance margin. This is exactly what the later root-germ argument requires.

The principal imported obligation is completeness. Every first-hit decision, competing candidate, section edge, occupation decision and terminal decision that can alter the physical exact label must occur in the finite primitive list on the chosen disk. The new proof cites the inherited margin-description lemma for this statement. If one primitive decision is omitted, the one-hot label need not remain constant on an arc even though the recorded signs do.

The second imported obligation is that each active primitive margin has nonzero differential at the critical center. The root theorem depends on this at every active boundary. I found no contradiction in the written chain, but this is a specialist geometric input rather than a consequence of analyticity alone.

No count-uniform analytic radius is asserted. This is appropriate. The word-dependent radius is later paid by the persistence cutoff.

## 6. Angular roots and cyclic order

For an active analytic margin `f`, the manuscript considers

\[
 F_f(r,\phi)=\frac{f(r\omega_\phi)}r
\]

for `r != 0`, with value `Df(0) dot omega_phi` at `r=0`.

Because `f(0)=0`, this quotient extends analytically in `(r,phi)`. The two zeros of the linear form on the unit circle are simple in the angular variable. The analytic implicit function theorem therefore produces exactly two root germs. Compactness of the angular complement excludes additional roots for sufficiently small radius.

For finitely many root germs, the difference of two analytic lifts is either identically zero or has a first nonzero Taylor coefficient. In the second case its sign is fixed for sufficiently small positive radius. Thus, after coincident germs are identified, the cyclic order is fixed.

This argument is correct at a fixed word. It also explains why a finite list of equal Taylor coefficients is not enough to identify two roots: infinite-order equality must be an analytic identity.

On each open arc between consecutive root germs, no active primitive vanishes and every inactive sign remains fixed. Hence the full primitive sign vector is constant. Subject to completeness of the primitive list, the original one-hot physical visit rule assigns the same exact label, or no label, to that arc.

I found no need for a quantitative angle-separation estimate in this fixed-word classification.

## 7. Analytic angular fractions and nonlinear births

The exact angular fraction is a finite sum of lengths of moving arcs carrying the chosen label. Each arc length is a difference of analytic root lifts, or of a root lift and the fixed cut. It therefore extends analytically to zero.

The constant term is the tangent angular fraction. If the germ is nonzero, its first nonzero coefficient is positive because the angular fraction is nonnegative for positive radius. This gives the claimed alternatives:

- an identically zero germ on a certified smaller disk; or
- a positive finite-order birth.

This is an important improvement over revision 67. A label with zero tangent fraction is no longer automatically assigned to the uncontrolled complement merely because it has no zero-width atom.

The theorem remains a fixed-word existence statement. It gives no collision-count-uniform bound on

- the analytic radius;
- the birth order;
- the leading coefficient;
- the first separating order of two root germs;
- or the relative derivative remainder.

Revision 68 does not hide this lack of uniformity. All relevant quantities are recorded in the persistence number.

## 8. Relative radial persistence and the physical guard

The original first-clearance multiplier is only Lipschitz; it is not declared analytic. This distinction is correct.

When the center value `g_z` is positive, the pointwise Lipschitz estimate gives

\[
 g_z(1-k_z^{\rm g}r)
 \le D_z^\varepsilon(r\omega)
 \le g_z(1+k_z^{\rm g}r).
\]

Combining this with the relative analytic estimate for the angular fraction yields

\[
 (1-Kr)c_{z,\lambda}r^d
 \le a_{z,\lambda}^\varepsilon(r)
 \le(1+Kr)c_{z,\lambda}r^d
\]

on the fixed persistence stratum. The factor `2` in the definition of the persistence number provides enough room for the product errors. The conditions `p <= K` and `r < K^{-1}` also ensure that the certified analytic radius has not been exceeded.

Multiplication by the inherited relative density distortion gives the physical roof-density profile. The normalization is consistent:

\[
 a^arepsilon=(2\pi)^{-1}\int BD,
 \qquad \gamma=J_zg_z\eta.
\]

There is no missing `2 pi` and no missing power of the radius.

The exclusions are mathematically necessary. If the angular germ is identically zero, only its certified inner disk has zero source. If `g_z=0`, a merely smooth guard may be positive away from the center and infinitely flat. Neither source class can be divided by a positive center value or assigned a finite guard birth order. Both remain in the positive complement.

## 9. The order-free annular comparison

The annular comparison is the strongest and cleanest new observation.

For `H < v < 2H`, the radial variable lies between `sqrt(2H)` and `2sqrt(H)`. The lower profile therefore gives

\[
 \overline q_{z,H}
 \ge e^{-2K_\chi\sqrt H}(1-2K\sqrt H)
        \gamma_{z,\lambda}(2H)^{d/2}.
\]

For `0 < u < H`, the upper profile is bounded by

\[
 e^{\sqrt2K_\chi\sqrt H}
 (1+\sqrt2K\sqrt H)
 \gamma_{z,\lambda}(2H)^{d/2}.
\]

Combining these estimates gives the displayed factor `F_{chi,K}(H)`. The argument uses only monotonicity of `r^d` for `d >= 0`. It introduces neither `2^d` nor a maximum allowed birth order.

The relation between the outer-annulus average and the full `0 < u < 2H` average is also correct:

\[
 \overline q_{z,H}\le2q_{z,2H}.
\]

The comparison is positive and source-level. It does not replace the nonlinear physical mask by its leading monomial.

## 10. Use of the inherited collar theorem

The inherited theorem is stated for any subfamily of the selected critical charts, each counted once, with exact labels imposed on the actual source inside each chart. It therefore applies to the fixed persistence subfamily.

This point is essential. If the collar theorem had only been proved for the complete chart family, restricting by a word-dependent analytic certificate could have introduced an uncontrolled counting factor. The actual statement is monotone and positive, so no such factor appears.

Summing the annular comparison over centers in an interval gives the scale-weighted trace concentration. At a prescribed roof `t`, only centers in `[t-H,t]` can contribute to the inner collar. Applying the collar theorem with collar width `2H` and an interval of length `H` gives `3CH`; the annular factor contributes the remaining factor `2`, producing `6CH F`.

Coincident critical values add positively and require no separation.

The common coarea representative excludes a finite-count null roof set. At fixed collision count there are finitely many physical words and exact labels, so taking their union remains null. The conclusion is appropriately stated as an essential-supremum estimate.

Subject to the inherited collar theorem and physical chart disjointness, the constant bookkeeping in the new height theorem is internally consistent.

## 11. What the all-order theorem actually controls

The theorem controls a genuine part of the original source, not a formal leading coefficient. It includes

- positive tangent-fraction sectors of order zero;
- zero tangent-fraction sectors with nonzero finite-order angular birth;
- all finite birth orders simultaneously;
- clearance seams with saturated guard;
- and non-seam critical centers with positive center guard.

This is a substantial widening of the revision-67 controlled class.

It is nevertheless a restriction in two independent senses.

First, it is restricted by the persistence cutoff. Every fixed qualifying germ has finite persistence, but no weighted tightness of the persistence number is proved in the long-orbit regime.

Second, it is restricted to the inner collar `0 < F_z-t_z < H`. The ordered vanishing as `H` tends to zero is a theorem about a shrinking source. Source in the outer portion of the same certified chart is transferred to the complement.

The theorem therefore cannot be read as saying that every finite-order birth has small complete height. It says that, once its relative profile persists uniformly on the selected radial scale, its sufficiently inner nonlinear collar has small ordered height.

## 12. The persistence tail is not the old angular tail

Revision 68 correctly distinguishes

- the old condition number `mathfrak a`, built from the tangent coefficient and active curvature-to-gradient budget; and
- the new persistence number `mathfrak p`, built from the certified analytic radius, relative first-nonzero-coefficient remainder and relative guard error.

The old weighted tail `E(K)` remains unproved. Analytic finite-order classification does not imply it.

The new theorem also does not prove a persistence-tail estimate. A fixed-count finite set of persistence numbers can be exhausted, but the required endpoint takes a supremum in the parameter and exact labels and then a collision limsup. Choosing a cutoff `K=K_m` would reverse the proved order of limits.

A future proof needs a positive physically weighted tightness statement for the actual source. An unweighted count of words or a finite maximum at each collision count is insufficient.

## 13. The complete positive complement

The exact partition

\[
 b^{\varepsilon,\mathrm{clr}}
  =b^{\mathrm p,K,H}
   +r_{68}^{\varepsilon,\chi,K,H}
\]

is one of the strengths of the revision. It prevents a partial theorem from being mistaken for complete source coverage.

The complement explicitly retains

1. the inherited outside source;
2. failed tapered incidence;
3. selected grazing;
4. noncritical-rank pieces;
5. every uncovered physical state;
6. zero-center-guard source;
7. identically zero angular germs outside their certified zero disks;
8. source outside every certified analytic disk;
9. persistence numbers above `K`;
10. source outside the inner collar;
11. omitted annuli;
12. and every class not included by the exact disjoint restriction.

No essential-height estimate is proved for this complement.

Small support, small mass, fixed-count analytic exhaustion and finite-width collar bounds do not imply small essential height. The manuscript does not make any of these invalid inferences.

## 14. The complete incidence source remains open

The new modules concern the clearance source on selected normal-critical charts.

The complete first-incidence term in the positive raw-error identity remains separate. The inherited inverse-incidence theorem gives a finite-count height bound with an exponential count constant. It does not yield the ordered estimate at fixed reconstruction band.

Thus even a future proof controlling the complete clearance complement would not by itself close the pointwise theorem.

A complete submission must either prove the incidence estimate directly or give one argument which treats both positive physical source types together.

## 15. Order of limits

The legitimate order in the new theorem is:

1. fix the reconstruction band `B` and its physical width `epsilon(B)`;
2. fix `chi`, `K` and `H` satisfying the stated inequalities;
3. take the collision-count limsup;
4. for the controlled source, let `H` decrease at fixed `chi` and `K`;
5. only after a separate weighted-tail theorem may one enlarge `K` or remove other source restrictions;
6. finally enlarge the reconstruction band.

The following shortcuts remain invalid:

- choosing `K=K_m` from fixed-count exhaustion;
- choosing `H=H_m` from a wordwise analytic radius;
- choosing the reconstruction band exponentially in the collision count;
- treating a constant independent of the birth order as uniform persistence control;
- replacing a persistence tail by an unweighted word count;
- using small source mass as an essential-height estimate;
- deleting the zero-center guard source;
- or treating the shrinking-collar theorem as coverage of the whole certified chart.

Revision 68 avoids these shortcuts. Any future revision should preserve the same order explicitly.

## 16. The canonical endpoint budget

The manuscript inserts the new estimate into the established positive-error identity and obtains

\[
 \mathcal E_M
 \le C_MB^{-1/192}
  +\mathcal H(b^{\varepsilon(B),\mathrm{inc}})
  +6CH F_{\chi,K}(H)
  +\mathcal H(r_{68}^{\varepsilon(B),\chi,K,H}).
\]

This is a useful and honest reduction.

Only the third term is controlled by the new theorem. To conclude `mathcal E_M=0`, one still needs

- the incidence term to vanish in the required outer band limit;
- admissible fixed choices whose complement height is small after the collision limsup;
- and a valid exhaustion of the persistence and geometric restrictions.

The finite arithmetic transition kernel and its zero classes remain unchanged. This is correct. Nothing in the analytic-germ argument proves residue triviality.

## 17. Consequences for the pointwise theorem and bridges

The target remains

\[
 \sup_{R,n,k}\operatorname*{ess\,sup}_{|Z_{m,R}|\le M}
 \left|m^2p_{n,R}(k,m,t)
       -\mathcal L_{m,R}(k_1,k_2,t,n)\right|
 \longrightarrow0.
\]

Revision 68 proves a small-height theorem for one positive part of the clearance source. Positivity prevents cancellation from removing the incidence and complementary clearance terms.

Therefore the unrestricted pointwise theorem does not follow.

The inherited complete mixed-measure total variation theorem, local `L^q` laws, positive lower law, good-set posteriors, bridge convergence in mean and all-resolution good-roof statements retain their previous scope. None turns a partial positive-source height into a full essential-supremum density theorem.

Accordingly the paper must not yet claim

- an unrestricted same-roof collision bridge;
- an unrestricted same-roof actual-return bridge;
- forward essential likelihood on the full central window;
- or a pointwise roof-conditioned path law for every positive arithmetic class.

The current manuscript does not make those claims.

## 18. What revision 68 closes

Relative to revision 67, the new source closes the following issues.

- Exact-label angular fractions are classified analytically at every fixed selected word.
- Truly coincident angular boundaries are distinguished from high finite-order contact.
- Zero tangent fraction no longer forces all nonlinear source into the uncontrolled complement.
- Every nonzero angular germ has a positive finite-order leading coefficient.
- The original clearance guard is restored without asserting guard analyticity.
- Positive non-seam center guards are included.
- Relative angular and guard errors are recorded in one persistence cutoff.
- One positive outer annulus controls every inner level.
- The comparison constant is independent of the finite birth order.
- All finite birth orders in the stratum are summed before the collision limit.
- The inherited collar theorem gives an ordered original-source essential-height estimate.
- The two author refs now both have successful exact-SHA qualification runs.

These are real advances, not changes in notation.

## 19. What revision 68 does not close

The manuscript still lacks

1. weighted tightness of the new persistence number;
2. the old physical angular-condition tail;
3. zero-center-guard source height;
4. source outside certified analytic disks;
5. source outside the shrinking inner collar;
6. failed-taper source height;
7. selected-grazing source height;
8. noncritical-rank source height;
9. all uncovered physical classes;
10. the complete positive clearance height;
11. the complete first-incidence height;
12. the unrestricted two-sided pointwise raw-density law;
13. unrestricted same-roof bridge convergence;
14. forward essential likelihood on the full central window;
15. the unrestricted pointwise roof-conditioned path theorem;
16. a general theorem with several independent singular-hyperbolic realizations; and
17. an independent human specialist audit.

The new result remains a component theorem.

## 20. Novelty and significance

The analytic-germ classification and order-free positive annular comparison are nontrivial and well adapted to the original Lorentz source. In particular, the theorem avoids a potentially fatal dependence on the finite birth order.

The most conceptually useful new observation is that a single positive annulus can pay all inner finite-order births before the long-orbit limit. This may be reusable in other positive-source coarea problems.

At the requested top-four benchmark, however, the following factors remain decisive:

1. the title and architecture still center an unproved unrestricted pointwise theorem;
2. the new theorem concerns a shrinking collar on a fixed persistence stratum;
3. no tail theorem removes that stratum cutoff;
4. the complete positive complement is unestimated;
5. the complete incidence source is unestimated;
6. the article contains 148 tightly interdependent mathematical modules;
7. the hardest continuum inputs remain highly model-specific; and
8. no independent expert audit has occurred.

A focused specialist-journal paper centered on analytic angular births, positive annular comparison and ordered collar height could be valuable if the inherited geometric inputs withstand expert scrutiny.

For a four-journal submission, the complete endpoint or a substantially broader verified theorem is still required.

## 21. Independent specialist verification

No independent human specialist audit has been obtained.

For the new modules, the highest-priority checks are:

1. completeness of the primitive physical and section margin list;
2. analyticity of each retained candidate after fixing its physical sign;
3. nonzero differential of every active margin;
4. analyticity and invertibility of the selected-contact graph;
5. analyticity of the specific matrix-square-root Morse coordinates;
6. exclusion of additional angular roots away from the two linear roots;
7. treatment of truly identical root germs;
8. preservation of the exact one-hot visit rule on moving arcs;
9. positivity of the first nonzero angular coefficient;
10. the certified radius and relative derivative remainder;
11. the guard Lipschitz constant on the actual source;
12. the common coarea representative and normalization;
13. the inherited relative physical density bound;
14. application of the collar theorem to an arbitrary positive subfamily;
15. disjointness of the physical chart restrictions;
16. summation over exact labels without a label-count factor;
17. the interval-of-centers argument for essential height;
18. the exact positive complement;
19. distinction between persistence and the old angular condition number;
20. and every inherited anisotropic, arithmetic and source-normalization input.

The source workflow, finite fixtures, symbolic checks and native build do not replace this audit.

## 22. Required mathematical changes before another top-four review

A subsequent revision seeking the same benchmark should address the following.

### 22.1 Prove physical weighted tightness of the persistence cutoff

Establish an ordered positive-source tail theorem for `mathfrak p` after the supremum in the radius and exact labels and after the collision limsup.

The weight must be the actual original source or an explicitly dominating positive physical trace. Fixed-count finiteness, a maximum over finitely many words, or an unweighted critical-word count is insufficient.

A verified moment bound for the inverse analytic radius, relative coefficient remainder and relative guard budget would be one possible route.

### 22.2 Control zero-center guards

Treat source with `g_z=0`. A merely smooth guard may be positive and infinitely flat away from the center, so the analytic angular birth order alone does not control it.

A valid argument must use the original physical guard and exact labels. It may not replace the guard by an analytic model without proving the comparison.

### 22.3 Control source outside the certified germ disk and inner collar

The current theorem shrinks the controlled source as `H` decreases. Prove an ordered estimate for the outer part of each certified chart and for the source beyond the certified angular-germ radius.

A finite annular decomposition must be compatible with the collision limsup. An infinite dyadic decomposition cannot be interchanged with that limsup without a summable uniform bound.

### 22.4 Control the remaining positive clearance classes

Prove ordered essential-height estimates for failed taper, selected grazing, noncritical-rank components, non-seam zero-guard centers and every uncovered physical class.

Retain the original first-clearance witness, next-collision mark, exact labels and finite arithmetic kernel.

### 22.5 Complete the first-incidence height

The finite-count inverse-incidence theorem does not suffice. Establish the complete exact-label ordered first-incidence estimate in the fixed-band regime.

### 22.6 Complete the clearance height

Combine persistence tightness, zero-center control, outer-chart control, the new all-order theorem, the revision-67 order-zero theorem, transverse and finite-type coarea, buffered caustics and all remaining positive pieces into one complete ordered clearance estimate.

### 22.7 Deduce the unrestricted pointwise theorem

Insert the complete incidence and clearance estimates into the established positive-error identity. Retain the finite arithmetic transition kernel and zero classes unless a separate residue theorem is proved.

### 22.8 Derive unrestricted same-roof consequences only afterwards

Only after the full pointwise theorem is established should the paper claim unrestricted same-roof bridges, forward essential likelihood or pointwise roof-conditioned path laws.

### 22.9 Obtain independent specialist review

The physical margin description, analytic selected-contact continuation, nonlinear source profile, collar theorem and complete positive-source decomposition require expert human verification.

### 22.10 Reduce the proof burden

A journal submission should expose the shortest complete route to one principal theorem. Historical front matter, source ledgers, validation material and unfinished alternative routes may remain in the repository without dominating the article.

### 22.11 Sharpen the generality route only after verification

If a broader top-four case is sought, formulate a reusable positive-annulus theorem with quantitatively checkable hypotheses and verify the persistence tail and complement in several genuinely different singular systems. The present Lorentz component theorem alone does not supply that breadth.

## 23. Technical and presentation comments

1. Keep the unweighted angular fraction, guard-weighted angular fraction and roof density distinct.
2. Keep the zero-width physical trace, the scale-weighted trace and the finite-width collar trace distinct.
3. State explicitly that the scale-weighted coefficient for positive birth order is not a nonzero zero-width atom.
4. Keep the old angular condition number and the new persistence number distinct.
5. Keep the certified analytic radius, inactive-sign radius, Morse radius and physical collar width distinct.
6. State that every one of those radii may shrink with the word length unless a separate theorem says otherwise.
7. Do not certify analytic identity by checking finitely many equal jets.
8. Preserve the full primitive sign list when identifying exact labels.
9. Keep coincident root germs as simultaneous primitive tests.
10. State that fixed cyclic order is one-sided in positive radius.
11. Keep boundary conventions separate from open-arc labels; angular endpoints have zero measure.
12. State that the first nonzero coefficient is positive because the physical angular fraction is nonnegative.
13. Do not infer a uniform birth-order bound from analyticity.
14. Keep the guard merely Lipschitz; do not call it analytic.
15. Do not divide by a zero center guard.
16. Keep the common coarea representative and the phrase “almost everywhere” in density statements.
17. Preserve the exact `2 pi` normalization in the angular fractions.
18. Keep `H`, `2H`, `h_chi`, `K`, `chi`, `epsilon` and the reconstruction band visibly distinct.
19. State `2K sqrt(H) < 1` wherever the annular denominator is used.
20. Keep the persistence subfamily independent of `H` before applying the collar theorem.
21. State that the birth orders are summed at fixed count before the collision limsup.
22. Do not introduce a count-dependent persistence cutoff.
23. Do not replace the positive outer annulus by a signed leading approximation.
24. Keep the interval of contributing centers `[t-H,t]` visible in the height proof.
25. Keep coincident critical values additive.
26. State that the ordered vanishing concerns a shrinking source restriction.
27. Keep the complete positive complement next to every partial height theorem.
28. Do not infer complement height from small support or small mass.
29. Keep the complete incidence term explicit in the final endpoint budget.
30. Preserve the finite arithmetic transition kernel and zero classes.
31. Keep probability total variation, variation mass, path bounded-Lipschitz dual and essential-supremum density norms distinct.
32. Do not infer pointwise bridge convergence from integrated bridge convergence.
33. Preserve the fixed-band order of limits.
34. Record both exact-SHA workflow runs, but keep workflow success separate from proof certification.
35. Preserve every false status flag until the corresponding complete theorem is actually proved.
36. Consider moving extensive provenance and validation discussion outside the journal narrative.

## 24. Final assessment

Revision 68 is a serious and mathematically coherent response to the revision-67 report.

It proves a correct-looking analytic classification of exact-label angular germs, including nonlinear sectors invisible to the tangent trace. It restores the original clearance guard through a relative persistence cutoff and obtains a positive outer-annulus comparison whose constant is independent of the finite birth order. Applied before the collision limit, this gives an ordered essential-height theorem for an original-source restriction containing all finite birth orders on each fixed persistence stratum.

I found no decisive error in modules 146--148. The constants and the order of limits in the new restricted theorem are internally consistent.

The advance nevertheless remains stratified and collar-local. The physical persistence tail is unproved, zero-center guards are excluded, the outer and uncovered positive source is unestimated, and the complete first-incidence height remains open. Therefore the complete clearance height and unrestricted pointwise raw-density theorem are not established.

The article also remains extraordinarily long, model-specific and dependent on continuum inputs which have not received independent specialist verification.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**

A focused specialist-journal paper centered on analytic angular births, positive annular comparison and ordered collar heights could be valuable if the inherited geometry survives expert audit. A future top-four submission should return only after the physical persistence tail, complete positive complement and incidence source have been controlled in the correct ordered regime, or after the mechanism has been extracted and independently verified as a substantially broader theorem.
