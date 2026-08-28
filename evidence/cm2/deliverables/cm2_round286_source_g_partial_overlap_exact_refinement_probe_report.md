# CM2 Round286 — partial-overlap exact refinement probe

Status: **PASS PROBE — ZERO CREDIT**

The 2,184 genuine partial positive-volume overlap regions isolated by
Round284 were refined against all matching frozen Round279 atom boundaries.
Every refinement uses exact rational axis-aligned cuts, preserves the complete
Round275 region, and assigns each output cell either zero or one existing atom
owner.  No occurrence identity is issued by this probe.

Results:

- 2,184 input partial-overlap regions;
- 7,616 pairwise interior-disjoint exact refinement cells;
- 5,700 cells lie in exactly one frozen atom support and are alias-subcell
  candidates;
- 1,916 cells lie in no frozen atom support and are new-disjoint subcell
  candidates;
- multi-atom occupancy cells: 0;
- 960 input regions are fully covered by multiple uniquely owned atom
  subcells;
- 1,224 input regions retain one or more uncovered new subcells.

For every input region, the refinement cells reproduce its exact rational
coordinate volume with no gap or positive-volume overlap.  Cells belonging to
one connected Round275 region retain their internal component-frontier
relation; the refinement does not split connectivity merely because it
separates occurrence-alias from new-disjoint support.

Seeds `286071` and `286929` reproduce both the result and deterministic gzip
ledger byte-for-byte.  The formal occurrence count, DSU quotient, maximality,
fibres, global dispositions, and `Jx/Jy` glue remain unchanged.

## Independent verification

The standalone Round286 verifier does not import or execute the producer.  It
treats the producer only as pinned inert bytes, reloads the frozen
Round275/Round279/Round280/Round284 inputs, and independently reconstructs all
2,184 partial regions using `fractions.Fraction`.

The independent reconstruction found:

- 5,572 positive region/atom clips from 456 referenced frozen atoms;
- 7,616 exact cells with the same complete row digest
  `ef4529302d5a072b04133abb433ee4676acd4e8867a360fd09e05e28053917c6`;
- 17,604 exact pairwise interior-disjointness comparisons;
- 5,700 uniquely atom-owned alias candidates and 1,916 uncovered new
  candidates;
- zero multi-atom cells;
- exact volume cover for every one of the 2,184 parent regions;
- byte-identical verification output under external seeds `286071` and
  `286929`;
- 13/13 directed attacks rejected, including deletion, duplication, bound,
  owner, classification, volume, input-pin, row-hash, ledger-hash,
  ledger-file-digest, result-object-digest, and premature-credit attacks.

Independent verifier object digest:
`2f5d25fcb1f93f7e4791e7eb5d1baafd524ac7daaffa1c95b30c0f3308e5eb29`.

The next safe step is to combine this exact cell ledger with the completed
Round283 outgoing-seam arrangement, then close the Round285 endpoint-pairing
contract before issuing any occurrence IDs or any of the 152 same-point seam
edges.
