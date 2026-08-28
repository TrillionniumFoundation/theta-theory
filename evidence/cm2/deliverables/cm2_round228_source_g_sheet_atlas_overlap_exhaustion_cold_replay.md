# Round228 cold replay — 2026-07-27

Environment: Python `3.12.3`.

Commands:

```text
PYTHONHASHSEED=228041 python3 cm2_round228_source_g_sheet_atlas_overlap_exhaustion_verifier.py --no-write
PYTHONHASHSEED=228919 python3 cm2_round228_source_g_sheet_atlas_overlap_exhaustion_verifier.py --no-write
```

Both runs exited `0` with identical output:

```text
PASS_PARTIAL_FORMAL_ROUND228
result_sha256=5eb0af344cb14154f97c1c7baa4972011e0ed5a2f180c419d628d95ed0d41654
verification_sha256=121250e31c5832d775f165ea63fb68d40fcc445865d62367600138febc642976
sheets=17716 source_seam_candidates=0 outgoing_unique_owner=17716 unclassified=0
semantic=10/10 JSON=16/16 file=8/8 new_component_credit=0
```

