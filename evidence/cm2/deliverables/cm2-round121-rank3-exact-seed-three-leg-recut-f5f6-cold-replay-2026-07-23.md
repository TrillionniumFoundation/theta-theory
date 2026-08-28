# CM2 Round121 cold replay

Date: 2026-07-23

## Frozen code and logical digests

```text
producer             30c69e1849867841398483749f547a7840d401bc3cc24b9e4ef0a4892ad990ed
certificate          ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e
certificate result   962db517d76b18e7681c411734b568491e600776dbf5317d9ebff8494a9aebd8
verifier             d35c0e04b9d339c1271533abdefa5addcb73096b70abdec94d60e475daa45e95
verification         ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80
verification result  8c830e2e26d9b4cce6f034ad382420bf7c7aac0b422979b14e88888fe1b888e5
```

## Producer replays

Two clean producer runs used different hash seeds and fixed locale/timezone:

```text
PYTHONHASHSEED=121731 LC_ALL=C TZ=UTC
PYTHONHASHSEED=912107 LC_ALL=C TZ=UTC
```

The canonical certificate and both temporary outputs have exactly the same
SHA256:

```text
ba56b41a41fbf0d77c6467fcb5fc521ef4d6928f65a9f79d5bba8b83c9b4fc6e
```

Both `cmp` checks pass.  The exact seed, interval brackets, endpoint order,
recut rows, common-refinement rows and 720 slots are byte-stable.

## Independent verifier replays

Two additional complete 2048-bit verifier runs used:

```text
PYTHONHASHSEED=121917 LC_ALL=C TZ=UTC
PYTHONHASHSEED=791121 LC_ALL=C TZ=UTC
```

The canonical verification and both temporary outputs have exactly the same
SHA256:

```text
ec527c19a8c50025514db0769808ce21aeb53c7d1cc64edb75f1a9c5a6aa3e80
```

Both temporary outputs compare byte-for-byte equal to the canonical
verification.  Every replay reports:

```text
verdict                         PASS
verification precision         2048 bits
upstream/helper pins            43
exact analytic b seeds          1
stage natural cells             1 / 7 / 18
pullback internal cuts          23
stage recut rows                26
common actual children          24
refined subbranches             24
full-key F1-F6 slots            720
F5 slots                        120
F6 slots                        120
semantic mutations rejected     79
strict-JSON mutations rejected  15
rank3 seed-child maturity       6/18
global Gate5 maturity           10/18
complete 18-field blocks        0
CM2                             NO-GO_FOR_CLAIM
```

The byte comparison includes every independently recomputed rational
enclosure, all ordered replay rows and the complete attack-label ledgers.
