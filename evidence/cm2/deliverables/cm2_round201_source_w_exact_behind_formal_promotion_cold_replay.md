# CM2 Round201 cold replay

Date: 2026-07-26

## Frozen artifact identities

The formal Round201 producer source SHA256 is:

```text
f7e53607d9a2c6b2f4fda76c9a6a92845f12cced04e28168f227cb516a1f4010
```

The official certificate contains `1,115,443,418` bytes, has file SHA256:

```text
72b9f2959f362a7918bf628989faf2f0f5ed295fc3e28a305b727ff4ed216536
```

and has result SHA256:

```text
9d3dc29c07f81ba2b71743e983c3d4718e40a430d3566cc934d4a3098facad3c
```

The independent verifier source SHA256 is:

```text
29344dd3c0590ac9d0d3f0618a3f0f034316759468e15af2674813ab72f7ce2b
```

The official verification has file SHA256:

```text
6361e38dd01892f8df164a0d8b58a5b7fe1741a9d61cb0727618a76e63759c1a
```

and result SHA256:

```text
7b4e95f87a75fa3a02b925f202b156947c27b08c77a3c1e704a6b7625a2c8f8d
```

The frozen Round184 manifest retained SHA256:

```text
3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1
```

and all six Round184 manifest entries passed `sha256sum -c` after the
Round201 runs.

## Producer runs

The official producer run used `PYTHONHASHSEED=201052`:

```bash
PYTHONHASHSEED=201052 /usr/bin/time -v \
  .venv-neurips/bin/python \
  deliverables/cm2_round201_source_w_exact_behind_formal_promotion.py
```

The independent-seed producer replay used `PYTHONHASHSEED=201072` and the
producer's authorized hidden output name:

```bash
PYTHONHASHSEED=201072 /usr/bin/time -v \
  .venv-neurips/bin/python \
  deliverables/cm2_round201_source_w_exact_behind_formal_promotion.py \
  --output deliverables/.cm2_round201_seed201072_certificate.json
```

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Official, seed `201052` | 1,275.53 s | 8.78 s | 21:36.26 | 5,847,932 KiB | 0 |
| Replay, seed `201072` | 1,301.38 s | 9.29 s | 39:49.92 | 5,844,888 KiB | 0 |

Both stdout files contained only the same result SHA256.  `cmp` returned zero
for the official and hidden certificates, and each file had SHA256
`72b9f2959f362a7918bf628989faf2f0f5ed295fc3e28a305b727ff4ed216536`.
They were byte-identical.

## Independent-verifier runs

The first verifier replay used `PYTHONHASHSEED=201061` and a distinct
authorized hidden verification output:

```bash
PYTHONHASHSEED=201061 /usr/bin/time -v \
  .venv-neurips/bin/python \
  deliverables/cm2_round201_source_w_exact_behind_formal_promotion_verifier.py \
  --output deliverables/.cm2_round201_seed201061_verification.json
```

The official verifier run used `PYTHONHASHSEED=201062`:

```bash
PYTHONHASHSEED=201062 /usr/bin/time -v \
  .venv-neurips/bin/python \
  deliverables/cm2_round201_source_w_exact_behind_formal_promotion_verifier.py
```

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Hidden replay, seed `201061` | 1,723.44 s | 25.09 s | 38:37.27 | 7,527,056 KiB | 0 |
| Official, seed `201062` | 1,567.29 s | 25.02 s | 26:32.49 | 7,528,960 KiB | 0 |

Both stdout files contained only result SHA256
`7b4e95f87a75fa3a02b925f202b156947c27b08c77a3c1e704a6b7625a2c8f8d`.
`cmp` returned zero for the hidden and official verification files, and both
had SHA256
`6361e38dd01892f8df164a0d8b58a5b7fe1741a9d61cb0727618a76e63759c1a`.
They were byte-identical.

Each verifier run reconstructed the complete expected result before reading
the certificate, treated the producer only as pinned inert regular-file
bytes, and did not import or execute it.  Each run rejected:

- `13/13` fully re-signed semantic mutations;
- `13/13` strict JSON and encoding attacks; and
- `17/17` path, parent-alias, file-type, protected-output, and output-name
  attacks.

Thus all `43/43` attacks were rejected on both seeds.  The semantic mutations
included whole-credit, credited-row, inherited-terminal, cell-disposition,
source-seam-credit, residual-partition, official-ledger, child-credit, D02,
D03, Gate5, global-block, and CM2 changes.

## Static and dimension-safe audit

Both Python sources compiled successfully.  A Python AST scan found zero
duplicate constant keys in dictionary literals in both the producer and the
verifier.  The verifier's frozen AST audit found no producer/diagnostic
import, no producer execution, and no reuse of the producer's `build_result`
or `main` body.  It explicitly discloses 13 lower-level exact AST-body
overlaps rather than claiming a fully implementation-diverse derivation.

The accepted ledger requires complete closed 3D terminal coverage.  Strict
closed-box enclosures propagate to owned boundaries; every binary split has
an explicit 2D owner face, deduplicated 1D edges, and deduplicated 0D corners.
Clipped-discriminant terminals separately account for their 3D open sides,
2D graph, 1D graph/face intersections, and 0D graph edge/corner
intersections.  Only whole strict physical-chart-interior origins receive
integer credit.

The two credited cohorts contain 156 and 390 origins, have empty
intersection, and contribute 546 whole-origin credits.  Six pure target-first
source seams, six generalized complete source seams, twelve other inherited
pure source seams, 54 compact-q origins, and 200 incomplete mixed origins all
remain at zero integer credit.  The 278 remaining origins are an exact
disjoint partition.

## Formal state invariant

The frozen Round184 source-W ledger and the Round201 promotion give:

```text
74,012 + 546 = 74,558 excluded
2,820 - 546 = 2,274 conservative live
74,558 + 2,274 = 76,832
```

No child count, refined volume, analytic stratum, source seam, compact-q
origin, or incomplete mixed origin is counted as an integer record.  Round201
does not promote any global claim:

- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`; and
- CM2: `NO-GO_FOR_CLAIM`.

The hidden producer and verifier replay files were retained only through
byte comparison, hash capture, formal documentation, and manifest validation,
then removed.
