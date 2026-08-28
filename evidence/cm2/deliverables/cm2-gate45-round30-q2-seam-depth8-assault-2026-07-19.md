# CM2 Gate 4/5 round 30: Q2 chart-seam depth-eight assault

Date: 2026-07-19  
Status: **F4 strict-chart subledger enlarged; Gate 4/5 and CM2 remain open**

The round-29 fair Q2 target-chart refinement is extended from additional
depth six to depth eight with the same 384-bit Arb predicates and normalized
`(t,p,s)` longest-side split rule.

The 5,280 original chart-seam parents produce 457,964 terminal cells:

- 163,330 strict single-chart children;
- 294,634 residual representation-seam cells;
- exact resolved mass `64527087/655360000000`;
- exact residual mass `2559121/655360000000`.

Together with the 108,726 original strict-chart Q2 atoms, F4 now has 272,056
mixed-resolution strict single-chart cells. The residual mass is strictly
smaller than the original seam mass, but a finite depth-eight ledger is not a
complete chart atlas or a limiting chart-tube theorem.

The parent-canonical-W registry remains absent on the same Q2 strong
restriction. Therefore actual recut instance IDs, F7 characteristic-Z
charges, connected physical face pieces, numerical coarea/trace rows and
F14--F18 slots all remain zero. Gate-5 maturity stays `4/18`; CM2 remains
`NO-GO_FOR_CLAIM`.

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate45_round30_q2_seam_depth8_verifier.py

# Heavy full replay:
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate45_round30_q2_seam_depth8_verifier.py --replay
```
