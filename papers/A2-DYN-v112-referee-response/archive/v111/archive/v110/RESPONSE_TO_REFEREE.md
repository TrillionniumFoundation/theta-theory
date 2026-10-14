# Response to the v109 referee report — A2-DYN, revision 110

**Author:** Qian Qi. **Date:** October 14, 2026.
**Title:** Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas.

The controlling report is `reviews/a2-dyn-v109-capacity-abundance-external-top4-review-2026-10-14/REFEREE_REPORT.md`, at review commit `cdf0149246de7dd6b68b0b276d9dc1c4ca5537c2`, blob `dac29f62397ea98f43d6229928d45faced6dbc2a`. The reviewed author commit is `ab0ad79b9c101b82c80e33511529588d101a45c0`. The complete reviewed packet is preserved without byte changes under `archive/v109`, and the controlling report is copied without byte changes to `provenance/REFEREE_REPORT_v109.md`.

## 1. The main mathematical objection

The report correctly distinguishes completion of the visited-grazing argument from the required collision-uniform nongrazing microscopic height estimate. The revision retains the same exact-label raw pointwise target, radius supremum, essential roof supremum, original section and guard, arithmetic reference, and order of limits. It does not replace that target by an averaged statement.

The new argument is an actual payment of a positive submeasure of the original microscopic source. Let V be the total variation of the original weighted density on its complete physical pairing segment, and let c be the original minimum of its two endpoint traces. Before any pushforward, write

    c = min(c, gamma_B V) + (c - gamma_B V)_+,
    gamma_B = max(2, epsilon(B)^(-1/32)).

Lemma 7.1 proves that V is Borel and bounded by the integral of the inherited regular variation majorant on the full closed segment. Theorem 7.2 then completes the positive physical sum and bounds the first coefficient by the original uncut volume in a previously fixed roof window. Corollary 7.3 gives its ordered essential height O(B^(-95/384)). This does not depend on a lower residence cutoff, a comparison reach certificate or a count of collision words.

Theorem 8.1 proves a necessary physical property of every surviving coefficient: the density is relatively nearly constant on the entire closed segment and the original incidence/clearance guard remains positive everywhere on it. A segment which contains even one point where that original guard vanishes has its entire original paired coefficient paid. The witnessing bad test is allowed to change along the segment.

Theorem 8.3 retains the full original nongrazing comparison pool and gives the exact identity

    U_micro = U_var + min(U_per, K_B P_ng) + R_per.

It also proves 0 <= R_ng - R_per <= U_var, including the O(B^(-95/384)) ordered height difference. No coefficient has been deleted. U_per is explicitly a positive submeasure, not a renamed original source with a changed normalization.

This is a positive-source decomposition of the type requested in the report's route C, with a proved payment for its variation part. It is not a proof of an inverse-residence insertion, a full weighted-complexity theorem, or full capacity abundance. The remaining equation (8.9), labelled `eq:v110-remaining-limit`, is still the collision-uniform persistent-guarded shortage estimate. The present revision does not prove its vanishing. Accordingly, the primary referee request is not marked closed and no unrestricted point-conditioned or likelihood conclusion is promoted. This statement concerns the supplied proof, not a negative conclusion about the original target.

## 2. Optical denominator and the corner cofactor

Lemma B.1 supplies the signed formula for G_0m, including the deletion minor in Cramer's rule, the endpoint/interior coupling factors, the Schur-complement sign, the m=2 empty product and the m=1 direct flight. It also displays the identical recurrence satisfied by the continuant denominator and the optical top-right entry. The absolute value is taken only when passing to omega.

Proposition B.2 proves a positive subset expansion of the optical denominator. Expanding only a prescribed set of marked reflections factors its coefficient into the intervening optical blocks. This gives a simultaneous product-incidence bound, with its dependence on the number of marks displayed. It includes the one-mark estimate as a special case. It is explicitly a fixed-itinerary statement and is never summed by replacing a weighted pressure argument with a bare word count.

## 3. Uniformity of the trace modulus

Corollary B.4 makes the constant explicit:

    C_H = 500 C_reg sqrt(2 Lambda_circle) / (4 pi c_* lambda_circle^2).

Its geometric constants are fixed and its remaining inherited dependence is C_reg from the regular weighted derivative estimate. It is independent of collision count, radius, exact labels and the individual sheet. This gives the uniformity requested in the report without claiming that a per-sheet estimate proves the global shortage bound.

## 4. Simultaneous endpoints and multiple grazings

Lemma B.3 states and proves the whole-approach one-sided limit separately. It treats the designated entry root, a non-collapsing flight, the continuous reflection law, finite third-disk clearance minima and a section decision which changes at the limiting state. Visited grazing, unvisited tangency, a section boundary and an incoming critical endpoint may occur simultaneously. The lemma does not extend the exact event through a singular boundary.

Multiple visited grazing incidences are included in the same physical union Gamma. One vanishing incidence already forces the paired source to vanish, while Proposition B.2 additionally controls simultaneous products. The old zero-source and positive-capacity distinction is retained without modification.

## 5. Positive nongrazing endpoint mechanisms

Unvisited third-disk tangencies are not treated as visited grazing. A positive critical entrance, a section cut, a flat segment or a short-reach segment receives exactly the two positive coefficients in the new split. It is fully paid when the proved variation condition applies, and otherwise its remaining coefficient is retained. No uniform incidence lower bound is inferred from positivity at a fixed collision count.

The remark in Section 8 explicitly warns that a third-disk tangency can retain positive source, and that its name alone does not supply a variation payment. The complete original guard is unchanged: no section-distance factor, extra endpoint cutoff, or later collision-dependent width has been introduced.

## 6. Scalar allocation and limit order

The capacity allocation remains global and scalar at the original roof. It is not interpreted as a sheetwise coupling. The nongrazing pool is not restricted to the persistent source class: capacity on already-paid sheets remains available. This matters for the identity and the comparison with the old shortage.

At each outer B, epsilon, h, gamma, r and K are fixed first. The finite-count inequality is proved on the original physical measure; the positive sheet sum is completed; only then are the uniform norms and collision limsup taken. B tends to infinity last. No application of a fixed-width estimate uses a width chosen after inspecting m.

## 7. Presentation and preservation

The exact original unproved residual is printed in the introduction before the new positive results. Sections 1–6 retain the v109 model, input statements and complete optical/endpoint/capacity proofs. Sections 7–8 contain the new positive-source argument. Appendix A preserves the scope of the earlier scalar comparison results; Appendix B supplies the requested optical and endpoint details. The article uses an `amsart` theorem–proof structure, with explicit hypotheses, constants and dependencies. The title, topic and organizing pointwise assertion have not changed.

The active model, inputs, v109 core 260 and 261, and comparison-scope source have the same Git blob hashes as the reviewed source. The complete historical tree is retained, not reconstructed from excerpts. Historical derivations consulted include the v100 uncut weighted moment theorem, the v102/v103 source comparison and limit-order statements, and the v105–v108 microscopic-source and comparison-pool reductions. Their role is recorded in `PROOF_LEDGER.md`; they are not independently recertified by this revision.

## 8. Validation evidence and CI chronology

The finite diagnostics use exact rational arithmetic for the continuant, corner cofactor, Schur complement, positive optical expansion, marked inequalities, positive source identities and exponent arithmetic. They also run with Python optimization enabled, using explicit failures rather than removable assertions. They are not continuum proof certificates.

The report's freeze-time record that v109 CI was queued remains historically unchanged. A subsequent direct query now shows v109 run 38522526482 completed successfully at author SHA `ab0ad79b9c101b82c80e33511529588d101a45c0`, updated at 2026-10-14T07:04:47Z. Its artifact 11874809998 supplied the exact source archive used for local materialization. This later event does not retroactively alter the report and is not v110 CI evidence.

The v110 workflow checks its own exact checkout SHA, the unchanged original and copied historical tree, the frozen referee blob, and the scope of all additions. It builds the active revised article and uploads its source, diagnostics, PDF and logs. Historical retention is certified by the identical Git tree; this workflow does not claim to rebuild every historical supplement. A queued or missing v110 run is not recorded as a successful run. Local checks and observed remote run results are recorded separately.
