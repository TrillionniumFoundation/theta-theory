# Independent harsh referee report on A2 revision 77

**Manuscript:** *Statistical action recovery and smooth rigidity of dispersing billiards*  
**Author:** Qian Qi  
**Date:** September 17, 2026  
**Reviewed source branch:** `revision/a2-v77-three-clock-smooth-atlas-2026-09-17`  
**Reviewed head:** `97d1ead42809508cea508ee44576e71b95fdcc06`  
**Reviewed head tree:** `db66b4a3bb22751d4eb6eca1ac93bc7b149060ee`  
**Reviewed baseline:** `revision/a2-v76-relative-envelope-2026-09-17` at `ba8e40b92887e2cd8dcc92f3358401aac8c961d2`  
**Revision delta:** 25 commits ahead of the v76 head, with no commits behind  
**Prior controlling report addressed by the authors:** `review/a2-v76-independent-harsh-top4-2026-09-17`, report commit `fd4c9f57b9d0b142b60e163b266a708b61d80c94`  
**Requested standard:** the level expected of *Annals of Mathematics*, *Inventiones Mathematicae*, *Acta Mathematica*, or the *Journal of the American Mathematical Society*.

This is an author-requested independent referee-style assessment, not a commissioned journal report or an editorial decision. I deliberately apply a severe general-journal standard. I distinguish mathematical correctness of the new proof chain from the separate question whether the theorem, data model, and conceptual advance justify one of the four leading general mathematics journals.

A versioning warning is important at the outset. An earlier branch named `revision/a2-v77-weighted-action-global-reconstruction-2026-09-17` was source-identical to the v76 branch, and the earlier `review/a2-v77-independent-harsh-top4-2026-09-17` report correctly objected that there was then no new v77 mathematical source. That report is not controlling here. The branch reviewed now is a genuine later revision: it is 25 commits ahead of the v76 head and contains a substantial new finite-action/global-geometry argument.

## 1. Recommendation

**I do not recommend acceptance at the requested highest general-journal level in the present form.**

This recommendation is materially different from the v76 recommendation. Revision 77 does answer the most obvious scope objection to v76: the paper no longer stops at smooth germs around a supplied periodic polygon. It now proves, for a finite identifying atlas, a global Euclidean reconstruction theorem from three-clock conditional endpoint laws; it proves existence of such finite atlases for a nonempty class of finite-horizon periodic dispersing tables with locally nonconic boundaries; and it gives stability and a finite-record consequence. It also supplies the explicit periodic determinant bridge requested in the v76 report. Those are genuine mathematical additions, not relabelling or bookkeeping.

After a focused audit of the new chain, I have **not found a fatal local mathematical error** in the central algebraic and geometric mechanisms under the hypotheses as stated. In particular, the three-clock cancellation, the shared-prefix Schur-complement calculation, the finite distance certificate, and the finite-cover construction all have substantive content and should not be dismissed merely because some individual ingredients are elementary.

The problem is instead the level and nature of the theorem being offered as a top-general-journal result. The global statement remains based on an object-dependent, highly marked acquisition design: exact branch and lift labels, a supplied scalar boundary atlas and overlap maps, branch-specific gates, clock windows chosen from coarse action/free-flight information, and root brackets that select the intended shared-prefix match. The manuscript proves that **for each table there exists a finite identifying experiment of this rich marked kind**. It does not prove reconstruction from one canonical natural data set, a table-independent finite protocol on a substantial class, or a universal finite adaptive acquisition procedure.

Moreover, once the three-clock conditional laws are available under the cross-clock shared-weight hypothesis, the manuscript algebraically recovers the full exact two-variable branch action on each gate. From that point, generating-function composition recovers a final-flight distance kernel and standard Euclidean distance geometry reconstructs the boundary patches. This is a clever synthesis, but the manuscript does not yet establish a theorem showing that its statistical records constitute a genuinely weaker or structurally different information class than the rich travel-time/lens or enriched marked-length data already known to yield global rigidity. Saying that an individual travel-time function is not directly supplied is not, by itself, an information-order theorem when the proposed records exactly invert to an action function.

Finally, the 70-page principal article is not conceptually unified. Its first part is the new finite-action global inverse. Its second part essentially retains the earlier periodic asymptotic smooth-germ paper, with its own introduction, theorem, determinant normalization, jet inverse, and actual-function envelope. The authors themselves correctly call the two experiments complementary and logically independent. Concatenating two substantial inverse problems into one article does not create one stronger top-four theorem. At this standard the paper needs a single organizing theorem or principle, not cumulative length.

My negative recommendation is therefore a **placement judgment**, not a declaration that the new main theorem is false.

## 2. Scope of this review

I compared the reviewed v77 head with the v76 head and inspected the new material that controls the revision-specific claims:

- `A2_REVISION_V77_REVIEW_READY.md`;
- `RESPONSE_TO_REFEREE_V77.md`;
- `rigidity_v77.tex` and `main_v77.tex` as active entry points;
- `article/v77/01_experiments.tex`;
- `article/v77/02_physical_clocks.tex`;
- `article/v77/03_prefix_cancellation.tex`;
- `article/v77/04_distance_registration.tex`;
- `article/v77/05_finite_coverage.tex`;
- `article/v77/06_stability_records.tex`;
- `article/10n_periodic_determinant_bridge_v77.tex`;
- the v77 periodic-relative copy and the inherited v64 relative-law proof at the estimates used by the new determinant bridge;
- the historical derivation audit and the v77 verification records.

I also checked the paper's stated comparison with the neighboring rigidity literature, including Noakes--Stoyanov's planar lens-rigidity theorem, the Finamore--Leguil Sinai-billiard marked-length preprint, and Connelly--Gortler--Theran's complete-bipartite global-rigidity work.

I did **not** treat source-preservation counts, successful typesetting, numerical fixtures, PDF hashes, or label checks as proof verification. The repository itself correctly says these are integrity and diagnostic checks rather than independent mathematical certification.

## 3. What revision 77 genuinely changes

The authors should receive full credit for addressing the old objection at the theorem level rather than merely refining constants.

### R77-C0. The new v77 is a real mathematical revision

Relative to the reviewed v76 head, this branch adds a new six-section proof chain and new active manuscripts. The central theorem now starts from a finite collection of branch-specific three-clock conditional endpoint laws in abstract scalar boundary coordinates and concludes Euclidean recovery of target boundary patches, and of the whole marked periodic table and lattice when the atlas covers the whole table.

This is not the earlier nominal v77 whose branch name changed while its tree did not. Any report that merely repeats the earlier “there is no v77 source delta” objection would be obsolete.

### R77-C1. The v76 “local marked germs only” objection has been materially addressed

The new theorem no longer assumes the Euclidean contact positions, tangent frames, chart speeds, periodic polygon, absolute branch lengths, or lattice Gram matrix. The recovered object is not merely a germ at a supplied finite list of contacts. For a finite identifying atlas, the theorem reconstructs complete parametrized target arcs and registers them in one Euclidean plane. The finite-atlas theorem then supplies whole-boundary coverage on its stated geometric class.

This is a substantial strengthening of scope relative to v76.

### R77-C2. The requested determinant instantiation has also been supplied

The new periodic-block corollary explicitly specifies the first/last retained blocks, the middle-deletion trace-norm cost, the off-diagonal Hilbert--Schmidt coupling, the finite-to-half-line trace-norm error, the common interpolation margin, and the final logarithmic determinant rate. This is materially better than the one-paragraph bridge criticized in the v76 report.

I return below to whether this should count as an independent top-level contribution; as an answer to the concrete referee request, however, it is a real improvement.

## 4. Correctness audit of the new central mechanism

The following are positive findings. They do not settle originality or placement.

### R77-C3. The three-clock absolute-action algebra is correct under the stated shared-weight model

The physical law is

\[
 f_j(z)=Z_j^{-1}a(z)(T_j-W(z)),\qquad j=1,2,3,
\]

with the same positive multiplier `a` at the three clocks. After normalizing each density at a reference point, the displayed affine identity

\[
 (T_j-W_0)g_j(z)=b(z)(T_j-W(z))
\]

is exact. The coefficient vector

\[
 (c_1,c_2,c_3)=(T_2-T_3,T_3-T_1,T_1-T_2)
\]

annihilates both constants and the clock variable. The resulting formula for the anchor value `W_0` and the subsequent two-clock fractional-linear inversion recover the absolute action. The nonconstancy argument gives a usable point where the anchor denominator is nonzero.

I do not find an algebraic defect here. The theorem also correctly states the necessary denominator floors for local Lipschitz stability.

### R77-C4. The physical Jacobian calculation is coherent under the source assumptions

In the pre-collision flow box, the phase-volume element becomes `ds dp d alpha`; the endpoint change of variables contributes `|W_st|`; and the admissible clock window makes the allowed alpha-interval have length exactly `T-W`. Hence

\[
 a(s,t)=e(s,t)\rho(s,-W_s)|W_{st}|
\]

is indeed common across the three clocks provided the preparation density is independent of the initial free-time coordinate and the retention law is clock-independent on that branch.

These hypotheses are strong and important for significance, but the derivation under them is not obviously wrong.

### R77-C5. The nonlinear shared-prefix cancellation has the correct Schur-complement sign

For the prefix action `U` and its one-flight extension `V`, the stationary composition gives

\[
 V=U+\ell,\qquad U_t+\ell_t=0.
\]

The interior second variation is positive definite for a regular dispersing trajectory. Eliminating the prefix variables leaves a positive Schur complement

\[
 B=U_{tt}+\ell_{tt}>0.
\]

Differentiating the stationary relation yields

\[
 t_s=-U_{st}/B
\]

and therefore, for the matching equation `H=V_s-U_s`,

\[
 H_s=-\frac{U_{st}^2}{B}<0.
\]

This supplies precisely the monotonicity needed for a unique physical root on a sufficiently small product box. Substituting that root into `V-U` recovers the full final-flight distance including its additive constant.

I do not see a hidden use of measured momenta: the covectors are derivatives of the recovered actions.

### R77-C6. The finite Euclidean distance certificate is mathematically sound under its rank assumptions

The squared-distance double differences factor as

\[
 X_{ij}=(a_i-a_0)\cdot(b_j-b_0).
\]

Rank two determines the relative two-dimensional span. The five additional equations solve the symmetric metric and translation parameters, after which ordinary trilateration recovers the full parametrized patches from the whole distance kernel. The ambiguity is exactly one common Euclidean isometry.

The nonconic condition is used as a sufficient finite certificate: linear dependence of

\[
 1,A_1,A_2,A_1^2,A_1A_2,A_2^2
\]

would place the arc in a quadratic zero set. Conversely, linear independence permits a six-point evaluation basis. This is a clean argument. The manuscript also appropriately does **not** claim that conic arcs are necessarily nonidentifiable.

### R77-C7. The finite-cover argument is nontrivial and, at the level inspected, plausible

The argument avoids the invalid step “dense visits imply a uniform inverse collar.” It instead constructs regular long prefixes locally, proves connectivity of the lifted visibility graph, covers each compact boundary by finitely many reconstructible patches, and then registers the finite cover through overlap triples.

The explicit triangular-lattice example also has the right shape. The support-function inequalities give strict convexity and separation; the contained disks close all rational and irrational corridors under the stated radius bound; analyticity plus noncircular threefold symmetry excludes containment in a conic; and sufficiently small nonanalytic smooth perturbations preserve the finitely many strict certificates.

I have not found a fatal gap in this existence construction during this review.

### R77-C8. The new global route does not rely on equality of smooth jets

A major strength of the older periodic argument was its care with flat `C^infty` differences. The new finite-action route is different: after action recovery and prefix cancellation it reconstructs an **actual distance function**, and the Euclidean inversion acts on that full function. Thus the global theorem does not secretly use analytic continuation or the false implication “all jets equal implies smooth functions equal.”

### R77-C9. The determinant bridge is consistent with the inherited Green estimates at the displayed level

The inherited periodic proof supplies exponential Green decay, reflected finite/half-line Green comparison, endpoint localization of the Hessian perturbation, and a uniform small operator margin on a fixed collar. The new corollary organizes these into trace-class diagonal blocks and a Hilbert--Schmidt cross coupling. Squaring the latter is the correct second-order cost after block parity kills the first trace variation.

I do not find a newly introduced dimension factor or a trace-ideal category error in the stated bridge.

These findings are deliberately more positive than the placement conclusion. A harsh referee should not manufacture a mathematical error merely because the editorial threshold is not met.

## 5. Major concerns

### R77-M1. The “global reconstruction” theorem is still based on an object-dependent acquisition design

This is the most important unresolved issue.

The theorem does **not** say that one fixed natural observation operator on a class of billiards is injective. For a given table it first constructs a finite identifying atlas whose ingredients depend on the table's geometry and regular trajectories. The retained experimental information includes, among other things:

- an abstract scalar boundary atlas and exact overlap maps;
- obstacle and lattice-lift labels;
- exact reflection words / branch identities;
- exact gate membership;
- a paired identification of a branch with its one-flight extension;
- a prescribed common initial scalar coordinate for that pair;
- a root bracket selecting the intended solution of the matching equation;
- three absolute clock times on a branch-specific admissible window;
- enough coarse branch-length and adjacent-free-flight information to choose those windows;
- anchor points and finite-rank nondegeneracy margins;
- and, in the whole-table case, labelled copies corresponding to two abstract lattice basis elements.

The manuscript is commendably explicit that its design theorem is an existence-and-persistence theorem and **not** a universal finite adaptive search. That honesty is a strength. But it also identifies the limitation.

At a specialist level, a theorem of the form “every object admits a finite identifying marked experiment” can be useful. At the requested top-general-journal level, the missing step is substantial: can the experiment be chosen canonically, or from a table-independent acquisition family with a proved finite stopping rule, on a natural class? Can the labels be inferred rather than supplied? Can one state injectivity of a fixed observation map rather than injectivity after choosing an object-dependent finite certificate?

Without such a result, “whole-table reconstruction” risks overstating what has actually been proved. The theorem is global in the **target**, but not yet natural or global in the **data acquisition problem**.

### R77-M2. The paper does not establish that the statistical data are genuinely weaker than classical global rigidity data

The introduction emphasizes that no individual travel-time function, Euclidean ray position, lens map, or marked periodic-length family is directly observed. Formally that is true.

But under the shared-weight, alpha-independent source model, three exact conditional densities on a gate determine the full exact two-variable branch action `W(s,t)`. After this algebraic inversion, the rest of the proof uses the generating-function composition law to obtain an exact Euclidean distance kernel.

For significance, the relevant question is therefore not whether `W` is literally listed among the raw observations. It is whether the proposed statistical experiment is **strictly coarser, more natural, or otherwise mathematically distinct in information content** from the rich travel-time/action data already known to yield rigidity.

The manuscript does not currently prove such an information comparison. In particular:

1. there is no theorem placing the three-clock law experiment below a standard lens/travel-time experiment in a precise order;
2. there is no actual-billiard nonidentifiability theorem for two clocks showing that the third clock crosses a sharp physical information threshold;
3. the “two clocks leave a fractional-linear freedom” statement is proved in an unrestricted weighted-function model, and the authors correctly disclaim that every such fractional-linear deformation is a realizable billiard action;
4. the exact branch identities and endpoint atlas marks are substantial information not present in many standard formulations.

A top-four case would be much stronger if the paper proved a sharp observation theorem: for example, two-clock nonidentifiability and three-clock identifiability within a genuine billiard class, or a rigorous comparison showing that the proposed records are obtainable from substantially coarser measurements than a lens relation but are still complete.

As written, the statistical front end is elegant, but it may be an invertible reparameterization of already very rich action information rather than a fundamentally weaker inverse datum.

### R77-M3. The new theorem is a synthesis of several local mechanisms, but the manuscript has not isolated a genuinely new general principle

The new route combines:

- an elementary three-clock elimination of an unknown common multiplier;
- standard generating-function / stationary-action composition;
- a positive Hessian / Schur-complement monotonicity argument;
- finite Euclidean distance geometry and trilateration;
- compactness and finite covering;
- and classical dispersing-billiard regularity of finite orbit branches.

The synthesis is clever and nontrivial. Nevertheless, for one of the four leading general journals, I would expect the paper to extract from this synthesis a theorem whose conceptual content is visible beyond the particular assembly.

What is the general principle? For example, is there an abstract theorem for reconstructing a configuration manifold from finitely many normalized clocked generating-function laws? Is there a category of twist systems in which three-clock debiasing plus one-step composition implies global rigidity? Is there a sharp statistical-to-symplectic reconstruction principle with applications outside planar billiards?

The current manuscript does not formulate such a result. It proves the billiard case directly. That may be entirely appropriate for a strong specialist journal, but it weakens the claim of broad general-journal significance.

### R77-M4. The finite-atlas theorem is qualitative and nonuniform in exactly the quantities that control practical and mathematical complexity

The whole-table theorem proves existence of a finite design, but the number and quality of its components are uncontrolled. The manuscript itself notes that the number of settings may depend on the table and on the prescribed prefix length `J`.

More seriously, the stability constants retain inverses of:

- the three-clock anchor determinant;
- the clock residual floors;
- the mixed twist;
- the shared-prefix matching derivative;
- the distance-certificate singular values;
- the overlap registration singular values;
- and the finite registration-tree condition numbers.

The matching derivative is

\[
 -U_{st}^2/B,
\]

and can become very small for long prefixes. Thus the theorem allows the identifying experiment to become arbitrarily ill-conditioned as the requested number of prefix flights grows. The sampling consequence then adds a retained-success floor `p_*`, which can itself be very small.

None of this invalidates the theorem. But a top-level “finite global reconstruction” result would be substantially more convincing with at least one natural bounded geometric class on which the atlas size, flight lengths, gate widths, rank margins, and stability constants are quantitatively controlled. A purely existential finite subcover can hide extreme complexity.

### R77-M5. The branch labels are doing more work than the paper's high-level rhetoric suggests

The manuscript correctly states that unlabelled branch mixtures are not separated by the three-clock algebra. Indeed it displays the exact mixture identity showing that multiple branches collapse to a weighted average action.

This should be elevated from a final caution to a central limitation of the theorem. The experiment assumes exact branch identity rather than discovering it from the scalar records. For a dynamical inverse problem, branch labelling is not innocuous bookkeeping: it can encode substantial itinerary information.

The finite-atlas existence theorem therefore establishes global rigidity from **marked branch-resolved statistical laws**. The title and abstract should make that marking as prominent as the unknown Euclidean geometry. Otherwise readers may naturally infer a stronger unlabelled statistical inverse problem than the theorem proves.

A major advance would be to recover, or at least finitely disambiguate, branch structure from the observed records themselves.

### R77-M6. The paper still needs a theorem-level comparison with neighboring rigidity results, not only a prose comparison of raw inputs

The introduction cites relevant work and avoids several priority overclaims. That is an improvement. But the comparison remains descriptive.

Noakes--Stoyanov prove global determination from rich travelling-time/scattering data for planar unions of strictly convex bodies. Finamore--Leguil study rigidity of finite-horizon Sinai billiards from enriched marked-length information. The present paper reconstructs from branch-resolved normalized endpoint densities which, under its clock assumptions, invert exactly to branch action functions.

A reader deciding top-four novelty needs a precise map between these information structures. For instance:

- Does the present data determine a local lens relation, and if so on what set?
- Does a local lens relation conversely determine the present laws modulo the nuisance weights?
- Is the new experiment strictly weaker because it forgets outgoing directions but recovers them by differentiation?
- Which marking information is stronger than in the competing formulations?
- Is there an example where the present theorem applies but the hypotheses/data of the neighboring global rigidity theorems are unavailable in a meaningful sense?

Without such a theorem or at least a rigorous proposition-level comparison, the claim of a new observation interface remains difficult to weigh.

### R77-M7. The principal manuscript currently reads as two substantial papers concatenated, not one top-level article

`rigidity_v77.tex` first presents the new finite statistical-action / Euclidean-reconstruction theorem. It then begins a second major part containing the inherited periodic boundary-law inverse, including a fresh “Introduction,” a different observation model, a different limiting regime, different normalization, a different smooth inverse mechanism, and additional consequences.

The response explicitly says the two observation models are separate and neither theorem depends on the other. That is mathematically clean, but editorially it argues for separation rather than concatenation.

The combined abstract literally appends the new v77 abstract to the old v76 principal abstract. This reinforces the impression that the principal article is an aggregation of two mature manuscripts. The 390-page full technical manuscript intensifies that problem by carrying a large historical catalogue of related results.

For a leading general journal, the paper should either:

1. state and prove a genuinely unifying theorem that explains both the finite-action global inverse and the asymptotic periodic inverse as instances of one principle; or
2. split the new global theorem into a focused self-contained article and move the older periodic programme to a separate companion.

More pages and more inherited theorems do not increase the significance of the new result. They make it harder to identify the one reason the paper belongs in a general journal.

### R77-M8. The finite-record theorem remains a conditional consequence, not an independent statistical breakthrough

The sampling corollary assumes a fixed identifying atlas, exact branch and lift labels, smoothness bounds, denominator margins, and a positive retained-success floor. Recording error is bounded and the estimator is an existence construction through a countable dense subset, not an effective acquisition/reconstruction algorithm. The paper correctly says the rate is not minimax.

This is a useful bridge from law-level uniqueness to finite records. It should not be counted as a second independent top-level contribution. In particular, the real statistical difficulty of discovering the identifying branches and dealing with rare successes is not solved by this corollary; those difficulties are placed in the fixed-design constants and `p_*`.

### R77-M9. The determinant bridge closes a referee request but is still not a broad independent theorem

The new corollary is much better than the v76 application paragraph. I regard the old R76-M3 request as substantially answered.

However, the proof remains inseparable from the inherited one-dimensional tridiagonal Green/gluing estimates and fixed-order polynomial losses. It is not an abstract trace-ideal decoupling theorem with an independent class of applications. The dimension-free quadratic off-end coupling is a useful mechanism, but in the current paper it should be presented as a technical engine for the periodic theorem rather than as an independent reason for top-four placement.

### R77-M10. Reproducibility infrastructure is strong, but the current remote source head is not accompanied by a completed native-product/CI record

This is not a mathematical objection. It is an editorial/provenance point.

The source branch is now genuinely published at the reviewed head. The source tree includes local build/layout records and a review-ready handoff. But at the time of this review the reviewed source commit has no associated GitHub Actions status or workflow run, and the planned `revision/a2-v77-native-products-2026-09-17` branch is not present among the current v77 branches. The committed build record itself still states that remote publication was not performed at package-preparation time.

The manuscript source can be reviewed without this. Before any submission-quality archival claim, however, the repository should pin the actual remote native build and immutable product hashes to the reviewed source head, rather than relying on a local packaging record whose own text disclaims remote publication.

## 6. The central top-four significance question

Revision 77 has crossed an important internal threshold in the project: it is no longer merely a marked local smooth-germ inverse. It now contains a mathematically coherent route to whole-table Euclidean reconstruction on an explicit smooth class.

That is a significant improvement.

But the requested editorial threshold is not “is this broader than v76?” It is whether the result changes how a broad part of mathematics should think about inverse rigidity.

At present the theorem says, roughly:

> given a table-dependent finite marked atlas of regular branches, exact branch-resolved scalar endpoint laws at three clocks remove an unknown common weight, thereby recovering exact generating actions; paired branch extensions recover exact final-flight distances; enough such distance kernels reconstruct and register the table.

This is a strong piece of inverse engineering. The part I find insufficiently developed for a top general journal is the **information theorem**. Why are these records a natural minimal or near-minimal data object? Which exact marks can be removed? Why is three clocks the true physical threshold rather than a feature of the algebraic nuisance model? Can the atlas be found without already knowing substantial geometry? What is the relationship, in a precise order-theoretic sense, between these records and lens/travel-time or marked-length data?

If those questions were answered sharply, the present proof chain could become the mechanism supporting a much stronger conceptual result. Without them, the global theorem remains highly tailored to an experiment designed around the unknown object.

## 7. What would change my placement assessment

For renewed consideration at the requested level, I would want a revision that changes the **nature of the data theorem**, not merely adds more verification, more historical material, or more quantitative constants. Any one of the following directions could potentially do that if carried through strongly enough:

1. **Canonical or table-independent acquisition.** Give one fixed natural observation map, or a universal adaptive scheme with a proved finite stopping rule, on a substantial class. The object-dependent existence of an identifying atlas would then become a lemma rather than the endpoint.

2. **Remove a major exact mark.** Recover branch identity, lift identity, overlap registration, or clock/gate selection from the statistical observations themselves. A finite ambiguity theorem would already be meaningful if exact recovery is too strong.

3. **Prove a sharp information threshold.** Establish within an actual billiard class that two-clock data are nonidentifying while three-clock data are identifying, rather than demonstrating only an unrestricted weighted-function gauge freedom.

4. **Give a theorem-level comparison with lens or marked-length data.** Prove that the statistical records are strictly coarser in a precise sense, or identify a natural family on which they determine the table while the competing data structure is genuinely unavailable or stronger.

5. **Quantify finite-atlas complexity on a natural class.** Bound the number of branches, maximal flight length, gate sizes, rank margins, and conditioning in terms of geometric class parameters. This would turn qualitative finite identifiability into a robust global theorem.

6. **Extract a genuinely general principle.** Formulate the statistical-action-to-geometry mechanism for a wider class of twist/generating-function systems and prove at least one substantial application outside planar dispersing billiards.

7. **Unify or split the article.** Either prove one theorem that conceptually contains both the finite-action global inverse and the periodic asymptotic smooth inverse, or submit the new global theorem as a focused article. The present two-paper concatenation obscures rather than strengthens the placement case.

## 8. Minor and editorial comments

1. The title should reflect that the global theorem uses **branch-resolved / marked** records. “Statistical action recovery” alone may suggest a less labelled experiment than is actually assumed.
2. The principal abstract should not simply concatenate the new v77 abstract with the old v76 abstract. Write one abstract with one hierarchy of results and one central claim.
3. The second full “Introduction” inside the principal paper should be eliminated if the article remains unified. It is evidence that the second part is still a separate manuscript.
4. The 390-page full technical manuscript is valuable as an archive but should not be presented as the primary journal article. A referee should not be asked to infer novelty by traversing the whole historical programme.
5. State the shared-weight and alpha-independence hypotheses prominently in the first theorem-level description of the experiment. They are the exact reason the three-clock nuisance cancellation works.
6. Likewise state exact branch labels and lift labels in the abstract or opening theorem summary. The manuscript itself proves that branch mixtures are not resolved.
7. The finite-atlas theorem should distinguish more visibly between existence of clocks from coarse brackets and an observer's ability to obtain those brackets. At present the proof is honest, but a casual reader may miss the distinction.
8. In the distance-certificate section, emphasize that the nonconic hypothesis is only a sufficient certificate and not believed necessary; the text already says this, but it matters for the scope of the whole-table class.
9. The determinant bridge should cite the precise inherited estimates at each rate in the final journal version, preferably in a compact dependency table or lemma chain.
10. Keep the distinction between repository diagnostics and proof verification. The current verification files handle this responsibly.
11. Once a remote native build exists for the exact reviewed source head, record its workflow run, immutable source tree, PDF hashes, and product branch in one source-pinned provenance file.
12. The citations to author-requested AI-assisted referee memoranda are unusually prominent inside the article. Attribution is appropriate, but the final journal manuscript should avoid giving internal review history the visual weight of primary mathematical literature unless a particular mathematical contribution genuinely requires citation.

## 9. Final assessment

Revision 77 is the strongest version of this A2 line I have reviewed. It contains a genuine new theorem and a serious response to the v76 report. The authors have moved from a local marked-germ inverse to a whole-table reconstruction mechanism, and they have supplied the concrete determinant instantiation previously requested. I do not find a simple mathematical failure that would justify dismissing the new proof chain.

Nevertheless, **I would reject the manuscript for the requested Annals/Inventiones/Acta/JAMS-level placement in its present form.** The decisive remaining issue is not technical completeness but conceptual naturality and information content. The global inverse is proved after choosing a rich table-dependent marked experiment, and the exact statistical records are then inverted to full action functions. The manuscript has not yet shown that this data model constitutes a sharp, natural, or genuinely weaker global rigidity datum relative to the neighboring literature, nor has it extracted from the proof a broad inverse principle with consequences beyond this setting.

For a strong specialist journal, after substantial compression and clarification of the data model, I would view the new finite-action theorem as a serious result deserving careful consideration. For one of the four leading general journals, I would require a further theorem-level advance of the kind listed above rather than another round of source-preservation, numerical, or packaging refinement.

**Recommendation:** reject for the requested top-general-journal placement in the present form; mathematical core worthy of further development and possible resubmission only after a substantive change in the data theorem or a genuinely broader conceptual theorem.