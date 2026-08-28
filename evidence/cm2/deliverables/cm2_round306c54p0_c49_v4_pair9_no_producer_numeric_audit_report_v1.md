# CM2 Round306 C54p0 C49-v4 pair9 cold independent numeric audit v1

Status: **PASS cold no-C49-import/execute numerical replay for the frozen
pair9 collision 3 -> 4 -> 5 regression; zero formal/D02 credit**.

## Frozen artifacts

- Independent verifier source SHA-256:
  `364d07968a226c5e6e2707392412feb58f58a911b7fb7b4f8134424fa453b02d`
- Full audit file SHA-256:
  `221791b63d73950a6b88ce306cdc45005abb8f1222324272720701a1a2c0ed99`
- Full audit object SHA-256:
  `664072d98116ae3da2b2fd057e232579a6f72c659cc904483c201b94096d2f00`
- Self-test file SHA-256:
  `ba4d1504922a95965b4d8be47bcf5af9ff882faf457a49f45605bb6f3da911bc`
- Self-test object SHA-256:
  `cdb78399b5d466a77011043234084024a9f167808d20875ec479a0c5f9a5cf96`
- Reference projection extractor SHA-256:
  `7fd328d03498227151692fea321fed4230de5d746f1b9796004be822dea141ac`
- Frozen reference binding file SHA-256:
  `bbd5adfb4eb1b56410e55b637cc413adbeacb7d0198de8a06cfdc77937de3fb9`

The patched C49-v4 source is pinned to
`80bb67a46ae4f8a10195aa6b1b17f539708eafc83be4b39bc7724624fd64295f`.
Its frozen regression bytes/object are respectively `88beb4c0...` and
`9a39a439...`.

## Independence and input authority

The verifier contains no static import of C49 v2, v3, or v4 and rejects if
any such module appears in `sys.modules`, including by transitive import.  It
does not execute C49.  It loads only the lower C46/C45/C41 queue and
geometric/registry authorities, then implements its own collision state
machine, interval recentering, candidate census, root ordering, auxiliary
strata checks and sensitivity splitting.

Pair9 is located independently in both the C46 full queue and the frozen C41
`routed_ambient_cells.jsonl.gz`.  The two rows are exactly equal and bind:

```text
C46 full queue manifest  9dd2ec13da5509d7f4c8e947090feaee05ac31924e2855086c17a6dc05b7b5f4
C41 result object        b7e47a4ca9d6f4bb1fee10e78877850d5070f6d3c2b06bb0234fbabdaa2b7b24
C41 pair9 row            204f68a9496b643c5207d1d33156bab04824e021a8f0d49a14025bbb907ba93a
REFLECTED source binding d9d1ad4f4bf856764733d8f1f8360e51f8f003572104e868eb445e90c6073482
REPRESENTATIVE binding   486f959429f2b69440e0c68349c308eb07060303185536e3c771188658ab5dab
```

All pinned source and C41 authority files are stable-read before imports and
again after the complete numerical replay.  The 12-file snapshots are equal.
The runtime is pinned to python-flint 0.9.0 with Arb precision 384 bits.

## Complete numerical replay

The semantic comparison includes every numeric step field and every split
decision, while excluding only producer-specific schemas, self hashes,
handoff serialization and authenticated input echoes.  A separate reducer
consumed the already-produced canonical C49 JSON as reference data; it does
no numerical work and is never imported by the independent verifier.

The independent and reference semantic hashes match exactly:

```text
collision3 REFLECTED       266ebff0ad264d55b9392e6c079c95812d14d74a6b07530f317aca51bb712490
collision3 REPRESENTATIVE  c99198f17bb3cda1e6079f86d31f6d9f7e7dc1f23278680b12d24b99f96149b9
collision4                 fa91e106d1d4999d4d8c9c63171d6769f474d2a049f40c8f88e2dc4d8563ad57
collision5 selected step   cb03b21eb7edb01bc3b7e6dae0fc23cc75caf55bd72592f7bd3281528e6f195b
combined                   b2700d1fd48686557a7b918037b9c89a8b8054c710f00af4e66cf0c953521447
```

Coverage is complete for this frozen regression:

- collision3, each physical side: 99 nodes, 49 performed splits, 50 leaves,
  plus 32 exact bounded next decisions; Kraft sum 1;
- collision4: 233 nodes, 116 performed splits, 117 leaves, plus 56 exact
  bounded next decisions; Kraft sum 1;
- semantic reference counts: 81 decision rows and 50 leaves per collision3
  side; 172 decision rows and 117 leaves for collision4;
- selected chain: `000000:W[0,0] -> 00000000000011:G[0,1] -> G[0,0]`;
- collision indices are exactly `[3,4,5]`, history is contiguous, and every
  performed split observes the exact `selected_child_bit` enum `{"0","1"}`.

## Actual file-fault matrix

The verifier creates disposable real source files and exercises five faults:

1. atomic source replacement after the first descriptor read;
2. truncation during read;
3. injected premature EOF/short read on a real open file descriptor;
4. permission denial (`chmod 000`);
5. rename-away during read.

All 5/5 fail closed.  The temporary directory is removed.  Repeated cold runs
produce byte-identical self-test and audit output.

## Strict boundary

This closes the prior P0 **pair9-scoped independent numeric verifier and file
fault-test gap**.  It does not constitute a global D02-B verifier or authorize
full production shards.  Both public global oracles remain absent:

- `GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE`
- `GLOBAL_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_ORACLE`

The audit writes no runtime authority, candidate, pointer, receipt, seal or
canonical status.  Formal credit and D02 credit are both zero.  CM2 remains
`NO-GO_FOR_CLAIM`.

## Replay

```bash
.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c54p0_c49_v4_pair9_no_producer_numeric_verifier_v1.py \
  --self-test

.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c54p0_c49_v4_pair9_no_producer_numeric_verifier_v1.py \
  --verify
```
