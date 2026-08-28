# CM2 Gates 3/4: positive all-scale core-hit charge

Date: 2026-07-17 (Asia/Shanghai)  
Frozen inputs: selected actual-parameter germs, the typed core/cemetery
ledger, and the frozen 24-core registry  
Strict verdict: **two selected occurrences, hence four oriented branches,
contain explicit positive coordinate cylinders that enter strict interiors
of two frozen cores after 20 post-suffix collisions.  This is the first
positive physical core-hit charge, but it is not a uniform fraction of all
128 branches and does not close Gate 4.**

## 1. High-precision shooting and interval expansion

Binary64 screening was used only to propose candidates and was explicitly
rejected when chaotic roundoff changed the long itinerary.  Final shooting
and replay use 1024-bit Arb.  The selected reference-row shifts are

```text
occ:f2b4833eb8dccd403eec3485: 3/2251799813685248,
occ:c5fde0378e6e76eec93a0ceb: 1/4503599627370496.
```

Around each shifted source point, both hit and miss branches are certified
on

```text
base-z half-width = 2^-220,
every parameter scale 0<|h|<=2^-220.
```

The hit side includes the grazing square-root limit by a nonnegative Arb
enclosure.  Both sides reach the same regular suffix chart and then follow a
common 20-target future word.

## 2. Core entrance

Across the four branches the certificate validates

```text
84 suffix and post-suffix flights, all strictly in (0,2),
no intermediate collision singularity,
20 post-suffix collisions to a core,
2 strict destination-core interiors.
```

The labelled base-parameter coordinate volume is exactly `2^-437`.  It is
strictly positive but is not identified with collision-SRB mass.

## 3. Strict frontier

```text
POSITIVE ALL-SCALE CORE-HIT OCCURRENCES:            2 CERTIFIED
POSITIVE ALL-SCALE ORIENTED BRANCHES:               4 CERTIFIED
POST-SUFFIX COLLISION TIME TO CORE:                 20 CERTIFIED
POSITIVE LABELLED COORDINATE VOLUME:              2^-437

ALL 128 SELECTED BRANCHES CHARGED:                 NOT CERTIFIED
GLOBAL SELECTED CORE-HIT FRACTION:                 NOT CERTIFIED
QUANTITATIVE CEMETERY TAIL:                        NOT CERTIFIED
POST-CORE 2018/12108 NATIVE DWELL:                 NOT CERTIFIED
COMMON STRONG-SPACE RECOVERY OPERATOR:             NOT CERTIFIED
GATE 3 / GATE 4:                                  NOT CERTIFIED
```

Replay and integrity pass, the verifier rejects `24/24` hostile mutations,
and live mode exits `2`.
