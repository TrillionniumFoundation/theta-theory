# CM2 Round162 cold replay

Date: 2026-07-25

## Interpreter

Arb-dependent blocks use

```text
.venv-neurips/bin/python
python-flint 0.9.0.
```

The system `/usr/bin/python3` does not provide `flint` and is not a valid
replay interpreter for those blocks.

## Compact angular infrastructure

The producer and independent verifier were replayed to temporary outputs
under distinct hash seeds.  Both temporary files were byte-identical to the
frozen certificate and verification files.

```text
certificate file SHA256
f796617726a725577b7f28d499f1c68f91c278eef453cf698a2afe8d60248cf1

verification file SHA256
880a8b06af9243314d987493be631e4b3b8c4ff41c49c623ea85f5340e5c6214
```

## Compact-to-Gate3 coordinate bridge

The producer ran with `PYTHONHASHSEED=1301`; the verifier ran with
`PYTHONHASHSEED=3301`.  Both temporary outputs were byte-identical to their
frozen files.

```text
certificate file SHA256
7a9889bd306567d8f68b203cab54e6fd821dd303f801e61bd82d9f32e012e4fe

verification file SHA256
99b443650b5f74c508e25d982aa09b06632432bd9dd880f1364c69ff7afa1583
```

## Named-margin checkpoint

The 8,192-bit producer ran with `PYTHONHASHSEED=1709` and completed in
9 minutes 15 seconds.  The verifier ran with `PYTHONHASHSEED=2903` and
completed in 9 minutes 3 seconds.  Both temporary outputs were
byte-identical to the frozen files.

```text
certificate file SHA256
c721c884f9bf07c6e802d8fbed7d9ef24ddab22e698465502e4cfa2bcf76b8fb

verification file SHA256
97b2ef6f70fc3c4959ed25e7e7f219634ddd9044d30c0b951b8ee8a00eb25a8c
```

## Original W:W frozen-prefix block

The producer and independent verifier replay byte-identically under
different hash seeds.

```text
certificate file SHA256
927bc20ca139e5bd1756c0b35bb10a8dbdddad1dde09bb4e6f2f3e73ddd88980

verification file SHA256
a86f898d7457cec8a2f221a5ce257236cba065f58d1699e2caeacbddf44c42f3
```

## Unique-owner frozen-prefix block

The optimized producer replays only the two direct source-W 192-bit atlases
and obtains the other two by the pinned exact reflections.  The verifier
independently performs the same upstream reconstruction without importing or
executing the Round162 producer.

The frozen producer ran with `PYTHONHASHSEED=1901`; the verifier ran with
`PYTHONHASHSEED=3907`.  Both temporary outputs were byte-identical to their
frozen files.

```text
certificate file SHA256
9cf6e0a65659a6c835e476d283b48d3fcd3b29f450ca2bf1b71d66dfb695f97f

verification file SHA256
c7dda884faa817e5dbafc94756f01023eafe00def62de1676fa830d605e45b79
```

## Fail-closed correction

An initial full four-representative-atlas replay exited nonzero at a fixed
count assertion because a prose-only observation had stated 25,008
unique-owner mismatches.  No certificate was written by that failed run.

The corrected implementation derives every count from the pinned leaf rows.
The successful source-W replay establishes 25,028 mismatches and retains
1,176 owner-matching leaves as unresolved.  This correction changes no old
artifact and causes no status promotion.
