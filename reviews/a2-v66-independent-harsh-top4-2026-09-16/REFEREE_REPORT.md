# Independent referee report on A2, revision 66

**Manuscript:** *Boundary laws and rigidity of periodic dispersing billiards*  
**Author:** Qian Qi  
**Review date:** September 16, 2026  
**Requested standard:** Annals of Mathematics / Inventiones Mathematicae / Acta Mathematica / Journal of the American Mathematical Society.

This is an author-requested, AI-assisted external-referee-style assessment. It is not commissioned by any journal, is not an editorial decision, and is not a formal proof certificate. Mathematical correctness, originality, significance, presentation, and mechanical reproduction are assessed separately.

## 1. Recommendation and frozen submission

**Recommendation: do not accept at the requested highest general-journal level on the present exceptional-significance case.** The new global positive-curvature inverse and exact marked identification are substantive improvements and withstand the scoped examination below. I establish no fatal error in Theorems 10.2 or 10.3. There is **one minor quantitative clarification/correction** to the finite-iteration sentence following Proposition 10.4: the curvature iteration error must be propagated through the finite higher-jet inverse, not added to the full jet error with an implicit coefficient one. The proposition with the exact fixed point is unaffected. See R66-m1 for an explicit control and the required bound.

The absence of a closeness assumption is genuinely new relative to the previous formulation. It is no longer accurate to describe exact marked contact identification as depending on selection of a local curvature branch. Conversely, this global exact statement is not a global same-disc analytic stability theorem, an unknown-polygon reconstruction, or a general-period preparation-budget theorem. The manuscript makes these distinctions. The placement assessment in Section 6 credits the stronger result rather than automatically repeating the v65 recommendation.

| Object | Immutable identity |
|---|---|
| Actual compiled mathematical source | `38f798a9b28237420f070a032d3601f0bee72cde` |
| Reconstructed manuscript subtree | `c693d717577dc5f501f2a86ec937cfa36bf6ce4e` |
| Source branch | `revision/a2-v66-referee-response-2026-09-16` |
| Native-products branch | `revision/a2-v66-native-products-35063645908-1` |
| Products head used as review parent | `c11a0427289f88c4c83e3932bd28569ae2c00db8` |
| Native workflow / attempt / artifact | `35063645908` / `1` / `10433187185` |
| Preceding v65 report | `7f4603531f7b97a23ce627fec47b7ddc5f4f9912` |
| Source reviewed in that report | `06a197e4d11bc3d4193e9f0b7904105df35875fa` |

All manuscript sources below lie under `papers/A2-v17-boundary-information-coarsening/`; that directory name is historical. The principal article has **149 pages**, the full technical manuscript **324 pages**, and the companion **seven pages**. Page references below are to the principal article. The discovery snapshot listed source and native-products branches, not a separately named v66 review-ready branch. The source-to-products comparison has two delivery commits and changes no compiled mathematical input. The new module's Git blob, read directly at the compiled commit, is `4ea7cca000a98ea7ac6d48bd9d4f12e5becb94a9`, matching the archive. [D1]

### Coverage and exclusions

The complete 313-line new module `article/10c_global_curvature_inverse_v66.tex` was read and analyzed, including all four statements and proofs. The new common abstract and introductory synthesis, revised opening, response, cover-letter argument, historical audit, and dependency ledger were checked. The audit directly revisits the inherited graph Hessian, two-offset extraction, actual smooth envelope, signed jet recursion, and relevant physical/relative normalization interface. It also checks how the global exact result is separated from the retained local analytic norm theorem. [S1–S6, R1–R2]

This is **not** a fresh line-by-line verification of all 480 pages. The entire earlier finite-chain/full-phase construction, every detail of the retained Banach inverse and conditional continuation theorem, all unregistered global matching/lattice and moving-family arguments, the full statistical/calibration catalogue, and the companion's mathematics are not freshly certified. The complete old periodic-forward, periodic-inverse, finite-experiment, and position-pilot files were separately verified byte-identical. That establishes retention, not fresh certification of their contents. Mechanical comparison of every page has a different scope from proof review.

## 2. Disposition of the preceding report

| v65 point | v66 disposition |
|---|---|
| The new general-period result is a genuine marked inverse, not forward only | Retained. |
| Degree-two curvature inversion previously only local | **Strengthened.** Theorem 10.2 gives global injectivity and an image characterization; Theorem 10.3 removes the candidate-closeness condition from exact identification. |
| Complete analytic inversion requires more than graded block invertibility | Retained. Global coefficient uniqueness is expressly not substituted for the local full-operator proof. |
| Supplied polygon, signed phases, and common amplitudes across two offsets | Retained and visible beside the new leading theorem. |
| Fixed lattice/full visitation versus unknown-lattice recovery | Retained as different observation models. |
| R65-E2: mechanism-led synthesis rather than a catalogue of strongest claims | Materially improved by the common opening and explicit discussion of three observation models. |
| Exceptional significance | Reassessed below; neither correction of wording nor a successful native build settles it. |

The earlier report supplied a Riccati differential cross-check, not a proof of the present global inverse. The new text appropriately attributes that antecedent and then supplies its own nonlinear inverse argument. No prior mathematical defect is being repaired merely by proving a stronger exact theorem. Previously closed pilot-grid and physical-gauge points remain closed. [R1–R2, D1]

## 3. The global quadratic inverse

### R66-M1. The Schur identity has the correct endpoint multiplicities and an actual converse

Lemma 10.1, p. 45, uses the normalized graph curvature $c_i=F_i''(0)$, not the physical curvature without its incidence factor. The latter is $\kappa_i=\nu_i c_i$. With fixed $k_i=L_i^{-1}$, adjoining the first edge to the next future tail gives the quadratic form

$$\frac12(k_i+c_i)u^2-\epsilon_i k_iuy
  +\frac12(k_i+c_{i+1}+s_{i+1})y^2.$$

The initial contact contributes its curvature once. At the next contact the first edge and the remaining half-line supply the appropriate combined contribution; inserting $2c_i$ at the initial boundary would be incorrect. Elimination gives

$$s_i=k_i+c_i-\frac{k_i^2}{k_i+c_{i+1}+s_{i+1}},\qquad
 a_i=\frac{k_i}{k_i+c_{i+1}+s_{i+1}}.$$

Since the actual next action Hessian and curvature are positive, $0<a_i<1$ and $c_i<s_i<c_i+k_i$. The signed ratio is $\epsilon_i a_i$; squaring the mixed entry is why the signs do not appear in this particular degree-two identity. [S1, lines 23–64; S3, lines 1–148]

The converse is important and is present. It is not enough to select an algebraic Riccati solution. Substitution yields

$$\frac{k_i}{a_i}=k_i+k_{i+1}+2c_{i+1}-k_{i+1}a_{i+1}.$$

The products of successive $a_i$ therefore solve the sign-conjugated Jacobi equation. With finitely many phases their uniform maximum is below one, so the solution decays. The difference from the physical linearized half-line has zero boundary value and vanishing tails; coercivity of the positive Jacobi quadratic form forces that difference to be zero. Restoring the signs then recovers the actual half-line and its boundary Hessian. This closes the formal-versus-physical direction used in the image theorem.

Independent exact controls use 56 positive periodic Jacobi data sets, with periods two through eight. They verify the Schur identities, contraction ratios, and finite-chain eliminations. These scalar configurations are not claimed to be global billiard tables. The general converse rests on the preceding argument, not on the sample. [D2]

### R66-M2. The projected contraction is global on its declared data domain, not surjectivity onto all positive action data

Theorem 10.2, pp. 45–46, defines

$$ (\Phi_s z)_i=\left[s_i-k_i+
       \frac{k_i^2}{k_i+s_{i+1}+z_{i+1}}\right]_+,\qquad q(s)=\max_i\left(\frac{k_i}{k_i+s_{i+1}}\right)^2<1.$$

For every $s>0$ this maps the complete closed orthant into $\prod_i[0,s_i]$. Its untruncated derivative in the next coordinate is negative with magnitude at most $q(s)$; positive part is one-Lipschitz. Thus contraction applies from any nonnegative starting vector, not merely one already near the unknown curvature. Summing the successive differences proves equation (10.3), including $m=0$. [S1, lines 66–150]

A positive actual curvature vector is a fixed point, and hence is the unique fixed point. Conversely, a strictly positive fixed point makes the truncation inactive and satisfies the untruncated Schur equation. Lemma 10.1 then identifies it with actual quadratic action data. The resulting equivalence

$$s\in\mathcal R_k((0,\infty)^r)\quad\Longleftrightarrow\quad z_i(s)>0\text{ for all }i$$

is valid. Positivity of the observed $s$ alone is not sufficient. The manuscript's control $k=(1,1)$, $s=(1/10,10)$ indeed gives $z=(0,109/11)$; the first untruncated component at that fixed point is $-98/115$. Clipping has not produced an admissible strictly positive-curvature inverse. Nor is the extension outside the image asserted to be an inverse for zero-curvature tables. [S1, lines 186–195; D2]

Contraction is also not monotone iteration. For $k=(1,1)$, $s=(3/4,3/4)$, the fixed point is $(1/4,1/4)$, while the first two scalar iterates from zero are $9/28$ and $27/116$, on opposite sides of $1/4$. No monotonicity is claimed by the source. This control explains why the error certificate, rather than an informal one-sided bound from successive iterates, matters.

The stated image is the image of the **local contact quadratic map**. The proof does not show that every arbitrary curvature tuple extends to a collection of prescribed globally disjoint closed analytic obstacles. Global table existence is not silently inferred from a fixed point. The later whole-table theorem compares actual tables, which is the appropriate formulation.

### R66-M3. Global analyticity and data-dependent stability follow without a hidden branch selection

For positive $s,\widetilde s$, use

$$q_* =\max_i\left(\frac{k_i}{k_i+\min(s_{i+1},\widetilde s_{i+1})}\right)^2<1.$$

Changing the two action-data occurrences costs $(1+q_*)\|s-\widetilde s\|_\infty$, and changing the unknown fixed point costs $q_*\|z-\widetilde z\|_\infty$. Moving the last term to the left proves the printed two-point inequality. The argument includes clipped data outside the image. It needs the action-Hessian floor embodied in $q_*$; it gives no uniform bound as that floor disappears. [S1, lines 125–150]

At a strictly positive fixed point the clipping can be removed on a neighborhood. Differentiating the Schur equation gives

$$ (I-T_2)\,ds=(I+T_2)\,dc,\qquad (T_2v)_i=a_i^2v_{i+1}.$$

Both factors have convergent Neumann inverses. Analyticity of the forward quadratic map follows from the locally uniformly invertible periodic half-line operator; equivalently, it is a boundary matrix element of its analytic resolvent. Thus the forward map is a local real analytic diffeomorphism at every positive curvature, its image is open, and global injectivity joins the local inverses into one analytic inverse on that image. No assertion of convexity of the image is needed.

There is a short independent uniqueness argument which deserves to remain visible. Equal action data imply

$$c_i-\widetilde c_i=-a_i\widetilde a_i(c_{i+1}-\widetilde c_{i+1}).$$

Going around the cycle gives a multiplier whose absolute value is strictly below one. The difference must vanish for both odd and even physical periods. This is a genuine nonlinear equal-data argument, unlike merely knowing that the Jacobian is nonsingular everywhere. [S1, lines 161–170]

The normal two-site formulas also agree with the retained alternating result when their recovered curvatures are positive. The nonimage example prevents extending that agreement to an assertion that arbitrary positive Hessians give positive physical curvatures. Eight 70-digit numerical cases and three two-site specializations provide additional algebraic controls; they are not proofs of the analytic assertions. [D2]

## 4. Identification, finite flights, and a minor stopping-error correction

### R66-M4. Global finite-jet identification is not a local inverse-function argument repeated at each candidate

Theorem 10.3, pp. 47–48, first determines curvature globally. The polygon fixes the remaining first-order geometry and signs. The reconstructed curvature then fixes the actual one-step factors. At order $n\ge3$ the inherited relation is

$$q_n=(I-T_n)(I+T_n)^{-1}
       \{s_n-\mathcal R_n(q_2,\ldots,q_{n-1})\},\qquad (T_nz)_i=\sigma_i^n z_{i+1}.$$

Invertibility at every degree determines the next coefficient uniquely once lower coefficients agree. Crucially, the remainder is a function of actual smooth jets. The retained stationary-envelope argument proves this by interpolating local representatives with equal lower jets, estimating their action difference, and disposing of the terminal term only after its decay is proved. It does not identify arbitrary formal generating functions. Global interpolation of closed obstacles is unnecessary for this local finite-jet conclusion. [S1, lines 199–256; S3, lines 208–346]

The degree-two signs cancel, but the higher odd-degree signs do not. Orientation doubling therefore cannot erase the signed physical contact cycle. The new proof uses the unchanged signed recursion rather than a positive-only surrogate.

For analytic candidates, equality of all graph coefficients implies equality on some common smaller neighborhood, even when their original analytic radii or norms differ substantially. No common local inverse ball is required for this exact conclusion. For smooth candidates the theorem concludes equality of jets, not equality of germs from flatness. Those are the correct distinctions.

The finite-jet inverse is smooth on its image: the quadratic inverse is globally defined there, and each of the finitely many remaining steps is a smooth operation with an invertible signed block. This does not give a uniform infinite-order operator bound. The complete local analytic inverse remains a separate theorem, as the manuscript expressly states.

### R66-M5. Whole-obstacle identity removes closeness, not the supplied lattice or visitation

For actual connected closed embedded analytic boundaries, the recovered germ provides a common open arc at every visited obstacle. At a limiting point of a common arc the tangents agree. Both curves are graphs over that tangent on a small neighborhood; analytic identity continues the coincidence across the limiting point. Compactness and connectedness continue it around the boundary. Fixed labels and lattice then identify the entire table, provided every obstacle is visited. [S1, lines 228–256]

This is an exact whole-image statement without candidate closeness. It should not be dismissed as merely local equality. It is equally not an unknown-lattice or unmarked matching theorem: placement and coverage are assumptions. The manuscript's new opening now puts this distinction next to Theorem 1.1, rather than relying on a distant qualification.

### R66-M6. The finite-flight proposition has a sound exact-fixed-point argument

Proposition 10.4, p. 48, starts from finite-flight densities and compares them with realizable limiting densities in an interior $C^M$ norm. Only then are the stable two-offset rational formulas used. Finite bridges are not assumed to obey exact limiting factorization. The known momenta are restored, and removal of constant and linear Taylor terms is a bounded projection fixing the true gauged action. [S1, lines 270–313; S3, lines 150–202]

On the compact positive class the true action Hessians and curvatures have positive floors. Sufficiently small $C^M$ error, with $M\ge2$, keeps the estimated Hessians positive. The global two-point estimate puts the reconstructed fixed point close to the true curvature and therefore inside the strictly positive image. At each of the finitely many later orders, smoothness and compactness control the block and lower-jet remainder. This proves the stated $C_M(\tau^N+\varepsilon)$ bound with the exact fixed point.

The relative density input is substantive. The inherited proof cancels the exponentially small reference twist in an exact cofactor identity before taking the two-ended trace-class limit. It uses entrywise summability of localized Hessian perturbations, reflected Green estimates and trace-series telescoping, rather than dividing a crude absolute action error by a rare-event mass. The new Schur contraction is an inverse step after that input, not a replacement proof of it. [S4, lines 186–359]

### R66-m1. Propagate the curvature stopping error through the full finite-jet map

**Location:** the final paragraph of the proof of Proposition 10.4, new module lines 308–310, p. 48. The sentence says the quadratic iteration can be stopped with the error from (10.3) added to the bound. Equation (10.3) controls the curvature vector only. As a literal coefficient-one addition to the complete contact-jet error, that statement is not justified and is false in the usual maximum norm of the derivative coefficients used in the paper.

Here is an explicit local smooth control. Take a normal two-contact polygon with $g=1$, $k_0=k_1=1$, and identical profiles

$$F_i(x)=\frac18x^2+\frac{10}{6}x^3.$$

They have curvature $c_i=1/4$ and third derivative $q_{3,i}=10$; on $|x|<1/100$ their second derivatives are positive. Their action Hessians are $s_i=3/4$ and their common one-step factor is $a=1/2$. The cubic remainder at the even quadratic reference is zero, and the symmetric cubic block has eigenvalue $(1+a^3)/(1-a^3)=9/7$. Thus $s_{3,i}=90/7$.

Starting the curvature iteration at zero gives $z^{(1)}=9/28$ in each component. Its certified curvature error in (10.3) is

$$E_1=\frac{16/49}{1-16/49}\frac9{28}=\frac{12}{77}.$$

Recomputing the actual tail factor from this approximate curvature gives

$$\widetilde a=1+\frac9{28}-\sqrt{\frac9{28}\left(2+\frac9{28}\right)}
=\frac{37-3\sqrt{65}}{28},$$

and the reconstructed third derivative is

$$\widehat q_3=\frac{1-\widetilde a^3}{1+\widetilde a^3}\frac{90}{7}
=\frac{2754\sqrt{65}}{2093}.$$

Hence $|\widehat q_3-10|>0.6084$, whereas $E_1<0.1559$. The inequality can be checked exactly by squaring positive quantities. Using the observed $s$ in the Schur ratio instead also fails the coefficient-one interpretation: it gives $\widetilde a=14/29$ and cubic error $48740/189931>12/77$. These are controls of finite-iteration error propagation, not counterexamples to exact curvature inversion or to the finite-flight proposition with its exact fixed point. [D2]

**Required clarification:** for a curvature stopping error $E_m$, write the complete-jet estimate as

$$\|\widehat q_{\le M}^{(m)}-q_{\le M}\|
\le C_M\{\tau^N+\varepsilon+E_m\},$$

on the same compact class, possibly after increasing $C_M$. Equivalently specify the Lipschitz constant of the finite-jet reconstruction and multiply $E_m$ by it. The preceding smooth-recursion proof already supplies such a constant. This is a minor quantitative correction, not a change of the exact theorem, an exponent, or the observation model.

The response also calls (10.3) an a posteriori bound; its displayed form is the standard first-increment a priori estimate. A genuine residual stopping bound, available from the same contraction, is $\|z^{(m)}-z(s)\|\le\|z^{(m+1)}-z^{(m)}\|/(1-q(s))$. Either correct the terminology or state that bound. This terminology point is subordinate to the full-jet propagation issue, not a second mathematical blocker.

## 5. Observation scope, exposition, and primary literature

The new shared introduction is a real improvement. It states the supplied contact points, signed frames, phase labels and closing translation before the leading theorem. It separates exact marked identification, local analytic norm control, weaker-data alternating-channel results, and charged preparation results. The old results remain active under explicit headings. No unproved implication is needed to combine their strongest features into one observation model. [S2, S5]

The global curvature algorithm is a finite-dimensional deterministic reconstruction from action Hessians. It does not supply finite computational complexity for the inherited countable realizable-law selector, nor does it price obtaining the conditional laws. Its observable contraction constant is observable in the exact-data sense; extraction of Hessians from noisy density records still needs the stated differentiable norm or other regularity assumptions. The fixed-order proposition supplies such a norm, rather than deriving derivatives from total variation alone.

The targeted primary-source check was refreshed. Bálint–De Simoi–Kaloshin–Leguil, Theorem D, Corollary E and Remark 2.3 on printed pp. 9–10, distinguish general-period Lyapunov recovery from separation of individual contact parameters using their length asymptotics. The new introductory comparison is accurate: supplied polygons and phase-resolved function laws are different observations, not a solution of that contact-separation issue using marked lengths. [L1]

Bolotin–Treschev's discrete Hill formula and orientation discussion provide established determinant/monodromy context, not the present projected boundary-curvature inverse. De Simoi–Kaloshin–Leguil's analytic open-billiard result retains its symmetry/genericity setting, and Finamore–Leguil's Sinai result uses an enriched marked length datum. Florio–Leguil's version-5 notice expressly removes the affected geometric rigidity assertion; it cannot be used as an available competing theorem. These record checks establish distinctions, not priority or redundancy of the present results. [L2–L5]

This was not an exhaustive novelty search or a proof audit of those papers. In particular I do not claim that the global curvature inverse or the principal relative/contact theorem is already in the literature. The new Riccati argument's simplicity does not establish prior art.

## 6. Exceptional significance at the requested level

### R66-E1. The exact global improvement should be credited at its actual strength

The paper now has a coherent mechanism: a physically normalized relative law retains nonlinear actions despite the small twist; the actual boundary envelope gives contact response; global curvature identification and signed recursion remove ambiguity among arbitrary positive marked analytic candidates. The complete local analytic inverse and the separate statistical consequences add genuine content. It would be unfair to reduce the whole paper to the projected scalar recurrence or to say that the new global conclusion is merely another local inverse theorem.

Nevertheless, I remain unconvinced by the proposed highest-general-journal placement. The v66 extension removes a genuine branch qualification, but the new obstruction is finite-dimensional and is resolved once the boundary Schur relation is available: equal data contract differences around the cycle, and the positive-part extension supplies a convergent algorithm and the image test. The passage to higher exact jets then uses the existing triangular inverse, and exact whole-table identity uses analytic continuation in supplied placement. These are useful improvements, but not a new global norm estimate or a reconstruction from weaker geometric observations.

Accordingly the exceptional-significance case must rest primarily on the **combined relative physical law and actual boundary-response mechanism**, not on counting global curvature inversion, jet induction and analytic continuation as independent major breakthroughs. The full general-period theorem continues to supply substantial polygon geometry and phase-resolved laws. Important inverse problems may legitimately have rich data; this is not an objection based merely on the number of assumptions. My concern is the demonstrated depth and reach of this particular mechanism beyond its calibrated local variational setting, compared with the weight placed on the later consequences. The current submission does not persuade me that the requested placement follows.

This is an evaluative judgment, not evidence that the theorem is false or lacks novelty. A specialist may reasonably assess the combined mechanism more favorably. The targeted primary records do not settle that disagreement. Nor would repairing R66-m1 alone change my recommendation: that small correction is a separate correctness matter.

### R66-E2. A repair-only loop is not an answer to the importance question

The author has improved the opening and correctly preserved distinctions that earlier reports requested. It would be inappropriate to reissue those closed concerns as new defects. No arbitrary deletion of the mathematical corpus is requested. No unmarked reconstruction, period-uniform or grazing theorem, global same-disc stability, general-period sampling rate, or marked-length rigidity theorem is imposed as a missing prerequisite of the stated results.

For editorial reconsideration, the decisive question is whether the relative/contact theorem itself is an exceptional advance. Another auxiliary proposition, source-preservation certificate, or new version number is not a mathematical answer to that question. The current four statements should be viewed as one global-identification extension of that mechanism. The revised synthesis now makes that interpretation possible; it does not by itself establish acceptance-level significance.

## 7. Disposition codes

**R66-D1 — Exact mathematics:** Lemma 10.1 and Theorems 10.2–10.3 withstand the scoped examination. The exact-fixed-point proof of Proposition 10.4 also withstands it. No fatal counterexample or new mandatory core reconstruction is established.

**R66-D2 — Minor quantitative correction:** clarify the final finite-iteration sentence of Proposition 10.4 using $C_M E_m$, or an explicit propagation constant, as in R66-m1. Do not inflate this into a failure of the global inverse or a change of statistical exponents.

**R66-D3 — Updated scope:** retire the candidate-closeness objection to exact marked identification. Preserve fixed polygon/placement, shared two-offset factors, strict positivity, complete visitation, and the distinction between global uniqueness and local norm stability. The projected extension is not a realization theorem for arbitrary positive data.

**R66-D4 — Placement:** do not accept at the requested level on the present exceptional-significance case, after crediting the global improvement and revised presentation. This recommendation is not a claim of established redundancy or an instruction to invent another technical repair cycle.

## 8. Reproduction and evidentiary limits

The downloaded native artifact has SHA-256 `81998d447b67fba243b860d639b68e31876a1d8f048f0941c8c2bd41cf628876`. Independent verification checked lengths, SHA-256 values and Git blob identities for **837 frozen files**, reconstructed the manuscript subtree using recorded modes, checked **134 distinct active inputs**, and verified **45 build-report evidence entries**. The active counts are 123 full, 55 principal and one companion. Baseline comparison verifies all 818 inherited paths: 811 unchanged in bytes and recorded mode, seven modified with byte-exact originals archived. [D1]

Fresh builds with shell escape disabled and regenerated auxiliary files succeeded for all three entries. All **480 pages** agree with the native PDFs in extracted text and same-renderer **72-dpi RGB arrays**. The PDF bytes differ. Final logs have four full-manuscript underfull notices and none in the principal or companion; no undefined-reference/citation, missing-character, overfull-box or LaTeX-error pattern was found. Actual visual inspection covered principal pp. **2, 45, 46, 47 and 48** at **108 dpi**; no clipping or unreadable formula was observed there. All-page mechanical parity is not all-page visual inspection. [D1]

The independent mathematical script imports no author code. It verifies 56 rational Schur data sets, 1,176 exact iteration-error inequalities, 57 two-point inverse inequalities, 168 exact terminal-tail eliminations and 168 finite Dirichlet comparisons. It includes the positive-nonimage and nonmonotone controls and an exact stopping-error propagation control for R66-m1. Eight 70-digit numerical cases compare the forward map, inverse, curvature Jacobian and finite Dirichlet tails; the maximum Jacobian discrepancy is below $2.3\times10^{-42}$ in that diagnostic. Three normal two-site specializations and a nonnegative-curvature boundary control are also included. [D2]

Normal and optimized Python emit identical JSON. Finite scalar and high-precision checks are not proofs of arbitrary-order smooth factorization, infinite-dimensional analytic inversion, global billiard realization, analytic continuation, or statistical risk bounds. The author's preservation/diagnostic program was not rerun. The mechanical verifier is reused from the previous independent audit and the baseline comparator is adapted; neither is claimed as new mathematics.

## Source keys

All S-keys refer to actual compiled source `38f798a9b28237420f070a032d3601f0bee72cde`, under the manuscript directory stated above.

- **S1:** `article/10c_global_curvature_inverse_v66.tex`, lines 1–313. Lemma 10.1 and Theorem 10.2, pp. 45–46; Theorem 10.3, pp. 47–48; Proposition 10.4, p. 48. R66-m1 concerns lines 308–310, not the displayed exact-fixed-point estimate.
- **S2:** `article/00g_contact_synthesis_v66.tex`; `article/00h_abstract_v66.tex`; Theorem 1.1 and the adjacent observation-model discussion, pp. 2–4.
- **S3:** `article/10b_periodic_contact_inverse_v65.tex`, especially lines 1–346, 348–454 and 541–650: graph sensors/Hessian, two-offset separation, actual envelope, signed blocks and interfaces with retained analytic and finite-flight results. No complete fresh certification of every inherited norm/continuation premise is claimed.
- **S4:** `article/10a_periodic_itinerary_relative_v64.tex`, especially lines 186–359: weighted construction, relative log determinant, endpoint compressions and trace-series comparison. The full earlier phase-space construction is not freshly certified here.
- **S5:** `journal/00_principal_introduction_v61.tex`; `article/00_structural_introduction_v48.tex`; current entry points and `journal/DEPENDENCY_LEDGER_V66.md`.
- **S6:** retained `article/23f2_finite_experiment_analytic_inverse_v62.tex` and `article/25a_common_observables_v25.tex`. Byte retention and separation of observation assumptions, not a fresh full statistical proof audit.
- **R1:** preceding report `reviews/a2-v65-independent-harsh-top4-2026-09-16/REFEREE_REPORT.md` at `7f4603531f7b97a23ce627fec47b7ddc5f4f9912`, especially R65-M5 and E1–E2.
- **R2:** current `RESPONSE_TO_REFEREE_V66.md`, `COVER_LETTER_V66.md`, `HISTORICAL_DERIVATION_AUDIT_V66.md`, and `LITERATURE_CHECK_V66.md`. Author claims/provenance, not proof substitutes.
- **D1:** `AUDIT_LEDGER.md`, `AUDIT_RESULTS.json`, `verify_delivery.py`, and `compare_baseline.py` in this review directory; downloaded artifacts and the source-to-products GitHub comparison.
- **D2:** `independent_checks.py` and its output summary in `AUDIT_RESULTS.json`. Full output and rebuild logs accompany the separate audit archive.
- **L1:** P. Bálint, J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectrum, homoclinic orbits and the geometry of open dispersing billiards*, DOI 10.1007/s00220-019-03448-x; arXiv:1809.08947. Author-hosted PDF, printed pp. 9–10 inspected: https://leguil.perso.math.cnrs.fr/Articles/Balint_DeSimoi_Kaloshin_Leguil.pdf .
- **L2:** S. Bolotin and D. Treschev, *Hill's formula*, Russian Mathematical Surveys 65 (2010), 191–257; arXiv:1006.1532. Theorem 2.1 and orientation discussion, printed p. 12 inspected: https://arxiv.org/pdf/1006.1532 .
- **L3:** J. De Simoi, V. Kaloshin and M. Leguil, *Marked Length Spectral determination of analytic chaotic billiards with axial symmetries*, DOI 10.1007/s00222-023-01191-8; primary record https://arxiv.org/abs/1905.00890 .
- **L4:** D. Finamore and M. Leguil, *A CAT(0)-approach to the marked length spectral rigidity of Sinai billiards*; enriched-datum primary record https://arxiv.org/abs/2510.18983 .
- **L5:** A. Florio and M. Leguil, *Smooth conjugacy classes of 3D Axiom A flows*; version-5 correction notice https://arxiv.org/abs/2010.04120v5 .

Primary records were checked September 16, 2026. Only review files are added on the new branch; manuscript source, existing reports, native deliveries, the default branch and repository permissions are not altered by this review.
