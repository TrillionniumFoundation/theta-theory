# Independent harsh referee report on A2 revision 98

**Manuscript:** *Projective polynomial observations: joint spectral atlases and a weight-wall transition*  
**Reviewed branch:** revision/a2-v98-relative-spectral-atlas-proof-2026-09-20  
**Reviewed exact head:** 72faee076147dbabd3c50a8cd46390f770102a0e  
**Principal entrypoint:** papers/A2-v17-boundary-information-coarsening/rigidity_v98.tex  
**Principal article source:** papers/A2-v17-boundary-information-coarsening/article/v98/paper.tex  
**Controlling prior report:** review/a2-v97-independent-harsh-top4-2026-09-20  
**Controlling prior review head:** 3b1f657871936a8807f0b3a3b6e86fd75851c9f8  
**Reviewed v97 manuscript head:** 5c8b57c655aaec0df76dc3178554de2d1736b076  
**Date:** 2026-09-20

## 1. Recommendation

**Recommendation for an Annals / Acta / Inventiones / JAMS-level general mathematics journal: reject in the present form.**

Revision 98 is a serious mathematical revision, not an incremental cosmetic response. It directly attacks the principal criticism of my v97 report. In particular, it replaces the former generic-fibre blueprint by a stated spreading lemma and a relative real-principalization theorem; separates the fixed-centre joint initial set from the uniform parameter-family asymptotics; updates the comparison with the current Hà manuscript; supplies a quantitative cross-rank inverse; promotes the remote tangent-cone argument to its own proposition; and improves the weight-wall entrance remainder from the earlier order \(O(\delta^{3/2})\) to \(O(\delta^2)\).

I also do **not** presently have a counterexample to the explicit multiplicity formulas, the cubic exact-fibre classification, the local Fisher constants, or the stated weight-wall mechanism. The finite exact regressions are appropriately labelled as regressions rather than proof certificates, and the source discipline is substantially better than in much earlier revisions.

The negative recommendation therefore has a different basis from several earlier reports.

The paper now asks a genuinely broad theorem to carry the article:

> a fixed-format compact semialgebraic family admits a finite real spectral atlas with fibrewise proper real-accessible monomial data, fixed rational orders, a definable joint leading family, Nash leading diameters, compact-uniform power remainders, and effective algebraic descriptions.

That theorem is close to the natural endpoint of the programme developed in the paper. It is also exactly where the proof remains too compressed for a top-four general journal. The revision has converted a former sketch into a plausible proof architecture, but several of the interfaces in that architecture are themselves nontrivial theorems: spreading a generic resolution certificate with the claimed fibrewise properties, passing from Nash/semialgebraic data to algebraic lifts without losing the real inequality geometry, descending finite algebraic covers with fixed accessibility combinatorics, and turning quantifier-elimination output into the advertised uniform and effective spectral data.

For a specialist journal, one might reasonably ask whether these interfaces can be filled by standard machinery. At the level claimed here, that is not enough. If the finite real spectral atlas is the organizing theorem, then those interfaces are part of the theorem and must be proved or cited in exactly applicable form.

There is a second, independent issue. Even if I grant the general atlas theorem, the manuscript still has not made a persuasive top-four significance case. Much of the general family theorem is assembled from resolution/principalization, real quantifier elimination, Hardt triviality, semialgebraic/Puiseux asymptotics, and finite optimization. The genuinely distinctive mathematics is more specific: the **joint constrained leading coefficient set and its root-multiset diameter**, the explicit multiplicity/Fisher laws in the identifiable binary polynomial experiment, and the **remote-fibre weight-wall transition**. Those are interesting. But the first is currently presented with a very large infrastructure theorem whose novelty relative to established real-algebraic and definable machinery is not yet sharply isolated, while the two explicit model theorems remain confined to a particularly structured finite-dimensional experiment.

I would encourage another serious revision, but not another round of local patching. The authors should either make the relative real-atlas theorem fully reference-grade and sharpen the conceptual theorem that is genuinely new beyond the standard machinery, or narrow the paper around the fixed-centre joint invariant and the explicit multiplicity/cubic/wall results.

## 2. What revision 98 genuinely fixes

The paper deserves credit for substantial progress.

### 2.1 The previous "relative theorem is only a blueprint" objection is materially addressed

Revision 97 had an eleven-step relative-resolution paragraph whose difficult words contained essentially the whole theorem. Revision 98 now introduces:

- Lemma 3.3, the spreading lemma;
- Theorem 3.4, relative real principalization;
- Theorem 4.1, the fibrewise joint initial family;
- Proposition 4.2, semialgebraic decay on strata;
- Theorem 4.3, the uniform spectral power law;
- Theorem 4.4, the finite real spectral atlas.

That modularization is the right response to the previous report.

### 2.2 The literature comparison is much more responsible

The introduction now explicitly grants classical resolution/principalization and scalar divisor-ratio inputs, cites the current v2 of Hà, and distinguishes Theorems 5.8, 9.9, and 12.3 rather than treating wall-chamber language itself as new. In particular, the text acknowledges that Theorem 9.9 already supplies a non-toric finite-candidate chamber principle.

That is a significant improvement in scholarly calibration.

### 2.3 The local inverse through rank changes is now an actual quantitative argument

Proposition 7.2 and Lemmas 7.3--7.4 are much stronger than the corresponding v97 prose. The second marginal is used to obtain a uniform inverse for the competing second channel, the component polynomials are placed near the affine pencil with a controlled error, and separate robust isolation estimates are given near the two pencil endpoints. The final stochastic recovery avoids dividing by \(\det U\).

I regard this as a real repair.

### 2.4 The remote tangent cone is now treated as a theorem rather than a heuristic

Proposition 8.1 gives a local Nash chart at the remote corner, identifies the four one-sided coordinates and seven free directions, proves both secant completeness and converse feasible realization, and writes exact second-order coefficient identities. This is exactly the kind of theorem-level statement requested by the previous report.

The subsequent constrained entrance programme is consequently much better founded.

### 2.5 The stronger quadratic entrance remainder is plausible and useful

The explicit simple/double cluster factorization at the remote point removes the generic order-\(\delta^{3/2}\) coefficient remainder. The identities displayed in the remote chart support the improved
\[
d_{\rm rem}(\delta)=\mu_E\delta+O(\delta^2).
\]
This is a meaningful strengthening, and the paper correctly limits it to the geometry actually proved.

### 2.6 The evidence boundary is much cleaner

The exact SymPy regression record explicitly says that it is not a universal theorem verifier. The local validation record likewise distinguishes the locally compiled principal article from the not-yet-certified archival/complete exact-head products. This is good mathematical hygiene.

These improvements make the remaining objections more, not less, important: revision 98 is now close enough to a serious article that the foundational interfaces should be held to a final-publication standard.

## 3. Main objection I: Lemma 3.3 is now the foundational algebraic-geometric theorem, but its proof still compresses several nontrivial spreading statements

Lemma 3.3 is the load-bearing new result. Its purpose is clear: start with a finite resolution/principalization certificate over the function field \(K=k(S)\), shrink the algebraic base, and obtain a certificate whose smoothness, normal crossings, monomial identities, and covering properties persist fibrewise.

This is the correct strategy. The issue is that the proof currently passes over several steps at exactly the places where a family theorem can fail if hypotheses are not tracked carefully.

### 3.1 The spread of the stratifying chain and its inverse isomorphisms needs a precise theorem

The proof begins with a generic closed chain
\[
Y_{0,K}\supset Y_{1,K}\supset\cdots\supset Y_{q,K}=\varnothing
\]
and projective maps that are isomorphisms over successive differences. It then says that every scheme, morphism, closed immersion, inverse morphism, and unit in the generic certificate is finitely presented, so denominators can be cleared and all identities spread after localization.

At the level of individual equations this is standard. But the statement ultimately needed is stronger:

- the closures chosen over the base have exactly the required fibrewise relation after shrinking;
- the inverse maps remain inverse on the intended fibrewise complements;
- no extra fibre components alter which member of the chain is the first containing a given real point;
- the final finite set of sources still covers the whole retained fibre in the manner later used by Theorem 3.4.

These are not merely equation-spreading statements. They are assertions about a finite stratification by locally closed pieces and its compatibility with specialization.

A publishable proof should either cite a precise spreading-out result for the entire finite diagram or package and prove the needed statement as a separate scheme-theoretic lemma. At present the proof moves from "all data use finitely many equations" to the full fibrewise certificate too quickly.

### 3.2 The reduced/geometrically reduced issue is treated as optional prose although later arguments use fibre components

The proof says:

> "The reduced structure is immaterial to real points; fibrewise reducedness may also be imposed on the generic geometrically reduced pieces after shrinking."

This is not an adequate replacement for tracking the hypotheses actually used later.

Nilpotents do not alter the set of real points, but reducedness and geometric reducedness do matter to:

- the description of irreducible components;
- smoothness of strata;
- statements that a nonzero function cannot become identically zero on a retained fibre component;
- the recursion on vertical and special components;
- the assertion that the chosen closed chain covers all fibre points with the intended dimensions.

The paper should state exactly which objects are replaced by their reductions, when geometric reducedness is imposed, and why the relevant component structure is stable on the retained open set. "May also be imposed" is too weak for a property used by the next theorem.

### 3.3 The blow-up base-change argument is promising but needs a clean algebraic lemma

The most technically valuable paragraph is the one that avoids simply asserting that blow-up commutes with arbitrary base change. The manuscript applies generic freeness to the ambient algebra and to the associated graded algebra, then argues through the \(I\)-adic exact sequences that all quotients are flat and hence powers of the centre ideal commute with passage to fibres.

This is exactly the right issue to address.

However, the final publication should turn this into a self-contained lemma with a precise base ring and module hypotheses. In particular, the reader should be able to verify in one place that:

1. the associated graded algebra is finite type in the required sense;
2. after localization, each relevant graded piece is flat;
3. the induction gives flatness of every quotient used;
4. tensoring the exact sequences preserves the inclusion of \(I^m\);
5. the Rees algebra base change is consequently the Rees algebra of the fibre ideal;
6. the same localization works simultaneously for the finite sequence of subsequent centres.

The present paragraph contains the ingredients, but the reader still has to reconstruct the exact lemma being invoked.

For a secondary technical result this would be acceptable. Here it is one of the central repairs promised in response to the previous referee.

### 3.4 "Bad images have proper closures" has to be checked for each property being globalized

The proof uses Chevalley constructibility and the fact that a constructible dense subset of an integral noetherian space contains the generic point. This is a sensible way to remove bad parameter values without requiring the original family itself to be proper.

But the argument depends on every "bad locus" having empty generic fibre. That needs to be verified for the full list of properties:

- smoothness of each source;
- smoothness of every centre over the base;
- normal-crossing rank and codimension conditions;
- coverage of the chosen finite étale charts;
- invertibility of all declared units;
- persistence of the inverse isomorphism loci;
- nonappearance of a fibrewise identically zero specialization of a function declared nonzero.

The paper currently states that all of these are finite Jacobian/nonvanishing conditions and then removes their image closures. Some are indeed open rank conditions. Others are coverage or component statements. The distinction matters.

I am not claiming that the construction is false. I am saying that Lemma 3.3 is now a theorem whose proof should be written at the level where each of these properties has an explicit algebraic locus and a precise specialization argument.

## 4. Main objection II: Theorem 3.4 still hides the decisive real-semialgebraic-to-algebraic interface

Even if Lemma 3.3 is granted, Theorem 3.4 has to transfer an algebraic generic-fibre resolution into the **real-accessible monomial cover of the original inequality-constrained stochastic graph**.

That is the part most specific to this paper, and it remains too compressed.

### 4.1 The square-slack lift needs a fibrewise equivalence statement, not only a set-theoretic slogan

The proof decomposes the semialgebraic closure into basic closed sets and replaces each inequality \(p\ge0\) by \(p=s_p^2\). It correctly notes that projection of real points of this lift is exactly the basic closed set.

However, the subsequent resolution is performed on algebraic closures and generic fibres. The theorem ultimately needs a uniform statement that, after all spreading, exceptional-set recursion, branch selection, and descent:

- every retained real source point still projects to a point of the original semialgebraic graph;
- every original real graph point in the relevant observation neighbourhood is covered by at least one retained real source;
- no algebraic component introduced solely by closure or by a finite base cover contributes a spurious "real accessible" divisor to the order list;
- strict denominator exclusions and branch inequalities remain enforced.

The proof says that the original sign conditions are "retained throughout", but the mechanism by which they are retained through every algebraic operation should be formalized.

This is not a pedantic request. The difference between a complex/algebraic divisor and a real admissible degeneration is one of the central conceptual points of the manuscript.

### 4.2 The passage from a Nash stratum to an integral algebraic base needs more precise bookkeeping

The proof takes a Nash stratum, passes to the smooth real locus of a Zariski closure, selects an integral algebraic component, and sometimes adjoins algebraic root labels via finite covers.

This is standard technology in spirit, but the theorem claims **fixed source-chart presentations and fixed real-accessibility flags** on the resulting semialgebraic strata. Therefore the paper should explicitly explain:

- how the chosen real Nash branch is embedded into the algebraic base;
- how conjugate or nonreal branches of the finite algebraic cover are discarded;
- how monodromy of root/component labels is handled before claiming a fixed labelled chart list;
- how the order data descends if several algebraic sheets correspond to the same original parameter;
- why the resulting finite permutation quotient preserves the claimed family of leading sets rather than merely their unordered scalar order list.

The current descent paragraph is plausible, but it is not yet a reference theorem.

### 4.3 The treatment of zero functions and vertical components should be separated from the generic argument

Revision 98 explicitly recognizes the key difficulty: a function nonzero on the generic source may become identically zero on a special fibre, and new vertical components may appear. The response is to put all such parameters into the exceptional algebraic set and redo the complete construction by Noetherian induction.

Again, this is the right architecture.

But the proof currently bundles several distinct exceptional phenomena into one sentence. A final proof should state a finite list of exceptional loci and show that each has strictly smaller base dimension. In particular:

- the locus where a spread source acquires an additional vertical component;
- the locus where a declared unit ceases to be a unit;
- the locus where a nonzero function vanishes identically on a fibre component;
- the locus where the chosen finite chart family no longer covers;
- the locus where a real branch/accessibility flag changes.

The entire finiteness of the atlas is obtained by iterating this step. The dimension drop should therefore be auditable rather than implicit.

### 4.4 Real accessibility deserves its own lemma

Definition 3.2 does not count every exceptional divisor; it counts those admitting a real point away from the other divisors and an admissible real transversal with \(G>0\). This is important and, in my view, one of the genuinely useful refinements of the paper.

Theorem 3.4's proof says that existence of such a point is first-order, so one partitions the base by the corresponding conditions, and then an inverse étale chart supplies a real transversal.

This should be extracted as a lemma. It should make explicit:

- the exact first-order condition;
- the dependence on the square-slack lift;
- why the chosen transversal remains in the correct real semialgebraic component;
- why no unrecorded real degeneration can yield a smaller scalar order.

The later "intrinsic scalar orders" corollary depends on precisely this completeness statement.

## 5. Main objection III: Proposition 4.2 and Theorem 4.3 are plausible, but the definable asymptotics package is still compressed into an argument that should be cited or proved at full strength

The parameter-uniform remainder was one of my main objections to v97. Revision 98 now addresses it directly, which is welcome.

Proposition 4.2 says that a nonnegative semialgebraic function \(e(\theta,t)\), tending pointwise to zero as \(t\downarrow0\), can be finitely Nash-stratified so that on each stratum
\[
e(\theta,t)\le t^\nu
\]
eventually, with a positive rational \(\nu\) and a positive continuous semialgebraic threshold. The proof invokes quantifier elimination, the fact that a one-dimensional graph lies locally on a polynomial zero set, one-variable algebraic branch expansions, finiteness of Newton-slope candidates from the finite polynomial support, and semialgebraic choice.

This is believable. But for a theorem carrying the uniform error term in the article's principal atlas, I would require one of the following:

1. a precise citation to an applicable semialgebraic preparation/Puiseux theorem in families, followed by a short deduction; or
2. a more formal proof that specifies the cell decomposition and the finite algebraic branches used.

At present several assertions are compressed:

- after quantifier elimination, the graph may be represented by Boolean combinations of many polynomial conditions; the paper should explain the finite cell refinement on which a single algebraic branch description applies;
- coefficients can specialize to zero, changing the Newton polygon; the argument says this only removes monomials and therefore cannot create new slopes, but the branch selected by the Boolean formula also has to be tracked;
- the eventual-zero pieces and positive branches have to be separated uniformly;
- the semialgebraic threshold selected pointwise must be shown to be positive on the whole stratum before its compact minimum is taken.

None of these looks insurmountable. The problem is one of proof level. The uniform remainder is no longer a side remark; it is a named output of the main theorem.

The same comment applies to the statement that \(C(\theta)\) is Nash after finite refinement. "A semialgebraic function is Nash on a finite Nash stratification" is standard in an appropriate formulation, but the manuscript should cite the precise theorem or state the exact graph-stratification result being used. The one-sentence inverse-function-theorem explanation is too compressed for a flagship assertion.

## 6. Main objection IV: Theorem 5.1 still claims more algorithmic effectivity than the proof has earned

The separation between mathematical existence and executable finite diagnostics is now excellent. Unfortunately the abstract algorithmic theorem itself remains too strong.

Theorem 5.1 says that, for an algebraic input, finite algorithms compute:

- rigidity;
- the exponent;
- quantifier-free presentations of the joint initial sets;
- the root leading set;
- an integer polynomial and rational isolating interval for the leading diameter;
- and, in families, the corresponding strata and formulas.

There are two proposed routes.

### 6.1 The geometric route still requires an explicit algorithmic interface for resolution and spreading

The proof invokes:

- reduced decomposition;
- constructive characteristic-zero principalization;
- the finite spreading charts;
- induction on base dimension;
- real-accessibility elimination;
- finite branch selection and projection.

This may well be algorithmic over an effective characteristic-zero field. But the paper needs exact references or a formal dependency theorem specifying the representations passed from one stage to the next.

"Constructive principalization" is not itself an input-output specification.

For example, if a resolution procedure returns centres over a field extension or after affine chart refinement, the subsequent spreading, real branch selection, and integer-order extraction need to specify how those objects are encoded. The article promises an effective theorem, not merely that each individual operation is known somewhere to be algorithmic.

### 6.2 The semialgebraic-maximum route is cleaner, but "isolate its positive real algebraic branch" is still not an algorithm

The alternative route constructs
\[
m_H(s)=\max\{H(x):G(x)\le s\}
\]
by quantifier elimination and then says:

> isolate its positive real algebraic branch at \(s=0\) and use Newton polygon and real branch selection to obtain its first Puiseux order.

A quantifier-free semialgebraic graph near a boundary point can have several algebraic pieces before one performs a cell/branch decomposition. The algorithm needs to:

1. decompose the graph into finitely many sign-invariant algebraic cells or arcs near \(s=0\);
2. identify the unique branch selected by the graph on each sufficiently small interval;
3. detect the eventual-zero case;
4. compute the first nonzero Puiseux term of each surviving branch;
5. select the actual maximum-function branch;
6. perform the same process uniformly enough to produce parameter strata.

All of this is standardly possible in real algebraic geometry. But the theorem as written skips from quantifier elimination to branch isolation.

The correct repair is straightforward: either provide an explicit algorithmic lemma with references to real-algebraic curve decomposition/Puiseux algorithms, or weaken "finite algorithms compute" to "the objects are effectively definable in the first-order theory of real closed fields, with algebraic specialization computable by standard elimination and real-root algorithms" and carefully state what is actually being promised.

At present the theorem is stronger than the proof.

## 7. Main objection V: the top-four originality case remains unresolved even if the general atlas theorem is granted

This is now a serious editorial issue rather than a wording issue.

The revision has done the right thing by conceding the classical scalar ingredients. Once those are granted, one has to ask:

> Which theorem in this paper would change a specialist's understanding rather than assemble existing machinery for this particular inverse problem?

I see three candidates.

### 7.1 The joint constrained initial set is conceptually the strongest general object

Theorem 4.1 does more than take separate scalar Łojasiewicz exponents. It keeps the centre fixed, rescales all observation and coefficient coordinates simultaneously, takes the real feasible closure, projects to the **joint** coefficient set, and maps that through the clustered root map before taking the exact bottleneck diameter.

That is a meaningful invariant because it preserves relations that separate coefficient envelopes destroy.

In my view this should be the conceptual centre of the paper.

However, the present article still gives substantial rhetorical weight to the existence of a finite atlas itself. Finite stratification, rational exponents, definability, and power-type asymptotics are precisely the outputs one expects after combining resolution with semialgebraic geometry. The paper needs a theorem explaining what the joint object does that cannot be recovered from an existing scalar/definable atlas.

A nontrivial comparison example would help: two families with the same scalar valuation/order data but different joint leading spectral sets or different exact bottleneck constants. Such an example would isolate the new invariant sharply.

### 7.2 The full-rank multiplicity theorem is clean, but structurally favourable

Theorem 6.2 is useful. But its hypotheses deliberately make the coefficient inverse easy:

- two latent components;
- fixed degree;
- coprime component polynomials;
- strict positive weights;
- both channels strictly positive and invertible;
- at least \(2d+1\) exterior clocks.

Lemma 2.2 then gives a Lipschitz inverse for the entire polynomial/stochastic parameter vector. Once this is available, the singular spectral law is largely the geometry of real roots of nearby monic polynomials plus a finite projected Fisher quadratic programme.

The formulas are elegant, but I do not regard this theorem alone as a top-four-level singularity classification. The hard inverse degeneracies have been excluded by hypothesis.

### 7.3 The weight-wall theorem is genuinely interesting but model-specific

Theorem 8.4 is the most distinctive explicit phenomenon in the paper:

- local Fisher conditioning remains finite;
- exact global identification is lost because a remote component enters;
- the entrance scale is linear in the wall parameter;
- the spectral modulus jumps from a local square-root scale to a positive remote distance;
- the nonidentified side opens with a separate square-root root-splitting term.

This cleanly separates local conditioning, multiplicity singularity, and global identification.

I regard this as publishable mathematics.

But it is proved for one rank-one cubic binary pencil geometry. The geometric wall is explicitly left without a complete two-scale theorem, and no general theorem classifies remote-fibre entrances for broader rank-deficient polynomial experiments.

For a top-four journal, either this mechanism has to be developed into a broader structural theorem, or the paper has to be presented as a focused high-quality contribution about this specific model rather than as a general real spectral atlas theory.

## 8. Detailed assessment of the explicit multiplicity theorem

I rechecked the main scaling logic in Theorem 6.2.

For a repeated interior cluster, the order-\(\sqrt t\) centred root splitting contributes an order-\(t\) second elementary symmetric coefficient. The observation map is coefficient-Lipschitz in the full-rank regime, so the Hellinger radius \(t\) indeed corresponds to a root scale \(\sqrt t\). The projected quadratic programme and the formula
\[
C=\max_j 2\sqrt{\frac{m_j-1}{m_j}}\,\kappa_j^{-1/4}
\]
are consistent with the ordered zero-sum cluster diameter.

For endpoint clusters, one-sidedness forces the sum of displacements to control the individual root shifts, so the linear root scale is plausible.

The general coefficient-order formula
\[
\beta_1=1,\qquad \beta_k=k/2
\]
for interior clusters and \(\beta_k=k\) at an endpoint is also consistent with the explicit realizing arcs.

I therefore do **not** base this report on an alleged algebraic error in Theorem 6.2.

My remaining requests are about presentation and scope:

- explicitly call this the fixed-degree, full-rank, coprime binary multiplicity theorem whenever it is summarized;
- keep the distinction between whole-model competitors and a fixed root-pattern stratum visible;
- retain the proof that the leading set is jointly constrained rather than a product of marginal cluster balls;
- do not use this theorem as evidence that arbitrary rank-deficient or multi-component singularities have been classified.

## 9. Detailed assessment of the cubic fibre and cross-rank inverse

Theorem 7.1 and the subsequent inverse lemmas are a considerable improvement over earlier versions.

The exact fibre argument at rank-one \(U\) reduces competitors to the affine pencil and uses the discriminant/root geometry plus the weight floor. The realization of the remote component by changing the second-channel mixture is explicit. The two wall quantities \(B\) and \(E\) therefore have a clear geometric role.

Proposition 7.2 also gives a credible route from observation closeness to an approximate affine pencil without a lower bound on \(|\det U|\). Lemma 7.3 then supplies two separate isolation estimates near the two exact pencil endpoints, including the depressed-cubic real-rootedness inequality near \(c=1\).

I do not presently see a direct contradiction in these arguments.

For final publication I would nevertheless tighten two points.

First, the matrix dimensions and singular-value convention in the second-marginal argument should be made explicit. The inequality used to infer a lower bound on the smallest singular value of \(V'\) is correct only with the exact row/column convention and the appropriate operator norm on the remaining factor. This is easy to state and would remove avoidable ambiguity.

Second, Lemma 7.4 should explicitly say that the coefficient neighbourhood is chosen after fixing the component permutation and that the dual coefficient functionals are uniformly bounded on the stated compact family. The proof uses both facts, and they are available from the hypotheses.

These are not rejection-level objections.

## 10. Detailed assessment of the remote corner and entrance law

The remote analysis is now one of the strongest sections.

Proposition 8.1 does what the v97 report requested: the tangent cone is not guessed from first-order inequalities but derived from a local feasible coordinate chart, and every cone vector is realized by an exact feasible arc. The explicit product identities justify the \(O(\tau^2)\) coefficient remainder.

Lemma 8.2 then separates the base derivative \(B_0\) from the remote score cone. The obstruction
\[
\pi t_h+c_*k=-1
\]
is an effective way of proving that the centre's wall-crossing direction cannot be reproduced by a feasible remote tangent.

The resulting programme for \(\mu_E\) is finite dimensional and the positive minimum is conceptually clear.

Theorem 8.4's localization argument is correspondingly convincing: compactness excludes all competitors outside the two wall representatives; the remote local inverse forces a minimizing competitor into \(O(\delta)\) chart coordinates; Taylor expansion gives the linear entrance plus quadratic error.

Again, I do not base the rejection on a counterexample to this theorem.

The limitation is breadth. The paper itself correctly says that the geometric \(B=0\) wall has a different cone and is not covered by the complete entrance theorem. That honesty should be preserved throughout the abstract and introduction.

## 11. The centre-known minimax corollary is correct in spirit but should not carry significance weight

The statistical corollary is explicitly centre-known and local. The lower bound is a two-point Hellinger/TV argument and the upper bound is a constant decision over the specified local ball.

This is fine as a corollary connecting the spectral modulus to a statistical risk scale.

It is not an adaptation theorem, an honest confidence theorem, or a minimax theorem over an unknown singularity class. The text already says so. I would keep it brief and avoid using it in the journal-significance pitch.

## 12. The exact finite regressions are useful and appropriately limited

The v98 exact diagnostics check, among other things:

- the cubic discriminant factorization;
- the remote double-root factorization;
- the pencil-ratio derivative;
- the two explicit second-order remote coefficient identities;
- depressed-cubic algebra;
- multiplicity witnesses and ordered-diameter inequalities over a finite range;
- three explicit Fisher programmes;
- the remote four-variable constrained programme and a positive exact \(\mu_E^2\).

These are useful regression tests. They reduce the risk of a transcription or finite algebra error in the displayed examples.

They do not verify:

- Lemma 3.3;
- Theorem 3.4;
- Proposition 4.2;
- Theorem 4.3;
- Theorem 4.4;
- the universal fixed-degree statement for arbitrary \(d\);
- the effectivity theorem.

The repository and manuscript now say this clearly. That distinction should remain.

## 13. Reproducibility status at the reviewed exact head

The reviewed exact head is
72faee076147dbabd3c50a8cd46390f770102a0e.

The local validation record reports a 26-page principal build with no recorded TeX warnings and records hashes of the principal inputs and products. It also explicitly records:

- scope: local staging, not a Git checkout;
- checkout head: null;
- CI run id: null.

The branch contains an exact-head GitHub Actions workflow intended to:

- audit the exact source head and preservation constraints;
- rerun the v97 and v98 finite exact regressions;
- compile the v97 principal/archive and the v98 principal/archive/complete products;
- bind the resulting PDFs, logs, and recorder input graphs to the checked-out head.

At the time I finalized this report, workflow run **35483001933**, run number 2, was **pending** with no conclusion.

Accordingly, I do not certify an exact-head remote build of the archive and complete volume in this report. A successful later run would close this reproducibility item. It would not resolve the mathematical and significance objections above.

## 14. Disposition of the v97 referee requests

The v98 response is substantially more successful than earlier response matrices. My assessment is as follows.

### Substantially answered

1. **Separate the relative theorem, joint family, and uniform asymptotics:** yes.
2. **Update the comparison with current Hà, including Theorem 9.9:** yes.
3. **State the additional invariant after granting scalar theory:** substantially yes.
4. **Expand the cross-rank inverse:** yes.
5. **Promote the remote tangent cone to its own theorem:** yes.
6. **Keep the multiplicity theorem's explicit scope:** mostly yes.
7. **Separate executable diagnostics from universal proof:** yes.
8. **Strengthen the remote entrance analysis:** yes, beyond what was requested.

### Improved but not fully closed at top-four proof standard

1. **Relative principalization/spreading:** the paper now has the right theorem architecture, but the algebraic spreading and real descent interfaces remain too compressed.
2. **Uniform family remainder:** an explicit proposition now exists, but it needs a reference-grade semialgebraic preparation/branch argument.
3. **Effectivity:** substantially clarified, but the theorem still outruns the formal algorithmic interface.
4. **Top-four originality positioning:** improved literature comparison does not by itself establish that the finite-atlas theorem, as opposed to the joint invariant and explicit wall phenomenon, is a sufficiently new general theorem.

### Not yet evidenced at report time

- **Successful exact-head CI build of principal/archive/complete products:** the workflow exists, but the visible run was still pending.

The response should therefore not describe all nine prior requests as "closed" without qualification.

## 15. Specific revisions I would require before reconsideration at a top-four general journal

The next revision should not add another layer of broad claims. It should finish the proof interfaces already introduced.

### R1. Turn Lemma 3.3 into a reference-grade spreading theorem

State the base ring, finite-type hypotheses, reductions, geometric reducedness assumptions, centre ideals, and exact base-change lemma for the successive blow-ups. Give exact citations for generic freeness and any resolution/principalization functoriality used. Separate equation-spreading from fibrewise coverage and component control.

### R2. Formalize the real algebraization and descent step

Give a theorem or lemma showing that the square-slack algebraic lifts, finite algebraic root-label covers, Nash branch selections, and subsequent resolutions produce exactly the intended real semialgebraic fibrewise cover. Track sign conditions and denominator exclusions through the construction.

### R3. Isolate zero specializations and vertical components

List the exceptional loci explicitly and prove strict base-dimension descent for each. Do not hide all specializations under one generic "recompute on the exceptional set" sentence.

### R4. Give a standalone real-accessibility lemma

The finite order list is only intrinsic if every order-relevant real degeneration is represented and every recorded divisor has a genuine admissible real transversal. State and prove that completeness cleanly.

### R5. Replace the compressed proof of Proposition 4.2 with a standard preparation theorem or a full branch decomposition

The parameter-uniform power remainder is a central theorem output. It should rest on a precise, citable semialgebraic/o-minimal preparation statement or a detailed finite cell/Puiseux argument.

### R6. Narrow or fully formalize Theorem 5.1

Either:

- provide exact algorithmic references and data representations for every step of the geometric and semialgebraic routes; or
- weaken the theorem to effective definability plus explicit algebraic specialization, which is closer to what the present proof directly establishes.

### R7. Demonstrate that the joint leading set contains information not reducible to the scalar atlas

A concrete theorem or example with identical scalar exponent/order data but different joint feasible spectral limits would materially strengthen the originality case.

### R8. Broaden the remote-wall theorem or narrow the paper's top-level framing

A top-four case would be stronger if the remote-fibre entrance theorem were extended to a structural class of rank-deficient polynomial experiments or to both principal wall mechanisms. Otherwise the article should be framed as a focused study of the joint invariant and this explicit model rather than a general singularity atlas.

### R9. Preserve an exact-head successful CI receipt

The principal, archive, and complete products should be built from the exact reviewed commit with source-input hashes and successful workflow status preserved in the repository.

## 16. A publication route I would find more convincing

I see two coherent routes.

### Route A: finish the general atlas theorem completely

Keep the current title and broad architecture, but make the actual mathematical centre a theorem of the following strength:

> After a finite semialgebraic stratification of a fixed-format compact real-algebraic/semialgebraic family, there exists a fibrewise proper real-accessible monomial cover with fixed order combinatorics; the fibrewise joint weighted initial sets form a definable compact family; their root-multiset images have a Nash leading diameter and a compact-uniform power remainder.

Then prove every transition in that sentence at reference level.

To justify a top-four venue, add a theorem showing that the joint initial set is a genuinely stronger invariant than all scalar valuation data, not merely a convenient container for them.

### Route B: narrow to the strongest model-specific mathematics

Remove the general family-effectivity theorem from the principal burden and centre the paper on:

1. the fixed-centre joint real specialization theorem;
2. the full-rank multiplicity/boundary law;
3. the complete rank-deficient cubic fibre;
4. the uniform local inverse through rank changes;
5. the local Fisher normal form;
6. the remote tangent cone;
7. the weight-wall entrance theorem;
8. the contrast between multiplicity crossover and remote identification loss.

This would be a much tighter paper. It would give up the claim of a universal finite spectral atlas, but every main theorem would be close to the actual explicit mathematics developed in the article.

For a specialist journal, I would presently prefer Route B. For a top-four general journal, Route A would need to be completed at a substantially higher proof and conceptual level.

## 17. Editorial and expository comments

The principal 26-page article is much better structured than the older accumulated volumes. I recommend preserving that scale.

Several smaller changes would improve it further.

- In the abstract, "finite relative real monomial presentation" currently sounds like an established theorem at the same confidence level as the explicit cubic formulas. Until Lemma 3.3/Theorem 3.4 are fully closed, this is the most vulnerable phrase.
- Define "finite algebraic étale coordinate presentation" once with an exact encoding convention if it is also used in the effectivity theorem.
- State explicitly whether all algebraic bases and covers are over \(\mathbb Q\), a fixed real algebraic extension, or a general effective characteristic-zero field at each stage.
- Distinguish fibrewise proper source maps from the smaller coordinate boxes used for unit bounds; the text mostly does this already.
- Keep the warning that Hardt triviality supplies topology, not a metric rate.
- Keep the warning that no general leading set is asserted to be quadratic.
- Keep the local/whole-model modulus distinction visible in theorem headings.
- Keep the critical-ray remark: the sign of the higher-order correction should not be decided by convention.
- Do not summarize the geometric-wall remark as a second completed wall theorem.
- The very large numerical Fisher constants are acceptable examples, but they are conditioning diagnostics, not evidence for general singular behaviour.

## 18. Final assessment

### Correctness

The explicit model calculations are substantially more convincing than in earlier revisions. I found no direct counterexample to the multiplicity theorem, cubic fibre classification, local Fisher law, or weight-wall entrance mechanism.

The main correctness concern is **proof completeness of the general relative real-atlas theorem and its effectivity/uniformity interfaces**, not an identified false finite formula.

### Originality

The most original-looking object is the joint real constrained leading spectral set and its exact bottleneck diameter. The remote-fibre weight-wall transition is also conceptually distinctive.

By contrast, finite stratification, rational orders, semialgebraic wall chambers, and power asymptotics themselves sit close to established resolution and definable geometry. The article should not ask those words alone to carry the novelty claim.

### Depth

The cubic rank-loss and remote-wall analysis has real depth. The relative family theorem could also have substantial depth, but only if the current compressed interfaces are fully made into mathematics rather than treated as infrastructure that specialists will supply.

### Breadth

The abstract framework is broad. The strongest fully explicit theorems remain in a two-component fixed-degree polynomial observation architecture, with the most interesting wall theorem proved for one cubic rank-one family.

### Exposition

Substantially improved. The current principal article is readable as a coherent paper rather than a repository history.

### Reproducibility

The source and finite diagnostics are disciplined. The exact-head remote workflow was still pending at the time of review, so full build certification remains open.

## 19. Bottom line

Revision 98 is the strongest revision of this A2 line that I have reviewed. It responds seriously to the previous report and, importantly, does not merely rename the old gaps.

That progress changes the nature of the editorial decision but not the decision itself.

The paper now has a plausible high-level theorem architecture and several strong explicit model results. What it still lacks is the final level of proof granularity and conceptual separation required for a top-four general mathematics journal. The relative algebraic spreading theorem, the real-accessible descent, the uniform semialgebraic asymptotics, and the claimed algorithmic effectivity must be made reference-grade. Separately, the article must demonstrate that its general joint spectral invariant yields a genuinely new structural theorem beyond what standard resolution/definability machinery already predicts.

I therefore recommend **rejection in the present form**, with encouragement to resubmit only after a structural revision along Route A or Route B above.

This recommendation should not be interpreted as a claim that the explicit v98 cubic or wall mathematics is wrong. On the contrary, those sections are now the strongest reason to continue the project. The issue is that the manuscript's broadest theorem still asks the reader to accept several deep interfaces at a level of compression that is below the standard set by the journal class being targeted.
