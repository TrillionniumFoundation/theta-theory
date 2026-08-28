# CM2 Gates 2/5: selected homoclinic component-incidence assault

Date: 2026-07-16  
Arithmetic: 384-bit Arb (`python-flint==0.9.0`)  
Strict verdict: **the initial collision occurrence of the selected physical
QNL homoclinic orbit belongs to one of the 24 positive implicit maximal-word
components; Gates 2 and 5 remain NOT_CERTIFIED.**

## 1. The previously missing incidence

The frozen maximal-word frontier materialized 24 positive connected
components but correctly left the following field false:

```text
selected_occurrence_membership_in_one_of_24_maximal_word_components_certified
```

The selected homoclinic point is on the QNL unstable graph at the gray disk
with

```text
x_h = -8.293762...e-15 +/- 1e-50,
|h_u(x_h)| < 7e-29.
```

In physical collision coordinates,

```text
r = x_h+h_u(x_h),
theta = pi/4 + r/(9/25),
t = sin(theta),
p = kappa (x_h-h_u(x_h)).
```

A 384-bit Arb evaluation gives the deliberately coarse strict rational
enclosure

```text
69/100 < t < 35355339059327/50000000000000,
-1/50 < p < 1/50.
```

The upper rational additionally satisfies

```text
2 t_max^2 < 1,
```

so it is strictly below the `E/N` normal-chart seam `t=1/sqrt(2)`.

The first collision in the frozen `Q5` word is `W[0,0]`.

## 2. A connected physical corridor

Define the full-parameter corridor

```text
source chart  G:E,
69/100 <= t <= 35355339059327/50000000000000,
-1/50 <= p <= 1/50,
-1/400 <= s <= 1/400.
```

The complete retained first-hit replay proves, uniformly on this entire
rectangle:

- the unique first solid collision is `W[0,0]`;
- no transparent wall is crossed;
- source and target collision momenta obey `|p|<3/10`;
- both incidence cosines exceed `19/20`;
- the target stays in the same `(-1,-1)` open-semicircle chart.

The corridor contains the original positive seed
`69/100<t<7/10`, `|p|<1/50` and also contains the selected homoclinic point
strictly at `s=0`.  Its rational upper face lies strictly below the `E/N`
source-chart seam.  Since the corridor is connected and remains inside the
exact word/chart/central-homogeneity predicate, the two points belong to the
same connected component.  Its frozen component ID is

```text
7359148da1c43a255f2238d9c831b8638f2c9885035034a5792699c968b2f3b5
```

Thus the missing occurrence-to-component incidence is now certified.

## 3. Exact scope boundary

This result binds a genuine selected collision occurrence to a genuine
positive physical word component.  It does **not** turn that component into
a branch of a stable quotient.  Still missing are:

- a stable-saturated product base and stable projection;
- quotient density `rho` and physical reverse weights;
- same-carrier endpoint maps and PPE contraction;
- full-key characteristic-boundary `Z`;
- the remaining 17 full-key operator fields and every complete 18-field
  block.

Therefore Gates 2 and 5, and hence unconditional CM2, remain fail-closed.

## 4. Replay

```bash
PY=/tmp/cm2-flint-venv/bin/python
$PY -m py_compile \
  deliverables/cm2_gate25_selected_homoclinic_component_incidence_frontier_cert.py \
  deliverables/cm2_gate25_selected_homoclinic_component_incidence_frontier_verifier.py
$PY deliverables/cm2_gate25_selected_homoclinic_component_incidence_frontier_verifier.py \
  --replay
$PY deliverables/cm2_gate25_selected_homoclinic_component_incidence_frontier_verifier.py \
  --self-test
```
