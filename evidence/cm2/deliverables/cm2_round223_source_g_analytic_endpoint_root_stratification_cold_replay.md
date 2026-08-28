# Round223 cold replay

## Frozen formal objects

| object | SHA256 |
|---|---|
| producer source | `fb5d46a31857cb09c2606747d4fbec996eecffdf65702431a17624a2260ad970` |
| official certificate | `3d28f097419e11bde6733462736fcb70cd0164b18ac06a793a34b5dc26113168` |
| certificate result | `db012bb2e68176c8a5c144455bac9ff780521bbfa3c03110694390c70a3343d9` |
| independent verifier source | `c67d5898a24e04e367f46fa3ffc67e6773de69616287877e88c89e5e417819e6` |
| official verification | `e5e48f7553580f36710e0f7de9c3a59f866fcad434bc1f2ae9e151900372b820` |
| verification result | `5191d6e993678bb2f9fdd437b4bbea580d0d2fec9887b55eacfe75d1a548977e` |

The official certificate embeds the frozen producer SHA exactly.  The
official verification embeds the frozen producer, certificate, result, and
verifier hashes.

## Producer replay

The frozen producer was run into three distinct paths:

| seed | output | exit | elapsed | max RSS |
|---:|---|---:|---:|---:|
| 223051 | official certificate | 0 | `1:46.68` | `1,784,840 KiB` |
| 223052 | hidden isolated replay | 0 | `1:48.12` | `1,785,240 KiB` |
| 223053 | hidden isolated replay | 0 | `1:49.09` | `1,784,720 KiB` |

Both hidden producer outputs compare byte-for-byte equal to the official
certificate (`cmp=0`), and the two hidden outputs compare equal to each
other.  All three file SHA256 values are
`3d28f097419e11bde6733462736fcb70cd0164b18ac06a793a34b5dc26113168`;
all three result SHA256 values are
`db012bb2e68176c8a5c144455bac9ff780521bbfa3c03110694390c70a3343d9`.

## Independent verifier replay

The verifier reconstructs the complete expected Round223 object before
loading the candidate.  It does not import or execute the Round223 producer
or either Round221 outcome-blind probe.

| seed | output | exit | elapsed | max RSS |
|---:|---|---:|---:|---:|
| 223061 | official verification | 0 | `7:28.92` | `2,218,204 KiB` |
| 223062 | hidden isolated replay | 0 | `7:40.48` | `2,218,416 KiB` |

The hidden verification compares byte-for-byte equal to the official
verification (`cmp=0`).  Both file SHA256 values are
`e5e48f7553580f36710e0f7de9c3a59f866fcad434bc1f2ae9e151900372b820`;
both verification result SHA256 values are
`5191d6e993678bb2f9fdd437b4bbea580d0d2fec9887b55eacfe75d1a548977e`.

Each successful verifier run reports:

- full expected Python-object equality;
- full expected canonical equality;
- `7,236 / 7,236` endpoint-edge partitions;
- `8,000 / 8,000` terminal edge segments;
- `7,232 / 7,232` exact analytic roots;
- `28,932 / 28,932` exact symbolic strata;
- `7,232 / 7,232` endpoint-to-curve joins;
- `7,016 / 7,016` newly completed exact contacts;
- `18/18` genuinely re-signed semantic attacks rejected;
- `15/15` strict JSON attacks rejected;
- `21/21` filesystem/path/output attacks rejected; and
- zero duplicate literal dictionary keys.

The path suite includes input and output symlink-parent aliases and explicit
parent-`..` aliases.  Every successful replay used an exact absolute
allowlisted output parent and rebuilt the complete expected object from
scratch before candidate loading.

## Cleanup and strict boundary

After all SHA and byte comparisons, the two hidden producer files and hidden
verification file were deleted.  No hidden replay or temporary output is part
of the six-object formal package.

The cold-replayed boundary is:

- cumulative exact `p/s` contacts: `7,932 / 7,932`;
- remaining incomplete exact `p/s` contacts: `0`;
- analytic endpoint roots: `7,232`;
- newly completed exact contacts: `7,016`;
- remaining partial contacts: `236`;
- component/whole-origin/global credit: `0`;
- source-G dispositions: `0 / 224,580`;
- D02: unchanged `BLOCKED`;
- Gate5: unchanged `10/18`; and
- CM2: unchanged `NO-GO`.
