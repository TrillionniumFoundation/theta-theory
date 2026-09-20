# Independent harsh referee report on the current A2 v105 revision state

**Manuscript under the latest mathematical revision:** *Intrinsic finite-sheet reduction and reconstruction of metric quotients*  
**Nominal reviewed revision branch:** revision/a2-v105-ramification-native-binary-endpoint-strata-2026-09-20  
**Nominal v105 head:** aa7fbd71a3a8273ca51d91e607d7c43b68da1ef2  
**Last branch containing a substantive mathematical revision:** revision/a2-v104-intrinsic-reduction-endpoint-reconstruction-2026-09-20  
**v104 revision head:** b8c9da734b8ecbadc16ec95c5a8490c7fcf0276a  
**Pinned v104 mathematical/build source:** ff20178a3ac04712ceed5eb333e1ba3e1c518b74  
**Principal article source:** papers/A2-v17-boundary-information-coarsening/article/v104/paper.tex  
**Immediately preceding referee report:** reviews/a2-v104-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md  
**Review branch:** review/a2-v105-independent-harsh-top4-2026-09-20  
**Date:** 2026-09-20

## 1. Recommendation

**Recommendation for an Annals / Acta Mathematica / Inventiones / JAMS-level general mathematics journal: reject in the present state, and do not treat the nominal v105 branch as a substantive revised submission.**

This recommendation has two logically separate components.

First, the repository state does not contain a mathematical v105 revision. A direct comparison of the nominal v105 branch against v104 shows that v105 is ahead by exactly one commit and that the only added file is the previous independent referee report on v104:

reviews/a2-v104-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md.

There are no modified manuscript files, no added v105 article source, no v105 revision package, no v105 response to the v104 referee requests, no new theorem statements, no new proofs, and no new mathematical diagnostics. The head commit itself is titled “Review A2 v104: independent harsh top-four referee report.”

Thus the branch name “v105” is presently a label without a corresponding mathematical revision.

Second, after independently re-reading the actual latest mathematical manuscript, namely v104, I do not find a direct counterexample to its principal theorems. The mathematical work is serious and substantially stronger than earlier versions. But the top-four objection identified at v104 remains entirely unresolved because there is no subsequent mathematics to assess. The manuscript still stops one structural level short of a general intrinsic theory: the finite-sheet theorem is conditional on polar-gap inequalities; the endpoint theorem classifies an open fully visible stratum but not its first singular degeneracies; and the all-dimensional native theorem is exact for a deliberately paired contrast model rather than a natural pre-existing family whose quotient geometry is forced by the original singular observation problem.

The proper editorial conclusion is therefore not “v105 has failed to answer the requests after attempting them.” The more basic conclusion is:

> **No mathematical v105 response has yet been submitted in the repository state reviewed here.**

All unresolved mathematical requests from the v104 report therefore remain open.

## 2. Repository-state audit

The latest nominal revision branch is:

revision/a2-v105-ramification-native-binary-endpoint-strata-2026-09-20.

Its head is:

aa7fbd71a3a8273ca51d91e607d7c43b68da1ef2.

The immediately preceding substantive revision branch is:

revision/a2-v104-intrinsic-reduction-endpoint-reconstruction-2026-09-20.

Its head is:

b8c9da734b8ecbadc16ec95c5a8490c7fcf0276a.

The comparison is unambiguous:

- status: ahead;
- ahead by: 1;
- behind by: 0;
- total new commits: 1;
- mathematical manuscript files changed: 0;
- only new path: reviews/a2-v104-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md.

This is important because the nominal v105 branch name suggests new content in ramification, native binary geometry, and endpoint strata. None of those suggested developments is present as new mathematical source in the branch delta.

A referee should not infer a theorem from a branch name.

Accordingly, the mathematical object reviewed below remains the v104 principal and its seven literal input parts.

## 3. Independent mathematical assessment of the still-current principal

The v104 principal is an 18-page article organized around four substantial mathematical mechanisms:

1. finite-sheet reduction from a polynomial finite map under quantitative polar-gap conditions;
2. a finite moment/tensor lift of the resulting affine residual set;
3. all-dimensional reconstruction of minimal endpoint representations on a fully visible orthant-profile stratum; and
4. an exactly classified paired-contrast stochastic family, together with a local Gaussian experiment interpreting the ray cost.

Appendix A supplies real factorization and positive-time accessibility. Appendix B repairs the clock-pair quantifier in the preserved binary inverse.

This is a coherent article.

It is not, however, yet a general intrinsic classification of the singular observation problems that motivate the program.

### 3.1 Theorem 2.2 is a real reduction theorem, but its decisive hypothesis is itself unclassified

Theorem 2.2 no longer assumes affine sheets. That is a major improvement over earlier versions.

Starting from a polynomial finite map \(F\), it excludes the critical/boundary value set and imposes quantitative conditions on

\[
A_F = DG\,DF^{-1}
\]

and

\[
D_x A_F\,DF^{-1}.
\]

Under

\[
\sup_{\Omega_t}\|A_F\|\le K_0,\qquad
c(t)/r(t)\to0,\qquad
r(t)M(t)\to0,
\]

the manuscript constructs every local inverse sheet, obtains a quadratic Taylor remainder, localizes minimizers, proves a relative comparison with the exact affine-sheet costs, and identifies the complete leading residual set.

I find this mechanism mathematically plausible and useful.

But the polar-gap conditions encode exactly the delicate interaction between ramification of the fast inverse and order of the slow residual. At present they are checked, not intrinsically classified.

The paper can say:

> if the polar-gap inequalities hold, the finite-sheet object follows.

It cannot yet say:

> for a broad natural singularity class, these inequalities are forced by intrinsic ramification/contact data, with a controlled stratification at their boundary.

At top-four level that distinction is decisive.

### 3.2 The weighted-homogeneous corollary and the ramified example are sufficient classes, not the missing classification theorem

Corollary 2.5 gives a broad weighted-initial sufficient class. Example 2.6 is genuinely useful because the target approaches a real discriminant and the inverse branch separations occur at unequal scales.

Neither result classifies the polar-gap regime.

The manuscript still lacks a theorem explaining, in invariant terms:

- which ramification exponents control \(\|DF^{-1}\|\);
- how residual valuations control \(DG\,DF^{-1}\);
- when the second derivative term \(rM\) is forced to vanish;
- stability under admissible perturbations;
- the codimension-one transition where \(rM\asymp1\);
- whether the affine residual object has a canonical nonlinear replacement beyond that wall; and
- how the criterion behaves under a chosen real resolution.

Appendix A proves that relevant semialgebraic suprema have one-variable orders that can be tested. That is not the same as a structural theorem characterizing the geometric locus where the strict inequalities hold.

### 3.3 The tensor lift is clean, but it is downstream of the same conditional bottleneck

The finite moment lift in Section 3 is one of the technically clean parts of the article.

For a finite union of affine sheets, the manuscript gives a closed semidefinite representation of the tensor envelope and identifies the positive-metric exposed faces by nearest points on the minimizing sheets.

I found no direct mathematical objection to that part.

Its limitation is conceptual: the tensor object is intrinsic once the finite-sheet reduction has been obtained, but the article still does not classify when the original singular observation germ necessarily lies in that regime.

### 3.4 The endpoint reconstruction theorem is strong on the fully visible stratum

Theorem 4.3 is a substantial theorem.

Under full visibility, the local Hessians form a Boolean lattice under Loewner order. The largest local matrix gives \(A\); its rank-one covers recover the normalized cross columns; the largest-to-smallest difference reconstructs the normalized endpoint coupling; rank gives the minimal endpoint number; and every competing representation of the same minimal endpoint dimension is forced back into the same visible structure.

The complete minimal-dimensional fibre is then positive diagonal endpoint scaling plus permutation.

That is a meaningful all-dimensional classification.

The problem is not the theorem as stated.

The problem is that the singular boundary of full visibility is exactly where the quotient geometry becomes more interesting:

- active faces disappear;
- local Hessians coalesce;
- endpoints can become indistinguishable;
- minimal dimension can fall;
- nonminimal representations can acquire extra continuous redundancy;
- different cone geometries can produce the same restricted value function.

Proposition 4.5 supplies a finite coordinate-deletion test, but the manuscript correctly concedes that repeated deletion need not produce a global minimum outside the fully visible class.

Thus the general fibre of \(Q\mapsto G_Q\) remains unclassified.

For a paper whose title emphasizes reconstruction of metric quotients, the first nonvisible strata are not peripheral.

### 3.5 The paired-contrast theorem is exact because the model has been designed to linearize the quotient geometry

Theorem 5.1 is elegant and appears internally sound.

The symmetric pair design makes the nuisance-retained Fisher cross block vanish identically, giving

\[
Q(a)=4\sum_j \frac{z_jz_j^{\mathsf T}}{a_j}.
\]

After the reciprocal-mass reparametrization, the quotient image is a linear image of an open set. The dimension, normalized secant sphere, and exact deterministic fixed/adaptive ray complexity therefore reduce to finite-dimensional linear algebra on the span of the rank-one tensors.

This is a complete theorem for the stated family.

It is also precisely why the theorem does not yet solve the natural native-classification problem.

The model was introduced so that the difficult nuisance geometry collapses.

Corollary 5.2 shows that one can realize a neighbourhood of any prescribed positive quotient inside this flexible class. That is a realization theorem. It is not a theorem saying that a natural observation family that independently produced the quotient must have this paired structure or an equivalent canonical quotient geometry.

For a general top-four paper, “every quotient can be realized in an exactly solvable model” is weaker than “a broad natural class has a forced intrinsic quotient classification.”

### 3.6 The local experiment theorem gives the right interpretation but not the missing structural advance

Theorem 6.1 correctly connects the quadratic ray cost with efficient Gaussian discrimination in a finite-alphabet LAN experiment.

The manuscript also correctly separates exact query complexity from sample complexity.

This resolves an interpretive weakness of earlier versions.

The proof uses classical finite-alphabet likelihood expansion, Schur-complement efficient information, whitening, Hellinger affinity, and Neyman–Pearson power. Its value in the paper is explanatory and integrative.

It does not replace the missing geometric classification theorem.

### 3.7 Appendix A substantially improves proof completeness but remains an order-presentation theorem

The real-analytic factorization lemma, proper pruning lemma, and accessible-face construction are valuable.

They repair the danger of substituting complex or formal divisor data for actually feasible positive-time real arcs.

The resulting theorem gives a proper real presentation

\[
t=u r^a,\qquad R=r^bV
\]

and identifies the exact residual order as a maximum of accessible ratios \(b_i/a_i\).

Again, this is a strong scalar-order theorem.

It does not by itself characterize the matrix inverse-derivative quantities that control the polar-gap mechanism.

### 3.8 Appendix B appears to repair the clock-pair quantifier correctly

The corrected statement is existential:

for each fixed clock \(i\), some clock \(j\) separates the two component ratios.

That is the right quantifier.

The compact-uniform conclusion is obtained by a finite cover of locally chosen separating pairs, not by falsely asserting a universal prescribed pair.

I regard this aspect as repaired.

## 4. Proof-level comments that remain important even before the next conceptual theorem

I did not find a direct counterexample to the principal v104 results in this audit.

That is not the same as saying every proof is written at a top-four-ready level.

### 4.1 Parameterized covering/trivialization should be a standalone lemma

The proof of Theorem 2.2 passes quickly from the fixed-\(t\) proper local-diffeomorphism argument to the total map

\[
(t,x)\mapsto (t,F(x)-a(t))
\]

over a variable-radius semialgebraic base.

This should be formalized as a definable covering/trivialization lemma, including:

- the precise domain;
- properness over compact subsets;
- constancy of fibre cardinality;
- treatment of only continuous semialgebraic \(a(t)\) and \(r(t)\);
- definable sheet labelling; and
- the passage to analytic/Puiseux representatives after shrinking the interval.

I believe the step is repairable. It is too compressed for the central theorem.

### 4.2 The minimal-competitor visibility step in Theorem 4.3 deserves its own lemma

The proof uses a sharp counting argument:

- the intrinsic function has exactly \(2^e\) distinct open-cell quadratic polynomials;
- an \(e\)-endpoint representation has at most \(2^e\) active-set polynomials;
- hence every active set must occur;
- full column rank prevents all strict KKT inequalities from degenerating identically on the corresponding open cell.

This is an important structural step.

It should not be compressed into a few sentences in the middle of the reconstruction theorem.

### 4.3 The distance representation should state its ambient dimension convention explicitly

The claim that two factors of a fixed Gram matrix differ by a left orthogonal map requires a clear statement of the minimal ambient factor dimension in which the factor is invertible.

The intended argument is standard once dimensions are fixed.

The manuscript should state them.

## 5. The current v105 state answers none of the v104 referee requests

The preceding v104 report requested seven items.

Because the v105 branch contains no new mathematics, their disposition is straightforward.

| Request from the v104 review | Current v105 disposition |
|---|---|
| Geometric characterization of the polar-gap regime | **Not addressed** |
| Natural unification theorem replacing permissive realization | **Not addressed** |
| First nonvisible endpoint strata | **Not addressed** |
| Native classification for a natural pre-existing model family | **Not addressed** |
| Expanded novelty/priority comparison | **Not addressed** |
| Expanded proof transitions / explicit equivalence conventions | **Not addressed** |
| Successful source-bound native receipt | **Still not closed** |

This is not a matter of my disagreeing with the proposed solution.

No proposed mathematical solution exists in the branch delta.

## 6. Reproducibility status remains open

The source-bound v104 GitHub Actions run remains:

- run: 35509714156;
- workflow: A2 v104 native revision and exact v103 replay;
- head source: ff20178a3ac04712ceed5eb333e1ba3e1c518b74;
- status: pending;
- conclusion: null;
- last recorded update: 2026-09-20T12:07:16Z.

Therefore no durable successful composite native receipt was available at the time of this review.

The manuscript and its revision records have been appropriately cautious about not treating a queued or pending workflow as validation.

That caution should be preserved.

This issue is secondary to the mathematical scope problem, but it remains an open reproducibility item.

## 7. Literature positioning is still too narrow for the breadth claimed

The principal bibliography identifies some classical ingredients:

- real algebraic geometry and semialgebraic preparation;
- real uniformization/normal crossings;
- parametric quadratic programming;
- convex optimization;
- comparison of experiments; and
- LAN/efficient information.

That is enough for basic proof provenance.

It is not enough for a manuscript attempting to span singular inverse geometry, real contact invariants, inverse representation of piecewise-quadratic value functions, semidefinite moment envelopes, information quotients, statistical experiment comparison, and exact quadratic-form reconstruction.

Before top-four reconsideration, the authors should provide theorem-by-theorem positioning against the closest work in each adjacent area and distinguish:

- classical ingredients;
- known special cases;
- known inverse/fibre results;
- genuinely new structural statements; and
- the new contribution of combining the structures.

The manuscript should not rely on the novelty of the vocabulary or the breadth of the program as a substitute for this comparison.

## 8. Required next revision

The next branch should first be a real mathematical revision.

I recommend the following concrete blockers.

### R105.0 — Materialize an actual v105 manuscript before requesting another referee round

A branch called v105 should contain a v105 principal source, revision index, response to the v104 report, and the associated proof/validation materials.

Do not advance the mathematical revision number by adding only a referee report.

This is a provenance requirement, not cosmetic bookkeeping.

### R105.1 — Prove a geometric theorem characterizing the polar-gap regime

This is the highest-priority mathematical request.

The next manuscript should derive the gap conditions from intrinsic ramification/contact data for a broad natural class.

A strong result would relate:

- valuation or polar data of \(F\);
- growth of \(DF^{-1}\);
- valuations of \(G\) along the inverse branches;
- first and second fast-coordinate derivatives;
- admissible tube radius;
- stability under perturbation; and
- the transition locus where the affine reduction ceases to be asymptotically exact.

A theorem giving only another family of hand-checkable sufficient examples would not close the central objection.

### R105.2 — Prove natural unification, not only universal realization

Identify a family of observation models defined independently of the desired quotient geometry and show that its singular germs naturally generate the three structures studied in the paper:

1. the finite-sheet residual;
2. the endpoint quotient; and
3. the native information metric.

The family should not be reverse-engineered by selecting contrast vectors to realize a prescribed \(Q\).

### R105.3 — Classify the first visibility-loss strata

At minimum, treat codimension-one degenerations of the fully visible endpoint class.

The paper should describe:

- which active sets disappear;
- which Hessians coalesce;
- when the minimal endpoint dimension falls;
- the fibre dimension/gauge group on the degenerate stratum;
- whether coordinate deletion detects the degeneration; and
- normal forms for the simplest nonvisible cases.

This is the natural continuation of Theorem 4.3.

### R105.4 — Derive a native tensor/secant theorem for a natural pre-existing model

The paired-contrast family should remain as an exactly solvable benchmark.

The next conceptual step is a comparable theorem for a model that already belongs to the original singular observation program, for example a nontrivial class of the preserved binary polynomial observations.

The point is not merely to obtain full dimension in another example.

The point is to derive the quotient geometry from the model rather than design the model from the quotient.

### R105.5 — State the intrinsic equivalence relation globally

The paper uses several notions of equivalence:

- source reparametrization;
- linear/smooth observation-coordinate covariance;
- endpoint positive diagonal congruence and permutation;
- orthogonal equivalence of distance representations; and
- labelled statistical equivalence by Markov randomizations.

These are related but different.

A top-four treatment should define at the outset what the “metric quotient” object is and which morphisms/equivalences are allowed in each category.

### R105.6 — Expand the two compressed proof transitions

Promote the parameterized covering step and the minimal-competitor visibility step to standalone lemmas, and specify the ambient factor dimension in the distance representation.

### R105.7 — Expand the novelty map

The next revision should contain a real literature section, not only a short list of classical references.

### R105.8 — Close the source-bound runtime item with a successful durable receipt

Do not claim full archival replay until the exact source-bound workflow succeeds and the promised composite receipt, logs, PDFs, and hashes are durable on the revision branch.

## 9. What would change my top-four assessment

A useful next revision is not one that merely makes v104 longer.

The paper would become qualitatively different if it proved a theorem of the following kind:

> For a broad, naturally defined class of singular polynomial observation germs, intrinsic ramification/contact data determine a finite stratification on which the polar-gap reduction, endpoint quotient type, and native information geometry are all controlled; on the principal stratum the quotient is reconstructible, and on the first degeneracy strata the failure modes are classified.

Such a theorem would convert the current article from a collection of strong compatible components into a structural theory.

That is the level of inevitability and conceptual closure I would expect before recommending a general top-four journal.

## 10. Final assessment

The current repository state does not contain a substantive mathematical v105 revision.

The nominal v105 branch adds only the previous referee report on v104.

Accordingly:

- there is no new v105 theorem to validate;
- there is no new v105 proof to audit;
- there is no response to R104.1–R104.7 in mathematical source;
- the latest mathematical manuscript remains v104;
- the principal v104 theorems remain serious and, in this audit, without a direct discovered counterexample;
- the main top-four objection remains conceptual rather than a demonstrated fatal correctness error;
- the missing step is an intrinsic structural classification replacing one more layer of conditionality/realizability;
- the first nonvisible endpoint strata and a natural native-family classification remain open;
- literature positioning remains too thin for the programmatic breadth;
- the source-bound native workflow remains pending with no conclusion.

**Disposition: reject in the present state. The next referee round should begin only after an actual mathematical v105 (or later) manuscript is committed and directly addresses the unresolved structural requests.**
