# External top-four referee report on A2-DYN revision 78

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v78-referee-response-2026-10-11`, `revision/a2-dyn-v78-referee-copy-2026-10-11`  
**Reviewed commit:** `5af5cbc845bfe1f73d835fee2f65fffddc7c0e55`  
**Reviewed repository tree:** `e7c7d9757a3ef3e3ebd7b7c2bcdf477c9d23d1c4`  
**Active manuscript directory:** `papers/A2-DYN-v78-referee-response`  
**Active mathematical source:** one hundred seventy-nine numbered core modules; revision 78 adds modules 177--179  
**Frozen revision-77 author baseline:** `2d88b8e6cc5dd1ebc72aaec5c77fffb08bf20e2f`  
**Frozen revision-77 paper tree:** `dcdbbd9d49cc707bdcf6a1d41066ac26cdfd39b6`  
**Controlling report:** `reviews/a2-dyn-v76-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `fd9875f55291c7804f8dc12f8b73b5886046b168` / `6857e4851ff12b7d0828f4eb661152e131fba091`  
**Exact-SHA qualification runs:** response `38115522414`; referee-copy `38115531156`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 78 is a substantive and mathematically relevant response to the principal objection in the revision-76 report. That report identified a gap between per-word optical estimates and a collision-uniform estimate for the complete, source-dependent guard mismatch on the unchanged exact-label probability space. Revision 78 now supplies an all-contact optical response estimate, a uniform modulus for the original smooth guard, and an averaging argument which converts that modulus into an ordered `m^2`-scale bound without assuming a pointwise upper bound for the unweighted roof density.

This is genuine progress. In particular, the new argument does not replace the original guard by protected words, insert a section-distance cutoff, pool occupation labels, delete arithmetic zero classes, or evaluate a fixed-band theorem at a collision-dependent frequency. The source and target remain the original exact event.

I audited the new modules

- `core/177_all_contact_motion_and_guard.tex`;
- `core/178_averaged_guard_distortion.tex`;
- `core/179_exact_occupation_boundary_current.tex`;

and their direct use in `main.tex`, together with the retained endpoint-momentum modules 174--176, the response, proof ledger, source manifest, controlling report and exact-SHA workflow records.

I found no decisive counterexample, sign error in the guard product estimate, illegal conversion of averaged control into a pointwise density bound, loss of an exact label, or suppression of a nonzero occupation-frequency phase in the new written chain.

The decisive negative point is instead explicit in the manuscript itself. Revision 78 proves the complete **guard-distortion** contribution small after averaging, but it does not prove the complete **geometric** contribution small. The remaining quantity contains

1. every true forward exit from the regular exact event;
2. the positive loss of physical coarea volume along surviving trajectories;
3. small-chart and exhaustion effects retained by the full source; and
4. surface-current insertions at section decisions, including nonzero arithmetic peaks.

The manuscript reduces the original endpoint to the condition

\[
 \lim_{B\to\infty}\inf_{0<r<r_0}
 \left\{\mathcal G_{\varepsilon(B),M}(r)
             +\varepsilon(B)^{-1}\sqrt r\right\}=0,
 \qquad \varepsilon(B)=A_0B^{-1/12},
\]

but does not prove that condition. It also states, correctly, that a bounded volume-multiplier theorem is not automatically a spectral estimate for a surface-current insertion.

Consequently the organizing exact-label pointwise local limit theorem remains unproved. At the requested benchmark, a sharp and honest reduction of the last obstruction is not a substitute for closing it.

## 2. Frozen source, chronology and qualification

Both reviewed author branches resolve to

`5af5cbc845bfe1f73d835fee2f65fffddc7c0e55`.

The repository tree is

`e7c7d9757a3ef3e3ebd7b7c2bcdf477c9d23d1c4`.

The active journal source is

`papers/A2-DYN-v78-referee-response/main.tex`.

The technical supplement is

`papers/A2-DYN-v78-referee-response/supplement.tex`.

The source manifest records 176 inherited core modules and 179 active modules. The additions are exactly modules 177--179. It also records byte preservation of the inherited cores, Python sources, appendices, bibliographies and provenance snapshots.

The final author commit is a clarification commit. It retains the exact internal-current identity and corrects the statement at nonzero occupation peaks: the ordinary occupation difference is small only after the retained leading term is separately controlled; that term need not vanish identically. This clarification is mathematically necessary and is correctly reflected in the final source.

The final exact-SHA qualification workflows completed successfully on both author branches:

- response run `38115522414`;
- referee-copy run `38115531156`.

This remedies the source-qualification defect noted in the revision-76 report. The runs establish exact source identity, preservation, native journal and supplement builds, finite-fixture consistency, recorder coverage and rendered-page checks. They do not prove the continuum optical estimates, coarea transport, surface-current spectral bounds or the final geometric smallness condition.

The source manifest is appropriately conservative. It marks the all-contact derivative decay, original-guard modulus, guard-distortion bound, exit localization, internal discrete current identity and peak-aware difference as proved, while leaving false the complete geometric exit/volume bound, uniform surface-current spectral insertion bound, full raw return LLT, pointwise roof-density LLT and unconditional path/likelihood conclusions.

## 3. Scope of this audit

The complete archive contains 179 core modules. I have not attempted to re-certify every historical theorem. The substantive review concerns:

1. the incidence-normalized inverse and all-contact motion;
2. the original guard modulus;
3. localization of true exits;
4. the averaged source/target comparison;
5. the use of the fixed-width unweighted concentration input;
6. the exact internal section-current identity;
7. the arithmetic effect of the factor `z-1` at all spectral peaks;
8. the remaining geometric quantity and its relation to the organizing theorem;
9. source identity and qualification evidence; and
10. the requested top-four standard.

The inherited spectral splitting, positive scalar remainder, fixed-width complete-source estimate, endpoint-momentum field and earlier coarea constructions are treated as source-pinned inputs. This report does not independently re-prove them.

## 4. The incidence-normalized inverse

Module 177 begins from the tridiagonal optical matrix and writes it as

\[
 A=D(I-P),
\]

where `P` has nonnegative nearest-neighbor entries and uniformly subunit row sums. The Neumann series gives

\[
 0\le (A^{-1})_{ij}
 \le C_A\min(c_i,c_j)q_0^{|i-j|},
 \qquad
 |(D_c^{-1}A^{-1})_{ij}|
 \le C_Aq_0^{|i-j|}.
\]

The important feature is the factor of the internal incidence cosine. It compensates the degeneracy which would otherwise appear when an internal collision approaches grazing. The argument therefore does not require a positive lower incidence cutoff.

Using the endpoint forcing in the differentiated stationary equations, the manuscript obtains exponential decay of each contact displacement from the nearer endpoint. At the level of the stated first-derivative calculation, this is coherent. It is also properly limited to actual regular trajectories: no common continuation neighborhood through a true singular boundary is claimed.

A specialist should still compare the exact matrix normalization and tangent-sign conventions line by line with the inherited module-140 Green-function estimate. I found no contradiction in the present derivation.

## 5. Motion of incidences and clearances

The differentiated flight direction is written as

\[
 dv_j=\ell_j^{-1}(I-v_jv_j^{\mathsf T})
                   (dQ_{j+1}-dQ_j).
\]

Because the flight lengths have a fixed positive lower bound and the two endpoint displacements have the appropriate tapered depths, this gives uniform control of the angular and tangential records.

The manuscript correctly avoids differentiating

\[
 c_j=\sqrt{1-p_j^2}
\]

by division by `c_j`. Instead it differentiates the relevant scalar products of unit velocities and normal/tangent vectors. This is essential near grazing.

For clearance, distance from a segment to a fixed third disk is one-Lipschitz in the Hausdorff displacement of the segment. Taking a finite minimum preserves this Lipschitz bound even if the minimizing disk changes. Thus differentiability of the minimum is not required.

The resulting estimates

\[
 |\Delta_j(x)-\Delta_j(y)|
 \le C_Dq_0^{d'_j}\ell_q
\]

and their incidence analogues are internally consistent.

## 6. The complete original guard

The original guard is a product over all contact-incidence and flight-clearance factors. For factors in `[0,1]`, the difference of two products is bounded by the sum of the factor differences. The contact and flight derivative estimates produce the summable weights

\[
 q_0^{3d_j/4},\qquad q_0^{3d'_j/4}.
\]

Summing over depths gives

\[
 |W^\varepsilon(\Phi_hx)-W^\varepsilon(x)|
 \le \min\{1,K_\Theta\varepsilon^{-1}\sqrt h\}.
\]

This is one of the principal achievements of the revision. It applies to the complete original product and adds no incidence cutoff, clearance cutoff, section-distance factor or monotonicity assumption on the smooth cutoff.

The statement concerns survivors in a fixed regular exact event. It does not assert survival across a word change or section-decision boundary, and the manuscript does not use it that way.

## 7. True-exit localization

If the stopped field cannot be continued for time `h`, module 177 shows that at least one tapered incidence, clearance or section-distance margin is of order at most `sqrt(h)` with the appropriate depth factor.

This is a useful geometric inclusion. It identifies where a true exit must occur. The manuscript is also correct to state that this is **not** a pointwise concentration estimate on the starting roof fiber.

The distinction is decisive. Even a very thin phase-space layer can have a large conditional density on a single roof. A mass estimate for the layer does not by itself control

\[
 m^2\operatorname*{ess\,sup}_t
 \mu_t(\mathcal B_h).
\]

Thus exit localization is a necessary geometric input, but it does not close the endpoint.

## 8. Averaged separation of guard and geometry

Module 178 defines the residual geometric defect as

\[
 G_h^\varepsilon(t)
 =E_h^\varepsilon(t)
 +\int_{S_h(t)}W^\varepsilon(x)[1-J_h(x)]_+\,d\mu_t(x).
\]

The first term contains every true exit; the second contains positive physical coarea-volume loss. The change of the guard itself is not put into this definition.

For source weight `w`, transported target weight `w'` and Jacobian `J`, the elementary inequality

\[
 [w-w'J]_+
 \le w[1-J]_+ +J|w-w'|
\]

correctly separates geometry from guard mismatch.

Coarea covariance on survivors gives

\[
 \int_{S_h(t)}J_h\,d\mu_t
 \le p(t+h),
\]

where `p` is the unweighted density of the same exact event. Averaging over `0<h<r` then yields

\[
 b^\varepsilon(t)
 \le 2A_rb^\varepsilon(t)
 +\overline G_r^\varepsilon(t)
 +2K_\Theta\varepsilon^{-1}\sqrt r\,A_rp(t).
\]

The order of operations is correct: the target is averaged before the collision limit is taken. The proof does not replace `A_rp` by an unproved pointwise bound for `p`.

## 9. The unweighted fixed-width input

The journal restates as an analytic input that, for every previously fixed width,

\[
 \limsup_m\sup_{R,n,k}m^2\|A_\delta b^\varepsilon\|_\infty
 \le C\varepsilon^{1/16},
\]

with a constant independent of that fixed width.

To apply it to the unweighted density, the manuscript sets the auxiliary guard parameter to one. Since the initial incidence factor is `Theta(c_0)` and `c_0\le1`, the complete good guard satisfies `H^1=0`; hence `W^1=1` and `b^1=p`. This use is legitimate.

It follows that for each width fixed before the collision limit,

\[
 \limsup_m\sup_{R,n,k}m^2\|A_rp\|_\infty\le C.
\]

Consequently the ordered guard contribution is bounded by

\[
 C_\Theta\varepsilon^{-1}\sqrt r.
\]

This closes the complete guard-distortion term promised by the revision. The strength of the conclusion depends on the inherited width-uniform concentration theorem. For a conventional submission, that theorem should be stated with its precise quantifiers and proof location immediately adjacent to the present application, rather than only as an inherited interface.

## 10. The residual geometric criterion

Combining the averaged persistence inequality with the positive spectral remainder gives

\[
 \mathcal E_M
 \le C_MB^{-1/192}
 +\mathcal G_{\varepsilon(B),M}(r)
 +C_\Theta\varepsilon(B)^{-1}\sqrt r.
\]

The manuscript also proves that, under the stated analytic input, the organizing pointwise theorem is equivalent to the vanishing of the corresponding optimized geometric expression.

This equivalence is useful. It shows that guard mismatch is no longer the final obstacle. It also prevents future revisions from moving the unresolved term between notations without estimating it.

However, the theorem is an endpoint **criterion**, not the endpoint itself. No bound of the form

\[
 \mathcal G_{\varepsilon,M}(r)
 \le A_M\varepsilon^{-q}r^\beta
\]

is proved for the unrestricted Lorentz source.

## 11. The exact internal section current

Module 179 treats internal section decisions on a compact regular domain by retaining a polynomial variable `z` for the occupation count. Across an oriented interface, the two cell fluxes combine as

\[
 z^{a_+}-z^{a_-}=(z-1)P_{a_-,a_+}(z).
\]

After summing interfaces, the signed current factors as

\[
 \mathscr S_D(z)=(z-1)\mathscr F_D(z),
\]

and coefficient extraction gives

\[
 \mathscr S_{D,n}
 =\mathscr F_{D,n-1}-\mathscr F_{D,n}.
\]

This is the correct way to retain exact occupation labels before taking absolute values. It also handles coincident regular interfaces through the net occupation change; lower-dimensional intersections carry no surface flux.

The theorem is appropriately restricted. Initial and terminal section boundaries, grazing boundaries, first-hit switches and true word transitions are not identified with regular internal interfaces.

## 12. Nonzero occupation peaks

A factor `e^{iv}-1` is small only near an occupation-frequency peak with `v=0` modulo `2 pi`. Near a general peak `v_j`, the manuscript proves

\[
 S_{m,j}(y)
 =(e^{iv_j}-1)F_{m,j}(y)+O(m^{-5/2}).
\]

Equivalently, the covariant difference

\[
 F_{m,j}(k,t,n-1)
 -e^{iv_j}F_{m,j}(k,t,n)
\]

is of order `m^{-5/2}` under the stated surface-amplitude Gaussian bound.

The final clarification correctly states that at a nonzero peak the ordinary difference requires a separate bound for the retained leading term; it need not vanish identically. This preserves the full finite arithmetic transition and avoids a spurious cancellation of nontrivial classes or transition-radius peaks.

The proposition is conditional on a scalar Gaussian bound for the surface-current primitive. Such a bound is not supplied by the existing volume-operator spectral theorem.

## 13. The remaining surface-current problem

The exact polynomial current identity is algebraic and local. To use it in the full pointwise theorem one still needs a collision-uniform estimate for the Fourier transform of the surface-current primitive over all regular interfaces and through the relevant exhaustions.

That estimate must address:

- the anisotropic norm or trace class in which the surface insertion lives;
- uniform control of its peak amplitudes;
- transition radii and moving peak charts;
- the retained leading term at every nonzero occupation peak;
- small-frequency cancellation where `v_j=0`;
- summation over all physical interfaces at fixed exact labels; and
- compatibility with the collision limit before any outer band is enlarged.

None of these follows automatically from bounded multiplication by the section indicator in the volume transfer operator.

## 14. The remaining true-exit and volume-loss problem

The geometric quantity also contains contributions unrelated to regular internal section currents.

First, a trajectory may hit a grazing, first-hit, clearance or word-transition boundary. Module 177 locates such events in tapered layers but supplies no roof-fiber concentration theorem for those layers.

Second, on surviving trajectories the physical coarea Jacobian can lose volume. The guard modulus does not estimate

\[
 W^\varepsilon[1-J_h]_+.
\]

A complete proof must control the averaged `m^2`-normalized essential height of both effects, after summing the unchanged exact-label source.

An integrated phase-space boundary-layer estimate is insufficient unless it is converted into the required roof-fiber estimate with the legal quantifier order.

## 15. Relation to the original pointwise theorem

The target remains

\[
 \sup_{R,n,k}\operatorname*{ess\,sup}_{|Z|\le M}
 |m^2p_{n,R}(k,m,t)-\mathcal L_{m,R}(k,t,n)|
 \longrightarrow0.
\]

Revision 78 does not replace this with a window law or an averaged-density theorem. This is a strength of the revision.

It nevertheless does not prove the target. The source manifest accordingly leaves false:

- `complete_geometric_exit_volume_bound_proved`;
- `uniform_surface_current_spectral_insertion_bound_proved`;
- `full_raw_return_LLT_proved`;
- `pointwise_roof_density_LLT_proved`;
- `unrestricted_same_roof_pair_bridge_proved`; and
- `forward_essential_likelihood_convergence_proved`.

These are not editorial details. They are the remaining mathematical endpoint.

## 16. Downstream path and likelihood conclusions

The inherited positive path-remainder framework may make the bounded-Lipschitz path numerator follow once the scalar pointwise theorem is closed. Likewise the collision-to-return clock transfer and normalized forward likelihood may then be invoked on positive reference classes.

At present those consequences remain conditional. One may not divide by a vanishing arithmetic reference, and a fixed-width average does not provide the pointwise denominator required for same-roof conditioning.

The manuscript is correct to keep scalar closure first in the logical order.

## 17. Presentation and architecture

The journal-facing file is much more focused than the historical archive. It states the unchanged problem, isolates the analytic inputs, presents the retained endpoint field and the three new modules, and then states exactly what remains.

The supplement preserves the complete 176-module inherited pipeline. This is preferable to deleting the derivation history, but a formal submission would still benefit from a sharper separation between:

1. the journal theorem and its complete proof;
2. a technical supplement containing only necessary inherited inputs; and
3. provenance and historical revision materials.

The current packet remains unusually large and difficult to audit. The journal source relies on several inherited input statements whose proof locations should be given as theorem-level cross-references in a stable supplement.

## 18. Independent verification

No independent human specialist audit is recorded. The points most in need of such review are:

- the optical matrix normalization at arbitrarily small incidences;
- the all-contact endpoint derivative calculation;
- the stopped coarea coupling and Jacobian orientation;
- the inherited fixed-width concentration theorem and its width-uniform constant;
- the exhaustion of regular domains in the internal current;
- the surface-current trace space and peak amplitudes; and
- the conversion of tapered exit layers into roof-fiber essential-height bounds.

The successful exact-SHA workflows are meaningful source and typesetting evidence. They are not substitutes for these checks.

## 19. Required work before another top-four review

A further revision seeking the same benchmark should complete the following tasks.

1. **Prove the complete geometric smallness estimate.** Establish the optimized vanishing of `G_{epsilon,M}(r)` with all true exits and coarea-volume losses included at fixed exact labels.
2. **Convert exit localization into roof-fiber control.** A phase-space layer inclusion must yield the required collision-normalized essential-height estimate in the legal order of limits.
3. **Build the surface-current spectral theory.** Specify a trace/insertion space, prove uniform peak-amplitude bounds, and control every nonzero-peak leading term rather than deleting it.
4. **Close the organizing scalar theorem.** Deduce the exact-label pointwise raw return LLT with the full finite arithmetic transition and all zero classes retained.
5. **Only then promote conditional consequences.** Establish same-roof collision and actual-return path limits and forward likelihood statements on positive reference classes.
6. **Obtain independent specialist audits.** The billiard geometry, anisotropic transfer-operator, coarea-current and arithmetic-peak parts should be checked by appropriate experts.
7. **Stabilize the submission architecture.** Provide a concise theorem-level dependency map from every journal input to a fixed supplement theorem, while leaving the historical archive in provenance.

The earlier paired-flux route remains another possible sufficient mechanism, but revision 78 no longer needs to prove paired-flux decay if it closes the equivalent geometric criterion directly. The authors should choose one route and carry it to the unconditional scalar endpoint.

## 20. Final assessment

Revision 78 makes a real advance. It closes the complete source-dependent guard-distortion term which was a principal obstruction in the revision-76 report. It does so while preserving the original exact event, original guard, all arithmetic peaks and the correct collision/band order. The exact internal occupation-current identity is also useful, and the final nonzero-peak clarification is correct.

The manuscript now isolates the unresolved mathematics more sharply than previous revisions. But the complete true-exit/coarea-volume defect and the surface-current spectral insertion are still unestimated, and the organizing pointwise theorem is explicitly not proved.

At the requested *Annals* / *Acta* / *Inventiones* / *JAMS* benchmark, this remains an incomplete endpoint rather than a publishable theorem.

**Final recommendation: reject in the present form.**
