# Response to the independent report on A2 v103

Controlling report: `reviews/a2-v103-independent-harsh-top4-2026-09-20/REFEREE_REPORT.md`, commit `f38495b78e52496d78b44cb5d461fbec65ff530b`.  
Revised mathematical/build source: `ff20178a3ac04712ceed5eb333e1ba3e1c518b74`.  
Principal: `papers/A2-v17-boundary-information-coarsening/article/v104/paper.tex`.

The report identifies a structural rather than a direct correctness objection: the earlier finite-sheet, native-query, and endpoint results were established at different levels of generality. The present revision adds a finite-map reduction theorem, an arbitrary-dimensional minimal endpoint reconstruction theorem, and an exactly classified native probability family. Corollary 5.2 connects these results inside genuine Hellinger observation models. The earlier paper and its historical mathematical record are preserved without alteration; the new principal contains complete proofs of its new results.

The numbering below is from the compiled 18-page v104 principal.

## R103.1 — Extract finite sheets from the original observation germ

**Location:** Definition 2.1, Theorem 2.2, Corollary 2.3, Proposition 2.4, Corollary 2.5, Example 2.6, Theorem 3.1, and Appendix A.

The new starting point is a polynomial map `F: R^r -> R^r`, a polynomial vector residual `G`, and a marked semialgebraic target arc. No inverse-sheet normal form or independent monomial fast equations are assumed. The critical and boundary value set is defined directly from `F`. On a fast target tube avoiding this set, the hypotheses are explicit bounds on `DG DF^{-1}`, its derivative in fast coordinates, and the exact residual on the finite inverse fibre.

Properness and the absence of critical values produce a finite covering of a contractible target tube. Trivializing that covering constructs every inverse branch. Taylor's integral formula then yields the affine residual and a quadratic remainder. The radius-gap inequalities make the latter uniformly small relative to the entire affine residual, even when its exact vertical vector vanishes. The global minimum is localized by its fast coordinate, not by a separately assumed localization lemma.

The proof identifies both inclusions in the complete leading residual set. Its distinct affine sheets, tensor envelope, metric exposed faces, and positive-metric costs are consequently extracted from the marked feasible residual image. The presentation may change, but that residual set does not. Corollary 2.3 states the source and observation-coordinate covariance and the exact uniformity requirements.

Corollary 2.5 verifies the original-map inequalities for coupled weighted initial maps with an isolated zero and a regular marked initial value. Example 2.6 treats `F=(x^2+y^2,xy)` and a target approaching its discriminant with two different branch-separation scales. This enters the nontrivial discriminant regime singled out by the report.

Proposition 2.4 and Theorem A.3 connect real feasible order computations to the gap tests. The residue vectors and limiting fast derivatives are retained in addition to the orders. We do not claim that orders alone determine affine sheets, or that every polynomial singularity automatically satisfies the gap inequalities.

## R103.2 — Native quotient geometry beyond the d=2 witness

**Location:** Theorem 5.1 and Corollaries 5.2–5.3; fixed-pattern discussion at the end of Section 5.

The new native model is a categorical polynomial observation with paired contrast cells. Its observation metric is ordinary Hellinger distance. Positive centre masses are free nuisance coordinates and the retained directions have opposite probability derivatives in each pair. Their nuisance cross block vanishes exactly, so the quotient is

`Q(a) = 4 sum_j z_j z_j^T / a_j`.

Consequently the image is relatively open in `V = span{z_j z_j^T}`, its exact dimension is `s = dim V`, and its normalized nonzero secants are exactly the unit sphere of `V`, of dimension `s-1`. Fixed and deterministic adaptive exact-ray complexities are both exactly `s`. The lower bound uses an adversary in a relative open native image; the upper bound selects a dual basis of legal quadratic evaluations. Thus the generic `2s+1` bound is not sharp in this whole class, and the improvement is structural rather than a new isolated determinant.

The contrasts `e_i` and `e_i+e_j` give full dimension `k(k+1)/2` in every retained dimension `k`. Corollary 5.2 goes further: a fixed experiment can be constructed whose native image contains a neighbourhood of any prescribed positive definite quotient. The fully visible endpoint class therefore occurs natively, and the finite-map reduction is embedded with its relative Hellinger and exact-zero conclusions.

Corollary 5.3 gives the exact rank-drop equations as tensor minors, the formula under retained-coordinate pullback, and polynomial realizations of fixed root patterns. The `X=h^2` calculation distinguishes loss of the first-order split-root coordinate at a collision from the nonzero second-order variance experiment. It does not assert cross-pattern uniformity.

**Scope of this answer:** this is an arbitrary-dimensional classification for the explicitly defined paired-contrast polynomial class. It is not a claim that every higher-degree two-component binary-mixture pattern has now been classified. The v103 binary moment theorem and its sharp fixed-experiment two-variance theorem remain in the supporting volume with their original hypotheses. The general higher-degree binary-pattern classification requested in its strongest form is not claimed as a theorem of v104.

## R103.3 — Higher-dimensional endpoint fibres

**Location:** Definition 4.1, Lemma 4.2, Theorem 4.3, and Propositions 4.4–4.5.

For an arbitrary number `e` of endpoints, full visibility means that the cross block has rank `e` and every active set occurs with strict complementary inequalities on an open visible region. Lemma 4.2 proves that the unlabelled local quadratic matrices form a Boolean lattice under Loewner order: `S_I >= S_J` exactly when `I` is contained in `J`, and the rank of the difference on an inclusion is the number of added endpoints.

The largest local matrix recovers `A`. Its immediate rank-one deficits recover the normalized cross columns up to sign, and the empty-active region fixes every orientation. The smallest local matrix then reconstructs the entire normalized endpoint coupling matrix by an explicit inverse formula. This recovers interactions between endpoints, not only their separate hinges.

Theorem 4.3 proves global minimality against arbitrary competing representations: the intrinsic difference between the largest and smallest local matrices has rank `e`, and every such difference in any representation lies in its cross-block range. Hence no representation with fewer than `e` endpoints exists. A representation with exactly `e` endpoints must realize all `2^e` distinct local polynomials, and the reconstruction applies to it. The entire minimal-dimensional fibre consists of positive diagonal endpoint congruences and permutations. Its continuous dimension is `e`. Normalizing the endpoint diagonal and ordering the oriented columns gives a representative. The minimal distance pair `(T,K)` is unique up to an orthogonal ambient change, with an intrinsic normalized ray Gram matrix.

Proposition 4.4 proves that this is a nonempty open class in every endpoint dimension, rather than a diagonal special case: full column rank together with a strictly positive vector in `ker B^T` makes every active face visible for every positive definite endpoint coupling. Proposition 4.5 gives a finite coordinate-deletion criterion for all positive definite representations, without visibility, and a universal intrinsic lower bound for endpoint dimension.

The fibre theorem is complete on the stated open fully visible class. It does not claim that all nonvisible fibres or all representations with redundant extra coordinates have a single classified normal form. Nor does it assert that iterated coordinate deletion always finds a global minimum outside this class.

## R103.4 — The ray cost as an intrinsic statistical object

**Location:** Theorem 6.1 and Corollary 6.2.

The article now proves a finite-alphabet local likelihood expansion from the probability score paths. The nuisance-free Gaussian limit is `Y ~ N(Qv,Q)`. Its affinity against the centre is `exp(-v^T Qv/8)` and its simple-alternative Neyman–Pearson power is the displayed function of `sqrt(v^T Qv)`. Bidirectional Markov equivalence of the labelled quotient experiments forces equality of these affinities and therefore of `Q`; the converse is immediate.

This makes the ray cost the efficient local discrimination cost of the observation germ. The proof distinguishes the quotient by an unrestricted nuisance translation from an invalid claim that unknown nuisance data can be simulated. Corollary 6.2 proves that the same variational Hellinger cost is obtained from feasible singular root paths, with `n^{-1/4}` repeated-root and `n^{-1/2}` simple/endpoint scales.

This does not turn an exact-query count into a sample-complexity bound. The model, pattern, and oracle family are supplied in the query problem, but the unknown numerical centre is not. If the entire exact centre law is supplied, `Q` is computable directly. These distinctions remain prominent in Sections 5–6.

## R103.5 — Local factorization and real accessibility

**Location:** Lemma A.1, Lemma A.2, Theorem A.3, and Proposition 2.4.

Lemma A.1 proves the individual monomial-times-unit factorization from a normal-crossings product using the primality of coordinate ideals in the real analytic local ring. It separately proves even exponents and common vector factorization for a real sum of squares, including the nonvanishing vector unit.

Lemma A.2 gives the quantified properness argument: lifts of positive-time points have a compact convergent subsequence, so pruning to the closure of the positive-time source does not lose any feasible point. Every divisor face subsequently used in a ratio is exhibited with fixed positive transverse coordinates and a concrete analytic positive-time arc. Theorem A.3 combines the precise uniformization and normal-crossings inputs with these lemmas, and proves the lower bound and matching feasible arc. Inaccessible complex or formal divisors are never substituted for those real arcs.

## R103.6 — Clock-pair quantifier and proof audit

**Location:** Lemmas B.1–B.2 and `QUANTIFIER_AUDIT.md`.

The corrected statement is stronger and precise: for each fixed clock `i`, there exists a clock `j` with distinct component ratios. It does not assert distinctness for an arbitrary prescribed pair, nor one universal pair over a compact family. The finite-cover argument uses locally selected pairs. This is consistent with the existential form already present in the v102 historical source.

Lemma B.2 displays the simple and repeated-interior double-pole columns, their inward endpoint sign, and their linear independence. It explains how the analytic coefficient/stochastic inverse transfers that independence to the full score matrix. The separate audit records the distinction between uniform gap-controlled statements and pointwise opening arcs, fixed-pattern and cross-pattern claims, native family and artificial metric variation, exact zeros and nonzero leading ties, and exact queries and samples.

The historical v103 source is retained verbatim. Appendix B is the operative erratum rather than a silent alteration of the archived review object.

## R103.7 — Source-bound full native receipt

**Location:** `scripts/build_a2_v104.py`, `.github/workflows/a2-v104.yml`, `LOCAL_VALIDATION.json`, and `SOURCE_MANIFEST.json`.

The new principal was compiled locally by native pdfLaTeX/latexmk: 18 pages, no unresolved references or citations, no duplicated labels, no LaTeX warnings, and no overfull/underfull boxes. Its exact source blob identifiers and PDF/log hashes are recorded. The rational/symbolic checker passed. Those checks are explicitly not formal proof verification or full historical compilation.

The full builder replays the actual v103 trigger `618b0b098654f53e61a782138272349df92d16ad` in a detached worktree, using its unchanged builder. A successful old receipt is required before any old PDF is reused. The inherited source hashes and all replay output hashes are checked, then all four v104 volumes are compiled and the native recorder inputs are bound to the new source commit. The workflow is configured to preserve both the exact v103 replay and the four new PDFs, logs, source hashes, and composite receipt on this revision branch only.

At the recorded check, run **35509714156** for source `ff20178a3ac04712ceed5eb333e1ba3e1c518b74` was **pending**, with no conclusion. Full archival native compilation was not executed locally. Therefore **R103.7 and the inherited R102.8 remain runtime-unconfirmed and are not marked closed**. The configured replay is an attempted operational remedy, not fabricated runtime evidence. The durable `native/RUNTIME_RECEIPT.json` is the criterion for closure.

## Editorial changes and preservation

The abstract separates the finite-map class, fully visible endpoint class, and paired-contrast native class. It no longer suggests that one binary two-variance witness proves an all-pattern statement. The introduction identifies the common reduction/profile/discrimination mechanism and cites classical ingredients separately from the reconstruction conclusions. The BMDP corrigendum and the experiment-comparison/statistical background are included in the bibliography.

No inherited mathematical file has been deleted or overwritten. `CONTENT_PRESERVATION.md` maps the earlier main results and archive to the supporting and complete volumes. The new principal is organized as definitions, theorems, and proofs, with real-local and binary-inverse details in appendices. Journal-level significance and universal proof correctness remain matters for the next independent referee; a source commit or certificate count is not a substitute for that review.
