# Proof ledger — A1 English revision 4.0

All 13 original principal proof-bearing labels remain. Nine additional theorem labels appear, one of which is the overview theorem. The analytical proofs, finite arithmetic certificate, source regression checks, and independent review are distinct kinds of evidence. The 24 executed checks do not constitute 24 mathematical proofs.

## Retained principal statements

| Statement (page) | Label | Proof / disposition |
|---|---|---|
| 1.1 — Operational closure (p. 3) | `thm:main` | Original theorem retained; five-coordinate wording corrected |
| 2.1 — Actual apparatus kernel (p. 7) | `prop:raw` | Verbatim source |
| 3.1 — Realizability and cartridge pasting (p. 8) | `thm:attainable` | Verbatim source |
| 4.1 — Positive exact filter (p. 10) | `thm:filter` | Verbatim source |
| 4.2 — Degree elevation and rational closure (p. 11) | `thm:general` | Verbatim source |
| 4.3 — Sharp continuous state dimension (p. 12) | `thm:dimension` | Verbatim source |
| 5.1 — Moment body and Borel representatives (p. 13) | `lem:body` | Proof retained; intrinsic-dimension wording clarified |
| 5.2 — Attained Bellman recursion (p. 14) | `thm:control` | Proof retained |
| 5.3 — Full comparator interval (p. 15) | `thm:boundary` | Proof retained, including rare-failure normalization |
| 6.1 — Fixed-controller response and information (p. 17) | `thm:response` | Verbatim source |
| A.1 — Retained-bias entropy (p. 31) | `prop:biased` | Statement and proof retained |
| A.2 — Both density traces (p. 31) | `thm:two-trace` | Eulerian convention and outer flux made explicit |
| A.3 — Transported chamber response (p. 32) | `thm:transport-prep` | State/report distinction and reporting-space dimension corrected |

## New statements

| Statement (page) | Label | Proof / disposition |
|---|---|---|
| 1.2 — Structural and performance summary (p. 4) | `thm:strengthening` | Collects the new independently proved statements |
| 8.1 — Gram criterion, physical right inverse, perturbation margin (p. 20) | `thm:rank-criterion` | Finite-dimensional range proof; positive experiment normalization retained |
| 8.2 — Sharp intrinsic degree-q lower bound (p. 20) | `thm:q-dimension` | Open physical family -> coprime differential -> local section -> invariance of domain |
| 9.1 — Optimal Borel endpoint policies (p. 22) | `thm:endpoint` | Homogeneous convex continuation, layer cake, right continuity; referee proposal credited |
| 9.2 — Exact final-cartridge formula and two arcs (p. 23) | `thm:two-arcs` | Compact censoring decision -> pointwise gate maximum -> convex cosine envelope |
| 9.3 — Quantified endpoint lookup error (p. 23) | `thm:lookup-rate` | Unnormalized failure variation, finite-cube convexity, Bellman error recurrence |
| 10.1 — Complete-policy model error and regret (p. 25) | `thm:model-stability` | Common-history coupling; uniform payoff oscillation |
| 10.2 — Positive normalized physical approximation (p. 25) | `thm:smooth-surrogate` | Bernstein averaging; exact flag masses; binomial error; complete-policy transfer |
| 11.1 — Strict full-cubic adaptive advantage (p. 27) | `thm:adaptive-advantage` | Full-Borel nominal reduction; all 64 nonadaptive pairs; exact intervals; model/prior transfer |

## Boundaries that are retained, not silently removed

The qn dimension bound concerns exact continuous likelihood states across known command histories; it does not exclude discontinuous encodings or approximate compression. Positive degree elevation can introduce redundant stored coefficients. The two-arc statement concerns the last cartridge with tagwise rewards, whereas endpoint-gate existence holds at every finite budget under the original payoff assumptions. The lookup rate states its additional Lipschitz bounds and does not claim a polynomial-time global solver. The physical surrogate preserves positivity, normalization, and flag masses; its TV and value bounds do not establish convergence of parameter derivatives. The adaptive example compares the entire declared classes; its final interval encloses a rigorous lower-bound expression, not the exact final gap.

## Execution and review separation

`V4_CHECKS.json` records 24/24 newly executed diagnostics. `ADAPTIVE_CERTIFICATE.json` is the complete exact-rational finite certificate used by Theorem 11.1. `V4_BUILD.json` records the principal PDF and source digests. `V4_VISUAL_REVIEW.md` records actual rendered-page inspection. Historical 39/20/12 counts are excluded, and the inherited foundation companion was not rebuilt. A new independent referee review has not yet occurred.
