# CM2 Round306C43 f1 authority transaction contract v1

Date: 2026-08-11 (Asia/Shanghai)

Status: `DESIGN_ONLY__NOT_INSTALLER_READY__NO_C43_AUTHORITY`

## Scope and non-authority boundary

This document is a read-only transaction design. It is not an installer, an
independent audit, an installation receipt, an authority seal, or an authority
claim. Creating this file must not create or alter anything below
`.cm2-runtime`.

At the time of this design the following three authority targets are absent:

- `.cm2-runtime/c43-current-token`;
- `.cm2-runtime/c43-current-audit-token`;
- `.cm2-runtime/c43-current-authority-seal`.

The C43 producer candidate exists, but its independent audit is not yet frozen
and installed authority therefore remains C42. No installer source may be
written from this contract until every item marked `UNSET` below has been
replaced by an independently verified exact pin.

## Frozen existing C43 inputs

The proposed transaction is restricted to this one formal f1 producer run. No
path override, f2 token, review-only directory, or byte-identical alternate run
is admissible.

| Item | Exact value |
|---|---|
| Candidate token | `c43-sole-deficit-owner-closure-20260811T082400Z-f1` |
| Candidate directory | `.cm2-runtime/candidates/c43-sole-deficit-owner-closure-20260811T082400Z-f1` |
| Candidate result file SHA-256 | `76e367a7e02d5d4fb568e11e85c1facb5a24ce3dd522448bebf66c3ec6e5df07` |
| Candidate object SHA-256 | `79831178f4450c41540b7ff0f51bde96e61517cbc36a2287efbf0a100cba5bbc` |
| Root-manifest file SHA-256 | `8bc3b4259f7a600260344436cfc337621c532b44514866ed9fb8425a378390ff` |
| Manifest inventory | exactly 12 members, all 12 verified |
| Producer receipt path | `.cm2-runtime/audit/c43-sole-deficit-owner-closure-20260811T082400Z-f1/execution_receipt.json` |
| Producer receipt file SHA-256 | `38761997cdf8df6f6f1a7b1aecffa5e165ea8af4139a28a329bc544e88489263` |
| Producer receipt object SHA-256 | `96ba926d2e20db3c2d9905757736f6a3c0eac4e4dd471f911b38caef4ee0e215` |
| Producer InvocationID | `c43-formal-producer-20260811T082400Z-f1` |
| Producer source | `deliverables/cm2_round306c43_d02_sole_deficit_owner_closure_v1.py` |
| Producer source SHA-256 | `a279b3cb7ff4b7ec7d8f11f097971acf51a510087a796eab60b73cf139c331f4` |
| Future candidate pointer bytes | ASCII token above followed by exactly one LF |
| Future candidate pointer SHA-256 | `ba1772c646f2cba85ebad502f59b20ac0d9dc69e801c37c84301caf68ab3a24c` |

The installer must parse canonical JSON with duplicate-key and non-finite-value
rejection, verify each document self-hash, verify the manifest's strict sorted
grammar, require exact candidate-directory inventory, and descriptor-capture
all 12 manifest members. A successful `sha256sum -c` alone is necessary but not
sufficient.

The exact proposed post-commit census is:

| Quantity | Installed C42 | Proposed C43 |
|---|---:|---:|
| Paired coarse cells terminal | 574 | 578 |
| Whole representatives | 287 | 289 |
| Remaining representatives | 575 | 573 |
| `EARLIEST_PREFIX_EXCLUDED` | 75,386 | 75,390 |
| `TYPED_EVENT_GRAPH` | 296 | 296 |
| `UNRESOLVED_R1648_CONTINUATION` | 1,150 | 1,146 |
| Terminal total | 76,832 | 76,832 |

Only pairs 592 and 715 receive whole-parent credit. Pairs 97, 211, and 664
remain zero-credit blockers. Pair 391 and all other pre-existing C42 parent rows
must be unchanged. The candidate must retain `unresolved_zero=false`,
`D02=BLOCKED_BY_1146_COMPLETE_R1648_CONTINUATIONS`, `D03=UNAUTHORIZED`,
`D04=NOT_MINTED`, `Gate5=10/18`, and `CM2=NO-GO_FOR_CLAIM`.

## Frozen installed C42 predecessor authority

C43 must extend the exact currently installed C42 transaction, not merely a C42
candidate with matching payload bytes.

| Item | Path or token | File SHA-256 | Object SHA-256 |
|---|---|---|---|
| Current C42 candidate pointer | `.cm2-runtime/c42-current-token` -> `c42-p391-formal-producer-20260811T044500Z-f1` | `fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07` | n/a |
| Current C42 audit pointer | `.cm2-runtime/c42-current-audit-token` -> `c42-independent-audit-20260811T052900Z-p391-f1` | `59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5` | n/a |
| C42 authority seal | `.cm2-runtime/c42-current-authority-seal` | `0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d` | `b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460` |
| C42 installation receipt | `.cm2-runtime/audit/c42-f1-authority-install-a50914a266af-85a7cd719cee-v1/installation_receipt.json` | `3599494ff330a367a6c27ee57c19c01e86626428871d014c9153f290fdfc407f` | `c5f2eb78a0d9d717326bc57fb14df823ab3c5181e3e613a0327425c5e33e784e` |
| C42 candidate result | `.cm2-runtime/candidates/c42-p391-formal-producer-20260811T044500Z-f1/result.json` | `f029c3ce6af33e2f93c33b4155286f60bfafecd724720a598b103ca3c263ccb0` | `a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2` |
| C42 candidate manifest | `.cm2-runtime/candidates/c42-p391-formal-producer-20260811T044500Z-f1/root_manifest.sha256` | `ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058` | n/a |
| C42 producer receipt | `.cm2-runtime/audit/c42-p391-formal-producer-20260811T044500Z-f1/execution_receipt.json` | `5a14c48b028dd20951d02659f9d9655f5718a13e69d2811ee823d78c38530a55` | `e89f66d0e7636bfa781a6ef7e0309fc1ad00c3215ea699c08b231003e1c39f08` |
| C42 independent audit | `.cm2-runtime/audit/c42-independent-audit-20260811T052900Z-p391-f1/independent_audit.json` | `d60bb3c8f79f989df776effa4616ec170097a018547b1f4c929ad068c11138d3` | `85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c` |

The C42 installer and independent transaction-auditor sources are also frozen
as provenance anchors:

- `deliverables/cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_v1.py`,
  SHA-256 `4b4e96bcb2c701fd6820a04271e2f02058e3699d980a4bee61d4090b2ce30c78`;
- `deliverables/cm2_round306c42_d02_singleton_wall_endpoint_owner_closure_independent_auditor_v1.py`,
  SHA-256 `6da5c8a3f2960ec9f763e314be01e909722b6b03bcd2817e5030295dcd6086eb`;
- `deliverables/cm2_round306c42_f1_authority_transaction_installer_v1.py`,
  SHA-256 `66f88bc5913af695691c5ae58be7938f94f3f68a9eeeeed32bcd96b37938c276`;
- `deliverables/cm2_round306c42_f1_authority_transaction_independent_auditor_v1.py`,
  SHA-256 `a37bf76da4674831c90d4e5839e7134b7ebfd9167a0a60840996a331039a06e2`.

Before any C43 publication, an independent parser must reconstruct the C42
receipt and seal, require their exact mutual bindings, verify exact pointer
bytes, and replay the C42 installed-state census of 574 paired / 287 whole /
1,150 unresolved. Invoking the C42 auditor can be an additional check but must
not replace the C43 installer's own inert-byte validation.

## Mandatory future freeze gate

The following values are deliberately not guessed. Every field must be frozen
before a C43 installer source is created.

The audit-only object
`8acaf57389cf4d4e741a1824217eb2f50213b07aeae2c9b10c3c299ee59067d0`
at token `c43-independent-audit-20260811T114800Z-owner-subset-f1` does **not**
satisfy this gate.  Hostile review rejected it for non-independent core logic,
post-rename fallible publication checks, and incomplete source/authority
TOCTOU closure.  See
`deliverables/cm2_round306c43_owner_subset_audit_rejection_report_v1.md`.
It must not be substituted for any `UNSET` field below.

The proposed v2 source at SHA-256
`ef0607b6d8063dd5368f7b0963dede438eca70d25da4ad95eec8e8486b879abe`
also does **not** satisfy this gate.  Pre-run hostile review found that it
still imports the C41/C39/C40 high-level router, substantially reproduces the
v1 ledger projection, uses a constant-plus-delta 76,832 census, verifies
owner-writable dependencies only after import, and lacks filesystem/commit
fault injection.  Its formal audit was deliberately not run and the reserved
v2 token is absent.  The rejection report above records both decisions.

| Required future item | Required value now |
|---|---|
| C43 independent-audit token | `UNSET` |
| C43 independent-audit JSON path | `UNSET` |
| C43 independent-audit file SHA-256 | `UNSET` |
| C43 independent-audit object SHA-256 | `UNSET` |
| C43 independent-auditor source path | `UNSET` |
| Frozen independent-auditor source SHA-256 | `UNSET` |
| Exact PASS status and coherent attack count | `UNSET` |
| Future audit pointer SHA-256 (`audit-token + LF`) | `UNSET` |
| C43 installation release id | `UNSET` |
| C43 installer source path and SHA-256 | `UNSET` |
| C43 transaction-auditor source path and SHA-256 | `UNSET` |
| Exact installation confirmation phrase | `UNSET` |

The future independent audit must bind, at minimum, the exact C43 candidate
path/object/manifest, producer receipt object and InvocationID, producer source
hash, its own frozen source hash, and the installed C42 candidate/audit/seal/
installation-receipt objects above. It must report every coherent attack as
true, retain `authority_pointer_installed=false` and
`producer_output_is_authority=false`, and independently reconstruct rather than
self-compare the candidate aggregates, two-pair eligibility, three blocked
pairs, all 862 conservation rows, 76,832 census, gzip members, lower-strata
ownership, and reflection bindings.

The audit source currently in the working tree is not a pin merely because it
has a file hash. Its source hash becomes admissible only after code review,
self-test, formal audit publication, manifest/receipt verification, and a
terminal stable read. The installation release id should then be derived from
the fixed candidate and audit object prefixes, for example
`c43-f1-authority-install-79831178f445-<audit-object-prefix>-v1`; the literal id
must be frozen, not formatted from mutable runtime input.

## Filesystem and descriptor contract

The installer must follow these rules for every input and output:

1. Resolve all paths beneath the fixed workspace root and reject every symlink
   component lexically. Open the workspace, `.cm2-runtime`, its `audit`
   directory, candidate directory, and release directory using retained dirfds
   with `O_DIRECTORY|O_NOFOLLOW|O_CLOEXEC`.
2. Open every pinned input once with `O_RDONLY|O_NOFOLLOW|O_CLOEXEC`; require a
   user-owned, bounded, single-link regular file; retain its fd through the
   seal commit and terminal replay. Compare path stat, fd stat, size, mode,
   uid/gid, nanosecond times, inode/device, link count, and content SHA before
   and after publication.
3. Bind the runtime and audit-root directory identities before publication and
   reattest them before seal and after commit. Acquire a nonblocking exclusive
   advisory lock on the retained runtime dirfd for cooperative serialization;
   correctness must still rely on no-replace operations rather than the lock.
4. Create output files relative to retained dirfds with
   `O_WRONLY|O_CREAT|O_EXCL|O_NOFOLLOW|O_CLOEXEC`, write all bytes with short-write
   handling, set mode `0444`, `fsync` the file, replay exact bytes, and `fsync`
   the containing directory.
5. Publish only with Linux `renameat2(RENAME_NOREPLACE)` on the same filesystem.
   If `renameat2` or `RENAME_NOREPLACE` is unavailable, fail closed. Ordinary
   `rename`, `replace`, `mv`, hard-link promotion, overwrite, and unlink-then-
   rename are forbidden.
6. The prepared receipt is the sole file in a release-specific directory. Its
   private stage directory begins mode `0700`; after writing and fsync it becomes
   mode `0500`, is fsynced again, and is renamed no-replace into the final
   release directory. The final receipt is mode `0444`, and the final directory
   inventory must remain exactly one file.
7. Use release-specific private stage names for the candidate pointer, audit
   pointer, seal, and receipt directory. A stage created in the current live
   process is guarded by an open fd and exact inode/byte checks through its
   rename. A pre-existing stage is never assumed to be trustworthy.
8. Every successful rename is followed by parent-directory `fsync`, exact target
   byte replay, and inode/descriptor reattestation. Every error, short write,
   fsync failure, identity drift, extra directory member, or target collision
   rejects the transaction.

The intended final paths are:

- receipt: `.cm2-runtime/audit/<frozen-release-id>/installation_receipt.json`;
- candidate pointer: `.cm2-runtime/c43-current-token`;
- audit pointer: `.cm2-runtime/c43-current-audit-token`;
- authority seal: `.cm2-runtime/c43-current-authority-seal`.

All four are new C43 nodes. The transaction must not modify or replace any C42
node.

## Publication order and sole commit point

The only allowed durable order is:

```text
prepared installation receipt
    -> C43 candidate pointer
    -> C43 audit pointer
    -> C43 authority seal
```

The final no-replace rename of the exact authority seal is the sole semantic
commit point. The receipt and both pointers explicitly carry no formal
authority before that seal. The seal publication must be followed by runtime
directory fsync; if a process dies in the rename/fsync window, recovered state
is decided solely by a stable exact read after restart: an exact persisted seal
means committed, and no seal means not committed. No log message or process
exit code can substitute for the seal.

Immediately before constructing the seal, the installer must reattest all held
input fds, the complete C42 authority, the prepared receipt, both C43 pointers,
the runtime and audit-root identities, the release-directory identity and exact
inventory, and the absence of every private stage. The seal is then constructed
from those recaptured bytes, not from unverified in-memory labels.

## Exact-prefix crash states and recovery

`A` means absent and `E` means the exact frozen regular-file/directory object.
Any other value is a mismatch and fails closed.

| State | Receipt | Candidate pointer | Audit pointer | Seal | Authority? | Allowed action |
|---|---:|---:|---:|---:|---:|---|
| S0 | A | A | A | A | no | Fresh install may prepare receipt |
| S1 | E | A | A | A | no | Revalidate all pins and resume candidate pointer |
| S2 | E | E | A | A | no | Revalidate all pins and resume audit pointer |
| S3 | E | E | E | A | no | Revalidate all pins, rebuild receipt/seal, then publish seal |
| S4 | E | E | E | E | yes | No installation writes; independently audit installed state |

The only automatically resumable states are S1 through S3 with exact final
prefix nodes and no stage nodes. An existing receipt is the immutable receipt
of the original preparing process: resume must validate and reuse its exact
InvocationID, installer hash, capture records, self-hash, and bytes. It must not
rewrite timestamps, PID metadata, or stat fingerprints to make them match a new
process.

The following are forbidden non-prefix states: any pointer without the exact
receipt; audit pointer without candidate pointer; seal without all three exact
predecessors; any wrong bytes, object, mode, owner, link count, inventory, path,
or release id; and any exact target accompanied by a private stage.

A crash before a stage rename can leave an orphan stage. Normal install and
resume modes must stop without deleting, adopting, or overwriting it. A separate
read-only recovery inspector must first bind the stage by dirfd, prove exact
bytes/schema/object/inode and that the recorded producer process is no longer
the same live process. Only a separately authorized recovery operation may then
promote that exact stage using `RENAME_NOREPLACE` or quarantine it. There is no
automatic `unlink` cleanup because a name may have been replaced between checks.

Crash outcomes by boundary are therefore deterministic:

- before a stage rename: no new final prefix node; an orphan stage blocks normal
  recovery and has no authority;
- after a receipt or pointer rename but before parent fsync: restart sees either
  the exact next prefix or its prior prefix and acts accordingly;
- after seal rename but before runtime fsync: restart sees either exact S4
  authority or exact S3 non-authority; there is no third semantic state;
- after final fsync but before the installer reports success: exact S4 remains
  committed, and rerun performs only installed-state audit.

## Prepared installation receipt contract

The receipt is canonical ASCII JSON with exactly one terminal LF and a
self-hash calculated over all other fields. Its exact schema must include:

- fixed schema, prepared/non-authority status, literal release id, InvocationID,
  original installer PID/start ticks/time, installer path and frozen source hash;
- descriptor capture records for the C43 producer source, all 12 candidate
  manifest members, candidate manifest, result, producer receipt, future C43
  independent audit and source, current C42 pointers/seal/receipt, referenced
  C42 candidate/audit/manifest/producer receipt, and all sources needed to
  validate those bindings;
- object bindings for C43 candidate, producer receipt and independent audit, and
  for C42 candidate, producer receipt, independent audit, installation receipt,
  and authority seal;
- exact candidate and audit pointer path, token, bytes SHA-256, stage name and
  publication order;
- the sole seal commit rule, `pointers_before_seal_have_formal_authority=false`,
  and `exact_final_prefix_recovery_only=true`;
- exact pre-install C42 census and proposed post-install C43 census;
- filesystem policy flags for `O_EXCL`, `O_NOFOLLOW`, `O_CLOEXEC`, file fsync,
  directory fsync, dirfd-relative operations, and
  `renameat2(RENAME_NOREPLACE)`; and an explicit false flag for ordinary rename,
  replace, overwrite, hard-link publication, and `mv`.

Receipt validation must reconstruct the exact expected object from frozen pins
and current descriptor records. Merely checking its self-hash is insufficient.

## Authority seal contract

The seal is canonical ASCII JSON with one LF, mode `0444`, a self-hash, and no
fields supplied by a caller. It must bind at least:

- literal release id and receipt path;
- receipt file SHA-256 and installation-receipt object SHA-256;
- exact C43 candidate and audit tokens, pointer file hashes, candidate object,
  independent-audit object, producer-receipt object, and candidate manifest;
- frozen installer source SHA-256 and the frozen mathematical independent-
  auditor source SHA-256;
- predecessor C42 candidate/audit/seal/installation-receipt objects and the four
  current C42 node file hashes;
- exact formal census `578 paired / 289 whole / 573 remaining / 1,146
  unresolved`, total 76,832, `unresolved_zero=false`, `D02=BLOCKED`, and
  `CM2=NO-GO_FOR_CLAIM`;
- `this_seal_is_required=true`, compatibility pointers without this seal are not
  authority, and publication is
  `renameat2_RENAME_NOREPLACE_then_runtime_fsync`.

The seal validator must independently reconstruct this entire document from
the exact receipt and compile-time pins. A self-consistent but differently
bound seal is rejected.

## Independent transaction auditor

A later C43 transaction auditor must be a separately frozen source file. It
must not import or execute the installer or trust installer helper functions.
It needs three non-writing modes:

1. `--preflight`: validate every frozen C43/C42 input and require pristine S0
   plus absence of all stage nodes;
2. `--classify`: report S0-S4 or a precise forbidden/stage state without
   changing it;
3. `--audit-installed`: require exact S4, independently reconstruct receipt and
   seal, replay all pointer and lineage bytes, require no stages, and perform
   initial/terminal descriptor reattestation.

It must pin the final installer source hash, while the installer pins the frozen
mathematical C43 auditor source and its published audit object. This one-way
dependency avoids a source-hash cycle. Successful installed audit must still
report D02 blocked and CM2 no-go.

## Minimum hostile and crash test matrix

Tests must mutate coherent copied fixtures and rebuild downstream container,
row, object, and manifest hashes where appropriate. A stale-checksum rejection
does not demonstrate semantic independence.

### Frozen input and semantic attacks

1. Substitute a different C43 token, alternate producer run, f2 path, or
   review-only directory.
2. Mutate candidate result and coherently rebuild its self-hash and manifest.
3. Add, remove, reorder, duplicate, rename, or swap a manifest member.
4. Add an unmanifested candidate-directory file.
5. Mutate producer receipt path, object, InvocationID, source hash, manifest
   hash, PID/start-tick type, or non-authority fields.
6. Drift the producer source after initial capture.
7. Change eligible pairs 592/715, grant credit to 97/211/664, or mutate pair
   391 while coherently rebuilding every aggregate.
8. Drop or duplicate an 862-parent conservation row; report 577/579 paired,
   288/290 whole, 1,145/1,147 unresolved, total other than 76,832, or
   `unresolved_zero=true`.
9. Set D02 PASS, authorize D03/D04, change Gate5, or set producer authority true.
10. Corrupt a gzip header, trailer, row order, row hash, reflection binding,
    face/corner owner, or closed-leaf proof while rebuilding outer hashes.
11. Substitute the future C43 audit token, JSON, object, source, candidate
    binding, receipt binding, manifest binding, PASS status, attack count, or
    change one attack result to false.
12. Supply an audit that self-compares baseline objects, hard-codes the eligible
    set instead of deriving it, omits cold replay, or does not reattest held
    descriptors.

### Predecessor-authority attacks

13. Replace either current C42 pointer with f2, an alternate token, missing LF,
    extra LF, or non-ASCII bytes.
14. Mutate the C42 candidate, manifest, producer receipt, independent audit,
    installation receipt, or authority seal, including coherently rebuilt
    self-hashes.
15. Change any C42 seal-to-receipt, receipt-to-pointer, audit-to-candidate, or
    candidate-to-C42-lineage binding.
16. Change the C42 census or make the C43 candidate name a different predecessor
    authority.
17. Replace a C42 input path after its fd capture or swap a parent directory
    before seal.

### Transaction object attacks

18. Duplicate a JSON key, inject NaN/Infinity, non-ASCII, noncanonical spacing,
    missing LF, or double LF into receipt or seal.
19. Change receipt release id, InvocationID, installer hash, capture record,
    pointer record, publication order, filesystem policy, census, or self-hash.
20. Change seal receipt path/file/object, pointer token/hash, candidate/audit
    object, predecessor object, installer/auditor hash, census, semantic commit,
    or self-hash.
21. Present a self-consistent receipt or seal for another release.
22. Claim that receipt or compatibility pointers have authority before seal.

### Filesystem and state-machine attacks

23. Use a symlink in any parent component or as any input, stage, target,
    receipt directory, or receipt file.
24. Use a hard link (`st_nlink>1`), FIFO, socket, device, directory-as-file,
    oversized file, foreign uid, wrong output mode, or extra receipt member.
25. Precreate any target with wrong bytes, or collide during
    `RENAME_NOREPLACE`; verify neither source nor target is clobbered.
26. Exercise every forbidden non-prefix combination, especially pointer without
    receipt, audit without candidate, and seal without all exact predecessors.
27. Place an exact or mismatched stale stage in each of the four stage
    locations; normal install/resume must perform zero cleanup and fail closed.
28. Run two installers concurrently and require at most one exact prefix, never
    mixed receipts or pointers.
29. Replace a staged name after validation, replace a pinned input during the
    transaction, or perform an inode-preserving/content-changing TOCTOU attempt;
    descriptor and terminal guards must reject.
30. Make `renameat2` unavailable, return `EXDEV`, inject a short write, or fail
    any file/directory fsync; no later node may publish.
31. Crash after every file creation, file fsync, stage-directory fsync, no-
    replace rename, parent fsync, and terminal replay for receipt, both pointers,
    and seal; classification must match the exact-prefix table.
32. Crash after seal rename but before runtime fsync, and after runtime fsync but
    before output; stable restart classification alone decides S3 versus S4.
33. Retry exact S1, S2, and S3 with the original receipt and require byte-
    identical continuation; retry with a different InvocationID or source hash
    and reject.
34. Retry exact S4 and require no writes, no stage creation, and independent
    installed-state audit only.

Installer and transaction-auditor self-tests are necessary but not sufficient.
Before live installation, the complete protocol must pass in an isolated clone,
including injected crash/restart at every durable boundary and a separately
implemented terminal audit.

## Freeze and execution sequence

1. Finish, code-review, and freeze the mathematical C43 independent auditor.
2. Publish its audit-only object with no-replace/fsync semantics; independently
   verify its source, receipt, object, attack census, and exact C43/C42 bindings.
3. Fill every `UNSET` pin in a successor of this contract and freeze the literal
   release id, audit pointer bytes/hash, and confirmation phrase.
4. Only then write the dedicated C43 installer; self-test it, code-review it,
   freeze its source hash, and run read-only pristine preflight.
5. Write a separate transaction auditor that pins the frozen installer; freeze
   and self-test it, then run its independent pristine preflight.
6. Execute a full isolated-clone install/crash/recovery matrix and independent
   installed-state audit.
7. Obtain explicit authorization for the live installation transaction. Recheck
   S0 and all input pins immediately before running it.
8. After a committed S4, run the frozen independent transaction auditor before
   updating canonical status documents. Formal accounting then becomes 578
   paired / 289 representatives / 1,146 unresolved, while D02 remains blocked
   and CM2 remains no-go.

## Strict conclusion

The transaction shape is fixed, but installation is not yet authorized or even
installer-ready because the C43 independent audit token, object, file hash,
source hash, PASS status, and audit pointer hash do not yet exist as frozen
inputs. Until those values are fixed and the later seal commits, the only formal
authority is C42 at 574 paired / 287 representatives / 1,150 unresolved.
