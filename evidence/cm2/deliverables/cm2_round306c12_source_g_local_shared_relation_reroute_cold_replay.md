# C12 cold replay

The producer ran under `python3 -I -B` with an environment reduced to `PATH`, `LANG=C`, `LC_ALL=C`, and `TZ=UTC`.

Cold and both ordinary seeds were byte-identical:

- reroute ledger: `37c99c69907d57375d07803d651ac9b878db8bb25c33501b8b7846ccc45bbef5`
- result: `da77e963ec0a1e2bfef84dd5cf333484e47fd5ffe9ca946c6b77c1a762c10661`

The formally published bytes passed the independent verifier. Eight coherent mutations were rejected.
