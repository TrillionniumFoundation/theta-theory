# CM2 Round306C43 owner-subset audit rejection report v1

Date: 2026-08-11 (Asia/Shanghai)

Status: `REJECTED_FOR_AUTHORITY__ZERO_FORMAL_CREDIT`

## Scope

The audit-only object below completed a deterministic run and is internally
self-hash consistent, but a subsequent hostile static review found blocking
independence and publication-protocol defects.  It must not be frozen, pointed
to, installed, or used to alter the installed C42 census.

- audit token: `c43-independent-audit-20260811T114800Z-owner-subset-f1`;
- audit object SHA-256:
  `8acaf57389cf4d4e741a1824217eb2f50213b07aeae2c9b10c3c299ee59067d0`;
- audit file SHA-256:
  `a9043963a154377555aeae2653197c6fd72f9c500c20c9556dc2f66d404ddeb3`;
- auditor source SHA-256:
  `1e9e6d5c8031fc5863a9ac7cfc9fe1e7f40029797f2549a30e8d19852124f259`.

The embedded `88/88` mutation result is retained only as same-implementation
deterministic replay evidence.  No C43 authority pointer or seal was created.

## Blocking findings

1. **HIGH — no genuinely independent implementation.**  The import guard
   rejects a direct producer import, but the C43-specific reconstruction is
   substantially isomorphic to the producer and shares the same C41, pilot,
   and planner helpers.  Adaptive traversal, reflection, owner/incidence,
   parent conservation, and census logic can therefore reproduce a common
   implementation error.
2. **HIGH — a visible PASS object can survive a failed publication tail.**
   The final audit directory is renamed into place before parent-directory
   fsync, final identity/inventory replay, byte replay, and terminal pointer
   checks.  Failure after the rename leaves the PASS JSON visible while the
   exception path claims `audit_published=false`.
3. **HIGH — terminal source/authority TOCTOU is not closed.**  The parent does
   not re-establish the exact C41/C42 installed-authority state after both cold
   cores, and it can bind a later auditor-source hash that was not the source
   executed by those cold cores.
4. **MEDIUM — receipt path binding follows a symlink before applying
   `O_NOFOLLOW`.**  The lexical frozen receipt path itself is not protected.
5. **MEDIUM — the published audit remains owner-writable.**  The directory and
   file were left at modes `0700` and `0600`.
6. **MEDIUM — the 88 attacks do not cover filesystem/TOCTOU publication
   failures.**  They are reclosed semantic mutations only.
7. **MEDIUM — parts of the final census and descriptor projection are
   hard-coded or observed-byte-derived rather than independently rebuilt.

## Required replacement

A replacement must use a new source and audit token, must not import or execute
the C43 producer, this rejected auditor, or the C43 pilot/planner, and must
derive the owner-eligible subset and all leaf/face/corner/incidence/reflection/
Kraft/census facts independently from frozen lower-level inputs.  It must bind
lexical no-follow paths by retained dirfds, exercise real filesystem and
TOCTOU attacks, reattest source and installed C42 authority after all cold
cores, complete every fallible replay before the no-replace publication commit,
and leave a read-only exact artifact.

Until such a replacement passes hostile review and a later separate authority
transaction commits, the formal state remains:

```text
whole paired coarse cells = 574
whole representatives = 287/862
unresolved = 1,150
remaining representatives = 575
D02 = BLOCKED
CM2 = NO-GO_FOR_CLAIM
```

## Proposed auditor v2 pre-run rejection

A second source was prepared but deliberately stopped before any formal audit:

- source:
  `deliverables/cm2_round306c43_d02_sole_deficit_owner_closure_independent_auditor_v2.py`;
- source SHA-256:
  `ef0607b6d8063dd5368f7b0963dede438eca70d25da4ad95eec8e8486b879abe`;
- reserved, absent token:
  `c43-independent-audit-v2-20260811T121500Z-owner-subset-f1`;
- compile and two-fixture self-test: PASS;
- formal audit: **not run**;
- audit object: **not published**.

The v2 source corrected the v1 rename/commit-state defect: all semantic and
terminal replays precede the no-replace rename, the staged file and directory
are read-only, and any post-rename failure is reported as committed and
replay-required.  It also improved raw C41/C42 inventory replay.

Hostile static review nevertheless retained the blocking independence finding.
The source still imports and executes C41/C39/C40 high-level task and routing
helpers.  Static comparison found 56 of 71 same-named top-level definitions
AST-identical to v1, about 81.7 percent v2 token coverage by v1, 99.9 percent
similarity in the principal ledger reconstructions, and about 86.5 percent
coverage by the producer's seven ledger-generation regions.  The expected
four-class census also keeps the fixed `75,386 / 296 / 1,150 / 76,832`
baseline and applies a delta instead of rebuilding all frozen occurrences.
Dependency verification remains after import for owner-writable sources, and
the 88 coherent mutations still omit symlink/path swaps, dependency races,
rename-success/fsync-failure, close failure, and stdout failure injection.

Therefore v2 is also `REJECTED_PRE_RUN_FOR_AUTHORITY`.  Its source may be kept
as non-authoritative design evidence, but it must not be formally run, frozen,
or used to authorize C43.  A future clean-room implementation may share only
low-level exact arithmetic/data codecs; it must independently construct the
tasks, router, restriction ledger, and full 76,832 census and must pin every
dependency before import through retained no-follow directory descriptors.
