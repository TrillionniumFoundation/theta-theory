# Round289 cold replay

Environment:

- project-local `.venv-cm2`;
- Python 3.12.3;
- `python-flint==0.9.0`;
- Linux x86_64.

Commands:

```text
.venv-cm2/bin/python \
  deliverables/cm2_round289_source_g_outgoing_seam_tail_child_materialization.py \
  --seed 289071 \
  --output /tmp/cm2-r289-a.json \
  --ledger /tmp/cm2-r289-a.json.gz

.venv-cm2/bin/python \
  deliverables/cm2_round289_source_g_outgoing_seam_tail_child_materialization.py \
  --seed 289929 \
  --output /tmp/cm2-r289-b.json \
  --ledger /tmp/cm2-r289-b.json.gz

cmp /tmp/cm2-r289-a.json /tmp/cm2-r289-b.json
cmp /tmp/cm2-r289-a.json.gz /tmp/cm2-r289-b.json.gz
gzip -t /tmp/cm2-r289-a.json.gz
gzip -t /tmp/cm2-r289-b.json.gz
```

Both comparisons and both gzip integrity checks exited successfully.  The
seed is accepted as a replay parameter but does not affect output bytes.

Cold replay SHA256 values:

- result, both seeds:
  `9091e06b8aca3d5e883621e0e3f701a6b90ce2f02b84f6813cef7727f45c516c`;
- ledger, both seeds:
  `6c5680574c17d50749d39fb25970b7fbcbc677f4f73029aca833f549c0ef5001`.

The result's canonical object digest, excluding its own digest field, is:

`4b572fccb1963b4bfd4caa51d0915f3e1882e64ef6192491ccfbbd0fd76b2ac7`.

The replay establishes deterministic producer bytes only.  It does not
replace the required independent reconstruction from frozen upstream inputs
and does not authorize occurrence, seam-edge, or component credit.

