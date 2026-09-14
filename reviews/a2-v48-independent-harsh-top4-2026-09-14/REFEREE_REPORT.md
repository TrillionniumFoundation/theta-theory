# Independent referee-style report on A2 revision 48

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Report date:** September 14, 2026  
**Requested standard:** the highest-level general mathematics journals.  
**Status:** an author-requested, AI-assisted independent assessment. This is not a commissioned journal report, a claim of journal affiliation, or an actual editorial decision.

| Reviewed object | Frozen identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Review-ready branch | `revision/a2-v48-review-ready-2026-09-14` |
| Review-ready snapshot | `5babd4cd1515b7f64488d997d89d0860a4eff96c` |
| Actual compiled mathematical source | `fe21046e47a89ec3b3df8493f4d885b087e3ad7f` |
| Native run / attempt / artifact | `34852676783` / `1` / `10351522484` |
| Complete manuscripts | Main: 255 pages; two-collision companion: 7 pages |
| Preceding report head | `757f2ee4e3bf766d2eb56d972e6d2f621b3fd2a6` |
| Actual mathematical source reviewed in that report | `219b39e94b14187561dc3b7e5bdbae49dbd92cc2` |

All manuscript page numbers refer to the final 255-page main PDF. Source identifiers S01–S12 and literature identifiers L1–L4 are defined in [AUDIT_AND_REPRODUCTION.md](AUDIT_AND_REPRODUCTION.md). The historical source-directory name `A2-v17-boundary-information-coarsening` does not identify the revision being reviewed.

## Recommendation to the editor

**I do not recommend acceptance at the requested highest-level general-journal standard. My recommendation is rejection at that level on the demonstrated contribution and its presentation, not technical rejection based on a newly established false theorem.** Within the fresh proof coverage specified below, I have not found a fatal error in the new infinitesimal rigidity theorem or its finite-coordinate consequence. In particular, I would not characterize revision 48 as an invalid inference from exact injectivity to an injective derivative.

This revision is materially stronger than revision 47. Theorem A organizes a genuine structural inverse, and Section 20 supplies the missing type of argument needed to pass from exact reconstruction to a derivative-kernel statement. The new result allows contact points, obstacle shapes, gaps and the marked lattice to move. The proof treats the analyticity of the variation itself, rather than merely the analyticity of each parameter slice. It also accounts for inter-channel rotation and lattice motion. These are mathematical improvements, not merely better delivery records. [S01–S04]

Nevertheless, the differential result is an extension of the manuscript's existing smooth finite-order inverse, analytic uniqueness and incidence reconstruction. Its final finite-dimensional coordinate theorem is the expected duality and inverse-function consequence once the kernel has been identified. The substantial original mechanisms that must justify an exceptional general-journal placement remain the nonlinear relative law and its signed, actual-smooth contact inverse. The new section organizes and strengthens their consequences; it does not by itself establish a new dynamical mechanism or a substantially different rigidity datum. I remain unpersuaded that the contribution, in its present 255-page exposition, meets the requested exceptional threshold.

That is an editorial evaluation, not a mathematical obstruction or a prediction binding on another editor. It is not a demand to abandon the program, weaken valid theorems, delete technical material, or supply an indefinitely expanding list of new theorems. A different referee may value this observation-specific inverse more highly. An unfavorable placement assessment must not be converted into an invented proof gap.

## 1. Scope, changes, and disposition of the previous review

The new active mathematical modules are `00_structural_introduction_v48.tex` and `23m_differential_rigidity_v48.tex`. The latter occupies pages 89–93. Theorem A is on page 4. The main entry and the heading of the earlier detailed introduction receive editorial amendments. The independently rerun preservation control verifies 103 inherited active inputs: 101 are byte-identical in place, and exact originals of the two amended inputs are archived. The final active graph contains 105 inputs. [S01–S03, S12]

The fresh mathematical examination covers the complete new introduction and Section 20; the four-density inverse; the weighted half-line, terminal-envelope and smooth finite-jet arguments at the interfaces used by Section 20; the relative amplitude construction at its parameter-differentiation interface; the finite clear-channel skeleton and harmonic/cochain reconstruction; the distinction from the earlier fixed-contact variation bundle; and the unchanged v47 calibration module. The historical audit and response were checked against those sources, not treated as substitutes for them. [S04–S11]

This is not a new line-by-line certification of every inherited theorem in 255 pages plus the companion. In particular, this round does not independently re-prove every relative-operator estimate, compact Le Cam approximation, LAN theorem, Poisson limit, deficiency estimate, deconvolution theorem, appendix or companion result. The complete PDFs were rebuilt and compared, but that operational coverage is not mathematical proof coverage.

| Previous issue or claim | Disposition in this revision |
|---|---|
| R46-P1: distinguish exact-offset bias from timing and chart errors | Remains resolved; the corrected source is retained. |
| R47-C1: offset amplification and normalization | Retained correctly; old Lemma 19.7 is now Lemma 21.7. |
| R47-C2: hard-cell crossings, including outer edges and singular chart maps | Retained correctly; old Lemma 19.8 is now Lemma 21.8. |
| R47-C3: pilot conditioning and separate preparation-cap accounting | Retained correctly; old Theorem 19.9 is now Theorem 21.9. |
| R47-C4: fix the final flight before the pilot; leave strict error-budget slack | Retained correctly; old Corollary 19.10 is now Corollary 21.10. |
| v47 added only an acquisition extension, rather than a new rigidity consequence | No longer a sufficient description of the revision: Section 20 adds a whole-table differential theorem. |
| Complete source-matched native delivery | No outstanding objection on the independent checks performed here. |
| Exceptional general-journal significance | Reassessed on the new structural theorem; still not established to my satisfaction. |

The earlier report did not require a new infinitesimal theorem to repair the calibration mathematics. Credit for the new theorem and the historical status of the old issues should remain separate.

## 2. The observation and the claims actually made

The datum is the gap of each selected channel and the two same-type signed conditional endpoint laws at a known positive offset. It includes the obstacle, channel and deck marks and signed coordinate conventions. It does not supply the Euclidean lattice vectors, their Gram matrix, or an inter-channel registration. The choice of a persistent finite skeleton is part of the marked design, not the output of an unmarked discovery algorithm. [S01, S08]

The distinction between a finite number of channels and a finite amount of scalar information matters. Each exact law is a function-valued object. The count of N+1 channels is minimal for the specified tree-plus-two-independent-cycle architecture, not a universal information-theoretic lower bound. The manuscript now states this limitation explicitly. It is not a contradiction in Theorem A.

The differential experiment keeps the excess time fixed in smoothly moving intrinsic contact coordinates. The contact-centered squares contain the axis slices and nonzero anchors required by the density inverse. The frame convention is not an observed inter-channel pose. This is an intrinsic derivative theorem; it is not, without an additional argument, a theorem for one fixed laboratory chart with parameter-independent contact origins. The author does not make that latter assertion. [S02, lines 31–58]

Theorem 20.6 selects p exact scalar observables for an immersed p-dimensional model, locally at a stipulated base table. These observables may depend on that table and model. It does not supply one fixed finite vector identifying every analytic table, a global coordinate system, a uniform conditioning constant over all models, or a finite-sample efficiency theorem. The full-class histogram theorem and the richer planar-position calibration pilot remain separate results with their own priors and error accounting. [S01, S02, S10]

## 3. Fresh mathematical audit

### R48-C1 — forward differentiability and moving normalization

**Location:** Lemma 20.1, pages 89–90; S02, lines 13–130.

The common-strip hypothesis is appropriate. A C1 map into the supremum-norm space of bounded holomorphic support functions gives the required finite real derivatives by Cauchy estimates. After a moving Euclidean frame change, restricting to a smaller strip also controls the term involving the derivative of the original support function. Merely assuming that every parameter slice is analytic would not give this conclusion.

The contact equations have the positive Hessian displayed in the manuscript, with determinant

$$
\kappa_0\kappa_1+g^{-1}(\kappa_0+\kappa_1)>0.
$$

Thus the implicit-function argument for the contact frame and gap is nondegenerate. At the half-line level, the weighted inverse and endpoint estimates in Lemmas 13.2–13.3 supply the finite-order parameter differentiation used here. The parameter is allowed to enter through the entire support function; only finitely many real smooth bounds are required for each derivative order. [S05]

The amplitude step is compressed, but the relevant inference is supported by the relative construction. In its determinant representation, writing the trace-class perturbation as T=G Delta H, the parameter derivative has the form

$$
\frac{d}{dt}\log B
=\dot U-\operatorname{tr}\bigl((I+T)^{-1}\dot T\bigr),
\qquad
\dot T=\dot G\,\Delta H+G\,\dot{\Delta H}.
$$

The moving reference operator must be differentiated too. Endpoint decay applies to the perturbation after subtraction of that reference; the uniform weighted bounds give the needed summability. This is the functional-family version of the differentiated construction used in Lemma 20.1, not differentiation of an arbitrary limiting sequence. Printing this intermediate identity near the lemma would make the dependence easier to audit. I classify that as an expositional improvement, not a newly established gap. [S06]

The normalization calculation is correct. On a fixed box,

$$
Z_t=\int w_t(d-A_t)_+,\qquad
\dot Z=\int\left[\dot w(d-A)_+-w\dot A\,\mathbf1_{\{A<d\}}\right].
$$

For d>0 the cap boundary is a regular level set, hence has planar measure zero. Positive-part difference quotients admit a common integrable bound, and the same argument gives continuity of the derivative. On the chosen positive interior square the cutoff is inactive. No omitted first-order boundary Dirac term occurs. No claim about differentiability across the boundary in an arbitrary global strong density norm is needed.

The independent radial-cap control checks the normalizer and normalized derivative exactly and detects omission of the normalizer derivative. It is a functional diagnostic, not a billiard realization or a proof of the preceding infinite-flight construction.

**Finding:** the printed C1 conclusion is supported at the audited interface under the stated common-strip and persistent-channel hypotheses.

### R48-C2 — the signed density inverse and actual finite contact jets

**Location:** Lemma 20.2, pages 90–91; S02, lines 134–190; Theorem 14.1 and Lemma 13.4.

Let R be the four-density ratio, q=sqrt(1-R(a,a))>0, and t(u)=(1-R(u,a))/q. Direct differentiation gives

$$
\dot t(u)=-\frac{\dot R(u,a)}q+
\frac{t(u)\dot R(a,a)}{2q^2},
\qquad
\dot S(u)=\frac{d\dot t(u)}{(1+t(u))^2}.
$$

The sign of the second term is positive. The nonzero scalar anchor avoids the singular pointwise square-root operation at the minimum of the action. The square is explicitly contact-centered, so every required slice is available. Amplitude and normalizer variations cancel in R; they are not presumed known. Zero density derivative therefore gives zero action derivative in every separately prescribed finite smooth norm, including odd signed derivatives. [S02, S04]

The leading curvature recovery is smooth in the positive variables. At each higher order, the identity

$$
s_n=M_nq_n+R_n
$$

is an identity for actual smooth representatives, not only for formal Taylor series. This is precisely why Lemma 13.4 matters. Differentiation must retain both dot R_n and dot M_n q_n. The manuscript retains them. Induction on the finite order then makes the recovered graph-jet derivative zero. There is no interchange of a parameter derivative with an infinite inverse series and no asserted order-uniform bound for M_n inverse. [S05]

As an independent algebraic check, summing the linear endpoint visits gives diagonal entries (1+z^(2n))/(1-z^(2n)) and off-diagonal entries 2 r_b^n z^n/(1-z^(2n)), with r_0 r_1=1. Their determinant is one. The supplied diagnostic checks orders 3–16 at positive unequal curvatures. The geometric-series calculation does not replace the smooth remainder proof, which was separately inspected.

**Finding:** I found no lost odd term, missing derivative contribution, or formal-to-smooth substitution in this argument.

### R48-C3 — analytic propagation applies to the variation

**Location:** Lemma 20.3, page 91; S02, lines 192–224.

The graph-to-support conversion at each finite order is nondegenerate because curvature is positive. Contact translations are fixed to first order when the gap derivative vanishes. Consequently every normal-angle derivative of the support variation vanishes at the contact normal.

The essential next statement is that the support variation itself is holomorphic on a common smaller strip. In moving coordinates it is a combination of translated dot h, a multiple of translated h prime, and first harmonics. The stipulated C1 holomorphic-support family justifies this statement. The identity theorem then kills the entire channel-frame image variation.

There is no appeal here to a bounded inverse for analytic continuation. Qualitative uniqueness and quantitative continuation stability are different assertions. The adverse conditioning discussed in L4 does not refute this exact kernel argument. Conversely, the identity theorem does not supply the noisy histogram modulus, which the manuscript treats separately. [S09]

**Finding:** the analytic step is valid for the announced family class. It is not proved merely from pointwise analyticity of the slices, and the author correctly avoids that weaker premise.

### R48-C4 — general asymmetric registration and the unknown lattice

**Location:** Lemma 20.4, pages 91–92; S02, lines 228–304; S08.

For an obstacle with trivial proper symmetry, finitely many nonzero centered support harmonics have indices with greatest common divisor one. Selecting integers a_k with sum a_k k=1 gives

$$
r_k=\frac{z_k(C_t)}{z_k(C_s)}=e^{-ik\alpha},
\qquad
U=\prod_k r_k^{-a_k}=e^{i\alpha}.
$$

This formula is differentiable on its nonvanishing domain and avoids a choice of argument or root branch. It is not restricted to the second-and-third-harmonic subclass. In particular, the witness (6,10,15), with coefficients (1,1,-1), works although no pair is coprime. The corresponding support perturbation can have strictly positive curvature. The proof makes no unjustified extension of this congruent-image formula to arbitrary noisy image pairs.

After the tree rotations are recovered, the displacement cochain gives

$$
v_i=p_{a_i}+d_{f_i}^{\rm cen}-p_{b_i},\qquad
L=(v_1\ v_2)M^{-1},\qquad
c_a=p_a-Lm_a.
$$

The integer matrix M is fixed by the marked design and is invertible over the reals, not necessarily unimodular. Hence

$$
\dot L=(\dot v_1\ \dot v_2)M^{-1}.
$$

The unknown scale and Gram form have not been supplied as calibration. The independent cochain control uses det M=6 and detects the incorrect omission of M inverse.

I also inspected the clear-skeleton argument supporting the design: obstructed closest segments are replaced by strictly shorter connections, periodic separation gives finite descent, and two independent gain cycles are selected after a finite connected graph has been obtained. Those replacement paths are graph constructions, not claimed billiard trajectories. The N+1 count is used only for the stipulated architecture. [S08, Theorem 19.3, Proposition 19.5]

**Finding:** the registration and lattice parts close the derivative kernel under the stated hypotheses. Treating M as automatically unimodular, or treating the channel frames as already registered, would invalidate a different proof; neither mistake is present here.

### R48-C5 — the full derivative kernel and finite scalar coordinates

**Location:** Theorems 20.5–20.6, pages 92–93; S02, lines 306–432.

Zero derivatives of all smooth compactly supported expectations imply zero interior density derivative because a nonzero continuous derivative has one strict sign on a small ball. The preceding steps then give zero gauge-fixed support and lattice derivatives. Undoing the gauge gives exactly

$$
\dot h_i(\theta)=a\cdot n(\theta)-\omega h_i'(\theta),
\qquad \dot L=\omega J L.
$$

This is a proof of the kernel, not an inference from injectivity of the undifferentiated map. Conversely, simultaneous proper Euclidean motion leaves the intrinsic data invariant.

On an immersed p-dimensional gauge-fixed model, the derivatives of the allowed gaps and expectation functionals have zero common kernel. They therefore span the p-dimensional dual, and p members can be selected as a basis. These are actual observable functionals, not density-derivative evaluations disguised as observations. The inverse function theorem applies. The lower Lipschitz estimate follows from closeness of DF to one fixed invertible matrix on a convex ball, not merely from pointwise nonsingularity of DF. The additional support-norm bounds are local, fixed-order consequences of the common-strip family.

The earlier variation-bundle theorem concerns compatible fixed-contact finite jets and positive information designs, allowing several offsets. It is not the same theorem. Revision 48 adds whole-table, moving-contact and moving-lattice rigidity at one fixed offset per channel. [S11]

**Finding:** the differential and finite-coordinate clauses of Theorem A are supported by the new chain at the level examined. The finite-dimensional last step is standard; the geometric kernel proof is the substantive prerequisite.

### R48-C6 — calibration has not silently changed its experiment

**Location:** Lemmas 21.7–21.8, Theorem 21.9 and Corollary 21.10, pages 101–104; S10.

The unchanged module still uses the true offset d_0+j(g_hat-g)+omega. Its hard-category coupling includes outer as well as internal edges and permits a singular image chart map. The final even flight is fixed before the same-flight pilot. Concentration is applied to the uncapped successful streams conditional on the pilot; cap failure is charged separately. The final tolerance budget remains 15 eta_*/16, leaving strict slack.

The new smooth scalar tests are used for a different local exact-coordinate theorem. They have not replaced hard histogram categories in the acquisition theorem. Nor has the richer planar-position pilot been relabelled as calibration from histograms alone. These distinctions are correctly retained. No new calibration objection is raised in this round.

## 4. A useful mathematical distinction: finite symmetry versus an infinitesimal symmetry

The following is a referee observation derived from the audited chain, not a claim already made by the manuscript and not a condition for repairing the current theorem.

**Local strengthening.** For the derivative-kernel and model-local coordinate conclusions, trivial proper symmetry of every obstacle can be weakened to noncircularity of every obstacle, provided the other hypotheses and the persistent selected skeleton are retained. This statement concerns the local differential conclusions only; it does not assert global exact uniqueness on that larger class.

Indeed, a noncircular strictly convex support function has some nonzero harmonic z_k with k>=2. For two copies of that obstacle along a C1 family, choose the local angular lift through their actual base alignment. Then

$$
\frac{\dot r_k}{r_k}=-ik\dot\alpha.
$$

Stationary channel-frame images imply dot r_k=0, hence dot alpha=0. Their centers then make the relative translation derivative zero. One nonzero harmonic suffices to determine an angular velocity; a greatest-common-divisor-one set is needed to remove all discrete global rotational alternatives. Propagate these zero relative velocities along the spanning tree and use the same two-cycle cochain to obtain zero gauge-fixed lattice and placement derivatives. Lemmas 20.1–20.3 do not use proper asymmetry, so this replaces the only affected step. The finite-coordinate argument follows unchanged on an immersed local gauge slice.

This distinction makes the role of symmetry more precise. A finite cyclic symmetry does not itself create a nonzero infinitesimal symmetry. The current theorem is correct on a smaller class; its hypothesis is not sharp for its differential clause. The observation above should not be used to extend the global exact clause without an additional discrete matching argument.

There is also a genuine geometric control showing why arbitrary circular obstacles cannot simply be included. Take one disk orbit of radius 1/10 and

$$
L_t=\begin{pmatrix}1&-\sin t\\0&\cos t\end{pmatrix},
\qquad |t|<1/10.
$$

Select the channels with deck gains e_1 and e_2. Both lattice columns have length one, so both gaps are 4/5. Each selected two-disk configuration is congruent to its base configuration in its own channel frame. The gaps and the two same-type conditional laws in each selected channel are therefore unchanged.

These are admissible clear channels for small t. One elementary check is that ||L_t-I||<=1/10, so every nonzero lattice displacement has length at least 9/10 and the disks are separated. At t=0 every other lattice center is at distance at least one from either unit center segment. A center within distance 1/2 of a perturbed segment would have norm less than 3/2, and its integer mark would have norm less than 5/3. It is therefore among the eight nearest integer neighbors. For these marks, perturbing the center and segment decreases the original distance by at most (sqrt(2)+1)/10<1/4, a contradiction. Thus the selected segments remain clear, with ample room for gates.

Yet

$$
\dot L_0=\begin{pmatrix}0&-1\\0&0\end{pmatrix},
\qquad
\left.\frac{d}{dt}\right|_0 L_t^T L_t
=\begin{pmatrix}0&-1\\-1&0\end{pmatrix}.
$$

This motion is not a common Euclidean motion: the first lattice column has zero derivative while the second does not, and the Gram form changes. The example is outside the asymmetric hypotheses and is **not a counterexample to Theorem A or Theorem 20.5**. It concerns the local selected-channel setting, not a finite-horizon assertion. The independent script checks its lattice identities; the clearance and observation arguments are the geometric reasoning given here.

## 5. Contribution, literature, and writing at the requested level

The manuscript's strongest conceptual sequence is

**nonlinear relative boundary law -> amplitude-free signed action inverse -> actual smooth contact jets -> analytic obstacle images -> intrinsic periodic registration.**

The first two arrows deserve particular emphasis. A quadratic orbit approximation alone would not recover the nonlinear actions, and a formal coefficient computation alone would not recover actual smooth boundaries. It would be inaccurate to dismiss the entire paper as an application of finite-dimensional linear algebra. Section 20, however, differentiates this already developed sequence and then applies analytic uniqueness and algebraic registration. Its final scalar-coordinate result does not add an independent general embedding principle. [S04–S08]

Theorem A improves the presentation by placing the whole recovered object and its derivative kernel together. It does not follow that seven additional proved statements resolve the placement question. Nor does the existence of a 255-page proof corpus establish breadth or significance by itself. The same observation-specific inverse now supports many consequences, but the article still distributes its central argument across a new structural introduction, the retained detailed introduction, the local density inverse, the finite-channel section, the differential section and separate statistical parts. The reader must repeatedly distinguish foundational results from consequences and changes of observation. Source preservation is valuable; it is not a substitute for a single economical proof architecture.

The literature comparison is now appropriately cautious. Finamore–Leguil's current arXiv record treats finite-horizon Sinai billiards using an enriched marked length spectrum. De Simoi–Kaloshin–Leguil treat marked length data for analytic open billiards under symmetry and genericity assumptions. These are not the boundary-law datum of this manuscript. I found no justified reduction identifying the observation maps, and I do not claim that these papers already prove Theorem A. [L1, L3]

The cited fifth version of Florio–Leguil explicitly removes an earlier geometric spectral-rigidity assertion affected by an error while retaining dynamical conjugacy results. The manuscript uses the appropriate version and does not rely on the removed assertion. That historical correction is not evidence against the present density inverse. [L2]

The targeted primary-source comparison does not establish exhaustive priority. It does establish that the contribution should be defended as a new observation-specific inverse, not advertised as merely removing hypotheses from an existing marked-length theorem. The current introduction substantially respects that distinction. The remaining unfavorable significance judgment is mine; it is not a missing citation or an algebraic lemma that the author can mechanically close.

For any further submission, I would preserve the valid results and reorganize their dependency path rather than append another unrelated theorem in response to this report. The finite-symmetry distinction in Section 4 can sharpen the explanation of the derivative result, and the displayed amplitude derivative in R48-C1 can make its functional-family input explicit. Neither is a demand for an entirely new research program, and neither is represented here as a fatal defect in the present proof.

## 6. Independent reproduction and final disposition

The final Actions artifact was downloaded through the authorized GitHub connector. Its main PDF, companion PDF and native-source archive match the recorded SHA-256 digests. The comparison from the mathematical source commit to the review-ready snapshot contains delivery and navigation changes, not changes to the compiled TeX sources. Both complete entries were then rebuilt locally from the downloaded source with shell escape disabled. [S12]

The rebuilt main has 255 pages and the companion has seven. All 262 pages agree with the native PDFs in extracted text and in 100-dpi RGB raster arrays using the same renderer. The rebuilt PDF byte hashes differ from the native hashes; byte-identical PDFs are not claimed. The final local main log has four underfull-box warnings, no overfull boxes and no unresolved-reference/citation warning; the companion has none of those layout warnings. This is a reproducible build, not a warning-free one.

Direct visual inspection in this round covers main pages 4 and 89–94 and companion pages 1 and 7. Those pages include Theorem A and the complete new differential section. The full-page automated comparison is additional evidence of rendering parity, not a fresh visual or mathematical reading of every page. The independently written finite diagnostics and the author preservation control both pass in ordinary and optimized Python, with identical paired outputs. Their scope is stated in the accompanying JSON files.

**Final disposition:** the new differential proof is materially responsive and survives the fresh checks reported here; the old calibration issues remain closed; complete delivery is independently reproduced. I nevertheless do not recommend acceptance at the requested highest-level general-journal standard on the contribution and presentation demonstrated. I am not reporting a newly proved counterexample to a stated theorem, and I am not certifying all inherited mathematics. These conclusions must remain distinct in the next author response.
