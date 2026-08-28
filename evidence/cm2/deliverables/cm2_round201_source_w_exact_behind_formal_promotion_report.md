# CM2 Round201 — formal source-W exact-behind promotion

Date: 2026-07-26  
Verdict: `PARTIAL__FORMAL_EXACT_BEHIND_CONSERVATIVE_WHOLE_ORIGIN_PROMOTION__D02_STILL_BLOCKED`

## Frozen inputs and result

Round201 starts from the independently verified Round184 priority registry and
the pinned Round180/Round176 interval geometry.  It promotes an origin only
when every inherited Round180 terminal and every newly refined terminal is
strictly excluded, the complete owned 3D/2D/1D/0D target partition is present,
and the physical source parent is a strict chart interior.

Frozen identities:

- producer SHA256:
  `f7e53607d9a2c6b2f4fda76c9a6a92845f12cced04e28168f227cb516a1f4010`;
- certificate file SHA256:
  `72b9f2959f362a7918bf628989faf2f0f5ed295fc3e28a305b727ff4ed216536`;
- certificate byte count: `1,115,443,418`;
- certificate result SHA256:
  `9d3dc29c07f81ba2b71743e983c3d4718e40a430d3566cc934d4a3098facad3c`;
- frozen Round184 manifest SHA256:
  `3c2a50663dc47479f67435109b737362895e53a2c1b4c29991fe875c5ac68cd1`.

The complete 1,444-row Round184 priority registry is independently replayed in
the same outcome-blind order.  Round201 never imports or uses a Round190,
Round193, Round194, or Round197 probe as mathematical evidence.

## Pure target-first cohort

The pure scan selects exactly 162 Round184 origins with at least one
independently rebuilt `TARGET_NOT_STRICT_POSITIVE_FIRST` residual.  A fixed
depth-two refinement produces:

- 37,262 exact-behind terminal cells;
- exact refined volume `3297687/838860800000`;
- 156 complete strict physical-interior origins;
- 6 complete physical source-seam origins held at zero integer credit.

Every exact-behind row independently proves strict negative `ell`, strict
positive direct distance margin, deletion of the impossible candidate, and a
strict excluded disposition after reclassification.  The complete per-origin
terminal volume and split-face lineage are conserved.  The six seam origins
remain held even though their target partitions close.

## Generalized mixed and compact-q cohort

The generalized scan is fixed before Round201 outcomes:

- 596 `DELTA_H_OR_MULTI_NO_Q` origins;
- 54 `COMPACT_Q_PRESENT` origins;
- 650 origins and 182,776 final cells in total;
- exact final-cell volume `4043919/52428800000`.

The full cell registry deletes 233,356 exact-behind candidates and leaves
22,580 unresolved candidates.  It classifies 161,648 final cells as
geometrically excluded and 21,128 as residual.  Its final-disposition census
is:

- 142,986 `EXCLUDED_UNIQUE_FIRST_OWNER_MISMATCH`;
- 18,662 `EXCLUDED_OUTGOING_CHART_MISMATCH`;
- 48 `LIVE_FROZEN_STAGE_ONE_OWNER_CHART_MATCH`;
- 21,080 `UNRESOLVED`.

Whole-origin outcomes are:

- 390 strict-interior whole-origin credits;
- 6 complete source-seam origins held;
- 200 incomplete mixed origins retained;
- 54 compact-q origins retained for an independent source-stratum treatment.

The inherited-terminal audit covers 45,948 Round180 terminals.  Sixteen
uncredited origins contain 358 nonexcluded inherited terminals
(`102 LIVE + 256 MIXED`); 14 of those origins are an overlapping diagnostic
subgroup of the 200 incomplete mixed origins.  None enters formal credit.
All 390 strict credits and all 6 complete seam holds have zero inherited
nonexcluded terminal.  Consequently both the formal strict-bad and formal
seam-bad sets are empty.

## Conservative integer ledger

The two disjoint formal cohorts contribute:

- 156 pure strict-interior origins;
- 390 generalized strict-interior origins;
- 546 new whole-origin exclusions in total.

No child count, refined volume, analytic stratum, physical source seam,
compact-q origin, or incomplete mixed origin is converted into integer
credit.  The official source-W ledger therefore becomes:

```text
74,012 + 546 = 74,558 excluded
2,820 - 546 = 2,274 conservative live
74,558 + 2,274 = 76,832
```

The remaining 278 Round184 priority origins form an exact disjoint partition:

- 6 pure target-first seams complete but held;
- 12 other pure source seams inherited from Round184;
- 6 generalized source seams complete but held;
- 200 incomplete mixed origins;
- 54 compact-q origins.

There is no complete-but-inherited-nonexcluded partition group; the 14
incomplete mixed origins with such terminals are explicitly recorded only as
an overlapping diagnostic subgroup.

## Independent verification boundary

The verifier source SHA256 is
`29344dd3c0590ac9d0d3f0618a3f0f034316759468e15af2674813ab72f7ce2b`.
It treats the producer only as pinned, inert, same-directory regular-file
bytes and never imports or executes it.  It imports only the Round180
independent verifier as the geometry evaluator; the existing pinned
Round176 evaluator is reached transitively.  Round180 and Round176 are pinned
both before and after import.  The complete six-entry Round184 manifest,
certificate, and independent verification are replayed before reconstruction.

The verifier rebuilds the complete expected result before loading the
Round201 certificate.  Acceptance requires:

- reconstructed result SHA256 equal to
  `9d3dc29c07f81ba2b71743e983c3d4718e40a430d3566cc934d4a3098facad3c`;
- full Python-object equality;
- full canonical pretty-JSON equality, including the exact byte count and
  certificate file hash.

The verification is `PASS`:

- verification result SHA256:
  `7b4e95f87a75fa3a02b925f202b156947c27b08c77a3c1e704a6b7625a2c8f8d`;
- verification file SHA256:
  `6361e38dd01892f8df164a0d8b58a5b7fe1741a9d61cb0727618a76e63759c1a`;
- re-signed semantic attacks rejected: `13/13`;
- strict JSON/encoding attacks rejected: `13/13`;
- path, alias, type, protected-output, and output-name attacks rejected:
  `17/17`.

The semantic attacks are performed by bounded in-place mutation, complete
top-level result-digest recomputation, equality rejection, and exact
restoration; no 1.1 GB result is deep-copied for each attack.  They cover
whole credit, a credited ledger row, inherited exclusion, a generalized cell
disposition, seam credit, residual partition, the official ledger, child
credit, D02, D03 authorization, Gate5, complete global blocks, and CM2.

The output writer uses a strict official/hidden allowlist, rejects symlinks,
hardlinks, FIFO and directories, nested/escaping paths, a symlink-parent
alias, wrong hidden suffixes, certificate-shaped output names, and all pinned
artifacts.  It fsyncs the file before replacement and the parent directory
after replacement.

## Implementation-overlap limitation

The verifier is independent in the non-import/non-execution, fresh-process,
input-pinning, certificate-after-reconstruction, and full expected-result
senses.  It is not claimed to be an implementation-diverse second derivation
of every Round201 formula.

A normalized AST-body audit compares all top-level functions in the frozen
producer and verifier:

- producer top-level functions: 38;
- verifier top-level functions: 51;
- exact body-overlap pairs: 13;
- producer `build_result` body reused: false;
- producer `main` body reused: false.

The 13 disclosed overlaps consist of six low-level output/IO helpers, one
upstream-chain checker, and six Round201 reconstruction/evidence kernels:
registry replay, pure-cohort rebuild, generalized-cohort rebuild, clipped
partition proof, single-candidate evidence, and generalized-candidate
evidence.  A shared algorithm error in those kernels can therefore survive
both artifacts.  Full certificate tamper resistance is established, but a
fully implementation-diverse mathematical audit remains a stronger optional
future check.

## Reproducibility and global state

Producer seed `201072` reproduced the official 1,115,443,418-byte certificate
byte for byte.  Verifier seeds `201061` and `201062` reproduced the same
verification byte for byte.  Exact commands, timings, peak memory, hashes, and
comparisons are recorded in the cold-replay note.

Round201 changes only the formal source-W integer ledger.  It makes no global
claim promotion:

- `D02 = BLOCKED`;
- `D03 negative oracle = UNAUTHORIZED`;
- Gate5 remains `10/18`;
- complete global 18-field blocks remain `0`;
- `CM2 = NO-GO_FOR_CLAIM`.

The next source-W core gate is the exact treatment of the remaining 278
origins: half-open source-seam ownership, compact-q/source-grazing strata, and
the still-incomplete mixed origins.  No global exact-key credit is permitted
until all required dimensions for the same key are closed.
