# C11b cold replay

The producer was executed with `python3 -I -B` under an environment reduced to `PATH`, `LANG=C`, `LC_ALL=C`, and `TZ=UTC`.

Cold output was byte-identical to both ordinary candidate seeds:

- interface ledger: `815ed3b2ab73b3165e203cf8215421c89412b6d4f5190b816cb0d2e02f409a59`
- relation ledger: `37155fe874b8f4acd49773c013f4ec605a2f9388a0d1eb7443c88a731f1e0299`
- result: `0b6ac3d0107ec39d4d7313d731b0d719eb1d8338930fbafd9f6d651c1493260e`

The independent verifier passed the formally published bytes, and the published-byte attack suite rejected 8/8 coherent mutations.
