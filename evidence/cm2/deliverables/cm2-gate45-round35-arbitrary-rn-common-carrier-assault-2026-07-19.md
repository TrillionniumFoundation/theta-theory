# CM2 Gate 4/5 round 35: arbitrary-Rn common recovery carrier

Date: 2026-07-19  
Status: **a same-ID forward/reverse carrier now exists on every regular finite-depth return component; final numerical q remains open**

## Carrier construction

Fix `|s|<=1/400`, a finite `n>=1`, and one nonempty regular rank-refined
component `U` of `R_n`.  The existing arbitrary-path certificate gives a
canonical component ID, a real-analytic branch

```text
H = T_s^n|U,
```

an inverse on its regular image, and collision-area Jacobian one.  Foliate
`U` by the common unstable curves

```text
phi(r)=4r+b,       p(r)=sin(4r+b).
```

Every intersection with `U` is a countable union of open intervals.  The
least closure-contained rational-dyadic interval, the incidence-rank path and
the adapted short-cell index give immutable parameterized parent-W IDs at
arbitrary finite return depth.  This is a standard-Borel actual curve
registry; it is deliberately not represented as a finite integer list of
nonempty components.

## Physical disintegration

The coordinate map `(r,b)->(r,p)` has Jacobian `cp=cos(phi)`.  Since
`dell=sqrt(17)dr` on a slope-four leaf, collision SRB disintegrates with leaf
density

```text
rho_leaf = cp/sqrt(17).
```

On incidence-rank shells,

```text
|d_r log(cp)| < 4/cp.
```

The mesh `delta_B=2^-ceil(3(B+1)/2)` therefore supplies the required uniform
one-third log-Hoelder control.  Integrating the leaf weights recovers
`mu_s|U`, not a surrogate coarea measure.

## Same-ID forward/reverse pair

For a source cell `A subset U`, set `B=H(A)`, recut `B` to adapted length and
pull the cut back to `A`.  The two orientations are

```text
forward: A -> B,
reverse: I(B) -> I(A).
```

They share one physical restriction ID and one carrier-pair ID.  Area
preservation and billiard reversibility give

```text
mu_s(A)=mu_s(B)=mu_s(I(B)).
```

Thus fw/rev are two views of one charge, never two independently charged
copies.

## Numeric recovery clock

For each positive carrier cell define

```text
D = ceil(log2(m_parent/m_cell)).
```

The frozen numerical recovery constants give, on both views,

```text
R(D) <= 301500 + 1005 D,
R_fw(D)+R_rev(D) <= 603000 + 2010 D.
```

This is a finite numerical clock on every positive cell.  It does not supply
a physical global tail or moment for `D`; hence it does not yet produce
complete numerical `C_fw,C_rev` or final `q`.

## Evidence and replay

- `deliverables/cm2_gate45_round35_arbitrary_rn_common_carrier_cert.py`
- `deliverables/cm2_gate45_round35_arbitrary_rn_common_carrier_verifier.py`
- `deliverables/cm2-gate45-round35-arbitrary-rn-common-carrier-manifest-2026-07-19.json`

Using `.venv-neurips/bin/python`:

```text
independent replay:               AUDIT_MODE: PASS
self-test:                        HOSTILE_MUTATIONS_REJECTED: 16/16
default live mode:                exits 2
```

