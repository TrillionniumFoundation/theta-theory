# Round306A fresh R305B-extended legal-component DSU rebuild — exact promotion report

Status:
`PASS_EXACT_CACHELESS_ROUND306A_FRESH_LEGAL_COMPONENT_DSU_REBUILD`.

Round306A starts from a new empty integer DSU over exactly `564,492`
extended-registry members and `367,964` base roots.  It reconstructs all
`478,710` sealed Round304 legal edge applications and then appends exactly the
eight independently sealed Round305B canonical component edges.  The complete
fresh application has `478,718` edge applications, `275,276` rank reductions,
and `92,688` final components.  Forward and reverse application reconstruct the
same partition:
`a3f7ce1e28a956a46803ef466709ded0053633f5e104746c6d1e6e51b873e19c`.

No serialized Round304 partition is loaded as state.  Round306A is a
replacement certificate that supersedes the Round304
`478,710 / 275,268 / 92,696` quotient; the new `275,276` rank total is not
added to the old `275,268` total.

## Frozen implementation and dependency pins

```text
producer_file_sha256=ab798332c82f7aa3656c61e3b31698a30b0fa1a83d24900432e076e445d6f5d5
verifier_file_sha256=60cc0f9cec6c8f4121f7ed7fde45b11e1b72bd9adc897364d9c0937c92a54c72
schema_snapshot_sha256=abfe46bd4ce053ec78af31a1e159dfe9325dac2da9952493058c86b891d1f2ae

Round304_verifier_engine_sha256=f605191b318b7d82106d8f7a872ea8101a59ffdf39999ad48fce9d44888d13fb
Round304_manifest_sha256=de49f4233f6a22f43385e727071c5a5ebac68c35788dc2dd13e71d045639838c
Round304_partition_sha256=72a745845f322255b95bfabb4b7254709e3f7c40359a0314e96b8e0d91c4bcff
Round305B_manifest_sha256=1b80e7470e1ad1893f9323f47c64bd0d1aa48b35e0920c0821b25fe316b7dca7

result_file_sha256=febe77da4285791b54e098c80a4b868c1e5dc6e43e98a7553bfff5e065075010
result_object_sha256=6ee906cddae42e6df086cec26c7e0898ebe198519ce96605fd609a20c4f1e46a
attack_file_sha256=9e3f2bcf3f39af739bc05ca2f3acef2828f96e6f19402fe6a85bb3353f5fc25e
attack_object_sha256=215edf7d7071739d1711ad7b616b8c9f6d2e7fa51ab01f7d7c19cbf42039a7bb
attack_rows_sha256=26dafe27e0ce7ba37492abaeb0eea713cc4a458f0b886313d983ef30a201c5ea
verification_file_sha256=38fd7f9d41dcf39a2ec887d72b31da3d003cf03eda154da34d3a5d87ff12ba7e
verification_object_sha256=147372b651a11aec9101da717bbd82c2a744a801a2c581d130fe7c03464f5f9e
```

The attack and verification file/object hashes were first fixed by exact
zero-credit candidate admission.  Formal promotion subsequently published
byte-identical attack and verification objects.

## Exact ledger commitments

| Ledger | Rows | File SHA-256 | Ledger SHA-256 | Rows SHA-256 | Row IDs SHA-256 | Row hashes SHA-256 |
| --- | ---: | --- | --- | --- | --- | --- |
| Edge application | 478,718 | `6da4620a100c980f921350f162fda064580e603f8ff7221eeed768b8bd091d1f` | `d253106bf33d892e254fa49dcd63a1e470600e827b61a20a34d401701303be1d` | `e3bf699433e828b345cc7da624b03f2768e5e427ce6bdf12b10543d08a718d4a` | `31a9000f3e93f38698cf5f114a2f237924b381e3a3b2a143ce9cdcd01d254df5` | `dfd479ca56965f7b63644b296596587560b74ef0ace88999f2132918e689794d` |
| Member/component | 564,492 | `710ebb660a7e7fad6a691c03bf845cf0081037ed09cc49a885c94c4bc472c276` | `42d02c90e9e607f2d1c6ae53f5d2f67f0205c023f918a40fb1b64bec0213cafc` | `43bc3ca15f58b6dd089b776c6c21f68fb246eb6af0590974129e20beef93eabd` | `befaf5ae8a8ae109912649201e5efd90a03898edc02b5518cadec93e1f835165` | `003ecfe414434477a404c7b1912bfd117e98fc4883faee36119144b877f923ad` |
| R305B promoted edge | 8 | `08f9ff2f5df0210cedd8cb3f8d998846e3722bd6bb0a2216d8d6c24a95a64a41` | `1a88f452735c244fd8285ae7a89f1a499ac62f1d0ed265c446bff922865a9398` | `5b11b8e81be332ec7dd6b0a5f43fa37de9515ee538646c0c63a7c5746f30192e` | `7d2a6a4de0dc3e01b3c4833e2738998d76966360d8f0bcf8201a3c5fc6e3ed8c` | `9150090596043a3f9eb20c8999791dcea1790fd924da6987d835da9215f1936e` |
| R300A reprojection | 3,232 | `c3e62f9833c333fb89758edd5c3f1648364a70b91bd1ed85650241a4cd10b673` | `e67bed73cb2b871460ee80a465a518be7340a0af33b9758a6e137016d1071e01` | `2b5feadb5eb00912f459422ef5dc6137c0658d57049f8345da6293c9fc6e4ea0` | `922dc65852c22574626bbc7bbd0b90dfbd216ce64a540f098163e216067f9e8a` | `3a74f0d7cb378bda3d61c8a170950c129abfd1135d9aea4dacc1ddf4f168b368` |
| W-tail disposition | 4 | `6bdcc231b3cfd67f18ff3c62c27af08fdc9eb562a2c4e24a601798c0ad6d2556` | `b7232d207f587de52ffb4ffb23d6c1cd9d22a76aebb09ac19aa360cc0bb01ee6` | `9f5eb2a68d6d5804d3cdebb0493e34a0b58be23f0cb78fa4c4824ab2abd94707` | `05880fa19289820e0d8d15e9e60bca0f8e5b3a6bc9b83bbdda96ec9274dbda53` | `8a626525b8ca65163e50133c6ecd24d0e77be242f41544ef9b8290e523f0cd2a` |
| Residual gate | 1 | `1e79d529f3ca1fcefa170263a5d8b88929361ea27c0eeb3c6de108b870f9d8b8` | `8ca2c8b339fa1a57c54a619cf670777c0acac2cd3d5e4d5cd589511b6462596b` | `52af1c720e57e3fc04540ebc20be6fd264eb6b32d3fa7d4dca28dd965002e77d` | `33ade8aafaf1e0863719e0db53d51b8fc015d8ede353f5b30f1f8a855e3163c1` | `b91e12a97dffc7f450b55d72d74fd60e7125a9d320f42842a548f3aa0edb5324` |

All six ledgers use deterministic single-member gzip encoding with `mtime=0`
and an empty stored filename.

## Round305B consumption and Round300A closure

The sealed Round305B package contributes `1,024` physical witness rows as
provenance for exactly eight canonical component-edge applications.  Witness
rows are not union rows.  The eight edges connect sixteen distinct Round304
components and all eight reduce rank.

The complete Round300A reprojection has `128` prior witnessed rows already in
one component, `2,080` rows reclosed by another legal DSU path, and `1,024`
rows reclosed by a Round305B physical edge.  Its cross-component residual is
exactly zero.  This closes only the exact `3,232`-row Round300A frontier; it is
not a full maximality theorem.

## Independent replay, admission, and formal promotion

| Run | Effective mode | Exit | Elapsed | Maximum RSS |
| --- | --- | ---: | ---: | ---: |
| Producer default process | CLI seed `306101`; `PYTHONHASHSEED` unset | 0 | `28:05.16` | 2,634,612 KiB |
| Producer named seed A | CLI/hash seed `306101` | terminal receipt lost | not retained | not retained |
| Producer named seed B | CLI/hash seed `306997` | 0 | `31:35.21` | 2,631,044 KiB |
| Independent verifier no-write | `PYTHONHASHSEED=306551` | 0 | `28:36.59` | 2,576,912 KiB |
| Exact candidate admission | isolated `-I`; no seed claim | 0 | `28:04.74` | 2,575,972 KiB |
| Formal promotion | isolated `-I`; no seed claim | 0 | `33:06.27` | 2,577,576 KiB |

The named-seed-A terminal timing/exit receipt was lost during an interrupted
turn and is not reconstructed.  Its complete seven-file output survived,
passed gzip and canonical-result validation, and is byte-for-byte equal to the
default and named-seed-B candidates.  All three candidate directories are
mode `0700`; all candidate files are regular, mode `0600`, and link count one.

The independent no-write verifier returned
`PASS_INDEPENDENT_CACHELESS_NO_WRITE_ROUND306A_RECONSTRUCTION`, opened no
candidate, wrote no candidate or formal output, and treated the producer as
inert pinned bytes.  Exact admission returned
`PASS_EXACT_ROUND306A_PRIVATE_CANDIDATE_ADMISSION__ZERO_FORMAL_CREDIT`.
Admission created and removed temporary filesystem-defense fixtures, so the
correct claim is no candidate or formal output, not no filesystem writes.

## Attack and atomic-publication boundary

The formal attack bundle rejected `28 / 28` semantic contract units,
`28 / 28` exact-wire units, and `9 / 9` real filesystem transaction attacks.
One positive partial/invalid-stage recovery self-test also passed.  Thus there
are `65` rejected attacks and `66` total defense scenarios.  The lightweight
self-test object hash is not used as the formal attack object hash.

The formal transaction order is exactly:

```text
attack -> edge -> member -> R305B-promoted-edge -> R300A-reprojection ->
W-tail -> residual -> result -> verification
```

The verification file is the sole final credit marker.  Marker validity
requires the complete marker-bound nine-file bundle; mtime is diagnostic only.
The observed attack and verification mtimes were respectively
`2026-08-01 14:19:25.742619331 +0800` and
`2026-08-01 14:19:31.972408979 +0800`.

Post-promotion live checks passed exactly:

```text
formal_attack_file_matches_admission=true
formal_verification_file_matches_admission=true
all_seven_formal_candidates_equal_private_candidate=true
all_six_formal_gzip_members_pass=true
result_attack_verification_object_self_hashes_close=3/3
all_nine_transaction_files_mode_0600_nlink_1=true
orphan_promotion_stage_count=0
```

## Exact credit boundary and next step

Round306A formally admits `478,718` fresh legal edge applications,
`275,276` fresh rank reductions/unions, one replacement component quotient,
and `92,688` post-Round306A components.  Its incremental Round305B rank credit
is exactly eight.

It grants zero maximality, official-fibre exhaustion, or global-disposition
credit.  Source-G global dispositions completed remain `0`; D02 remains
`BLOCKED`; unconditional CM2 remains `NO-GO_FOR_CLAIM`.

Round306B must next perform fresh exhaustive maximality routing over all
transformed-face, cross-chart, retained/event, lower-stratum, and
occurrence-fibre channels.  No fibre or Source-G disposition credit is
authorized before that dependency passes.
