# CM2 Round198 — source-G outgoing-W return-signature adjacency spike

Date: 2026-07-26  
Verdict: `PARTIAL`

## Question

Can all `36,040` strict candidate regions assembled by Round195 receive one
unique frozen local return signature from strict resolved occurrences in the
same Gate3 parent, without using a single point or extrapolating into an
unanchored outgoing cell?

The requested signature consists of:

- target lift;
- ordered integer wall events and signed wall word;
- outgoing cell and target chart;
- roof; and
- frozen Gate5 exact-key row, ordinal, and identifier.

## Method and trust boundary

The read-only probe
`cm2_round198_source_g_outgoing_return_signature_probe.py` was run at
SHA256

`59dac5b6e2d79e1612dad51780174f97f71dc1223c01a21b502805d6e9510fbf`.

It pins:

- the complete verified Round174 package manifest;
- the complete verified Round179 package manifest;
- the verified Round182 package manifest; and
- the final Round195 probe and report.

Because the local Python modules are imported before their hashes can be
checked, this is a feasibility-probe trust boundary, not an adversarial
verifier.

The only signature anchors are the strict positive-volume resolved
occurrence rows:

- Round174 `resolved_3d_occurrence_rows`; and
- Round179 `resolved_3d_child_rows`.

Round179 `outgoing_normal_form_rows` supplies the occurrence-to-parent
binding and certified whole-tube outgoing derivative sign. The probe never
uses `dynamic_signature`, a sampled point, or an inferred key.

For each relevant parent, all anchor fields other than outgoing cell and
target chart must collapse to one base signature. The Gate5 registry is
then independently rebuilt from the frozen Round174 verifier inputs, and
each parent key is recomputed from

`[source_chart, target_lift, signed_wall_word, roof]`.

For every candidate region, the outgoing cell is reconstructed from
whole-leaf interval signs:

`F = HPLUS * HMINUS = NX^2 - NY^2`.

The sign-pair map is exact:

| HPLUS | HMINUS | outgoing cell |
|---|---|---|
| positive | positive | E |
| negative | negative | W |
| positive | negative | N |
| negative | positive | S |

A signature is assigned only if a strict same-parent, same-cell anchor box:

1. shares exactly one positive-two-dimensional box-face patch with the
   candidate leaf box; and
2. pinned whole-face interval enclosures certify both HPLUS and HMINUS
   strictly with the candidate cell signs on that entire patch.

This is stronger than mere closure contact: edge/corner contact,
equality-only contact, a box face with no certified compatible cell patch,
and a same-parent base with no same-cell anchor all remain residual.

## Reproducibility

The development census was first obtained without output pins. It was used
only to add fail-closed pins for the status census, candidate-region rows,
U|U rows, parent-join rows, probe result, and output JSON. Development
outputs are not final evidence.

The final run used:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=198052 \
  /usr/bin/time -v -o /tmp/cm2_round198_seed198052.time \
  ../.venv-neurips/bin/python -B \
  cm2_round198_source_g_outgoing_return_signature_probe.py \
  > /tmp/cm2_round198_seed198052.json \
  2> /tmp/cm2_round198_seed198052.stderr
```

Static checks:

- AST parse: pass;
- synthetic `--bad-option`: rejected with exit `2`;
- output-path option present: no;
- runtime filesystem writes: zero.

The pinned final replay exited zero:

- elapsed: `4:42.17`;
- maximum RSS: `932,744 KiB`;
- byte-for-byte identical to the final development census replay.

Final pinned digests:

- probe result:
  `b6f1660dfe18613ac2b3443c68f56a05f9399d3715c4e7f301fdc0482be459d5`;
- output JSON:
  `5d3ddddd6445bc364f7b4febd5f81adcb311d085bce636f9ec74c7a54d3711ee`.

## Anchor ledger

The relevant outgoing-W scope has:

| item | count |
|---|---:|
| Gate3 parents | 912 |
| Round174 strict anchors | 12,140 |
| Round179 strict child anchors | 6,192 |
| strict anchors total | 18,332 |
| Round179 carried outgoing forms | 8,268 |

All `912` parents have exactly one base signature and no base conflict or
missing base.

Anchor outgoing-cell coverage by parent is:

- one observed cell: `592` parents;
- two observed adjacent cells: `320` parents.

The exact one-cell sets are E `132`, N `164`, S `164`, and W `132`.
The exact two-cell sets are E|N `80`, E|S `80`, N|W `80`, and S|W `80`.
No opposite-cell pair occurs.

The compact parent-anchor rows have SHA256

`9e28c2aa6435ae945f5569fa57163caa36b0fd0823e1ca8a318aa24116fa1993`.

The independently rebuilt scope contains `24` distinct Gate5 exact keys.
Outgoing cell is not part of a Gate5 key row.

## Candidate-region audit

The complete Round195 scope is reconstructed:

| leaf class | candidate regions |
|---|---:|
| clipped 2D boundary 1D | 34,616 |
| full 2D | 816 |
| empty | 608 |
| total | 36,040 |

Strict F signs are negative `18,024` and positive `18,016`. The derived
outgoing-cell census is E `9,008`, N `9,012`, S `9,012`, and W `9,008`.

The fail-closed signature result is:

| status | regions |
|---|---:|
| compatible strict shared-face anchor; unique local signature | 3,264 |
| same-cell anchor exists, but no positive-2D face adjacency | 26,388 |
| no same-cell strict resolved anchor | 6,388 |
| box-face adjacency exists but compatible strict sign patch fails | 0 |
| parent-base conflict or carried-form missing | 0 |
| total | 36,040 |

Thus `32,776` regions remain unsigned. They cover:

- `18,176` leaves;
- `8,264` origins; and
- `908` parents.

The residual class ledger is:

| leaf class | unsigned regions |
|---|---:|
| clipped 2D boundary 1D | 31,504 |
| full 2D | 808 |
| empty | 464 |

Residual outgoing cells are E `8,216`, N `8,172`, S `8,172`, and W
`8,216`.

The `3,264` assigned regions have `4,328` compatible anchor incidences
because some regions touch more than one strict anchor. Their exact
provenance is:

| compatible anchor incidence | count |
|---|---:|
| shared p face | 2,888 |
| shared s face | 16 |
| shared t face | 1,424 |
| Round174 anchor | 2,216 |
| Round179 anchor | 2,112 |

Every positive-2D box-face adjacency found had a full strict compatible
factor-cell patch; none was promoted from box adjacency alone.

The candidate-region rows have SHA256

`e2d8acbfaa3c8377106ea42a72bdd43d11025d43417f7513fe48e6d07677c259`.

The `3,264` assignments collapse to `40` distinct local signatures across
the `24` involved exact keys. This does not dispose any exact-key fibre.

## U|U glue

The Round195 ordering proof is rebuilt for all `88` U|U leaves and their
`176` candidate regions. Signature anchoring remains incomplete:

| U|U region status | count |
|---|---:|
| no same-cell strict anchor | 4 |
| same-cell anchor but no positive-2D face adjacency | 172 |
| assigned | 0 |

The U|U signature-region rows have SHA256

`9743e4b22ac4f9a89aa7590d79af56c7e5721a28a0a558c173626050a3bfd65c`.

Therefore Round195's strict cross-t curve order is preserved, but it does
not by itself transport a return signature across the U|U glue.

## Verdict and next gate

`PARTIAL`: the strict direct-adjacency rule reconstructs `3,264/36,040`
local side-specific signatures. It deliberately refuses to fill the
remaining `32,776` regions from a parent-wide base or from a factor-derived
cell alone.

The immediate feasible next question is a component propagation audit:
within each parent and outgoing cell, connect candidate regions and strict
anchor boxes only across positive-two-dimensional shared patches whose
entire HPLUS/HMINUS enclosure is strictly compatible. A component may
inherit a signature only if it contains a real strict anchor and has no
signature conflict. Unanchored or conflicting components must remain
residual.

Even complete local outgoing-W component anchoring would still leave:

- the separate `64` wall-G residual leaves;
- formal side-specific signature attachment and independent verification;
- half-open boundary ownership;
- global source-G occurrence join/deduplication by official exact key; and
- proof that every full exact-key fibre is covered or excluded.

The strict global state remains:

- source-G global dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- CM2: `NO-GO_FOR_CLAIM`.
