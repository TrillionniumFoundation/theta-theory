# CM2 Round129 — positive-Borel rank-three recut/field stratum

Date: 2026-07-24

Verdict: **VERIFIED for one explicit positive-Borel local family carrying
F1–F13 and F16 on every exact fibre and all 24 common ranks.  This is a local
14/18 stratum, not a global Gate5 block.**

## Positive-Borel collar

Round129 thickens the frozen Round121 anchor in the analytic miss coordinate

```text
lambda = b3
c0     = 1/16384
center = 3/65536
radius = 2^-512
```

The exact closed collar lies strictly inside the frozen Round113 relative
interior and one Round117 operator cell.  On the BYPASS sheet,

```text
F(t,c0,lambda) = Delta3(t,c0) + (16/625) lambda^2 = 0.
```

The independent 4096-bit verifier establishes strict root-face signs
`(+,-)`, `-8 < F_t < -7`, and
`1/500000 < F_lambda < 3/1000000`.  It also checks the symbolic identity

```text
F_lambda = (32/625) lambda
```

against the interval Jet enclosure.  Implicit differentiation gives

```text
1/4000000 < dt/dlambda < 1/3000000
1/2250000 < db/dlambda < 1/2000000
```

for

```text
b(lambda) = acos(1/16384) - (36/25)*(pi-asin(t(lambda))).
```

Hence `b(lambda)` is strictly increasing and its image is a nondegenerate
positive-Borel interval.  A certified exact lower bound for its length is

```text
1/15083783921185421737020778122981576893414286548166442549939006624186984533832740348902108585437766356151285840459796807210473118163439891189737855131844608000000
```

The family ID is built only from the frozen sheet, parent, operator cell,
angular lift, fixed `c0`, and exact rational collar endpoints.  Arb or decimal
text does not enter stable IDs.

## Uniform recut geometry

For every exact `lambda` fibre, the source adapted coordinate is

```text
u0(lambda,x) = 10^-90*x,  0 <= x < 1.
```

The verifier independently replays the two moving adapted coordinates and
checks the uniform length and derivative ranges:

```text
34/5 < U1(lambda,1)/delta < 7
87/5 < U2(lambda,1)/delta < 18
6    < U1_x/delta         < 7
17   < U2_x/delta         < 18
```

All 23 frozen dyadic guards remain strict root-face guards on the full
lambda collar.  Their order is

```text
S2:1,S2:2,S1:1,S2:3,S2:4,S2:5,S1:2,S2:6,S2:7,S1:3,
S2:8,S2:9,S2:10,S1:4,S2:11,S2:12,S1:5,S2:13,S2:14,
S2:15,S1:6,S2:16,S2:17
```

The two source endpoints and these 23 graphs produce 24 strictly positive
common ranks.  The independently replayed minimum guarded gap is greater
than `1/200`.  The official three-leg path, owners, charts, words, roof
counts, recut references, and right-cell ownership conventions remain
unchanged.

## Independent lambda and physical parameters

Two parameters are deliberately kept distinct:

```text
lambda = b3   indexes exact parent-W Borel fibres
s             horizontally translates every W-obstacle centre
```

The joint scope is one exact lambda fibre times the independent closed collar
`|s| <= 2^-512`.  No identifier substitutes one parameter for the other.

The verifier feeds the full lambda `t`-guard into the separately frozen
Round122 native Jet2 replay and then checks the complete `lambda × s`
physical audit.  Per common rank the candidate census is

```text
stage 0   57
stage 1   55
stage 2   57
total    169
```

Across 24 ranks, the typed occurrence counts are:

```text
candidate tangency        4056
root signs                 384
owner gaps                 144
C24 core faces            1152
integer corner rays       2040
coordinate velocities      144
six chart/wall/homogeneity classes, each 72
```

Every one of the twelve strict predicates clears its frozen rational margin.
The tight diagnostics include candidate tangency above `10^-12` and source
homogeneity above `10^-14`.  The resulting complete five-face/seven-boundary
physical family is empty:

```text
physical five-face incidences   0
residual physical faces         0
```

The empty physical statement does not erase the 25 artificial recut faces,
48 artificial traces, or 24 two-sided child/face incidences.

## Parameterized field registry

The finite rows are templates, not a finite enumeration of an uncountable
family:

```text
stage recut templates                    26
common-rank templates                    24
base-key templates                      120
certified fields per base                14
field-slot templates                   1680
```

For every exact lambda locator, the constructors materialize:

```text
actual parent-W cells                      1
actual common children                    24
actual base keys                         120
actual F1-F13/F16 slots                 1680
```

The verifier reconstructs every template ID and crosslink from the pinned
Round121/Round122 registries.  It enforces exact-once coverage of

```text
F1,F2,...,F13,F16
```

on each of the 120 base templates.  F5 and F6 retain their fixed three-leg
scope.  F11 uses the authoritative full-phase values

```text
stage 0   150*2^15 = 4915200
stage 1   150*2^14 = 2457600
stage 2   150*2^14 = 2457600
```

and never substitutes the `<7,<3,<12` along-curve diagnostics.

## Independent verifier and assault

The verifier does not import or execute the Round129 producer.  It combines:

- a fresh lambda-root and monotone-`b` interval replay;
- the byte-pinned independent Round122 Jet2 mathematical layer;
- an independent rebuild of all stable IDs, row closures, aggregate
  closures, and 23/26/24/120/1680 registries;
- 77 fully re-signed semantic mutations;
- 16 byte-level strict-JSON attacks;
- resolved-path and inode protection for all inputs, sources, pins, and
  outputs.

```text
producer SHA256
  bb0884aa14c256d16acd86c47ef1bf75e910507fa0b9334be704a6ee3995a054
certificate SHA256
  1e2527ddb73158554ad238ff2f9f7fd6cb805f80d55bdafd770a8c9c1688d762
certificate result SHA256
  79cb3501fd7d52d1a22fecf3dc0faaa979dfd9b06fea7ce7afd872b39fbf2bd5
verifier SHA256
  64c20bae8ea2944cb8487b253f9e0ff0a1a68a0c11fe0cd8d6d2206427981ea7
verification SHA256
  4d22ba14e44fe05bf564914d05b335a831f375560e6fbd6b31831f52eb6351db
verification result SHA256
  680c9cadb5612c28a157124bed9e8154dc112b4ead7d9ef46871b1c7b28f8905
```

Both verifier hash seeds produced byte-identical artifacts.  Missing,
tampered, symlinked, hardlinked, and FIFO certificate inputs fail with
nonzero status and create no output.  Symlink, hardlink, and FIFO output
targets are also rejected.

## Frozen safety boundary

```text
positive-Borel local maturity       14/18
F14/F15/F17/F18 on this family      absent
global complete 18-field blocks          0
Gate5 blocks                             0
global Gate5 maturity                10/18
Gate5 status                 NOT_CERTIFIED
CM2                         NO-GO_FOR_CLAIM
```

Round129 does not certify the global 441280-word universe, arbitrary return
depth, nonempty physical F10/F13/F16, F14/F15/F17/F18 on the positive-Borel
family, a global same-root 18-field block, Wiener invertibility, Kac closure,
Gate5, or CM2.

The separately audited `2^-17` collar is only a future widening candidate.
Its physical predicates can be covered after subdivision, but its 23 recut
graphs still require a correlation-safe normalized/integral formulation.
It is not part of the frozen Round129 claim.
