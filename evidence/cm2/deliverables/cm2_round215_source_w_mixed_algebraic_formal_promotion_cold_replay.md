# CM2 Round215 cold replay

Date: 2026-07-27

## Frozen artifact identities

The bounded probe is a pinned dependency of the formal producer and
independent verifier.  It is not one of the six official manifest entries.
Its source SHA256 is:

```text
463dfe832b32459b356bdfa0602c5eacea82569734f7ad1016c97ffa9d6c40c1
```

The formal producer source SHA256 is:

```text
ed36ada7a6fe499b16eb62f005e60482589d38126f6141edde25ae64405ff9d0
```

The official certificate contains `398,480` bytes, has file SHA256:

```text
9ad5321f5b29111aabe9f044ee22220c83d8c76ace45383ed34a0255a485a3ec
```

and has result SHA256:

```text
39d38cda12566e25b341b861e0e1ee379138aa465424254a6b60ea35da5629ee
```

The independent verifier source SHA256 is:

```text
47c6759d10a722c9a8e2561d55b66754e91d01b4a3c0a6342b1385563ef6f46a
```

The official verification contains `5,576` bytes, has file SHA256:

```text
9af901607edd4b95f1ec149bb6426a84315de22decbcd331a8d71d727894c519
```

and has result SHA256:

```text
f6fd2b6927d003f216dac1caf24452149283286227475cab423aa8fde77e960d
```

## Environment

All four formal runs used:

```text
Python 3.12.3
python-flint 0.9.0
Arb precision 192 bits
LC_ALL=C
TZ=UTC
```

The interpreter was `/tmp/cm2-flint-venv/bin/python`.  The external hash
seed was varied independently for every producer and verifier replay.

## Producer runs

The two producer runs used the sole allowlisted official certificate path:

```bash
/usr/bin/time -v env PYTHONHASHSEED=215101 LC_ALL=C TZ=UTC \
  /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_round215_source_w_mixed_algebraic_formal_promotion.py

/usr/bin/time -v env PYTHONHASHSEED=215102 LC_ALL=C TZ=UTC \
  /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_round215_source_w_mixed_algebraic_formal_promotion.py
```

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Official, seed `215101` | 704.48 s | 0.56 s | 11:45.18 | 168,956 KiB | 0 |
| Independent seed `215102` | 701.96 s | 0.36 s | 11:42.53 | 168,960 KiB | 0 |

Both stdout files contain only certificate-result SHA256
`39d38cda12566e25b341b861e0e1ee379138aa465424254a6b60ea35da5629ee`.
They are byte-identical, and the official certificate file remained
`9ad5321f5b29111aabe9f044ee22220c83d8c76ace45383ed34a0255a485a3ec`.

## Independent-verifier runs

The two verifier runs likewise used the sole allowlisted official verification
path.  Before the second run, the first verification was copied to a temporary
hidden file solely for post-run byte comparison:

```bash
/usr/bin/time -v env PYTHONHASHSEED=215121 LC_ALL=C TZ=UTC \
  /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_round215_source_w_mixed_algebraic_formal_promotion_verifier.py

/usr/bin/time -v env PYTHONHASHSEED=215122 LC_ALL=C TZ=UTC \
  /tmp/cm2-flint-venv/bin/python \
  deliverables/cm2_round215_source_w_mixed_algebraic_formal_promotion_verifier.py
```

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Official, seed `215121` | 682.61 s | 0.51 s | 11:23.25 | 172,204 KiB | 0 |
| Independent seed `215122` | 677.58 s | 0.37 s | 11:18.06 | 172,696 KiB | 0 |

Both stdout files contain only verification-result SHA256
`f6fd2b6927d003f216dac1caf24452149283286227475cab423aa8fde77e960d`
and are byte-identical.  The hidden seed-`215121` verification and the
seed-`215122` official verification compare byte-for-byte (`cmp = 0`), with
identical file SHA256
`9af901607edd4b95f1ec149bb6426a84315de22decbcd331a8d71d727894c519`.
The temporary hidden comparison file was deleted after this check.

Each run completed the full independent rebuild before reading the Round215
certificate.  The producer and bounded probe were pinned as inert bytes and
were neither imported nor executed.  Each run established full expected
Python-object and canonical-byte equality and rejected:

- `24/24` genuinely re-signed semantic mutations;
- `13/13` strict JSON and encoding attacks;
- `18/18` lexical/path attacks, including a parent symlink;
- `6/6` producer output-path attacks;
- `7/7` actual hostile input objects; and
- `4/4` actual hostile output objects.

## Exact reconstructed census

Both producer seeds and both verifier seeds reconstructed:

```text
596 outcome-blind priority origins
200 Round201-incomplete origins
  2 frozen Round212 source seams
198 active strict-source-interior mixed origins
18,432 active residual cells
 2 complete promoted origins
16 new strict closed 3D cells
54 separately audited compact-q origins
650 mixed-plus-compact outer conservation origins
```

The two promoted keys are
`W:N:06.00.01111000` and `W:S:H.06.00.01111000`.
Each complete original parent is partitioned into 638 excluded closed 3D
leaves, with every owned 2D face, 1D edge, and 0D corner reduced to one of
those leaves.  Internal and outer strata are disjoint.  The legacy ledger
conclusion boolean is not trusted.

No child count, exact volume, compact-q box, 2D sheet, 1D edge, 0D corner, or
source seam contributes integer credit.

## Formal state invariant

Round215 composes with the frozen Round212 ledger as:

```text
74,582 + 2 = 74,584 excluded
 2,250 - 2 =  2,248 conservative live
74,584 + 2,248 = 76,832
```

The remaining priority set is exactly 252 origins: 198 incomplete mixed plus
54 compact-q.

No global claim is promoted:

- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`; and
- CM2: `NO-GO_FOR_CLAIM`.
