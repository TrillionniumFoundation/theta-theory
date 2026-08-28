# CM2 Round120 cold replay

Date: 2026-07-23

## Frozen code and logical digests

```text
producer             ea1b4cd78a8009063e87cfe09b0d3fa80097f430a1f742d5f109761c20973a9a
certificate          a7b9df3450268c9a812aff682520ae24b36970a0526bad9aad15431a79f288d5
certificate result   83289f6cd5cf02c1fd29f6f2975e2dee107866c0577da3690688937a6082791e
verifier             5d9c48807fdc540fc53970508bd377c911d98ec72b49a210a5ca05777b708a18
verification         ad5be920fc6864009f5d2966d41b9271419aa053866c5ac50d8d7186731c17bc
verification result  2f53a205da86e4d08f5f90812e0dcaa08fc73b0456b17f4e72f0bcc39623193e
```

## Producer replays

Two clean producer runs used different hash seeds and fixed locale/timezone:

```text
PYTHONHASHSEED=120731 LC_ALL=C TZ=UTC
PYTHONHASHSEED=981207 LC_ALL=C TZ=UTC
```

The canonical certificate and both temporary outputs have exactly the same
SHA256:

```text
a7b9df3450268c9a812aff682520ae24b36970a0526bad9aad15431a79f288d5
```

Both `cmp` checks pass.  The producer output is therefore byte-stable, not
merely logically equivalent.

## Independent verifier replays

The canonical 1024-bit verifier run and two additional full runs used:

```text
PYTHONHASHSEED=120917 LC_ALL=C TZ=UTC
PYTHONHASHSEED=731120 LC_ALL=C TZ=UTC
```

All three outputs have exactly the same SHA256:

```text
ad5be920fc6864009f5d2966d41b9271419aa053866c5ac50d8d7186731c17bc
```

Both temporary outputs compare byte-for-byte equal to the canonical
verification.  Every replay reports:

```text
verdict                         PASS
verification precision         1024 bits
independent parents             72
independent official legs       216
generator templates             112
recut frontier rows             216
F1-F4 slot rows                 2240
Round31 physical cores checked  24
nonempty R117 parents checked   24
semantic mutations rejected     49
strict-JSON mutations rejected  15
rank3 actual-child maturity     4/18
global Gate5 maturity           10/18
CM2                             NO-GO_FOR_CLAIM
```

The comparison is byte-for-byte and includes the ordered independent replay
rows and complete attack-label ledgers.

