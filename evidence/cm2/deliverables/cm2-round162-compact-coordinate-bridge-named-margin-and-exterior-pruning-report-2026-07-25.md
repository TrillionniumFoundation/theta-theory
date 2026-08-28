# CM2 Round162 — compact-coordinate bridge, local named-margin baseline, and exterior-prefix pruning

Date: 2026-07-25

## Decision

Round162 certifies four nonpromotional blocks:

1. a four-chart rational half-angle compact source-coordinate
   infrastructure;
2. an exact compact-to-Gate3 source-W coordinate-cover bridge;
3. one full-R1648 local C24 named-margin checkpoint at the Round161 upper
   endpoint;
4. two recordwise pruning blocks, with their `W:W` record overlap removed,
   for the pinned Round139 first-collision frozen prefix.

These blocks remove important infrastructure and local-ledger gaps, but they
do not locate the globally first continuation face, exhaust the fundamental
angular exterior domain, close D02, authorize D03, or change Gate5.

## 1. Compact angular infrastructure

The physical source quotient is represented by four rational half-angle
charts

```text
z = tan((A-theta_C)/2) in [-kappa,kappa],
q = tan(Phi/2) in [-1,1],
kappa = sqrt(2)-1,
C in {E,N,W,S}.
```

The state map is rational:

```text
n      = ((1-z^2)e_C + 2z J e_C)/(1+z^2),
p      = 2q/(1+q^2),
radial = (1-q^2)/(1+q^2),
v      = radial n + p Jn.
```

All four cyclic source-chart seams are exactly glued in
`Q[kappa]/(kappa^2+2kappa-1)`.  Both `q=+/-1` strata are retained and typed
as physical source-grazing boundaries.  The infrastructure verifier passes,
rejecting 14/14 semantic attacks and 7/7 strict JSON/encoding attacks.

## 2. Exact compact-to-Gate3 source-W bridge

Round162 adds the missing certificate-level coordinate map from each compact
source-W chart to the corresponding pinned Gate3 chart:

```text
E: t =  2z/(1+z^2)
N: t = -2z/(1+z^2)
W: t = -2z/(1+z^2)
S: t =  2z/(1+z^2)
p  =  2q/(1+q^2)
s  =  s.
```

The normal, quarter-turn normal, radial factor and velocity agree exactly
with the Gate3 formulas.  The compact endpoints map to
`t=+/-1/sqrt(2)`, while

```text
(177/250)^2 - 1/2 = 79/62500 > 0.
```

Hence every true compact chart image lies strictly inside the rational Gate3
guard interval.  The identity

```text
8 kappa^2 - (1+kappa^2)^2 = 0
```

is reduced exactly in the basis `(1,kappa)`, and

```text
1-p(q)^2 = ((1-q^2)/(1+q^2))^2
```

proves state equality including the two grazing endpoints.

Consequently every compact source-W point, after adjoining the same
`s in [-1/400,1/400]`, has a covered image in the pinned Gate3 source-W
atlas.  Only the true dominant-coordinate subdomains are used for this
forward cover.  Reverse recharting of the rational Gate3 guard bands remains
deferred to the exterior face ledger; this block makes no physical-sheet
conclusion about those guard-band records.

This block is purely a coordinate-cover theorem.  It adds zero dynamical
leaf dispositions.  Its independent exact verifier passes, rejecting 24/24
semantic attacks and 7/7 strict JSON/encoding attacks.

## 3. Local full-R1648 named-margin checkpoint

At

```text
u in [2500000000000000,2500000000000001],
w in [-410,-408],
kind = C24_EVENT,
```

the 8,192-bit Arb producer replays all 1,648 collision stages and all
`161*1648 = 265,328` radius-four candidate tests.

It exports 24 unrelated non-event named margins, with 461,002 total
observations, covering exactly the required local families

```text
CANDIDATE_DISCRIMINANT
FLIGHT_ROOT
OWNER_ROOT_GAP
WALL
CHART
HOMOGENEITY
INCIDENCE
CORE.
```

Every exported non-event minimum is strictly positive.  The weakest depth is
4256, attained by the two collision-3 correlated-anchor miss ledgers.  The
intentional collision-1648 C24 graph zero is recorded separately, with a
strictly positive `partial F/partial w` enclosure and a parametric
interval-Newton root strictly inside the event box.

The separate fail-closed verifier re-runs the same pinned checkpoint engine
and passes, rejecting 14/14 semantic attacks and 7/7 strict JSON/encoding
attacks.  This is an independent process and document reconstruction, not an
independent numerical implementation; shared engine-logic risk remains.

Strict limitations:

- the box is a one-unit C24 interior checkpoint, not a continuation interval;
- bridge and D3 are not audited by this block;
- all 24 unrelated margins explicitly defer stagewise
  `(partial_u,partial_w)` export;
- event-graph transversality loss and Newton-box boundary contact are not yet
  promoted to continuously monitored first-face families;
- the computation still runs in `(u,w)`.  The new compact-to-Gate3 bridge
  does not retroactively turn this checkpoint into a `(C,z,q)` continuation.

Therefore this block does not identify the globally first R1648 face and
does not extend the certified corridor.

## 4. Exterior frozen-prefix pruning

The pinned Round139 first-collision prefix requires

```text
owner          W[1,0]
outgoing chart W.
```

The earlier exact target-registry block proves that `W[1,0]` is absent from
the complete conservative `W:W` candidate list because

```text
support_upper = -707/1000 < R_source-R_target = 0.
```

Thus all 18,930 `W:W` leaves are excluded for this one frozen prefix.

Round162 additionally replays the two direct 192-bit source-W Gate3 atlases,
reconstructs the two reflected atlases, checks every pinned leaf-row digest,
and assigns all 26,204 unique-first chart-leaf records by first-owner
mismatch:

```text
chart   unique   owner mismatch excluded   owner match unresolved
W:E      6,518             5,652                      866
W:W      6,518             6,518                        0
W:N      6,584             6,429                      155
W:S      6,584             6,429                      155
total   26,204            25,028                    1,176
```

The old `W:W` block already contains its 6,518 unique records.  After
removing that exact same-chart overlap, the new unique-owner block contributes
18,510 additional chart-leaf-record exclusions.  The recordwise combined
frozen-prefix census is therefore

```text
source-W leaves                         76,828
distinct frozen-prefix exclusions       37,440
remaining                               39,388
  unique owner match / chart unresolved  1,176
  tangency graph                            32
  multi-candidate                        38,180.
```

These are conservative chart-leaf records, not a quotient count of physically
disjoint parameter regions.  Cross-chart guard-band/seam overlap is not
removed here; its reverse-rechart ledger remains pending.

The first full replay intentionally failed closed because a prior prose-only
observation had claimed 25,008 mismatches.  The certificate does not retain
that stale number: the pinned leaf replay establishes 25,028, with the
difference localized to `W:E`.

This pruning is only for one frozen prefix.  It does not remove any of the
26,204 unique, 56 tangency, or 50,568 multi-candidate source-W leaves from
other return-signature searches.  The source-G atlas has another 66,420
leaves, and the full eight-chart Gate3 atlas remains

```text
143,248 = 47,436 unique + 216 tangency + 95,596 multi-candidate.
```

The unique-owner verifier does not import or execute the Round162 producer.
It separately replays the same pinned upstream 192-bit Gate3 atlas
implementation, rebuilds all 26,204 disposition rows and their digests, and
checks the same-chart-overlap-safe combined counts.  It rejects 18/18
semantic attacks and 7/7 strict JSON/encoding attacks.  This separate replay
does not isolate common errors in the pinned upstream Gate3 implementation.

## Reproducibility

The compact infrastructure, compact-to-Gate3 bridge, named checkpoint,
original `W:W` prefix block, and unique-owner block are all bound by the
Round162 manifest.

- The compact infrastructure producer/verifier replay byte-identically.
- The compact-to-Gate3 bridge producer/verifier replay byte-identically
  under different hash seeds.
- The named producer/verifier replay byte-identically under hash seeds
  1709 and 2903.
- The unique-owner producer/verifier replay byte-identically under different
  hash seeds.

The 8,192-bit named-margin signs come from Arb recomputation.  Coarser
serialized outers must not be used to infer signs independently.

## Strict state

```text
certified abs(delta_x)/h corridor       [0,2500000000000000]
typed atlas                             75 slabs / 225 boxes
interior untyped event cells            0
upper endpoint                          nonterminal
globally first continuation face        NOT LOCATED
all exterior leaves/signatures resolved false
D02                                     BLOCKED
D03 negative oracle                     UNAUTHORIZED
Global Gate5                            10/18
global complete 18-field blocks         0
CM2                                     NO-GO_FOR_CLAIM
```

## Next core gate

1. Bind the Round161 endpoint and the C24/bridge/D3 full typed chain directly
   into compact `(C,z,q)` charts.
2. Export stagewise parameter derivatives for every non-event margin and
   continuously monitor event-graph transversality and Newton containment.
3. Validate consecutive full-chain compact checkpoints until the first
   nonintentional named face is isolated and typed.
4. For the present frozen prefix, resolve outgoing chart on the 1,176
   owner-matching unique leaves, type the 32 outside-`W:W` tangency strata,
   and subdivide the 38,180 outside-`W:W` multi-candidate leaves.
5. Extend the four-disposition census to source-G and every relevant return
   signature, including seams, grazing and corners, with unresolved leaves
   equal to zero.

Only after both the connected continuation and the full exterior census
close may D02 be reconsidered.
