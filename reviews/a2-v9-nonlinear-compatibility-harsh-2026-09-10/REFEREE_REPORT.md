# Referee report: completed A2 v9 nonlinear-boundary revision

**Manuscript:** Qian Qi, *Relative boundary laws and inverse experiments in dispersing billiards*, September 9, 2026.  
**Review date:** September 10, 2026 (Asia/Singapore).  
**Standard requested:** Annals / Acta / Inventiones / JAMS.  
**Capacity:** Independent AI referee-style assessment requested by the repository owner; not an appointment or decision of any journal.  
**Recommendation:** **Reject in its present form at the requested journal level.** This is a significance and positioning judgment, not a claim that the audited principal theorems are false. The completed revision makes substantial, genuine mathematical progress. No fatal error was found in the new arguments and the essential dependencies examined below.

## 1. Exactly what has been reviewed

Repository: `TrillionniumFoundation/theta-theory`.

- Revision branch: `revision/a2-v9-nonlinear-boundary-compatibility-2026-09-09`.
- Frozen source commit: `33ef794a398b23015651482e93be7667c08d6fad`.
- Source commit time: `2026-09-09T19:27:44Z`, or September 10, 03:27:44 in Singapore.
- Root tree: `1ec6d1a33e24f4017dc83b5388adb004f12163c3`.
- Restored paper directory: `papers/A2-v9-nonlinear-boundary-compatibility/`.
- Published entry point: `A2_REVISION_V9_INDEX.md`; source restorer: `papers/A2-v9-nonlinear-boundary-compatibility/restore_sources.py`.
- Immediate mathematical baseline: A2 v8 at `9345433799379d23993a038e213e62b6b0c16e34`.
- Controlling v8 review: `79ff2f96fc2e41899666065355238915f21273b0`, including `REFEREE_REPORT.md` and `SMOOTH_ENVELOPE_MINIMAX.md` in `reviews/a2-v8-relative-boundary-harsh-independent-2026-09-09/`.

There is another branch named `revision/a2-v9-relative-flux-poisson-minimax-2026-09-09`, at `12a3f50e143cc4951d8e9bea888206d965b90e51`. That earlier initialization is not the completed revision reviewed here. The existing `review/a2-v9-source-pinned-harsh-2026-09-10` review concerned that other source state. Its conclusion that the v9 mathematical changes were not yet present must **not** be transferred to the present source.

The current source is supplied through a lossless publication payload, rather than every native manuscript file being directly exposed at the restored path. A previously delivered packet was used for local access, but its title was not accepted as authentication. I reconstructed the complete publication JSON from its 119 files and obtained the exact published digest

```text
payload JSON SHA-256:
eeba93cc4d5e0bc4f03d7dd2604bcdc13e62fd885b6cb8fe8195f3b367e687d0
XZ transport SHA-256:
ef947b9ee98acd7348d4e6d3b76a8d9f0384e63a9ea062afd30f30d48fff9a91
```

Both match the publication metadata at the frozen GitHub source. This establishes the identity of the complete packet used for the audit, not merely the identity of selected excerpts. It comprises 117 text files and two PDFs. Source-relative references below refer to this authenticated restoration. PDF page and theorem numbers were checked against the independently rebuilt auxiliary file.

**Coverage.** The detailed fresh audit covered the three new sections, the response to the v8 review, and the central localization → nonlinear bridge → relative determinant → half-line factorization → physical integration chain. It also covered the physical experiment transfer, finite-offset analytic descent and inverse, the joint binary minimax argument, and the smooth-envelope upper bound needed by the new lower bound. The nonlinear quartic calculation was checked as a concrete nonconstant physical example. This is not a fresh line-by-line certification of every historical appendix, the entire eleven-paper program, or the companion's every proof. Retention and compilation of that material were checked separately. No formal proof assistant or nonlinear finite-offset billiard probability oracle was used.

## 2. Editorial assessment

The strongest part of this manuscript remains the uniform, nonlinear **relative** boundary law. The v9 additions are not cosmetic. In particular, Section 9 gives an actual full-function consequence of the two-boundary limit, not another finite-dimensional fit decorated with long-bridge terminology. Its positive-offset compatibility, full smooth-profile uniqueness, differentiated-norm stability, and finite-record defect deserve to be evaluated on their own terms.

Nevertheless, I do not find that the revision yet establishes the exceptional mathematical importance required for the requested journals. Once the separated half-line density has been established, the principal new inverse mechanism is a normalized, weakly singular deautoconvolution problem. The parity identity follows from commutativity and associativity; the jet inverse is a triangular square root; and the stability proof is an Abel reduction to a second-kind Volterra equation followed by Gronwall. These are useful and correctly deployed mechanisms, but their application here does not by itself settle the significance question left by v8.

This is not an assertion that a short proof is unimportant, that classical ingredients preclude an important theorem, or that the exact relative billiard law is already a theorem in the cited literature. I did **not** locate an exact published theorem subsuming the entire physical relative law, and do not claim an exhaustive priority search. The problem is that the manuscript still needs a substantially sharper account of why the particular invariant and its quantitative recovery change the geometric or dynamical understanding of this problem, beyond organizing the two separated boundary measures already constructed.

The four-window inverse is a meaningful theorem in its exact analytic family, but it is not an application requiring arbitrarily long bridges. The new smooth-envelope minimax theorem is mathematically useful and properly attributed; it is a different observation model, and does not become an exact-billiard lower bound merely by retaining physical leading parameters. Neither result should be used to amplify the significance of the general relative law by changing the experiment under discussion.

A negative venue recommendation is therefore defensible, but it must be stated honestly: **the remaining rejection ground is editorial significance, not a newly discovered contradiction in the main mathematics.** It would be misleading to manufacture fatal proof objections after the author has explicitly supplied the hypotheses that avoid them.

## 3. Disposition of the previous review

### 3.1 Classical operator comparison: substantially answered

Section 8, pp. 20–23, now makes a meaningful separation. Proposition 8.1 is the scalar Dirichlet Schur/cofactor identity and a Neumann-series inverse estimate. Proposition 8.2 isolates trace-norm control of logarithmic determinants and its fixed-order differentiated version. Proposition 8.3 treats the normalized physical sublevel integral on a common positive-Hessian neighborhood.

The distinction from Bolotin–Treschev's **periodic** discrete Hill formula is correct. Their Theorem 2.1 relates the periodic monodromy determinant to a periodic action Hessian and mixed-edge determinants [P1]. It is not the same boundary-value problem as the scalar Dirichlet cofactor here. The manuscript also credits the inverse-entry/decay framework rather than claiming the elementary Green estimate as new; Meurant's paper is explicitly a review of inverse structure and decay [P2].

This does more than repeat “an absolute error cannot be divided by a small twist.” It identifies the additional summability, two-block localization, and physical integration work. I regard that technical clarification as substantially supplied. What remains open is the **importance** assessment of their combined billiard application, not the existence of the comparison itself.

### 3.2 A nonlinear consequence requiring the long-bridge result: supplied

Theorems 9.1–9.3 and Corollary 9.5, pp. 24–28, meet the literal mathematical request. The two oriented even limiting laws determine both normalized weighted energy profiles, and then the odd law. The finite-record defect depends on the uniform relative estimate and is not justified by unrelated fixed-flight Taylor expansions.

It would be factually wrong to repeat the earlier criticism that there is still no nonlinear consequence depending on the long-bridge theorem. That objection is closed in its former form. Closing it does not constitute an automatic acceptance recommendation.

### 3.3 Smooth-envelope comparison: supplied with the necessary extra hypothesis

Theorem 18.1, pp. 49–51, incorporates the referee-supplied nuisance-splice construction, including a fixed strict interior margin for the sum-convention C^m norm. The proof treats arbitrary legal local offsets, adaptive histories, random stopping, and the confidence logarithm. Section 17 supplies the all-history upper bound. Attribution to the v8 referee memorandum is explicit.

The conclusion is an envelope minimax theorem. The text correctly declines to realize arbitrary nuisance triples as exact finite-offset probabilities of a billiard table. No objection based on conflating these two experiments is sustained against the printed theorem.

### 3.4 Scope and reproducibility safeguards: retained

The manuscript does not equate symmetrized energy profiles with arbitrary asymmetric contact graphs; it does not assume convergence of factorially reweighted infinite Taylor series; it does not turn C^3 observation error into raw-frequency C^0 error; and it distinguishes selected orientations from an unlabelled complete event. These restrictions are present in the revised text, not repairs invented by this referee. Source retention and build claims were independently checked as described in Section 8 below.

## 4. Fresh examination of the principal analytical chain

### 4.1 Localization and the physical experiment

Source: `v3/10_geometry_action.tex`, Lemma `lem:g-channels`; `v3/20_integration.tex`, equation `eq:g-full-flux` and the threshold proof.

The finiteness of short lifted pairs, uniqueness of closest contact under strict convexity, clearance from third obstacles, and separation of outgoing normal states are used in the right order. The total near-minimal length condition bounds each summand separately, so alternating-channel localization does not accumulate a flight-number-dependent collar. For a nonminimal selected chord, the restriction to its local itinerary is essential and is retained.

The full-phase flux is not silently replaced by a transverse ensemble. In endpoint/residual coordinates the density is

$$\frac{-W_{uv}}{2\pi A}\,du\,dv\,dr.$$

The lower roof bound ensures that the small residual interval is neither cut off by the preceding roof nor followed by an extra hit. This is also why a global upper roof bound or finite-horizon assumption is not needed in this local argument. I found no normalization contradiction in the checked passage to the threshold probability.

### 4.2 Relative determinant, rather than an absolute-error division

Source: `v3/10_geometry_action.tex`, Lemmas `lem:g-jacobi` and `lem:g-relative`; `v4/10_boundary_layers.tex`, Theorem 6.2; `v5/15_differentiated_operators.tex`; Section 8.

The unequal-contact Jacobi scaling produces a uniformly positive endpoint Hessian while the mixed endpoint derivative is exponentially small. Those two quantities must not be confused. Direct independent Schur elimination for unequal curvatures agrees with the cofactor and normalized determinant formulas, including the empty interior at one flight.

More importantly, the proof controls the logarithm of the normalized cofactor by a summable edge correction and a trace-class Hessian perturbation. A uniform entrywise error multiplied by the number of sites would not suffice; the source instead bounds the sum of absolute entries using endpoint localization. The half-line amplitudes are defined with a fixed Fredholm-determinant normalization. The two retained boundary blocks, remote Green reflections, and discarded tails have exponentially small errors in the appropriate norm.

The differentiated argument also avoids assuming that derivatives of a small operator remain small. It uses bounded trace-norm derivatives and geometric decay from the undifferentiated factors. Fixed polynomial factors in the series index and bridge length can be absorbed by strict exponential slack. Higher derivative constants may grow; the theorem only fixes each finite order. I did not find a hidden factor of the matrix dimension invalidating this argument.

### 4.3 Offset-zero integration and statistical transfer

Source: Theorem 6.3; `v3/20_integration.tex`, Lemma `lem:g-radial`; Proposition 8.3; `v6/10_experiment_transfer.tex`.

The constructive Morse chart uses the positive endpoint Hessian, not the small twist, as the inverse bound. Both the action and amplitude are compared after passage to a common fixed disk. Odd Taylor terms vanish under that disk integral. This supplies smooth right-hand offset derivatives without assuming an even scatterer and without differentiating a moving sharp boundary informally.

The experiment-transfer proof is also appropriately relative: the mass error is multiplied by the selected-event probability, and unsuccessful preparations remain in the experiment. The action difference vanishes to second order, so division by the offset in scaled coordinates is legitimate. Comparing residual-time fibres gives the claimed total-variation control. The source does not assert total-variation convergence between different embedded full collision arrays. These distinctions should remain intact in future revisions.

## 5. Examination of the new nonlinear results

### 5.1 Theorem 9.1: normalization, compatibility, and smooth uniqueness

Source: `article/20_boundary_compatibility.tex`, especially the signed Morse coordinate, Theorem 9.1 and its proof, pp. 23–25.

With the manuscript's normalized profiles V_b and kernels k_b(x)=x^{-1/2}V_b(x), the correct law is

$$F_{bc}(d)=\frac{2}{\pi d^2}\int_{x+y<d}(d-x-y)\frac{V_b(x)V_c(y)}{\sqrt{xy}}\,dx\,dy.$$

Both branches of the signed Morse coordinate are required. Their sum accounts for the coefficient 2 and removes the curvature-dependent factors after the prescribed normalization. For V_b=V_c=1 the integral is exactly pi d^2/2, giving F_{bc}=1.

Twice differentiating d^2F yields

$$K_{bc}=\frac{\pi}{2}(d^2F_{bc})''=k_b*k_c,\qquad K_{bc}(0)=\pi.$$

Hence K_{01}*K_{01}=K_{00}*K_{11}. All these are finite-collar Volterra convolutions. No unseen data beyond the collar or analytic continuation of a Laplace transform is required.

The uniqueness proof concerns full smooth functions, not just their jets. If k*k=l*l, set f=k-l and a=k+l. Convolution with k_*(x)=x^{-1/2} changes a*f=0 into a second-kind equation because k_* * a=2pi+R, R(0)=0, and R' is bounded. Thus 2pi f+R'*f=0 and Gronwall implies f=0. The normalization makes f continuous at zero. I find this argument sound in the stated class.

### 5.2 Theorem 9.2: the differentiated data norm is substantive

Source: same file, Theorem 9.2, p. 25.

For candidates normalized at zero with first derivatives bounded by B, the printed forced equation is

$$2\pi f+R'*f=k_* * Q',\qquad Q=K-\widetilde K,$$

with ||R'||_infinity <= pi B. The constant in

$$\|V-\widetilde V\|_\infty\le \frac{D}{\pi}e^{BD/2}\|K'-\widetilde K'\|_\infty$$

is consistent with the Abel integral bound and Gronwall. The identity

$$Q'=\frac{\pi}{2}\big[6(F-\widetilde F)'+6d(F-\widetilde F)''+d^2(F-\widetilde F)'''\big]$$

explains the C^3 norm. The statement is on the image and does not provide a regularized estimator from raw binary observations. It also does not prove that three derivatives are the optimal loss.

An explicit norm-separation example is proved in Section 7.1 of this report. It shows that one cannot simply replace the printed data norm by C^0 even on a positive normalized abstract profile class with a uniform first-derivative bound. This supports the importance of the manuscript's qualification; it is **not** a counterexample to Theorem 9.2, and no physical realization of the abstract example is claimed.

### 5.3 Theorems 9.3 and Corollaries 9.4–9.5

Source: same file, pp. 26–28.

The simplex coefficient is

$$\int_{x+y<d}(d-x-y)x^{r-1/2}y^{s-1/2}\,dx\,dy
=\frac{\pi(1/2)_r(1/2)_s}{(r+s+2)!}d^{r+s+2}.$$

Consequently the factorially reweighted finite series has rank one. Normalized diagonal square roots give the stated triangular inverse, and division by the nonzero Pochhammer coefficients recovers the profile jets. This is a finite-order polynomial calculation, not a claim of convergence of an infinite factorial transform.

Independent calculation confirms the coefficient and sign in

$$F_{01}''(0)=\frac{F_{00}''(0)+F_{11}''(0)}2-\frac3{16}\big(F_{00}'(0)-F_{11}'(0)\big)^2.$$

The finite-record corollary follows by applying the relative C^k law before the bounded finite-dimensional polynomial maps. Two even laws are sufficient for the reconstruction; the odd law gives a predicted observable and a compatibility test. The O(tau^{2n}) statement is a deterministic approximation statement at each fixed derivative/jet order. It is not a claim of uniformity in the order, a cost-free measurement of derivatives, or an unknown-normalization inverse.

### 5.4 Section 18: an actual sharp envelope result, with a model boundary

Source: `article/65_envelope_minimax.tex`, pp. 49–52; upper bound in `article/60_smooth_remainders.tex`.

The same-gap splitting alternatives differ in the physical symmetric coefficients by O(s^3) while their curvature matching distance is of order s. A nuisance splice at h=L s^{3/m} makes the two positive-offset probabilities identical above h. Its r-th derivative perturbation is of order L^{-r}s^{3(1-r/m)}, so the fixed sum-norm budget is respected after using the strict interior slack. Below h, the Bernoulli relative entropy is bounded by C s^{6+6/m} per preparation. No assumption forcing the statistician to choose only shrinking windows is needed: the constructed nuisance functions erase the larger-window information.

The stopped entropy calculation is correctly conditional on the same history and common parameter-independent randomization. Truncation and padding by stop symbols give the finite-horizon identity; passage to the full transcript is justified when expected cost is finite. The testing entropy supplies the confidence logarithm. A separate circular gap pair supplies the timing term, with the correct one-sided entropy direction at the onset. The maximum of the two lower bounds gives their sum up to constants.

For the upper bound, h proportional to min(epsilon^{3/m},delta^{1/(m+1)}) in Section 17 yields the claimed order. Retaining the pilot gap estimate separately from the fitted coefficient parameter matters: otherwise the finer timing rate would not follow from a coarser coefficient fit. The source makes that distinction. All-history admissibility is checked even after unsuccessful calibration.

I find no new fatal defect in this proof. However, the conclusion remains

$$(\varepsilon^{-(6+6/m)}+\delta^{-2})\log(1/\eta)$$

for the smooth **observation envelope**, as opposed to

$$(\varepsilon^{-6}+\delta^{-2})\log(1/\eta)$$

for the separate exact-family bounded-flight binary experiment. The nuisance alternatives need not be exact billiard probabilities. This distinction is mathematically essential and already acknowledged.

## 6. Remaining concerns, ordered by importance

### E1. The case for exceptional significance remains unpersuasive

**Severity: major editorial reservation, not a correctness defect.**

The most important achievement is a relative physical boundary law uniform in bridge length, with a genuinely nonlinear limit and controlled derivatives. The new compatibility theorem is a natural and useful organization of that limit. But the current presentation still relies heavily on the accumulation of consequences to justify the importance of the central construction.

The completed revision answers the previous request for a nonlinear long-bridge application. I am not retroactively making a global rigidity theorem, arbitrary itineraries, or unknown-orientation recovery a condition for correctness. Nor am I requiring the author to abandon the general setup. Rather, the introduction must now make a credible, sharply delimited case for the significance of **this actual invariant** and **this actual experiment**. If the requested venue is retained, the work needs either a more compelling explanation of the impact of the proved result or a further conceptual advance that genuinely changes that assessment. Adding another elementary reformulation of the same rank-one identity would not do so.

### E2. The new inverse result lacks its closest inverse-problem comparison

**Severity: substantive positioning revision.**

The manuscript's bibliography discusses billiard rigidity, Hill formulas, inverse tridiagonal matrices, and statistical experiments, but it does not include a focused deautoconvolution comparison. This is the relevant comparison for Section 9, rather than only the classical operator comparison for Section 8.

Dai–Lamm develop local regularization for nonlinear inverse autoconvolution, preserving its causal structure [P3]. Hofmann–Werner–Deng discuss uniqueness and ill-posedness in an L^2 deautoconvolution setting, with limited-data uniqueness tied to positivity and support at the origin [P4]. Those papers do **not** automatically imply Theorem 9.2: the present kernel x^{-1/2}V(x) is locally integrable but not in L^2 near zero, and the stated observation norm is much stronger. Conversely, L^2 ill-posedness in those settings does not disprove the present C^3-to-C^0 estimate.

A satisfactory comparison should identify the different kernel class, finite-collar data, normalization, topology, and geometric origin. It should attribute the standard uniqueness/regularization framework without pretending that the exact physical result is already contained in an unrelated theorem. The text's disclaimer that it does not invent convolution machinery is welcome, but it is not a substitute for this comparison.

### E3. Keep the three observation models visibly separate

**Severity: synthesis and interpretation; the printed individual theorems are appropriately qualified.**

The normalized oriented long-bridge laws in Section 9, the four unlabelled fixed-window means in the exact analytic family in Section 15, and the unknown C^m nuisance probabilities in Sections 17–18 are different experiments. Their inverses recover different objects and require different supplied quantities. The reader should not have to reconstruct these distinctions from widely separated qualifications.

The appropriate remedy is a concise theorem-level comparison of what is observed, what is known, what is recovered, and in which norm or loss. In particular, area, multiplier, selected patch labels and onset normalization in Section 9 are not removed by the separate self-calibrated finite-dimensional result. The simple variance calculation in Section 7.3 explains why finite-bridge approximation error alone is not an acquisition theorem for the profile.

### E4. Organization and a minor logical wording correction

**Severity: expository, not a demand to delete mathematical content.**

The 91-page article is reproducible and now has a more coherent center, but it still carries substantial historical architecture. Source files named by successive revisions are not themselves a mathematical problem. The issue is the dependency narrative: the primary relative law and its new profile consequence should be distinguishable from ancillary finite-dimensional experiments and retained historical results without following revision labels.

Preserve the complete mathematics and proofs. A stable submission-facing organization and a more selective statement of the main contribution would improve the article without downscoping it. The old delivery-status text in the restored response describes a historical local packet; the root publication index records the later remote state. These should be explicitly distinguished in a submission-facing manifest so that the old “not pushed” sentence does not look like a present status claim.

Finally, the closing language of Section 9 concerning the necessity of both orientations and both parity subsequences should distinguish reconstruction from validation. Theorem 9.1 itself uses the two even laws to reconstruct both profiles and **predict** the odd law. Observing the odd subsequence is needed for the stated direct compatibility test, not as a third datum for that reconstruction.

## 7. Additional analytical checks and limitations

These calculations are supplied by this referee. They are not attributed to the author, and they do not enlarge the physical claims of the manuscript.

### 7.1 A smooth positive example separating C^0 from the printed stability norm

Set D=1 and x_0=3/4. Choose a nonnegative eta in C_c^infinity((0,1)) with maximum one and positive integral. For 0<h<1/8 define

$$V_h(x)=1+h\,\eta((x-x_0)/h),\qquad V_0(x)=1.$$

Then V_h(0)=1, V_h is positive, ||V_h'||_infinity <= ||eta'||_infinity independently of h, and ||V_h-V_0||_infinity=h. Let F_h be the same-type law in Theorem 9.1 with both profiles equal to V_h.

Both perturbation factors can never contribute simultaneously on x+y<d<=1, since their supports lie above 3/4. Integrating the unperturbed other factor gives exactly

$$F_h(d)-1=\frac{16}{3\pi d^2}\int_{x_0}^{x_0+h}
 h\eta((x-x_0)/h)\,x^{-1/2}(d-x)_+^{3/2}\,dx.$$

The expression is zero for d<=x_0. For each x in the support, (d-x)^{3/2}/d^2 is increasing on x<d<=1 because d<4x. Its supremum is consequently attained at d=1. Substitution x=x_0+ht gives

$$\|F_h-1\|_\infty=\frac{16h^2}{3\pi}\int_0^1
 \eta(t)\frac{(1-x_0-ht)^{3/2}}{\sqrt{x_0+ht}}\,dt\asymp h^2.$$

Thus no locally uniform C^0-data-to-C^0-profile Lipschitz constant can hold on this normalized positive abstract class with only the stated first-derivative bound. The quotient of the two errors grows like 1/h. This is not inverse discontinuity and does not rule out weaker moduli under additional assumptions. It does not contradict Theorem 9.2 and is not a realized-billiard counterexample.

The same example also separates full smooth-function recovery from recovery of all jets at zero: F_h is identically one on an entire initial interval, yet V_h differs from V_0 later in the collar. Taking both contact profiles equal gives a triple satisfying the parity identity exactly. Hence infinite Taylor information alone cannot replace the full-collar smooth data. The manuscript correctly uses a Volterra uniqueness argument rather than making that replacement.

### 7.2 Why the energy profile is not the asymmetric boundary data

At the level of the forward profile construction, set S(u)=a u^2/2 and B_epsilon(u)=1+epsilon u on a sufficiently small symmetric interval. Then chi(t)=t/sqrt(a), and the two-branch sum defining V cancels the odd amplitude term. All these choices give V=1.

This elementary example illustrates loss of odd weighted-coordinate information in symmetrization. It is not a construction of billiard tables with prescribed S and B; those objects satisfy additional dynamical constraints in the physical problem. It explains why the manuscript's explicit refusal to claim arbitrary asymmetric graph reconstruction is appropriate. No geometric nonuniqueness theorem is inferred from this example.

### 7.3 Finite approximation and the cost of direct empirical observation

Assume the normalization is known and consider direct estimation of one normalized selected-event law from N independent preparations at fixed positive offset d. Write

$$a_{j,d}=\frac{2A\sinh(j\gamma)}{d^2},\qquad F_{j,d}=a_{j,d}p_{j,d}.$$

For the empirical proportion, the unbiased estimator a_{j,d} times that proportion has exact variance

$$\operatorname{Var}(\widehat F_{j,d})
=\frac{a_{j,d}F_{j,d}(1-p_{j,d})}{N}
\asymp\frac{e^{j\gamma}}{Nd^2}$$

on the fixed positive collar where the normalized law is uniformly bounded above and below. Making a deterministic bias bound C tau^j smaller than a target error requires choosing a sufficiently long bridge; that choice increases this direct estimator's variance per preparation. Derivative estimation and uncertain normalization require further work.

This is an elementary variance statement for the specified estimator, **not** a minimax lower bound over all physical data, and it does not invalidate the existing experiment-transfer theorem. It identifies the work still needed before describing the Section 9 profile result as a raw-count statistical reconstruction procedure.

## 8. Reproducibility findings

All runs were performed on a separate working copy, leaving the authenticated input packet unchanged.

**Author suite `tools/verify_v9.py`:** 407 checks pass, comprising 136 exact algebraic checks, 113 ordinary 70-digit numerical checks, and 158 source-integrity checks. Normal and `python -O` runs produced byte-identical JSON outputs.

**Inherited suite `tools/verify_revision.py`:** 249 checks pass, comprising 86 exact algebraic checks, 31 ordinary floating-point checks, and 132 source-integrity checks. Normal and optimized outputs are byte-identical. The two suites overlap; 407+249 is not a count of independent mathematical proof obligations. In particular, retention of 148 formal theorem/proof environments is a source-integrity fact, not verification of 148 theorems.

**Independent referee script `verify_review.py`:** 115 finite checks pass in both modes, with byte-identical JSON outputs: 111 exact symbolic algebra/sign checks and four ordinary 60-digit bump-integral diagnostics. The script imports no manuscript code. It independently checks the simplex normalization, differentiated convolution kernels, finite transformed rank-one identities and inverse, the universal first two parity formulas, a forced Volterra identity, unequal-curvature Schur reductions, the nuisance scaling exponents, and the empirical variance identity. Its numerical examples illustrate the separately proved norm-separation calculation; they are not interval enclosures.

**Clean build:** the author build command was rerun from fresh temporary auxiliary state with shell escape disabled. The main article has 91 pages and the companion seven. Both output PDFs are byte-identical to the authenticated packet:

```text
main.pdf
  bytes: 968816
  SHA-256: aac894798467a94c5b3ad05cde2d677bf50dc1b0d272c5e4129992d0c39f99b9

two_collision.pdf
  bytes: 333376
  SHA-256: 1aaf0d2ed11571e3744aa7126adeec95d6781b8a5116e28c12955d9c232be241
```

The build records no unresolved references or overfull boxes. It retains the expected disabled-shell-escape notice and nonfatal underfull/font-expansion notices rather than suppressing them. Actual rendered main-article pages 25, 27 and 50 were visually inspected in this review; no clipping or illegible displayed formula was observed on those pages. This is a limited visual inspection, not a claim that all 98 pages were individually inspected.

`VERIFICATION.json` records the source hashes, run summaries and output identities. These local results are not represented as a successful GitHub Actions run or as a formal correctness certificate. Literature checking was targeted; the primary sources below were used for the specific comparisons stated, not for an exhaustive novelty claim.

## 9. Requested disposition and next revision criteria

I do not recommend acceptance, and do not recommend treating the previous rejection as discharged simply by the additional sections. Equally, I do not recommend withdrawing correct generality, deleting the nonlinear theory, or returning to an unchanged v8 carrier.

A response should address **E1–E4 separately**. The first requires a substantive argument about importance at the requested level; the second requires the closest inverse-problem comparison with explicit functional settings; the third requires a clear separation of experimental information; and the fourth is an organizational and wording correction. The technical assessments in Sections 4–5 should be treated as independently checked positive evidence, not as an invitation to rewrite sound arguments for cosmetic novelty.

No claim is made that adding one particular new theorem will guarantee acceptance. Conversely, any future negative review should not revive objections this revision has actually resolved. The correct current assessment is: **a real and mathematically coherent strengthening, with a still-unconvincing case for the requested top-four venue.**

## Primary references used for the targeted comparison

**[P1]** S. V. Bolotin and D. V. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257. DOI: `10.1070/RM2010v065n02ABEH004671`; arXiv: `1006.1532`. Theorem 2.1 is the periodic discrete Hill formula. Only this relevant framework and theorem were used here; the full 78-page preprint was not re-refereed.

**[P2]** G. Meurant, *A review on the inverse of symmetric tridiagonal and block tridiagonal matrices*, SIAM Journal on Matrix Analysis and Applications 13 (1992), 707–728. DOI: `10.1137/0613045`. Used for the established inverse-structure and decay framework, not as a theorem subsuming the nonlinear physical boundary law.

**[P3]** Z. Dai and P. K. Lamm, *Local Regularization for the Nonlinear Inverse Autoconvolution Problem*, SIAM Journal on Numerical Analysis 46 (2008), 832–868. DOI: `10.1137/070679247`. The publisher's primary abstract and bibliographic record support the causal local-regularization comparison; no uninspected detailed theorem is claimed to apply directly to the singular kernel here.

**[P4]** B. Hofmann, F. Werner and Y. Deng, *On uniqueness and ill-posedness for the deautoconvolution problem in the multi-dimensional case*, arXiv: `2212.06534v1` (2022). Relevant text: the L^2 setup, Section 2's convolution support discussion, and Section 3's limited-data uniqueness framework. The difference between that L^2 setting and the present locally integrable x^{-1/2} kernel is essential.
