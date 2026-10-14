# A2-DYN revision 95 — proof ledger

Authority: `SOURCE_MANIFEST.json`, with inherited flags resolved from the unchanged v94 sibling. All statements use the explicitly restated inherited analytic and geometric inputs. No inherited flag is promoted.

| Assertion | Location | Scope |
|---|---|---|
| Two-ended packet replacement | `thm:v95-packets` | Complete original short-segment source; smaller of the same segment's two physical traces; finite-count pointwise error, no residence lower cutoff. |
| Grazing-ended residence charge zero | Same theorem | Either physical endpoint grazing; positive entrance gradient fixed first. Common leading height error `C(1+epsilon^-1) delta`. Not zero at all gradients. |
| Target-gradient packet | `cor:v95-target-gradient` | Requires `delta<=rho^2/(8 Lambda)` and uses `v^(rho/2)` on the complete joining interval. |
| Intrinsic critical anchor | `thm:v95-anchor` | Actual annulus `q<=z<2q`, residence at least `q^2/(16 Lambda)`; no prescribed shell crossing; finite-count floor and remainder explicit. |
| Relatively thin classification | `eq:v95-thin-inlet` | Such segments have positive entrance gradient comparable to the target; critical births belong to the other class. |
| Thin grazing-ended height | `prop:v95-thin-grazing` | Complete annular source, no incidence cutoff; height `C(1+epsilon^-1) q^(257/128)`. |
| Bidirectional projected comparison | `thm:v95-bidirectional` | Both signed projected measures retained; minimum after projection; all artificial and true end signs explicit. |
| Bidirectional scalar criterion | `thm:v95-endpoint` | Exact equivalence under legal radii; not a proof of joint forcing zero. |
| Full two-nongrazing packet charge zero | Not proved | Both positive traces may remain; equality of inlet, outlet and volume charges is not decay. |
| Zero-gradient annular tail | Not proved | Finite annulus sums do not justify cutoff/collision interchange. |
| Full pointwise LLT and unrestricted downstream laws | Not promoted | The original scalar upper height is still required. |

The complete v94 report and active source were read. Direct derivation checks use modules 187, 196, 198, 202, 220–225 and their explicit current input statements. Complete preservation/compilation is not an independent re-proof of every historical module. Software diagnostics and a successful CI run do not constitute a continuum proof certificate.
