# CM2 Gate 1: biprojective half-density frontier

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: the faithful finite clean SFT, the invariant-frame diagonal
representative, and the two separately solved variable-diagonal one-sided
Green equations  
Strict verdict: **a determinant-one biprojective gauge eliminates both cubic
off-diagonal cross terms exactly and converts the combined class-`H` problem
into two explicit coupled half-density groupoid equations.  No solution of
those coupled equations, uniform big-cell bound, or twisting calculation in
the same representative is certified; Gate 1 remains open.**

## 1. Exact nonlinear coordinate

The product gauges `U_v L_u` and `L_u U_v` each leave one critical cubic
cross term.  Instead put

```text
q(x)=1-u(x)v(x),
D(x)=q(x)^(-1/2) [[1,v(x)],[u(x),1]],
q(x)>=q_*>0.
```

Then `det D=1`, and direct `2x2` algebra gives

```text
D(y)D(x)^(-1)
 =(q(y)q(x))^(-1/2)
   [[1-v(y)u(x), v(y)-v(x)],
    [u(y)-u(x), 1-u(y)v(x)]].
```

Thus the lower critical coordinate is the clean difference `du`, the upper
critical coordinate is the clean difference `dv`, and neither coordinate
contains a base-value cubic term.  The former noncommutative obstruction has
not disappeared for free: it has moved into the scalar terminal
half-density `(q(y)q(x))^(-1/2)`.

The certificate verifies this identity and both determinant identities
exactly over the rationals.

## 2. Exact combined class-H criterion

For a local stable pair define

```text
c_s(x,y)=(u(y)-u(x))/sqrt(q(y)q(x)).
```

Writing `r=a_s/a_u`, the critical lower coordinate cancels the forward
diagonal conjugation exactly if

```text
u(sigma y)-u(sigma x)
 =r(x) sqrt(q(sigma y)q(sigma x)/(q(y)q(x)))
  [u(y)-u(x)].
```

Iteration then gives

```text
R_n(x)^(-1)
 [u(sigma^n y)-u(sigma^n x)]
 /sqrt(q(sigma^n y)q(sigma^n x))
 =c_s(x,y).
```

The conjugated relative matrices converge to `I+c_s E_21`: the diagonal
entries converge to one because the iterated endpoints coalesce, and the
opposite upper entry is contracted by the forward diagonal ratio.

For a local unstable pair, the time-reversed condition is

```text
v(sigma^-1 y)-v(sigma^-1 x)
 =R_minus_1(x)
  sqrt(q(sigma^-1 y)q(sigma^-1 x)/(q(y)q(x)))
  [v(y)-v(x)].
```

It yields the conjugated limit `I+c_u E_12`, where

```text
c_u(x,y)=(v(y)-v(x))/sqrt(q(y)q(x)).
```

Consequently, if the inherited `u,v` are Hölder, `q>=q_*>0`, and `c_s,c_u`
are uniformly Hölder on all local plaques, finite tails produce global
stable and unstable canonical families.  The actual holonomies are obtained
by restoring the endpoint factors `D(y)^(-1)` and `D(x)`.  This is a
sufficient combined class-`H` criterion, not an existence proof.

## 3. What remains physical

The new normal form sharpens the nonlinear target but does not solve it.
The following are still missing:

```text
UNIFORM BIG-CELL LOWER BOUND q>=q_*>0:             NOT CERTIFIED
COUPLED STABLE HALF-DENSITY EQUATION:              NOT CERTIFIED
COUPLED UNSTABLE HALF-DENSITY EQUATION:            NOT CERTIFIED
COMBINED ALL-PLAQUE CLASS-H REPRESENTATIVE:        NOT CERTIFIED
TWISTING IN THAT SAME REPRESENTATIVE:              NOT CERTIFIED
GATE 1:                                            NOT CERTIFIED
```

The next Gate-1 attack is therefore precise: solve the two displayed pair
equations simultaneously, or prove a contraction/implicit-function scheme
for them in a uniform Hölder plaque norm while preserving `q>=q_*`; only
then evaluate the selected homoclinic wedges in the resulting canonical
families.

## 4. Technology check

The official arXiv records for Butler--Park `arXiv:1909.11548` and
Kalinin--Sadovskaya `arXiv:2604.13401` were checked on 2026-07-17.  They
provide the class-`H`/periodic-rigidity context but no theorem that supplies
this coupled half-density solution.  The advance here is exact groupoid
algebra, not a literature promotion.

## 5. Replay

```bash
PYTHONPATH=deliverables python3 -m py_compile \
  deliverables/cm2_gate1_biprojective_half_density_frontier_cert.py \
  deliverables/cm2_gate1_biprojective_half_density_frontier_verifier.py

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate1_biprojective_half_density_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate1_biprojective_half_density_frontier_verifier.py \
  --self-test

# Expected exit 2: the coupled solution and Gate 1 remain open.
PYTHONPATH=deliverables python3 \
  deliverables/cm2_gate1_biprojective_half_density_frontier_verifier.py
```
