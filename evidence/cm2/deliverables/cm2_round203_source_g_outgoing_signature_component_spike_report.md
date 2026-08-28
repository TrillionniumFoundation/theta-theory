# CM2 Round203 — source-G outgoing-W signature-component propagation spike

Date: 2026-07-26  
Verdict: `PARTIAL`; strict transitive gain is zero

## Question

Can the `32,776` Round198 unsigned outgoing-W candidate regions inherit a
unique local return signature by transitive propagation through compatible
shared-face components, without using a parent-wide guess or a single
point?

The graph contains:

- all `36,040` strict Round195 candidate regions; and
- all `18,332` strict Round174/Round179 resolved anchor boxes.

An edge is allowed only when two nodes:

1. have the same Gate3 parent;
2. have the same outgoing cell;
3. share an exact positive-two-dimensional box-face patch; and
4. have whole-face HPLUS and HMINUS interval enclosures that are both
   strict with that cell's signs.

A component can propagate a local signature only when it contains at least
one real strict anchor and every anchor signature in the component agrees.

## Method and trust boundary

The read-only probe
`cm2_round203_source_g_outgoing_signature_component_probe.py` was run at
SHA256

`86214ed1d37400cdde787c915b4467c7d081e018a7c7522470bdcb5d1abc351f`.

It pins the final Round198 source and report, which recursively pin the
verified Round174, Round179, and Round182 chain and final Round195 probe.
Imports occur before local hash checks, so this remains a feasibility-probe
trust boundary rather than an adversarial verifier.

Candidate cells are rebuilt directly from whole-leaf strict HPLUS/HMINUS
signs. Round198 assignments are not loaded as graph results. The probe
reconstructs the Round195 leaf and U|U hashes, rebuilds all candidate and
anchor nodes, and independently reconstructs the direct candidate-anchor
edge set. The `3,264` Round198 directly anchored candidates are a hard
fail-closed pin.

Edges are generated through deterministic parent/cell/axis/face-coordinate
buckets. Edge/corner contacts and volumetric overlap are rejected. Every
surviving box-face pair is reevaluated on its exact degenerate face box with
the pinned factor evaluator.

Connected components are computed only after all edges are complete.
Multi-source BFS from every anchor in an accepted component records the
minimum compatible-edge hop count for each candidate.

## Final replay

Static checks:

- AST parse: pass;
- synthetic `--bad-option`: rejected with exit `2`;
- output-path option present: no;
- runtime filesystem writes: zero.

Two final cold seeds were run from the same pinned source:

```text
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=203052 \
  ../.venv-neurips/bin/python -B \
  cm2_round203_source_g_outgoing_signature_component_probe.py \
  > /tmp/cm2_round203_seed203052.json

env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=203062 \
  ../.venv-neurips/bin/python -B \
  cm2_round203_source_g_outgoing_signature_component_probe.py \
  > /tmp/cm2_round203_seed203062.json
```

Both exited zero:

| seed | elapsed | maximum RSS |
|---:|---:|---:|
| 203052 | `6:56.26` | `933,764 KiB` |
| 203062 | `6:57.57` | `934,444 KiB` |

The two output JSON files are byte-for-byte identical.

Final hashes:

- probe result:
  `8addc49f7e1c2661fa82525f59765627f7a2cbb322a0b3b55d4ca5c6a04341d9`;
- each output JSON:
  `7c4e34d146adb5f34637bed6eeae19719bdd477c47c235a9e57384f950f63e48`.

## Node ledger

| node kind | count | compact-row SHA256 |
|---|---:|---|
| strict candidate region | 36,040 | `4907c49e33454110fb9d53eb728761608cf773b802ddb606115f89dbbb1acd17` |
| strict resolved anchor | 18,332 | `81c55aa424486784bc1b7b950210b4d4906fe178a8a81a498a95e3907b11b53d` |
| total | 54,372 | — |

Anchor provenance is:

- Round174: `12,140`;
- Round179: `6,192`.

The candidate nodes cover all `18,324` Round195 leaves, `8,268` origins,
and `912` Gate3 parents. Their reconstructed Round195 leaf and U|U row
hashes exactly equal the final Round195 pins.

## Strict edge ledger

The probe examines `50,608` deterministic face buckets. It certifies
`39,200` compatible edges:

| edge kind | count |
|---|---:|
| candidate region ↔ strict anchor | 4,328 |
| strict anchor ↔ strict anchor | 34,872 |
| candidate region ↔ candidate region | 0 |

The shared-face axis census is:

| axis | compatible edges |
|---|---:|
| p | 16,140 |
| s | 7,848 |
| t | 15,212 |

An additional `32,576` positive-two-dimensional box-face contacts fail the
whole-face compatible strict-cell test and are rejected. Thus box adjacency
alone never becomes an edge.

The compatible-edge rows have SHA256

`110be08dd6a95bc0bee306abed35d452c6f17b65897b5c9acd3edaf6bcaadf9e`.

The rejected-face rows have SHA256

`29b5f3dfe8987a08e9a97c6b8f5888513073638392cfd95cc71a2f4eac85b5b0`.

## Component and propagation ledger

The graph has `34,008` connected components:

| component status | count |
|---|---:|
| uniquely anchored | 1,232 |
| unanchored residual | 32,776 |
| conflicting anchors | 0 |

There are `1,820` parent/cell groups. Node, candidate, anchor, and edge
counts are conserved both globally and within every parent/cell group.

The component rows have SHA256

`d9fb8825b8689889c35e3028bc8a275c662230b72a9f96eb7853f4fdeb2daeb7`.

Because there is no compatible candidate-candidate edge:

- each unsigned candidate remains an unanchored singleton component;
- every assigned candidate is directly adjacent to a real anchor;
- minimum-hop census is exactly hop 1: `3,264`;
- maximum minimum hop is `1`; and
- newly assigned at hop 2 or greater: `0`.

The final candidate ledger is therefore unchanged from Round198:

| assignment status | regions |
|---|---:|
| uniquely assigned | 3,264 |
| unanchored residual | 32,776 |
| total | 36,040 |

Assigned regions cover `3,260` leaves, `2,164` origins, `572` parents, and
`24` distinct official Gate5 exact keys. Residual regions cover `18,176`
leaves, `8,264` origins, and `908` parents. These overlapping leaf/origin
counts reflect that different regions of one leaf or origin can have
different component status.

The assignment rows have SHA256

`d0d1fdb87da141b2c7260d266ec86415d958c7f773a1a5ccac224a3125dabc3a`.

No local assignment is interpreted as global exact-key disposition.

## U|U glue

All `88` U|U leaves and `176` side-specific candidate regions are rebuilt.
No U|U candidate lies in an anchored component:

- assigned regions: `0`;
- residual regions: `176`;
- leaves with both regions assigned: `0`;
- leaves with one region assigned: `0`;
- leaves with neither region assigned: `88`.

The U|U assignment rows have SHA256

`4223bcc9a07b15969003cec3fe30ca77679ad1e36f80282aa2007b95ae09259d`.

Round195's cross-t ordering proof remains valid, but no component edge
crosses outgoing cells and no signature is inferred from the ordering
alone.

## Verdict and next gate

`PARTIAL`: the strict transitive-component strategy is internally
consistent and conflict-free, but it adds exactly zero signatures beyond
Round198's direct adjacency result. The obstruction is structural under
the required edge rule: candidate regions have no compatible
candidate-candidate full-face edge.

The next feasibility route must not broaden the component rule or guess
from the parent base. It should instead directly certify every unsigned
strict region:

- target lift;
- ordered integer wall events and signed wall word;
- roof;
- outgoing chart; and
- official Gate5 exact key.

Every field must be constant and canonical on the whole region. U|U sides
must be audited separately. Any region without a full-region proof remains
residual.

Even complete local reconstruction would still leave the separate `64`
wall-G leaves, formal attachment and independent verification, half-open
ownership, and the global fibre-wide occurrence join/deduplication.

The strict global state remains:

- source-G global dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- CM2: `NO-GO_FOR_CLAIM`.
