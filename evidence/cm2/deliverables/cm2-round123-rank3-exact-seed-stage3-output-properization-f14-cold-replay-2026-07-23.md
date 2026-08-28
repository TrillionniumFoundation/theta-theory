# CM2 Round123 cold replay

Date: 2026-07-23

## Frozen code and logical digests

```text
producer             e00b85d722e3784c0c2427ea0f7b32f8306b9d706b902b22df334b8aa9b00c38
certificate          d3d45e32e45d1a37d5364c0d5fc1f34b537190c2450b7e8f9ead729dc77fe993
certificate result   e3ebade59b4bf8672f72f960a3fe0c13364ee27cd22f3ffe048b0ba7debd8296
verifier             eec966baae120a442f621e03f4575161545fc6d65604aba5f255a440c90f0625
verification         37b70e60e1b9a66875e4565a44c115d50f55d718320fa79187d26bc45a1136d6
verification result  8786d225f86c213cab626229d6220f54f7f7a5e09a15d5e8850e52fd0f32142b
internal helper      8eda085e342655f20ef68a7aa0554b3bed3c26312d1261c49d4f6567d0bbb9e0
```

The common helper is an internal producer/verifier pin.  It is deliberately
not an eighth entry in the top-level direct-assault manifest.

## Producer replays

Two complete 1536-bit producer runs with 240 root bisections used the
workspace Python environment containing `python-flint`, fixed locale and
timezone, disabled bytecode writes, and distinct hash seeds:

```text
PYTHONHASHSEED=123731 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=731123 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
```

The canonical certificate and both temporary outputs have exactly the same
SHA256:

```text
d3d45e32e45d1a37d5364c0d5fc1f34b537190c2450b7e8f9ead729dc77fe993
```

All three pairwise `cmp` checks pass.  The comparison covers the 192
third-output endpoints, 193 natural cells, 215 merged cuts, 216 output
fragments, 24 partitions, 72 leg-output rows, 120 F14 slots, all nested row
digests, and the closed result digest.

## Independent verifier replays

Two complete mutation-enabled 3072-bit verifier runs used:

```text
PYTHONHASHSEED=123307 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=307123 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
```

The canonical verification and both replay outputs have exactly the same
SHA256:

```text
37b70e60e1b9a66875e4565a44c115d50f55d718320fa79187d26bc45a1136d6
```

All three pairwise `cmp` checks pass.  The semantic and strict-JSON attack
label arrays are also exactly byte-for-byte equal to the canonical
verification arrays:

```text
semantic labels       110 = 110
strict-JSON labels     15 = 15
```

Every replay reports:

```text
verdict                                  PASS
verification precision                  3072 bits
upstream/helper pins                     27
third-output internal cuts              192
third-output natural cells              193
merged internal cuts                    215
third-output fragments                  216
input child partitions                   24
physical-leg output rows                 72
new F14 full-key slots                  120
combined child-local slots             1800
F14 one-step slot value                  34
generic three-leg composition         39304
direct exact-seed three-leg bound        34
semantic mutations rejected         110/110
strict-JSON mutations rejected        15/15
rank3 seed-child maturity             15/18
remaining child fields          F15,F17,F18
global Gate5 maturity                 10/18
complete 18-field blocks                  0
Gate5 blocks                              0
CM2                             NO-GO_FOR_CLAIM
```

The canonical producer, certificate, verifier, and verification hashes were
fixed before these replays began.  No provisional verifier or verification
digest is included in the freeze pack.
