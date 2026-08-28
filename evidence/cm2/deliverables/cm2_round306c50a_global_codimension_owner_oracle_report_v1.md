# CM2 Round306 C50a global codimension owner oracle v1

Status: **PASS generic full-universe owner capability and pair-1 two-task
owner replay; independently verified; strict zero formal/D02 credit**.

## Delivered capability

`cm2_round306c50a_global_codimension_owner_oracle_v1.py` is a request-driven
producer for arbitrary finite, hash-chained replacement histories.  It binds
four frozen protocol versions independently: occurrence identity, two-sided
binary split decisions, overlay history, and codimension ownership.  Each
transaction replaces exactly one representative/reflected predecessor pair,
requires exact prefix-free Kraft-one leaves on both sides, checks every
logical-to-physical split-child map and exact rectangular conservation, and
then recomputes face/corner owners against the current full overlay.

The frozen base input is the complete C41 `91,879`-row active universe plus
the C32 `76,832`-cell chart registry.  It expands to `183,758` physical-side
occurrences: `183,700` exact rational occurrences and `58` algebraic/unknown
occurrences.  Unknown rows are never silently dropped: every queried face and
corner must be provably disjoint from its conservative C32 cell envelope, or
the oracle rejects.

Nested endpoint refinement is supported through `ACTIVE_OCCURRENCE_ID`
predecessors and `ALL_ACTIVE_HISTORY_REPLACEMENTS` targeting.  Thus a later
transaction may refine one endpoint child while earlier strict siblings remain
in the globally audited active frontier.  The contract intentionally does not
claim a genuinely infinite or algebraically degenerate limiting ray; such an
input fails closed pending a separate exact endpoint/limit certificate.

## Independent boundary

`cm2_round306c50a_global_codimension_owner_oracle_independent_verifier_v1.py`
does not import or execute the producer or any C48/C41/C32 producer.  It parses
the frozen ledgers directly, reconstructs occurrence/history/split bindings,
uses boundary indexes for faces and a separate point-query implementation for
corner germs, and repeats the full overlay traversal in opposite order.  It
also performs terminal-byte/identity replay and pre/post frozen-file snapshot
comparison.

The generic C48 regression passed with:

- baseline/final overlay: `183,758 -> 183,762`;
- target occurrences: `6`;
- face atoms / corner entities: `20 / 16`;
- all face degree-two incidence, all corner four-quadrant germs, and all
  owners complete and unique;
- full candidate object `8910975eaf491d117234dab71fdfc7d3e6a4deb9bdeed5be90241fb1ddbf015a`;
- independent audit object
  `e535260235b4404c17cc7ed647c25046c0dc346fc349e04d24492f6e05dc7d3d`.

## Pair-1 full owner replay

The adapter consumes frozen C51 probe object
`187344a3c524dce1898151bf64f507c181dde137a3710eb9bc5cd1b895a81f6e`.
Fields not printed explicitly by C51 (ambient row hash, semantic path,
relative fraction, exact split coordinate, and reflected logical/physical
child map) are derived from the pinned C41 row and exact leaf geometry; no
field was guessed.

It produced two history transactions:

- task `daada4d9...`: frontier `0,1`, two logical/four physical leaves;
- task `e37b5274...`: frontier
  `00,01,10,110,1110,11110,11111`, seven logical/fourteen physical leaves.

The final pair-1 result passed with:

- request object
  `db6292e002ec3c0b810f74af192524407afb1cfa3566c4898aa7fa7b2a8e3496`;
- full candidate object
  `da4557c64b4ce9675a3f8bff8a250b7ec7b643c48aecd738c03b7abed01d0b82`;
- full candidate file SHA-256
  `0c3ffd0a9ff26fd128366a6af22aabeb29f72346303988deb4773b5adcd4131e`;
- baseline/final overlay `183,758 -> 183,772`;
- two transactions, nine logical / eighteen physical target leaves;
- `52` face atoms, `36` corner entities, `78` target face-atom occurrences,
  and `72` target corner occurrences;
- face atom sequence root
  `57495aa6ca955fffe92ad6dfe987c8f263c790502237d0bd76bea825e8cef113`;
- corner entity sequence root
  `1855b65360a534f8f9df1a0128a705eea8a9929c56be49c45173323833b9b099`;
- all face atoms degree two, all incident sets complete, all four-quadrant
  corner germs complete, and every codimension owner unique.

The independent pair-1 audit also passed:

- audit object
  `c037b3b15d19b839a254e3122bce7b1f882f6f9e198638c50a08909bf71231d6`;
- audit file SHA-256
  `5068afb70ec8bf7fddc719324aeae4703fbc4e22d07a9b5555e348471c23dd66`;
- identical two-transaction history head
  `543e2289de5a465745f821f510efa62ea2d4985921e2649b7404665ae71c730f`;
- dual traversal equality and frozen-input immutability.

Because the full owner JSON is about 423 KB, the readable result/audit JSON
files are compact cryptographic bindings with replay commands and sequence
roots.  The complete immutable bytes are also delivered as deterministic-gzip
base64 bundles:

- `cm2_round306c50a_pair1_two_task_global_owner_full_candidate_v1.json.gz.b64`
  decodes to full candidate SHA-256 `0c3ffd0a...`;
- `cm2_round306c50a_pair1_two_task_global_owner_full_independent_audit_v1.json.gz.b64`
  decodes to full audit SHA-256 `5068afb7...`.

The manifest binds both encoded and compressed bytes.  A consumer can decode
the full rows without executing a producer.

## Replay

```bash
base64 -d \
  deliverables/cm2_round306c50a_pair1_two_task_global_owner_full_candidate_v1.json.gz.b64 \
  | gzip -dc > pair1_full_owner_candidate.json

base64 -d \
  deliverables/cm2_round306c50a_pair1_two_task_global_owner_full_independent_audit_v1.json.gz.b64 \
  | gzip -dc > pair1_full_owner_audit.json

.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c51_d02a_pair1_two_task_route_probe_v1.py \
  --probe --event-budget 16 > pair1_probe.json

.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c50a_pair1_probe_to_owner_request_adapter_v1.py \
  --probe-result pair1_probe.json > pair1_request.json

.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c50a_global_codimension_owner_oracle_v1.py \
  --request pair1_request.json > pair1_full_owner_candidate.json

.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c50a_global_codimension_owner_oracle_independent_verifier_v1.py \
  --candidate pair1_full_owner_candidate.json
```

## Strict boundary

These artifacts install no authority, pointer, receipt, canonical status, or
seal.  They do not independently verify C51 numerical route/margin evidence
and cannot alone authorize a pair-level successor.  D02-A, D02-B, and D02-C
remain incomplete; formal/D02 credit is exactly zero and CM2 remains
`NO-GO_FOR_CLAIM`.
