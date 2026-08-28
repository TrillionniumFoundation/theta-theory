# CM2 Gate 3: common free graph-current carrier and finite two-cut algebra

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the complete depth-one fixed-gauge DQ, the complete future
side-owner current, and the all-key/all-component characteristic theorem  
Strict verdict: **a fixed 41,508-slot free graph-current carrier and the exact
additive two-cut product identity are now certified, with positive TV outer
`2590777728/5`.  The bounded physical lift/quotient in all strong fields is
not proved, so physical strong DQ, `MT_DQ`, `FACE`, and Gate 3 remain open.**

## 1. Fixed carrier

The frozen depth-one atlas has 64 complete face rows.  The completed future
side-owner atlas has 41,444 conditionally physical-first graph charts.  Their
tagged disjoint union gives

```text
Omega_<=2 = Omega_initial disjoint-union Omega_future,
|Omega_<=2| = 64+41444 = 41508.
```

Pull every coefficient measure back to one reference interval `I=[0,1]` and
keep empty charts as zero-measure slots.  This gives the fixed free triple

```text
X2_hat = C^1(N) +_1 l1(Omega_<=2; W^{1,1}(I)),
X1_hat = BV(N)  +_1 l1(Omega_<=2; BV(I)),
X0_hat = (C^{1,alpha}(N))* +_1 l1(Omega_<=2; M(I)).
```

The injections `X2_hat -> X1_hat -> X0_hat` are continuous.  Graph
pushforward has norm at most one from the slotwise l1-TV norm to the dual of
sup-normalized static tests.  Thus every frozen finite-depth current now has
one common ambient carrier independent of the number of nonempty slots.

This is a **free carrier**, not the physical Demers--Zhang triple.

## 2. Exact two-cut algebra

For `Delta_s(P)=(P_s-P_0)/s`, the finite-difference product rule is exactly

```text
Delta_s(P^2) = Delta_s(P) P_0 + P_s Delta_s(P).
```

There are two additive single-face insertions.  A product of two graph deltas
does not occur in a first derivative; it is a second-order object.  Adding
the two frozen positive TV outers gives

```text
initial face current:        16128/5,
future side-owner current:   518152320,
two-cut outer:               518152320+16128/5
                           = 2590777728/5.
```

This closes the finite-depth occurrence and algebra layer, including the
fail-closed exclusion of a spurious delta-product term.

## 3. Exact physical bridge still missing

To promote the carrier to Gate 3 one must still construct, uniformly in the
parameter and branch record,

```text
R_s : B2_physical -> X2_hat,
Q_s : X0_hat       -> B0_physical,
Q_s P_hat_s R_s = P_s,
```

with bounded restriction/trace and quotient/assembly estimates in all 18
operator fields.  Only field 7 is currently finite, with worst multiplier
`580000/1999>1` after no contraction gain; 17 fields and every complete block
are absent.  The existing TV assembly bound targets static-test duals, not
the physical weak anisotropic norm.

The same gap blocks moving branch tests, BL convergence on one
component-indexed atlas, and the no-`|s|^-1` growing-depth positive-current
tail.  Therefore the official interfaces remain:

```text
COMMON FREE GRAPH-CURRENT CARRIER:       CERTIFIED
FINITE TWO-CUT ADDITIVE FACE ALGEBRA:    CERTIFIED
POSITIVE TWO-CUT TV OUTER:               2590777728/5
PHYSICAL DEPTH-TWO STRONG DQ:            NOT CERTIFIED
MT_DQ / FACE_2CUT / FACE_TIME:           NOT CERTIFIED
GATE 3:                                  NOT CERTIFIED
```

## 4. Replay

```bash
PYTHONPATH=deliverables python3 -m py_compile \
  deliverables/cm2_gate3_common_graph_current_carrier_frontier_cert.py \
  deliverables/cm2_gate3_common_graph_current_carrier_frontier_verifier.py

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate3_common_graph_current_carrier_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate3_common_graph_current_carrier_frontier_verifier.py \
  --self-test

# Expected exit 2: the physical strong interfaces remain open.
PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate3_common_graph_current_carrier_frontier_verifier.py
```
