# Round225 cold replay — 2026-07-27

Environment: Python `3.12.3`.

Commands:

```text
PYTHONHASHSEED=225052 python3 cm2_round225_source_g_certified_connectivity_rebuild_verifier.py --no-write
PYTHONHASHSEED=225997 python3 cm2_round225_source_g_certified_connectivity_rebuild_verifier.py --no-write
```

Both runs exited `0`; their stdout was identical:

```text
PASS_PARTIAL_FORMAL_ROUND225
result_sha256=979456672f3a2bcf535f907a969a9803223f27efa78d9c6f71682e4260ee3534
verification_sha256=160f8f038edc954361a70ae90a3feed13d299e4e218f5cd5e01482af26736b51
semantic_attacks=12/12_rejected
strict_JSON_attacks=16/16_rejected
path_and_file_attacks=10/10_rejected
producer_imported_or_executed=false
blocks=7640->7404
maximal_physical_component_credit=0
```

