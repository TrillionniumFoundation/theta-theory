# CM2 Round124 cold replay

Date: 2026-07-23

## Frozen code and logical digests

```text
producer             084634863c9ecb9dd16fe1c16ef7ae286315525509b5d703df48359426a291a5
certificate          ec2df85d5caf87f4bd25fa70c32afc5893bfbb147c3d0af21b3be9bc09c62b3b
certificate result   fe8a0c7e2b25452246748b46e3a73b256b0942606e55568979e38b7815ad2124
verifier             4a964cc016cee5de5cc42469bee96f87f61803f46973da24084e79a02e770a3f
verification         3c1987adcefd7986128b5a35c77babd3c00f760ef28d8b73f491961f0dff0ccd
verification result  a6363cd73600666a4be15e58df71682724bc2176624681ebc92713df3469eae8
```

## Producer replays

Two complete producer runs used fixed locale and timezone, disabled bytecode
writes, and distinct hash seeds:

```text
PYTHONHASHSEED=124731 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=731124 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
```

Both producer processes exited with status `0`.  The canonical certificate
and both replay outputs have exactly the same SHA256:

```text
ec2df85d5caf87f4bd25fa70c32afc5893bfbb147c3d0af21b3be9bc09c62b3b
```

All three pairwise `cmp` checks return `0`.  The comparison covers the closed
canonical JSON envelope, all 72 family-leg rows, all 72 relative
zero-cemetery rows, all 120 F15 slots, all nested row digests, the 1920-key
combined ledger, and the outer result digest.

## Independent verifier replays

Two complete mutation-enabled 3072-bit verifier runs used the corresponding
producer replay certificates:

```text
PYTHONHASHSEED=124307 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=307124 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
```

Both verifier processes exited with status `0`.  The canonical verification
and both replay outputs have exactly the same SHA256:

```text
3c1987adcefd7986128b5a35c77babd3c00f760ef28d8b73f491961f0dff0ccd
```

All three pairwise `cmp` checks return `0`.  Both replay outputs strict-parse
as canonical JSON and satisfy:

```text
status                                     PASS
verification precision                    3072 bits
upstream byte pins                          32
family-leg operator rows                    72
relative zero-cemetery rows                 72
tagged stage-3 payload members             216
new F15 full-key slots                     120
stage slot counts                     48/24/48
combined child-local slots                1920
F15 one-step value                          34
semantic mutations rejected           154/154
strict-JSON mutations rejected           15/15
rank3 seed-child maturity                16/18
remaining child fields                 F17,F18
global Gate5                            10/18
complete 18-field blocks                     0
Gate5 blocks                                 0
CM2                                NO-GO_FOR_CLAIM
```

The canonical producer, certificate, verifier, and verification hashes were
fixed before the replay documentation and manifest were created.  No
provisional artifact is included in the seven-entry freeze pack.
