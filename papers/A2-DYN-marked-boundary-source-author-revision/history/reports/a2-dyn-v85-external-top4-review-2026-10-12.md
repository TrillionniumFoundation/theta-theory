# External top-four referee report on A2-DYN revision 85

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v85-referee-response-2026-10-12`, `revision/a2-dyn-v85-referee-copy-2026-10-12`  
**Reviewed commit:** `a2f03cccc6bdce440311f2a95f160e63f5c21a4b`  
**Reviewed repository tree:** `bf14c402dd487cfd89e535b5bb009fc8f0888bac`  
**Active manuscript directory:** `papers/A2-DYN-v85-referee-response`  
**Active mathematical source:** one hundred ninety-eight numbered core modules; revision 85 adds modules 196--198  
**Frozen revision-84 author baseline:** `f94ff549308db3fbba2087be0852c3f1e4d0739a`  
**Frozen revision-84 paper tree:** `ddae47df392cc5ca659cdef8250f96a0ff33fcab`  
**Controlling report:** `reviews/a2-dyn-v84-external-top4-review-2026-10-12/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `ef77954a0faa2677028edf971327edca35051ead` / `29a2d3e77b637e34b107d8b9638fea51bc104e64`  
**Exact-source qualification runs:** response `38194847968`; referee-copy `38194855539`  
**Date:** 12 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 85 is a genuine theorem-bearing response to the revision-84 report. It addresses, in a mathematically substantive way, two of the three positive surface-height blockers isolated there.

The new manuscript proves:

1. an explicit Borel parametrization of complete maximal regular roof segments, with a Borel inverse and the exact physical angular density;
2. a theorem-level audit of the cutoff-independent leading constant in the positive inverse-gradient source estimate, while retaining the cutoff-dependent finite-count remainder;
3. an essential-height estimate for every complete positive residence band, including all incoming endpoint types and critical outgoing restrictions;
4. a full surface-height bound of order `r^(1/32)` at every previously fixed positive residence cutoff, with a leading constant independent of that cutoff;
5. a critical short-surface bound of order `r^(129/256)(1+|log r|)` at every such cutoff;
6. the same positive-cutoff height bound for the full paired incoming assignment; and
7. an exact identification of the limiting full surface height with a zero-residence concentration charge, together with a comparison of that charge to an actual short-segment collision-source restriction through the inherited fractional optical potential.

I audited the new modules

- `core/196_measurable_segments_and_cutoff_audit.tex`;
- `core/197_complete_residence_band_heights.tex`;
- `core/198_zero_residence_charge_and_original_source.tex`;

and their direct use of the retained first-exit, surface-mass, inverse-gradient, optical-variation and microscopic-tail inputs. I also checked the revised opening, response to the referee, proof ledger, source manifest, specialist audit map, validation protocol, qualification workflow and final exact-SHA workflow conclusions.

I found no decisive counterexample, no reversal of the roof-flow direction, no erroneous dyadic exponent, no illicit collision-dependent cutoff, no hidden word-count factor in the written parametrization, and no promotion of a fixed positive-cutoff estimate to a zero-cutoff theorem.

In particular, revision 85 genuinely closes the revision-84 requests concerning

- the height of the paired short nongrazing assignment at every fixed positive residence cutoff;
- the height of the short critical surface at every fixed positive residence cutoff;
- the formal measurable map underlying the no-word-count transfer; and
- the independence of the leading positive-cutoff source constant from the cutoff.

The negative recommendation is forced by what remains. The article now reduces its organizing pointwise endpoint to two nonnegative microscopic charges:

\[
 \mathfrak A_{\eta,M}
 =\lim_{h\downarrow0}\mathcal H_M(\mathsf P_{\eta,h}v^\eta)
\]

and

\[
 \mathfrak B_M
 =\lim_{\delta\downarrow0}\mathcal H_M(\mathcal Z_\delta),
\]

or, after the proved comparison, the corresponding original short-segment volume charge `mathfrak Q_M` together with `mathfrak A_{eta,M}`.

Revision 85 does **not** prove that either charge is zero.

Its final bound is

\[
 \mathcal E_M\le
 C_MB^{-1/192}
 +C\mathfrak B_M
 +C_\eta\mathfrak A_{\eta,M}
 +C_\eta r^{1/32}
 +C_\Theta(1+\varepsilon(B)^{-1})\sqrt r.
\]

Thus the unrestricted exact-label pointwise raw local limit theorem remains unproved. So do the pointwise roof-density theorem and the unconditional same-roof path and likelihood conclusions which depend on scalar closure.

The new charge identities are valuable because they show precisely that every fixed positive residence scale is already controlled. They also show why a formal choice of a smaller cutoff cannot finish the proof: the complete tail remains inside the collision-normalized essential-height functional before the cutoff is removed.

At the requested benchmark, identifying the final two concentration mechanisms is not a substitute for proving that they vanish.

## 2. Frozen source, chronology and preservation

Both author branches resolve to

`a2f03cccc6bdce440311f2a95f160e63f5c21a4b`.

The repository tree is

`bf14c402dd487cfd89e535b5bb009fc8f0888bac`.

The active article is

`papers/A2-DYN-v85-referee-response/main.tex`,

and the complete inherited mathematical archive is assembled through

`papers/A2-DYN-v85-referee-response/supplement.tex`.

The author commit descends from the controlling revision-84 review commit. The frozen mathematical baseline is revision 84 at

`f94ff549308db3fbba2087be0852c3f1e4d0739a`,

with paper tree

`ddae47df392cc5ca659cdef8250f96a0ff33fcab`.

The source manifest records 195 inherited core modules and 198 active modules. The three new files are precisely modules 196--198. It also records preservation of the inherited Python sources, appendices, bibliographies, provenance records and the complete preceding article.

The manuscript retains the original

- circular Lorentz family;
- actual-return record;
- section and occupation convention;
- smooth physical guard;
- source normalization;
- exact return index, displacement and collision count;
- pointwise roof variable;
- finite arithmetic transition reference; and
- arithmetic zero classes.

It does not substitute a collision-count window, a fixed roof interval, a pooled occupation class, a removed source, or a smoothed event for the organizing endpoint.

The active manifest accurately distinguishes the new positive-cutoff results from the unproved zero-scale assertions. In particular, it leaves false the flags for

- zero fractional optical concentration;
- zero residence surface charge;
- zero short-segment original volume charge;
- the full raw return LLT;
- the pointwise roof-density LLT;
- unrestricted same-roof pair bridges;
- forward essential-likelihood convergence;
- independent human review; and
- formal proof certification.

This source-level restraint is mathematically important and should be preserved.

## 3. Qualification evidence and its boundary

The final exact-SHA qualification workflows completed successfully on both reviewed author refs:

- response branch run `38194847968`;
- referee-copy branch run `38194855539`.

Both runs identify the reviewed SHA and repository tree stated above.

According to the validation protocol and workflow, the qualification checks include

- the frozen revision-84 paper tree;
- the controlling revision-84 report blob;
- preservation of all inherited sources and root snapshots;
- inclusion of all 198 core modules across the focused article and complete supplement;
- ordinary and optimized finite diagnostics;
- native TeX compilation of both documents;
- stabilized references and warning gates;
- recorder coverage; and
- PDF word-box and rendered-page checks.

The focused article is reported as 19 pages and the complete supplement as 664 pages. These figures describe the built artifacts, not editorial suitability.

The checks are meaningful evidence of source identity, algebraic consistency and typesetting integrity. They do not certify

- the inherited anisotropic spectral insertion estimates;
- the complete first-exit surface local-mass theorem;
- the physical coarea normalization;
- one-sided optical traces at every endpoint type;
- the maximal-segment disintegration in the continuum billiard;
- cutoff-uniform inverse-gradient insertion beyond the written input;
- the two microscopic charge limits; or
- the full pointwise theorem.

The manuscript states this boundary correctly.

## 4. Scope of this review

The full archive now contains 198 core modules. I have not attempted to independently re-prove the entire historical pipeline.

The substantive audit concentrates on

1. the rational-roof Borel transversal;
2. angular-chart disjointization and the explicit inverse map;
3. the exact physical area and fiber densities;
4. the incident-component convention at outgoing faces;
5. the lower-gradient-cutoff layer-cake calculation;
6. persistence on complete residence bands;
7. the passage from local surface mass to actual essential height;
8. the critical outgoing restriction and its exponents;
9. the finite dyadic summation at a fixed positive residence cutoff;
10. the full paired incoming assignment;
11. the definition and monotonicity of the zero-residence charge;
12. the surface-to-volume comparison;
13. the two-charge endpoint budget;
14. the legal order of cutoffs and limits; and
15. source and workflow identity.

The inherited spectral, arithmetic, coarea, positive-remainder, path-remainder and collision-to-return chains are treated as source-pinned inputs, not as independently recertified results.

## 5. Borel parametrization of maximal regular segments

Module 196 fixes a collision count, parameter and exact labels, removes the critical set from the regular exact event, and considers the stopped physical flow with `XF=1` and constant angle coordinate.

The construction chooses, on each maximal open roof interval, the first rational in a fixed enumeration. It then uses the corresponding roof slice and countably many local angular charts, disjointized by first membership, to produce

\[
 \Psi:\coprod_j\{(\theta,u):\theta\in E_j,
 a_j(\theta)<u<b_j(\theta)\}\longrightarrow\Omega.
\]

The inverse is explicit: recover the maximal roof interval, choose its first enumerated rational, flow to that rational roof, and select the first angular chart containing the representative.

This is a coherent way to avoid an unproved measurable quotient of the flow into maximal segments. It also keeps angular-chart seams as Borel assignments rather than physical exits.

The proof then identifies the density

\[
 A_j(u,\theta)
 =\frac{\omega(\Psi_j(\theta,u))}
        {4\pi c_*\chi(\Psi_j(\theta,u))}
\]

and states the exact area identity

\[
 \int_\Omega f\,d\bar\nu
 =\sum_j\int_{E_j}\int_{a_j(\theta)}^{b_j(\theta)}
 f(\Psi_j(\theta,u))A_j(u,\theta)\,du\,d\theta.
\]

The outgoing face measure is correspondingly

\[
 d\zeta_+=A_j(b_j-,\theta)\,d\theta.
\]

The incident component is retained, so two geometrically coincident boundary points carried by different components are not silently identified.

I found no internal contradiction in this construction. It substantially improves the auditability of the paired-transfer argument.

The following remain specialist verification points:

- lower semicontinuity and Borel measurability of the stopped lifetimes on every exact-event component;
- compatibility of the angular charts with the endpoint-angle coarea convention;
- the countable determining-class passage from area identities to roof fibers;
- existence and measurability of the one-sided endpoint traces;
- removal of transverse null strata and their flow saturations; and
- injectivity of the nongrazing endpoint map with the incident-component convention.

These are not objections based on a discovered counterexample. They are load-bearing continuum steps for which software fixtures are not proof.

## 6. Audit of the positive inverse-gradient cutoff constant

Module 196 restates the finite-count critical-volume input, including its spectral remainder, and applies the positive layer-cake majorant

\[
 z^{-1}\mathbf1_{\{c\le z<b\}}
 \le b^{-1}\mathbf1_{\{z<b\}}
 +\int_c^b q^{-2}\mathbf1_{\{z<q\}}\,dq.
\]

With `alpha=129/128`, the leading coefficient becomes

\[
 b^{\alpha-1}
 +\int_c^b q^{\alpha-2}\,dq
 \le\left(1+\frac1{\alpha-1}\right)b^{\alpha-1},
\]

while the finite-count remainder contains

\[
 2C_{B_*}(1+B_*|J|)m^2c^{-1/2}\rho_{B_*}^{m/4}.
\]

The arithmetic is correct. The leading coefficient is independent of the positive lower cutoff `c`; the finite-count remainder is not.

The resulting theorem is correctly ordered:

1. fix `c`, the roof-window length and the auxiliary band;
2. take the collision limsup;
3. enlarge the auxiliary band.

It does not set `c=0`, nor does it allow `c` to depend on the collision count.

This is exactly the distinction needed in the paired-transfer proof. It supplies a common leading constant at `c_r=2 sqrt(Lambda r)` because `r` is fixed before the collision limit. It does not justify removing `c_r` inside that limit.

I found no hidden cutoff exchange in the new module.

## 7. Audited paired transfer

For a selected family of short noncritical segments, the outgoing and incoming assignments use the same exit-window kernel. The manuscript differentiates the full physical angular density, retaining both `omega` and `chi`, and uses

\[
 |\partial_uA|\le C A I_m/z.
\]

Radial growth keeps the entire selected segment above

\[
 c_r=2\sqrt{\Lambda_\circ r}.
\]

The variation between the two one-sided traces is therefore bounded by a physical volume integral over `(t-2r,t+2r)`. The new Borel parametrization identifies the sum over all selected sheets with a submeasure of the actual source `v^{c_r}` with multiplicity one.

Applying the cutoff-uniform fixed-window theorem gives a global ordered difference bound of order `r`.

At a grazing incoming endpoint, the incoming trace is zero because `omega` tends to zero while `chi` remains bounded below. The same argument then controls the entire outgoing component.

This closes the formal no-word-count objection in the previous report, subject to specialist verification of the density and trace statements.

It remains important that this transfer estimate alone controls an outgoing-minus-incoming difference. Revision 85 closes the positive incoming assignment itself only through the independent residence-band height argument described below.

## 8. Persistence on a complete residence band

For a nongrazing outgoing face with maximal backward residence `l=b-a`, the band source is

\[
 \mathcal B_s(t)
 =\int\mathbf1_{\{s<l\le2s\}}
       \mathbf1_{\{a<t<b\}}\,d\zeta.
\]

If the segment contains `t`, then the whole segment lies in `(t-2s,t+2s)`. On every interior roof `v` of the same segment,

\[
 k_{4s}(v;y)=1-\frac{b-v}{4s}\ge\frac12.
\]

The integrated kernel over the window is therefore at least `l/2>s/2`, yielding

\[
 \mathcal B_s(t)
 \le\frac2s\int_{t-2s}^{t+2s}
      \overline{\mathcal F}_{4s}(v)\,dv.
\]

This is a genuine persistence mechanism. It converts the inherited local surface-mass bound into an essential-height estimate. The argument does not infer height merely from small mass.

After division by `s`, the stated inherited local-mass exponents give

\[
 \limsup_m\sup_{R,n,k}m^2
 \|\mathcal B_s\|_\infty
 \le C_\eta s^{1/32}.
\]

All incoming endpoint types and outgoing gradients are retained.

I find the kernel direction, window size and normalization consistent.

## 9. Critical residence bands

The same band argument is restricted to outgoing faces with `z(b-)<b_0`. Forward radial monotonicity keeps the entire backward segment within the same small-gradient restriction.

The surface comparison then yields

\[
 \limsup_m\sup_{R,n,k}m^2
 \|\mathcal B_s^{[b_0]}\|_\infty
 \le Cb_0^\alpha
 +C_\eta s^{(1+\eta)/2}b_0^{\alpha-\eta}.
\]

At the natural threshold

\[
 b_0=\sqrt{8\Lambda_\circ s},
\]

the leading exponent is

\[
 \alpha/2=129/256,
\]

and the second exponent is

\[
 (1+\alpha)/2=257/256.
\]

Thus each complete critical residence band has an actual essential-height estimate of order `s^(129/256)`.

This is materially stronger than the revision-84 local-mass result with exponent `385/256`. The manuscript does not confuse the two.

No incoming endpoint type is removed in this band proof.

## 10. Summation at a fixed positive residence cutoff

Fix `r>0` and `delta>0` before taking the collision limit.

Long segments `l>2r` are controlled by the earlier long-residence persistence estimate. The remaining segments with `delta<=l<=2r` are covered by finitely many dyadic bands

\[
 (2^{-j}r,2^{1-j}r],
 \qquad 0\le j\le N,
\]

where `N` is chosen after `delta` but before the collision limit.

Because the physical sum is finite at this stage, the collision limsup may be applied after summing the selected bands. The numerical leading bounds form a convergent geometric series:

\[
 \sum_{j=0}^N(2^{-j}r)^{1/32}
 \le\frac{r^{1/32}}{1-2^{-1/32}},
\]

independently of `N` and hence of the positive cutoff `delta`.

This proves

\[
 \mathcal H_M(\overline{\mathcal F}_r^{\ge\delta})
 \le C_\eta r^{1/32}
\]

for every fixed positive `delta`, with one leading constant.

The critical sum uses the smaller of the unrestricted band estimate and the fixed outgoing-threshold estimate. The finite head contributes

\[
 C r^{129/256}(1+|\log r|),
\]

and the numerical tail is geometric. I found the head-tail exponent calculation consistent.

Finally, the complete short noncritical outgoing assignment is bounded by the full surface theorem, and the paired incoming assignment differs by `O(r)`. Since `r=O(r^(1/32))` for small `r`, the incoming assignment satisfies the same leading height bound.

Revision 85 therefore closes both positive short-surface height blockers from revision 84 at every fixed positive residence cutoff.

## 11. What cutoff-uniformity does and does not mean

The theorem's leading constants are independent of `delta`, but its statement still fixes `delta` before the collision limit.

This permits the subsequent sandwich argument for an ordered zero-residence charge. It does **not** imply a pre-limit estimate at `delta=0`, and it does not justify choosing a collision-dependent residence cutoff.

This distinction is not merely technical. A sequence of surfaces may concentrate on residence lengths tending to zero as the collision count grows, while every fixed positive cutoff family has a uniform small-height estimate.

The manuscript records precisely this possibility and does not claim an interchange.

## 12. The zero-residence surface charge

At finite count, define

\[
 \mathcal Z_\delta(t)
 =\int\mathbf1_{\{0<l\le\delta\}}
       \mathbf1_{\{a<t<b\}}\,d\zeta.
\]

Its ordered height decreases as `delta` decreases, so

\[
 \mathfrak B_M
 =\lim_{\delta\downarrow0}\mathcal H_M(\mathcal Z_\delta)
\]

is well defined as an extended nonnegative number.

For `delta<r`, the pointwise comparisons are

\[
 (1-\delta/r)\mathcal Z_\delta
 \le\overline{\mathcal F}_r
 \le\mathcal Z_\delta
     +\overline{\mathcal F}_r^{\ge\delta}.
\]

Applying the ordered height and only then letting `delta` decrease gives

\[
 \mathfrak B_M
 \le\mathfrak F_M^{\rm all}(r)
 \le\mathfrak B_M+C_\eta r^{1/32}.
\]

Consequently

\[
 \lim_{r\downarrow0}\mathfrak F_M^{\rm all}(r)
 =\mathfrak B_M.
\]

I find this sandwich argument correct as an identity of ordered obstructions, including the possibility that the charge is infinite.

Its conclusion is structural, not a vanishing theorem. It says that after all positive residence scales have been paid, the full surface endpoint is exactly the zero-residence concentration charge.

## 13. Comparison with the original short-segment collision source

The manuscript defines `q_delta` as the original collision volume measure restricted to actual maximal segments of total residence at most `delta` and with a nongrazing forward exit. It is not a boundary collar or a newly transported source.

In segment coordinates, `mathcal Z_delta` uses the outgoing trace

\[
 A_j(b_j-,\theta),
\]

whereas `q_delta` uses the interior density

\[
 A_j(t,\theta)
\]

on the same segment and at the same roof.

The variation estimate gives

\[
 |A_j(b_j-,\theta)-A_j(t,\theta)|
 \le C\int_t^{b_j}
       A_j(u,\theta)I_m(u,\theta)/z(u,\theta)\,du.
\]

Radial growth implies, for `u=t+s`,

\[
 z(u)\ge\sqrt{2\lambda_\circ s},
\]

and hence

\[
 z(u)^{-1}
 \le C_\eta s^{-(1-\eta)/2}z(u)^{-\eta}.
\]

The Borel segment map identifies the fiber sum with a submeasure of the actual fractional volume source. Tonelli then yields

\[
 |\mathcal Z_\delta-q_\delta|
 \le C_\eta\mathsf P_{\eta,\delta}v^\eta.
\]

Passing to the ordered charges gives

\[
 \mathfrak B_M
 \le\mathfrak Q_M+C_\eta\mathfrak A_{\eta,M},
 \qquad
 \mathfrak Q_M
 \le\mathfrak B_M+C_\eta\mathfrak A_{\eta,M}.
\]

This is a useful source-level identification. When the fractional charge is zero, the zero-residence surface charge equals the original short-segment volume charge.

Again, the theorem compares two possible concentration mechanisms. It does not prove either one absent.

A specialist should verify that the target-direction fractional potential used here has exactly the offset convention stated in the active corrected theorem and not the superseded historical display.

## 14. The fractional microscopic charge

The canonical fractional charge is

\[
 \mathfrak A_{\eta,M}
 =\lim_{h\downarrow0}
   \mathcal H_M(\mathsf P_{\eta,h}v^\eta).
\]

Revision 85 restates the full dyadic domain, proves the outer-width invariance in the corrected offset convention, and keeps the complete finite-count tail inside the ordered height before its microscopic width is removed.

The resulting comparison is internally coherent. It has the same important negative implication as in revision 84: a nonzero charge cannot be paid by choosing a smaller dyadically related outer width.

No new estimate in revision 85 proves

\[
 \mathfrak A_{\eta,M}=0.
\]

The complete weak-`L^q`, fixed-width and positive-cutoff estimates do not by themselves imply this ordered uniform-integrability statement.

## 15. The final endpoint theorem

The final theorem gives

\[
 \mathcal E_M\le
 C_MB^{-1/192}
 +C\mathfrak B_M
 +C_\eta\mathfrak A_{\eta,M}
 +C_\eta r^{1/32}
 +C_\Theta(1+\varepsilon(B)^{-1})\sqrt r.
\]

Equivalently, after the trace-volume comparison, one may use `mathfrak Q_M` and `mathfrak A_{eta,M}`.

The legal order is retained:

1. fix `B`;
2. fix `epsilon(B)`, `eta`, `r`, every positive residence and gradient cutoff, and all auxiliary bands;
3. take the collision-count limsup and exact-label suprema;
4. enlarge auxiliary bands;
5. choose the outer relation between `r` and `epsilon(B)`; and
6. send `B` to infinity last.

If both microscopic charges vanish, choosing

\[
 r(B)=c\varepsilon(B)^\gamma,
 \qquad \gamma>2,
\]

makes every explicit error tend to zero.

This is a correct conditional closure statement. The conditions are not proved.

Accordingly, revision 85 does not establish

- the unrestricted exact-label scalar pointwise raw LLT;
- the pointwise roof-density LLT;
- a uniform positive pointwise denominator on all positive arithmetic classes;
- unconditional same-roof collision path conditioning;
- the actual-return path bridge after clock transfer; or
- forward essential arithmetic likelihood convergence.

The manuscript correctly leaves these conclusions unpromoted.

## 16. Are the remaining charges plausibly minor?

No such conclusion follows from the present manuscript.

Both charges encode concentration on scales which vanish with the collision count before the outer cutoff is removed. This behavior is invisible to any family of estimates in which the microscopic cutoff is fixed first.

The proved bounds imply excellent control of

- every fixed positive residence band;
- every fixed positive gradient cutoff;
- every fixed roof window;
- several weak or fractional norms; and
- the complete positive surface away from zero residence.

They do not rule out a sequence of narrow high peaks whose residence and optical scales collapse with `m` while preserving a nonzero normalized essential height.

A proof of zero charge therefore needs a genuinely collision-uniform envelope, a Carleson-type estimate, an equiintegrability theorem, a monotonicity mechanism, or another source-specific argument which acts before the microscopic cutoff is removed.

This is the main mathematical task for the next revision.

## 17. Mathematical significance at the requested benchmark

The manuscript contains an unusually extensive body of geometric, arithmetic and operator work. The recent revisions have progressively converted informal or conditional obstructions into precise source-level theorems.

Revision 85 is a substantial advance. It proves actual essential-height estimates on every positive residence scale and gives a formal measurable segment disintegration. These are not cosmetic changes.

Nevertheless, the requested four-journal benchmark is governed by completed theorems. The title, abstract and opening continue to organize the article around the unrestricted exact-label pointwise raw local limit theorem. That theorem is still conditional on two unproved zero-charge assertions.

The charges are not ancillary presentation issues. They are the complete remaining endpoint after the positive-scale analysis. The manuscript's own rigidity statements explain why they cannot be removed by a change of outer width.

At this level, the paper needs either

1. a proof that both microscopic charges vanish, followed by the unconditional scalar and downstream theorems; or
2. a separate broad theorem of independent significance whose main statement and applications do not depend editorially on the unfinished Lorentz endpoint.

Revision 85 supplies neither yet.

## 18. Presentation and architecture

The focused 19-page article is much easier to audit than the historical pipeline. It states the unchanged problem, lists the exact retained inputs, proves the new modules, and gives the current endpoint budget.

The complete 664-page supplement remains an archival object rather than a conventional journal supplement. The new input/equation/proof-page guide is a useful improvement, but independent verification of the load-bearing inherited results is still necessary.

Before a formal submission I recommend an even sharper separation between

- the principal journal theorem and indispensable proof;
- a technical supplement containing only the inherited machinery actually used;
- provenance and historical revision material; and
- finite diagnostics and build records.

The article should continue to state prominently that the two microscopic charge-zero assertions remain open.

## 19. Required mathematical changes before another top-four review

### 19.1. Prove zero fractional optical concentration

Establish

\[
 \mathfrak A_{\eta,M}=0
\]

for a fixed admissible `eta`, uniformly in radius and exact labels, with the complete microscopic potential inside the ordered height before the cutoff is removed.

A collection of fixed-width or fixed-cutoff estimates is insufficient. The proof must control collapsing optical scales before the collision limsup.

### 19.2. Prove zero residence concentration

Establish

\[
 \mathfrak B_M=0,
\]

or equivalently, once the fractional charge is zero,

\[
 \mathfrak Q_M=0.
\]

This requires a collision-uniform estimate for actual maximal segments whose total regular residence tends to zero. The result must preserve the original exact labels, section decisions and physical source.

### 19.3. Close the scalar pointwise theorem before promoting downstream laws

After the two charge-zero theorems are proved, state and prove the unrestricted scalar endpoint in the main article. Only then should the pointwise denominator, same-roof path bridge, actual-return bridge and forward likelihood be promoted from conditional consequences.

No arithmetic zero class should be normalized.

### 19.4. Obtain independent specialist verification

At minimum, independent experts should audit

- the inherited anisotropic spectral insertion;
- the physical coarea and angular-density normalization;
- the Borel maximal-segment parametrization;
- endpoint trace and incident-component conventions;
- the cutoff layer-cake calculation and its finite-count remainder;
- the complete residence-band persistence argument;
- the fractional-potential offset convention; and
- both microscopic charge limit orders.

### 19.5. State any eventual envelope in a reusable theorem

If the charge-zero proof uses a Carleson or equiintegrability estimate, formulate it at theorem level with explicit dependence on radius, exact labels, collision count and microscopic scales. This would make the final closure auditable and potentially reusable beyond the present endpoint.

## 20. Expository comments

1. Keep the distinction between a constant independent of a **fixed positive cutoff** and a theorem valid at cutoff zero in every summary statement.
2. The symbols `b` for an endpoint roof and `b_0` for a gradient threshold are close; a more distinct threshold symbol would reduce ambiguity.
3. State the precise null-set convention for the fiber identities at the first use of the Borel segment map in the focused article.
4. In the cutoff-surface theorem, explicitly note that the number of physical bands is finite before the collision limsup; this is central to the logic.
5. Keep the exponent calculations `129/256` and `257/256` visible near the critical-band theorem.
6. In the final endpoint theorem, display both equivalent unresolved pairs: `(mathfrak A, mathfrak B)` and `(mathfrak A, mathfrak Q)`.
7. The supplement's dependency guide should continue to identify the exact active correction to the historical module-189 offset display.
8. Build and finite-regression evidence should remain separated from mathematical certification language.
9. The phrase “complete surface estimate” should always be qualified by “at every fixed positive residence cutoff” until `mathfrak B_M=0` is proved.
10. The abstract's final sentence accurately states the two remaining requirements and should be retained.

## 21. Final assessment

Revision 85 is a substantial mathematical advance over revision 84.

It proves

- a Borel bijection for maximal regular segments with exact physical density;
- a theorem-level audit of cutoff-independent leading constants;
- essential-height bounds for every complete positive residence band;
- a complete positive-cutoff surface bound of order `r^(1/32)`;
- a positive-cutoff critical surface bound of order `r^(129/256)(1+|log r|)`;
- the corresponding paired incoming height bound;
- an exact zero-residence surface charge identity; and
- a comparison with the original short-segment collision source through the fractional optical potential.

I found no decisive flaw in these new arguments at the level of this referee-style audit. Their continuum parametrization, inherited source estimates and endpoint traces still require independent specialist verification.

The revision does not prove

- zero fractional optical concentration;
- zero residence or short-segment volume concentration;
- the unrestricted exact-label pointwise raw LLT;
- the pointwise roof-density LLT; or
- the unconditional same-roof path and likelihood consequences.

The organizing theorem therefore remains open inside the submitted manuscript.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
