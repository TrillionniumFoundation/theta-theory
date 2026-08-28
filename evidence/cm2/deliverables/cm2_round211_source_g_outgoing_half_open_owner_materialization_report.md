# CM2 Round211 — formal source-G outgoing-W half-open owner materialization

Date: 2026-07-27

## Verdict

`PASS_PARTIAL_FORMAL_ROUND211`.

Round211 upgrades the valid part of the Round209 feasibility result into a
formal, independently verified local dimensional-owner ledger:

```text
17,716  2D factor-sheet owner rows
20,456  1D clipping-incidence owner rows
40,912  0D endpoint-incidence owner rows
79,084  total formal local dimensional-owner credits.
```

Every nonempty source-G outgoing-W leaf now has exactly one factor-derived
half-open `E/W` owner.  Every carried curve and endpoint incidence joins that
owner lineage with closed row and parent hashes.

This is not a global-component theorem.  Separate incidences have not been
deduplicated into physical components.  Whole-leaf, whole-origin, whole-tube,
global-component, and global exact-key disposition credits remain zero.

## Why Round209 had real but bounded upgrade credit

The Round209 probe was not merely a numerical count.  On each of the `17,716`
nonempty leaves it checked:

1. the Round173 frozen rule `E or W owns; N or S excludes`;
2. the exact factorization
   `F=(Nx+Ny)(Nx-Ny)=HPLUS*HMINUS`;
3. a whole-box strict sign for the inactive factor;
4. the resulting unique `E/W` owner and `N/S` shadow;
5. the exact strict sign pair of both open regions; and
6. equality of the paired return signatures after removing only
   `outgoing_cell` and `target_chart`.

All `17,716/17,716` pairs passed.  The inactive-factor proofs are all direct
whole-box C0 proofs.  The owner/shadow census is:

| owner | shadow | sheets |
|---|---|---:|
| E | N | 4,429 |
| E | S | 4,429 |
| W | N | 4,429 |
| W | S | 4,429 |

Thus Round209 supplied genuine local dimensional ownership data suitable for
formal attachment.  It did not identify equal incidences across leaves or
prove a complete exact-key fibre, so those stronger credits were not
upgradable.

## Frozen trust boundary

The Round211 producer pins:

| artifact | SHA256 |
|---|---|
| Round209 probe | `dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f` |
| Round209 report | `7501e73fdad0c3721ed70b73226a4c3a4f7288f9b8429a553a50dde725812524` |
| Round208 producer | `c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913` |
| Round208 certificate | `4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938` |
| Round208 result | `d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8` |

It deliberately does not depend on the Round208 verifier, verification file,
report, cold replay, or manifest while those artifacts are being finalized
elsewhere.

The Round209 probe is used only as a pinned producer-side evaluator.  The
Round211 verifier does not import or execute Round209 or the Round211
producer.  It independently loads the pinned Round173 and Round208
producer/certificate boundary, checks every carried row closure, strips the
Round208 formal wrapper fields, and exactly reconstructs the Round195
geometry digests before rebuilding the complete expected Round211 result.

## Formal dimensional census

The input cover is conserved exactly:

```text
18,324 leaves
   608 empty leaves
17,716 nonempty single-sheet leaves
36,040 strict open 3D regions = 608 + 2*17,716.
```

The formal lower-dimensional ledgers are:

| ledger | rows | rows SHA256 |
|---|---:|---|
| 2D sheet owner | 17,716 | `ed26068a92d4ed74f54cd724680da5bc9cafa811d553415380999ae69ea7fdeb` |
| 1D curve-incidence owner | 20,456 | `3d93dd7860c1025bb68acf3568a0b4b66e3106189776aae4bafa12d3902a8522` |
| 0D endpoint-incidence owner | 40,912 | `e5466d386b45ea8ab473a8483b5a90a244592491cdb9ecbcdf01b7a40c87d712` |

The endpoint identity is exact:

```text
40,912 = 2 * 20,456.
```

The sheet rows cover `8,264` origins, `8,264` occurrences, and `11,952`
retained children.  Four of the `8,268` Round208 origins contain only empty
leaves and therefore need no factor-sheet owner.  This difference does not
create whole-origin credit.

There are `24` distinct paired signature cores.  Owner cells are balanced at
`E=8,858`, `W=8,858`; shadows are balanced at `N=8,858`, `S=8,858`.

The clipping-incidence geometry is:

| boundary pair | incidences |
|---|---:|
| E\|N | 3,959 |
| E\|S | 3,959 |
| N\|S | 4,620 |
| N\|W | 3,959 |
| S\|W | 3,959 |

The two t-face sides each contribute `10,228` incidences.  Graph axes are
`p=20,200` and stereographic `u=256`.

## U\|U audit

All `88` U\|U sheets and `76` origins join a deterministic owner:

- owner cells: `E=44`, `W=44`;
- active factors: `HPLUS=44`, `HMINUS=44`;
- 1D incidences: `164`;
- 0D endpoint incidences: `328`;
- `76` two-curve sheets are strictly ordered and disjoint;
- `12` sheets have one curve and one strictly zero-absent t face; and
- curve-pair intersections: `0`.

No signature is copied across the outgoing seam.

## Independent verification and attacks

The verifier rebuilt the entire expected Python object before opening the
Round211 certificate, then required exact Python-object and canonical JSON
equality.  It never imported or executed the producer or Round209 probe.

Attack results:

| suite | rejected |
|---|---:|
| re-signed semantic mutations | 20/20 |
| strict JSON / encoding attacks | 9/9 |
| path / type / output attacks | 8/8 |

The semantic attacks explicitly include:

- changing a sheet or endpoint owner;
- setting local owner credit to zero or two;
- falsely merging an incidence into a global component;
- forging sheet/curve/endpoint lineage IDs or parent hashes;
- adding component, whole-leaf, whole-origin, whole-tube, or global
  disposition credit; and
- promoting Gate5 or CM2.

## Frozen package identities

| artifact | SHA256 |
|---|---|
| producer | `9e8874672150d7585316524a7724070f4543e231de5481d1c1dfbd00ddc65a02` |
| certificate | `bb03a39a74a237b9f4449214c698795856fce4d6be2195c4f9d7774cd1d4183f` |
| certificate result | `3b831c67669e52f1247ea30c0a1ed7d5c1002931a1c0f621dd934085e87c2d5b` |
| verifier | `df90f2dd869bef3b873fe800fe124a256e82ef7e772359fbea49a9b793725176` |
| verification | `1dee3afbe5cc04829ef5546ef16f8ef76b6d9a32f7bd1aab61037066419ad2f9` |
| verification result | `eed5687f736c6244421ec432a4d1fc283d84386147293825a19837173cbb819d` |

The certificate is `140,690,802` bytes.

## Reproducibility

Two producer seeds and two verifier seeds passed:

| run | seed | elapsed | maximum RSS |
|---|---:|---:|---:|
| producer official | 211051 | `1:08.01` | `748,700 KiB` |
| producer replay | 211052 | `1:01.55` | `749,088 KiB` |
| verifier official | 211061 | `1:42.77` | `1,022,724 KiB` |
| verifier replay | 211062 | `1:49.25` | `1,021,828 KiB` |

The two certificates are byte-identical, and the two verification files are
byte-identical.

## Round210 multi-candidate audit

Round210 is a separate source-G baseline refinement probe over the original
`45,028` Gate3 multi-candidate leaves.  Its finalized source SHA256 is

```text
accc57b7e3257b44e1d14051458b7aa40d0a03cc1fe8f234863b035ada195962.
```

A depth-one, 256-bit run exited zero.  Its output SHA256 is
`54a39abdbd2a56223aa57835f7a1766066ba1dec46ed45754d34b277e9e7384f`
and result SHA256 is
`3cb1a76fc196af044fceb7d72e41ddcdbeb3f1c61fc3793169d2529158ee0737`.
The run took `13:24.48` with maximum RSS `118,984 KiB`.

At depth one it found:

```text
17,776 unique-first child boxes = 8,888 parent-equivalents
72,280 residual child boxes     = 36,140 parent-equivalents
45,028 exact conserved parent-equivalents.
```

The residual split is:

- `69,908` discriminant/first-order unresolved children;
- `2,012` source-grazing-face children; and
- `360` typed tangency-graph collars whose off-graph bulk remains unresolved.

The probe does not track a complete dimensional replacement of any original
parent and explicitly issues zero whole-parent and global credit.  A deeper
rectangular split alone also cannot close smooth graph collars.  Round210 is
therefore a useful local dynamic-input tranche, but not a shorter formal
promotion route than Round211.

## Full Round182 local residual coverage audit

A fresh read-only set audit gives the following exact identities:

```text
Round208 outgoing-W origin IDs       8,268
Round204 wall-G origin IDs              64
intersection                            0
union                                8,332
Round182 not-fully-replaced origins  8,332
union equality                          true
parent union                          928
Round208 local key ordinals             24
Round204 local key ordinals             12
key-ordinal intersection                 0
local key-ordinal union                 36
local open 3D region occurrences    36,776 = 36,040 + 736.
```

The compact audit hashes are:

- origin-ID union:
  `5799c69f51d4dbdfd890fffc4b4fa260bc76f022ee37dc0c3bf036e477fc8156`;
- parent-ID union:
  `96aa885986f7ece9487d2ccd9b3ab291e663d11f93f2c08fa7f45ff1e243ba3d`;
- local key-ordinal union:
  `5ba4d5186ddb7ddb1868957f83af9d5224dbddaa619ecfedf1cdc51f7bc03763`.

This is a strong local coverage identity, not a whole-tube or global-fibre
identity.  It proves that the Round204 and Round208 local packages partition
the Round182 residual-origin registry; it does not prove that all occurrences
of any one immutable key across the global source-G domain have been joined
or exhausted.

## Strict residual and next gate

After Round211:

```text
local outgoing-W open-3D signature rows        formal
local outgoing-W 2D/1D/0D owner incidences     formal
local wall-G replacement and owner lineages     formal (Round204)
cross-incidence physical component dedup        not done
complete global occurrence join by exact key    not done
complete exact-key fibre exhaustion             0
source-G global dispositions                    0/224580
D02                                             BLOCKED
Gate5                                           10/18
complete global 18-field blocks                 0
CM2                                             NO-GO_FOR_CLAIM.
```

The next source-G core gate is exact physical-component join/deduplication
across the Round211 incidence rows, followed by a global occurrence census
for the `36` locally involved immutable ordinals.  A key may be promoted only
if every open-region occurrence and every owned lower-dimensional component
in its complete global fibre is present or rigorously excluded.
