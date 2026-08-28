# Round295-A dual-seed cold replay

## Verdict

PASS.  Two producer seeds and two independent-verifier hash seeds reproduce
identical output commitments.  The three deterministic GZIP ledgers pass
`gzip -t`; the result, verification and attack-suite embedded self-hashes
recompute exactly.

## Producer replays

Initial writing run:

```text
python -B cm2_round295a_source_g_r291_positive_t_retained_continuation_closure.py --seed 295101
```

Second no-write replay:

```text
PYTHONHASHSEED=295929 python -B cm2_round295a_source_g_r291_positive_t_retained_continuation_closure.py --seed 295929 --no-write
```

Observed wall-clock and peak RSS:

| seed | time | peak RSS |
|---:|---:|---:|
| 295101 | 7:11.02 | 4,258,980 KiB |
| 295929 | 7:02.60 | 4,257,892 KiB |

Both runs report:

```text
representation_alias_ledger_file_sha256
5c826ef03dd6f8662528e565c36089422e590d1ebf9fc8bade99f1665c68ad2f

physical_incidence_ledger_file_sha256
2d9addfc9fca55366a58b29a7084c063674c3f556dd5398b038ae7d51fe97dcf

absence_ledger_file_sha256
9e28ee87b5a031a7f1c457d3fa26601925dbdf07dd5857c8e2108891891243b0

result_file_sha256
0deb8b9c88595762df3844b988af777a6b5f55347acbb8b9e8784308c2d4381d

result_sha256
117cc5c3629d4d2288e64c4c33307cb43cf0ff39889844907005e390edf47ce7
```

## Independent-verifier replays

```text
PYTHONHASHSEED=295171 python -B cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_verifier.py --seed 295171
PYTHONHASHSEED=295929 python -B cm2_round295a_source_g_r291_positive_t_retained_continuation_closure_verifier.py --seed 295929
```

Observed wall-clock and peak RSS:

| hash seed | time | peak RSS |
|---:|---:|---:|
| 295171 | 7:22.26 | 4,275,248 KiB |
| 295929 | 7:29.12 | 4,275,416 KiB |

Both runs independently reconstruct all 276 owner identities, all 431,208
registry rows/tranches, the complete 113,452 physical-incidence table, the
complete 28,016 absence table, and reject all 36 attacks.  They report
identical commitments:

```text
verification_file_sha256
1b5c3423ea3854a8ae206677c740f31f5f9133edf66926271a10eec96b052349

verification_sha256
7dfbdd9dac84857855f3af0007ae44226e9a0a2dd9329f1066eb984819c802ed

attack_suite_file_sha256
ecf3da6b5be1d6e790d39240ee93f5457651f7e3605c6388e05a69c9027ece16

attack_suite_sha256
34d47d2701a196372cd104988c0b8c4a7652c308081e555776e942f99e2ee088
```

## Scope held fixed

Every replay preserves 431,208 expanded occurrence IDs, adds zero occurrence
IDs, increases representation bindings only from 46,288 to 46,564, and closes
the Round291 unresolved census from 576 to zero.  No replay grants component,
DSU, seam, Jx/Jy, maximality, fibre or disposition credit.  The expanded
registry quotient remains null and not rebuilt.
