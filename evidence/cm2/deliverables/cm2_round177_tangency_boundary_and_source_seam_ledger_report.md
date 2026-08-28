# CM2 Round177 — tangency boundary and source-seam ledger

Date: 2026-07-26

## Decision

Round177 resolves the boundary-clipping geometry left nominal in Round175,
but it does not issue a new whole-parent exclusion:

```text
Round175 mixed tangency parents                 16
Round177 fully excluded parents                  0
Round177 fully live parents                      0
Round177 mixed bounded residual parents         16
new whole-parent integer credit                  0
```

Every parent still has an independently replayed strict collision-1 live
open witness and a strict mismatch open witness.  This makes whole-parent
exclusion impossible even though some internal open strata are mismatches.
No 3D sub-stratum, 2D graph, 1D intersection, or chart guard slice is
converted into one parent-record credit.

## Exact H clipping census

The fourteen frozen-owner parents each have one, and only one, outgoing-H
clipping line.  After cancelling the common source-centre shift, `H` is
independent of `s`.  On the relevant `p` face its derivative with respect to
`t` is strictly negative on the whole parent.  Rational bisection therefore
isolates a unique root:

```text
H(t_*,p_face)=0
p=p_face
s in [-1/400,1/400]
dimension                                          1
transversality                    strict dH/dt < 0
integer credit                                      0
```

The seven negative roots have exact reflected positive partners.  Their
approximate magnitudes are:

```text
0.24503556076922073
0.33157629989443166
0.5887475068627966
0.6253813826946107
0.6637111157410273
0.6836513941831841
0.7042124653623363
```

The two mismatch-target exceptions
`W:N:05.00.00100110` and `W:S:H.05.00.00100110` have full-base H graphs and
no `p`-face clipping.  The Round175 strict graph order is preserved.  Thus
all sixteen Delta-H intersections remain empty.

## True physical source-chart partition

The rational atlas guard `[-177/250,177/250]` is not the physical chart.
The physical E-chart partition is:

```text
1-2*t^2 > 0        3D E-chart interior
1-2*t^2 = 0        2D diagonal source seam
1-2*t^2 < 0        3D adjacent-chart recoordination region
```

Exactly two parents cross the algebraic seam:

```text
W:E:00.15.0000000       selected seam -1/sqrt(2), adjacent chart W:S
W:E:07.00.1111111       selected seam +1/sqrt(2), adjacent chart W:N
```

The E/W half-open rule owns both diagonal seams; N/S does not.  The
positive-volume guard-outside parts are chart-domain rejections that require
the exact recoordination

```text
t_adjacent=sqrt(1-t_E^2), p_adjacent=p_E, s_adjacent=s_E.
```

They are not exterior exclusions and receive zero credit.

For both cross-seam parents the H clipping root is
`t_*≈±0.7042124653623363`, while the physical seam is
`t=±1/sqrt(2)≈±0.7071067811865475`.  Their rational isolating brackets are
strictly disjoint.  Hence no unresolved clipping/source-seam double point
remains.

On each physical source seam:

```text
open 2D sign regions cut by Delta and H              3
source seam intersect Delta, dimension 1             1
source seam intersect H, dimension 1                 1
source seam intersect Delta intersect H              0
```

The H intersection is half-open owned by W.  Both one-dimensional rows
receive zero integer credit.

## Dimension-safe stratum ledger

Each non-crossing parent has three connected 3D analytic sign strata.  Each
crossing parent has the same three sign patterns on both chart-domain sides,
giving six.  The exact bounded totals are:

```text
connected open 3D sign strata                       54
Delta=0 two-dimensional pieces after source cuts    18
H=0 two-dimensional pieces after source cuts        18
H parent-face clipping lines                         14
source-seam/Delta one-dimensional intersections       2
source-seam/H one-dimensional intersections           2
Delta/H one-dimensional intersections                 0
source-seam/Delta/H points                             0
```

Every Delta and H graph has four explicitly typed one-dimensional parent-face
edges.  Boundary edges, corners, analytic seams, and mismatch pieces all
remain non-credit strata.

## Later frozen-prefix processing

Later return processing is allowed only on the one strict collision-1 live
open component in each parent.  Collision 1 is independently replayed as
owner `W[1,0]` with outgoing chart `W`.

No collision-2-or-later exact-key row is promoted in this round.  A pinned
global return-coordinate/exact-key bridge for these sixteen semi-algebraic
live strata is not yet available.  The exact bounded residual is therefore:

```text
strict collision-1 live open components             16
later exact-key rows materialized                     0
later-prefix whole-parent exclusions                  0
```

## Composition

This branch is composed against its pinned Round175 dependency:

```text
refined source-W total                           76,832
whole-record exclusions                         73,178
conservative live                                3,654
conservation                         73,178+3,654=76,832
```

The sixteen mixed tangency composites remain in the conservative-live term.
Any independently developed multi-parent promotion must be merged only after
its own verification; it is outside the Round175-to-Round177 dependency
chain.

## Independent verification

The verifier imports or executes neither the Round177 producer nor the
Round175 producer.  It independently:

- decodes all sixteen dyadic parents from the pinned Gate3 atlas;
- replays all sixteen strict collision-1 live witnesses;
- re-isolates fourteen H-clipping roots and proves strict `dH/dt<0`;
- re-isolates both roots of `2*t^2=1` used here;
- re-isolates the four source-seam graph intersections;
- recomputes every row digest and exact-key digest.

Fail-closed suites:

```text
re-signed semantic mutations rejected            57/57
strict JSON attacks rejected                        9/9
path-safety attacks rejected                        7/7
```

Cold producer and verifier replays under `PYTHONHASHSEED=1` and
`PYTHONHASHSEED=987654321` are byte-identical.

## Strict state

```text
D02                                      BLOCKED
D03 negative oracle                     UNAUTHORIZED
global Gate5                            10/18
global complete 18-field blocks             0
CM2                                      NO-GO_FOR_CLAIM
```

The next tangency gate is a global later-return coordinate/exact-key bridge
for the sixteen strict live strata plus exact adjacent-chart processing of
the two positive-volume guard slices.
