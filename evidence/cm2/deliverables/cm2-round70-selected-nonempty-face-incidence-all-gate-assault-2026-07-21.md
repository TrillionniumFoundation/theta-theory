# CM2 Round 70 — selected nonempty face incidence and all-gate assault

Date: 2026-07-21  
Scope: append-only continuation from the frozen Round-69 aggregate  
Strict verdict: **Round 70 materializes the first two nonempty, time-qualified
physical pullback-face components on an actual positive path component.  Each
receives connected rank zero, two one-sided trace IDs, an incidence edge, and
explicit local F8/F9/F10/F13 bounds.  The construction is one selected compact
germ, not a uniform arbitrary-return atlas; no composite gate closes and CM2
remains `NO-GO_FOR_CLAIM`.**

## 1. The actual path cell

Use the frozen selected maximal-word component

```text
component_id = 7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5
physical word = G:E -> W[0,0]
return depth = 1
```

The earlier physical corridor and reachability proof identify this as one
positive connected component.  At fixed parameter write

```text
a=1/2+s, c=sqrt(1-t^2), c_p=sqrt(1-p^2),
A=a c+t/2-9/25, B=c/2-a t,
T=c_p B-p A, p_1=T/(4/25).
```

The component predicate is `|p|<3/10` and `|T|<6/125` on the forced physical
word/chart domain.

## 2. Two nonempty physical face graphs

Take the compact germ

```text
13/20 <= t <= 2/3,
-1/10000 <= s <= 1/10000,
-3/10 < p < 3/10.
```

The frozen uniform bounds give

```text
partial_p T < -13277/76000 < -1/6,
partial_t T < -11/64 < 0,
T(t,-3/10,s) > 2759/40000 > 6/125.
```

At `t=13/20,p=3/10,s=0`, elementary radical bounds
`sqrt(21021)<145`, `sqrt(91)>19/2`, `sqrt(231)>15` give

```text
T < -193/4000.
```

The parameter variation is less than `29/300000`, so on the entire germ

```text
T(t,3/10,s) < -7223/150000 < -6/125.
```

Therefore, for every `(t,s)` in the compact rectangle, strict monotonicity in
`p` produces unique analytic graphs

```text
T(t,p_+(t,s),s)=+6/125  <=> p_1=+3/10,
T(t,p_-(t,s),s)=-6/125  <=> p_1=-3/10,
p_+(t,s)<p_-(t,s).
```

Each graph is connected and closure-contained in one regular physical branch.
It is assigned connected rank zero in its own carrier family.  Both faces have
one inside trace and one outside trace; the sign of `partial_p T` determines
which side is component-interior.

## 3. Explicit local fields

The transversality row is immediate:

```text
F8 gradient lower: 13277/76000.
```

Using `c>7/10`, `c_p>19/20`, `|a|<51/100`, the level-function derivative
ledger may be bounded by

```text
|T_t|<3, |T_s|<2,
|T_tt|<3, |T_ts|<2, |T_tp|<3, |T_sp|<2, |T_pp|<1.
```

Since `1/|T_p|<6`, implicit differentiation gives

```text
|p_t|<18, |p_s|<12,
|p_tt|<2610, |p_ts|<1740, |p_ss|<1152.
```

Thus a physical `(t,s)->(r(t),p(t,s))` face chart has a conservative local F9
graph-C2 bound `3000`.

For collision-area weight `w=(9/25)/c`, the signed moving-face current density
relative to `dt` is `rho=w p_s`.  The same ledger gives

```text
|rho|<12, |partial_t rho|<1752, |partial_s rho|<1152.
```

Conversion from `t` to physical arclength costs less than `25/9`, hence

```text
|rho|+|partial_tau rho|+|partial_s rho| < 6031.
```

This materializes an explicit F10 integer upper `6031` on both compact germs.
For each face, current variation is less than `1/5`; each one-sided physical
trace mass is less than `19/60`.  The two-face packet therefore has current
variation less than `2/5` and four-trace mass less than `19/15`.

## 4. Gate impact

- **Gate 1/3:** one actual local two-face material/trace/current row now exists
  on the selected component.  It is not crosswalked to the Gate-1 `Q,E,u,v`
  representative and is not uniform over all cells or depths.
- **Gate 2/4:** two nonempty `time_j=1` physical face-to-path incidence edges
  are certified.  No stable plaque, stable holonomy, marker saturation or
  all-depth commuting-square family follows.
- **Gate 5:** instantiated finite-`R_n` materialized nonempty compact face rows
  rise from zero to two on this selected depth-one component.  Each row has actual F8,
  F9, F10 and F13 data.  F14--F18, a complete limiting face atlas, weighted
  global sums and complete blocks remain open; global maturity stays `10/18`.

## 5. Strict shortest route

Replicate this construction over an exhaustive finite limiting-R1 face atlas,
then prove a rank/path-weighted summation of the actual F9/F10/F13 values and
attach F14--F17 operator costs.  Separately crosswalk the selected path cell to
the stable/material representative needed by Gates 1--4.  Two compact face
rows do not justify any global gate promotion.
