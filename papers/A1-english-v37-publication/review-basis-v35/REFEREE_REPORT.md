# Independent referee report on A1 v35

**Manuscript:** *Attainable information and causal compression at exponent collisions*.  
**Author:** Qian Qi.  
**Assessment date:** 8 September 2026.  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica.  
**Controlling revision branch:** `revision/a1-english-v35-spectrum-native-2026-09-08`.  
**Reviewed commit:** `02a19f2ddb83cf68bfbf8361c137613e2ffd3925`.  
**Reviewed repository tree:** `86f7d70a14b464425b934e3d5e62ff8f2a84bb94`.  
**Manuscript directory:** `papers/A1-english-v35-spectrum-native/`.  
**Controlling preceding report:** `a177077ede2b64e11af1efb016eaa6bb5ddf2a13`, reviewing v34.  
**New review branch:** `review/a1-english-v35-harsh-independent-2026-09-08`.  
**Recommendation:** **Minor revision; favorable toward publication of the main article after the bounded clarifications in Section 7. No further major mathematical revision is requested by this report.**

This is an owner-requested, AI-assisted independent referee-style assessment. It is not a journal commission, acceptance decision, or endorsement by any named journal. A request for a harsh review requires adversarial examination, not a predetermined adverse conclusion. The assessment below distinguishes mathematical findings, literature comparison, production evidence, and editorial judgment.

## 1. Recommendation to the editor

The preceding report requested a bounded revision: a closer comparison with clustered Fourier–Vandermonde spectra and superresolution minimax results, a current complete native publication build, and removal of duplicated one-step controller arguments. V35 has answered those requests substantively. The comparison identifies cumulative singular-value products, not merely a least-singular-value analogy. It preserves the distinction between Fourier bandwidth, reconstruction noise and persistent labels. The complete-build receipt is tied to the exact current source objects. The streamlined Blackwell arguments retain their mathematical content. [S1–S5]

**I have not established a fatal counterexample or a fatal gap in the principal collision proof chain or the new spectral statements examined here.** The remaining changes I request are limited clarifications, not repairs of a disproved theorem. I would support publication of the main article following those changes, with the editor retaining the usual independent assessment of breadth, priority and journal fit. This recommendation is more favorable than the v34 recommendation because its principal unresolved objections have been answered, not because compilation or a larger diagnostic count establishes mathematical distinction.

The positive case rests on the inherited attainable collision theorem. It identifies a joint calibration-and-memory law for a family actually produced by an experiment, proves lower mass rather than postulating a quantization rectangle, and realizes matching upper bounds with one per-report finite-state process. The newer spectral bridge explains where the collision scales sit relative to established matrix theory. It does not itself create a second deep classification, and the manuscript now gives it appropriately secondary weight.

This is not an unqualified certificate of every companion theorem or worldwide originality. The audit has the coverage stated in Section 2. In particular, no positive assessment of the main article should be extrapolated to all eleven planned papers. Nevertheless, the objections established by this review do not justify demanding another unrelated theorem, an efficient optimizer, or an indefinitely expanding revision. The core result must now be evaluated on its own mathematical merits rather than against repeatedly enlarged requirements.

## 2. Identity, scope and disposition of v34

The reviewed commit is dated 8 September 2026, 13:02:16 UTC. Its parent is the controlling v34 review. The revision search was followed to an empty final page; the manuscript is pinned to its commit rather than to the moving default branch. The response explicitly addresses R34.1–R34.3, not an amalgam of all historical referee suggestions. [S0, S1]

I read the current spectral comparison, introduction, comparison section, entry point, changed Blackwell proofs, native builder, complete v35 build receipt and sampled-visual-inspection record. I examined the inherited exact-information, tangent, positivity, confluent-flag, covering and common-filter chain available in the preceding source reads, using the identical Git objects confirmed in the current source manifest. The complete general finite-cell arguments and their risk boundaries were considered in that same versioned context. The new numerical program was fetched, reproduced byte for byte against its Git blob, and executed.

This is not a fresh line-by-line audit of all 159 companion pages or every historical derivation. **I did not independently compile the native manuscript or visually inspect its PDFs in this assessment.** I inspected the author's current execution records and independently verified their source identity. Targeted primary-source reading supports the literature comparison; it is not an exhaustive originality search. The separate computations in Section 8 are finite diagnostics, not formal verification of continuum theorems.

| Controlling v34 request | Finding in this assessment |
|---|---|
| R34.1: compare closer full-spectrum and superresolution results | **Substantively answered.** The specified results are compared at theorem, parameter and loss level; the auxiliary spectral bridge is proved with its fixed-size qualification. |
| R34.2: supply a current complete native build | **Closed as an absence-of-current-build-evidence objection.** The receipt describes the actual two entry points, not a stubbed smoke harness, and all 80 listed TeX objects match the reviewed tree. This is not an independent referee rebuild. |
| R34.3: reduce duplicated Blackwell exposition without losing quantifiers | **Answered in the examined edits.** Identification is proved once, the support and compactness proof remains, and overlap invokes the already established common submeasure. |

The earlier alternative—center the attained collision theorem and treat controller algebra as realization theory—remains legitimate. A new multi-checkpoint optimizer phase diagram was not a cumulative condition of that alternative and is not imposed now. Conversely, answering the requests is not by itself a proof of significance: the substantive grounds for the present recommendation are stated in Section 6.

## 3. New spectral statements: mathematical audit

### 3.1 Exterior products, including exact repeated nodes

**Location:** `prop:v35-exterior-spectrum`, `v35/spectral_comparison.tex`. [S2]

For fixed $q$ and $L\ge q-1$, put

$$
F_L(x)=(e^{\mathrm i kx_j})_{0\le k\le L,\ 1\le j\le q},
\qquad x\in[0,1]^q.
$$

The proposition asserts uniform comparison between the largest $\ell$-node Vandermonde volume $V_\ell(x)$ and the product of the first $\ell$ singular values. Its proof is correct under the printed fixed-size and short-arc hypotheses.

Writing $z_j=e^{\mathrm i x_j}$, every selected row-and-column minor is an alternating polynomial in the selected $z$ variables. Each pair difference divides it; the distinct linear factors are relatively prime, so their product divides it. The quotient is a polynomial, uniformly bounded on the unit torus for the finitely many allowed row sets. This is an algebraic factorization, not division by a numerical gap. It continues to hold when labels coincide.

The exterior matrix consists of these minors. Its operator norm is bounded above by its Frobenius norm and below by any entry. For the lower bound, choose columns maximizing $V_\ell$ and consecutive rows $0,\ldots,\ell-1$, available because $L\ge q-1$. This minor is the ordinary Vandermonde in the corresponding $z$ values. The chord estimate

$$
2\sin(1/2)|x-y|\le |e^{\mathrm ix}-e^{\mathrm iy}|\le |x-y|
$$

then gives the printed lower constant. The singular-value decomposition identifies the exterior operator norm with $\prod_{j\le\ell}\sigma_j$. Repeated labels have exactly the stated rank effect because exponentiation is injective on this arc. Thus both comparison sides vanish at the same unavailable cardinalities.

The constants must not be read as uniform in increasing $L$. Already for one column, $V_1=1$ but $\sigma_1=\sqrt{L+1}$. The author explicitly allows $C_{q,L}$ and does not claim the sharper growing-bandwidth content of the cited spectral literature. I therefore do not raise that nonexistent stronger claim as a counterexample. The proposition is an elementary but useful comparison of scales, accurately described as such.

### 3.2 Acquired spectral envelope and its logical dependence

**Location:** `cor:v35-spectral-envelope`. [S2]

The substitution

$$
\Psi_{n,m}(M,a)\asymp
\max_{1\le\ell\le p_{n,m}}
\left(\frac{\prod_{j=1}^{\ell}\sigma_{m,j}(a)}{M}\right)^{2/\ell}
$$

follows immediately and correctly from the proposition, since only finitely many indices are involved. Exact zero products are retained; no positive lower bound on a nonzero gap is introduced.

Its statistical interpretation is not supplied by the matrix proposition. The cutoff $p_{n,m}=\min\{n(r-1),q_m\}$, actual acquired mass and common causal implementation remain conclusions of the preceding experimental theorem. The auxiliary Fourier matrix is a function of known exponent labels, not an observation or an extra memory resource. There is no circularity: the geometric theorem was proved using the attainable chart and cover before the spectral reformulation is invoked.

The distinction also fixes the novelty claim. The corollary makes the result comparable to established spectral language; it is not a new independent derivation of the risk law from singular values alone. The current text acknowledges this dependence.

### 3.3 Fixed future spectrum, different acquisition lengths

**Location:** `cor:v35-fixed-future`. [S2]

In the two-parameter detector example, the six separated future groups and three possible within-group gaps give volumes of orders $1$ through index six, followed by $\rho,\rho^2,\rho^2\tau$. Successive ratios of positive spectral products therefore give

$$
(\sigma_{2,1},\ldots,\sigma_{2,9})
\asymp(1,1,1,1,1,1,\rho,\rho,\tau).
$$

At $\tau=0<\rho$ the final singular value vanishes, and at $\rho=0$ the last three vanish. Using the rank clause there, rather than dividing zero by zero, is correct.

The acquired cutoffs for $n=1,2,3$ are three, six and nine. Substitution gives the stated $M^{-2/3}$, $M^{-1/3}$ and three-term checkpoint envelopes. The total horizons are explicitly $n+2$. Consequently this is a comparison between three experiments with the same future test menu, not a concealed claim about three checkpoints sharing the same remaining horizon in one physical run.

The example usefully demonstrates why the future spectrum alone does not determine the acquired law. Its proof is a consequence of the existing classification, not a new optimization theorem. One small normalization clarification would make “the same spectrum” literally unambiguous: choose the same admissible $H$ once for all three horizons; Section 7 gives a concrete choice.

### 3.4 Smooth flat paths and crossover orders

**Location:** `rem:v35-flat-path`. [S2]

For the displayed flat path, $\rho\asymp e^{-1/\theta^2}$ and $\tau=e^{-1/\theta^4}$ for sufficiently small positive $\theta$. Balancing the first and second terms of the two-parameter envelope yields $M\asymp\rho^{-6}$. Balancing the second and third gives $M\asymp\rho^2\tau^{-8}$. Hence the two exponential orders in the remark are correct and separated.

These are crossover orders for the comparison envelope, not exact integer thresholds of the unknown finite-budget optimum. The finite-power collision-tree corollary does not apply to this path, whereas the pointwise determinant classification does. This distinction is now explicit. It is a useful boundary illustration, not a new hypothesis or a strengthening that must be added to the main theorem.

## 4. The closer literature comparison

### 4.1 Full clustered spectra

I checked Theorems 2.2–2.3 of Batenkov–Diederichs–Goldman–Yomdin in the cited version. The multicluster statement compares the complete spectrum with the ordered union of cluster spectra, with square-root multiplicative bounds controlled by reciprocal bandwidth–separation and bandwidth–diameter terms. The single-cluster statement gives all scales $L^{1/2}(Lh)^{j-1}$ in its separated-within-cluster, small-$Lh$ regime. V35 respects these restrictions and does not misdescribe the work as solely a least-singular-value result. [L1]

The relevant distinction is therefore not that A1 alone notices multiple spectral scales. It is that the manuscript converts those fixed-size comparison scales into prediction losses on an experimentally attained family, with an acquisition-dependent cutoff and a common retained-label process. The exterior proposition makes the shared algebra explicit while disclaiming a new uniform growing-bandwidth estimate. This is the comparison R34.1 requested, rather than merely an added citation.

### 4.2 Superresolution minimax bounds

Definition 3.13 and Theorem 3.14 of Batenkov–Demanet–Goldman–Yomdin concern unknown-support complex-amplitude grid measures, noisy Fourier data over a frequency interval, and coefficient $\ell^2$ recovery error. Their clustering-dependent minimax scale has separate upper and lower quantifiers: the upper assertion selects arbitrarily large fixed superresolution factors before taking sufficiently small grid spacing; the lower assertion uses specified cluster parameters and a stated sufficiently-large-factor range. V35 preserves that distinction and does not assert the theorem for every bandwidth and configuration. [L2]

A1's loss is instead squared prediction excess relative to the full-history predictor under the same prescribed stochastic experiment. Its $M$ counts retained labels; neither bandwidth nor inverse external noise is interchangeable with $M$. This does not make the cited minimax theory irrelevant—it explains the common degenerating exponential system—but it prevents a formal substitution from proving A1. The manuscript now acknowledges both the spectral and the statistical content of the antecedent.

These comparisons substantiate a distinction, not an exhaustive priority claim. I have not established an earlier theorem identical to the attained collision law. Equally, a targeted search cannot certify that no such theorem exists anywhere. That limitation belongs to this review's evidence, not to a demand that the author prove a universal negative.

## 5. Re-examination of the publication-bearing proof chain

### 5.1 Attainment rather than an assumed posterior rectangle

The positive detector's failure family contains an interior neighborhood of the constant one half. At a common feasible binomial tuple, the polynomials $P/(1+c_i z)$ form a basis through degree $n-1$. Their associated product tangent has exactly $n(r-1)+1$ distinct monomials. Strict mixed-moment positivity pairs this tangent with the future tests for any fixed full-support prior. The product itself lies in the tangent, so normalization removes exactly one direction. This establishes the acquired rank rather than merely counting the ambient future test space. [S6]

The lower-dimensional continuous-encoding conclusion uses a local section and invariance of domain. The upper construction retains normalized chronological factors until the future-moment representation is smaller, then changes representation once. It does not require a false global embedding theorem for an arbitrary curved variety. These elementary details matter to the claimed generality.

### 5.2 Confluent flags and probability

The Newton/Leja construction retains repeated formal labels, with a uniformly conditioned leading nonzero triangular block and zero pivots handled explicitly. The initial divided differences span complete confluent test systems. Their continuity at the endpoint $t=0$ follows from positive exponents bounded away from zero and the boundedness of the accompanying logarithmic factors. Pairing against the actual tangent and taking finitely many orderings over a compact chamber gives uniform differential bounds. [S7]

At an exact collision the auxiliary confluent differential may have more independent directions than the physical future law. This is not a contradiction: zero Newton scales annihilate the extra directions when returning to raw tests. Only positive initial scale products enter the lower bound.

The inverse-function step includes kernel coordinates and the probability of the all-failure word. It produces a subprobability minorization under the actual command-and-report law. A singular latent prior causes no difficulty here: the local absolutely continuous variables are acquisition commands. The fixed-prior qualification remains essential; no uniform constant over all full-support priors has been proved or claimed.

### 5.3 Whole-image covering and causal compatibility

For a fixed report word, the scaled prediction coordinates are rational functions of commands with positive evidence. Their coefficients may contain arbitrary real prior moments and node values. Bounded semialgebraic format therefore applies without requiring semialgebraic dependence on calibration. The real entropy inequality and coefficient-independent section bounds justify the thin-rectangle estimate; the primary texts support the particular inputs used. [S7; L3, L4]

The section-integral argument explains why products stop at attained dimension rather than ambient dimension. The integer-budget proof separately treats small $M$, replaces centers by reachable representatives, and includes zero-width directions. Thus a local chart is not being used as an unjustified cover of the whole experiment.

The final causal step is indispensable. A representative is updated in raw moments by a Bayes ratio whose denominator is bounded below on posterior mixtures. The update is uniformly Lipschitz without inverse exponent gaps and maps a reachable representative to a reachable next state. Quantization after each update gives a finite-horizon error recurrence for one $M$-label process. Every such process is also a checkpoint encoder, and the lower laws are prefixes of one common exploration law. [S8]

No discarded history, persistent decoder-indexing seed, or collection of separately optimal encoders is smuggled into that construction. Its constants may depend on the fixed horizon; it is not an infinite-horizon stability or finite-precision arithmetic theorem. I find no reason in the examined chain to retract the favorable mathematical assessment of the main law.

### 5.4 Controller algebra and certificate layer

The finite-cell realization formula remains a compact nonconvex representation, not an optimizer classification. Its one-step body is the exact Blackwell postprocessing region, with a shared failure kernel. Occupancy propagation and conditional independence given the full history justify the centroid formula. The bounds $0\le b^2/w\le w$ and $0\le\mu(LH)^2/\mu(L)\le\mu(L)$ handle zero occupancy and zero evidence. [S3]

Atomless-command purification preserves the entire mean-risk vector, not every history's risk or a persistent public seed. Polyhedral rules are proved for scalarized means, not by an unproved minimax exchange. The fixed-$M$ collision continuity statement does not acquire all-budget content merely from compactness. These boundaries remain visible.

V35 shortens only the repeated identification and overlap calculations in this portion. The earlier proposition supplies the complete identification and common-submeasure proof; the following lemma still proves compactness and maximizes the support functional. The dependency is forward and noncircular. This is legitimate proof integration, not suppression of a missing argument.

The finite-compatibility and arbitrary-precision layer retains its earlier scope: complete-net coverage is required for its lower certificate, and chosen approximation powers are not intrinsic collision exponents. The one-checkpoint continuum example is a genuine analytically solved example, but is not promoted into a multistage tradeoff theorem. None of these secondary results is the basis of my exceptional-journal assessment. [S9]

## 6. Significance: the favorable case and its limits

The manuscript's strongest point is the identification of the attained collision profile at every label budget, not the number of named statements in the submission. A dimension formula at an exact collision and a generic dimension away from it would miss intermediate resolutions. A full matrix spectrum would still not provide the acquired cutoff, lower mass under the prescribed experiment, or one implementable causal process. The proof supplies those ingredients rather than assuming them. Its two-parameter and high-contact consequences show that the joint uniformity has mathematical content beyond a fixed-calibration asymptotic slope.

The scope is specialized: positive finite detectors, monomial test spaces, fixed horizon and prior, and calibration-dependent read-only programs. Within that scope, the conclusion is coherent and stronger than applying a spectral inequality to an arbitrary posterior family. I regard this as a defensible mathematical contribution at the requested level, although the journal's own judgment of breadth and priority remains independent of mine.

The v35 additions themselves should not be oversold. The exterior comparison is elementary; the fixed-future example is substitution into the inherited theorem; the flat path is a direct consequence of a path-free estimate. Their value here is precision of interpretation and comparison. They remove a substantive objection without pretending to be a new central theory.

There is still no sharp finite-budget causal price, global classification of optimal label allocations, or efficient general solver. These are boundaries of the present results, not established failures. The previous report explicitly allowed a focused case for the attained collision theorem instead. I see no mathematical justification for converting those unclaimed strengthenings into mandatory additions after the author has followed that route.

## 7. Remaining bounded clarifications

**R35.1 — Fix the normalization in the same-spectrum example.** At the start of `cor:v35-fixed-future`, state explicitly that one $H$ is chosen for all three total horizons. In the displayed calibration square, $H=16$ is admissible even for the largest horizon five. Then the nine normalized future nodes and the chosen $F_L$ are literally identical across the three acquisition problems. The proof already permits this choice; the request removes an avoidable ambiguity, not a gap in the risk comparison.

**R35.2 — State the meaning of a crossover once in the new remark.** Add that the exponential crossover budgets in `rem:v35-flat-path` are orders obtained by balancing the comparison envelope, not exact optimizer transition thresholds. The inherited two-parameter corollary already says the analogous thing. Repeating it locally would prevent a reader from inferring information about optimizer partitions that the paper does not supply.

These are the only changes made conditions of my favorable recommendation. An additional explanatory sentence separating fixed-size spectral comparison from varying-bandwidth results is unnecessary: the manuscript already contains it. No deletion of historical proofs, rerun of an astronomical controller net, new theorem, new prior regularity assumption, or extra decimal precision is requested. Ordinary final copy-editing and native reference checking after any text changes remain appropriate production work, not a fresh substantive review requirement.

## 8. Execution evidence and its limits

### 8.1 Current build record and independently verified source identity

The current receipt records six successful compiler invocations for the actual main and companion entry points, convergence after three paired cycles, agreement between the declared source closure and TeX recorder inputs, and no final unresolved-reference or overfull-box entries. It reports a 42-page main article and 159-page companion. The native builder removes generated external exports, obtains labels from actual auxiliary files, and checks final logs after convergence; it does not substitute theorem markers or reference stubs. [S4]

I independently checked all **80** TeX objects in that receipt against the published commit. Specifically, overlaying the listed source paths with their receipt Git blob IDs on the controlling repository tree returned **the identical tree hash**, `86f7d70a14b464425b934e3d5e62ff8f2a84bb94`. No branch or manuscript file was changed by this identity check. This verifies that the recorded source object list matches the publication, rather than trusting a directory name or a historical receipt.

The receipt's `source_commit: null` is not a defect: the build preceded creation of the revision commit and identifies its inputs by content. The successful source mapping supplies the missing publication association without pretending an uncreated commit was compiled.

The author reports visual samples of main pages 1, 37–39 and 42, and companion pages 1, 80 and 159. The record explicitly disclaims all-page visual inspection. I read this record; I did not perform that inspection, reproduce the PDF hashes from binary files, or execute a native build myself. These distinctions close the missing-current-build-record objection without turning provenance into mathematical verification. [S5]

### 8.2 Replayed programs

Three published programs were executed in ordinary Python and with `python -O`, with byte-identical outputs between the modes. The copies are verified against these Git blobs:

| Review copy | Published Git blob | Execution result |
|---|---|---|
| `audit/inherited_finite_cell_checks.py` | `9a7e45be79d15e3efa31664908346a8f1ffd5362` | The finite-cell diagnostics reproduce, including zero evidence, zero occupancy and atomic ties. |
| `audit/inherited_core_checks.py` | `30e9371e967b3bc200b88f7b820795d23c9d3ffd` | The inherited 298 core checks reproduce. |
| `audit/author_spectral_checks.py` | `d4e973bde4896d45583038df1b83d2b4f060c58e` | 52 exact alternating factorizations, 28 high-precision exterior comparisons, 72 exact arrangement brackets and two crossover identities pass. |

The first two are deliberately unchanged regression programs, not newly authored independent tests. Their historical embedded metadata is preserved. The last program's SVD calculations are high-precision diagnostics, not directed interval proofs. Its exact polynomial and rational computations establish their finite identities, not uniformity on a calibration chamber.

### 8.3 New independent boundary checks

`audit/independent_v35_checks.py`, written for this assessment, passed **200 explicit checks** in both ordinary and optimized Python; the outputs agree byte for byte. It checks exact Cauchy–Binet identities and repeated-node ranks using rational complex points on the unit circle. Separate 160-digit SVD comparisons include the minimum allowed sampling length, exact collisions, gaps at very different scales, and nine-node detector arrangements. An independently derived conservative minor bound is used rather than merely comparing two floating-point evaluations of the same formula.

The script also verifies the three flat-path regimes in logarithmic variables with exact rational arithmetic for selected parameters, and the one-column Gram identity illustrating why a growing-$L$ uniform upper constant is impossible. It tests the leading comparison orders, not an exact optimum along the full flat path.

The code does not optimize a continuum controller, prove the uniform chart or entropy theorem, verify all singular priors, or compile the manuscript. The audit manifest records these restrictions and hashes every supplied artifact. Numerical residues at repeated nodes are treated as numerical diagnostics; exact rank in the rational tests is established algebraically. A large check count is not offered as a publication argument.

## 9. Source ledger

Unless otherwise stated, the native paths below are relative to `papers/A1-english-v35-spectrum-native/` at commit `02a19f2ddb83cf68bfbf8361c137613e2ffd3925`. Stable source labels control theorem references; printed numbering in the response is the author's build numbering.

**[S0]** Revision metadata and parent: current commit and repository tree in the header; preceding report `reviews/a1-english-v34-harsh-independent-2026-09-08/REFEREE_REPORT.md` at `a177077ede2b64e11af1efb016eaa6bb5ddf2a13`. Consulted for its bounded requests, not treated as proof of correctness.

**[S1]** `RESPONSE_TO_REFEREE_V35.md`, blob `149cad18a46d02b241045e647c307261dc64f62b`; `main.tex`, blob `5969aab254b9743fa4d0a512650a15e42c3c534c`; `v35/introduction.tex`, blob `2ca59260fb5b6a615000e1bf5ffe88dab260469c`; `v35/comparison.tex`, blob `6ce1c82613854d201acebde042ac461ace54f9c4`.

**[S2]** `v35/spectral_comparison.tex`, blob `2a3f9081e8a14ccc75c978695c66b619a5b0bcff`; `v35/verify_revision.py`, blob `d4e973bde4896d45583038df1b83d2b4f060c58e`.

**[S3]** `v35/moment_controllers.tex`, blob `6c6dd32df4c30a3074870bd5b346cee9cf2c33d4`; general finite-cell formulation and integrated proofs, with the inherited v34 argument used in its versioned context.

**[S4]** `v35/build_native.py`, blob `66e5fa5a5fe7ba7c551b62bc38afb4c5951823a4`; `verification-v35/NATIVE_BUILD_V35.json`, blob `1e5f92cf41b563779ad702c85ee440a470a689fe`. Entire receipt and builder read; source-list identity independently checked, native compilation not independently executed.

**[S5]** `verification-v35/VISUAL_INSPECTION.json`, blob `00ae52d0b918da6dea5f6a25cfef5574e5df879f`. Author's sampled inspection record, not a referee PDF inspection.

**[S6]** `core/02_experiments.tex`, blob `1bd4f6273d62c860f8a348dcc4f72734dbc388db`; `core/03_transversality.tex`, blob `6395724ba2c4bed3ead19178a1cfe8206f9a3824`; `text/exact_information.tex`, blob `4d105ba3bd2c9900029530a22438dab288700665`.

**[S7]** `text/analytic_inputs.tex`, blob `92c431918df8894dbab4e2bef267a1b3d086370c`; `text/collision_flags.tex`, blob `558972ba3ad6f42ca1f782b80fed4b7ef9a87fe8`.

**[S8]** `text/main_classification.tex`, blob `307a694dacddee85104212dfa51a222053ee1769`; `text/collision_direct.tex`, blob `12db8bce89cd0a731cb3bc5c383c3c70699ced60`; `text/collision_consequences.tex`, blob `27c4bef2c95c87dc4d91e3d6842d2b5b3b79031c`; `risk_criteria.tex`, blob `da5403fdde6bed138d33b252d52d75e4255c8528`; `text/operational_model.tex`, blob `62b00087d3000d1a6303b7f65479047172a851e2`.

**[S9]** `v33/finite_compatibility.tex`, blob `6254d766c1469292dbc1125a1eea3fd42de571de`; `v33/precision.tex`, blob `f54e913c2e7e0e0f4db2a5572ded6b53ec431479`; `v33/exact_instance.tex`, blob `8c79906419c9974425fcd0c65d7c6a18eb5dd4a0`. Unchanged inherited proofs; they are not newly proved by v35 diagnostics.

### Primary literature inspected

**[L1]** D. Batenkov, B. Diederichs, G. Goldman and Y. Yomdin, *The spectral properties of Vandermonde matrices with clustered nodes*, arXiv:1909.01927v2, Theorems 2.2–2.3, printed p. 6. The primary PDF text and this theorem page were inspected. The source supports the specific full-spectrum comparison, not a claim of prior publication of A1's acquired risk law.

**[L2]** D. Batenkov, L. Demanet, G. Goldman and Y. Yomdin, *Conditioning of partial nonuniform Fourier matrices with clustered nodes*, arXiv:1809.00658v2, Definition 3.13 and Theorem 3.14, printed p. 10. The primary PDF text was inspected, including the separate quantifiers; the attempted screenshot did not succeed and is not claimed as a visual check.

**[L3]** G. Comte and I. Halupczok, *Motivic Vitushkin invariants*, arXiv:2206.15412, introduction, equations (4)–(5). Used only for its explicit recall of the classical real section-variation and entropy inequality. No nonarchimedean theorem is applied to the manuscript, and the cited Yomdin–Comte monograph was not independently reconstructed in this review.

**[L4]** Y. Zhang and J. Kileel, *Covering Number of Real Algebraic Varieties and Beyond: Improved Bounds and Applications*, arXiv:2311.05116, Lemma 2.18 and its appendix proof. Used for bounded-format semialgebraic section regularity; not as a source of A1's anisotropic acquired probability law. Parsed primary text was inspected; unsuccessful PDF screenshot attempts are not represented as visual verification.

## 10. Final disposition

The original major objections have been answered at the level requested. The new comparison propositions withstand the examined boundary cases, the inherited collision proof remains coherent, and current build provenance is associated with the actual published sources. The residual requests concern explicit common normalization and the interpretation of crossover orders.

I therefore recommend **minor revision with a favorable publication assessment for the main article**, not another major-revision cycle. The recommendation remains an independent referee judgment, not a guarantee of acceptance or an exhaustive certificate of correctness and priority. A future assessment that finds a concrete overlooked gap should of course address it. On the evidence established here, however, manufacturing a new mandatory research agenda would not be a rigorous response to this revision.
