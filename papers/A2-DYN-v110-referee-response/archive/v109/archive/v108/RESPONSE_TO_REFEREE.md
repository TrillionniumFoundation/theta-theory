# Response to the referee on A2-DYN revisions 105--107

**Revision:** 108.  
**Unchanged manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v107-positive-source-external-top4-review-2026-10-14/REFEREE_REPORT.md`.  
**Review commit / report blob:** `6811140ec51276247d75057980692d4a4d5e77b6` / `82cff2e2fc14e6a1eaa12b75fb41012dd155bdae`.  
**Author baseline:** `7f660346afea9500138920ca87fef46026a7e507`; frozen paper tree `7f6fcd70afa7a54f6891d4d399bf370c302eb526`.

We retain the paper's original problem and all inherited mathematics. We respond to the comparison-capacity issue by constructing a canonical pool at the original target roof, rather than by selecting another family of angular source blocks. The new construction has a proved one-copy overlap bound and an attained maximum in a precisely stated class of roofwise certificates. It pointwise dominates the preceding fixed-family allocations at the same total cost. We distinguish these results from the collision-uniform capacity-shortage estimate, which is not proved in this revision. No favorable recommendation or completion of the raw pointwise theorem is presumed.

## 1. The principal capacity objection: report Sections 15--17 and 23A

The referee correctly distinguishes paid endpoint trace loss from unpaid comparison capacity. Modules 258--259 keep that distinction and act on the original positive microscopic source.

For each original roof t, module 258 includes every admissible physical segment of length below Delta containing either [t,t+r] or [t-r,t] in its interior. A deterministic orientation rule counts a sheet once when both windows fit. Consequently the full physical comparison weight is at most one by construction. The Borel pool is built from the original endpoint maps; no optimal angular family or measurable selection over candidate families is assumed.

The endpoint maximum remains comparison capacity. It is not substituted for the source's paired minimum. The identity `P_r=D_r+E_r`, the inherited endpoint-variation inequality and the localization of every admitted segment inside `(t-Delta,t+Delta)` give the complete finite-count bound in `thm:v108-pool`. Its leading constant has the same fixed-window and outer-schedule interpretation as the inherited analytic inputs.

The source allocation is explicit:

`V(t)=min(U(t),K P_r(t))`,  
`R(t)=(U(t)-K P_r(t))_+`.

Both are obtained by multiplying the original source by measurable fractions at its original roof. The complete source is retained before taking any norm. There is no source deletion outside a selected angular family.

This replaces the old sufficient all-source-interval inclusion with a direct roofwise-window proof; we do not claim that the former inclusion now holds on every angular block. The new mechanism is genuinely broader: `prop:v108-strict` gives explicit regular interval data on which a roofwise certificate is positive but no whole-source-window block is possible at that width. The example is identified as a certificate-class diagnostic, not as a Lorentz realization.

## 2. Maximality and comparison with revision 107: report Sections 15 and 24(6)

`thm:v108-maximal` specifies its class in `def:v108-certificate`: fixed r, Delta and K, the same admissible physical comparison space, one-sided roof-window inclusion, and total physical comparison weight at most one. Every certificate in that class has accepted height at most `min(U,KP_r)`. The weights `gamma q_+` and `gamma q_-` attain this bound and are explicit measurable functions. This is a pointwise maximum, not an optimization of total angular mass.

`thm:v108-dominance` proves that every compatible revision-107 allocation with width at least r and cost N*kappa is pointwise dominated by the canonical allocation at K=N*kappa. At an active roof the old common-window lemma places every old comparison support inside the canonical pool. Summing the old accepted capacities with the *full physical* overlap bound proves the inequality. There is no interchange of a collision limsup with a block sum or an optimization.

We do not claim maximality over arbitrary transport mechanisms, costs, variable scales or unverified singular comparison spaces.

## 3. The seven requested construction properties in Section 23A

The new mechanism supplies actual same-event roof-window inclusion by explicit endpoint inequalities, Borel weights, original-selector compatibility, and one-copy overlap. The outer cost is a previously fixed K_B bounded by a constant times epsilon(B)^(-1/32), and Delta_B is 8 delta(B). The construction is evaluated on each finite-count physical source using this fixed rule; no width is selected after the collision limit.

The distinction between a *complete admissible pool* and *enough available capacity* is essential. Flat, short-reach and nonstationary source sheets can draw on any admitted sheet of the same exact event at the original roof; they need not themselves possess a continuation corridor. Nevertheless the pool may have insufficient capacity. Singular extensions without the inherited finite-trace and variation hypotheses are not automatically admitted merely by being named singular. Their unallocated source is retained in the canonical residual.

Thus the construction/overlap/selection part of Route A is advanced without adding another unconstructed comparison family. The requirement that the unallocated fractions have vanishing ordered essential height remains a separate physical estimate. We do not report Section 23A as fully closed.

## 4. Original target and exact residual: report Sections 16, 20 and 26

`thm:v108-original` proves

`E_M <= H_M(R_B_can) + C_M B^(-1/384)`.

The residual has its original-source integral formula in `eq:v108-residual`. At comparable windows and costs it is pointwise no larger than the v107 residual, independently of which compatible v107 family was chosen. The inherited necessity direction is kept, so the unchanged raw pointwise assertion is still equivalent to the stated residual-height decay.

The title, section, radius range, collision event, occupation and displacement labels, arithmetic zero classes, normalization, central roof sets and scalar-first conditional-law order are unchanged. We do not take the report's alternative Route C or substitute a standalone comparison paper for the raw pointwise problem.

## 5. Microscopic insertion and the order of limits: report Sections 8--9, 18 and 23B

The inherited inverse-residence and logarithmic criteria remain in the typeset article. No Lorentz moment estimate is inferred from them, and no B-dependent constant is silently treated as uniform.

`prop:v108-exhaustion` proves only the correctly ordered finite-count statement: when source and comparison space coincide, K>=1 and r decreases to zero after fixing the collision count, the shortage decreases to zero almost everywhere. This is not the order needed for the raw LLT. The text and the quantifier appendix explicitly separate the two assertions. The finite diagnostic suite tests this distinction on artificial interval data, which are not asserted to model the Lorentz family.

The remaining physical obligation is a collision-uniform estimate on `(U_B_micro-K_B P_rB)_+`, or a direct original-source microscopic estimate implying it. This revision does not claim such a bound.

## 6. Endpoint passage, Fubini and physical multiplicity: report Sections 11--14 and 22

The inherited finite one-sided traces, local absolute continuity and weighted variation remain explicit inputs. The new proof uses the original coarea kernels and one-copy uncut source. It does not differentiate a minimum, maximum, Borel selector or roofwise allocation weight. The comparison weights are held at the original roof t while integrating the auxiliary roof u.

The new kernel construction removes the need to choose an active source angle through the product-Fubini argument for each new block. It does not invalidate that argument or delete its inherited proof. Its Borel endpoint inequalities and positive Tonelli integrals are written directly in module 258. The uniformity order remains `sup_R esssup_t`; no radius-uniform null set is asserted.

The physical endpoint-trace, seam multiplicity and uncut-volume chain still requires the independent specialist reconstruction requested by the referee. No independent human audit is represented as having occurred.

## 7. Revision-106 metadata: report Sections 10 and 24(1)

The v106 local manifest indeed declares revision 105 and the v105 active directory. The versioned replacement `provenance/v106-metadata-supersession.json` records the actual v106 identity, author head, frozen tree, entry file and logarithmic appendix. It explicitly supersedes the identity claims in both the frozen local README and manifest. The frozen source tree is not rewritten. A workflow identity is not invented from the stale v105 workflow field.

The current v108 README, manifest, publication status and proof ledger agree. Other inherited validation/status notes are expressly historical, not current qualification claims.

## 8. Mathematical and qualification commits: report Sections 2--3 and 24(2--5)

The v107 theorem-bearing commit remains `2fad9446935a3c3efe6682715c8989ef66f1726d`; head `7f660346...` is the later narrow TeX-advisory repair. The response run `38513503361` succeeded at that head. The previously queued copy run `38513612021` has now also completed successfully at the same head; its API record was re-read, and its completion time is recorded in `provenance/v107-final-qualification.json`. The original report's freeze-time observation is preserved.

The v108 build records its exact checked-out SHA and theorem-bearing commit separately. It retains the byte-preserved `audit_v107_texlog.py`, including the exact document/source/line/message exception for the inherited plain-TeX fraction advisory. No general warning class is disabled. Undefined references, missing glyphs, overfull diagnostics, source mutations and recorder omissions remain fatal.

All completion flags for raw LLT, canonical shortage decay, complete positive-capacity coverage, collision-uniform logarithmic insertion, independent human review and formal proof certification remain false. Workflow success is not used as mathematical evidence for these claims.

## 9. Preservation and the next referee packet

All 257 inherited core modules and all inherited non-replaced files retain their exact blobs and modes. The entire v107 directory remains unchanged. The active v108 article typesets the exact previous article snapshot and inserts modules 258--259 before its appendices; it does not delete older proofs or criteria. A dependency/quantifier appendix, exact rational checks and recorder coverage of all 259 modules accompany the revision.

The proof ledger states precisely what the canonical construction supplies and what still needs a Lorentz-specific uniform estimate. This packet is submitted for further scrutiny of those new mathematical statements and their interaction with the unchanged raw pointwise target.
