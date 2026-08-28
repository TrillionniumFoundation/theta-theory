# Round295-C dual-seed cold replay

## Verdict

PASS.  Two producer seeds and two independent-verifier hash seeds reproduce
identical ledger, result, verification, and attack-suite commitments.  The
ledger passes `gzip -t`; all embedded self-hashes recompute exactly.

## Producer replays

```text
PYTHONHASHSEED=295301 python -B cm2_round295c_source_g_all_stratum_scope_composition_closure.py --seed 295301
PYTHONHASHSEED=295929 python -B cm2_round295c_source_g_all_stratum_scope_composition_closure.py --seed 295929 --no-write
```

| seed | time | peak RSS |
|---:|---:|---:|
| 295301 | 4:04.10 | 1,448,160 KiB |
| 295929 | 4:08.53 | 1,448,140 KiB |

Both runs report:

```text
ledger_file_sha256
24000c3f370d2ec9805dd9ecf0ad1e4fdc63c1a380d194d056cac92e28bb98d2

result_file_sha256
4d14262636260c96af56f0f7d0f0147c8d93bb2261c92c2b6ce6bb2758d2f71f

result_sha256
adb82bbacdf62d63c659921c4b4da7aaba35676c2cdf80f2e7ed06966c5d44a5
```

## Independent-verifier replays

```text
PYTHONHASHSEED=295371 python -B cm2_round295c_source_g_all_stratum_scope_composition_closure_verifier.py --seed 295371
PYTHONHASHSEED=295929 python -B cm2_round295c_source_g_all_stratum_scope_composition_closure_verifier.py --seed 295929
```

| hash seed | time | peak RSS |
|---:|---:|---:|
| 295371 | 3:48.75 | 1,383,468 KiB |
| 295929 | 3:53.04 | 1,384,228 KiB |

Both runs independently reconstruct all 9,528 relation rows and all eight
inventory rows, normalize 5,292 source-row references while retaining 6,156
already canonical references, prove the final 3,780-target universe, and
reject all 36 attacks.  They report:

```text
verification_file_sha256
4e37a5639fdc574d7a1d58e0dd3529780e379b17e39e2e48a2705bea1890a96c

verification_sha256
2f17dfb41ae55b4475566a0568729ec420e24872ac72eb688891f4042864b8ab

attack_suite_file_sha256
f767766fc080ccfb383b4943beff76b08b663b81bd1c9f650e57731441bcafe2

attack_suite_sha256
b30747f1b4b528c95393bd5ef8f67ba73edd265f155affbb3fb4c7d3efc8cb07
```

## Scope held fixed

Every replay keeps 431,208 registry rows, 46,564 representation
bindings/aliases, zero unresolved Round291/Round289 scope, and zero seam,
component, DSU, maximality, fibre, or disposition promotion.  Round296 remains
the sole owner of the complete 152 true-seam edge pairing.
