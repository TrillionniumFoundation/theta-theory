# Independent harsh referee report on A2 revision 110

**Manuscript:** *Single-contact recovery of information metrics: sharp thresholds and native realization*  
**Reviewed revision branch:** revision/a2-v110-sharp-threshold-native-realization-2026-09-21  
**Principal source:** papers/A2-v17-boundary-information-coarsening/article/v110/paper.tex  
**Principal source blob:** 51c9ab6b56035f97356870e82734d116980451b9  
**Source-bound mathematical snapshot:** 2e8953cc3fa1f5b9c0b7716a524ea930d3c47c06  
**Controlling preceding referee report:** review/a2-v109-independent-harsh-top4-2026-09-21, commit 87b63e155dac402ec6a9d0a34f69ff0ba5363fdb  
**Verified three-volume workflow run:** 35560676072, completed successfully  
**Date of report:** 21 September 2026  
**Standard applied:** general-journal standard comparable to Annals of Mathematics / Inventiones Mathematicae / Journal of the AMS / Acta Mathematica  
**Recommendation:** **reject in the present form**

This is an owner-requested, AI-assisted external-referee-style assessment. It is not a journal-commissioned report and must not be represented as an editorial decision. I have treated the revision branch as immutable review material and placed this report only on a new isolated review branch.

---

## 1. Executive assessment

Revision 110 is a major mathematical improvement over revision 109.

The previous report identified a precise central defect: the all-dimensional theorem was based on the visibly nonsharp witness \(k=3d+2\), while the proof itself exposed the much more natural product-space problem
\[
   \operatorname{Sym}^2 U\longrightarrow \mathcal P_{2k-2}.
\]
Revision 110 addresses that objection directly. It replaces the engineered interval construction by the exact dimension threshold
\[
   \binom{k-d+1}{2}\ge 2k-1,
\]
and consequently obtains
\[
   k_{\min}(d)
   =
   d+\left\lceil\frac{3+\sqrt{16d+1}}2\right\rceil
   =
   d+2\sqrt d+O(1).
\]
This is the correct natural scale suggested by the dimension count, and the manuscript now proves generic realizability in the loading family rather than only exhibiting one convenient witness.

The paper also makes several other substantive improvements:

1. it separates the monomial additive-basis problem from the unrestricted polynomial-subspace problem;
2. it gives a Grassmannian determinantal formulation of failure and a kernel-to-cokernel tangent map;
3. it identifies an explicit base-point family inside the bad locus;
4. it derives a local distance-to-degeneracy conditioning statement at transverse corank-one points;
5. it extends the realization mechanism to arbitrary fixed linear matrix families and computes the diagonal family sharply;
6. it starts a statistical section from finite categorical observations rather than from an imposed Gaussian contact oracle;
7. it now contains a genuine source-bound, successfully executed three-volume verification receipt.

I therefore regard several of the principal R109 objections as genuinely closed.

I did not find a fatal algebraic counterexample to the sharp threshold theorem in the scope of this review. The dimension algebra is correct. The realization lemma is coherent. The generic global-separation argument is coherent. The rational-curve maximal-rank input appears to be the appropriate classical theorem in the stated range, and the manuscript now attributes that input rather than presenting it as new. The finite diagnostics are also consistent with the displayed small cases.

Nevertheless, I still recommend rejection at the stated top-four standard.

The reason has changed again.

Revision 109 was rejected because it stopped before the sharp mathematical problem. Revision 110 reaches that sharp problem, but in doing so it reveals that the headline threshold itself is largely a transfer of a **classical maximal-rank theorem for general rational curves** through a new but comparatively elementary loading-realization map. The exact threshold follows immediately from that classical maximal-rank statement plus the elementary dimension obstruction once one has shown that the native loading family maps dominantly enough to the Grassmannian.

That transfer is elegant and useful. I do not think it is, by itself, a result of Annals / Inventiones / JAMS / Acta depth.

The other new sections do not presently supply the missing depth:

- the failure-locus section gives the first standard determinantal layer, not a classification or a new theorem about its global geometry;
- the arbitrary-linear-family theorem defines the relevant rank as a maximum \(\rho(\mathcal K,c)\) and then transfers that maximum to generic loadings, so most of the mathematical content is deferred into the undefined quantity \(\rho\);
- the finite-sample contact pipeline first estimates \(\theta\) from the raw data, then computes contact values from \(\widehat\theta\), then inverts those contact values back to approximately \(\widehat\theta\). This is primarily a deterministic re-encoding theorem, not a new statistical inverse theorem based on independently observed contact data;
- the Poisson exposure experiment is a useful explicit regular experiment, but its \(N^{-1}\) risk and efficiency statements are standard smooth-parametric consequences once the map is identified;
- the paper remains built around a highly specialized calibrated square-clock/Hankel experiment.

My overall assessment is therefore:

- **core correctness:** substantially improved and plausible;
- **sharp threshold:** genuinely obtained;
- **previous nonsharpness objection:** closed;
- **genericity:** materially improved;
- **failure geometry:** only partially developed;
- **raw-data connection:** improved, but the advertised contact pipeline is largely tautological as an inference procedure;
- **broader structured-family theorem:** formally correct but mathematically thin in its present abstraction;
- **source-bound reproducibility:** closed;
- **top-four originality/significance:** still not established;
- **recommendation:** reject in the present form.

---

## 2. What revision 110 genuinely accomplishes

The strongest part of the revision is the new theorem architecture.

Let
\[
  R_\theta=JH(\theta)J^{\mathsf T},
  \qquad
  H(\theta)_{ab}=\theta_{a+b},
\]
with \(\theta\in\mathbb R^{2k-1}\). At a smooth contact point with Euclidean normal space \(N\), the second jet determines
\[
   B=Z^{\mathsf T}R_\theta Z
\]
through
\[
   \frac12 Z^{\mathsf T}D^2C_{R_\theta}Z=B^{-1}.
\]

After transporting \(N\) by \(J^{\mathsf T}\), the normal space becomes a polynomial subspace
\[
  U\subset \mathcal P_{k-1}.
\]
The observed bilinear form is the moment functional restricted to the multiplication image
\[
   \operatorname{im}
   \left(
      \operatorname{Sym}^2U
      \longrightarrow
      \mathcal P_{2k-2}
   \right).
\]

The exact fibre statement
\[
   (\theta+\mathcal U^\perp)\cap\Omega
\]
is therefore the right basis-free formulation of the partial-contact inverse problem.

At one contact point, with \(c=k-d\), there can be at most
\[
   \binom{c+1}{2}
\]
independent symmetric products. Hence
\[
   \binom{c+1}{2}\ge 2k-1
\]
is necessary.

Revision 110 then supplies the two ingredients that v109 lacked:

1. a realization/submersion theorem showing that the native loading family reaches a Euclidean-open, Zariski-dense family of normal polynomial spaces; and
2. a classical maximal-rank theorem ensuring that a general \(c\)-plane has maximal multiplication rank.

This closes the dimensional gap exactly.

That is a real theorem. It is much stronger than the old \(k=3d+2\) construction.

---

## 3. Correctness audit of the main threshold theorem

### 3.1 Normal-block reduction

The normal-block lemma is correct in the stated smooth local setting.

For a positive metric \(R\), minimizing the ambient quadratic form over the tangent affine space gives the Schur-complement/normal-block formula. The factor of \(1/2\) in the Hessian convention is handled consistently.

I do not see a normalization error here.

### 3.2 Exact fibre theorem

The exact fibre theorem is essentially finite-dimensional duality after the normal-block lemma, but it is clean and correct.

Equality of the observed normal blocks is equivalent to
\[
   \ell_{\theta'-\theta}(fg)=0
\]
for all within-contact products \(fg\). Thus the fibre is the affine annihilator of the product span.

The paper now appropriately avoids inserting cross-contact products that are not observed.

### 3.3 Native Hankel information derivation

The interpolation argument leading to
\[
   R=JH(\theta)J^{\mathsf T}
\]
remains one of the most model-specific parts of the paper.

The square rational score matrix, interpolation formula, nuisance Schur complement, and Vandermonde rank give the claimed finite moment representation. I did not find an internal contradiction in the displayed derivation.

The positivity of the resulting Hankel matrix follows from the positive atomic representation at distinct clocks.

### 3.4 Positive realization lemma

Lemma 4.1 is an important improvement over v109.

The key identity is
\[
   T=\operatorname{ran}(\operatorname{diag}(Ae_1)A),
   \qquad
   U=J^{\mathsf T}T^\perp.
\]
If \(t>0\) lies in \(T=JU^\perp\), the construction
\[
  z_i=\sqrt{t_i},
  \qquad
  A=[z,\operatorname{diag}(z)^{-1}t_2,\ldots]
\]
does realize the desired tangent plane.

The frame-bundle argument then gives a submersion.

This is, in my view, the genuinely new structural step on which the paper should focus.

### 3.5 Global separation

The finite sign-pattern argument is also coherent.

If
\[
   q_A(\eta)=q_A(e_1),
\]
then
\[
   A\eta=D_sAe_1
\]
for a sign vector \(s\). For each nonconstant sign pattern, the condition
\[
   D_sAe_1\in\operatorname{ran}A
\]
is algebraic and proper. Removing finitely many such sets leaves only the two constant signs.

Properness of \(q_A\) then prevents another remote sheet from accumulating at the contact image.

This is the correct mechanism for upgrading the local normal-space calculation to the global distance function.

### 3.6 Classical maximal rank

The critical external input is Proposition 4.3.

The manuscript invokes classical maximal rank for a general nonspecial rational curve, after observing that a general \(c\)-dimensional linear series on \(\mathbb P^1\) with \(c\ge4\) gives an embedding in \(\mathbb P^{c-1}\).

In the range used by Theorem 1.1, the inequality forces \(c\ge5\), so the embedding issue is not a boundary case.

I found the claimed use of the classical theorem plausible and consistent with the cited Ballico–Ellia literature.

However, because the entire exact threshold depends on this input, a journal version should cite the **exact theorem statement and hypotheses**, not merely two papers and a prose reduction. The proof should make completely explicit:

- which maximal-rank theorem is being applied;
- the degree and ambient dimension;
- why the projected rational normal curve lies in the theorem's general nonspecial family;
- why the relevant multiplication map is exactly restriction of quadrics;
- how the real nonempty open locus is obtained from the complex theorem.

At a top-four standard, the main theorem should not depend on a citation whose precise scope the reader must reconstruct.

### 3.7 Threshold algebra

With \(k=d+c\), the dimension condition is
\[
   \frac{c(c+1)}2\ge2(d+c)-1,
\]
equivalently
\[
   c^2-3c-4d+2\ge0.
\]
The positive root is
\[
   \frac{3+\sqrt{16d+1}}2.
\]
Thus the displayed integer formula for \(k_{\min}(d)\) is correct.

I independently checked the first threshold values against the inequality; the listed cases \(7,8,10,11,13,\ldots\) are consistent.

---

## 4. The main new top-four problem: the sharp theorem is mostly a classical maximal-rank transfer

The exact threshold is a much better theorem than the previous \(3d+2\) result.

But sharpness alone does not establish top-four originality.

Once the fibre theorem and the loading submersion are in place, the existence question becomes:

> Does a general \(c\)-plane in \(H^0(\mathbb P^1,\mathcal O(n))\) have maximal quadratic multiplication rank?

Revision 110 answers this by citing the classical maximal-rank theorem.

Consequently the numerical threshold is not produced by a new classification of native inverse problems, a new theorem on polynomial product spaces, or a new piece of algebraic geometry. It is produced by:

1. the elementary dimension obstruction;
2. a classical maximal-rank theorem;
3. a new realization transfer from loading matrices to a dense family of Grassmannian points.

The third step is valuable, but the manuscript currently overweights the numerical threshold and underdevelops the transfer principle.

For a specialized inverse-problems/algebraic-statistics paper, this architecture may be entirely appropriate.

For a general top-four paper, I would expect one of the following:

- a genuinely new maximal-rank theorem under the native constraints;
- a classification of realizable subspaces that is substantially subtler than density;
- a new multivariate or higher-order product theorem not covered by classical rational-curve postulation;
- a sharp multi-contact theorem with nontrivial incidence geometry;
- a singular inverse/statistical theory whose difficulty is not already resolved by classical maximal rank and the implicit function theorem.

The present paper has not yet crossed that threshold.

---

## 5. The loading realization lemma is elegant, but its mathematics is too short to carry the whole venue claim

The strongest original-looking lemma says, essentially, that the loading map reaches exactly those tangent planes containing a positive vector after the fixed \(J\)-transformation, and that this map is a submersion.

This is a useful observation.

But the proof is a frame change:
\[
  A\mapsto B=\operatorname{diag}(Ae_1)A,
\]
followed by the standard frame-bundle map
\[
  B\mapsto\operatorname{ran}B.
\]

The positivity condition is open, so the image is Euclidean open and hence Zariski dense.

This is clean mathematics. It is not, in its present form, a deep classification theorem.

In particular, the sharp threshold theorem does not discover a subtle native obstruction beyond the obvious positivity condition. It shows that there is essentially **no additional generic algebraic obstruction**.

That is a useful conclusion, but its proof is short enough that the paper needs another major layer of genuinely new mathematics if it is to sustain the stated venue target.

---

## 6. The monomial section correctly separates two problems, but is now secondary

Revision 110 correctly recognizes that the monomial problem is stricter than the general-subspace problem.

For a monomial space
\[
   U_S=\operatorname{span}\{t^a:a\in S\},
\]
full product rank is equivalent to
\[
   S+S=\{0,\ldots,2n\}.
\]

The forced representations of \(0,1,2n-1,2n\) imply
\[
   0,1,n-1,n\in S,
\]
and hence the pair collision
\[
   0+n=1+(n-1).
\]
Therefore one needs at least one more unordered pair than the raw count \(2n+1\), giving
\[
   \binom{|S|+1}{2}\ge2n+2.
\]

This is a neat elementary observation.

It also correctly explains why the unrestricted Grassmannian optimum can beat every monomial space at specific equality cases.

However, this section no longer carries the principal theorem. It is now an illuminating comparison with classical restricted additive bases.

That is the right role for it.

I would resist expanding this section unless the authors actually solve a new additive-basis problem. A catalogue of better monomial witnesses would not strengthen the top-four case.

---

## 7. Failure geometry: useful first layer, not yet a geometric theory

Section 6 is an improvement, but it remains preliminary.

The manuscript defines the tautological multiplication map
\[
   \mu:\operatorname{Sym}^2\mathcal S
        \longrightarrow
        V_{2n}\otimes\mathcal O
\]
over the Grassmannian and studies its determinantal rank loci.

The incidence description via annihilating Hankel forms is natural.

The displayed differential
\[
   \beta_U:
   \operatorname{Hom}(U,V_n/U)
   \longrightarrow
   \operatorname{Hom}(K_U,Q_U)
\]
is the standard kernel-to-cokernel differential for a determinantal rank condition.

The conclusion that the tangent space is \(\ker\beta_U\), and that surjectivity gives the expected codimension, is correct determinantal geometry.

The base-point locus is more interesting. It gives an explicit irreducible family of codimension \(c-1\) contained in corank at least two, and it meets the native realizable open set. This usefully demonstrates that one cannot blindly import generic-matrix codimensions.

Still, the section stops at the first questions.

It does **not** determine:

- the irreducible components of the full bad locus;
- which component dominates near the sharp threshold;
- its degree;
- its generic singularities;
- whether the base-point locus is a component or lies inside larger components in each regime;
- the distribution of condition numbers for random native loadings;
- sharp codimension statements after pullback to loading space;
- multi-contact rank strata;
- asymptotics of the distance to the bad locus as \(d\to\infty\).

The response letter is careful not to claim these results. That restraint is good.

But it also means that the promised “failure geometry” remains largely a formal determinantal setup plus one explicit family.

At a top-four level, I would expect this section to contain one genuinely new global theorem about the rank locus.

---

## 8. The conditioning theorem is local and conditional

Theorem 6.3 states two different facts:

1. generally, the least multiplication singular value is bounded above by a constant times distance to the failure locus;
2. near a real transverse corank-one point, it is comparable above and below to that distance.

This is the correct distinction.

The second conclusion follows from the local Schur-complement row and the surjectivity of the rank-locus differential.

I have no objection to the local theorem itself.

But this is not yet a robust average-case or dimension-uniform conditioning theory. The constants depend on the chosen norms, \(J\), frames, and local chart. No probability estimate is given for random loadings. No lower bound is given on compact design families except the tautological compactness statement away from the bad locus.

Thus the stability section does not yet turn the exact threshold into a quantitative high-dimensional theorem.

That would be one promising direction for a stronger paper.

---

## 9. The arbitrary structured-family theorem is formally broad but mathematically thin

Section 7 defines
\[
   \rho(\mathcal K,c)
\]
to be the maximum rank of the compression map for the structured linear family \(\mathcal K\).

The theorem then says that generic native loadings attain this maximum, so the fibre dimension is
\[
   s-\rho(\mathcal K,c).
\]

This follows from:

- upper semicontinuity / nonvanishing of maximal minors on the Grassmannian;
- the loading submersion/density result;
- ordinary rank-nullity.

As a transfer lemma, this is correct and useful.

As a “general structured-information theorem,” it is close to tautological: all of the hard family-specific mathematics is hidden in the number \(\rho(\mathcal K,c)\), which the theorem does not compute.

The diagonal family is the one nontrivial explicit example, and there the rank calculation is elementary:
\[
  \theta\mapsto\sum_i\theta_i u_iu_i^{\mathsf T}.
\]
The standard vectors \(e_a\) and \(e_a+e_b\) give a basis of \(\operatorname{Sym}_c\), yielding
\[
   \rho=\min\left\{k,\binom{c+1}{2}\right\}.
\]

This is a good example. It is not a broad new theory of structured compression.

For a serious generalization beyond Hankel matrices, I would want explicit sharp formulas for \(\rho(\mathcal K,c)\) for several nontrivial structured families—for example Toeplitz, banded, block-Hankel, low-displacement-rank, graph-sparse, or representation-theoretically defined families—and a theorem explaining which structural invariants determine \(\rho\).

At present R109.4 is closed on the “make the Hankel case genuinely sharp” route. The additional arbitrary-family theorem should be presented as a transfer corollary, not as a second major source of novelty.

---

## 10. The raw categorical theorem is useful, but it estimates the metric directly

Theorem 8.1 is a welcome correction to the previous paper.

The observations are now the actual categorical samples at the clocks.

The estimator
\[
   \widehat\pi_j
\]
is constructed from empirical cell frequencies, and the moment coordinate estimator
\[
   \widehat\theta
   =
   W\bigl(g(\widehat\pi_j)\bigr)_j
\]
has the natural \(O(\sum_j n_j^{-1})\) risk bound on compact interior parameter sets.

This is a legitimate finite-sample result.

But it has an important implication for how the rest of the statistical section should be interpreted:

> the raw data already estimate \(\theta\), and therefore \(R_\theta\), directly.

No contact inversion is needed.

The manuscript acknowledges this point, but the title and response letter still risk suggesting that the finite-sample theorem validates contact tomography as a statistically necessary route.

It does not.

The raw categorical theorem validates the **native metric model** statistically. It does not show that contact data are a statistically sufficient or efficient reduction of the raw experiment.

That distinction matters.

---

## 11. The finite-contact pipeline is essentially deterministic recoding

This is my strongest criticism of the new statistical section.

The paper defines
\[
   \widehat\mu_h=\mu_h(\widehat\theta),
\]
where \(\widehat\theta\) has already been estimated from the raw categorical or Poisson data.

It then reconstructs
\[
   \widetilde\theta_h
\]
from those computed contact values.

Thus the procedure is:

\[
   \text{raw sample}
   \longrightarrow
   \widehat\theta
   \longrightarrow
   \mu_h(\widehat\theta)
   \longrightarrow
   \widetilde\theta_h.
\]

The middle contact representation is not an observed random object. It is a deterministic function of an already available estimator of the parameter of interest.

Consequently the theorem
\[
   \mathbb E\|\widetilde\theta_h-\theta\|^2
   \le
   \frac{2K}{N}
   +
   \frac{2C^2h^4}{\gamma^2}
\]
is mainly a stability theorem for passing an existing estimator through a nonlinear encoding and approximate inverse.

The paper itself says that direct use of \(\widehat\theta\) is more economical. That sentence is correct and should be taken seriously.

I would not advertise Theorem 8.3 as a finite-sample “contact recovery theorem” of the same conceptual status as the geometric identifiability theorem.

A genuinely new statistical contact theorem would require one of the following:

- contact values are themselves physically observed, with a sampling model derived from the original experiment;
- the raw observations can be reduced to contact statistics without first estimating the full \(\theta\), and the information loss of that reduction is quantified;
- an asymptotic equivalence theorem shows that a contact experiment and the original experiment are Le Cam equivalent;
- a semiparametric problem makes contact statistics natural while direct \(\theta\)-estimation is unavailable;
- a singular regime makes the contact geometry determine a nonstandard minimax rate.

Revision 110 does none of these.

Therefore R109.3 is only **partially** closed in the substantive statistical sense.

---

## 12. The Poisson exposure experiment is explicit and valid, but auxiliary

The Poissonized protocol is much cleaner than the earlier ambiguity around exposure parameters.

Now the counts
\[
  N_j\sim\operatorname{Pois}(N\lambda_j)
\]
are themselves observed, so the \(\lambda_j\) are identifiable from the count likelihood.

The displayed covariance
\[
 \Sigma_\theta
 =
 \sum_j
 \frac{\rho_j^2}{\lambda_j^3\kappa_j^2}
 w_{2n}(T_j)w_{2n}(T_j)^{\mathsf T}
\]
is the delta-method image of the Poisson information in the known-mark-law subexperiment.

That calculation is standard and correct.

The open-image statement follows from Vandermonde rank.

Again, however, this is a regular parametric subexperiment introduced to make the exposure coordinates observable. Its local asymptotic minimax conclusion is standard LAN theory after the Jacobian has been identified.

This supports the statistical coherence of the model. It is not a new statistical principle.

The manuscript correctly says this. The venue-level novelty discussion should do the same.

---

## 13. A remaining foundational statistical issue: the root-coalescence baseline is on a boundary

The native score construction is described at
\[
   s=v=0
\]
with retained variance coordinates satisfying
\[
   v_i\ge0.
\]

That means the baseline is on the boundary of the physically constrained variance parameter space.

This has been present in the project for several revisions, but it becomes more important now that the paper makes explicit statistical efficiency claims.

There are at least three logically different objects:

1. a formal Fisher matrix obtained by differentiating a smooth algebraic extension through \(v=0\);
2. the Fisher information of a regular two-sided local statistical model;
3. the local asymptotic experiment of the physically constrained one-sided model \(v_i\ge0\).

These are not automatically the same.

The paper's Poisson exposure efficiency result varies exposure coordinates and therefore avoids this difficulty in that subexperiment. But the broader motivating narrative still identifies the native metric with a profiled information geometry arising at a coalesced-root boundary.

A final statistical treatment should say explicitly which parameter space is being differentiated and why the matrix used in the contact problem is the appropriate information object for the physically admissible experiment.

If a two-sided smooth extension is used merely as a geometric device, say so.

If the physical one-sided root-splitting experiment is intended, then tangent-cone/nonregular asymptotics should be addressed.

I do not regard this as a demonstrated algebraic error in Theorem 1.1. It is a foundational interpretation issue that should not remain implicit in a top-four submission.

---

## 14. Known design weights versus actual sample sizes should be separated more sharply

The fixed-design categorical theorem uses known design weights \(\lambda_j\) in the target information metric while the actual sample sizes are \(n_j\).

Unless the weights satisfy an explicit relation such as
\[
   n_j/N\to\lambda_j,
\]
the metric being estimated is a design-indexed target, not literally the inverse information matrix of the realized finite sample.

The paper partly acknowledges this near the end of Theorem 8.1 by saying that one can instead use the actual weights \(n_j/N\).

That clarification should be moved into the theorem's conceptual setup.

There should be a clean separation between:

- estimating a **prespecified design metric** indexed by \(\lambda\);
- estimating the information of the **realized sample allocation**;
- estimating unknown exposure parameters from observed counts.

The current text is correct enough to reconstruct these distinctions, but it still makes the statistical narrative harder to audit than necessary.

---

## 15. “One contact” remains a full matrix-valued second-jet observation

The manuscript now repeatedly states this, and that is good.

A single contact point does not mean one scalar datum.

The observation is the full normal Hessian block of dimension
\[
   \binom{c+1}{2}.
\]

Near the exact threshold this is precisely large enough to cover the \(2k-1\) moment coordinates.

This is mathematically legitimate, but it matters for interpretation.

The abstract and introduction should continue to make this explicit. Any popular description of “one-point recovery” without the words “full second jet” would be misleading.

---

## 16. The bibliography is improved but still too narrow for the current breadth

Revision 110 has added the right immediate references:

- Ballico–Ellia for maximal rank;
- Mourrain–Pan for polynomial duality / structured matrices;
- Scheiderer for binary-form product spaces;
- Yu and Kohonen for finite/restricted additive bases;
- GKZ for discriminants;
- van der Vaart for regular asymptotics.

This closes the most obvious bibliography defect in v109.

It does not yet provide a convincing literature map for a top-four paper spanning:

- partial quadratic inverse problems;
- structured matrix recovery from compressions;
- Grassmannian multiplication maps;
- algebraic statistics;
- inverse information geometry;
- finite-sample experiment comparison;
- singular inverse problems near rank failure;
- nonregular boundary asymptotics.

In particular, the paper would benefit from distinguishing the classical rational-curve maximal-rank theorem used here from modern broader maximal-rank/postulation results, and from positioning its normal-compression problem relative to structured quadratic sensing and phase retrieval.

The issue is not bibliography length. The issue is that the paper currently claims breadth across several mature areas while the references make the contribution look more isolated than it is.

R109.5 is improved but not fully closed at the level expected for this venue.

---

## 17. Reproducibility and source binding are now genuinely closed

This is a clear success.

The v110 evidence receipt records:

- source-bound execution;
- source commit 2e8953cc3fa1f5b9c0b7716a524ea930d3c47c06;
- source manifest hash;
- principal PDF/log hashes;
- compiler and latexmk versions;
- inherited v109/v108 verification;
- exact diagnostics;
- workflow run 35560676072.

I independently checked the recorded GitHub Actions run.

The review job completed successfully, including:

- checkout of the exact source;
- dependency installation;
- preservation check;
- three-volume build;
- diagnostic replay;
- artifact upload;
- evidence commit step.

This is materially different from the v109 reviewed snapshot, where the verifier existed but the authoritative source-bound execution receipt was absent.

R109.6 is closed.

I would nevertheless move most of this material out of the journal article itself. Commit hashes and workflow receipts belong in a reproducibility supplement or repository metadata, not in the mathematical narrative of a top-four paper.

---

## 18. Independent exact checks

I performed independent consistency checks of several finite aspects of the revision.

### 18.1 Threshold arithmetic

For the first several dimensions, the manuscript's formula agrees with the least integer \(k>d\) satisfying
\[
   \binom{k-d+1}{2}\ge2k-1.
\]

The first values are
\[
   k_{\min}(2)=7,\quad
   k_{\min}(3)=8,\quad
   k_{\min}(4)=10,\quad
   k_{\min}(5)=11,\quad
   k_{\min}(6)=13.
\]

### 18.2 Monomial obstruction examples

At \((d,k)=(3,8)\), one has \(n=7,c=5\). Exhaustion of the \(56\) five-element subsets of \(\{0,\ldots,7\}\) finds no full restricted two-basis.

At \((d,k)=(5,11)\), one has \(n=10,c=6\). Exhaustion of the \(462\) six-element subsets finds no full restricted two-basis.

These checks agree with Proposition 5.1.

### 18.3 Native finite witnesses

The committed diagnostics contain rational/integer loading witnesses at several optimal dimensions and certify the required product ranks by nonzero minors modulo a prime, together with finite sign-class separation checks.

These are useful stress tests.

They are not a proof of the all-dimensional theorem, and the manuscript correctly says so.

### 18.4 Build verification

The exact-source three-volume workflow completed successfully as noted above.

Again, this certifies build/replay integrity, not mathematical correctness.

---

## 19. Assessment of the six R109 requests

### R109.1 — Replace the loose \(k=3d+2\) witness by a sharp or asymptotically sharp threshold

**Closed strongly.**

Revision 110 gives the exact unrestricted native threshold and separates it from the monomial restricted-basis problem.

This is the largest mathematical improvement in the revision.

### R109.2 — Determine genericity and failure geometry

**Materially but not completely closed.**

Generic full rank in the loading family is now proved.

The bad locus is formulated determinantal-geometrically, its tangent map is given, a base-point family is identified, and transverse corank-one conditioning is analyzed.

What remains is a genuinely global theorem about components, codimensions, degrees, or probabilistic conditioning.

For the literal R109 request, the revision is a substantial response. For a top-four venue, the geometry is still preliminary.

### R109.3 — Connect the noisy theorem to actual calibrated observations

**Partially closed.**

The raw categorical observations now appear explicitly and yield a genuine finite-sample estimator of \(\theta\).

However, the finite-contact pipeline computes contact values from that already estimated \(\widehat\theta\). It therefore does not establish contact statistics as an independent observational route.

The Poisson exposure experiment is explicit but auxiliary and regular.

### R109.4 — Broaden the structured-information theorem or make the Hankel case genuinely sharp

**Closed on the sharp-Hankel route.**

The Hankel theorem is now exact.

The arbitrary-family transfer theorem is a useful corollary but is not, in my view, a major separate generalization because the hard quantity \(\rho(\mathcal K,c)\) remains uncomputed except for the diagonal example.

### R109.5 — Expand and correct the literature positioning

**Partially closed.**

The central additive-basis, product-space, maximal-rank, structured-matrix, discriminant, and LAN references are now present.

The broader inverse-problem/statistical positioning is still too thin for the breadth of the paper.

### R109.6 — Commit exact source-bound evidence

**Closed.**

The evidence exists, is source-bound, and the recorded workflow run succeeded.

---

## 20. The paper's present architecture is still not top-four architecture

The principal manuscript is much shorter and cleaner than the historical archive, but it still contains a substantial amount of repository/process material:

- revision numbers;
- exact commit hashes;
- statements about preserved prior versions;
- build receipts;
- descriptions of companion source retention;
- appendices preserving historical results primarily because earlier versions contained them.

This is excellent project hygiene.

It is not the same thing as mathematical exposition.

A top-four manuscript should be written as a definitive paper, not as a changelog that happens to contain theorems.

The final article should have one mathematical spine:

1. the observation-to-product-space fibre theorem;
2. native realization;
3. sharp threshold;
4. genuinely new geometry/statistics beyond the classical maximal-rank transfer.

Historical version provenance should live in the repository or supplement.

The current appendices dilute the central result by preserving too many earlier directions that are no longer part of the strongest theorem.

---

## 21. What would make the work substantially stronger

I do not recommend another revision whose primary action is adding more examples, more verification files, or more local lemmas around the same theorem.

A top-four reconsideration would need a new mathematical layer.

### 21.1 Go beyond the classical rational maximal-rank theorem

The most convincing route would be to formulate a native product-space problem not already solved generically by classical rational-curve postulation.

Examples of genuinely stronger directions include:

- multivariate polynomial normal spaces;
- higher Veronese degree / higher contact order;
- constrained loading families whose Grassmannian image is not dense;
- several coupled structured metric families;
- multi-contact product maps with nontrivial incidence constraints.

A new maximal-rank or rigidity theorem in one of these settings would materially change the paper.

### 21.2 Classify or sharply quantify the failure locus

Determine at least one of:

- irreducible components in the sharp-threshold regime;
- exact codimension of the dominant failure component;
- degree or cohomology class;
- generic singularity type;
- a sharp random-loading tail bound for the smallest multiplication singular value.

The current tangent formula is a starting point, not an endpoint.

### 21.3 Make the statistical contact experiment genuine

Do not estimate \(\theta\) first and then generate contact values from the estimate.

Instead prove that contact-type statistics are directly obtainable from the raw observations, or prove an experiment-equivalence theorem showing that retaining contact information is asymptotically sufficient.

A particularly interesting direction would be a singular regime in which
\[
   \gamma_N\to0
\]
and higher-order contact changes the minimax rate.

That would connect the geometry of the determinantal failure locus to nonregular statistics in a way that the current regular plug-in section does not.

### 21.4 Resolve the boundary/singularity interpretation of the native Fisher geometry

Clarify whether the root-coalescence information matrix is:

- an information matrix of a regular extended model;
- a tangent-cone object of the physical constrained model;
- or simply a geometric quadratic form extracted from formal local expansion.

If a nonregular statistical model is intended, derive its actual local asymptotic experiment.

### 21.5 Compute nontrivial structured-family ranks

If the arbitrary-family theorem is to remain central, calculate \(\rho(\mathcal K,c)\) sharply for nontrivial families beyond diagonal matrices.

Otherwise state the theorem as a useful abstract transfer lemma and keep the focus on the Hankel case.

---

## 22. Detailed proof-level and presentation comments

1. **State the precise maximal-rank citation.** Proposition 4.3 is the hinge of the whole paper. Give the exact external theorem and verify each hypothesis explicitly.

2. **Separate external and internal novelty in Theorem 1.1.** The theorem statement or immediately following discussion should say: dimension obstruction + classical maximal rank + new native realization/global transfer.

3. **Do not let “sharp” imply that the maximal-rank theorem itself is new.** The response letter is careful; the abstract should be equally explicit.

4. **Clarify the real-open/Zariski-open intersection.** The proof is sound in spirit, but a one-line lemma about nonempty real Zariski opens being Euclidean dense on the relevant real chart would make the argument cleaner.

5. **Retain the distinction between local realizability and global separation.** The current remark is good and should remain.

6. **Specify the loading-domain irreducibility used in the genericity proof.** State the ambient affine space and the open conditions being removed.

7. **For the global separation lemma, emphasize that the two preimages \(\pm e_1\) determine the same image germ because the map is even.** This is important to the “one embedded germ” conclusion.

8. **Give the exact dependence of the uniform projection tube on \(A\) and the compact metric set.** Avoid wording that could be read as uniform over all generic loadings.

9. **In the maximal-rank reduction, distinguish projective dimension \(c-1\) from vector-space dimension \(c\) throughout.**

10. **The monomial obstruction is elegant but should not grow into a second paper inside this one.** Keep only what explains the strict gap.

11. **In the failure-locus section, say explicitly “rank exactly \(r\)” wherever the kernel-to-cokernel tangent formula is invoked.**

12. **Do not call the base-point locus a component unless that is proved.** The current text correctly avoids this; keep that restraint.

13. **The local distance comparison needs its norm conventions in the theorem statement or an immediately preceding definition.** “Fixed coefficient norms” is acceptable, but the constants should be visibly local.

14. **Avoid presenting compactness away from \(\Delta\) as a quantitative theorem.** It is a continuity corollary, as the paper currently admits.

15. **Demote Theorem 7.1 unless more \(\rho(\mathcal K,c)\) values are computed.** In its current form it is a generic-rank transfer principle.

16. **For the diagonal example, note explicitly that column-orthonormalizing a full-rank frame preserves linear independence of the outer products up to congruence.** This closes a small presentation gap between an arbitrary row construction and an orthonormal normal frame.

17. **The raw categorical risk theorem should distinguish target-design weights from realized sample proportions at the start, not after the proof.**

18. **State whether the constants in the raw risk bound remain controlled as clocks or roots approach collision.** The paper currently fixes separated roots and clocks, so no uniform singular-limit claim should be inferred.

19. **The Poisson theorem should be labelled an additional observation protocol, not merely a variation of the original fixed-count experiment.** The current text mostly does this.

20. **The known-mark-law efficiency claim should remain explicitly a subexperiment result.** Estimating both marks and exposures can have a different joint efficient covariance.

21. **The finite-contact theorem should be renamed to emphasize that the contacts are computed plug-in features.** “Raw samples to finite-offset encoding and inversion” would be more accurate than language suggesting separately observed contact data.

22. **Do not treat the contact reconstruction risk as a new minimax rate.** The leading \(K/N\) term is inherited from the raw estimator.

23. **The \(h_N=o(N^{-1/4})\) condition is a deterministic approximation-bias requirement in this plug-in construction.** Contrast it clearly with the \(1/(Nh^4)\) variance behavior in the independent Gaussian-contact experiment.

24. **Explain the physical status of the \(v_i=0\), \(v_i\ge0\) boundary.** This is important if “Fisher information” is meant statistically rather than formally.

25. **Keep the independent Gaussian-contact experiment separate.** The current appendix does this correctly.

26. **Move commit hashes and CI descriptions out of the mathematical article.** Keep them in the repository README or supplement.

27. **Remove historical language such as “all earlier results are retained” from the abstract.** A journal abstract should describe the mathematics in the paper, not version-preservation policy.

28. **The title is now substantially better than “contact tomography.”** Keep the narrower title unless the theory is broadened substantially.

29. **The phrase “least ambient dimension” should be read with the model family changing with \(k\).** A short sentence clarifying the comparison class would help.

30. **The paper should explicitly distinguish theorem sharpness within the calibrated family from universality across information models.** The diagonal example already shows family-dependent thresholds.

31. **If the failure geometry remains only local, do not feature it too prominently in the abstract.** The current abstract risks suggesting a fuller classification than is proved.

32. **The exact-source diagnostics should remain outside the correctness proof.** The manuscript currently says this; preserve that boundary.

33. **Do not expand the finite computational witness table as evidence for the universal theorem.** The classical theorem, not the examples, proves universality.

34. **A final version needs a conventional literature-oriented introduction rather than a response-letter introduction.** The mathematical problem should make sense to a reader who has never seen v108/v109.

35. **The paper should state a clean one-paragraph novelty theorem.** At present the reader must reconstruct which ingredients are classical and which are new across the introduction, response file, and dependencies file.

---

## 23. Venue-level significance assessment

The best way to state my concern is this:

Revision 110 has now become a **good theorem-transfer paper**.

It starts from a structured inverse problem, identifies the correct product-space dual object, proves that the native loading family is sufficiently rich, imports a classical maximal-rank theorem, and thereby obtains a sharp threshold. It also supplies several useful extensions and a careful computational/reproducibility package.

That is a substantial achievement.

But the deepest algebraic theorem in the proof is external and classical.

The deepest new proof is the native realization/submersion argument, which is elegant but elementary.

The failure-locus geometry is introductory determinantal geometry rather than a new classification.

The statistical contact theorem is a plug-in re-encoding of a direct estimator.

The general matrix-family extension defers its difficulty into the definition of a maximum rank.

For a broad specialized journal, this package could be strong after substantial editorial tightening.

For Annals / Inventiones / JAMS / Acta, I would expect a new theorem whose proof creates new mathematics at the level where revision 110 currently invokes classical maximal rank or standard regular asymptotics.

---

## 24. Final recommendation

Revision 110 is the strongest version of the A2 line so far.

It directly solves the principal mathematical problem raised in my v109 report: the loose \(k=3d+2\) witness has been replaced by an exact threshold, and genericity in the native loading family is now proved. The determinantal formulation is better, the raw-data discussion is more honest, and the source-bound verification defect is genuinely closed.

I therefore no longer reject the paper because the central recovery theorem is nonsharp.

I reject it at the stated top-four standard because the new sharp theorem is, at its core, a clean transfer of a classical rational-curve maximal-rank theorem through an elementary but useful realization/submersion mechanism. The additional failure-geometry, structured-family, and statistical sections do not yet add a second result of comparable depth. In particular, the advertised finite-contact statistical pipeline is not an independent contact observation theorem: it estimates \(\theta\) first, computes contacts from that estimate, and then reconstructs \(\theta\).

The next decisive advance should not be another local strengthening of the same one-variable Hankel setup. It should introduce genuinely new mathematics: a nonclassical constrained maximal-rank theorem, a global classification/quantitative theory of the failure locus, a multivariate or multi-contact extension, or a true raw-data-to-contact statistical experiment with singular minimax theory.

**Recommendation: reject in the present form for a top-four general mathematics journal.**

**Publication-level summary:** mathematically substantial, materially corrected, plausibly sound in its main algebraic spine, and potentially suitable for a strong specialized venue after refocusing; not yet at the originality/depth threshold of Annals / Inventiones / JAMS / Acta.
