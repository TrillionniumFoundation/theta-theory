# CM2 Round197 — source-W generalized exact-behind reduction spike

Date: 2026-07-26  
Verdict: `VALIDATED`

## Question

How much of the outcome-blind Round184 tail can be closed by iteratively
removing every unresolved target that satisfies, on the complete closed cell,

```text
ell < 0
and distance^2 - R^2 = ell^2 - Delta > 0,
```

then independently rebuilding the remaining records, leaf, owner, outgoing
chart, and terminal disposition after each deletion?

The frozen scope is exactly:

- `596` `DELTA_H_OR_MULTI_NO_Q` origins; and
- `54` `COMPACT_Q_PRESENT` origins.

Compact-q/source-grazing origins, physical source seams, and every remaining
mixed cell retain their independent strata and receive no official credit.

## Frozen probe and command

The read-only probe
`cm2_round197_source_w_generalized_exact_behind_reduction_probe.py` is frozen
at SHA256

`7b22a5e46896fa448e6346a73b9e9153743047c30800d179b00bf4b58b15af12`.

It pins Round194 at

`d4eb7ba9f2932083da2266a0ae67df7b4b941625472849fb9a52cbdc8e7c371f`

before import, then rechecks the pinned Round176/180/184 chain.  The frozen
Round184 registry-row digest is

`d6d247658c26c685a6df4f385902122e212dfdf5ed74ca6058ca14510591712e`.

The full command was:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=197052 \
  /usr/bin/time -v \
  -o /tmp/cm2_round197_seed197052.time \
  .venv-neurips/bin/python \
  deliverables/cm2_round197_source_w_generalized_exact_behind_reduction_probe.py \
  > /tmp/cm2_round197_seed197052.json \
  2> /tmp/cm2_round197_seed197052.stderr
```

It exited `0` in `12:22.49`, used `140,052 KiB` maximum RSS, and consumed
`741.96` user CPU seconds.  The script has no output-path option and performs
no filesystem writes; the shell and `/usr/bin/time` own the `/tmp` captures.

The final JSON SHA256 is

`dde430b868dcee1ab29bb96925d81fa94f478edf0a5173327798197c96eb072a`.

Its canonical `probe_result` SHA256 is

`b8d7531890aa498890b4530335e26827b9354b0799c2f855b86ff170bb5902ab`.

## Frozen selection and exact reconstruction

Selection uses only the pre-existing Round184 priority class.  It does not
inspect any Round197 closure outcome.

| priority class | origins | origin-key SHA256 | cells | exact volume |
|---|---:|---|---:|---:|
| `DELTA_H_OR_MULTI_NO_Q` | 596 | `b6440ea91a3fd331cf55b1a5e7a530c3ca688d48a3e2ec0897f1981d05edbd1d` | 161,442 | `14287617/209715200000` |
| `COMPACT_Q_PRESENT` | 54 | `d5fd64dc6d287982b6bf6739295869a21991b758917754eea3aa55476e504e7b` | 21,334 | `1888059/209715200000` |
| total | 650 | `36c2f93e9252373ee95fd4574c84f8d8084b1d6cd2e4467ebb6e6670d48e7467` | 182,776 | `4043919/52428800000` |

Every selected registry row was reconstructed from the pinned Round180
depth-4 refinement.  For each origin, the probe checked:

- Round176 residual-root and preclosed counts;
- preclosed-kind support;
- Round180 final-cell count and key digest;
- exact final-cell volume;
- residual-category counts and support; and
- initial residual-category counts.

The input residual-category census is:

| original category | cells | exact volume |
|---|---:|---:|
| clipped/single discriminant graph | 74,968 | `1658667/52428800000` |
| full-p/first-root equality | 50,902 | `4504827/209715200000` |
| multi-discriminant, 2–5 targets | 50,808 | `1124127/52428800000` |
| source-grazing compact-q | 5,862 | `518787/209715200000` |
| typed tangency plus outgoing-seam double graph | 236 | `10443/104857600000` |

The original failure census is:

- `UNTYPED_DISCRIMINANT_COLLAR`: `176,678`;
- `SOURCE_GRAZING_ENDPOINT_COLLAR`: `5,862`;
- `TYPED_OWNER_MISMATCH_TANGENCY_GRAPH_COLLAR`: `236`.

The 650 origins consist of `642` strict physical-chart interiors and `8`
physical chart-seam/guard composites.

## Iterative exact-behind evidence

The `182,776` cells contain `255,936` original unresolved candidates.
Candidate cardinality per cell is:

| unresolved candidates | cells |
|---:|---:|
| 1 | 128,672 |
| 2 | 41,072 |
| 3 | 9,412 |
| 4 | 2,256 |
| 5 | 1,008 |
| 6 | 128 |
| 9 | 228 |

For every candidate, the preferred direct enclosure
`distance^2-R^2` is cross-checked for overlap with the independent
`ell^2-Delta` enclosure.  Eligible candidates are deleted in lexicographic
target-id order, one at a time, with a complete remaining-record rebuild
after each deletion.

The result is:

- exact-behind candidates deleted: `233,356/255,936` (`91.177482%`);
- candidates left: `22,580`;
- every failed candidate has the sole reason
  `ELL_NOT_STRICT_NEGATIVE`;
- distance-margin failures among the nondeleted candidates: `0`;
- maximum deletions from one cell: `6`.

The deletion-count distribution is:

| deleted candidates | cells |
|---:|---:|
| 0 | 12,424 |
| 1 | 122,284 |
| 2 | 36,684 |
| 3 | 9,096 |
| 4 | 1,152 |
| 5 | 1,008 |
| 6 | 128 |

After all eligible deletions, the remaining unresolved-candidate
distribution is:

| remaining unresolved candidates | cells |
|---:|---:|
| 0 | 162,512 |
| 1 | 18,860 |
| 2 | 1,176 |
| 6 | 228 |

The full ordered per-cell reduction-evidence digest is

`931fced14334273f90be4d92d719628906446c2f0c1c64a5681409111dbf214c`.

## Independently rebuilt dispositions

The final remaining-record leaf census is:

- `unique_first`: `162,512`;
- `multi_candidate`: `18,208`;
- `tangency_graph`: `2,056`.

The terminal dispositions are:

| final disposition | cells |
|---|---:|
| `EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH` | 142,986 |
| `EXCLUDED_OUTGOING_CHART_MISMATCH` | 18,662 |
| unresolved | 21,080 |
| `LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH` | 48 |

Thus candidate deletion geometrically excludes `161,648/182,776` cells
(`88.440495%`).  This consists of:

- `142,866` noncompact mixed cells, exact volume
  `12643641/209715200000`; and
- `18,782` cells inside compact-q-priority origins, exact volume
  `1662207/209715200000`.

The complete `COMPACT_Q_PRESENT` origin class is conservatively held as an
independent stratum, including its non-q child categories.  Consequently the
probe-admissible noncompact closure is only:

- closed cells: `142,866/182,776` (`78.164529%`);
- closed exact volume: `12643641/209715200000`;
- closed-cell key digest:
  `f5a856cf588948be372f1432368bd2aa14e2c30a6373dbf23c04d33182d7d89f`.

The exact residual partition is:

| residual reason | cells | exact volume |
|---|---:|---:|
| no exact-behind unresolved candidate | 10,564 | `467457/104857600000` |
| reduced remaining disposition unresolved | 7,964 | `352407/104857600000` |
| reduced remaining disposition live | 48 | `531/26214400000` |
| compact-q/source-grazing independent stratum | 21,334 | `1888059/209715200000` |
| total | 39,910 | `706407/41943040000` |

The residual-cell key digest is

`31b422463b4a4642cd7210309998709a7ca86f188033d7626c63c26c78bd9d95`.

The exact global identity is:

```text
142866 + 39910 = 182776

12643641/209715200000
+ 706407/41943040000
= 4043919/52428800000.
```

## Outcome by original residual category

| original category | probe closed | no deletion | reduced unresolved | reduced live | compact/source hold |
|---|---:|---:|---:|---:|---:|
| clipped/single graph | 63,436 | 9,328 | 546 | 0 | 1,658 |
| full-p/root equality | 42,252 | 0 | 222 | 0 | 8,428 |
| multi-discriminant | 37,178 | 1,176 | 7,196 | 48 | 5,210 |
| compact-q | 0 | 0 | 0 | 0 | 5,862 |
| typed double graph | 0 | 60 | 0 | 0 | 176 |

This is why the remaining hard mathematical tail is concentrated in cells
whose undeleted records still form a multi-candidate/tangency arrangement,
plus the independently held source-grazing stratum.

## Whole origins and source strata

Candidate deletion geometrically closes the complete residual support of
`424/650` selected origins:

- `396` noncompact origins have every cell probe-closed;
- of those, `390` are strict physical-chart interiors;
- the other `6` are physical source-seam composites and retain their
  half-open source partition;
- `28` compact-q-priority origins are geometrically complete but all `54`
  compact-q origins remain held as one independent origin class;
- `200` noncompact mixed origins remain incomplete.

Digests are:

- all 424 geometrically complete origins:
  `a48a936e09db3fccbf62bf4311428a59ea903b3207b2c890443dd9d6a4a5fcec`;
- 390 strict-interior noncompact complete origins:
  `10d69f94b08b35b199dbb5eeb4d4047b84d7b104b7df1123eb8938121b438080`;
- 6 source-seam complete-but-held origins:
  `fe8d0a7d4c04c66f47d011d54478d011849abd8a90152391a4bb269bf42bd812`;
- 54 compact-q held origins:
  `d5fd64dc6d287982b6bf6739295869a21991b758917754eea3aa55476e504e7b`;
- 200 other incomplete mixed origins:
  `5f2c635ea4f05d3ffca603031b06caffee9460271705787def0c499f286a72d1`.

No one of these probe counts is applied to the official ledger.

## The frozen 210-origin clipped plus full-p cohort

Exactly `210` outcome-blind origins have Round180 category support equal to
`{CLIPPED,FULL_P}` and no other category.  Their key digest is

`35041af235b0eb1e9793b636942446cb6dc6329c9193df1afbf0b4cbf33732b1`.

This cohort contains:

- input cells: `34,816`;
- input exact volume: `3009/204800000`;
- probe-closed cells: `33,916`;
- residual cells: `900`;
- completely closed origins: `194/210`;
- complete-origin conservative exact volume:
  `1471047/104857600000`.

All 194 complete origins are strict physical interiors.  The remaining 16
origins are residual.  This strongly validates the exact-behind rule across
the root-equality support, but it does not promote the 194 origins here.

## Independent checks

A separate strict-JSON checker using only the Python standard library and not
importing the Round197 probe passed:

- canonical result-digest reconstruction;
- all priority-class, category, failure, and source-domain count partitions;
- exact input-volume reconstruction by both priority class and category;
- original-candidate identity
  `255936 = 233356 deleted + 22580 remaining`;
- eligible/deleted candidate and per-target census equality;
- final leaf, owner, chart, and disposition count conservation;
- exact closed/residual cell and volume conservation;
- all emitted origin-list counts and digests;
- the 210-origin cohort count, key digest, and cell conservation; and
- every zero-promotion field.

The stderr stream contains only monotone progress through `650/650`; it has
no traceback, assertion failure, or warning.

## What worked

- One exact-behind rule generalized from the Round194 clipped/full-p tail to
  multiple simultaneous unresolved candidates.
- `233,356` candidates were removed using whole-cell strict inequalities.
- Every deletion was followed by an independent remaining-record rebuild.
- The rule geometrically excluded `161,648` cells.
- It completely closed `390` strict-interior noncompact origins and another
  `6` source-seam origins that remain separately held.
- The outcome-blind 210-origin clipped/full-p cohort closed 194 complete
  origins and 33,916 cells.

## What remains

- This is a read-only spike that imports prior probe implementations.  It is
  not a formal producer and is not an independent verifier.
- The 390 strict-interior origins require a formal producer that independently
  reconstructs every cell and emits complete per-cell/whole-origin ledgers.
- The 6 source-seam origins require a half-open source-domain partition.
- All 54 compact-q-priority origins remain in the source-grazing stratum.
- The 200 incomplete mixed origins retain `18,576` noncompact residual cells.
- The 48 reduced-live cells cannot be converted to exclusions.
- Complete lineage, semantic attacks, independent non-importing verification,
  cold replay, and a manifest do not yet exist.

## Recommendation

Formalize two disjoint strict-interior cohorts:

1. the 156 whole origins already closed by the Round194 rule; and
2. the 390 new strict-interior noncompact complete origins from Round197.

The formal producer must independently rebuild the pinned Round180/Round184
registry and exact-behind evidence.  It must prove the two origin sets are
disjoint, materialize per-cell and whole-origin ledgers, and keep all seams,
compact-q origins, reduced-live cells, and incomplete mixed origins residual.

Round197 issues strictly zero promotion:

- official-ledger mutations: `0`;
- whole-origin integer credits: `0`;
- Gate5: unchanged at `10/18`;
- complete 18-field blocks: unchanged at `0`;
- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- CM2: `NO-GO_FOR_CLAIM`.
