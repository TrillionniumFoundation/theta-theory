# Response to the external report on A2-DYN revision 90

**Author:** Qian Qi. **Revision:** 91, 12 October 2026.

**Controlling report:** `reviews/a2-dyn-v90-external-top4-review-2026-10-12/REFEREE_REPORT.md`, commit `3ffe7d107ef847562fd503ec98a41e33e7963c91`, blob `6fb5c325fc24eff1934b8134a5c4432a90d04486`.

**Immediate author baseline:** `4f0432884896a5a470a31aa18d4a8b7f4d9b8a23`, paper tree `01d42f467a87817d7b756615a438f95bd8072369`. The revision branch starts from the controlling review commit. The complete v90 source is additionally snapshotted under `provenance/v90-source`; all 213 inherited cores remain byte-identical.

We thank the referee for distinguishing integrated oscillation, critical weak convergence and pointwise closure. This revision proves the previously unestablished **unweakened critical weak convergence**, gives a polynomial critical-norm estimate on the **original exceptional union**, and controls every local roof averaging radius outside one quantified exceptional roof set. The original pointwise theorem, physical model, section, exact labels, guard, normalization, arithmetic reference and actual-return interpretation are unchanged. The essential-height charge is not marked zero.

## 1. Original essential-height charge — §§5,10,13–14

The primary pointwise request is not claimed closed. The new maximal theorem controls all local averages outside a quantified set; it does not prove that set empty. The source-specific zero essential-height charge still requires a stronger physical assertion. No finite norm, capacity statement or exceptional-set estimate is relabeled as an essential supremum. The original scalar and point-conditioned downstream flags stay false.

The revision nevertheless advances an explicitly open statement in the report: convergence at the unweakened finite critical exponent. This is not obtained by improving 1/33 to another fractional exponent or by an embedding claim. It uses the scale information in the complete surface theorem already in the repository.

## 2. The missing scale-gluing step — §§12–14 and the v89 endpoint objection

Module 208 proves the complete surface critical norm is at most C r when the tested roof window also has length r. Module 210 supplies the measurable-set gluing inequality with factor N^(1/Q), Q=32/31. These two statements can be combined before the collision limit. For a window of fixed length L, partition it into N=ceil(L/r) pieces, with r fixed first. The complete-source result is

`limsup_m sup_{R,n,k,J:|J|=L} N_Q(m^2 Fbar_r;J) <= C (L+r)^(31/32) r^(1/32)`.

The factor N^(31/32) is paid explicitly. Both the partition and the complete physical residence sum precede the collision limit; no number of words is estimated. Thus the scale-matched O(r) statement gives fixed-window decay, not merely fixed-window boundedness. Module 214 proves this connection in full. The old proof and its cautious final paragraph are preserved as historical statements, not edited retroactively.

The fractional optical potential is estimated on the same scale by Minkowski: its L^Q kernel is integrable because (3/8)Q=12/31<1. Finite gluing then yields C(L+r)^(31/32)r^(5/8). Applying the original positive source comparison gives critical-norm smallness C L^(31/32) epsilon^(1/16) for the original bad source. The positive scalar remainder proves raw-error convergence in N_Q itself, with no logarithmic denominator. The complete diffusive-window theorem uses the exact factor m^(-31/64); its measure remains dt/sqrt(m).

## 3. The estimate acts on the original exceptional union — §14.4

Module 215 keeps `z<a or ell<delta` as a single union in the original coarea fiber. Its unweighted upper source U is used only for domination: all original weighted sources with smaller cutoffs and arbitrary epsilon lie below U, which lies below p. No monotonicity of the original smooth guard in epsilon is assumed.

The actual source mass has ordered bound C_L(a^(129/128)+delta^(1/32)). At each finite collision count, the central source is bounded by the uniformly bounded finite-peak reference plus the absolute raw error. The new positive domination lemma gives

`N_Q(g) <= D^(1-1/Q) mass(g)^(1/Q) + N_Q(error)`.

With the unweakened error tending to zero, the original union has critical norm at most C(a^(129/128)+delta^(1/32))^(31/32). The original cofinal choice a=h^(1/8), delta=h^(1/4) therefore yields **h^(31/4096)**. This replaces the prior logarithmic critical bound by a power on the same source, not on its regular complement.

## 4. Pointwise maximal route, with its exact scope — §§14.1–14.3

Module 216 proves the interval maximal inequality directly with a finite disjoint covering and the measurable-set norm. Applied at finite count to U on an enlarged window, it controls the set where **some** local interval average of **some** smaller-cutoff original weighted source exceeds lambda. Its ordered measure is at most

`C lambda^(-32/31) (a^(129/128)+delta^(1/32))`,

and hence C lambda^(-32/31) h^(1/128) for the original cofinal schedule. There is one measurable exceptional set for all averaging radii and all the dominated selectors, not a separately chosen bad set at each scale. Lebesgue differentiation also controls source values at their Lebesgue points outside it.

This is a genuine all-radius maximal statement but remains a weak maximal statement. It does not satisfy the stronger requirement in §14.2 that would force the essential height to vanish. The pulse example is retained precisely to prevent that inference. No source-specific lower spike-width theorem is claimed.

## 5. Exact physical data and order of limits — §14.5, editorial comments 1–3,7–8

Every source and norm keeps the exact displacement and occupation labels, the original section decisions, both physical ends, critical entrances, original normalization and all finite arithmetic peaks. The complete first-exit surface retains incident components and backward lifetime. The two v88 variants stay in their distinct existing directories.

For fixed L and r the roof partition is finite before the collision limsup. Auxiliary bands are fixed and enlarged only as permitted by the inherited local theorems. The outer reconstruction band B is last. The explicit alternative r(B)=c epsilon(B)^4 is independent of collision count. The full diffusive-window partition may grow with m, but its exact norm factor is canceled by the coordinate Jacobian. No unnormalized growing-window theorem is asserted.

The earlier v90 lifted oscillation and regional capacity statements remain intact. They are not needed to make an invalid pointwise embedding in the new argument.

## 6. Qualification — §3 and editorial comments 5–6

The frozen report is not changed when later workflow status changes. The v91 workflow pins the v90 tree, its complete snapshot, the controlling v90 report and both v88 variant trees. It checks every inherited source byte and mode, all three new theorem files, ordinary/optimized fixtures, the full article and supplement, and recorder coverage of 216 cores.

The local new-article preview compiles without warnings, and 1,428 finite diagnostic fixtures agree in ordinary and optimized modes. These checks are not continuum proof certificates. Full native supplement qualification must be reported from an actual completed exact-SHA run, never inferred from the presence of the workflow or a prior successful version.

## 7. Independent verification and manuscript architecture — §§11.6,15–16

No independent human specialist approval has been obtained. The response and dependency map distinguish the inherited optical/coarea/spectral inputs from the short new gluing, domination and maximal arguments. The full original problem remains in the journal, followed by explicit inputs, theorem-proof sections and the exact remaining pointwise obligation. Historical proofs and the complete preceding article remain in the supplement and source snapshots. No alternate topic or substitute journal objective is introduced.

Only the historical false flag for unweakened critical weak error convergence is explicitly superseded by Theorem `thm:v91-raw`. All original pointwise, denominator, same-roof ratio and unconditional likelihood flags remain unchanged. The verifier enforces this distinction.
