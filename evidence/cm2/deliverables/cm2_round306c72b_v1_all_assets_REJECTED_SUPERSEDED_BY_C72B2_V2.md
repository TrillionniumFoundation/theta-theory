# C72b v1 family rejected and superseded

The following v1 family is permanently non-consumable:

- `cm2_round306c72b_boundary_arrangement_chart_seam_oracle_v1.py`
- `cm2_round306c72b_boundary_arrangement_chart_seam_oracle_independent_verifier_v1.py`
- `.cm2-runtime/c72b-build-a.v1` (empty / no result)
- `.cm2-runtime/c72b-build-a2.v1` (interrupted partial / no result)

Final frozen rejected identities (SHA-256, after the fail-closed entry-point
guards were installed):

- producer source: `7ff6a4cb77a6a49151ededbaced2b3d698534de973d9b6a5d11b68a251d9ebd5`
- independent-verifier source: `76e99740913780acc41af225a29ea6d6e086fcf09b43b79369ab084d145596b4`
- `c72b-build-a.v1` sole partial member
  `cm2_round306c72b_boundary_arrangement_chart_seam_oracle_v1.jsonl.gz`:
  20 bytes, SHA-256
  `9ceffb7310338057cfe71a4ae1e2c98d2c485d81cdef906532a801f457a38d64`
- `c72b-build-a2.v1` sole partial member
  `cm2_round306c72b_boundary_arrangement_chart_seam_oracle_v1.jsonl.gz`:
  32,517,357 bytes, SHA-256
  `aa7184956b6bcf87cc7d1672165990ac6230cd0367385df323cb72a69d53f705`

These two exact directory/member identities are the complete rejected partial
stage set.  Any byte change, additional member, completion attempt, or renamed
copy is outside this rejection record and remains non-consumable.

The first stage failed a boolean guard before row publication.  The second
draft incorrectly typed the outgoing compact-chart seam itself as a physical
terminal.  Neither stage has a result object, verification, receipt, or any
credit.  Both are append-only rejection evidence and must not be completed,
renamed, overwritten, or pinned.  Only a fresh C72b2 v2 successor with exact
W-owned physical state glue may be considered.
