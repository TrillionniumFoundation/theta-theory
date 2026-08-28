# CM2 Round209 — source-G outgoing-W half-open owner feasibility spike

Date: 2026-07-26

## Verdict

`VALIDATED_READ_ONLY_FEASIBILITY`.

Every one of the `17,716` nonempty Round195/Round208 outgoing-W leaves has
exactly one strict `E/W` owner region and exactly one strict `N/S` shadow
region.  The owner is derived from the whole-box strict sign of the inactive
factor, not from a point sample, adjacency propagation, component propagation,
or a preferred copied signature.

The probe constructs deterministic in-memory owner-lineage rows for all
`17,716` 2D sheets, `20,456` 1D clipping incidences, and `40,912` 0D endpoint
incidences.  It emits only a compact JSON summary to stdout.  This is a
feasibility result, not a formal producer, certificate, or global-component
claim.

## Frozen trust boundary

The probe pins and reads:

| input | SHA256 |
|---|---|
| Round173 transport source | `bdbf794a99dc9276b11b7680818994d63f52fe0e5a857948701f64e8d5d16a0f` |
| Round173 certificate | `5ff82c5822f543109da0d50c0637d0d2f9148a738b1a21b16878c70e5505cf1a` |
| Round173 result | `948ab0a8539b08adc96c9493de415b44a5ffb75a1ee3ef47a4742902c211c11f` |
| Round195 probe source | `f70734937ed2630f4357b9e1d860e862c1a932c573c1f93c45788cd5697ee4e1` |
| Round195 spike report | `2f4318f381b79c28c457ce3e2f54e0b6e843c649738789c6d0f95dc8a6332dac` |
| Round195 probe result | `bc1a983b5acab0b3a41c9c5941a77313a80d4376932b41ea31e3aabeed96511b` |
| Round195 stdout document | `5ddd98453bf313b2cbed862aa5ca05bef76ba542750beaba75259a41415454a0` |
| final Round208 producer | `c9fe0cdfb4631c31702473d705b04fa89fb8d51e4c71c9b2b652dc98e4641913` |
| final Round208 certificate | `4d01fb9cee639ec59786c078f7a20b3bbcd5c18ea674fabbfce64e250e765938` |
| final Round208 result | `d00674fa4061364539ce6f36f6f8de938f50bc54afbf5497266dcfa0e078bca8` |

Round208 was finally re-pinned after its independent cold replay; its producer,
certificate, and result hashes did not change during Round209 development.

The Round208 envelope result hash and all used closed rows are recomputed.
Removing only the Round208 formal wrapper fields reconstructs the exact
Round195 compact geometry hashes:

| Round195 geometry ledger | rows | SHA256 |
|---|---:|---|
| final factor faces | 18,412 | `0efb78285bc7836c84860f157ab4ec45593029aa523a95fd62171d307d7a5396` |
| leaf geometry | 18,324 | `0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5` |
| U\|U cross-t audit | 88 | `12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0` |

Round173, Round195, and Round208 are trust-boundary inputs.  The probe does not
claim to independently reprove them, and it does not import or execute the
Round195 probe or Round208 producer.

## Factor-derived half-open owner

Round173 freezes the rule

```text
E or W owns; N or S excludes.
```

Round195/Round208 use

```text
F = Nx^2 - Ny^2 = HPLUS * HMINUS,
HPLUS  = Nx + Ny,
HMINUS = Nx - Ny.
```

On every nonempty sheet exactly one factor is active and the other factor has
a strict sign on the whole 3D leaf box.  Hence:

```text
HPLUS = 0  =>  HMINUS = 2*Nx,
HMINUS = 0 =>  HPLUS  = 2*Nx.
```

The strict inactive-factor sign is therefore the sheet's strict `Nx` sign.
A positive sign selects owner cell `E`; a negative sign selects owner cell
`W`.  Flipping only the active-factor sign gives the unique `N/S` shadow.
All `17,716` inactive-factor signs came from direct whole-box C0 enclosures.

The census is perfectly balanced:

| owner | shadow | sheets |
|---|---|---:|
| E | N | 4,429 |
| E | S | 4,429 |
| W | N | 4,429 |
| W | S | 4,429 |

Thus:

- owner regions: `E=8,858`, `W=8,858`;
- shadow regions: `N=8,858`, `S=8,858`;
- active factor `HPLUS`: `8,858`;
- active factor `HMINUS`: `8,858`;
- strict `Nx` positive: `8,858`;
- strict `Nx` negative: `8,858`.

The owner is always the strict-positive `F` region; the shadow is always the
strict-negative `F` region.

## Paired return-signature audit

For every sheet, the probe joins its two Round208 strict region rows and
requires:

1. one and only one outgoing cell in `{E,W}`;
2. one and only one outgoing cell in `{N,S}`;
3. the exact factor-sign pair associated with each cell;
4. a common strict inactive factor and common whole-box C0 enclosure;
5. the factor-derived owner/shadow cells described above; and
6. exact equality of the two complete local return signatures after removing
   only `outgoing_cell` and `target_chart`.

All `17,716/17,716` pairs pass.  Both target-chart fields are also checked to
equal the common target-lift obstacle followed by their respective outgoing
cell.  There are `24` distinct shared signature cores.

No return-signature field other than `outgoing_cell` and `target_chart` is
allowed to differ.

## Dimension-safe lineage materialization

The exact identities are:

```text
17,716 2D sheets
20,456 1D clipping incidences
40,912 0D endpoint incidences = 2 * 20,456
36,040 strict regions = 608 empty leaves + 2 * 17,716 sheet sides.
```

Each compact row contains deterministic IDs, its parent lineage IDs and
hashes, the owner and shadow region IDs/cells, the shared signature-core hash,
and explicit zero-credit/non-component fields.  The full rows remain in
memory; stdout carries their exact aggregate hashes plus the first and last
closed row.

| lineage | rows | rows SHA256 |
|---|---:|---|
| 2D sheet owner lineage | 17,716 | `be4955bf1d705ffd8730505b8407a05a220940d5b76878a9a7059a5df762289a` |
| 1D curve owner lineage | 20,456 | `a3e375fc26afa4df3db6e8fd4b07e4bc4f97d91c9eceb6893e29ffe4ce89422e` |
| 0D endpoint owner lineage | 40,912 | `23eee8138694f9b53436a66740da7801146877a62ee2b8b2fce6e2cfc36e916b` |

Every curve joins exactly one sheet owner lineage.  Every endpoint joins
exactly one curve and one sheet owner lineage.

The clipping-incidence geometry census is:

| boundary-edge pair | incidences |
|---|---:|
| E\|N | 3,959 |
| E\|S | 3,959 |
| N\|S | 4,620 |
| N\|W | 3,959 |
| S\|W | 3,959 |

The two t-face sides are balanced at `10,228` each.  Graph axes are
`p=20,200` and stereographic `u=256`.

These are incidence rows, not connected components and not global
components.  In particular, repeated owner lineage does not merge separate
incidences or create any global credit.

## U|U audit

The `88` U|U sheets cover `76` origins and inherit the same deterministic
owner rule:

| item | count |
|---|---:|
| E owner | 44 |
| W owner | 44 |
| active HPLUS | 44 |
| active HMINUS | 44 |
| each active-factor/owner-cell combination | 22 |

Their dimensional ledger is:

- 2D sheets: `88`;
- 1D clipping incidences: `164`;
- 0D endpoint incidences: `328`.

Of the `88` sheets, `76` carry two t-face curves.  All `76` curve pairs are
strictly ordered and disjoint:

- upper curve strictly greater in `p`: `38`;
- upper curve strictly less in `p`: `38`;
- curve-pair intersections: `0`.

The remaining `12` have one curve and one strictly zero-absent t face, so
there is no second curve that could intersect.

## Reproduction

The finalized probe source SHA256 is

```text
dcd8d6d2354151a0aa1c45db8f1ce78f1385b665741ee5a79521bf261cebc13f
```

It was run with two independent Python hash seeds:

```bash
PYTHONHASHSEED=209061 python -B \
  cm2_round209_source_g_outgoing_half_open_owner_probe.py \
  > /tmp/cm2_round209_seed209061.json

PYTHONHASHSEED=209062 python -B \
  cm2_round209_source_g_outgoing_half_open_owner_probe.py \
  > /tmp/cm2_round209_seed209062.json
```

Both runs exited zero.  Their stdout documents are byte-identical
(`cmp=0`):

```text
stdout SHA256  d561ad855ff22b067f5ac997941a0cc96ba53d368ba6dcaa303c6d6d5672471d
result SHA256  7bb2117148571c23432ab8bbee86107fdadc3198c61628b2f8a46760be91a120
```

Measured replay resources:

| seed | elapsed | maximum RSS |
|---|---:|---:|
| 209061 | `0:47.80` | `572,588 KiB` |
| 209062 | `0:53.48` | `572,544 KiB` |

The probe has no output-path option.  A runtime audit hook rejects write-mode
opens and filesystem mutation events; the result is emitted only to stdout.

## Strict nonpromotion boundary

This spike issues:

```text
formal half-open owner credit       0
whole-leaf credit                   0
whole-origin credit                 0
whole-original-tube credit          0
global-component credit             0
global exact-key disposition credit 0
source-G global dispositions        0/224580
D02                                 BLOCKED
Gate5                               10/18
CM2                                 NO-GO_FOR_CLAIM.
```

The next core step is a fresh formal producer and an independent verifier
that recompute and attach these lower-dimensional owner lineages.  That
formalization must preserve the distinction between sheet/curve/endpoint
incidences and global components.
