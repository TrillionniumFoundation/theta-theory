# Round306C42 f1 authority installation transaction

Installed: `2026-08-11 15:04 CST (+0800)`  
Verdict: `COMMITTED_C42_F1_AUTHORITY_TRANSACTION`  
CM2 verdict after installation: `NO-GO_FOR_CLAIM`

## Bound authority objects

- C42 formal candidate token:
  `c42-p391-formal-producer-20260811T044500Z-f1`
- C42 candidate object:
  `a50914a266aff3396054d7f16e91d69db7fa735ad15f01cbf07eee8e708d99d2`
- C42 candidate manifest file SHA256:
  `ce1b6260b26a901a9dda3cfbd94eba5a752b5188d6bdbe7c7d3cd7a4d3f7d058`
- C42 producer execution-receipt object:
  `e89f66d0e7636bfa781a6ef7e0309fc1ad00c3215ea699c08b231003e1c39f08`
- C42 independent-audit token:
  `c42-independent-audit-20260811T052900Z-p391-f1`
- C42 independent-audit object:
  `85a7cd719cee9dceb1763135f74d50bcf28f78ff2426e65996b975b1def7790c`
- Original C42 audit result:
  `54/54 attacks fail-closed`

The independent audit binds the f1 candidate and f1 execution receipt.  No
f2 or review-only directory was admitted.

## Installation transaction

- Installer source SHA256:
  `66f88bc5913af695691c5ae58be7938f94f3f68a9eeeeed32bcd96b37938c276`
- Independent transaction-auditor source SHA256:
  `a37bf76da4674831c90d4e5839e7134b7ebfd9167a0a60840996a331039a06e2`
- InvocationID:
  `c42-f1-authority-install-20260811T070000Z-v1`
- Installation receipt object:
  `c5f2eb78a0d9d717326bc57fb14df823ab3c5181e3e613a0327425c5e33e784e`
- Authority seal object:
  `b321552768a6aeae6c1d229e52b61ca0b4420314234e02e98366153d4156d460`

The logical transaction order was durable prepared receipt, candidate
pointer, audit pointer, and finally an authority seal.  The seal is the sole
semantic commit point; either compatibility pointer without the seal has no
formal authority.  Publication used `O_EXCL`, `O_NOFOLLOW`, file and parent
directory `fsync`, and `renameat2(RENAME_NOREPLACE)`.  Every transaction node
is a user-owned, single-link, mode-`0444` regular file.  The receipt directory
is mode `0500` with exact one-file inventory.

Before the real transaction, the installer passed 9/9 hostile self-tests,
the independent transaction auditor passed 8/8 hostile self-tests, both
pristine preflights passed, the C42 root manifest passed 8/8, and an isolated
72 MiB end-to-end clone completed installation and independent installed-state
audit in one invocation.

## Independent installed-state replay

The frozen transaction auditor returned:

```text
PASS_INDEPENDENT_C42_F1_AUTHORITY_SEAL_AUDIT__574_PAIRED__1150_UNRESOLVED
```

It independently replayed the C41 lineage, C42 f1 producer receipt, 54/54
original attacks, exact candidate and audit pointer bytes, prepared receipt,
absence of staging nodes, and the final seal binding.

Installed file SHA256 values:

```text
fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07  .cm2-runtime/c42-current-token
59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5  .cm2-runtime/c42-current-audit-token
0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d  .cm2-runtime/c42-current-authority-seal
3599494ff330a367a6c27ee57c19c01e86626428871d014c9153f290fdfc407f  .cm2-runtime/audit/c42-f1-authority-install-a50914a266af-85a7cd719cee-v1/installation_receipt.json
```

The installed-state audit can be replayed without writes with:

```bash
python3 deliverables/cm2_round306c42_f1_authority_transaction_independent_auditor_v1.py \
  --audit-installed \
  --expect-auditor-sha256 a37bf76da4674831c90d4e5839e7134b7ebfd9167a0a60840996a331039a06e2
```

## Formal census after commit

```text
EARLIEST_PREFIX_EXCLUDED                      75,386
TYPED_EVENT_GRAPH                                296
CONNECTED_TO_KNOWN                                 0
SOURCE_GRAZING_OR_CEMETERY                         0
UNRESOLVED_R1648_CONTINUATION                  1,150
total                                          76,832
unresolved_zero                                 false
```

C42 closes one representative and its exact reflected partner.  The formal
whole-cell boundary is therefore 574 paired coarse cells, 287 of 862
representatives, with 575 representative continuations remaining.  D02 stays
blocked; this installation does not authorize D03, mint D04, change Gate5
from 10/18, or authorize an unconditional CM2 claim.
