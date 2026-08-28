# Round285 cold replay

The producer was executed twice from the pinned frozen inputs:

```text
seed 285071
seed 285929
```

Both runs produced byte-identical artifacts:

- result:
  `132d6ab861b1ffb0e718d6e79136db8a5acd4b53dafde5b02dcdcc4ad019e6b0`
- deterministic GZIP ledger:
  `92462778ad249c5aff2d7a8d0205efa288ccaf191ab8a419c8b6f58a18dfcc1e`

Checks:

- deterministic seed replay: PASS;
- result object SHA256: PASS;
- ledger row count `152`: PASS;
- ledger rows SHA256: PASS;
- `gzip -t`: PASS;
- formal seam edges `0`: PASS;
- formal DSU rank credit `0`: PASS;
- `Jx/Jy` same-point glue credit `0`: PASS.
