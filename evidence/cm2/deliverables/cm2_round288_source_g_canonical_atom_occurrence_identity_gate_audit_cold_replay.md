# Round288 cold replay

The cacheless producer was executed twice from the pinned frozen inputs:

```text
PYTHONHASHSEED=288071 --seed 288071
PYTHONHASHSEED=288929 --seed 288929
```

Both executions produced byte-identical artifacts:

- result:
  `9b5875777f3937efe05a4d871a8c8b76c92ca69d0f636eb014542f59dfe49569`;
- atom-disposition ledger:
  `6b0a8aa1cd38019322a61f5aaefc936006d10769cd21a5c8df374576f9ac570a`;
- existing-overlap ledger:
  `d76d27c436735511dc34056d9237a2772decd30129e3019b74c5a02a118ab24e`.

The embedded result-object SHA-256 is
`b8f07b3ed53afc2f011bcb241d3946bf77f00d4dc58190874baf8f3043234e78`.

The standalone cacheless verifier was then executed independently twice with
the workspace `python-flint==0.9.0` environment:

```text
PYTHONHASHSEED=288071 .venv-cm2/bin/python ..._verifier.py --seed 288071 --processes 16
PYTHONHASHSEED=288929 .venv-cm2/bin/python ..._verifier.py --seed 288929 --processes 16
```

Both runs exited `0` with status
`PASS_INDEPENDENT_CACHELESS_ROUND288__332020_SOURCE_ROWS__332016_ATOMS__126468_EXISTING_GEOMETRIES__36680_EXACT_ALIASES__295336_DISJOINT_CANDIDATES__661448_CORRIDORS_FRESHLY_DYNAMICALLY_VERIFIED__ZERO_CREDIT`.
Their `9,874`-byte verification outputs were byte-identical to one another and
to the frozen verification artifact.  The verification file SHA-256 is
`f08749d2f90ea63a696c482a342489c12e2c86436734a59c6a2e2b79d9cf9b23`;
the embedded verification-object SHA-256 is
`1bff07352d0b58eff1220d58f389939eb0956d0e22926c4c630d0e03358f0cd6`.

Checks:

- deterministic dual-seed byte replay: PASS;
- independent verifier dual-seed byte replay: PASS;
- all `330,724` Round279 face edges structurally rebound: PASS;
- all `661,448` positive-volume rational corridors freshly dynamically
  verified: PASS;
- all `26` targeted re-signed attacks rejected: PASS;
- all `332,016` atom dispositions reconstructed: PASS;
- `36,040` Round208 identities preserved: PASS;
- `640` Round204 aliases found: PASS;
- `274,176` pinned-corridor candidates partitioned: PASS;
- `21,160` isolated inner-support residuals retained fail-closed: PASS;
- distinct same-chart/same-signature positive-volume atom overlaps `0`: PASS;
- both deterministic gzip ledgers pass `gzip -t`: PASS;
- formal occurrence/component/maximality credit `0`: PASS;
- true-seam and `Jx/Jy` same-point glue credit `0`: PASS.
