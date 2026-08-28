# K2P0 cold replay

Commands:

```text
python -B cm2_round306b1af4k2p0_preserved_nongraph_authority_frontier_producer.py --full-replay
env PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=731 python -I -B cm2_round306b1af4k2p0_preserved_nongraph_authority_frontier_independent_verifier.py
```

Producer replay: exit 0; wall 1:23.20; peak RSS 636,056 KiB; ledger payload SHA-256 `bfb94eb3949182687df3342d4fe3e542e4f2eb46b33ffcb96d60da8ee987100f`.

Independent replay: exit 0; wall 1:29.90; peak RSS 634,896 KiB; result SHA-256 `73b1f768da3f5522f7f8addf757e767f524f1c2f055ffd3e83e1d101835a9b8c`.

Final type-strict replacement replay: self-test 4/4 passed, including explicit `false != 0` credit and `true != 1` count regressions; exit 0; wall 88.54 s; peak RSS 635,464 KiB; result SHA-256 remained `73b1f768da3f5522f7f8addf757e767f524f1c2f055ffd3e83e1d101835a9b8c`.  The earlier verifier and manifest hashes are superseded by this replacement.

Both replays preserve `formal_credit=0`, `normalized_full_support_credit=0`, `B1A_credit=0`, and `CM2_credit=0`.
