# CM2 Round163 — frozen-prefix outgoing-chart pruning

Date: 2026-07-25

## Decision

Round163 resolves the strict outgoing dominant chart on every Round162
unique-first leaf whose first owner is the frozen owner `W[1,0]`.  It adds
40 exact earliest-prefix exclusions.  This is a recordwise pruning result
for one pinned prefix; it is not an exterior-sheet exhaustion theorem and
does not close D02.

## Pinned prefix

The Round139 frozen first-collision prefix requires

```text
owner             W[1,0]
outgoing chart    W.
```

Round162 left 1,176 unique-first leaves with the correct owner and an
unchecked outgoing chart.  Round163 replays the two direct 192-bit source-W
atlases, reconstructs the two exact reflections, and evaluates the physical
contact normal on each closed owner-matching leaf.

For contact normal `(n_x,n_y)`, the four strict dominant-chart tests are

```text
E: n_x-n_y>0 and  n_x+n_y>0
W: -n_x-n_y>0 and -n_x+n_y>0
N: n_y-n_x>0 and  n_y+n_x>0
S: -n_y-n_x>0 and -n_y+n_x>0.
```

A leaf is classified only when both inequalities for one chart are strictly
positive.  Any interval overwrap of a dominant-chart seam remains
unresolved.

## Census

```text
chart   owner-match input   chart mismatch   stage-one match   seam overwrap
W:E                   866               40               358             468
W:W                     0                0                 0               0
W:N                   155                0                80              75
W:S                   155                0                80              75
total                1,176               40               518             618
```

The 40 strictly classified non-W leaves are exact earliest-prefix
exclusions.  The 518 W-chart leaves match only the first frozen stage and
remain live for later return-prefix tests.  The 618 seam-overwrapped leaves
must be subdivided or entered into a typed dominant-chart seam graph.

Combining this block with the overlap-safe Round162 census gives

```text
source-W chart-leaf records                    76,828
prior recordwise frozen-prefix exclusions      37,440
new outgoing-chart mismatch exclusions             40
combined recordwise exclusions                 37,480
remaining                                      39,348
  stage-one owner/chart matches                    518
  outgoing-chart seam overwrap                     618
  tangency graph                                   32
  multi-candidate                              38,180.
```

These are conservative chart-leaf records.  Cross-chart guard-band overlap
is not quotiented, and a mismatch for this one prefix does not remove the
same physical region from other return-signature searches.

## Verification

The verifier does not import or execute the Round163 producer.  It
independently replays the pinned Gate3 atlas, reconstructs all 1,176 contact
normal tests and every disposition digest, and checks the overlap-safe
combined census.  It passes with

```text
semantic attacks rejected       12/12
strict JSON attacks rejected      7/7.
```

The first verifier run failed closed after numerical reconstruction because
the new strict JSON loader had not recursively rejected decoded NUL and
isolated-surrogate strings.  Both producer and verifier loaders were fixed;
the final verifier then passed.  No numerical count or certificate payload
changed during that correction.

## Strict state

```text
certified abs(delta_x)/h corridor       [0,2500000000000000]
globally first continuation face        NOT LOCATED
all exterior leaves/signatures resolved false
D02                                     BLOCKED
D03 negative oracle                     UNAUTHORIZED
Global Gate5                            10/18
global complete 18-field blocks         0
CM2                                     NO-GO_FOR_CLAIM
```

## Next core gate

1. Adaptively subdivide the 618 dominant-chart seam-overwrapped leaves and
   type any surviving seam graph.
2. Type the 32 outside-`W:W` first-tangency strata.
3. Subdivide the 38,180 outside-`W:W` multi-candidate leaves with exact
   earliest-prefix witnesses.
4. Extend the four-disposition census to source-G and every relevant return
   signature, including chart seams, grazing strata and corners.

Only a zero-unresolved fundamental-domain census can support reconsidering
D02.
