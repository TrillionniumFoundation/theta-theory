# External top-four referee report on A2 v21

**Manuscript:** Qian Qi, *Intrinsic marked boundary laws and rigidity of periodic dispersing billiards*  
**Reviewed revision:** `revision/a2-v21-finite-aperture-persistent-rigidity-2026-09-29`  
**Equivalent source alias:** `revision/a2-v21-referee-copy-2026-09-29`  
**Reviewed commit:** `5ab3be483386dab1b2f53575f47dbf7aebd92bd3`  
**Reviewed repository tree:** `6c185f711874fc65a344d6b42ed2768c6c0ff08d`  
**Paper directory:** `papers/A2-v21-finite-aperture-persistent-rigidity`  
**Date:** 29 September 2026  
**Requested benchmark:** *Annals of Mathematics* / *Acta Mathematica* / *Inventiones Mathematicae* / *Journal of the AMS*  
**Status:** author-requested, AI-assisted referee-style assessment; not a journal decision or formal proof certificate.

## 1. Recommendation

**Recommendation at the requested four-journal benchmark: reject.**

Version 21 is a genuine mathematical response to the v20 report. It does not merely rename the complete-catalogue theorem. The new finite-aperture result replaces an acquisition output already quotiented by an unknown lattice with a bounded physical scan. The new pair-key lemma proves that exact recovered pair geometries remove translation repetitions and reverse returns intrinsically. The sparse-witness theorem isolates a finite period-generating subcollection, and the persistence theorem permits unused catalogue edges to cross the cutoff or lose visibility. The paper also adds a concrete analytic cutoff-crossing family and theorem-level comparisons with relative-neighborhood and visibility-complex literature.

On the new v21 arguments audited in detail, I found no fatal counterexample. The lattice-covering estimate, aperture radius, padding reduction, orbit-key criterion, logarithmic saturation bound, witness persistence, cutoff-crossing example, local key isolation, and the stated conditional statistical exponent are internally coherent in their stated scope. Independent exact diagnostics accompanying this report support the finite subgroup, weighted-graph, pair-orbit, aperture and rate calculations.

The negative recommendation is therefore an editorial and conceptual judgment, not a finding that the new core is false. The fundamental observation remains two complete endpoint-arclength density functions for a selected three-impact branch. The finite-aperture scanner still assumes exhaustive access to shortest-pair and clearance primitives on the unknown physical bodies. The statistical theorem is local around a known reference class and assumes that a qualifying saturated witness is retained. Analyticity, asymmetry and pairwise shape separation continue to perform the whole-image identification and synchronization. These hypotheses produce a serious specialized inverse theorem, but in my judgment they do not yield the exceptional naturality, breadth or conceptual transformation expected by the four journals named above.

The focused local inverse and the finite-aperture/persistent-witness package could be strong specialist-journal material after a fresh human proof review and substantial compression. I would not recommend another open-ended revision cycle at the requested top-four benchmark.

## 2. Frozen source and chronology

Both v21 revision aliases listed above resolve to author commit

`5ab3be483386dab1b2f53575f47dbf7aebd92bd3`.

Its parent is the frozen v20 external-review commit

`40e9f1beaf49bf7f870f2f6f73ac027feab1a84e`,

whose report reviewed author commit

`c376e802e6e86735888dcd685f987c7a8f475903`.

Thus v21 is based directly on the latest report. At creation of this review branch, no `revision/a2-v22...` branch existed. The complete reviewed v20 paper tree is preserved under `history/v20-reviewed`; Supplement R retains the complete v18 paper tree and Supplement S retains the smooth relative-law tree.

The six v20 mathematical core files `core/01_setting.tex` through `core/06_canonical.tex` retain their Git blob identities. The principal new mathematical chapter is

`core/07_aperture_persistence.tex`,

with a new theorem overview in `core/00_new_results.tex`, revised front matter, response, proof and literature ledgers, source pins, validator and workflow.

The present review branch was created directly from the v21 author commit. It adds files only under

`reviews/a2-v21-external-harsh-top4-rereview-2026-09-29/`.

No author source, earlier review, revision branch or unrelated paper is changed by this review.

## 3. What v21 substantively fixes

### 3.1 It removes the unknown-lattice quotient from the acquisition output

The v20 canonical catalogue supplied one representative of every translation orbit of short clear bridges. This was an exact mathematical datum, but operationally it presupposed the unknown group that the inverse theorem was meant to recover.

Version 21 defines the intrinsic translation group

\[
P(\mathcal O)=\{v\in\mathbb R^2:\mathcal O+v=\mathcal O\}
\]

and proves that, on the asymmetric pairwise shape-separated class, it is exactly the period lattice in every admissible presentation. It then distinguishes literal experimental records from normalized records and from the geometric key consisting of the entire recovered pair in relative position with marked contacts.

The finite-aperture theorem assumes only bounds on the number of obstacle orbits, obstacle diameter and obstacle-union covering radius. It scans all relevant physical bridges whose midpoints lie in a stated disk. The period quotient is performed after the inverse, by exact equality of geometric keys. This is a real improvement over v20's acquisition contract.

### 3.2 It no longer freezes every redundant catalogue edge

The v20 statistical theorem required a regular complete catalogue with a positive cutoff and clearance margin for every record. Version 21 extracts a saturated witness: a spanning tree visiting every obstacle orbit together with enough cycle edges to generate the full period group.

Only the witness must persist. Other channels can cross the range cutoff, be repeated, disappear from the qualified list, or lose visibility. The paper provides an explicit analytic family in which a surplus `(1,2)` bridge crosses the cutoff while the horizontal and vertical period-generating loops persist.

This is not merely a change of terminology. It replaces full catalogue-topology stability by stability of a finite sufficient subcollection.

### 3.3 The nearest proximity and visibility comparisons are now present

Section 7.5 compares the strict shorter-neighbor mechanism with Toussaint's relative-neighborhood graph theorem and the Jaromczyk--Toussaint survey. It separately compares the finite geometric selection problem with Pocchiola--Vegter's visibility-complex and free-bitangent constructions.

The manuscript correctly distinguishes point distances from gaps between bodies, finite point-set spanning trees from deck-period generation, and tangent free bitangents from the normal non-grazing bridges used by the billiard law. It does not import an algorithmic complexity theorem whose primitive operations are unavailable here. This closes the most concrete literature objection in the v20 report.

## 4. Correctness audit of the new core

### 4.1 Translation group and geometric keys

If a translation preserves the obstacle union, pairwise noncongruence forces every connected component to be mapped to the same obstacle type. A compact body has no nonzero translational symmetry, so the displacement is a period. Hence `P(O)` equals the full period lattice.

For geometric keys, one direction is immediate: periods and reversal of the return leave the undirected pair key unchanged. Conversely, suppose an isometry matches two recovered pairs. Shape separation fixes the obstacle type of one matched member. Translation by the difference of the corresponding period copies is one such matching. Trivial Euclidean symmetry of that body makes it the unique matching, so the pair is carried by a period translation. The argument also handles loops and exchange of the two members.

I found this criterion correct. The hypotheses are essential: repeated congruent shapes or nontrivial body symmetries would create additional matchings.

### 4.2 Derived lattice covering bound

Let `r` be the number of obstacle orbits and choose one point in every representative lifted along a quotient spanning tree. Across a tree edge of gap less than `R`, two chosen points are separated by less than

\[
R+2D_0.
\]

A path has at most `r-1` edges. If an arbitrary point `x` lies within `rho_0` of an obstacle, it lies within `rho_0+D_0` of that obstacle's chosen point. Thus

\[
\operatorname{dist}(x,c_1+\Lambda)
 \le \rho_0+D_0+(r_0-1)(R+2D_0)=L_0.
\]

This is a valid upper bound for the covering radius of the unknown lattice. Every midpoint coset consequently has a representative in the open aperture of radius `L_0+xi`.

The estimate is deliberately coarse but sufficient. It uses the retained completeness theorem at the same range `R>2rho_0` and does not assume a period basis.

### 4.3 Finite padding and exhaustive testing

A bridge with midpoint in the aperture and gap below `R` lies inside the disk of radius `B+R/2`. Every endpoint or blocking body meets this disk. The diameter bound places the complete bodies in the padded disk of radius

\[
Q=B+R/2+D_0.
\]

For a fixed table, local finiteness gives only finitely many such bodies. With a lower separation `d_0`, the area-packing bound

\[
(1+2Q/d_0)^2
\]

is correct. Testing all pairs and removing long, obstructed, and out-of-aperture segments therefore reproduces the exact scan.

This is a finite geometric reduction. It is not a method for obtaining the bodies, their complete shapes, or the clearance primitive from the endpoint-law sensor. The manuscript now states that limitation explicitly.

### 4.4 Sparse saturated witness

Start with a spanning tree and two independent cycle vectors generating a subgroup of index `n`. If the current subgroup has index `q>1`, some remaining cycle lies outside it because the complete cycle group is the lattice. Adjoining it produces a strict intermediate subgroup, so the new index is a proper divisor of `q` and at most `q/2`.

After at most `floor(log_2 n)` adjunctions the index is one. The edge count is therefore

\[
(r-1)+2+\lfloor\log_2 n\rfloor
 =r+1+\lfloor\log_2 n\rfloor.
\]

The group-theoretic argument is correct. It does not require a primitive observed pair.

### 4.5 Witness persistence

Every selected witness bridge has a strict gap inequality and positive clearance. For positively curved strictly convex bodies, the closest normal pair is nondegenerate; it varies smoothly under sufficiently small boundary and placement perturbations. Only finitely many third-body copies can threaten the finitely many bounded witness segments. Hence one neighborhood preserves all witness branches and their local experimental margins.

In a fixed local lattice presentation the integer copy labels of the persisting edges remain constant. Since those integer vectors generate `Z^2` at the reference table, their deformed physical vectors generate the full nearby period group. The labels are proof coordinates rather than inverse data.

This is a sound local persistence theorem. It is intentionally not a global statement across lattice-presentation changes or arbitrary bifurcations.

### 4.6 Genuine cutoff crossing

For one small asymmetric body on the square lattice, the bridges associated with `(1,0)` and `(0,1)` generate the period group. The `(1,2)` center segment has positive clearance from every other lattice point. Scaling the body changes its gap with nonzero derivative. Choosing the cutoff equal to that gap at one parameter value creates a true birth/death across the strict inequality, while the two generating loops remain clear and well below cutoff.

The covering condition also remains valid: for sufficiently small bodies, twice the obstacle-union covering radius is close to `sqrt(2)`, whereas the extra bridge gap is close to `sqrt(5)`.

This example adequately demonstrates that the new theorem covers a genuinely changing redundant catalogue.

### 4.7 Local isolation and statistical rate

In a bounded local lattice presentation, only finitely many relative copy labels can have gap below `R+1`. At the reference table, distinct undirected translation orbits have distinct exact geometric keys. A finite set of distinct keys has positive separation. Shrinking the physical neighborhood and the key neighborhoods preserves classification, including pair types obstructed at the reference table. No unknown copy label is used in the observed list.

For every qualified record, the retained pilot and two endpoint histograms give simultaneous density error

\[
e_N\le C\{h^\beta+\sqrt{r_N}h^{-3}+r_Nh^{-4}\},
\qquad r_N=\frac{\log(CJN/\delta)}{N}.
\]

The first two terms balance at

\[
h=r_N^{1/(2\beta+6)}.
\]

The linear Bernstein term is then smaller, and one analytic-continuation loss gives the table rate

\[
C r_N^{\beta\theta/(2\beta+6)}.
\]

A single multinomial endpoint sample contributes to every histogram cell, so the number of cells enters the logarithm rather than as a multiplicative number of phase preparations. The preparation count `CJN` is consistent with the specified observation model.

The proof is logically conditional on physical-pair fitting, witness-key neighborhoods, qualification, witness retention and a compact local physical prior. Within those hypotheses I found the rate calculation and the use of stable all-cycle saturation coherent.

## 5. Qualifications and corrections required for any resubmission

### 5.1 “Finite acquisition” still contains a geometric scanner oracle

The output is no longer pre-quotiented by an unknown lattice, which is an important correction. Nevertheless, the scanner is assumed to enumerate bodies in a physical region, test complete body pairs, compute shortest gaps, and test clearance against every possible blocker. These are operations on the unknown geometry itself.

The inverse theorem only receives local probability records, but the acquisition mechanism uses substantially more geometric access to decide which records exist. This should remain explicit in the title, abstract and theorem summaries. The result is not acquisition from unmarked trajectories alone.

### 5.2 The stated aperture priors do not give a uniform record-count bound by themselves

The bounds `r_0,D_0,rho_0,R` give a uniform aperture radius. They do not prevent arbitrarily small period cells and arbitrarily small bodies, so they do not uniformly bound the number of copies in the aperture. The optional separation parameter `d_0` supplies the displayed packing bound.

Thus the scan is finite for every fixed periodic table, while a uniform complexity bound requires an additional lower separation or covolume prior. The paper essentially says this, but “explicit finite acquisition” should not be read as a prior-uniform bounded number of tests without `d_0`.

### 5.3 The statistical theorem uses a known local reference chart

Witness-key neighborhoods are chosen around a reference table and are part of the local prior. They are exactly what lets the estimator recognize the useful records in an unlabelled varying list. This is mathematically legitimate local stability, but it is not global witness discovery.

The headline should say that the theorem is local around a known reference class with a retained witness, not merely that “qualified unlabelled lists” suffice.

### 5.4 Qualification and witness retention are assumptions, not inferred robustness

The acquisition list is assumed to retain at least one observation of every witness orbit and to omit records that fail the uniform local density bounds. Neither property is statistically certified from the same noisy data. The theorem therefore does not tolerate arbitrary erasures, adversarial omissions, or loss of every period-generating set.

This limitation is accurately stated in the body and should remain adjacent to every informal description of persistence.

### 5.5 The sensor remains function-valued and highly marked

One exact record consists of two complete endpoint-density functions with a local origin, return branch and paired absolute times. Its finite approximation is two growing two-dimensional histograms plus a pilot. The phrase “finite aperture” concerns the number and location of records, not finite-dimensional information per exact record.

The observation is an intrinsic local scattering/lens law, not a collision-count law, marked length spectrum, or fixed finite list of real numbers.

### 5.6 Global genericity remains decisive

Analyticity extends local arcs to complete bodies. Asymmetry makes cross-record matching unique. Pairwise noncongruence identifies obstacle types. The finite-aperture and key theorems do not remove these assumptions from the whole-table inverse.

Repeated shapes and symmetric bodies fall back to registered or finite-candidate statements. This should remain prominent rather than being relegated to qualifications.

### 5.7 The theorem is not algorithmic

Exact congruence of analytic bodies, Borel minimization over compact physical priors, exhaustive geometry tests and continuation by harmonic measure are mathematical existence operations. The paper does not supply an efficient representation, comparison, discovery or optimization algorithm. The current disclaimers are necessary.

### 5.8 Hosted v21 qualification was not complete at review time

The local receipt reports 70,662 finite checks, identical normal and optimized output for the two diagnostic suites, and a warning-free 29-page primary build. It correctly identifies itself as source-content execution rather than a Git checkout.

GitHub Actions run `36535427881`, bound to author commit `5ab3be48...`, was still `queued` with no conclusion when this report was finalized. I therefore do not record an independently completed exact-source all-volume v21 build. This is a delivery item, not the mathematical basis for the recommendation.

## 6. Top-four significance assessment

The positive case is substantial:

- the unknown period quotient is removed from the exact acquisition output;
- pair keys intrinsically identify translation orbits;
- a coarse but explicit finite aperture is proved from global bounds;
- the complete catalogue can be reduced to a logarithmically sparse saturated witness;
- sufficient data persist while redundant channels bifurcate;
- the statistical theorem no longer freezes the entire catalogue topology;
- the requested proximity/visibility literature is now addressed;
- the previous local inverse, all-cycle index and exact ambiguities remain active and source-pinned.

The negative case remains decisive at the requested benchmark:

1. **The local datum is exceptionally rich.** Two full endpoint densities almost explicitly contain the stationary action, and retain local origin, branch and time marks.
2. **The finite scanner still uses the unknown geometry as a selection oracle.** It assumes exhaustive shortest-pair and blocker tests on complete bodies in a physical aperture.
3. **The global theorem remains strongly generic.** Analyticity, asymmetry and pairwise shape separation perform the continuation and synchronization.
4. **The persistence theorem is local and conditional.** A reference witness, key neighborhoods, qualification and witness retention are built into the prior.
5. **The new global ingredients are elegant but elementary.** They combine a coarse lattice-covering estimate, relative-neighbor descent, finite subgroup saturation and compact-prior regularization.
6. **No natural lower-information rigidity theorem results.** Exact analytic count-only rigidity, a conventional marked-length result without symmetry/genericity, and an unmarked trajectory inverse remain unresolved.
7. **No minimax or efficient acquisition theorem is proved.** The rate is a class-dependent conditional upper bound.
8. **The submission remains a broad multi-volume programme.** The 29-page primary relies on two retained supplementary volumes and a long revision lineage.

Version 21 successfully answers the concrete v20 objections. What remains is not another local gap that can be closed by appending one more lemma; it is the editorial question whether the customized sensor and acquisition contract reveal a sufficiently universal principle. In my judgment they do not yet meet the exceptional threshold of *Annals*, *Acta*, *Inventiones*, or *JAMS*.

## 7. Independent diagnostics and review limits

The accompanying `verify_review.py` imports no author verification code. In exact integer or rational arithmetic it performs 23,945 checks:

- 1,775 existence-of-new-generator checks and 1,775 proper-divisor/halving checks;
- 1,200 saturation and 1,200 logarithmic-step checks;
- 6,000 sparse witness edge-count checks;
- 1,000 arbitrary-weight relative-graph component checks;
- 3,000 translation and 3,000 reversal pair-key checks;
- 2,000 normalized cycle-minor persistence checks;
- 2,700 aperture-coset representative checks and 81 packing identities;
- 50 covering-range, 50 witness-saturation, 50 basis-cutoff and 50 extra-edge crossing checks;
- 14 statistical exponent checks.

All passed. These are finite diagnostics, not proofs of the infinite geometric theorem, analytic continuation, physical scanner, statistical estimator or literature novelty.

I did not perform an exhaustive priority search and did not re-prove every retained result in Supplements R and S. The previous successful v20 workflow is historical evidence, not a v21 pass.

## 8. Final verdict

**Response to the v20 report:** substantively successful. The unknown quotient, full-catalogue topology freeze and closest proximity/visibility comparison have all been addressed by theorem-level additions.

**Correctness:** no fatal counterexample found in the new v21 core. The aperture, orbit-key, sparse-witness, persistence, cutoff-crossing and local statistical arguments survived targeted audit and independent finite checks.

**Scope:** the exact inverse still uses a rich marked local scattering law and an exhaustive geometry-aware scanner. The statistical result is local to a compact analytic/generic prior and assumes witness qualification and retention.

**Significance:** the revision is technically serious and has strong specialist-journal potential, but its information contract, strong genericity, conditional discovery mechanism and elementary global ingredients leave it below the exceptional conceptual threshold of the requested four journals.

**Recommendation: reject at the requested Annals/Acta/Inventiones/JAMS benchmark.**