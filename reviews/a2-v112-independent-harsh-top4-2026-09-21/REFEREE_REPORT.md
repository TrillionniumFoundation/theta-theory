# Independent harsh referee report on A2 revision 112

**Repository:** `TrillionniumFoundation/theta-theory`  
**Revision reviewed:** `revision/a2-v112-components-schemes-quantitative-experiments-2026-09-21`  
**Mathematical source commit bound by the revision receipt:** `0c696736e6ec22259c730672f61ebd8ef0d95460`  
**Controlling previous review:** `review/a2-v111-independent-harsh-top4-2026-09-21`, commit `cafc6c1bd403dae4acc66177fb43feee54c02b1d`  
**Principal manuscript:** `papers/A2-v17-boundary-information-coarsening/article/v112/paper.tex`  
**Title:** *Recovery of information metrics: multiplication failure schemes*  
**Referee standard:** general top-four mathematics journal (Annals / Inventiones / JAMS / Acta level)  
**Recommendation:** **Reject in the present form at a general top-four journal.**

## 1. Executive assessment

Revision 112 is a substantial mathematical improvement over revision 111. It does not merely add examples or patch individual referee bullets. The new Section 5 attempts a genuine structural theorem for the multiplication-failure scheme: in the stable range it identifies the full-rank component, the signed rank-two secant components, the wall between the two codimension mechanisms, Cohen--Macaulayness in expected codimension, generic reducedness, and the resulting cycle class. The residual ((k-2,c-1)) multiplication map gives a real geometric/deformation interpretation of the wall. On the statistical side, the former weak local-limit argument has been replaced by a quantitative jittered-Poisson total-variation comparison and a deterministic finite-precision alternative.

These are the right kinds of changes.

Nevertheless, the manuscript still does not meet a general top-four standard. The problem is no longer that the paper lacks a nontrivial theorem. It now has one. The problem is that the theorem remains too special, too incompletely developed at its singular/intersection boundary, and too weakly situated in the full literature to support the venue claim. The paper also continues to combine two largely separable stories: a specialized algebraic-geometric classification of quadratic multiplication failure for binary linear series, and an engineered known-mark local Gaussian/Poisson score experiment. The second story uses the first as a rank criterion, but it does not elevate the first into a broader principle; conversely, the algebraic geometry does not need most of the statistical development.

I do **not** see an immediate one-line counterexample that invalidates Theorem 5.1. The incidence counts, Eagon--Northcott purity argument, corank-one chart, and residual multiplication calculation are substantially more coherent than in the previous revision. My recommendation is therefore not based on an identified fatal false statement. It is based on (i) proof-completeness demands that are still too compressed for the strength of the scheme-theoretic claims, and, more importantly, (ii) significance, generality, priority, and conceptual-unification deficiencies relative to a top-four bar.

For a strong specialized journal in algebraic geometry, algebraic statistics, inverse problems, or mathematical statistics, this revision is materially closer to a viable paper than v111. For a general top-four journal, it still needs another conceptual layer.

---

## 2. What v112 genuinely fixes

The previous review asked for a structural explanation of the two branches in
[
operatorname{codim}Delta^{(L)}
=min{Linom{c+1}{2}-(2k-1)+1,;Lc-3}.
]
Revision 112 responds in a serious way.

The new theorem introduces
[
a=Linom{c+1}{2}-2k+2,qquad b=Lc-3,
]
and, under (cge 8), (kge 2c+1), (Linom{c+1}{2}ge2k-1), claims:

1. if (a<b), the maximal-minor scheme is integral and Cohen--Macaulay, supported on a nondegenerate-Hankel component (Phi_L);
2. if (a=b), the whole scheme is reduced Cohen--Macaulay with exactly (1+2^{L-1}) components, one full-rank component and (2^{L-1}) signed secant components;
3. if (b<a), the signed secant varieties are exactly the maximal-dimensional components;
4. in expected codimension, the cycle is the Thom--Porteous class (c_a(mathcal E^*)).

This is qualitatively stronger than the v111 codimension theorem plus one common-secant component.

The signed secant construction is also the correct refinement of the old common-secant picture. For a rank-two annihilator, the two isotropic hyperplanes produce independent (pm) choices at each contact, modulo simultaneous interchange. The residual identity
[
a-b=Linom{c}{2}-(2k-5)
]
then identifies the rank-two tangent calculation with saturation of multiplication by the residual ((c-1))-planes in a ((k-2))-dimensional binary space. This is the best conceptual idea in the revision.

The statistical repair is also real. Lemma 10.1 now proves a quantitative (L^1)/total-variation approximation for jittered Poisson counts, and Theorem 10.3 gives a deterministic quantized protocol with error
[
O!left(N^{-1/5}+rac{1}{sqrt N,eta_N}+eta_Night).
]
This closes a genuine gap from v111, where a weak Gaussian approximation was carrying a stronger Le Cam conclusion than had been proved.

Finally, the process separation is good: proof sources, response letter, literature audit, build receipts, and finite diagnostics are kept outside the mathematical article. The source-bound receipt also makes clear that successful compilation and finite tests are not formal proof certificates.

---

## 3. Principal top-four blocker: the structural theorem is still too special

Theorem 5.1 is now the paper's real theorem. The entire venue assessment should therefore be made by asking what mathematical principle it reveals.

At present the theorem is still tied to all of the following simultaneously:

- binary forms / (mathbb P^1);
- quadratic multiplication (operatorname{Sym}^2 U);
- Hankel/catalecticant annihilators;
- a product of independent Grassmannians;
- the stable range (cge8), (kge2c+1);
- the expected-codimension regime for the complete scheme statement.

This is a substantial special-case theorem, but a general top-four paper normally needs either much broader scope or a classification so complete and unexpected that the special case itself becomes a model theorem of independent interest.

The present paper does not yet explain whether the two-branch phenomenon is:

- specific to quadratic multiplication of binary forms;
- a general secant-versus-determinantal principle for (operatorname{Sym}^m U);
- a feature of projections of rational normal curves;
- a manifestation of a broader apolarity/catalecticant stratification;
- or the first case of a higher-dimensional/higher-degree theory.

The manuscript explicitly declines the higher-product direction. That is a legitimate authorial choice, but it leaves the top-four significance problem unresolved.

A serious next step would be one of:

1. extend the component mechanism to (operatorname{Sym}^m U	o H^0(mathbb P^1,mathcal O(mn))) for (mge3);
2. formulate and prove a version for higher-dimensional source varieties / Veronese-type multiplication;
3. identify an invariant categorical or deformation-theoretic principle from which the rank-two/full-rank dichotomy follows;
4. remove most of the stable-range restrictions and classify the exceptional low-dimensional behavior.

Without something of this scale, the theorem reads as a strong specialized classification, not a general mathematical breakthrough.

---

## 4. The “failure schemes” story is incomplete exactly where the geometry becomes most interesting

The title now foregrounds schemes, and Theorem 5.1 makes scheme-theoretic claims. But the scheme is only structurally understood in the easiest part of its geometry.

### 4.1 Expected-codimension regime

When (ale b), Cohen--Macaulayness follows from the expected grade of the maximal-minor ideal, and generic reducedness on all minimal components is then used to deduce reducedness. This is a reasonable argument.

But at the wall (a=b), where there are (1+2^{L-1}) components, the manuscript says almost nothing about how these components meet.

That omission is not cosmetic. The intersections are where the singularities and the real geometry of the wall live. A top-level structural theorem should address at least some of:

- pairwise intersections (Sigma_arepsiloncapSigma_{arepsilon'});
- intersections (Phi_LcapSigma_arepsilon);
- codimensions of these intersections;
- tangent cones / local equations at generic intersection points;
- whether the scheme is normal, seminormal, or has normal-crossing-type behavior on a dense boundary stratum;
- the singular locus of (mathscr D_L);
- whether the signed components have a combinatorial intersection complex indexed by sign patterns.

At present the theorem classifies minimal components but leaves their interaction essentially untouched. For a paper titled *multiplication failure schemes*, this is the next natural theorem, not an optional appendix.

### 4.2 Excess regime

When (b<a), the paper classifies only maximal-dimensional components and explicitly leaves open:

- smaller components;
- embedded structure;
- unmixedness;
- global singularities.

That is an appropriate disclaimer, but it means the scheme-theoretic story stops exactly when expected codimension fails.

For a specialized journal this may be acceptable. For a top-four claim, the excess regime should either be classified or replaced by a theorem explaining the entire associated-prime / excess-intersection structure.

---

## 5. The proof of Theorem 5.1 needs a more explicit global incidence argument

I do not currently see a contradiction in the proof, but several decisive steps are compressed enough that I would not accept them in final top-four form without expansion.

### 5.1 From rank-gap estimates to the complete list of minimal components

The proof uses:

- expected-codimension purity from Eagon--Northcott;
- the strict rank-gap lemma;
- irreducibility of the full-rank incidence;
- the signed rank-two incidences;
- generic corank-one smoothness.

The intended conclusion is that every minimal component is one of (Phi_L) or the (Sigma_arepsilon).

This is plausible, but the manuscript should state and prove a clean proposition of the following form:

> Every irreducible component of the support has a dense open subset on which the maximal rank of an annihilator is constant, and the corresponding component is dominated by the appropriate rank-(r) incidence.

The current proof moves directly from the dimension inequality for pair incidences to a statement about generic annihilator ranks on components. That is standard reasoning, but for a theorem claiming an exact list of all components and reduced scheme structure it should be written without any inferential shortcuts.

### 5.2 Birationality of the nondegenerate component

For (Phi_L), the manuscript argues that the full-rank incidence and its image have the same dimension, hence the generic fibre is zero-dimensional; since the fibre is the full-rank open subset of a projective annihilator space, the generic multiplication corank is one, hence the fibre is a point.

Again, the idea is sound. But this is a key theorem, so I would separate it into an explicit lemma:

- establish generic finiteness;
- prove the generic annihilator space is exactly one-dimensional;
- prove degree one of the incidence projection;
- state clearly what happens on the boundary where the full-rank annihilator degenerates.

The present paragraph is too compressed relative to the importance of the claim “(mathfrak F_L	oPhi_L) is birational.”

### 5.3 The confluent rank-two boundary is swept under the generic rug

The signed components are parametrized on the dense open set of two distinct evaluation points. The manuscript correctly says that confluent rank-two forms lie in a lower-dimensional subset and cannot affect generic assertions.

That is enough for birationality of the components. It is **not** enough for a complete structural understanding of the wall scheme. The confluent boundary is a natural candidate for component intersections and enhanced singularity. It should be analyzed rather than repeatedly dismissed as lower-dimensional.

### 5.4 The reduction “Cohen--Macaulay + generically reduced = reduced” should be localized explicitly

The statement is correct under the no-embedded-primes/(S_1) hypothesis supplied by Cohen--Macaulayness, but this is central to the claim that the whole equality-case scheme is reduced. Give the exact commutative-algebra lemma, state the minimal primes, and apply it chartwise/globally. Do not leave this as a one-sentence bridge in the proof of the main theorem.

---

## 6. The residual wall is the strongest idea and should be developed much further

The identity
[
a-b=Linom{c}{2}-(2k-5)
]
and the reduction from a general rank-two signed component to multiplication of residual ((c-1))-planes in dimension (k-2) is the conceptual center of the paper.

At present it is used mainly to compute the tangent dimension and prove generic smoothness.

That is not enough.

The residual construction should be promoted into a reusable geometric mechanism. In particular:

- Does it iterate at higher-rank degenerations?
- Can it describe intersections of signed components by successive residualization?
- Can it explain the singularity type when residual multiplication is itself on its failure locus?
- Is there a stratified recursion by Hankel rank?
- Can it recover the full low-dimensional exceptional behavior rather than requiring (cge8)?

If the authors can turn the residual wall into an actual recursive theory of the failure scheme, the paper could become much more important.

In the current version, the most original mechanism appears once, solves one generic tangent problem, and stops.

---

## 7. The stable-range hypotheses look like proof technology rather than natural geometry

The structural theorem assumes
[
cge8,qquad kge2c+1.
]

These conditions are used to make the strict rank-gap inequalities clean and to avoid the two-component maximal orthogonal Grassmannian cases.

But the paper does not convincingly explain whether these are:

- sharp;
- close to sharp;
- merely convenient;
- or hiding genuinely different geometry.

A top-four treatment should classify the excluded cases, not simply move them outside the theorem.

At minimum, I would require:

1. an exact list of exceptional triples/ranges where intermediate Hankel ranks can tie the extremal dimensions;
2. a statement of what happens when (k=2c) or near the maximal-isotropic boundary;
3. a description of how the two orthogonal-Grassmannian components affect the full-rank incidence;
4. examples showing genuinely new components or proving that the theorem extends after finite corrections.

The wall case itself is also arithmetically sparse:
[
a=b
quadLongleftrightarrowquad
2k-5=L,rac{c(c-1)}2.
]
The manuscript should discuss when this can actually occur and what the neighboring regimes look like. The current exposition treats the wall as a continuous phase boundary without discussing the arithmetic restrictions on integral parameters.

---

## 8. The cycle formula is classical and currently underexploited

Once expected codimension is proved, the formula
[
[mathscr D_L]=c_a(mathcal E^*)
]
is a classical Thom--Porteous application.

That is fine, and the paper correctly does not oversell it.

But if the cycle is going to appear in the abstract as part of the structural result, more should be extracted from it.

For example:

- compute explicit degrees with respect to natural Plücker polarizations;
- decompose the wall cycle into the class of (Phi_L) plus the (2^{L-1}) signed component classes;
- determine whether all signed components have the same class;
- compare the full-rank and rank-two component degrees;
- identify enumerative consequences.

At present the cycle formula is a short classical corollary rather than a new piece of geometry.

---

## 9. The local conditioning exponent is correct-looking but not a top-four probabilistic theorem

Corollary 5.8 proves, near a fixed smooth real corank-one point, that
[
gamma_{m mult}asymp operatorname{dist}(A,|mathscr D_L|)
]
and therefore a bounded-density law in a fixed coordinate box has
[
Pr{gamma_{m mult}learepsilon}asymp arepsilon^{operatorname{codim}}.
]

This is a useful local consequence of smooth transversality. It is not a global random-conditioning theorem.

The constants depend on:

- a fixed chart;
- a fixed sign chamber;
- a fixed compact closure;
- the chosen smooth stratum.

No dimension-uniform law, global sampling model, or control near component intersections is proved.

This only partially addresses the robustness direction raised in the previous report. A genuinely strong contribution would give a natural random-design model and quantitative tails that see the stratified failure geometry globally.

---

## 10. The statistical section is repaired technically but remains conceptually auxiliary

The Poisson and finite-precision arguments are much better than in v111. I would no longer object that the Le Cam claim rests only on weak convergence.

But the conceptual limitation remains.

### 10.1 The target experiment is deliberately engineered

The local submodel
[
lambda_N(h)=lambda^0+N^{-1/2}B_*h,
qquad
B_*=Lambda D^{mathsf T}Sigma^{-1},
]
is a least-favourable/right-inverse construction chosen so that (DB_*=I).

The resulting Gaussian experiment
[
Zsim N(h,Sigma)
]
and the information projector after applying the contact operator are then standard finite-dimensional Gaussian compression facts.

This is legitimate and clean, but it is not an intrinsic observation theory forced by the physical model.

### 10.2 The full exposure “quotient” should be formalized or renamed

Proposition 10.4 is careful to say that no kernel reconstructs the unknown nuisance from (Z). Good.

But “quotienting the limit experiment by translations of this unrestricted nuisance” is informal language unless an explicit quotient category/equivalence notion for experiments is defined.

For a final paper, either formalize the quotient operation or state more concretely:

- the Gaussian limit decomposes into independent target and nuisance coordinates;
- the contact statistic acts only on the target coordinate;
- after ignoring nuisance by design, the target experiment is (N(h,Sigma)).

### 10.3 The finite-precision theorem is a technical repair, not a conceptual advance

Theorem 10.3 elegantly removes the lattice-injectivity pathology without analyst-added observation jitter. But it remains a discretization theorem for a chosen score map.

It does not make the contact statistic physically intrinsic, solve unknown-mark sufficiency, or produce a new nonregular minimax regime controlled by the algebraic failure geometry.

Thus the statistical section is now defensible, but it still does not raise the algebraic theorem to top-four significance.

---

## 11. The priority audit is still not adequate for a top-four claim

The new `LITERATURE_AUDIT.md` is more careful than the previous literature discussion and should be commended for explicitly saying it is **not** an exhaustive priority certificate.

That disclaimer is also the problem.

The audit itself states that a relevant Ballico 1993 paper was not fully examined. More broadly, the paper concerns:

- non-complete linear series on (mathbb P^1);
- quadratic multiplication maps;
- projections of rational normal curves;
- quadratic normality / projective normality;
- secant and catalecticant geometry;
- degeneracy loci over Grassmannians.

For a general top-four submission, the priority review must cover this entire intersection of literatures, not only Green--Lazarsfeld, one Ballico paper, Hankel determinantal rings, and the determinantal formulas used in the proof.

The authors do not need to prove that no related theorem exists. They do need to demonstrate that the precise component classification and residual-wall mechanism are genuinely new relative to the best existing work on projections/subseries of rational normal curves and failure loci of multiplication maps.

Until that is done, the novelty assessment is not stable enough for a top-four recommendation.

---

## 12. The manuscript still contains two papers

The current 29-page principal manuscript contains, in one narrative:

- exact fibres of contact data;
- calibrated Hankel information models;
- global multiplication-failure geometry;
- component/scheme classification;
- native loading realization;
- local stability;
- structured matrix examples;
- physical boundary LAN;
- Poisson score experiments;
- deterministic finite-precision reductions;
- classical maximal-rank material;
- additive/monomial comparisons;
- finite-sample categorical recovery;
- observed-exposure protocols;
- computed finite-offset features.

This is cleaner than v111, but it remains heterogeneous.

The strongest paper inside the manuscript is now the algebraic-geometric one:

> classify the multiplication-failure locus/scheme for moving binary subseries, explain the two extremal mechanisms, and relate the wall to residual multiplication.

That paper could stand on its own and would be easier to evaluate for novelty and depth.

The statistical paper could then begin from the multiplication-rank criterion as an input and develop a genuinely intrinsic observation theory.

Keeping everything together makes the submission look cumulative rather than inevitable.

---

## 13. Detailed mathematical comments

### 13.1 Lemma 4.1 / Hankel rank strata

The citation has been improved and now identifies the affine dimension and secant parametrization precisely. Good.

For a final version, I would still prefer a one-paragraph self-contained statement of the exact catalecticant rank-locus fact needed, including the relation between the (k	imes k) Hankel matrix and the rectangular Hankel determinantal presentation. This theorem is too central to be left partially implicit in a change-of-shape reference.

### 13.2 Lemma 4.2 / isotropic incidence

The dimension calculation is standard and appears correct. Since maximal orthogonal Grassmannians can have two components, the stable-range theorem later avoids that issue. The manuscript should say explicitly where connectedness of the nonmaximal orthogonal Grassmannian enters the proof of irreducibility of (mathfrak F_L).

### 13.3 Lemma 4.3 / rank optimization

The arithmetic optimization is improved but still looks like bookkeeping rather than geometry.

The new residual-wall theorem partially explains the two endpoints. The paper should use that insight to rewrite the optimization conceptually. In particular, explain why intermediate ranks cannot compete in terms of radical dimension plus orthogonal-isotropic cost, rather than only through a concave integer inequality.

### 13.4 Lemma 5.2 / strict rank gap

This lemma is essential because the entire component classification depends on it.

The passage from the equal-(s) inequality
[
L D_{r,s}-h_r>min(a,b)
]
to heterogeneous (s_
u) should be written explicitly as an averaged inequality. It is currently correct-looking but too terse for the theorem that follows.

Also provide a finite table of the exact excluded low-dimensional equality cases, not merely the sentence that the stable range excludes them.

### 13.5 Lemma 5.3 / signed secant incidences

The generic recovery of the secant hyperplane from (U_1) is a good argument.

However, the geometry would be much clearer if the authors introduced the abstract rank-two annihilator incidence first, then showed that its normalization has (2^{L-1}) connected/irreducible sign sectors modulo the global involution. At present the sign count is encoded through coordinates (h_pm), and the relation to monodromy around the rank-two Hankel stratum is left implicit.

That reformulation would also prepare the analysis of component intersections.

### 13.6 Lemma 5.4 / nondegenerate incidence

The irreducibility argument via connected special orthogonal groups is plausible in the strict (2c<k) range.

Please state precisely that the relative isotropic Grassmannian over the nonsingular Hankel open is a smooth morphism with geometrically irreducible fibres, and cite the standard fact that this implies irreducibility over an irreducible base.

The dimension estimate excluding secant hyperplanes from a general isotropic plane is useful and should be retained.

### 13.7 Lemma 5.5 / corank-one chart

This is a clean local determinantal calculation and one of the more convincing parts of the proof.

It would be useful to state the resulting normal space explicitly: at a corank-one point, the conormal to the maximal-minor scheme is canonically the image of the derivative of the Schur-complement row. This would make Corollary 5.8 feel less ad hoc.

### 13.8 Lemma 5.6 / generic smoothness of signed components

The residual multiplication argument is the conceptual highlight.

But the proof should isolate one technical point: why the (K_
u) obtained from a general signed incidence are general enough in (operatorname{Gr}(c-1,V_{n-2})^L) to invoke the generic saturation theorem. This is intuitively true from the product relative-Grassmannian parametrization, but it should be stated as dominance of the residual map.

### 13.9 Proof of Theorem 5.1 / expected-codimension scheme

The Eagon--Northcott step is reasonable: the global reduced codimension lower bound plus the universal maximal-minor height upper bound forces expected height on every nonempty chart.

Still, this should be separated into a proposition:

> On every affine Grassmannian chart meeting (mathscr D_L) in the range (ale b), the maximal-minor ideal has grade (a); hence the Eagon--Northcott complex resolves the quotient and the scheme is Cohen--Macaulay and unmixed.

Then prove the associated-prime/reducedness conclusion in a separate commutative-algebra lemma.

The current proof compresses too many logically distinct statements into one paragraph.

### 13.10 Thom--Porteous class

The use of the **dual** map should be emphasized because it explains why the class is (c_a(mathcal E^*)), not a Segre class of (mathcal E) written in an ambiguous convention.

The current formula is consistent, but this is a place where readers can easily become confused.

### 13.11 Corollary 5.7 / real native points

The real-open/Zariski-dense distinction is now handled correctly.

The remaining issue is that this produces selected smooth real points, not a global description of the real locus of each complex component. The paper should resist any language suggesting more.

### 13.12 Corollary 5.8 / local tube exponent

This is standard smooth-tube behavior once the singular value is a transverse defining function.

It is useful, but should not be advertised as a global random-conditioning theorem.

### 13.13 Lemma 10.1 / Poisson total variation

The new proof is much stronger than v111.

For final publication I would still request a slightly more explicit derivation of the Stirling/Taylor bound and a statement of the threshold (N_0(lambda_-,lambda_+)) beyond which the central-region expansion is uniform.

The (N^{-1/5}) rate is deliberately crude, which is acceptable because optimality is not claimed.

### 13.14 Theorem 10.3 / deterministic quantization

The grid-boundary argument is plausible and useful.

State explicitly that the limiting covariance in the (r)-dimensional (F)-coordinates has eigenvalues bounded away from zero and infinity on the fixed problem, which is what makes the one-dimensional boundary-density constants uniform across coordinates.

### 13.15 Proposition 10.4 / nuisance decomposition

The algebraic covariance orthogonality is correct-looking.

Replace “quotienting the experiment” by a formally defined operation or by a more concrete decomposition statement.

---

## 14. What would materially change my top-four assessment

Another revision that only adds:

- more finite diagnostics;
- more source receipts;
- another structured matrix family;
- more examples;
- another response table;
- sharper constants in the (N^{-1/5}) bound;

would not change my recommendation.

A serious top-four reconsideration would require at least one advance of the following scale.

### A. A recursive structural theory of the entire failure scheme

Use the residual construction to classify component intersections, singular strata, and lower-dimensional/excess components. Ideally the rank stratification should feed a recursive description rather than only a dimension bound.

### B. A higher-product or higher-dimensional theorem

Extend the component mechanism beyond binary quadratic multiplication. Even a sharp theorem for (operatorname{Sym}^m U) on (mathbb P^1) for general (m) would substantially change the paper's conceptual status.

### C. Removal of the stable-range restriction

Classify all exceptional cases and prove a full theorem for (4le c<k), perhaps with a finite explicit list of low-dimensional anomalies.

### D. A genuinely intrinsic statistical experiment

Derive the contact statistic or an equivalent reduced experiment from a natural observation model without selecting the least-favourable right-inverse submodel, and treat unknown centre/marks/nuisance at the experiment level.

### E. A global random-conditioning theorem

Give dimension-dependent tails for the least multiplication singular value under a natural random loading model, including behavior near the intersections of failure components.

### F. A complete priority theorem-level literature audit

Close the projection/subseries/quadratic-normality literature gap and state precisely which theorem is new relative to the strongest known results.

---

## 15. Publication-level presentation recommendations

If the authors decide to target a strong specialized journal rather than a general top-four journal, I recommend the following restructuring.

1. Lead with Theorem 5.1 (or its strengthened successor) as the paper's main theorem.
2. Move the information-metric inverse-problem motivation to a short motivating section.
3. Keep the algebraic-geometric core self-contained.
4. Move most statistical experiment material to a companion paper unless it is strengthened into an intrinsic theorem.
5. Remove historical cumulative appendices from the principal submission.
6. Add a dedicated section on component intersections and singularities.
7. Complete the literature audit before making venue-level novelty claims.
8. Replace response-driven exposition with theorem-driven exposition; the current article is much better in this respect but still visibly carries the history of many revision rounds.

---

## 16. Final recommendation

Revision 112 crosses an important threshold: I now regard the paper as containing a genuine structural theorem rather than primarily a collection of sharp dimension counts, realization lemmas, and statistical consequences.

That is significant progress.

However, at a general top-four mathematics journal the standard is not “contains a correct new theorem.” The central theorem must either have broad conceptual reach or deliver a classification of such completeness and depth that the special setting becomes a paradigm.

The present theorem remains a stable-range classification for quadratic multiplication of binary subseries. Its scheme geometry is incomplete at component intersections and in excess codimension. Its literature positioning is explicitly non-exhaustive. Its statistical half, while now technically defensible, is still a chosen local score-compression experiment whose deepest conclusions reduce to Gaussian linear algebra once the model has been engineered.

Accordingly:

**Recommendation: reject in the present form at Annals / Inventiones / JAMS / Acta level.**

I would not characterize the revision as mathematically unsuccessful. On the contrary, it is now plausibly a strong specialized-journal paper after proof expansion, a complete priority audit, and substantial conceptual consolidation. But another top-four round should be justified only by a new theorem of the scale described in Section 14, not by incremental closure of the remaining referee bullets.
