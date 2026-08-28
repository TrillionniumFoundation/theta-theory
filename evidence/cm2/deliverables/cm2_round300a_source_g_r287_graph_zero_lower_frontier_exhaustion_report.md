# CM2 Round300-A — R287 graph-zero lower-frontier exhaustion

Status: `PASS_INDEPENDENT_CACHELESS_ROUND300A_FAIL_CLOSED_FRONTIER_EXHAUSTION__ZERO_COMPONENT_EDGE_CREDIT`

## Outcome

Round300-A independently reconstructs and exhausts the tentative R287
graph-zero frontier, but does **not** promote it as a component-edge set.

The exact accounting is:

| Stage | Count |
|---|---:|
| R287 regular-graph opposite-side source pairs | 3,488 |
| Raw Round294 endpoint cross-products | 6,292 |
| Canonical unordered Round294 occurrence pairs | 3,232 |
| Self pairs | 0 |
| Duplicate source expansions removed by canonicalization | 3,060 |
| Pairs already carrying an explicit R295-A lower graph-sheet witness | 128 |
| Pairs lacking an endpoint-specific common zero-trace witness | 3,104 |

The full Round295-A two-target witness universe was streamed and recommitted:
111,852 witness rows, 111,524 unique endpoint pairs, and 328 duplicate witness
rows.  Its exact intersection with the 3,232-row R287-derived frontier is 128.
All 128 intersecting rows are
`NOMINAL_REGULAR_ZERO_SET_IF_PRESENT / WHOLE_PHYSICAL_SUPPORT /
ROUND182_GRAPH_SHEET_LEAF` witnesses with the exact two-sided graph-sheet
incidence classification.  Round300-A records their provenance but gives them
no duplicate credit.

## Why the 3,232 pairs are not promoted

Each R287 source row consists of the two strict open sides of one continuous
active factor:

```text
U = {f < 0}
V = {f > 0}
```

Their positive-open-support intersection is exactly empty.  A regular graph
`{f = 0}` occurs in the closures of the parent sides, but closure contact is
not an endpoint-specific component edge.

The elementary counterexample is `f=x`: the sets `{x<0}` and `{x>0}` have
overlapping outer boxes and closures meeting on `{x=0}`, while their
intersection is empty and their union is disconnected.

This distinction becomes essential after the R286/R292 refinements.  One
R275 side can map to as many as 11 Round294 occurrence IDs.  A source-level
cross-product therefore includes endpoint subcells that need not approach a
common positive-area part of the zero graph.  Outer-representation overlap,
source-level closure contact, occurrence identity, and a canonical unordered
pair key do not repair that missing incidence proof.

For each of the exact 3,104 unresolved pairs, a future promoting gate must
provide:

1. an endpoint-specific common positive-area zero-trace patch; and
2. a two-sided positive-volume corridor to that patch, or a separately sealed
   gluing lemma with equivalent force.

Until then, every component-edge, DSU-rank, identity-collapse, seam,
maximality, fibre, and global-disposition credit remains zero.

## Ledgers

The deterministic gzip ledger contains two independently closed tables:

- 3,488 source-pair expansion rows, including the normalized Round294
  endpoint sets and all 6,292 raw expansions;
- 3,232 canonical occurrence-pair disposition rows, including complete
  R287 provenance, duplicate accounting, R295-A witness references, and the
  exact 128/3,104 disposition.

Commitments:

```text
producer SHA256
f61dccfb8a20328c80bcfaa3458a10988dae73985a2ba23daa7491f4306f5e65

ledger file SHA256
ddc1a8bc53861afeb93d3569c6efa228f17d86f161db31a39fa9b72458ab8f2d

result file SHA256
b8f7c27f8761f1eb611f8fd57a0e773572f045963560f5d63b44baa1680e7ee4

result self-closure
dbba3aaa96a494144427709c7d908fc816c12cd9f87ff13ec06a818c832d7f98
```

## Independent verification

The verifier treats the producer only as inert bytes fixed by SHA-256.  It
does not import, execute, tokenize, AST-parse, or decode the producer source.
Before opening either candidate artifact it independently:

- rebuilds the 3,488 R275/R287 regular-graph pairs;
- streams and recommits all 46,288 Round294 representation bindings;
- streams and recommits all 431,208 Round294 registry rows;
- reconstructs the complete R275-region-to-Round294-occurrence map;
- streams and recommits all 113,452 Round295-A incidence rows;
- rebuilds the 6,292 raw expansions, 3,232 canonical pairs, 128 prior
  witnesses, and 3,104 exact unresolved obligations; and
- regenerates the expected deterministic gzip ledger and result bytes.

The candidate objects and bytes match the independent reconstruction exactly.
The verifier rejects 25/25 attacks, including 24/24 reclosed semantic attacks
against counts, signs, exclusion semantics, witness provenance, input pins,
and every forbidden credit.

```text
verifier SHA256
b425a9836a474122a99cd76a0f4e81175c65c2f426ad7e38773cce46220c64d5

independent attack-suite file SHA256
59e30957150d30b796edab4afc74267d5c885d3d3caea0d52f3cfd0338b21e80

independent attack-suite self-closure
390a4fc6558d9cee9dc0cb3b024946e5fe4354504dd461107d4fe6f0915617c1

verification file SHA256
e976fc2912c1d902029b8c4c7d4864bd8bb1cb6895bc09c215f2a5ac2400c696

verification self-closure
fed82ab1403e0f496245066b469d686b3126a3588c27459d9b0b53f8b08e7495
```

