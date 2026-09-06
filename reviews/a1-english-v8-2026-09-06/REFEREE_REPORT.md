# Referee report — A1, English revision 8

**Manuscript:** *Sparse observation algebras, attainable resolution flags, and finite-state memory*  
**Author named in the submission:** Qian Qi  
**Review date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT at the requested four-journal level in its present form.**

This is an owner-requested, AI-assisted external referee-style assessment, not a report commissioned by any named journal. The recommendation is an assessment of this submission's demonstrated mathematical significance. It is not a finding that the main formula is false, a prediction of an actual editorial decision, or a judgment that the research program is impossible.

## 1. Submission identity and audit scope

```text
repository:       TrillionniumFoundation/theta-theory
revision branch:  revision/a1-english-v8-attainable-filtration-2026-09-06
submission SHA:   5d3d7e04b172f98bddfd037c488d93d516d20a98
repository tree:  4666fb5df64e6de9ef985e0fe7c90aaca9b8a252
principal path:   papers/A1-english-v8/
build input:      b6b107e61ae67529043aedee6c4495c7ebda1fae
previous review:  72eb41e358bd9af122367fea66d0de9bdda07456
v7 submission:    02f68484cf92ef312037cf455bd3f3737ae4facd
```

The controlling predecessor is the [v7 report](https://github.com/TrillionniumFoundation/theta-theory/blob/72eb41e358bd9af122367fea66d0de9bdda07456/reviews/a1-english-v7-2026-09-06/REFEREE_REPORT.md) and its [technical note](https://github.com/TrillionniumFoundation/theta-theory/blob/72eb41e358bd9af122367fea66d0de9bdda07456/reviews/a1-english-v7-2026-09-06/TECHNICAL_NOTE.md). The submission is the head identified above, not merely the preceding build-input commit or the response letter.

I read the main source, all eleven principal sections, bibliography, response, proof ledger, reference audit, historical map and diagnostic programs, together with the controlling report and note. The claim-by-claim disposition of all **34 result labels and two operational definitions** is in [CLAIM_AUDIT.md](CLAIM_AUDIT.md). Source line references below are relative to `papers/A1-english-v8/` at the immutable submission SHA. Result numbers refer to the freshly compiled principal PDF.

The authenticated [publication run](https://github.com/TrillionniumFoundation/theta-theory/actions/runs/34009496356) supplied artifact `9982031590`. Its ZIP digest agreed with the GitHub artifact digest. All **24 source-manifest entries** matched their recorded sizes, SHA-256 values and Git blob hashes. The main TeX and the new attainable-filtration source also agreed with the separately retrieved, submission-pinned GitHub blob hashes. The submitted PDF matched its recorded SHA-256. The GitHub comparison from the controlling review to the submission contained 29 added paths and no modified or deleted pre-existing paths. These checks establish the stated provenance and preservation; they do not establish the mathematics.

The author programs were freshly run in a separate extracted copy: **97/97 inherited v7 checks and 255/255 executable v8 checks**. The CI receipt says 256 v8 checks. The difference has an exact explanation: `test_v8.py:208–218` conditionally performs a predecessor-label assertion only when the sibling v7 source directory exists. That directory is absent from the downloaded bundle, so this assertion was not executed locally. I neither count it as passed nor report a mathematical test failure. The repository-level preservation comparison was checked separately.

A separately written program importing no author code passed **327/327 finite check families**, including 24 index-only seven-trial fixtures and **2,688 exact rational raw-update comparisons**. It also checks an attained second-order jet, rather than only the first-order seven-trial example. See [referee_checks.py](referee_checks.py), [INDEPENDENT_DIAGNOSTICS.json](INDEPENDENT_DIAGNOSTICS.json) and [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md). These are diagnostics, not a proof of a continuum entropy theorem or an all-prior statement.

Three fresh pdfLaTeX passes with shell escape disabled produced **37 pages**, no undefined references or citations, no overfull boxes, and two underfull-box notices. All pages were inspected in contact sheets; the new statements and the covering/seven-trial proofs were additionally enlarged, including independent Poppler renders of pages 21 and 25. No material typesetting defect was found. [EXECUTION_REPORT.json](EXECUTION_REPORT.json) records the actual execution and its limits. I did not recompile or freshly re-audit every legacy companion, all historical branches, or all eleven planned papers. Their preservation is not their endorsement.

## 2. Executive judgment

**V8 supplies the general attainable-geometry and causal-compatibility extension whose absence limited v7. That objection is now closed at the printed affine, fixed-horizon scope.** The new result is not a seven-trial example attached to an unchanged full-future theorem. It proves both a dimension-truncated global covering bound and a lower bound on the actually attainable initial flag, then realizes their maximum over stages by physical-moment updates.

I did not identify a blocking counterexample or an essential unfilled step in the principal arguments under their stated hypotheses. In particular, the new semialgebraic argument does not require a semialgebraic prior; the lower bound does not assume that a curved attainable image is a flat box; the zero-calibration rank is proved directly; and the online upper bound does not invert the collision scale or reread an exact prefix.

My negative recommendation is therefore **editorial, not a mathematical refutation**. The paper now presents a coherent, nontrivial class theorem. Nevertheless, after separating its experiment-specific transversality from the classical spectral, entropy and approximation mechanisms, I am not persuaded that the demonstrated contribution has the exceptional depth, reach or consequences required for the requested general-mathematics destination. Section 7 explains this assessment of the strengthened theorem itself. It must not be confused with a claim that the author failed to answer the previous concrete requests.

## 3. Disposition of the controlling review

| V7 item | V8 evidence | Disposition in this review |
|---|---|---|
| E1: theorem-level comparison with clustered spectral work | Introduction, final comparison paragraphs; explicit distinction between classical integer powers and attainable posterior geometry | The requested comparison is supplied and substantially accurate. The editorial significance question is assessed anew, not relabeled as a missing citation. |
| E2: past-limited geometry and general sequential compatibility | Theorems 7.1–7.2, Lemmas 7.3–7.6 and Corollary 7.8 | **Closed for the stated affine class and fixed horizon.** Both sides of the attainable law and genuine streaming realization are proved. |
| E3: do not count the ticket transfer as independent structural depth | Introduction and Section 9 expressly identify it as a consequence | **Closed as a positioning request.** The decision comparison remains valid; it is not a separate geometric advance. |
| P1: positive future length and zero-dimensional convention | Section 5 explicitly fixes positive future length; Section 7 defines trivial cases separately | Closed. |
| P2: necessary budget versus exact threshold | Corollary 9.3, with attribution to the v7 note and the exact uncompressed comparator | Closed. |
| P3: hierarchy and preservation | Class theorem, causal theorem and examples distinguished; pre-existing paths unchanged | Closed at the requested substantive level. A remaining exposition suggestion below is not a demand to delete results. |
| P4: diagnostics versus proof | Scope statements in the programs, response and manuscript | Properly delimited. The local bundle's one conditional omission is documented above. |

The earlier closures concerning actual failure evidence, genuine index-only updates, the common decision baseline and the distinction between a history encoding and a global quotient chart remain closed. A later report should not resurrect them without identifying a new, concrete defect.

## 4. Audit of the new attainable theorem

### 4.1 The correct object is an initial attainable flag

**Sources:** `sections/03_transversality.tex:48–148`; `sections/05_confluence.tex:8–66,117–217`; `sections/06a_attainable_filtration.tex:11–53,227–293`.

The ordering first by jet order and then by limiting exponent matters. A selected coordinate of order k carries with it all preceding orders at that same cluster. Adjoining the constant to the first p nonconstant coordinates therefore produces complete initial jet blocks, where

\[
p=\min\{n(r-1),K_m-1\}.
\]

At positive calibration each such block is an invertible transform of distinct selected monomials. At zero it is a confluent Chebyshev block. The attainable binomial product tangent has n(r−1)+1 distinct monomials, enough to pair surjectively with these p+1 tests. Strict mixed or confluent moment positivity applies for each full-support prior. Normalization removes precisely one dimension because the product itself belongs to the tangent and its constant normalized coordinate is one.

This argument genuinely proves the required flag transversality; it does not assume it. It also explains why selecting arbitrary jets without their predecessors would not be justified by the same proof. The remaining ambient coordinates are not claimed to be independently attainable.

### 4.2 The uniform local lower bound is an acquired-history bound

**Source:** `sections/06a_attainable_filtration.tex:263–293`; Lemma 7.5.

After rank has been established at every calibration, including zero, compactness supplies a positive least row singular value. Uniform second-command-derivative bounds and an interior command radius give a common local inverse construction. Orthonormal row/kernel frames need not depend continuously on calibration: their uniform norm bounds suffice.

The joint command/all-failure law includes its evidence, bounded below by the appropriate power of the command margin. Integrating complementary command coordinates yields a subprobability multiple of a p-dimensional cube in the selected desingularized coordinates. This is the correct distribution for the lower bound. No density of the prior is used; the density being changed in variables is the commanded exploration density. The proof does not condition away the cost of an all-failure prefix.

### 4.3 The global covering step is valid and materially new to this revision

**Source:** `sections/06a_attainable_filtration.tex:95–178`; Lemma 7.3.

The argument uses the real Vitushkin–Ivanov entropy inequality, with variations given by integrals of affine-section component counts. A bounded semialgebraic format supplies coefficient-independent component bounds. Variations above the set's dimension vanish. For a section of codimension j, the translations that can meet the set lie in a j-dimensional projection of the containing rectangle. The projected rectangle is a zonotope; its volume is bounded by a dimensional multiple of the product of the j largest side lengths. Consequently

\[
\mathcal N(S,\varepsilon)
 \le C\sum_{j=0}^{p}\varepsilon^{-j}a_1\cdots a_j.
\]

The use of the dimension p, rather than the ambient dimension q, is justified by the section argument. The proof neither bounds a curved image by an unjustified p-dimensional coordinate chart nor replaces a global cover by the local lower-bound patch.

The integer-budget inversion is also supplied: large M absorbs the constant term, while bounded M is treated by the diameter estimate. Recentering nonempty balls on the reachable set costs only a factor of two. Zero widths and a Borel tie convention are handled. I found no missing logarithmic factor or dependence on a smallest nonzero coefficient in this step. This is an appropriate application of classical real geometry, not a new general entropy inequality.

### 4.4 Bounded format follows from the experiment, not from regularity of the prior

**Source:** `sections/06a_attainable_filtration.tex:180–225`; Lemma 7.4.

For each report word, the evidence and each moment numerator are polynomials in the command entries. The prior integrals, including the logarithmic-test integrals, are fixed real coefficients in these polynomials. A formula with quantified command variables and equations Z(u)y_j=theta^{nu_j}N_j(u) has bounded format, with Z bounded away from zero. Finite union over report words preserves a format bound.

The parameter dependence of those coefficients need not itself be semialgebraic. The covering theorem is applied separately at each calibration with a coefficient-independent constant. This distinction is essential and is correctly made.

For the dimension cap, separately prior-normalizing the n report factors places them in n affine hyperplanes of dimension r−1. The moment map is rational in these coordinates. It therefore has image dimension at most n(r−1), as well as the ambient cap. The uniform side bounds are expectations of uniformly bounded test functions under probability measures. None of these steps assumes a global coordinate chart of the operational quotient.

### 4.5 The physical metric and the lower-center argument match

**Sources:** `sections/05_confluence.tex:162–217`; `sections/06a_attainable_filtration.tex:295–329`.

Newton interpolation gives a fixed nonsingular within-cluster matrix followed by powers theta^{nu_i}. The product-probe expansion is fixed and has full column rank. Thus the actual prediction difference is G D_theta times the desingularized moment difference, with fixed G. The singular diagonal identifies physical widths; it is not an observable supplied to the filter.

Arbitrary decoder centers may first be projected to the physical affine query span and then transformed using a fixed left inverse of G. Projection onto the first p coordinates reduces to a minorized rectangle. Applying the volume lower bound to each initial group of axes gives exactly

\[
\Phi^{\mathrm{att}}_{n,m}(M,\theta)
 =\max_{1\le\ell\le p}
    \theta^{2S_{m,\ell}/\ell}M^{-2/\ell}.
\]

Decoder randomization is removed by conditional averaging, and randomized assignment cannot improve on a nearest center. Independent public coding randomness can be fixed and averaged because it does not generate the acquisition history. These qualifications are sufficient for the declared randomization model. Zero calibration is handled by omitting physically vanishing axes, not by retaining nonexistent information.

### 4.6 The general sequential theorem is genuinely sequential

**Source:** `sections/06a_attainable_filtration.tex:331–423`; Theorem 7.2 and Lemma 7.6.

Keeping all formal raw-moment labels, including labels with coincident values, gives the exact shrinking update

\[
v'_b=\frac{\sum_i f_i(g,x)v_{b+e_i}}{\sum_i f_i(g,x)v_{e_i}}.
\]

The denominator is a report probability. It remains at least the positivity margin on a segment between reachable states, since that segment represents posterior mixtures. Bounded coefficients and coordinates therefore give a calibration-uniform Lipschitz estimate. There is no exponent-separation denominator.

At each stage the global cover has at most M reachable representatives. Updating a representative and then quantizing the result stays within the next reachable domain. The error recurrence accumulates every previous compression error. Taking the maximum stage profile produces the claimed upper rate for every fixed horizon. Conversely, every streaming index is an M-message encoder at each checkpoint; the command laws are prefixes of one common exploration law, so the maximum of checkpoint lower bounds applies to one filter. The order of maximum and infimum is used correctly.

The codebooks and transitions may depend on the known calibration, prior and M. Only the representative label is charged as persistent storage. The result is not effective codebook synthesis, calibration-blind filtering, a workspace bound or a horizon-uniform complexity theorem. Those are declared conventions, not concealed defects.

## 5. Consequences and inherited results

### 5.1 Seven trials: the old obstruction has been resolved

**Source:** `sections/06a_attainable_filtration.tex:450–519`; Corollary 7.8.

At n=4,m=3 the ambient nonconstant order list is six zeros followed by three ones, but p=8. The attainable list has six zeros and two ones. Its intermediate seven-dimensional term is the geometric interpolation of its six- and eight-dimensional endpoint terms. Hence

\[
\mathfrak R_{M,7}(\theta)\asymp
 \max\{M^{-1/3},\theta^{1/2}M^{-1/4}\}.
\]

The crossover has order M=theta^{−6} and regret theta^2. The limiting selected tests, including the constant, pair with the polynomial tangent through degree eight. The independent uniform-prior minor is

\[
\frac{1}{5263867814258605833254325984952320000000000}>0.
\]

This one determinant is a diagnostic; the confluent positivity argument supplies the all-prior assertion.

The extension to the entire interval [0,1/2] is not obtained by falsely assuming that all longer formal sumsets have no positive collisions. Earlier stages use their crude dimension caps, the peak uses its ten distinct three-fold exponents, and later stages use smaller covers. Raw updates tolerate coincident labels. This separately proves the advertised full interval. The previous nine-dimensional extrapolation criticism is therefore inapplicable to v8.

The technical note additionally tests the p=18 checkpoint at n=9,m=5, where an attained second-order jet introduces a third resolution regime. This is a consequence of the v8 theorem, not a demanded extension or a new independent achievement to be counted in its favor.

### 5.2 Decision value and the necessary budget

**Source:** `sections/08_sequential_value.tex:28–214`; Proposition 9.1, Theorem 9.2 and Corollary 9.3.

The ticket identity is correct: integrating the optimal threshold decision over the independent uniform price gives p^2/2, so the optimal value gap for a fixed encoder is one half of its squared-prediction regret. The erased statistic is explicitly the entire exact four-coordinate T_theta in the same experiment, not an optimally selected four-dimensional encoding and not a different raw apparatus.

The exact erasure gap is a positive fixed coefficient times theta^2 E Var(Z_theta|T_theta). Its lower bound follows from the actual minorized five-dimensional cube. Subtracting the full encoder loss from that gap uses a common baseline. The new necessary-budget argument correctly combines the upper erasure loss with the M^{−1/2} lower loss to prove M_beat(theta) asymptotic to theta^{−4}, with integer rounding and the zero-calibration case correctly distinguished.

No exact numerical threshold or equality between two equally compressed experiments follows. The manuscript does not claim either. This is a rigorous operational consequence of the same geometry, not an additional independent mechanism of comparable depth.

### 5.3 Inherited exact, control and mechanical assertions

The normalized sparse rank, continuous-encoding lower bound and factor-to-moment causal representation survive the revision unchanged in substance. The separate control bound uses observable bounded rewards and has the weaker M^{−1/D_A(N)} power; it is not presented as a matching lower bound for arbitrary control problems. The mechanical section uses a different, explicitly uncensored two-cartridge experiment. Its finite partition formula, deterministic optimum, weighted merge loss and small-amplitude three-state threshold are consistent with that experiment's own counting and common risk baseline. I found no new blocking defect in these sections. Their distinct hypotheses should remain visible; their presence does not enlarge the scope of Theorem 7.2.

## 6. Targeted primary-source comparison

I checked the actual statements of Batenkov–Diederichs–Goldman–Yomdin, [arXiv:1909.01927v2](https://arxiv.org/pdf/1909.01927), printed page 6, Theorems 2.2–2.3 and Corollary 2.1. They describe clustered Fourier Vandermonde spectra, including the N^{1/2}(Nh)^{j−1} single-cluster scales and multiplicities in the clustered spectrum. The v8 comparison correctly credits these powers. That paper does not supply this manuscript's normalized attainable-product flag, its acquired-history minorization or its index-only causal theorem. I found no basis for calling the principal result an already published identical theorem.

For the covering input I checked the real statements recalled in Comte–Halupczok, [arXiv:2206.15412](https://arxiv.org/pdf/2206.15412), introduction equations (4)–(5), and the coefficient-independent regularity statement in Zhang–Kileel, [arXiv:2311.05116v4](https://arxiv.org/pdf/2311.05116), Lemma 2.18, printed page 11. Bounded-format quantifier elimination and finite unions legitimately bridge the latter statement to the manuscript's formulas. Only the recalled real entropy inequality is used; no nonarchimedean theorem is imported as a real result. I corroborated the monograph attribution through this primary paper, but did not separately inspect the text of Yomdin–Comte's Theorem 3.5.

The [JMLR primary record](https://jmlr.org/papers/v23/20-1165.html) for Subramanian–Sinha–Seraj–Mahajan confirms the appropriate context of recursive approximate information states and bounded policy-loss transfer. It does not establish the sparse lower bound here. This is a targeted dependency and nearest-comparison check, not an exhaustive priority certification or a complete rereview of every cited work.

## 7. Why I still do not recommend this version to the requested journals

### E8.1 — The genuinely new content is narrower than the combined vocabulary suggests

The paper's strongest contribution is the attainable normalized-product calculation, now strengthened to an ordered confluent flag and made compatible with causal finite-state approximation. That is a real contribution. It should not be diluted by treating a Hilbert-function identity, a spectral hierarchy, a classical entropy inequality, a quantization exponent and an approximation recurrence as five additional major advances.

Once the attainable flag and the bounded-format representation are established, the resolution formula follows from a classical upper-cover/lower-volume mechanism. The general causal step is powerful here because the raw update is a uniformly conditioned rational map, but the error propagation itself is a standard finite-horizon recurrence. The source acknowledges these facts, correctly. My assessment is that the residual experiment-specific theorem is elegant and useful but has not yet been shown to command the breadth or depth expected at the requested destination.

This is not the assertion that a short proof cannot support a major paper, or that combining classical tools cannot be profound. The issue is the importance of the mathematical problem thereby settled and the force of its consequences. I do not identify an earlier equivalent theorem, and I do not describe the new result as a tautology or a false claim.

### E8.2 — A precise class-wide result is not yet a broad useful-memory principle

The new theorem is general within its stated one-parameter affine monomial class. It is no longer restricted to a full-future checkpoint or a five-trial online example. Nevertheless, its sharpness is in M and calibration for a fixed positive experiment, fixed prior and fixed horizon, with read-only exact-real codebooks. Its matching lower task uses prescribed continuous-command exploration and a spanning product-probe family. The general optimal-control bound remains separate and weaker.

These restrictions are not errors. They also are not cosmetic: they determine what the theorem says about observable information and persistent memory. In particular, constants cannot be made uniform over all full-support priors merely by invoking the all-prior rank theorem; the concentration calculation in the technical note explains why. Likewise, an all-failure target may have exponentially small absolute loss at long horizons. The manuscript acknowledges both kinds of limitation.

I therefore assess the paper as a sharp classification for a specified statistical experiment, rather than as a general lower law for artificial intelligence, arbitrary decision making, or effective online computation. The present manuscript largely observes that distinction. The issue for the requested journal is whether the classification itself has sufficiently compelling mathematical significance, not whether more sweeping language could be added to it.

### E8.3 — The displayed consequences mostly expose the same construction

The five- and seven-trial laws are good demonstrations of the theorem; the latter is a genuine test of past limitation. The ticket task is an exact loss transformation, and its erasure comparison uses the same minorized coordinates. The mechanical partition calculation is a distinct operational model but not an application of the full affine attainable-filtration theorem that establishes a further broad mathematical consequence.

The paper accordingly offers one central mechanism with several consistent manifestations. That is sufficient for coherence, but I am not convinced it establishes the exceptional contribution sought here. I would find an independently consequential theorem or application more persuasive than another special horizon, another count of labels, or another successful diagnostic run. This is an explanation of my evaluation, **not a new mandatory theorem checklist**, and no particular extension is promised to produce acceptance. The author has already answered v7's concrete requests and should receive unambiguous credit for doing so.

## 8. Specific, nonblocking corrections and presentation requests

**P8.1 — Make the quantifier order of the online theorem unmistakable.** At Theorem 7.2, state explicitly that for each M and known calibration there exists a stage-compatible M-state filter, with comparison constants uniform in M and calibration. “A single transducer” should mean one filter for all checkpoints of that experiment, not one calibration-blind codebook. The current proof and resource definition support the former reading. No joint-in-calibration computable or measurable codebook selection is proved or needed. The abstract should similarly make clear that comparison constants may depend on the fixed full-support prior.

**P8.2 — Finish the bibliographic version pinning.** Specify the version used for Zhang–Kileel's numbered Lemma 2.18. Add the published record for Comte–Halupczok while retaining the preprint equation locations actually used: *Compositio Mathematica* **161** (2025), no. 5, 959–992, [DOI 10.1112/S0010437X25007031](https://doi.org/10.1112/S0010437X25007031). The existing preprint citation is not mathematically invalid; this is a bibliographic completion, not a rejection ground.

**P8.3 — Let the introduction present the final theorem as the main theorem.** The principal named theorem in the introduction is still the exact-rank predecessor, followed by prose about the stronger uniform classification. A compact, fully quantified statement of the final checkpoint/streaming theorem there would make the article's mathematical center easier to identify. The full-future proof and five-trial realization can remain as explicit subsidiary developments; wholesale deletion of correct proofs is neither necessary nor requested. The hierarchy is much improved already, so this is an exposition request, not a claim that v7 P3 was ignored.

**P8.4 — Make the standalone bundle's skipped assertion visible.** Have the diagnostic receipt record the predecessor-label check as skipped when the sibling directory is absent, or package the exact predecessor input required for that assertion. Silent conditional omission currently changes 256 to 255 without a skip field. This does not affect the analytic proofs or the successful numerical checks. It is a small reproducibility defect in the standalone review bundle.

No displayed central rate needs correction on the evidence of this audit. The two underfull-box notices are not a substantive objection.

## 9. Final recommendation and handoff

**Reject this submission at the requested four-journal level.** The grounds are the demonstrated significance and consequences of the strengthened class theorem, not the old full-future limitation, an alleged missing global cover, a hidden exact-prefix tape, a singular online denominator, or a mismatched decision baseline. Those objections would be inaccurate descriptions of v8.

A subsequent review should start from the closures recorded here, review genuinely new claims on their merits, and keep correctness, originality and editorial significance separate. This audit does not certify the absence of an undiscovered error, establish exhaustive priority, or rule out a more compelling development of the program. It does establish what was actually checked and why this referee-style assessment remains negative at the specifically requested publication level.
