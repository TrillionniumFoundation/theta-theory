# Round306B1G0 graph-source inventory/join freeze — exact promotion report

Status:
`PASS_EXACT_ROUND306B1G0_GRAPH_SOURCE_INVENTORY_AND_JOIN_FREEZE__ZERO_THEOREM_CREDIT`.

Round306B1G0 freezes the exact graph, sheet, side, correction, and Round306B0
member-backbinding inventories needed by the later Source-G support proof.  The
independent verifier reconstructed the complete source inventory before it
opened a private candidate, then published the exact candidate bytes under a
verification-last marker.  This is an inventory and source-join freeze only:
it grants no graph-definition, physical-incidence, full-support, maximality,
fibre, or global-disposition credit.

## Frozen implementation and formal nine-file package

```text
producer_file_sha256=97f1d0736a616071dbb0dba3bf533e3fae96091fc6b165395436216bb69c9321
producer_file_size=90721
verifier_file_sha256=47d642bfd90c8f8040a7de97df88788f2295e60b50ad7c72bb8ae2e85d89004b
verifier_file_size=128011

attack_file_sha256=fc7e6fa712638ffd37c7963229d85df69d0ed7ceb219650eda44ae93627f7333
graph_file_sha256=5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0
sheet_file_sha256=041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3
side_file_sha256=d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1
correction_file_sha256=834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a
member_file_sha256=79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b
gap_file_sha256=2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809
result_file_sha256=3f494ebc9f046bfe9f42aef16edeadaece099d7ba7547b11f07484e3f6d81b9e
verification_file_sha256=65b7a01fd82535f357dbb44b8c68a68c86afcbb75b1c1c9b9159b71f9815139a

attack_object_self_sha256=163e7afe7b23f85bc18d040fb21bc3b1823fafe8d1f36701eff93c87467f0feb
result_object_self_sha256=7bb3def1952176cbaf98723a6a2c5126e3c9193efac36a0d9a2c07533e0ec9bd
verification_object_self_sha256=542de6d90a6dcb6cd8775a1caf6fe3c3e62bbae49a10e864a7820ba3d083f700
attack_rows_sha256=f36df3913af61d66e621d4141cfe3c0aafc5eb31d25ff402c6b93c74da96ba99
```

The verifier treated the producer as inert SHA-pinned bytes: it did not
import, execute, parse, or tokenize it.  Its reconstruction was bound to an
exact 22-file source snapshot spanning the sealed Round235, Round236,
Round242, Round245, Round248, Round264, and Round306B0 inputs.  The snapshot
includes the Round306B0 manifest with SHA-256
`9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269`.
All source file sizes and hashes were pinned and the source descriptors were
checked for post-read stability.

The promoted result retains its private zero-credit candidate status and
`candidate_is_formal=false` by design.  It is consumable only inside the
complete marker-bound nine-file transaction; the verification object is the
sole package marker.

## Exact graph, join, and gap census

```text
graphs=38624
graph_sheet_join_rows=38624
graph_side_join_rows=76848
R264_correction_rows=400
distinct_Round306B0_member_backbindings=115456
physical_incidence_rows=115472

graph_definition_gaps=38624
physical_incidence_gaps=115472
total_gap_rows=154096
```

The exact family decomposition is:

| Lineage | Graphs | Sheets | Side rows or references | Physical incidences |
| --- | ---: | ---: | ---: | ---: |
| Round235 / Round248 after Round264 | 38,328 | 38,328 | 76,256 | 114,584 |
| Round236 / Round248 | 32 | 32 | 64 references | 96 |
| Round242 / Round245 | 264 | 264 | 528 | 792 |
| **Total** | **38,624** | **38,624** | **76,848** | **115,472** |

For the Round235 / Round248 family, the pre-correction side inventory is
76,656.  Round264 supplies exactly 400 dispositions:

```text
absent_owner_prunes=184
present_phantom_drops=216
total_Round264_corrections=400
retained_Round235_Round248_sides=76656-400=76256
```

Round236 has 16 partitions producing 32 graphs and 32 sheets.  Its 64 side
references resolve to 48 distinct side members; this distinction explains
why the 115,472 incidence rows bind to 115,456 distinct Round306B0 members.
The graph family histogram is exactly 38,328
`R235_SINGLE_ENDPOINT_GRAPH`, 32 `R236_DOUBLE_ENDPOINT_GRAPH`, and 264
`R242_UNIQUE_TRANSITION_GRAPH` rows.

Every graph has an exact graph-to-sheet join, every retained side reference
has an exact graph-to-side join, and every joined member is backbound to the
sealed Round306B0 universe.  Official key is checked only as post-lineage
metadata consistency; it is not used as a join or routing filter.  These
exact joins do not prove that the graph definition is source-free or that an
inventory incidence is a legal physical incidence.

## Exact ledger commitments

| Ledger | Rows | File SHA-256 | Ledger SHA-256 | Rows SHA-256 | Row IDs SHA-256 | Row hashes SHA-256 |
| --- | ---: | --- | --- | --- | --- | --- |
| Graph-source inventory | 38,624 | `5ac33be2b7639e1d30ae14abd5a7cf4cc6d1cc65fb0730e98616434f08921cb0` | `a684dad14281e44c9dc02a0f825af661ef152f86a436c827fc0b113d25b4d6a0` | `beda6faaf7d3be25075d8f2a7f292cba97f591d6255758b6b16efc141339673f` | `982ee86845f92368cee72b74c52e401eecfb6dd225a4b198910b89ce34a8a7dc` | `7fde3bb652a469eb3b04fe31a80c365d010d914700348954c5d917ac1162dace` |
| Graph-sheet join | 38,624 | `041328aa135a1a67cbbdc8c5d84fe2c1a9bef2231a6cb33668ab05ecd6b227e3` | `3686f3b90a77195dbecd08750707a32f98e07f9fdff5f59d57f09c1178a48fda` | `9238a05af9a97002488576d3648ce06ee750858f156638c314ba2e0a24fe3e1f` | `b36ca314b15b8b8297dfeda9cb4fe37360ff20339e7603a6388ac172cfb87300` | `a3c606a9ba302ced5593d941529946729da5d160a32384ca37060b20011a01f5` |
| Graph-side join | 76,848 | `d79af13182f99cdb2df6d39731e762b0d145baf79772b99be5069669c5b80ee1` | `108bdcbe1c124de15d8f48f82a3cdb7aa545f6f61294be34e3e5b07979d6670e` | `43ee8ffd2b77231c43c0af10198bbcc1f1def12f2e6bfd28f82c66ea26a207b2` | `9e2a2c015372aa22e5f2cfa1f11ae268496831b3118da5bd5087fc6d7f403f53` | `2090d073d45f0097df68a60b36085786de0db51d76219b562734465bbf6daff6` |
| Round264 correction disposition | 400 | `834b687845a156328873888e405793f52a12df9d6286ae07d8a572c6163a361a` | `a4af6f87737028981be9dccae9c2c28236408aa1f112f507418b6e4516eeb671` | `a3df5bc8c8a86ea6958daefa7ec9b99013a04152378e5bcb18991ec4860cac67` | `b3dec2b9ef34fd5ebc3701201593ca90146f6d6150e5b593284a2a974a1d8caf` | `f172394acdc909f6bc58f59fd1f361c4a4c5b00d06b2a8e8369b7638a6e6c592` |
| Round306B0 member backbinding | 115,456 | `79382a6d8c3d086aeb29eff9fcb8653f2a73d85d79aab27e71e72cc8b1165a0b` | `65493ba72be6047b7c1c4ea64045460ad8160ab05440d02204393d3697a4d541` | `35189ef67c69078e44bbd440be37ef870935a8fd67817501ae995cceae383ea6` | `ff6c659209636eec5235a375e8f8ba1cd5bf69c39df6630e6dfaeb95b0945d72` | `88026547b175b4ee968f738fe1276163d364b4482d164dbc2e84377039088eae` |
| Explicit graph/incidence gap | 154,096 | `2ba1903e2ce6d44ee623d0ccaacce973f7327e1e36ba8f97d0ab3865f1ec9809` | `5324319ce7b3f90f67b3e12af6848f851008fd52c7cbd7c8d433cd0652c52f9e` | `d47d29e9eccc04374851cf12a3bc08fbe62837673fe8beb5dd1c9382337ad27b` | `f1c3bf0bb9991f1298a3bc8ce90d55871122ef81b679f32fca21b81087ee1421` | `ca9e836b8ca114ba2843a9196748128b6194adb3bd801bb9a28dfff44d28af35` |

All six ledger streams are exact single gzip members.  Their common ten-byte
header is `1f8b08000000000002ff`, encoding `mtime=0` with no stored filename,
and all six formal streams pass gzip integrity checks.

## Independent production, admission, and promotion

| Run | Artifact or mode | Outcome | Elapsed | Maximum RSS |
| --- | --- | --- | ---: | ---: |
| Producer A | private candidate `seed3063101` | exit 0 | `2:47.25` | 695,692 KiB |
| Producer B | private candidate `seed3063999` | exit 0 | `2:42.86` | 696,172 KiB |
| Bounded-prelude admission | independent verifier; candidate remained unopened | fail-closed | `0:01.93` | 70,084 KiB |
| Final exact admission | independent verifier, seed `3064666` | exit 0 | `3:25.25` | 700,348 KiB |
| Formal promotion | independent verifier, seed `3064777` | exit 0 | `3:33.67` | 695,160 KiB |

The two private seven-file candidates are byte-for-byte identical.  The
seven candidate payloads in the formal package are byte-for-byte identical
to both private candidates.  The failed bounded-prelude attempt stopped
before opening either candidate and wrote no formal object.

Seed labels, elapsed times, maximum-RSS figures, and filesystem timestamps
are execution records, not content-authenticated proof recoverable from a
later manifest.  A post-promotion read-only audit rechecked the formal hashes,
commitments, marker, permissions, and publication facts; it did not rerun the
heavy reconstruction.

## Attack and exact-wire boundary

The formal defense-in-depth bundle rejects all `50 / 50` recorded attacks:

```text
semantic_contract_units=35/35
real_filesystem_transaction_attacks=5/5
strict_wire_grammar_attacks=10/10
reconstruction_attacks=0
```

The semantic rows are contract-unit mutations, the filesystem rows execute
real temporary-directory transaction paths, and the wire rows are strict
grammar mutations.  The suite reports its scope honestly: it contains no
full-source reconstruction attack.  The heavy verifier's source-bound
independent reconstruction and exact candidate equality checks are separate
from these 50 defense-in-depth fixtures.  Neither the attacks nor the
inventory reconstruction constitute a graph-definition, physical-incidence,
support, or maximality theorem.

## Atomic publication boundary

The exact formal publication order is:

```text
attack -> graph -> sheet -> side -> correction -> member -> gap -> result -> verification
```

Publication uses no-clobber `renameat2(RENAME_NOREPLACE)`, exact-prefix
recovery, precise rollback of an owned marker, and fsync of both stage and
output directories after each rename.  Verification is last and is the sole
package marker; downstream consumers must validate the complete marker-bound
nine-file bundle.  All nine transaction files have mode `0600` and link count
`1`, and no Round306B1G0 promotion stage remains.

The transaction model explicitly retains two residual limitations.  A crash
or power loss may leave a recoverable formal prefix without the verification
marker, and hostile same-UID namespace races are not cryptographically
eliminated.  Neither state grants formal credit; recovery and downstream use
remain fail-closed on the complete marker-bound bundle.

## Exact credit boundary and next step

```text
inventory_and_source_joins_frozen=true
source_free_graph_definition_complete=false
physical_incidence_theorem_complete=false

graph_definition_credit: 0 -> 0
physical_incidence_credit: 0 -> 0
full_support_credit: 0 -> 0
maximality_credit: 0 -> 0
fibre_credit: 0 -> 0
global_disposition_credit: 0 -> 0
D02_status=BLOCKED
CM2_status=NO-GO_FOR_CLAIM
```

The next strict-critical-path step is Round306B2: combine this sealed B1G
graph inventory and its 154,096 explicit gaps with the sealed B1R predicate
source/union inventory and the B1A carrier-witness/support-gap atlas.  B2 must
prove or fail-closed exclude every remaining graph-definition, physical-
incidence, carrier, transition, and support channel against the full sealed
Round306B0 denominator.  Until that exhaustion succeeds, maximality and all
downstream credits remain zero.
