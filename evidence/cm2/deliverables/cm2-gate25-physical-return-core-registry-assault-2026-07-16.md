# CM2 Gates 2/5: physical return-core registry assault

Date: 2026-07-16 (Asia/Shanghai)  
Model: centred rational two-disk torus pilot  
Frozen inputs: the 441,280-key envelope, exact first-hit candidate reduction,
and eleventh-round Gate-2 collision-key frontier were read only

## Verdict

Gate 5 remains **`NOT_CERTIFIED`**, but the first missing field in the
441,280-key schema is no longer empty everywhere.

- **24 distinct candidate keys are now rigorously nonempty**, uniformly on
  the full parameter window `|s|<=1/400`.
- Each key contains an explicit positive compact central-homogeneity core.
  The 24 cores carry seven strictly typed **local seeds**: exact physical wall
  words, source/target endpoint collision charts, collision-SRB area
  Jacobian one, zero log-area-Jacobian distortion, and a local full-return
  dynamic-test pullback cost strictly below `158`.
- Their normalized collision-SRB mass is strictly larger than

  ```text
  147/550000 = 0.0002672727...
  ```

  This is positive physical mass, not Borel label cardinality.

Only the full-key nonemptiness field is completed by these cores.  The seven
local seeds are not seven completed `(word,homogeneous level,roof level)`
operator fields: in particular, the four roof-two words still lack their
intermediate transparent-wall charts and levelwise prefix/suffix costs, and
the area-Jacobian identities are not unstable-curve Jacobian estimates.

The exact total number of nonempty keys, maximal word domains, the global
homogeneity partition, boundary-`Z`, all face fields, complete 18-field
operator blocks, three CM2 norm lifts, Kac and operator phase remain open.

Gate 2 also remains **`NOT_CERTIFIED`**.  These are two-dimensional collision
cores, not stable-saturated Young rectangles.  They supply no stable
projection, `rho`, reverse weights, endpoint carrier, native stopping or PPE.

## 1. The 24 physical keys

The certificate uses canonical collision coordinates

```text
(normal chart coordinate t, p=sin(phi), table parameter s).
```

Every box is compared with the complete retained first-hit list in its
source chart, using 384-bit Arb arithmetic.

### 1.1 Eight axial translate keys

For each source obstacle `G,W` and chart `E,W,N,S`, take

```text
t in [1/100,1/50],
p in [-1/500,1/500],
s in [-1/400,1/400].
```

The four gray keys hit the adjacent gray lift and have no transparent-wall
record:

```text
G:E -> G[1,0],   G:W -> G[-1,0],
G:N -> G[0,1],   G:S -> G[0,-1].
```

The gray disk straddles the grid wall, so each short inter-lift gap remains
inside one open cell.  The four white keys hit the adjacent white lift after
exactly one clean wall event:

```text
W:E -> W[1,0]   with X+,
W:W -> W[-1,0]  with X-,
W:N -> W[0,1]   with Y+,
W:S -> W[0,-1]  with Y-.
```

The transverse endpoint intervals remain strictly in one open grid cell, so
there is no unregistered corner or second wall event.

### 1.2 Sixteen diagonal two-obstacle keys

For each diagonal quadrant, the two adjacent dominant-normal charts use

```text
|t| in [69/100,7/10] with the prescribed quadrant sign,
p in [-1/50,1/50],
s in [-1/400,1/400].
```

There are eight `G->W` and eight `W->G` chart-target keys.  Their targets are
the appropriate diagonal lifts among

```text
W[0,0], W[-1,0], W[0,-1], W[-1,-1],
G[1,1], G[0,1], G[1,0], G[0,0].
```

Every flight stays in one open lifted unit square and has empty wall record.
The two source charts per diagonal occupy opposite sides of the exact chart
seam and are disjoint in physical normal angle.

Thus the registered roof histogram is

| roof | 1 | 2 |
|---:|---:|---:|
| nonempty keys | 20 | 4 |

It creates 28 physical roof-level prefix/suffix pairs and 52 endpoint split
positions.  These are symbolic slot counts.  For the four roof-two keys the
intermediate transparent-wall chart and its two levelwise operator costs are
not constructed here.

## 2. Strict first-hit and homogeneity margins

For every core, the selected circle root is strictly positive and below the
frozen horizon `3`.  All other retained candidates are certified either
absent/behind or strictly later.  This is a domain proof against the complete
finite candidate universe, not a center-point sample.

Writing `p_+` for the target momentum, the dependency-reduced contact formula
gives, throughout all 24 boxes,

```text
|p_-|<3/10,       |p_+|<3/10,
cos(phi_-)>19/20, cos(phi_+)>19/20.
```

Hence each rectangle is a compact central regular homogeneity core at both
ends.  A target local semicircle chart is fixed by an integer direction
vector, with target normal dot direction strictly greater than `1/3`.

These are genuine physical homogeneous **subblocks**.  They are not claimed
maximal inside the corresponding word domain.

## 3. Seven local seeds, not seven completed word fields

The following seven local data types are bound on every compact core:

1. nonempty domain proof;
2. compact central physical homogeneity **subcore**;
3. source endpoint collision chart;
4. target endpoint collision chart;
5. collision-SRB area-Jacobian identity `1` in `(r,p)`;
6. log-area-Jacobian identity `0`;
7. local full-collision-branch `C^alpha` test pullback seed `<158`,
   `0<alpha<=1`.

For the last item, the exact one-collision Birkhoff matrix is

```text
-1/cp_1 * [[tau*kappa_0+cp_0, tau],
 [tau*kappa_0*kappa_1+kappa_0*cp_1+kappa_1*cp_0,
  tau*kappa_1+cp_1]].
```

The already exact numerator bound is `2391/16<150`; here both incidence
cosines exceed `19/20`, hence forward and reverse infinity norms are

```text
<150*(20/19)<158.
```

The area-Jacobian statement is deliberately typed: billiard invariance gives
`dr dp` exactly, but this is not an unstable-curve Jacobian or a global
standard-family distortion estimate.  It therefore does **not** fill schema
fields 5--6.  Likewise a compact central subcore does not fill the complete
homogeneity-subbranch table, and endpoint charts do not fill every roof-level
prefix/suffix chart.  Of the 18 immutable full-key fields, the only one
decided on each of these 24 keys is field 1: the key is nonempty.

## 4. Positive physical mass

On a dominant normal chart, `dr=R dtheta` and

```text
dtheta/dt=(1-t^2)^(-1/2) >= 1.
```

The 24 word keys are distinct and the frozen regular-word domain contract is
a partition.  Since every core is rigorously contained in its displayed key,
their domains are pairwise disjoint; no collision mass is counted twice.
Summing the 24 source rectangles therefore gives the rational
unnormalized lower bound

```text
sum R_source Delta t Delta p = 273/156250.
```

The total collision volume is `4*pi*(R_G+R_W)`.  Using the strict rational
upper bound `pi<22/7` yields

```text
mu_collision(union of cores) > 147/550000.
```

This is the first executable positive-mass physical subregistry inside the
441,280 candidate-key envelope.

## 5. Why no complete Gate-5 promotion follows

The cores do not decide the rest of any word fibre.  In particular, the
following remain absent:

- maximal connected nonempty word domains and their full homogeneity cuts;
- global one-step cut-growth/`Z` after characteristic restriction;
- face transversality, face `C2`, coarea-density and moving-boundary DQ data;
- global regular-density, standard-family, flux-face and dynamic-test costs;
- operator phase blocks, complete Kac typing and all three CM2 norm lifts.

Accordingly the complete 18-field physical operator-block count remains
strictly `0`.  Each registered core has seven useful local seeds, but only
one full-key schema field is decided.

## 6. Gate-2 nonpromotion

The new lower bound is collision-SRB mass on the two-dimensional standard
section `N=G sqcup W`.  The earlier `>0.903` gap is the unsaturated fraction
of a different declared common rectangle.  Without a stable saturation and
projection there is no legitimate map between these two mass statements, so
the `0.903` figure is unchanged.

Moreover, refining an invertible two-dimensional collision branch by these
physical keys still leaves one physical predecessor at each target.  Its
reverse conditional remains Dirac and its two-copy energy coefficient
remains one.  The registry therefore supplies none of

```text
Lambda_A, pi^s, rho, h_a, p_a, endpoint maps, native stopping, PPE.
```

## 7. Exact remaining boundary

```text
AT LEAST 24 PHYSICAL NONEMPTY RETURN KEYS:          CERTIFIED
POSITIVE COLLISION-SRB CORE MASS >147/550000:       CERTIFIED
SEVEN TYPED LOCAL SEEDS ON EACH REGISTERED CORE:    CERTIFIED
FULL-KEY NONEMPTY FIELD ON EACH OF 24 KEYS:         CERTIFIED
SEVEN COMPLETE WORD/LEVEL SCHEMA FIELDS:            NOT CERTIFIED
ROOF-TWO INTERMEDIATE WALL LEVELS:                  NOT CERTIFIED

EXACT TOTAL NONEMPTY KEY COUNT:                     NOT CERTIFIED
MAXIMAL HOMOGENEOUS WORD PARTITION:                 NOT CERTIFIED
COMPLETE 18-FIELD OPERATOR REGISTRY:                NOT CERTIFIED
THREE CM2 NORM LIFTS / KAC / OPERATOR PHASE:        NOT CERTIFIED
STABLE QUOTIENT / rho / REVERSE WEIGHTS / PPE:      NOT CERTIFIED
GATE 2:                                             NOT CERTIFIED
GATE 5:                                             NOT CERTIFIED
```

## 8. Reproduction

```bash
PY=/tmp/cm2-flint-venv/bin/python

PYTHONPATH=deliverables $PY -m py_compile \
  deliverables/cm2_gate25_physical_return_core_registry_cert.py \
  deliverables/cm2_gate25_physical_return_core_registry_verifier.py

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_physical_return_core_registry_verifier.py \
  --replay --integrity-only

PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_physical_return_core_registry_verifier.py \
  --self-test

# Expected exit 2: neither Gate 2 nor Gate 5 is complete.
PYTHONPATH=deliverables $PY \
  deliverables/cm2_gate25_physical_return_core_registry_verifier.py
```

Replay/integrity exits zero, eleven independent mutations are rejected, and
live mode exits two by design.
