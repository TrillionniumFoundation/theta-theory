# CM2 Round204 — source-G wall return-signature local replacement

Date: 2026-07-26  
Verdict: `CERTIFIED_LOCAL_SOURCE_G_WALL_RETURN_SIGNATURE_REPLACEMENT__NO_WHOLE_TUBE_OR_GLOBAL_EXACT_KEY_DISPOSITION`

## Frozen scope and result

Round204 starts from the complete pinned seven-entry Round182 formal package.
It isolates the 64 residual source-G wall origins that Round182 left as a
separate tail, reconstructs their 512 exact leaves, and replaces the sole
wall return-signature obstruction by an explicit local signed-wall
cell complex. Round192, Round196, and Round203 probe outputs are not formal
inputs.

Frozen identities:

- producer SHA256:
  `7e4b81846155c1edad0807362c7086a290702da7ce6680d7c449b7193635da77`;
- certificate file SHA256:
  `e7e1c49bebcb8c01f0fb4b33af66e4f2a8de560f121cae65f4971b2fec3e1818`;
- certificate byte count: `7,157,575`;
- certificate result SHA256:
  `ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd`;
- pinned Round182 manifest SHA256:
  `32dea92dd0de87d3ded6ed69a908b58b01402ddcdef3f0e2b5ffde096a9383c5`.

The Round182 leaf classification is exactly:

- `256` empty leaves;
- `192` full 2D graph leaves;
- `64` residual 3D tail leaves.

All 512 leaves have exactly one recorded wall endpoint/count-transition
obstruction and strict nonwall signature fields. Absence of a carried row is
never used as positive evidence.

## Local signed-wall replacement

Round204 materializes 736 unique strict open 3D regions. The exact incidence
census is:

- leaf-region histogram: `288 × 1 + 224 × 2 = 736`;
- origin-region histogram: `32 × 8 + 32 × 15 = 736`;
- tail open-region count: `96`;
- signed-word histogram:
  `512 × []`, `56 × [X+]`, `56 × [X-]`, `56 × [Y+]`,
  and `56 × [Y-]`;
- tail signed-word histogram:
  `64 × []` and eight of each signed singleton.

Every region has a unique local signature and joins exactly one immutable
official key. The 736 region occurrences are partitioned byte-exactly among
12 local exact-key joins with official ordinals
`18715,18716,18717,70920,70921,70922,128050,128059,128060,186165,186174,186175`.
This is a local occurrence join only; no global exact-key fibre is declared
exhausted.

The exact coordinate-volume ledger remains:

- relevant input: `177/1600000`;
- Round182 closed portion: `22479/204800000`;
- Round182 tail: `177/204800000`;
- integer leaf delta: `0`;
- exact coordinate-volume delta: `0`.

Individual curved open-region volumes are deliberately not summed. Each
leaf's outer volume is counted exactly once, while every 2D/1D/0D stratum has
zero ambient 3D volume.

## Complete 2D/1D/0D lineage

The closed-dimensional ownership complex contains:

- `224` source `t=0` 2D sheet cells;
- `224` target regular-graph 2D sheet cells;
- `1,024` unique 1D strata;
- `580` unique 0D strata.

Every 2D cell records its incident strict 3D regions, boundary 1D rows,
boundary 0D rows, and deterministic half-open owner. Every 1D row has exactly
two 0D endpoints, one half-open owner, and complete incident-sheet lineage.
Every 0D row has one half-open owner and complete incident 1D/2D lineage.

The exact source-target intersection has:

- `16` unique 1D segments;
- `32` source-sheet boundary incidences;
- `32` target-sheet boundary incidences;
- `20` globally deduplicated 0D endpoints.

All 32 tail pairs have explicit empty-event-empty glue. Each glue row binds
its two tail leaves, source and target 2D sheets, source-target 1D
intersection, adjacent crossing region, and two outer empty regions. No
unexpected signature change occurs.

All 64 origins have complete local 3D/2D/1D/0D references and one formal
local replacement credit. Across the complete nested result, the verifier
found 7,184 occurrences of whole-tube/global-disposition credit fields and
required every one to equal zero.

## Independent formal verification

The verifier source SHA256 is
`6bcfbb794005e5a92590b7bb60ffceda34db3441ced143a15ceb23e15d5c035e`.
It treats the Round204 producer only as pinned inert same-directory regular
bytes and never imports or executes it. It imports only the pinned Round182
independent verifier chain. The Round182 manifest and all seven entries are
re-pinned before, during, and after reconstruction.

The complete expected Round204 result is rebuilt before the candidate
certificate is opened. Acceptance requires:

- reconstructed result SHA256 equal to
  `ef106d06399094a453eb5e66d73a0022a9bb5343f8c4788b3a3fbc9177d45ccd`;
- complete Python-object equality;
- complete compact canonical-JSON byte equality;
- exact certificate byte count and file SHA256;
- all row closures, ledger digests, counts, partitions, and cross-dimensional
  references to pass a second outer audit.

The official verification is `PASS_PARTIAL_FORMAL_ROUND204`:

- verification result SHA256:
  `bd523e7c288e8b6830a7e94d78d06039b324bc8d2fdcfd38dab2ec85b532b1fd`;
- verification file SHA256:
  `04525bd3f1257825fe4825cfbf17674b3391c503b3cbe987b45ffd6f7346e852`;
- re-signed semantic attacks rejected: `20/20`;
- strict JSON/encoding/oversize attacks rejected: `15/15`;
- path/type/alias/temp attacks rejected or safely bypassed: `21/21`.

The semantic suite attacks every material ledger: Round182 binding, formal
scope, empty anchors, the 512 obstruction rows, tail leaf/pair geometry,
3D regions, both 2D sheet families, 1D and 0D lineage, tail glue, origin
completion, exact-key joins, exact volume conservation, strict nonpromotion,
probe nondependency, provenance, and the next-gate statement. Affected row
closures and ledger hashes are recomputed before the complete expected-result
comparison, and the top-level result is genuinely re-signed.

Strict JSON tests cover duplicate keys, floats, NaN/infinities, BOM, NUL,
invalid UTF-8, surrogate keys/values, trailing input, non-object input,
noncanonical whitespace, empty input, and oversize input. Path tests cover
input and output symlinks, hardlinks, FIFO, directories, parent escape,
symlink-parent aliasing, protected artifacts, wrong output names, direct
temporary names, and a prepositioned temporary symlink. Atomic output uses an
unpredictable same-directory `mkstemp` file, file `fsync`, `os.replace`, and
parent-directory `fsync`.

## Implementation-overlap limitation

The verifier is independent in the fresh-process, producer
non-import/non-execution, frozen-input pinning, certificate-after-rebuild,
complete expected-result, and outer lineage-audit senses. It is not claimed
to be an implementation-diverse second derivation of every interval formula.

A normalized AST-body audit reports:

- producer top-level functions: `47`;
- verifier top-level functions: `63`;
- exact body-overlap pairs: `43`;
- producer `build_result` body reused: false;
- producer `main` body reused: false;
- duplicate literal dictionary keys in either source: `0`.

The 43 disclosed overlaps are the lower-level reconstruction and utility
kernels copied into the standalone verifier. A shared algorithm error in
those kernels can survive both artifacts. The separate outer census,
row-closure, zero-credit, partition, and 3D→2D→1D→0D cross-reference audit
reduces but does not eliminate that risk. A fully implementation-diverse
mathematical derivation remains a stronger optional future check.

## Reproducibility and strict nonpromotion

Producer seeds `204051` and `204062` reproduced the certificate byte for
byte. Verifier seeds `204071` and `204072` reproduced the verification byte
for byte. Commands, timings, memory, hashes, and comparisons are recorded in
the cold-replay note.

Round204 certifies only the local replacement:

- whole-original-tube credit: `0`;
- global exact-key-disposition credit: `0`;
- source-G global exact-key dispositions: `0/224580`;
- D02: `BLOCKED`;
- Gate5: `10/18`;
- complete global 18-field blocks: `0`;
- CM2: `NO-GO_FOR_CLAIM`.

The next core gate remains the other Round182 source-G residual origins. The
64 locally closed wall occurrences must not be identified with complete
global exact-key fibres.
