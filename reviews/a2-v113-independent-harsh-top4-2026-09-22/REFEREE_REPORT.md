# Independent harsh referee report on A2 revision 113

Repository: TrillionniumFoundation/theta-theory

Revision branch reviewed: revision/a2-v113-residual-conormal-wall-crossings-2026-09-22

New review branch: review/a2-v113-independent-harsh-top4-2026-09-22

Latest revision head reviewed: c604b9d444db281ea8d662cd15e9bc7822ad55df\n\nSource/build receipts currently record source_commit 1874b76c3d16143f3487e33f2ade7ff35f85010b; the latest head contains one later source commit, reviewed separately below.

Controlling previous review: reviews/a2-v112-independent-harsh-top4-r2-2026-09-22/REFEREE_REPORT.md at 66220b85960a5a50db15342ccfacfbf1395bca88

Principal manuscript: papers/A2-v17-boundary-information-coarsening/article/v113/paper.tex

Title: Recovery of information metrics: residual geometry of multiplication failure schemes

Referee standard: a general top-four mathematics journal (Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica level)

Recommendation: **Reject in the present form at a general top-four mathematics journal.**

This is a materially stronger paper than revision 112. I do not repeat the earlier objections as if nothing had changed. Revision 113 closes several of the most serious mathematical gaps identified in the second v112 review: it gives an all-rank residual tangent sequence, an explicit incidence-to-component proposition, a full low-dimensional equality analysis with five exceptional incidences, a residual dominance morphism, an expected-grade/reducedness package, a same-annihilator signed intersection complex, a rank-two fibre calculation, and a genuine ordinary-double-crossing theorem on a dense divisor of the wall. I did not find a one-line counterexample that invalidates the main quadratic component theorem.

The negative recommendation is now driven by a different and narrower set of issues. The paper has become a serious algebraic-geometric classification, but the step from “serious and technically substantial” to “general top-four” is still missing. The remaining problems are concentrated exactly at the new headline claims: the orientation-descent and wall-normal-form arguments are too compressed for independent certification at this level; the wall and excess scheme geometry remain only partially classified; the higher-product section does not extend the global quadratic theorem; and the priority audit still explicitly leaves a close 1993 failure-locus antecedent unexamined theorem by theorem. The manuscript is also still trying to be an algebraic-geometry paper, an inverse-information paper, and an asymptotic-statistics paper simultaneously.

## 1. Provenance and review scope

I reviewed the actual v113 manuscript, not the two earlier v113-named branches that contained no new principal manuscript. The present branch is a genuine new mathematical revision based on the second v112 report.

The latest evidence commit f352be19dd524a6c5ff640289cd00b4bf87049e1 binds the generated 43-page PDF and verification receipts to mathematical source c604b9d444db281ea8d662cd15e9bc7822ad55df. That source commit separates the analytic node equation from the completed local-ring statement in the wall theorem and alphabetizes the retained bibliography. The receipts record an additions-only revision relative to the controlling review, 134 labels, 25 bibliography keys, and no overfull boxes. The finite diagnostic package checks, among other things, 1,541,451 rank-cost cases in bounded ranges, the five exceptional equality tuples, finite phase-orbit counts, low-dimensional rank-two fibre algebra, several tangent examples, and one residual-wall Jacobian example over a finite field.

Those diagnostics are useful. They are not proofs, and the repository itself correctly says so. I have therefore treated them as consistency checks only.

I also checked the external bibliographic point that matters most for priority. Wiley confirms E. Ballico, “On the Failure Locus of Higher Order Properties of Embeddings in Projective Spaces,” Mathematische Nachrichten 163 (1993), 5–13, DOI 10.1002/mana.19931630102. The accessible publisher page confirms the article and its bibliography but did not expose the theorem text to me. Therefore I make no claim that Ballico 1993 contains the results of v113. The relevant fact for this review is simpler: the manuscript's own literature audit still says that a theorem-by-theorem comparison with this close antecedent is unverified.

## 2. Executive mathematical assessment

The strongest part of v113 is no longer the codimension formula. It is the residual deformation mechanism.

For an annihilator ell, the paper sets W_nu = U_nu intersect rad(H_ell) and proves that the obstruction to solving the infinitesimal isotropy equations is exactly the restriction of dot(ell) to the residual product span sum W_nu^2. The resulting exact tangent sequence is the first genuinely invariant statement in this line of revisions. It explains why rank two produces the smaller multiplication problem and why the equality a=b is a residual saturation wall rather than merely a coincidence of two dimension formulas.

The all-dimensional component theorem is also a substantial improvement. The stable restriction c>=8, k>=2c+1 has been removed from the component and expected-codimension scheme assertions. The manuscript identifies exactly five nonendpoint equality incidences and gives them one geometric description: the plane contains the full radical and becomes maximal isotropic in the quotient. That is much better than a table of numerical exceptions with no mechanism.

The wall theorem is the most ambitious new result. On a specified dense divisor of Phi_L intersect Sigma_epsilon, the manuscript obtains the completed local ring

C[[t_1,...,t_{d-1},u,v]]/(uv),

identifies the two branches, computes the conductor, and derives an epsilon^a log(1/epsilon) local conditioning law. If fully secured, this is an attractive piece of geometry.

Nevertheless, I would not certify the present paper at a general top-four level. There are four independent reasons.

1. **The conceptual reach remains narrower than the rhetoric of a general theory.** The complete global theorem is still about quadratic multiplication of binary subseries and Hankel annihilators. The higher-symmetric-power section classifies only two-point annihilator sectors; it explicitly does not determine the full higher-product failure locus.

2. **The global scheme geometry remains incomplete at exactly the singular boundary where the paper now claims its strongest geometric insight.** The node theorem is a dense-open theorem on one residual divisor, not a classification of the full component intersection. The excess regime still classifies only maximal-dimensional components, not the global associated-prime or embedded structure.

3. **The most delicate new proofs are still written one layer too tersely for the strength of the conclusions.** In particular, the orientation monodromy, exceptional-incidence irreducibility, global residual divisor, and normal-derivative factorization need independent lemmas with explicit descent/trivialization arguments. I regard these as proof-completeness blockers, not stylistic preferences.

4. **Priority is not yet auditable at the claimed venue level.** The manuscript openly leaves Ballico 1993 without a theorem-level comparison. A top-four referee cannot be asked simultaneously to verify a new delicate classification and to reconstruct the closest historical comparison from scratch.

## 3. What revision 113 genuinely fixes

### 3.1 The previous incidence-to-component gap is substantially repaired

Proposition “From rank incidences to components” isolates the projection argument that was implicit in v112. It correctly recognizes that a finite locally closed stratification of the projective annihilator incidence must have a piece dense over any irreducible component of the failure support. It also isolates the key point that a nonempty open subset of a positive-dimensional projective annihilator space cannot be a zero-dimensional generic fibre.

This is the right structural lemma to have introduced.

### 3.2 Residual-plane generality is no longer assumed

The rank-two residual morphism to Gr(c-1,V_{n-2})^L is now stated as a smooth surjection with affine fibres. This directly answers one of the most serious v112 objections: “the residual planes are general” is now a theorem, not a sentence inserted immediately before using the earlier generic saturation result.

### 3.3 The low-dimensional cases are no longer swept into a stable range

The five exceptional tuples are not merely computer output. The manuscript provides an analytic equality analysis, an orientation description, and an explicit corank-one example for the excess exception (5,7,1). My independent reading of the rank-cost argument did not reveal an omitted sixth equality family, and the repository's bounded exhaustive diagnostic is consistent with the analytic list.

This is a meaningful closure of a previous weakness.

### 3.4 The expected-codimension scheme argument is organized correctly

The manuscript now separates:

- height and grade of the maximal-minor ideal;
- Eagon–Northcott perfection;
- Cohen–Macaulayness and unmixedness;
- generic reducedness;
- reducedness via R0 + S1.

That is considerably better than burying all four logical steps in one paragraph.

There is one bibliographic precision issue: the bibliography cites Stacks tag 031O, which is the section “Serre's criterion for normality.” The exact lemma stating “Noetherian reduced iff R0 and S1” is Lemma 10.157.3, tag 031R. This should be corrected, but it is not a mathematical defect.

### 3.5 The wall now has an actual local equation on a dense open set

Revision 112 only gestured toward component intersections. Revision 113 proves substantially more: same-annihilator signed intersections over the split rank-two base, a residual determinant divisor, and a dense ordinary-double-crossing locus. This is real progress and should be credited as such.

## 4. Principal top-four blocker: the paper still has a complete theorem only in one very special representation

The complete classification is still tied simultaneously to

- P^1 and binary forms;
- quadratic multiplication Sym^2(U);
- Hankel/catalecticant annihilators;
- products of Grassmannians of subseries;
- a very specific secant-versus-nondegenerate rank competition.

The new residual tangent sequence is invariant enough to suggest a broader theory, but the paper does not yet formulate that theory.

The higher-product section does not solve this problem. Theorem “Phase-sector classification for every symmetric power” classifies the reduced incidence of **two-point annihilators**. It then explicitly says that it does not assert that these sectors are all components of the higher-product failure scheme or that the higher-product failure codimension is known. The residual conormal theorem for m>2 is likewise a local sector statement.

That is mathematically honest. It also means that the previous significance objection has not been removed; it has been reframed.

For a general top-four paper, I would want one of the following two advances.

**Route A: a genuine higher-product theorem.** Determine the global failure codimension and the maximal components, at least in a nontrivial range, for Sym^m(U) with m>=3. It is not necessary that the answer be as explicit as in the quadratic case, but the paper should show that the residual mechanism predicts and controls more than the two-point sector.

**Route B: an invariant theorem from which the quadratic classification is a model case.** Formulate hypotheses on a family of bilinear multiplication maps, annihilator rank strata, and radical residual products under which endpoint components, residual singularity recursion, and wall crossings follow formally. Then the binary quadratic case could legitimately serve as a complete worked classification of a general mechanism.

At present the manuscript contains the ingredients of Route B but not the theorem. The exact residual tangent sequence is close to being the correct abstraction. The rest of the paper should be reorganized around it if the goal is a general mathematics journal.

## 5. The wall geometry is improved but still not globally classified

The new title emphasizes “residual geometry of multiplication failure schemes.” That raises the standard for what counts as closure.

### 5.1 Same-annihilator signed intersections are not all projected intersections

Theorem “Normalization and all signed intersections over the rank-two base” is deliberately restricted to:

- the distinct-support rank-two base B_2^circ;
- a labelled double cover;
- reduced incidence components;
- projected intersections only where multiplication has corank one and the annihilator lies in that base.

The manuscript itself correctly warns that signed images can meet through different annihilators at higher-corank points or through support collisions.

Those omitted intersections are not peripheral to a global scheme theorem. They are precisely where the projection from the annihilator incidence ceases to be locally an isomorphism and where new singularities can appear.

A top-four version should either classify these loci or explicitly downgrade the geometric claim from “wall geometry” to “generic wall geometry.”

### 5.2 The node theorem treats a dense divisor, not the full Phi_L intersect Sigma_epsilon

Theorem “The residual double-crossing divisor” proves a beautiful local normal form on a dense open subset of Z_epsilon. It does not determine:

- whether every codimension-one component of Phi_L intersect Sigma_epsilon is obtained this way;
- what happens on the complement of the residual-corank-one open set;
- how support collision changes the local equation;
- what happens when the original multiplication corank exceeds one;
- whether different signed branches and Phi_L can meet simultaneously;
- the global normalization or conductor of the whole wall scheme;
- the singular locus of the entire expected-codimension determinantal scheme.

The theorem should not be weakened merely to avoid these questions. Rather, these questions are the natural next layer generated by the theorem. For a specialized paper, a generic ordinary-double-crossing result may be sufficient. For a general top-four claim built around “residual geometry,” the current stopping point still feels premature.

### 5.3 The excess regime remains structurally incomplete

When b<a, the theorem classifies the maximal-dimensional irreducible components. It explicitly does not classify all smaller components or the associated primes of the full maximal-minor scheme.

The fixed-annihilator rank-two fibre calculation does not close this gap. In fact the manuscript correctly emphasizes that the embedded origin prime in that fibre is **not** being asserted as an embedded prime of the global scheme.

That distinction is good mathematics, but it leaves the global excess scheme open.

If the authors keep the present title and top-four target, I would want at least one of:

- an unmixedness/associated-prime theorem in the excess range;
- a complete annihilator-rank stratification of the excess support;
- or a precise theorem showing why the smaller excess structure is controlled recursively by residual multiplication schemes.

## 6. Proof-completeness issues in the new headline results

I emphasize that I am not presenting the following as discovered counterexamples. I am saying that I would not sign off on the corresponding theorems from the present proofs at a top-four level.

### 6.1 Orientation monodromy and irreducibility need a formal descent lemma

The all-dimension theorem depends on the assertion that two geometric components of maximal orthogonal Grassmannians are exchanged by monodromy, making the total incidence irreducible.

For the (7,14,1) full-rank case the argument is:

- take the orientation double cover by adjoining a square root of the determinant of the universal Hankel form;
- show the determinant is not a square because its zero divisor is an irreducible corank-one Hankel hypersurface appearing with multiplicity one;
- conclude the cover is connected;
- conclude that it exchanges the two maximal orthogonal families;
- conclude the total incidence is irreducible.

The exceptional incidences use an analogous argument with the product of the diagonal weights.

This is plausible, but too much geometry is compressed into “the connected orientation cover exchanges the two families.” The paper needs a proposition stating the relative orthogonal-Grassmannian situation, the exact double cover, the deck action on the two geometric components, and the descent criterion implying irreducibility of the total space.

In particular, connectedness of the discriminant cover and geometric irreducibility of each component after pullback should be connected by a written monodromy/descent argument, not by an implicit appeal to standard folklore.

Because this step decides whether a putative top-dimensional incidence is one component or two, it is central to the all-dimensional classification.

### 6.2 The exceptional-incidence orientation cover deserves the same treatment

For the five exceptional cases the manuscript writes the quotient form as diag(alpha_i) over an ordered support/weight parameter space and observes that product alpha_i is nonsquare.

Again, this is suggestive rather than fully formal. Please specify:

- the exact irreducible base on which the quotient form is defined;
- the removal of diagonals and zero weights;
- the function field in which nonsquareness is asserted;
- the finite cover that labels orientation;
- the action of the deck transformation on maximal isotropic components;
- why taking the unordered support quotient does not introduce an additional splitting.

This is not excessive pedantry. These exceptional incidences are the new content that removes the stable-range hypothesis.

### 6.3 The global residual determinant divisor needs a cleaner relative proof

The wall theorem says that at residual dimensions (k-2,c-1), the residual determinant is an integral reduced divisor, and that pullback by the smooth affine-space bundle preserves generic irreducibility and reducedness; local bundle trivializations as support points vary are then said to give the same assertion for Z_epsilon.

I would want this replaced by a precise relative statement. In particular:

- identify the residual Grassmannian bundle over the split rank-two base;
- state the determinant section as a section of an explicit line bundle;
- prove its zero scheme is irreducible and reduced in the total relative space;
- then pull it back along the affine bundle.

Fibrewise integrality plus local triviality often gives the desired result, but the present proof makes the reader reconstruct the needed relative argument.

### 6.4 The normal-derivative factorization is too important to remain a paragraph

The key identity is that, up to a unit,

det(normal derivative along S) = det(mu_K').

This is the hinge on which the uv normal form turns.

The paper explains the two blocks: the mixed/square equations give an invertible block in transverse plane coordinates; the normal space to the rank-two Hankel base is identified with (g^2 V_{2n-4})^*; the remaining derivative block is the dual residual multiplication map.

I believe this mechanism is correct. But it should be a named proposition with:

- explicit local coordinates or vector-bundle maps;
- a basis-independent identification of the normal bundle;
- a proof that the determinant equality is compatible with changes of trivialization;
- and a statement of the unit ambiguity.

The headline singularity theorem should not depend on the referee accepting a block decomposition reconstructed from prose.

### 6.5 Nonemptiness of the corank-one wall open set should be made constructive or formally intersected

The proof of the wall theorem imposes several open conditions on a general residual tuple and then varies the lift a_1 to fill the missing residual direction.

The argument is convincing locally, but the paper should make explicit why all the required open conditions meet the residual determinant divisor simultaneously. A clean route would be either:

- one explicit point satisfying all conditions, followed by openness; or
- an irreducibility argument showing that none of the relevant failure conditions contains the residual divisor.

This is particularly important because the theorem asserts a **nonempty dense open** ordinary-double-crossing locus, not merely “if such a point exists, then its germ is a node.”

### 6.6 The higher-product monodromy should be algebraic, not only described by loops

The phase-sector count

N_{m,L} = (m^{L-1} + gcd(m,2)^{L-1})/2

is attractive, and the orbit count itself is elementary once the group action is known.

The proof says that a loop in the nonzero weight ratio realizes simultaneous cyclic translation and that support interchange realizes inversion. For a theorem stated over an algebraic base, I would prefer a finite splitting cover with an explicitly identified deck group and a descent proof that its orbits are exactly the irreducible components.

The present topological language does not clearly rule out additional monodromy, stabilizer issues, or a splitting after descent on an inversion-fixed sector.

This is fixable, but it should be fixed before the theorem is advertised as the higher-product conceptual extension.

### 6.7 The rank-two fibre algebra should receive a compact algebraic verification

The local ring

C[a_1,...,a_c,b_1,...,b_c] /
(a_i b_i, a_i b_j+a_j b_i)

is simple enough that the stated nilradical and associated primes are likely correct, and the repository diagnostics agree in small c.

Because the proposition is one of the manuscript's advertised scheme-theoretic results, I would nevertheless prefer either:

- an explicit primary decomposition; or
- a short Gröbner-basis/Hilbert-series argument that proves the mixed quadratic classes are exactly wedge^2 C^c and that no additional associated primes occur.

The current short-exact-sequence argument states that the reduced quotient has only its two minimal primes and no embedded prime, and that the nilradical module has only the origin as an associated prime. Those facts are plausible but deserve one extra line of algebraic justification.

## 7. Priority remains a formal blocker at the claimed venue level

The literature audit is unusually candid, which I appreciate. It says that Ballico 1993 has been bibliographically confirmed but not compared theorem by theorem.

That is not enough for a top-four submission.

The paper's core subjects are classical and densely connected:

- failure loci of embeddings;
- higher-order and quadratic normality;
- secant spaces;
- projections/subseries of rational normal curves;
- catalecticant/Hankel rank loci;
- maximal-rank multiplication;
- orthogonal degeneracy loci.

Ballico 1993 is not an obscure tangential citation; its title is directly adjacent to the manuscript's stated failure-locus theme. The publisher page also shows that its bibliography already sits in the older secant/maximal-rank literature.

I am **not** saying that Ballico 1993 proves the v113 component theorem, wall node, or residual tangent sequence. I have not verified that. I am saying the opposite: until someone has read and compared the actual theorem statements, the novelty boundary is not referee-certifiable.

A revision aimed at a general top-four journal should contain a theorem-by-theorem priority table. For each principal theorem, identify:

1. the strongest prior theorem on the same or nearest parameter space;
2. whether the prior result concerns complete series, a fixed embedding, varying subseries, or a failure cycle;
3. whether it is set-theoretic, scheme-theoretic, or only generic;
4. what v113 adds that is not present there.

The burden should not be shifted to the referee.

## 8. The statistical and inverse-information material still weakens the main paper's architecture

The new organization moves much of the earlier stable theorem and statistics to appendices, which is an improvement. It is not enough.

The manuscript still contains, in one 43-page article:

- a calibrated inverse-information model;
- exact contact fibres;
- a global algebraic-geometric failure-locus theorem;
- an all-dimensional component classification;
- residual deformation theory;
- a wall singularity theorem;
- higher symmetric powers;
- native loading realizability;
- local asymptotic boundary experiments;
- Poisson-to-Gaussian Le Cam comparisons;
- deterministic quantized score compression;
- finite-sample estimators;
- additive-basis comparisons;
- complete-conormal and inverse-parametric-programming complements.

Several of these pieces are individually interesting. Together they obscure what the paper is asking a general mathematics journal to regard as its central theorem.

The algebraic geometry has now become strong enough that the cleanest paper would begin with the multiplication failure scheme and the residual tangent sequence, develop the component and wall theorems, and end with a short application section explaining why the geometry controls information recovery. The full Poisson, quantization, pilot, finite-offset, and endpoint-representation developments should be a companion paper or supplementary technical note unless the authors can prove that they are logically necessary to the main theorem.

At present they are mostly consequences or parallel protocols. They do not increase the conceptual generality of the algebraic theorem.

## 9. The higher-product section is interesting but presently over-sold by its placement

I would keep the phase-sector theorem only if one of two things happens.

Either develop it into a true extension of the main theorem by determining when the sectors are actual maximal components of the entire higher-product failure locus.

Or move it to a final “outlook/generalization” section and state clearly that it demonstrates the monodromy pattern of one obstruction family but does not provide a higher-product analogue of the global codimension/component theorem.

As written, placing the section directly after the wall theorem makes the reader expect that the quadratic classification has been lifted to arbitrary symmetric power. It has not.

The distinction is correctly stated in the fine print; it should be reflected in the theorem hierarchy and introduction.

## 10. Statistical comments

I re-read the new and inherited statistical material sufficiently to test whether it repairs the earlier category errors.

The most important fixes from prior versions remain intact:

- the paper distinguishes raw counts, randomized/quantized score compression, computed finite-offset features, and independent noisy distance observations;
- the Poisson comparison is in total variation, not merely weak convergence;
- the physical boundary parameter is treated as a cone;
- nuisance removal in the Gaussian limit is explicitly an invariant/quotient construction, not an equivalence of the full nuisance experiment;
- the exact-lattice-encoding loophole is removed by jittering or finite precision.

I do not identify a new fatal statistical error that would independently kill v113.

But these results should not be used to justify the top-four significance of the algebraic classification. Their main function is to show that the geometric rank loss can arise in a well-specified statistical experiment. That is a good application, not a substitute for conceptual generality of the geometry.

## 11. Minor and presentation points

1. Correct the Stacks citation from the section tag 031O to the exact reducedness lemma tag 031R (Lemma 10.157.3), while retaining 031O if the intention is to cite the whole section.

2. The introduction should distinguish more sharply between “component theorem,” “generic wall theorem,” and “global scheme theorem.” At present the abstract can be read more globally than the precise scope boundaries later allow.

3. “All signed intersections” in the heading of Theorem thm:signed-normalization should probably say “all same-annihilator signed intersections over the split rank-two base.” That is what is actually proved.

4. The phrase “components in all dimensions” is defensible for maximal-dimensional support in the excess regime only because the theorem explicitly says “maximal-dimensional components.” Keep that qualifier in every summary statement.

5. The proof of the exceptional orientation cases should not mix function-field nonsquareness, topological monodromy language, and geometric irreducibility without a formal bridge.

6. The latest source correctly separates the analytic equation uv=0 from the completed local-ring statement, and the latest evidence commit rebinds the generated PDF to that source. Preserve this distinction in any subsequent revision.

7. The finite diagnostics are useful enough to keep, but the main manuscript should not mention their successful execution as evidence for universal theorems. The current repository documentation handles this distinction correctly.

## 12. What would change my top-four assessment

A subsequent revision would need more than another layer of local patches. I would want the following package.

### A. Harden the new proofs

Write full standalone propositions for:

- orientation-cover descent and irreducibility of relative maximal orthogonal incidences;
- the exceptional orientation covers;
- the relative residual determinant divisor;
- the normal-derivative/residual-determinant factorization;
- algebraic monodromy/descent for the higher-product phase sectors.

These should be proofs a reader can verify without reconstructing unstated standard facts.

### B. Complete one genuinely global singularity statement

Either classify the full codimension-one intersection Phi_L intersect Sigma_epsilon at the wall, including the complement of the node locus, or prove a global recursive theorem reducing every singular stratum to a residual multiplication failure scheme.

A generic node theorem is good; a recursive singularity theorem would be substantially more important.

### C. Give a real generalization beyond quadratic binary multiplication

A full m>=3 classification is not the only option, but the paper needs a theorem whose scope is not exhausted by Sym^2 of binary subseries.

The present residual tangent sequence is the natural starting point.

### D. Close the priority audit

Read Ballico 1993 and the nearest secant/projection/subseries literature. Put the comparison in the paper, not only in a repository audit file.

### E. Refocus the article

Make the algebraic geometry the principal paper. Keep only the amount of statistical/inverse-information material required to demonstrate a nontrivial application of the geometric theorem.

## 13. Final recommendation

Revision 113 is the first version in this sequence for which I would describe the algebraic-geometric core as a potentially publishable research paper rather than as a promising theorem surrounded by unresolved proof architecture.

That is a meaningful improvement.

It is still not, in my judgment, a general top-four paper in its present form.

The decisive remaining gap is no longer the basic codimension theorem or the existence of a residual mechanism. It is the absence of a sufficiently general conceptual theorem and a sufficiently complete global singularity/priority package to justify the venue claim. The new wall and orientation results are exactly the places where the manuscript is most interesting, and exactly the places where I would demand more proof detail before certifying correctness.

**Recommendation: reject in the present form at a general top-four mathematics journal.**

I would welcome a new mathematical review only after the authors have either (i) promoted the residual mechanism to a genuine general theorem and completed the wall proof package, or (ii) refocused the submission as a sharp specialized classification with a narrower venue claim and a completed priority audit.
