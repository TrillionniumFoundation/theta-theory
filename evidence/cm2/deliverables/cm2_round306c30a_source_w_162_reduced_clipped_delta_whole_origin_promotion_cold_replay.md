# C30a Cold Replay

- Locked runtime: CPython 3.12.3, `python-flint` 0.9.0, FLINT 3.6.0 / release 30600, x86_64 glibc 2.39.
- The sealed wheel SHA256 is `376b88cacd30612479e839ffdba887599d3f9c8c0e214852bf80bb2b194e4d76`; installation is hash-required by the frozen requirements file.
- Producer seed `30630071`: 1,416.27 seconds; peak RSS 281,488 KiB.
- Scrubbed cold producer seed `30630929`: 1,431.86 seconds; peak RSS 284,188 KiB.
- Both producer runs emitted all four files byte-identically.
- Independent reconstruction: 12,888 cell rows, 160 excluded whole-origin rows, and two inherited-H hold rows; 13,050 rows total; 1,427.36 seconds; peak RSS 284,324 KiB.
- The independent verifier emitted one canonical JSON document on stdout. A syscall trace observed one stdout write, 50 stderr writes, and zero candidate/deliverable writes; trace SHA256 is `c0bf42f3f00ea7a95616b6186ebd2f15fff6fb449b7419df56587aadf1dbf3b6`.
- Nine coherent, fully reclosed attacks were rejected. The deepest attack reordered the whole-origin ledger and rebound all file, sequence, descriptor, and result hashes, forcing a full independent source reconstruction. The suite took 1,191.86 seconds with peak RSS 284,476 KiB.

## Fail-closed correction history

The first full producer attempted the proposed 162-origin promotion. It correctly stopped after 973.15 seconds at `W:N:04.00.10101011`: the inherited Round180 partition contains four `MIXED` outgoing-H terminals with a positive-measure prefix-stage-one matching side. Its symmetric partner `W:S:H.04.00.10101011` has the same obstruction.

The theorem was narrowed, not the checks. The sealed result promotes exactly 160 origins, retains those two origins at zero exclusion credit, and changes the Source-W unresolved tail from 252 to 92. The failed overclaim candidate is preserved under `.cm2-runtime/candidates/c30a-failed-162-overclaim-seed30630071` for audit history.
