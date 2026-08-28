# CM2 Round 140 parent-W audit — cold replay

Date: 2026-07-24

## Replay isolation

A fresh temporary directory received only the Round140 producer, the
Round140 verifier, and the nine byte-pinned Round27/Round35/Round137/Round139
inputs.  Neither the existing Round140 certificate nor the existing
verification JSON was copied into the directory.

The producer was run there with `PYTHONHASHSEED=1`.  Its newly generated
certificate was compared byte for byte with the frozen workspace
certificate.

The verifier was then run twice, with `PYTHONHASHSEED=1` and
`PYTHONHASHSEED=987654321`.  The first output was compared byte for byte with
the frozen workspace verification artifact, and the two seed outputs were
compared with each other.

## Exact outcome

All three byte comparisons succeeded:

```text
clean producer certificate:
bb6283e2fccba194b47f9aa174e85594560ba88062ed57d06651003744755a79

clean verifier output, seed 1:
b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d

clean verifier output, seed 987654321:
b38306fb85e4a8a27d0339d95ff9e7ee3eabea044239972c719c926e0891782d
```

The replay independently reproduced:

```text
source/path tuple SHA256:
5cec1061ec331e8f37929dfb1b2b2a78757309ba60198d571abd9e8cf6c70ed9

incidence path SHA256:
a2669f5587b2c7c10dc0d18fe1db2516df2b2049a7bf8cd37292636cd9c6fbe7

2D rank decimal SHA256:
81ee4f795045d8478e621dbcaf2cba2437ccb168b34b770f995c012c0060927f

1D rank decimal SHA256:
fe02c53ca61c7ae9a81d189ffbf5d58cbae33ee16cb68e6248c65d5fc708c24d

natural short-cell k:
null
```

## Replay boundary

The replay establishes deterministic reconstruction from the frozen
Round27/Round35/Round137/final-Round139 chain.  It does not turn the
prospective contained ranks into historical labels and does not supply the
oriented maximal leaf endpoint needed for a natural `1e-90` index.
