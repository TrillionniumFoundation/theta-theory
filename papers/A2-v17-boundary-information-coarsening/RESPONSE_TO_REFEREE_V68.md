# Response to the independent referee on A2, revision 67

**Qian Qi — September 16, 2026**  
**Revised title:** *Boundary laws and smooth contact rigidity of periodic dispersing billiards*  
**Report answered:** `review/a2-v67-independent-harsh-top4-2026-09-16`, frozen head `2786efc1351e82f61a24ba4f827712e3e04ca39f`.  
**Reviewed mathematical source:** `97b0c5bf15d6581c42b0f503bbe902c9d89b42db`; manuscript tree `5ba7cc8f87aaadd2e3f734c41bb030668e15cff7`.

We thank the referee for distinguishing a completed mathematical correction from the independent question of exceptional significance. We accept the disposition of R66-m1 as closed. Revision 68 does not relabel that correction as a new theorem, infer acceptance from the absence of a new error, or respond to the placement judgment with another preservation certificate.

The principal change is an extension of the **same relative-law/contact-response theorem** from analytic contact germs to complete **smooth contact germs**, together with real-profile stability under a finite-smoothness prior. The extension concerns the same supplied polygon, the same measured tangent sensors, the same physical two-offset laws, and the same actual envelope. It is not a replacement by an unrelated inverse problem. All earlier mathematical modules, observation models, and complete technical entries remain available.

## What is new mathematically

The new Section `sec:v68-smooth-contact`, in `article/10d_smooth_contact_rigidity_v68.tex`, proves six results, including a realized geometric information distinction.

1. **Actual successive visits with constant one.** The shifted half-line is the half-line of the next physical phase by uniqueness. On a uniform real collar its one-step map has derivative bounded by `a<1`. Consequently `|x_(b,j)(u)| <= a^j |u|`, simultaneously along the segment joining two graph candidates. The proof explicitly derives this estimate; it does not substitute the weaker `C rho^j` estimate into a large-weight argument.
2. **A functional separation estimate.** Integrating the actual envelope gives `g = alpha_bar h + K h`, where `alpha_bar >= 1/2`. In the real norm `||h||_(m,R) = max sup |h_b(u)|/|u|^m`, the tail norm is at most `3a^m/(1-a^m)`. Thus, for `theta_m = 6a^m/(1-a^m)<1`, `||h||_(m,R) <= 2/(1-theta_m) ||g||_(m,R)`. The coefficients depend on the candidate segment, so this argument is not represented as an observation-only reconstruction algorithm.
3. **Smooth germ identification.** The existing global curvature comparison and actual finite-jet inverse first match the jets. The new functional estimate then annihilates the remaining flat difference using equality of the complete actions. No convergence of Taylor series or holomorphic extension is used. Candidates need not be close. The reasoning does not identify smooth functions from their Taylor series alone.
4. **Finite-order comparison.** Curvature two-point control and the signed triangular inverse align the finitely many low graph jets. Differentiating the actual envelope along an anchored polynomial perturbation gives a uniform real `C^m` action bound. The proof records the summable `rho^(2j)` chain-rule estimate and a `C^(m+3)` regularity reserve.
5. **Complete real-profile stability.** On a fixed positive marked class, an order `m` is chosen from its contraction bound. For realizable pairs with a sufficiently small `C^m` law difference, the complete graph difference in `C^0` is bounded linearly by that difference. This uses a finite real-smoothness prior, not an analytic one. The proof aligns jets by a small polynomial, estimates the remaining function in the weighted norm, and removes the polynomial. Density derivatives, positivity floors and the separated offsets are specified.
6. **A physical distinction beyond all formal contact data.** An actual smooth obstacle is changed by a nonnegative flat graph perturbation `epsilon exp(-1/u^2)` near one contact. A separate boundary bump outside all visited collars preserves area exactly. Every marked graph and action jet remains fixed, but the complete action changes by `epsilon exp(-1/u^2)(1+O(|u|)+O(exp(-(a^(-2)-1)/u^2)))`. Two-offset laws therefore differ on every small common square. The family is realized by closed obstacles, not freely assigned formal coefficients.

These results are stated together with the retained relative physical law in the shared principal theorem `thm:v66-main`. Stable source labels are retained even where their historical version suffix is older than the current revision.

## R67-M1: residual certificate and quadratic image

**Disposition: accepted and retained.** The residual certificate and its certified inexact-evaluation variant remain in Theorem `thm:v66-curvature`, including the distinction from the first-increment a priori bound. A strictly positive certified fixed point identifies membership in the positive quadratic contact image, not realization by an arbitrary globally prescribed obstacle collection. The new smooth result does not weaken this distinction or claim a finite-time certificate of nonmembership at a zero component. Uncertainty in extracted Hessians remains separate from fixed-datum iteration error.

## R67-M2: the specified off-fixed-point reconstruction

**Disposition: accepted and retained.** The observed-Schur off-point prescription, the exact-fixed-point limit, and the actual finite-jet remainders are unchanged. The smooth functional proof is an additional use of the *actual* envelope along local graph representatives, not an interpretation of the off-point algebraic extension as a physical half-line solution. No interpolation of globally closed tables is needed for the uniqueness argument. The flat example separately supplies an actual global realization where claimed.

## R67-M3: noncommutative derivative and full-jet propagation

**Disposition: accepted and retained.** The sandwiched resolvent derivative, the joint lower-jet norm convention, and the recursively defined propagation constants remain exactly in force. In particular,

`||qhat_(<=M)^(m)-q_(<=M)|| <= C_M(tau^N+epsilon)+L_M E_m`.

The new section introduces a different integer `m` for a weighted real-function norm and labels that choice locally; it does not set the inherited propagation constant to one or claim unweighted all-order uniformity. Its real-profile estimate uses a finite number of derivatives and an explicit regularity prior. The diagnostic retains the preceding exact-arithmetic curvature, residual and signed-block controls through a clearly identified reuse of their pure mathematical routine.

## R67-M4: the cubic negative control

**Disposition: accepted and retained.** The coefficient-one cubic interpretation remains explicitly superseded. Its exact counterexample and a sufficient propagated bound remain in the preceding proof and diagnostic. No change to an observational exponent is inferred from the new weighted separation argument. No rational matrix test is described as a realization of a complete billiard.

## R67-C1: exact relative normalization and the physical clock

**Disposition: retained as the forward part of the central mechanism.** The chronological reference cofactor, normalized mixed derivative, two-ended trace-norm comparison, endpoint half-mass convention, and physical time interval are unchanged. The new inverse uses the *complete real action functions retained by this law*. An absolute exponentially small estimate could not supply these functions with the stated relative normalization. The unconditioned prefactor still contains free area; the conditional two-offset inverse does not assume that area has been observed. No general Hill-formula claim, grazing extension, or period-uniform theorem is inserted.

## R67-C2: actual boundary response and exact identification

**Disposition: the acknowledged finite-jet mechanism is retained and extended at the functional level.** The v67 inference “smooth jets do not identify smooth germs” remains correct for jets alone. Revision 68 now proves what the complete law adds. After low jets have been matched, the initial normal-graph variation can be separated from all contracted later visits in a real weighted space. The terminal term has already been controlled uniformly in the actual envelope before the parameter integral is taken. Signs, endpoint multiplicities and graph sensors remain physical.

The new exact conclusion is equality of visited smooth contact germs, without candidate closeness. The stronger whole-obstacle conclusion still requires actual connected closed analytic boundaries, fixed placement/lattice and full visitation. It is not extended to arbitrary unvisited smooth arcs. The local bounded-holomorphic inverse also remains a separate normed-space theorem.

## R67-C3: realized nonlinear information

**Disposition: the existing analytic equal-leading-data family is retained, and a different smooth information distinction is proved.** The analytic area-preserving quartic family is not replaced or reinterpreted. The new flat family keeps *every* graph and action Taylor coefficient, not merely the leading hierarchy, and proves a nonzero action signal. The remote area correction has zero local action contribution because all relevant half-lines remain inside the unchanged contact charts.

The new example does not claim equal full marked length spectra, equal fixed-window counts, or equal Taylor coefficients of normalized densities: normalizing factors may change. Its precisely stated conclusion is the difference between complete formal contact/action data and the real two-offset boundary-law functions. It explains why the new smooth theorem is not a formal corollary of the old all-order recursion.

## R67-C4: nonlinear dynamical information

**Disposition: retained.** The integrated amplitudes still determine the marked nonlinear stable and reversed unstable return coordinates, with their physical normalization. The smooth contact extension does not replace these amplitude identities with an abstract linearization theorem or permit arbitrary offset-dependent detector efficiencies. The shared observation model remains explicit.

## R67-E1: mathematical reach and exceptional significance

The referee's assessment concerned the depth and reach of the controlled relative/contact mechanism, not an established lack of novelty. The revision responds by demonstrating a new reach of that mechanism: **the actual boundary law determines local geometry beyond the formal Taylor category, with quantitative real-profile control under a finite-smoothness prior**. Analytic continuation is no longer the bridge from contact jets to local contact geometry. The formal/functional distinction is witnessed by actual equal-area tables with flat perturbations invisible to every contact and action jet.

The critical proof step is not another inversion of a finite cyclic matrix. It is the uniform passage from actual graph variations to a separating operator on real functions: shift-covariance gives a common one-step collar, the initial endpoint is counted once, the infinitely many later endpoints are summably contracted, and the difference is estimated only after finite-jet alignment. The same argument supplies the finite-smoothness stability theorem. The forward relative law is what provides the full real action input to this inverse.

We present this extension as a strengthened central theorem, not as a numerical tally of independent breakthroughs. The marked polygon is still supplied, general-period preparation rates are not asserted, and whole smooth obstacles are not inferred from local contacts. The submission asks for a renewed assessment of the resulting mechanism and its consequences. It does not claim that the referee's significance judgment has thereby been disproved, that priority has been exhaustively established, or that a particular editorial outcome is guaranteed.

## R67-E2: no artificial repair cycle or arbitrary deletion

Agreed. The revision does not treat the closed stopping issue as outstanding and does not make unrelated spectral, unmarked, grazing or acquisition theorems prerequisites. It retains the principal article, the complete technical manuscript and the companion. The new proof is integrated into both substantive entries immediately after the global curvature/jet inverse; it is not an unattached note offered in place of the paper.

Every inherited manuscript path remains. Edited originals are preserved byte-for-byte under `history/v67-review-baseline/`. The source checker verifies preservation and the compiled input graphs. Such checks substantiate delivery and retention only; they are not offered as evidence of mathematical importance.

## R67-D1–D4 and observation scope

| Code | Revision 68 action |
|---|---|
| D1 | Keeps the closed quantitative correction and its domain, proof and diagnostic controls. |
| D2 | Keeps global no-closeness curvature and finite-jet identification; proves smooth functional contact identification by an additional actual-envelope argument; retains analytic global and local-operator qualifications. |
| D3 | Recasts the shared theorem around the relative physical law and smooth functional inverse; connects the new flat family and finite-smoothness estimate to that mechanism. |
| D4 | Requests renewed assessment on the strengthened theorem without declaring the placement judgment reversed or disguising it as a correctness objection. |

The density norm in the new stability theorem is an interior real `C^m` norm. It is not supplied by total variation alone. A common finite-flight fit gives a deterministic candidate-comparison bound only when the same differentiated forward estimates and regularity constants apply. It is not a general-period sampling theorem, a budget for the countable selector, or a computable observation-only inverse derived from the candidate-dependent separating operator. All earlier weaker-data and charged-experiment results retain their own assumptions.

## Literature and evidence

The targeted primary-literature comparison is recorded in `LITERATURE_CHECK_V68.md`. It distinguishes the supplied polygon and endpoint laws from marked lengths and from enriched marked lengths, and respects the corrected primary record identified by the referee. No priority claim is inferred from differences in hypotheses alone.

`HISTORICAL_DERIVATION_AUDIT_V68.md` and `journal/DEPENDENCY_LEDGER_V68.md` identify the actual proof inputs. `VALIDATION_V68.md` states the mechanical and mathematical validation boundary. Source-matched native products, their immutable identities and completed verification belong in the versioned repository delivery and final review-ready index. No statement in this response is a proof certificate for the entire inherited corpus.
