# K2G0 cold replay

Two seed-distinct cacheless verifier commands are required and deterministic:

```text
PYTHONHASHSEED=3064201 python -I -B cm2_round306b1af4k2g0_source_g_g2_semantic_authority_frontier_independent_verifier.py --verify --write
PYTHONHASHSEED=3064999 python -I -B cm2_round306b1af4k2g0_source_g_g2_semantic_authority_frontier_independent_verifier.py --verify --no-write
```

The second run must accept only byte-identical verification/report/cold/manifest
artifacts.  Runtime and maximum RSS are execution observations, not theorem
claims.  Availability/resource exhaustion cannot mint credit.
