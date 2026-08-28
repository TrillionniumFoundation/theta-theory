# Round300-C positive-volume edge promotion: dual-seed cold replay

## Verdict

PASS.  Two final cacheless independent-verifier runs with distinct seed and
`PYTHONHASHSEED` values reconstructed all sealed inputs, all 94,660 retained
positive 3D carriers, all 231,503 exact candidate comparisons, all 6,322
witnesses, and all 6,314 canonical edges.

The independent attack suite and verification were byte-identical across the
two runs.  The seed is accepted for replay bookkeeping only.

## Commands

Canonical write:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=300311 /usr/bin/time -v \
  python -B \
  deliverables/cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_verifier.py \
  --seed 300311
```

Distinct-seed no-write replay:

```text
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=300929 /usr/bin/time -v \
  python -B \
  deliverables/cm2_round300c_source_g_virtual_stratum_new_occurrence_positive_volume_edge_promotion_verifier.py \
  --seed 300929 --no-write
```

Observed resource use:

```text
seed 300311: 247.27 s wall, 245.59 s user, 1.63 s system,
             715676 KiB maximum RSS
seed 300929: 239.24 s wall, 237.43 s user, 1.79 s system,
             716104 KiB maximum RSS
```

## Identical outputs

Both runs reported:

```text
94660 retained positive 3D carriers
229663 Round288 rational comparisons
1840 Round292 transformed comparisons
6322 exact positive-volume witnesses
6314 canonical virtual-root/new-occurrence edges
edge multiplicity {1: 6306, 2: 8}
6314 incident and 298426 nonincident new occurrences
46/46 attacks rejected
36/36 semantic attacks fully reclosed
```

Both runs emitted:

```text
attack-suite file SHA-256
6fdddd23cec9eae8e885953e303fd10fa1fa48f45039be822c1d75e3a4240c3e

attack-suite self-closure
e9ee7a407a2155995e1f701f80f2416ad2ef679179bae2e9e76e2947f2e89e6c

verification file SHA-256
692a9d0323d13d2f85a6426f1bf5c4724428221dfe508fa01d1eb6e2826838ff

verification self-closure
7e37df4fa7070fa4af415a4883e3f6d8fedc67688d84b3ec1b0379ecba714b90
```

The no-write run checks the existing independent attack-suite and verification
bytes directly and exits nonzero on any difference.  Candidate ledgers are
also independently regenerated with canonical JSON, deterministic GZIP
(`mtime=0`, empty embedded filename), and compared byte-for-byte.

## Determinism hardening

An exploratory pre-final replay correctly exposed temporary path names in
human-readable attack rejection details.  Those runtime-local details were
removed before the two final runs above.  The final artifacts contain no seed,
temporary directory, generated temporary filename, timestamp, or runtime GZIP
mtime.  Both final runs are byte-identical.

## Result self-closure

The result is canonical JSON with:

```text
result file SHA-256
415705e38662fa12260320ae0daf77e5e154c38ee9a886ea82f03f22894b44ad

result self-closure
7c07180b4879bec521bc9a432bc9c7ed354de6d0f033429544a19bb1310645b2
```

The verifier independently rebuilds this result after reconstructing both
ledgers and before opening the candidate result.

## Nonpromotion replay

Both runs preserve the same fail-closed boundary:

```text
complete virtual/new-occurrence frontier claimed = false
withheld Round248 wall sheets = 38360
withheld inherited 2D sheets = 264
occurrence identity / alias / new-ID credit = 0
component union / DSU rank credit = 0
quotient / maximality / fibre / global disposition credit = 0
post-Round300C component count = null
D02 = BLOCKED
CM2 = NO-GO_FOR_CLAIM
```
