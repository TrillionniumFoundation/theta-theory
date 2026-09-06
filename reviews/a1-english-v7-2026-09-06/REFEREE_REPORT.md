# Referee report — A1, English revision 7

**Manuscript:** *Sparse observation algebras, confluent directions, and finite-state memory*  
**Author named in the submission:** Qian Qi  
**Review date:** 6 September 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Journal of the American Mathematical Society / Acta Mathematica  
**Recommendation:** **REJECT at the requested four-journal level in its present form.**

This is an owner-requested, AI-assisted external referee-style assessment, not a review commissioned by any named journal. “Independent” below means fresh examination and a separately written diagnostic program, not an independent human appointment or formal proof verification. The recommendation concerns this submission, not the viability of the research program.

## 1. Submission identity and actual audit scope

```
repository:       TrillionniumFoundation/theta-theory
revision branch:  revision/a1-english-v7-confluent-resolution-2026-09-06
submission SHA:   02f68484cf92ef312037cf455bd3f3737ae4facd
repository tree:  90701f87967557adac0abb798c8040df08040472
principal path:   papers/A1-english-v7/
principal tree:   2a499f613db54f9966d553ddb727562fe71a537d
previous review:  414f8c43a6236586362c1532c00aa9b9da01fe64
```

The controlling predecessor is the [v6 referee report](https://github.com/TrillionniumFoundation/theta-theory/blob/414f8c43a6236586362c1532c00aa9b9da01fe64/reviews/a1-english-v6-2026-09-06/REFEREE_REPORT.md), not an easier earlier review. The source/build input of the final publication job is `fcc628087b8a9abde4767e25ce4a76a1f1b31ef3`; the submission head above adds the resulting PDF and receipts. I reviewed the head's manuscript, not merely the author's response letter or a branch name.

I read the main TeX, all ten sections, bibliography, response, proof ledger, historical map, manifest and diagnostic script, together with the relevant preceding review and technical note. The authenticated Actions artifact supplied the complete source bytes. All **23 manifest entries** matched their recorded byte lengths, Git blob hashes and SHA-256 hashes. All **25 principal result labels**, as well as the two operational definitions, are covered in [CLAIM_AUDIT.md](CLAIM_AUDIT.md).

The author's script was freshly run in a separate copy: **97/97 finite checks**. A new script importing no author code passed **60/60 check families**, including **3,072 exact rational shrinking updates**, higher-multiplicity confluent pairings and **128 floating-point rectangular-allocation cases**. These numbers measure executions, not proofs. The independent script and receipt are [referee_checks.py](referee_checks.py) and [INDEPENDENT_DIAGNOSTICS.json](INDEPENDENT_DIAGNOSTICS.json).

The principal source was freshly compiled in three passes with shell escape disabled. The resulting **28 pages** were rendered and inspected in contact sheets, with pages 12 and 20 additionally enlarged. The final log has no undefined references, undefined citations or overfull boxes; two underfull-box notices remain. The submitted CI PDF's hash was also checked. [EXECUTION_REPORT.json](EXECUTION_REPORT.json) records the environment and provenance. This is not a fresh audit or compilation of the complete legacy companion, every historical branch, or all eleven planned papers. Their retention does not imply their approval.

All source paths and line ranges below refer to the immutable submission SHA above. Theorem numbers refer to the newly compiled principal PDF; labels are the controlling identifiers.

## 2. Executive judgment

**V7 genuinely answers the central finite-resolution objection to v6. It also gives the new sparse direction a value in one common sequential decision task. Neither achievement may honestly be described as absent.** The revision is not merely a change of terminology, an additional numerical example, or the previous exact-rank argument repeated without quantitative content.

I found **no blocking counterexample or unfilled essential proof step in the principal theorems under their printed restrictions**. In particular, the confluent pairing at zero is proved directly; the physical query metric is not confused with the desingularized coordinate metric; the lower bound retains the acquired history's probability; and the streaming update does not divide by the collision parameter. The common-payoff comparison uses one actual experiment and one baseline. These are substantial positive findings.

My negative publication recommendation is therefore **an editorial assessment of demonstrated mathematical significance**, not a claim that a displayed main formula is false. The strongest new general result is a full-future, affine-collision checkpoint theorem. Its genuinely sequential uniform realization is proved for a particular five-trial, one-weak-direction family. The decision result gives that same geometry an exact scoring interpretation and a specific information-erasure comparison. This is a coherent and useful synthesis. I am not persuaded that its present structural reach and consequences establish the exceptional contribution sought at the requested general-mathematics level.

The distinction matters. The author has now done what the preceding report identified as a meaningful quantitative development. It would be unfair to keep rejecting the paper on the ground that this development has not occurred. It is nevertheless necessary to evaluate the resulting theorem itself. My residual concerns concern its relation to closely adjacent mathematics, what its hypotheses exclude in the same model, and the extent to which the decision section adds a separate advance rather than a rigorous corollary. These concerns are made precise below. I have not found an earlier theorem identical to the main attainable-pairing result, and I do not assert one.

## 3. Disposition of the v6 requirements

| Previous item | V7 disposition | Present conclusion |
|---|---|---|
| E1: establish the significance of the central contribution | Adds a class-wide confluent checkpoint theorem and a uniform streaming crossover | Material improvement. The remaining significance judgment must concern these new results, not v6's missing quantitative theorem. |
| E2: exact rank does not determine resolved directions | Theorems 5.1 and 7.1 identify the scales and prove matching two-parameter bounds | **Closed for the stated full-future checkpoint class and five-trial streaming family.** The degeneration of the five-dimensional lower constant is now determined in order. |
| E3: give the sparse direction value in one evolving common-payoff problem | Section 8 uses the same exploration, query and future event, with a binary ticket decision and a precise erased statistic | **Closed for this prescribed acquisition-and-decision experiment.** It is not an optimal-exploration theorem, and does not claim to be. |
| P1: published sumset reference | Published Eliahou–Mazumdar bibliographic data supplied | Corrected. |
| P2: meaning of “constructive” | Heading revised; existential real-program convention repeated at the upper theorem | Corrected. |
| P3: measurability | Borel maps, kernels and quantizer conventions stated | Corrected. |
| P4: history encoding versus quotient chart | Distinction maintained | Closed; do not remove this distinction. |
| P5: diagnostics versus proof | Finite fixtures and inherited regressions are explicitly delimited | Properly handled. Fresh review executions are distinguished from author and inherited receipts. |

The v5 objections already closed by v6 remain closed. In particular, the sparse theorem is not confined to a saturated polynomial space, and the filter is not secretly a checkpoint encoder that rereads an exact prefix.

## 4. Mathematical audit of the new central theorem

### 4.1 The attainable geometry remains the essential input

**Sources:** `sections/02_experiments.tex:25–109`; `sections/03_transversality.tex:5–202`; labels `lem:interior`, `lem:binomial-tangent`, `thm:rank`, `thm:causal`.

The calibration map has a fixed linear right inverse. Thus the binomial witness is realized by interior commands of one actual apparatus, not by parameter-dependent commands. Complementary products of the factors `1+c_i t^D` form a polynomial basis in `t^D`. The differential image is exactly the monomial space with exponent set

\[
B_{A,n}=\{jD:0\le j\le n\}\cup\bigcup_{0<a<D,\ a\in A}\{a+jD:0\le j<n\}.
\]

The strings are disjoint, giving `n(r−1)+1` dimensions. Strict mixed-moment positivity applies to this attainable tangent and the future tests for every full-support prior. After including the constant test, the normalized derivative is

\[
Z^{-1}\{LQ-p\,e_0(LQ)\}.
\]

Because `p` belongs to the image and `e_0p=1`, normalization loses exactly one rank. This is a valid reason for the formula, unlike subtracting one from an unrelated ambient dimension. Genericity, the projected local section and the invariance-of-domain lower bound follow as stated.

The global upper representation is an encoding of histories, not an asserted global chart of the operational quotient. Chronological normalized factors can retain redundant factorization information. The one-way switch to shrinking future moments is valid, and the required indices remain in the previous future sumset. I found no new defect in these inherited arguments.

### 4.2 The singular limit is not justified by a false continuity-of-rank argument

**Source:** `sections/05_confluence.tex:8–66,112–156`; labels `lem:confluent-positive`, equations `divided-tests`, `jet-tests`.

The formal pair construction correctly separates permanent additive identities from collisions occurring only at zero. The zero-exponent cluster contains only the constant function. Every logarithmic jet of positive order therefore has a positive base exponent, so the functions and the required calibration derivatives are bounded at `t=0`.

The exponential-polynomial zero-count argument is adequate: divide by the first exponential and differentiate according to its multiplicity. The operators on the remaining polynomial coefficients are invertible because the exponent differences are nonzero. The Wronskian/confluence argument fixes the evaluation determinant's positive sign. Determinant integration then gives strict mixed pairing for every full-support prior, including priors with atoms or without densities.

This proves rank at the singular parameter itself. Continuity is used only afterward, to obtain uniform bounds from already-established surjectivity on a compact parameter interval. That order of argument is correct and is the important repair relative to an unjustified singular limiting argument.

### 4.3 The physical metric really has the claimed scales

**Source:** `sections/05_confluence.tex:157–212`; label `lem:observable-scales`.

Newton interpolation at the exponent nodes gives a fixed triangular matrix followed by the diagonal factors `theta^k`. The expansion of actual product probes in formal pair monomials has full column rank: invert the one-step basis change, multiply, and then identify equal pairs. This quotient does not destroy the spanning assertion.

After deleting the constant coordinate, the result is

\[
p_\theta(h)-p_\theta(\widetilde h)
   =G\operatorname{diag}(\theta^{\nu_i})
           [z_\theta(h)-z_\theta(\widetilde h)],
\]

with **fixed**, full-column-rank `G`. Consequently the comparison constants come from a fixed matrix rather than a singular change of basis. At zero, the vanishing diagonal entries remove the unresolved jets. The analytic jet coordinate is not presented as a new measurement delivered to the filter. I found no missing power, factorial or hidden inverse power of `theta` in this step.

### 4.4 The uniform distributional patch retains the evidence

**Source:** `sections/05_confluence.tex:214–280`; label `lem:uniform-patch`.

The full-future inequality `K_m−1 <= n(r−1)` is used exactly where it should be: it makes the desingularized map onto all nonconstant future coordinates. The common binomial command tuple has this rank throughout the compact parameter interval. The least row singular value thus has a positive minimum.

The use of possibly discontinuous orthonormal frames is harmless: only their orthogonality and uniform estimates enter the local inverse construction. Bounded second derivatives and a common interior radius permit a uniform contraction/implicit-inverse argument. A uniform forward derivative bound supplies the lower inverse-Jacobian bound needed in the change of variables.

Finally, the joint density of commands and the all-failure word includes `mu(product F_i) >= eta^n`. Integrating complementary coordinates yields a subprobability minorization on a translated cube. This is not a fictitious uniform distribution on a tangent space, and not a lower bound conditional on a rare word with its probability discarded. The argument does not need a density for the prior: the density used here belongs to the independently randomized commands.

### 4.5 Quantization and normalization of the criterion

**Source:** `sections/05_confluence.tex:283–352`; labels `lem:rectangle`, `thm:confluent-law`.

The integer grid construction respects the actual budget, including `M=1`. The lower bound projects onto each initial group of axes and uses the volume of a union of `M` balls. It allows centers outside the box. Projection onto the physical affine query space followed by inversion of fixed `G` is also legitimate.

Decoder randomization can be averaged under squared loss, leaving at most `M` centers. Encoder randomization cannot beat the closest center for a fixed history. Independent public randomness may be fixed and averaged; it is not a retained command-generation seed. At zero, omitting zero-length sides gives the right limiting exponent. These steps prove the printed two-sided order, not a leading distortion constant.

The theorem is explicitly a **checkpoint** theorem. The lower bound applies to streaming encoders, but the checkpoint upper bound does not automatically give a streaming upper bound. The manuscript acknowledges this distinction; the next section of this report examines its separate sequential proof.

## 5. Streaming and the common decision task

### 5.1 The five-trial filter is genuinely uniform and online

**Source:** `sections/07_uniform_resolution.tex:7–241`; labels `thm:uniform-streaming`, `lem:five-patch`.

The apparatus has a fixed positivity margin, the command and query labels are common across calibrations, and the exploration law does not change with `theta`. At the common three-command tuple, the limiting product tangent contains all polynomials through degree six. Its pairing with

\[
1,t,t^2,t^2\log t,t^3,t^4
\]

has rank six. Normalization leaves five, even at zero in the analytically continued coordinates. The displayed rational minor is correct. That one minor is a diagnostic, not the justification for the all-prior conclusion.

The sequential construction uses two and four normalized-factor coordinates before the peak, the five **physical** coordinates at time three, and two moments afterward. The weak coordinate is `M_(2+theta)−M_2`, of width at most `theta`; it is not divided by `theta` inside the implemented state. For a new factor `f=a+bt+ct^(2+theta)`, the shrinking update is

\[
Z_f=a+bw_1+c(w_2+w_5),\qquad
M'_1=\frac{aw_1+bw_2+cw_3}{Z_f},\qquad
M'_{2+\theta}=\frac{a(w_2+w_5)+bw_3+cw_4}{Z_f}.
\]

The denominator is uniformly positive along mixtures of reachable posteriors. The earlier factor-to-moment changeover also has a uniform derivative bound. Therefore the recurrence accumulates all previous quantization errors without a singular amplification factor. Choosing reachable representatives ensures that every next update remains in the quantizer's domain.

This supports

\[
\mathcal R_{M,5}^{\theta}\asymp
\max\{M^{-1/2},\theta^{2/5}M^{-2/5}\}
\]

with constants independent of `theta` and `M` in the stated ranges. The lower bound is in the same prescribed acquisition experiment, not in a different least-favorable input experiment selected after the code. The bit law and the order of `c_opt(theta)` follow by the stated algebra. I found no obstruction at `theta=0`, no uncharged exact-prefix tape, and no omitted repeated-update error.

The construction remains existential in its read-only real transition functions. It is not effective finite-precision synthesis, a bound on temporary arithmetic storage, or a uniform-in-horizon theorem. These are openly declared resource conventions, not concealed contradictions.

### 5.2 The decision comparison is valid, but is a transfer of the same geometry

**Source:** `sections/08_sequential_value.tex:8–171`; labels `prop:ticket-identity`, `thm:resolved-value`.

For the independently priced ticket, the integrated optimum conditional on a success probability `p` is `p^2/2`. Conditional expectation therefore makes the optimal value gap exactly one half of the prediction regret for the same streaming encoder. The identity is correct for randomized encoders and terminal actions under the stated independence conditions.

More importantly, the erased statistic is precisely specified. The comparison is with uncompressed access to the first four physical moments, in the **same calibration, exploration law, query, target and payoff**. It is not a comparison of regrets normalized by different Bayes baselines.

Writing `Z=(M_(2+theta)−M_2)/theta`, the exact gap is

\[
V_*^\theta-V_T^\theta
 =b_*\theta^2\,\mathbb E\operatorname{Var}(Z\mid T_\theta),
\qquad b_* = \frac{169}{7962624}>0.
\]

The minorized five-dimensional cube bounds the residual variance below after conditioning on its first four coordinates. This remains valid when the full distribution outside the cube is singular. Uniform boundedness gives the upper bound. The streaming theorem then yields the positive advantage when `M >= K theta^(−4)`.

The result closes the preceding review's request for a value comparison tied to the newly resolved sparse direction. Nevertheless, its prediction-to-decision exponent is an exact change of scoring rule, not an independent solution of an acquisition-control problem. Its erased statistic is one specified history map, not a theorem about every four-real-coordinate encoder or every one-step sensor erasure. The author states these limitations correctly. They affect the depth and scope of the contribution, not the correctness of the proof.

There is a useful additional consequence: the state-budget order for beating the **uncompressed** erased statistic is necessary as well as sufficient. The existing lower value-loss bound and upper erasure-gap bound imply `V_M−V_T <= C_e theta^2−c_s M^(−1/2)`. Thus sufficiently small constant multiples of `theta^(−4)` cannot beat that comparator. The complete argument, with its comparator restriction, appears in [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md). This is a corollary of v7, not an erratum or an additional theorem the author must discover from scratch.

### 5.3 Inherited control and mechanical conclusions

**Sources:** `sections/06_streaming.tex:219–287`; `sections/09_common_risk.tex:7–243`.

The additive-control estimate is a separate upper bound. State-Lipschitz action values, compact actions and Bellman telescoping suffice; no derivative of an optimizing action is required. It is not a matching lower bound for arbitrary decision objectives.

The mechanical short-time calculation counts every ambient insertion and uses the collision-tube Jacobian with the correct preparation normalization. The raw/erased finite-state comparison has one common total-risk baseline. Conditional means give the partition formula, and the finite-partition continuity argument gives the small-amplitude threshold. These remain sound on the present audit. They are a separate finite-alphabet application, not a further proof of the new singular streaming law.

## 6. Remaining publication objections

### E1. The nearest spectral/confluent comparison needs to be made explicitly

The bibliography acknowledges divided differences, positivity and quantization. That is appropriate but does not complete the positioning of the new collision-scale claim.

A particularly close comparison is Batenkov–Diederichs–Goldman–Yomdin, *The spectral properties of Vandermonde matrices with clustered nodes*, arXiv:1909.01927v2. Theorems 2.2–2.3 and Corollary 2.1 describe cluster-multiplicity spectral scales; the single-cluster powers are `(Nh)^(j−1)` after the common normalization. Section 3 uses divided-difference and limiting bases. Their setting is Fourier/Vandermonde sampling on the unit circle, not this attainable posterior experiment. Their results do **not** supply the all-prior minorization or the causal filter here. Nevertheless, the manuscript should explain its precise additional statement relative to this closer comparison, rather than positioning its spectral hierarchy only against general classical tools. [Primary paper](https://arxiv.org/pdf/1909.01927), printed pages 6–7.

For the divided-difference integral itself, de Boor's Genocchi–Hermite formula is an exact classical reference: *Divided differences*, Surveys in Approximation Theory 1 (2005), 46–69, equation (52), printed page 64. [Primary paper](https://arxiv.org/pdf/math/0502036). The present manuscript already attributes this ingredient correctly.

These are targeted comparisons, not an exhaustive priority search. I make no allegation that the entire attainable or streaming theorem is already proved elsewhere. The requested revision is a theorem-level comparison of assumptions, outputs and genuinely additional steps. Merely adding another citation without making that comparison would leave the significance issue unchanged.

### E2. The general checkpoint classification and the sequential theorem do not yet form a general singular memory theory

The hypothesis `K_m−1 <= n(r−1)` is structural, not a dispensable technical inequality. It supplies a full-dimensional cube in the desingularized future coordinates. When the past cannot attain that dimension, cluster multiplicities of the **ambient future space** no longer determine the entropy of the **attainable image** by the same proof.

This issue occurs in the paper's own family without changing the detector. At total horizon seven, the exact profiles are

\[
(0,2,4,6,6,4,2,0)\quad(\theta=0),\qquad
(0,2,4,6,8,5,2,0)\quad(0<\theta\le1/2).
\]

At the positive-calibration peak, `n=4,m=3`, the future dimension is nine but the attainable dimension is eight. Theorem 5.1 does not apply. Its ambient orders would be six zeros and three ones; naively extending its lower formula would give an eventual `M^(−2/9)` rate, contradicting the actual fixed-calibration eight-dimensional `M^(−1/4)` upper bound. [TECHNICAL_NOTE.md](TECHNICAL_NOTE.md) gives the exact sumset calculation and contradiction.

**This is not a counterexample to v7:** the paper states the full-future restriction and does not make the naive extension. It explains why I do not read the five-trial construction as establishing a general sequential classification from collision multiplicities. The delicate remaining object is the attainable filtered geometry and its compatibility with successive updates, rather than the ambient scale list alone.

A general compatibility result, a substantial past-limited consequence, or an application in which the existing full-future theorem already resolves a significant independently motivated question would strengthen the case. These are alternative ways of demonstrating significance, not a demand to prove all extensions or a newly imposed condition for the correctness of the printed theorem. An isolated seven-trial addendum would not automatically establish a general result either.

### E3. The decision section must not be counted as a second independent source of depth

The new same-task comparison is worthwhile, and I have closed the preceding objection. But the ticket identity transforms the quadratic prediction problem exactly, while the erasure lower bound uses the very same minorized cube and one discarded coordinate. The resulting decision result is best understood as a sharp operational consequence of the geometry, not a second major structural theory.

The already-cited approximate-information-state literature also supplies a broad context for recursive approximations and policy-loss transfer; the primary JMLR record for Subramanian–Sinha–Seraj–Mahajan states that framework explicitly. [Primary record](https://jmlr.org/papers/v23/20-1165.html), JMLR 23(12) (2022), 1–83. This does not supply the sparse rank or the present lower bound. The editorial question is what additional mathematical problem the new geometry resolves, not whether policy-loss transfer exists in general.

The author need not abandon the prescribed task or pretend to solve arbitrary optimal exploration. It should instead give a compelling account of why the current attainable-singularity theorem and its present consequences warrant the claimed general-mathematics significance. Multiplying theorem labels, test counts or archival pages does not answer that question. Nor does the present review's negative judgment amount to a proof that no such account can be made.

## 7. Specific corrections and presentation requests

**P1 — State the nontrivial domain of the confluent formula.** Section 5 introduces a “fixed future length m” without an explicit positive-integer restriction, whereas Theorem 1.1 previously allows zero horizons. For `m=0`, its list of orders is empty and the displayed `Phi_0` expression divides by `|0A_0|−1=0`. Explicitly assume `m>=1` in Section 5, or define the trivial zero-query risk separately. Under the full-future condition this then also forces `n>=1`. This is a minor statement-domain correction, not a failure of the positive-horizon proof.

**P2 — Separate rate-sharpness from a threshold location.** The manuscript already calls the crossover an order statement. Keep that qualification. The complementary necessary-budget corollary in the technical note sharpens the interpretation of Theorem 8.2 without yielding an exact integer threshold or a leading constant. It applies to beating `V_T`, not automatically to comparing two optimally compressed `M`-state experiments.

**P3 — Present the hierarchy of contributions without double counting.** State clearly which result is the class-wide geometric theorem, which is the special uniformly causal realization, and which is the exact decision-theoretic transfer. The current proof order is serviceable; this request concerns the significance argument, not removal of proofs. Keep the complete historical record, but do not make inherited mechanical breadth substitute for the new paper's central contribution.

**P4 — Keep reproducibility claims at their actual scope.** The author suite already includes higher-multiplicity checks and actual index-only finite-input fixtures. It would be inaccurate to criticize it for their absence. Neither those fixtures nor this review's exact updates verify the continuous-command asymptotic lower bound, arbitrary-prior assertions, global representative selection or top-journal significance. Those depend on the written mathematics and editorial assessment.

No substantive typesetting correction emerged from the fresh build. The two underfull notices are not a mathematical objection. I do not recommend deleting valid content merely to make the manuscript appear more selective.

## 8. Final recommendation

**Reject this version at the requested four-journal level.** This is not rejection for a false main formula, missing history evidence, singular online amplification or mismatched decision baselines: those criticisms would be unsupported by the current manuscript.

V7 is materially stronger than v6. Its central positive contribution is the combination of an attainable confluent pairing, a physically weighted local information geometry and a genuinely uniform finite-state realization in the five-trial family. The prior E2 and E3 requests have been answered at the stated scope. The surviving objection is that, after distinguishing the classical mechanisms and the consequences of one geometric construction, the submission has not yet made a sufficiently compelling case for exceptional general-mathematics significance.

A future review should start from these closures. It should not require the author to reprove the absence of an exact-prefix tape or to rediscover the same crossover. What would matter is a precise positioning against the nearest spectral work and a stronger demonstration of the reach or consequence of the attained geometry. No particular extension, extra example, test count or response checklist guarantees acceptance. I found no reason to declare the research direction impossible, and this audit does not certify the absence of an undiscovered error or an earlier equivalent theorem.
