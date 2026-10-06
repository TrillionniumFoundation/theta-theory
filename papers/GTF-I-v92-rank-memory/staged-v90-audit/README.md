# General Theta Foundations I — Revision 89

## Finite-Use Discrimination Geometry of Ordered Quantum Measurements

This response uses the actual R58-reviewed remote v88 publication `d1add4a7ba45230b3cba71b47ef46da5e4a88d72`, not the distinct unpublished local v88 allocation draft. The two R58 reports are frozen verbatim. The four-leading-general-mathematics-journal objective and the paper's topic are retained. Every inherited mathematical section remains byte-identical and active.

### New results

For a prescribed allocation of complete probe–reference groups, put `N=sum n_r` and `V=sum n_r²`. Both independent parallel groups and the larger prescribed-profile reset-feedback class have the same three local orders:

```
regular tangent:   min(1,sqrt(N)*s)
coherent tangent:  min(1,sqrt(V)*s)
support opening:   min(1,N*s).
```

For a history-dependent reset policy with worst-path reservation bounds `N_pi<=N`, `Q_pi<=Q`, `N<=Q<=N²`, optimizing over the budget class gives the coherent order `min(1,sqrt(Q)*s)`. The other rows are unchanged. A fixed profile with no feedback attains the lower. A specified policy is not claimed informative just because its cost is large.

These results are uniform in all profiles, all public integer budgets and all legal `F` with `sum_j||F_j-E_j-sH_j||op<=Lambda*s²`, after fixing the base measurement E, nonzero one-sided tangent H and allowance Lambda. Constants and the small-scale interval remain fixed-object dependent. They are local trace-distance orders, not arbitrary-pair metric equivalences or memory-dimension classifications.

The proof retains the finite `n*r*s²` and `m*kappa*s²` errors. Unequal coherent blocks use one common bounded classical readout independent of the unknown remainder. Reset-feedback upper bounds use subnormalized conditional fidelity, not unconditional tensor-product outputs. The refined finite policy upper is `min(2,2s(alpha sqrt(Q_pi)+sqrt(r N_pi)))`.

A separate proposition budgets a certified deviation from the ideal reset-preparation channel: worst-path diamond error sum epsilon changes a two-hypothesis separation by at most `2epsilon`. Another proposition proves strict containment, at the tester-operator level, of Ohst et al.'s two-call measure-and-reprepare class within the unit-reset retained-receiver class. Its explicit Bell-reference tester has partial-transpose eigenvalue `-1/8`. This is not a universal optimal-score separation for identical channel pairs.

### Reading and reproduction

| Entry | Purpose |
|---|---|
| `quantitative.tex` / `paper.pdf` | Primary discrimination article; new profile and budget proofs |
| `supplement.tex` / `BINARY_SUPPLEMENT.pdf` | Complete current binary proof dependency package |
| `structural.tex` / `STRUCTURAL_PAPER.pdf` | Independent unchanged structural article |
| `main.tex` / `COMPLETE_REVISION.pdf` | Full archival mathematical development |
| `sections/80-allocation-profiles.tex` | Unequal common readout and complete-profile comparison |
| `sections/81-quadratic-budgets-and-memory.tex` | Policy-sensitive bound, sharp hard budget, reset stability and memory witness |
| `RESPONSE_TO_REFEREE.md` | All 15 required items, 25 detailed comments, 29 gates and 18 risks |
| `PROOF_AUDIT.md` | Written proof dependencies, inequalities and scope |
| `RESOURCE_BUDGET_SCHEMA.md` | Exact arithmetic and conditional-certificate interface |
| `LOCAL_PREDECESSOR_RECONCILIATION.json` | Explicit reconciliation of the earlier unpublished allocation work |
| `evidence/BUILD_RECEIPT.json` | Current native-source identity and fresh execution results |

```sh
python build_revision.py --check-source
python profile_check.py
python resource_check.py
python resource_budget.py examples/resource-budget.json > budget.json
python resource_budget.py examples/resource-budget.json --verify budget.json
python build_revision.py --preflight        # local, not publication qualification
python build_revision.py --isolated         # from actual native-source commit
python build_revision.py --verify-published # read-only exact publication/final head
```

The production builder reruns all 26 inherited suites and both new suites under ordinary and optimized Python. The fixed-profile suite has 7206 positive checks and 24 rejection controls; the resource/memory suite has 39787 checks and 19 rejection controls. These finite tests do not prove continuum theorems or physically certify reset independence, gamma or implementation error.

The baseline has 665 native files, 975 complete labels, 488 current quantitative-package labels and 116 structural labels. Changed entry/audit/build files retain exact originals under `predecessor-v88-audit/`. The seven selected unpublished local v88 derivation files are separately preserved under `unpublished-local-v88/`; no prior remote publication of that draft is claimed.

The R58 provenance correction is explicit in `RELEASE_PROVENANCE.md`. The old v88 publisher verified its own child internally; this revision separately reconstructed pinned v88 read-only. A new v89 exact-final-head receipt must identify the actual triggering SHA; configured workflows alone are not successful runs. Independent human priority, a human signature, physical execution, general efficient recovery/dictionary synthesis, arbitrary-pair global geometry, full-boundary learning, growing-k minimax and the separate analytic programme are not claimed complete.
