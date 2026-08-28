# CM2 Gate 2: two-branch common-rectangle assault

Date: 2026-07-15 (Asia/Shanghai)  
Model: frozen centered rational fixed-section pilot  
Scope: combine the short QNL return and the certified 96-collision shadow
return in one gray Perron rectangle; do not edit v51/v52 or the shared log  
Verdict: **the short QNL branch full-crosses an explicit common rectangle,
and candidate source strips are disjoint, but the fixed 96-word full-height
strip is rigorously impossible in the QNL and loop affine Perron charts
audited here; arbitrary coordinates, a curvilinear two-branch horseshoe, and
Gate 2 remain OPEN / NO-GO**

## 1. Executive result

The two fixed points can be expressed exactly in one gray Perron chart.  In
the QNL chart

```text
delta s=u+v,          delta p=k_A(u-v),
```

they are

```text
p_A=(0,0),
z_*=(a_*,a_*),
a_*=-8.2937621943296019634...*10^-15.                     (1.1)
```

Thus any axis-aligned rectangle containing both must have unstable and
stable half-width at least

```text
|a_*|/2=4.1468810971648009817...*10^-15.                  (1.2)
```

The certificate chooses the nearly minimal common rectangle

```text
R_c=[c-r,c+r]^2,
c=a_*/2,               r=4.2*10^-15,                     (1.3)
```

whose coordinate interval is

```text
[-8.3468810971648009817...*10^-15,
  5.3118902835199018281...*10^-17].                       (1.4)
```

On `R_c`, the two-collision QNL return has the full-height source strip

```text
S_Q=[-8*10^-16,10^-17] x [c-r,c+r].                       (1.5)
```

All physical first hits, both unstable face signs, stable entry, and both
cone inequalities are certified at 900 bits.  The output enclosures are

```text
left unstable face   = -8.878161547*10^-15 +/- 5.31*10^-25,
right unstable face  =  1.10977019 *10^-16 +/- 8.27*10^-25,
stable image subset
 [-7.55911556690278*10^-16, 8.57104927690187*10^-18].     (1.6)
```

Comparing (1.6) with (1.4) proves a genuine full-cross.

A candidate 96-word source interval can be placed around `u=a_*` with

```text
[a_*-10^-69,a_*+8*10^-68].                                (1.7)
```

It is disjoint from (1.5) by more than

```text
7.4937621943296*10^-15.                                   (1.8)
```

The construction nevertheless stops rigorously before a two-branch
horseshoe.  A full-height axis-aligned vertical strip containing `z_*` must
also contain the mixed corner

```text
P_mix=(u,v)=(a_*,0).                                      (1.9)
```

In the QNL Perron chart, `P_mix` follows the intended 96-word for 69
collisions, but the intended 70th target `G(1,0)` has

```text
discriminant=-0.29709078292987004589...< -0.29.           (1.10)
```

Hence that collision does not exist and the declared word is not physical
on the required strip.  This is an exact negative discriminant, not failed
interval convergence.

Nor does changing to the loop's own Perron chart rescue an affine vertical
strip.  Its corresponding mixed corner follows 73 intended collisions, but
the intended 74th target `G(0,0)` has

```text
discriminant=-0.21453706238702593528...< -0.21.            (1.11)
```

Therefore the proposed affine two-branch common-rectangle route is ruled out
in both natural Perron eigencharts audited here.  This does not rule out an
arbitrary affine coordinate choice.

This does not rule out a **curvilinear**, stable-saturated branch following
the actual stable manifold of `z_*`.  Constructing that object now requires
continuing the certified stable plaque from radius `10^-43` through a stable
distance at least `8.29*10^-15`, a factor greater than `8.29*10^28`, while
retaining the whole 96-collision word.  No such continuation is currently
certified.

## 2. Common-coordinate identity

The QNL fixed point is the gray normal point, so its Perron coordinates are
zero.  The shadow-loop point is represented in physical coordinates by

```text
delta s=2a_*,             delta p=0.
```

Solving

```text
delta s=u+v,
delta p=k_A(u-v)
```

gives (1.1) exactly.  The same conclusion holds if `k_A` is replaced by the
loop slope because `delta p=0`.

For any Cartesian product `I_u x I_v` containing both `(0,0)` and
`(a_*,a_*)`, both intervals contain `0` and `a_*`.  Hence the product also
contains `(a_*,0)`.  If a vertical source strip spans the full stable
interval `I_v` and its unstable interval contains `a_*`, it necessarily
contains (1.9).  This is the elementary corner lemma used by the
falsification certificate.

The common half-width lower bound (1.2) follows independently of where the
rectangle is centred.  The midpoint choice (1.3) is optimal up to the strict
margin

```text
4.2*10^-15-|a_*|/2=5.3118902835...*10^-17.
```

## 3. Certified short-QNL branch

The source (1.5) contains `p_A` and lies strictly inside `R_c`.  A direct
two-collision `G(0,0)->W(0,0)->G(0,0)` Jet2 replay evaluates the whole
source.  Mean-value forms are used for the face images, so the exact return
correlation is not discarded by a raw interval evaluation.

The strict physical margins on the entire strip are

```text
minimum flight        > 0.18710678118,
minimum discriminant  > 0.02559999999998,
minimum incidence     > 0.99999999998,
minimum clearance     > 0.364982758415.                   (3.1)
```

The derivative enclosure is

```text
DF_Q(S_Q) subset
[[11.09770193 +/- 4.83*10^-9, +/-1.16*10^-10],
 [       +/-1.02*10^-9,       0.090108746 +/-5.43*10^-10]].
                                                                    (3.2)
```

For unstable and stable-inverse cone slopes `10^-9`, the respective image
slopes satisfy

```text
9.9993*10^-11 < 10^-9,
1.8504*10^-11 < 10^-9.                                    (3.3)
```

Together, (1.6), (3.1), and (3.3) certify one clean local QNL branch across
the common rectangle.  This is a positive result, but one branch alone does
not make a two-symbol horseshoe.

## 4. The two Perron axes are close but not identical

The loop slope and QNL slope satisfy the strict enclosure

```text
k_loop-k_A
=-3.7441133149505990395...*10^-25.                        (4.1)
```

Thus the loop stable direction has slope, in QNL `(u,v)` coordinates,

```text
|du/dv|=2.7613359828919487785...*10^-26.                  (4.2)
```

This number looks tiny, but the loop expansion exceeds `10^53`.  In the
QNL common chart its exact fixed-point derivative becomes

```text
D_loop^Q =
[[ 1.0722583849647160...*10^53, -2.9608656613606777...*10^27],
 [ 2.9608656613606777...*10^27, -81.759448912244...       ]].
                                                                    (4.3)
```

So an affine QNL-vertical segment is not a loop-stable segment.  The
vertical shear in (4.3) already rules out reusing the microscopic loop
covering certificate unchanged on the common height.

Equation (1.10) is stronger than this linear warning: it evaluates the
actual nonlinear billiard word at the forced mixed corner and proves that
the prescribed target ceases to exist.

## 5. Loop-Perron control experiment

One might instead declare the loop Perron basis to be the common basis, so
that the derivative (4.3) is diagonal at `z_*`.  Fixed-point coordinates
remain `(0,0)` and `(a_*,a_*)`; hence the same Cartesian corner lemma forces
the loop-Perron point `(a_*,0)` into a full-height affine loop strip.

The certificate propagates that point directly, using momentum

```text
p=k_loop*a_*.
```

Every one of the first 73 intended collisions and its exhaustive first-hit
test passes.  The next intended line-circle discriminant is (1.11), so the
word still fails.  This shows that the obstruction is not merely the tiny
eigenslope difference (4.1): nonlinear stable-manifold curvature matters
over the required `8.29*10^-15` height.

The audit also allows a quantified amount of curvature.  If a full-height
graph `u=g(v)` passes through `(a_*,a_*)` and satisfies

```text
Lip(g)<=10^-100,                                          (5.1)
```

then its crossing at `v=0` must lie within
`10^-100|a_*|` of `u=a_*`.  The certificate replays the entire resulting
crossing interval, not merely its centre.  It still obtains

```text
QNL-Perron collision 70 discriminant = -0.297090783 +/- 7.75*10^-10,
loop-Perron collision 74 discriminant = -0.215       +/- 6.69*10^-4,
```

with strict upper bounds below `-0.29` and `-0.21`, respectively.  Hence
this narrow-cone full-height plaque class is ruled out as well.  The earlier
local loop certificate only places the stable tangent in a much wider
`10^-53` cone, so (5.1) does not eliminate every curvilinear stable plaque.

## 6. Exact status of the requested horseshoe

| layer | status |
|---|---:|
| common rectangle containing `p_A,z_*` | certified |
| short-QNL full-height source strip | certified |
| short-QNL full physical word | certified |
| short-QNL face covering/stable entry | certified |
| short-QNL stable/unstable cones | certified |
| disjoint candidate unstable source intervals | certified |
| QNL-chart affine 96-word full-height strip | ruled out |
| loop-chart affine 96-word full-height strip | ruled out |
| full-height graph class with `Lip(g)<=10^-100` | ruled out |
| audited QNL/loop affine common-rectangle route | ruled out |
| arbitrary affine-coordinate two-branch horseshoe | not certified |
| curvilinear stable-saturated 96 branch | not certified |
| two-symbol Cantor product | not certified |
| two onto stable-quotient inverse branches | not certified |
| full-mass physical quotient | not certified |
| physical Gate 2 | not certified |

No Cantor product, quotient branch, or SRB weight is inferred from the one
surviving QNL branch.  In particular, the prior one-branch Dirac-kernel
obstruction is not bypassed.

## 7. What remains possible

The negative certificate is specific to full-height **affine** vertical
strips in the two natural Perron eigencharts.  A viable continuation would
have to use a curvilinear strip centred on an actual stable plaque of the
96-loop point.  It must provide, in one proof:

1. a multi-chart validated continuation of `W^s(z_*)` over stable distance
   at least `8.29*10^-15`;
2. a tube around that graph with unstable width of order `10^-68` or less;
3. all 96 physical first hits on the entire curved tube;
4. two unstable face signs into `R_c`, stable entry, and cone invariance;
5. disjointness from (1.5) and a common local product/holonomy structure.

Even success would yield only a finite clean subsystem.  It could not be
promoted to the full-mass SRB/Gibbs quotient without a complete countable
return partition, physical conditional density, branch weights, and tail.

## 8. Reproduction

```bash
/tmp/cm2-flint-venv/bin/python -m py_compile \
  deliverables/cm2_gate2_two_branch_common_rectangle_obstruction_cert.py \
  deliverables/cm2_gate2_two_branch_common_rectangle_manifest_verifier.py

/tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_gate2_two_branch_common_rectangle_obstruction_cert.py

python3 \
  deliverables/cm2_gate2_two_branch_common_rectangle_manifest_verifier.py \
  --self-test

python3 \
  deliverables/cm2_gate2_two_branch_common_rectangle_manifest_verifier.py

sha256sum -c \
  deliverables/cm2-gate2-two-branch-common-rectangle-manifest-2026-07-15.sha256

sha256sum -c deliverables/cm2-v52-manifest.sha256
```

The arithmetic certificate and verifier self-test must exit zero.  The live
physical verifier must exit two by design.  Final verdict:

```text
SHORT_QNL_COMMON_RECTANGLE_FULL_CROSS: CERTIFIED
CANDIDATE_SOURCE_STRIPS_DISJOINT: CERTIFIED
QNL_PERRON_FIXED_96_WORD_FULL_HEIGHT_BRANCH: RULED_OUT
LOOP_PERRON_FIXED_96_WORD_FULL_HEIGHT_BRANCH: RULED_OUT
AUDITED_AFFINE_TWO_BRANCH_COMMON_RECTANGLE_ROUTE: RULED_OUT
ARBITRARY_AFFINE_COORDINATE_TWO_BRANCH_HORSESHOE: NOT CERTIFIED
CURVILINEAR_STABLE_SATURATED_TWO_BRANCH_HORSESHOE: NOT CERTIFIED
FULL_MASS_COUNTABLE_RETURN_PARTITION: NOT CERTIFIED
PHYSICAL_GATE2: OPEN / NO-GO
```
