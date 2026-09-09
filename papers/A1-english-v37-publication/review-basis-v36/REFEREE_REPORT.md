# Independent referee report on A1 v36

**Manuscript:** *Attainable information and causal compression at exponent collisions*.  
**Author:** Qian Qi.  
**Assessment date:** 8 September 2026.  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica.  
**Reviewed branch:** `revision/a1-english-v36-common-normalization-2026-09-08`.  
**Controlling manuscript commit:** `8f074b8027627a71a81a362b9d15f47975e1f3ae`.  
**Repository tree:** `a01dbba1dc9009e14cfa1b47879d3682d3d51813`.  
**Manuscript directory:** `papers/A1-english-v36-common-normalization/`.  
**Controlling preceding review:** `30ea5daf9c1f5cf345061f940b55bd559e2e1686`, reviewing v35.  
**New review branch:** `review/a1-english-v36-harsh-independent-2026-09-08`.  
**Recommendation:** **Accept the main article. No further mandatory mathematical revision is requested by this report.**

This is an owner-requested, AI-assisted independent referee-style assessment, not a commission or acceptance decision from any named journal. The recommendation concerns the pinned main article and the mathematical scope examined below. It is not a certificate for every companion theorem or all eleven planned papers. Adversarial examination does not require inventing an adverse finding after the established objections have been resolved.

## 1. Recommendation to the editor

The two bounded requests in the controlling v35 report have been answered in the actual manuscript. Corollary 13.3 now uses one admissible normalization and one Fourier row count across the three acquisition problems. Remark 13.4 now explicitly distinguishes crossover orders of a comparison envelope from exact transitions of optimizing controllers. The changes preserve the hypotheses, lower bounds, upper bounds and previously proved consequences. They introduce no new resource or weakened conclusion. [S1, S2]

**I have not established a counterexample or an unresolved fatal proof gap in the principal collision chain, finite-cell realization arguments, or spectral statements examined in this review.** This is a bounded mathematical assessment, not a formal verification claim. Having checked the two revisions, reconsidered the publication-bearing proof chain, and verified the closer literature comparison, I support acceptance of the main article at the requested standard. The editor retains the actual publication decision and may seek further specialist opinions; my recommendation is nevertheless favorable, not another open-ended request for additional theorems.

The mathematical reason is the attained, joint calibration-and-memory classification. The theorem does not merely compute a rank or identify small singular values. It proves that feasible acquisition produces uniformly positive mass in the relevant confluent directions, covers the complete attainable image, and realizes matching upper bounds by one state process charged after every report. The finite-cell algebra and spectral comparison now have their proper supporting roles. Their classical ingredients are acknowledged rather than counted as several independent breakthroughs.

This round also independently rebuilt both complete native volumes. The 80 active TeX inputs match the pinned content-addressed source manifest, the six compiler invocations succeed, and the resulting 42-page main article and 159-page companion have converged actual cross-volume references. These facts close production concerns; they are not the reason for the mathematical recommendation. Exact and numerical diagnostic replays have similarly limited evidentiary roles, set out in Section 7.

## 2. Identity, scope, and disposition of the preceding review

The manuscript commit is dated 8 September 2026, 13:52:18 UTC. Its parent is the controlling v35 review. The revision search was followed to an empty final page. The review is pinned to this commit rather than to the default branch or a floating filename. Native source packages were used only after their relevant objects and active source closure were checked against the repository's pinned manifests. [S0, S8]

The examination covers the current spectral comparison and its two changes, the active introduction and comparison, the exact information and risk definitions, and the principal tangent, mixed/confluent pairing, Newton-flag, whole-image covering and common-filter proof chain. The inherited arguments were considered using their previously read sources and their verified current Git identities. The finite-cell controller arguments and their zero-evidence, randomization and scalarization boundaries were reexamined in the selected current module. The new native build and execution evidence were inspected and independently reproduced.

This is not a fresh line-by-line verification of all 159 companion pages, every inactive historical source, or all planned papers. The primary-source literature check is targeted, not an exhaustive worldwide priority search. The mathematical diagnostics do not prove uniformity over every calibration, every full-support prior, or every Borel controller. These limits constrain what is endorsed; they are not allegations of defects in unexamined material.

| Controlling request | Finding and disposition |
|---|---|
| R35.1: make the fixed-future comparison use literally identical normalized matrices | **Closed.** One H = 16 and one fixed L >= 8 are printed; admissibility over the full square is proved. |
| R35.2: distinguish envelope crossover orders from exact optimizer transitions | **Closed.** The qualification now appears beside the flat-path calculation. |
| Preserve the principal theorem and complete mathematical source | **Verified for the active source closure.** The precise bounded source delta and block preservation checks are recorded below. |
| Current complete native production evidence | **Independently reproduced in this review.** It is no longer merely an inspected author receipt. |

The earlier request for a closer spectral comparison remains answered. A multi-checkpoint optimizer phase diagram was an optional way to strengthen a different contribution hierarchy, not a cumulative condition after the author chose to center the attained collision theorem. It is not imposed now.

## 3. The two v36 corrections: adversarial examination

### 3.1 One normalization, three acquisition lengths

**Location:** Corollary 13.3 and proof, main p. 38; `cor:v35-fixed-future`. [S2]

The future length is two in all three problems. The past lengths are one, two and three, so the total horizons are three, four and five. On the original square, |u|, |v| <= 1/16, the strongest normalization requirement is

$$
5\max(3+v)=5\left(3+\frac1{16}\right)=\frac{245}{16}<16.
$$

The slack is 11/16. Thus H = 16 is admissible for all three horizons without shrinking the parameter square. The common formal positive node list is

$$
\frac1{16}(1,2,2+u,3+u,3+v,4+2u,4+v,5+u+v,6+2v).
$$

It lies in [1/16, 49/128], hence inside the short arc used by Proposition 13.1. With the same fixed integer L >= 8, the matrices are literally identical at each calibration, including repeated columns at collisions. Neither the prior nor the acquisition length enters their definition.

What changes is the acquired cutoff: p_(1,2) = 3, p_(2,2) = 6 and p_(3,2) = 9. The first two checkpoint laws are consequently M^(-2/3) and M^(-1/3), while the third retains the complete three-term envelope. These are separate checkpoint problems with explicitly different total horizons, not an assertion that three incompatible protocols have the same physical history. Both mean and worst-history checkpoint conclusions remain justified.

The componentwise spectral statement also survives at its boundary. Six separated groups give cumulative volume orders 1 through cardinality six, followed by rho, rho squared and rho squared times tau. Ratios of positive cumulative products give the positive singular-value orders. At tau = 0 or rho = 0, the remaining zero singular values follow from exact rank, not from taking a ratio 0/0. The common-H clarification removes an ambiguity without changing this argument.

### 3.2 What the flat-path crossovers actually locate

**Location:** Remark 13.4, main p. 39; `rem:v35-flat-path`. [S2]

Write the three terms as

$$
f_1=M^{-1/3},\qquad f_2=\rho^{1/2}M^{-1/4},\qquad
f_3=(\rho^2\tau)^{2/9}M^{-2/9}.
$$

Balancing the first two gives M_1 = rho^(-6), with value rho squared. Balancing the last two gives M_2 = rho squared times tau^(-8), with value tau squared. The third term at M_1 is rho^(16/9) tau^(2/9), and the first term at M_2 is rho^(-2/3) tau^(8/3). When tau <= rho these do not exceed the balanced values. Thus the claimed regimes concern the actual maximum envelope, not merely two pairwise intersections hidden below a third term.

Moreover,

$$
\frac{M_2}{M_1}=(\rho/\tau)^8.
$$

On the stated flat path this ratio tends to infinity. Substitution gives crossover orders $\exp(6/\theta^2)$ and $\exp(8/\theta^4-2/\theta^2)$. The determinant theorem applies directly because it is uniform on the compact calibration family; it does not require the path gaps to be comparable to finite powers of theta. The finite-power collision-tree specialization has that additional hypothesis and is not invoked for this example.

The correction about exact optimizer thresholds is necessary and now correct. Two-sided comparison constants do not identify an exact integer budget, let alone the transition partition of an optimizing controller. The revised sentence makes this limitation local to the calculation. It does not remove a regime or diminish the proved risk envelope.

## 4. Reexamination of the publication-bearing mathematics

### 4.1 Attained tangent and normalization

**Locations:** Lemmas 3.1–3.2 and the normalized rank argument; `core/03_transversality.tex`. [S3]

The tangent construction is a substantive experiment-level input. At the feasible binomial factors (1+c_i t^D)/2, the polynomials obtained by deleting one factor form a basis through degree n-1 in t^D. Variations in the constant and endpoint monomials supply the multiples jD; variations in each interior exponent supply a+jD. These exponent sets are disjoint because the interior exponents lie strictly between zero and D. The unnormalized tangent therefore has n(r-1)+1 distinct monomial directions.

The mixed pairing is strictly positive for a fixed full-support prior. The determinant integration argument uses separated positive subintervals, each of positive prior mass, rather than a density of the prior. The product itself lies in the tangent. Consequently normalization removes exactly its one-dimensional radial direction, not an unspecified number of dimensions. This supports the acquired dimension min{n(r-1), |mA|-1}; an ambient rank count alone would not.

The continuous-state upper construction is also not an unsupported embedding of an arbitrary curved image into its dimension. It retains normalized factors while that representation is smaller, then makes the single permissible changeover to future moments. Sufficiency is allowed to distinguish more histories than posterior equivalence does. The lower dimension uses an actual local section and invariance of domain.

### 4.2 Confluent flags and acquired probability

**Locations:** Lemma 4.1, Lemma 5.2 and the Newton-scale construction. [S4]

The confluent tests occur in complete multiplicity blocks. Initial Newton divided differences span the appropriate Hermite evaluation functionals even when repeated nodes are not adjacent in the formal order. Adjoining the constant gives the complete test system needed by the mixed-pairing argument. The proof does not select isolated high logarithmic derivatives and assume they inherit positivity.

Uniform continuity at the latent endpoint zero is justified by the positive lower bound on the nonzero one-step exponents. Powers of log t multiplied by t to a uniformly positive exponent remain bounded and vanish there. For each of finitely many formal orderings, the relevant derivative is continuous on the compact calibration set and has full row rank. The resulting lower singular-value bound is therefore uniform.

The probability step includes kernel coordinates in the inverse-function argument and retains the all-failure evidence. The minorization is under the actual joint command/report law. It is not a chart in an attainable image with no mass, and it is not the command distribution after silently dropping evidence. This is how a possibly singular latent prior is consistent with the needed continuous acquired chart.

At an exact collision, an auxiliary complete confluent flag can have more directions than the physical future image. There is no contradiction: the corresponding zero Newton scales annihilate the extra physical directions. Confusing these two ranks would produce a spurious objection to the theorem.

### 4.3 Whole-image entropy and causal implementation

**Locations:** Lemma 4.2 and Theorems 6.1–6.2, main pp. 11 and 15–16. [S4, S5]

For a fixed calibration and report word, the normalized prediction coordinates are rational functions of the commands with positive evidence denominator. Moments and node values enter as real coefficients. Thus bounded semialgebraic format is available without assuming semialgebraic dependence on calibration or a semialgebraic prior.

The thin-rectangle estimate uses the classical real entropy inequality and bounded component counts for affine sections. The recalled real inequality in Comte–Halupczok and the semialgebraic regularity statement of Zhang–Kileel support these inputs. The application is to real sets; it does not use the nonarchimedean theorem of the former paper. Above the attained dimension, almost every section is empty. Below it, projections of the containing rectangle bound the variations by the initial products of side lengths. The separate small-budget argument respects integer M. [L3, L4]

The causal step is indispensable. The filter stores a reachable raw representative, updates it by the positive-evidence moment quotient, and rounds in the next reachable codebook. The quotient is uniformly Lipschitz on segments between reachable moment vectors because these segments are represented by posterior mixtures. The update contains no inverse exponent gap and reads no discarded prefix. The finite-horizon error recurrence then realizes all checkpoint upper bounds with the same number of labels.

For the converse, every streaming state is an admitted checkpoint encoder, and the acquired laws at all checkpoints are prefixes of one common exploration law. Taking the maximum of their lower bounds is therefore legitimate. The proof does not replace a common controller by independently selected encoders when proving the upper bound. I find no unresolved gap in these examined steps.

## 5. Spectral comparison and realization theory

### 5.1 The spectral bridge is valid, with the printed limits

**Location:** Proposition 13.1 and Corollary 13.2, main pp. 37–38. [S2]

For fixed q and L >= q-1, every selected Fourier minor is an alternating polynomial in z_j = exp(i x_j). The product of the pair differences divides this polynomial algebraically; its quotient is bounded on the unit torus for the finitely many row choices. This gives the upper bound for the exterior matrix. Consecutive initial rows and columns attaining the largest Vandermonde product give the lower bound. The chord comparison on [0,1] and the exterior singular-value identity then prove

$$
\prod_{j=1}^{\ell}\sigma_j(F_L(x))\asymp V_\ell(x).
$$

Repeated labels are included by the polynomial identity and exact rank, without a numerical division by a gap. The boundary case q = 1 is consistent. It also demonstrates why the upper comparison constant cannot be uniform in growing L: the column norm is sqrt(L+1), while V_1 = 1. The manuscript explicitly allows L-dependence; this boundary test discharges, rather than establishes, an objection.

Substituting cumulative products into the acquired profile is valid. It identifies the available spectral scales, but the truncation and their interpretation as prediction loss still require Section 4's acquisition and causal arguments. The manuscript now makes precisely that distinction.

### 5.2 The closer literature comparison has been answered

Batenkov–Diederichs–Goldman–Yomdin study the full clustered Fourier–Vandermonde spectrum. Their single-cluster theorem gives the successive powers of the small cluster scale, while their multi-cluster theorem compares the full spectrum with the ordered union of cluster spectra under explicit bandwidth/separation conditions. The relevant Theorems 2.2–2.3 were checked in the primary preprint. A1 does not claim their growing-bandwidth control for its fixed-size exterior comparison. [L1]

Batenkov–Demanet–Goldman–Yomdin also derive minimax reconstruction conclusions, not merely matrix conditioning. Their Definition 3.13 and Theorem 3.14 concern unknown point-source coefficients and support, an entire noisy Fourier observation, and specified superresolution-factor regimes. The separate upper and lower quantifiers matter. A1's comparison retains the distinction between this coefficient reconstruction problem and retained-label prediction excess under a prescribed stochastic experiment. [L2]

Accordingly, neither a Fourier sample count nor reciprocal external noise may simply be renamed M to obtain A1. Conversely, A1 is not evidence that the existing spectral work lacked statistical consequences. The revised section avoids both misrepresentations. The common-future example now gives an exact way to separate spectral geometry from acquisition length. This is a substantive answer to the earlier comparison request, not just an added citation.

I have not established worldwide priority for the exact A1 theorem or located an earlier source proving it in full. That limitation should not be converted into a perpetual requirement for an exhaustive originality certificate. The verified comparisons support the distinction actually needed for this recommendation.

### 5.3 The finite-cell layer remains correctly delimited

**Location:** Section 8, especially Theorems 8.4, 8.9–8.11. [S6]

The one-step body is exactly a finite-output postprocessing region of the auxiliary raw-cell experiment. The physical law is its mixture with the latent cell probabilities; the raw index is not revealed after failure. The shared failure kernel couples its rows. The support formula and common-submeasure overlap have their classical decision-theoretic interpretation, now stated without redundant claims of a new general principle.

Conditional-state propagation gives both necessity and sufficiency for one common controller. The mean-risk identity follows from conditional independence of latent parameter and retained state given the complete history, not from granting the decoder that history. Completing the square yields the checkpoint centroids. The bounds 0 <= b <= w make b squared divided by w continuous at zero occupancy. Likewise, a zero-evidence baseline integrand extends by zero because its numerator is bounded by the evidence squared. The generalized finite-cell algebra therefore does not need individual cell positivity; the later collision and approximation conclusions retain their stronger hypotheses.

Finite-action purification preserves the implementability coefficients, conditional state laws and mean-risk vector when commands are atomless. It does not preserve each history's risk or remove a persistent decoder-indexing seed. The scalarized polyhedral theorem starts from a global minimizer and replaces one affine block at a time; it does not promote a local optimum to a global one. Its half-open tie convention includes atomic boundary mass. It implies no minimax exchange for the maximum-checkpoint objective.

Fixed-M compact collision transfer is a continuous minimization statement. Its all-budget comparison comes from the separate attained theorem. None of these valid supporting conclusions is used as a substitute for the principal result's significance. The preserved one-checkpoint continuum certificate is likewise an exact realization example, not a multistage optimizer classification.

## 6. Scope tests and the significance judgment

The principal conclusion is strong within its chosen resource: simultaneous control over all integer budgets and additive collision strata, for one finite-horizon transducer in the actual experiment. It is not an unrestricted theorem about every information-processing system. Its constants can depend on the detector, horizon and fixed full-support prior, and the program may use known calibration and read-only real constants. The result concerns persistent labels, not bounded workspace, execution time or finite-precision arithmetic.

The fixed-prior qualification is mathematically substantive. As an independent boundary check, let $\mu_\epsilon=(1-\epsilon)\delta_0+\epsilon\operatorname{Unif}[0,1]$, with $0<\epsilon<1$. Each prior has full support. For any bounded future likelihood H, the one-label prediction H(0) satisfies, by conditional Jensen,

$$
\mathbb E\bigl[(\mathbb E[H(t)\mid\text{history}]-H(0))^2\bigr]
\le \mathbb E[(H(t)-H(0))^2]\le\epsilon.
$$

The same bound holds after query averaging and the finite checkpoint maximum. A positive lower constant uniform over all full-support priors would therefore be false at M = 1. The manuscript does not assert such a constant. This is a check of the necessity of a printed boundary, not a counterexample to its theorem.

The distinction between mean and worst-history randomization is equally important, as is the distinction between fixed-M continuity and joint all-budget comparison. Those boundaries remain attached to the conclusions. No hidden weakening or renewed overstatement was found in the reviewed revisions.

In my judgment, the original core's synthesis of attainable transversality, confluent probability geometry and finite-state causal realization is sufficient to support the favorable recommendation. Classical tools do not make a theorem routine when the experiment-specific hypotheses needed to connect them must be proved. Equally, merely accumulating classical consequences would not have made the case. The current hierarchy separates these two considerations convincingly enough. I request no additional mandatory theorem, optimizer computation, asymptotic regime, or expansion of the companion.

## 7. Independent execution, preservation, and production

### 7.1 Source identity and the bounded delta

The current compact source receipt, its v35 base manifest, the native builder and the revised spectral module were directly checked against their pinned GitHub blob identities. The complete 80-file active source manifest was reconstructed from the content-addressed base and the three recorded replacements. Every active byte sequence agrees with it; recursive entrypoint closure and the compiler's recorder agree with the same set. This is not a claim that 80 independent connector fetches were made. [S8]

An independently written delta checker also verifies the old 80-file closure against that base. Seventy-seven paths have identical bytes; `main.tex` changes its selected comparison input, and two old comparison-module paths are replaced in the active closure by their v36 counterparts. Counting complete theorem-like blocks gives 222 before and after, with 220 verbatim multiset matches. The 210 proof blocks have 209 verbatim matches. These counts concern active source blocks, not correctness and not a census of every inactive historical file. Ordinary and optimized executions of this checker agree.

### 7.2 Actual native rebuild by this referee

`audit/reproduce_native.py` verifies source identity and copies the source into a separate new working directory. It runs the unmodified, blob-verified native builder with the actual reviewed commit and edition `v36-referee`. The original source directory and repository are not changed.

The execution on 8 September 2026, 14:02:35–14:02:43 UTC, compiled the complete `main.tex` and `companions.tex` in three paired cycles. All six `pdflatex` invocations returned zero. Actual external labels stabilized; there were no final unresolved references, citations, changing or multiply defined labels, or overfull-box entries. Recorder inputs matched the declared closure. No external-reference stubs or substitute theorem statements were used.

The regenerated PDFs have 42 and 159 pages. Their SHA-256 values are:

- Main: `84d5d46a03188e4fbc185bd4aecf28c8c0c8ff8a2fa13d40e3693c1a61c6a4f5`.
- Companion: `838b6449e886bd9e976586b1da9f26b695b1638e7fd57cf56c9aadd2acedab8a`.

They are not byte-identical to the author's supplied PDFs, and this report does not claim otherwise. Extracted text is identical page by page across all 201 pages. Thirteen selected original/rebuilt raster comparisons are pixel-identical. These checks establish specific production equivalences, not full graphical identity on unrendered pages or mathematical correctness.

All 42 main pages were manually inspected at coarse contact-sheet scale. Main pages 8, 22, 38 and 39 and companion page 80 were additionally inspected enlarged. No apparent clipping, overlap or missing glyphs was identified in these samples. This is not a full-resolution proofread of every equation or a visual inspection of all companion pages. The automated raster comparison and manual inspection are recorded separately.

### 7.3 Mathematical diagnostics: actual replay, limited inference

Five pre-existing mathematical programs were executed both normally and with Python optimization, giving ten successful invocations. Each normal/optimized pair is byte-identical, and every output matches its published recorded hash. Four are the author's current clarification, spectral, finite-cell and inherited-core programs. The fifth is the independent v35 referee checker, which the v36 author did not claim to replay but which was actually replayed in this review. [S9]

The inherited core program reports 298 checks, including 64 complete confluent pairing systems. The prior referee's spectral/boundary program reports 200 checks. These are replays, not newly invented tests attributed to this round. Exact rational identities, finite history enumerations, support-function checks, zero-evidence cases and tie conventions are distinguished from high-precision singular-value diagnostics. The latter are not directed interval certificates. The atomic command examples do not verify atomless purification, and uniform-prior pairing examples do not replace the full-support proof.

The new source-delta, source-identity, native-build and production-comparison scripts supply independent reproducibility checks. None is a formal proof assistant or a global optimizer over all Borel controllers. Successful compilation and finite diagnostics cannot establish editorial distinction; they also should not be ignored when assessing whether a concrete delivery objection has actually been resolved.

## 8. Source ledger and final disposition

All manuscript paths below are relative to `papers/A1-english-v36-common-normalization/` at the controlling commit. Theorem numbers and pages refer to the independently regenerated current main PDF. Stable source labels govern identification if later pagination changes.

**[S0]** Commit `8f074b8027627a71a81a362b9d15f47975e1f3ae`, tree `a01dbba1dc9009e14cfa1b47879d3682d3d51813`. Controlling v35 report: `reviews/a1-english-v35-harsh-independent-2026-09-08/REFEREE_REPORT.md` at `30ea5daf9c1f5cf345061f940b55bd559e2e1686`, blob `d041356c0ca6b6a17750011717af51a7b479d380`.

**[S1]** `RESPONSE_TO_REFEREE_V36.md`, blob `a7a0c5c70dcef2e2dd3ee33c63c2946d8aa1ae92`; `CHANGES_FROM_V35.diff`; `main.tex`, blob `026f6bba962691410bc724677474d3d6b210811f`; current README, blob `7629b2a4360a23679ecd5ed46ea42baed4c03af4`.

**[S2]** Complete `v36/spectral_comparison.tex`, blob `2fd691e92008175c072d04e17a5c7cc1fc79234d`; `v36/comparison.tex`, blob `be6827fbcb9897850a9306c0e6b326dce538d688`. Labels `prop:v35-exterior-spectrum`, `cor:v35-spectral-envelope`, `cor:v35-fixed-future`, `rem:v35-flat-path`.

**[S3]** `core/02_experiments.tex`, blob `1bd4f6273d62c860f8a348dcc4f72734dbc388db`; `core/03_transversality.tex`, blob `6395724ba2c4bed3ead19178a1cfe8206f9a3824`; `text/exact_information.tex`, blob `4d105ba3bd2c9900029530a22438dab288700665`.

**[S4]** `text/analytic_inputs.tex`, blob `92c431918df8894dbab4e2bef267a1b3d086370c`; `text/collision_flags.tex`, blob `558972ba3ad6f42ca1f782b80fed4b7ef9a87fe8`.

**[S5]** `text/main_classification.tex`, blob `307a694dacddee85104212dfa51a222053ee1769`; `text/collision_direct.tex`, blob `12db8bce89cd0a731cb3bc5c383c3c70699ced60`; `text/collision_consequences.tex`, blob `27c4bef2c95c87dc4d91e3d6842d2b5b3b79031c`. Theorem 1.1 is the principal result; Theorems 6.1–6.2 supply its checkpoint and common-controller conclusions.

**[S6]** `v35/moment_controllers.tex`, blob `6c6dd32df4c30a3074870bd5b346cee9cf2c33d4`; `risk_criteria.tex`, blob `da5403fdde6bed138d33b252d52d75e4255c8528`; `text/operational_model.tex`, blob `62b00087d3000d1a6303b7f65479047172a851e2`.

**[S7]** Preserved `v33/finite_compatibility.tex`, blob `6254d766c1469292dbc1125a1eea3fd42de571de`; `v33/precision.tex`, blob `f54e913c2e7e0e0f4db2a5572ded6b53ec431479`; `v33/exact_instance.tex`, blob `8c79906419c9974425fcd0c65d7c6a18eb5dd4a0`. The historical directory names do not make these inactive: the current entrypoint selects them.

**[S8]** `verification-v36/NATIVE_BUILD_V36.json`, blob `f4dbd653b585f0fa446d95653b247b3bffd14268`; base `verification-v35/NATIVE_BUILD_V35.json`, blob `1e5f92cf41b563779ad702c85ee440a470a689fe`; native builder `v35/build_native.py`, blob `66e5fa5a5fe7ba7c551b62bc38afb4c5951823a4`. The independent execution, full source identity and production receipts accompany this report; raw compiler logs are also in the local review package.

**[S9]** `verification-v36/EXECUTION_RECORD.json`, blob `48bd7a55894b749ed3801585ef225ec9676c79fe`, pins the four current diagnostic programs. The fifth is `audit/independent_v35_checks.py` in the controlling v35 review, blob `e06fb129364e549bd6ff99577783346d69be0516`. `audit/replays/REPLAY_RECEIPT.json` records the actual ten invocations without changing historical script provenance.

### Targeted primary literature

**[L1]** D. Batenkov, B. Diederichs, G. Goldman and Y. Yomdin, *The spectral properties of Vandermonde matrices with clustered nodes*, Linear Algebra and its Applications 609 (2021), 37–72. DOI: [10.1016/j.laa.2020.08.034](https://doi.org/10.1016/j.laa.2020.08.034). Primary preprint [arXiv:1909.01927](https://arxiv.org/abs/1909.01927), Theorems 2.2–2.3, printed p. 6. The theorem text was retrieved and that PDF page was visually inspected.

**[L2]** D. Batenkov, L. Demanet, G. Goldman and Y. Yomdin, *Conditioning of partial nonuniform Fourier matrices with clustered nodes*, SIAM Journal on Matrix Analysis and Applications 41 (2020), 199–220. DOI: [10.1137/18M1212197](https://doi.org/10.1137/18M1212197). Primary preprint [arXiv:1809.00658](https://arxiv.org/abs/1809.00658), Definition 3.13 and Theorem 3.14. The relevant parsed primary text was examined; the attempted screenshot did not succeed.

**[L3]** G. Comte and I. Halupczok, *Motivic Vitushkin invariants*, [arXiv:2206.15412v2](https://arxiv.org/abs/2206.15412v2), introduction, equations (4)–(5). Used only for the explicitly recalled classical real variations and entropy inequality, which cites Yomdin–Comte, Theorem 3.5. No independent reconstruction of that entire monograph is claimed.

**[L4]** Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, [arXiv:2311.05116v4](https://arxiv.org/abs/2311.05116v4), Lemma 2.18 and its proof. Used for the bounded-format real semialgebraic regularity input. Relevant primary text was retrieved; the attempted PDF screenshots for [L3] and [L4] failed and are not represented as visual verification.

**Final disposition.** R35.1 and R35.2 are closed. The closer literature comparison and complete current native production concerns remain resolved, with the latter now independently reproduced. Within the stated review scope, I recommend acceptance of the main article and request no further mandatory mathematical revision. This is a referee recommendation, not a journal acceptance or a proof certificate for the entire repository.
