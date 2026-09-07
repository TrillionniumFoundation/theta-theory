# Referee report on A1 English v24

**Main manuscript:** *Attainable information at exponent collisions*, Qian Qi.  
**Companion:** *Attainable information in positive experiments: complete companion developments*.  
**Assessment date:** 7 September 2026.  
**Examined branch:** `revision/a1-english-v24-core-companions-2026-09-07`.  
**Immutable submission:** `6f648bc3da0543e8361b4053ae7da33cb172f597`, `papers/A1-english-v24/`.  
**Controlling report:** `78e948fe03a3969fde4c96411ae1fee5915cb908`, `reviews/a1-english-v23-harsh-independent-2026-09-07/REFEREE_REPORT.md`.  
**Previous submission identified in the response:** `e7c1111d0ab8fb39e4b213902186db2cdf6d0dea`, `papers/A1-english-v23/`.

This is an owner-requested, AI-assisted repository assessment at the requested Annals/Inventiones/JAMS/Acta level of scrutiny. It was not commissioned by any journal and is not a human referee appointment. The independent diagnostics accompanying this report were designed and executed for this assessment without importing the author's implementation. They are finite calculations, not formal verification.

## 1. Recommendation

**I do not recommend acceptance at the requested four-journal level. My recommendation is rejection on the mathematical-significance assessment explained below, not rejection for a demonstrated false principal theorem or an identified unresolved central proof gap.**

The distinction is particularly important in this round. The author has implemented the previous architectural recommendation and put the strongest example near the beginning. Those requests should be closed. The main article now presents the collision theorem through a direct proof rather than requiring the reader to traverse the general transfer framework and the separate developments. I withdraw the previous objection to the principal article's disproportionate architecture. I do not reclassify the reported 20-page main article as a 128-page main article merely because a complete companion has been preserved.

The principal argument survives this assessment's analytic reading and new exact diagnostics. Its strongest step is the uniform acquisition of complete confluent prefixes from actual command histories. The compatibility of that acquisition statement with a cover of the whole image and a gap-independent causal recursion is genuine mathematical content. Describing the result as merely a Vandermonde-rank calculation would be inaccurate.

My remaining negative recommendation concerns the weight of this established, experiment-specific classification. The direct presentation makes its scope and mechanisms clearer, but does not change the mathematical advance whose significance must be judged. I do not find the demonstrated advance exceptional enough for the requested venues. This is an editorial judgment about the result actually proved, not a claim that its exact statement has already appeared in the literature. I have not established that priority claim. Specialization and a finite horizon are not themselves disqualifications; a specialized theorem can certainly have exceptional depth. My assessment here concerns the depth and reach exhibited by this particular theorem and its proof.

There is no new mandatory list of alleged fatal defects in this report. Another rearrangement, another test receipt, or another response paragraph should not be represented as a predictable route to reversing the venue recommendation. Equally, the recommendation is not a no-go conclusion about the research direction, and does not justify weakening a correct theorem.

## 2. Submission identity and scope of this assessment

The revision branch and its commit were resolved through the connected GitHub repository. Mathematical readings were pinned to the immutable submission above. The native source publication, rather than a filename from an earlier package, is the object assessed.

The complete mathematical inclusion route of the main article was read: the introduction and classification statement; the experimental model; the retained-state and risk definitions; the exact information theorem; the transversality proofs; the analytic inputs; the collision flags; the direct checkpoint and streaming proofs; and the bit, tree and two-parameter consequences. The main bibliography and the companion's inclusion structure were also inspected. Within the companion, this assessment additionally read the multistep observation-algebra section, including its acquisition and update arguments, its direct saturated-geometry proof and finite quotient, and the nonlinear-filter comparison.

The previous report and the current response were read to identify what was actually requested and answered. An earlier favorable assessment of an appendix was not silently converted into a fresh audit here. This is not a new exhaustive proof review of the structural, exact-kernel, circular, uncertainty, mechanical, decision or effective-construction developments, nor of the eleven-paper program.

The author reports a 20-page main article and a 108-page companion, preservation of 130 inherited formal statements and 129 complete proofs, and a single documented navigation-only edit in one inherited proof. These are inspected author statements, not independently reproduced preservation counts. This assessment did not reconstruct the 772-file historical manifest, rerun the author's validation suites, rebuild the two volumes, or inspect the manuscript PDFs. Direct runtime repository access was unavailable; authenticated connector source reads were available and used. That limitation is not a mathematical objection to a source publication with an explicit build procedure.

Primary-source PDFs used for the literature checks in Section 9 were separately inspected, including page screenshots. That is not a claim to have visually inspected the submitted PDFs. `REVIEW_SCOPE.json` records the distinction and the GitHub-reported source blob identifiers. All source locators below are relative to `papers/A1-english-v24/` unless another commit is specified.

## 3. Disposition of the controlling requests

| Controlling request | What the v24 source actually does | Disposition |
|---|---|---|
| E23.1: venue-level mathematical significance | The response identifies the collision/acquisition/global-cover/causal conjunction as the principal contribution and requests reassessment without claiming a stronger theorem. The direct main article allows that contribution to be judged on its own. | The response is substantive and candid. The significance disagreement remains; it is not a missing-proof request that can be marked mechanically complete. |
| E23.2: submission-focused architecture without deleting mathematics | `main.tex` includes the complete direct collision route. `companions.tex` organizes the separate developments and alternative routes in a distinct active volume. The main proof does not invoke the transfer, algebra, exact-kernel or mechanical results. | Closed at the source-architecture level. The earlier objection to an overextended principal article is withdrawn. Preservation hashes and final typesetting were not independently certified. |
| E23.3: use the existing two-parameter example earlier | `introduction.tex`, `sec:early-collision-example`, gives the actual four-cell experiment, the 6/8/9-dimensional profile and the two crossover orders. The full argument remains in `cor:two-parameter`. | Closed. No additional example or enlarged theorem is required to satisfy this request. |

The E22.1–E22.4 requests had already been closed by the controlling report. The current source retains the contribution statement, the filtering comparison, the algebra's saturation disclosure and direct proof, and the local algebra risk criteria. They should not be reopened under new numbers.

The new `risk_criteria.tex`, `def:monomial-risks-v24`, is also a useful clarification. It explicitly places the common-filter infimum outside the maximum over checkpoints, averages coding randomness before the worst-history supremum, and defines the actual unconditional acquisition law. The author correctly presents this as clarification, rather than attributing a new mathematical objection to the previous report.

## 4. Main collision theorem: technical assessment

### 4.1 What is observed, what is retained, and what is uniform

The theorem concerns a fixed positive categorical experiment whose likelihood space is a sparse monomial space, a fixed full-support prior on `[0,1]`, a fixed finite horizon, and a compact subset of the strictly ordered one-step exponent chamber. Additive sums may collide inside that chamber. The calibration is known, and the codebook may depend on it and on the integer label budget.

At a checkpoint, a query is selected independently after the index has been retained. It is one of the ordered products of a fixed attainable failure-factor basis. Only the selected query is executed, and all remaining trials are counted. Under squared loss, excess risk is the squared error in its conditional success probability. These conventions are specified in `core/02_experiments.tex`, `text/operational_model.tex` and `risk_criteria.tex`.

The distinction between complete posterior labels and signal-grid sites is essential. The charged resource is the number of possible complete retained states, not the number of support points in a posterior with an uncharged continuously varying weight vector. Conversely, read-only real program data, arithmetic workspace and finite-precision implementation are not charged by `def:finite-state`. The theorem is not a total computational-space or efficient-construction result. Its source does not claim otherwise.

The formal product-probe coefficient matrix remains of full column rank when evaluated exponents coincide. At a collision, reachable raw moment vectors satisfy additional equalities; the symbolic polynomial change of variables does not thereby become singular. The query/raw-moment metric comparison is consequently legitimate. An objection based on a supposed loss of the formal left inverse would target the wrong matrix.

The constants are not asserted uniform over arbitrary full-support priors, over unbounded horizons, or for a single calibration-blind codebook. These restrictions must remain visible when stating the implications, but are not omitted hypotheses in this submission.

### 4.2 Acquisition rank is derived from the experiment

The relevant source is `core/03_transversality.tex`, especially `lem:mixed-moment`, `lem:binomial-tangent` and `eq:normalized-derivative`.

At the common binomial factors, the product tangent has the monomial support

`{jD: 0 <= j <= n} union {a+jD: a in A\{0,D}, 0 <= j < n}`.

Its cardinality is exactly `n(r-1)+1`. Independence of the factor-omission polynomials follows by evaluating at their distinct negative reciprocal roots. The interior exponents lie strictly between zero and `D`, so the claimed tangent exponents cannot coincide accidentally.

The mixed-moment determinant is strictly positive. The integrated determinant identity involves two generalized Vandermonde determinants of the same sign. Full support supplies positive measure on a product of separated interior intervals. A density of the prior is not needed.

The normalization step is then exact, not a dimension heuristic. If `L` is the paired tangent map and `v=L(P)/mu(P)`, then `v` belongs to its image and its constant coordinate is one. On that image the map `w -> w-v e_0(w)` has kernel precisely `span{v}`. Thus exactly one direction is lost, yielding

`d_A(n,m) = min{n(r-1), |mA|-1}`.

This is the acquired dimension, not the dimension of a potentially larger observation-side affine hull. The introductory example `A={0,1,3}`, `n=1,m=2`, correctly has five distinct nonconstant future monomials but only two acquired dimensions. The continuous-state lower bound uses an actual local section and invariance of domain; the upper construction stores normalized factors before a single switch to the shrinking moment state. I found no gap in that argument under the stated continuity convention.

### 4.3 Complete confluence, including exact collisions

The algebraic scale comparison in `text/collision_flags.tex`, `lem:leja-scales`, is valid at zero pivots. Greedy selection bounds the normalized Newton coefficients by one. The leading block on the distinct nodes is triangular with diagonal entries of absolute value one, and hence has a uniformly bounded inverse in the fixed finite dimension. Repeated-node columns have zero scale and are not inverted. Evaluating monic Newton polynomials on arbitrary selected nodes gives

`product_{j<=ell} d_j <= V_{m,ell} <= ell! product_{j<=ell} d_j`.

This comparison alone would not prove the statistical theorem. The important additional argument is `lem:newton-attainment`. Every initial node multiset generates the complete Hermite family at its distinct nodes, including all derivative orders below the relevant multiplicities. Independence of the successive divided-difference functionals on polynomials of increasing degree proves this assertion even for nonadjacent repeated nodes. The proof is not asserting a Chebyshev property for an arbitrary collection of isolated higher derivatives.

Together with the constant test, this complete family pairs with the actual binomial tangent through `lem:confluent-positive` in `text/analytic_inputs.tex`. The normalized derivative is surjective onto every required prefix. Positive exponents remain separated from zero; the bounds on `t^a |log t|^j` justify continuous passage to confluent configurations, including for priors without densities. Compactness for each of finitely many node permutations then gives a positive uniform least row singular value.

The compactness argument is allowed to depend on the fixed prior and horizon. That dependence is central to interpreting the result but does not invalidate the uniformity in calibration claimed here.

### 4.4 Actual mass is not a conditioned command slice

A rank calculation at one command tuple would be insufficient for the unconditional lower bound. The final part of `lem:newton-attainment` addresses this correctly.

The square inverse chart contains both the selected output coordinates and complementary command coordinates. Its inverse maps a product box into the interior command cube. Uniform first- and second-derivative bounds provide a uniform local inverse and the required Jacobian control. The complementary box has positive volume and is integrated out. The all-failure word probability is retained in the joint command-and-report density, with a positive lower bound.

Thus the minorized cube is a subprobability component of the original exploration experiment. It is not a command law conditioned on a selected word, and it is not mass assigned to a frozen lower-dimensional command slice. This supplies the acquired measure needed for the lower bound. I found neither an omitted word-probability factor nor a hidden prior-density assumption.

### 4.5 The upper bound covers the entire attainable image

The source is `text/collision_direct.tex`, `thm:intrinsic-checkpoint`, together with `lem:tame-rectangle`.

For each report word, posterior coordinates are rational functions of the command variables, with numerator degree bounded by the horizon and a strictly positive evidence denominator. Multiplication by the fixed Newton scales gives a bounded-format semialgebraic image. Prior moments and calibration values are real coefficients in that description. They do not have to be semialgebraic functions of calibration for the coefficient-independent format estimate used here.

Normalizing each factor independently places it in an affine hyperplane of dimension `r-1`; this gives the bound by `n(r-1)` for the dimension of the image. Its containing rectangle has the Newton-scaled side lengths. The real variation argument truncates the covering polynomial at the dimension of the set, not at the ambient dimension. The cover is consequently a whole-image cover, rather than the cover of the regular acquisition patch used for the converse.

The classical inputs behind the rectangle estimate are identifiable: a uniform component bound for affine sections, the real Vitushkin entropy inequality, and the volume bound for projections of a rectangle. Sections of codimension exceeding the image dimension are empty almost everywhere in translation. Projection volumes are bounded by products of the largest side lengths. These facts support the printed estimate; they should not be counted as a new general entropy theorem of the paper.

The all-integer-budget step is present. Large budgets absorb the constant term in the covering count; small budgets use one representative and a diameter bound. Empty balls can be discarded and centers replaced by reachable points at a bounded radius cost. Thus the statement is not restricted to an asymptotic sequence of sufficiently large budgets.

### 4.6 The converse admits arbitrary decoder centers

For the lower bound, decoder predictions need not be reachable. Orthogonal projection onto the affine physical query span, followed by the fixed product-probe left inverse and the inverse of the nonzero Newton block, provides uniformly controlled coordinates. Projecting to a prefix of the minorized cube gives a rectangle with side scales `d_1,...,d_ell`.

A union of `M` balls of radius `b` covers at most a constant times `M b^ell/(d_1...d_ell)` of its uniform mass. Choosing `b` at the corresponding volume scale leaves a fixed positive mass uncovered. This gives the squared-error lower bound for every nonzero prefix and every integer budget. Maximizing over prefixes produces the determinant profile.

Randomized label assignments cannot beat nearest-center distance. Private decoder randomization can be averaged under squared loss, and independent public coding randomness can be conditioned on and then integrated. These steps do not license history-correlated randomness as an uncharged storage channel. At exact collisions only the nonzero scaled coordinates enter the metric; the argument does not divide by a vanishing pivot.

### 4.7 A common causal filter, not independent checkpoint encoders

The source is `text/collision_direct.tex`, `thm:intrinsic-streaming` and `eq:formal-multiindex-update`. The recursion uses raw remaining moments, including the constant moment. Multiplication by the next likelihood preserves the required formal indexing, and equal exponent values cause no ambiguity.

An explicit endpoint estimate makes the absence of collision denominators transparent. Write the new likelihood as `f=sum_i f_i t^{a_i}` and set `A_f=sum_i |f_i|`. Let `v,w` be reachable raw moment states, with Bayes denominators `D_v,D_w >= kappa`. For a remaining coordinate, write its numerator as `N(v)`. Since `N(w)/D_w` is a posterior moment in `[0,1]`,

`|N(v)/D_v - N(w)/D_w| <= |N(v)-N(w)|/D_v + [N(w)/D_w] |D_w-D_v|/D_v`

`<= (2 A_f/kappa) ||v-w||_infinity`.

The likelihood coefficients are uniformly bounded. This is a gap-independent Lipschitz estimate in physical raw coordinates; it does not use any reciprocal Newton scale. The manuscript's posterior-mixture segment argument gives the same essential control.

Updating a reachable representative produces a reachable next state, which can be quantized in the next whole-image codebook. The recurrence retains every preceding error. At the fixed horizon its accumulated bound is a constant times the maximum checkpoint profile. The retained state is only the representative index; the exact prefix is used in the proof of the error bound, not by the implemented transition.

For the converse, each fixed common filter induces an admissible checkpoint encoder. Its lower bound holds at every checkpoint under marginals of the same exploration law. Taking the maximum first and the infimum over filters afterward is legitimate and gives the claimed common-filter lower bound. The local risk definition has the same quantifier order. I found no substitution of separately optimized encoders for one causal filter.

## 5. Collision phases: an independent assessment of the flagship example

The early four-cell example is well chosen. It demonstrates something the fixed-calibration rank formula alone does not explain. In `text/collision_consequences.tex`, `cor:two-parameter`, the nine positive two-fold sums form six separated groups and three internal gaps:

`|u|, |v-u|, |v-2u|`.

Writing the gaps in decreasing order as `g_1,g_2,g_3`, one has `g_1 <= 2g_2`, `g_1,g_2` comparable to `rho=max(|u|,|v|)`, and `g_3=tau`. Subset counting gives constant-order determinant volumes through cardinality six, followed by the orders `rho`, `rho^2` and `rho^2 tau`.

The putative seven-dimensional risk term is bounded by the maximum of the six- and eight-dimensional terms because it is their geometric interpolation with weights `3/7` and `4/7`. This is a mathematical redundancy, not a missing term. Consequently the profile is

`max{M^(-1/3), rho^(1/2) M^(-1/4), (rho^2 tau)^(2/9) M^(-2/9)}`.

The exact peak dimensions are six at the intersection, eight on a nontrivial collision line, and nine away from the three lines. The other checkpoints cannot add a larger branch: their acquired dimensions are at most three, six and three, respectively. The explicit detector has the claimed positive bounds and full coefficient rank.

Along `u=theta`, `v=theta+theta^k`, `k>=2`, the determinant valuation list for cardinalities one through nine is

`(0,0,0,0,0,0,1,2,k+2)`.

Equating the first two risk branches gives budget order `theta^(-6)` and regret order `theta^2`. Equating the last two gives budget order `theta^(-(8k-2))` and regret order `theta^(2k)`. The crossovers are separated for `k>1`. The manuscript correctly states comparison orders, not exact integer transition thresholds.

The tree formulation in `thm:collision-tree` also checks out. The triangle inequality forces the pair orders to satisfy the ultrametric inequality in the stated direction. Each pair order is the sum of increments along its common ancestor chain, so the subset energy is the sum of cluster increments times the number of selected pairs in each cluster. The dynamic program follows. A positive common collision order requires a nontrivial cluster below the height-zero root; the diagnostic suite explicitly includes that case.

The bit law is the inversion of the determinant profile, with a bounded change from comparison constants and at most one additional bit from integer rounding. It is useful, but it is not an independent exact-leading-constant quantization theorem. Likewise, once the determinant classification is established, the tree and crossover formulas are consequences of finite subset optimization and valuation arithmetic. Their clarity strengthens the exposition without multiplying the number of independent foundational advances.

## 6. Companion developments inspected in this round

The main result does not depend on the observation-algebra theorem. Nevertheless, its source was inspected because the response relies on separating its role from the monomial problem.

In `sections/algebra_multistep.tex` and `sections/algebra_saturated_geometry.tex`, bounded multiplication yields a whole-history representation `v_n=m+Sigma theta_n`, with uniformly bounded coefficient coordinates. The inverse chart at zero commands has identity first-command derivative. Its probability argument integrates an open neighborhood of the remaining commands and retains the actual all-positive word density. This supplies a ball in coefficient space uniformly over priors.

The sandwich `m+Sigma(rB) subset S_n subset m+Sigma(RB)` then makes the geometry saturated at every positive checkpoint. The finite observable quotient is disclosed and proved. If exactly `t` observable parts have positive prior mass, the covariance rank is `t-1`. The qualitative partition-indicator construction is not used to introduce ill-conditioned coefficients into the quantitative estimates.

The direct proof uses covariance eigenvalues, not their square roots, as geometric scales. Its physical squared-loss factor is `2^(-2(N-n)) delta^2/(d+1)`. The cover handles `M=1`, larger integer budgets and zero rank separately. The lower bound allows arbitrary decoder centers and support loss. The raw update denominator stays positive on posterior mixtures. These arguments are coherent under the stated bounded-multiplication assumptions, including redundant feature representations.

The important editorial distinction is now explicit: this is a prior-uniform classification of an immediately saturated finite observable geometry, not a second instance of delayed acquisition of growing confluent flags. I do not use it as evidence that the monomial theorem is uniform over all priors, nor as a second independent source of the main collision mechanism.

The new diagnostic script primarily tests the monomial route; it is not a fresh computational suite for every algebra representation. The algebra assessment above is an analytic source reading. No new certification of the other companion sections follows from it.

## 7. Mathematical significance after the architectural repair

The proper candidate for exceptional significance is the collision-uniform experimental classification, especially the simultaneous complete-prefix acquisition statement. It is not Newton interpolation in isolation, generic total positivity, an ellipsoid covering estimate, or quantization followed by a stable recursion. The author now credits and distinguishes these components accurately.

My negative venue judgment rests on the following assessment of the assembled result. The decisive experiment-specific step establishes nonvanishing of a family of finite mixed pairings at a common binomial tangent, then turns nonvanishing into uniform acquisition using fixed-dimensional compactness and an inverse chart. The remaining passage to optimal label rates uses established covering and volume mechanisms, while the causal step uses a closed, positive-denominator moment recursion. Making these ingredients compatible at every collision is nontrivial. However, in the form exhibited, I regard it as a strong specialized compatibility and classification argument rather than a sufficiently deep new structural principle for the requested venues.

The multiscale example shows why the result is more informative than a rank theorem. It does not, by itself, establish a broader application or structural consequence outside this experiment class. The tree and bit formulas organize information already contained in the determinant theorem. The saturated algebra result has its own useful prior uniformity, but its immediate ellipsoid geometry does not add comparable conceptual depth to the central collision problem. The companion's theorem count is therefore not a measure of the main article's significance.

This assessment does not rely on demanding assumptions the author never claimed. I do not require an unbounded-horizon theorem, unrestricted-detector theorem, calibration-blind codebook, all-prior monomial uniformity, or an efficient numerical implementation as a newly invented condition for closing the previous requests. Those would be different research problems. The point is instead that the implications of the present result must be weighed within its actual quantifiers, and I do not judge the demonstrated advance sufficient at the selected journal level.

Nor is this a disguised assertion of lack of originality. The targeted literature checks below establish relevant classical mechanisms and model distinctions, not that somebody else has proved this exact theorem. Reasonable specialists could assign greater weight to the uniform acquired-flag conjunction. A journal-level judgment is not converted into a mathematical impossibility theorem by writing it in a referee report.

The architectural response has succeeded. It deserves to remain in the manuscript, not to be undone or answered with another layer of programmatic rhetoric. The author should not be told that a further explanatory paragraph will resolve a disagreement that is now genuinely about the importance of the established mathematics.

## 8. Executed independent diagnostics and their limits

The accompanying `independent_diagnostics.py` uses only the Python standard library and exact `fractions.Fraction` arithmetic. It completed **13,903 explicit checks**. Ordinary Python and `python -O` produced byte-identical JSON receipts. Checks raise exceptions explicitly, so optimization does not disable them. The script's SHA-256 is

`106e1ccd421593488aeddbadcb6fdf4954b2d2d6be87863ea795d6d8a9b03e54`.

`DIAGNOSTICS.json` records the per-category counts. The tests include 48 product-tangent rank calculations; 441 mixed-prefix and evidence-normalized rank cases; 16 finite Leja multisets and 77 maximal-volume comparisons; repeated-node Newton identities; 11 two-parameter contact orders; 12 tree-versus-subset-allocation comparisons; five representative rank strata; 775 complete report-history extensions; 8,065 exact raw-moment update comparisons; and 75 endpoint checks of the gap-independent update bound. Complete report-word probabilities sum to one for the tested command sequences. Integer-profile inverse witnesses, binary rounding, a common-filter quantifier witness and causal error accumulation are checked separately.

For the pairing diagnostics, the priors include beta densities and mixtures of the uniform law with an atom at zero. For positive Newton nodes the exact identity

`integral_0^1 t^alpha [b_1,...,b_j](b -> t^b) beta t^(beta-1) dt = beta (-1)^(j-1) / product_i(beta+alpha+b_i)`

makes the computation rational even at repeated nodes. In the mixed prior the atom at zero contributes zero to these positive-node tests, while its contribution to the constant coordinate is retained. This directly distinguishes paired rank from evidence-normalized rank. These tests do not exhaust all permutations, all priors, or singular full-support measures; the no-density assertion is assessed analytically from the proof.

Six explicit negative controls distinguish omission of the normalization direction, use of ambient dimension instead of acquired dimension, removal of report probabilities, interchange of the filter infimum and checkpoint maximum, deletion of earlier accumulated errors, and invalid use of a large-budget inequality at `M=1`. These are independent diagnostic witnesses, not mutations of the author's source or a formal proof checker.

The counts are execution evidence, not a measure of theorem depth. Finite tests do not prove the uniform positive-mass estimate, the semialgebraic covering theorem, optimal-code lower bounds, arbitrary collision paths or journal suitability. Integer tests concern inversion of the finite model profile, not computation of an exact minimax optimizer. The script does not establish source preservation, successful typesetting, or correctness of all companion results.

The author's 45,393 focused assertions, replay of 3,878 earlier referee checks and 201 additional v24 checks remain separate author-reported receipts. They are not included in the 13,903 new checks. The source README explicitly records a failed branch-specific Actions probe; this assessment does not describe that job as successful CI. Local diagnostic success is not a GitHub Actions receipt.

## 9. Targeted primary-source checks

**[P1]** Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116v4, 6 June 2025. Lemma 2.18, on PDF page 11, was inspected in text and by page screenshot. It supplies the coefficient-independent semialgebraic regularity/component input relevant here. It does not supply experimental acquisition mass, and its general covering results should not be identified without argument with the particular anisotropic estimate of A1. Source: `https://arxiv.org/pdf/2311.05116v4`.

**[P2]** G. Comte and I. Halupczok, *Motivic Vitushkin invariants*, arXiv:2206.15412v2. The introductory real variations and entropy inequality, equations (4)–(5), were inspected, including PDF page 3 by screenshot. These support the classical real input in `lem:tame-rectangle`. No nonarchimedean theorem is being used to prove the real rectangle estimate. Source: `https://arxiv.org/pdf/2206.15412v2`.

**[P3]** G. Pagès and A. Sagna, *Improved error bounds for quantization based numerical schemes for BSDE and nonlinear filtering*, arXiv:1510.01048v3, Section 6, Theorem 6.3 and Remark 6.4. The accessible mathematical text gives normalized-filter error control through weighted squared signal-quantization errors, with explicit normalization, regularity and moment conditions. This supports the acknowledgement of established propagation mechanisms. It does not identify a signal grid size with the number of complete retained posterior labels or establish the collision-uniform minimax converse of A1. Source: `https://arxiv.org/html/1510.01048v3`.

**[P4]** G. Pagès and H. Pham, *Optimal quantization methods for nonlinear filtering with discrete-time observations*, Bernoulli 11(5) (2005), 893–932, DOI `10.3150/bj/1130077599`. Bibliographic and topic information was checked. The publisher full-text request did not provide usable article text, so no full-text inspection of this item is claimed. The technical comparison above relies on the accessible source [P3] and the resource definitions in the submission, not an invented reading of [P4].

This was a targeted check of the main analytic dependencies and the closest cited filtering comparison. It was not an exhaustive literature search establishing either priority or lack of priority for the submitted classification.

## 10. Final disposition

The concrete source-architecture and early-example requests are satisfied. The local risk definitions are clear. The inspected principal proof establishes a coherent route from actual acquisition to whole-image compression and one causal filter, and no fatal counterexample or unresolved central gap was found in this assessment. The new finite diagnostics support, rather than contradict, that route.

My recommendation at the requested four-journal level nevertheless remains negative for the significance reasons stated in Section 7. That disagreement must not be rewritten as a list of mathematical errors the author has not made. The full main argument should be preserved; the complete companion should remain available with its separate hypotheses and evidentiary scope. Any subsequent assessment should start from the pinned sources and the closed dispositions above, rather than recycling objections to older manuscripts.
