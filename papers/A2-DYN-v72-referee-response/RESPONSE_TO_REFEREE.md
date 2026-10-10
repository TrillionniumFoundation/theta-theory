# Response to the v71 referee report — A2-DYN revision 72

**Manuscript:** Qian Qi, *Collision records, arithmetic, and raw local inversion in a triangular Lorentz gas*.  
**Controlling report:** `reviews/a2-dyn-v71-external-top4-review-2026-10-11/REFEREE_REPORT.md`, commit `3bf84b862a393456b0a57049d2966f9fbe34da08`, blob `129f78b849ebf2639130090189bb7b6e9bfebf8d`.  
**Reviewed author baseline:** `85152b57d47493e8d0ec2125e8365560aeb75cf0`.  
**New complete manuscript:** `papers/A2-DYN-v72-referee-response/main.tex`.

We thank the referee for separating the valid capacity and BV identities from the missing ordered estimates. We keep the original topic and unrestricted pointwise arithmetic target. The present response supplies a genuine derivative of the complete physical source, with all chart-boundary terms, and an unconditional recovered-height estimate which now acts on first incidence and the outside source as well as selected-chart loss. It does not represent these advances as a proof of the remaining full-source decay.

## 1. Principal changes

Modules 157--159 are compiled first. Module 157 differentiates the moving chart window, retains entrance and exit traces and true jumps, and proves gluing and Fourier identities. A full-window limit is taken in distributions rather than silently assuming outer-edge finite variation.

Module 158 defines `Db` directly on the unchanged complete physical source. It proves partition independence, the oriented regular-patch coarea formula, distributional exhaustion, and the exact compact-primitive identity `kappa_delta * Db = b - A_delta b`. The current includes first incidence, competing-hit clearance and every outside state. No boundary is lost by moving to the global roof line.

Module 159 retains `s71,1` and recovers a bounded fraction of `d71,1 + b_inc + e70` using the same exact-label average. The controlled part has ordered height `O(chi^6 + K epsilon^(1/16))`. The complementary residual is displayed on the original source and is bounded by `[b-K A_delta b]_+`. The resulting all-source reserve pays `K B^(-1/192)`, not the selected-disk `K B^(-1/4)` rate. A directed local-flux estimate gives a quantitative sufficient bound on this complete excess.

## 2. Response to required mathematical changes (report section 20)

### 20.1. Quantitative pooled-current tail

The v71 quantity `N_chi(K)` is not declared estimated. The new argument instead offers a second route on the complete source, without changing the physical record. Its exact excess `U_(epsilon,delta)(K)` is expressed by a genuine global current. Proposition `prop:v72-flux-height` proves `U(K) <= U(1) <= V_epsilon(delta)/2` under the explicitly stated finite-measure hypothesis. If `V_epsilon(delta) <= A epsilon^(-q) delta^beta` is established, the legal choice `delta(B)=epsilon(B)^((q+a)/beta)` supplies the rate `B^(-a/12)` with `K=1`.

This is a proved implication with a quantitatively specified input, not a proof of that input. The unrestricted tail request is therefore only partially addressed. The complete current estimate, rather than fixed-word perimeter or an unweighted interface count, is the remaining analytic task.

### 20.2. Complete first incidence

First incidence now participates in the allocation on the original exact-label source. Its recovered subsource is bounded by the new controlled source and hence has the same ordered `O(chi^6+K epsilon^(1/16))` height. The remaining incidence contribution is exactly `(1-alpha)b_inc`. It is not discarded. The complete incidence height is not declared small, and the old `C A^m epsilon` estimate is not inserted into the fixed-band limit. The recovered-height proof instead uses the complete physical local-variation estimate of module 106 at a fixed averaging width.

### 20.3. Outside clearance

The identical statement applies to `e70`: its recovered part is now quantitatively controlled, and its remaining part is `(1-alpha)e70`. Failed taper, selected grazing, noncritical roof-rank pieces and uncovered states remain in that identity. The complete current is defined on them before any chart decomposition. No exceptional roof set of positive measure or small-mass deletion is used. The complete outside height remains unresolved.

### 20.4. Unrestricted pointwise theorem

Theorem `thm:v72-complete-budget` proves the explicit full-source inequality

`E_M <= C_M B^(-1/192) + C B^(-1/4) + C K(B) B^(-1/192) + U_(epsilon(B),delta(B))(K(B))`.

The original finite arithmetic transition kernel and zero classes remain unchanged. Vanishing of the final term, with the legal reserve cost, is a sufficient condition. It is not proved for the unrestricted Lorentz family here. The full endpoint status remains false; the theorem has not been replaced by a window or integrated law.

### 20.5. Conditional consequences

Unrestricted same-roof collision/return bridges, forward essential likelihoods and pointwise roof-conditioned paths are not inferred from the new source algebra. Their inherited numerator and positive-reference hypotheses remain explicit. No conditional law is defined on a zero arithmetic reference class. This request awaits the necessary scalar and numerator estimates.

### 20.6. Actual global current, active windows and Fourier inversion

This is directly addressed at the distributional level. Theorem `thm:v72-window-current` includes both active-window trace atoms. Proposition `prop:v72-window-fourier` proves the corresponding Fourier identity, with zero-frequency compatibility. The complete-source current in module 158 is `Db`, not the old scalar `C=X-Y`. Its coarea formula retains oriented boundary flux, and its primitive identity is valid without assuming `Db` is a measure.

The required operator/resolvent norm bound is not supplied. In particular the `1/|xi|` factor of the primitive is not an integrable high-frequency majorant. The revision therefore closes the construction and sign/bookkeeping portion of this objection, but not the requested collision-uniform analytic control.

### 20.7. Independent expert review

No independent human review has been obtained. The active specialist map identifies the new BV-trace, exhaustion, source-allocation and ordered-limit questions, as well as all inherited collision-spectrum and arithmetic obligations. Source/finite-check/TeX evidence is not offered in place of such review.

### 20.8. Journal proof burden

The first part now presents a contiguous three-section route and the opening states only the actual theorem and remaining quantitative condition. A dependency map separates the shortest new route from the retained historical development. Every inherited proof remains compiled, and the preceding opening is preserved verbatim in an appendix. The cumulative manuscript remains very large; no assertion is made that a final journal-length complete endpoint proof has been achieved.

## 3. Technical comments (report section 21)

Comments 1--8: every capacity, current, allocation and supremum fixes `m,R,n,k`; pooling different exact labels is forbidden. Scalar maximality is distinguished from transport. Complementary weights are not misnamed disjoint events. Zero residual uses a harmless explicit convention. Common coarea versions precede allocation. `K`, `delta`, `epsilon` and `chi` are fixed before the collision limsup.

Comments 9--15: the unestimated quantities remain visibly unestimated; scalar fixtures are not Lorentz realizations. The old two-sided kernel and atoms are preserved byte-for-byte. New global derivatives contain the physical weights, translations and window traces before signed cancellation. The old scalar current is never identified with the derivative of the whole source.

Comments 16--19: all contents of `e70`, the complete incidence source, the finite arithmetic kernel and zero classes remain present. No exponential finite-count incidence estimate is used in the ordered limit; no pointwise conditioning is inferred from integrated total variation.

Comments 20--24: variation mass and probability total variation are not conflated. The section normalization occurs once. Occupation/terminal indexing is unchanged. Exact-SHA qualification is labeled source, finite-algebra and typesetting evidence. Provenance and validation records remain separate from the new mathematical opening.

## 4. Preservation and verification

All 156 inherited core modules, 209 Python sources, 11 appendices and `references.tex` remain byte-identical. Every previous compiled input and mathematical label remains active. The complete v71 `main.tex` and source manifest have additional exact provenance copies. No existing paper, review, root README or unrelated branch is modified.

The new qualification checks source preservation, status inheritance, normal and optimized finite fixtures, full native no-shell-escape TeX, stabilized references and new-proof page renders. Its records distinguish local extracted-source checking from actual remote-SHA checking. Passing these checks does not prove the unrestricted continuum statements.

## 5. Mathematical status of this response

The revision gives a global distributional construction and a source-preserving quantitative gain on all three original remainders. It also supplies the precise directed-flux estimate which would turn that gain into full closure. The unrestricted current-excess decay and complete incidence/outside heights have not been proved in this revision. We retain that distinction in every status record and request assessment of the supplied proofs without presenting an unresolved hypothesis as an established theorem.
