# CM2 Round306B1AF4K2R235D cold replay

All credited commands use `.venv-cm2/bin/python -I -B`; both programs fail
closed without isolated mode and disabled bytecode writes.

- producer no-write: rc `0`, `8:32.64`, peak RSS `2,489,112 KiB`;
- producer publish: rc `0`, `8:55.39`, peak RSS `2,486,632 KiB`;
- both fresh producer processes reproduced result object `abe7b63d...fbbe`,
  result file `3856a04a...e5ff`, and ledger `6eaeee6a...cfe0`
  byte-for-byte;
- independent verifier publish: rc `0`, `8:20.87`, peak RSS `2,485,052 KiB`;
  verification result `b0b43f4a...6867`, attack suite `27/27`.

The manifest-first sealed command is:

```text
.venv-cm2/bin/python -I -B \
  deliverables/cm2_round306b1af4k2r235d_source_g_double_endpoint_source_only_local_theorem_independent_verifier.py \
  --verify-no-write
```

It requires the package manifest before opening any of its eight payload
members, checks every manifest digest through held file descriptors, performs
two-pass/final-path revalidation, independently rebuilds the complete result
and ledger, requires the frozen attack and verification bytes, and publishes
nothing.
