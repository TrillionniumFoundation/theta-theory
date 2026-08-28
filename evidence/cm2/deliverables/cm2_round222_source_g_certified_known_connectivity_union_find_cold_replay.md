# Round222 cold replay — 2026-07-27

Environment: Python `3.12.3`, `python-flint 0.9.0`.

Command:

```text
../.venv-neurips/bin/python cm2_round222_source_g_certified_known_connectivity_union_find_verifier.py
```

Final status:

```text
PASS_PARTIAL_FORMAL_ROUND222
result_sha256=ef3a2e4b4c866e972db058ac4ad1c28dc8ea800582a3ebbcd8e59e9e33a0bb21
```

The final replay followed two fail-closed verifier repairs discovered during
the same cold audit: binding the false-contact-completion aggregate and the
outcome/oracle-dependency field, plus strict rejection of invalid Unicode
surrogates and non-integral JSON numbers.  After repair, all `15` semantic,
`16` JSON, and `10` file/path attacks were rejected.

