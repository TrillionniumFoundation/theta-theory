# Round306B1AF4K2P0 preserved/non-graph authority frontier

Verdict: `PASS_ENGINEERING_FRONTIER`, with `formal_credit=0`.  This package freezes and independently replays the direct-source byte, property-path, row-count, row-order, manifest, and authority-status frontier requested by P1 blocker B06.  It is not normalized full support, a representation-cover theorem, B1A, B2, or CM2 credit.

## Exact replay

- 30 upstream files, exactly 234,258,243 bytes, were opened through a held directory descriptor with `O_NOFOLLOW`, regular-file and `nlink=1` checks.
- Every held file passed two initial full SHA-256 passes and a third full SHA-256 pass after all JSON/table/manifest replay, followed by final path/FD and directory-path revalidation.  File identity includes device, inode, mode, link count, size, `mtime_ns`, and `ctime_ns`.
- 17 exact result property paths yielded 204,162 ordered rows.  Each table has an ordered-list SHA, ordered row-digest-sequence SHA, unordered multiset SHA, and first/last row SHA.
- 67,026 rows carry and pass an upstream per-row SHA closure.  137,136 rows do not; that absence is frozen as a gap, not silently upgraded.
- Each selected canonical row is capped after final canonical encoding at 8,388,608 bytes.
- Independent verifier SHA-256 is recorded by the final package manifest.  It hardcodes the 30-file and 17-table allowlists and does not import the producer.
- All nested contract comparisons that contain numbers or booleans are recursive type-strict comparisons.  The verifier self-test explicitly rejects both `false == 0` credit substitution and `true == 1` count substitution.

## Authority disposition

- `R209`: `BLOCKED_MISSING_AUTHORITY`.  The pinned item is explicitly a nonformal probe with only compact summary hashes; no sealed direct row payload or independent receipt package exists.
- `R230`: row extraction is `ENGINEERING_READY`; semantic/full-support authority remains `BLOCKED_MISSING_AUTHORITY` because the rows grant only local bulk/incidence facts and explicitly zero membership, maximality, fibre, and global credit.
- `R231`: row extraction is `ENGINEERING_READY`; authority remains blocked because no independent verifier/verification/report/cold-replay/manifest package exists in the root, and its selected rows lack per-row SHA closure.
- `R233`: row extraction is `ENGINEERING_READY`; semantic/full-support authority remains blocked and its selected rows lack per-row SHA closure.
- `R235_PRESERVED_NONGRAPH`: row extraction is `ENGINEERING_READY`.  This is the single-endpoint graph-word partition in the preserved/non-graph chain, not a G2 authority.  Sixteen double-endpoint factors remain deferred; semantic/full-support authority is blocked.
- `GATE5_R147`: `ENGINEERING_READY` only as the latest strict frontier receipt.  It records 10/18 satisfied, 8/18 strictly blocked, zero upgrades, and zero complete global 18-field blocks; it is not automatic row-level theorem authority.

## Availability boundary

Whole pinned certificate documents and selected arrays are decoded in memory.  The exact input sizes are frozen and per-row canonical encoding is capped, but this package makes no runtime or RSS bound.  Measured producer replay peak RSS was 636,056 KiB; final type-strict independent cold replay peak RSS was 635,464 KiB.

## Remaining hard gates

R209 needs a sealed row-bearing formal certificate and independent receipt package.  R231 needs its missing independent receipt package.  Every consumed direct row still needs an input-bound semantic theorem certificate, construction-source exhaustion, representation backbinding, incidence/equivalence, and full-support equality.  Therefore normalized full-support, B1A, B2, maximality, and unconditional CM2 credit remain zero.
