# Response to the referee — A2-DYN revision 70

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.

**Controlling report:** `reviews/a2-dyn-v69-external-top4-review-2026-10-10/REFEREE_REPORT.md`, commit `f37e5d9431265cb16aebdc2211ed4706f73abb79`, blob `88ee6f3f4271119c39aaa84420db8f2446940ff6`.

**Reviewed author baseline:** `b959bbca34c35db82176c8f35bf029fec347e739`, complete paper tree `8209e73091651e5e95eebec221b1f0517a5d4863`.

**New source:** `papers/A2-DYN-v70-referee-response`. New proofs: cores 152--154. All 151 inherited mathematical modules remain byte-identical and compiled.

We thank the referee for distinguishing the valid comparison results from the missing full-source estimates. We retain the original triangular Lorentz problem, physical record, exact arithmetic kernel and unrestricted pointwise target. This revision does not replace that target by a different realization or remove an inconvenient positive source.

The principal new step distinguishes radial growth from angular loss. A supremum-to-average ratio can be arbitrarily large merely because a profile increases rapidly. Such growth need not obstruct comparison of an inner level with an outer annulus. We make this distinction at the level of the original physical source rather than assuming that the old radial moment is finite.

## 1. The new mathematical argument

For the actual exact-label angular fraction L_z(u), define a receiving-interval overlap

    a_z,J(u) = average over v in J of min(1, L_z(v)/L_z(u)),

with value one at zero source. Its exact complementary capacity is

    L_z(u)(1-a_z,J(u)) = average over v in J of (L_z(u)-L_z(v))_+.

Multiplication by a and 1-a partitions the original clearance source into complementary positive weights. It does not transport an orbit, substitute another exact label, or identify distinct angular sets. This is not a disjoint event partition.

Core 152 proves the ordered height bound

    H(s^{I,J}) <= C [d/(d-c)] [b-a+d]
                  exp(K_chi(sqrt(2b)+sqrt(2d))) W_delta(b),

where I=(a,b), J=(c,d), and W_delta is the unchanged absolute guard envelope. The proof uses the actual positive collar trace after the physical source has been summed. There is no radial-ratio cutoff, no assumed moment and no word-count factor in this theorem.

An exact no-loss condition on (0,H) against (H,2H) makes the overlap equal the entire inner source. Its height is then

    6 C H exp((2+sqrt(2)) K_chi sqrt(H))
          min(1, delta + C_g epsilon^{-1} sqrt(2H)).

This theorem needs neither an analytic-germ radius nor a uniform birth-order bound. It includes nondecreasing angular occupation and later births in that class. At a zero center guard the gain remains epsilon^{-1} H^{3/2}. Rapidly increasing scalar profiles can have arbitrarily large radial ratio while satisfying the no-loss condition. The paper explicitly distinguishes these diagnostic profiles from a claim that every such profile is realized by a Lorentz word.

Core 153 proves finite-word BV for the exact physical angular occupation on every compact radial interval. It identifies the distributional derivative as the radial projection of the signed reduced-boundary current of the actual physical angular set. The factor 1/(2 pi), outward-normal sign, cancellations and radial jump atoms are retained. Loss to an outer annulus is bounded by negative variation with the explicit triangular kernel kappa_H. This is a physical geometric identification, not an unweighted count of words or an assumption that a new moment is bounded.

Core 154 uses I=(0,h_chi), J=(0,h_chi/2) to allocate the entire selected disk. The overlap part has height at most

    (3/2) C h_chi exp((1+1/sqrt(2)) K_chi r_chi) = O(chi^6).

The original outside source is unchanged. All selected-disk annuli are allocated, but their loss is not declared small. With chi(B)=sqrt(epsilon(B)), chosen before the collision limit, the controlled part contributes O(B^{-1/4}) to the original raw-error identity.

These are scoped source theorems. They do not establish a finite uniform radial moment, a vanishing complete signed-current tail, the outside-source height, or the complete first-incidence height. Those obligations remain explicit below and in the manuscript status map.

## 2. Required change 19.1: the weighted radial tail

The referee is correct that the v69 moment was only a sufficient condition. We do not assert its finiteness in v70.

The new estimate instead proves a moment-free bound for a canonical positive part of every selected chart, and a full inner-source theorem on an exact class not requiring a radial-ratio bound. The distinction is substantive: angular growth incurs no outward loss even when the radial ratio is unbounded. An angular spike followed by disappearance does incur loss and is retained.

The remainder is expressed by the exact angular deficit Delta, not by a new declared finite moment. Core 153 identifies a sufficient negative-current bound from the original physical decision interfaces and keeps atomic deaths. Fixed-word finite perimeter is proved, but ordered weighted tightness is not inferred from it. Thus this requirement is advanced by a new source estimate and geometric reduction, not claimed closed for the entire Lorentz family.

## 3. Required change 19.2: the exterior clearance source

The previous e69 included annuli excluded by an extra radial cutoff. The v70 allocation uses the whole selected Morse disk. Its complete source is divided between s70 and d70, and no selected-disk annulus is left unassigned or declared negligible by its support alone.

The new e70 is exactly the original complement of the selected physical disks. It still contains failed taper, selected grazing, noncritical roof-rank pieces and uncovered states. The improvement is complete allocation and a count-uniform estimate for the overlap part of those entire disks. It is not a claim of height smallness for d70 or e70. In particular a birth outside the receiving collar can be wholly in d70. This example is included to prevent mistaking the new allocation for complete source closure.

## 4. Required change 19.3: complete first-incidence height

The original first-incidence source remains separate. The exponential finite-count estimate in core 131 is retained verbatim and is not inserted as a central-scale estimate. Choosing a count-dependent protection width to offset that exponential factor would not be justified by the inherited fixed-band reconstruction theorem.

The v70 endpoint inequality therefore still includes H(b_inc). No theorem flag for complete first-incidence height is upgraded. A uniform physical exact-label level-sum estimate remains necessary; neither angular overlap nor finite-word BV supplies it.

## 5. Required change 19.4: the original pointwise theorem

The title, source probability, exact return record and arithmetic transition kernel are unchanged. All arithmetic zero classes remain. The active introduction states the original two-sided pointwise target before the new scoped theorems.

The new complete source identity is

    b_clr = s70 + d70 + e70,

and its insertion into the original positive error identity yields

    E_M <= C_M B^{-1/192} + C' B^{-1/4}
           + H(b_inc) + H(d70) + H(e70).

Every term is accounted for on the same physical record. The last three heights have not been set to zero, absorbed into an unspecified remainder, or replaced by a small-mass statement. Their vanishing would complete the original pointwise theorem; it is not asserted by the new comparison theorem.

## 6. Required change 19.5: same-roof consequences

The inherited bridge, likelihood and conditioned-path derivations remain compiled. No unrestricted same-roof conclusion is promoted before the scalar pointwise denominator and complete source heights are proved. The source decomposition retains its original first-defect witness and next-collision mark, so that subsequent source disintegration can use the same identities once the scalar estimates are available.

## 7. Required change 19.6: independent specialist review

No independent human specialist audit has been obtained. The revised audit map identifies the exact continuum obligations in both the accepted v69 chain and the new v70 chain: physical masks, chart disjointness, collar-event domination, coarea representatives, restricted-analytic physical decisions, signed current and the remaining uniform weighted estimates.

Finite diagnostics, source hashes and TeX compilation are explicitly separated from these mathematical checks. This author response does not represent an independent referee acceptance, a formal certificate or an editorial decision.

## 8. Required change 19.7: audit metadata

The stale specialist map is replaced by a revision-70 map covering 140--151 and 152--154. The active main, source manifest, proof ledger, response, journal route, publication status, validation protocol and root index identify revision 70 and the same frozen v69 report.

The verifier preserves the complete recursive inherited boolean status map, not just a hand-picked list of recent flags. New true entries name only scoped results. Full raw inversion, complete source coverage, radial moment and independent human review remain false. Version-named older checkpoints and unchanged historical input maps are identified as historical rather than current status.

Qualification records bind themselves to the actual checkout SHA and active paper tree. The manifest describes the protocol and does not self-assert a successful workflow result.

## 9. Required change 19.8: journal proof burden

The opening now states two precise leading theorems and the original endpoint, followed immediately by the three new proof sections. The quantitative overlap argument needs only the actual physical density and positive collar trace. The signed-current identification separately identifies its finite-word analytic/BV inputs. The final section gives the exact source budget.

All old 151 mathematical modules and their labels are retained and compiled; the old opening is moved verbatim to an additional compiled appendix, with a byte-identical full-main provenance copy. The short proof route is editorial organization, not deletion of mathematical content or a claim that all inherited continuum inputs have been newly re-proved. Operational records are outside the principal proof.

## 10. Required change 19.9: literature comparison

Core 154 compares the observable and topology of the actual cited statements. The DPZ endpoint theorem resolves the two-dimensional cell index with admissible endpoint observables; it does not state the present simultaneous exact occupation and pointwise accumulated-roof boundary-height estimate. The DN framework uses additive-coordinate test functions and arithmetic/minimality hypotheses; its finite-horizon billiard application does not supply the essential-height estimate needed here. The paper states the additional density-height requirement, not a broad claim that existing Lorentz or suspension local limits are absent.

The cited DPZ Theorem 2.2/Remark 2.3 and DN Definition 2.2/Remark 2.5/Proposition 6.3 were checked in the primary preprint texts. Restricted-analytic monotonicity and cell decomposition are used only for fixed-word definability, not as a uniform dynamical theorem. Existing bibliography entries are preserved.

## 11. Technical comments 1--36

| Comments | Revision-70 treatment |
|---|---|
| 1--3 | Guarded b, unguarded comparison, scalar angular capacity and signed physical current are distinct. The exact label is fixed in every overlap and current definition. |
| 4--6 | Common coarea versions are specified; the 1/(2 pi) angular normalization and polar cancellation remain in the inherited exact profile. |
| 7--9 | The guard enters through its absolute C_g epsilon^{-1} envelope. It can vanish or be infinitely flat; it is never a divisor. |
| 10--15 | Old angular certificates and admissibility conditions remain unchanged. The new no-loss proof uses fixed I and J and makes no moving-band spectral claim. |
| 16--22 | The old V and its allowed-infinite moment remain. The new overlap is a chart-label quantity, with an explicit zero-source convention. No fixed-word finiteness is promoted to ordered tightness. |
| 23--25 | Both the old disjoint identity and the new positive-weight identity are retained. The meaning of d70 and e70, and the allocation of all selected-chart annuli, are explicit. |
| 26--28 | Complete first incidence stays separate. chi(B), I_chi and J_chi are fixed before m tends to infinity. No m-dependent cutoff enters the theorem. |
| 29--33 | Arithmetic zero classes, height versus mass/variation, and source versus probability normalizations remain distinct. The comparison is not a full reversible trace. |
| 34--36 | The active audit map is corrected, SHA qualification is not proof certification, and operational/history records are separated from the leading proof route without deleting inherited mathematics. |

The new proof also adds checks not present in the prior list: the overlap components are not disjoint events; radial BV jumps cannot be omitted; signed projection precedes taking the negative part; and coincident primitive decision interfaces are attributed once using the actual Boolean jump.

## 12. Scope submitted for the next review

The new claims for review are the finite-scale overlap theorem, the complete no-loss inner-source corollary, the fixed-word physical boundary-current identity, the one-sided BV loss formula and the whole-chart O(chi^6) source theorem with its ordered band choice. They are proved in full in cores 152--154, conditional only on the explicitly cited inherited physical inputs.

The full target remains the original unrestricted two-sided pointwise arithmetic law. The uniform angular-loss, outside and complete first-incidence heights remain outstanding mathematical estimates, not silently accepted assumptions. This distinction is reflected consistently in the main text, response, proof ledger and source manifest.
