# CM2 Round145 finite connected leaf-corridor atlas

Date: 2026-07-24

## Result

Round145 certifies the complete fixed-`s=0`, slope-four R1648 physical leaf
branch between the collision-three D0 boundary and the terminal
`G:S, p=-1/50` boundary.

The certified scaled coordinate is

```text
lambda = (x_star - x) 2^4289.
```

The physical branch is the open interval
`0 < lambda < lambda_terminal`.  Its versioned local identifier is

```text
round145-v1-connected-physical-r1648-leaf:
a863f420f91c4975d892c454eb2ba7f62564186f44c93c7861fc7d894d4557c7
```

This is a complete one-dimensional physical branch for the frozen itinerary
and destination core.  It is not a proof of maximality of a
two-dimensional H1 component.

## Adaptive atlas

The atlas has 13 cells and 12 exact shared internal faces:

- eight `K4292` cells cover `lambda in [0,1]`;
- four `K4294` cells, indices 32 through 35, cover
  `lambda in [1,9/8]`;
- one clipped cell covers `[9/8, lambda_upper]`, where
  `lambda_upper` is the upper endpoint of the Round143 isolated root
  bracket.

The initially requested single `K4292` cell `[1,9/8]` failed closed only at
the terminal C24 interval classification: its enclosure straddled the
`p=-1/50` face.  `K4293` still failed at the same exact door.  `K4294`
was the first tested scale whose terminal tail cell gave a strict return, so
the tail was refined into four exact cells rather than weakening the
classifier.

Each regular cell independently passed all 1,648 collision stages:

- retained owner search and the complete radius-four universe;
- official wall endpoints and strict event ordering;
- outgoing chart;
- `H0_CENTRAL` homogeneity;
- incidence rank 14;
- 1,647 strict nonreturns and one strict terminal return.

The clipped closed cell passed the same owner, official-word, chart,
homogeneity and incidence audits.  Its first 1,647 stages are strict
nonreturns; at stage 1,648 the only unresolved boundary is the intended
terminal `p=-1/50` face.  Round143 supplies the unique root and strict
negative `dp_1648/dlambda`, selecting the returning open side.

Adjacent cells substitute the same exact lambda face and the same frozen
D0-root generator into the same analytic initial leaf map and the same
1,648 selected-circle composition.  Thus the atlas adjacency graph is a
connected path with no artificial gap or itinerary change.

## Image monotonicity

An interval-sensitivity replay on every atlas cell proves

```text
dp_1648/dlambda < 0
d[asin(t_1648)+asin(p_1648)]/dlambda < 0.
```

It also proves the terminal coordinates stay strictly inside both `asin`
domains.  Consequently the connected image has no internal extremum, and
the Round143 endpoint difference is the complete adapted image span rather
than merely a formal endpoint expression.

## Corrected versioned promotions

The newly certified branch promotes the Round143 prospective data within
the explicit corrected-v1 chain:

- canonical H1 `x=sqrt(17)r` Round137-v1 least basis level: `4290`;
- canonical rank decimal SHA256:
  `2650e59e81848f02e30fabbce2cad195e95c979c8bc695a7f577ae9c73ffb1c9`;
- normalized-`t` cross-check level: `4283`;
- normalized-`t` rank decimal SHA256:
  `da159470a46c7e5b75b099dda6c7aa939daee12b72fb47b471f08f8ea549eaa0`;
- corrected left-anchored natural source short-cell index: `k=0`;
- corrected source-cell ID:
  `round145-v1-source-short-cell:ef713d451631988da505537ae3fcd9e8d11ccf062efcf81cd86bec4404e53d29`;
- corrected image-recut count:
  `18482025737079285768196755871683993421335748959797565447882270854942728583699291803410531`;
- image-recut count decimal SHA256:
  `866cc155fbf90260eefa345d454f554ef920d297b9d58a2e6e283139907350ae`;
- corrected image ranks:
  `0` through
  `18482025737079285768196755871683993421335748959797565447882270854942728583699291803410530`;
- corrected image registry:
  `round145-v1-image-recut-registry:ad828d2da71cf42c1b5fcee3245fcde0c40244f6436b505c19617f6c00be55db`.

These are corrected, coordinate-explicit versioned objects.  They are not
the unnamed historical Round27/Round35 enumeration or restriction IDs.

## Counts

```text
atlas cells                              13
exact shared internal faces              12
cell/collision stages                 21,424
radius-four candidate tests        3,449,264
preterminal nonreturn cell/stages     21,411
coordinate-explicit v1 leaf ranks          2
corrected v1 source short cells            1
corrected v1 image registries               1
historical identifiers                      0
complete Gate5 18-field blocks              0
```

## Cross-precision identity contract

The 8,192-bit primary and 12,288-bit secondary replays deliberately retain
their generation-precision-specific model-radius ledger hashes.  Those
evidence hashes are excluded from the versioned branch identity.  The
identity instead hashes the exact cell specifications, shared faces, frozen
paths and derivative signs.  The independent verifier requires every other
topological, path, radius, margin, derivative, endpoint, rank and promoted-ID
field to be byte-exact across the two precisions.

## Frozen core hashes

```text
Round145 engine       c2bf266f715a8214a13f87308dd9c982e520b39a2747e23fedc1c7955fd62c78
Round145 producer     6deed0506b0105eee9ee9a89dd4c28ee9bed81aa4922586eb8b8005a433ba4c7
Round145 certificate  5edac93e1425c72992ab671f3b3f7db269d236819ea3ad689b612505426ccec6
certificate result    16cec30f7af9d3f0d278d0bae85f8dca4a9a3041186021fc7ebd1b9c43a7fc0b
```

The verifier, verification, replay, assault and manifest hashes are recorded
in the final SHA256 manifest.

## Global nonpromotion

All historical Round27/Round35 component, interval, parent-W, short-cell,
image-recut and restriction identifiers remain null.  No Round50 owner,
Round54 token or Round67 `q_j` is emitted.

```text
Gate5 maturity                  10/18
complete 18-field blocks             0
Gate5                    NOT_CERTIFIED
CM2                 NO-GO_FOR_CLAIM
```
