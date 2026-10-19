# External top-four referee report on the A2-DYN clearance-to-roof and critical-stability author revision

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author refs:** `revision/a2-dyn-clearance-roof-2026-10-15`, `revision/a2-dyn-v114-clearance-roof-author-revision-2026-10-15`  
**Reviewed current author head:** `d98549fc721f757ad2a4b5918d57110368acbf9f`  
**Current repository tree:** `9b3e596785310ecb01538ddab718d4664e404ec4`  
**Theorem-bearing author commit:** `8a5a7c2be5630bf5919e9f74ee79de01af0dbb85`  
**Theorem-bearing repository tree:** `45d94258a8be8bc49fb01c620213f4c17e0a7f38`  
**Published article tree recorded by the author:** `c2e9e83f39985a34690300433f4b40de4f1f88ac`  
**Active manuscript directory:** `papers/A2-DYN-clearance-roof-2026-10-15`  
**Newly published mathematical modules relative to the last theorem-bearing remote manuscript:** `core/270_exact_clearance_flux.tex` through `core/275_critical_roofs_reversibility_and_stability.tex`  
**Modules counted by the author as new in the present local revision:** 274--275  
**Immediate theorem-bearing baseline:** revision 112, commit `45015de51c652bcdaca13123bf65627bf199b2ab`  
**Controlling report:** `reviews/a2-dyn-v112-incidence-load-external-top4-review-2026-10-14/REFEREE_REPORT.md`  
**Controlling review commit / report blob:** `d7fd0b24314d7341f9a611130bb650371d2d5ef2` / `0ad9f500c92db32ea4fc9f6d9ee28630b4484699`  
**Exact-SHA qualification at review freeze:** theorem-bearing run `38821386148`, queued; current-head run `38828204759`, pending; conclusion `null` for both  
**Local build evidence:** passed; revised article 47 pages; zero unresolved references, duplicate labels, or overfull boxes in the recorded final build  
**Date:** 15 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, an independent human billiards or transfer-operator audit, or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

This is a genuine theorem-bearing author revision.

It should not be confused with the workflow-only revision-113 branch.

The substantive manuscript was first published at

`8a5a7c2be5630bf5919e9f74ee79de01af0dbb85`.

The current author head

`d98549fc721f757ad2a4b5918d57110368acbf9f`

adds only a post-push publication receipt and leaves the mathematical article unchanged.

The revision contains real new mathematics.

In particular, it establishes:

1. an exact one-copy flux formula for unvisited-disk near misses;
2. a grazing-uniform transverse strip estimate on short physical test curves;
3. arbitrary-time stable-test propagation, conditional on an explicitly retained homogeneous-curve growth input;
4. an exact disintegration of physically marked exact records over the clearance coordinate;
5. the long-record clearance-to-endpoint and roof--Gauss Jacobians;
6. local positive roof-density bounds for finite-type charts and integrated angular folds;
7. a characterization of regular critical roofs as halves of actual reversing periodic orbits;
8. an exact monodromy determinant identity at a critical roof;
9. a selector-uniform local critical-roof coarea formula with an explicit coefficient and error;
10. a finite-count positive sum of the regular critical coefficients, relative to the retained pressure input.

I audited modules 270--275 because all six are newly present in the remote theorem-bearing manuscript relative to the revision-112 paper reviewed previously.

The author distinguishes modules 270--273 as inherited local work and modules 274--275 as the new response.

That provenance distinction is appropriate, but it does not remove modules 270--273 from the mathematical scope of the present external review.

Within the hypotheses actually stated in these six modules, I found no decisive normalization error, reversed Jacobian, missing section factor, incorrect fold constant, sign error in the return derivative, invalid positive-source subtraction, hidden independence assumption, or uncontrolled insertion of the number of collision words.

The new local formulae are coherent and in several places elegant.

The negative recommendation is nevertheless forced by the exact endpoint of the argument.

The organizing assertion remains the original exact-label raw pointwise local limit theorem, equivalently the remaining positive shortage limit

\[
 \lim_{B\to\infty}\limsup_{m\to\infty}
 \sup_{R,n,k}m^2
 \operatorname*{ess\,sup}_{t\in\mathcal C_{m,R,n,k}(M)}
 \bigl(
   \mathsf U_{B,m}^{\rm low}(t)
   -K_BP_{r_B,m}^{\rm ng}(t)
 \bigr)_+
 =0.
\]

No theorem in the revision proves this limit.

The clearance results are either:

- integrated mass identities;
- stable-test estimates in a norm weaker than the required roofwise essential height;
- local chart estimates with chart-dependent constants;
- conditional sufficient bridges;
- or unscaled finite-count coefficient sums.

They have not been assembled into a collision-uniform, all-chart, exact-label bound in the required

\[
 m^2L^\infty(dt)
\]

topology.

The manuscript states this boundary honestly.

The source ledger and publication flags continue to leave false:

- the uniform normalized clearance chart sum;
- the remaining low-incidence-load shortage decay;
- full comparison-capacity abundance;
- the full raw return LLT;
- the four-coordinate inversion conclusion;
- closure of the primary referee request;
- independent human review;
- and formal proof certification.

Thus the revision advances the correct obstruction but does not close it.

At the requested benchmark, substantial local calculations do not substitute for the incomplete global theorem around which the article is organized.

## 2. Frozen source and chronology

The relevant Git chronology is now clear.

### 2.1. The last reviewed theorem-bearing baseline

Revision 112 is frozen at

`45015de51c652bcdaca13123bf65627bf199b2ab`.

Its repository tree is

`f377dc19c5df4be7c620e0bbed2caabf3b28042d`.

Its active manuscript directory is

`papers/A2-DYN-v112-referee-response`.

The controlling revision-112 report was added at

`d7fd0b24314d7341f9a611130bb650371d2d5ef2`.

That report identified the low-incidence-load and clearance shortage as the decisive remaining positive source.

### 2.2. Workflow-only preparation branches

The branch

`revision/a2-dyn-v113-clearance-geometry-2026-10-15`

at

`3d91709d12db4a292f212d07304ff036f594d892`

contains only a source-export workflow beyond the revision-112 review commit.

It is not a theorem-bearing manuscript.

The separate clearance-coarea preparation branch was likewise workflow-only at the checked head.

Those branch names do not constitute scientific baselines.

### 2.3. The theorem-bearing clearance-roof delivery

The actual author delivery is the commit

`8a5a7c2be5630bf5919e9f74ee79de01af0dbb85`.

It is one commit ahead of the revision-112 review commit and adds the isolated manuscript directory

`papers/A2-DYN-clearance-roof-2026-10-15`

plus its dedicated workflow.

The commit message records a 206-file delivery and identifies modules 260--275 as the active source chain.

The complete new article is 47 pages in the recorded local build.

### 2.4. The current author head

The current author refs

- `revision/a2-dyn-clearance-roof-2026-10-15`;
- `revision/a2-dyn-v114-clearance-roof-author-revision-2026-10-15`

both resolve to

`d98549fc721f757ad2a4b5918d57110368acbf9f`.

This head has the theorem-bearing commit as its parent and adds only

`A2_DYN_CLEARANCE_ROOF_REMOTE_PUBLICATION_RECEIPT_20261015.md`.

The receipt correctly explains that the manuscript's internal `REVISION_BASE.json`, `PUBLICATION_STATUS.json`, and validation notes are frozen pre-push records.

The present report therefore reviews the mathematical source at the theorem-bearing parent while using the current author head as the branch base so that the post-push provenance correction is retained.

### 2.5. Review-branch isolation

The present review branch starts directly from the current author head.

It adds only

`reviews/a2-dyn-clearance-roof-external-top4-review-2026-10-15/REFEREE_REPORT.md`.

No author manuscript, workflow, source receipt, prior review, historical archive, or unrelated paper is intentionally modified.

## 3. Qualification evidence and its boundary

The dedicated workflow is

`.github/workflows/a2-dyn-clearance-roof-20261015.yml`.

At the freeze of this report:

- run `38821386148` at the theorem-bearing commit was queued;
- run `38828204759` at the current author head was pending;
- neither had a conclusion.

I therefore do not describe the present author head as remotely qualified at the review freeze.

The local completion receipt reports:

- a successful exact-source and diagnostic build;
- three pdfLaTeX passes for both the baseline and revised article;
- a 31-page rebuilt baseline;
- a 47-page revised article;
- zero unresolved references;
- zero multiply defined labels;
- zero overfull boxes;
- agreement between ordinary and optimized Python diagnostics;
- and successful checks of the clearance, critical-coarea, finite, load, research, manifest, and source programs.

These are meaningful reproducibility and implementation checks.

They do not certify:

1. the original incident-component pairing construction;
2. the family-uniform pressure theorem;
3. the stable optical comparison on every relevant physical branch;
4. the curve-growth input in exactly the stated varying-radius coordinates;
5. a complete chart decomposition of the clearance source;
6. uniform finite-type or fold constants across all words and collision counts;
7. collision-uniform control of the critical coarea remainders;
8. the pointwise bridge from clearance disintegration to the roof density;
9. capacity abundance of the full nongrazing pool;
10. the remaining low-incidence source;
11. the original raw pointwise LLT;
12. or the four-coordinate inverse problem.

The manuscript generally maintains this distinction correctly.

## 4. Scope of this review

The substantive audit concentrates on:

1. the exact one-copy clearance-flux change of variables;
2. the factor of `R` and the section normalization;
3. physical multiplicity of unvisited centers;
4. the forward and past-flight transverse derivatives;
5. the stable-test propagation under the retained growth input;
6. the exact-record clearance disintegration;
7. the strength and quantifiers of the proposed pointwise bridge;
8. the long-record clearance-to-endpoint Jacobian;
9. the noncritical Hessian chain term;
10. the one-dimensional finite-type band lemma;
11. the integrated simple-fold estimate;
12. criticality and physical reversibility;
13. the half-map generating derivative;
14. the return-stability determinant;
15. the local polar coarea normalization;
16. arbitrary Borel exact-event cuts;
17. one-sided unvisited tangency and section boundaries;
18. the finite-count critical coefficient sum;
19. the order of limits;
20. and the exact classes which remain unpaid.

Modules 260--269 are treated as the source-pinned revision-112 baseline except where their formulae are needed to check the new deductions.

This report does not independently reconstruct the complete historical spectral, arithmetic, pressure, pairing, and inversion chain.

## 5. Exact clearance flux

Module 270 introduces a genuine unvisited near-miss count on the original physical flights.

It does not insert an extra reflection and does not alter the collision clock.

For a marked center the signed impact coordinate is

\[
 b=(z-q)\cdot v_\vartheta^\perp.
\]

The local change of variables satisfies

\[
 \left|\det D_{(\alpha,p)}(\vartheta,b)\right|=R,
 \qquad
 d\nu=\frac{d\vartheta\,db}{4\pi R}.
\]

The two impact signs correspond to

\[
 b=\pm(R+u).
\]

The resulting identity is

\[
 \int\sum_{z\in\mathcal Z_\delta(x)}a(x,z)\,d\nu(x)
 =
 \frac{1}{4\pi R}
 \sum_{\sigma=\pm1}
 \int_0^{2\pi}\int_0^\delta
 a(X_R(\vartheta,\sigma,u),Z_R(\vartheta,\sigma,u))
 \,du\,d\vartheta.
\]

Setting `a=1` gives

\[
 \int N_\delta\,d\nu=\frac{\delta}{R}.
\]

I found the radius and sign factors consistent.

The geometric inverse is also correctly tied to actual flights.

The disk of radius `R+delta_*` around the marked center is disjoint from every other actual disk in the stated radius interval.

Following the oriented line to the nearest actual collision in each direction therefore produces one physical flight which misses the marked disk.

Different marked centers on the same flight remain distinct copies.

This is a useful exact identity.

It is, however, an integrated collision-measure statement.

It has no `m^{-2}` gain and by itself gives no target-roof density estimate.

The manuscript correctly says so.

## 6. Transverse clearance geometry

Module 271 proves a one-flight strip estimate which remains nondegenerate near grazing.

On an increasing-slope graph the direction angle is

\[
 \vartheta=s/R+\varphi(s),
\]

and for a candidate center

\[
 b_z'=-\cos\varphi-t_z\vartheta'.
\]

At a physical near miss the perpendicular-foot estimate gives a positive lower bound for `t_z`.

Thus the term

\[
 t_z\vartheta'
\]

supplies transversality even when `cos(varphi)` tends to zero.

The proof also avoids an uncontrolled component count.

For one candidate center, the relative angle `beta-vartheta` is strictly monotone and has variation at most `pi/2` on the chosen short graph.

Consequently the forward-foot region is a single interval and each impact band is crossed at most once.

Summing over the finite one-flight candidate set gives

\[
 |W^+\cap E_\delta^+|
 \,\le\,
 C_{\rm geo}\delta.
\]

Time reversal gives the corresponding past-flight estimate on decreasing-slope stable tests.

Within the declared coordinate convention and curve-length threshold, I found no sign reversal in this argument.

The theorem is nevertheless one-flight and one-test-curve geometry.

It is not yet the required complete roof-density estimate.

## 7. Stable-test propagation

Module 272 separates its genuinely new geometric estimate from an inherited dynamical input.

The additional input is the homogeneous inverse-curve growth bound

\[
 \sum_{V\in\mathcal G_l(W)}
 \sup_V J_VT_R^l
 \le C_g.
\]

Assuming this input in precisely the stated coordinates, the proof changes variables over the inverse branches and applies the past-flight strip bound.

For a bounded function supported on the marked event it obtains

\[
 \int_W
 |\mathcal L_{R,\xi}^{\,l}h|\,d\ell
 \le
 H\min\{|W|,C_gC_{\rm geo}\delta\}.
\]

It follows that

\[
 \mathcal S_a(
 \mathcal L_{R,\xi}^{\,l}h)
 \le
 H(C_gC_{\rm geo}\delta)^{1-a},
 \qquad 0\le a<1.
\]

The modulus-one twists cause no frequency loss in this absolute seminorm.

The all-depth schedule then gives a bound of order

\[
 \varepsilon^{1-a}
\]

in the stable-test seminorm.

This is a valid conditional consequence of the declared growth interface.

It does not provide decay in the unbounded roof frequency.

It does not show that the Fourier inversion is integrable.

It does not imply a roofwise `L^infty` density estimate.

The paper correctly distinguishes these facts.

A specialist audit must still match the varying-radius collision coordinates, homogeneous partitions, arclength Jacobian, subdivision convention, and curvature bounds to the exact external curve-growth theorem.

## 8. Exact-record disintegration

Module 273 keeps the original return, displacement, occupation, and roof labels.

For almost every clearance `u` it defines the positive roof measure

\[
 \mathcal K_{m,R,n,k,j,u}(A)
 =
 \sum_{\sigma=\pm1}
 \int_0^{2\pi}
 \mathbf1_{\Pi_{n,k,m,R}}(X_{R,j})
 \mathbf1_{\{L_{m,R}(X_{R,j})\in A\}}
 \,d\vartheta.
\]

The exact disintegration is

\[
 \int
 \mathbf1_\Pi
 N_\delta(T_R^jx)
 \mathbf1_{\{L_{m,R}\in A\}}
 \,d\nu_R^*
 =
 \frac{1}{4\pi Rc_*}
 \int_0^\delta
 \mathcal K_{m,R,n,k,j,u}(A)
 \,du.
\]

The factor contains one section normalization, not two.

The initial-section conditioning is used only once.

The mark does not create a second conditioned probability space.

I found this normalization consistent with the flux identity.

The same module then states a sufficient bridge:

\[
 \mathcal K_{m,R,n,k,j,u}ig|_{\mathcal C_{m,R,n,k}(M)}
 \le C_Mm^{-2}\,dt.
\]

If this held uniformly, the complete clearance witness source would have the correct normalized height.

The manuscript is explicit that this bridge is unproved.

This is important.

The exact disintegration by itself allows the conditional roof measure to be singular.

The stable-test estimate does not establish absolute continuity of each kernel.

The bridge remains one of the principal mathematical obligations.

## 9. The long-record Jacobian

Module 274 composes the line-coordinate map, the actual inverse collision iterate, and the endpoint map.

It obtains

\[
 |\det D\mathcal Q_j|
 =
 \frac{1}{R\omega}.
\]

Away from the critical set it obtains

\[
 \left|
 \det D_{(\vartheta,u)}(S,\arg\nabla F)
 \right|
 =
 \frac{\chi}{R\omega}.
\]

The normalization check is correct:

\[
 \frac{1}{4\pi Rc_*}
 \left/
 \frac{\chi}{R\omega}
 \right.
 =
 \frac{\omega}{4\pi c_*\chi}.
\]

There is no extra radius or section factor.

The Hessian identity

\[
 D^2S
 =
 A^{\mathsf T}GA
 +
 \sum_{a=1}^2g_aD^2(\mathcal Q_j)_a
\]

is also correctly retained.

The second term vanishes only at a critical roof.

The paper does not improperly discard it in the noncritical regime.

At a critical roof the determinant identity becomes

\[
 \sqrt{\det D^2S}
 =
 \frac{\sqrt{\det G}}{R\omega}.
\]

The derived determinant lower bounds are genuine product bounds.

They do not control individual singular values, chart condition numbers, or the number and weight of charts.

The paper states this limitation correctly.

## 10. The finite-type band lemma

The one-dimensional band estimate is proved rather than cited.

For a `C^ell` function with

\[
 |f^{(\ell)}|\ge\kappa,
\]

it obtains

\[
 |\{a<f<a+h\}|
 \le
 2\ell(h/\kappa)^{1/\ell}.
\]

The divided-difference proof uses `ell+1` measure quantiles.

The spacing gives the factorial denominators

\[
 i!(\ell-i)!.
\]

The sum produces the safe coefficient `2ell`.

I found no missing factorial or sign condition in this lemma.

## 11. Local finite-type clearance slices

On a chart with

\[
 0<b_f\le |S_u|\le B_f,
 \qquad
 |\partial_\vartheta^\ell S(\vartheta,0)|
 \ge\kappa_f,
\]

module 274 obtains

\[
 \|D_{E,h,\delta}\|_\infty
 \le
 \frac{2\ell H_f}{b_f}
 \left(
   \frac{B_f\delta}{\kappa_f}
 \right)^{1/\ell}.
\]

The proof first inverts the clearance coordinate at fixed angle.

The inverse condition places the base roof `S(theta,0)` inside a band of width `B_f delta`.

The band lemma then bounds the angular measure of that set.

Arbitrary Borel event cuts only reduce the integral.

This is a sound local conditional theorem.

The manuscript does not prove that every physical chart has such a finite type with collision-uniform order and constants.

It does not provide a summable decomposition of the complete exact-label source into such charts.

Those missing statements are decisive for the main theorem.

## 12. Integrated simple folds

The simple-fold theorem assumes

\[
 S_{\vartheta\vartheta}\ge a_f>0,
 \qquad
 S_u\ge b_f>0,
\]

and a unique angular critical point for each clearance.

At fixed clearance the angular density can have a square-root singularity.

The manuscript integrates that singularity over the transverse clearance coordinate before taking the roof supremum.

The resulting estimate is

\[
 \|D_{E,h,\delta}\|_\infty
 \le
 2H_f
 \sqrt{
   \frac{2\delta}{a_fb_f}
 }.
\]

The proof uses

\[
 |S_\vartheta|^2
 \ge
 2a_f(S-v(u))
\]

and

\[
 v'(u)\ge b_f.
\]

The constant agrees with the normal form

\[
 S(\vartheta,u)=\vartheta^2+u.
\]

This is a real improvement over requiring a bounded density at every fixed clearance.

It is nevertheless local.

The paper has not proved:

- that all noncritical clearance charts are finite type or simple folds;
- that the constants `a_f`, `b_f`, `kappa_f`, `B_f`, and the chart weights have a collision-uniform weighted sum;
- or that charts with `S_u=0` and higher degeneracy are negligible in the required topology.

## 13. Critical roofs and physical reversibility

Module 275 uses the retained first variation

\[
 \nabla_qF=R(-p_0,p_m).
\]

Thus a regular endpoint roof is critical exactly when

\[
 p_0=p_m=0.
\]

At the normal terminal collision the reflected velocity reverses the incoming velocity.

The trajectory retraces its actual flights and closes after `2m` collisions.

The doubled displacement is zero and the roof is `2t_x`.

The occupation identity is correctly written as

\[
 A_{2m,R}(x)
 =
 A_{m,R}(x)
 +
 A^{\mathcal I}_{m,R}(x).
\]

The manuscript does not replace the second term by the forward occupation without checking reversal of the section tests.

This is the correct level of care.

## 14. The return-stability determinant

Let

\[
 G_x=
 \begin{pmatrix}
 a&e\\
 e&d
 \end{pmatrix},
 \qquad
 \Delta_x=ad-e^2>0.
\]

The generating derivative of the half map is

\[
 B_x
 =
 \begin{pmatrix}
 -a/e&-R/e\\
 -\Delta_x/(Re)&-d/e
 \end{pmatrix},
 \qquad
 \det B_x=1.
\]

The sign of `e` is retained in this matrix.

At the normal endpoints, reversibility gives

\[
 \mathcal M_x
 =
 J B_x^{-1}J B_x,
 \qquad
 J=\operatorname{diag}(1,-1).
\]

For a determinant-one matrix,

\[
 \operatorname{tr}(J B^{-1}JB)-2
 =
 4b_{12}b_{21}.
\]

Substitution yields

\[
 \operatorname{tr}\mathcal M_x-2
 =
 \frac{4\Delta_x}{e^2}
 =
 |\det(I-\mathcal M_x)|.
\]

The critical coefficient is therefore

\[
 \mathfrak J(x)
 =
 \frac{\omega(x)}{2c_*\sqrt{\det G_x}}
 =
 \frac{1}{
   Rc_*\sqrt{|\det(I-DT_R^{2m}(x))|}
 }.
\]

I found the factor of four, the absolute determinant, and the radius normalization consistent.

The coefficient is a local density coefficient for nearby collision area.

It is not a conditional probability on the periodic orbit and not a periodic-orbit trace formula.

The paper states this correctly.

## 15. Critical-roof coarea

The critical coarea theorem normalizes endpoint coordinates by

\[
 y=G_x^{1/2}(q-q_x).
\]

Then

\[
 D^2f(0)=I_2.
\]

The collision density in the `y` coordinate is

\[
 w(y)\,dy,
 \qquad
 w(y)=
 \frac{\omega(q)}{4\pi c_*\sqrt{\det G_x}}.
\]

The radial substitution gives

\[
 D_E(t_x+s)
 =
 \int_0^{2\pi}
 \mathbf1_E(q_s(\theta))
 w(r_se(\theta))
 \frac{r_s}{\partial_rf(r_se(\theta))}
 \,d\theta.
\]

The polar factor is essential.

It produces

\[
 2\pi w(0)=\mathfrak J(x),
\]

not one half of that value.

The error estimate

\[
 \left|
 D_E(t_x+s)
 -
 \mathfrak J(x)a_E(s)
 \right|
 \le
 2\pi\sqrt3
 \{2L_w+Kw(0)\}
 \sqrt{s}
\]

is uniform over the Borel selector on the fixed chart.

The proof does not differentiate the selector.

For a regular finite collection of boundary inequalities, the limiting sector fraction is taken after the `G_x^{-1/2}` transformation.

For a general Borel selector the exact angular fraction is retained.

This is mathematically appropriate.

The local radius, third-derivative constant, and weight modulus are not uniform in `m` or in the physical word.

The theorem therefore does not provide the collision-uniform critical budget required by the organizing limit.

## 16. One-sided unvisited boundaries

At an unvisited-disk tangency or a section cut, the manuscript uses a smooth extension of the visited finite-itinerary action only as a calculus device.

It retains the actual physical side as a Borel selector.

It does not assert that the physical billiard map extends through the forbidden side.

It does not assign zero coefficient merely because the limiting boundary point has zero collision area.

Visited grazing remains under the inherited trace argument.

This distinction is correct and important.

What remains unproved is compatibility with the complete global pairing construction, the collision-uniform sum of all such one-sided charts, and the positive budget for simultaneous or higher singularities.

## 17. The critical coefficient sum

At fixed `m,R,n,k`, the revision sums the regular critical half-path coefficients.

The individual estimate is

\[
 \mathfrak J(x)
 \le
 \frac{47}{12c_*\lambda_\circ}
 \varrho^{m-1}.
\]

The complete positive sum uses the retained selected-word pressure theorem and gives

\[
 \sum_x\mathfrak J(x)
 \le
 \frac{C_0Q_*}{2c_*\lambda_\circ}.
\]

The use of pressure occurs only after the global equal-gradient uniqueness theorem has supplied at most one critical point per physical word.

The argument therefore does not multiply a per-orbit estimate by an uncontrolled raw word count.

The estimate is, however, unscaled.

It contains no `m^{-2}` gain.

It does not control the local coarea error constants or their fixed-window neighborhoods.

It cannot be multiplied by `m^2` at a fixed outer stage and declared negligible.

The manuscript states this explicitly.

## 18. The decisive missing global theorem

The central gap is not another local formula.

The central gap is the passage from the local clearance and critical charts to the complete original positive source in the exact target topology.

A successful theorem must control, simultaneously:

1. all unvisited-clearance marks on all physical flights;
2. exact displacement and occupation labels;
3. the original initial and terminal section tests;
4. arbitrary physical word length;
5. all regular folds and finite-type pieces;
6. charts with vanishing clearance derivative;
7. higher or simultaneous degeneracies;
8. critical roofs and one-sided boundary sectors;
9. the weighted number and overlap of charts;
10. the local remainder constants;
11. the full physical one-copy summation;
12. the radius and exact-label suprema;
13. the roof essential supremum;
14. the collision limsup;
15. and the outer limit.

The current determinant growth estimate does not supply this theorem.

A lower bound on a determinant is not a lower bound on every relevant derivative.

It does not control condition numbers.

It does not control chart cardinality.

It does not establish finite type with a uniform order.

The stable-test estimate does not supply this theorem either.

A weak or stable-test norm is not the required roofwise `L^infty` norm.

Absence of growth in the absolute twist estimate is not high-frequency decay.

The exact clearance disintegration does not supply the theorem without a pointwise or suitably integrated roof-kernel estimate.

The critical coefficient sum does not supply it because the sum is unscaled and the chart errors are uncontrolled.

This is the decisive reason for rejection.

## 19. The remaining low-incidence and capacity source

Even a complete payment of the clearance-only source would not, by itself, close the manuscript.

The retained source still permits:

- a bounded number of shallow incidence witnesses;
- total incidence load below the paid logarithmic threshold;
- incidence-only configurations with no clearance witness;
- capacity-deficient fibers of the nongrazing pool;
- positive critical entrances and section cuts outside the controlled local families;
- and singular pairing configurations outside the regular hypotheses.

No uniform abundance theorem for

\[
 P_{r_B}^{\rm ng}
\]

is proved.

No direct original-source `m^{-2}` estimate for the remaining low-incidence class is proved.

The new critical stability coefficient identifies a physical quantity which a future comparison theorem might use.

It does not itself provide the comparison capacity.

## 20. Inherited global interfaces

Several load-bearing inputs remain inherited rather than independently verified in the present packet.

They include:

- the complete physical pairing-sheet construction;
- one-copy multiplicity across seams;
- common roofwise versions;
- the family-uniform geometric pressure theorem;
- the stable optical comparison;
- the homogeneous stable-curve growth theorem in the exact varying-radius coordinates;
- the original spectral and arithmetic local-limit chain;
- and the equivalence between the positive shortage and the final raw theorem.

The new local calculations do not circularly assume the final shortage estimate.

That is a strength.

But at the requested journal standard, the inherited chain still needs an independent specialist reconstruction before the complete article can be trusted as a top-level theorem.

## 21. Significance at the requested benchmark

The exact flux identity, integrated fold estimate, and critical return-stability coefficient are valuable.

The relation

\[
 \mathfrak J(x)
 =
 \frac{1}{
   Rc_*\sqrt{|\det(I-DT_R^{2m}(x))|}
 }
\]

provides a concrete dynamical interpretation of the critical density coefficient.

The fold argument also removes an unnecessarily strong fixed-clearance density premise on the charts to which it applies.

These results could form useful components of a strong specialist paper after independent verification and appropriate reorganization.

The present article, however, is organized around the full exact-label raw pointwise LLT and four-coordinate inversion.

Those theorems remain unproved.

The new results are highly tailored to the circular triangular Lorentz family and to the accumulated proof architecture of this manuscript.

No general theorem for singular hyperbolic systems is extracted.

No second independent application is supplied.

No complete standalone theorem of evident top-four breadth replaces the unfinished organizing result.

For these reasons, the new local progress does not change the top-four recommendation.

## 22. Required work for a further revision

A further revision should not merely add another local chart class.

It should prove a theorem which closes a complete positive source in the required topology.

At minimum, the following obligations remain.

### 22.1. Full clearance chart theorem

Construct a measurable, one-copy physical decomposition of the entire clearance-selected source into chart classes.

For every class, prove bounds whose complete weighted sum is compatible with

\[
 m^{-2}
\]

after the physical and exact-label sums.

The theorem must cover:

- simple folds;
- verified finite type;
- zero clearance derivatives;
- higher degeneracy;
- critical roofs;
- one-sided tangencies;
- section cuts;
- and simultaneous singular mechanisms.

### 22.2. Uniform chart constants

Prove quantitative collision-uniform control of the quantities which enter the local estimates, including:

- finite-type order;
- derivative lower bounds;
- fold curvature;
- clearance transversality;
- local chart radii;
- third-derivative constants;
- weight moduli;
- physical overlap;
- and total weighted chart multiplicity.

A determinant lower bound alone is not enough.

### 22.3. A valid pointwise bridge

Either prove the kernel domination

\[
 \mathcal K_{m,R,n,k,j,u}
 \,\le\,
 C_Mm^{-2}\,dt
\]

with the stated uniformity, or replace it by a rigorously summed-in-clearance theorem which directly yields the same final roofwise bound.

A stable-test estimate without a justified inversion step is insufficient.

### 22.4. Critical and boundary budget

Sum the critical coefficients and the explicit `O(sqrt(s))` remainders on fixed outer neighborhoods.

Do not choose a separate shrinking chart after the collision count is known.

Prove compatibility with the original pairing sheets and positive one-sided traces.

### 22.5. Low-incidence and capacity closure

After the clearance source is controlled, prove either:

- direct collision-uniform scarcity of the low-incidence source;
- sufficient abundance of the full nongrazing comparison pool;
- or a positive hybrid decomposition which pays every remaining class.

The final theorem must establish the unchanged shortage limit, not replace it by another equivalent residual.

### 22.6. Independent expert verification

The pressure, optical, pairing, singularity, and anisotropic-transfer interfaces should receive independent specialist review.

Finite diagnostics and exact algebra tests are useful but cannot replace this reconstruction.

## 23. Source and presentation requests

The mathematical source is substantially clearer than many earlier packets.

A future submission should nevertheless improve the active provenance presentation.

1. The active paper-directory status files still say `remote_push_completed=false` and `remote_commit=null` because they are frozen pre-push records.
2. The root publication receipt correctly supersedes those observations.
3. The next theorem-bearing packet should incorporate a versioned metadata supersession inside the active manuscript directory, rather than requiring a reader to reconcile a root-level receipt with stale internal status files.
4. The two reviewed author refs should be identified explicitly as aliases of the same current head.
5. The theorem-bearing parent and the documentation-only current head should remain separately recorded.
6. The final exact-SHA workflow status should be added only after the corresponding run actually completes.
7. The manuscript should continue to distinguish the one-flight geometric constant `delta_*` from the outer microscopic width `delta(B)`.
8. The local fold and critical constants should be collected in one table with their exact quantifiers and dependencies.
9. Any later use of the stable-test seminorm should state the precise bridge to the historical anisotropic norm or to roofwise inversion.
10. The term “critical coefficient” should continue to be qualified as a local component coefficient, not a jump of the whole roof density.

These presentation issues are secondary to the missing global theorem, but resolving them will make the next mathematical audit more reliable.

## 24. Final assessment

The clearance-to-roof revision is a meaningful response to the preceding referee report.

It addresses the correct geometry rather than renaming the residual.

It supplies exact normalizations and preserves the original event.

It handles integrated folds without assuming a bounded fixed-clearance density.

It identifies regular critical roofs with actual reversing periodic orbits and derives an exact return-stability coefficient.

It preserves one-sided boundary contributions rather than deleting them by area-nullness.

It avoids an uncontrolled raw word-count factor in the finite critical sum.

Within the written local hypotheses, I found no decisive new mathematical error.

The revision nevertheless leaves the main theorem open.

The complete clearance chart sum is not proved in the required normalized topology.

The critical remainders are not collision-uniformly summed.

The pointwise clearance bridge is not proved.

The low-incidence and capacity-deficient source remains.

The inherited global chain lacks independent specialist verification.

Accordingly, my formal recommendation at the requested benchmark is:

**reject in the present form.**

The next revision capable of changing this recommendation must establish the complete positive shortage decay, or extract and prove a standalone theorem of genuinely broader significance which does not depend on that unfinished endpoint.
