# External top-four referee report on A2-DYN revision 76

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*  
**Reviewed author branches:** `revision/a2-dyn-v76-referee-response-2026-10-11`, `revision/a2-dyn-v76-referee-copy-2026-10-11`  
**Reviewed commit:** `766ecf40dc2662c8d922f6ced71bef17c8d87763`  
**Reviewed repository tree:** `e894ec3428d98e4db3bdfac2a9204e003270d714`  
**Reviewed paper tree:** `a33c145a96aba6fe6005796b554f0bfa2fd607f5`  
**Active manuscript directory:** `papers/A2-DYN-v76-referee-response`  
**Active mathematical source:** one hundred seventy-three numbered core modules; revision 76 adds modules 171--173  
**Frozen revision-75 author baseline:** `fa296376d1b25b0d10459c00d02c58834c500b45`  
**Frozen revision-75 paper tree:** `3787ef425f38505c6d715161bc045ac2eebf0609`  
**Controlling report:** `reviews/a2-dyn-v75-external-top4-review-2026-10-11/REFEREE_REPORT.md`  
**Controlling report commit / blob:** `3a69da183d94b3bc695717d66971968e5396e624` / `01355269b3c3984bb51dca20e64dc46daa329743`  
**Exact-SHA qualification runs:** response `38108265948`; referee-copy `38108271404`; both concluded `failure`  
**Date:** 11 October 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a commissioned journal report, an editorial decision, a formal proof certificate, or an independent human billiards, geometric-measure-theory, or anisotropic-transfer-operator audit.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject in the present form.**

Revision 76 is a genuine theorem-bearing revision and a mathematically meaningful response to the revision-75 report. Revision 75 had replaced an uncontrolled level-component count by a uniform convex-support and Gauss-coarea estimate on every single physical word. Its remaining obstruction was that the resulting comparison depended on endpoint caps and did not control the complete weighted sum over all exact-label physical words.

Revision 76 improves that situation in three substantive ways.

First, it abandons cap-angle matching as the primary sufficient estimate and constructs a stopped transport directly on the original collision cylinder and the original exact-label roof fibers. For a specified geometric vector field satisfying `XL=1`, the transport is coordinate invariant. Its unmatched source mass is decomposed exactly into genuine exit mass and positive transported-density loss. Artificial endpoint-cap reassignment is therefore no longer charged as a dynamical defect.

Second, the revision proves a positive optical transfer recursion and an explicit hyperbolic-sine upper bound for the inverse twist of every regular physical word. The estimate retains simultaneous gains from any selected set of small internal incidences. It is a genuine bound on the actual regular word, not a comparison with a modified trajectory.

Third, the revision treats regular interior critical roofs in the correct direction. The local density jump is positive, and a forward Morse-adapted radial transport has unit Euclidean Jacobian. Its constant-density part causes no unmatched mass; only the nonconstant part produces a square-root defect.

I audited the new modules

- `core/171_stopped_physical_roof_transport.tex`;
- `core/172_optical_weights_and_morse_transport.tex`;
- `core/173_complete_source_persistence.tex`;

and their use in the journal-facing `main.tex`, response, proof ledger, source manifest, status files, specialist-audit map, validation contract, workflow records, job records, and failed-build artifact.

I found no decisive counterexample, sign error in the coarea Jacobian, failure of the two marginal dominations, missing exact-label restriction, incorrect optical recurrence, erroneous determinant power, reversed critical-jump sign, or illegal use of a collision-dependent Fourier band in the new written chain.

The negative recommendation is nevertheless unavoidable. The revision does **not** prove the collision-normalized complete true-exit and distortion estimate required by its closure theorem. The principal pointwise theorem remains conditional on

\[
 \mathcal Q_{\varepsilon,M}(r)
 \le A_M\varepsilon^{-q}r^\beta,
\]

where `Q` is formed only after all physical words and all contributions to the original exact-label source have been included. The manuscript explicitly labels this estimate an additional premise.

The per-word optical factor, the local Morse square-root estimate, and fixed-count finiteness do not control the full exact-label sum. The remaining defect includes trajectories hitting true singularities, section-decision boundaries, first-hit boundaries, and critical-neighborhood boundaries, together with transported-density distortion. No collision-uniform bound is supplied for their aggregate `m^2`-normalized concentration at one roof.

Consequently revision 76 does not establish

- the unrestricted exact-label pointwise raw actual-return local limit theorem;
- the pointwise roof-density theorem;
- unconditional same-roof collision or actual-return path bridges;
- unconditional forward essential arithmetic likelihood convergence; or
- the claimed downstream endpoint consequences on all positive arithmetic classes.

The source manifest correctly leaves all of these claims false and records that the primary referee request remains open.

There is also a concrete source-qualification defect. Both exact-SHA workflows failed before a full remote journal-and-supplement build completed. The failure is reproducible and appears to be a file-name mismatch in inherited finite diagnostics rather than a mathematical contradiction: `build.sh` writes `evidence/certify_excursion.json`, while the default invocation of `tools/verify_v2.py` attempts to read `evidence/certify_excursion.py.json`. Nevertheless, the active v76 commit has no successful exact-SHA full qualification run. A local journal-only build cannot substitute for the qualification contract, which expressly requires the complete supplement and all 173 modules.

Revision 76 therefore offers a sharper and more intrinsic formulation of the final obstruction, but it still proves an implication rather than the organizing theorem. At the requested benchmark, that is not a publishable endpoint.

## 2. Frozen source, chronology, and preservation

Both reviewed author branches resolve to

`766ecf40dc2662c8d922f6ced71bef17c8d87763`.

The repository tree is

`e894ec3428d98e4db3bdfac2a9204e003270d714`.

The active paper subtree recorded by the exact-checkout evidence is

`a33c145a96aba6fe6005796b554f0bfa2fd607f5`.

The author commit descends from the revision-75 review commit

`3a69da183d94b3bc695717d66971968e5396e624`.

The active directory is

`papers/A2-DYN-v76-referee-response`.

The source manifest records 170 inherited core modules and 173 active modules. The additions are exactly modules 171--173. Every inherited core, appendix, Python source, and bibliography is declared byte-preserved. The complete revision-75 article is retained under `provenance/v75-main.tex` and assembled into the technical supplement.

The journal entry is `main.tex`. It contains the unchanged exact-label problem, the inherited analytic inputs in the form used by the new proof, the three new modules, and an explicit section stating the boundary of the present argument. The technical supplement is `supplement.tex`.

The active status files accurately distinguish the new proved statements from the open endpoint. In particular, they record as proved:

- intrinsic stopped physical coarea transport for a specified field;
- removal of cap-partition artifacts from that transport;
- the explicit hyperbolic-sine inverse-twist bound;
- simultaneous selected-incidence gains;
- a forward Morse transport which does not charge the positive jump coefficient;
- the complete-source persistence inequality; and
- the implication from a quantitative transport premise to the original pointwise theorem.

They retain as unproved:

- collision-uniform true-exit and distortion control;
- true word-transition decay;
- collision-uniform weighted-word trace decay;
- closure of the primary referee request;
- the full raw return LLT;
- the pointwise roof-density LLT;
- unrestricted same-roof path conditioning;
- forward essential-likelihood convergence;
- independent human review; and
- formal proof certification.

This bookkeeping is honest and consistent with the mathematics I reviewed.

## 3. Qualification evidence and the failed exact-SHA runs

The v76 qualification contract requires an exact checkout, preservation of the revision-75 tree and report blob, normal/optimized agreement, native compilation of the journal and complete supplement, recorder coverage of all 173 active cores, stable references, warning-free logs, and PDF geometry checks.

The two final runs on the reviewed author SHA are:

- response branch run `38108265948`;
- referee-copy branch run `38108271404`.

Both are completed failures. In both jobs, checkout, source pinning, and dependency installation succeeded. The step entitled

`Preserve sources and compile all 173 proof modules`

failed.

The response artifact shows that the new v76 finite fixtures and the inherited v74/v75 fixtures completed and agreed in ordinary and optimized Python. The artifact also contains the generated supplement sources and exact-checkout record. The next inherited check failed with

`[Errno 2] No such file or directory: .../evidence/certify_excursion.py.json`.

The build script creates the certificate as

`evidence/certify_excursion.json`,

whereas the no-argument default in `tools/verify_v2.py` searches for

`evidence/certify_excursion.py.json`.

Thus the workflow stops before producing qualified `main.pdf` and `supplement.pdf` outputs. The copy job fails at the same build step on the same source SHA.

This appears readily repairable: pass the actual certificate path to `verify_v2.py`, or make the producer and consumer use one canonical filename. The repair must be landed in a new author SHA and both author refs must receive successful exact-SHA runs. A rerun of the unchanged failing SHA would not correct the mismatch.

I do not use this scripting error as evidence against the mathematical lemmas. I do regard it as a submission defect. The manuscript's own validation contract says that the local `--journal-only` build cannot certify the full inherited supplement or a remote checkout. The current revision therefore lacks the complete remote source/build evidence it claims as its qualification route.

## 4. Scope of this mathematical audit

The full packet contains 173 modules and a long inherited proof pipeline. I have not attempted to re-prove every historical statement. My substantive audit is concentrated on:

1. the definition of the regular exact-event domain;
2. the coarea fibers and original source normalization;
3. the existence and role of a roof vector field with `XL=1`;
4. coarea covariance under the stopped flow;
5. the two marginal dominations and exact unmatched mass;
6. the distinction between cap artifacts and true physical exits;
7. the physical drift representation of distortion loss;
8. the positive optical transfer recursion;
9. the inverse-twist and selected-incidence factors;
10. the interior critical jump normalization;
11. the forward Morse transport and its square-root defect;
12. the complete-source persistence inequality;
13. the quantitative closure implication and order of limits;
14. the status of the unresolved complete transport premise;
15. the scalar-before-path logical order;
16. the journal/supplement architecture; and
17. exact-SHA qualification evidence.

The inherited fixed-count `BV` theorem, fixed-width complete-source estimate, positive scalar remainder theorem, moving spectral reference, path-remainder theorem, arithmetic transition formula, and collision-to-return clock transfer are treated as source-pinned inputs. This report does not independently certify them.

## 5. The regular exact-event domain

Module 171 fixes one collision count, radius, occupation count, displacement, and terminal test. It removes finite-time collision singularities, preimages of section boundaries, and critical points of the roof from the regular exact event, producing an open domain `Omega`.

At fixed collision count there are finitely many physical words. The manuscript relies on the inherited endpoint-cap and strict-convexity results to assert finiteness of regular interior critical points on each relevant word. The removed sets have zero two-dimensional collision-source measure and zero coarea fiber measure for almost every roof.

This is the correct measure-theoretic starting point for a stopped transport. The argument does not simply delete the resulting boundary contributions. A trajectory whose roof flow reaches one of these boundaries is killed, and its entire initial weighted mass is charged to the exit term `E`.

The distinction is essential. Removing a null boundary from the two-dimensional source does not make the flux into that boundary negligible after normalization. Revision 76 correctly retains that flux in the unresolved quantitative defect.

A specialist should still verify the inherited claim that all critical points relevant to one fixed word and exact event are isolated in the form required here. I found no contradiction in the stated use of strict convexity.

## 6. Coarea fibers and physical covariance

The source area is

\[
 d\bar\nu_R=(4\pi c_*)^{-1}d\alpha\,dp
\]

on the regular domain. The level measure is

\[
 d\mu_t=(4\pi c_*|\nabla L|)^{-1}d\mathcal H^1.
\]

This retains the original section normalization exactly once.

Let `X` be a smooth vector field on the regular domain satisfying `XL=1`. The normalized gradient is a valid local choice away from critical points. Its maximal flow is stopped at its lifetime in the regular domain.

The Jacobian

\[
 J_h^\sigma(x)=
 \exp\left(\int_0^h\sigma\,\operatorname{div}_{\bar\nu_R}X
       (\Phi_{\sigma s}x)\,ds\right)
\]

is the area Jacobian of the flow. Because `L(Phi_{sigma h}x)=L(x)+sigma h`, disintegration of the ordinary change-of-variables formula yields the stated coarea covariance.

I found the direction and normalization of this formula correct. In particular, the source-to-target pushforward of a density `m(x)dmu_t` has target density `m(x)/J_h^sigma(x)` in the corresponding transported coordinates. This is why the source density used in the graph coupling must be bounded by `W(Phi x)J_h^sigma(x)`.

The countable flow-box exhaustion and monotone-convergence passage are appropriate for the nonnegative formula. The chain-rule and drift arguments are confined to regular flow boxes; no global integrability is inferred.

## 7. The stopped subcoupling

On survivors, the coupling uses the source density

\[
 \min\{W(x),W(\Phi_{\sigma h}x)J_h^\sigma(x)\}\,d\mu_t(x).
\]

Its first marginal is dominated by the weighted source fiber. Coarea covariance gives domination of the second marginal by the weighted target fiber. The unmatched initial mass separates into

- `E`, the weighted mass of trajectories whose stopped flow dies before time `h`; and
- `D`, the positive decrease of the transported weighted density on survivors.

Subtracting the coupled mass gives exactly `R=E+D`. Target marginal domination then yields

\[
 [b_W(t)-b_W(t+\sigma h)]_+\le R_h^\sigma(t).
\]

This is a genuine complete-source statement. It does not compare one selected word with another, and it does not reassign the event label. The flow remains inside the fixed exact event until stopping.

I found no missing multiplicity factor. Distinct physical initial states are disjoint, and uniqueness of the flow prevents multiple preimages within the surviving graph.

## 8. What “intrinsic” means here

The new construction is intrinsic with respect to coordinate charts and auxiliary endpoint-cap partitions. If the same geometric vector field is written in another chart, its flow graph and the two physical marginals are unchanged. A trajectory which merely changes its cap label is assigned to its target chart rather than killed.

This is an important improvement over the representation-dependent sufficient modulus in revision 75.

The construction is not canonical in a stronger variational sense. The field `X` is specified data. Different fields satisfying `XL=1` may have different lifetimes, divergences, and defects. The manuscript acknowledges this and does not claim that `Q` is an optimal transport distance or that the field has been chosen using the unknown scalar density.

Future statements should preserve this qualification. To close the theorem, the authors must exhibit an explicit family of fields with uniform geometric estimates. Merely asserting the existence of some field for which the desired quantitative premise holds would relocate the endpoint rather than prove it.

## 9. Distortion as physical drift

For locally Lipschitz `W`, differentiation along a survivor gives

\[
 \frac d{ds}
  \bigl(W(\Phi_{\sigma s}x)J_s^\sigma(x)\bigr)
 =\sigma(XW+W\operatorname{div}X)(\Phi_{\sigma s}x)
       J_s^\sigma(x).
\]

The positive part of the net decrease is bounded by the integral of the negative derivative. Coarea covariance at intermediate times then gives

\[
 D_h^\sigma(t)\le
  \int_0^hG_\sigma(t+\sigma s)\,ds.
\]

The written proof correctly treats this as an extended nonnegative inequality. `G_sigma` may be nonintegrable on a large roof interval. No global drift finiteness or collision-uniform estimate is inferred.

This formula is useful because it identifies the precise weighted divergence source which must be estimated. It is not itself a smallness theorem.

## 10. The positive optical transfer denominator

For one regular word, module 172 writes the internal optical matrix as a positive tridiagonal matrix with diagonal

\[
 t_{i-1}+t_i+V_i,
 \qquad V_i=2/(Rc_i),
\]

and off-diagonal entries `-t_i`.

The first-order recursion

\[
 f_i=f_{i-1}+V_i y_i,
 \qquad y_{i+1}=y_i+\ell_i f_i
\]

has positive coefficients and gives

\[
 y_m=\left(\prod_{i=0}^{m-1}\ell_i\right)\det A.
\]

This is preferable to using only the subtractive second-order continuant relation, because monotonicity in each flight length and potential is immediate from the positive recursion.

The corner Schur-complement calculation gives

\[
 |F_{uv}|=c_0c_m/y_m,
 \qquad |B_m|^{-1}=R|F_{uv}|.
\]

The empty determinant convention correctly covers `m=1`.

Replacing all flights by the minimal flight and all potentials by their smallest permitted values produces the homogeneous recurrence with

\[
 \cosh\eta=53/47,
 \qquad e^{-\eta}=(53-10\sqrt6)/47.
\]

The resulting denominator is proportional to `sinh(m eta)`. I found this computation internally consistent. The manuscript also correctly distinguishes this optical decay ratio from the unchanged guard ratio `q_0=47/53`.

## 11. Simultaneous incidence gains

To recover small-incidence gains at selected internal collisions, the proof first lowers their optical potentials by replacing the corresponding incidence by one. Restoring the actual incidence increases one diagonal element at a time.

The determinant ratio at that step is controlled by the scalar Schur complement. The printed upper bound

\[
 Q(c)=\frac{53c}{6+47c}
\]

follows from the uniform upper bound on that Schur complement and the range of `R/tau_-`.

All intermediate matrices remain positive definite, so the determinant factors multiply for an arbitrary selected set. This gives

\[
 |B_m|^{-1}
 \le C\,\frac{\sinh\eta}{\sinh(m\eta)}
       c_0c_m\prod_{i\in S}Q(c_i).
\]

I found no illicit replacement of the physical word. The comparison matrices are algebraic devices only.

This is a strong per-word estimate. It does not control the number of admissible words or the distribution of small incidences among all words satisfying the exact displacement, occupation, and terminal constraints. Multiplication by an uncontrolled exponential word count would destroy the conclusion and is expressly disallowed by the manuscript.

## 12. Interior critical charge

At a regular interior critical point, the inherited supporting trajectory gives a local lower support whose endpoint Hessian is `R I`. Therefore the reduced roof Hessian satisfies

\[
 K\ge RI.
\]

Morse coordinates put the roof in the form

\[
 F=F_*+|z|^2/2.
\]

The coarea density just above the critical value is the angular integral of the transformed area density. The resulting right-minus-left jump

\[
 J_*^W=
 \frac{W(x_*)}{2c_*|B_m(x_*)|\sqrt{\det K}}
\]

has the correct positive sign and normalization. At the critical point the endpoint incidences are one, so the optical estimate gives the displayed upper bound.

The statement is properly local. Contributions from section decisions, first-hit boundaries, or other physical pieces at the same roof are not assigned this sign.

## 13. Forward Morse transport

In Morse coordinates the forward map

\[
 z\mapsto \sqrt{1+2h/|z|^2}\,z
\]

moves the roof upward by exactly `h`. Its radial derivative is `r/r_h` and its tangential factor is `r_h/r`, so its planar Jacobian is one.

For a source density `a(z)` with Lipschitz constant `L_a`, the constant part transports without loss. The unmatched level mass is bounded by

\[
 2\pi L_a(r_h-r)\le2\pi L_a\sqrt{2h}.
\]

The radius restrictions ensure that the complete starting and target circles remain inside the selected physical disk.

This calculation correctly explains why the coefficient of the positive critical jump should not itself be charged to a forward transport defect.

It remains a fixed-count local statement. Neither the admissible Morse radius nor the sum of local Lipschitz constants is controlled uniformly in the collision count. The authors correctly refrain from inserting these local radii into the global collision limit.

## 14. Complete-source persistence

For each sign, the subcoupling gives

\[
 b^\varepsilon(t)\le
 b^\varepsilon(t+\sigma h)+Q_r^\sigma(t)
\]

for almost every `h<r`. Integrating in `h`, and using nonnegativity to compare a one-sided average with twice the centered average, gives

\[
 [b^\varepsilon(t)-2A_rb^\varepsilon(t)]_+\le Q_r(t).
\]

The minimum over the two directions is taken only after both complete physical defects have been defined. Fibers at translated roofs are not artificially restricted to the central target.

I found the factor two and the order of the essential suprema correct. Joint coarea versions in `(t,h)` prevent the proof from taking a supremum over an uncontrolled exceptional set.

The physical budget

\[
 Q_r(t)\le
 \min_\sigma\left\{
  \mathcal X_r^\sigma(t)
  +\int_0^rG_\sigma(t+\sigma s)\,ds
 \right\}
\]

is also correct as an extended inequality. Its right side may be infinite. This display identifies, rather than solves, the complete exit/distortion problem.

## 15. The conditional closure theorem

The closure theorem assumes

\[
 \mathcal Q_{\varepsilon,M}(r)
 \le A_M\varepsilon^{-q}r^\beta.
\]

Combining persistence with the inherited positive remainder gives

\[
 \mathcal E_M
 \le C_MB^{-1/192}
   +\mathcal Q_{\varepsilon(B),M}(r),
 \qquad \varepsilon(B)=A_0B^{-1/12},
\]

up to the fixed-width term of the same `B^{-1/192}` order.

Choosing

\[
 r(B)=\varepsilon(B)^{(q+a)/\beta}
\]

then closes the scalar endpoint. The order of choices is legal: `B`, the guard width, `r`, and the auxiliary spectral band are fixed before the collision limsup; the auxiliary band is enlarged afterwards and `B` last.

This implication is useful and correctly stated. It is not the theorem promised by the title and organizing objective. The additional premise is the missing dynamical estimate.

## 16. Why the new per-word estimates do not prove the premise

The quantity `mathcal Q` is formed after the complete exact-label word sum and after true boundaries have been charged. A proof must control, uniformly in radius, displacement, occupation, collision count, and central roof:

- exits at collision singularities;
- changes of first-hit decisions;
- section-entry and terminal-section boundaries;
- true word transitions;
- neighborhoods of interior and boundary critical points;
- weighted divergence of the guard under one explicit roof field;
- the aggregate of all regular inverse branches; and
- concentration after multiplication by `m^2`.

The hyperbolic-sine factor is approximately exponential in `-m`, but the admissible word family may also grow exponentially. The selected-incidence factors could overcome this growth only after a genuine summability or pressure estimate using the exact event and the physical guard. No such theorem is proved.

Likewise, the local Morse estimate is `O(L_a sqrt h)`. Without collision-uniform control of the number of neighborhoods, their radii, the transformed density Lipschitz constants, and overlap with exact-label fibers, summing it does not yield the required global power law.

The new results therefore sharpen the structure of the missing estimate. They do not make it automatic.

## 17. Field choice and the next quantitative theorem

The closure premise is stated for a fixed chosen field at each exact event. To turn it into an unconditional theorem, the manuscript should construct the field explicitly and prove uniform bounds for its lifetime and weighted divergence.

A successful route would have to combine the field with the optical recursion and the physical guard so that:

1. cap changes remain invisible;
2. true singular and decision exits are assigned quantitative source weights;
3. regular survivor distortion is summable;
4. critical neighborhoods use the favorable direction without losing uniformity;
5. the exact occupation and displacement constraints are preserved; and
6. the final estimate has a positive power of `r` after the `m^2` normalization.

This is the next theorem, not a technical corollary.

## 18. Scalar theorem before path consequences

Module 173 restates the inherited positive path remainder with the same scalar mass. Since the bounded-Lipschitz class contains the constant function one, scalar closure controls the mass of the positive path remainder, and the path-numerator error then vanishes in the same ordered limits.

The manuscript correctly forms ratios only on arithmetic classes whose scalar reference has a uniform positive lower bound. Zero classes are not divided by. Collision-to-return clock transfer and forward-likelihood convergence retain their separate inherited hypotheses.

No path statement is used to prove the scalar estimate. This logical order is correct.

The current revision cannot promote these path consequences because the scalar transport premise is unproved.

## 19. Journal article and supplement

The new journal-facing article is substantially clearer than the historical proof archive. It defines the physical section, exact event, guard, arithmetic reference, central target, inherited analytic inputs, and the three new arguments without requiring the reader to resolve old equation numbers.

This is a genuine editorial improvement.

However, the journal article is a short chain of local transport and optical results culminating in a conditional implication. Its full analytic and spectral foundations remain in a very large supplement. At a top-four journal, the principal article must culminate in an unconditional theorem of commensurate significance. A self-contained implication to an unproved premise is not enough.

I do not recommend deleting the inherited mathematics. The appropriate route is to retain the supplement as a proof archive while making the eventual journal theorem unconditional and giving a concise dependency map for the necessary inherited results.

## 20. Required changes before another top-four review

A further top-four review should begin only after the following items are addressed.

### 20.1. Prove the complete transport estimate

Establish the v76 premise, or a quantitatively equivalent estimate, on the original exact-label source:

\[
 \mathcal Q_{\varepsilon,M}(r)
 \le A_M\varepsilon^{-q}r^\beta
\]

for some finite `q` and positive `beta`, with the stated order of limits.

The proof must include all true exits and survivor distortion after the full word sum. It must not replace the source by protected words, omit terminal membership, pool labels, discard arithmetic zero classes, or use a collision-dependent spectral band.

### 20.2. Make the roof field explicit

Specify the field or finite family of fields used at every exact event. Prove the required lifetime, divergence, patching, and parameter-uniform estimates. Clarify how the Morse-adapted fields are selected and glued without introducing a collision-dependent collar into the limit.

### 20.3. Sum the optical weights dynamically

Convert the per-word hyperbolic-sine and incidence factors into a complete pressure, transfer-operator, or source-summability estimate. Do not multiply by an uncontrolled word count. The exact displacement, occupation, section, and terminal restrictions must remain visible in the sum.

### 20.4. Control true boundary exits

Give quantitative estimates for source reaching finite-time singularities, first-hit switches, section boundaries, and physical word transitions under the stopped roof flow. Nullity of the boundaries in the two-dimensional source is not sufficient.

### 20.5. Globalize the critical transport

Control the aggregate Morse radii and transformed-density Lipschitz constants, or replace the local cover by a global critical-value argument. The current fixed-count local square-root bound cannot simply be summed over an uncontrolled family.

### 20.6. Repair exact-SHA qualification

Fix the `certify_excursion.json` / `certify_excursion.py.json` mismatch, land a new author commit, and obtain successful exact-SHA runs on both response and referee-copy branches. Confirm that both `main.pdf` and `supplement.pdf` compile, all 173 cores are recorded, and no warnings or source-preservation failures remain.

### 20.7. Obtain independent specialist audits

The stopped coarea disintegration, optical Schur-complement identity, critical transport, complete weighted summability, and inherited spectral/arithmetic interfaces should be checked by specialists in dispersing billiards, anisotropic transfer operators, and geometric measure theory.

### 20.8. Promote downstream statements only after scalar closure

After the scalar theorem is unconditional, verify the positive-reference lower bound, same-roof path normalization, collision-to-return clock transfer, and forward likelihood on their exact stated domains. Do not normalize arithmetic zero classes.

## 21. Significance at the requested benchmark

The stopped physical transport is a useful conceptual improvement. It replaces a chart-dependent trace comparison by an exact subcoupling on the physical source. The optical transfer denominator and the direction-sensitive treatment of a critical jump are also technically interesting.

As presently written, these results are tools toward the original theorem rather than a completed theorem of independent breadth. Their strongest global conclusion is conditional on the precise estimate which remains open. No second singular-hyperbolic realization or general theorem with verifiable hypotheses removes the paper's dependence on the unfinished Lorentz endpoint.

At a strong specialist journal, a carefully framed technical article on the stopped transport and optical estimates might eventually be viable after independent verification. At the requested four-journal benchmark, the submission must first close the original pointwise theorem or supply a genuinely broader unconditional theorem.

## 22. Final assessment

Revision 76 is a real advance over revision 75.

It successfully:

- removes artificial cap reassignment from the sufficient transport defect;
- gives an exact label-preserving stopped subcoupling;
- separates genuine exits from survivor distortion;
- identifies the physical weighted drift source;
- proves a positive optical denominator recursion;
- obtains explicit hyperbolic-sine decay and simultaneous incidence gains on every regular word;
- computes the positive interior critical charge;
- constructs a forward Morse transport which does not charge the positive jump coefficient;
- derives a complete-source persistence inequality; and
- preserves the legal order of spectral and collision limits.

I found no decisive mathematical counterexample in these new scoped results.

The revision does not prove the collision-uniform complete exit/distortion estimate. Therefore it does not prove the organizing pointwise raw local limit theorem or its downstream consequences. In addition, both final exact-SHA qualification runs fail before the complete journal-and-supplement build.

**Final recommendation: reject in the present form at the requested four-journal benchmark.**
