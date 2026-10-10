# Response to the revision-70 external report

**Paper:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Revision:** 71, 11 October 2026.  
**Controlling report:** `reviews/a2-dyn-v70-external-top4-review-2026-10-10/REFEREE_REPORT.md` at `acf8568f8ce23f3067532f87d4264bdc41e3901b`, blob `17cc59fa6d9063db8dabf4b2dbaa6a81247198c6`.  
**Frozen author source:** `9eb04448ca20772c99c500b406a62bca1d2172c7`; full paper tree `6ac66c423de6b7705441cf346b927f04de9ad1a1`.

We thank the referee for separating the established overlap theorem from the complete source estimates still required by the original pointwise problem. We retain the original title, model, section, normalization, exact record, finite arithmetic kernel, zero classes and unrestricted two-sided endpoint. The revision does not replace the problem by a different realization, remove a set of roofs, or claim that finite-word BV supplies collision-uniform height.

## 1. The new mathematical argument

The new proof occupies two sections, `core/155_pooled_physical_collar.tex` and `core/156_two_sided_current_and_raw_budget.tex`. It retains the old controlled source rather than replacing its theorem by a weaker one.

At one fixed collision count, radius, exact label and absolute roof, let X be the sum of physically weighted angular capacities, O the sum of old overlap capacities, and Y the sum of receiving-collar averages over exactly the same active charts. Thus O <= min(X,Y). The old guarded sources satisfy s70 <= E O and d70 <= E(X-O). For K >= 1 we use the fraction

    theta_K = min(1,(K Y - O)/(X - O)),

with theta_K=1 at X=O. The recovery is made on the original probability space:

    s71,K = s70 + theta_K d70,
    d71,K = (1-theta_K) d70.

Theorem `thm:v71-pooled-height` proves the exact source identity, s71,K >= s70, d71,K <= d70, the residual bound E(X-KY)_+, and the count-uniform height H(s71,K) <= C K chi^6. The old overlap already spends O, so the available capacity is KY-O, not KY. This subtraction is essential.

The proof uses one unchanged positive physical collar after summing the chart contributions. It introduces no count of words, no new spectral insertion bound, no change of section normalization, and no physical coupling of trajectories. Different integer labels cannot share capacity. K is fixed before the collision limit.

The signed collar-balance lemma then proves X-Y as a weighted sum of actual two-sided radial currents. A whole disk compared with its inner half-collar requires positive births below the source roof as well as negative deaths above it. The older inner-to-outer formula correctly pays only negative current in its different geometry; it is not by itself a bound for the entire whole-disk residual. An isolated late birth beyond the receiving collar has positive loss and zero negative radial current. This distinction is now explicit in the theorem and in a negative control.

Crucially, the current is kept signed through the physical weights, critical-value translations and sum over the exact label. Taking positive parts chart by chart would discard receiving credits. The resulting net-current excess may therefore be strictly smaller than the former sum of per-chart deficits. Complementary scalar profiles demonstrate the strict improvement; they are not asserted to be independently realized Lorentz words.

## 2. Response to the required mathematical changes

| Report request | Revision and exact status |
|---|---|
| 25.1: ordered angular-loss estimate | Theorems `thm:v71-pooled-height` and `thm:v71-net-current` give a new dominating controlled source and an exact signed residual. Corollary `cor:v71-reserve-class` proves the complete original selected-source height, hence the old d70 height, on the stated X<=KY receiving-reserve class. For unrestricted Lorentz records the ordered net-current estimate is **not yet proved**. We do not relabel the new residual as negligible. |
| 25.2: outside-source height | The original e70 is retained exactly, with failed taper, selected grazing, noncritical-rank and uncovered states. It appears in every complete endpoint budget. Its ordered height is **not proved by the new collar argument**. |
| 25.3: complete first-incidence height | The complete original incidence source is retained. The finite-count CA^m epsilon bound remains finite-count; no m-dependent reconstruction band is introduced. The required uniform level-sum estimate is **not proved here**. |
| 25.4: complete arithmetic pointwise theorem | Corollary `cor:v71-raw-budget` substitutes the new source identity into the original positive raw-error theorem. It states the precise sufficient ordered limits, preserving the finite arithmetic transition kernel and zero classes. The unrestricted conclusion is not claimed without those limits. |
| 25.5: same-roof consequences | The original numerator and positive-reference hypotheses remain in force. Scalar denominator control alone is not presented as a new path-valued local law or forward essential-likelihood theorem. No conditioning on a zero reference class is defined. |
| 25.6: independent specialist review | `SPECIALIST_AUDIT_MAP.md` identifies the physical comparison inputs and the new cancellation and current checks. No independent human review has been obtained or represented as obtained. |
| 25.7: shorter principal proof | The new opening presents two leading theorems; the new argument occupies two sections. Source governance, validation records and response history are outside the principal proof narrative. The entire earlier mathematical development and opening remain compiled rather than being deleted. |
| 25.8: breadth without replacing the topic | The scalar recovery lemma and two-sided BV identity are reusable and are immediately applied to the original physically weighted Lorentz source. The complete selected-source reserve class is broader than chartwise no-loss assumptions. We do not claim multiple new singular-system realizations or substitute a model theorem for the original endpoint. |
| 25.9: active audit metadata | The active manifest, proof ledger, status, response, validation protocol and specialist map all identify revision 71. The complete earlier boolean status map is recursively inherited unchanged. Version-named historical checkpoints are not current proof statuses. |

The three unrestricted heights remain an actual mathematical task, not an editorial qualification to be removed by changing terminology. The new theorem addresses the old angular-loss source positively: its height is bounded by C K chi^6 plus the ordered pooled net-current excess. It also closes that original source on the explicit reserve class. It does not close the outside and incidence terms.

## 3. Technical comments 1--30

Comments 1--10: all capacities retain the exact label; controlled and residual pieces are complementary weights; zero angular capacity carries zero source; source and receiving intervals are different; the receiving average and center-plus-collar factor are explicit. The new factor is 3h/2. The original guard is bounded above, not substituted into the unguarded comparison density. The comparison is made after summing physical charts. No orbit transport or universal monotonicity is claimed.

Comments 11--17: scalar diagnostics are not Lorentz realizations. The BV cylinder is open; the current has its original outward-normal sign and factor 1/(2 pi). Coincident primitive interfaces use the actual Boolean jump once. Projection precedes Jordan decomposition, and weighted translated chart summation precedes the positive part used in the new endpoint. Atomic births and deaths are retained. Finite-word BV is always distinguished from ordered uniform height.

Comments 18--23: both old d70 and e70 remain identified. The new identity explicitly states how d70 is subdivided, with no source discarded. Every selected annulus is allocated. The fixed-band parameters obey epsilon=A0 B^(-1/12), chi=sqrt(epsilon); the recovered controlled part is O(K B^(-1/4)). This rate is not assigned to the residual, outside source or incidence. K may depend on B but never on the collision count within the fixed-band limit.

Comments 24--30: essential height is not replaced by source mass or variation; arithmetic zero classes and positivity restrictions remain; inherited distinctions between probability total variation, variation mass and path bounded-Lipschitz dual are unchanged. Finite diagnostics and successful compilation do not certify continuum proofs. False unrestricted endpoint flags remain visible. Operational metadata is separate from the journal-facing proof.

## 4. Preservation and validation

All 154 inherited core modules, 206 inherited Python sources, ten inherited appendices and the bibliography remain byte-identical. Every inherited compiled input and mathematical label is retained. The exact v70 opening is compiled as an appendix, and its full main source and manifest are preserved separately. The unchanged v70 sibling retains every superseded editorial document.

The new diagnostics use exact rational arithmetic for recovery, weighted translated currents and jump profiles. Negative controls reject cross-label borrowing, discarded physical weights, missing critical-value translations, premature positive parts, omitted atoms, negative-current-only inward comparison and double spending of receiving capacity. They do not establish Lorentz realizability or the remaining ordered height estimates. The read-only qualification workflow binds preservation, normal/optimized diagnostics, native TeX compilation and rendered proof pages to its actual checkout SHA. Only a successful run on the final author SHA counts as remote qualification evidence.
