# Round171 cold replay

Date: 2026-07-26

The producer was run under `PYTHONHASHSEED=17101` and `17103`.  Both outputs
were byte-identical to the frozen certificate.

The independent verifier was run against those two certificates under
`PYTHONHASHSEED=17107` and `17109`.  Both outputs were byte-identical to the
frozen verification.

```text
certificate sha256
1fb4827b42569d41602765445d0333c76b2ef97615873fc406563ac0e18af7a5

verification sha256
effdfd4306dbf7bd70df1e9b5ed9166a58dc00a5d333b0f2f2a5f0cb930ccce9
```

The replay used `.venv-neurips/bin/python`.  No earlier artifact was
modified.
