# Response to the two external reports on A2-DYN revision 88

**Author:** Qian Qi. **Revision:** 89, 12 October 2026. **Canonical variant:** `a2-dyn-v89-critical-distribution-2026-10-12`.

**Controlling weak-Lp report:** commit `c615c2e8a9ac955634fceb5c6f7ab0da8263af6e`, report blob `90affffc4882c6312707aea59b0d2c51d6f4be28`. **Parallel main-v88 report:** commit `3b1fb458831d4a1a2e51d01ab4682b30ae1a6cb7`, report blob `874290c1568d86c93d7e93606b05fc8439d6662f`.

**Weak-Lp author baseline:** `24eaaab3b0564c1b8eecbb2217959e3be4320032`, paper tree `af3d5707cc0ccad7fc20a6a67887cc0dc0e58ef6`. **Parallel main-v88 author source:** `e0d462e7b04c35fa3547435ede29adafe1968d8f`, paper tree `1c3e7c85c15f7265f66f8ee96ce6617d2f65488d`.

We thank both referees for distinguishing full-source estimates from fixed-cutoff estimates, and critical distribution bounds from essential height. This revision keeps the organizing pointwise theorem, its original source, exact labels, physical guard, section, normalization and all arithmetic classes. It does not replace that theorem with a different topic or a reduced journal objective. It adds a critical measurable-set estimate, a logarithmic estimate directly on the original exceptional source, and a global theorem in explicitly normalized diffusive roof measure. The essential-height charge is not declared zero.

## 1. The critical exponent — weak-Lp report §7.1

Module 208 proves endpoint weak boundedness at `Q=32/31` for the complete untruncated first-exit surface. The earlier negative residence moment required an order strictly below `1/32`; simply putting the endpoint order into that theorem would be invalid. The new proof instead retains `min(|E|,ell)` from the actual roof-set intersection and only then sums all residence bands. The leading dyadic sum is bounded by `C |E|^(1/32)`. The physical square-root cap makes the complete finite-count error bounded by `C_B(1+B|J|) m^3 rho_B^(15m/32) |E|^(1/32)`. Thus the tested set may shrink with collision count: its supremum and the complete residence sum occur before the collision limit.

The whole-segment optical triangle pays both factors in the angular density, with the actual fractional volume insertion and multiplicity one. It yields the additional term `s^(19/32) m^2 integral v^(1/4)`. No negative moment of the critical residence order is claimed. All residence lengths and incoming endpoint types remain present.

The new conclusion is a critical weak bound, not convergence in the unweakened endpoint norm. Module 209 proves convergence at that critical exponent with every positive logarithmic loss, using a stated pre-limit interpolation inequality between endpoint norm and mass. This supplies the logarithmic endpoint conclusion absent in the reviewed packet while identifying precisely the loss that remains.

## 2. A mechanism acting on the original exceptional union — main report §§23.1–23.3; weak-Lp report §8

The source in Theorem `thm:v89-exceptional-log` is exactly the original weighted union

`R_h^epsilon(t) = integral W^epsilon 1_{z<h^(1/8) or ell<h^(1/4)} dmu_t`.

It is not a protected-word source, a surface collar, a common-survivor restriction, or a sum that double counts the intersection. Theorem `thm:v89-endpoint-surface` and the original source-shift inequality first prove a critical weak bound for the unweighted original raw density. This majorizes the exceptional union at every guard parameter. The critical fractional input and the capped short-residence estimate give its ordered interval mass `C_L h^(1/128)`.

The elementary mass-to-logarithmic-critical interpolation then gives

`limsup_m sup_{R,n,k,J} N_{32/31,sigma}(m^2 R_h^epsilon;J) <= C_{L,sigma}(1+|log h|)^(-sigma)`

for every `sigma>0`, with all tested measurable sets included before the collision limsup. This is an additional quantitative restriction on concentration on the exceptional union itself. It is not confined to the complementary regular fibers.

This estimate does not control the essential supremum, so the primary zero-charge request is advanced but not marked closed. The proof states that distinction explicitly. A source-specific mechanism excluding arbitrarily narrow high peaks is still needed to conclude the governing pointwise theorem. Neither new status flags nor the abstract identify a logarithmic critical estimate with that missing conclusion.

## 3. The full central roof window — weak-Lp report §7.2 and editorial comment 4

Module 210 proves convergence on the entire central window after the exact coordinate change `u=(t-m bar(tau_R))/sqrt(m)`. In original coordinates the conclusion is

`sup_{R,n,k} [m^(-1/2) integral_{C(M)} |m^2 p-L|^p dt]^(1/p) -> 0`,

for `1<=p<32/31`, with the analogous critical logarithmic norm in the fixed diffusive interval. The raw density and every label are unchanged; only the measure used for the growing-window norm is explicit.

The proof partitions the roof interval into at most `2M sqrt(m)+2` pieces. It retains this growing factor, and the Jacobian `dt/sqrt(m)` cancels it at the stated normalization. For the critical norm the exact gluing factor is `N^(31/32)` and the rescaling factor is `m^(-31/64)`. This is not an unnormalized growing-window theorem. The factor `m^(-1/2)` is displayed in the statement and is not suppressed in any summary.

## 4. Limit order and exact physical data — both reports

One auxiliary band is fixed before each complete capped dyadic sum. The finite-count bound in module 208 holds uniformly over the tested set measure. No collision-dependent band is introduced. In module 209 the interpolation inequality is applied to each actual density before uniform limits; the outer reconstruction band is sent to infinity last. In module 210 the interval count is estimated at finite collision count rather than regarded as fixed.

The initial and terminal section tests, exact displacement and occupation coefficients, one-sided incident components, backward lifetime, original guard and single normalization factor remain visible. No arithmetic peak is deleted and no zero reference class is normalized. The pointwise source charge remains the cofinal limit of the original union restriction; changing the cofinal powers does not establish its vanishing.

## 5. Source identity and simultaneous preservation — weak-Lp report §11

The two v88 alternatives are preserved as different objects. The weak-Lp source stays at its historical directory and is the immediate mathematical baseline of the new `papers/A2-DYN-v89-referee-response` directory. The complete parallel main-v88 source is also retained, byte for byte, at `papers/A2-DYN-v88-main-preserved`, with its original tree hash. Existing branches are not overwritten. The final v89 author commit records both report histories as parents.

All 207 inherited weak-Lp cores, Python files, appendices, bibliographies and provenance remain unchanged. The complete preceding article and its archive are included in the new supplement; all 57 preceding top-level files are snapshotted. The current manifest has a unique revision identifier. Its stale `new_estimate` field is renamed `inherited_estimate_v87`; a single `new_complete_estimate` describes the current results. The parallel main-v88 source retains its own independent status record rather than being silently substituted for weak-Lp modules 205–207.

Two factual clarifications do not alter either report. The exact v87 paper tree verified by both author archives is `086086bf42a833b241422b0b8a145fa5771a6f2d`; the different value printed in the main-v88 report is not used as a source pin. Also, for `0<h<1`, `h^(1/8)<h^(1/128)` and `h^(1/4)<h^(1/64)`: the main-v88 lower thresholds enlarge the selected regular family, not shrink it. Neither correction settles the residual height charge.

## 6. Interfaces and dependency map — both editorial reports

The focused article retains the exact short-exit finite-count bound, its physical cap, the Borel segment map and density, full angular derivative, source-shift inequality, fractional source, long-residence theorem and positive scalar remainder in the normalization used in the proof. The dependency appendix displays the chain from capped residence distribution and complete trace to critical surface control, raw-density control, logarithmic interpolation and diffusive-window limits. Source receipts and finite fixtures stay outside the mathematical argument. The prior module-189 notation remains explicitly superseded at its archive inclusion.

## 7. Downstream laws and independent verification

No unconditional point-conditioned path law, denominator theorem, ratio, actual-return bridge or forward essential likelihood is promoted. The scalar-first order and positive-reference restrictions remain unchanged. The new proofs are provided in full, but no independent human specialist audit or formal proof certificate is claimed. Inherited four-record spectral, geometric and coarea inputs retain their explicit mathematical dependency status; the cited Demers–Pene–Zhang background is not treated as proving the repository's four-record assertions.

## 8. Qualification

The new exact-SHA workflow pins both v88 source trees and both controlling report blobs. It checks all inherited files and snapshots, finite normal/optimized agreement, complete native journal and supplement builds, all 210 active core recorder entries, stable references and PDF geometry. The parallel source is separately hash-pinned; its prior successful native qualification is not relabelled as a new v89 compilation. Only completed runs at the final v89 SHA constitute remote qualification. Software checks do not certify the continuum theorems or the missing essential-height conclusion.
