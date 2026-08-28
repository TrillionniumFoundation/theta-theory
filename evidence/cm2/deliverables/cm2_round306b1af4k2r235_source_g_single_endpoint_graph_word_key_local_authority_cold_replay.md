# CM2 Round306B1AF4K2R235 cold replay

All credited runs use `.venv-cm2/bin/python -I -B`; both programs fail closed
without Python isolated mode and disabled bytecode writes.

- producer, `PYTHONHASHSEED=235071`, isolated publish: rc `0`, `1:51.84`, peak
  RSS `2,008,924 KiB`;
- producer, `PYTHONHASHSEED=235929`, isolated no-write: rc `0`, `1:50.83`, peak
  RSS `2,010,184 KiB`;
- both seeds reproduced result object `066abcdc...330ee`, result file
  `ff907604...65f8a`, and ledger `904d6504...109f5` byte-for-byte;
- independent verifier, `PYTHONHASHSEED=235929`, isolated publish: rc `0`,
  `2:31.67`, peak RSS `2,395,776 KiB`; verification result
  `74ba8a89...a8cb5`, attack suite `13/13`.

The final sealed command is:

```text
PYTHONHASHSEED=235071 .venv-cm2/bin/python -I -B \
  deliverables/cm2_round306b1af4k2r235_source_g_single_endpoint_graph_word_key_local_authority_independent_verifier.py \
  --verify-no-write
```

It requires the package manifest before opening package payloads, recomputes
all `38,344` rows, requires the frozen attack and verification bytes, and
publishes nothing.  Package-file hashes, sizes, inode identities, mtime_ns,
and ctime_ns are checked externally before and after that command.
