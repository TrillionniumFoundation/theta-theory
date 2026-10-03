# Independent referee report on A2 v13

**Manuscript:** Qian Qi, *Nonlinear boundary laws and two-contact rigidity in dispersing billiards*.

**Date:** 10 September 2026. **Requested standard:** Annals of Mathematics / Acta Mathematica / Inventiones Mathematicae / Journal of the American Mathematical Society.

**Status:** author-requested, AI-assisted referee-style assessment. This is not a journal-commissioned report, an editorial decision, or a formal proof certificate.

## 1. Reviewed version and recommendation

The reviewed revision is `revision/a2-v13-two-flight-relative-invariants-2026-09-10`, frozen at commit **`0e54099f079232df233316ae6fe7986fc51b7ea1`**, root tree `41f68e02205e10d48e917559f0f5092c10799948`. Its manuscript directory is `papers/A2-v13-two-flight-relative-invariants`. Its parent is the completed v12 review, `2ae2751f61224b66f314915fd5fc22f6321b606f`; the v12 author revision reviewed there was `2b515c4ce6ed95f66880f1c2f6e629ff2bd83f86`.

All manuscript paths below are relative to the frozen v13 directory. TeX labels are authoritative; displayed theorem numbers follow the author's reading map, not an independently compiled cross-reference audit.

**Recommendation: major revision; I do not recommend acceptance at the requested four-journal level in the present form.**

The reason is now principally the assessment and positioning of the central forward contribution, not a failed two-contact calculation. In the principal arguments examined, I found no fatal mathematical error in the relative determinant construction, the new two-flight inverse, the stated finite-family experiment, or the complete-profile Abel acquisition and calibration argument. This is a scoped finding, not certification of every statement in the long appendix.

V13 has materially answered the previous review. It incorporates the independent-contact two-flight calculation correctly, proves the direct fixed-window consequence with two flights, and separates finite-jet geometry from the general smooth function-valued invariant. The requested comparisons with three inverse-spectral results have actually been supplied. It would be improper to repeat those requests as though the revision had ignored them.

Two issues remain. First, the newly emphasized relative forward law needs comparison with the local analytic hyperbolic normal-form mechanism, not only with Jacobi algebra and global spectral rigidity. The companion [analytic benchmark](ANALYTIC_NORMAL_FORM_BENCHMARK.md) gives an explicit endpoint-flux calculation showing why this is a substantive comparison. It does **not** show that the entire smooth theorem is already known. Second, the abstract's universal wording about finite-dimensional families is stronger than the actual observation theorem and is false when read literally; a precise counterfamily is described below.

The paper contains worthwhile mathematics. Nevertheless, correctness, extensive coverage, and a different choice of observations do not by themselves establish the exceptional conceptual or geometric advance needed for the requested venues. A focused revision should settle what the main theorem adds to the closest forward mechanism and make the abstract's quantifier match the proved theorem. More diagnostic counts or another unrelated theorem would not resolve that question.

## 2. Disposition of the v12 referee requests

| Previous request | Present disposition |
| --- | --- |
| R12-1: prove the independent-contact two-flight comparator and its physical observation consequence | **Closed.** Theorem 11.1, Corollary 11.2 and Theorem 11.3 include the action, twist, moment, finite-jet, coordinate-change and observation arguments. The flight number is two for every fixed jet order; offsets and conditioning may depend on that order. |
| R12-2: separate finite-jet information, short records, the long-bridge invariant and regular parametric statistics | **Substantially answered in the mathematics and presentation.** The introduction explicitly makes these distinctions. Exceptional significance remains an editorial assessment, not an unfulfilled request to repeat the distinctions. |
| R12-3: theorem-level comparison with De Simoi–Kaloshin–Leguil, Finamore–Leguil and Zelditch | **Closed as the specific requested comparison.** Section 1.5 states the differing observations, supplied information and conclusions. The new forward normal-form comparison below is a further finding of this review, not retroactive noncompliance with R12-3. |
| Earlier objections concerning discarded regularity gain, derivative observations, uncharged failures, exact-law pilot oracles, nonmeasurable fitting, or formal jets substituted for smooth uniqueness | **Remain closed in the arguments examined.** The revised source should not be criticized for defects that it explicitly repairs. |

The source credits the previous referee's two-flight derivation and the earlier acquisition improvements. I found no basis for an attribution objection to those passages. The fact that valid older proofs are retained does not make them additional independent breakthroughs, but it also is not grounds for deleting them from the repository.

## 3. Correctness audit of the mathematical chain

### 3.1 The new two-flight block survives an independent calculation

**Source:** `article/29_two_flight_benchmark.tex`, `thm:v13-two-flight`, `eq:v13-schur`, `eq:v13-action-variation`, `eq:v13-twist-variation`, and `eq:v13-two-flight-block`.

For an itinerary $b,o,b$, the stationary middle coordinate of the quadratic action is $w_0=(u+v)/(2c_o)$. The endpoint Schur complement is

$$
H_b=\frac1g\begin{pmatrix}c_b-(2c_o)^{-1}&-(2c_o)^{-1}\\-(2c_o)^{-1}&c_b-(2c_o)^{-1}\end{pmatrix}.
$$

With $z=c_0c_1-1$ and $L_b=g/(2c_bz)$, direct inversion gives

$$
\nu(u)=\nu(v)=L_b(1+2z),\qquad \nu(w_0)=L_o.
$$

The first highest-jet action variations count each endpoint once and the middle contact twice. The other-contact variation of the normalized mixed derivative also contributes at the relevant order:

$$
\partial_{q_{o,2m}}b_2
 =-\frac{g}{c_o}\frac{w_0^{2m-2}}{(2m-2)!}+O(|(u,v)|^{2m}).
$$

This term is essential. Combining its residual-weighted moment with the action variation gives the factor $1+2mz$, not merely 1. The manuscript retains it with the correct sign and unequal-curvature scale. Consequently

$$
D_{q_m}\xi_{m-1}
 =-\begin{pmatrix}(1+2z)^m&1+2mz\\1+2mz&(1+2z)^m\end{pmatrix}
   \operatorname{diag}(k_mL_0^m,k_mL_1^m),
\qquad k_m=\frac4{2^m(m+1)(m!)^2}.
$$

The determinant is nonzero because the difference of the two symmetric eigenvalues is the strict binomial remainder $\sum_{r=2}^m\binom mr(2z)^r$. No division by a curvature difference occurs. At $g=1,c_0=c_1=2,m=2$, the printed matrix $-\frac1{1728}\bigl(\begin{smallmatrix}49&13\\13&49\end{smallmatrix}\bigr)$ and its antisymmetric eigenvalue magnitude $1/48$ are correct.

The proof does not rely solely on this algebra. The finite stationary equation establishes finite-jet dependence; the fixed Morse domain justifies the degree bookkeeping; evenness places the first unvaried corrections two endpoint degrees higher. Thus lower nonlinear terms cannot contaminate the displayed last-jet coefficient. Its independence from the highest jet gives affinity and the stated recursive analytic inverse. Analytic continuation is used only for analytic graphs, not to recover a general smooth graph from formal jets.

**Assessment:** no new correctness objection. Equal curvature is not a degeneracy of this block. Lack of estimates uniform in jet order or in a vanishing hyperbolicity margin is not a defect in the compact, fixed-order statement actually made.

### 3.2 The limiting block and the physical open image remain substantive

**Sources:** `article/23_two_contact_rigidity.tex`, `thm:v12-two-contact`; `article/24_physical_image.tex`, `thm:v12-realization`.

The limiting block's antisymmetric factor is

$$
m\tanh((m-1)\gamma)-(m-1)\tanh(m\gamma)>0.
$$

Strict concavity of $\tanh$ verifies the sign. The own- and other-contact action sums, the diagonal Hessian variation in the relative determinant, and the identity $K_{m,b}r_b^{2m}=K_{m,1-b}$ account for the unequal-curvature column normalization. I found no inconsistency between this limiting block and the finite two-flight block; they represent different data coordinates.

The physical realization is not merely an abstract coefficient perturbation. Its two support-function directions start at order $2m$ at their selected contact and at order $2m+2$ at the opposite contact. The area compensator starts beyond every retained jet and has a nonzero area derivative. The support-envelope derivative gives the triangular diagonal entries $-(2m)!\kappa_b^{2m}$. Thus both contact-jet vectors vary independently in a genuine local analytic family while the selected leading hierarchy remains fixed.

The theorem constructs such families near the specified periodic disk configuration. It does not assert an open infinite-dimensional image of all smooth energy profiles. That stronger statement is neither proved nor claimed, and is not a missing lemma in the finite-dimensional argument.

### 3.3 The two-flight observation theorem is correct with its actual family hypothesis

**Source:** `article/29_two_flight_benchmark.tex`, `cor:v13-jet-coordinates`, `thm:v13-two-flight-observation`.

At fixed order $M$, the two jet maps have analytic triangular inverses. Their composition therefore gives a finite-dimensional coordinate change, not an equality of complete law functions. In the two-flight coordinates the nodal derivative has two Vandermonde blocks $V_h$ plus a remainder $O(h^{M})$; $\|V_h^{-1}\|=O(h^{-(M-1)})$. The transformed error is consequently $O(h)$. Choosing one sufficiently small positive $h$ establishes rank without a finite-to-infinite bridge approximation.

The passage to actual probabilities multiplies rows by fixed positive factors on the constructed family. Restriction to a small convex parameter ball, followed by integration of a Jacobian uniformly close to a fixed invertible matrix, gives genuine bi-Lipschitz coordinates. This is stronger than merely invoking pointwise nonsingularity.

The ordered finite-net estimator is Borel. Its concentration bound charges every binary preparation. For the lower bound, the alternatives are actual tables separated by $N^{-1/2}$, and the probabilities have fixed positive margins. Conditional relative entropy controls adaptive and randomized choices among the specified windows. These arguments justify the stated confidence cost and $N^{-1}$ squared-risk order.

That risk order is a regular parametric consequence of local invertibility, as the revision now acknowledges. It is not a new general principle of statistical rigidity, a bound for unknown arbitrary smooth families, or an optimal full-profile rate.

### 3.4 The relative determinant argument does address exponentially small physical flux

**Sources:** `v3/10_geometry_action.tex`, `v3/20_integration.tex`, `v4/10_boundary_layers.tex`, and `article/15_operator_comparison.tex`.

The manuscript normalizes the exact corner-cofactor formula before estimating the determinant. Locality and endpoint decay give summable Hessian perturbations in trace norm. The logarithmic series uses one trace-class factor and bounded operator factors, so the estimate does not accumulate the number of interior sites. The two-block comparison separates the endpoint perturbations, controls the discarded middle part, and estimates the remote Green kernels. Fixed-order differentiated series remain summable.

The passage to probabilities is separate and legitimate. Uniform positivity of the endpoint Hessian gives a common Morse chart. The physical residual-time interval is not truncated by a preceding roof on the chosen small collar. Odd endpoint terms vanish after integration on the fixed disk, making the normalized law smooth down to zero with the required finite-order derivative control.

Thus an objection based simply on dividing an absolute action error by an exponentially small twist would miss the actual proof. The remaining concern is not that this proof uses an invalid normalization. It is how much of its forward conclusion is already explained by the closest local hyperbolic mechanism; see Section 4.

### 3.5 Smooth-profile inversion and acquisition are not being replaced by formal or oracle observations

**Sources:** `article/20_boundary_compatibility.tex`, `article/21_abel_stability.tex`, `article/28_regularized_observation.tex`, and the pilot in `article/27_profile_calibration.tex`.

The same-type law produces an autoconvolution of $x^{-1/2}V(x)$. The uniqueness proof convolves once more with $x^{-1/2}$ and obtains a second-kind Volterra equation with a nonzero constant leading term. Gronwall's inequality proves equality of complete smooth profiles on the collar. This is not formal Taylor-series inversion.

The Abel flux discrepancy has an affine nullspace on arbitrary functions, and the paper removes it only on the physical zero-value/zero-slope class. Its two-sided inverse estimate is derived in that specified norm. In particular, a uniform raw-probability error is not silently used as a differentiated norm.

The acquisition proof uses the two extra integrated-flux derivatives on the unchanged $C^{m-1,1}$ profile class. Its three reconstruction bounds have distinct jobs: approximation error $h^{m-1/2}$, bounded transport of structured $C^3$ bridge error, and amplification $h^{-5/2}$ of scalar nodal noise. The Bernoulli variance and the sum of all ceilings give the stated sufficient exponent

$$
2+\frac6{m-1/2}+\frac\gamma{|\log\tau|}.
$$

The self-calibrated proof uses the exact conditional mean $R H_{j,b}(d+\Delta)$ of the scaled new bit. It estimates translation before regularization, includes the energy origin, and projects pilot outputs into supplied boxes so that the charge remains bounded on bad histories. The pilot uses unknown smooth one-/two-flight remainders and positive-node extrapolation, not an exact-family probability oracle. Its smaller accuracy power is absorbed into the total bound.

These are meaningful observation results. Their sufficient exponent is explicitly not claimed to be minimax, and the physical finite-family lower bound is not imported as a full-profile lower bound. I do not reopen those distinctions.

## 4. R13-1 — The closest forward comparison is still missing

**Classification:** major contribution/positioning issue; **not** a counterexample to the stated smooth relative theorem.

**Locations:** Introduction Sections 1.4–1.5, `thm:v8-main-relative`, and `article/15_operator_comparison.tex`, `sec:v9-operators`.

The revision correctly distinguishes its inverse data from global spectral data. But this does not compare the central relative factorization with the local forward structure of a hyperbolic symplectic map. The cited De Simoi–Kaloshin–Leguil paper itself recalls analytic normalizing coordinates near a period-two orbit, with a map

$$
N(s,p)=(\Delta(sp)s,\Delta(sp)^{-1}p),\qquad \Delta(0)=\lambda\in(0,1).
$$

Its global symmetry restrictions should not be mistaken for restrictions on the mere existence of that local analytic normal form. See that paper's printed pp. 10 and 13 in arXiv:1905.00890v4. The endpoint calculation used for this review is derived separately in the companion note; it is not attributed as a theorem proved there.

For fixed incoming stable coordinate $s$ and outgoing unstable coordinate $t$ after $n$ returns, the invariant $I$ obeys $I=st\Delta(I)^n$. Therefore the exact mixed-boundary derivative is

$$
T_n=\frac{\Delta(I)^n}{1-nI\Delta'(I)/\Delta(I)},\qquad
\lambda^{-n}T_n=1+O_{C^k}(\sigma^n)
$$

on a fixed small box, for any fixed derivative order and a suitable strict exponential margin. This is already a relative estimate.

A canonical calculation alone would not compare the actual billiard observable. The companion therefore also carries out the physical endpoint projection. Write $u=U(s,p_0)$ and $v=V(s_n,t)$, with nonzero stable and unstable projection derivatives. The physical flux is exactly

$$
J_n=\left|T_n/\det D_{s,t}(u,v)\right|.
$$

After normalization at the orbit it converges to the product of the two normalized inverse projection Jacobians. The stationary action similarly separates by integrating its limiting first variations. These calculations show that the analytic relative product phenomenon is accessible without the half-line determinant construction. They also offer a stable/unstable geometric interpretation of the analytic amplitudes.

There are important limits to this comparison. The note does not supply uniformly smooth normalizing charts for the manuscript's arbitrary smooth families, does not derive its full odd-parity theorem, and does not prove its energy-profile inverse or preparation theorem. I therefore do **not** claim that A2's full theorem is an immediate consequence of the cited paper, or that a local analytic argument disposes of its smooth and statistical achievements.

Nevertheless, the current comparison with elementary matrix identities is insufficient to establish the conceptual novelty of the forward law. The revision should do the following, as one focused mathematical comparison: state the restricted analytic benchmark with its physical projection step; identify precisely which hypotheses and conclusions of Theorem 1.1 remain outside that benchmark; and explain the significance of that remainder together with the geometric and observation results. The existence, differentiability and uniformity of any proposed smooth normal-form replacement must be checked rather than asserted.

This request does not require replacing the valid determinant proof, deleting retained material, claiming an unproved general rigidity result, or optimizing the statistical exponent. Its object is to establish what is actually new at the center of the paper.

## 5. R13-2 — Correct the universal family claim in the abstract

**Classification:** localized statement error; straightforward qualification, not a failure of Theorem 11.3.

**Location:** `main.tex`, abstract; compare `thm:v13-two-flight-observation`.

The abstract says that “every fixed finite-dimensional family” can be observed through positive windows at two flights. The actual theorem begins with a physical analytic family of Theorem 10.1 and then restricts to a small coordinate neighborhood. That hypothesis cannot be dropped.

Here is a physical counterfamily to the literal universal claim. In a sufficiently large periodic cell, fix two analytic strictly convex obstacles forming an isolated shortest channel. Place a third small analytic obstacle far from its contact neighborhoods and chords, with a strict clearance margin. Translate only that third obstacle through a small one-parameter interval. Choose a generic configuration so these translated tables are not all isometric. The lattice, obstacle areas, free area, selected gap, selected curvatures and both participating boundaries are unchanged. Separation and positive curvature persist.

Every sufficiently near-onset selected alternating bridge in the fixed channel is therefore unchanged. Its exact endpoint action, mixed derivative and phase normalization are unchanged, and its small residual-time interval remains below every preceding roof. Hence its selected two-flight probabilities, and indeed its selected longer near-onset probabilities, are identical throughout the family. They cannot give a bi-Lipschitz coordinate for the translating parameter. This is not a claim that all collision statistics of the entire table are identical; it concerns precisely the selected-channel experiment.

The appropriate repair is to say **each of the locally full-rank physical finite-jet families constructed here**, or an equally precise reference to Theorem 10.1. Alternatively, state a full-rank hypothesis explicitly. The surrounding context makes the intended narrower reading understandable, but the abstract should not ask the reader to supply a missing quantifier restriction.

## 6. Significance assessment at the requested level

The new two-flight proof is satisfactory. The finite physical image is real. The general energy invariant is not a formal jet placeholder, and the observation theorem is not an oracle reformulation. These points should be retained in any fair assessment.

The strongest case for the paper is now the combination of a uniform smooth physical relative law, its explicit endpoint-amplitude construction, a complete symmetrized invariant on a collar, and an observation procedure respecting the rarity and normalization of the physical event. The independent-contact inverse adds geometric content in its clearly stated even class.

The outstanding problem is demonstrating the exceptional advance of that package after the two close mechanisms are accounted for: finite nonlinear records already give the fixed-order geometry, and analytic hyperbolic coordinates already explain a relative endpoint product law. A different proof that is robust in smooth families can be valuable, but its scope and conceptual gain must be stated precisely. Simply repeating that the data differ from a marked or Laplace spectrum does not answer the forward comparison.

Conversely, absence of unrestricted nonsymmetric boundary reconstruction, a global classification, an infinite-dimensional physical lower bound, or a sharp acquisition exponent is **not** presented here as a logical gap in the current theorems. Those are different possible research directions, not compulsory extra theorems for the next revision. I am not requesting arbitrary theorem inflation as a substitute for a significance argument.

My present recommendation remains negative for acceptance at the specified level and positive for a focused major revision. Closing R13-1 and R13-2 is a concrete next step; it does not pre-certify a subsequent editorial outcome. If the completed comparison leaves only a technically careful implementation of existing local mechanisms, a different venue could be appropriate. If the smooth uniformity and physical inverse consequences constitute a genuinely stronger advance, the manuscript must make that case through its actual theorem statements and proofs.

## 7. Verification, reading scope and source access

I wrote and ran a separate standard-library rational-arithmetic suite, [verify_review.py](verify_review.py). It imports no author module. Both ordinary Python and `python3 -O` passed **5,033 explicit checks**, and their JSON outputs were byte-identical. The committed [verification.json](verification.json) records the category counts and limits.

The diagnostics include 243 contact blocks across 27 positive rational geometries and orders $m=2,\ldots,10$, with 486 oriented rows; direct Schur variances, action/twist moments, invertibility and a negative control omitting the twist are checked. There are also 45 rational limiting-block identity cases and 216 normal-form cases comparing a product of one-step derivatives against the implicit mixed-boundary formula and its physical symplectic projection. These are finite algebraic checks, not replacements for the displayed all-order arguments.

I did **not** run the author's advertised 3,295-check suite or the prior review's 1,335-check suite in this review. I did not compile the main manuscript or companion, verify every historical-retention count, run remote CI, perform a nonlinear billiard simulation, or independently check every auxiliary appendix theorem. Author statements about those activities remain author statements. The [source audit](SOURCE_AUDIT.md) distinguishes direct reading from contextual comparison and records the frozen source blobs.

The present review directly examines the complete new two-flight section and the principal relative-law, compatibility, Abel, regularized acquisition and smooth pilot chain. Selected inherited supporting sections were also read, as specified in the audit. No result was declared correct merely because it had passed an earlier AI review.

### Primary literature locations used

- De Simoi–Kaloshin–Leguil, arXiv:1905.00890v4: Definition 1.3, Main Theorem and Remark 1.5 for the revised inverse comparison; printed pp. 10 and 13 for the local normal form and scope distinction. [Versioned source](https://arxiv.org/abs/1905.00890v4).
- Finamore–Leguil, arXiv:2510.18983v1: introduction and Theorem A, retaining the enriched marked length spectrum and finite-horizon hypotheses. [Versioned source](https://arxiv.org/html/2510.18983v1).
- Zelditch, *Inverse spectral problem for analytic domains II*: the stated symmetry classes and Theorems 1.1 and 1.4, not an unrestricted spectral determination assertion. [Primary preprint](https://arxiv.org/abs/math/0111078).

These checks verify the particular comparisons used here; they are neither an exhaustive priority search nor an independent re-refereeing of those publications. The new forward benchmark is deliberately narrower than a claim that any of them subsumes A2.
