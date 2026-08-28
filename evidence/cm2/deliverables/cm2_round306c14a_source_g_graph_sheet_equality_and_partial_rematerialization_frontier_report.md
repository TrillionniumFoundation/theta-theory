# C14a graph-sheet equality and partial rematerialization frontier

C14a splits the 5,264 current graph-to-sheet relations at the exact semantic boundary.

- 832 rows have independently verified set equality between the graph projection and the current full-base/full-patch sheet: 552 R235 source rows, 264 R242 rows, and 16 R235D source rows.
- 4,432 R235 target rows are not equal to their current sheet. Their C10 exact support is a partial-base AST, while the inherited R248 relation is explicitly `OUTER_ENVELOPE_ONLY__NOT_FULL_GRAPH_SUPPORT`.
- Each partial row receives a deterministic proposed exact-sheet natural key, but no member or DSU credit is minted before rematerialization and impact audit.

Verification: independent verifier PASS; 8/8 coherently reclosed attacks rejected; two ordinary seeds and one scrubbed cold replay are byte-identical. Representation pullback, normalized support, B1A, B2, maximality, and CM2 remain zero.
