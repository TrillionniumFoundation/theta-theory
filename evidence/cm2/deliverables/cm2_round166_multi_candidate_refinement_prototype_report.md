# CM2 Round166 prototype — outside-`W:W` multi-candidate refinement

Date: 2026-07-26

## Decision

This prototype finds a scalable exact route through the 38,180
outside-`W:W` `multi_candidate` leaves, and profiles six additional dyadic
levels.  It is nonpromotional: no Round162--164 artifact is changed, no
integer leaf census is decremented, and D02 remains blocked.

Its machine status is

```text
NONPROMOTIONAL_PROTOTYPE__VALID_ROUND163_AMBIENT_BASELINE.
```

The principal result is that 35,564 of the 38,180 pinned multi leaves
(93.1482%) already carry an exact frozen-prefix impossibility witness in the
pinned depth-8 active registry.  Only 2,616 leaves require any subdivision.
After refinement from absolute depth 8 to 14, exact full-dimensional
dispositions cover

```text
596685/16 = 37,292.8125 baseline-leaf-equivalent volume
119337/122176 = 97.676303% of the 38,180-leaf multi atlas volume.
```

The remaining collar volume is

```text
14195/16 = 887.1875 baseline-leaf equivalents
2839/122176 = 2.323697%.
```

This is a volume/profile statement on a dyadic refinement, not a new integer
recordwise exclusion count.

## Strict baseline and the Round164 correction

The valid recordwise frozen-prefix baseline remains the Round163 census:

```text
source-W chart-leaf records                  76,828
recordwise exclusions                        37,480
remaining                                    39,348
outside-W:W multi-candidate leaves            38,180.
```

Round164 types 12 owner-mismatch tangency graphs, but each such graph is
codimension one inside a full-dimensional leaf.  It does not remove the
off-graph bulk of that leaf.  Therefore those 12 rows must not be subtracted
from the integer leaf census.  This prototype treats every newly found
`tangency_graph` in the same way: it records a stratum witness and continues
subdividing both off-graph sides.

This interpretation is now bound to the formal Round164 v2 chain:

```text
certificate file SHA256
2f1fcb72224f39c8d4a9d9f666a8579f71d77542e31552aa7c9dbc4b7338f092

certificate result_sha256
0f6d7f47ac20734ed294dd04cd7720ccbb9c0a1d4236980f814dd2ea2d5e79d9

verification file SHA256
850bd24ae60979aaaea3f6819dcab665a1f7228d0c104014bfe8cce9e91299b0

verification result_sha256
bb2e51bdbbd457a5782038efc527000cbf89b73c8645fd6facd126fa453af8c4.
```

The Round166 producer checks ambient dimension 3, typed graph dimension 2,
32 ambient parents, zero full-dimensional exclusions, all off-graph bulk
unresolved, and the unchanged `37,480 / 39,348` ambient census before doing
any multi-leaf profiling.

## Audit of the pinned interval/BnB implementation

The upstream root enclosures and active-target pruning are sound.  The
`tangency_graph` label must be read only as a typed stratum witness, not as a
full-box volumetric disposition.  Apart from that semantic distinction, the
replay has three avoidable hot spots.

1. `base.candidate_ids(chart_id)` reclassifies all 162 target lifts for every
   box, even though the retained list is chart-constant.
2. `atlas.records(chart_id, box)` calls `atlas.root_record` once per retained
   target, and every call recomputes the same phase geometry.
3. `base.target_by_id` linearly scans the 162-target registry for every root
   record.

The prototype caches and digest-checks each 55-target source-W candidate
list, uses an O(1) target map, and evaluates `(q,u,s)` once per box.  It
reproduces the exact pinned leaf-row digests

```text
W:E  248c0b77c22594ceb69f475978bcc9d7867530fcfaeefe1518e3538938c268e2
W:N  728dbce4e414bc859d050b3fa5619febcddd277d3354b2af6c32f3414212ea82
W:S  e3fbab0ef15d6b9fd06e1b78da40050eb29b8bb724ceb4ad5408926f7eeaa373.
```

The pinned active-set rule is also safely inheritable.  If target `T` is
removed on a parent box, the parent contains a strict root `U` satisfying

```text
upper(tau_U) < lower_possible(tau_T)
```

throughout that entire box.  The same inequality holds on every child.
Following the finite strict-domination chain ends in the retained parent
active set.  Hence an exact first target among inherited active targets is
also exact among all 55 pinned candidates.

## Depth-8 census before subdivision

All 38,180 multi leaves lie at the pinned maximum depth 8.  Their active-set
sizes are already small:

```text
active size       2      3      4      5      6      7      8      9     10     11     12     13
leaf count    29,048  6,350  1,376    446    376    256    112     28     26     58     84     20
```

Testing only whether the frozen owner `W[1,0]` remains active gives

```text
chart   multi input   owner absent   owner active
W:E          12,388         11,260          1,128
W:N          12,896         12,152            744
W:S          12,896         12,152            744
total        38,180         35,564          2,616.
```

The 35,564 exact whole-parent prefix exclusions split as

```text
frozen-owner discriminant strictly negative        34,310
frozen-owner intersection strictly behind           1,178
strict earlier-root domination witness                  76
  dominator G[1,0]                                      38
  dominator G[1,1]                                      38.
```

These are exact frozen-prefix impossibility witnesses.  They do not
mislabel a leaf as `unique_first` when the identity of the globally first
non-frozen target is still unnecessary for pruning.

## Depth profile

The prototype applies the pinned stable longest-width split rule to only the
2,616 owner-active parents.  Since every pinned multi parent has the same
depth and volume, `parent equivalent` is also an exact fraction of multi
atlas volume.

```text
absolute depth   unresolved subboxes   unresolved parent equivalents   terminal parent equivalents
8                       2,616                     2,616                       0
9                       4,400                     2,200                     416
10                      7,092                     1,773                     843
11                     11,834                    5,917/4                 4,547/4
12                     22,538                   11,269/8                 9,659/8
13                     34,204                    8,551/8                12,377/8
14                     56,780                   14,195/16               27,661/16.
```

The exact depth-14 full-dimensional terminal volume is

```text
unique-first owner mismatch             12649/16 = 790.5625
frozen owner, outgoing-chart mismatch   11437/32 = 357.40625
frozen owner and W-chart match          18587/32 = 580.84375
total                                   27661/16 = 1,728.8125.
```

Together with the 35,564 immediate whole-parent exclusions, this gives the
97.676303% classified-volume figure above.

## What remains at depth 14

The 56,780 unresolved depth-14 subboxes occupy only 14,195/16 parent
equivalents.  Counts and corresponding parent-equivalent volumes are

```text
failure type                                  subboxes   parent equivalents   share of unresolved
untyped discriminant collar                     46,418       23,209/32             81.7506%
outgoing dominant-chart seam overwrap            7,510        3,755/32             13.2265%
source-grazing endpoint collar                   1,632             51/2              2.8743%
typed owner-mismatch tangency graph collar       1,140           285/16              2.0077%
typed frozen-owner tangency graph collar            80              5/4              0.1409%.
```

No strict-root-order-overlap failure survives as a separate type.  This is
not accidental.  Distinct target disks are exactly disjoint:

```text
G--G minimum centre distance squared       1 > (18/25)^2
W--W minimum centre distance squared       1 >  (8/25)^2
G--W minimum centre distance squared   79601/160000
cross-radius-sum squared                43264/160000
strict squared gap                      36337/160000 > 0.
```

For the cross case, the closest possible coordinates are
`(1/2-1/400,1/2)=(199/400,1/2)`.  Equal positive collision times for two
distinct targets would put one point on both disjoint target boundaries,
which is impossible.  Thus owner-switch boundaries can only be mediated by
a tangency/absence transition or a typed domain boundary, not by an
untyped equal-root sheet.

## Scalable exact completion algorithm

Increasing a rectangular-box maximum depth alone cannot yield a
zero-unresolved census: every smooth tangency or chart-seam graph leaves a
shrinking but nonzero collar of axis-aligned boxes.  Completion requires
graph cells, not merely deeper boxes.

The recommended exact router is:

1. Replay each pinned depth-8 multi leaf and export one of:

   - frozen owner has `Delta<0`;
   - frozen owner has `tau_far<0`;
   - a named strict competitor satisfies
     `upper(tau_competitor)<lower_possible(tau_owner)`;
   - frozen owner remains in the inherited active set.

2. On owner-active children, evaluate geometry once and only inherited
   targets.  A uniform `unique_first` result is exact over the full pinned
   registry by the parent-domination argument.

3. For an unresolved target discriminant

   ```text
   Delta_T = R_T^2 - transverse_T^2,
   partial_p Delta_T = 2 transverse_T ell_T / sqrt(1-p^2),
   ```

   use a parametric interval-Newton step in `p`.  When the derivative has a
   strict sign and the Newton image is contained in the `p` interval, export
   the unique graph `p=g_T(t,s)`.  Use rational dyadic face tests to peel the
   two off-graph bulk slabs and recurse only on the graph range.  If Newton
   containment fails because the graph enters through a `t` or `s` face,
   split the base direction with the largest interval contribution rather
   than blindly bisecting the widest raw coordinate.

4. A certified tangency graph is a stratum row, never a whole-box
   disposition.  Keep the input inherited active set while classifying its
   off-graph sides; the tangency target can be absent on one side.

5. Once `W[1,0]` is uniformly unique first, route the two independent
   outgoing-chart equations

   ```text
   H_- = n_x-n_y,       H_+ = n_x+n_y.
   ```

   The opposite chart margins are duplicates of these two equations.
   A unit contact normal prevents `H_-=H_+=0`, so there are seams but no
   physical chart corner.  Apply the same interval-Newton/graph-cell split
   and classify the off-seam bulk as W-match or chart mismatch.

6. Route `p=+/-1` as typed source-grazing boundary strata.  For adjacent
   bulk, use the Round162 rational compact coordinate
   `p=2q/(1+q^2)` and
   `sqrt(1-p^2)=(1-q^2)/(1+q^2)`.  This removes the square-root derivative
   singularity from the endpoint boxes.

On the complement of these finitely many typed graphs and boundaries, every
relevant discriminant, root-order and chart margin is continuous and
nonzero.  Compactness then supplies a positive local margin, so interval BnB
terminates.  The graph rows themselves supply the exact zero set rather than
leaving an infinite sequence of rectangular collars.

## Measured cost

On the loaded host, with concurrent work present:

```text
fast pinned W:E/W:N replay                       90.468 s
targeted depth-8 through depth-14 refinement     90.034 s
total                                           180.503 s
refinement boxes evaluated                      167,984
target root records evaluated                   415,570
average inherited targets per evaluated box       2.474.
```

Evaluating all 55 candidates on every refinement box would require
9,239,120 root records, 22.23 times as many, before accounting for the much
larger savings from one geometry evaluation per box and chart-constant
candidate caching.

## Artifacts and strict state

The producer, statistics, limited independent verifier, and verification
result are

```text
cm2_round166_multi_candidate_refinement_prototype.py
cm2_round166_multi_candidate_refinement_prototype_stats.json
cm2_round166_multi_candidate_refinement_prototype_verifier.py
cm2_round166_multi_candidate_refinement_prototype_verification.json.
```

The final producer file and statistics file are bound by

```text
producer file SHA256
6479a78249a717169dea55ecabae98c05f240ea323fa0370037d43339158ae7c

statistics file SHA256
ffa028ff9e46219a48b3950a49a7c8f8d111fb54e7c3322aa4387366a2870999

statistics result_sha256
6972926f909815e041842fe5582f89898d1589ab69b54a801f5e28fdfa19e548.
```

The verifier does not import the producer.  It independently rebuilds the
three pinned source-W leaf-row digests, all 35,564 immediate witness
classifications, the `2,616` owner-active remainder, the two 38/38
dominator counts, the Round164 v2 dimension chain, and all seven dyadic
accounting identities.  It passes with

```text
verifier source file SHA256
b069bc640d6bcf7d6eb16570d5844ce88504e00abc587cee958b59a775c68cdf

verification file SHA256
66f61b657eb72a0db90291d390d1021859c65ab059fdeaedabee95170102d1af

verification result_sha256
bf88161e1310db2dc3531e300b0a20af9b7f1c008c0909824b8bfcf64b14097f

semantic attacks rejected      12/12
strict JSON attacks rejected     8/8.
```

Wall-clock runtime is excluded completely from the signed verification
result and is emitted only on stdout.  Full verifier replays under
`PYTHONHASHSEED=1901` and `PYTHONHASHSEED=3907` produced byte-identical
verification files, both with file SHA256
`66f61b657eb72a0db90291d390d1021859c65ab059fdeaedabee95170102d1af`.

The verifier intentionally does not independently replay all 167,984
six-level refinement boxes.  Therefore this remains a verified prototype
baseline and conservation profile, not a sealed/promotable exterior atlas.
No Round162--164 artifact was modified by this Round166 work.

```text
recordwise exclusions                  37,480
recordwise remaining                   39,348
D02                                    BLOCKED
D03 negative oracle                    UNAUTHORIZED
CM2                                    NO-GO_FOR_CLAIM.
```
