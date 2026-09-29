# External top-four referee report on A2 v22

**Manuscript:** Qian Qi, *Reference-free certification from intrinsic boundary laws*  
**Reviewed revision:** `revision/a2-v22-reference-free-certified-recovery-2026-09-29`  
**Equivalent source alias:** `revision/a2-v22-referee-copy-2026-09-29`  
**Reviewed commit:** `ef51836da1744fc4a7133e3a3fd0e85848c73dc6`  
**Reviewed tree:** `cca7d5a3c6fb4028982e92f8c9a84d145ed302d3`  
**Mathematical checkpoint:** `3c6c6d6667d9a0506dc3de472498f21a4cb550d1`  
**Manuscript directory:** `papers/A2-v22-reference-free-certified-recovery`  
**Date:** 29 September 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 22 is a genuine and substantial revision. It closes the two most concrete structural objections in the v21 report. First, it gives an exact, false-positive-free certificate that a finite collection of genuine local records has seen every obstacle orbit and generated the full period lattice. Second, it removes the known reference table and retained witness from the noisy theorem: body types are clustered from the recovered shapes, the cycle subgroup is reconstructed arithmetically before any area calibration, and the completion defect is then tested with a uniform gap.

The new exact identity

\[
\mathcal D=\operatorname{covol}\Gamma-A-\sum_{i\in I}\operatorname{area}(C_i)
 =([\Lambda:\Gamma]-1)\operatorname{covol}\Lambda
   +\sum_{i\notin I}\operatorname{area}(C_i)
\]

is simple, effective, and well chosen. It converts two logically different omissions—unseen obstacle types and an unsaturated period subgroup—into one nonnegative observable defect. The reference-free noisy arithmetic is also a real advance: bounded cycle vectors and a covolume lower bound yield a finite denominator bound, rational separation recovers the exact cycle coordinates, and Hermite reduction recovers the subgroup before the area test is invoked.

On the v22 core audited in detail, I found no fatal counterexample to the completion identity, the exact assembly, the bounded-denominator argument, the noisy defect gap, the histogram reconstruction bound, or the hidden-area testing calculation. The accompanying independent exact checks support the displayed finite arithmetic. I therefore do **not** base the negative recommendation on a known false central theorem.

The negative recommendation is a top-four editorial judgment. The theorem still starts from an unusually rich and purpose-built observation: for each selected return branch it uses two complete two-dimensional endpoint-arclength densities with the absolute Liouville normalization of the whole periodic cell. That normalization is precisely what exposes the free area of bodies that have not been observed. The certificate decides whether a supplied finite list of genuine records is collectively complete; it does not itself produce those records. Exact exhaustive enumeration is formal and non-algorithmic, while the noisy theorem remains conditional on a fixed finite scanner/list containing a covering rank-two component and on strong analytic, separation, asymmetry, area, covolume, and local-branch margins.

Thus v22 proves a serious reference-free **completion certificate and conditional inverse theorem** for a richly marked local-scattering experiment. It does not yet prove whole-table rigidity or stable acquisition from a standard unmarked billiard invariant, solve the exact analytic count-only problem, or provide a noisy discovery theorem over an unknown growing record catalogue. In my judgment the result could support a strong specialist-journal submission after a full proof review and completed exact-source qualification, but it does not reach the exceptional conceptual threshold of the four journals named above. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

The two v22 revision aliases named above resolve to the same author head

`ef51836da1744fc4a7133e3a3fd0e85848c73dc6`

with repository tree

`cca7d5a3c6fb4028982e92f8c9a84d145ed302d3`.

The head has parent `3c6c6d6667d9a0506dc3de472498f21a4cb550d1`, the mathematical checkpoint. The latest frozen external report used by the author is the v21 report at

`b263abc35b2aacb038185d66c5cb13f488d3fe93`,

which reviewed author commit

`5ab3be483386dab1b2f53575f47dbf7aebd92bd3`.

The exact reviewed v21 paper tree is preserved under

`papers/A2-v22-reference-free-certified-recovery/retained/v21`

with tree `a13f1cabd3bc11214bc92ecb6fb49ea51fde87bb`. The older complete supplement is retained at tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`.

The present review branch starts directly from the v22 author head and adds files only below

`reviews/a2-v22-external-harsh-top4-rereview-2026-09-29/`.

No manuscript source, author revision branch, previous report, or unrelated paper is modified by this review.

The principal current mathematical inputs are:

- `core/01_setting.tex`;
- `core/02_local.tex`;
- `core/03_completeness.tex`;
- `core/04_reference_free.tex`;
- `core/05_statistics.tex`;
- `core/06_acquisition_comparison.tex`.

I also inspected the response, source pins, publication binding, proof/history/literature ledgers, validation tools, local receipt, exact-SHA workflow, and the frozen v21 report.

## 3. Information category and theorem summary

A record is attached to one selected isolated clear normal channel and one three-impact return branch. At two absolute times, the observation records the complete endpoint-arclength subprobability densities on a strictly active rectangle. Failure and successful endpoints outside the rectangle remain outcomes. One coherent simultaneous reversal of the two endpoint signs is allowed within a record, but no cross-record origins or signs are supplied.

The records use the same absolute normalized phase measure

\[
\frac{dq\,d\vartheta}{2\pi A},
\]

where `A` is the free area of the full periodic cell, including bodies that may never appear in the selected records. This is essential to the completion theorem. Conditional-on-success laws or aperture-renormalized laws would erase the absolute factor that carries the hidden-area information.

For one record the retained local inverse gives

\[
W=\frac{T_1f_2-T_2f_1}{f_2-f_1},
\qquad
A=\frac{(T_2-T_1)(-W_{st})}{2\pi(f_2-f_1)}.
\]

The action and its diagonal derivatives recover the two reflecting arcs in their relative placement. Analytic continuation recovers each complete obstacle image.

For a connected observed component, congruence of recovered complete images identifies visible obstacle types. A spanning tree places representatives; non-tree edges yield physical cycle displacement vectors. Their integer span is a subgroup `Gamma` of the true period lattice `Lambda`. If `I` is the set of visible types and `S_I` their total area, the completion theorem tests

\[
\mathcal D=\operatorname{covol}\Gamma-A-S_I.
\]

The noisy theorem first reconstructs type clusters and approximate cycle vectors, then recovers the exact rational cycle coordinates and subgroup, and only then evaluates an estimated defect. On acceptance it returns a whole-table reconstruction with conditional error `C e^theta`.

The finite-histogram theorem estimates each record's two densities in `C^2`, applies the reference-free certificate, and obtains the conditional whole-table upper bound

\[
C\left\{\frac{\log(CJN/\delta)}{N}\right\}^{\beta\theta/(2\beta+6)}.
\]

A separate fixed-window subexperiment proves that detecting a hidden obstacle of area `a` has the sharp two-point scale `a` of order `N^{-1/2}`. This lower bound is not a minimax theorem for reconstruction of the entire table.

## 4. Correctness audit of the exact certificate

### 4.1 Absolute normalization and the local area

On a strictly active endpoint rectangle, the density is affine in the absolute observation time:

\[
f_T(s,t)=\frac{-W_{st}(s,t)}{2\pi A}\{T-W(s,t)\}.
\]

The two-time quotient eliminates the common flux factor and recovers `W`; differentiating it recovers `-W_st`, and comparison with `f_{T_2}-f_{T_1}` recovers `A`. This is the same local mechanism already audited in the earlier full-law version. Version 22 uses its absolute normalization globally rather than recalibrating a candidate cell after coverage is presumed.

The observational contract is strong but mathematically coherent: the same normalized phase preparation is used for all records, and no record is conditioned on success. Under that contract the recovered `A` is the actual free area of the full quotient, not the free area of a guessed visible subsystem.

### 4.2 Defect identity

Every cycle displacement obtained from a physical periodic table lies in `Lambda`, so `Gamma` is a subgroup of `Lambda`. If it has rank two, then

\[
\operatorname{covol}\Gamma=[\Lambda:\Gamma]\operatorname{covol}\Lambda.
\]

The cell area identity gives

\[
A=\operatorname{covol}\Lambda-
       \sum_{i=1}^r\operatorname{area}(C_i).
\]

Substituting this and separating visible from invisible types gives the displayed defect formula. Every term on the right is nonnegative. It vanishes precisely when the subgroup index is one and no positive-area type is invisible.

Repetition of records does not alter `S_I`, because one representative is counted per recovered congruence type. Surplus edges enlarge neither the hidden-area term nor the subgroup index in a way that could make a positive defect vanish. Rank-deficient components are rejected before a covolume is assigned. I found no false-positive configuration within the stated asymmetric shape-separated physical class.

### 4.3 Exact assembly and genericity assumptions

For asymmetric pairwise noncongruent obstacle types, equality of complete recovered images identifies vertices and gives a unique Euclidean match at every tree step. The edge's partner image is carried by the same motion. A non-tree edge then compares two copies of the same compact body and determines a unique translation vector. This is a valid unregistered assembly mechanism.

The hypotheses are substantial. Pairwise shape separation excludes repeated congruent types, while asymmetry excludes nontrivial rotations and reflections. They are not merely technical regularity assumptions: they are the mechanism that turns independent record frames into one global incidence graph. Version 22 states this honestly and does not claim the same reference-free result for symmetric or shape-repeated tables.

### 4.4 Exact stopping by enumeration

If all genuine finite records are available, one can enumerate finite subsets, reconstruct every connected component, and stop at the first zero-defect full-rank component. The exact certificate makes this stopping rule sound: acceptance cannot occur before both type coverage and lattice saturation.

This is an exact existence/stopping statement, not a finite-time acquisition theorem. The collection of all genuine records is not presented as an effectively enumerable sensor output with a complexity bound. That distinction is central to the remaining editorial objection.

## 5. Correctness audit of reference-free noisy arithmetic

### 5.1 Type clustering and cycle-vector stability

Uniform analytic continuation turns a `C^2` density error `e` into a complete-image support error `Delta=C e^theta`. The fixed pairwise shape gap `zeta` separates same-type from different-type recovered images, so threshold clustering identifies the visible type incidence without a known catalogue. The rotation/reflection margins control the placement maps along a data-selected spanning tree.

The argument is uniform over repeated and surplus edges because every record is retained as a multigraph edge. Distinct channel orbits need not be classified or deduplicated. This is a material improvement over a theorem formulated in neighborhoods of preselected witness keys.

### 5.2 Bounded-denominator reconstruction

The manuscript bounds every physical cycle vector by

\[
B_0=(2r_0-1)(R+2D_0).
\]

For an independent pair `D`, its determinant is an integer multiple of the true lattice covolume and lies between the lower covolume bound `V_0` and `B_0^2`. Hence

\[
n_D=\frac{|\det D|}{\operatorname{covol}\Lambda}
\]

is an integer at most

\[
Q=\max\{1,\lceil B_0^2/V_0\rceil\}.
\]

Every coordinate of every cycle vector in the basis `D` lies in `n_D^{-1} Z`. Distinct reduced rationals with denominators at most `Q` are separated by at least `Q^{-2}`. Once the continuous displacement error is below the stated class-dependent threshold, finite rational search recovers all coordinates exactly.

Taking their common denominator and the integer column group, followed by Hermite reduction, recovers a subgroup basis without using `A+S_I`. This order of operations is important: it avoids the v21 circularity in which candidate covolume was calibrated from an area equation before coverage had been established.

I independently checked the determinantal-index, rational-coordinate, common-denominator, and unimodular-invariance identities on exact random integer grids. I found no arithmetic defect in the stated two-dimensional argument.

### 5.3 Noisy defect gap

On the uniform class, an incomplete rank-two component has defect at least

\[
g_0=\min\{V_0,a_0\}.
\]

If the period subgroup is proper, its index contributes at least one true cell covolume, hence at least `V_0`. If a type is unseen, its area contributes at least `a_0`. The support-area functional is locally Lipschitz on the bounded `C^1` class, and the recovered subgroup covolume is stable after exact rational decoding. Therefore the estimated defect differs by `O(Delta)`.

Reducing the accuracy threshold until this error is below `g_0/4` makes the acceptance rule

\[
|\widehat{\mathcal D}|<g_0/2
\]

uniformly sound and complete on the class. Deleting arbitrary records cannot create a false positive, because the exact defect identity applies to every remaining physical component. A rejected component is correctly interpreted as a noncertificate rather than as proof that no table exists.

## 6. Statistical audit

### 6.1 Density estimation

For a `C^{2,\beta}` density, tensor cell averages and local quadratic reconstruction give the deterministic error decomposition

\[
e_N(h)=C\{h^\beta+\sqrt{r_N}\,h^{-3}+r_N h^{-4}\},
\qquad
r_N=\frac{\log(CJN/\delta)}{N}.
\]

The first term is the second-derivative bias. The square-root term comes from the multinomial cell fluctuations divided by cell area and differentiated twice. The linear Bernstein term is of smaller order at the selected bandwidth. Choosing

\[
h=r_N^{1/(2\beta+6)}
\]

balances the first two terms and yields

\[
e_N\le C r_N^{\beta/(2\beta+6)}.
\]

Conditional analytic continuation then raises this to the power `theta`. The rate algebra is correct in its stated model. One sample at a histogram time is a multinomial endpoint outcome and supplies all cell indicators simultaneously; the cell count affects the logarithm and data dimension, not a multiplicative `h^{-2}` preparation factor.

### 6.2 Fixed list versus acquisition

The finite theorem starts with a fixed finite list of genuine record branches. Soundness does not assume coverage, and an incomplete list cannot falsely certify. Consistency, however, is conditional on the list containing a connected covering component with full lattice rank and on the stipulated local physical margins.

This is not a noisy discovery theorem for an unknown or growing catalogue. It does not show how an observer, without geometric access to the table, generates a list guaranteed to contain all necessary clear normal channels. The retained canonical scanner supplies such lists only under its own geometric-access and persistence assumptions. Version 22 correctly separates these statements, but the separation also identifies the remaining acquisition gap.

### 6.3 Hidden-area testing

In the fixed-window subexperiment, adding a hidden body of area `a` changes every selected probability through the common normalization factor `1/A`. On a compact margin, the probability difference is linear in `a`. Bernoulli KL divergence is therefore `O(a^2)` per preparation, so the entropy chain rule gives the lower scale `a` of order `N^{-1/2}`. A fixed active window gives the matching test.

This is a clean local decision result. It is not a minimax lower bound for finding every obstacle, selecting all records, reconstructing all boundaries, or estimating the whole period lattice. The manuscript generally preserves this distinction and should continue to do so in every summary.

## 7. What v22 successfully resolves from the v21 report

The revision deserves explicit credit for closing the following concrete objections.

1. **Omission safety.** Coverage and lattice saturation are no longer assumptions hidden inside the acceptance rule. A positive defect or rank failure is a noncertificate; zero defect is equivalent to completeness on the exact class.
2. **Unknown visible catalogue.** No reference table or supplied body-shape catalogue is used for noisy type clustering.
3. **No retained witness.** The robust theorem no longer assumes that one preidentified covering witness survives a deletion or perturbation.
4. **No premature area calibration.** Discrete cycle arithmetic is recovered from bounded-denominator separation before the area identity is used.
5. **Reference-free period recovery.** The subgroup and a period basis are reconstructed from the recovered cycle vectors rather than from integer labels supplied with each edge.
6. **Exact/noisy/acquisition separation.** The paper now distinguishes a certificate, exact exhaustive stopping, and a fixed-scanner finite experiment.
7. **Closest literature category.** The primary text and literature audit now compare the local density/action inverse with boundary/lens and obstacle travel-time inverse problems, rather than only with marked-length rigidity.
8. **Delivery discipline.** Source pins, publication binding, a primary local receipt, and an exact-triggering-SHA all-volume workflow are present and make fewer unsupported verification claims than earlier revisions.

These are substantive mathematical and expository improvements.

## 8. Remaining top-four objections

### 8.1 A certificate is not an acquisition theorem

The strongest new global statement answers:

> Given a finite collection of genuine local records, can the data themselves certify that the collection is complete?

Version 22 answers this question positively under its generic physical assumptions. It does not answer:

> From a standard observer with no prior geometric access, how are all required genuine records found in finite noisy time?

Exact enumeration over all records is formal. The noisy theorem is for a fixed finite list or for the retained scanner under separate access assumptions. The certificate makes stopping safe once a complete component appears, but it does not ensure appearance. At the requested editorial level, this distinction is decisive.

### 8.2 The sensor remains tailored and information-rich

Each record consists of two full endpoint-density functions, or two increasingly fine two-dimensional histograms. It records intrinsic endpoint locations, an itinerary branch, local origins, paired-record identity, and absolute times. Most importantly, all records share the absolute Liouville normalization of the entire cell.

This is a geometrically legitimate marked scattering law, but it is far richer than counts, ordinary marked lengths, or an unmarked trajectory spectrum. The hidden-area certificate works because the preparation measure already carries the total free area. The result should not be presented as if omissions were detected from local shapes alone.

### 8.3 Strong global priors remain essential

The uniform theorem assumes, among other conditions:

- an upper bound on the number of obstacle types;
- positive lower bounds for free area, cell covolume, and every obstacle area;
- pairwise shape separation;
- quantitative exclusion of rotations and reflections;
- common analytic-strip and local graph bounds;
- curvature, separation, channel-clearance, active-rectangle, twist, time-separation, and non-grazing margins;
- bounded lattice bases and inverses;
- a compact physical model class.

These assumptions permit an infinite-dimensional analytic class, but they exclude symmetric tables, repeated congruent types, degenerating lattices, and weakly separated channels. “Reference-free” is therefore not “prior-free” or “uniform on all analytic dispersing tables.”

### 8.4 The global mechanism is still assembly after a rich local inverse

Two endpoint densities recover the complete local action by affine elimination. The action recovers boundary arcs; analyticity recovers complete images. Once complete asymmetric noncongruent images are known, the global steps are shape matching, finite graph placement, discrete subgroup recovery, and area bookkeeping.

The completion identity is elegant, but the overall result remains conceptually closer to a marked lens/scattering reconstruction with a consistency certificate than to a new rigidity theorem from a conventional dynamical spectrum. The revised literature comparison makes this clearer rather than eliminating the editorial issue.

### 8.5 No whole-table minimax theorem

The paper proves a conditional upper rate for one finite marked histogram experiment and a sharp lower scale for a hidden-area two-point subexperiment. It does not prove that the whole-table exponent is optimal, characterize the minimax difficulty of record discovery, or give a matching lower bound for analytic continuation, shape synchronization, and lattice reconstruction.

### 8.6 Natural unresolved problems remain outside the theorem

The revision does not settle exact analytic count-only rigidity or nonrigidity, remove the endpoint sensor, recover an unmarked catalogue of trajectories, treat congruent repeated shapes without registration, or derive the period group from an ordinary marked-length invariant. The paper says so. These are not correctness objections, but they delimit its conceptual reach.

### 8.7 Algorithmic status

The rational subgroup stage is finite and can use standard Hermite/Smith methods. The difficult continuous stages are countable-dense near-minimizers over compact analytic physical classes, exact enumeration of records, conditional analytic continuation, and congruence matching. No polynomial-time or practically implementable whole-table algorithm is proved.

This is acceptable for a pure existence theorem, but the language of “certificate package” and “reference-free recovery” should not suggest a computational inverse beyond what is established.

### 8.8 Submission architecture and qualification

The new primary is concise relative to earlier A2 manuscripts, but the submission still preserves and relies on a large nested chain of earlier volumes. An editor must assess the 17-page v22 primary together with the retained v21/v18 material and the complete smooth-law supplement.

The exact-SHA workflow is well designed, but at the final review check its run was still queued. The only completed receipt in the repository is a source-content, primary-only local execution rather than an authenticated Git checkout or an all-volume hosted pass. This is a reproducibility limitation, not the basis of the mathematical rejection.

## 9. Corrections required for any resubmission

1. **State in the abstract that the certificate does not acquire records.** Say explicitly that the exact stopping rule ranges over genuine records and that the finite noisy theorem begins with a fixed finite genuine list or a separately justified scanner.
2. **Distinguish reference-free from prior-free.** List the obstacle-count bound, area/covolume gaps, shape/asymmetry margins, analytic strip, and local physical margins wherever the uniform theorem is summarized.
3. **Make the absolute normalization operational.** Explain precisely what physical preparation supplies the common cell-normalized Liouville law when the primitive cell and its full obstacle content are themselves unknown.
4. **Separate the three statistical statements.** Do not merge the conditional whole-table upper bound, the hidden-area `N^{-1/2}` decision scale, and scanner persistence into one “sharp recovery rate.”
5. **Keep failure closed.** A rejected component is only a noncertificate; it is not evidence that the table is incomplete or that another component cannot certify.
6. **Formalize catalogue complexity.** State whether exact record enumeration is countable, effective, or merely existential, and give no algorithmic implication beyond the finite arithmetic stage.
7. **Preserve the travel-time/lens comparison in the article.** The focused audit is useful, but the theorem-level comparison belongs in the mathematical narrative, not only in repository metadata.
8. **Close the hosted qualification.** Record the exact-head all-volume workflow conclusion and artifact hashes, or report the failure without substituting the local primary receipt.
9. **Consider splitting the programme.** The completion certificate and reference-free arithmetic form a coherent paper; the historical moment inverse, count fibers, relative-law theory, and auxiliary statistical experiments may be better treated as separate companion work.

These changes would improve a specialist-journal submission. They would not, without a broader acquisition or natural-invariant theorem, change my top-four recommendation.

## 10. Literature assessment

The revised literature audit now includes the closest information categories:

- local and global boundary/lens rigidity under convexity and foliation assumptions;
- obstacle travel-time/scattering rigidity;
- marked-length rigidity for dispersing billiards;
- quantitative instability of analytic continuation;
- Hermite and Smith normal-form algorithms for the integer stage.

None of the inspected sources obviously contains the exact combination of a two-density intrinsic local inverse, the missing-area/period-index defect, and reference-free subgroup certification. Conversely, the rich endpoint law and its affine recovery of the action place the local theorem within a well-established inverse travel-time/lens paradigm. The principal new contribution is therefore the specific billiard realization and the global completion certificate, not a new general principle that two boundary travel-time functions encode local geometry.

I did not perform an exhaustive priority search. The accompanying literature audit records the sources and precise scope used in this report.

## 11. Reproducibility and independent diagnostics

The author records a source-content local execution containing:

- 5,110 new finite checks;
- 3,635 selected retained local checks;
- 90 nonlinear curvature comparisons within the retained subset;
- identical normal and optimized diagnostic output;
- a warning-free 17-page primary build.

The receipt explicitly says `source_content_not_git_checkout`, `primary_only`, and `formal_proof_certificate: false`. It is not an exact-commit all-volume pass.

The exact-triggering-SHA workflow is present and invokes the checkout-bound validator on the primary plus four retained entry documents. At finalization of this report, workflow run `36541269616` for the reviewed head remained `queued`, with no conclusion.

The accompanying `verify_review.py` imports no author verification code. In exact rational arithmetic it performs 30,544 checks of:

- the completion identity, nonnegativity, and zero criterion;
- cycle-group determinantal indices;
- rational coordinates and common denominator bounds;
- invariance under unimodular pair changes;
- bounded-denominator rational separation;
- the hidden-area signal and its inversion;
- the Bernoulli-KL quadratic envelope;
- the histogram bias/variance balance.

Normal and optimized Python executions produced identical output. These diagnostics support only the finite displayed arithmetic. They do not certify analytic continuation, physical record production, global compactness, source preservation, statistical measurability, or the full proof chain.

I did not independently complete a TeX build or re-prove every retained theorem in the multi-volume programme.

## 12. Final verdict

**Response to the v21 report:** substantively successful on its main concrete objections. The paper now has a genuine omission-safe exact certificate and a noisy reference-free subgroup/defect test that does not presuppose the desired witness or calibrate the lattice from an unproved coverage identity.

**Correctness:** no fatal counterexample found in the new v22 core. The exact defect, denominator separation, subgroup recovery, robust acceptance gap, and hidden-area testing algebra survived independent exact diagnostics. The principal remaining issues are information category, acquisition, global priors, architecture, and incomplete hosted qualification—not an identified false central formula.

**Significance:** the theorem certifies and reconstructs an analytic asymmetric shape-separated periodic table from a finite collection of rich, absolutely normalized endpoint-density records. It does not generate that complete record collection from a standard observer, remove the strong uniform priors, or derive whole-table rigidity from a conventional unmarked dynamical invariant.

**Recommendation: reject at the requested Annals/Acta/Inventiones/JAMS benchmark.** The completion certificate and reference-free arithmetic could form a serious strong-specialist-journal paper after fresh independent proof review, source-bound full-package qualification, and substantial restructuring.