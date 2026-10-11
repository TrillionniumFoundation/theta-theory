# Independent external top-four referee rereview on A2-DYN revision 78

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v78-referee-response-2026-10-11`, `revision/a2-dyn-v78-referee-copy-2026-10-11`  
**Reviewed commit:** `5af5cbc845bfe1f73d835fee2f65fffddc7c0e55`  
**Reviewed repository tree:** `e7c7d9757a3ef3e3ebd7b7c2bcdf477c9d23d1c4`  
**Active manuscript directory:** `papers/A2-DYN-v78-referee-response`  
**Active mathematical source:** one hundred seventy-nine numbered core modules; revision 78 adds modules 177--179  
**Frozen revision-77 author baseline:** `2d88b8e6cc5dd1ebc72aaec5c77fffb08bf20e2f`  
**Controlling external report:** `reviews/a2-dyn-v76-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit:** `fd9875f55291c7804f8dc12f8b73b5886046b168`  
**Exact-source qualification runs:** response `38226161822`; referee-copy `38226177520`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style rereview; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, optical-geometry, geometric-measure-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 78 contains genuine new mathematics. It is not merely a change of terminology, a new averaging kernel, or a reclassification of an inherited residual. The revision combines the canonical endpoint-momentum flow developed in the preceding manuscript with a new optical inverse estimate, propagates the resulting perturbation through all collision contacts, proves a quantitative bound for the variation of the complete original smooth guard, and derives an averaged inequality for the full exact-label source. It also identifies an exact discrete-divergence structure for internal section-interface currents in the occupation coordinate.

The new argument materially sharpens the endpoint problem. Its principal estimate has the form

\[
 \mathcal E_M
 \le C_M B^{-1/192}
 +\mathcal G^{\varepsilon(B)}(r(B))
 +C\varepsilon(B)^{-1}\sqrt{r(B)},
 \qquad \varepsilon(B)=A_0B^{-1/12},
\]

where every auxiliary choice is made before the collision limit. The term \(\mathcal G^\varepsilon(r)\) is no longer an unspecified collection of all guard errors: it consists of true forward exits from the same physical word and the positive part of the optical/coarea volume loss on the surviving subcoupling.

I audited the new modules

- `core/177_all_contact_motion_and_guard.tex`;
- `core/178_averaged_guard_distortion.tex`;
- `core/179_exact_occupation_boundary_current.tex`;

and their immediate dependence on the inherited canonical endpoint flow and angular-recoupling modules 174--176. I also checked the revised opening, response to the referee, proof ledger, source manifest, specialist-audit document, publication status, validation protocol, and the exact-SHA workflow records.

Within that scope, I found no decisive counterexample, sign error in the endpoint flow, incorrect ordering of source- and image-side observables, illicit pooling of exact labels, missing positive-part operation in the Jacobian defect, misuse of a collision-dependent Fourier band, or false claim that the final all-source error has already vanished.

In particular, the following structural points are internally coherent.

1. The inverse optical Hessian is estimated through a diagonally normalized nonnegative contraction, giving exponential decay away from the perturbed endpoint.
2. The endpoint displacement propagates to every contact, flight, incidence cosine, reflection coordinate, clearance, and section-boundary distance with the stated depth decay.
3. The product guard is compared along the same physical word before any exit, and its total variation is bounded by \(C\varepsilon^{-1}\sqrt h\), rather than by a collision-length factor times that quantity.
4. The stopped coupling separates a true exit from an interior density distortion and retains both as positive defects.
5. The full source is bounded by its shifted copy, the true-exit source, the positive Jacobian loss, and the guard distortion on the unchanged exact-label probability space.
6. Averaging in the endpoint-flow parameter is performed at a fixed width before the collision limit.
7. Internal section-interface currents form a discrete divergence in the exact occupation index and therefore gain one scaled occupation frequency near the joint central peak.
8. The manuscript explicitly states that this lattice divergence does not control physical grazing, occlusion, true section exits, or the interior optical/coarea volume term.

These are substantive advances over the previous source state.

The negative recommendation is nevertheless forced by the central missing estimate. Revision 78 does **not** prove

\[
 \lim_{B\to\infty}
 \inf_{0<r\le r_0}
 \left\{
   \mathcal G^{\varepsilon(B)}(r)
   +\varepsilon(B)^{-1}\sqrt r
 \right\}=0.
\]

Equivalently, it does not prove a collision-uniform all-source motion budget for the two components of \(\mathcal G\):

- the roof-localized mass of true forward exits; and
- the positive optical/coarea volume loss on surviving same-label trajectories.

The new guard estimate controls only the variation of the smooth decision weight **while the physical itinerary remains valid**. The exact occupation-interface theorem controls only the internal section boundaries which admit a coefficient-wise lattice divergence. Neither theorem estimates the physical word boundaries where the same-label coupling stops, nor the positive interior Jacobian defect which remains after the stopped transport.

Consequently the manuscript still does not establish

- the unrestricted exact-label pointwise raw actual-return local limit theorem;
- the pointwise roof-density local limit theorem;
- the unconditional same-roof collision or actual-return bridge;
- forward essential arithmetic-likelihood convergence; or
- the complete pointwise endpoint consequences on every positive arithmetic class.

At the requested benchmark, isolating the final defect and proving the smooth-guard part of its control are important. They are not substitutes for proving the remaining defect small.

## 2. Frozen source and qualification

Both reviewed author branches resolve to

`5af5cbc845bfe1f73d835fee2f65fffddc7c0e55`.

The Git tree at that commit is

`e7c7d9757a3ef3e3ebd7b7c2bcdf477c9d23d1c4`.

The active article is

`papers/A2-DYN-v78-referee-response`.

The source packet identifies revision 77 at

`2d88b8e6cc5dd1ebc72aaec5c77fffb08bf20e2f`

as the immediate author baseline. The controlling external assessment is the revision-76 report at

`fd9875f55291c7804f8dc12f8b73b5886046b168`.

According to the source manifest, revision 78 retains all one hundred seventy-six inherited core modules, all inherited Python sources, appendices, bibliography, labels, and the preceding proof archive, and adds exactly modules 177--179. The active status correctly distinguishes the new scoped theorems from the missing endpoint. In particular it leaves false the flags for

- the final all-source motion budget;
- the final true-exit budget;
- the final optical/coarea volume budget;
- the full raw return LLT;
- the pointwise roof-density LLT;
- the unrestricted same-roof bridge;
- forward essential-likelihood convergence;
- independent human review; and
- formal proof certification.

The exact-source qualification workflows completed successfully on both final author refs:

- response branch run `38226161822`;
- referee-copy branch run `38226177520`.

These runs establish the checked-out SHA, source preservation, deterministic finite fixtures, native TeX compilation, recorder coverage, and rendered-page checks. They do not establish the continuum optical inverse bounds, the stopped physical coupling, the true-exit flux estimate, the coarea-volume estimate, the inherited spectral/arithmetic chain, or the final local limit theorem.

The present rereview branch starts directly from the final author SHA and adds only this report under

`reviews/a2-dyn-v78-external-top4-rereview-2026-10-11/`.

## 3. Scope of this rereview

The complete manuscript is an extensive historical proof archive. I have not attempted to re-prove all one hundred seventy-nine modules. The substantive audit concerns the new proof route and its immediate interfaces:

1. the canonical endpoint-momentum flow inherited from module 174;
2. complete angular recoupling and the ordered endpoint inherited from modules 175--176;
3. the optical Hessian normalization and inverse decay in module 177;
4. all-contact sensitivity under the endpoint flow;
5. classification of the first failure of the same physical word;
6. complete smooth-guard distortion;
7. the stopped same-label subcoupling in module 178;
8. the source-shift inequality and its averaging;
9. the definition and exact scope of \(\mathcal G^\varepsilon(r)\);
10. the exact occupation-boundary current in module 179;
11. the relationship between the new estimates and the original scalar endpoint;
12. quantifier order and exact-label uniformity;
13. source identity and workflow evidence; and
14. the requested top-four significance standard.

The inherited fixed-width local-variation estimate, complete source disintegration, coarea formulas, positive scalar remainder, arithmetic main term, collision spectral chain, path remainder, and collision-to-return transfer are treated as source-pinned inputs. This report does not independently recertify those historical arguments.

## 4. The optical inverse estimate

Module 177 studies the derivative of the collision equations along the endpoint-momentum flow. After choosing the contact variables, the relevant linearized optical matrix has the tridiagonal form dictated by neighboring free flights. The manuscript writes this matrix as

\[
 A_m=D(I-P)D,
\]

where the diagonal matrix \(D\) contains the local optical scales and \(P\) is nonnegative with row sums bounded by

\[
 q_0=47/53<1.
\]

The Neumann series gives

\[
 (I-P)^{-1}=\sum_{j\ge0}P^j,
\]

and the tridiagonal nearest-neighbor structure then yields exponential off-diagonal decay. In the manuscript's variables this becomes

\[
 0\le (A_m^{-1})_{ij}
 \le C_A q_0^{|i-j|}\min\{c_i,c_j\}.
\]

This is the correct kind of estimate for transmitting an endpoint perturbation through a long optical word without paying its full length. The proof does not replace the exact nonlinear orbit by a free random walk, nor does it infer decay from positivity of the Hessian alone. It uses the normalized M-matrix structure.

I did not find an algebraic inconsistency in the normalization, the sign pattern, or the Neumann-series argument. The load-bearing specialist checks are nevertheless substantial:

- every diagonal and off-diagonal coefficient must use the same collision-coordinate convention;
- the row-sum bound must hold uniformly on the full guarded word, not only at a reference periodic orbit;
- the optical weights \(c_i\) must remain comparable to the physical incidence and flight scales used later;
- endpoint and terminal rows must satisfy the same strict contraction after the boundary terms are included; and
- the estimate must be applied only up to the first true exit, where the same smooth branch still exists.

These are continuum geometric statements. The finite matrix fixtures in the qualification packet are useful regressions, but they are not a substitute for a specialist verification of the physical coefficients.

## 5. Propagation to all contacts

The inverse bound is used to compare two points on the same physical word whose terminal momentum differs by a small amount. The endpoint-flow parameter is denoted schematically by \(h\). The manuscript obtains depth-dependent estimates of the form

\[
 |\Delta r_j|+|\Delta p_j|+|\Delta\tau_j|
 +|\Delta c_j|+|\Delta\Delta_j|
 \le K_0 q_0^{d_j}\sqrt h,
\]

with analogous bounds for the section-boundary distances and the remaining guard coordinates.

The square-root scale is consistent with the endpoint-momentum parametrization inherited from the canonical flow. The exponentially decaying factor is what makes a collision-uniform product-guard estimate plausible.

A notable strength of the revision is that it does not audit only the selected endpoint. It explicitly follows

- contact arclength;
- reflected momentum;
- every flight length;
- every incidence cosine;
- every third-obstacle clearance;
- the section-membership margins; and
- terminal exact-label data.

This is the correct list for the literal original guard.

The proof also distinguishes continuation on one smooth physical branch from an attempted continuation through a singularity. The estimates are asserted only until the first failure of the original word. That restriction is mathematically necessary and is respected in the subsequent stopped coupling.

I did not identify a missing guard coordinate in the displayed ledger. A specialist should still verify that the finite list of candidate third obstacles used by every clearance variable remains uniform in the radius and word geometry, and that no section boundary is counted twice under overlapping chart descriptions.

## 6. Classification of true exits

The new proof identifies the first failure of the same-label continuation as one of the following physical events:

1. an incidence cosine reaches zero, producing grazing;
2. a free flight degenerates or a third obstacle occludes the intended next hit;
3. the trajectory crosses a true boundary of the inducing/observation section; or
4. a corresponding exact-event boundary is reached.

Artificial coordinate cuts are not classified as exits. They are to be glued by the inherited interface ledger before positive parts or Jordan decompositions are taken.

This classification is important because it determines the scope of the residual \(\mathcal G^\varepsilon(r)\). The manuscript does not hide a physical exit inside the smooth guard variation, and it does not infer that a vanishing guard weight makes the exit source negligible. The exit source is retained as a separate positive measure.

The classification appears complete at the level of the stated collision model, subject to the inherited first-hit geometry. What is not supplied is a collision-uniform quantitative estimate for the roof-localized mass of these exits.

## 7. Distortion of the complete original guard

The original guard is a product of smooth cutoffs applied to incidence, clearance, and section-margin variables with depth-dependent scales. A naive telescoping estimate could produce a factor proportional to the number of collisions. The revision instead combines

- exponential depth decay of the contact motion;
- the depth weights already built into the guard scales; and
- compact support of the cutoff derivative.

The resulting bound is

\[
 |H^\varepsilon(\xi_h)-H^\varepsilon(\xi)|
 \le K_H\varepsilon^{-1}\sqrt h
\]

on the surviving same physical word.

This is one of the main achievements of the revision. It controls the **complete** original smooth guard, not a selected contact, a single clearance variable, or a word-dependent replacement guard.

The proof is internally coherent in three respects.

First, the comparison is pointwise on the same exact-label source before averaging. Second, the product is telescoped without changing trajectories or conditioning events. Third, the final constant is independent of the collision length because the weighted depth series is summable.

The estimate does not control discontinuous changes at true exits. That is not a defect in its statement; it is precisely why the stopped exit term remains in module 178.

A specialist audit should verify the exact exponent in every guard scale. If a margin at depth \(d\) is divided by a scale decaying faster than the corresponding motion bound, the series could lose summability. The source currently claims compatible exponents, and I found no contrary arithmetic in the displayed chain.

## 8. The stopped same-label subcoupling

Module 178 uses the endpoint flow only while the two trajectories remain on the same physical word and in the same exact event. The coupling is stopped at the first exit. For a roof level \(t\), the comparison produces three contributions:

1. the shifted surviving source;
2. a true-exit source;
3. a positive optical/coarea Jacobian loss on the surviving source.

Together with the guard distortion, the pointwise comparison has the schematic form

\[
 b^\varepsilon(t)
 \le b^\varepsilon(t+h)
 +E_h^\varepsilon(t)
 +\int_{\mathrm{surv}}W^\varepsilon[1-J_h]_+\,d\mathsf D_t
 +K_H\varepsilon^{-1}\sqrt h\,p(t+h).
\]

The manuscript packages the middle two positive defects as

\[
 G_h^\varepsilon(t)
 =E_h^\varepsilon(t)
 +\int_{\mathrm{surv}}W^\varepsilon[1-J_h]_+\,d\mathsf D_t.
\]

This is a clean decomposition. It avoids cancellation between exits and interior volume distortion, so any subsequent upper bound remains valid. It also avoids taking an absolute Jacobian error when only the positive loss is relevant to the source-height inequality.

The elementary inequality used to separate the guard difference from the positive Jacobian loss is valid for nonnegative weights. I found no reversal of a positive part or missing factor of the surviving Jacobian in the written argument.

The principal unresolved question is quantitative, not definitional: no bound is proved for the normalized essential height of either term in \(G_h^\varepsilon\), uniformly in the collision count and exact labels.

## 9. Averaging and quantifier order

Averaging the pointwise comparison for \(0<h<r\) gives an estimate of the form

\[
 b^\varepsilon(t)
 \le 2A_r b^\varepsilon(t)
 +G^\varepsilon(r)(t)
 +C\varepsilon^{-1}\sqrt r\,A_rp(t).
\]

The inherited fixed-width local-variation theorem controls the first average, and the unweighted source average is controlled separately. The resulting ordered height estimate is

\[
 \mathcal H(b^\varepsilon)
 \le 2C\varepsilon^{1/16}
 +\mathcal G^\varepsilon(r)
 +C\varepsilon^{-1}\sqrt r.
\]

After insertion into the inherited positive-remainder inequality, this gives the displayed endpoint budget.

The order of choices is correct in the manuscript:

1. fix the outer frequency band \(B\);
2. set \(\varepsilon(B)=A_0B^{-1/12}\);
3. choose the physical flow width \(r(B)\);
4. hold these parameters fixed while taking the collision limsup;
5. only then enlarge \(B\).

No estimate is evaluated at a collision-dependent spectral band.

The identification of the unweighted roof source with the guard source at the normalization value used in the argument is explicitly justified from the initial-incidence factor of the original guard. This point should remain visible in any condensed version because otherwise the control of \(A_rp\) appears circular.

## 10. The exact occupation-boundary current

Module 179 addresses interfaces created by the exact section occupation. Across an internal section boundary, entering and leaving coefficients differ by one in the occupation index. The generating current therefore contains a factor

\[
 z-1
\]

in the occupation variable. Coefficient-wise, the boundary source is a discrete divergence:

\[
 S_n=F_{n-1}-F_n.
\]

Near the joint central peak, \(z=e^{iv/\sqrt m}\), so this factor contributes one additional \(m^{-1/2}\). Against the four-dimensional central Gaussian scale, the corresponding inverse contribution is improved from the natural \(m^{-2}\) scale to \(O(m^{-5/2})\).

The Fourier scaling and coefficient indexing are consistent. The theorem correctly retains the two sides of each internal interface before taking the difference, rather than estimating them separately by total variation.

Its scope is also stated correctly. The factor \(z-1\) does **not** imply ordinary smallness at a fixed nonzero occupation phase, and it does not apply to

- a grazing boundary;
- a third-obstacle occlusion boundary;
- a terminal physical-word boundary;
- a genuine exact-label boundary with no paired neighboring occupation cell; or
- the interior optical/coarea Jacobian loss.

Thus module 179 removes an important false positive from the remaining exit budget, but it does not close \(\mathcal G^\varepsilon(r)\).

## 11. The decisive residual

The final residual is now sharply identified:

\[
 \mathcal G^\varepsilon(r)
 =\text{true-exit height}
  +\text{positive optical/coarea volume-loss height},
\]

with internal section-interface currents treated by their exact lattice divergence.

The manuscript proves that the original scalar endpoint is equivalent, modulo the already controlled band term, to the vanishing of

\[
 \inf_{0<r\le r_0}
 \left\{
 \mathcal G^{\varepsilon(B)}(r)
 +\varepsilon(B)^{-1}\sqrt r
 \right\}
\]

in the required outer limit.

This equivalence is mathematically useful, but it is not closure. An estimate for \(\mathcal G\) must overcome two different mechanisms.

### 11.1. True exits

For true exits one needs a roof-localized flux estimate which is uniform in

- the radius;
- the return index;
- displacement labels;
- collision count;
- the original guard scale; and
- the exact central roof target.

A total exit probability is insufficient. A thin exit layer can have small mass while producing a large essential roof density after normalization by \(m^2\). Likewise, fixed-count semialgebraic complexity or finite total variation does not by itself provide the required collision-uniform local height.

The natural route is an oriented coarea/flux theorem on each genuine exit hypersurface, followed by a collision-uniform transversality and multiplicity estimate. Internal interfaces may be paired before positive parts; actual exits cannot be discarded and must be quantitatively bounded.

### 11.2. Optical/coarea volume loss

For surviving trajectories the positive term \([1-J_h]_+\) records compression of the source under the endpoint flow. Controlling the displacement of every contact does not automatically control the accumulated divergence of the full source density. One needs a collision-uniform estimate for the logarithmic Jacobian or an exact divergence identity with sufficient cancellation.

A bound of the form

\[
 [1-J_h]_+\le Ch^\alpha\mathcal W
\]

is useful only if the roof-localized weighted source \(\mathcal W\) has a uniform normalized height or an integrable coarea flux. The manuscript does not yet supply this second step.

The two defects may require different exponents and should not be hidden inside one undifferentiated constant in the next revision.

## 12. What revision 78 proves, and what it does not

Revision 78 proves, subject to the inherited inputs and specialist verification:

- exponential optical inverse decay along guarded words;
- collision-uniform all-contact sensitivity under the canonical endpoint flow;
- variation of the complete original guard by \(C\varepsilon^{-1}\sqrt h\);
- a stopped same-label source comparison;
- an averaged reduction of the original pointwise error to \(\mathcal G^\varepsilon(r)\) plus explicit controlled terms;
- an exact occupation-interface discrete divergence; and
- an equivalence between the original endpoint and decay of the final all-source motion defect.

It does not prove:

- collision-uniform decay of the true-exit source;
- collision-uniform decay of the positive optical/coarea volume loss;
- decay of their sum \(\mathcal G^\varepsilon(r)\);
- the unrestricted exact-label scalar pointwise LLT;
- the pointwise roof-density LLT;
- the unconditional same-roof path numerator and conditional bridge;
- the unrestricted actual-return bridge; or
- forward essential-likelihood convergence.

The abstract, leading theorems, response, proof ledger, and active status generally preserve this distinction. It must remain explicit in any future summary.

## 13. Relation to the inherited path conclusions

Earlier revisions established, on the inherited positive path-remainder chain, that the ordered bounded-Lipschitz path-numerator error has the same vanishing condition as the scalar pointwise error. Revision 78 does not change that logical relation.

Therefore, a proof of the final scalar endpoint would propagate to the same-roof path numerator and, on positive reference classes, to normalized collision and actual-return consequences after the inherited clock transfer. Conversely, the existing path formalism does not make the missing scalar defect disappear.

The current paper should avoid language suggesting that module 179's occupation divergence already supplies the path bridge. It supplies one interface cancellation inside the scalar source analysis; the unconditional bridge remains downstream of \(\mathcal G\)-decay.

## 14. Independent verification boundary

The new chain crosses several specialist areas:

- dispersing-billiard optical geometry;
- uniform first-hit and clearance geometry;
- M-matrix estimates for long collision words;
- endpoint-flow Jacobians;
- coarea disintegration of exact-label sources;
- lattice-valued interface currents;
- anisotropic transfer operators; and
- pointwise local inversion.

The source packet correctly records that no independent human specialist audit has occurred. Before a positive editorial assessment, at least the following should be read independently and line by line:

1. the physical coefficients and row-sum bound in the normalized optical Hessian;
2. the passage from endpoint momentum to every guard coordinate;
3. the first-exit classification and stopped coupling;
4. the full source Jacobian convention and positive volume-loss term;
5. the common roof versions used in the pointwise inequality;
6. the occupation-interface orientation and coefficient shift;
7. the inherited fixed-width local-variation theorem; and
8. the complete spectral/arithmetic/path chain used downstream.

Native compilation and finite rational fixtures are valuable engineering evidence. They do not certify these continuum statements.

## 15. Significance at the requested benchmark

The manuscript represents a large and persistent attempt to prove a very sharp local theorem for a concrete singular hyperbolic system. Revision 78 advances the program by converting a diffuse all-source obstruction into two geometrically recognizable quantities and by proving the complete smooth-guard distortion estimate.

At the level of *Annals*, *Acta*, *Inventiones*, or *JAMS*, however, the article's organizing theorem must be complete. The missing \(\mathcal G\)-estimate is not an editorial refinement or a removable technical lemma. It is the step that turns averaged source control into the literal exact-label pointwise density theorem named in the title.

There is a second editorial issue. The full source is an archival manuscript of exceptional length, with one hundred seventy-nine modules and a long sequence of retained revision layers. Even after the final endpoint is proved, a journal submission should distinguish clearly among

- the principal theorem and indispensable proof;
- a technical supplement containing long geometric and operator estimates; and
- provenance, finite diagnostics, historical reports, and prior revision material.

Preserving the research archive is valuable. Presenting the entire archive as the journal article makes independent verification harder rather than easier.

## 16. Required mathematical work before another top-four review

A genuinely new top-four submission should close the following items.

### 16.1. Prove a true-exit height bound

Establish a quantitative estimate for the exact-label roof density of first true exits under the endpoint flow. The estimate must be uniform in all original parameters and respect the order

\[
 (B,\varepsilon(B),r(B))\quad\text{fixed before}\quad m\to\infty.
\]

It must control local roof height, not merely total exit mass.

### 16.2. Prove an optical/coarea volume bound

Control the positive Jacobian loss on surviving trajectories, preferably through an explicit divergence formula or a collision-uniform logarithmic-Jacobian estimate combined with a roof-localized source bound. The dependence on \(\varepsilon\) and \(r\) must be explicit.

### 16.3. Combine the two bounds at a legal scale

Choose \(r(B)\) so that both

\[
 \mathcal G^{\varepsilon(B)}(r(B))\to0
 \quad\text{and}\quad
 \varepsilon(B)^{-1}\sqrt{r(B)}\to0.
\]

No count-dependent Fourier band or post-limsup choice is admissible.

### 16.4. Close the original scalar theorem

Insert the resulting estimate into the exact arithmetic main term and state the unconditional pointwise raw-return LLT with all zero classes and exact labels preserved.

### 16.5. Propagate the endpoint consequences

Only after scalar closure should the paper promote the same-roof path numerator, positive-class conditional bridge, collision-to-return transfer, and forward essential-likelihood statements from conditional implications to unconditional theorems.

### 16.6. Obtain independent specialist audits

The optical, coarea, transfer-operator, arithmetic, and path components should be audited by appropriate human specialists. Given the length and number of interfaces, one generalist reading is not sufficient.

## 17. Expository and technical revisions

The following changes would materially improve the next version even before the final estimate is inserted.

1. State the exact definition of \(\mathcal G_h^\varepsilon\) and \(\mathcal G^\varepsilon(r)\) in the opening, including the source measure and Jacobian convention.
2. Separate the true-exit and volume-loss contributions in every theorem statement and status flag.
3. Display the order of \(B\), \(\varepsilon\), \(r\), the collision limit, and the final band limit directly below the principal estimate.
4. Give a diagram or table matching each original guard coordinate to its all-contact sensitivity estimate.
5. State explicitly where same-word continuation stops and which boundaries are artificial interfaces rather than true exits.
6. Keep the distinction between internal occupation boundaries and physical word boundaries visible in the abstract and introduction.
7. Pin the exact inherited propositions used to control \(A_rb^\varepsilon\) and \(A_rp\), rather than referring only to the historical module number.
8. Explain in one place why the unweighted source is represented by the chosen guard normalization.
9. Isolate the optical Hessian lemma, including endpoint rows and coefficient conventions, in a self-contained proposition suitable for independent citation.
10. Move build receipts, historical responses, and provenance ledgers out of the journal narrative while preserving them in the repository.

## 18. Final assessment

Revision 78 is a substantive advance. It establishes a collision-uniform smooth-guard distortion estimate along the canonical endpoint flow, derives a full-source averaged budget with exact labels unchanged, and proves an exact lattice-divergence structure for internal occupation interfaces. I found no decisive flaw in the audited new chain.

The manuscript also accurately identifies the remaining obstruction: true physical exits and positive optical/coarea volume loss. But it does not prove a collision-uniform roof-height estimate for either component, and therefore does not prove that the final defect \(\mathcal G^\varepsilon(r)\) vanishes.

The original pointwise raw local limit theorem and its unconditional path consequences remain open within the submitted source.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
