# CM2 Round126 cold replay

Date: 2026-07-23

## Frozen digests

```text
producer             db5a3a4250e26bdeeb6ac4a2a6abade5014073b5901339e30d5c4b4907fcba68
certificate          5980d0714aade1d71b32d3fa280d157e98dc97cefca2dd1e8e614f5203a8897e
certificate result   0a15b8afe9e6434fa2766ffa55159b5f7944eb7d2a3d3a39a31d67261effd63a
verifier             2fa8136e0c07457486515bc7c342a4857ed61705f33c7a91bf681ab02905a9ec
verification         bfbee771cc25cfb623297fe5e5c63483cbd296c372c1c4a143b247c834046f4b
verification result  6ac2ff5a80d08b1e0a133599ca35836bd087b9c8a831ce9128a7225c0dba63fd
```

## Deterministic producer replay

Two complete producer runs used:

```text
PYTHONHASHSEED=0 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1
```

Both exited `0`.  Their outputs and the canonical certificate are
byte-identical with SHA256
`5980d0714aade1d71b32d3fa280d157e98dc97cefca2dd1e8e614f5203a8897e`.

## Deterministic verifier replay

The same two environments were used for full mutation-enabled verifier
runs.  Both exited `0`, returned `PASS`, and produced byte-identical
artifacts with SHA256
`bfbee771cc25cfb623297fe5e5c63483cbd296c372c1c4a143b247c834046f4b`.
The outer verification result digest recomputes to
`6ac2ff5a80d08b1e0a133599ca35836bd087b9c8a831ce9128a7225c0dba63fd`.

```text
semantic mutations                       38/38 rejected
strict-JSON attacks                      12/12 rejected
actual children                             24
rebuilt F1–F17 slots                      2040
new F18 slots                              120
stage slot counts                     48/24/48
combined child-local slots                2160
seed-local complete level blocks           120
seed-local complete child packets           24
```

## Negative cold paths

The CLI was run with a nonexistent certificate, a certificate whose CM2
verdict was changed without updating the digest, and a certificate whose
false `GO_FOR_CLAIM` result was fully re-signed.  Each run exited `1`; none
wrote its requested output.

This closes the earlier false-green condition in which an incomplete
verifier file had no entry point and therefore exited successfully without
performing verification.

## Safety replay

Both deterministic verification artifacts retain:

```text
seed-local child maturity                 18/18
global Gate5 maturity                     10/18
global complete 18-field blocks               0
Gate5 blocks                                  0
CM2                                 NO-GO_FOR_CLAIM
```
