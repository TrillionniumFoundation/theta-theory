# CM2 Round306 C50c D02-A/B common protocol freeze v1

Status: **FROZEN INTERFACE CONTRACT; IMPLEMENTATIONS REQUIRE SEPARATE AUDIT;
ZERO FORMAL/D02 CREDIT**.

This document freezes the common occurrence, split, history, owner, handoff,
and successor semantics used between D02-A and D02-B.  It does not certify an
oracle, close a task, install an authority, or change the C42 coarse census.

## 1. Version set and canonical encoding

The only v1 schema identifiers admitted by this contract are:

```text
cm2.round306c50c.d02-ab-protocol.v1.occurrence
cm2.round306c50c.d02-ab-protocol.v1.split-decision-preimage
cm2.round306c50c.d02-ab-protocol.v1.owner-history-row
cm2.round306c50c.d02-ab-protocol.v1.owner-evidence
cm2.round306c50c.d02-ab-protocol.v1.collision-handoff
cm2.round306c50c.d02-ab-protocol.v1.task-successor
```

Objects use strict canonical ASCII JSON: sorted keys, separators `,` and `:`,
no duplicate keys, no NaN/Infinity, and a terminating newline only at the file
boundary.  Every semantic object contains exactly one SHA-256 field over the
same object with that field absent.  A verifier must reject unknown fields,
missing fields, wrong primitive types, noncanonical bytes, and any reclosed
object whose semantics fail below.

Schema versions are immutable.  A change in field meaning, owner ordering,
numeric precision, split selection, or authority source requires a new schema
version and explicit supersession; a hash change alone is not a version.

## 2. Occurrence v1

An occurrence is one physical side of one exact D02 task at one collision and
one adaptive-history position.  It must bind all of:

- installed predecessor authority seal and frozen C41/C46 plan objects;
- `task_id`, `task_binding_sha256`, pair index, shard id/index, task index;
- side in exactly `REPRESENTATIVE` or `REFLECTED`;
- physical cell id, physical origin key, compact chart, official semantic
  path, physical route path, exact closed rational box, and box hash;
- original unsplit box, refinement-parent box/path, current adaptive path,
  and the complete ordered split-decision chain;
- collision index, incoming handoff id, owner-history hash, source-binding
  preimage/hash, and occurrence id derived from the whole semantic body;
- occurrence/history/split protocol versions and numeric runtime pin.

The collision index is exactly `len(owner_history)+1`.  Representative and
reflected occurrences are distinct objects even when related by an exact
involution.  Reflection is independently reconstructed from exact child-box
matching; copying the other side's numerical evidence is forbidden.

The numeric runtime is frozen to python-flint `0.9.0` with Arb precision 384
bits for the present kernel.  Every public producer and verifier entry must
check that pin before accepting or computing an object.

## 3. Split-decision preimage v1

Every adaptive split row binds:

- zero-based split ordinal and collision index;
- source binding, occurrence, owner-history, and incoming handoff ids;
- exact parent box/path and the full numerical evidence projection that made
  the parent unresolved;
- the recomputed sensitivity decision, axis, and exact rational coordinate;
- `selected_child_bit`, whose only legal values are the strings `0` and `1`;
- exact left/right children, selected child box/path, and exact conservation;
- codimension face/endpoint/corner obligations created by the split;
- zero-credit locks and its self-hash.

Validation must replay the unresolved parent numerically, recompute the split
decision, construct both children, enforce the child-bit enumeration, and
compare the selected child byte-for-byte.  Treating every value other than
`0` as the right child is forbidden.  A suffix that can merely be interpreted
as some t/p shuffle is insufficient without the complete decision chain.

Every finite frontier must be prefix-free and have exact relative Kraft sum
one.  Resource exhaustion returns the whole conserved pending frontier; it is
never a terminal proof.  A nested endpoint limit is discharged only by an
explicit globally complete codimension oracle, not by an implicit depth cap.

## 4. Owner-history row and owner-evidence v1

History is a contiguous ordered list.  Row `i` has collision index `i+1` and
contains the complete evidence preimage plus its digest, selected owner,
previous evidence digest/handoff, and next handoff.  Splicing, deletion,
duplication, reordering, or an occurrence/source/box discontinuity rejects the
entire continuation.

Each owner-evidence preimage binds, at minimum:

```text
exact owner; discriminant; strict root order; frozen candidate order;
complete candidate rows and their sequence hash; official word;
incoming/outgoing chart and strict chart margins; wall and event order;
homogeneity; incidence; physical core; structured terminal margin;
full original occurrence; prior history; next handoff; zero-credit locks.
```

Hashes provide integrity only.  An independent verifier must recompute the
entire numerical body and split history; a coherently edited and rehashed body
must be rejected.  A verifier that imports the producer or calls its numeric
decision functions is structural replay, not an independent implementation.

## 5. Global owner and exterior obligations

Local strict collision evidence does not by itself issue a terminal class.
Before terminal promotion, the occurrence must reference independently sealed
results for both global contracts when applicable:

```text
GLOBAL_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_ORACLE
GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE
```

The codimension oracle reconstructs the full active occurrence universe after
all replacements, atomizes every target face, represents endpoint/corner
germs explicitly, checks all incident sides/quadrants and reflection
equivariance, and chooses one owner by the frozen semantic-path ordering.
Local siblings or a task-local overlay are not a global completeness proof.

The exterior oracle may issue only a strict cemetery/disconnected certificate
against the frozen global registry.  `BOUNDED`, no current contact, an empty
local wall list, or failure to find a known component are pending states, not
cemetery evidence.

## 6. Collision handoff v1

A handoff binds the completed evidence hash, occurrence id, completed and next
collision indices, exact output box/path, selected owner, appended history
row, both global-oracle references/status, and zero-credit locks.  D02-B may
consume only a D02-A handoff installed under a no-replace seal.  Candidate,
unsealed, diagnostic, or merely hash-matching A output is rejected.

The only legal terminal classes are:

```text
STRICT_EXCLUDED
CONNECTED_TO_KNOWN_COMPONENT
STRICT_CEMETERY_OR_DISCONNECTED
```

Everything else remains a conserved pending continuation through collision
1,648.

## 7. Task-successor v1

A successor binds the exact predecessor checkpoint/seal, protocol versions,
pair-preserving shard, generation, complete ordered task-binding and task-state
sequences, selected indices, unchanged-state byte equality, split/frontier/
exit evidence, pending counts, and all credit locks.  It may change only the
explicitly selected task states.  A task is formal-closed only after both
physical sides, exact Kraft, incidence, global codimension ownership, strict
terminal evidence, a no-producer-import cold verifier, and no-replace seal all
pass.

Task-level closure and D02 gate credit are separate.  Installing a narrow
task successor may reduce the logical task queue while leaving the formal
coarse census unchanged.  Whole-pair/coarse credit is updated only by a
separately audited conservation/census transaction.

Publication order is bundle/manifest, candidate, independent audit, receipt,
compatibility pointers, and semantic seal last.  Required primitives are
`O_EXCL`, `O_NOFOLLOW`, stable pre/post reads, file and parent-directory
`fsync`, and atomic no-replace rename.  The seal is the only commit point.

## 8. Frozen supersession and present credit boundary

- C49 v2 is rejected for authenticated/pure use.
- C49 v3 is retained only as superseded diagnostic provenance.
- Pre-fix C49 v4 source SHA-256
  `c4457b66dc1fdf05848011db2e5eb5369a2f90cb57b5b3b2fb99f5026b8bf860`
  is rejected: it accepted a reclosed non-enumerated child bit and its public
  entries did not enforce the runtime/precision pin.
- The patched v4 source is a fresh zero-credit candidate and requires a new
  full audit/freeze.  Passing local regression does not supply either global
  oracle and cannot promote D02.
- Installed C48 closes exactly one task-level successor and has zero D02 gate
  credit.  The formal coarse authority remains C42's `574 paired / 1,150
  unresolved / 575 representatives remaining` until a later audited
  transaction explicitly changes it.

No implementation is authorized to start full production shards until the
patched C49 line and both global-oracle lines each have a frozen independent
PASS under this protocol.
