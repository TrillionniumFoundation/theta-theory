# CM2 Round306 C49 D02-B authenticated `advance_one_collision` v3 report

Status: **PASS AUTHENTICATED LOCAL KERNEL AND STRUCTURAL REPLAY; PENDING TWO GLOBAL ORACLES; ZERO FORMAL CREDIT**.

## Frozen files and scope

- Producer: `cm2_round306c49_d02b_pure_advance_one_collision_v3.py`
- Producer SHA-256:
  `2f603c17f634ac1d5dca9763235f41e7a0259e0b384daa7d7c95cea63704a705`
- Structural/replay auditor:
  `cm2_round306c49_d02b_pure_advance_one_collision_structural_replay_auditor_v3.py`
- Auditor SHA-256:
  `d5328cb30bc7bb9670af745d4d485cf9582b882089352c0ca47b14fdb3af30e0`
- Regression object SHA-256:
  `eeb5e1cc3c25f23f6701348400b611a94a48095789c6ca76c95038bef40bbcfc`
- Structural/replay audit object SHA-256:
  `379d587ef6d7b99fc5f735b8f856f1be1b98ece65b3db065bdfe585ae5bddd60`

The auditor imports the frozen producer for structural inspection and exact
byte replay.  It is explicitly not a no-producer-import numeric verifier, not
an independent mathematical implementation, and not D02-C.

## Authenticated public contract

The public signature remains
`advance_one_collision(original_box, owner_history)`, with collision index
derived only as `len(owner_history)+1`.

Before numeric work, v3 verifies:

- complete pinned source-binding preimage and its self-hash;
- complete evidence preimage for every genesis/prior-step history row;
- every prior step's self-hash and evidence-body hash;
- contiguous collision index and exact recursive history prefix;
- full candidate row count, frozen order, and candidate-table SHA-256;
- strict unique owner, selected discriminant, and strict root-order binding;
- previous next-handoff identity and appended history row;
- exact occurrence, source, closed-box, suffix, and handoff continuity;
- exact t/p dyadic refinement geometry via suffix-shuffle replay.

The public function deep-copies both inputs before validation.  Sealing also
deep-copies the output body.  Registry tables and physical cores are local
variables; the runtime AST has no global statement, cache helper call, or
attribute mutation assignment.

## Executed tests

- `py_compile`: PASS for producer and auditor.
- Ten executed adversarial attacks: 10/10 PASS.
- Cold/warm byte identity: PASS.
- Cache-poison byte identity and cache nonmutation: PASS.
- Caller-input mutation isolation: PASS.
- Pair-9 regression replayed twice byte-identically by the structural auditor.
- Recursive full preimages and collision 3→4→5 box/suffix/occurrence/handoff
  chain: PASS.

Adversarial self-test object SHA-256:
`3410953c101dca1c615ef52189c65f6209a979db23ce4666c1b952a28bd4850c`.

## Exact pair-9 regression

The exact queue freeze remains 7,463 representative rows / 14,926 physical
sides, with physical queue SHA-256
`c79b7e8736c7cf9c8e95e6249d76c0d0b31fb4d3b6d5dbb12d359a4c7a41f5e0`.

Both collision-3 physical sides preserve the C44 numeric census exactly:

- each side: 99 nodes, 49 splits, 50 leaves, Kraft 1;
- each side: 18 locally strict live leaves and 32 bounded unresolved leaves;
- reflected tree SHA-256:
  `db39c8173aaad00558c525ebe64bef15407caf8b6522e9b77595d37d6ae8d02f`;
- representative tree SHA-256:
  `308d51793a9e1770a9adfdcb909f00f077c6cdc96bd09abda204ce51c1483231`.

The authenticated continuation is:

- collision 3: reflected suffix `000000`, owner `W[0,0]`, evidence SHA-256
  `d6054fe5145cc0d3b2e276e77e97c8744ce8be8423fe5139c36b989b94955328`,
  object SHA-256
  `d28a82c071af1cb320b666ddd7b7fba4526e4368aa6cb13947dea5afd856a526`;
- collision 4 tree: 233 nodes, 116 splits, 117 leaves, Kraft 1, with 61
  locally live and 56 bounded unresolved; tree SHA-256
  `3243b49587d20303b7b2e42a892aef6b0b96a9a92a4ce3e0f4d2aa8fb66526ff`;
- first collision-4 live child: suffix `00000000000011`, owner `G[0,1]`,
  55 complete candidate rows, candidate rows SHA-256
  `1e7f0dd182fe60a1187476beb200d0643a02cc5c571964da4e79f98f5352d530`,
  local structured margin lower bound `1/4`, evidence SHA-256
  `7ff04f2f49a8e0eb9f4425cac3a105e343c6df966452d72c38a3d59ec72864b5`,
  object SHA-256
  `65477f591f021368091964ba4a3105d24f77cc1da53f141142befd94110f2906`;
- collision 5: owner `G[0,0]`, 57 complete candidate rows, candidate rows
  SHA-256
  `6efc4a5698fc393d1a79a43219242f8f8d111671f6b1a2ed4acc05efa81371ed`,
  local structured margin lower bound `1/4`, evidence SHA-256
  `715990cbe634855f7d647a222a1b9f7e3fe8d4d67f388f43dfb67f64c6f53dc2`,
  object SHA-256
  `53eda4b79e050c9de1e5a90e2146cf8c149802daec187b41eb45283f619f854e`.

V3 object hashes necessarily differ from v2 because complete authenticated
preimages are now part of every step.  The numeric collision census, owners,
candidate counts, candidate-row hashes, and strict margin bounds are preserved.

## Exact remaining gaps

Two global oracles remain absent:

1. `GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE`;
2. `GLOBAL_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_ORACLE`.

Every locally complete collision-3/4/5 step therefore returns
`PENDING_GLOBAL_ORACLE` with both names.  Every emitted step has
`formal_credit=0` and `D02_credit=0`.

This remains a single pair-9 diagnostic through collision 5.  It does not
close the other 14,925 physical queue entries, the bounded collision-3/4
leaves, or collisions 6→1,648.  It does not rebuild the 862-parent Kraft or
76,832 census and is not D02-C.  D02 remains blocked, D03 unauthorized, and
CM2 remains `NO-GO_FOR_CLAIM`.
