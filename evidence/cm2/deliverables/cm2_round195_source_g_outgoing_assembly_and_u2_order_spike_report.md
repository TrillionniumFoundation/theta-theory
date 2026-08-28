# CM2 Round195 — source-G outgoing-W final assembly and U|U ordering spike

Date: 2026-07-26  
Verdict: `VALIDATED` for local outgoing-W geometric assembly

## Question

Do the mutually exclusive final face normal forms from Round186, Round188,
and Round191 eliminate every local geometric residual in all `18,324`
Round182 outgoing-W leaves? In particular, can the `88` U|U leaves be glued
without allowing their two t-face factor curves to intersect or exchange
order?

## Method

The read-only probe
`cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py` was run at
SHA256

`f70734937ed2630f4357b9e1d860e862c1a932c573c1f93c45788cd5697ee4e1`.

It pins the complete verified Round182 package and the final Round186,
Round188, and Round191 sources and spike reports. Imports occur before those
pins can be checked, so this is a probe trust boundary rather than an
adversarial verifier.

For every one of the `18,412` unresolved t-face incidences the probe applies
exactly one final normal form:

1. Round186 direct two-factor strict absence;
2. Round186 one-active-factor strict absence;
3. Round186 full-base active-factor graph;
4. Round188 unique clipped two-endpoint factor curve;
5. Round191 unique stereographic two-endpoint factor curve; or
6. Round191 strict-monotone active-factor absence.

It then combines the final U face with the frozen Round182 status of the
opposite t face, independently recomputes the whole-leaf outgoing equation

`F = HPLUS * HMINUS = NX^2 - NY^2`,

and requires a strict whole-box `partial_t F` agreeing with the pinned
Round182 collar sign. Each leaf is classified as `EMPTY`, `FULL_2D`, or
`CLIPPED_2D_BOUNDARY_1D`, with an exact 3D volume and separate 2D/1D/0D
accounts.

For every U|U leaf, the probe additionally requires:

- the same active factor on both t faces;
- one compatible p-graph atlas;
- strict `partial_t`, `partial_p`, and `partial_s` of that factor on the
  complete 3D leaf box; and
- for a two-curve leaf, a strict p-order from
  `d p_zero / d t = -partial_t(h)/partial_p(h)`.

This proves that the lower and upper t-face curves are disjoint and cannot
exchange order.

The first successful development run used source SHA `f65e74b0...8e6830`.
Its computed census was used only to add fail-closed exact output pins for
face/leaf/U|U volumes, dimensions, and four row hashes. That changed the
source to the final SHA above. The earlier `/tmp` output is not final
evidence. The final seed195052 run below was performed from the pinned final
source.

## Static and runtime checks

- AST parse: pass;
- `py_compile`: pass;
- synthetic `--output` option: rejected with exit `2`;
- output-path option present: no;
- script runtime writes: zero.

Final run:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=195052 \
  /usr/bin/time -v -o /tmp/cm2_round195_seed195052.time \
  ../.venv-neurips/bin/python -B \
  cm2_round195_source_g_outgoing_assembly_and_u2_order_probe.py \
  > /tmp/cm2_round195_seed195052.json \
  2> /tmp/cm2_round195_seed195052.stderr
```

The final run exited zero:

- elapsed: `3:18.61`;
- maximum RSS: `743,912 KiB`;
- probe result SHA256:
  `bc1a983b5acab0b3a41c9c5941a77313a80d4376932b41ea31e3aabeed96511b`;
- output JSON SHA256:
  `5ddd98453bf313b2cbed862aa5ca05bef76ba542750beaba75259a41415454a0`.

## Final face assembly

The exact input was reconstructed:

| item | count |
|---|---:|
| outgoing-W residual leaves | 18,324 |
| distinct origins | 8,268 |
| retained children | 11,960 |
| single-U leaves | 18,236 |
| U\|U leaves | 88 |
| unresolved t-face incidences | 18,412 |

Exact 3D coordinate volume:

`861459/419430400000`.

The mutually exclusive final face census is:

| final method | faces |
|---|---:|
| Round186 both factors strict absent | 4 |
| Round186 one active factor strict absent | 1,172 |
| Round186 one active factor full graph | 1,104 |
| Round188 unique clipped two-endpoint curve | 15,844 |
| Round191 unique stereographic two-endpoint curve | 256 |
| Round191 strict-monotone active factor absent | 32 |

Thus:

- curve faces: `17,204`;
- zero-absent faces: `1,208`;
- local face residuals: `0`.

Both face sides are balanced: lower `9,206`, upper `9,206`. The exact face
coordinate area is `31351/26214400`; the face-incidence 3D volume, counting
both incidences of U|U leaves, is `1726989/838860800000`.

The compact final face rows have SHA256

`0efb78285bc7836c84860f157ab4ec45593029aa523a95fd62171d307d7a5396`.

## Per-leaf dimensional ledger

All `18,324` leaves are locally assembled:

| final leaf class | leaves | exact coordinate volume |
|---|---:|---:|
| clipped 2D sheet with 1D boundary | 17,308 | `824643/419430400000` |
| empty zero set | 608 | `47259/838860800000` |
| full 2D sheet | 408 | `26373/838860800000` |

The three volumes sum exactly to the input volume.

Dimension-safe totals:

| stratum/candidate kind | count |
|---|---:|
| regular 2D graph sheets | 17,716 |
| 1D clipping-curve segments | 20,456 |
| 0D boundary-endpoint incidences | 40,912 |
| strict side-specific signature candidate regions | 36,040 |

The endpoint identity is exact:

`40,912 = 2 * 20,456`.

Candidate regions obey:

`36,040 = 608 empty single regions + 2 * 17,716 sheet sides`.

Their strict F signs are:

- negative: `18,024`;
- positive: `18,016`.

These are candidate regions, not materialized return signatures. The leaf
rows have SHA256

`0370fb57e9d2881a8bc2d0e66351a6c551e147d483558c682f051153924f88b5`.

All `8,268` participating origins have zero local geometric residual. Their
compact rows have SHA256

`57cdf91214dbc632ee39cb657a79e83344d34600376e85e12faec7de8ddaaa80`.

## U|U cross-t audit

The `88` U|U leaves cover `76` origins and exact coordinate volume

`4071/838860800000`.

Every leaf uses one identical active factor on both t faces:

- `HPLUS`: 44;
- `HMINUS`: 44.

All use a compatible p graph atlas and have strict active-factor
`partial_t`, `partial_p`, and `partial_s` on the entire 3D box. The final
cross-t classes are:

| class | leaves |
|---|---:|
| two curves, strictly ordered and disjoint | 76 |
| one curve, other t face strictly zero-absent | 12 |

For the `76` curve pairs:

- upper curve strictly greater in p: `38`;
- upper curve strictly less in p: `38`;
- curve-pair intersections: `0`.

The U|U dimensional ledger is:

- 2D sheets: `88`;
- 1D clipping curves: `164`;
- 0D endpoint incidences: `328`;
- side-specific candidate regions: `176`.

The U|U audit rows have SHA256

`12fbc70f82645ae2ad252b4e88587a7841814a03fda1972a0241cd63c45d6ee0`.

## Verdict and promotion boundary

`VALIDATED`: the Round186/188/191 normal forms completely assemble the
outgoing-W local geometry. All `18,412` unresolved faces, `18,324` leaves,
and `8,268` origins have local residual zero, and all `88` U|U leaves have a
strict cross-t glue/order proof.

This is not yet a source-G global disposition:

- the `36,040` strict candidate regions do not yet carry frozen
  side-specific return signatures;
- half-open shared-boundary ownership has not been materialized;
- the separate `64` wall-G residual leaves remain outside this probe;
- no global exact-key fibre join/deduplication has been performed; and
- no formal attachment, certificate, or independent verifier exists.

The strict global state remains:

- source-G global dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- CM2: `NO-GO_FOR_CLAIM`.

The next feasibility question is whether each of the `36,040` strict
candidate regions can inherit one unique frozen local return signature from
same-parent Round174/Round179 resolved occurrence anchors without using a
single-point guess. Only after that local materialization may a formal
producer attempt the still-separate wall-G tail and complete global
exact-key-fibre join.
