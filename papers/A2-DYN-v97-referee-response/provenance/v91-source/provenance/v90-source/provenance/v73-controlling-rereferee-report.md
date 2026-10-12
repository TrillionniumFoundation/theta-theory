# Independent external top-four referee rereview on A2-DYN revision 73

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v73-referee-response-2026-10-11`, `revision/a2-dyn-v73-referee-copy-2026-10-11`  
**Reviewed commit:** `39575228f055862103edbebdd984bd6764fa0ad9`  
**Reviewed repository tree:** `73fba4f71220b8582b21bdabf06a80920adbadaa`  
**Active manuscript directory:** `papers/A2-DYN-v73-referee-response`  
**Active mathematical source:** one hundred sixty-three numbered core modules; revision 73 adds modules 160--163  
**Frozen revision-72 author baseline:** `295800b658aa2ff3aada1707d5785ff757d60724`  
**Frozen revision-72 paper tree:** `bd761b97e603b666ed97b27241f9ab83c7f2550b`  
**Controlling report:** `reviews/a2-dyn-v72-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `fad5823b36f2c68595c6b17bebf62c70032d30a9` / `f10920ea44a658b3b0ab75eac1f1d910a0946417`  
**Exact-source qualification runs:** response `38079689357`; referee-copy `38079695588`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style rereview; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, o-minimality, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 73 contains genuine new mathematics and responds directly to a central objection in the revision-72 report. The previous revision had constructed a canonical distributional current for the complete original positive physical source, but it had not proved that this current was a finite signed measure. Revision 73 now proves that, for every fixed physical collision count, the complete original exact-label roof density belongs to `BV(R)`. The proof is not wordwise differentiation: it represents the unchanged smooth guard as a signed threshold integral, proves finite monotonicity for each positive threshold pushforward by tame parameterized integration, and then integrates the resulting variation bounds.

This closes an important qualitative gap. The Jordan parts used by the subsequent flux argument are now genuine finite measures for the actual full source, rather than additional hypotheses or formal notation.

The revision also proves two further statements of real value:

1. a reserve-two, two-sided averaging inequality which bounds the unrecovered pointwise height by the **minimum** of incoming positive and outgoing negative current masses near the same roof; and
2. equality, under the inherited common positive path-remainder theorem, of the ordered scalar pointwise error and the bounded-Lipschitz path-numerator error.

I audited the new modules

- `core/160_common_source_versions_and_interfaces.tex`;
- `core/161_full_source_bv_by_threshold_mixtures.tex`;
- `core/162_paired_flux_capacity_bound.tex`;
- `core/163_scalar_path_error_equivalence.tex`;

and their immediate interfaces with the inherited density-height, coarea-current, positive-remainder and path-remainder results. I found no decisive counterexample, sign error, invalid use of positivity, illicit pooling of exact labels, or hidden claim that fixed-count finite variation already yields the desired local limit theorem.

The negative recommendation is forced by the same quantitative endpoint that the manuscript itself leaves open. Define

\[
 \mathcal P_\varepsilon(\delta)
 =\limsup_{m\to\infty}\sup_{R,n,k}
   \operatorname*{ess\,sup}_{t}m^2
   \min\{(Db)^+([t-\delta,t]),(Db)^-([t,t+\delta])\}.
\]

Revision 73 proves

\[
 \mathcal E_M\le C_MB^{-1/192}
       +\mathcal P_{\varepsilon(B)}(\delta(B)),
 \qquad \varepsilon(B)=A_0B^{-1/12},
\]

with all widths fixed before the collision limit. It does **not** prove that the second term tends to zero for any legal choice of `delta(B)`. The sufficient estimate

\[
 \mathcal P_\varepsilon(\delta)\le A\varepsilon^{-q}\delta^\beta
\]

is explicitly a premise, not a conclusion.

The fixed-count variation bound

\[
 \|Db\|_{TV}
 \le 4(J_m+1)(CA^m/c_*)\|d\Theta\|_{TV}^{2m+1}
\]

has uncontrolled collision-count growth. It gives neither local concentration control for the Jordan parts nor a normalized estimate after multiplication by `m^2`. A sequence of positive sources may have finite variation at every count while concentrating paired incoming/outgoing flux into narrower and higher roof intervals. Thus the new theorem makes the final obstruction mathematically legitimate and sharper; it does not prove the obstruction small.

Consequently the manuscript still does not establish its stated organizing endpoint:

- the unrestricted exact-label pointwise raw actual-return local limit theorem;
- the pointwise roof-density local limit theorem;
- unconditional same-roof point-conditioned collision or actual-return bridges;
- unconditional forward essential arithmetic likelihood convergence; or
- the full endpoint consequences on every positive arithmetic class.

At the requested benchmark, identifying the final obstruction precisely is not equivalent to resolving it.

## 2. Frozen source, chronology and preservation

Both reviewed author branches resolve to

`39575228f055862103edbebdd984bd6764fa0ad9`.

The corresponding repository tree is

`73fba4f71220b8582b21bdabf06a80920adbadaa`.

The active source directory is

`papers/A2-DYN-v73-referee-response`.

The author identifies revision 72 at

`295800b658aa2ff3aada1707d5785ff757d60724`

as the mathematical baseline and the report at

`fad5823b36f2c68595c6b17bebf62c70032d30a9`

as the controlling external assessment.

Revision 73 retains all one hundred fifty-nine inherited core modules, all inherited Python sources, all inherited appendices and the bibliography byte-for-byte, and adds exactly four new core modules. The old master source, manifest and build script are preserved in provenance. The final author commit also repairs theorem-counter exhaustion and hardens the PDF geometry checker; those are source-qualification corrections rather than additional mathematical claims.

The complete native build contains 496 pages and all 163 core modules. The present rereview branch starts directly from the final reviewed author SHA and adds only this report under

`reviews/a2-dyn-v73-external-top4-rereview-2026-10-11/`.

No author source, workflow, prior report, historical manuscript or unrelated path is intentionally modified.

## 3. Qualification evidence and its boundary

The exact-SHA qualification workflows completed successfully on both reviewed author refs:

- response branch run `38079689357`;
- referee-copy branch run `38079695588`.

Both runs use the final author SHA `39575228f055862103edbebdd984bd6764fa0ad9`. The workflow pins the revision-72 paper tree and controlling report blob, archives the exact checkout, runs the source-preservation checks and rational fixtures, compiles the complete manuscript without shell escape, stabilizes references and checks rendered-page geometry.

This is meaningful evidence for

- source identity;
- preservation of inherited inputs;
- correct inclusion of all 163 core modules;
- finite algebraic fixtures;
- native TeX compilation; and
- the exact author SHA under review.

It does not prove

- semialgebraicity of every physical graph component;
- applicability of parameterized constructible integration to the complete event formula;
- the fixed-count uniform monotonicity decomposition;
- collision-uniform control of the paired Jordan flux;
- the inherited anisotropic/spectral chain;
- the common positive path-remainder theorem; or
- any independent mathematical certification.

The local full-build record states this boundary accurately.

There is, however, a concrete source-governance defect. In the active revision-73 directory,

- `VALIDATION.md` is still headed “revision 72” and names the v72 workflow;
- `PUBLICATION_STATUS.json` still records revision 72 and modules 157--159; and
- `REFEREE_STATUS.md` still describes revision 72 and the v71 report.

The v73 `README.md`, `SOURCE_MANIFEST.json`, revision index and workflow correctly identify the reviewed object, so this does not create ambiguity about the Git SHA audited here. Nevertheless these active, unversioned status files should not remain stale in a submission packet. They should either be updated to v73 or moved under provenance with explicitly historical names.

## 4. Scope of this rereview

I did not attempt to re-prove all 163 core modules. The substantive audit concerns:

1. the common roof disintegration kernel and version discipline;
2. the complementary source allocation;
3. the oriented interface ledger;
4. the exact signed threshold representation of the original smooth guard;
5. the definability and monotonicity argument for the threshold pushforwards;
6. the fixed-count full-source `BV` theorem;
7. the two-sided paired-flux inequality;
8. the full-source raw-height budget and quantifier order;
9. the scalar/path error equality;
10. the normalization consequences and their exact scope;
11. the unresolved collision-uniform endpoint;
12. source preservation, qualification and active metadata; and
13. the requested top-four significance and presentation standard.

The inherited finite-count height bound, physical graph construction, coarea current, finite-band local-variation theorem, arithmetic main term, positive scalar remainder, path-remainder theorem, cylinder inversion and collision-to-return transfer are treated as source-pinned inputs. This report does not independently certify those historical modules.

## 5. One common roof kernel

Module 160 fixes the exact event, the physical roof and the unchanged source measure, and disintegrates the latter over the roof marginal:

\[
 \mu(A\cap L^{-1}(J))=\int_J\mathsf D_t(A)\,dt,
 \qquad \mathsf D_t(1)=p(t).
\]

For a specified Borel physical weight `W`, the roof density is then defined by `p_W(t)=D_t(W)`.

This is the correct way to compare pointwise decompositions and path-valued numerators. Without a common disintegration, separately selected Radon--Nikodym versions can satisfy source identities only on unrelated exceptional sets. The manuscript avoids this by fixing a finite or countable collection of actual Borel weights and identities before choosing the exceptional set.

The fiber concentration `Q_t(L=t)=1` is the standard property of the regular conditional probability obtained by disintegrating over `L`. Setting the finite kernel to zero on the remaining null set and where `p=0` is harmless.

For path-valued measures, the manuscript fixes a countable bounded-Lipschitz norming class. It also keeps the correct radius/roof order

```text
sup_R esssup_t
```

instead of forming an uncountable union of radius-dependent null sets.

I found this construction coherent.

## 6. Complementary source allocation

The complete positive density is written on the common kernel as

\[
 b=s+r,
 \qquad
 r=d_{71,1}+b^{\varepsilon,\mathrm{inc}}+e_{70},
\]

where `e70` is first clearance outside the selected disks and does not include first incidence.

For `q=A_delta b`, the coefficient

\[
 \alpha(t)=\min\{1,(Kq(t)-s(t))_+/r(t)\}
\]

on `{r>0}`, with `alpha=0` on `{r=0}`, is Borel. Positivity of the common kernel makes the convention on `{r=0}` irrelevant. Multiplying the original physical weights by `alpha(L)` and `1-alpha(L)` realizes the two complementary densities on the unchanged trajectory space.

This is not a transport argument and does not replace the conditioning event. The allocation preserves exact labels and the old controlled source. It makes no unwarranted regularity claim for the coefficient `alpha`.

I found no defect in this source realization.

## 7. Oriented interfaces and endpoint atoms

The interface ledger combines physical fluxes before taking Jordan parts. This order is essential: taking absolute variations patch by patch would destroy cancellation at artificial cuts.

With the interface normal directed from the minus patch to the plus patch, the two boundary terms have opposite orientations. They cancel when both patches describe the same physical roof and source. A true source jump leaves the difference of the two oriented fluxes. If the roofs differ, no cancellation is asserted.

The one-dimensional formula

\[
 D(f\mathbf1_{(a,b)})
 =(Df)|_{(a,b)}+f(a+)\delta_a-f(b-)\delta_b
\]

has the correct signs. In particular the negative exit atom is indispensable. Adjacent artificial pieces cancel; a genuine jump is counted once; a compactly supported derivative has total mass zero.

The manuscript also correctly distinguishes distributional exhaustion from total-variation convergence of patch currents. Existence of the final finite current in module 161 does not retrospectively imply that every arbitrary geometric exhaustion converges in variation.

## 8. Exact threshold representation of the smooth guard

The physical guard contains `N=2m+1` factors of a fixed smooth cutoff `Theta`. Put `sigma=dTheta`. Since `Theta` is zero to the left of the transition and one to the right, `sigma` is a finite signed measure of mass one supported in `[1,2]`. Monotonicity of `Theta` is not required; its total variation appears explicitly.

For threshold vector `y`, the manuscript defines

\[
 W_y=1-\prod_{i=1}^N\mathbf1_{\{a_i>y_i\}}.
\]

Each `W_y` is nonnegative even though the outer threshold superposition is signed. The identity

\[
 1-H^\varepsilon
 =\int W_y\,d\sigma^{\otimes N}(y)
\]

follows from the Stieltjes representation of each cutoff factor and the mass-one property of the product measure.

Finite signed Fubini is legitimate because `0<=W_y<=1` and the original source is finite. The pushforward identity therefore holds as an equality of finite measures and, on the common roof kernel, in `L1` for the densities.

The inherited complete-density theorem bounds every positive threshold restriction by

\[
 0\le b_y\le L_m=CA^m/c_*
\]

at the fixed collision count. This is the correct domination input.

I found no misuse of positivity or signed integration in this step.

## 9. Parameterized integration and definable monotonicity

This is the most delicate new part of the proof.

For fixed `m`, the manuscript uses rational collision charts and an auxiliary finite physical graph. Once the finite center itinerary and exact labels are fixed, the collision equations, first-hit inequalities, positive-flight and incidence conditions, threshold inequalities and roof sublevel condition are semialgebraic on that graph. Integration is over the two original initial coordinates, not ambient volume on the auxiliary graph.

The initial density in a rational half-angle chart is rational. Hence the parameterized sublevel mass

\[
 M(R,\varepsilon,y,t)
 =\int W_y\mathbf1_{\{L\le t\}}\,d\mu
\]

falls within the constructible integration framework. The cited Cluckers--Miller theorem has exactly the required stability-under-parameterized-integration form for constructible functions.

The complete-density bound makes every `t`-section of `M` uniformly Lipschitz at the fixed count. The derivative, where finite, is definable in the same o-minimal expansion by the first-order definition of differentiability; it need not be asserted constructible. It agrees almost everywhere with `b_y`.

Uniform cell decomposition and one-variable monotonicity for a fixed definable family then provide a finite number `J_m` of monotonicity intervals, uniform over the displayed finite-count parameters. This is a legitimate fixed-formula statement. It gives no information as `m` changes, because the defining formula itself grows with the collision length.

The written argument is plausible and internally consistent, but it is compressed relative to its importance. A journal version should isolate a theorem or lemma which explicitly records:

1. the full parameter domain;
2. the finite candidate list at fixed `m`;
3. the semialgebraic description of the moving section centers, including the half-angle representation of the analytic periodic angle used in `Y_R`;
4. the projection from the auxiliary collision graph to the two physical initial variables;
5. the exact constructible integrand supplied to the integration theorem; and
6. the uniform-family cell decomposition which defines `J_m`.

The moving section does not appear to create a counterexample: its relevant angle is determined by a unique algebraic half-angle root on a fixed interval, so a semialgebraic encoding is available. That reduction should nevertheless be written explicitly rather than left inside the phrase “same physical graph.”

I do not identify a fatal flaw here, but this proof requires an independent audit by a specialist in tame integration and semialgebraic billiard geometry.

## 10. The fixed-count `BV` theorem

A representative of each threshold density takes values in `[0,L_m]` and is monotone on at most `J_m` intervals, with at most `J_m` intervening point cells. Extension by zero outside the finite roof range adds only the two outer traces.

The estimate

\[
 \|Db_y\|_{TV}\le4(J_m+1)L_m
\]

is a safe, nonsharp bound for the interval variations and jumps.

For a compactly supported smooth test function,

\[
 \langle Db,\phi\rangle
 =\int\langle Db_y,\phi\rangle\,d\sigma^{\otimes N}(y).
\]

Taking absolute values and integrating against the total variation of the signed threshold measure yields

\[
 |\langle Db,\phi\rangle|
 \le4(J_m+1)L_m\|\sigma\|_{TV}^{N}\|\phi\|_\infty.
\]

The order-zero representation theorem therefore identifies `Db` as a finite signed measure, equivalently `b in BV(R)`. It is the same canonical distributional derivative already defined in revision 72 because both act by `-int b phi'`.

Compact support implies total current mass zero.

This proves the qualitative finite-measure statement requested in the previous report. It applies to the complete original scalar source, including incidence and original clearance outside the selected disks. It does not automatically apply to arbitrary bounded marks or to the allocated source obtained after multiplication by a merely Borel capacity weight.

The theorem's limitation is fundamental:

```text
C_m = 4(J_m+1)(CA^m/c_*) ||dTheta||^(2m+1)
```

has no controlled growth. The result is uniform in radius, guard width and attainable exact labels **only after `m` is fixed**.

## 11. The two-sided paired-flux inequality

For a nonnegative compactly supported `BV` function, define the left and right averages

\[
 L_\delta f(t)=\delta^{-1}\int_{t-\delta}^t f(u)\,du,
 \qquad
 R_\delta f(t)=\delta^{-1}\int_t^{t+\delta}f(u)\,du.
\]

At continuity points of the standard `BV` representative, the increment formula gives

\[
 f(t)-L_\delta f(t)
 =\int_{(t-\delta,t)}\frac{u-t+\delta}{\delta}\,Df(du),
\]

\[
 f(t)-R_\delta f(t)
 =-\int_{(t,t+\delta)}\frac{t+\delta-u}{\delta}\,Df(du).
\]

The triangular weights lie in `[0,1]`. Since `L_delta f` and `R_delta f` are nonnegative and

\[
 2A_\delta f=L_\delta f+R_\delta f,
\]

the positive excess above `2A_delta f` is bounded by each one-sided discrepancy. Therefore

\[
 [f(t)-2A_\delta f(t)]_+
 \le\min\{(Df)^+([t-\delta,t]),(Df)^-([t,t+\delta])\}
\]

for almost every `t`. The same bound holds for any reserve `K>=2`.

The proof is correct.

The inequality is strictly sharper than the previous directed-sum estimate. A wide rectangular pulse has separated entrance and exit atoms; no single roof sees both, so the minimum vanishes even though the directed sum is positive. A narrow pulse places the incoming and outgoing flux within the same local roof window and remains charged. Thus the estimate removes an artificial cost for isolated physical edges without deleting a genuine narrow excursion.

## 12. The full-source endpoint budget

Applying the paired inequality to the complete current gives

\[
 \mathcal U_{\varepsilon,\delta}(K)
 \le\mathcal P_\varepsilon(\delta)
 \le\tfrac12\mathcal V_\varepsilon(\delta).
\]

The second inequality is simply `min(x,y)<=(x+y)/2` and is correct.

For fixed `delta`, the inherited fixed-width theorem gives

\[
 \mathcal H(A_\delta b)\le C\varepsilon^{1/16}
\]

in the legal order: fix the auxiliary band, take the collision limit, and only then enlarge that auxiliary band. The elementary inequality

\[
 b\le2A_\delta b+[b-2A_\delta b]_+
\]

then produces

\[
 \mathcal E_M
 \le C_MB^{-1/192}
      +\mathcal P_{\varepsilon(B)}(\delta(B)).
\]

The scale substitution under the additional power premise is arithmetically correct. All choices depending on the outer band are made before `m tends to infinity`; no collision-dependent spectral band is introduced.

This is a clean reduction. It is not a closure theorem because `P_epsilon(delta)` is permitted to be infinite and no decay is proved.

## 13. Why finite variation does not close the endpoint

The new fixed-count theorem only says

\[
 (Db)^+(\mathbb R)+(Db)^-(\mathbb R)<\infty
\]

for each `m`.

The desired quantity is instead a collision-normalized local concentration:

\[
 m^2\min\{(Db)^+([t-\delta,t]),(Db)^-([t,t+\delta])\},
\]

uniformly in radius, exact labels and central roofs, followed by a collision limsup and an outer shrinking-width limit.

Neither finite total variation nor zero total mass controls this local quantity. Positive and negative variation can both concentrate in a window of width much smaller than `delta` while the density forms a narrow positive peak. The wide-pulse example shows why isolated jumps are harmless; it does not rule out narrow paired pulses.

The exponential height factor and uncontrolled monotonicity count in `C_m` are far too large to imply normalized local decay. A count of monotonicity intervals, a small source mass, or an average-height estimate is also insufficient without a quantitative anti-concentration or pairing mechanism.

The remaining task is therefore genuinely dynamical/geometric. A successful revision must prove either

\[
 \mathcal P_\varepsilon(\delta)\le A\varepsilon^{-q}\delta^\beta
\]

with constants compatible with the required limit order, or a direct estimate on the equivalent central excess. Merely improving the fixed-count total-variation constant without controlling its collision growth will not suffice.

## 14. Scalar and path-numerator errors

Let

\[
 \mathbf P=m^2p\,\mathsf Q_t,
 \qquad P=\mathbf P(1),
 \qquad G=\mathcal L_{m,R},
\]

and use the inherited decomposition

\[
 \mathbf P-G\mathsf W_R=\mathbf b_B+\mathbf E_B,
\]

where `bold b_B` is a positive kernel and the bounded-Lipschitz dual norm of `bold E_B` has collision limsup `O(B^{-1/192})`.

Positivity gives

\[
 \|\mathbf b_B\|_{BL^*}=\mathbf b_B(1).
\]

The constant test `1` and the triangle inequality imply

\[
 |P-G|
 \le\|\mathbf P-G\mathsf W_R\|_{BL^*}
 \le |P-G|+2\|\mathbf E_B\|_{BL^*}.
\]

The factor two is correct: the upper norm is at most the positive remainder mass plus the signed error, while the scalar discrepancy bounds the positive remainder mass from below up to the same signed error.

Taking the collision limsup at fixed `B` and then sending `B` to infinity proves equality of the ordered scalar and path-numerator errors. This is a useful consequence: under the inherited positive path-remainder theorem, a second independent pointwise-height estimate for every bounded-Lipschitz numerator is unnecessary.

The result is conditional on the inherited path chain. It does not independently prove cylinder inversion, path tightness, the positive remainder representation or the collision-to-return clock transfer. It is a bounded-Lipschitz dual statement, not path-space total variation.

## 15. Central excess and normalization

The central excess satisfies the two-sided comparison

\[
 U_M(B,\delta,K)
 \le E_s(M)+C_MB^{-1/192},
\]

\[
 E_s(M)
 \le U_M(B,\delta,K)+C_M(1+K)B^{-1/192}.
\]

The first inequality follows because the positive excess is bounded by `b`, and the scalar positive-remainder identity controls the central height of `b`. The second follows from

\[
 b\le KA_\delta b+[b-KA_\delta b]_+
\]

and the inherited fixed-width estimate. The quantifier order is correctly retained.

Where the arithmetic reference satisfies `G>=d>0`, vanishing of the scalar error gives a positive denominator and the displayed bounded-Lipschitz conditional comparison. The density ratios `P/G` and `G/P` are then legitimate. Zero arithmetic classes are not normalized.

The forward essential-likelihood estimate on a positive roof window follows from the elementary comparison of the two scalar densities and their normalizing integrals. Again, this is a consequence **after** the scalar endpoint is proved; revision 73 does not establish the endpoint itself.

## 16. Mathematical significance at the requested benchmark

The new fixed-count `BV` theorem is technically interesting. It combines exact guard thresholds, semialgebraic finite-word geometry, tame parameterized integration and distributional superposition to prove a property of the full physical source which was previously only formal. The paired-flux lemma also identifies the correct local obstruction more sharply than the directed-sum budget.

Nevertheless, the article's organizing theorem remains open after seventy-three revision stages and 496 compiled pages. The principal new conclusion is a qualitative fixed-count regularity theorem plus a conditional endpoint criterion. Neither alone has the breadth or finality expected for *Annals*, *Acta*, *Inventiones* or *JAMS*.

A different top-four case could in principle be made by extracting a broad theorem about tame finite-word pushforwards and collision-uniform paired flux for singular hyperbolic systems, with several genuinely different realizations. Revision 73 does not provide such a quantitative general theorem. Its decisive application still depends on an unproved Lorentz-specific anti-concentration estimate.

Subject to specialist verification, the fixed-count source theorem, the current formalism and the scalar/path comparison are meaningful contributions to the programme. They do not make the present archival article ready for the requested venues.

## 17. Architecture and presentation

The new opening is considerably clearer than the inherited cumulative front matter. It states the exact pointwise target, the finite-count `BV` theorem, the paired budget and the scalar/path equality, and it explicitly says that the target remains unproved.

The journal route is useful. However, the active manuscript is still a 496-page archive containing 163 core modules and a long sequence of historical theorem interfaces. A top-tier submission should distinguish sharply between

- the journal article containing the principal new theorem and its indispensable proof;
- a technical supplement containing inherited operator, arithmetic and geometric inputs; and
- provenance records and historical revision material.

This does not require deleting mathematics. It requires presenting one stable theorem-bearing article rather than asking a referee to treat the full revision archive as the submission itself.

The stale active status files noted above also undermine this goal. One authoritative status document should govern the packet, and all unversioned active metadata should agree with it.

## 18. Required changes before another top-four review

A further review at the requested benchmark should begin only after a genuinely new author SHA addresses the following points.

1. **Prove collision-uniform paired-flux decay.** Establish a legal estimate for `P_epsilon(delta)` or directly for the equivalent central excess. The constants must be uniform in the radius and exact labels and compatible with the prescribed order: choose widths, take the collision limit, then enlarge the outer band.

2. **Control concentration, not only total variation.** A bound on `C_m`, word counts, total source mass or fixed-width averages is not enough. The proof must exclude narrow paired positive excursions at the normalized `m^{-2}` scale.

3. **Close the original scalar endpoint.** Deduce the exact-label pointwise raw density theorem with the full arithmetic kernel and all zero classes retained. Do not substitute an interval theorem, pooled label or discarded roof set.

4. **Then state the unconditional consequences.** Use the scalar/path equality and positive reference floor to close the same-roof collision bridge, the inherited return-clock transfer and forward essential-likelihood convergence on the correct positive classes.

5. **Expand the tame-geometry proof at theorem level.** Give an explicit semialgebraic/constructible encoding of the moving section, collision graph, exact labels, threshold parameters and roof sublevels. State precisely how `J_m` is obtained as a uniform fixed-formula monotonicity number.

6. **Obtain independent specialist audits.** The fixed-count physical graph and height theorem, tame integration step, oriented coarea interfaces, inherited spectral/path chain and the new collision-uniform flux estimate should be checked by appropriate human experts.

7. **Correct active metadata.** Update or move `VALIDATION.md`, `PUBLICATION_STATUS.json` and `REFEREE_STATUS.md`, which currently identify revision 72 inside the v73 active directory.

8. **Produce a conventional submission architecture.** Keep the full archive, but separate the journal manuscript, technical supplement and provenance history.

## 19. Technical and expository comments

1. Define `A_delta` explicitly in the revised opening before the paired-flux theorem, even though it is defined in the inherited body.
2. In module 161, state the finite set of attainable `n,k` labels at fixed `m` before taking the maximum defining `J_m`.
3. Add a short lemma recording the semialgebraic half-angle representation of the moving periodic angle `theta_R` used by the section squares.
4. State whether the parameter `epsilon` is restricted to the range used by the physical guard or allowed over all positive values; the o-minimal uniformity statement works either way, but the domain should be explicit.
5. In the threshold-mixture lemma, emphasize once more that `sigma` may be signed while every individual threshold source is positive.
6. In the `BV` theorem, distinguish the compact physical roof range at fixed `m` from any bound uniform in `m`.
7. In the paired-flux example, specify endpoint conventions only up to null sets, consistently with the essential-supremum formulation.
8. Keep the distinction between `BL^*` convergence and path-space total variation in the abstract and all theorem summaries.
9. Make `SOURCE_MANIFEST.json` the sole active status file, or regenerate all status files from it during qualification.
10. Preserve the exact final author SHA and repository tree in every review copy; do not allow two nominal copies of one report to carry different source-tree fields.

## 20. Final assessment

Revision 73 is a substantive advance over revision 72.

It proves that the complete original exact-label physical source has a finite signed current at every fixed collision count. It derives that theorem from an exact signed threshold representation and tame finite-word pushforward geometry rather than from unjustified wordwise absolute variation. It proves a genuinely sharper paired incoming/outgoing flux inequality and shows, on the inherited positive path-remainder chain, that the scalar and bounded-Lipschitz path errors have exactly the same ordered vanishing condition.

I found no decisive defect in those new arguments at the level of this audit.

The revision nevertheless stops one quantitative theorem short of its organizing endpoint. It does not control the paired physical flux uniformly in collision count and exact labels, and therefore does not prove the unrestricted pointwise raw local limit theorem or its unconditional path and likelihood consequences.

The appropriate conclusion at the requested benchmark is therefore:

**Reject in the present form.**

A future revision which proves collision-uniform paired-flux decay, closes the exact pointwise endpoint, survives independent specialist audit and is reorganized into a conventional journal manuscript would merit a fundamentally different assessment.
