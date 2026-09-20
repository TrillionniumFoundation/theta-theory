# Independent harsh referee report on A2 revision 97

**Manuscript:** *Projective polynomial observations: real spectral atlases and identification walls*  
**Reviewed branch:** revision/a2-v97-real-singularity-atlas-weight-wall-2026-09-20  
**Reviewed exact head:** 5c8b57c655aaec0df76dc3178554de2d1736b076  
**Reviewed principal entrypoint:** papers/A2-v17-boundary-information-coarsening/rigidity_v97.tex  
**Controlling prior report:** review/a2-v96-independent-harsh-top4-2026-09-20, report head b4ab165062f3625e06717002fb419bd44ab8e7f7  
**Prior v96 manuscript head:** 423a0e135c217d6dc42fc973d8da4ee13893e865  
**Date of this report:** 2026-09-20

## 1. Recommendation

**Recommendation for a top-four general mathematics journal: reject in the present form.**

This is a substantially stronger paper than revision 96. I do not regard revision 97 as cosmetic, and I do not have a counterexample to the explicit multiplicity formulas, the cubic exact-fibre classification, or the weight-wall entrance law. The authors have also corrected the previous source-control error and have rebuilt the principal article into a much more coherent 21-page theorem graph.

Nevertheless, revision 97 now makes one theorem so broad that the burden of proof has moved. The paper's top-four case now depends on the claimed **finite real spectral atlas for a general fixed-format semialgebraic family**. The proof of that theorem is not presently at the same level of completeness as the theorem statement. The key relative-resolution argument is a plausible research blueprint: resolve a generic fibre, spread the construction over an open base, remove bad parameters, recurse on the exceptional locus, test real accessibility, and then combine Hardt triviality, quantifier elimination, and semialgebraic asymptotics. That is exactly the right architecture. It is not, in its present compressed form, a publication-grade proof of all the uniformity and effectiveness assertions that the theorem carries.

The significance issue is also not closed. The explicit degree-d theorem is broader than the old cubic calculation, but it lives in a very favorable full-rank regime where the observation locally recovers all polynomial and stochastic coefficients Lipschitzly. Once that inverse has been established, the remaining multiplicity exponents are largely the real-root perturbation geometry of monic polynomials plus a finite Fisher projection. The genuinely distinctive part of the manuscript is therefore not "finite stratification" or "finite valuation lists" by themselves; it is the **joint real constrained leading set, its spectral root image, and the remote-fibre stochastic transition**. The current literature comparison still does not isolate that boundary sharply enough.

I would encourage a new submission only after a structural revision rather than another incremental patch. Either the authors should prove the family-resolution/atlas theorem at full theorem-level granularity and update the novelty comparison against the current literature, or they should narrow the principal paper to the parts that are already most convincing.

## 2. What revision 97 genuinely changes

The revision deserves credit for several nontrivial advances.

First, the source chronology is now correct. The response pins the v96 report and its exact head, acknowledges the erroneous chronology statement in v96, and answers both v96 and v95. This closes a concrete referee-process defect.

Second, the principal article is no longer an accretive import graph. The new entrypoint is a focused paper with the spine

real constrained graph → joint weighted specialization → finite parameter atlas → multiplicity/boundary laws → rank-deficient cubic fibre → remote weight-wall transition.

The historical material is retained in an archival companion rather than being silently deleted. This is a major editorial improvement.

Third, Theorem thm:mult-atlas does answer the central breadth objection of the previous report at the level of explicit model classes. For fixed degree d, the manuscript now permits arbitrary coprime root-multiplicity patterns and arbitrary endpoint/interior assignments in a full-rank binary experiment. The formulas
\[
\beta_1=1,\qquad \beta_k=k/2
\]
for an interior cluster and
\[
\beta_k=k
\]
at a boundary cluster are accompanied by realizing root arcs and a whole-model Hausdorff statement, not merely a pointwise perturbation heuristic.

Fourth, the weight-wall analysis is mathematically meaningful. The earlier report asked whether the local Fisher constant must blow up at an identification wall. Revision 97 gives a different mechanism: a **remote exact component enters the observation ball while the base local Fisher law stays coercive**. I accept this correction. There is no mathematical reason that every loss of global identification must be detected by divergence of a local inverse constant. The distinction between local conditioning and remote exclusion is conceptually important.

Fifth, the paper is much more disciplined about computational evidence. The committed SymPy script is explicitly labeled a finite regression rather than a proof verifier. That is the correct epistemic role for those calculations.

These improvements are substantial. My negative recommendation is not based on a view that revision 97 has made no progress. It is based on the fact that the revision has now promoted a new family theorem to the top of the paper without yet supplying the proof infrastructure commensurate with its breadth.

## 3. Main objection I: the relative family-resolution lemma is the load-bearing theorem, and its proof is still a blueprint

The central new statement is Lemma lem:relative, which is then used in Theorem thm:atlas. The lemma asserts that on the singleton exact-fibre locus, parameter space has a finite semialgebraic refinement on which one has fixed cluster multiplicities, a fixed finite list of monomial orders, and fixed real-accessibility flags. Its proof contains the following chain:

1. apply semialgebraic triviality to compact graph fibres;
2. pass to an irreducible algebraic closure of a parameter cell and to its function field;
3. resolve every dominating component of the generic lifted fibre;
4. recursively resolve generic singular subvarieties;
5. principalize all nonzero functions;
6. spread the equations, blow-up centres, and normal-crossing data after clearing denominators;
7. delete proper algebraic subsets so that smoothness, relative dimensions, and normal crossings persist;
8. replace constructible bad-fibre images by proper algebraic closures;
9. recurse on the excluded parameter locus by Noetherian induction;
10. descend finite algebraic base covers by real semialgebraic branch selection;
11. partition once more by first-order real accessibility of divisors.

This is a reasonable strategy. But every difficult word in the theorem sits inside these eleven steps.

The manuscript needs an actual **relative principalization theorem with interfaces**, not a paragraph saying that the generic construction can be spread. In particular, the paper should state and prove, or cite in exactly applicable form, the following facts.

- What is the precise algebraic base after replacing a semialgebraic cell by an algebraic closure? Which components are retained, and how are the original sign conditions remembered throughout the spread-out construction?
- What is the precise statement guaranteeing that the generic sequence of blow-ups extends after shrinking the base to a sequence whose centres are smooth over the base and whose total transforms have relative normal crossings on every retained fibre?
- How are components on which G or one of the H functions becomes identically zero on a special fibre detected and separated? A function that is generically nonzero can specialize to zero, and this changes the monomial-data type.
- How are vertical components created under specialization handled? Saying that they lie over an exceptional algebraic subset is plausible, but that assertion is one of the things that must be proved in the induction.
- Why does the recursion produce a **finite list of source charts and order data** that is sufficient for every real fibre in the stratum, rather than merely fibrewise finite lists?
- Which exact theorem guarantees compatibility of the proper real cover with all square-slack equations after the family construction is spread out?
- When a finite algebraic base cover is introduced to label clusters or components, what is the precise descent statement that preserves the finite order list and real-accessibility information on the original semialgebraic base?
- How is effectiveness preserved through irreducible decomposition, field extensions, generic resolution, specialization, and descent?

The present proof gives answers in prose, but it does not make the dependence chain auditable. This matters because Theorem thm:atlas is not merely an existence theorem. It also claims a **finite real-algebraic description** and feeds those finite data into the subsequent semialgebraic leading-set theorem.

The correct standard here is not "a specialist can probably fill this in." For a general-journal paper whose principal novelty claim is a parameter atlas, this construction is the theorem.

I therefore regard lem:relative as **not yet proved at the level required by its use in the paper**. I am not asserting that it is false. I am asserting that revision 97 has moved the paper's main gap into this lemma.

## 4. Main objection II: Theorem thm:atlas bundles several distinct uniformity statements whose proofs need to be separated

Theorem thm:atlas combines four different levels of structure:

- topological triviality of exact target fibres;
- constancy of finite divisorial order data;
- semialgebraic triviality of joint leading coefficient/root sets;
- a compact-uniform power remainder and Nash dependence of the leading constant.

These should not be presented as if they all follow from the same application of Hardt triviality.

The first part is standard semialgebraic geometry once the correct compact fibre graph is specified.

The second part is the difficult content of lem:relative.

The third part requires a parameterized version of the fixed-centre closure formula in which the centre is held fixed inside each fibre. The manuscript correctly warns that one must not take a closure while allowing the parameter to drift across strata. But the proof should then explicitly construct the semialgebraic family
\[
\{(\theta,U,V):(U,V)\in\mathcal I_0(\theta)\}
\]
with all quantifiers written over the same fibre. This is more than a notational detail: it is the object to which Hardt is later applied.

The fourth part is analytically stronger. The argument says that the Hausdorff error of the rescaled root images is a semialgebraic function of \((\theta,t)\), applies cylindrical decomposition, extracts finitely many possible positive orders, and then obtains
\[
\omega_\theta(t)=C(\theta)t^\alpha+O_H(t^{\alpha+\nu}).
\]
This is plausible, but it should be isolated as a **uniform semialgebraic asymptotics proposition**. The current paragraph compresses several issues:

- the rescaled root-set map is set-valued, so one needs to specify the definable compact family whose Hausdorff distance is being taken;
- the Hausdorff distance must itself be shown semialgebraic in the parameter and radius;
- one needs a finite stratification on which the leading exponent of this error is positive and bounded away from zero;
- the threshold \(t_0(\theta)\) and bound \(M(\theta)\) must be controlled on compact subsets of the stratum;
- the result must be compatible with changes in root labeling and with the finite matching metric.

Again, I think these statements are likely true in an o-minimal/semialgebraic setting. But the proof as written is a compressed invocation of an entire definable asymptotics package. If this remainder is important enough to appear in the main atlas theorem, the package should be stated and proved once.

A clean revision would split thm:atlas into at least three theorems: (A) relative finite monomial data, (B) definable family of joint initial sets, and (C) uniform power asymptotics of the root-set diameter.

## 5. Main objection III: the novelty comparison is still not current-version complete

The paper has improved its tone around classical resolution and Łojasiewicz theory. It now explicitly says that the scalar divisor-ratio formula is classical. That is correct and welcome.

However, the literature comparison remains incomplete in a way that matters for a top-four originality assessment.

The bibliography pins T. H. Hà, *An algebraic theory of Łojasiewicz exponents*, to **arXiv:2602.18410v1, February 20, 2026**. The current arXiv version is **v2, revised March 14, 2026**. The current version contains, among other things:

- Theorem 5.8, a finite-testing/finite-max formula under a finite testing hypothesis;
- Theorem 9.9, a finite wall-chamber decomposition for parameter families once a uniform finite candidate set is available and the valuation data vary continuously;
- Theorem 12.3, a more structured wall-chamber theorem for Newton-controlled families admitting a common toric model.

The manuscript's comparison paragraph focuses on Theorems 5.8 and 12.3 and characterizes the family theorem mainly through the common-toric-model hypothesis. That is not the whole current comparison because Theorem 9.9 already isolates a more abstract finite-candidate wall-chamber mechanism.

This does **not** make revision 97 redundant. Hà's objects and hypotheses are different, and the present paper has real stochastic inequalities, a joint coefficient initial set, a root-set image, and a global remote-fibre transition. But the paper must now say exactly that.

The novelty table should therefore be rewritten around the following question:

> Grant the reader all scalar finite-max and wall-chamber structure available from current valuative theory. What still has to be proved to obtain this paper's spectral theorem?

The answer appears to be:

1. construction of a **real-accessible**, inequality-constrained family of relevant branches;
2. preservation of **joint** weighted coefficient relations rather than coordinatewise scalar envelopes;
3. passage from that joint coefficient set to a root-multiset Hausdorff limit and exact bottleneck diameter;
4. coupling to the stochastic normalization model;
5. analysis of a remote exact-fibre component entering at an identification wall.

Those are potentially distinctive contributions. The current paper should make them the novelty claim instead of allowing "finite atlas" or "wall-chamber" language itself to carry originality weight.

For a top-four paper, citing an obsolete arXiv version while making a novelty comparison to a rapidly evolving 2026 preprint is not acceptable. The comparison must be against the current version at the time of submission.

## 6. Main objection IV: the "arbitrary multiplicity" theorem is useful, but its scope is materially narrower than the surrounding rhetoric

Theorem thm:mult-atlas is a real improvement over v96. It should stay.

But it is important to understand why it is tractable. The theorem assumes:

- exactly two latent components;
- fixed degree d;
- coprime component polynomials;
- strictly positive weights;
- strictly positive, invertible U and V;
- at least 2d+1 clocks;
- clocks outside the entire root interval;
- a fixed binary stochastic observation architecture.

Under those assumptions Lemma lem:fullrank gives a local Lipschitz inverse for the **entire coefficient and stochastic parameter vector**. The singular behavior is then concentrated in the map from nearby real-rooted polynomial coefficients to roots. The square-root law at a repeated interior root and the linear one-sided law at a boundary root are exactly the kind of polynomial-root geometry one should expect after coefficient recovery.

The Fisher program for the leading constant is nontrivial and useful, but the theorem is not yet a classification of general stochastic polynomial singularities. It does not include, in one explicit formula, changes of:

- second-channel rank;
- simultaneous shared roots between components;
- vanishing channel entries;
- number of latent components;
- observation architecture;
- degree;
- global remote branches.

The paper no longer literally claims all of these. Nevertheless, phrases such as "arbitrary multiplicities" and "real spectral atlas" can easily make the explicit theorem sound broader than it is. The article should consistently qualify it as an **arbitrary fixed-degree multiplicity/boundary atlas in the full-rank coprime binary regime**.

This is not a correctness objection. It is a significance calibration objection. At a top-four venue, a theorem cannot derive its breadth from the word "arbitrary" while fixing all the other structural axes that remove the difficult inverse degeneracies.

## 7. Main objection V: the local inverse through rank and identification walls is still too compressed

Lemma lem:local-cubic is better than its predecessor because revision 97 now lists the actual uniform margins. That is progress.

But it remains a load-bearing lemma for all of the following:

- coercivity of the projected Fisher cone;
- completeness of the local leading set;
- continuity of the local leading constant through B=0 and E=0;
- separation of local conditioning from remote identification;
- the two-scale weight-wall theorem.

The proof uses several delicate reductions in rapid succession:

1. normalizer recovery controls q'-q and K'-K;
2. the second marginal forces the competitor's second channel to remain invertible;
3. every nearby component polynomial is reduced to an approximate affine-pencil coordinate;
4. endpoint and discriminant inequalities force the first pencil coordinate to be O(delta);
5. a depressed-cubic real-rootedness inequality forces the second coordinate to be 1+O(delta);
6. coefficient functionals recover the rank-one coefficient matrices;
7. entry sums and normalized marginals recover weights and both channels.

For a theorem crossing the rank-one/rank-two locus, I would require a standalone quantitative proposition for steps 2--5. In particular, the paper should write the exact perturbation inequalities that pass from second-marginal closeness to
\[
f'_b=h_{c_b}+O_{\mathrm{coef}}(\delta)
\]
with constants uniform on a compact K0, and then state the neighborhood sizes for which the discriminant and depressed-cubic arguments are valid.

The present proof is credible, but it is still written at the level of an expert derivation rather than a final reference proof. Since the new wall theorem depends on this lemma twice, the standard should be higher than "the constants can be chosen uniformly by compactness."

## 8. Main objection VI: the remote tangent cone and its converse realization deserve their own theorem

The weight-wall theorem is the most interesting new model-specific result in revision 97. I therefore read the remote-point argument carefully.

The definition of the cone in eq:remote-jets is natural:

- the simple root at 0 gives a one-sided nonnegative variable;
- each interior double cluster gives a nonnegative splitting variable;
- means and the remote simple root are free;
- the weight on the newly admissible component is one-sided at the floor;
- channel directions are free in the tangent spaces of the stochastic simplices.

The positivity argument for mu_E is also conceptually good. The differentiated normalizer equations reduce a hypothetical score equality to a pencil motion, and the weight-floor obstruction
\[
\pi \dot c+c_* k=-1
\]
rules it out.

What is still too fast is the assertion in Lemma lem:remote-control that the coefficient tangent cone is **exactly** the displayed cone and that every bounded vector in it is realized by a closed-model stochastic root arc with a uniform O(delta^(3/2)) observation remainder.

That statement is not just a convenience. It is what identifies the variational quantity mu_E with the first-order remote entrance distance rather than merely an upper or lower bound.

The paper should isolate a tangent-cone proposition proving both directions:

- every normalized secant sequence at xi_* has a subsequential jet of the displayed form, including all stochastic simplex constraints and the active weight floor;
- every displayed jet admits an actual semialgebraic/analytic feasible arc;
- the coefficient/root parametrization is uniform enough to give the claimed remainder;
- no additional first-order directions arise from component permutation or an alternative local factorization.

I see no obvious missing direction in the displayed cone. My objection is proof completeness, not a counterexample. But this is precisely the kind of cone-identification step that a referee should not be asked to reconstruct.

## 9. Main objection VII: the "finite effective algorithm" claim remains stronger than the provided certificate

Revision 97 has significantly improved the formal input model. Definition def:input now says how algebraic constants are represented and places inequalities, branch choices, clocks, weights, and isolating data inside first-order formulas. This answers one of the v96 requests.

The remaining issue is the word **algorithm** in Theorem thm:joint and the effectiveness claim in Proposition prop:real-cover.

The theoretical pipeline is:

- real semialgebraic decomposition;
- algebraic square-slack lifting;
- reduction and irreducible/component handling;
- constructive resolution;
- recursive resolution of lower-dimensional real singular loci;
- simultaneous principalization;
- exact real-accessibility testing;
- compact chart selection around G=0;
- cluster-factor selection;
- quantifier elimination for the weighted closure;
- elimination of bounded model coordinates;
- algebraic root encoding;
- permutation matching for bottleneck distance;
- compact semialgebraic maximization;
- extraction of a defining polynomial and isolating interval.

No complexity bound is needed. But a proof of effectiveness should cite or formulate exact algorithms for every change of representation and explain how their outputs are passed to the next stage.

The repository's scripts/verify_a2_v97_math.py does not implement this pipeline, and it correctly says so. It verifies finite symbolic identities and selected Fisher programs. The script is good evidence for those finite examples; it is **not evidence for the universal algorithm theorem**.

I recommend separating the results into:

- an existence theorem requiring only resolution/uniformization;
- an abstract effectivity theorem over encoded real algebraic input, with a formal algorithmic dependency list;
- executable diagnostics for the explicit polynomial families.

That separation would make the evidentiary status of each claim much clearer.

## 10. The joint specialization theorem is one of the strongest parts, but it should carry more of the paper's novelty burden

Theorem thm:joint is, in my view, closer to the actual mathematical identity of the paper than the scalar exponent theorem.

The important point is that the paper does not independently maximize scalar coefficient envelopes and then multiply unrelated worst cases. It fixes the observation centre, performs a simultaneous weighted rescaling, takes the real feasible closure, projects to a **joint coefficient set**, sends that set through the cluster-root map, and finally takes a bottleneck diameter. This retains constraints between clusters and between coefficients.

That is a meaningful object.

The proof of fixed-centre Hausdorff convergence is also reasonably convincing:

- boundedness comes from the scalar order estimates;
- the closure formula describes the outer limit;
- semialgebraic one-variable monotonicity upgrades subsequential approach to full approach for a fixed limit point;
- compactness and finite nets give Hausdorff convergence;
- cluster separation prevents optimal matchings from crossing distinct base clusters.

I would not ask the authors to weaken this theorem.

I would instead recommend making this theorem the conceptual centre and reducing the rhetorical weight placed on the scalar valuation formula. The scalar order is an input; the joint initial spectral set is the additional structure.

## 11. The weight-wall theorem corrects the previous referee's suggested mechanism

The v96 report asked whether kappa_x or kappa_y must vanish at an identification wall and whether the leading constant must blow up. Revision 97 shows that at the E=0 weight wall this is the wrong necessary mechanism.

I accept the correction.

The theorem distinguishes:

- a local base law with finite positive C_loc;
- a remote branch whose observation separation is d_rem(delta)=mu_E delta+O(delta^(3/2));
- a subcritical regime t=lambda delta, lambda<mu_E, in which only the base component is seen;
- a supercritical regime lambda>mu_E, in which the remote spectrum enters and the modulus jumps to a positive D_* up to O(sqrt(delta));
- a nonidentified-side square-root opening of the extra exact branch.

This is a real conceptual contribution. It cleanly separates three phenomena that were blurred in earlier revisions:

1. root-multiplicity singularity;
2. exact identification;
3. local inverse conditioning.

My objections to this section concern the tangent-cone proof granularity, not the theorem's conceptual value.

## 12. The geometric wall is still only sketched

Revision 97 has one full wall theorem, which is enough to answer the previous request "analyze at least one identification wall." I do not require a second wall theorem as a condition of correctness.

However, the final remark on B=0 should not be allowed to do more rhetorical work than it proves. It derives a quadratic opening of the affine-pencil interval in the geometric clearance and notes that the local constants remain finite. It explicitly says that the two-scale entrance cone is different and is not analyzed.

That limitation is appropriate. The abstract and introduction should preserve it. Any claim that the paper has classified "identification walls" in general would be too broad; it has a detailed **weight-wall theorem** and a local calculation at the geometric wall.

## 13. Current exact arithmetic is useful but cannot validate the general theorem

The finite regressions are well chosen:

- the cubic-pencil discriminant factorization;
- the remote double-root factorization;
- the wall splitting coefficient;
- ordered-root diameter inequalities for a finite range of m;
- a distinct degree-four multiplicity pattern;
- coefficient-order witnesses for a finite range of multiplicities;
- a geometric-wall quadratic-opening identity;
- exact Fisher/KKT values at the wall example.

I specifically appreciate that the script labels itself "exact finite regression; not universal proof verification."

That should remain.

The current diagnostics support the absence of elementary algebra mistakes in the displayed examples. They do not address the principal gap identified in Sections 3--4 of this report: the family-resolution and uniform-atlas theorem.

## 14. Build and exact-head reproducibility status

At the time I finalized this report, the exact reviewed head was 5c8b57c655aaec0df76dc3178554de2d1736b076.

The branch contains an exact-head workflow named A2 v97 exact-head manuscript and archive. The workflow is designed to:

- verify the source manifest and addition-only ancestry;
- rerun the exact finite regressions;
- build the principal article;
- build the unchanged v96 archival entrypoint;
- build the assembled complete volume;
- bind the PDFs, logs, and TeX input graphs to the checked-out head.

That design is good.

However, the workflow run visible to this referee at report time was **run 2, status pending, conclusion null**. I therefore do **not** certify an exact-head CI build from this report. The author's local-validation statement says that the principal article compiled locally; the response also correctly says that the archival and complete volumes were not compiled in that local staging directory.

A later successful workflow run would close this reproducibility item. It would not resolve the mathematical objections above.

## 15. Disposition of the v96 requests

My assessment is more differentiated than the response's repeated use of "Answered."

### Substantially answered

- **Source pin / chronology:** yes.
- **G identically zero handling:** yes, now explicit in def:monomial.
- **Encoded algebraic input model:** substantially improved.
- **Article architecture:** yes; the focused principal article is a major improvement.
- **Finite diagnostics in their proper role:** yes.
- **At least one identification wall asymptotically analyzed:** yes.
- **Three meanings of stability separated:** yes, and the distinction is mathematically useful.
- **Root multiplicity and endpoint/interior patterns broadened:** yes, in the full-rank fixed-degree binary class.

### Partially answered

- **Theorem-by-theorem novelty comparison:** improved, but not current-version complete and not yet sharp enough about what is genuinely new beyond finite-candidate wall-chamber theory.
- **Real-accessible cover theorem:** the fixed-centre proposition is much better, but the family version still hides the principal relative-resolution argument.
- **Effective construction:** the input and logical formulas are improved, but the full algorithmic interface is still compressed.
- **Uniform inverse:** stronger and more explicit, but still too terse for its load-bearing role.
- **Connection between valuation and Fisher strata:** a common refinement is stated, but the genuinely difficult parameterized valuation construction is precisely what still needs a full proof.

### Answered in statement, not yet in proof

- **A genuine finite singularity atlas:** revision 97 now states one. This is the most important advance and also the main remaining proof-standard issue.

This distinction matters. A response document is not a certificate of closure; the revised proof must carry each assertion.

## 16. Specific mathematical revisions required for a serious resubmission

I would require the following before reconsidering the manuscript for a top-four general journal.

1. **Replace the proof sketch of lem:relative with a theorem-level relative principalization/spreading argument.** State the algebraic base, the generic construction, the open set on which it spreads, the handling of vertical and special components, and the induction on the exceptional locus. Cite the exact functorial or constructive resolution results used.

2. **Separate the atlas theorem into modular results.** Give one theorem for finite relative monomial data, one for the definable family of joint leading sets, and one for uniform power asymptotics and Nash leading constants.

3. **Update the novelty comparison to the current literature.** In particular, compare to arXiv:2602.18410v2, including Theorems 5.8, 9.9, and 12.3, not only the v1 snapshot.

4. **State the genuinely new output after granting scalar finite-max theory.** The joint feasible weighted initial set, root-set image, exact bottleneck diameter, and remote stochastic wall should be the centre of this comparison.

5. **Expand the rank-crossing local inverse proof.** Turn the affine-pencil approximation and the two endpoint isolation arguments into standalone quantitative lemmas with uniform constants.

6. **Give a standalone remote tangent-cone proposition.** Prove secant completeness, converse arc realization, stochastic feasibility, and the uniform remainder needed for mu_E.

7. **Calibrate the explicit multiplicity theorem's scope in the title, abstract, and introduction.** It is an arbitrary-multiplicity result inside a specific full-rank fixed-degree binary architecture, not an unrestricted singularity classification.

8. **Keep algorithmic evidence separated from mathematical proof.** The current scripts already do this well; the theorem statements should reflect the same discipline.

9. **Obtain and preserve a successful exact-head CI receipt** for the principal, archive, and complete builds before calling the revision reproducibly built.

These are not requests for cosmetic rewriting. Items 1--6 are mathematical proof requirements.

## 17. A more convincing publication route

I see two coherent routes.

### Route A: finish the general atlas theorem

This would justify the current title and broad framing.

The paper would need a self-contained relative theorem roughly of the following form:

> For a fixed-format compact real algebraic or semialgebraic family, after a finite semialgebraic stratification of the parameter base, one has a fibrewise proper real-accessible monomial cover with fixed integer order data and accessibility combinatorics; the joint weighted initial sets form a definable compact family; the spectral diameter admits a uniform power expansion on compact subsets of each stratum.

If this theorem is proved carefully, then the multiplicity atlas and weight wall become compelling explicit cells of a genuine general structure.

### Route B: narrow the paper to what is already strongest

If the authors do not want to build the full relative-resolution machinery, I would narrow the principal paper to:

1. the fixed-centre joint real specialization theorem;
2. a precise current-literature novelty comparison;
3. the full-rank arbitrary-multiplicity and boundary law;
4. the complete rank-deficient cubic fibre;
5. the local Fisher normal form;
6. the weight-wall entrance theorem;
7. the centre-known statistical corollary, briefly.

The general parameter-atlas statement could then be moved to a future paper once its relative proof is complete.

This narrower paper would lose breadth but gain proof density and a much cleaner originality claim.

## 18. Editorial points

The new 21-page principal article is far better organized than the v96 complete article. I would preserve this architecture.

Several smaller changes are still needed.

- Update the Hà reference from v1 to the current v2 and update all theorem-number comparisons after checking the current source.
- Expand the bibliography around parameterized or functorial resolution and definable family asymptotics if those are to be used as infrastructure.
- Define "constant semialgebraic topological type" precisely for the exact target fibre and distinguish it from constant type of the root-multiset image.
- Use "effective" only where the representation transitions are actually specified.
- Keep the sentence saying no complexity bound is claimed.
- Keep the explicit warning that the critical ray t=mu_E delta is not decided by the first-order coefficient alone.
- Keep the distinction between local modulus and whole-model modulus visible in theorem statements.
- Do not let the geometric-wall remark be summarized elsewhere as a second complete wall theorem.
- The exceptionally large numerical local constants are fine as examples, but they should never be presented as evidence for a universal singular mechanism.

## 19. Final assessment

### Correctness

I found no fatal counterexample to the explicit v97 polynomial formulas, the multiplicity and boundary scaling laws, the cubic fibre classification, or the stated weight-wall mechanism. The finite symbolic regressions are consistent with the displayed examples.

The main correctness concern is **proof completeness of the new general family theorem**, not an identified false formula.

### Originality

The strongest distinctive objects are the joint real constrained weighted leading set, its root-set diameter, the explicit stochastic Fisher constants, and the remote exact-fibre entrance law.

The scalar valuation formula and finite wall-chamber rhetoric sit much closer to established and current Łojasiewicz and valuative theory than the manuscript's broad framing sometimes suggests.

### Depth

The cubic wall theorem and joint leading-set construction are serious. The full-rank degree-d theorem is useful and clean but benefits substantially from a coefficient-level Lipschitz inverse.

### Breadth

Revision 97 is broader than revision 96 in a mathematically meaningful way. It now has a general atlas statement and an explicit variable-multiplicity class.

The problem is that the broadest theorem is also the least fully proved part.

### Exposition

Substantially improved. The principal article is now readable as one paper.

### Reproducibility

Good source discipline and sensible exact diagnostics. Exact-head CI was still pending when this report was finalized, so I do not record a successful CI build.

## 20. Bottom line

Revision 97 crosses an important threshold: it is the first revision in this sequence that actually tries to connect the fixed-centre real-valuative construction, parameter stratification, arbitrary multiplicity patterns, and an identification-wall transition in one compact principal article.

That is exactly why the referee standard must now become stricter.

The paper has **stated** a top-four-scale organizing theorem. It has not yet **proved** that theorem at top-four-scale granularity. The generic-fibre resolution and spreading argument, the uniform definable asymptotics, and the current-literature novelty boundary must be made fully explicit.

I therefore recommend **rejection in the present form for a top-four general mathematics journal**, while encouraging a serious resubmission along either Route A or Route B above.

This recommendation should not be read as a claim that the new explicit mathematics is wrong. The revision contains several results that are worth publishing. The issue is that the manuscript currently asks the broad atlas theorem to carry more generality, originality, and algorithmic content than its proof has yet earned.
