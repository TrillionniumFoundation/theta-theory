# Round306C30b scrubbed cold replay and write audit

## Frozen executables and input

```text
producer SHA256  = 003191131bff227453d07fa22ecd6e95b4f9d48e9ff74604ea4b7116f5818762
verifier SHA256  = 1776137520b1add49a218e6ccce680aaffdafc195c99ef7992c1a5ee31694b66
harness SHA256   = c00d45077511eb87bd650fea090cd5f01b285e6b68d42bab311f2051878eae5d
auditor SHA256   = 0309dc5710421a5e56b0d1b7b04ef2c5ccf971d054943dc6baf7765e512b76f8
sealed directory = deliverables/cm2_round306c30b_sealed
```

Only `.cm2-runtime/candidates/c30b-controlled-seed30630071` was used as the publication source. `.cm2-runtime/candidates/c30b-controlled-seed30630929` is the byte-identical determinism witness. Historical directories named `c30b-final-*` or `c30b-sealed-*` were not used.

## Controlled producer replay

The producer was run in a scrubbed environment with the pinned interpreter, `-P -s -B`, and two real `PYTHONHASHSEED` values:

| Seed | Elapsed | Peak RSS | Output comparison |
|---:|---:|---:|---|
| 30630071 | 327.76 s | 175,368 KiB | official |
| 30630929 | 333.62 s | 173,988 KiB | 4/4 byte-identical |

The four common SHA256 values are:

```text
6b48cd0ca3fd53f9fdd457cc3c1106055e12db4d4ad999fcfd1fc89ad36b95df  runtime attestation
4259fdaadfe1b5e1c0b7b315ef71fdae245bb3bbc45c5f814c4d4b7a670e8672  H-cell ledger
b015e5bd6a4ee01d71ac95765d07dcbc63c3888f0c8ff9205e2d8c688958c11b  result file
19edfece87d4f95e3e25a62d508654918c03ec879f574ab01854bde5bee4c6c9  whole-origin ledger
```

## Independent and attack replay

The frozen independent verifier passed against both controlled candidates. Its output status was:

```text
PASS_INDEPENDENT_C30B__688_H_CELLS__8_DELTA_FOLLOWUP_H__2_EXCLUDED__10_RESOLVED_MIXED__92_TO_80__D02_COMPOSITE_BLOCKED
```

The frozen attack harness reconstructed its mathematical reference once and rejected all 13 coherent corruptions with exact `Reject` types and expected reason prefixes:

```text
PASS_13_OF_13_COHERENT_CORRUPTIONS_REJECTED
```

## Published-copy syscall replay

The published copy was replayed with an empty environment except for an explicit allowlist:

```text
HOME=$AUDIT/home
TMPDIR=$AUDIT/tmp
LC_ALL=C
LANG=C
TZ=UTC
PATH=/usr/bin:/bin
PYTHONHASHSEED=30630137
PYTHONDONTWRITEBYTECODE=1
```

The interpreter was invoked as `python -I -B` for the read-only cold verifier. `strace 6.8` traced `%file`, write-family, truncate, copy, sendfile, and sync syscalls for the verifier and its runtime-auditor child.

Results:

```text
exit status                            0
elapsed                                931.17 s
peak RSS                               321,580 KiB
trace SHA256                           75253bee70c481caa219bcac912a533c0474c3d2ffe9206675b0615e8c409420
stdout SHA256                          08ca7566f90ea7599c7b9b765176ebe7c60cf95ff5cfb4da46fb22896ca1864c
stderr SHA256                          addac86a8584f1a097ddf37a779e30f2c573657e7323c9494dc0429b4504f7bf
stdout canonical newline JSON          yes
top-level stdout writes                1
auditor writes to anonymous pipe       1
progress writes to audit stderr        50
write-capable opens in protected roots 0
path mutations in protected roots      0
writes to protected-root file fds      0
historical C30b candidate reads         0
sealed copy byte identity               4/4
```

The 52 traced write calls are exactly the one top-level stdout write, the one auditor-to-parent anonymous-pipe write, and 50 progress writes to the temporary audit stderr file.

## Final manifest-first contract

The final publication is valid only if this exact order succeeds without changing any manifest member:

1. from `deliverables/`, run strict SHA256 verification of the 14-member C30b manifest;
2. only after 14/14 success, run the frozen verifier against `cm2_round306c30b_sealed` in the scrubbed environment;
3. require exit zero and stdout SHA256 `08ca7566f90ea7599c7b9b765176ebe7c60cf95ff5cfb4da46fb22896ca1864c`;
4. recheck the 14-member manifest and the exact four-file sealed directory.

Failure of any item leaves C30b unsealed and preserves the prior C30a `92`-origin official state.
