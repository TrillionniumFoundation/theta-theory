# CM2 Round126 — exact-seed operator-phase registration and child-local F18

Date: 2026-07-23

Verdict: **VERIFIED exact-seed structural F18 on all 24 Round121 children;
seed-local maturity is 18/18.  Global Gate5 remains 10/18 with zero complete
blocks.**

## Certified payload

Round126 joins every pre-existing exact-seed F1–F17 slot to one immutable
full key and installs one structural F18 row on that same key.

```text
Round121 exact-seed children                         24
standard-family child/stage carriers                72
F1–F17 same-key map rows                           120
rebuilt pre-existing F1–F17 slots                 2040
new F18 slots                                      120
combined child-local slots                        2160
F18 stage-level census                        48/24/48
seed-local complete 18-field level blocks          120
seed-local complete 18-field child packets          24
```

The 120 base keys are exactly the five symbolic roof levels on each child:
two at stage 0, one at stage 1, and two at stage 2.  The verifier checks this
`2/1/2` census separately on every one of the 24 children; the aggregate
`48/24/48` count alone is not accepted as a substitute.

## Exact phase arithmetic

For stage return length `r` and roof level `0 <= j < r`, the registered
direct-standard-`N` identity is

```text
prefix  = z^j
suffix  = z^(r-j)
block   = z^j z^(r-j) = z^r.
```

The three stage lengths are derived from the frozen carrier rows as
`[2,1,2]`.  Their sum is `5`, so each exact-seed child packet has the
structural identity

```text
z^2 z^1 z^2 = z^5.
```

This is a symbolic phase registration.  It does not prove that the symbol
`z` is an actual operator composition on a global Banach space, Wiener
invertibility, aperiodicity, or Kac return-wide closure.

## Same-key binding

Each of the 120 map rows independently binds:

- one official return-word key;
- one refined physical homogeneous subbranch;
- one roof level;
- one Round121 child, stage, and materialized recut;
- one Round125 standard-family carrier whose roof split adds no extra family
  factor; and
- exactly one source slot for every field F1 through F17.

The F14 row is cross-linked to the same-key F10/F13/F16 rows, F15 to the
same-key F7/F14 rows and operator carrier, and F17 to the same-key F11/F15
rows.  The new F18 row binds the hash of that complete F1–F17 map.  All 2040
pre-existing slot IDs and all 120 new F18 slot IDs are unique and disjoint.

## Independent verification

The verifier does not import or execute the Round126 producer.  It
strict-parses byte-pinned Round121, Round122, Round125, and Round125
verification artifacts, reconstructs all maps and F18 rows, and compares the
closed result exactly.

```text
status                         PASS
semantic mutations rejected   38/38
strict-JSON attacks rejected   12/12
producer SHA256                db5a3a4250e26bdeeb6ac4a2a6abade5014073b5901339e30d5c4b4907fcba68
certificate SHA256             5980d0714aade1d71b32d3fa280d157e98dc97cefca2dd1e8e614f5203a8897e
certificate result SHA256      0a15b8afe9e6434fa2766ffa55159b5f7944eb7d2a3d3a39a31d67261effd63a
verifier SHA256                2fa8136e0c07457486515bc7c342a4857ed61705f33c7a91bf681ab02905a9ec
verification SHA256            bfbee771cc25cfb623297fe5e5c63483cbd296c372c1c4a143b247c834046f4b
verification result SHA256     6ac2ff5a80d08b1e0a133599ca35836bd087b9c8a831ce9128a7225c0dba63fd
```

Valid, missing, stale-digest tampered, and fully re-signed semantic-tampered
certificates were exercised through the CLI.  Only the valid certificate
returned zero or wrote an output artifact.  Two independent hash-seed
replays were byte-identical for both producer and verifier.

## Frozen safety boundary

Round126 certifies only the one exact analytic seed used by Round121:

```text
rank-3 seed-child maturity             18/18
global Gate5 maturity                  10/18
global complete 18-field blocks            0
Gate5 blocks                               0
CM2                              NO-GO_FOR_CLAIM
```

In particular, the 120 level blocks and 24 child packets are not global
physical blocks.  They do not cover arbitrary return depth, all Borel word
keys, the global owner/cemetery ledger, raw `Z_col` or power-Orlicz recovery,
or an all-input anisotropic current recipient.

The next honest route is a local-to-global coverage join against the frozen
441,280-key return-word envelope, followed by fieldwise global deficit
ledgers.  No local count may be aggregated into a Gate5 promotion.
