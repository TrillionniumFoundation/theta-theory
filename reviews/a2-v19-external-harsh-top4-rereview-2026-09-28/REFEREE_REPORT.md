# External top-four referee report on A2 v19

**Manuscript:** Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v19-intrinsic-network-descent-2026-09-28`  
**Equivalent source alias:** `revision/a2-v19-referee-copy-2026-09-28`  
**Reviewed commit:** `2f51ac5a2ab72deceb21c23084ca3062056edb4c`  
**Reviewed tree:** `bb540dea1085da7ff4e7fcfcbca36be282b77a1f`  
**Paper directory:** `papers/A2-v19-intrinsic-network-descent`  
**Date:** 28 September 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or a formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 19 is a genuine and substantial revision. It directly addresses the strongest objections in the v18 report. The primary article is now focused, the local observation is explicitly identified with local lens/scattering information plus a volume normalization, and the global theorem no longer assumes obstacle identities, a supplied incidence graph, cross-channel contact registration, relative edge signs, or integer lattice-copy labels on the stated generic class. The recovered free area and obstacle images determine the lattice covolume; geometric cycle displacements then determine a finite arithmetic list of possible period lattices. The primitive case gives whole-table uniqueness, while a prime-index construction proves that the remaining finite ambiguity is real rather than a proof artifact.

On the new v19 core audited in detail, I found no fatal counterexample. The local quotient and curvature formulas retain the sound scope identified in the v18 review. The shape-based incidence reconstruction, covolume identity, finite-index lattice classification, primitive uniqueness criterion, prime-index physical ambiguity, variance-aware histogram estimate, and integer-locking argument are internally coherent under their stated hypotheses. Independent exact-rational diagnostics accompanying this report support the displayed finite algebra and combinatorics.

The negative verdict is therefore an editorial and conceptual judgment, not a claim that v19 is false or cosmetic. The observation remains a selected, function-valued local scattering law: every record contains two full endpoint-density functions, a marked contact origin, a selected three-impact itinerary, and a within-record grouping. Exact whole-image recovery uses analyticity. Incidence recovery uses pairwise noncongruence and asymmetry. Unique global reconstruction additionally uses connected coverage and a primitive recovered cycle pair. The finite-data theorem assumes a compact uniformly analytic class, onset brackets, quantitative symmetry and shape-separation margins, and bounded geometry. Once complete obstacle images and real cycle displacements are recovered, the new global step is a clean but largely elementary combination of shape matching, area bookkeeping, finite-index lattice theory, and compactness.

This is serious mathematics and, after a fresh full proof review and completed exact-source qualification, could be a strong specialist-journal paper. In my judgment it still does not reach the exceptional naturality, breadth, or conceptual force expected at the four journals named above. I would not recommend another open-ended revision cycle at that benchmark.

## 2. Frozen source and chronology

The latest A2 source is the v19 author commit

`2f51ac5a2ab72deceb21c23084ca3062056edb4c`

with repository tree

`bb540dea1085da7ff4e7fcfcbca36be282b77a1f`.

Both v19 revision aliases resolve to that commit. Its parent is the frozen v18 review commit

`e727a7ac9b73b6928ecc194d74628125159d49cf`.

Thus v19 is based directly on the latest external report rather than on an unreviewed side branch. No later `revision/a2-v20...` branch was present when this review branch was created.

The new primary article consists of five active core files:

- `core/01_setting.tex`;
- `core/02_local.tex`;
- `core/03_descent.tex`;
- `core/04_stability.tex`;
- `core/05_comparison.tex`.

The complete reviewed v18 paper is retained as Supplement R at `retained/v18`, with native tree `3c558d7799e9e49812e7bab98320d3a98e7f7418`. The complete earlier smooth-theory supplement is retained at `complete`, tree `14b2e5379e5b223bc0bdc823c97fd77c2dca2cda`. I treated those preserved volumes as retained mathematical claims, but concentrated the new audit on the v19 primary and the dependencies it invokes.

The present review branch was created directly from the author commit and adds files only under

`reviews/a2-v19-external-harsh-top4-rereview-2026-09-28/`.

No author source, revision branch, previous review, or unrelated paper is modified.

## 3. What v19 substantively fixes

### 3.1 The nearest information category is now stated correctly

Proposition 2.2 proves that, on a fixed strictly active physical rectangle, the two endpoint densities at known absolute times are equivalent to the stationary action `W` together with the normalization `A`. The positive twist then gives the local canonical scattering graph

\[
(s,-W_s(s,t))\longmapsto(t,W_t(s,t)).
\]

Conversely, that graph, one action value, and `A` recover the densities. This is the right information statement. It makes clear that the affine two-time elimination is elementary and that the data are local lens/scattering data in intrinsic boundary coordinates, not “two scalar windows.”

The new comparison with Stefanov–Uhlmann–Vasy, Gurfinkel–Noakes–Stoyanov, Noakes–Stoyanov, Santaló-type volume identities, and marked-length rigidity is materially better than the v18 discussion. The manuscript distinguishes identified-boundary metric recovery and exterior scattering data from the present problem of two unknown reflecting arcs. It no longer presents travel-time differentiation or the passage to a canonical relation as an isolated new principle.

This closes the closest-literature objection from the v18 report.

### 3.2 Incidence is recovered rather than supplied

For analytic, asymmetric, pairwise noncongruent obstacle representatives, each local record reconstructs two complete boundary images in relative placement. Partitioning all image occurrences by Euclidean congruence recovers the obstacle classes. The two slots in every record then recover the incidence multigraph, including loops and repeated edges.

Asymmetry makes the Euclidean map from one occurrence of a shape to another unique. A spanning-tree induction therefore places one representative of each recovered class. Independent simultaneous reflections of the local records cancel through this unique matching. A non-tree record then supplies a real translation vector between its reconstructed target and the already placed target representative.

This is a genuine information reduction from v18. It is not merely a relabelling of previously supplied registration.

### 3.3 The normalization produces a finite lattice problem

Each local density pair recovers the same free area `A`. The complete recovered images determine one obstacle area per incidence class. Hence

\[
V=A+\sum_i \operatorname{area}(C_i)=\operatorname{covol}\Lambda .
\]

Two independent non-tree displacement vectors form a matrix `D`. Since `D Z^2` is a sublattice of the unknown period lattice,

\[
n=\frac{|\det D|}{V}
\]

is a positive integer. Normalizing by `D`, dualizing, and using row Hermite normal form gives the finite list

\[
\Lambda_B=D B^{-1}\mathbb Z^2,\qquad
B=\begin{pmatrix}a&b\\0&d\end{pmatrix},\quad
ad=n,\quad 0\le b<d.
\]

The number of algebraic candidates is the divisor sum `sigma_1(n)`. Additional cycle and physical constraints only delete candidates. When `n=1`, the recovered cycle subgroup is already the full period lattice.

The lattice argument is correct, subject to the row/column convention being kept explicit. It converts the previously supplied integer copy labels into an inferred finite arithmetic ambiguity.

### 3.4 The ambiguity theorem is physical and exact

For every odd prime `p`, the manuscript constructs `p-1` distinct superlattices

\[
\Lambda_j=\mathbb Z d_1+\mathbb Z d_2+
          \mathbb Z\frac{d_1+j d_2}{p}
\]

with common covolume and the same two selected axial channel laws. The modular argument excludes intermediate centers on either selected axis, while large periods give a common clearance margin. The obstacle is chosen asymmetric, so an isometry cannot identify distinct period groups.

This is equality of exact physical density functions, not merely a formal or finite-jet ambiguity. It convincingly shows that rank-two geometric cycle data and calibrated volume do not imply uniqueness at index greater than one.

### 3.5 The primary article and source binding are improved

The main argument is now a self-contained fifteen-page primary rather than another cumulative one-hundred-page revision. The prior article and the smooth theory are retained as identified supplementary volumes instead of being silently deleted.

The revision includes source pins, a publication binding, a dedicated validator, a read-only exact-triggering-SHA workflow, and a local receipt. The local source-content execution records 43,864 diagnostics, identical normal and optimized output, and a warning-free fifteen-page primary build. It correctly does not relabel that execution as an authenticated Git checkout or a hosted full-package pass.

These are meaningful source-delivery repairs, although the hosted run remained incomplete at the time of this report.

## 4. Correctness audit of the new global theorem

### 4.1 Exact incidence recovery

The analytic continuation step is logically separated from the smooth local inverse. A recovered open arc determines the complete analytic boundary by the identity theorem in normal-angle support coordinates. No equality of smooth Taylor series is substituted for equality of smooth functions.

On the shape-separated class, congruence classes of complete images correspond exactly to obstacle orbits. Coverage ensures that every physical representative appears. The theorem does not claim to infer an unvisited obstacle.

Unique matching is correctly tied to trivial Euclidean symmetry. If one independently reflects a local pair realization, the unique map matching its source to the placed source is correspondingly composed with that reflection, leaving the placed partner unchanged. This removes the edgewise sign choices rather than hiding them.

A non-tree target image and the placed target representative differ by one translation in a physical table. A compact body has no nonzero translational symmetry, so this displacement is unique. I found no contradiction in the tree or cycle construction, including loops and repeated records.

### 4.2 Covolume recovery

The sum in

\[
V=A+\sum_i\operatorname{area}(C_i)
\]

is taken once per recovered congruence class, not once per image occurrence. This is exactly where pairwise noncongruence and the one-representative-per-orbit convention matter. Repeated observations do not multiply obstacle area. The support-function area formula is translation invariant.

The argument would fail on a collection with repeated congruent representatives unless additional multiplicity information were supplied. The manuscript excludes that case and retains older marked results for it.

### 4.3 Finite-index classification

The subgroup-area identity gives `[Lambda:D Z^2]=|det D|/V`. The duality reduction from an overlattice of `Z^2` to an index-`n` sublattice of `Z^2` is standard. The row-Hermite form with `ad=n` and `0<=b<d` gives exactly `sigma_1(n)` sublattices. The membership test for additional cycles is also correct.

For editorial clarity, a future version should write once and for all whether vectors are columns and whether `B` generates the dual sublattice by rows. The current formulas are consistent, but the proof moves between “row basis,” `B^{-1} Z^2`, and column matrices quickly enough to invite avoidable confusion.

### 4.4 Primitive uniqueness

If an independent recovered cycle pair has determinant equal to `V`, its subgroup has index one and is the full period lattice. The observer need not be told which pair is primitive: the finite recovered graph permits enumeration of trees and cycle pairs.

This is a sufficient certificate of uniqueness, not a conclusion that every connected covering collection contains a primitive pair. The distinction is present in the theorem and must remain prominent in summaries.

### 4.5 Stable discrete recovery

The finite experiment estimates cell probabilities in two active endpoint histograms per record. Since one phase preparation produces one multinomial outcome, the same sample supplies all cell indicators. Using `p_B=O(h^2)`, Bernstein's inequality gives cell error

\[
O\!\left(h\sqrt{r_N}+r_N\right),
\qquad
r_N=\frac{\log(CJN/\delta)}{N}.
\]

After the local quadratic cell reconstruction, the density error is

\[
e_N=O\!\left(h^\beta+\sqrt{r_N}h^{-3}+r_Nh^{-4}\right).
\]

Choosing `h=r_N^{1/(2 beta+6)}` balances the first two terms and makes the third smaller. Conditional analytic continuation contributes the exponent `theta`.

The shape-separation margin stabilizes the congruence partition; asymmetry stabilizes rotations and reflections. For two admissible physical candidates, the determinant/covolume ratios are integers. Once their real errors are below one half, the index locks. At index one, the corresponding cycle matrices are period bases. This is a valid comparison argument between physical candidates; it is not an unjustified rounding rule on arbitrary noisy vectors.

The estimator is an admissible approximate minimizer over a compact physical prior. It is measurable but not computationally constructive. The theorem says so.

## 5. Qualifications and corrections required for any resubmission

### 5.1 “Unlabelled” is only an inter-record statement

Every local record still contains:

- a selected isolated itinerary;
- a marked contact origin;
- a source return orientation;
- the pairing of its two absolute times;
- a coherent simultaneous reversal convention.

The collection is also assumed to cover every obstacle orbit and to have a connected physical incidence graph. These are substantial experimental selections. “Unlabelled” means that obstacle identities, incidence relations, relative signs, contact registrations, and integer copy labels are not supplied **between records**. This qualification should accompany every headline use of the word.

### 5.2 The genericity assumptions do most of the incidence work

Analyticity turns one arc into a complete image. Pairwise noncongruence turns image equality into obstacle identity. Asymmetry turns shape matching into a unique Euclidean placement. If any of these hypotheses is removed, the unlabelled conclusion can acquire continuous, finite, or multiplicity ambiguity.

These are not minor technical assumptions. They define the class on which the global information reduction occurs. The abstract states them, but the introduction should more sharply separate the local theorem, which is smooth and nongeneric, from the global theorem, which is analytic and strongly generic.

### 5.3 Coverage is assumed, not observed

The data cannot reveal an obstacle that participates in no selected record; the free area alone cannot supply its shape or even its number. The manuscript says coverage is an experimental property, but the theorem should explicitly state that the number of unvisited representatives is assumed to be zero rather than statistically tested.

### 5.4 Primitive uniqueness is a network condition

The determinant equality `|det D|=V` is recovered and checkable, but the existence of such a pair is an assumption on the selected collection. Connectedness and two independent cycles do not imply primitivity. The prime-index examples demonstrate the difference. The abstract and statistical theorem should continue to call the result “primitive-class” reconstruction rather than generic whole-table reconstruction without qualification.

### 5.5 Add a standard lattice reference

The row-Hermite/overlattice classification is elementary and correctly proved, but the submitted version should cite a standard source for Hermite normal form and finite-index sublattices. This is not a novelty objection; it is ordinary mathematical attribution and gives readers a stable convention for the matrix formulas.

### 5.6 Do not turn exact congruence tests into an algorithmic claim

In the exact theorem, obstacle classes are recovered by equality of analytic images modulo Euclidean motion. In the stable theorem, compact margins separate those classes. Neither proof supplies an efficient general algorithm for comparing arbitrary analytic functions or minimizing over the compact physical class. The manuscript disclaims computational efficiency; that disclaimer should remain adjacent to the reconstruction language.

### 5.7 Complete the hosted full-package qualification

At final review check, GitHub Actions run `36439719156` for the exact v19 commit remained `queued` with no conclusion. The local receipt is useful and accurately scoped, but it did not authenticate the Git checkout or rebuild Supplements R and S. A specialist-journal submission should include the actual hosted receipt, document hashes, and any build failures rather than only the workflow definition.

## 6. Top-four significance assessment

The strongest positive case is now clearer than in v18. The paper combines:

- a smooth function-level inverse from two intrinsic endpoint densities;
- an explicit two-reflector curvature reconstruction;
- recovery of complete analytic images;
- incidence recovery from an unlabelled record multiset;
- volume-calibrated finite-index period descent;
- an exact arithmetic ambiguity theorem;
- conditional finite-data recovery of both continuous and discrete structure.

This is coherent and significantly better organized.

The reasons I still do not recommend a top-four journal are the following.

### 6.1 The local data are essentially lens data

The paper now proves this itself. Two endpoint densities on an active rectangle are equivalent to the local generating action and area normalization. The quotient step is elementary once the full density functions are observed. The Schur-complement reconstruction of two unknown reflecting arcs is elegant, but its information category is substantially richer than marked lengths, collision counts, or a conventional finite observation.

The result is best understood as a selected local scattering inverse, not as a new rigidity principle for a standard billiard spectrum.

### 6.2 The global descent is generic and assembled from complete shapes

After analytic continuation, the unknown local geometry has become a collection of complete obstacle images. Pairwise noncongruence identifies vertices; asymmetry supplies unique matches; area supplies covolume; Hermite normal form supplies a finite list. Each step is correct, but the conceptual mechanism is an assembly of established analytic-continuation, shape-matching, and lattice facts rather than a new dynamical rigidity mechanism of comparable depth to the leading top-four literature.

### 6.3 Unique reconstruction is restricted to primitive experiments

The general exact theorem gives only a finite list, and Proposition 3.5 proves that the ambiguity cannot be removed from these data. Unique whole-table recovery holds on collections whose geometric cycle subgroup is already the full period lattice. This is a meaningful open class, but it is not a theorem for arbitrary connected full-rank channel data.

### 6.4 Stability is highly conditional

The exponent is fixed with respect to contact-jet order, which is an improvement. It depends on the complete compact prior: analytic strip, continuation geometry, onset brackets, curvature and clearance bounds, asymmetry, shape separation, bounded presentations, and a primitive cycle margin. No minimax lower bound or optimality statement is given. The estimator is existential.

### 6.5 The natural count-only problem remains open

The manuscript carefully preserves the distinction, but the exact analytic count-germ problem is still unresolved. The new theorem changes to a much richer endpoint sensor; it does not settle whether ordinary selected counts determine asymmetric analytic contacts or tables modulo reflection.

### 6.6 The submission is still a multi-volume programme

The focused primary is a major improvement. Nevertheless, the submission retains the whole v18 article as Supplement R and the complete smooth theory as Supplement S. A top-four editor is still asked to assess a very broad accumulated programme. For a specialist-journal submission, I would recommend publishing the local inverse and finite-index descent as one paper and treating the older moment/profile programme separately.

Taken together, these limitations leave the paper below the exceptional threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*, despite its real mathematical merit.

## 7. Recommended form of a specialist-journal submission

1. Make the local two-reflector inverse and the unlabelled finite-index descent the only principal theorems.
2. State the local lens-equivalence proposition before any rigidity claim, so the information content is transparent from the outset.
3. Put the precise remaining marks and the connected-coverage assumption in the main theorem statement, not only in definitions.
4. Separate the smooth local theorem from the analytic/generic global theorem typographically and conceptually.
5. Add a standard Hermite-normal-form reference and fix a single row/column convention.
6. Retain the prime-index ambiguity theorem prominently; it is one of the cleanest results in the paper.
7. Present the finite-data theorem as conditional regularization on a compact prior, without suggesting computational efficiency or statistical optimality.
8. Move the old moment, count-fiber, Volterra, Abel, and auxiliary experiment programme to independently citable companion manuscripts rather than two large submission supplements.
9. Supply a successful exact-SHA full-package build receipt and an independent human proof audit.

## 8. Independent diagnostics and limits

The accompanying `verify_review.py` imports no author code and uses exact rational arithmetic. It performs 33,934 checks:

- 3,600 source/opposite curvature, foot-speed, and local-margin identities;
- 2,880 cubic two-density quotient, flux, and reversal identities;
- 21,131 row-Hermite, quotient-index, dual-membership, and divisor-count checks through index 24;
- 3,595 prime-index lattice and clearance controls for primes through 19;
- 256 incidence permutation/reversal checks;
- 4,134 cell-average, rate-balance, calibrated-index, and integer-locking checks.

Normal and optimized Python executions produced identical output. These diagnostics support only the displayed finite algebra and bookkeeping. They do not prove the phase-density formula, analytic continuation, physical channel realization, compact-prior estimator, complete retained volumes, or literature novelty.

I did not obtain an independent complete TeX build of the primary and both supplements. I did not perform an exhaustive priority search, and I did not re-prove every theorem retained in Supplements R and S.

## 9. Final verdict

**Response to the v18 report:** substantively successful. The closest information comparison, source-delivery structure, primary-paper focus, obstacle/incidence labels, integer lattice labels, and finite-index obstruction have all been addressed at theorem or source level.

**Correctness:** no fatal counterexample found in the new v19 core. The incidence, covolume, HNF, primitive, ambiguity, and stability calculations survived targeted independent checks. The remaining issues are mainly scope, genericity, attribution, delivery completion, and editorial significance.

**Significance:** v19 gives a serious inverse theorem for a rich intrinsic local scattering law and a clean finite-index descent on generic primitive periodic tables. It does not establish rigidity from a standard global billiard invariant, and its unique/stable global conclusions rely on strong selection and prior hypotheses.

**Recommendation: reject at the requested Annals/Acta/Inventiones/JAMS benchmark.** The focused primary could be a strong candidate for a specialist journal after full human proof review, exact-source qualification, and further separation from the retained multi-volume programme.
