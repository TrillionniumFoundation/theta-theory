# Actual local primary execution

`receipt.json` is the unmodified receipt of the executed source-content run. It is primary-only and has null checkout/run fields. `logs.tar.xz` contains the eight actual command logs named in the receipt; extract it in this directory to compare their SHA-256 digests. Archive SHA-256: `f61f0dd2715b501c4526c3aac1befae6cc1cc8912dd8522a201a6f80bea09f8b`.

The source-content run passed 18,945 finite diagnostics and 19 contract checks, with matching normal/optimized output. It compiled a 12-page primary without final TeX diagnostics. It did not build the retained volumes, run a physical sensor, or certify the continuum proofs. The current hosted workflow has its own independent exact-checkout receipt and must not reuse this as a full-package pass.
