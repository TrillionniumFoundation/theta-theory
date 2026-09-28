# Independent harsh referee report on A2 revision 92

**Review date:** 19 September 2026  
**Repository:** TrillionniumFoundation/theta-theory  
**Reviewed revision branch:** revision/a2-v92-sharp-modulus-and-singular-normal-forms-2026-09-19  
**Reviewed branch head:** d55c480f8cdf9f1327b4142bf1bb31a315f71b2b  
**Previous revision base:** revision/a2-v91-integrated-quotient-geometry-2026-09-19 at d1acb5d047a3c32b2c676ebe76ca0a64f8952ed2  
**Controlling previous report:** reviews/a2-v91-independent-harsh-top4-2026-09-19/REFEREE_REPORT.md  
**Reviewed manuscript:** *Projective polynomial observations: intrinsic geometry and additive normalization*  
**Author:** Qian Qi

## 1. Recommendation

**Recommendation to the editor: reject in the present form at the stated four-leading-general-mathematics-journal level.**

This is a materially different assessment from a routine repetition of the v91 report. Revision 92 is a serious response. It directly attacks nearly every concrete mathematical request made in the previous report:

- it states the missing coefficient-level analytic recovery theorem across internal root multiplicities;
- it proves a first-order bridge between the exact Hellinger observation-ball modulus and the quotient Fisher covariance;
- it computes a profiled quartic leading law and an explicit leading constant at real-rooted internal multiplicities;
- it gives a uniform crossover law from a split double root to the double-root singularity;
- it constructs an explicit binary family in which normalization failure, channel collapse, component equality, and root multiplicity meet;
- it proves a finite Laurent cancellation test for common-flag matrix polynomials;
- it gives matching lower perturbations on exposed common-flag classes and positive noncommuting examples;
- it repairs the missing v91 source manifest.

These are substantive additions. In particular, v92 should not be described as merely renaming the implicit modulus or adding another diagnostic script. The regular geometry is now much more integrated, and the repeated-root calculation is a genuine model-specific second-order theorem.

Nevertheless, I do not think the manuscript has crossed the threshold for one of the four leading general mathematics journals.

The principal reason is now very specific. The manuscript advertises a theory of singular intersections, but the one explicit intersection that simultaneously combines the normalization, channel, component-equality, and multiplicity defects is a point at which the entire spectrum is already exactly unidentifiable: its exact fibre has diameter D-L. At that datum there is no vanishing intrinsic spectral modulus to classify. The three-monomial ideal gives useful transverse arc information, but the hardest question raised by v91 remains open: what is the intrinsic observation modulus at a genuinely intersecting, still spectrally identifiable singularity with omega_P(0)=0?

The second major reason is the common-flag sharpness theory. The new Laurent test exactly computes the pole order of M^{-1}, but the admissible observation perturbations lie in a proper zero-sum subspace. The manuscript therefore needs an exposure hypothesis to turn the resolvent pole into a lower bound. When exposure fails, the actual observation-slice Hölder exponent is not classified. Moreover, when cancellation reduces the true pole order below the flag-path count, the unknown-normalizer theorem explicitly falls back to the old path exponent because the interpolation gauge may destroy the cancellation. Thus the genuinely cancellation-aware, unknown-normalizer observation geometry remains unresolved in precisely the cases where the new finite invariant is most interesting.

I found no short counterexample invalidating the principal v92 statements. My recommendation is instead based on the combination of these remaining structural gaps and the top-four editorial standard.

## 2. Scope of this review

I reviewed the exact branch head d55c480f8cdf9f1327b4142bf1bb31a315f71b2b, not main and not an earlier A2 revision.

Relative to v91, v92 is twelve commits ahead and introduces the following principal mathematical sources:

- article/v92/coefficient_recovery.tex;
- article/v92/intrinsic_modulus.tex;
- article/v92/modulus_bridge.tex;
- article/v92/singular_normal_forms.tex;
- article/v92/sharp_flag.tex;
- article/v92/paper.tex.

I also reread the inherited v90 local quotient theorem, exact local condition theorem, and common-flag theorem because the v92 claims depend on them directly, and I reread the v91 report to distinguish repaired objections from still-open ones.

For external context I checked the classical structured polynomial-eigenvalue and multiple-eigenvalue perturbation literature represented in the manuscript by Tisseur--Higham and Kressner--Pelaez--Moro. That literature confirms the manuscript's current positioning: the general resolvent/Hölder machinery is classical; the potentially new content is the pullback through the normalized probability observation, the additive scalar gauge, and the model-specific quotient geometry. The v92 exposition is substantially more responsible on this point than early revisions.

The committed Python programs are treated as finite diagnostics and source checks only. They are not evidence for a theorem that is not proved in the text.

## 3. What v92 genuinely fixes

### 3.1 The repeated-root coefficient-recovery gap is fixed

Proposition “Ambient coefficient recovery” is exactly the lemma requested in the v91 report.

The important point is that the analytic inverse is constructed in monic polynomial coefficient coordinates before scalar roots are extracted. Internal root multiplicity therefore does not obstruct recovery of:

- the monic normalizer;
- the numerator matrix polynomial;
- the rank-one joint projectors for distinct complete component polynomials;
- the weights and stochastic columns;
- the complete component coefficient tuples.

The text correctly avoids claiming that the real-rooted coefficient subset is itself a smooth manifold at a repeated root. This is the right formulation.

I no longer regard the anchored multiplicity theorem as citing a recovery theorem outside its stated hypotheses.

### 3.2 The regular condition objects are now connected by an actual theorem

Theorem “Exact regular observation-ball modulus” is an important improvement.

With the manuscript's Hellinger normalization, the local Hellinger ball pulls back to the Fisher ellipsoid with radius two. The unordered root target at a cross-component collision is handled through the finite permutation group Gamma acting inside equal-base-value blocks. The theorem

omega_P(t) = 2 D_Gamma(V_H(P)) t + o(t)

is the correct kind of bridge that v91 requested.

The distinction between radial distance from the base and the diameter of the whole local target set is essential. The factor four in the collision-free case follows because the target ellipsoid is centrally symmetric; at a collision the quotient diameter can be strictly smaller than twice its ordinary sup-norm radius. The manuscript's two-coordinate example illustrates this correctly.

This materially improves the conceptual architecture. V_H is no longer merely a separate local differential object sitting next to omega_P.

### 3.3 The profiled quartic calculation is a real singular theorem

Theorem “The real-rooted singular leading constant” is, in my view, one of the strongest new results in v92.

After analytic coefficient recovery, a symmetric root split has no first-order coefficient displacement. Its order-t coefficient displacement is controlled by the quadratic statistic

v_g(x) = (1/2) sum_{i in g} x_i^2.

Profiling the corresponding second-order polynomial directions against channel, weight, and centroid tangents gives the positive definite Schur-complement matrix S. The resulting compact quartic section X_S gives an explicit leading constant for the square-root observation modulus.

This is substantially better than saying only that a Puiseux exponent exists.

The double-root formula

C_S = sqrt(2) s^{-1/4}

is also a useful exact benchmark, and the uniform crossover

omega_{P_Delta}(t) asymp t + t/(Delta + sqrt(t))

correctly connects the diverging regular derivative to the singular square-root regime at t asymp Delta^2.

### 3.4 The common-flag cancellation discussion is more precise

The finite matrices C_{r,s} correctly encode cancellations between path terms in the triangular resolvent expansion. The actual pole order of M^{-1} is an intrinsic quantity even though a flag is used to calculate it.

This answers an important weakness in v91: the old path count was only an upper certificate and could overestimate the true pole order. The concrete 3 by 3 example where two z^{-4} terms cancel and the true pole order is three is exactly the sort of example the paper needed.

The positive rational constructions also make clear that the phenomenon is not confined to a formal triangular matrix.

### 3.5 The v91 manifest defect is repaired

Revision 92 adds revisions/a2-v91/SOURCE_MANIFEST.json, so the inherited v91 verifier is no longer missing the file that it explicitly reads.

This closes the concrete repository defect identified in the previous report.

## 4. Status of the main v91 requests

My present assessment is:

| v91 request | v92 status | Current assessment |
| --- | --- | --- |
| Separate coefficient recovery theorem at repeated roots | Resolved | Proposition v92 gives the needed ambient analytic recovery |
| Bridge eta_d, V_H, omega_P on regular quotient | Substantially resolved | Exact V_H-to-omega constant is proved; eta_d remains a one-sided global certificate |
| Compute a model-specific singular modulus | Resolved on the internally repeated-root, coefficient-identifiable stratum | Quartic cone and crossover are genuine computations |
| Compute a hard intersection of defects | Only partially resolved | The chosen full-collapse point has omega_P(0)=D-L, so the spectrum is already exactly unidentifiable |
| Characterize flag cancellations | Resolved for the resolvent pole | Not yet a complete classification of admissible observation perturbations |
| Prove sharp flag exponents | Resolved on exposed fixed-normalizer classes and when nu=nu_Q | Non-exposed and cancellation-sensitive unknown-normalizer cases remain open |
| Repair reproducibility | Improved but not cleanly closed | v91 manifest is added; exact v92 head still has provenance/trigger issues described below |

The remaining objections are therefore narrower than in v91, but they are central.

## 5. Major objection I: the advertised “hard intersection” is completely nonidentifiable

Theorem “Collapse normal form and transverse phase law” studies the binary family

(u_j,v_j,w_j) = (a chi_j, b chi_j, ab)

with local ideal

(ab, ax, bx).

This calculation is clean. The observation order along a positive power arc is indeed

min{p+q,p+r,q+r}.

The difficulty is what happens at the intersection a=b=x=0.

At that point both stochastic channel matrices have collapsed columns. Consequently the observed probability matrix is constant and no longer depends on the component polynomials at all. The paper correctly proves

omega_{P_*}(t) = D-L

for every t >= 0.

That statement is correct, but it changes the meaning of the example.

The spectral inverse at P_* has not developed a subtle fractional modulus. It has disappeared completely. Every shrinking observation neighbourhood already contains an exact fibre with the maximal possible root diameter.

Thus the example does not answer the most difficult question posed in the v91 report:

> What happens when several algebraic defects intersect but the spectral target remains locally identifiable, so that omega_P(0)=0 and a nontrivial fractional observation modulus must be computed?

The v92 example instead answers a different question:

> How do regular inverse constants blow up when approaching a point of total spectral nonidentifiability, and what monomial ideal describes one selected family of approaches?

That is useful, but it is not the missing intrinsic singularity theorem.

### Why this matters at the stated journal level

A general-journal theorem should distinguish between:

1. exact-fibre nonidentifiability;
2. weak identification with a vanishing nonlinear modulus;
3. regular identification with a diverging differential condition.

The manuscript now treats all three notions, but the multi-defect intersection itself is in category 1, while the nontrivial fractional calculations remain in a category where coefficient recovery is regular.

The most convincing next theorem would be an intersection involving at least two of normalization failure, channel-rank loss, component equality, or internal multiplicity for which the exact spectral fibre is a singleton but the derivative degenerates. The paper should derive the local ideal or tangent cone, compute the resulting exponent, and preferably identify a leading constant or a finite variational problem.

Without such an example or theorem, the “singular intersections” narrative remains incomplete.

## 6. Major objection II: the binary singular labels are not intrinsic to the observation datum

The paper describes P_* as an intersection having:

- channel collapse;
- normalization failure;
- equality of complete component polynomials;
- internal multiplicity d.

The first two properties are visible from the selected parametrization and the datum. The latter polynomial properties are not intrinsic to P_* because the exact fibre is enormous.

When both channels collapse, the same P_* is represented by arbitrary admissible component polynomials. The exact fibre therefore contains:

- the repeated common polynomial used in the displayed normal form;
- distinct component polynomials;
- simple-root polynomials;
- repeated-root polynomials;
- many different equality and multiplicity patterns.

Accordingly, “P_* has internal multiplicity d” is not an intrinsic statement about the observation point. It is a statement about a selected representative or selected arc in a nonidentifiable fibre.

The manuscript partially acknowledges this by referring later to the “selected repeated-root representative,” but the singular-normal-form section and the introduction should be more disciplined about the distinction.

This is not just terminology. The paper repeatedly emphasizes representation-free geometry. At an observation with a nontrivial exact fibre, defect labels attached to one latent representative cannot be used as intrinsic invariants of the datum unless the paper explicitly works with a stratified fibre or a pointed pair (P,theta_0).

A clean formulation would introduce separate objects for:

- the intrinsic observation germ at P;
- a pointed latent germ at (P,theta_0);
- the union of strata inside the exact fibre.

The current binary theorem mixes these levels.

## 7. Major objection III: the flag “exact cancellation test” is exact for the resolvent, not for the observation modulus

Proposition “Exact cancellation test” computes the actual pole order nu_r of M^{-1}. I agree with that proposition.

However, the observation perturbations are not arbitrary coefficient perturbations.

On the fixed-normalizer slice they must satisfy

1^T E(z) 1 = 0.

Theorem “Exposure, sharpness, and the observation modulus” therefore imposes the additional condition

L_r notin C 11^T

in order to expose the leading Laurent coefficient by an admissible rank-one zero-sum perturbation.

This reveals that nu_r is not, by itself, the exact invariant of the observation modulus.

When L_r lies in the annihilator of the admissible perturbation space, the leading pole is invisible to first-order zero-sum perturbations. The manuscript then provides only the general upper bound t^{1/nu}; it does not identify the first lower Laurent order that is visible through the admissible perturbation space.

### The missing invariant

The natural object is not merely the largest pole order of M^{-1}. It is the largest Laurent order whose coefficient acts nontrivially on the allowed numerator-perturbation space after the normalization constraint is imposed.

At minimum the paper should define and analyze a constrained exposure filtration such as:

- for each Laurent order s, project the corresponding coefficient functional onto the dual of {E: 1^T E 1=0};
- find the largest s for which this projected functional is nonzero;
- allow polynomial-in-z perturbations when constant perturbations are insufficient;
- prove that this constrained order gives the fixed-normalizer observation Hölder exponent.

That would turn the current sufficient exposure condition into a classification theorem.

Without it, the phrase “sharp flag exponents and observable cancellations” is stronger than the theorem actually proved. The cancellations of the resolvent are classified; the cancellations imposed jointly by the resolvent and the observation constraint are not.

## 8. Major objection IV: cancellation-aware sharpness is lost again when the normalizer varies

The paper is admirably explicit about this limitation.

When the actual pole order nu is smaller than the flag-path count nu_Q, the fixed-normalizer slice can exploit the cancellation and obtains the improved upper law t^{1/nu}.

But for the full positive rational experiment with unknown normalizer, the manuscript does not substitute nu for nu_Q. It states that the scalar interpolation gauge may break cancellations between path products and therefore retains the old path certificate.

Consequently the main unknown-normalizer conclusion is sharp only under the additional hypothesis

nu = nu_Q.

This leaves open precisely the regime introduced by the new cancellation theorem:

nu < nu_Q.

That is not a minor edge case. It is the regime in which the finite Laurent analysis carries new information beyond the v90 path count.

At the stated journal level, I would want one of the following:

1. a gauge-covariant cancellation invariant that survives scalar-normalizer perturbations;
2. a proof that a modified finite test gives the exact unknown-normalizer exponent;
3. a counterexample theorem showing that cancellation can be destroyed arbitrarily and therefore nu_Q is genuinely unavoidable in the full experiment.

At present the paper identifies the problem but does not resolve it.

## 9. Major objection V: the quartic theorem is strong but it is not a theorem about intersecting inverse defects

The profiled quartic theorem assumes:

- strictly positive full-rank channels;
- strict weights;
- tau(P)>0;
- pairwise distinct complete component polynomials;
- interior roots.

These are exactly the hypotheses under which the coefficient inverse is analytic.

Thus the singularity occurs only in the final scalar root-extraction map. The observation-to-coefficient inverse itself is regular.

This is still valuable mathematics. But it should be presented as a sharp second-order theorem for the real-rooted root map after regular coefficient recovery, not as evidence that the paper has classified the intersections where coefficient recovery itself degenerates.

The distinction is important because the proof depends crucially on coefficient displacement being O(t). At tau=0 or rank loss, that first step is unavailable and the entire quartic profile can interact with lower-order coefficient singularities.

A leading-general-journal version should show at least one instance where the quartic splitting variable couples nontrivially to a normalization or channel defect while the exact fibre remains spectrally identifiable.

## 10. Major objection VI: the binary “whole-model” lower perturbation deserves a separate admissibility lemma

The second lower bound in the degree-one binary condition theorem perturbs B while holding q and A fixed, producing the determinant

(1/4){ab y^2 + epsilon y - ab x^2}.

The manuscript then states that this is an admissible tangent for the entire original stochastic model because:

- the pencil has two distinct real roots at the base;
- its analytic rank-one spectral factors are strictly positive at the base;
- positivity persists for sufficiently small epsilon;
- row, column, and total sums recover strict weights and stochastic factors.

I believe this argument is plausible, and I do not presently have a counterexample. But this paragraph carries a large burden: it upgrades an algebraic pencil perturbation into a tangent inside the original constrained stochastic factorization.

For a top-level proof it should be isolated as a lemma and proved with explicit formulas or a precise spectral-factor perturbation argument. In particular, the proof should state:

- which normalized coefficient matrix has the analytic spectral projectors;
- why each recovered rank-one coefficient remains entrywise positive;
- why its total sum remains positive;
- why the two recovered roots remain in the permitted interval;
- why the factorization preserves the fixed total numerator q exactly.

The v90 quotient theorem contains closely related ingredients, so this repair should be straightforward. It should nevertheless not be left compressed inside the lower-bound paragraph.

## 11. The regular bridge theorem: positive assessment and one remaining limitation

I regard Theorem “Exact regular observation-ball modulus” as essentially the correct response to the v91 bridge objection.

The formula with D_Gamma(V_H) is stronger and more careful than a collision-blind multiple of the radial condition.

The remaining limitation concerns eta_d.

The paper proves:

- eta_d gives a global sufficient certificate;
- V_H gives the exact regular differential metric;
- omega_P gives the exact local target diameter;
- eta_d bounds the regular modulus from above;
- there is no uniform reverse comparison when a positive cell floor is allowed to vanish.

This is a coherent architecture.

What is still missing is a positive equivalence theorem on a maximal natural compact regular class. The negative example only shows that reverse comparison fails when the cell floor degenerates. It does not say whether eta_d is quantitatively equivalent to the Fisher condition under fixed margins on:

- cell probabilities;
- channel singular values;
- normalization residual;
- complete-polynomial separation;
- root margins.

This is not, by itself, a rejection-level gap. But such a theorem would greatly clarify whether eta_d is merely a convenient global certificate or a genuinely faithful global condition number on the intended regular class.

## 12. The common-flag theorem is still a structured extension, not a noncommutative classification

The paper now states this limitation more honestly, and the abstract says “admitting a common invariant flag.”

That is appropriate.

The new sharp examples show that:

- the full 1/(kd) path exponent can occur;
- a genuinely noncommuting defective family can attain 1/k;
- cancellations can strictly reduce the naive path count.

These are good results.

But the class still consists of simultaneously triangularizable coefficient algebras. There is no theorem for a general nontriangularizable recovered algebra, and there is no algebraic criterion for when the additive normalization principle survives without a common flag.

I no longer regard this as an overclaim in the current wording. It is simply a limitation that matters to the generality threshold.

## 13. Statistical claims: current assessment

The statistical layer remains one of the stronger parts of the manuscript.

### 13.1 Regular local asymptotic minimax theorem

The exact covariance

V_H = G(J^T H J)^{-1}G^T

has a clear deterministic and statistical meaning.

The finite-permutation Gaussian quotient is the correct object at cross-component root collisions, and the manuscript avoids differentiating the sorting map.

I have no new major objection here.

### 13.2 Arbitrary-point Hellinger-ball minimax theorem

The two-sided comparison with omega_P is general rather than model-specific, but it is clean.

Hellinger distance is the right choice at zero cells. The product bound and two-point testing argument survive singular probabilities without likelihood-ratio denominators.

The semialgebraic Puiseux statement is also appropriate as an envelope theorem.

My earlier novelty objection therefore remains only a novelty objection: the theorem is useful, but it does not by itself explain the model's singularities.

### 13.3 Distinguishing local experiments

The manuscript correctly distinguishes:

- fixed coefficient neighbourhoods;
- expanding tangent experiments;
- shrinking observation balls.

This resolves the apparent conflict between the fixed-neighbourhood N^{-1/m} moving-pair rate and the anchored N^{-1/2} squared-risk rate at a multiple real root.

This distinction should be retained.

## 14. Novelty relative to classical perturbation theory

The current literature positioning is much improved.

The following mechanisms are classical once one has a specified matrix polynomial and coefficient perturbation class:

- resolvent exclusion;
- argument-principle root counting;
- Laurent pole orders;
- Jordan/partial-multiplicity Hölder exponents;
- structured polynomial-eigenvalue perturbation bounds;
- finite triangular inverse expansions.

The manuscript now largely says so.

The observation-specific content is elsewhere:

- recovery of the scalar normalizer from projective probability observations;
- the complete-polynomial joint-projector decomposition;
- the additive separation of scalar normalization error from subsequent matrix perturbation;
- the exact quotient geometry of the stochastic inverse;
- the pullback Fisher metric and unordered target;
- the way the probability normalization constraint restricts admissible Laurent exposure.

The last item is exactly where I think the next decisive theorem lies. A constrained Laurent invariant would make the flag section genuinely more than a classical pole calculation plus a sufficient zero-sum exposure condition.

## 15. Editorial architecture

The manuscript now contains at least four different mathematical experiments:

1. the original real-rooted stochastic model;
2. the regular quotient and categorical sampling experiment;
3. the arbitrary closed-model Hellinger modulus;
4. a broader positive rational common-flag matrix-polynomial extension.

Each is mathematically legitimate.

The difficulty is that the paper now reads as a sequence of increasingly broad closure layers rather than one theorem with a single unavoidable conceptual spine.

At a specialist journal this breadth could be a virtue.

At a leading general journal, the manuscript needs a clearer central theorem that explains why these layers are all manifestations of the same new principle. The additive normalization gauge is the best candidate, but the singular-intersection and cancellation-aware results are not yet complete enough to provide that final unification.

A shorter manuscript would not solve the problem by itself. What is needed is structural compression: fewer theorem families, with one or two genuinely definitive results connecting them.

## 16. A more serious test for the singularity program

The next revision should not add another singular family chosen because it is easy to compute.

A decisive test would satisfy all of the following:

- omega_P(0)=0, so the target is exactly identifiable;
- tau(P)=0 or a channel rank drops, so coefficient recovery is genuinely singular;
- at least one additional defect is present, such as component equality or internal multiplicity;
- the observation germ is reduced to an explicit finite normal form;
- the spectral modulus exponent is computed from that normal form;
- the leading constant, or a finite sharp variational problem for it, is given;
- the result is shown invariant under the finite component quotient.

Such a theorem would directly answer the central objection that has survived from v91.

## 17. A more complete test for the flag program

Similarly, the next flag theorem should not stop at the sufficient condition L_r notin C 11^T.

The paper should determine the first Laurent coefficient that is visible to the admissible perturbation space.

A satisfactory result would:

1. define the full polynomial zero-sum perturbation space;
2. pair each Laurent coefficient with that space;
3. identify the maximal visible order;
4. prove the corresponding upper and lower observation-modulus exponent;
5. then analyze how scalar normalization perturbations transform this visible-order filtration.

This would convert the present exposed-class theorem into an exact constrained perturbation theory.

## 18. Repository and reproducibility audit

Revision 92 improves the repository state, but the exact head still has problems.

### 18.1 Exact reviewed head

The reviewed branch head is:

d55c480f8cdf9f1327b4142bf1bb31a315f71b2b

with commit message:

“A2 v92: pin all 22 active sources, 18 inherited blobs and both verification programs”.

That final commit changes only revisions/a2-v92/SOURCE_MANIFEST.json.

### 18.2 The v92 workflow does not trigger on the actual source set

The workflow .github/workflows/a2-v92-native.yml has a push paths filter containing only:

- .github/workflows/a2-v92-native.yml;
- revisions/a2-v92/BUILD_REQUEST.

It does not include:

- article/v92 manuscript sources;
- rigidity_v92.tex;
- verify_a2_v92.py;
- SOURCE_MANIFEST.json;
- inherited active sources.

Therefore a manuscript, verifier, or manifest change does not automatically trigger the native audit unless BUILD_REQUEST is also touched.

In particular, the final exact-head commit is manifest-only and is outside the configured push paths.

I found no combined commit status on d55c480f8cdf9f1327b4142bf1bb31a315f71b2b through the repository status interface available to me. The workflow-run interface available here exposes only pull-request-triggered runs, so I do not treat the absence of a returned run as proof that no manual dispatch exists. But the push-trigger defect is objective from the committed YAML.

The workflow should either remove the paths restriction or include the complete active source, verifier, and manifest graph.

### 18.3 The manifest provenance fields do not pin v92

revisions/a2-v92/SOURCE_MANIFEST.json declares:

- reviewed_head = d1acb5d047a3c32b2c676ebe76ca0a64f8952ed2, which is the v91 branch head;
- source_pin = aa6798d9030a7f75e95488441fec6058e52c566a, which is the previous v91 review-report commit.

The v92 verifier hardcodes the same aa6798... value and checks only that the manifest repeats it.

Thus neither field identifies the exact v92 revision head d55c480....

The active-source SHA256 inventory is still useful and is a real improvement. But the field names are misleading. The manifest should distinguish at least:

- revision_head;
- previous_review_commit;
- previous_revision_head;
- source-tree content hashes.

The verifier should print and, when run in a Git checkout, optionally verify git rev-parse HEAD against revision_head.

### 18.4 The source audit does not check all declared git_blob fields

The manifest records git_blob values for all active sources, but the verifier checks SHA256 for active files and separately checks git blob identities only for the inherited set.

This is not a mathematical problem, and SHA256 content checking is already substantial. But if git_blob is part of the claimed provenance contract, the script should verify it consistently for every declared entry rather than leaving some fields informational.

### 18.5 Diagnostics remain diagnostics

The v92 script contains useful finite tests for:

- the factor-four regular Hellinger constant;
- the collision quotient formula;
- binary moment identities;
- selected binary phase arcs;
- row-thinning separation;
- one quartic profile;
- the double-root crossover;
- one cancellation example;
- noncommuting sharp families.

This is a good regression suite.

It is not a proof checker for the universal theorems. The script itself says so, correctly. That qualification should remain visible in the manuscript/repository claims.

## 19. Smaller mathematical and expository comments

### 19.1 Rephrase the binary intersection intrinsically

Do not say without qualification that P_* “has” internal multiplicity d. Say that the selected pointed representative has that multiplicity, while the observation fibre contains other multiplicity patterns.

### 19.2 Separate exact-fibre geometry from transverse arcs

At P_* the intrinsic modulus has a constant term D-L. The positive arc order r is therefore a property of a selected approach to a selected representative, not the leading exponent of omega_{P_*}. Make this distinction visually explicit.

### 19.3 Rename the flag cancellation proposition if necessary

“Exact cancellation test” is exact for the Laurent expansion of the resolvent. It is not yet an exact test for the constrained observation modulus. The title should say which object is exact.

### 19.4 State the admissible-pencill perturbation lemma separately

The degree-one binary lower bound will be easier to trust if the stochastic refactorization is a named lemma.

### 19.5 Keep the real-rooted versus positive-rational experiments visibly distinct

The sharp flag examples may have complex root alternatives. The paper currently says this, but the notation Z(M), Lambda, omega_P, and omega_P^{rat} is dense enough that a reader can easily conflate the experiments.

### 19.6 Clarify what “all quantities are observable” means in the quartic theorem

S is observable only after invoking the coefficient recovery proposition and choosing the finite component labelling up to permutation. That is fine. A short sentence describing the actual reconstruction route would make the claim more transparent.

### 19.7 Explain whether eta_d equivalence is expected on fixed-margin compacta

The negative row-thinning example is useful. State whether the author conjectures a reverse bound after fixing cell floors and the usual regular margins.

### 19.8 Reduce theorem-status inflation

Several statements are classical tools specialized to this setting. The strongest new theorems should be visually separated from supporting propositions so that the contribution does not look larger merely because every ingredient has a theorem number.

## 20. What would change my recommendation

At this stage, another revision could change my view if it proves one genuinely definitive theorem rather than adding several additional modules.

The most persuasive options are:

### Option A: a partially identifiable multi-defect normal form

Construct and analyze a point with omega_P(0)=0 where coefficient recovery is singular and at least one other defect is present. Compute the exact modulus exponent and a sharp leading object.

### Option B: an exact constrained Laurent invariant

Replace the exposed-class condition by a finite invariant of the zero-sum perturbation space and prove that it equals the fixed-normalizer Hölder exponent. Then determine how that invariant transforms under the scalar interpolation gauge.

### Option C: a gauge-stable cancellation theorem

Show that the cancellation-reduced pole order, rather than nu_Q, controls the unknown-normalizer experiment under a natural algebraic condition, and prove matching positive lower constructions.

Any one of these, if executed at the level of the best v92 arguments, would materially strengthen the top-four case.

## 21. What I would regard as publishable now

Ignoring the stated top-four target, I regard v92 as a serious and potentially strong specialist paper.

The most compelling core is now:

1. normalization identification and sharp endpoint clock counts;
2. the complete-polynomial observable joint-projector gauge;
3. additive global inverse stability;
4. exact regular quotient and Fisher/minimax geometry;
5. the Hellinger observation-ball bridge;
6. the profiled quartic repeated-root constant and crossover;
7. the common-flag additive extension with exposed sharp examples.

That is already a substantial body of mathematics.

My negative recommendation is therefore not a statement that the paper lacks results. It is a statement about structural finality and general-journal significance.

## 22. Final assessment

Revision 92 is a major improvement over revision 91.

Several objections that were previously rejection-level have been resolved:

- the coefficient inverse across repeated roots is now explicit;
- the regular V_H-to-omega bridge is proved with the correct collision quotient;
- the repeated-root singular modulus has a finite profiled quartic leading constant;
- the double-root crossover is quantified;
- the flag path count is refined by an exact resolvent cancellation test;
- matching positive lower families are supplied on exposed classes;
- the broken v91 source-manifest dependency is repaired.

I therefore would not write the v91 report again.

The remaining reason for rejection at the stated level is more concentrated.

The manuscript still lacks a model-specific theorem for a genuinely intersecting but spectrally identifiable singularity. Its showcase multi-defect intersection is maximally nonidentifiable, so its exact intrinsic modulus is the constant D-L. The interesting monomial arc orders are transverse to a point whose exact fibre already contains every spectral scale.

At the same time, the common-flag section now computes the true resolvent pole but not the true constrained observation exponent when the leading Laurent coefficient is invisible to zero-sum perturbations, and it loses cancellation-awareness again when the unknown scalar normalizer is allowed to vary.

Those two problems are, in my view, the remaining mathematical frontier of the paper.

If the author solves either one at full strength, while tightening the provenance/CI contract, I would be willing to reconsider the manuscript at the stated level.

For the present v92 submission, my recommendation remains **reject at the four-leading-general-mathematics-journal level**, with the important qualification that the manuscript is now substantially stronger, technically more credible, and much closer to a definitive specialist contribution than the versions reviewed earlier.

---

*This is an owner-requested independent external-referee-style assessment of the repository manuscript. It is not a journal-commissioned report and does not represent an editorial decision.*
