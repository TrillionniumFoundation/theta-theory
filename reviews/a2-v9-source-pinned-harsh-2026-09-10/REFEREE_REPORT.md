# Independent referee-style report — A2 v9 carrier, unchanged v8 mathematics

**Recommendation:** **Not ready to be treated as a completed post-v8 resubmission. For the unchanged mathematical manuscript, I do not recommend acceptance at the requested top-four general mathematics-journal level.** The principal reason for the latter assessment remains the demonstrated significance of the contribution, not a newly established fatal error in its central theorems.

The source audit does not support inventing a mathematical failure to make this report harsher. The relative-flux proof, the exact four-window inverse, and the scoped joint minimax result survived the examinations described below. Conversely, their survival is not a proof certificate or sufficient reason for an affirmative recommendation at the requested venue. A new directory and branch name do not supply a new theorem or an answer to an outstanding referee request.

**Date:** September 10, 2026, Asia/Singapore.  
**Reviewer:** GPT-6 Astra Pro, conducting an independent AI referee-style audit at the repository owner's request. This is not a journal-commissioned report, an editorial decision, a human endorsement, a blinded review, or an exhaustive originality certification. The previous report was consulted, but the additional derivations and diagnostic script accompanying this report were produced and checked for this review.

## 1. The submission must first be identified correctly

| Item | Frozen identity |
|---|---|
| Repository | `TrillionniumFoundation/theta-theory` |
| Latest identified A2 revision branch | `revision/a2-v9-relative-flux-poisson-minimax-2026-09-09` |
| Reviewed head | `12a3f50e143cc4951d8e9bea888206d965b90e51` |
| Head timestamp recorded by GitHub | `2026-09-09T13:36:38Z` — September 9, 21:36:38 Singapore |
| Root tree | `ed5b559c9548b49ba9dd7e55c7eca8a7357df348` |
| Reviewed directory | `papers/A2-v9-relative-flux-poisson-minimax/` |
| Entire manuscript subtree | `b3056b1068aec2c9f2eafd90b8d2583c2dd3ac4a` |
| Latest preceding mathematical author revision | v8, `9345433799379d23993a038e213e62b6b0c16e34` |
| Intervening v8 review commit | `79ff2f96fc2e41899666065355238915f21273b0` |
| New review branch | `review/a2-v9-source-pinned-harsh-2026-09-10` |
| New review directory | `reviews/a2-v9-source-pinned-harsh-2026-09-10/` |

The v9 initialization commit follows the v8 review, but copies the v8 manuscript without mathematical changes. Both the v8 and v9 manuscript directories have the same complete Git tree object `b3056b...`. This is evidence of identical paths, modes, and contents throughout those subtrees, not a judgment based on similar titles. The v9 `README.md` still identifies the canonical v8 revision, and `RESPONSE_TO_REFEREES.md` still responds to the two v7 reports. The article's actual title remains *Relative boundary laws and inverse experiments in dispersing billiards*, by Qian Qi.

Importantly, the initialization commit explicitly disclaims completion of the mathematical revision. There is therefore **no basis for accusing the author of concealing an unchanged submission**. The correct conclusion is narrower: the latest branch exists, but it does not yet contain a completed response to the latest v8 referee report. This report reviews the material actually present rather than attributing anticipated “relative-flux Poisson minimax” results to the branch name.

The new review is based on the v9 head and adds only its own review directory. It does not replace either manuscript, edit the older reviews, change the default branch, or merge a revision.

## 2. Disposition of the preceding review

The controlling predecessor is `reviews/a2-v8-relative-boundary-harsh-independent-2026-09-09/REFEREE_REPORT.md` at `79ff2f96...`, together with its separately identified mathematical comparison `SMOOTH_ENVELOPE_MINIMAX.md`.

| Previous finding or request | Present disposition |
|---|---|
| The v7 exact-model/fixed-offset comparison and unknown-gap objection were answered in v8 | **Remain answered.** Identical source is not a reason to reopen a closed mathematical objection. |
| Analytic descent through coalescence and the four-window inverse had no fatal defect identified | **No contrary defect found in the present audit.** Relevant dependencies were inspected and the constrained determinant independently recomputed. |
| Joint minimax rates were valid only for the specified bounded-flight local binary experiment | **This scope is retained and remains indispensable.** No unrestricted-data lower bound is inferred. |
| One canonical article and retention of historical material | **The v8 organizational improvement remains.** Historical directories are not themselves a mathematical defect. The new carrier nevertheless needs an author-ready identity before it becomes a new resubmission. |
| V8-R1: demonstrate the exceptional significance of the nonlinear relative theorem with a sharper predecessor/consequence comparison | **No new response is present.** The same introduction and comparison section are carried forward. The assessment is elaborated in Sections 5–6 below. |
| Optional smooth-envelope lower bound supplied by the previous referee | **Still referee material, not an author theorem incorporated by v9.** Its absence from the paper is not itself a correctness objection. Its additional slack hypothesis and non-geometric nuisance status must not be dropped. |
| Author's v8 build and diagnostic evidence | **Inherited evidence for identical source, not independently repeated evidence in this review.** A copied manifest is not a new successful v9 build. |

The prior report's rejection recommendation was principally editorial. It did not identify a fatal new mathematical error which v9 could be declared to have left unfixed. That distinction is maintained here. Nor should successive AI-generated reports be counted as independent human referee votes.

## 3. Mathematical audit of the principal analytical chain

### 3.1 Short-flight localization and the Jacobi calculation

**Sources:** `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative`.

The geometric localization uses the correct sequence of facts: a finite set of relevant lifted pairs, uniqueness of each closest chord by strict convexity, positive clearance, separation of the outgoing normal states, and the observation that a bounded total excess makes every complete flight short. Reflection then forces alternation in one selected channel. The same neighborhood can be used at every impact; the proof does not introduce a new smallness loss at each collision. The claim concerns compact local families with gaps and curvatures bounded away from zero, not degenerating configurations.

For unequal contacts, the two-periodic rescaling is essential. Setting $c_b=1+g\kappa_b$, $c=\sqrt{c_0c_1}$ and $\gamma=\operatorname{arcosh}c$ reduces the interior recurrence to the constant-coefficient Jacobi recurrence. I independently eliminated the original finite Hessian for equal and genuinely unequal contacts, for both parities and including $j=1$. The printed endpoint Schur complement, Green kernel, and cofactor identity agree with these calculations.

In particular,

$$
\frac{-W_{uv}(0,0)}{\sqrt{\det H_j}}=\operatorname{csch}(j\gamma)
$$

is consistent with a uniformly positive endpoint Hessian and an exponentially small mixed derivative. Confusing these two scales would invalidate the proof, but the source keeps them separate.

### 3.2 Nonlinear localization, relative determinants, and differentiation

**Sources:** `v3/10_geometry_action.tex`; `v4/10_boundary_layers.tex`, `thm:v4-factorization`; `v5/15_differentiated_operators.tex`.

The nonlinear bridge is constructed in an endpoint-weighted space with weights $\rho^i+\rho^{j-i}$. The Green operator is bounded uniformly in that norm; local nonlinearities preserve the weights, and each fixed parameter derivative of the reference Green kernel is controlled after leaving an exponential margin. The action estimate and the trace-norm estimates use summability of the endpoint layers, not dimension times an operator norm.

The key identity is normalized before taking a limit:

$$
-W_{uv}=\frac{\prod_i[-\ell_{i,uv}]}{\det H_{\rm int}}.
$$

At the half-line level, the Hessian perturbation is trace class because it is both tridiagonal and localized. The logarithmic determinant is explicitly defined and normalized. The finite comparison retains two separated boundary blocks, discards the middle in trace norm, compares finite and half-line compressed Green kernels, and then uses the direct-sum determinant. This is sufficient in the printed argument to avoid a factor proportional to bridge length.

The differentiated-operator addendum is important, not cosmetic. Derivatives of $G\Delta H$ need not be small. After a fixed number of differentiations, one uses a trace-norm factor, bounded differentiated factors, and geometric decay only from the remaining undifferentiated factors. The resulting polynomial in the trace-series index is summable. This closes a possible gap which an unqualified appeal to termwise differentiation would leave.

I found no fatal defect in this chain on the stated compact local families. This is not a claim of arbitrary-itinerary control, sharpness of the exponential rate, or bounds uniform in derivative order. None of those stronger statements follows from the displayed argument.

### 3.3 Physical probability, residual time, and the common collar

**Sources:** `v3/20_integration.tex`, `lem:g-radial`; `v4/10_boundary_layers.tex`, `thm:v4-law`; `v6/10_experiment_transfer.tex`, `thm:v6-transfer`.

The full-phase density is the physical flux $(-W_{uv})\,du\,dv\,dr/(2\pi A)$, not an artificial transverse ensemble. The minimum roof bound prevents the preceding flight from truncating the small residual-time interval. An upper roof bound is unnecessary for this local argument, so lack of finite horizon is not a missing hypothesis.

The Morse change of coordinates is controlled by the positive endpoint Hessian, not by the exponentially small twist. Its fixed-disk integration removes odd endpoint powers and supplies a smooth right extension in the offset, with enough endpoint derivatives used for each requested offset derivative. The normalized integral can therefore be compared down to zero offset without differentiating a moving indicator formally.

For total variation, the crucial extra observation is that both residual fibers begin at zero. Their symmetric-difference length is bounded by the action difference. The latter vanishes quadratically at zero, which cancels the factor $1/d$ after scaling. Restoring the failure atom retains the rare-event factor:

$$
p_{j,d}\asymp d^2e^{-j\gamma},\qquad
\|P_{j,d}-P^\partial_{j,d}\|_{\rm TV}\le C p_{j,d}\tau^j.
$$

This is a genuine relative experiment statement. It is not a total-variation theorem for distinct embedded full collision arrays, and not a cost-free supply of successful records. The text expressly makes those distinctions.

## 4. Audit of the inverse and statistical claims

### 4.1 Symmetric analytic coordinates and the exact finite-window inverse

**Sources:** `v3/40_inverse.tex`; `v5/40_pairwise_inverse.tex`; `v6/30_three_amplitudes.tex`; `article/40_fixed_offset.tex`.

The chosen support family genuinely preserves all six shortest gaps while varying the three contact radii. Its area is constrained by those physical parameters. Central symmetry makes the two facing curvatures equal within each channel; without that equality, scalar amplitudes would identify the effective product parameter rather than both endpoint curvatures. The manuscript states this restriction.

The fixed-offset inverse needs analyticity in symmetric coefficients at coalescence, not merely smoothness in labelled radii. The proof supplies the required steps: an analytic stationary action and Morse map, normally convergent fixed-domain integration, full permutation symmetry from lattice rotations and reflections, and bounded holomorphic extension across the discriminant. The six equal gaps matter because no changing activation interface is introduced when summing the channels.

I independently differentiated the three elementary amplitude functions and recomputed the physical Jacobian, including its area terms. The result agrees with

$$
\det D=-\frac{2\sqrt2(15804720A_c+64253\pi)}{72930375A_c^4},
\qquad A_c=\frac{\sqrt3}{2}-\frac\pi{16}.
$$

The four programmed physical windows use a known reference gap, not the unknown true gap. Subtracting the two first-flight rows and scaling the gap column yields the nonzero limiting determinant $C_1\det D$. Fixing a sufficiently small positive design parameter before taking statistical accuracy to zero is legitimate. The inverse-function theorem is applied to the exact analytic finite-offset map and then restricted to the physical real-rooted locus. The root-matching estimate includes multiplicities.

The resulting theorem is an exact-family local inverse. Its constants may depend badly on the fixed window size. Its proof does not provide an efficient exact probability evaluator or an efficient optimization algorithm. Those are limitations already acknowledged in the source, not concealed correctness defects.

### 4.2 Joint minimax order and stopped experiments

**Sources:** `v7/30_count_lower_bounds.tex`; `article/50_joint_minimax.tex`; `v7/20_measurable_reconstruction.tex`.

The manuscript defines a fresh-preparation binary experiment with fixed maximum flight number, fixed local collar, a fixed physical neighborhood, parameter-independent rules, and an all-history admissibility condition. Only the requested bit is retained. Under those quantifiers, the sample order

$$
\mathcal N_K(\varepsilon,\delta,\eta)
\asymp(\varepsilon^{-6}+\delta^{-2})\log(1/\eta)
$$

is supported by the examined arguments.

The physical splitting pair has matching curvature separation of order $s$, but its **full finite-offset probabilities** differ by at most $Cd^2s^3$. The source proves this using physical rotational invariance and uniform third parameter derivatives, not only a leading-amplitude cancellation. Squaring that difference in Bernoulli entropy gives the sixth power. For timing, the higher-gap to lower-gap entropy direction is the correct one: it avoids an unsupported success where the reference law has zero probability. The bound is uniform even when a query crosses an onset.

The stopped chain rule is obtained by finite-history truncation and padding with stop symbols. The nearest-alternative test and binary data processing give the confidence logarithm. Separate curvature and timing pairs can legitimately be combined by taking the maximum of their lower bounds, which is comparable to the sum. The Borel compact selection is specified on every outcome, including nonunique minimizers and observations outside the inverse chart.

No part of this proves the same lower bound for full counts, positions, arbitrarily large flight numbers, or unrestricted observation times. The restriction is substantive, but it is not new criticism: the paper already imposes it.

### 4.3 The unknown-remainder envelope and the previous referee supplement

**Sources:** `article/60_smooth_remainders.tex`; `v7/40_fixed_bracket_acquisition.tex`; the predecessor's `SMOOTH_ENVELOPE_MINIMAX.md`.

The nuisance functions preserve the leading physical amplitudes but need not be exact probabilities generated by a billiard table. The source states only an upper bound for this envelope. Its fixed-budget pilot uses the square root of a probability with a quadratic onset; $C^m$ regularity suffices because a degree-$(m-1)$ approximation to the square-root amplitude is multiplied by the offset. The final normalized timing error is charged as the gap error divided by the sampling scale. The bracket search and all-history window bounds keep the construction valid on failed histories; there is no unbounded waiting for a success of possibly zero probability.

The finer pilot gap is retained separately from the compact-fit shape. This is permissible for the stated componentwise loss. It does not automatically mean that all returned coordinates encode one exactly consistent fitted table.

The previous referee supplement constructs a legitimate cutoff splice under an additional strict interior margin in the nuisance bounds. Its two physical leading triples have the same gap and cubic amplitude difference. A cutoff on scale $h\asymp s^{3/m}$ makes every larger offset exactly uninformative while bounding each query's entropy by $Cs^{6+6/m}$. Together with the timing pair and the manuscript's upper theorem, this yields the envelope comparison

$$
\mathcal N_m^{\rm env}(\varepsilon,\delta,\eta)
\asymp(\varepsilon^{-(6+6/m)}+\delta^{-2})\log(1/\eta).
$$

This is neither a new v9 author result nor a stronger lower bound within the exact physical family. Its nuisance alternatives are not asserted to be geometrically realizable. Incorporation is optional; dropping the strict-slack condition or reclassifying the alternatives as physical would not be acceptable.

## 5. Two additional significance tests supplied with this review

### 5.1 An explicit one-flight test of the flagship nonlinear example

The accompanying `TECHNICAL_AUDIT.md`, Section 1, derives a finite-flight comparison directly from the physical residual-time integral. For identical even contacts with $c=1+g\kappa$,

$$
\partial_q\mathcal R_1(0)=-\frac{g^2c^2}{12(c^2-1)^2}.
$$

For the exactly fixed-area family of `thm:v4-jet-fiber`, this gives

$$
\left.\partial_s\mathcal R_1^{(s)}(0)\right|_0=\frac89,
\qquad
\left.\partial_s\mathcal R_\infty^{(s)}(0)\right|_0=\frac{\sqrt3}{2}.
$$

Thus the same deformation which leaves every leading metric datum unchanged is detected by the first nonlinear coefficient at **one flight**. There is already a nonzero signal at every sufficiently small fixed positive one-flight offset. This is not merely a conjecture that shorter records might contain the information.

The conclusion does not invalidate the nonlinear example. It does show precisely why that example cannot by itself establish the indispensability of long-bridge analysis for higher-jet identification. The manuscript's existing one-flight discussion is consistent with this calculation. The long-bridge theorem must earn its significance through uniform relative asymptotics and growing-sample approximation, rather than through a claim of otherwise inaccessible quartic information.

### 5.2 What the erasure calculation does and does not buy

The same note, Section 2, supplies reversible kernels and a quantitative experiment-level Poisson comparison. In the exact tangent pair, put $r_i=\delta_{j_i}$ for successes and $r_i=p^0_{j_i,d_i}\delta_{j_i}$ for raw preparations. The entire binary product experiment compresses to an erasure with probability $\prod_i(1-r_i)$. A marked Poisson experiment with intensity $\lambda$ has erasure mass $e^{-\lambda}$. The difference is bounded by

$$
\frac{\sum_i r_i^2}{2(1-\max_i r_i)}+
\left|\sum_i r_i-\lambda\right|.
$$

For actual nonlinear laws, the tangent approximation errors must still be added. At finite critical intensity the printed assumptions require $d_j=o(e^{-2j\gamma})$ in the general case, or $d_j=o(e^{-j\gamma})$ for even graphs. They do not permit a fixed positive offset. The supercritical projection argument correctly removes the need to approximate the entire large sample, but does not remove these single-observation tangent restrictions.

The manuscript already records two-way randomizations after its triangular-schedule limit. The note makes the marked-Poisson formulation and a finite-schedule error bound explicit; it does not repair a missing experiment-convergence argument or supply an independently difficult nonlinear Poisson theorem. An unmarked Poisson count would contain no binary-hypothesis information at all; the revealing mark matters. The reverse kernels are for the known simple pair, not for a uniformly unknown table.

The existing text is careful about these limitations. The reviewer should preserve that care rather than treating a promising branch name, an exponential testing curve, and a temporal compound-Poisson theorem as interchangeable accomplishments.

## 6. Remaining major issue: significance, not invented falsehood

### R0 — Submission-readiness issue

A complete post-v8 resubmission is not currently present. A future author-ready head needs an explicit response to the actual v8 report and a change ledger referring to that report, not only a copied response to v7. The canonical directory, article, response, and verification provenance should agree about which version is being submitted. Since the current commit is honestly labelled as initialization, this request is a readiness requirement, not a misconduct allegation.

### R1 — Major editorial issue carried forward: identify the indispensable advance quantitatively

The central relative law is the most substantial piece of the paper. It combines a nonlinear boundary-value problem, relative determinants, and physical integration with uniform derivative control. I do not assert that a cited predecessor already contains this theorem, nor that a theorem proved with classical tools cannot be important.

Nevertheless, the unchanged manuscript has not persuaded me that this particular local synthesis and its consequences meet the exceptional significance threshold requested here. The finite-flight inverse and its singular statistical loss are soundly specified but do not automatically become deep applications of long-bridge factorization. The explicit computation in Section 5.1 makes that separation concrete. The elementary erasure/Poisson consequence likewise does not settle the importance of the genuinely nonlinear fixed-offset result.

The next response should provide a proposition-level comparison of **what is estimated, after what normalization, with which derivative and collision-length uniformities**, followed by a consequence which actually uses those uniformities. A useful comparison would set side by side the absolute stationary-action estimate, the relative mixed-derivative estimate, the trace-norm comparison, and the physical experiment bound. It should identify exactly which prior estimates fail to yield the claimed conclusion and why. Merely changing the observable's name or repeating that the flux is exponentially small does not complete that argument.

This is not a moving demand for global table rigidity, arbitrary itineraries, higher dimensions, or a sharp fixed-positive-offset exponent. Any of those would be a separate substantial research task, not a hidden missing hypothesis of the current theorem. A convincing analysis of the existing theorem's novelty and consequences could improve the editorial assessment without adding all or any of them. Nor does this report request deleting correct material or lowering the stated mathematical scope.

### R2 — Preserve experiment distinctions and avoid repackaging corollaries

This is an interpretation and presentation requirement, not a newly identified theorem defect. Maintain the distinctions between the exact analytic family, the unknown smooth envelope, selected endpoint experiments, and independent preparations. Maintain the distinction between tangent testing and nonlinear fixed-offset approximation. Any later Poisson-labelled statement should identify its complete observation space, kernels, intensity, remainder regime, and unknown parameters. If it is the corollary proved in the accompanying note, present it as such rather than as a replacement proof of a stronger nonlinear law.

### R3 — Evidence and presentation refinements

Keep one canonical submission identity, an explicit dependency map, and source-specific verification records. A successful compilation is valuable evidence of a readable artifact but is not a mathematical proof. Conversely, the failed source-bundle workflow observed for the initialization commit is not evidence that the TeX manuscript or its theorems fail: this review did not establish the cause of that workflow failure. No change of repository protections, permissions, or CI configuration is required by the present review.

## 7. Literature comparison and its limits

The following primary records were checked online for the limited comparisons made here. This was a targeted verification, not an exhaustive search or an independent re-proof of these papers.

| Primary work | Relevant predecessor theme | What this does not establish about A2 |
|---|---|---|
| Bolotin–Treschev, *Hill's formula* [L1] | Relates action Hessians and monodromy for discrete and continuous Lagrangian systems | Does not by this citation alone supply A2's normalized nonlinear physical endpoint law |
| Bálint–De Simoi–Kaloshin–Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards* [L2] | Recovers period-two curvatures and periodic Lyapunov exponents from marked length data | Does not identify those observations with fresh-preparation threshold probabilities |
| Batenkov–Yomdin, *On the accuracy of solving confluent Prony systems* [L3] | Studies local accuracy of singular algebraic reconstruction | Does not replace A2's constrained physical Jacobian or its exact-family likelihood argument |
| Carney–Nicol–Zhang, *Compound Poisson law for hitting times to periodic orbits in two-dimensional hyperbolic systems* [L4] | Studies scaled exceedances along hyperbolic dynamics, including dispersing billiards | Does not make an independent-product erasure calculation a dependent-orbit hitting-time theorem |

These differences are real. Different data alone do not prove exceptional importance, just as familiar ingredients alone do not prove absence of novelty. The remaining adverse recommendation is an editorial assessment made with these limits, not an asserted priority theorem.

## 8. Independent verification, coverage, and exclusions

The new `verify_review.py` was executed with ordinary Python and with `python -O`. Both runs passed **112 exact-algebra checks and 22 ordinary 60-decimal arithmetic checks**, and their JSON outputs were byte-identical. The new script does not execute or count the author's diagnostic suites, and is separate from the earlier referee's script. The total of 134 is the count of this independently written suite, not an adoption of an inherited 134-check claim.

The checks include direct finite Hessian elimination for both parities and unequal contacts, Green inverses, cofactors, the squared relative twist identity, the physical area constraint, all twelve amplitude derivative entries, the physical determinant and limiting four-window block, splitting distances, the new one-flight coefficient, the half-line coefficient, a finite-length quartic limit diagnostic, overlap quadrature, exact discrete erasure products, the Poisson-erasure bound, cutoff smoothness, rate exponents, and illustrative confidence/onset entropy inequalities. The synthetic onset checks are not evaluations of exact nonlinear billiard probabilities.

The principal relative, fixed-offset inverse, joint minimax, and nuisance-envelope proofs and the dependencies discussed above were inspected in source. The marked-source integration and pole argument were inspected as part of those source files. This is not a fresh line-by-line re-certification of every retained appendix, the full finite-jet realization theory, the collision-record response chapters, the historical arithmetic material, or the separate two-collision companion. Those exclusions are explicit in `VERIFICATION.json`.

No independent TeX compilation, PDF rendering, visual inspection, interval enclosure, proof-assistant check, exact nonlinear probability solver, or remote CI rerun was performed. The author-reported v8 build remains evidence supplied by the author. The review's finite checks cannot establish the infinite-dimensional nonlinear estimates or certify all bibliographic priority. These are limits of the evidence, not manufactured counterexamples.

## 9. Source locators and primary references

All manuscript sources in this report are pinned to [the reviewed carrier commit](https://github.com/TrillionniumFoundation/theta-theory/commit/12a3f50e143cc4951d8e9bea888206d965b90e51) under [the actual v9 directory](https://github.com/TrillionniumFoundation/theta-theory/tree/12a3f50e143cc4951d8e9bea888206d965b90e51/papers/A2-v9-relative-flux-poisson-minimax). The source paths and LaTeX labels cited next to each assessment identify the relevant arguments; the manifest records the associated blob identities.

The [preceding report](https://github.com/TrillionniumFoundation/theta-theory/blob/79ff2f96fc2e41899666065355238915f21273b0/reviews/a2-v8-relative-boundary-harsh-independent-2026-09-09/REFEREE_REPORT.md) and its [smooth-envelope comparison](https://github.com/TrillionniumFoundation/theta-theory/blob/79ff2f96fc2e41899666065355238915f21273b0/reviews/a2-v8-relative-boundary-harsh-independent-2026-09-09/SMOOTH_ENVELOPE_MINIMAX.md) remain distinct historical documents. The current author's response is the unchanged `RESPONSE_TO_REFEREES.md` in the reviewed directory.

- **[L1]** S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257. [Primary author preprint](https://arxiv.org/abs/1006.1532); DOI `10.1070/RM2010v065n02ABEH004671`.
- **[L2]** P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, Communications in Mathematical Physics 374 (2020), 1531–1575. [Primary author preprint](https://arxiv.org/abs/1809.08947); DOI `10.1007/s00220-019-03448-x`.
- **[L3]** D. Batenkov and Y. Yomdin, *On the accuracy of solving confluent Prony systems*, SIAM Journal on Applied Mathematics 73 (2013), 134–154. [Primary publisher record](https://epubs.siam.org/doi/10.1137/110836584); [author preprint](https://arxiv.org/abs/1106.1137).
- **[L4]** M. Carney, M. Nicol and H.-K. Zhang, *Compound Poisson law for hitting times to periodic orbits in two-dimensional hyperbolic systems*, Journal of Statistical Physics 169 (2017), 804–823. [Primary author preprint](https://arxiv.org/abs/1709.00530); DOI `10.1007/s10955-017-1893-9`.

## Final assessment

There is a coherent and nontrivial local analytical and statistical manuscript here. The examined mathematics should not be dismissed by resurrecting objections which its actual statements already answer. At the same time, the current v9 carrier supplies no post-v8 mathematical revision, and the unchanged submission has not yet earned my affirmative recommendation at the requested venue. The next author response should address the real outstanding significance question with an accurately identified manuscript and a precise demonstration of the relative law's indispensable contribution—not with additional version labels, larger theorem counts, or an inflated description of an elementary erasure corollary.
