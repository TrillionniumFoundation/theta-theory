# C66-L full-domain rooted-corridor owner decider report v1

Status: `CONSUMPTION_READY_FULL_DOMAIN__1042_OF_1042_EDGES__13103_OF_13103_ATOMS_UNIQUE__ZERO_CREDIT`.

C66 is a separately versioned successor to the frozen C64 candidate. It consumes C64's exact decision bytes for all 911 already-strict edges and applies one new semantic rule only to C64's 131 fail-closed tie edges:

`UNIQUE_ROOTED_CORRIDOR_DESCENT_TOWARD_STRICT_OPEN_ANCHOR_AFTER_SEMANTIC_PATH_TIE`.

## Exact partition

- C64 byte-exact inherited domain: 911 edges and 11,766 atom owners.
- C66 rooted supplement: 131 edges and 1,337 atoms.
- Of the supplement atoms, 992 were already unique under semantic-path order and retain that owner unchanged.
- The remaining 345 two-way semantic-path ties are uniquely resolved by strict descent toward the frozen C56L anchor.
- Full result: 1,042/1,042 edges and 13,103/13,103 atoms have unique owners; query and atom partition overlap are both zero.

## Rooted semantic evidence

For each of the 131 supplemented edges, C66 independently requires:

- both endpoint cells are frozen C56L topological-corridor cells;
- the endpoints have the same component, exact anchor cell, and full anchor binding;
- the anchor is either the original Round140 strict-open adaptive connected cell or its frozen C37 `Jy`-reflected strict-open collar;
- `source_corridor_step_count = target_corridor_step_count + 1`;
- the first frozen source corridor step names the exact target cell, face/seam ID, and glue kind of the C60 edge;
- each tied atom has exactly two minimum-semantic-path winners, one at each endpoint;
- the selected winner is the target occurrence at strictly smaller anchor distance.

The 131 edges divide into 67/64 across the two rooted components and 115 intra-chart / 16 source-seam edges. Source distances range 5–104 and target distances 4–103. Physical occurrence IDs and side labels never participate in the tie-break.

## Security and replay

The candidate binds exact C53, C56L, C60, C63, and C64 source/result/ledger/audit/manifest hashes. Reads require `O_NOFOLLOW`, a regular file with `st_nlink==1`, stable path/file-descriptor identity before and after reading, and exact SHA-256. Candidate and ledger schemas are closed and extra fields fail independent equality checks.

Two complete producer runs were byte-identical, including deterministic gzip ledgers. A cold no-producer verifier independently reconstructs all 13,103 atom rows, 131 rooted evidence rows, and 1,042 edge rows. It passes 42 coherently reclosed semantic attacks plus 8 TOCTOU attacks (50/50 total), including actual symlink, hardlink, truncation, and non-regular-file probes. Runtime and canonical snapshots remain unchanged.

This is consumption-ready but not installed. Formal credit and D02 gate credit remain `0`; CM2 remains `NO-GO_FOR_CLAIM`.
