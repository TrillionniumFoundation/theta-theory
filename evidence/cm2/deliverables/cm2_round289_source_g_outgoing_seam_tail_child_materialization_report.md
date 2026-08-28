# CM2 Round289 — outgoing-seam tail child materialization

Status: **PASS INDEPENDENT — cacheless upstream reconstruction confirms
analytic residual zero; all global credit remains zero**.

## Frozen inputs and scope

Round289 pins the frozen Round268 true-seam patch universe, the Round275
reverse-rechart regions, the Round280 patch-channel incidence ledger, the
Round282 residual normal-corridor cells, and every Round283 analytic probe
artifact.  It does not use Round287 or Round288.

The exact input census is:

- 152 true-seam patches in the complete frozen universe;
- 24 patches with outgoing-seam analytic tails;
- 40 directed tail endpoints;
- 48 guard-channel incidences;
- eight endpoints with two distinct guard channels;
- 540 disjoint Round282 rational residual cells;
- 6,596 Round275 region hits;
- 9,528 Round275-region/residual-cell incidences.

All upstream file hashes are checked before construction.

## Exact half-open analytic materialization

The producer materializes 64 explicit children:

- 40 regular `p`-graph children;
- 24 strict-zero-absence children;
- 16 logical splits at the exact boundary `s=0`.

For every one of the 16 split guards, the graph child owns `s=0` and the
absence child excludes it.  Thus each `s=0` boundary is owned exactly once.
Every regular graph also has one frozen zero-set owner: the sign corridor
meeting the lower `p` face owns `F=0`, where
`F = outgoing_normal_x² - outgoing_normal_y²`.

The 40 graph children have both strict sign corridors.  Each of the 24
absence children has its unique strict same-sign corridor.  The resulting
104 complete sign corridors are all nonempty and connect over the entire
analytic seam-to-Round275 gap.

The eight two-guard endpoints remain distinct by frozen source-guard ID.
Children that geometrically overlap across different return branches remain
separate analytic channels; such overlap is explicitly not an occurrence
identity.

## Round275 incidence and signature binding

Every one of the 9,528 positive-area region/cell overlaps maps to exactly one
half-open child.  The disposition is:

- 9,240 actual same-sign seam incidences;
- 288 opposite-sign cells separated from the seam by a regular outgoing
  graph.

The corresponding unique endpoint-region census is:

- 6,500 actual incident Round275 regions;
- 96 graph-separated Round275 regions;
- 6,596 total hits, with the actual and separated sets disjoint.

The sign-refined relation census is:

- 4,652 actual positive relations;
- 4,588 actual negative relations;
- 144 separated positive relations;
- 144 separated negative relations.

Every sign corridor stores its actual Round275 region IDs and relation IDs.
Each signature binding contains the complete ten-field return-signature
object, its SHA256 digest, and the exact bound region/relation ID lists.
There are 104 complete signature bindings.  No signature hash is used as an
occurrence or component equivalence.

All conserved totals close exactly:

- patches: 24;
- directed endpoints: 40;
- guard channels: 48;
- residual cells: 540;
- region hits: 6,596;
- region/cell incidences: 9,528;
- analytic residual endpoints: 0;
- analytic residual patches: 0.

## Independent cacheless verification

The independent verifier does not import or execute the Round289 producer.
It reconstructs the expected ledger solely from the pinned Round268,
Round275, Round280, Round282, and Round283 artifacts, using exact
`fractions.Fraction` arithmetic.  Only after rebuilding the full expected
ledger does it read and compare the candidate Round289 bytes.

The reconstruction confirms:

- 24 patches, 40 directed endpoints, 48 guard channels, and all eight
  two-guard endpoints;
- 540 disjoint residual rational cells;
- 64 half-open children (`40` graph + `24` absence);
- all 16 exact `s=0` splits, with one and only one owner apiece;
- 104 connected sign corridors and 104 complete ten-field bindings;
- 6,596 unique region hits and 9,528 region/cell relations;
- 6,500 actual incident regions plus 96 graph-separated regions;
- 9,240 actual relations plus 288 graph-separated relations;
- analytic residual `0`.

Both independent reconstruction seeds (`289071`, `289929`) produce identical
expected ledgers.  Full verifier executions under
`PYTHONHASHSEED=289071/289929` are byte-identical with SHA256
`3cd242981e64007e22dccc8deee43418be32a1841bb75de96c4871c89dda691f`.
All 19 re-signed directed attacks are rejected, including split-owner,
two-guard collapse, disposition, region/cell identity, complete signature,
cross-reference, residual, credit-promotion, `Jx/Jy`, and false-CM2 attacks.

## Strict non-promotion

Round289 therefore grants:

- expanded-occurrence credit: 0;
- seam-component-edge credit: 0;
- component-union credit: 0;
- maximality credit: 0;
- exact-key-fibre credit: 0;
- global-disposition credit: 0;
- `Jx/Jy` same-point glue credit: 0.

The strict baseline remains quotient 63,224; expanded occurrences 126,468;
maximality 0/63,224; fibres 0/116; global dispositions 0/224,580; Gate5
10/18; D02 blocked; CM2 `NO-GO_FOR_CLAIM`.

The analytic child-materialization gate is now independently closed.  No
seam DSU edge may nevertheless be emitted until the two directed sides of
every true-seam patch are bound to frozen physical occurrence identities.

## Artifacts

- producer:
  `cm2_round289_source_g_outgoing_seam_tail_child_materialization.py`;
- complete ledger:
  `cm2_round289_source_g_outgoing_seam_tail_child_materialization_ledger.json.gz`;
- result:
  `cm2_round289_source_g_outgoing_seam_tail_child_materialization_result.json`;
- independent verifier:
  `cm2_round289_source_g_outgoing_seam_tail_child_materialization_verifier.py`;
- verification:
  `cm2_round289_source_g_outgoing_seam_tail_child_materialization_verification.json`;
- cold replay:
  `cm2_round289_source_g_outgoing_seam_tail_child_materialization_cold_replay.md`.
