# Round219 cold replay

## Frozen formal objects

| object | SHA256 |
|---|---|
| producer source | `8b670ffbcabd5a9796fb67580cbb9e3318b8eb2ee1cd65c5e71f7f1f360b3019` |
| official certificate | `8341a8b08a0abd5c7a16c61b918b7b47db4d05c3c4e6fae8615892e3aafaf096` |
| certificate result | `f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e` |
| independent verifier source | `c8fe996f8a6c4faf22d51862e3f4c4a28d405c653159054841c962b6ad1c841c` |
| official verification | `564778c5172751006e5035f13a0caf421dcdc36ace1d61f28a1260d9ec24681c` |
| verification result | `e570f360e1d52380f708ea828501ab83846ce4e843445bf1d8230dc49f42c5ad` |

The official certificate embeds the frozen producer SHA exactly, and the
official verification embeds the frozen producer, certificate, result, and
verifier hashes.

## Producer replay

The frozen producer was run into three distinct paths:

| seed | output | exit | elapsed | max RSS |
|---:|---|---:|---:|---:|
| 219052 | official certificate | 0 | `4:53.19` | `1,533,628 KiB` |
| 219051 | hidden isolated replay | 0 | `4:53.88` | `1,527,204 KiB` |
| 219053 | hidden isolated replay | 0 | `4:57.39` | `1,528,916 KiB` |

Both hidden producer outputs compare byte-for-byte equal to the official
certificate (`cmp=0`), and the two hidden outputs compare equal to each
other.  All three file SHA256 values are
`8341a8b08a0abd5c7a16c61b918b7b47db4d05c3c4e6fae8615892e3aafaf096`;
all three result SHA256 values are
`f8d46a9a220b6b7e0e6f86430ad6d537d5358cd610f064417ab3e8b4c125744e`.

## Independent verifier replay

The verifier reconstructs the complete expected Round219 object before
loading the candidate.  It does not import or execute the Round219 producer.

| seed | output | exit | elapsed | max RSS |
|---:|---|---:|---:|---:|
| 219061 | official verification | 0 | `18:23.93` | `3,369,484 KiB` |
| 219062 | hidden isolated replay | 0 | `18:18.18` | `3,369,840 KiB` |

The hidden verification compares byte-for-byte equal to the official
verification (`cmp=0`).  Both file SHA256 values are
`564778c5172751006e5035f13a0caf421dcdc36ace1d61f28a1260d9ec24681c`;
both verification result SHA256 values are
`e570f360e1d52380f708ea828501ab83846ce4e843445bf1d8230dc49f42c5ad`.

Each successful verifier run reports:

- full expected Python-object equality;
- full expected canonical equality;
- `52,292 / 52,292` terminal subfaces;
- `7,484 / 7,484` exact-contact partitions;
- `264 / 264` partial-contact probes;
- `21/21` genuinely re-signed semantic attacks rejected;
- `15/15` strict JSON attacks rejected;
- `19/19` filesystem/path/output attacks rejected; and
- zero duplicate literal dictionary keys.

The path suite includes input and output symlink-parent aliases and an output
parent-`..` alias.  A preliminary replay invocation supplied a relative
output parent; after all verification and attacks passed, the frozen
raw-parent guard rejected that invocation before writing any file.  It is not
counted as a cold replay.  The successful seed-219062 invocation used the
exact absolute allowlisted parent and reran the complete verifier from
scratch.

## Cleanup and strict boundary

After all SHA and byte comparisons, the two hidden producer files and hidden
verification file were deleted.  No hidden replay or temporary output is part
of the six-object formal package.

The cold-replayed boundary remains:

- newly complete exact-contact common refinements: `468`;
- cumulative exact-contact prefix: `916 / 7,932`;
- remaining exact contacts: `7,016`;
- remaining unresolved terminal subfaces: `7,236`;
- partial zero absences: `28`;
- remaining partial contacts: `236`;
- component/whole-origin/global credit: `0`;
- source-G dispositions: `0 / 224,580`;
- D02: unchanged `BLOCKED`;
- Gate5: unchanged `10/18`; and
- CM2: unchanged `NO-GO`.

