# Round306B1AF4K2I1 R2 mechanical index cold replay

## Boundary

This replay covers only the R2 mechanical identity, representation-handle, owner,
and anti-join lane. It does not prove normalized full support, physical incidence
or equivalence, global representation set equality, B1A, B2, maximality, fibres,
global disposition, Gate5, or CM2.

Runtime: Python 3.12.3 on Linux 7.0.0-28-generic x86_64.

## Producer replay A

- Hash seed: 17
- Exit status: 0
- Wall time: 9:17.29
- Peak RSS: 101,996 KiB
- Result-object digest:
  3b67011a050d3283618305512d25acc03463724f29b1e41bdcfd6263496b8bf1

## Producer replay B

- Hash seed: 2305843009213693951
- Exit status: 0
- Wall time: 12:36.42
- Peak RSS: 98,424 KiB
- Result-object digest:
  3b67011a050d3283618305512d25acc03463724f29b1e41bdcfd6263496b8bf1

The following four artifacts were byte-identical across both seeds:

| Artifact | Bytes | SHA-256 |
|---|---:|---|
| member index | 202,108,710 | 7a114486eb75e654ed0077a63131acdde489c1a48010dd001da713eb8e9c2745 |
| representation index | 205,461,955 | 28dccab4f9bbba76171329fb4c55328592e8264686d14d2b47da8efc39867aca |
| W-tail blocked-obligation index | 2,782 | bd2e1e06d6ca5219ddbd2128ad42903a4c12f0328ed273e7a5576981c21e2e3a |
| result | 9,160 | 65ed7a13792edfe7609662126e4357b9e1ebff39b7d749a959b5a19cb3d5e96a |

## Independent receipt publication

- The verifier statically pinned the producer bytes but did not import or execute
  the producer.
- It reopened and held the producer, result, all three output ledgers, and all ten
  raw authorities from snapshot through verification publication and final path
  revalidation.
- It independently rebuilt all source joins and all expected rows.
- Exit status: 0
- Wall time: 9:35.06
- Peak RSS: 67,628 KiB
- Verification-document digest:
  44ff0bceeacaad7fcabc9c531c3da496ca7b0f417ba30370487eb1d80e7f9f7b
- Published verification-file SHA-256:
  5aa7f0e436835ac427cedd3c214d268832ac84894c519c920c5e42956c5f8280

The published verification document contains no wall time, RSS, timestamp, random
identifier, or environment-dependent path.

## Final strict no-write replay

Frozen verifier SHA-256:

    4841577e162bb73763fec8dcbd1eed809cb9df15650b1210437578dc4f373104

The final CLI separates the modes:

- --verify performs the complete reconstruction and is strictly no-write.
- --verify-and-publish is the only mode that can publish a receipt.

The final --verify replay reproduced the exact census, all eight ordered table
commitments, all zero anti-joins, all three ledger hashes and sizes, every row,
and every known gap.

- Exit status: 0
- Wall time: 10:00.38
- Peak RSS: 65,744 KiB
- Verification-document digest:
  44ff0bceeacaad7fcabc9c531c3da496ca7b0f417ba30370487eb1d80e7f9f7b

Before and after that replay, all 11 same-prefix files were snapshotted by SHA-256,
size, mtime, ctime, and inode. The two complete snapshots were byte-identical.
Only the explicitly rooted temporary database under /tmp was created and removed.

## Regression tests

Producer and frozen verifier self-tests both exited 0. The independent verifier rejected
ten recursive bool/integer alias mutations, four cross-certificate input-binding
collisions, three strict-JSON grammar attacks, a closed-row mutation, false versus
zero, true versus one, and a decoded canonical row one byte beyond the 8 MiB cap.
It accepted the exact 8 MiB boundary.

## Credit boundary

All formal-credit fields are exactly integer zero. In particular, the four W-tail
two-cell members are emitted only as blocked obligations. No replay result upgrades
them into physical reglues or full-support witnesses.
