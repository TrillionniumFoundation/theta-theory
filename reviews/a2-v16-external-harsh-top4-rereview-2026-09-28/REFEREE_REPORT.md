# External top-four referee report on A2 v16

**Manuscript:** Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
**Latest revision:** `revision/a2-v16-intrinsic-boundary-rigidity-2026-09-28`  
**Equivalent source alias:** `revision/a2-v16-referee-copy-2026-09-28`  
**Reviewed head:** `9b0f76a32d1296b4035b52e43a38b3e3ffb50f18`  
**Reviewed repository tree:** `db18329d561f7f2011e668a7517fe53938331859`  
**Mathematical checkpoint:** `36642945db6d1c3a10a73826d658ac90e01b09bd`  
**Checkpoint paper tree:** `16622a158c054df5a98912c5adbf2b2c874b4fca`  
**Paper directory:** `papers/A2-v16-intrinsic-boundary-rigidity`  
**Date:** 28 September 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 16 is the strongest and most substantive A2 revision I have reviewed. It is not a metadata-only resubmission. It answers the principal concrete objections to v15 by replacing the supplied Cartesian frame with an intrinsic arclength observation, recovering the previously supplied gap, separate curvatures and free area, promoting the lower-jet filtration to a standalone lemma, stating a precise analytic-image identity principle, and proving a registered whole-periodic-table reconstruction theorem. The count-only question is also treated with much greater logical care: finite and formal fibers are proved, smooth physical realizations are constructed, and the exact analytic count-germ problem is explicitly left open rather than inferred from a formal recursion.

On the parts audited in detail, I found no fatal counterexample to the intrinsic calibration, the arclength transfer of the all-parity blocks, the analytic continuation argument, the physical realization, or the registered-network reconstruction. Independent exact-rational diagnostics described below support the displayed calibration and lattice algebra. I therefore do **not** base the negative recommendation on a known false theorem.

The remaining objection is the level and naturality of the result at the requested venue. The local observation is a rich endpoint-arclength subprobability law with marked contact origins and a coherent sign orbit. The global theorem additionally supplies signed registration of all contact occurrences and integer copy labels on a full-rank channel network. Once each participating analytic obstacle has been reconstructed from one such marked local germ, the global step is essentially a finite gluing argument plus rank-two lattice linear algebra. This is a valid theorem, and materially more global than v15, but the information contract has been designed closely around the desired reconstruction.

The paper still does not decide the more intrinsic exact analytic **count-only** problem modulo simultaneous reflection, does not provide stable reconstruction of analytic boundaries or the registered table from noisy finite data, and does not derive the whole-table result from a standard dynamical invariant comparable in naturality to a marked length spectrum. In my judgment, the package is technically serious and potentially suitable for a strong specialist journal after a fresh full proof review, but it does not yet reach the exceptional conceptual threshold of the four journals named above.

I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

The two v16 revision aliases listed above resolve to the same head `9b0f76a...`. The mathematical sources were introduced at checkpoint `36642945...`; the head then adds the response, publication binding, local execution evidence and read-only hosted workflow. I reviewed the mathematics at the checkpoint as contained in the latest head, and I reviewed the latest delivery metadata separately rather than treating it as new proof.

The source pins identify the frozen v15 external report at `3de6ab93a81e76f35ccf507f8815852ea4c981f6`, the qualified v15 manuscript at `00f27ebd0071d75504995b61f9a15c67f896188f`, the preserved qualified v15 paper tree `db84120af7be42acd785a9bc8d87dc6c652ee8d9`, and the preserved complete supplement tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

The principal new mathematical inputs are:

- `core/00_intrinsic_setting.tex`;
- `core/06_intrinsic_calibration.tex`;
- `core/07_filtered_arclength.tex`;
- `core/08_global_rigidity.tex`;
- `core/09_count_fibers.tex`;
- `core/10_intrinsic_experiments.tex`.

The four v15 core files containing the local flux law, Cartesian asymmetric inverse, physical realization/experiment and smooth relative-law comparison are retained by their original Git blob identities. This is a satisfactory source-preservation arrangement.

## 3. The information category is now precise

For one isolated labelled normal channel, the observed object is the family of subprobability measures

\[
\mu_{b,T}(B)=\Pr\{E_b(T),(s_-,s_+)\in B\},\qquad b=0,1,
\]

where `s_-` and `s_+` are signed intrinsic boundary arclengths from the marked contact origin. Failure remains a separate outcome. The observation is the orbit under **one simultaneous sign reversal**

\[
(s_-,s_+)\mapsto(-s_-,-s_+),
\]

not an average with the reflected law and not an independent sign choice at each time, edge or endpoint. Consequently the observation retains odd information without supplying an ambient Cartesian frame.

The proof uses the onset, the two mass germs, the two signed first-moment germs and two quadratic limits. This is a finite list of scalar-valued germs and numbers, but it is not finite-dimensional data: the exact mass and first-moment germs carry infinitely many coefficients. The manuscript mostly respects this distinction. Any future version should avoid using “finite compression” in a way that could be read as “finitely many real observations.”

The contact origins, channel labels and selected patches remain part of the channel marking. The arclength sensor is strictly richer than a collision-count sensor. Version 16 states both facts openly, which resolves the principal category objection to the v15 title and abstract.

## 4. Correctness audit of the new core

### 4.1 Intrinsic leading-geometry calibration

The local reduced action has quadratic Hessian

\[
H_b=\frac1g
\begin{pmatrix}
 c_b-(2c_o)^{-1}&-(2c_o)^{-1}\\
 -(2c_o)^{-1}&c_b-(2c_o)^{-1}
\end{pmatrix},
\qquad c_b=1+g\kappa_b.
\]

After the scaling `y=sqrt(d)Y`, the conditional endpoint law converges to the compactly supported density proportional to

\[
(1-\tfrac12Y^tH_bY)_+.
\]

Its covariance is `H_b^{-1}/3`. Since `(1,-1)` is an eigenvector of `H_b` with eigenvalue `c_b/g`, the intrinsic difference moment gives

\[
\beta_b=\lim_{d\downarrow0}
\frac{\int(s_--s_+)^2\,d\mu_{b,2g+d}}{dP_b(d)}
=rac{2g}{3c_b}.
\]

Together with the onset and leading mass coefficient, this yields

\[
g=T_0/2,\qquad
\kappa_b=\frac{2}{3\beta_b}-\frac1g,\qquad
A=\frac1{4\alpha\sqrt{c_0c_1(c_0c_1-1)}}.
\]

I independently inverted the Hessian and checked these formulas over exact rational grids. The optional sum-moment formula and the displayed leading-coordinate Jacobian are also consistent. Equal curvatures create no ambiguity because the two oriented itineraries calibrate their corresponding endpoint curvatures separately.

This is a genuine improvement over v15: leading geometry is recovered from the same intrinsic observation rather than supplied as an external numerical chart.

### 4.2 Residual-flux filtration and arclength transfer

The new filtration lemma states the exact first variation before scaling:

\[
\partial_\theta\int f(d-E)_+b
=-\int_{E<d}fb\,\partial_\theta E
 +\int(d-E)_+\{f\partial_\theta b+b\partial_\theta f\}.
\]

There is no moving-boundary term because the residual factor vanishes on `E=d`. At `d=h^2`, `y=hY`, a degree-`r` action/twist variation first occurs at weight `h^(r-2)`; a linear mark adds one power. The regular quadratic level set controls the difference between the nonlinear and quadratic domains, and all unvaried nonlinear corrections add at least one further power. This makes the highest count and marked coefficients depend only on the homogeneous action/twist variations and the linear mark, even in the presence of arbitrary lower asymmetric jets.

For intrinsic arclength,

\[
\partial_{q_{b,r}}\mathfrak a_b(y)
=\frac{\kappa_b y^{r+1}}{(r+1)(r-1)!}+O(y^{r+2}).
\]

Thus the dependence of the mark itself enters two weights after the odd highest-jet contribution. The odd and even diagonal blocks are therefore exactly the previously derived Cartesian blocks, with only lower-order remainders changed. This removes the circularity that would arise from silently replacing an unknown intrinsic metric mark by a supplied Cartesian coordinate.

The argument is persuasive and much better organized than in v15. A minor exposition improvement would be to spell out the parity statement after the Morse change in parameter-differentiated form, rather than saying only that the fixed-domain expression is even in `h`. I found no low-order term contradicting the claimed filtration.

### 4.3 All-parity recursion and analytic images

Once the calibrated leading geometry is inserted, the nonsingular even and odd two-by-two blocks give the recursive inverse

\[
Q_r=B_r^{-1}\{Y_r-F_r(Q_3,\ldots,Q_{r-1})\}.
\]

At each fixed order, the finite collection of denominators is bounded away from zero on compact positive leading-geometry sets. The local analytic and bi-Lipschitz conclusions on a coherent orientation cover follow. No uniform-in-order stability is asserted.

The separate analytic identity lemma is correctly formulated for compact connected embedded real-analytic one-dimensional submanifolds without boundary. The set of points where the two germs coincide is open and closed; accumulation of coincident arcs gives local graph equality by the one-variable analytic identity theorem. This avoids the parametrization and monodromy ambiguity present in the earlier compressed continuation paragraph.

The conclusion remains analytic rather than smooth: equality of all smooth jets is not used to infer equality of smooth boundary germs.

### 4.4 Count-only finite and formal fibers

At fixed leading geometry, the truncated count map has equations

\[
\xi_{m-1}=B_{2m}Q_{2m}+F_{2m}(Q_3,\ldots,Q_{2m-1}).
\]

Because every even block is invertible, the odd jets are free coordinates on local analytic fibers, and the even jets are solved successively. The dimension `2M-2` is correct. The support-function family realizes these finite fibers in actual analytic periodic billiards at fixed gap, curvatures and area.

The formal infinite recursion is also legitimate degree by degree. The smooth realization uses localized support-function jets with rapidly shrinking supports and a remote area compensator. This is a Borel-type construction that can keep the total perturbation small in `C^2` while prescribing arbitrary higher jets. It therefore gives smooth physical tables, not merely formal curves, whose count laws have the same Taylor series but whose boundary germs are not related by common reflection.

Crucially, the manuscript does **not** infer equality of exact smooth or analytic germs from equality of Taylor series. It states that flat differences may remain and that convergence of an analytic formal fiber is unresolved. This is the correct logical boundary.

The exact analytic count-only inverse modulo simultaneous reflection therefore remains open. Version 16 now explains the obstruction substantially better, but it does not solve that natural problem.

### 4.5 Registered whole-table reconstruction

The registered network supplies:

- a connected graph visiting every labelled obstacle;
- isolated normal channels with integer copy labels `k_e`;
- one coherently oriented arclength registration of every contact occurrence on each obstacle;
- a single global reversal ambiguity;
- cycle labels spanning `R^2`.

After one root obstacle is reconstructed and placed, the signed registration locates every incident contact on its analytic image. Along a spanning tree, representative obstacle copies can be chosen so that tree labels vanish. A tree edge then places its partner contact at

\[
p_{v,e}+g_en_{v,e},
\]

and analytic continuation places the partner obstacle. For a non-tree edge,

\[
d_e=p_{v,e}+g_en_{v,e}-p_{w,e}=Lk'_e.
\]

Two independent transformed cycle labels recover the unknown period matrix by

\[
L=[d_{e_1}\ d_{e_2}]
  [k'_{e_1}\ k'_{e_2}]^{-1}.
\]

No unimodularity assumption is needed because the marked integer matrix need only be invertible over `R`. The shear example correctly demonstrates that one observed lattice direction does not determine an unseen second period.

I found this gluing proof coherent, including loops, backwards tree traversal and representative-copy gauge changes. It gives an authentic whole-periodic-table conclusion, not merely another two-contact theorem.

Its strength must nevertheless be stated in proportion to its information contract. Coherent cross-channel registration and integer copy labels are additional supplied data. They are not recovered from the independent local law orbits. Once complete analytic obstacle images and registered contact points are known, the remaining global proof is finite geometric assembly and rank-two linear algebra. This is important for the editorial assessment below.

### 4.6 Physical families and finite-window experiments

The support-function construction gives actual analytic physical families in which gap, two radii, area and all displayed higher jets are local coordinates. The support-to-graph diagonal remains nonzero at both parities, and the area compensator is independent of the displayed jets. The selected first-hit channel and clearance persist in a small neighborhood.

The positive-window designs are dimension-sharp for differentiable locally bi-Lipschitz maps into the specified scalar means. With area free, the two probability orientations share one intercept, and the first-moment blocks have no intercept. The Vandermonde/shared-intercept argument is sound for every fixed order. The manuscript correctly disclaims uniform conditioning as the order grows and does not call the endpoint-mark compression count-only.

The `N^{-1}` fixed-dimensional risk bounds are standard once the finite Bernoulli mean map is bi-Lipschitz with fixed margins. They concern the specified compressed experiment only. The onset, quadratic calibration limits, analytic continuation and network gluing are not given finite-sample stability theorems.

## 5. Remaining information-contract issues

### 5.1 The local datum is natural but very rich

Intrinsic arclength is substantially more natural than a supplied Cartesian transverse coordinate, and the common reversal quotient is geometrically appropriate. Nonetheless, the datum records a two-dimensional endpoint subprobability law for every sufficiently small time. Odd jets are visible because the law retains oriented endpoint information. This is far stronger than counts or periodic lengths.

The theorem is therefore best read as rigidity from an intrinsic **marked local scattering law**, not as rigidity from an ordinary collision-count invariant.

### 5.2 “Finite compression” still consists of exact germs

The theorem uses finitely many types of moments, but two of them are full exact germs. Their infinitely many Taylor coefficients drive the all-order analytic reconstruction. The wording should make this explicit wherever the result is compared with finite marked data or finite-window experiments.

### 5.3 Global coherence is supplied, not inferred

Each local channel law is observed only modulo reversal, while the network theorem assumes one coherent orientation and signed contact registration across all obstacles. This coherence amounts to genuine finite inter-experiment data. The paper says so, but a formal definition of equality of registered data would help: the clean object is an oriented metric circle for each recovered boundary, with marked occurrences and integer edge labels, modulo one global orientation reversal.

In particular, distances “modulo the perimeter” should be stated as marked points on that abstract metric circle rather than as numerical residues before the perimeter has been recovered. This is a definitional clarification, not a counterexample.

## 6. Top-four significance assessment

The positive case is substantial:

- the leading geometry is recovered intrinsically;
- the odd/even all-order inverse is transferred from Cartesian marks to boundary arclength;
- arbitrary lower asymmetry and equal curvatures are allowed;
- a precise analytic image theorem replaces an informal continuation step;
- actual analytic billiard families realize all finite directions;
- a connected registered network yields a whole-table and marked-lattice theorem;
- count-only finite/formal nonidentifiability is separated rigorously from the unresolved exact analytic question;
- the primary article is theorem-led and far clearer than the earlier A2 manuscripts.

The negative case remains decisive at the requested benchmark:

1. **The observation is tailored and information-rich.** It includes endpoint arclength laws, marked contact origins and a coherent orientation orbit, rather than a conventional global dynamical spectrum.
2. **The global theorem assumes the missing gluing data.** Signed contact registration and integer copy labels are supplied. The proof after local recovery is consequently finite assembly rather than a new dynamical rigidity mechanism.
3. **The natural count-only analytic problem remains open.** The paper proves strong finite/formal and smooth-Taylor fiber statements but not exact analytic nonrigidity or rigidity modulo reflection.
4. **No stable global inverse is given.** Exact onset limits, infinitely many germ coefficients, analytic continuation and network registration are not converted into a robust finite experiment.
5. **The statistical component is regular after local invertibility.** It does not supply a new asymptotic phenomenon.
6. **The submission package remains very large.** The 21-page primary is accompanied by the complete preserved smooth-theory supplement and auxiliary document. Their formal status is now clear, but the editor is still being asked to assess a broad multi-volume program.

Relative to the marked-length and dynamical-rigidity literature, v16 presents a different and plausibly new local observation and inversion mechanism. What is still missing for the four named journals is a principle whose naturality or consequences outweigh the customized information contract—for example, a resolution of the exact analytic count-only quotient problem, a global theorem from a standard invariant without supplied registration, or a sharp stability theorem that makes the exact-germ rigidity operational. I do not require all of these; the point is that the present registered theorem does not by itself bridge the conceptual gap.

## 7. Corrections required for any resubmission

1. **Formalize registered-data equality.** Define the abstract oriented metric circles, marked contact occurrences, edge labels and the single global reversal action before stating the global theorem.
2. **Replace “finite compression” by “finite collection of exact germs and limits” where appropriate.** Keep it distinct from finite-dimensional or finite-sample information.
3. **Make the supplied coherence count explicit.** State what sign/registration data are needed beyond the independent local law orbits.
4. **Sharpen the filtration presentation.** Record the parameter-differentiated parity argument after the Morse change and the precise uniformity needed on compact finite-jet sets.
5. **Preserve the analytic count-only disclaimer.** Do not summarize the formal/smooth fiber theorem as exact analytic nonrigidity.
6. **Separate exact rigidity from statistical observation.** The finite-window theorem does not estimate onset, curvature limits, analytic continuation or the network from noisy data.
7. **Complete a commit-bound hosted build.** The local source-content receipt is useful but is not an authenticated checkout, and Supplement S was not rebuilt in that local execution.
8. **Keep the literature comparison theorem-specific.** The current six primary lines are a material improvement over v15; a submitted version should explain more sharply why the registered arclength law is a natural invariant rather than only a purpose-built sensor.

These corrections would improve a specialist-journal submission. They would not, without a broader mathematical advance, change my top-four recommendation.

## 8. Reproducibility and independent diagnostics

The author records 5,844 exact finite diagnostics, identical normal and optimized Python output, and a warning-free 21-page local primary build. The receipt correctly states that this was source-content execution in a container directory, not an authenticated Git checkout, and that Supplement S was preserved rather than rebuilt during that run.

At the final review check, GitHub Actions run `36395491597` for head `9b0f76a...` was still `queued`, with no conclusion. I therefore do not report a successful hosted full-package build.

The accompanying `verify_review.py` imports no author code. In exact rational arithmetic it performs 3,115 independent checks:

- 1,000 Hessian, difference/sum moment and curvature-calibration identities;
- 1,000 area-recovery and leading-Jacobian identities;
- 378 nonlinear arclength-series checks with arbitrary lower coefficients;
- 480 rank-two lattice recovery and determinant checks;
- 96 covolume and observed-period controls;
- 192 finite-jet/window dimension identities;
- 29 count-fiber dimension identities;
- 28 reflection-parity controls;
- 10 spanning-tree, cycle-label and shear controls.

All passed. These diagnostics verify only finite displayed algebra, formal arclength coefficients, dimensions and lattice linear algebra. They do not certify the nonlinear billiard geometry, the all-order analytic proof, the smooth extension construction, the registered physical data, or the complete submission build.

I did not perform an exhaustive priority search or re-prove every theorem in Supplement S.

## 9. Final verdict

**Response to the v15 report:** substantively successful. All eight requested corrections are addressed at theorem or source level, and the paper now has a genuine intrinsic local inverse and a registered whole-table theorem.

**Correctness:** no fatal counterexample found in the new v16 core. The calibration and network algebra survived independent exact checks. The remaining issues are mainly information-contract formalization, proof exposition and unclosed hosted reproducibility, not an identified false central formula.

**Significance:** the result reconstructs analytic obstacles and a periodic table from a rich intrinsic marked law plus supplied cross-channel registration and lattice copy labels. It does not settle exact analytic count-only rigidity modulo reflection or derive whole-table rigidity from a standard unregistered dynamical invariant. The global step is powerful but largely a gluing theorem after local analytic recovery.

**Recommendation: reject at the requested Annals/Acta/Inventiones/JAMS benchmark.** The focused intrinsic theorem could be a serious candidate for a strong specialist journal after independent full proof review and a completed source-bound build.