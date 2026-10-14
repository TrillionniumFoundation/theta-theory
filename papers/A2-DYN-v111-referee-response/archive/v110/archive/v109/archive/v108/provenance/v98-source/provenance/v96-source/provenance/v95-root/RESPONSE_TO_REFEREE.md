# Response to the external report on A2-DYN revision 94

**Author:** Qian Qi. **Revision:** 95, 13 October 2026.

**Controlling report:** `reviews/a2-dyn-v94-external-top4-review-2026-10-13/REFEREE_REPORT.md`, commit `8dc6ce40f455a033b0473758cf1a85d61dbbf8a1`, blob `e8804c69db02415d59d244529ceb6d422fa4ddde`.

**Preserved author baseline:** `b672cc3f880052fd461b6a4d6099f92008ba47ba`, paper tree `f0788580c4fab60cdcef0277f8d92052fd12dd15`. The new author branch starts at the controlling review commit. All 225 inherited cores, other inherited source files and modes, and the complete v94 article are retained. Both distinct v88 variants remain untouched.

We thank the referee for distinguishing residence-zero and target-critical concentration from the already estimated positive-scale pieces. This revision returns to those physical sources. It proves an additional complete zero-residence elimination, a target-adapted critical annular height estimate, and a bidirectional projected comparison. None is obtained by replacing the principal pointwise objective with a finite norm.

## 1. Zero-residence inlet — report §§7,10.1,14.1

Module 226 attaches both physical endpoint traces to the same actual short segment. Its packet is the smaller trace on each segment, summed only afterwards. At every finite collision count the difference between the original weighted interior source and this packet is bounded by

`C(1+epsilon^(-1)) integral_[t-delta,t+delta] v^rho`.

The same bound controls the inlet and outlet packets. The proof retains the full angular density and uses multiplicity-one physical coarea, not a number of words. At each fixed positive entrance gradient, all four ordered residence-zero charges therefore agree.

There is a substantive elimination: whenever either physical endpoint is grazing, the smaller trace is zero. The complete original source of this family has essential height at most `C(1+epsilon^(-1)) delta`, and hence zero residence charge. This includes a nongrazing inlet followed by a grazing outlet, not merely the already zero grazing inlet trace. No positive lower residence cutoff is imposed in the finite-count formula. The remaining packet requires two nongrazing physical traces. Its zero-charge assertion is not proved.

A target-gradient version is also proved, with the explicit condition `delta<=rho^2/(8 Lambda)`. The gradient bound is verified throughout the segment rather than inferred from its target value alone. The report's notation `C_{rho,delta}` in §7 should not obscure the v94 theorem's common leading constant: the written source estimate fixes the positive cutoffs first and has a cutoff-independent leading constant. We preserve that precise quantifier and do not extrapolate it to gradient zero.

## 2. Target-critical histories without the prescribed crossing — §§8,10.2,14.2

Module 227 uses an intrinsic anchor on the longer physical side of the target. In the annulus `q<=z(t)<2q`, a segment of total residence at least `q^2/(16 Lambda)` admits an anchor interval of length `d=q^2/(256 Lambda)`. Along every joining interval, `q/2<z<3q`. This gives the complete pointwise comparison

`H_q(t) <= d^(-1) integral_[t-4d,t+4d] p_(3q) + C(1+epsilon^(-1)) integral_[t-4d,t+4d] v^(q/2,3q)`.

The inherited critical-volume and shell layer-cake bounds now prove

`H(H_q) <= C q^(129/128) + C(1+epsilon^(-1)) q^(257/128)`.

This family need not cross the shell specified in v94. It can remain inside that target core and supply an anchor on its own scale instead. A forward anchor may lie outside the selected prefix, but always stays in the same physical exact event; it is used solely in a positive upper comparison.

The complementary relatively thin segments obey `ell<z(t)^2/(16 Lambda)`, which implies `z(a+)^2 >= (7/8) z(t)^2`. Thus they are not critical births. If either endpoint is grazing, their complete annular target source has the stronger height bound `C(1+epsilon^(-1)) q^(257/128)`. Every critical directional birth lies in the relatively long class.

The finite-count estimate explicitly retains `B_*^(-1)` and the negative powers `q^(-3/2)` and `q^(-1/2)` in its remainder. We sum only finitely many annuli at each fixed positive lower gradient cutoff. The common leading radial bound is not a license to interchange that cutoff with the collision limsup. Concentration in disappearing critical annuli remains an unproved part of the original core problem.

## 3. Retain projected cancellation in both directions — §§9,14.3

Module 228 writes the exact projected measures

`K^- = D R - G^(+,>=rho)` and `K^+ = -D R - G^(-,>=rho)`.

The first is the backward measure already used in v94. In the second, actual entrances, including critical directional entrances, enter with the negative sign; terminal and artificial upper prefix cuts enter positively. Neither is discarded.

We take signed Stieltjes ramps first, then positive parts, and finally their minimum. The resulting `J` is bounded by the previous backward forcing and by the original source. It gives

`R(t) <= max(A_r^- R(t),A_r^+ R(t)) + J(t) + C(1+epsilon^(-1)) integral_[t-r,t+r] v^rho`.

The sharp version supplies persistence on at least one complete adjacent prescribed interval whenever the joint budget is small. A critical entrance is no longer automatically a positive obstruction in both directions. A terminal loss or critical decrease can still make the forward budget large. The minimum is formed after projection; we explicitly do not interchange a minimum with the sum over physical sheets or identify it with the separate two-ended positive packet.

## 4. Rates and the original scalar law — §§11,14.4–14.5

For the full original bad source the new joint forcing gives

`E_M <= C_M B^(-1/192) + J_(epsilon(B),M)(r) + C(1+epsilon(B)^(-1)) r`.

Its vanishing along any prescribed legal radius is necessary and sufficient for the unchanged pointwise law. This follows from the new comparison and `J<=b^epsilon`, not from a norm embedding. A common schedule `r=c epsilon^N`, `q=sqrt(r)`, `N>1`, makes the newly explicit linear and annular errors tend to zero. Widths and bands remain fixed during each collision limit.

The primary request is not marked closed. Neither the remaining two-nongrazing packet charge nor the zero-gradient concentration nor the joint forcing-zero assertion is proved. The unconditional pointwise scalar, unrestricted same-roof and forward essential-likelihood flags are unchanged. The new zero assertion concerns precisely the grazing-ended residence-zero subfamily at fixed positive entrance gradient.

## 5. Exact source, preservation, and architecture — §§2,4,15

The title, Lorentz family, section, exact displacement/occupation/collision labels, original guard, source normalization, actual-return interpretation and complete arithmetic reference are unchanged. The paper is an author revision in theorem-proof form, not a substitute finite-norm paper. The original union remains a target restriction in the common coarea kernels. Intermediate anchors do not redefine it.

All 225 inherited cores remain byte-identical; every v94 root file is snapshotted and the complete prior article is compiled in the supplement. The new journal loads exactly modules 226–228 and restates the indispensable inherited inputs. The dependency appendix identifies the source of each estimate and the precise unproved zero-scale passage. Historical variants and reports are not edited.

## 6. Qualification and independent review — §§3,14.6

The new workflow pins the v94 paper tree, its root snapshot, the v94 report and both v88 variants; checks inherited bytes and modes and unchanged historical flags; executes ordinary and optimized diagnostics; compiles the journal and the complete supplement; and requires recorder coverage of all 228 cores.

Local journal preview and finite rational fixtures are recorded separately from full-source exact-SHA qualification. A queued run is never reported as successful. The frozen v94 report is not retroactively altered when workflow status changes.

No independent human specialist audit has been obtained. The new finite fixtures check two-ended algebra, signed ramps and radial/exponent arithmetic; they do not certify the continuum billiard inputs. The primary Demers–Pene–Zhang abstract was consulted as background on the scope of billiard local-limit literature, not imported as a proof of this repository's four-record or pointwise theorem. The new elementary trace and Stieltjes proofs are written in full.
