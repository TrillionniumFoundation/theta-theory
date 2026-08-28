# CM2 Gates 2/5: roof-two transparent-wall chart assault

Date: 2026-07-16 (Asia/Shanghai)  
Frozen input: twelfth-round physical return-core registry  
Strict verdict: **the four missing roof-two intermediate transparent-wall
charts and all local roof-level chart slots on the 24 certified compact cores
are now explicit; the full-key 18-field registry, Gate 2 and Gate 5 remain
`NOT_CERTIFIED`**

## 1. Exact advance

The frozen physical registry contains 20 roof-one cores and four roof-two
cores.  The latter are the axial white-to-white translate keys

```text
W:E -> W[ 1, 0] with X+,
W:W -> W[-1, 0] with X-,
W:N -> W[ 0, 1] with Y+,
W:S -> W[ 0,-1] with Y-.
```

Their source boxes are uniform on `|s|<=1/400`:

```text
t in [1/100,1/50],   p=sin(phi) in [-1/500,1/500].
```

The previous stack proved the physical first hit and the unique wall token,
but did not construct the intermediate section chart.  The new certificate
does so with 384-bit Arb first-order automatic differentiation.

## 2. Oriented wall coordinates

Write `q=(q_x,q_y)` for the source collision point and `u=(u_x,u_y)` for
the outgoing unit velocity.  On a vertical wall `x=m`, use

```text
tau_w=(m-q_x)/u_x,
z=q_y+tau_w u_y,
eta=u_y.
```

On a horizontal wall `y=m`, use

```text
tau_w=(m-q_y)/u_y,
z=q_x+tau_w u_x,
eta=u_x.
```

Thus `(z,eta)` is the standard oriented transparent-section coordinate:
`z` is tangent to the wall and `eta` is the tangential velocity component.
The sign of the complementary normal velocity is fixed by the registered
token.  A transparent wall changes neither position nor velocity; it is not
a collision or a singularity.

## 3. Uniform strict geometry

Every one of the four physical roof-two boxes satisfies

```text
1/3    < tau_w                    < 7/20,
33/100 < tau_target-tau_w         < 7/20,
2/3    < tau_target               < 7/10,
1/2    < z                        < 53/100,
|u_normal| > 99/100,
|eta|      < 1/40.
```

The wall coordinate is therefore at distance strictly greater than `47/100`
from either integer corner.  The crossing is unique, uniformly transverse,
and cannot be a simultaneous grid-corner event.

## 4. Local chart costs

Differentiate the displayed wall map in the frozen local source variables
`(t,p)`.  On all four boxes,

```text
|det D_(t,p)(z,eta)| > 3/20,
||D_(t,p)(z,eta)||_infinity < 3,
||D_(z,eta)(t,p)||_infinity < 10.
```

This proves that each intermediate wall chart is a uniform local
diffeomorphism on the compact physical core.  The bounds are explicitly
typed in `(t,p)` and `(z,eta)` coordinates.  They are not unstable-curve
Jacobian/distortion estimates and are not CM2 strong-operator costs.

The source-to-wall part obeys the displayed `<3`/`<10` bounds without
subdivision.  The target collision chart cannot be borrowed from the reverse
compact source core: the target point is only known to lie in a larger local
central chart.  The certificate therefore computes the suffix directly.
Each source box is split `2 x 2 x 2` in `(t,p,s)`, giving 32 strict cells in
total.  On every cell, the dependency-reduced circle contact formula proves

```text
|t_target|,|p_target| <1/4,
|det D_(t,p)(t_target,p_target)| >1/10,
||D_(z,eta)(t_target,p_target)||_infinity <20,
||D_(t_target,p_target)(z,eta)||_infinity <20.
```

The target dominant-normal chart is `W:W`, `W:E`, `W:S`, or `W:N` for source
chart `W:E`, `W:W`, `W:N`, or `W:S`, respectively.  This is a direct
wall-to-target certificate; it makes no false assumption that the target
belongs to the small reverse source rectangle.

## 5. What becomes physical rather than symbolic

For a word of roof `r`, the frozen namespace has `r` roof-level
prefix/suffix pairs and `r+1` split slots.  The arithmetic is

```text
20*1 + 4*2 = 28 local roof-level prefix/suffix pairs,
20*2 + 4*3 = 52 local split-chart slots.
```

The 20 roof-one cores already had source and target collision charts.  The
four new wall charts and 32 directly certified suffix cells now bind all 28
local pairs and all 52 local split slots to physical charts on the 24
registered compact cores.  They are no longer merely symbolic slots at this
core-local layer.

This does **not** fill full-key schema fields 3--4.  A compact central core is
not the maximal homogeneous domain of its return key, and the chart costs
have not been propagated to every homogeneous subbranch.  Therefore the
immutable full-key completion count remains

```text
completed fields on each of the 24 keys: 1 (NONEMPTY only),
complete 18-field physical operator blocks: 0.
```

## 6. Gate-2 nonpromotion

The intermediate wall sections live inside four two-dimensional collision
cores.  They do not construct a stable-saturated Young base, a stable
projection, quotient density `rho`, onto quotient inverse branches, physical
reverse weights, native stopping, or PPE.  In particular, adding a
transparent-section chart does not turn the invertible collision-key kernel
into a nontrivial stable quotient.

## 7. Exact remaining boundary

```text
FOUR ROOF-TWO INTERMEDIATE WALL CHARTS:             CERTIFIED
ALL 28 CORE-LOCAL ROOF-LEVEL CHART PAIRS:           CERTIFIED
ALL 52 CORE-LOCAL SPLIT-CHART SLOTS:                CERTIFIED
ROOF-TWO WALL-ADJACENT LOCAL CHART COST <20:        CERTIFIED

MAXIMAL HOMOGENEOUS WORD DOMAINS:                   NOT CERTIFIED
FULL-KEY INVERSE-JACOBIAN / DISTORTION / Z:         NOT CERTIFIED
FACE / DQ / THREE CM2 STRONG OPERATOR FIELDS:       NOT CERTIFIED
COMPLETE 18-FIELD OPERATOR BLOCK COUNT:             0
STABLE QUOTIENT / rho / REVERSE KERNEL / PPE:       NOT CERTIFIED
GATE 2:                                             NOT CERTIFIED
GATE 5:                                             NOT CERTIFIED
```

The next useful Gate-5 step is to enlarge these compact cores to maximal
homogeneous word components and bind the physical homogeneity table,
inverse-unstable-Jacobian, log-distortion and one-step cut-`Z` fields before
attempting the three CM2 lifts.

## 8. Reproduction

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables $PY -m py_compile \
  deliverables/cm2_gate25_roof_two_wall_chart_frontier_cert.py \
  deliverables/cm2_gate25_roof_two_wall_chart_frontier_verifier.py

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_roof_two_wall_chart_frontier_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_roof_two_wall_chart_frontier_verifier.py \
  --self-test

# Expected exit 2: full-key blocks, stable quotient and both gates stay open.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_roof_two_wall_chart_frontier_verifier.py
```

Replay/integrity exits zero, all twelve mutations are rejected, and the live
default exits two by design.
