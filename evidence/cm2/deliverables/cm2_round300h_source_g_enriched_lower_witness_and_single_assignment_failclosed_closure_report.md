# Round300-H enriched-lower and single-assignment closure

## Result

Round300-H is closed fail-closed with **zero eligible component edges**.
The package exhausts:

- all 144 Round300-D canonical pairs whose witness family is not pure GRAPH;
- all 1,600 Round300-D single-target assignments; and
- the disjointness of the Round300-E/F/G/H pair tranches inside the complete
  111,524-pair Round300-D frontier.

The explicit eligible-component-edge ledger has zero rows.  No DSU, quotient,
maximality, fibre, or global-disposition credit is applied.

## Pair dispositions

The 144 enriched pairs partition exactly as follows:

| disposition | pair count | formal reason |
|---|---:|---|
| GRAPH + TRANS | 56 | The transverse line is an analytic boundary stratum with no adjacent-tube deduplication credit and no pinned included-stratum two-attachment lemma. |
| GRAPH + NEG + POS | 32 | Exact t=0 owner policy and atom cover prove incidence only; no owner child/origin to Round266-root lineage exists. |
| GRAPH + NEG + POS + TRANS | 56 | The same owner-lineage exclusion applies; the transverse witness adds no deduplication or gluing credit. |

The raw bindings are GRAPH 144, TRANS 112, NEG 128, and POS 88.  The 112
transverse lines split evenly between `LOWER_T_FACE` and `UPPER_T_FACE`.
All 88 owner-policy pairs exactly cover the graph-leaf base, but their
Round293 component-edge and same-point-glue credits and Round295-A component
union credits remain zero.

Round300-E (472), Round300-F (264), Round300-G (128), and Round300-H (144)
are pairwise disjoint.  Their union contains 1,008 pairs, leaving 110,516
pure-GRAPH incidence-only pairs.

## Single-target dispositions

The 1,600 single-target rows partition exactly as:

- 192 new Round288 assignments: NEG 116 and POS 76.  Each has a unique target
  assignment but no formal owner-root attachment lineage, hence no edge.
- 1,408 preserved assignments.  Their 1,108 distinct occurrences and 118
  distinct Round266 roots are reopened directly from the sealed Round266
  occurrence frontier; this is existing-provenance reclosure, not a new edge.

Every formal single disposition links to the exact
`source_Round300D_single_row_id` and
`source_Round300D_single_row_sha256`, together with its Round295-A binding
ID/hash and target registry occurrence.

## Independent verification

The verifier never imports, executes, parses, or tokenizes the producer.  It
treats the producer only as inert bytes pinned by SHA-256, independently
reconstructs expected artifacts before opening candidate output, and then
requires exact candidate-byte equality.

The independent audit reopens Round179/182 geometry, Round204/208/220 and
Round245/246/247/248 lineage channels, all selected Round291/293/295-A
bindings, all preserved Round266 occurrences, and prior Round300-C/E/F edge
endpoints.  Every direct-lineage and prior-edge endpoint hit count is zero.

All 61 targeted attacks are rejected:

- 49 semantically mutated and fully re-signed packages; and
- 12 parser/path/independence attacks, including duplicate keys, floats,
  nonfinite values, malformed GZIP, NUL/trailing bytes, symlink/hardlink
  substitution, and producer import/execute/parse.

## Commitments

| table | rows | row IDs SHA-256 | row hashes SHA-256 | rows SHA-256 |
|---|---:|---|---|---|
| enriched pair dispositions | 144 | `1d077d69858a380df2c18923f73f0794a5a06b784ea6867431804bedc624f3cc` | `547baddd341f9177e43550c860b8965eb9ede290e1f8ce66fd488e98273afeaf` | `9dd35a49e9c23e0228522d7a3c97ddaaa139a465e9a65f9cbacba9afada9a3cb` |
| single-target dispositions | 1,600 | `23d05b1483c95be92b397eba7f4413eae03dbec9d0fd3a2e62d6586e8a585e44` | `6cb93443ba7653d8adc8151cccaf40752c99de924f5808e43d59f1e97c8f6e31` | `f1ac5a8c3384bb33f2963ab0de73239834ff4b717bbb69da3621cfef882dc40b` |
| eligible component edges | 0 | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` | `4f53cda18c2baa0c0354bb5f9a3ecbe5ed12ab4d8e11ba873c2f11161202b945` |

The closed result commitment is
`f862df8912bfa762fafe476885eda17b68b1f4f9fcd4d6ff7df1fecd4d718da8`.

