# Round217 cold replay

## Frozen formal objects

| object | SHA256 |
|---|---|
| producer source | `687fd48134e204a99c807e1fd18954cef7633879396db5f4d291ece1568dfa66` |
| official certificate | `1ccf9b4bf65bb4f45603594ea19f47e3b2103ea682bebfff0b023234308938fd` |
| certificate result | `fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286` |
| independent verifier source | `172167d8e0c992645e0e5f546628be052868275808a5db733f3e5507daecaf71` |
| official verification | `13b6b3d3b2879d950c722e1ce92ad729f207a6abbb433d08acf0e22ae0d4cbda` |
| verification result | `48dd5123517f07bda9aa84ce76edd8e10e3baf1cc3924ad9e1398c1f3f28fb75` |

The official certificate's embedded producer provenance is exactly
`687fd48134e204a99c807e1fd18954cef7633879396db5f4d291ece1568dfa66`.

## Producer replay

The producer was run into three distinct paths after the source freeze:

| seed | output | exit | elapsed | max RSS |
|---:|---|---:|---:|---:|
| 217052 | official certificate | 0 | `2:02.04` | `1,499,544 KiB` |
| 217051 | hidden isolated replay | 0 | `2:04.11` | `1,500,036 KiB` |
| 217053 | hidden isolated replay | 0 | `1:59.51` | `1,499,848 KiB` |

Both isolated replay files compare byte-for-byte equal to the official
certificate (`cmp=0`).  All three SHA256 values are
`1ccf9b4bf65bb4f45603594ea19f47e3b2103ea682bebfff0b023234308938fd`,
and all three result SHA256 values are
`fb4519a43f76cbc765e24b3cb0a0e25267d9664091e22139913f3899fd1e2286`.

## Independent verifier replay

The verifier does not import or execute the producer or Round214 probe.  It
rebuilds the full expected certificate from the pinned Round204, Round208,
Round209, Round211, Round214-report, and Round186 evaluator boundaries.

| seed | output | exit | elapsed | max RSS |
|---:|---|---:|---:|---:|
| 217061 | official verification | 0 | `4:35.14` | `3,059,048 KiB` |
| 217062 | hidden isolated replay | 0 | `4:31.14` | `3,059,416 KiB` |

The hidden verification compares byte-for-byte equal to the official
verification (`cmp=0`).  Both SHA256 values are
`13b6b3d3b2879d950c722e1ce92ad729f207a6abbb433d08acf0e22ae0d4cbda`,
and both verification result SHA256 values are
`48dd5123517f07bda9aa84ce76edd8e10e3baf1cc3924ad9e1398c1f3f28fb75`.

Each verifier run reports:

- full expected Python-object equality;
- full expected canonical equality;
- 448/448 trace rows;
- 896/896 incidence rows;
- 448/448 glue rows;
- 7,484/7,484 exact fail-closed frontier rows;
- 264/264 partial fail-closed frontier rows;
- 25/25 re-signed semantic attacks rejected;
- 15/15 strict JSON attacks rejected;
- 16/16 filesystem/path attacks rejected; and
- zero duplicate literal dictionary keys.

## Round214 third-seed corroboration

The independently run `PYTHONHASHSEED=214053` Round214 probe produced
`156,006` canonical stdout bytes with SHA256
`9a90e2f01cf03b263803298ba1977c9ecfa6e70778698ea13e28a7fdcbc071d7`,
matching seeds 214051 and 214052.  It exited 0 in `54.88s`, with maximum RSS
`946,276 KiB`.

## Superseded pre-freeze object

Before the complete per-key ordinal maps were added, producer SHA
`29dc995327237e58c78e6bce85edb9593c106f4170f65d7409948ba66ef7aa91`
generated certificate SHA
`1f9e9ae63d27335557b4e107906fa38a663969f17edf855d8a2d423dfca1acb2`
and result SHA
`745e1ca633fbd84f0989d17ac4cbe3b72a6b887a01d2bdf9054b42541c7abcc6`.

That pre-freeze object was superseded.  A brief observation paired the newly
edited source with the not-yet-overwritten old certificate; the old
certificate itself embedded the old source hash.  It was not same-source
nondeterminism.  The superseded certificate is absent and is excluded from
the manifest.

## Cleanup and immutable boundary

After byte comparisons, the two hidden producer replay files and the hidden
verification replay file were deleted.  No replay file, temporary output, or
superseded certificate is part of the six-object formal package.

The cold-replayed formal boundary remains local:

- component-deduplication credit: 0;
- whole-leaf/origin/tube credit: 0;
- global component/fibre/disposition credit: 0;
- D02: unchanged `BLOCKED`;
- Gate5: unchanged `10/18`; and
- CM2: unchanged `NO-GO`.
