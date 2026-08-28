# Round305B two-sided physical inclusion and component-edge promotion — exact report

Candidate artifact status:
`PASS_ROUND305B_DIRECT_G0_G5_ZERO_CREDIT_CANDIDATE__PENDING_INDEPENDENT_VERIFICATION__ZERO_OFFICIALLY_ADMITTED_CREDIT`.

Independent promotion status:
`PASS_EXACT_CACHELESS_ROUND305B_TWO_SIDED_PHYSICAL_INCLUSION_COMPONENT_EDGE_PROMOTION`.

Round305B formally admits exactly `1,024` direct physical-witness rows,
`2,048` anchor-binding rows, and `8` canonical component edges.  The `3,536`
closure-contact rows and `2,696` owner-locus rows are published audit sidecars
with zero mathematical credit.  The `1,024` witness rows deduplicate to eight
component edges and are not `1,024` union rows.

The candidate ledgers and result deliberately remain zero-credit objects whose
status says that independent verification is pending.  They were frozen before
admission.  The separately published verification artifact is the sole final
credit marker and records the transition to `1,024 / 2,048 / 8` admitted rows.

Round305B performs no fresh DSU rebuild and grants zero DSU-rank, maximality,
fibre, or global-disposition credit.  The last actually reconstructed quotient
remains Round304's `92,696`-component quotient.  `92,688` is only the
conditional target of a later fresh rebuild if all eight promoted edges reduce
rank.  D02 remains `BLOCKED` and unconditional CM2 remains
`NO-GO_FOR_CLAIM`.

## Frozen source, wire, theorem, and promotion pins

```text
producer_file_sha256=bf2c451b782b2e9ecf7fe9b6b2eaef50e06b9e5499b47579d815665fb8cd914b
verifier_file_sha256=39e2514d7617bd7e638cf2739dcc40bca3be356802654800499f5065bad29bf9
schema_snapshot_sha256=ec5eab1b9aaeb851e8858b76d14ba7142d7db5aa41ea3286297317b105e547e7

wire_spec_id=CM2_ROUND305B_NORMATIVE_WIRE_SPEC_V2
wire_spec_file_sha256=8cd6cbcd936875885b76fe501f76bf949e81233c07d75f715c003beb021ef573
wire_contract_fixture_file_sha256=c2695472d522f1a24a2b8b7bbea0dff6e2c932b5dc63f154b27c6887b02e3f02

relative_limit_lemma_id=CM2_RELATIVE_PHYSICAL_P_TO_RHO_TWO_SIDED_LIMIT_V1
relative_limit_lemma_sha256=f789e796ccec6166ddad6839f1fa760dc0e63b6fb7d38681cef416057e12b234
two_sided_attachment_theorem_id=CM2_STRICT_P_MONOTONE_RECHART_WALL_ZERO_TWO_CLOSURE_LIMIT_V1
two_sided_attachment_theorem_sha256=d0959666a25ac6c0a0e67a2ed7bcc3bc90daded90f197afc097c737cdad87d2c

result_file_sha256=fcc18e0f0c2b05ca06c0c075521e50f00d5fe18bb1f39d853157f5c63cca3932
result_object_sha256=263292b6c816b1b50673520c64da7cf88e1c474c6eee1b80985779e18edbf7cb
attack_suite_file_sha256=b52c9c38ed262497769016602519fbf88f4601405f836c2bae2d7541a1af6735
attack_suite_object_sha256=2fbc7b60a84bdec8be4ad98f691b2b78e73b93cfbf97b014fa93182feb0ed51f
attack_rows_sha256=abac2d8a9df7afee283b5b72973f688179b08b694147781c774e61cfb7710230
verification_file_sha256=4b3307d480b56904a03b0820de65e283b57907da990b60dd6dac1de4e59f1dc9
verification_object_sha256=e4ab96e6614b4895631b068b479c04800266c0f8446cd5e7298d6d895fb5e9c5
```

The result self-hash is an object commitment and intentionally does not commit
its own file SHA-256.  The external manifest closes the result file without a
self-reference cycle.

## Exact ledger census and commitments

| Ledger | Rows | File SHA-256 | Ledger SHA-256 | Rows SHA-256 | Row IDs SHA-256 | Row hashes SHA-256 |
| --- | ---: | --- | --- | --- | --- | --- |
| physical witness | 1,024 | `629b8501e73c1e7bec9a9e21b1a27a4ca6021f9574c79caf83910ec25f3f95fb` | `f26ba6d230c185813d26fd25fc795b512e8ea9b45991ac1823295433e547dce9` | `8b1cd308ccd88e3fbd6e40cc8f2b3c75821d87cc5bbee2a5d023f896c56a3188` | `4ff29ac2eec8d21ddec1ca70304d1e25cd1fc53e58b2135acecd5f5e6f5fc895` | `e5655197de5ec484eae0970fb004b7b44db5e4971905cf641249aa5f5d86efc9` |
| anchor binding | 2,048 | `491a696e582bce2c1fe57692e62caf461073812adec953a1bf46d8d7da2423df` | `d27876749345d5db871764ad1d9011ec15956c3b8783f9c5f1aa4fc57783e285` | `1b2d9861c8d61decd735556657c68bf35186880e03c534ac985bac1843e865a0` | `c880362aceec077126f21d6138c832a15cc0c7e0c280d38371e22cf2d4368f74` | `0fc97990910270f36b644dc9ff3f98f1c9394b3b77bb321b6efc9b85645f96d2` |
| closure contact | 3,536 | `19a25d6b462eb13522ed285cf447421410c5a4958642d59106c4cc1dcb58d0bd` | `5f4bdc4a4b5710dad6b1a77bd94873eb754e144577576d45f5f3f25ca864ffc6` | `13cc4d4ed08aca361a6578ad3622ac4fec35c9c1a7620652538c3d9e5f8ed3a9` | `84819bb28a798646476134269b03827ce278bedf7c749738187b1828826ee4b6` | `a1120e2e556a137ee1aaddb2dc5e74a6865e216a4e5287302d8a2a93710a6a1e` |
| owner locus | 2,696 | `9cf42df2be1994a5669c52732434a9823cef7c1532ea86175c8e8996b44ce690` | `ae3d71841096fb5791c2e9227bb8e2b3149408f0ceba3b753546cdd372b2c847` | `0a5ac1b5fec6825a69a0b7b10d80beade829d54a3d526a968437507a88634702` | `ef591030ab92ed92249984d50a680d22feea55536ffb31e22c4588d9fb7a7305` | `489518323cfa8c015256847c3ae92e2b4aa4e60fa7579ae1f6e3f023a101d90c` |
| canonical component edge | 8 | `cf56d9b57cd972a2a3272ea465f83f6fadbc3c7ed6962cb70809f19e44addb27` | `4e01219cc503d5b0e5ee0c37faf7e410181eb3c530a970cc01a89c94176228e6` | `04ad49ec152443bb781b8439526c942bd81f3b97822a37379d57b9bb28f8b78b` | `3bc5f398057477c25a3e56b5e73cbfc4e3fccb4d6e66096b088f7314f372fdd7` | `f604f33bc9dad8668f2b04be917d7cb91ae403a79c30003b145102b0f93ea2ec` |

All `9,312` rows passed their individual self-hash checks.  All five ledger
wrappers, row arrays, row-ID arrays, row-hash arrays, and ledger self-hashes
were recomputed.  All five gzip members passed integrity testing and use the
deterministic header contract `mtime=0`, empty filename, `xfl=2`, and `os=255`.

## Physical theorem closure and exact scope

Every one of the `1,024` witnesses is directly instantiated; no D4 or axial
transfer is used.  The witnesses group into exactly eight unordered Round304
final-component pairs, with exactly `128` witnesses per pair.  The eight pairs
cover `16` distinct Round304 components and form a matching: every component
has degree one.

The residual endpoints carry exactly `16` distinct official keys.  All
`1,024` endpoint pairs are cross-official-key and none is same-key.  The
two-sided physical theorem permits the physical edge, while occurrence and
official-key identities remain distinct:
`occurrence_identity_collapsed=false` and
`official_key_identity_merged=false`.

For each witness, the proof reconstructs a connected positive-area closed
rational base `B_core`, a strict monotone target factor `F`, opposite strict
signs on the two p-faces, and the unique continuous graph `rho`.  Independent
full-sign-side certificates prove the complete face-to-`rho` half-open segment
inside each named R292 support and convergence in the relative physical space
to `Gamma_core` from both sides.  The included `Gamma_core` therefore lies in
both closures and yields one physical component edge.

The contact and owner ledgers replay the full support-closure boundary, but
remain zero-credit sidecars.  They are not part of `Gamma_core`, are not an
independent G3/G4 or edge basis, and do not merge occurrence or official-key
identity.  Positive-volume corridor boxes prove only local strict-side
nonemptiness; they are disjoint from `Gamma_core` and are not intersection
witnesses.

## Independent reconstruction, attacks, and publication

The final verifier treats the producer as inert pinned bytes: it is not
imported, executed, parsed, or tokenized.  It independently reconstructs every
candidate row and all six expected candidate bytes from the sealed inputs
before opening the private candidate directory.  Its exact candidate SHA map,
the attack baseline SHA map, and the six formally published files are equal.

All `99 / 99` attack mechanisms were rejected.  The suite is bound with
`binding_mode=EXACT_FORMAL_CANDIDATE` and includes schema, mathematical-credit,
geometry, owner/contact, canonical wire, stale-pyc, symlink/hard-link,
no-clobber, race, orphan-stage, exact-prefix, post-marker drift, and publication
order attacks.  The positive transaction checks include a fresh empty output,
exact-prefix resumption, idempotent full-bundle replay, and retraction of a
newly created verification marker after a post-marker integrity failure.

The publisher is an attack-first, verification-last, crash-recoverable
exact-prefix promotion with per-file `renameat2(RENAME_NOREPLACE)`, directory
locking, stage and output directory fsync after every rename, and no clobber.
It is not claimed to make eight files one indivisible filesystem operation.
The committed order was:

```text
attack -> physical -> anchor -> closure-contact -> owner-locus ->
canonical-edge -> result -> verification
```

The attack file mtime is `2026-08-01 09:35:58.826064994 +0800`; the
verification marker mtime is `2026-08-01 09:35:58.912490389 +0800`, exactly
`86,425,395 ns` later.  No formal orphan stage remained after publication.

## Pre-seal fail-closed findings

No failed diagnostic was promoted or admitted for credit.  Before the final
source freeze, strict replay exposed and corrected three representation and
runtime defects:

- formal-geometry imports had reset Arb precision below the required `768`
  bits; both paths now restore and audit the exact effective precision;
- an independently reconstructed owner histogram used integer object keys and
  was rejected before canonical wire construction; keys are now normalized to
  strings before wire admission;
- `256 / 1,024` physical rows used an older R275 rational t-bound in the
  independent whole-support replay, while the normative producer recomputed a
  512-bit outward dyadic square-root enclosure from the exact R292 z-box.  The
  verifier now independently recomputes the same normative enclosure.

The last mismatch affected only one G5 wire leaf in those 256 rows; witness IDs
and all mathematical signs were unchanged.  Its dependent physical, edge, and
result hashes were rejected and never published.  After repair, all six
candidate files matched exactly under independent reconstruction.

## Replay summary

| Replay | Effective seed/mode | Exit | Outcome |
| --- | --- | ---: | --- |
| Producer complete no-write | `PYTHONHASHSEED=305611` | 0 | exact `1024/2048/3536/2696/8`, no output |
| Producer private stage A | `PYTHONHASHSEED=305701` | 0 | exact six-file candidate |
| Independent verifier no-write | `PYTHONHASHSEED=306109` | 0 | exact six expected files, producer unopened/unexecuted |
| Candidate admission, no promotion | `PYTHONHASHSEED=306101` | 0 | exact candidate, formal credit remains zero without marker |
| Formal promotion | `PYTHONHASHSEED=306211` | 0 | attack first, verification last |
| Independent isolated admission replay | `-I` isolated mode | 0 | exact formal attack and verification hashes, no write |
| Producer isolated private replay | `-I` isolated mode | 0 | exact six files; no seed claim |
| Producer private stage B | `PYTHONHASHSEED=305997` | 0 | exact six files |

The two explicitly seeded producer stages, the isolated stage, and the formal
six candidate files compared byte-for-byte equal.  The isolated commands used
`-I`, which ignores `PYTHONHASHSEED`; they are recorded only as isolated
replays, not as named-seed evidence.  All three temporary private staging trees
were removed after comparison and were never manifest or credit inputs.

## Exact credit boundary and next authorized step

```text
officially_admitted_physical_witness_credit=1024
officially_admitted_anchor_binding_credit=2048
officially_admitted_component_edge_credit=8
formal_DSU_rank_reduction_credit=0
formal_maximality_credit=0
formal_fibre_credit=0
formal_global_disposition_credit=0
official_key_merge_credit=0
occurrence_identity_collapse_credit=0
D4_transfer_credit=0
owner_sidecar_credit=0
D02_status=BLOCKED
CM2_status=NO-GO_FOR_CLAIM
```

Round305B closes the P1 physical-inclusion task only.  It authorizes the eight
canonical edges as inputs to a later full fresh DSU rebuild.  It does not
perform that rebuild or establish maximality.  P2 must start from the complete
sealed member and legal-edge universe, distinguish eight edge applications
from at most eight rank reductions, and independently prove that every required
maximality channel is exhausted before any fibre or global-disposition work
receives credit.
