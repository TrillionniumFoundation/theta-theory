# Independent referee report — A2 v8

## Recommendation

**Reject in its present form at the requested top-four general mathematics-journal level.** This is a judgment about the demonstrated importance of the submission, not a finding that its principal new theorems are false. I found no fatal defect in the new analytic-descent, four-window inversion, joint binary minimax, smooth-envelope acquisition, or supercritical-projection arguments examined below. The nonlinear relative-law proof chain also survives the present source audit.

This distinction is not a polite qualification of an otherwise negative mathematical report. It is the substance of the assessment. The previous exact-model comparison objection has been answered. The unknown-gap issue has been answered. The two v7 manuscripts have a genuine canonical successor. An adverse report which simply repeated those objections would now be inaccurate.

The strongest contribution remains the uniform nonlinear relative boundary law, including differentiated physical integration. The finite-dimensional statistical results are now substantially better specified and, at their stated scope, convincing. I nevertheless do not find that the submission has yet demonstrated the exceptional mathematical significance needed for my recommendation at the requested venue. In particular, the independent finite-flight statistical results cannot by themselves establish the significance of the long-bridge theorem. Section 6 explains this assessment and its limits.

A constructive addition accompanies this report. `SMOOTH_ENVELOPE_MINIMAX.md` proves, with an explicit interior-slack assumption on the nuisance bounds, that the smooth envelope has joint binary preparation order

$$
\bigl(\varepsilon^{-(6+6/m)}+\delta^{-2}\bigr)\log(1/\eta).
$$

It also constructs two different curvature targets whose probabilities agree at every window in any prescribed finite positive-offset design. Thus the exact-family four-window result really does require its stronger information model. This is a referee-derived strengthening of the comparison, not a theorem already present in v8 and not a geometrically realized lower bound for the exact analytic family.

**Date:** September 9, 2026, Asia/Singapore.  
**Reviewer:** GPT-6 Astra Pro, acting as an independent AI referee-style reviewer at the repository owner's request. This is not a journal-commissioned report, editorial decision, human endorsement, exhaustive originality certification, or proof-assistant certificate. The earlier reports were consulted; the assessment is not blinded.

## 1. Frozen submission and review scope

**Repository:** `TrillionniumFoundation/theta-theory`.  
**Reviewed branch:** `revision/a2-v8-relative-boundary-fixed-offset-2026-09-09`.  
**Reviewed commit:** `9345433799379d23993a038e213e62b6b0c16e34`.  
**Root tree:** `faa17cd323ad3545c1d6d1cd5bda17d33c4b68e2`.  
**Manuscript subtree:** `b3056b1068aec2c9f2eafd90b8d2583c2dd3ac4a`.  
**Commit timestamp, as recorded by GitHub:** `2026-09-09T12:55:17Z`, or 20:55:17 Singapore.  
**Article:** Qian Qi, *Relative boundary laws and inverse experiments in dispersing billiards*.  
**Manuscript directory:** `papers/A2-v8-relative-boundary-fixed-offset/`.  
**New review branch:** `review/a2-v8-relative-boundary-harsh-independent-2026-09-09`.  
**Review directory:** `reviews/a2-v8-relative-boundary-harsh-independent-2026-09-09/`.

The A2 branch search and the v8 head were rechecked before writing. The head remained the displayed commit. This review adds only its own review directory; it does not revise the manuscript, merge branches, or modify earlier reports.

The principal new proofs were read in source form. Their geometric, relative-determinant, integration, physical-family, three-amplitude, count-testing, experiment-transfer, and measurable-selection dependencies were examined separately. The contact-jet theorem and analytic-continuation argument were also inspected. This is not a claim to have independently re-certified every historical appendix, the separate two-collision companion, or all 130 retained formal environments. The coverage statement is deliberately narrower than the author's preservation ledger.

Source paths and LaTeX labels are the controlling locators below. I did not independently compile the article or inspect its PDF, and therefore do not use unverified page numbers as evidence. Stable source links are collected in Section 9.

## 2. Disposition of the preceding v7 requests

The two controlling reports are the sharp-physical report at `861a1465ad332652e83dd118c9061d79062a5511` and the critical-boundary report at `3af77abc50561c99c42c2a10ee2a8221dfad06da`. The present author response identifies both and explains the choice of the critical-v7 mathematical source spine [S1].

| Earlier request | Disposition in this v8 |
|---|---|
| S-R1/C-R1: compare exact fixed-offset inversion with shrinking designs, finer timing loss, and unknown remainders | **Closed as a mathematical response.** The four-window theorem uses exact probabilities; the joint timing lower bound is new and appropriately scoped; the nuisance experiment is explicitly different. |
| S-R2/C-R2: identify the nonlinear result rather than inflate the tangent support calculation | **The requested distinction is supplied.** The relative law now organizes the article; the tangent restriction is stated adjacent to the testing theorem. Exceptional significance remains a separate editorial assessment, not an unrepaired missing hypothesis. |
| S-R3/C-R3: one canonical submission and one conceptual introduction | **Substantially closed.** The active main file has one introduction and a proof-oriented main sequence, with secondary material in appendices. The existence of retained version directories in source control is not itself an exposition defect. |
| S-R4/C-R4: source-specific build and diagnostic evidence | **Author evidence supplied; not independently reproduced here.** The manifest identifies the exact source, build commands, PDF hashes, diagnostics, and limitations. My lack of a separate rebuild is not evidence that this build failed. |

The report does not reopen the old distinctions between actual and effective curvatures, independent and physically constrained area, one-flight and long-flight information, selected channels and all channels, or constant-confidence and high-confidence lower bounds. Those distinctions remain necessary, but v8 generally observes them.

## 3. Audit of the nonlinear analytical chain

### 3.1 Geometry, quadratic reduction, and the relative quantity

**Locators:** `v3/10_geometry_action.tex`, `lem:g-channels`, `lem:g-jacobi`, `lem:g-relative` [S5].

The localization argument is genuinely local about an arbitrary separated positively curved periodic configuration. It does not require a global finite-horizon bound. Finiteness of the relevant lifted pairs, uniqueness of the closest segments, positive clearance, and separation of the near-normal outgoing states are used in the correct order. The total-excess estimate makes every complete flight short; reflection then forces reversal in one fixed channel neighborhood without introducing a length-dependent localization step.

For unequal facing curvatures, the two-periodic scaling is essential. With $c_b=1+g\kappa_b$, $c=\sqrt{c_0c_1}$, and $\gamma=\operatorname{arcosh}c$, the printed Schur complement separates a uniformly positive endpoint Hessian from an exponentially small mixed derivative. The determinant identity

$$
\frac{-W_{uv}(0,0)}{\sqrt{\det H_j}}=\operatorname{csch}(j\gamma)
$$

is consistent with both parities, including the one-flight case. The independent checks eliminate the finite tridiagonal Hessian directly for equal and genuinely unequal contacts, rather than merely substituting equal curvatures into the final formula.

The nonlinear contraction is performed in endpoint-weighted spaces. Its derivatives retain localization, and the sum of the relevant powers of the weights stays bounded independently of the number of sites. The cofactor identity

$$
-W_{uv}=\frac{\prod_i[-\ell_{i,uv}]}{\det H_{\mathrm{int}}}
$$

is then normalized before comparison. This is the correct relative quantity. An absolute stationary-action remainder would not justify the subsequent relative flux estimate.

### 3.2 Half-line limits and differentiated determinants

**Locators:** `v4/10_boundary_layers.tex`, `lem:v4-halfline`, `thm:v4-factorization`; `v5/15_differentiated_operators.tex` [S6].

The half-line action and amplitude are explicitly normalized. In particular, the determinant in the amplitude is defined by its trace expansion, so there is no unspecified infinite-determinant constant. The perturbation is trace class because it is tridiagonal and localized at the boundary; this is stronger than a small operator-norm assertion.

The finite-to-half-line comparison keeps two separated boundary blocks, controls the discarded entries in trace norm, compares the compressed Green kernels, and then uses the direct-sum determinant. The proof has enough exponential slack to absorb every fixed polynomial derivative loss. The statement uses constants depending on derivative order; it does not assert a bound uniform in that order.

The differentiated-operator addendum correctly says that derivatives of $G\Delta H$ need not be small. In a differentiated trace product, only the undifferentiated factors supply the geometric power; one factor supplies the trace norm. The finitely many short products are harmless. This closes a common dimension-loss trap rather than concealing it under a formal differentiation symbol.

I do not find a fatal defect in this argument on its printed local compact families. I also do not infer that the construction treats arbitrary itineraries or degenerating curvature/gap families: it treats the stated alternating local channels with uniform positive margins.

### 3.3 Physical integration and the common observation space

**Locators:** `v3/20_integration.tex`, `lem:g-radial`; `v4/10_boundary_layers.tex`, `thm:v4-law`; `v6/10_experiment_transfer.tex`, `thm:v6-transfer` [S7].

The phase measure and residual-time interval are not replaced by an artificial endpoint ensemble. The lower roof bound prevents truncation of the residual interval in the chosen collar, even though an upper roof bound is not assumed. The Morse map uses the positive endpoint Hessian, not the small mixed derivative, as its inverse bound. Integration over a fixed disk explains the smooth right extension in offset and its differentiated estimates.

For total variation, the decisive fact is that the finite and limiting residual fibers start at the same zero endpoint. Their symmetric-difference length is controlled by the action difference. Its quadratic vanishing cancels the scaling by $d$, giving a bound uniform down to onset. Normalization gives the conditional bound; restoring failures gives the additional physical rare-event factor. Neither step produces total variation for two different embedded full collision arrays.

The manuscript also distinguishes parameter-dependent proof coordinates from supplied knowledge of the unknown gap. The comparison in physical coordinates is between the stated statistical families; it is not an unknown-table simulation algorithm. These qualifications are mathematically necessary and are actually present.

## 4. Audit of the new inverse and statistical results

### 4.1 Analytic descent through the discriminant

**Locator:** `article/40_fixed_offset.tex`, `lem:v8-descent` [S2].

This is the correct missing ingredient for a finite-offset inverse at coalescence. Smoothness in labelled radii would not justify differentiation in elementary symmetric coefficients at a triple root.

The proof supplies more: analytic stationary action and an analytic Morse inverse on a smaller common complex neighborhood; normally convergent fixed-domain integration; cancellation of odd endpoint degrees; and full permutation invariance. The latter is justified by the rotation and reflection of the triangular physical support family, not assumed merely because leading amplitudes are symmetric. The support-family formula was checked directly [S8].

Off the discriminant, local root branches give a holomorphic function of coefficients. Symmetry makes it single valued, while boundedness as the roots approach each other permits extension across the discriminant, jointly with the other parameters. The identification at zero offset then gives

$$
F_j(g,e,d)=C_j(g,e)+dB_j(g,e,d)
$$

on a full coefficient neighborhood. This analytic extension is not a claim that physical probabilities are nonzero below onset. The common exact gap of all six channels is important: the argument would not automatically survive moving activation interfaces in a different family.

### 4.2 The exact unknown-gap four-window inverse

**Locators:** `thm:v8-four`, `cor:v8-fixed-sampling`; `v6/30_three_amplitudes.tex`, `eq:v6-three-determinant` [S2, S9].

The four windows are programmed at known times; they are not programmed using the unknown gap. The two first-flight windows separate timing from the first amplitude. Subtracting their Jacobian rows and scaling the gap column by $a$ yields the printed block limit with determinant $C_1\det D$.

I independently recomputed all twelve entries $\Phi_j^{(k)}(1/4)$, $j=1,2,3$, $k=0,1,2,3$, from the elementary hyperbolic-sine formulas. Incorporating the physical area constraint gives exactly

$$
\det D=-\frac{2\sqrt2(15804720A_c+64253\pi)}{72930375A_c^4},
\qquad A_c=\frac{\sqrt3}{2}-\frac\pi{16}.
$$

The nondegeneracy argument consequently applies to the **exact** finite-offset map after fixing one sufficiently small positive $a$. It is not an inversion of leading means masquerading as an exact experiment. The inverse-function theorem is applied before restriction to the real-rooted physical locus, and the subsequent compact-fit and root-matching steps do not exclude repeated roots.

There are important limits, but they are not hidden errors. The local set and conditioning constants depend on the chosen fixed window size. The result does not promise an efficient method to evaluate nonlinear probabilities or solve the compact fit. Its known physical family supplies substantial information about the shape and the area relation. It is not an inverse theorem for an arbitrary unknown smooth scatterer.

### 4.3 Preparation cost, moving support, and stopping

**Locator:** `article/50_joint_minimax.tex`, `lem:v8-gap-entropy`, `thm:v8-joint-minimax`, `cor:v8-comparison` [S3].

The four Bernoulli sample means, together with the Lipschitz coefficient inverse and the cube-root matching bound, give the stated deterministic upper cost. The Borel minimizing selection is specified on every outcome, including data outside the inverse chart [S12]. There is no requirement that a minimizer be unique.

The timing lower bound uses the correct entropy direction. If $d=t-jg_c$ and $z=j\Delta$, then the higher-gap law has probability $(d-z)_+^2H_j(g_c+\Delta,(d-z)_+)$. When the lower-gap probability vanishes, the higher-gap probability vanishes as well. For positive $d$, the estimates

$$
|p_\Delta-p_0|\le Cd\Delta,\qquad p_0\ge cd^2
$$

yield $D_{\mathrm{KL}}(\operatorname{Ber}(p_\Delta)\Vert\operatorname{Ber}(p_0))\le C\Delta^2$. The proof does not need an unsupported monotonicity assertion for the smooth amplitude, and does not take entropy in the direction with a support problem.

For curvature, the full finite-offset probability, not only its leading term, has cubic indistinguishability under the two physical splitting alternatives. Rotation invariance kills the linear differential and Taylor expansion cancels the even terms [S10]. Conditioning on a common recorded history leaves the same next query and stop decision under both hypotheses. Padding stopped histories and taking the entropy limit therefore justifies random stopping. Binary data processing supplies the confidence logarithm.

The two lower bounds use different physical alternatives. Combining them by a maximum, and then using $\max(u,v)\ge(u+v)/2$, correctly gives the sum order. There is no need to exhibit one pair simultaneously hardest for both losses.

Accordingly,

$$
\mathcal N_K(\varepsilon,\delta,\eta)
\asymp(\varepsilon^{-6}+\delta^{-2})\log(1/\eta)
$$

is supported for the printed exact-family, bounded-flight, local **binary** experiment. It is not a lower bound for complete collision counts, impact positions, unlimited flight orders, or unrestricted observation times. The all-history design condition is not removable from the statement merely because the proof is adaptive.

The finer timing target $\delta=\varepsilon^{3+3/m}$ really does restore order $\varepsilon^{-(6+6/m)}$ even in the wider fixed-collar exact-family class. The earlier shrinking-design rate is therefore neither disproved nor the curvature-only optimum of this wider experiment.

### 4.4 Unknown smooth remainders

**Locator:** `article/60_smooth_remainders.tex`, `thm:v8-nuisance` [S4].

The nuisance model is now explicit. It preserves only the physical leading map and bounded positive $C^m$ remainders; it does not pretend that arbitrary triples of those functions are realized by one billiard table.

The deterministic-budget proof avoids the failed-search infinite-wait problem. On bracket success, Bernoulli probabilities at the pilot and final windows are comparable to $h^2$, so sample size $h^{-(2m+2)}\log(C/\eta)$ is sufficient for relative error of order $h^m$. The square-root pilot uses a degree-$(m-1)$ Taylor polynomial of $\sqrt{H_1}$ multiplied by the offset. This explains why $C^m$, rather than an unmentioned $C^{m+1}$ assumption, suffices for the claimed $h^{m+1}$ root error. The polynomial comparison does not require a physical observation below onset.

The final normalization charges the timing error as $O(|\widehat g-g|/h)$; it is not canceled by the extrapolation weights. The supplied all-history bounds on the programmed times keep queries in the envelope after a failed search as well. The finite-stage deterministic budgets then control the cost on those histories.

The proof explicitly retains the pilot gap estimate while obtaining the other coordinates from a compact fit. Those two outputs need not belong to the same fitted physical parameter. This is allowed by the componentwise loss stated here; it should not be described as a reconstruction algorithm returning one exactly consistent billiard table without an additional argument.

The paper states only an upper bound for this envelope. That is not a defect. Section 5 supplies a matching comparison under a precise additional interior condition on the chosen envelope constants.

### 4.5 The supercritical extension and contact-rigidity scope

**Locators:** `article/30_supercritical.tex`, `thm:v8-supercritical`; `v7/10_critical_experiments.tex`; `v5/20_contact_rigidity.tex`, `thm:v5-jets`, `cor:v5-analytic-rigidity` [S11, S13].

The common whitening works for unequal contacts and both parities. Equal densities on the quadratic overlap give exactly the product of common masses and the erasure equivalence. The reverse erasure kernel is for the known simple pair, not a universal unknown-geometry kernel. The independent quadrature checks agree with $2\arcsin(e^{-j\gamma})/\pi$.

The v8 projection proof is valid: in the supercritical regime, a finite critical subsample is enough for a lower bound, so the full sample's accumulated tangent error need not vanish. Compactly varying geometries do not invalidate the argument because the estimates and the positive lower bound on $\gamma$ are uniform. The theorem remains asymptotically tangent under $\omega(d_j)/q_j\to0$; it does not identify the sharp nonlinear fixed-positive-offset rate.

The inspected contact-jet inverse has a nonzero triangular diagonal and explicitly assumes identical even facing graphs. Its analytic continuation concerns the participating connected analytic boundaries in their contact frames. It does not recover the lattice and other obstacles, and is not a noise-stable continuation statement. I do not elevate this limited inspection into a new audit of every realization and finite-jet appendix. The general forward theorem does not acquire the identical-even restriction from this separate application.

## 5. A stronger exact-family versus smooth-envelope comparison

The companion `SMOOTH_ENVELOPE_MINIMAX.md` gives a complete lower-bound construction and derives a joint order from the manuscript's upper theorem. Its assumption is that the constant functions with values $C_j(g_c,0)$ lie strictly inside the stated positivity and $C^m$ norm bounds. This is a natural choice of a nondegenerate envelope, but it is an additional condition and must be stated.

Take the physical leading parameters at $\beta=\pm s$, with the same gap, and denote the three leading amplitudes by $C_j^\pm$. They satisfy $C_j^+-C_j^-=O(s^3)$ and the curvature targets are separated by order $|s|$. Let $h=L|s|^{3/m}$ and let $\psi$ be a fixed $C^m$ cutoff with $\psi(0)=1$ and $\psi=0$ for arguments at least one. Set

$$
H_j^\pm(d)=\frac{C_j^++C_j^-}{2}
\;\pm\;\frac{C_j^+-C_j^-}{2}\psi(d/h).
$$

For fixed sufficiently large $L$ and small $s$, these are admissible functions in one fixed envelope. Their probability difference is supported in $0<d<h$. Each query has entropy at most $Ch^2s^6=C|s|^{6+6/m}$; outside that interval it has zero entropy. The stopped-history and high-confidence arguments therefore give the curvature lower order $\varepsilon^{-(6+6/m)}\log(1/\eta)$ without forcing the policy to use shrinking windows. A separate constant-nuisance gap pair gives $\delta^{-2}\log(1/\eta)$.

Choosing $h$ in the manuscript's upper theorem as a sufficiently small constant times $\min\{\varepsilon^{3/m},\delta^{1/(m+1)}\}$ matches both losses. Thus, for the declared three-indicator envelope and strict-slack bounds,

| Information supplied | Joint preparation order |
|---|---|
| Exact analytic physical probability family | $(\varepsilon^{-6}+\delta^{-2})\log(1/\eta)$ |
| Unknown positive $C^m$ remainder functions with the same leading inverse | $(\varepsilon^{-(6+6/m)}+\delta^{-2})\log(1/\eta)$ |

Moreover, at any finite set of fixed positive offsets, choose $s$ so that $h$ is below the smallest offset. The two envelope laws at all those windows then agree exactly, although their curvature targets differ. This is a direct nonidentifiability obstruction for a finite fixed-window envelope experiment, not merely a slower convergence calculation.

These nuisance alternatives are not asserted to be exact billiard probabilities. The conclusion does not contradict the physical fixed-window theorem and must not be advertised as a stronger physical-family lower bound. It explains, positively and quantitatively, why v8's distinction between the two information models is substantive. It also shows why their costs coincide at the manuscript's finer joint timing target.

This addition is offered as a useful strengthening, not as a retroactive claim that an upper-bound theorem was incorrect for omitting a lower bound, and not as an independently established publication-priority claim.

## 6. The remaining adverse venue assessment

### V8-R1 — Major editorial issue: establish the importance of the existing nonlinear theorem with a sharper predecessor comparison

The paper now identifies its strongest theorem. That is a substantial improvement, but identifying the theorem and proving that its observable differs from another observable are not sufficient for my top-four recommendation.

The analytic core combines exponential localization of a hyperbolic boundary-value problem, a tridiagonal cofactor identity, summable boundary perturbations, a two-block relative determinant comparison, and a uniform Morse integral. The resulting **relative physical law** is not supplied by an absolute action estimate, and I do not claim that one of the cited papers already contains it. At the same time, the manuscript has not yet made a sufficiently sharp case for why the completed construction is a major advance rather than a valuable, specialized synthesis of these mechanisms.

The closest operator ingredients deserve a proposition-level comparison, not only a comparison with inverse problems based on very different data. For example, Hill identities concern the action-Hessian/monodromy relation [L1], while exponential decay for tridiagonal and banded inverses is a pre-existing operator theme [L6]. Neither citation by itself proves the present nonlinear relative probability theorem. The point is to isolate exactly what the existing mechanisms give after normalization, and what indispensable estimate or consequence is newly achieved here.

This request does **not** impose global billiard rigidity, arbitrary-itinerary control, a sharp fixed-offset exponent, or a new higher-dimensional theory as moving acceptance conditions. A compelling theorem-level priority and consequence comparison could improve the assessment without adding any of those results. Conversely, simply repeating that an absolute action error cannot be divided by a small twist does not by itself settle the importance of the completed relative construction.

The finite-flight statistical result is now a sound, interesting parametric singular-inversion theorem. But it uses an explicitly designed analytic support family and only flight numbers one, two, and three. Its cube-root matching loss and cubic testing pair explain the sixth power; the gap term is a regular timing obstruction. Those results do not depend on the long-bridge factorization in the same way that the boundary experiment does. Their addition cannot automatically serve as a deep application of the long-bridge theorem. The source already acknowledges the finite-flight scope, so this is a significance assessment, not an allegation of a logical falsehood.

The smooth-envelope comparison strengthens the statistical story, including through the companion to this report. Its cutoff and entropy mechanism is nevertheless a local statistical construction, not evidence of a newly resolved global geometric inverse problem. The manuscript must be judged on what these particular results accomplish together, not on the number of theorem labels or the number of revision rounds.

### Other matters — presentation refinements, not correctness blockers

The active organization is substantially improved. I do not request deletion of proofs or a reduction of mathematical scope. A more concise dependency map would still help readers see that the general forward law, identical-even contact inverse, and finite-dimensional unlabelled count inverse have different hypotheses and different uses of long bridges. The present source already makes these distinctions in prose.

The four-window theorem is a statistical existence result with fixed, possibly poorly conditioned design constants. Its current computational disclaimer should remain. Similarly, the smooth-envelope estimator's separately retained timing output should not silently be re-described as one consistent fitted table.

The companion lower bound may be incorporated, checked independently, or omitted while retaining the present honest upper-bound wording. Its omission is not a rejection ground. An incorporation must preserve the interior-slack condition and the non-geometric status of the nuisance alternatives.

## 7. Literature boundaries

The primary records listed below were checked online for the comparisons used in this report. I did not re-prove their results or conduct an exhaustive search of every possible predecessor.

Bolotin–Treschev supply action-Hessian/monodromy identities for discrete and continuous Lagrangian systems [L1]. Zelditch uses localized wave-trace invariants and specified analytic symmetry classes [L2]. De Simoi–Kaloshin–Leguil obtain marked-length determination under symmetry and genericity assumptions in analytic open billiards [L3]. Finamore–Leguil use an enriched marked length datum for finite-horizon Sinai billiards [L4]. Batenkov–Yomdin study local accuracy of confluent Prony systems [L5]. Nabben discusses inverse structure and decay for tridiagonal and banded matrices [L6].

These are comparisons of observations, hypotheses, and mechanisms. None is cited as a proof that the submitted relative probability theorem is already known. Equally, the fact that the observable is different is not by itself proof of exceptional significance. The distinction between exact local analytic continuation and global rigidity from different data must remain explicit.

## 8. Independent verification and its limits

The accompanying `verify_review.py` was executed normally and under `python -O`; the JSON outputs were byte-identical. **211 checks passed: 148 exact-algebra checks and 63 ordinary high-precision checks.** The latter use 60-decimal mpmath arithmetic and are not interval enclosures.

The checks include independently differentiated amplitudes, the constrained physical determinant, the limiting four-window block, the support-family area and permutation identities, finite Schur complements and Green matrices with both parities and unequal contacts, cofactor and whitening determinants, extrapolation moments, cutoff splice regularity, error-exponent balances, disk/ellipse overlap quadrature, and illustrative likelihood inequalities for the constructed nuisance laws.

These are finite diagnostics, not a nonlinear billiard probability solver or a proof of the infinite-dimensional estimates. The nuisance likelihood diagnostics use the explicitly constructed envelope probabilities, not an exact finite-offset physical probability oracle. No author diagnostic script was executed in this review, and the author's 249/134-check records are not counted as independently reproduced checks.

The author reports a clean 79-page main build and a 7-page companion build, resolved references, no overfull boxes, disclosed ordinary notices, and visual inspection [S14]. Those remain **author-reported evidence** here. The manuscript source was inspected through the connector, but no independent TeX build, PDF rendering, visual inspection, interval certification, or remote CI rerun was performed. The preservation assertion of 130 retained formal environments was not independently recomputed. These limitations delimit this review; they are not invented mathematical counterexamples or independent grounds for rejection.

`VERIFICATION.json` records source pins, executed commands, environment, output hashes, coverage, and exclusions. The script regenerates the full per-check JSON result. The new mathematical comparison is established by its written proof, not by the finite tests.

## 9. Stable source and literature references

All manuscript links below are frozen at the reviewed commit.

- [S1 — Author response and resolution of the two v7 reports](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/RESPONSE_TO_REFEREES.md).
- [S2 — Exact fixed-offset inverse](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/article/40_fixed_offset.tex).
- [S3 — Joint minimax experiment](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/article/50_joint_minimax.tex).
- [S4 — Smooth remainder envelope](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/article/60_smooth_remainders.tex).
- [S5 — Geometry, Jacobi reduction, relative cofactor](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v3/10_geometry_action.tex).
- [S6 — Half-line and two-boundary proofs](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v4/10_boundary_layers.tex); [differentiated operator addendum](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v5/15_differentiated_operators.tex).
- [S7 — Physical integration](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v3/20_integration.tex); [experiment transfer](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v6/10_experiment_transfer.tex).
- [S8 — Physical support family](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v3/40_inverse.tex).
- [S9 — Three-amplitude determinant](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v6/30_three_amplitudes.tex).
- [S10 — Physical cubic testing and stopping](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v7/30_count_lower_bounds.tex).
- [S11 — Supercritical projection](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/article/30_supercritical.tex); [critical experiment proof](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v7/10_critical_experiments.tex).
- [S12 — Measurable selection](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v7/20_measurable_reconstruction.tex).
- [S13 — Contact jets and analytic continuation](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/v5/20_contact_rigidity.tex).
- [S14 — Author verification manifest](https://github.com/TrillionniumFoundation/theta-theory/blob/9345433799379d23993a038e213e62b6b0c16e34/papers/A2-v8-relative-boundary-fixed-offset/VERIFICATION.json).
- [L1 — Bolotin and Treschev, *Hill's formula*, arXiv:1006.1532](https://arxiv.org/abs/1006.1532).
- [L2 — Zelditch, *Inverse spectral problem for analytic domains, II*, Annals of Mathematics 170 (2009), 205–269](https://annals.math.princeton.edu/2009/170-1/p06).
- [L3 — De Simoi, Kaloshin and Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, Inventiones Mathematicae 233 (2023), 829–901, author-institution record](https://research-explorer.ista.ac.at/record/12877).
- [L4 — Finamore and Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*, arXiv:2510.18983](https://arxiv.org/abs/2510.18983).
- [L5 — Batenkov and Yomdin, *On the Accuracy of Solving Confluent Prony Systems*, DOI 10.1137/110836584](https://epubs.siam.org/doi/10.1137/110836584).
- [L6 — Nabben, *Decay Rates of the Inverse of Nonsymmetric Tridiagonal and Band Matrices*, DOI 10.1137/S0895479897317259](https://doi.org/10.1137/S0895479897317259).

## Final assessment

V8 is a real mathematical improvement, not merely a new title attached to the old proof gaps. Its strongest new statistical assertions withstand the targeted audit. The explicit smooth-envelope comparison can be strengthened further by the accompanying proof. My adverse venue recommendation is therefore restricted to the significance assessment explained above. It is not a no-go theorem for the research program, an instruction to discard valid results, or a claim that repeated revisions can never reach the intended standard.
