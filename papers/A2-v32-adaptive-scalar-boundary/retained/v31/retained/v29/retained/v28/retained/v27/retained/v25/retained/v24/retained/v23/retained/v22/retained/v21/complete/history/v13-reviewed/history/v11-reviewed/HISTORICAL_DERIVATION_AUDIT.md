# Historical derivation audit for A2 v11

## Source identity
The source is the completed v10 manuscript at author commit `f46dca20f3d1b73077522bb2041f463af033cb70`, native tree `452a9003b03ff8f6eed47e1f609a36a054271455`, and the independent review at `2b893b931a894dfc9e7730b853f575124ffb5c55`. All 104 native source files were independently rehashed and their tree reconstructed. The prior completed-v9 author and review are `33ef794a398b23015651482e93be7667c08d6fad` and `b756f4851669e34c7074ba61b5bcf48689756406`. The parallel v9 initialization is not the source.

## Derivation chain used

| Historical source | Content consulted and retained | Role in v11 |
| --- | --- | --- |
| `v3/10_geometry_action.tex` | Shortest-channel localization, alternating Green kernel, cofactor normalization and relative endpoint twist | Physical input, unchanged; not replaced by inverse-problem algebra |
| `v3/20_integration.tex` | Full-phase flux, common Morse domain, exact selected finite-flight coefficient and smooth radial integration | Justifies integrated physical means and the exact one-/two-flight leading coefficients used by the pilot |
| `v4/10_boundary_layers.tex` | Half-line stationary segments, actions and Fredholm amplitudes, separated-block factorization | Supplies full nonlinear limiting laws on a fixed collar |
| `v5/15_differentiated_operators.tex` | Bounded differentiated trace norms rather than small differentiated operators | Supplies uniform differentiated physical bounds; unchanged |
| `v4/20_nonlinear_information.tex` | Quartic variation and physical analytic families with fixed selected leading data | Physical evidence that the invariant carries nonlinear information; not a new v11 realization |
| `v5/20_contact_rigidity.tex` | Full finite-jet triangular inverse, higher-order realizations, identical-even analytic germ | Retained application; not extended without proof to asymmetric graphs |
| `article/20_boundary_compatibility.tex` | Weighted energy pushforward, even-law inverse, odd convolution compatibility and coefficient identities | Identifies the target and supplies the convolution equation used by the new Abel analysis |
| `article/25_profile_acquisition.tex` | Compact sum-norm class, positive-node finite dictionary, charged binary observations | Entire old theorem/proof retained; the new acquisition has a different global interpolator and discrepancy |
| `article/60_smooth_remainders.tex`, `article/65_envelope_minimax.tex` and retained count appendices | Distinct exact-family and smooth-nuisance count models | Remain separate benchmarks; their lower bounds are not transferred to full profiles |
| `history/` and `two_collision.tex` | Earlier source records, round-33 chapter and original two-collision response | Preserved without asserting a new line-by-line certification of every historical argument |

## New derivations
`article/21_abel_stability.tex` proves the explicit weighted Abel two-sided estimate. `article/26_abel_acquisition.tex` proves the global positive-node reconstruction and its full charge. `article/27_profile_calibration.tex` proves the translated-flux estimate, smooth-remainder pilot and combined unknown-normalization experiment. The report's monomial and mixed-norm benchmarks are credited explicitly. These new theorems are not treated as consequences of the unrelated exact-family calibration theorem.

## Scope of the audit
This is a targeted audit of the latest report and the A2 derivation chain used in the revision. It is not an exhaustive re-refereeing of all inherited appendices, every historical branch, or the eleven-paper research program. Existing formal source retention is tested independently; retention does not certify every proof.
