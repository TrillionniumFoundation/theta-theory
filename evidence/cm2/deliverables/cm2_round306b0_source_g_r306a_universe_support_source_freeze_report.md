# Round306B0 universe/support-source freeze — exact promotion report

Status:
`PASS_EXACT_ROUND306B0_UNIVERSE_SUPPORT_SOURCE_FREEZE`.

Round306B0 freezes the exact current Round306A member universe, component
census, support-source inventory, and unordered-pair denominator required by
the later Round306B maximality proof.  The independently verified formal
marker raises only `member_universe_freeze` and `pair_denominator_freeze` from
`0 / 0` to `1 / 1`.  It grants zero maximality, fibre, or global-disposition
credit.

## Frozen implementation and dependency pins

```text
producer_file_sha256=48f38e2b90aa2c1b934ba657f8c6e66a8cb97fa89f9439a0b11ed5fbb3d20d83
verifier_file_sha256=4d4fc9483b4ee65a55ccccf1ff30f4161c6f2fdd4853f64caef0291354cf1857
Round306A_manifest_sha256=35da99af5bb4c424284af2d7b396fc94b82dd6c6aa468c6a43a139107f9d9efc
Round306A_partition_sha256=a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c

result_file_sha256=badc000c6fadd8807b26a7c3511edc51796c962f150b438956e4c549fd0d5735
result_object_sha256=9ffe9144bc67f9bb7bb7e9c071b29a000f7d8e89396a3250b8207bfcc950d3d2
attack_file_sha256=d3d40aad0a6cd98d936524fb2f9c786adbdcede483de185121672a514ac87cfd
attack_object_sha256=742962bf7d84709e85c41d8e45b8db7e9c2b423d76defb65ec9b1f8500c56621
attack_rows_sha256=f054ffbfa30884c1aa2383c514b6f3c504d8104af4f7b8974a76e0528599461d
verification_file_sha256=f8acc3150d4663d92976a44ab1c3b35c7264f4c4d14808f9133f1184d3f4b590
verification_object_sha256=774813f546184aa30c342840ddfa6b0566ebe4d382acd16d74ead8f03dadaddc
```

The attack and verification file hashes were fixed by exact zero-credit
candidate admission.  Formal promotion subsequently published those exact
bytes.  The producer was not imported, executed, parsed, or tokenized by the
verifier; it was treated as pinned inert bytes.

## Exact universe and denominator

```text
members=564492
occurrences=431208
  preserved_Round266=126468
  new_Round288=295336
  new_Round292=9404
virtuals=133284
  positive_3D=94660
  sheets=38624
    Round248=38360
    inherited_Round245=264
official_keys=124
components=92688
minimum_component_size=1
maximum_component_size=10599
all_unordered_pairs=159325326786
within_component_pairs=487242432
cross_component_pairs=158838084354
component_size_histogram_sha256=4cae509311127a2451a3b36fb8ada073cfdaa95af466843bfdf4c4d8dd21bc6b
```

The six identity-class pair totals are exact and sum to the full unordered
pair denominator:

| Pair class | Pairs |
| --- | ---: |
| occurrence / occurrence | 92,969,954,028 |
| occurrence / positive-3D virtual | 40,818,149,280 |
| occurrence / sheet virtual | 16,654,977,792 |
| positive-3D virtual / positive-3D virtual | 4,480,210,470 |
| positive-3D virtual / sheet virtual | 3,656,147,840 |
| sheet virtual / sheet virtual | 745,887,376 |

Official-key equality is explicitly not used as a routing filter.  A later
maximality proof must allow and exhaust physically legal cross-key adjacency.

## Exact ledger commitments

| Ledger | Rows | File SHA-256 | Ledger SHA-256 | Rows SHA-256 | Row IDs SHA-256 | Row hashes SHA-256 |
| --- | ---: | --- | --- | --- | --- | --- |
| Member support/source | 564,492 | `c9a8649c8473bb6a170187e7f803e95748d2ff2198b1b846d97383dd5f0581af` | `58ad4ebe98be5023f31870a0d0d3e0d135d153553393aa56a67f4ef1760f68a3` | `c7dfb5534fddeb22fffb81bf539fe44d837aced46577aa5f490a0ae14aba77f5` | `87b4d34c40c3c1caf053ccb9b4c6c6c32cf6a33ac184f6181864105b500b6d3a` | `382e7a7ae0e857b812635e0d4bb10571d1aa459a27acd178d81b12f9c68d6285` |
| Component census | 92,688 | `d489b8480859d51ac6d98c9c59bc25c71c3cc6d0ffb1e0e13ddb988ecc80b8a7` | `bf55a27d4f34886a2656822783b91d0f68644bd2c248023487580d4b4aa7c681` | `4bc8edcd12855ab10e5fefe8c37b40eaf85e4f2c414d4303606e492899f728ec` | `c6ac54f54f11a5806804afd245c7ebb9788415f6753bbeae41d28c7b8d4c3cb7` | `822820be6147708555f0c5bbe71e728ebcc818fa170390372b92d4440006805a` |
| Pair denominator | 6 | `f8e22c93a0b070ae3ff2da557c1011ba74a214fbf4b841cdfeb219a2556f6261` | `7ca51af3afd4524f62d202649731e461472678e913cc975e0b8127fc4e19e5e3` | `63ebcc7713a6fdf5b4d6d96148802e88a2ec39f6a847d5eadfa4f7f906787cde` | `a1a4405b9f9f8090cbc592553effb169e046adb5ee06b17d93f8c862c53ca85c` | `d37b7b2b239f221ce70df0f565483dcb16ba0eaf6e4b45eeefaf5c6f89e49cb1` |
| Source-table inventory | 15 | `39ebbf26976b3c1e7b79b043f2f801d568638583a01fff8830f8886148a23fc3` | `817129ae66c30a351d8f452a66feb6bbe99591bcb7338f4a152ef425903194be` | `8efd11586a7443a505253d42e5672a04c4be97d3626c73acbe175a6ff3dd4392` | `b69cd80e13a69dfb3609f6b19d34a73189c5385dd66c1a9fdbad38e6bdae6061` | `2ba37c084ab4608244f5c8c3eed34177dd256f3a1c26da2235238a83c9c13859` |
| Source-binding gap | 0 | `b214bbb55a06e275c1b00f2f12e5f1e128840d3ed9b81cf474151a4e93af7f55` | `3168e2b042abcdf0e1ee1df93490e694420e049d10d34434d232ce934833e700` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |

All five ledgers use deterministic single-member gzip encoding with `mtime=0`
and an empty stored filename.

The zero-row source-binding gap means that every current member has an exact
primary-source binding.  It does not mean that geometry-feature coverage,
cross-component pair routing, or maximality has been proved.

## Independent production, admission, and promotion

| Run | Effective mode | Outcome | Elapsed | Maximum RSS |
| --- | --- | --- | ---: | ---: |
| Superseded v1 seed A | `PYTHONHASHSEED=306001` | complete; quarantined, never formal | `8:31.91` | 698,556 KiB |
| Superseded v1 seed B | alternate seed | interrupted; no target or stage survived | `5:06.27` before interruption | not asserted |
| v2 seed A | `PYTHONHASHSEED=306101` | exit 0 | `8:20.79` | 692,640 KiB |
| v2 seed B | `PYTHONHASHSEED=306997` | exit 0 | `5:04.06` | 697,124 KiB |
| Initial admission with pre-fix verifier | isolated `-I` | fail-closed; no formal writes | `6:05.93` | 548,308 KiB |
| Exact v2 candidate admission | isolated `-I` | exit 0 | `6:03.18` | 551,324 KiB |
| Formal v2 promotion | isolated `-I` | exit 0 | `6:13.36` | 550,616 KiB |

The two v2 six-file candidates are byte-for-byte identical.  Ten gzip
integrity checks pass.  The initial admission failure exposed an incomplete
exact-key expectation in the verifier for `virtual_count`,
`R248_sheet_count`, and `R245_sheet_count`.  The verifier was fixed, its
14-key universe regression was added, and the failed attempt wrote no formal
object.  Only the final verifier hash shown above is part of this package.

The superseded v1 candidate is recoverably quarantined under
`.cm2-round306b0-superseded-v1/`; schema v2 rejects it and no downstream
consumer may treat it as formal input.

## Attack and atomic-publication boundary

The formal attack bundle rejects `18 / 18` semantic contract units, `3 / 3`
strict candidate-wire grammar attacks, and `6 / 6` real filesystem transaction
attacks: `27 / 27` total.  Both producer and verifier lightweight self-tests
pass; the verifier self-test also reports `27 / 27` rejected attacks.

The formal transaction order is exactly:

```text
attack -> member -> component -> pair -> source -> gap -> result -> verification
```

The verification file is the sole final credit marker.  Marker validity
requires the complete marker-bound eight-file transaction bundle.  Publishing
uses no-clobber `renameat2(RENAME_NOREPLACE)`, exact-prefix recovery, and fsync
of stage and output directories after each rename.  Mtime is diagnostic only;
the observed attack and verification mtimes are respectively
`2026-08-01 15:42:40.826646651 +0800` and
`2026-08-01 15:42:44.447262505 +0800`.

Post-promotion live checks passed exactly:

```text
formal_candidate_cmp=6/6
formal_gzip_integrity=5/5
result_attack_verification_object_self_hashes_close=3/3
all_eight_transaction_files_mode_0600_nlink_1=true
orphan_promotion_stage_count=0
formal_attack_file_matches_admission=true
formal_verification_file_matches_admission=true
```

## Exact credit boundary and next step

The formal marker makes the following transition:

```text
member_universe_freeze: 0 -> 1
pair_denominator_freeze: 0 -> 1
maximality: 0 -> 0
fibre: 0 -> 0
global_disposition: 0 -> 0
official_fibres_exhausted=0
Source_G_global_dispositions_completed=0
D02_status=BLOCKED
CM2_status=NO-GO_FOR_CLAIM
```

Round306B1/B2 must now expand exact 3D/2D/1D/0D support features and
losslessly route all `158,838,084,354` cross-component member pairs across
transformed-face, cross-chart, retained/event, seam/rechart, sheet, and
occurrence-fibre channels.  Any newly admitted cross-component legal edge is
a fail-closed `NO-GO` for the current quotient and requires a new edge theorem
followed by another fresh DSU rebuild.
