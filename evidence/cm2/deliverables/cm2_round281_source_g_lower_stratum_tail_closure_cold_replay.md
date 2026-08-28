# Round281 cold replay

Environment: project-local `.venv-cm2`, Python 3.12,
`python-flint==0.9.0`.

Commands:

```text
.venv-cm2/bin/python cm2_round281_source_g_lower_stratum_tail_closure.py \
  --seed 281071 --ledger /tmp/r281_a_ledger.json.gz \
  --output /tmp/r281_a_result.json
.venv-cm2/bin/python cm2_round281_source_g_lower_stratum_tail_closure.py \
  --seed 281929 --ledger /tmp/r281_b_ledger.json.gz \
  --output /tmp/r281_b_result.json
cmp /tmp/r281_a_ledger.json.gz /tmp/r281_b_ledger.json.gz
cmp /tmp/r281_a_result.json /tmp/r281_b_result.json
.venv-cm2/bin/python cm2_round281_source_g_lower_stratum_tail_closure_verifier.py
gzip -t cm2_round281_source_g_lower_stratum_tail_closure_ledger.json.gz
```

Both comparisons and all verification commands exited successfully.

Cold replay SHA256 values:

- ledger (both seeds):
  `ffa333f040551d583c6afd34a1b466fbc67fe0628683782d80f905329b800fc7`;
- result (both seeds):
  `84ea62964c4199bdec66f7a82cfdee964b8b2b610f9c8c1c6298cc6fbaf1942c`.

