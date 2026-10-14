# Response to the external report on A2-DYN revision 96

**Author:** Qian Qi. **Revision:** 97, 13 October 2026.

**Controlling report:** `reviews/a2-dyn-v96-external-top4-review-2026-10-13/REFEREE_REPORT.md`, commit `c08d8186293dc55a7705945ca917596ff6eb859d`, blob `ea21dc4b10a43ffa53e7a3b0b79bf48f34ac0404`.

**Immediate author baseline:** `4b3ea4f4ce112338654279797cd4ce380842b4af`, paper tree `4490aafb771c8ff417c55030319a02d9602564fa`. The revision descends from the controlling review commit. The full baseline is snapshotted under `provenance/v96-source`, its main article is retained for complete archive assembly, and all 231 inherited core files keep their original bytes and modes.

We thank the referee for asking that the existing failure source actually be estimated rather than merely replaced by another conditional criterion. The new theorem bounds a nonnegative recovered part of that very source in the collision-normalized essential-height norm. Two mechanisms are used separately: capped two-sided coarea occupation, and running compression on complete same-event intervals. The remaining source is a subset of the old failure union. It is not asserted empty or of zero essential height.

## 1. Physical interruption and the artificial collar — request 13.1

Lemma `lem:v97-collar` proves that an original target cannot reach the artificial collar boundary within the uniform radius `r_col=R_-^2/(800 Lambda)`, in either direction. The original section has endpoint momenta below 17/20. Constant direction and radial growth of the endpoint gradient bound their change by `R_-^{-1} sqrt(2 Lambda |s|)`, which is at most 1/20 at this radius. The endpoints therefore remain below 9/10, strictly inside the 19/20 collar. This eliminates the artificial collar as a microscopic first obstruction, including simultaneous failures.

True grazing, first-hit loss and backward critical termination are not declared absent. The capped anchor samples both sides up to their actual available lifetimes, so neither side must survive the entire radius. Physical interruption is no longer an automatic rejection when shorter available pieces supply sufficient same-label coarea mass. The remainder near true original entrances is retained explicitly.

## 2. A target-height running-compression theorem — request 13.2

Theorem `thm:v97-running` estimates an actual maximum of the inverse angular-density ratio at the target roof. Let `d=2 q r`. On targets with original backward lifetime greater than `2d`, use the backward interval of length `d`; otherwise use a forward interval of length `d` when the original forward lifetime is longer and initial `z>=a`. The entire sampled interval remains in the identical original exact event. Its gradient is bounded below by `rho=min(a,sqrt(2 lambda d))`.

For the weighted target source where the running ratio exceeds `D_0>1`, the finite-count inequality is

`C_{a,q,r,D_0}^epsilon(t) <= C/(1-D_0^(-1)) int_{t-d}^{t+d} v^rho(u) du`.

The resulting ordered essential height is at most `C q r/(1-D_0^(-1))`. This includes the supremum over sampling time before the collision limit, every positive internal incidence, the full physical density `omega/(4 pi c_* chi)`, and the original starting weight. It is not an integral in the target roof and not an unweighted terminal-flux bound.

The leading constant is independent of each fixed positive `a`. Its finite-count remainder need not be. No limit at `a=0` is inferred, and no spectral estimate on states with changed occupation labels is imported. Thus the full comparison-domain compression tail is not claimed closed; the displayed complete same-event class is genuinely estimated.

## 3. Same-label occupation without a worst-time test — request 13.3

Module 232 defines the capped coarea clock

`c_{H,r}(x) = r^(-1) int_available 1_H(Phi_s x) min(1,A(Phi_s x)/A(x)) ds`.

It is formed on the actual physical survivor graph at finite count. It uses the ratio of physical transverse densities, not the projected roof density. Times carrying another exact label supply zero mass. The proof retains both signs in the single roof integral and uses fixed-time injectivity, so multiple returns carry no word or visit count.

The previous `D,beta` admission implies `c>=beta/D`. The capped clock can also admit targets rejected by the old whole-interval or worst-time tests; compression at unsampled labels does not by itself reject a target. The theorem estimates the old failed targets with `c>=q` by `C q^(-1)(epsilon^(1/16)+epsilon^(-1) sqrt(r))`, with `q=beta/D`.

This is an estimated part of the old failure source. There is no assertion that the recovered part is nonempty in every Lorentz fiber, or that every sparse-occupation target is recovered.

## 4. One disjoint finite-count decomposition and a quantitative decrease — request 13.4

The source is split into `c>=q`, `c<q` on the protected same-event class `P`, and `Y={c<q} intersect P^c`. If a target in `P` has running density ratio at most two, its chosen interval alone gives `c>=d/(2r)=q`. Hence the entire low-clock source on `P` is paid by the running-compression theorem and has height `C q r`.

The new residual obeys `0<=Y^epsilon<=Z_{r,D,beta}^epsilon`, where `Z` is exactly the preceding interruption/compression/occupation failure source. Theorem `thm:v97-reduction` proves

`H_M(Z^epsilon-Y^epsilon) <= C q^(-1)(epsilon^(1/16)+epsilon^(-1) sqrt(r)) + C q r`.

The recovered portions of all three old classes sum once to `Z-Y`. This quantitative estimate is the main result, not merely the subsequent endpoint equivalence.

The remaining target support is contained in

`{tau^-<=4 q r, z<a} union {ell<=6 q r}`.

Both lifetimes and `ell` refer to the original stopped exact-event segment, not the enlarged physical comparison. All gradients below the displayed upper threshold remain in the residual at finite count.

## 5. Signed forcing and scalar-first order — requests 13.5 and 13.7

The full finite-count source inequality also dominates the retained bidirectional signed forcing because that post-projection forcing lies between zero and `b^epsilon`. No positive part or minimum is moved inside a physical-sheet sum. Vanishing of the new residual would yield the forcing and scalar endpoint under the retained equivalence, but that vanishing is not asserted here. The upper pointwise LLT, original exceptional charge, unrestricted denominator, same-roof ratios, essential likelihood, total variation, entropy and arithmetic-zero normalization are not promoted.

## 6. One complete legal outer schedule — request 13.6

Use `D=2`, `beta=1/4`, `q=1/8`, `r=c epsilon(B)^4<=r_col`, and `a=sqrt(q r)`. The positive source cutoff is `rho=min(a,sqrt(4 lambda q r))`. Every one of these values and each auxiliary spectral band is fixed before the collision limit. Auxiliary bands are enlarged afterwards, and `B` is last.

The explicit recovered heights have orders `epsilon^(1/16)`, `epsilon`, and `epsilon^4`. With `epsilon=A_0 B^(-1/12)`, the recovered old failure is `O(B^(-1/192))`. The original pointwise error is bounded by the remaining residual height plus the same order. The residual has fixed-window mass bounded by `C L((q r)^(129/256)+(q r)^(1/32))`; this is not stated as its height bound.

The critical/short residual is therefore narrower at the prescribed comparison scale, but its essential-height zero-charge assertion remains the substantive missing theorem. The revision does not resolve that theorem by shrinking an outer parameter alone.

## 7. Independent verification and architecture — request 13.8; §§14–16

No independent human specialist audit has been obtained. The prior comparison flow and positive-cutoff spectral input are restated precisely and distinguished from the new elementary coarea and running-loss arguments. The new running-loss proof never uses a spectral source outside the fixed exact event. The original title, problem, model, section, guard, exact labels, normalization and finite arithmetic reference remain unchanged. Both revision-88 variants and every historical review retain their separate identity.

The focused article contains all three new proofs and explicit inherited inputs. The complete v96 article and 231 inherited modules remain in the technical archive, with the full source snapshot and claim authority outside the theorem narrative. Finite rational fixtures test the capped identity, running loss, disjoint decomposition, radial cutoff and schedule; abstract occupation fixtures are not presented as realized billiard trajectories.

## Qualification

The new workflow pins the v96 paper tree, its full snapshot, the controlling v96 report and both v88 variants. It checks source bytes and executable modes, inherited claim preservation, ordinary/optimized finite diagnostics, native article and full archive builds, actual coverage of all 234 cores, stable references and PDF geometry. Local preview results do not qualify the complete archive or a remote SHA. Final workflow conclusions must be read from the new author commit and are not inferred from an earlier revision.
