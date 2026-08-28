# CM2 round306c50d global successor CAS protocol freeze v1

As of 2026-08-12 05:50 CST.

## 1. Scope and authority boundary

This document freezes a successor-independent, append-only compare-and-swap
protocol for consuming one installed global authority predecessor and publishing
at most one successor. It supplements, but does not modify or supersede,
`cm2_round306c50c_d02_ab_common_protocol_freeze_v1.md`.

This document is a protocol contract only. It installs no runtime file, closes
no task, grants no whole-parent, formal, ambient, terminal, or D02 gate credit,
and does not change the installed C42 census. Until a conforming final global
head seal commits, the effective authority remains the already installed
predecessor and CM2 remains `NO-GO_FOR_CLAIM`.

## 2. Canonical encoding and hashes

All protocol JSON objects use the following single canonical encoding:

- JSON object keys are sorted lexicographically;
- separators are exactly `,` and `:` with no surrounding whitespace;
- strings are ASCII after JSON escaping (`ensure_ascii=true`);
- NaN and infinities are forbidden (`allow_nan=false`);
- duplicate keys, floats, BOM, NUL, and non-integer JSON numbers are forbidden;
- an object hash is SHA-256 of the canonical bytes after removing only that
  object's named self-hash field; and
- a stored JSON file is the canonical object followed by exactly one LF, while
  its file hash is SHA-256 of those complete stored bytes.

The global predecessor identity schema is exactly:

```text
cm2.global-authority-predecessor-identity.v1
```

The schema string, field names, head-role ordering, canonicalization, namespace,
and basename algorithm below are global protocol constants. A successor round,
candidate schema, release identifier, pair index, or successor hash must not
alter any of them.

## 3. Typed ordered authority heads

The predecessor identity is a closed JSON object with exactly these top-level
fields before its self-hash is appended:

```json
{
  "authority_heads": [],
  "before_census": {},
  "ordered_head_roles": [],
  "schema": "cm2.global-authority-predecessor-identity.v1"
}
```

Its self-hash field is exactly `predecessor_identity_sha256`.

Each `authority_heads` row has exactly these fields:

```json
{
  "authority_schema": "<installed seal schema>",
  "role": "<typed role>",
  "seal_file_sha256": "<64 lowercase hex>",
  "seal_object_sha256": "<64 lowercase hex>",
  "seal_path": ".cm2-runtime/<fixed relative path>",
  "successor_checkpoint_object_sha256": null
}
```

`successor_checkpoint_object_sha256` is either `null` when that authority has no
logical checkpoint or one 64-lowercase-hex object hash. No optional or extra
row fields are allowed in v1.

The v1 role registry and rank are:

1. `FORMAL_COARSE`
2. `LOGICAL_TASK`
3. `GLOBAL_COMPOSITE`

`ordered_head_roles` must contain unique roles in that rank order, and the
`authority_heads` rows must appear in exactly the same order. A legacy bridge
identity has exactly `FORMAL_COARSE, LOGICAL_TASK`. Once the first conforming
global head seal commits, its descendants use exactly one `GLOBAL_COMPOSITE`
row pointing to the immediately preceding committed global head seal. Mixing a
legacy bridge row with `GLOBAL_COMPOSITE`, reordering rows, duplicating a role,
or silently adding a head is rejected.

`before_census` has exactly these integer fields:

```json
{
  "logical_pending_task_count": 0,
  "paired_coarse_cells": 0,
  "representative_parents_remaining": 0,
  "two_side_pending_occurrence_count": 0,
  "unresolved_coarse_cells": 0,
  "whole_representative_parent_count": 0
}
```

The census is part of the predecessor identity. Thus the same seal bytes paired
with a different claimed census do not address the same CAS slot.

## 4. Frozen C42/C48 legacy bridge identity

The first successor governed by this protocol must construct the legacy bridge
identity with these exact roles and installed authorities:

```json
{
  "authority_heads": [
    {
      "authority_schema": "cm2.round306c42.f1-authority-commit-seal.v1",
      "role": "FORMAL_COARSE",
      "seal_file_sha256": "0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d",
      "seal_object_sha256": "b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460",
      "seal_path": ".cm2-runtime/c42-current-authority-seal",
      "successor_checkpoint_object_sha256": null
    },
    {
      "authority_schema": "cm2.round306c48.d02-a-pair668-generation1-successor-installer.v1.authority-seal",
      "role": "LOGICAL_TASK",
      "seal_file_sha256": "13a07654d2eba6b2f1072d4a6a70636a90437e1da18e0bbeb8630ab841e026c1",
      "seal_object_sha256": "95297adbe0d2ee86788008046bc47c337a9c7a3fa0e46bd896e674a2931ec6b1",
      "seal_path": ".cm2-runtime/c48-current-task-authority-seal",
      "successor_checkpoint_object_sha256": "bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984"
    }
  ],
  "before_census": {
    "logical_pending_task_count": 33640,
    "paired_coarse_cells": 574,
    "representative_parents_remaining": 575,
    "two_side_pending_occurrence_count": 67280,
    "unresolved_coarse_cells": 1150,
    "whole_representative_parent_count": 287
  },
  "ordered_head_roles": ["FORMAL_COARSE", "LOGICAL_TASK"],
  "schema": "cm2.global-authority-predecessor-identity.v1"
}
```

Before using this identity, a verifier and installer must capture both seal
files by stable `O_NOFOLLOW` file descriptors, verify their file and object
hashes, schemas, statuses, and censuses, and verify the C48 installation receipt
bound by the C48 seal. That receipt must in turn bind the exact C42 token, audit
token, and authority-seal hashes. Merely observing the two filenames or trusting
a candidate's copy of these facts is insufficient.

## 5. Global CAS namespaces and target names

The claim namespace is exactly:

```text
.cm2-runtime/cm2-global-successor-claims
```

For predecessor identity hash `<P>`, the only valid claim basename and path are:

```text
predecessor-<P>.claim
.cm2-runtime/cm2-global-successor-claims/predecessor-<P>.claim
```

The final global head namespace is exactly:

```text
.cm2-runtime/cm2-global-authority-heads
```

The only valid final seal/head basename and path for the same predecessor are:

```text
predecessor-<P>.seal
.cm2-runtime/cm2-global-authority-heads/predecessor-<P>.seal
```

Neither basename contains `C53`, a round number, a release identifier, a pair
index, a candidate hash, a transaction hash, a promotion hash, or any other
successor-controlled value. All conforming successor versions therefore
contend on the same two no-replace targets for the same predecessor.

An advisory runtime-directory lock may serialize conforming writers, but it is
not the fork-prevention primitive. Persistent fork prevention comes from the
predecessor-keyed targets and atomic no-replace publication.

## 6. Immutable claim payload and acyclic bindings

The claim schema is exactly:

```text
cm2.global-authority-predecessor-consumption-claim.v1
```

The claim is a closed canonical object with self-hash field
`claim_object_sha256`. Before that field is appended, it has exactly:

```json
{
  "authority_seal_target_path": ".cm2-runtime/cm2-global-authority-heads/predecessor-<P>.seal",
  "independent_audit_object_sha256": "<64 lowercase hex>",
  "installation_receipt_file_sha256": "<64 lowercase hex>",
  "installation_receipt_object_sha256": "<64 lowercase hex>",
  "pair_transaction_object_sha256": "<64 lowercase hex>",
  "post_seal_effective_checkpoint_object_sha256": "<64 lowercase hex>",
  "predecessor_identity": {},
  "promotion_derivation_object_sha256": "<64 lowercase hex>",
  "schema": "cm2.global-authority-predecessor-consumption-claim.v1",
  "successor_descriptor_object_sha256": "<64 lowercase hex>",
  "zero_credit_before_seal": true
}
```

The full closed predecessor identity is embedded, and `<P>` in the target path
must equal its verified self-hash. The successor descriptor must bind the exact
candidate checkpoint, pair transaction, independent audit, promotion
derivation, post-seal effective checkpoint, complete before/after censuses, and
all credit locks.

Bindings are strictly one-way:

```text
candidate and transaction
    -> independent audit
    -> promotion derivation and post-seal effective checkpoint
    -> successor descriptor and installation receipt
    -> predecessor-consumption claim
    -> final global head seal
```

The claim must not contain the final seal's file hash or object hash. The final
seal binds the claim file/object hashes, successor descriptor, receipt,
promotion derivation, and effective checkpoint. This direction forbids a
claim/seal hash cycle while still making the final seal uniquely reconstructible
and independently verifiable.

The claim by itself is only a durable reservation. It grants zero credit and
does not advance the global head. A different existing claim at the same path
is a fork attempt and is rejected. An existing claim may be resumed only when
its complete bytes, mode, ownership, link count, file hash, object hash, and all
referenced bindings are exact.

## 7. Post-seal effective state and pair credit

A zero-credit candidate may keep selected task states as
`candidate_closed=true`, `formal_closed=false`, with all task credit-lock fields
zero. The independently minted promotion derivation must construct and hash the
post-seal effective checkpoint rather than merely assert a census delta.

For the pair-1 two-task transaction, the effective checkpoint must establish:

- exactly the two selected tasks become `formal_closed=true`;
- the other 587 shard task states remain byte-equivalent to their required
  predecessor states;
- each selected task retains zero task-level ambient, terminal, whole-parent,
  D02 gate, and formal credit, so no task can claim partial parent credit;
- one pair-level lock, and only that lock, has `whole_parent_credit=1`;
- `D02_gate_credit=0` everywhere;
- formal closed task count increases by exactly two; and
- the effective checkpoint, promotion derivation, independent audit, claim,
  receipt, and final seal all bind the same transaction and selected task
  identities.

The exact prospective transition for this transaction is:

```text
logical pending tasks:          33,640 -> 33,638
two-side pending occurrences:   67,280 -> 67,276
paired coarse cells:                574 -> 576
unresolved coarse cells:          1,150 -> 1,148
representatives remaining:          575 -> 574
whole representative parents:      287 -> 288
whole-parent credit:                  0 -> 1
D02 gate credit:                       0 -> 0
```

The verifier must check `paired_coarse_cells = 2 *
whole_representative_parent_count`, `unresolved_coarse_cells = 2 *
representative_parents_remaining`, and `whole_representative_parent_count +
representative_parents_remaining = 862` before and after. Until the final global
head seal commits, all after-values are prospective only and the before-values
remain authoritative.

## 8. Publication order and required primitives

The only conforming publication order is:

1. stable capture and validation of every predecessor and evidence input;
2. immutable candidate, independent-audit, promotion, effective-checkpoint,
   successor-descriptor, manifest, and receipt bundles;
3. exact terminal replay and file/directory `fsync` of every referenced bundle;
4. the predecessor-keyed claim, published with
   `renameat2(RENAME_NOREPLACE)` and parent-directory `fsync`;
5. optional compatibility pointers, which have no authority without the final
   seal;
6. stable re-attestation of all inputs, bundles, the claim, runtime directory,
   and target-path absence/exactness;
7. the predecessor-keyed final global head seal, published last with
   `renameat2(RENAME_NOREPLACE)` and parent-directory `fsync`; and
8. read-only terminal replay of the complete committed chain.

Required file operations are `O_EXCL`, `O_NOFOLLOW`, `O_CLOEXEC`, bounded exact
reads, singleton regular-file checks, owner checks, file `fsync`, containing
directory `fsync`, and Linux atomic no-replace rename. Runtime and containing
directory file-descriptor identities must equal their path identities again
immediately before claim publication and immediately before final seal
publication.

The final global head seal is the only semantic commit. No runtime or canonical
file may be written after it. Post-commit work is limited to stable, read-only
replay and reporting to stdout or an already prepared receipt bound by the seal.

## 9. Crash recovery and idempotency

The durable states are:

- `S0`: no new exact bundle, claim, pointer, or seal;
- `S1`: some or all immutable bundles exist, but no claim;
- `S2`: all referenced bundles and the exact claim exist, but no final seal;
- `S3`: the exact claim and zero or more exact compatibility pointers exist,
  but no final seal;
- `S4`: the exact claim, all required bundles/pointers, and exact final seal
  exist.

At `S0` or `S1`, another candidate may still win the predecessor CAS. At `S2`
or `S3`, the predecessor is reserved and only byte-exact recovery of the same
claim and successor is allowed. A different candidate must fail closed; no
automatic deletion, replacement, expiry, or claim stealing is permitted. At
`S4`, an exact retry performs only verification and returns an idempotent
`RESUMED_EXACT` result.

An interrupted stage directory or file may be resumed only by verifying every
existing member and completing only absent members from the exact frozen
payload. Unexpected inventory, different bytes, wrong mode/owner/link count,
symlinks, hard links, or an unbound stage causes fail-closed rejection. A crash
after the final no-replace rename but before process output is still a committed
authority and must be recognized by exact replay.

Failure reporting must track whether bundle, claim, pointer, or seal writes may
have occurred. It must not claim `runtime_writes_performed=false` after a
partial prefix was published. Regardless of a partial prefix, formal and D02
credit remain zero unless the exact final seal is present and fully replayed.

## 10. Global head resolution and fork rejection

Starting from a verified predecessor identity, a resolver computes `<P>` and
examines only the two protocol paths derived in section 5.

- No claim and no seal means the predecessor remains the head.
- An exact claim without an exact seal is a reservation; the predecessor remains
  the effective head and no after-census is authoritative.
- A seal without the exact claim and complete referenced prefix is invalid.
- Exact claim plus exact final seal commits one successor. The final seal is the
  new `GLOBAL_COMPOSITE` authority head, and its exact after-census becomes the
  before-census of the next predecessor identity.
- Any different bytes at either predecessor-keyed target, more than one
  outgoing link, a role/order mismatch, or a census mismatch is a fork and must
  fail closed.

Release-specific `current` pointers, candidate tokens, audit tokens, reports,
or canonical summaries are compatibility aids only. None can select, replace,
or override the global head. A future successor consumes the immediately prior
committed global head through a `GLOBAL_COMPOSITE` row and competes on the new
predecessor-derived claim/head targets.

## 11. Mandatory installer blocking checks

A conforming installer must reject before the final seal unless all of the
following are true:

1. this protocol file and its SHA-256 companion are frozen and pinned;
2. canonical encoding and every source/file/object pin are exact;
3. the installed C42 seal, C48 seal, C48 receipt, and their pointer bindings are
   stably captured and cross-validated;
4. the predecessor identity uses the exact global schema, ordered roles,
   before-census, namespace, and successor-independent basenames;
5. candidate, independent audit, promotion derivation, effective checkpoint,
   successor descriptor, receipt, and manifests are independently valid and
   mutually bound;
6. the effective two-task formal closure and the pair-level-only credit lock
   reproduce `576 / 1,148 / 574 / 288` with D02 gate credit zero;
7. the existing claim/head states form one allowed exact recovery prefix;
8. different claim/head bytes are rejected as a fork;
9. all held inputs, parent directories, and staged/final bytes are unchanged at
   the pre-claim and pre-seal barriers;
10. the final global head seal is the last write and binds the exact claim,
    audit, promotion, effective checkpoint, receipt, and before/after census;
11. terminal read-only replay verifies the complete committed chain; and
12. failure output truthfully records partial writes and never awards credit
    merely because a claim, pointer, receipt, or unsealed candidate exists.

Any failed or unavailable check is a hard `NO_INSTALL`, with zero formal and
zero D02 gate credit.
