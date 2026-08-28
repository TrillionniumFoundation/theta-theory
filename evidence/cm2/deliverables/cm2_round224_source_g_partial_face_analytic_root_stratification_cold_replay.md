# Round224 cold replay

## Frozen hashes

| object | SHA256 |
|---|---|
| producer | `8bb6bd227be21d2c2c6e34394e4f83257f502bb9ab621355a306d5a20757336b` |
| certificate | `9ff49f0a55c0048f8dc7b636b1ddcc7291e01545e9775d95cb9738f4b3f237c7` |
| certificate result | `2015369b8f5eef92da2245981157bf4dbacc55a69939b087d893f954f3374ab8` |
| verifier | `70d7deb36cbafdde646051b8bdf6854764dea4ae9819a1c504f9cdc372cb7fdb` |
| verification | `2bbe71d59da32b89a63b5425c716863befab0c9b0825051b836e12a052a7115d` |
| verification result | `406b4e61f92cb017af502398a08209555a1971d5066042cb80236e5c835b221a` |

## Producer replay

| seed | output | elapsed | max RSS |
|---:|---|---:|---:|
| 224051 | official certificate | `1:24.08` | `1,888,100 KiB` |
| 224052 | hidden isolated replay | `1:24.79` | `1,888,440 KiB` |

The two producer outputs compare byte-for-byte equal (`cmp=0`).  Both have
certificate SHA256
`9ff49f0a55c0048f8dc7b636b1ddcc7291e01545e9775d95cb9738f4b3f237c7`
and result SHA256
`2015369b8f5eef92da2245981157bf4dbacc55a69939b087d893f954f3374ab8`.

## Verifier replay

| seed | output | elapsed | max RSS |
|---:|---|---:|---:|
| 224061 | official verification | `1:38.60` | `1,784,964 KiB` |
| 224062 | hidden isolated replay | `1:39.54` | `1,785,296 KiB` |

The verification outputs compare byte-for-byte equal (`cmp=0`).  Each run
independently rebuilds the expected Round224 object and rejects
`18/18 + 15/15 + 21/21` hostile cases.

## Cleanup and boundary

After byte and SHA comparisons, both hidden replay files are deleted.  They
are not part of the formal six-object package.

The cold-replayed boundary is `264/264` completed partial contacts, zero
remaining partial contacts, and zero component/whole/global credit.  The next
formal action is the connectivity quotient rebuild.

