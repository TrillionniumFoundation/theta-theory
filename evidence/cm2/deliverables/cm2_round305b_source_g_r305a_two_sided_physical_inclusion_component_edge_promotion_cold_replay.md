# Round305B exact cold-replay record

Verdict: `PASS`.

The final producer replays, independent reconstruction, candidate admission,
formal promotion, isolated replay, dual-seed comparison, and post-publication
audit all exited zero.  The record was made from the workspace root on
`2026-08-01` with CPython `3.12.3`, python-flint `0.9.0`, effective Arb
precision `768` bits, and zlib `1.3`.

## Frozen pins

```text
producer_file_sha256=bf2c451b782b2e9ecf7fe9b6b2eaef50e06b9e5499b47579d815665fb8cd914b
verifier_file_sha256=39e2514d7617bd7e638cf2739dcc40bca3be356802654800499f5065bad29bf9
wire_spec_file_sha256=8cd6cbcd936875885b76fe501f76bf949e81233c07d75f715c003beb021ef573
wire_contract_fixture_file_sha256=c2695472d522f1a24a2b8b7bbea0dff6e2c932b5dc63f154b27c6887b02e3f02

physical_file_sha256=629b8501e73c1e7bec9a9e21b1a27a4ca6021f9574c79caf83910ec25f3f95fb
anchor_file_sha256=491a696e582bce2c1fe57692e62caf461073812adec953a1bf46d8d7da2423df
closure_contact_file_sha256=19a25d6b462eb13522ed285cf447421410c5a4958642d59106c4cc1dcb58d0bd
owner_locus_file_sha256=9cf42df2be1994a5669c52732434a9823cef7c1532ea86175c8e8996b44ce690
canonical_component_edge_file_sha256=cf56d9b57cd972a2a3272ea465f83f6fadbc3c7ed6962cb70809f19e44addb27
result_file_sha256=fcc18e0f0c2b05ca06c0c075521e50f00d5fe18bb1f39d853157f5c63cca3932
result_object_sha256=263292b6c816b1b50673520c64da7cf88e1c474c6eee1b80985779e18edbf7cb

attack_suite_file_sha256=b52c9c38ed262497769016602519fbf88f4601405f836c2bae2d7541a1af6735
attack_suite_object_sha256=2fbc7b60a84bdec8be4ad98f691b2b78e73b93cfbf97b014fa93182feb0ed51f
attack_rows_sha256=abac2d8a9df7afee283b5b72973f688179b08b694147781c774e61cfb7710230
verification_file_sha256=4b3307d480b56904a03b0820de65e283b57907da990b60dd6dac1de4e59f1dc9
verification_object_sha256=e4ab96e6614b4895631b068b479c04800266c0f8446cd5e7298d6d895fb5e9c5
```

The producer and verifier hashes were unchanged throughout every final
admitted run.  The normative wire files and the six candidate file pins were
also unchanged before and after promotion and replay.

## Producer complete no-write replay

```bash
env PYTHONHASHSEED=305611 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion.py \
  --no-write
```

Observed:

```text
exit=0
status=PASS_FULL_ROUND305B_ZERO_CREDIT_CANDIDATE_NO_WRITE_REBUILD__INDEPENDENT_VERIFIER_REQUIRED__ZERO_OFFICIALLY_ADMITTED_CREDIT
rows=1024/2048/3536/2696/8
all_1024_rows_satisfy_G0_G5=true
producer_source_sha256=bf2c451b782b2e9ecf7fe9b6b2eaef50e06b9e5499b47579d815665fb8cd914b
formal_DSU_rank_reduction_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
```

No candidate or formal deliverable was written.

## Explicit producer dual-seed stages

Stage A was created with:

```bash
env PYTHONHASHSEED=305701 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion.py \
  --private-stage .cm2-r305b-private-parent-CD4IbTgA/candidate
```

Observed: `exit=0`; exact directory mode `0700`; exactly six regular files,
each mode `0600`; no manifest and no formal write.  Timing was not captured for
this run.

Stage B was created with:

```bash
/usr/bin/time -f \
  'SEED_B_ELAPSED=%e SEED_B_USER=%U SEED_B_SYS=%S SEED_B_MAXRSS_KB=%M SEED_B_EXIT=%x' \
  env PYTHONHASHSEED=305997 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion.py \
  --private-stage .cm2-r305b-seed-b-parent-ZzqAo0aB/candidate
```

Observed:

```text
SEED_B_EXIT=0
SEED_B_ELAPSED=389.76
SEED_B_USER=326.32
SEED_B_SYS=1.93
SEED_B_MAXRSS_KB=248832
rows=1024/2048/3536/2696/8
```

The six files in stages A and B were byte-identical and had the exact frozen
file hashes above.  Thus the effective, explicitly selected hash seeds
`305701` and `305997` do not affect candidate bytes.

## Independent no-write reconstruction

```bash
env PYTHONHASHSEED=306109 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion_verifier.py \
  --no-write-reconstruction
```

Observed:

```text
exit=0
status=PASS_INDEPENDENT_CACHELESS_NO_WRITE_ROUND305B_RECONSTRUCTION
expected_candidate_file_sha256s=exactly the six frozen candidate hashes
result_object_sha256=263292b6c816b1b50673520c64da7cf88e1c474c6eee1b80985779e18edbf7cb
G0_G5_direct_witness_rows=1024
anchor_count=2048
closure_contact_count=3536
owner_locus_count=2696
canonical_component_edge_count=8
candidate_outputs_opened=false
candidate_outputs_written_or_replaced=false
candidate_producer_imported_or_executed=false
formal_DSU_rank_reduction_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
```

The verifier executed six pinned formal-geometry sources through verified
source-byte compile/exec, read or wrote no project-local bytecode cache, and
reported effective Arb precision `768` bits.

## Candidate admission without promotion

```bash
env PYTHONHASHSEED=306101 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion_verifier.py \
  --candidate-dir .cm2-r305b-private-parent-CD4IbTgA/candidate
```

Observed:

```text
exit=0
status=PASS_EXACT_ROUND305B_PRIVATE_CANDIDATE_ADMISSION__VERIFICATION_COMMIT_MARKER_NOT_PUBLISHED__ZERO_FORMAL_CREDIT
attack_suite_file_sha256=b52c9c38ed262497769016602519fbf88f4601405f836c2bae2d7541a1af6735
verification_file_sha256=4b3307d480b56904a03b0820de65e283b57907da990b60dd6dac1de4e59f1dc9
formal_deliverables_written=false
officially_admitted_physical_witness_credit=0
officially_admitted_anchor_binding_credit=0
officially_admitted_component_edge_credit=0
```

This demonstrates the sole-marker boundary: exact admission and a complete
99/99 attack run do not grant formal credit without the published verification
marker.

## Formal independent promotion

```bash
env PYTHONHASHSEED=306211 \
  .venv-cm2/bin/python -B \
  deliverables/cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion_verifier.py \
  --candidate-dir .cm2-r305b-private-parent-CD4IbTgA/candidate \
  --promote
```

Observed:

```text
exit=0
status=PASS_EXACT_CACHELESS_ROUND305B_TWO_SIDED_PHYSICAL_INCLUSION_COMPONENT_EDGE_PROMOTION
binding_mode=EXACT_FORMAL_CANDIDATE
attack_count=99
rejected_count=99
formal_Round305B_promotion_permitted=true
officially_admitted_physical_witness_credit=1024
officially_admitted_anchor_binding_credit=2048
officially_admitted_component_edge_credit=8
formal_DSU_rank_reduction_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
```

The exact commit order was attack, physical, anchor, closure contact, owner
locus, canonical edge, result, and verification.  The first mtime was
`2026-08-01 09:35:58.826064994 +0800` and the verification marker mtime was
`2026-08-01 09:35:58.912490389 +0800`.  No orphan formal stage remained.

## Isolated independent admission replay

The following command used `-I`.  Isolated mode implies `-E`, so the displayed
`PYTHONHASHSEED` environment assignment was ignored.  This run is evidence for
isolated replay only and is not counted as named-seed evidence.

```bash
/usr/bin/time -f \
  'COLD_VERIFY_ELAPSED=%e COLD_VERIFY_USER=%U COLD_VERIFY_SYS=%S COLD_VERIFY_MAXRSS_KB=%M COLD_VERIFY_EXIT=%x' \
  env PYTHONHASHSEED=905701 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion_verifier.py \
  --candidate-dir .cm2-r305b-private-parent-CD4IbTgA/candidate
```

Observed:

```text
COLD_VERIFY_EXIT=0
COLD_VERIFY_ELAPSED=341.60
COLD_VERIFY_USER=253.95
COLD_VERIFY_SYS=2.08
COLD_VERIFY_MAXRSS_KB=336704
attack_suite_file_sha256=b52c9c38ed262497769016602519fbf88f4601405f836c2bae2d7541a1af6735
verification_file_sha256=4b3307d480b56904a03b0820de65e283b57907da990b60dd6dac1de4e59f1dc9
formal_deliverables_written=false
```

The independently rebuilt attack and verification bytes exactly equal the
already promoted formal files.

## Isolated producer replay

This additional `-I` producer run likewise receives no named-seed claim:

```bash
/usr/bin/time -f \
  'COLD_PRODUCER_ELAPSED=%e COLD_PRODUCER_USER=%U COLD_PRODUCER_SYS=%S COLD_PRODUCER_MAXRSS_KB=%M COLD_PRODUCER_EXIT=%x' \
  env PYTHONHASHSEED=305997 \
  .venv-cm2/bin/python -B -I \
  deliverables/cm2_round305b_source_g_r305a_two_sided_physical_inclusion_component_edge_promotion.py \
  --private-stage .cm2-r305b-cold-parent-STakjq4J/candidate
```

Observed:

```text
COLD_PRODUCER_EXIT=0
COLD_PRODUCER_ELAPSED=394.22
COLD_PRODUCER_USER=324.39
COLD_PRODUCER_SYS=1.82
COLD_PRODUCER_MAXRSS_KB=247052
rows=1024/2048/3536/2696/8
```

Its six files were byte-identical to both explicitly seeded stages and the
formal candidate files.

## Pre-seal rejected diagnostics

Two strict checks intentionally stopped non-admitted verifier builds before
formal publication:

1. an owner histogram with integer Python mapping keys was rejected as
   non-canonical wire and normalized to string keys;
2. a full recursive row diff found that `256 / 1,024` physical rows used an
   older R275 t-bound in one G5 whole-support replay field, while the normative
   candidate used the required 512-bit outward square-root enclosure from the
   exact R292 z-box.

The second diagnostic had identical witness IDs and differed at exactly one
semantic leaf per affected row plus dependent hashes.  The verifier was fixed
to reconstruct the normative enclosure; final independent no-write and
candidate admission then matched all six candidate bytes.  No diagnostic
ledger, result, attack, or verification was published or granted credit.

## Final byte, gzip, JSON, and manifest checks

The two explicitly seeded stages, the isolated stage, and the formal candidate
files passed all `18` pairwise `cmp` checks.  All five gzip ledgers passed
`gzip -tv`.  Post-publication audit recomputed all `9,312` row self-hashes,
five complete ledger closures, the result self-hash, the 99-row attack closure,
and the verification self-hash.  The actual six file hashes equal both the
attack baseline and verification candidate map.

The external `14`-member SHA-256 manifest passed `sha256sum -c` from the
deliverables directory.  It includes the producer, both normative wire files,
five ledgers, result, verifier, attack suite, verification, report, and this
cold-replay record.  It excludes itself and has no self-reference cycle.

All three private replay parent directories were deleted after exact
comparison.  They were never manifest, downstream, or credit inputs.  The
formal deliverables remain ordinary single-link files; no formal orphan stage
exists.

## Final credit boundary

Round305B formally grants only:

```text
officially_admitted_physical_witness_credit=1024
officially_admitted_anchor_binding_credit=2048
officially_admitted_component_edge_credit=8
```

It grants zero DSU-rank reduction, maximality, fibre, global-disposition,
official-key merge, occurrence-identity collapse, D4 transfer, and owner
sidecar credit.  No fresh DSU rebuild has occurred.  D02 remains `BLOCKED` and
unconditional CM2 remains `NO-GO_FOR_CLAIM`.
