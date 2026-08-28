# CM2 Round288 — canonical-atom occurrence-identity gate audit

## Verdict

Round288 is a **zero-credit, fail-closed audit** of the complete Round279
canonical-atom universe.  It reconstructs all `332,020` source signature rows
and all `332,016` canonical atoms from pinned frozen inputs, then compares them
with all `126,468` frozen Round266 expanded occurrences.

The audit corrects one material identity-accounting error:

- `36,040` atoms are exact aliases of existing Round208 occurrences;
- a further `640` atoms are exact aliases of existing Round204 occurrences;
- therefore the conditionally distinct new-atom count is `295,336`, not
  `295,976`;
- the conditional all-pass occurrence total is `421,804`, not `422,444`.

No occurrence, component, maximality, fibre, disposition, seam, or `Jx/Jy`
credit is issued by this round.

## Complete identity partition

The `332,016` atoms are partitioned without orphan or duplication as follows:

| Disposition | Count |
|---|---:|
| Existing Round208 occurrence ID preserved | 36,040 |
| Exact alias of an existing Round204 occurrence | 640 |
| New disjoint candidate with a pinned Round279 strict inward corridor | 274,176 |
| New disjoint candidate still lacking a materialized inner box | 21,160 |
| **Total** | **332,016** |

The `36,680` existing-overlap relations are all exact-equality relations:
`36,040` to Round208 and `640` to Round204.  There are no positive-volume
partial-overlap or containment relations with Round174/Round179/Round204/
Round208 occurrence geometry.

Across all same-chart, same-complete-signature atom groups, an exact rational
interval sweep performs `19,359,760` shortlist comparisons and finds **zero**
positive-volume overlap pairs between distinct canonical atoms.  Equality of
an exact key or signature is never treated as physical identity.

## Strict inner-support audit

Round279's independently verified common-face ledger contains `661,448`
positive-volume rational inward corridors incident to `310,808` canonical
atoms.  Round288 rebinds every corridor to its exact:

- Round182 leaf;
- canonical atom;
- source chart;
- owner target;
- complete ten-field signature;
- frozen support envelope; and
- geometric face side.

The standalone cacheless Round288 verifier has now independently passed.  It
structurally rebound all `330,724` frozen face edges and freshly dynamically
verified all `661,448` positive-volume rational inward corridors.  This
confirms `274,176` genuinely new atoms as promotion-ready candidates.  Their
frozen producer-time disposition string retains
`PENDING_INDEPENDENT_ROUND288_VERIFIER`, but the later independent
verification is PASS; no occurrence ID or credit is issued by that PASS.  The
other `36,632` incident atoms are the already-existing Round208/Round204
identities above.

The remaining `21,160` new candidates are face-isolated and remain
fail-closed:

| Source | Residual |
|---|---:|
| Round269 connected factor sides | 3,968 |
| Round270 connected factor sides | 6,728 |
| Round271 WALL point-witness sides | 10,448 |
| Round272 boundary-WALL point-witness sides | 16 |
| **Total** | **21,160** |

A whole-leaf support envelope and a zero-volume point witness are explicitly
not accepted as positive-volume inner support.

## Conditional counts only

- The `274,176` corridor-backed candidates now pass independent verification.
  If a later promoting round issues their occurrence identities, the
  conditional occurrence total is `400,644`.
- If the final `21,160` isolated candidates also receive independently
  verified positive-volume rational inner boxes, the conditional total is
  `421,804`.

Neither number is a frozen promoted occurrence census in Round288.

## Replay and nonpromotion contract

The producer is seed-inert.  Seeds `288071` and `288929` are required to emit
byte-identical result and attachment files.  The standalone verifier was also
executed independently under `PYTHONHASHSEED`/`--seed` pairs `288071` and
`288929`; both runs returned the full independent PASS status and emitted
byte-identical `9,874`-byte verification files with SHA-256
`f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23`.
The embedded verification-object SHA-256 is
`1bff07352d0b58eff1220d58f389939eb0956d0e22926c4c630d0e03358f0cd6`.
Both gzip attachments pass `gzip -t`; the manifest pins the producer,
verifier, result, ledgers, verification, report, and cold replay.

The strict frozen baseline remains:

- expanded occurrences: `126,468`;
- quotient components: `63,224`;
- maximality: `0/63,224`;
- exact-key fibres: `0/116`;
- dispositions: `0/224,580`;
- Gate5: `10/18`;
- D02: `BLOCKED`;
- CM2: `NO-GO_FOR_CLAIM`;
- `Jx/Jy` same-point glue credit: `0`.

## Required next

1. Materialize and dynamically verify a strictly positive-volume rational
   inner box for each of the `21,160` isolated residual atoms.
2. Only a later promoting round may issue occurrence identities; seam quotient,
   final DSU, maximality, fibres, and dispositions remain downstream gates.
