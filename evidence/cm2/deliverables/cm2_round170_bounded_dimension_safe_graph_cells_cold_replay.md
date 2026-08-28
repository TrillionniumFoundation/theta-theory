# Round170 cold replay

Date: 2026-07-26

Environment:

```text
python: .venv-neurips/bin/python
python-flint: 0.9.0
Arb precision: 192 bits
```

Producer commands:

```text
PYTHONHASHSEED=17   .venv-neurips/bin/python \
  deliverables/cm2_round170_bounded_dimension_safe_graph_cells.py \
  --output /tmp/cm2_round170_seed17.json

PYTHONHASHSEED=1701 .venv-neurips/bin/python \
  deliverables/cm2_round170_bounded_dimension_safe_graph_cells.py \
  --output /tmp/cm2_round170_seed1701.json
```

Both outputs were byte-identical to the official certificate:

```text
1a6fbab5676dc7e5ec91e5222810e34cfcc788517681e67441a1046e45ac62b8
```

Verifier commands:

```text
PYTHONHASHSEED=23   .venv-neurips/bin/python \
  deliverables/cm2_round170_bounded_dimension_safe_graph_cells_verifier.py \
  --output \
  deliverables/cm2_round170_bounded_dimension_safe_graph_cells_verification.json

PYTHONHASHSEED=2301 .venv-neurips/bin/python \
  deliverables/cm2_round170_bounded_dimension_safe_graph_cells_verifier.py \
  --output /tmp/cm2_round170_verification_seed2301.json
```

Both outputs were byte-identical:

```text
962d0f3fb86031ebc31d0808c5d0afd112d8796261652c720e1920246700a9c6
```

The verification result digest was

```text
70510d463dac73ad7eee775b0f4e3792d24b90be8f984894b651cdb0e6412b8b.
```

Verdict: deterministic `PARTIAL` bounded exploration.  Cold replay does not
promote any Round170 child count or volume into the Round168 integer ledger.
