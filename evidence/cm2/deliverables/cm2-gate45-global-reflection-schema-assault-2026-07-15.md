# CM2 Gates 4--5: global horizontal-reflection schema

Date: 2026-07-15  
Model: centred rational two-disk pilot on the standard solid-boundary section
`N=G disjoint-union W`  
Verdict: **the global scalar roof-current cancellation schema is certified;
Gates 4 and 5 remain `NOT_CERTIFIED`**

## 1. Exact finite ledger

The complete conservative Gate-3 candidate ledger has 448 source/target
rows: 57 targets on each gray source chart and 55 on each white source chart.
The horizontal reflection

```text
Jx(x,y)=(1-x,y),            Jx T_s = T_{-s} Jx
```

acts on all eight source cells and every retained lift.  The exact executable
check gives:

```text
448 rows = 218 two-row reflection orbits + 12 fixed-label orbits.
```

The 12 fixed labels are the vertical same-colour lifts on the `N/S` source
cells.  They must not be discarded: on them `Jx` acts inside the row by
`(t,p)->(-t,-p)`.

For every candidate the certificate verifies, over `Q`, the target-label
bijection and the affine displacement identity.  If

```text
d(s)=(a+b s,c+d s),          s'=-s,
```

then the reflected target displacement is exactly

```text
d'(s')=(-a+b s',c-d s')=Jx d(-s').
```

Together with the exact normal/tangent transformation this preserves the
discriminant, incoming root, first-hit order and absolute coarea Jacobian.

## 2. What cancellation is proved

Choose event functions compatibly with the conjugacy.  For any physical row
that eventually survives the exact Gate-3 normal-form partition,

```text
H_{Jx(e),s}(Jx z)=H_{e,-s}(z).
```

At `s=0`, its parameter derivative changes sign while collision flux and the
absolute coarea measure are preserved.  Hence every two-row orbit cancels
for the scalar roof test `1`.  On a fixed-label orbit the involution acts
inside the row, the signed density is anti-invariant, and the same scalar
integral is zero.  Thus the complete conservative universe has no unpaired
roof-mass row:

```text
GLOBAL_SCALAR_ROOF_MASS_CANCELLATION: CERTIFIED.
```

This agrees with the independent Kac identity
`mu_N(r_s)=1/mu_X(N)`, whose right-hand side is parameter independent in the
fixed-perimeter gauge.

## 3. Strict limits

The 448 rows are a conservative candidate universe, not yet an immutable
physical occurrence table.  Therefore this result does not provide:

- the Gate-3 normal-form decision and DQ witness for every row;
- a current identity against arbitrary, non-reflection-invariant tests;
- same-occurrence stopped-parent recovery or the global single-charge ledger;
- four separately typed Kac currents; or
- either phase CM2 norm lift.

In particular, scalar cancellation cannot be used to cancel norms of
oppositely oriented singular currents.  Gates 4 and 5 remain fail-closed.

## 4. Reproduction

```bash
PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate45_global_reflection_schema_cert.py

PYTHONPATH=deliverables /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate45_global_reflection_schema_cert.py
```

The certificate exits zero and prints both gate verdicts as
`NOT_CERTIFIED`.
