# Round306C0 R235D-corrected fresh freeze report

## Decision

`PASS_SEAL_CANDIDATE_PENDING_MANIFEST_FIRST_FINAL_REPLAY`

Round306C0 reconstructs the legal-component freeze after applying the sealed
R235D source-only invalidation theorem.  Producer artifacts remain zero-credit.
The independent verification document is the last and sole marker granting the
corrected DSU freeze one unit of formal credit.  B1A, B2, maximality, fibre,
global-disposition, D02, and CM2 credit remain zero.

## Frozen construction and authority boundary

- Producer: `cm2_round306c0_source_g_r235d_corrected_fresh_freeze_producer.py`
- Producer SHA-256: `35055dbdbe6562f3720c48a253d19089dd7263d8aed4243b0aa8b09dacad15a4`
- Independent verifier: `cm2_round306c0_source_g_r235d_corrected_fresh_freeze_independent_verifier.py`
- Independent verifier SHA-256: `bcabf0a64c0813f7d883d1380d313a1b51d82396796bf5304fb6f53d34e54f50`
- Authority pins: 23 regular one-link files, opened with `O_NOFOLLOW`, held by file descriptor, digested twice, and path/descriptor revalidated after reconstruction.
- Candidate transaction: nine regular one-link files, exact basename set, result last, then reverse identity/nlink/SHA revalidation.
- Runtime boundary: `env -i`, `python3 -I -B -S`, fixed `/tmp` spill outside deliverables, no user site, no `PYTHONPATH`, and no bytecode writes.

The verifier does not import or execute the producer or any upstream producer
or verifier.  It independently consumes the pinned sealed artifacts as data.

## Exact corrected freeze

- Corrected members: `564,460`
- Corrected base roots: `367,948`
- Corrected components: `92,672`
- Corrected partition SHA-256: `1ae914d4e2cff22d1fa6ddad4ffe4679c594bde3cdad27acf1480202b7a89434`
- Remapped legal edge applications: `478,718`
- Invalidated R235D members: `32`
- Old affected roots/components: `20`
- Deleted singleton transitions: sixteen exact `1 -> 0` transitions
- Surviving rekey component sizes: `[5438, 5438, 5486, 5486]`, computed from the fresh component map
- All unordered member pairs: `159,307,263,570`
- Within-component unordered member pairs: `487,155,016`
- Cross-component pair denominator: `158,820,108,554`

The two ordered R248 owner-binding commitments are recomputed independently;
the verifier does not trust the producer frontier for either sequence.

## Full-row comparator receipts

- Member invalidation rows: `32`
- Old-root disposition rows: `367,964`
- Edge-remap application rows: `478,718`
- Fresh member/component rows: `564,460`
- Fresh base-root/component rows: `367,948`
- Fresh component-census rows: `92,672`

Every row is decoded under the strict canonical JSON grammar, checked for its
exact field set and row self-hash, compared to an independently generated row,
and included in ordered row-id, row-hash, row-wire, and uncompressed-stream
commitments.

## Coherent attacks

The final verifier-pinned attack suite rejects `24/24` attacks.  It covers
extra/missing files, candidate and result symlinks, hardlinks, both ordered
R248 owner commitments, producer pin substitution, all five pair-arithmetic
quantities, forward partition substitution, delete/rekey census substitution,
pre-verification credit injection, artifact-descriptor substitution, and
coherent corruption of each of the six gzip ledgers.

- Attack object SHA-256: `bc2649e92dab7f1271967ce1059d78f4287564db8d07f101db646a5913b8e787`
- Attack file SHA-256: `efd3631209c9cccdd8a3e43acebe99011687cbab2ccf67666ac2ae7a5013daad`
- Attack elapsed: `55:20.13`
- Attack peak RSS: `1,661,256 KiB`

## Verification and cold replay

- Verification object SHA-256: `2dd819ef665e3f8ac704700a3d47cf8a21aa59ab29d8817de1223fb6c6d046d6`
- Verification file SHA-256: `9aee2aae01d116c6c6967c4aec1a9d80c9728eff3d3bdc8f7fc4d836c9f07eb2`
- Verification elapsed: `22:19.54`
- Verification peak RSS: `1,609,820 KiB`
- Cold no-write elapsed: `21:40.81`
- Cold no-write peak RSS: `1,613,960 KiB`
- Cold no-write deliverables writes: `0`

The companion manifest is generated only after this report and the cold replay
record are fixed.  The final seal requires one subsequent manifest-first,
held-FD, no-write full replay whose recomputed verification bytes exactly equal
the published verification document.

## Credit boundary and next step

Upon a successful final manifest-first replay, Round306C0 may seal the corrected
DSU freeze only.  The old `92,688` component-bound AF2/B1A/B2 products remain
invalid.  The next admissible construction is Round306C1, rebuilding the six
support families from the `564,460 / 367,948 / 92,672` corrected base.  No
maximality or downstream CM2 claim follows from Round306C0 alone.
