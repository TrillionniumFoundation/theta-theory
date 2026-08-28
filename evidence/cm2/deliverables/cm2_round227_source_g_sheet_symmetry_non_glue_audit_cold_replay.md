# Round227 cold replay — 2026-07-27

Environment: Python `3.12.3`.

Commands:

```text
PYTHONHASHSEED=227041 python3 cm2_round227_source_g_sheet_symmetry_non_glue_audit_verifier.py --no-write
PYTHONHASHSEED=227919 python3 cm2_round227_source_g_sheet_symmetry_non_glue_audit_verifier.py --no-write
```

Both runs exited `0` with identical output:

```text
PASS_PARTIAL_FORMAL_ROUND227
result_sha256=1e5c854ea9adbf4ee2d0e4959b2a043d135136e90cd4babb4639661759fa15d9
verification_sha256=a0446082bb4f7c9b2f35885ce085237dfd2eec4789aa8447c0b0e85864d500e6
sheets=17716 directed_partners=35432 Klein_orbits=4429 orbit_size=4
semantic_attacks=10/10_rejected strict_JSON=16/16_rejected file_attacks=8/8_rejected
symmetry_as_glue_attack=rejected component_credit=0
```
