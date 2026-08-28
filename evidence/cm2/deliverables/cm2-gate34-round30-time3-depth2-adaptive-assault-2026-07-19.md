# CM2 Gate 3/4 round 30: all-Q2 time-three depth-two adaptive assault

Date: 2026-07-19  
Status: **finite Q3 registry enlarged; Gate 3/4/5 and CM2 remain open**

## 1. Certified increment

Every one of the 114,006 round-29 Q2 anchors was replayed at 384-bit Arb
precision. Every unresolved time-three box was bisected along its longest
normalized `(t,p,s)` side, with at most two additional binary levels. The
complete terminal ledger is:

| class | terminal cells | coordinate-base mass |
|---|---:|---:|
| strict R3-inner | 0 | 0 |
| strict Q3-inner | 38,972 | 84093/2048000000 |
| unresolved finite outer | 388,890 | 10095133/10240000000 |
| total | 427,862 | 5257799/5120000000 |

The masses add exactly. The depth histogram is `4,088` at additional depth
zero, `15,898` at depth one, and `407,876` at depth two. Relative to round 29,
the certified finite-open Q3 component count increases by `34,884`.

## 2. Exact remaining outer

The 388,890 unresolved leaves split into:

- `373,816` third-flight competitor discriminants not sign-separated on the
  whole leaf;
- `15,074` inherited time-two outgoing chart/geometry leaves not whole-box
  strict.

This is a finite interval ledger, not a limiting tail theorem. In particular,
zero finite R3 cells is not promoted to physical R3 emptiness, and the depth
histogram is not extrapolated to uniform adaptive termination, singularity
growth, survivor recovery, or a strong-q weighted tail.

## 3. Gate status

The round advances the materialized finite Q3 registry only. It does not
construct the missing parent-canonical-W instance registry, numerical strong
coefficients, or the limiting component/tail estimates. Therefore Gate 3,
Gate 4, Gate 5 and CM2 remain `NOT_CERTIFIED` / `NO-GO_FOR_CLAIM`.

The Gate-1 literature audit also checked arXiv:2604.25881 and arXiv:2606.10155.
The former gives an exact symbolic Hausdorff-measure stable holonomy for its
one-sided product construction, but not the required physical SRB Green
marker/diagonal-ratio cohomology or a uniform `omega<m` rate on the frozen
clean family. No Gate-1 promotion is made.

## 4. Replay

```bash
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_round30_time3_depth2_adaptive_verifier.py \
  --self-test

# Heavy full 384-bit replay; deterministic forked chunks.
PYTHONPATH=deliverables .venv-neurips/bin/python \
  deliverables/cm2_gate34_round30_time3_depth2_adaptive_verifier.py \
  --replay --workers 16
```
