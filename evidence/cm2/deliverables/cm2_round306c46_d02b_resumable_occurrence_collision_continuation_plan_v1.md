# C46 D02-B resumable occurrence continuation v1 — zero-credit plan

Date: 2026-08-11 (Asia/Shanghai)

Status: `ACCEPTED_ONLY_AS_RESUMABLE_COLLISION3_ZERO_CREDIT_DIAGNOSTIC_INTERFACE`

This artifact does not close D02-B.  It binds the complete installed
collision-3-ready queue, materializes bounded C44 occurrence computations, and
provides an append-only replayable shard chain.  Collision 4 through 1,648 has
zero proof steps, and every terminal, D02, and formal credit remains zero.

## Frozen artifact and deterministic results

- source:
  `deliverables/cm2_round306c46_d02b_resumable_occurrence_collision_continuation_engine_v1.py`;
- source SHA-256:
  `95a9e30101368b4bc91142a75ec7821b0d035f3dab52a556377c761c1bdac7b7`;
- full queue manifest:
  `9dd2ec13da5509d7f4c8e947090feaee05ac31924e2855086c17a6dc05b7b5f4`;
- 128-shard plan, shard zero object:
  `19a1e207dbaac69222d4e3947c7c694de5062ac929505ab146ea8fe25c6404c8`;
- integrated end-to-end self-test object:
  `b121c79f219a619c9f01a7a3874095360f99839fd2e65057a9f682547b4a549f`;
- depth-zero one-row dry-run object:
  `6240c849ff24f892b59d4fb003e26cafba075bcfcac3973cf3122e2fe0676e53`.

Syntax compilation passed.  The plan and dry-run were stdout-only.  No formal
shard, runtime candidate, receipt, pointer, seal, or authority was published.

## Complete frozen queue

The plan rereads the frozen C35--C37 templates and the installed C41 ambient
ledger and reconstructs:

- 7,463 representative collision-3-ready rows;
- 14,926 distinct physical sides in exact
  `REFLECTED, REPRESENTATIVE` order;
- physical queue sequence
  `c79b7e8736c7cf9c8e95e6249d76c0d0b31fb4d3b6d5dbb12d359a4c7a41f5e0`;
- physical handoff-ID sequence
  `2558af09865e542b5eb969f636585baa815086de5d1f2b130a7ef152cf3a8c58`.

The 128 balanced selectors preserve both sides and cover 58 or 59
representatives per shard.  Range counts and balanced shard index/count are
rederived from exact start/stop bounds; selector metadata cannot redefine the
covered ordinals.

C35--C37 remain computation templates only.  They cannot replace a complete
per-side, per-adaptive-leaf, per-collision occurrence proof.

## Resume and append-only contract

`--resume-from` requires the complete chronological predecessor file list from
the first selection ordinal.  Every predecessor is stable-read and must be a
regular single-link canonical JSON file with exact self-hash, frozen source
pins, full queue manifest, selector, bounds, rows, census, nested zero-credit
locks, and a byte-exact C44/C45 replay.  Adjacent files bind predecessor file,
object, resume-key, pending-state, coverage-chain, and actual row-derived
cursor hashes.

Top-level shard, execution-bound, and range/balanced selection keys are closed
sets.  Unknown semantic aliases cannot acquire authority or credit.  Actual
start/stop and row ordinals, not a scalar claim, determine progress.

Persistent diagnostic shards use `O_EXCL|O_NOFOLLOW|O_CLOEXEC`, mode `0444`,
file and directory `fsync`, and `renameat2(RENAME_NOREPLACE)`.  The stage fd is
held across rename; fd/path inode and bytes are replayed before and after the
commit.  A failure after rename is reported as committed and never as an
unpublished retry.

## Independent validation

The integrated real-filesystem suite passed
`PASS_48_OF_48_END_TO_END_HOSTILE_RESUME_AND_PUBLICATION_TESTS`.  It published
two temporary shards, replayed the complete `p1 -> p2` chain to cursor two,
then removed every temporary output.  It rejected:

- omitted, reversed, or duplicated predecessor chains;
- coherent row and cursor mutations;
- symlink and hardlink inputs;
- nested credit and top/bounds/selection semantic aliases;
- coherent range-count and balanced-index/count inconsistencies;
- output collision and injected post-commit failure misclassification.

A separate implementation repeated the real two-shard exercise and 21
independent negative cases.  It reported zero HIGH and zero MEDIUM findings in
the diagnostic scope.  The publication stage-fd/inode/byte replay and commit
state also passed.

At depth six, one real pair-9 dry-run produced 86 collision-3 occurrence
records: 48 remained collision-3 adaptive pending and 38 reached exact
collision-4 handoffs.  All terminal margins were explicitly pending; no
terminal was credited and collision 4--1,648 proof-step count remained zero.

## Exact implementation boundary

The prior wording that all six mathematical primitives were absent was too
broad.  The accurate two-level registry is:

1. Mathematical kernels exist but are not yet a pinned formal occurrence
   engine: full-box AD/recenter; candidate/discriminant/root order;
   official word/chart/wall; and most homogeneity/incidence/core/margin logic.
2. Global oracles genuinely remain absent: the cemetery/disconnected exterior
   terminal oracle and arbitrary-history codimension face/endpoint/corner owner
   closure.

Reusable kernels include Round185 AD, C44 exact recenter, Round136/138 owner
and candidate audits, Round139 wall margins, Round117 homogeneity strata, and
the 24-core registry.  They still need an arbitrary-history
`advance_one_collision` wrapper, an unbounded homogeneity bracket, exact
per-occurrence field binding, and cold independent replay.

Round153--161 certify only an extremely narrow Round139 Source-W collar.  It
has no containment/crosswalk to the much wider C41 boxes and grants the current
queue no ambient credit.

## Strict nonpromotion and next step

The accepted scope is only a recoverable, occurrence-bound collision-3
diagnostic materializer and continuation interface.  It is not evidence that
collision 4--1,648 is complete, that D02-B is closed, or that any terminal,
D02, authority, seal, or promotion exists.

The shortest implementation order is:

1. freeze a pure `advance_one_collision(original_box, owner_history)` kernel;
2. verify it against Round139/C44 regressions;
3. run per-occurrence prefix/core continuation with all ten exact fields;
4. share a codimension owner ledger with D02-A for every adaptive split;
5. build the compact exterior/cemetery oracle only for the remaining branches.

Until those steps pass an independent implementation, all C46-B outputs stay
zero-credit and the installed C42 census remains 574 paired / 1,150 unresolved
/ 575 remaining representatives.
