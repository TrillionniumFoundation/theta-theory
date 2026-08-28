# CM2 Gate 2: common two-branch rectangle audit

Date: 2026-07-15 (Asia/Shanghai)  
Model: frozen centered rational fixed-section pilot  
Precision: 900-bit Arb through `python-flint==0.9.0`  
Verdict: **a physical short-QNL full crossing is certified in a rectangle
that also contains the 96-collision fixed point; the specified 96-word
full-height branch is impossible in both audited affine Perron charts and
in one explicitly quantified near-vertical graph class; a curvilinear
stable-saturated two-branch/full-mass quotient remains OPEN / NO-GO**

## 1. Exact scope

This calculation asks whether the already certified QNL period-two fixed
point and the certified 96-solid-collision shadow-loop fixed point can be
put into one product rectangle carrying two physical branches.

The answer has three separate layers:

1. A common rectangle and a regular two-collision QNL full crossing exist.
2. The natural attempt to use the fixed 96-collision word as a second
   full-height vertical branch fails at a forced mixed corner.  This is
   proved separately in the QNL and loop Perron charts.
3. This failure does not exclude a genuinely curvilinear stable-saturated
   branch, another return word, or a different nonlinear product chart.

The third distinction is essential.  The certificate does **not** claim
that every two-branch horseshoe is impossible.

## 2. Common product rectangle

In the gray QNL Perron coordinates

```text
delta s = u+v,
delta p = k_A (u-v),
```

the QNL point is `(0,0)`.  The reversible 96-word fixed point has physical
momentum zero and arclength displacement `2 a_*`, hence it is exactly
`(a_*,a_*)`, where

```text
a_* = -8.293762194329601963437427046452104... * 10^-15.
```

Set

```text
c = a_*/2,
r = 4.2 * 10^-15,
I = [c-r,c+r].
```

The 900-bit enclosure gives

```text
I subset
[-8.3468810971648010*10^-15,
  5.3118902835199020*10^-17].
```

Both `0` and `a_*` lie strictly in `I`, so `R=I x I` contains both fixed
points.  More generally, every axis-aligned product rectangle containing
the two points contains all four coordinate corners, including

```text
P_mix=(a_*,0).                                             (2.1)
```

Any centered common square has half-width at least

```text
|a_*|/2 > 4.14*10^-15.                                    (2.2)
```

The two Perron slopes are close but rigorously distinct:

```text
k_loop-k_A = -3.744113314950599...*10^-25,
|(k_A-k_loop)/(k_A+k_loop)|
             = 2.761335982891948...*10^-26.               (2.3)
```

The loop derivative has common-QNL-chart vertical shear of magnitude
greater than `10^27`.  Equation (2.3) and this shear are typing diagnostics;
they are not by themselves used as a no-go theorem.

## 3. The physical short-QNL branch

Inside `R`, take the full-height source strip

```text
S_Q = [-8*10^-16, 10^-17] x I.                            (3.1)
```

The exact gray-white-gray return is evaluated with interval first and
second derivatives.  Correlated mean-value bounds give

```text
left u-face image   = -8.878161547*10^-15 +/- 5.31*10^-25,
right u-face image  =  1.10977019 *10^-16 +/- 8.27*10^-25,
full stable image   subset
[-7.55911556691*10^-16, 8.57104927691*10^-18].            (3.2)
```

Thus the left face lies strictly below `I`, the right face lies strictly
above `I`, and the entire stable image lies strictly inside `I`.

Every point of (3.1) follows the intended two solid collisions as genuine
first hits.  The certified uniform lower margins are

```text
flight          > 0.18710678117,
discriminant    > 0.025599999999,
incidence       > 0.999999999,
clearance       > 0.3649827580.                            (3.3)
```

The finite lift test is exhaustive here: all flight endpoints stay in the
open unit square, hence every omitted lift outside `[-3,3]^2` is farther
than the largest disk radius from the convex flight segment.

On the full strip the derivative enclosure is

```text
DF_Q subset [[11.09770193 +/- 4.83*10^-9, +/-1.16*10^-10],
             [          +/-1.02*10^-9, 0.090108746 +/-5.43*10^-10]].
```

For the declared slope `10^-9`, the unstable cone maps to slope below
`1.00*10^-10`, and the stable inverse cone maps to slope below
`1.851*10^-11`.  Therefore (3.1)--(3.3) certify a regular hyperbolic
short-QNL full crossing of the common rectangle.

This is only one branch.  It does not create a two-symbol quotient.

## 4. Forced mixed-corner obstruction for the 96 word

Consider a full-height vertical source strip in `R` whose unstable interval
contains the loop point `u=a_*`.  Because its stable interval is all of `I`
and `0 in I`, it necessarily contains `P_mix` from (2.1).

### 4.1 QNL Perron chart

At `P_mix`, the physical initial state is

```text
theta = pi/4 + a_*/R_G,
p     = k_A a_*.
```

The complete first-hit replay certifies the first 69 collisions of the
declared 96 word.  At the intended 70th target `G[1,0]`, the unsquared
line-circle test has discriminant

```text
D_70 = -0.29709078292987004589... < -0.29.                (4.1)
```

The target circle is therefore not met at all.  The prescribed 96-word
branch cannot be physical on such a full-height strip.

### 4.2 Loop Perron chart

Changing the affine product axes to the exact loop Perron slope does not
repair the same construction.  The corresponding mixed corner has

```text
theta = pi/4 + a_*/R_G,
p     = k_loop a_*.
```

It follows 73 certified first hits, then misses the intended 74th target
`G[0,0]` with

```text
D_74 = -0.21453706238702593528... < -0.21.                (4.2)
```

Equations (4.1)--(4.2) rule out the fixed 96-word full-height vertical
branch in the two natural affine Perron charts audited here.  They do not
quantify over arbitrary coordinate changes.

## 5. A quantified near-vertical graph extension

There is a small but rigorous extension beyond exactly vertical fibres.
Let a hypothetical full-height graph in either audited chart be

```text
u=g(v),       g(a_*)=a_*,       Lip(g)<=10^-100.           (5.1)
```

Because the graph spans `v=0`, (5.1) forces

```text
|g(0)-a_*| <= 10^-100 |a_*| < 8.294*10^-115.              (5.2)
```

The certificate inflates the right side of (5.2) by one percent and
replays the complete interval of possible crossing states.  On that whole
interval it obtains

```text
QNL chart:  D_70 = -0.297090783 +/- 7.75*10^-10 < -0.29,
loop chart: D_74 = -0.215       +/- 6.69*10^-4  < -0.21.  (5.3)
```

Thus the near-vertical class (5.1) is also impossible for this fixed word.
This is a conditional obstruction, not a stable-plaque construction.  The
bound `10^-100` is intentionally reported exactly; it must not be enlarged
to the much wider local cone bounds proved elsewhere.

## 6. What remains open

The surviving route is not affine.  To obtain a genuine second branch one
must construct and validate a stable-saturated curvilinear product strip
whose leaves avoid the bad mixed-corner interval while retaining:

1. the full prescribed first-hit word (or a separately certified return
   word);
2. source and target stable saturation;
3. an interval-indexed invariant plaque family;
4. two onto quotient inverse branches on one reference interval;
5. a full-mass countable return partition and its physical density;
6. the complete reverse-weight/projective-map/tail registry;
7. stopped-parent pair-energy drift and PPE;
8. same-carrier endpoint and normalized amplitude typing.

None of these layers follows from the short-QNL crossing.  In particular,
the current result does not instantiate actual SRB/Gibbs quotient weights
or close physical Gate 2.

## 7. Reproduction and audit discipline

Run the positive certificate with

```bash
PYTHONPATH=deliverables \
  /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate2_two_branch_common_rectangle_obstruction_cert.py
```

Expected terminal labels include

```text
COMMON_GRAY_PERRON_CHART: CERTIFIED
SHORT_QNL_COMMON_RECTANGLE_FULL_CROSS: CERTIFIED
MIXED_CORNER_INTENDED_COLLISION_70: IMPOSSIBLE
LOOP_PERRON_MIXED_CORNER_INTENDED_COLLISION_74: IMPOSSIBLE
NARROW_CONE_FULL_HEIGHT_PLAQUE_CLASS: RULED_OUT
AUDITED_AFFINE_TWO_BRANCH_COMMON_RECTANGLE_ROUTE: RULED_OUT
CURVILINEAR_STABLE_SATURATED_TWO_BRANCH_HORSESHOE: NOT_CERTIFIED
FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT_CERTIFIED
PHYSICAL_GATE2: NOT_CERTIFIED
```

The fail-closed manifest verifier separately replays the exact 96-word
predecessor, fixes all source hashes, rejects promotion of any missing
physical layer, and exits `2` on the live incomplete snapshot.  Frozen
v51/v52 files are not modified.
