# A2-DYN revision 91 — proof ledger

Authority: `SOURCE_MANIFEST.json`; the verifier emits the inherited status plus explicitly listed changes as `source.resolved_claims`.

| Statement | Location | Exact scope |
|---|---|---|
| Scale-dependent measurable-set gluing | `lem:v91-gluing` | Finite-count norm inequality; fixed r gives finitely many intervals before the collision limsup. |
| Complete critical surface decay | `thm:v91-surface` | C(L+r)^(31/32) r^(1/32), all true one-sided faces and all positive residence lengths. |
| Matched-scale potential estimate | `lem:v91-potential` | Strong L^(32/31) norm of the actual fractional potential, C(L+r)^(31/32) r^(5/8). |
| Unweakened critical raw limit | `thm:v91-raw` | Weak L^(32/31) measurable-set norm, no logarithmic denominator; not strong LQ or essential height. |
| Complete central-window limit | `cor:v91-diffusive` | Same critical norm in diffusive measure dt/sqrt(m), not unnormalized dt. |
| Original union power bound | `thm:v91-exceptional` | Actual union; h^(31/4096) on the original cofinal cutoffs; uniform upper control for smaller cutoffs and all original weights. |
| All-radius maximal source estimate | `thm:v91-maximal-source` | One exceptional roof set for all local averages; measure C lambda^(-Q) h^(1/128); does not show the set empty. |
| Original essential-height charge zero | Not proved | Still the original pointwise requirement. |
| Strong critical LQ / pointwise LLT / unconditional downstream ratios | Not promoted | Only weak critical convergence is proved here; arithmetic zero classes are never normalized. |

## Exact supersession

The inherited flag `unweakened_critical_weak_error_convergence_proved: false` is preserved in the complete v90 snapshot. Its active v91 value is true by `thm:v91-raw`. This is the only inherited flag changed. Every prior mathematical source file remains byte-identical. The complete v90 article is compiled in the archive under its own reference namespace.

## Audit scope

The v90 report was read in full. Direct checks concentrated on the v89 complete critical surface bound (module 208), its existing norm gluing (210), the exact source comparison and fractional source inputs, the original-union mass estimate (209), and the v90 source and topology distinctions (211–213). The combination of the first two is the new route to unweakened critical convergence. All 213 inherited cores are preserved; preservation is not independent re-proof of the entire spectral chain.
