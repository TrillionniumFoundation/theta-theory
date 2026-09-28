# Response to the referee on A2 revision 71

Qian Qi · September 17, 2026

**Reviewed report:** `reviews/a2-v71-independent-harsh-top4-2026-09-17/REFEREE_REPORT.md`, commit `7bb8971f6b792894ee961f6fab5c6f68847d373d`.
**Reviewed source:** `b0a0c9a42e61422cdf7c82df3fb80bedc0d105af`; manuscript tree `8549bb0789d5e6cdce8ae12f70ed7c100f81510b`.

We thank the referee for separating the examined mathematics from the placement judgment. The report establishes no new mandatory correction of the examined core and explicitly closes the corrected planar lens comparison. We do not describe the significance judgment as a theorem defect or pretend that a revision number can settle it. We retain the full mathematical scope, all existing proof modules, and the precise observation hypotheses. The present response adds a mathematical consequence that changes the data required by the central smooth inverse.

## The substantive addition

The new Section `article/10g_uncalibrated_single_law_v72.tex` proves **smooth contact determination from one conditional endpoint law per oblique phase at a fixed but unreported positive offset**. Offsets may differ between phases. They are recovered along with the reflecting profiles; no second offset, acceptance probability, flux amplitude, boundary height or curvature is supplied. The original general two-known-offset theorem remains in place.

For a single phase, write the actual limiting physical law as

\[
f(u,v)=Z^{-1}B_-(u)B_+(v)\{d-A(u)-C(v)\},\qquad A'(0)=-p,\quad C'(0)=p.
\]

The supplied polygon gives the signed nonzero momentum `p`; it does not give `d`. The anchored quotient is

\[
\mathcal R_f(u,v)=\frac{f(u,v)f(0,0)}{f(u,0)f(0,v)}
=1-\frac{A(u)}{d-A(u)}\frac{C(v)}{d-C(v)}.
\]

Its mixed derivative at the origin is `p²/d²`, so `d=|p|/sqrt(∂uv R_f(0,0))`. The marked first derivatives then remove the multiplicative ambiguity between the two rank-one factors. The formulas recover both unequal actions and both normalized amplitudes. A fixed nonzero slice anchor, rather than differentiation along an entire axis, makes the inverse locally Lipschitz in the *same* `C^m` norm for `m≥2`. Since the smooth envelope theorem uses `m≥3`, this refinement costs no additional derivative in the geometric stability theorem.

The full actual-action inverse, not formal Taylor inversion, identifies smooth germs including flat differences. The finite theorem includes the nuisance offset in the countable realizable image selection, checks the forward bounds uniformly in a compact positive offset interval, and estimates both the table profiles and offsets. Its charged exponent is unchanged; it has `J=r` groups rather than the former `2r` phase/offset groups. All unsuccessful preparations remain charged. This is not a factor-two optimal sample-complexity claim: the constants and observation classes differ.

A separate first-collision argument proves that a clear periodic polygon with at least three distinct physical contacts has no normal reflection. Thus the new theorem covers **every** such polygon, without an extra genericity assumption. At a normal reflection the ray retraces its previous clear flight, forcing the preceding and following physical contacts to coincide. The distinct-contact two-periodic exception is self-retracing and has zero deck translation. The clock formula vanishes there; the unchanged two-offset theorem and the older known-offset symmetric theorem retain their respective roles. No general non-identifiability claim is made at normal incidence.

## Point-by-point disposition

| Report item | Revision 72 response and location |
|---|---|
| R71-M1: exact locality and area normalization | The entire v71 locality module is byte-exact. Its area factor, physical event, short free-segment margins, failure atom and independent-reset interpretation are unchanged. The new result concerns one fixed offset per phase; it does not invalidate locality at any fixed permitted offset. |
| R71-M2: contact-germ equivalence and normalization | The previous equivalence remains. The new inverse works with restrictions of `Q_+`-normalized densities on `Q`, without renormalization, because every formula cancels an arbitrary scalar. New rigidity is proved between actual table/offset pairs. |
| R71-M3: actual equal-area completions | The complete actual two-bump construction and corrected exterior comparison are unchanged. The new section applies smooth one-law determination to the inherited *different* flat contact family; it does not confuse unchanged contact collars with flat but different contact graphs. |
| R71-M4: relative physical numerator | The entire v64 module and its exact reference twist are unchanged. New clock recovery is applied to its differentiated physical limit, with linear momenta retained. It is not claimed exact for a finite-flight density: the relative `C^m` estimate supplies the finite-flight bias. |
| R71-M5: measured coordinates, quadratic and signed jet inverse | The v65 and v66 modules are byte-exact. The new formulas use the already supplied tangent projection and `p_b`; they do not supply graph height or curvature. The signed anchors retain their signs. |
| R71-M6: actual smooth functions and alignment | The v68 module is byte-exact. New rigidity invokes its action-level theorem, and new stability invokes its action-level estimate after polynomial alignment. No function is identified from its Taylor series alone. |
| R71-M7: differentiated topology and charged rarity | The v69 module is byte-exact. The new sampling theorem separately checks the `r`-group, nuisance-offset class, uses its derivative-estimation lemma, and repeats the realizability, binomial and balancing steps with the offset output included. Tags and gates remain exact, errors act after acceptance, and the count/bandwidth/local-error conditions remain explicit. |
| R71-E1: exceptional significance after adequate comparison | We retain the closed theorem-level lens comparison, and offer a new theorem rather than another citation or a renewed claim of same-data superiority. The new theorem removes the second offset and its supplied numerical calibration in the nonsymmetric smooth problem. Its significance remains for the referee and editor to assess. |
| R71-E2: distinguish depth from consequences | The response does not market rank-one algebra, kernel estimation or area adjustment as new general analytic technologies. The central mechanism remains the relative physical law and actual smooth envelope inverse. The new consequence shows that those interfaces support a strictly different observation theorem without offset calibration. |
| R71-E3: avoid a moving target or cosmetic revision | We do not invent mandatory tasks from the report. The revision supplies an explicit additional inverse, uniform fixed-order stability, a first-hit geometric lemma and a charged joint estimator, each with proofs. It neither promises a sequence of version increments nor announces the placement objection closed. |
| Presentation | A new introductory theorem and a compact observation/dependency map identify the three routes: general two-offset smooth recovery, oblique one-unreported-offset recovery, and the retained analytic/multichannel results. All full proofs and the wider technical catalogue remain available. |
| R71-D1 | All six operative v64–v71 proof modules and the two original introductory theorem statements are unchanged. Preservation checks are source checks, not mathematical certification. |
| R71-D2 | The already answered lens comparison and root-index request are not recycled as unresolved objections. The completed v72 root entry identifies the actual source and products. |
| R71-D3 | The exceptional-significance recommendation is answered with the new result and a precise account of its dependence on the inherited analytic work. We do not claim an acceptance recommendation, independent proof certification or exhaustive priority clearance. |
| R71-D4 | No fresh full proof audit is asserted for the later analytic continuation, global registration/lattice, moving-family, older catalogue or companion proofs. Their complete source is preserved. Review coverage and author-side verification remain separate. |

## Observation boundary

“Unreported offset” means a positive nuisance constant, fixed for each phase over all repetitions and returning lengths, inside a supplied compact interval with uniform physical margins. The actual experiment uses that offset. The reconstruction is not given its value. This is not arbitrary clock drift, an unknown phase label, an erroneous gate decision or a corrupted itinerary tag. The polygon, tangent/normal frames and signed momentum are still marks. Bounds deteriorate as the obliquity floor tends to zero. The result is local smooth contact determination, not unmarked whole-table determination.

## Comparison with the historical one-offset result

`article/23f_single_offset_law_inverse_v42.tex` already proves a known-offset same-type inverse with `A=C=S` by the factorization `1-t(u)t(v)` and a nonzero action anchor. We retain and explicitly cite it. The new theorem treats unequal past/future actions, uses their nonzero opposite marked slopes instead of equality of factors, and recovers the previously unreported offset. The change is therefore not the rediscovery of the older symmetric formula. The older onset-count calibration catalogue is also retained; its gap/area pilot is not used in this conditional-law calibration.

## Delivery and conservation

The downloaded native v71 archive was verified against all 929 listed source hashes and its exact Git subtree was reconstructed before editing. Four presentation/entry files are modified; their original bytes and modes are retained under `history/v71-review-baseline/`. All other inherited source files are unchanged. The active input union grows from 141 to 144, with no loss in any of the three entries. The new checker exercises signed rational unequal-action examples, scalar normalization cancellation, clock identification, amplitude recovery, the normal-incidence boundary and the charged exponent identity, with corruption/deletion/sign negative controls. It also runs the unchanged v71 checker against the reconstructed v71 source. These finite controls do not certify nonlinear or infinite-dimensional theorems.

Actual completed build identity, PDF inspection coverage and committed-product verification are recorded separately in the root v72 review-ready entry after execution. No previous report, A1 source, default branch, existing revision branch or repository permission is overwritten.
