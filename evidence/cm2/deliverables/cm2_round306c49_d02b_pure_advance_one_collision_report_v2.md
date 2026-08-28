# CM2 Round306 C49 D02-B pure `advance_one_collision` v2 report

Status: **PASS LOCAL KERNEL / REPLAY AUDIT; PENDING GLOBAL ORACLES; ZERO FORMAL CREDIT**.

## Frozen implementation

- Pure producer: `cm2_round306c49_d02b_pure_advance_one_collision_v2.py`
- Producer SHA-256: `25d87f0ae27b7946ab9f55dbe8a5f50c353eb9f05dd4a6e50810d92e438700df`
- Public signature: `advance_one_collision(original_box, owner_history)`.
- Collision index rule: `len(owner_history)+1`; the AST audit found no collision-index 3/4/5 special branch.
- Independent structural/replay auditor:
  `cm2_round306c49_d02b_pure_advance_one_collision_independent_auditor_v2.py`
- Auditor SHA-256: `8d9a4beb46d384a69a902549d35ced1f4f584d392343402857d24966b0844ae0`
- Canonical regression object SHA-256:
  `e82085e0b463dc3d38dccc9e4d58b4d0f20aa120bab0ccd7025b61e6de688fc3`
- Canonical audit object SHA-256:
  `cacd72f7af5416a537a33f965da5fd1e2b6968558007cb17966776e69c4b3a1e`

The producer and auditor are new C49 files.  They do not modify C42, C46,
C47, either authority pointer, any receipt/seal, or canonical status.

## Exact queue freeze

The v2 regression rejects unless all of the following replay exactly:

- 7,463 representative rows and 14,926 physical sides;
- representative key sequence:
  `9fe3435e1efdb935fb2756c0e808b8cc282baf04af95a31ca723bccbe4755ce5`;
- physical queue sequence:
  `c79b7e8736c7cf9c8e95e6249d76c0d0b31fb4d3b6d5dbb12d359a4c7a41f5e0`;
- physical handoff-ID line sequence:
  `2558af09865e542b5eb969f636585baa815086de5d1f2b130a7ef152cf3a8c58`;
- C35/C36/C37 diagnostic collision-3 row pins:
  `2d1e15152e61648237b33b7aeade8a9e0c4374ecc84b0f4c3f3ddbb173f1b5a1`,
  `7a4296ba0a1537b4a34ff9c0673e63c0b5874a0e27e8c2e456dc46d0db0f4995`,
  and `7d75d31baa4826a0ae821d9bc14bfdb03b1a311a2ab00ba48ba78cdd79cfc013`.

Those C35--C37 rows are queue/diagnostic pins only.  They never select a v2
owner or replace a full occurrence candidate table.

## Regression result

Pair 9, C41 path `011110111`, was recomputed on both physical sides.  Each
side exactly reproduces the frozen C44 collision-3 pilot census:

- 99 nodes, 49 splits, 50 prefix-free leaves, Kraft sum exactly 1;
- 18 locally strict live collision-4 handoffs;
- 32 bounded unresolved leaves with exact next split decisions.

The first canonical live occurrence uses C45 side order followed by binary
adaptive suffix order:

- collision 3: reflected side, suffix `000000`, owner `W[0,0]`, step SHA-256
  `03e2d72d5528f88a004cb981ff89dd505d0a122b9c2787c7133a316b87ec3172`;
- collision 4 adaptive tree: 233 nodes, 116 splits, 117 leaves, Kraft sum 1,
  with 61 locally strict live leaves and 56 bounded unresolved leaves; tree
  SHA-256 `963dfb04aca9e4b0ac62e22867783e7b214469cf6ea24c0bf095db606e97ea1f`;
- first collision-4 live child: suffix `00000000000011`, owner `G[0,1]`,
  all 55 frozen candidates recorded, structured local decision-margin lower
  bound `1/4`, step SHA-256
  `f8626355f519cef4a8bfff44d3be35b944a8aa21ad9b5fb0f86c8ffffbb62429`;
- collision 5 on that child: owner `G[0,0]`, all 57 frozen candidates
  recorded, structured local decision-margin lower bound `1/4`, step SHA-256
  `00bf54e317c9af90cdefbf53890d449afddbdb9d6335af9acece971649a701bf`.

Every locally complete step binds the exact owner, selected discriminant,
strict root order, official word, incoming/outgoing chart, wall/order record,
homogeneity, incidence, core decision, structured terminal-decision margin,
and the complete candidate table.  Candidate tables preserve frozen order and
carry an independent rows SHA-256.

## Tests and audit scope

- Python compilation: PASS for producer and auditor.
- Producer fail-closed self-test: `20/20` PASS.
- Full regression: PASS with collision indices `[3,4,5]`.
- Auditor: PASS; the complete regression replayed twice byte-identically.
- AST purity audit: public arguments exactly `original_box, owner_history`;
  zero mutating proof-kernel calls; zero collision-index 3/4/5 special branch.
- Self-hashes, history evidence links, candidate-row hashes, owner-history
  append links, prefix-free leaves, and exact Kraft sums were replayed.

The auditor imports the frozen producer only for structural inspection and
byte-for-byte replay.  It is **not** a D02-C independent mathematical
implementation and must not be represented as the independent implementation
required for D02 promotion.

## Exact remaining gaps and credit lock

Two required global oracles are absent:

1. `GLOBAL_CEMETERY_DISCONNECTED_EXTERIOR_ORACLE`;
2. `GLOBAL_CODIMENSION_FACE_ENDPOINT_CORNER_OWNER_ORACLE`.

Consequently, every locally complete collision-3, collision-4, and collision-5
step explicitly returns `PENDING_GLOBAL_ORACLE` naming both gaps.  Every step,
including bounded unresolved leaves, has `formal_credit=0` and `D02_credit=0`.
No strict cemetery/disconnected or global codimension-owner terminal was
issued.

This regression covers one pair-9 occurrence through collision 5 only.  It
does not close the 64 collision-3 bounded leaves across the two sides, the 56
collision-4 bounded leaves in the selected tree, the other 14,925 physical
queue entries, or collision 6 through 1,648.  It does not rebuild the 862-parent
Kraft conservation or 76,832 four-class census and is not D02-C.  D02 remains
blocked, D03 remains unauthorized, and CM2 remains `NO-GO_FOR_CLAIM`.
