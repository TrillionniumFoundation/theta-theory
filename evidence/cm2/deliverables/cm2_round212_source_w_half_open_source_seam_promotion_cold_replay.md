# CM2 Round212 cold replay

Date: 2026-07-27

## Frozen artifact identities

The formal producer source SHA256 is:

```text
dae73423b0db54987a23121197764feb3fee4c32763cf7a4b9e2275b7d5a6485
```

The official certificate contains `103,913` bytes, has file SHA256:

```text
70ad8ce31edba0d0a8b082d72ba5f191224193c683ee49181213119f762a18e9
```

and has result SHA256:

```text
a4e6e44aa55eedd376f5dd5d01a82f5c8dfae19ebb433dfb0017d07718004c7d
```

The independent verifier source SHA256 is:

```text
c214c2bacc079d68440ba6eaaf338eb6ed3a725933d3942a3a42734e28c9e1be
```

The official verification contains `3,689` bytes, has file SHA256:

```text
09b8a3282539740187776cb41e957212b2d61fafaa33d6984544564ddaa17aea
```

and has result SHA256:

```text
5ab0bb7fa213fa0e86c1252dad1a21b96ab54d4b48025e767c8af7a953383d2e
```

## Producer runs

The two producer runs used distinct external hash seeds and the sole
allowlisted official output path:

```bash
PYTHONHASHSEED=212052 /usr/bin/time -v \
  .venv-neurips/bin/python \
  deliverables/cm2_round212_source_w_half_open_source_seam_promotion.py

PYTHONHASHSEED=212053 /usr/bin/time -v \
  .venv-neurips/bin/python \
  deliverables/cm2_round212_source_w_half_open_source_seam_promotion.py
```

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Official, seed `212052` | 233.65 s | 0.55 s | 3:54.25 | 123,012 KiB | 0 |
| Independent-seed replay, seed `212053` | 251.99 s | 0.62 s | 4:13.04 | 122,536 KiB | 0 |

Both stdout files contain only result SHA256
`a4e6e44aa55eedd376f5dd5d01a82f5c8dfae19ebb433dfb0017d07718004c7d`
and are byte-identical.  The official certificate SHA256 was recorded before
and after the second run and remained
`70ad8ce31edba0d0a8b082d72ba5f191224193c683ee49181213119f762a18e9`.
Thus the two external hash seeds produced the same canonical bytes.

## Independent-verifier runs

The two verifier runs likewise used distinct external hash seeds and the sole
allowlisted official verification path:

```bash
PYTHONHASHSEED=212062 /usr/bin/time -v \
  .venv-neurips/bin/python \
  deliverables/cm2_round212_source_w_half_open_source_seam_promotion_verifier.py

PYTHONHASHSEED=212063 /usr/bin/time -v \
  .venv-neurips/bin/python \
  deliverables/cm2_round212_source_w_half_open_source_seam_promotion_verifier.py
```

| Run | User | System | Wall | Peak RSS | Exit |
|---|---:|---:|---:|---:|---:|
| Official, seed `212062` | 217.02 s | 0.54 s | 3:37.60 | 126,832 KiB | 0 |
| Independent-seed replay, seed `212063` | 223.32 s | 0.53 s | 3:43.89 | 125,280 KiB | 0 |

Both stdout files contain only verification result SHA256
`5ab0bb7fa213fa0e86c1252dad1a21b96ab54d4b48025e767c8af7a953383d2e`
and are byte-identical.  The verification SHA256 remained
`09b8a3282539740187776cb41e957212b2d61fafaa33d6984544564ddaa17aea`
across the two runs.

Each run reconstructed all 26 source-seam facts before reading the
certificate, treated the producer as pinned inert bytes, and did not import
or execute it.  Each run rejected:

- `14/14` genuinely re-signed semantic mutations;
- `8/8` strict JSON and encoding attacks; and
- `10/10` path, file-type, parent-alias, and protected-output attacks.

## Dimension-safe census

The exact source-seam cohort has 26 whole origins.  Twenty-four complete
origins are promoted; the two keys
`W:N:07.00.11111011` and `W:S:H.07.00.11111011` retain 72 unresolved final
cells each and receive zero credit.  The replay accounts for 3,666 final
cells, 1,630 inherited terminals, and 6,832 target proof objects.

The 24 promoted source parents have the following exact half-open partition:

- chart census `E/N/S = 6/9/9`;
- source-sign census `NEGATIVE/POSITIVE = 15/9`;
- seam owners `E/W = 12/12`; and
- adjacent guard charts `W/E/N/S = 12/6/3/3`.

Only a complete original chart-owned physical source parent receives an
integer credit.  No child cell, volume, diagonal sheet, guard slice, 1D edge,
or 0D corner is promoted independently.

## Formal state invariant

Round212 composes with the frozen Round201 ledger as:

```text
74,558 + 24 = 74,582 excluded
 2,274 - 24 =  2,250 conservative live
74,582 + 2,250 = 76,832
```

The remaining priority set is exactly 254 origins: 200 incomplete mixed plus
54 compact-q.  The two retained source-seam origins are members of the 200,
not an additional residual class.

No global claim is promoted:

- D02: `BLOCKED`;
- D03 negative oracle: `UNAUTHORIZED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`; and
- CM2: `NO-GO_FOR_CLAIM`.
