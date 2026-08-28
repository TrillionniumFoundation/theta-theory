# Round306B1R0 R288 predicate-source inventory/union freeze — exact promotion report

Status:
`PASS_EXACT_ROUND306B1R0_R288_PREDICATE_SOURCE_INVENTORY_AND_UNION_FREEZE__ZERO_THEOREM_CREDIT`.

Round306B1R0 freezes the exact predicate-source-cell inventory and the exact
outer-envelope union inventory for the Round288 atom-occurrence identities.
The independently reconstructed formal package records all remaining cell and
member support gaps explicitly.  Its verification marker grants no theorem,
full-support, maximality, fibre, or global-disposition credit.

## Frozen implementation and formal six-file package

```text
producer_file_sha256=3538e17fd523384d31a2fbf46505ff4ee5bf7ba8f41db14534e55edaa04eabca
producer_file_size=73458
verifier_file_sha256=60ff7e2e65adfd76f097c46068fdd49a1d5874916f030be238658835396f5ecb
verifier_file_size=119762

attack_file_sha256=a34f51d8371dbc48b444fc6eb9a1e677b496a5ed447505b04e07e61b6d64fa19
cell_file_sha256=19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96
member_file_sha256=4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7
gap_file_sha256=c6b1de08fc62e39d5c5cfc2d98ba5b558d467e1592cc101c19ebdbc9fab66c56
result_file_sha256=ca66501d42894dce364ff905045ae69f67cf52c9142ba8f7b45973f857966f04
verification_file_sha256=2242732077165e085f6f2e50f2d061a532a3b43d9e9bc0efc17afac3d45df040

attack_object_self_sha256=aa0c78e10aad22cf7b719ed41f4e7439381ab8fc9a2974eb01aefb4c3c51c76e
result_object_self_sha256=ad2454ded68ffdcd4b37d39a43b60220ca4fbad780197e0443bcf4ce1904a46c
verification_object_self_sha256=3cb6c976f411a4ad05369434dab8d60ff98fea7204fddd8dd628d6e67c644ea8
attack_rows_sha256=136a092241293ed54dc7f67de01fad5a8af5220537f85169812607c3d638e462
```

The verifier treated the producer as inert SHA-pinned bytes: it did not
import, execute, parse, or tokenize it.  Its independent reconstruction was
bound to an exact 27-file source snapshot, including the sealed Round306B0
manifest (`9846b36d28bb1507b273de3e613a5ecd5ac6515258042bf8b91b89e0c156b269`).

## Exact identity and predicate-source census

```text
Round288_atom_identities=332016
  existing_Round208=36040
  exact_Round204_aliases=640
  new_Round288_members=295336

predicate_source_side_rows=332020
  existing_Round208=36040
  exact_Round204_aliases=640
  predicate_source_cells=295340
  extra_W_tail_split_cells_not_identities=4

predicate_source_cells=295340
member_union_rows=295336
cell_gap_rows=295340
member_gap_rows=295336
total_gap_rows=590676
```

The source-cell round histogram closes exactly:

| Source round | Predicate-source cells |
| --- | ---: |
| Round269 | 187,128 |
| Round270 | 37,712 |
| Round271 | 70,356 |
| Round272 | 144 |
| **Total** | **295,340** |

The atom-identity source multiplicity histogram is exact:

| Source multiplicity | Atom identities |
| --- | ---: |
| 1 | 295,332 |
| 2 | 4 |
| **Total** | **295,336** |

The four multiplicity-two identities are the Round271 artificial W-tail
parent-normalization cases.  They account for the four-row difference between
`332,020` source-side rows and `332,016` identities; they are not additional
identities.

The reconstructed Round294 member set equals the sealed Round306B0 member
set for this tranche, and every member has an exact outer-envelope union
inventory.  This is an inventory statement only.  The source-free-interval
predicate theorem and the full-support-union theorem are both explicitly
incomplete.

## Exact ledger commitments

| Ledger | Rows | File SHA-256 | Ledger SHA-256 | Rows SHA-256 | Row IDs SHA-256 | Row hashes SHA-256 |
| --- | ---: | --- | --- | --- | --- | --- |
| Predicate-source cell | 295,340 | `19d13d93fc02296f673ca18cc2edbd96174985f7be8fb0e03694582b188b0f96` | `f473914afa7d9dab1598a3259be8a4ec2b08ab7992d7a7039cff8bde5f19512b` | `b89220807eef10bc8412be19c5037ea75fa3c6fdf4321c27938afec0c68c9246` | `b3fb242c0c130122b0e2e7e0c1e38f866f214e332aea93dc6ce03e705201fe9a` | `33ce0c07cf6eeeb7e8d3d10129dad7652aec94e3d30d18d807499380b35f279d` |
| Member outer-envelope union | 295,336 | `4b3633782e4514f598cb9cce19930ba31616f7d42aab002df4f77f9b4601ddf7` | `28c6e7944f440f9fee06f9ade150de2566a3aaa85b40c49d63e3721ec4a4c4c5` | `6665fc8e72824fba7dbd1d1b7462ae419bb31c25149037da3183d74569b62a3d` | `6c136186cd30608304293cc91185615ba6bec6418cb2c43a48ac833055c69bfe` | `d106b9e68817aa9504ec176be9c679f2e4fd29948c3614f7c109030a893f289f` |
| Explicit support gap | 590,676 | `c6b1de08fc62e39d5c5cfc2d98ba5b558d467e1592cc101c19ebdbc9fab66c56` | `6a61506040c6f48236d8f35ee393f3a1d08dc36dbbcfd5a6d58b9290ef1e8904` | `c6bc641ea84b5a25ed851b0d13cef3b8694fcf4224b59868e641a3339496cf3d` | `98aca1023d164e131c4755b0f35c777f3a984c8ffac6b58aaf1640bddb2dfdba` | `713e8415b88299f6db95446574f160b864f99a93ef8b12b14c8176cd12904df7` |

Each formal ledger is an exact, complete single gzip member.  The verifier
requires physical EOF after that member, rejects extra members and trailing
bytes, enforces the independently derived decompressed wire size, and bounds
the retained row token.  All three formal gzip streams pass integrity checks;
their common header is `1f8b08000000000002ff`, encoding `mtime=0` with no
stored filename.

## Independent production, admission, and promotion

| Run | Artifact or mode | Outcome | Elapsed | Maximum RSS |
| --- | --- | --- | ---: | ---: |
| Producer A | private candidate `seed3061101` | exit 0 | `8:53.08` | 8,072,884 KiB |
| Producer B | private candidate `seed3061999` | exit 0 | `8:18.58` | 8,077,368 KiB |
| Pre-fix admission | independent verifier; candidate remained unopened | fail-closed before candidate admission | approximately `2:07` | not asserted |
| Final exact admission | independent final verifier | exit 0 | `8:16.58` | 8,090,700 KiB |
| Formal promotion | independent final verifier with promotion enabled | exit 0 | `9:12.30` | 8,088,608 KiB |

The two private four-file candidates are byte-for-byte identical, and the
four promoted candidate payloads are byte-for-byte identical to them.  The
failed pre-fix admission exposed a streaming-parser boundary defect: a legal
comma at the end of a read buffer was mistaken for a trailing comma.  It
failed before the private candidate was opened and wrote no formal file.  The
parser was corrected, boundary regressions were added, and only the final
verifier hash reported above was used by the formal marker.

The seed labels, elapsed times, and maximum-RSS figures in this table are
execution records.  They are not recomputable from the six-file formal
package alone.  A later post-promotion read-only audit rechecked the frozen
hashes, contracts, lightweight tests, and publication facts; it did not rerun
the heavy reconstruction.  Filesystem mtime and ctime are diagnostic only and
are not authenticated evidence of execution order or elapsed time.

## Attack and exact-wire boundary

The formal defense-in-depth bundle rejects all `46 / 46` recorded attacks:

```text
semantic_contract_units=20/20
filesystem_transaction_attacks=2/2
wire_attacks=24/24
  strict_raw_single_gzip_member_attacks=15/15
  strict_JSON_wire_grammar_attacks=9/9
```

The raw-stream metadata records `fixture_count=20` and, as its exact reported
subcounts, `raw_gzip_fixture_count=19`, `positive_fixture_count=4`,
`negative_fixture_count=15`, `negative_fixture_rejected_count=15`,
`independent_ledger_wire_size_positive_fixture_count=1`, and
`giant_unclosed_row_negative_fixture_count=1`.  Raw validation precedes JSON
parsing, the exact decompressed size is mandatory, and the maximum retained
decompressed chunk is 1,048,576 bytes.  The suite includes second-member,
trailing-byte, CRC/ISIZE, truncation, chunk-boundary, size-cap, duplicate-key,
numeric, comma-grammar, and unclosed-token cases.  These are verifier and
transaction defenses; they do not constitute a support or maximality theorem.

## Atomic publication boundary

The formal publication order is exactly:

```text
attack -> cell -> member -> gap -> result -> verification
```

Publication uses no-clobber `renameat2(RENAME_NOREPLACE)`, exact-prefix
recovery, and fsync of both stage and output directories after every rename.
The verification object is the sole final package marker, and marker validity
requires the complete marker-bound six-file transaction.  All six formal
files currently have mode `0600` and link count `1`; no Round306B1R0 promotion
stage remains.  The marker explicitly grants no theorem credit.

## Exact credit boundary and next step

```text
outer_envelope_union_inventory_frozen=true
source_free_interval_predicate_theorem_complete=false
member_full_support_union_theorem_complete=false
cell_gap_count=295340
member_gap_count=295336

full_support_credit: 0 -> 0
maximality_credit: 0 -> 0
fibre_credit: 0 -> 0
global_disposition_credit: 0 -> 0
D02_status=BLOCKED
CM2_status=NO-GO_FOR_CLAIM
```

Official key remains metadata only and must not be used as an exclusion
filter.  The next strict-critical-path work is to seal Round306B1G's graph
source inventory/join freeze, then combine the B1G and B1R inventories with
the B1A support-gap atlas in Round306B2.  B2 must prove or fail-closed exclude
every remaining support/transition channel and exhaust the full Round306B0
cross-component denominator before any maximality credit can change from
zero.
