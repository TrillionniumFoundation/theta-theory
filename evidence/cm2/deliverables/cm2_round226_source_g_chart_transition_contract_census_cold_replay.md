# Round226 cold replay — 2026-07-27

Environment: Python `3.12.3`.

Commands:

```text
PYTHONHASHSEED=226041 python3 cm2_round226_source_g_chart_transition_contract_census_verifier.py --no-write
PYTHONHASHSEED=226919 python3 cm2_round226_source_g_chart_transition_contract_census_verifier.py --no-write
```

Both runs exited `0` and produced identical output:

```text
PASS_PARTIAL_FORMAL_ROUND226
result_sha256=a4f156431e310c9d322381b828a8225d070b0704935240d2d5e1a53d00fbc2b0
verification_sha256=b49d6c65df01851096682a1d1226d096a638ef38c3a0973ee898cc2c095a72e1
semantic_attacks=12/12_rejected strict_JSON=16/16_rejected file_attacks=8/8_rejected
contracts=16 candidates=9830 coordinate_only_no_event_sheet_endpoints=9830
```

