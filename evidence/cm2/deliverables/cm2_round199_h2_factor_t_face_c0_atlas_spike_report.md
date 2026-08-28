# CM2 Round199 — H2 factor endpoint-face C0-atlas spike

Date: 2026-07-26  
Verdict: `VALIDATED` (read-only feasibility only)

## Question

Can the 592 Round185 `H2_FACTOR_EXISTENCE_RESIDUAL` boxes be decided without
mistaking a strict derivative for existence?

Yes.  Every box has a complete absence proof for its one active signed
factor:

1. the active factor has one strict `dt` sign on the entire 3D box;
2. both complete `t`-endpoint faces have strict centered-C0 atlases;
3. every cell in each endpoint atlas has one common strict sign;
4. the two endpoint-face signs are identical.

Strict monotonicity in `t` plus two same-sign endpoint faces excludes an
interior zero.  The strict derivative is never used by itself.

This spike issues no formal local-key, whole-parent, stratum, or global
credit.

## Frozen input

The probe pins the exact six-entry Round185 formal delivery before importing
its independent evaluator:

- manifest SHA256:
  `ec018e261e866b48039d1cf775e972c6a9b1a9558a1ecf043665c6340ad3dc26`;
- certificate file SHA256:
  `2034e939a6046cd36f749546ab8dc2c0a004b3325c803b5335a3f5e34831fff1`;
- certificate result SHA256:
  `ae5af298b9d19b99863af600dca7f73fad4ff76f9db661ccfdf9b0e03afbeddf`;
- verifier SHA256:
  `88d5b72c68ba216a1c807b868156c8e0da7e9e63db968eda5b5a66dd86d5651f`;
- verification file SHA256:
  `bda1286ec582f17724b6478e3af98973280f482bf9192235f96842c55513642e`;
- verification result SHA256:
  `b63c15eabc468192c113d7221c7adfd37fec94aa38f4b02c97acb25598962cf6`.

The Round185 verification is `PASS`, requires full expected-result canonical
equality, and rejects `32/32` re-signed semantic, `9/9` strict-JSON, and
`11/11` path attacks.

The spike rechecks the full Round185 dynamic-residual rows digest

`707577c77ef26050b331c3be4e657431dcfade82a4caec51d3a65a26e37d0f73`

and reconstructs both official factor records for every selected box.  Each
official row digest, surface summary, and surface-evidence digest must agree.

## Exact input census

- boxes: `592`;
- parents: `4`;
- exact coordinate volume:
  `2301/2684354560000`;
- active `HMINUS`, fixed-negative `HPLUS`: `296`;
- active `HPLUS`, fixed-negative `HMINUS`: `296`;
- double-active boxes: `0`;
- active strict axes: exactly `dt,dp` on all `592`.

Parent counts and exact volumes are:

| Round185 parent | boxes | exact volume |
|---|---:|---:|
| `W:E:00.14.01101` | 264 | `8673/26843545600000` |
| `W:E:02.11.110` | 32 | `177/1677721600000` |
| `W:E:05.04.001` | 32 | `177/1677721600000` |
| `W:E:07.01.10010` | 264 | `8673/26843545600000` |

## Complete endpoint-face C0 atlases

There are `1,184` endpoint faces.  The probe first applies the centered
mean-value C0 enclosure to the whole face.  If that enclosure overlaps zero,
it bisects only the exact rational `p` interval, to maximum relative depth
two.  Every terminal cell is checked independently.

| endpoint-face method | faces | terminal cells per face |
|---|---:|---:|
| direct whole-face centered C0 | 928 | 1 |
| exact `p` atlas, depth 1 | 128 | 2 |
| exact `p` atlas, depth 2 | 128 | 3 |
| total | 1,184 | 1,568 cells |

The depth-two atlas has three terminal cells because one depth-one sibling is
already strict and only the unresolved sibling is bisected again.

For every endpoint face:

- all terminal centered-C0 enclosures are strict;
- all terminal signs are identical;
- terminal exact areas sum to the complete face area;
- no uncovered face fragment remains.

## Same-sign/strict-`dt` proof

The exact cross-census is:

| active factor | full-box `dt` | `t-` sign | `t+` sign | boxes |
|---|---|---|---|---:|
| `HMINUS` | positive | negative | negative | 136 |
| `HMINUS` | positive | positive | positive | 160 |
| `HPLUS` | negative | negative | negative | 136 |
| `HPLUS` | negative | positive | positive | 160 |

The 128 refined `HMINUS` cases occur only on `t-`; the 128 refined `HPLUS`
cases occur only on `t+`.  In both families, 64 faces close at depth one and
64 at depth two.  The opposite endpoint face is already strict as one whole
face.

All explicit counterexample gates are zero:

- non-strict full-box `dt`: `0`;
- incomplete endpoint-face C0 atlas: `0`;
- mixed or unresolved terminal-cell signs: `0`;
- opposite endpoint-face signs: `0`;
- `dt`/endpoint-direction contradiction: `0`.

Therefore the active factor is zero-absent on every box.  Combining its sign
with the other factor's strict negative sign gives the diagnostic potential
local outgoing-chart census:

- `W`: `272`;
- `N`: `160`;
- `S`: `160`.

These are feasibility classifications, not installed local keys.

## Result and conservation

| class | boxes | exact volume |
|---|---:|---:|
| `ACTIVE_FACTOR_ZERO_ABSENT` | 592 | `2301/2684354560000` |
| `FULL_2D_GRAPH` | 0 | `0` |
| `T_FACE_C0_ATLAS_RESIDUAL` | 0 | `0` |

Count delta and exact-volume delta are both zero.  Because this is a spike,
the official residual volume retained until formal verification remains
`2301/2684354560000`.

The compact per-box ledger has 592 unique rows:

- per-box evidence-hash rows SHA256:
  `3c7b054f27dffa07feaaa5a29d28e958214171fbf55546a3483440ae8a00d469`;
- all 592 terminal paths are unique;
- all 592 compact evidence-row hashes are unique.

Each hash covers the fresh full-box C0/C1 records, both complete endpoint-face
atlases, same-sign/direction gates, classification, and zero-credit fields.
The full interval rows are deliberately not emitted inline by this spike.

## Frozen probe run

Probe:
`cm2_round199_h2_factor_t_face_c0_atlas_probe.py`

Probe SHA256:

`a3a6fe64a3f0d22bc7837af38912deff05306ae8bdb7dde2af9e1202ab0b1e3c`

Command:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=199052 \
  /usr/bin/time -v \
  -o /tmp/cm2_round199_seed199052.time \
  .venv-neurips/bin/python \
  deliverables/cm2_round199_h2_factor_t_face_c0_atlas_probe.py \
  > /tmp/cm2_round199_seed199052.json \
  2> /tmp/cm2_round199_seed199052.stderr
```

Run facts:

- exit: `0`;
- elapsed: `0:29.19`;
- user CPU: `28.38 s`;
- maximum RSS: `603,068 KiB`;
- JSON bytes: `1,240,458`;
- JSON file SHA256:
  `d7eecb115678592b7b66c270a19f35d766abfacc6dbb23a1bad11dd1086a18dd`;
- `probe_result` SHA256:
  `d31621fdaf9f08a48ebc5be9fcbc37a1888d44d7409ee25850b5f31e27abed28`.

The source passes `py_compile`, contains no duplicate literal dictionary
keys, has no output-path option, and has no runtime filesystem-write call.
The shell and `/usr/bin/time` own the `/tmp` captures.

## Trust boundary and next formal gate

The probe pins Round185 before importing its evaluator, but it still reuses
that evaluator's low-level AD geometry.  It is not an implementation-diverse
formal verifier.  The JSON emits compact hashes rather than the complete
interval attachment, and it has no semantic/JSON/path attack matrix of its
own.

A formal successor should:

1. emit every full-box and endpoint-face terminal interval row;
2. install the 592 absence results only as local exact-key rows;
3. use a separately implemented verifier that treats the producer as inert
   bytes and rebuilds the complete C0 atlases;
4. test mutations of `dt`, face signs, p-refinement coverage, exact area,
   factor identity, chart inference, and every credit field; and
5. retain whole-parent/global nonpromotion until all other dimensions under
   the same exact keys close.

Round199 therefore leaves the official global state unchanged:

- `D02 = BLOCKED`;
- Gate5 = `10/18`;
- `CM2 = NO-GO_FOR_CLAIM`;
- formal local credit = `0`;
- whole-parent/global credit = `0`.
