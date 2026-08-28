# C48 pair-668 generation-1 successor installation transaction v1

Date: 2026-08-11 (Asia/Shanghai)

Verdict: `COMMITTED_C48_PAIR668_GEN1_TASK_SUCCESSOR_AUTHORITY__ONE_AUDITED_TASK_LEVEL_SUCCESSOR__ZERO_D02_GATE_CREDIT`

CM2 remains `NO-GO_FOR_CLAIM`.  This transaction installs one narrow,
independently audited task-level successor.  It does not modify C42, update
the canonical status, promote D02-A, or award ambient, whole-parent, coarse,
terminal, or D02 gate credit.

## Frozen evidence

- Producer source SHA-256:
  `a16d8802288c021d6d153942df15c7e7f0078628f5fb2c29eb927c6e9b94a7b8`
- Candidate file SHA-256:
  `5f356dd0b1bb9ded56548a8b046f2401ad59bf706c253d44dd151649035d283e`
- Candidate object SHA-256:
  `61de17d0a8122a4a03af34cf832cd717fdb715cd9c4cd2fac4162bdab8ddceab`
- Generation-1 successor checkpoint object SHA-256:
  `bbd909cad5a5d0b9cc44362be6acb26d527f86edc1b8191c06a246a514c9c984`
- Candidate report SHA-256:
  `57c6cacc057e13deae78379cb123be136ec03a33d79e2b8f6c54da4cf6f0af7c`
- Independent verifier source SHA-256:
  `e407758719341b69579dec3c73527c441c467b68f9e838dae7c7c4e0cf750a49`
- Independent audit file SHA-256:
  `9c06b31de75e8c751b3d3315f6f9be55e99f5551ae922ab01fdbb01e21327879`
- Independent audit object SHA-256:
  `cf0531127a5cd29625f9bf301646845a3b777d5f2ea973a6d2e085e9ffec380c`
- Independent audit report SHA-256:
  `e6696ab420ce19f914386df77f27e81ab378ed7052288fd465159b48b88c732a`

The cold verifier returned
`PASS_INDEPENDENT_C48_PAIR668_TWO_SIDE_ROUTE_MARGIN_FULL_GLOBAL_OWNER_AND_GEN1_SUCCESSOR_AUDIT__ZERO_FORMAL_CREDIT`.
It replayed six strict terminal margins, two full-universe traversal orders,
91,879 C41 rows / 183,758 baseline physical occurrences / 183,762 overlay
occurrences, reflection-owner equivariance, all 514 successor states, and
32/32 coherent attacks.

## Transaction

- Installer source SHA-256:
  `7c1c01d38d128bfe2556cc2b00574bfc280736c640e44bd63ab457352dfa9853`
- Release ID:
  `c48-pair668-gen1-bbd909cad5a5-cf0531127a5c-v1`
- Candidate token:
  `c48-pair668-gen1-bbd909cad5a5-61de17d0a812-v1`
- Audit token:
  `c48-independent-audit-cf0531127a5c-v1`
- Prepared installation receipt object SHA-256:
  `90e698b52b95a229805a5e800dd65bc7615998647564f5161b601c26e2b5b299`
- Installation receipt file SHA-256:
  `00338955b3225d96670806ab482775313e0afb68ebf7cafe01608787d828561b`
- Authority seal object SHA-256:
  `95297adbe0d2ee86788008046bc47c337a9c7a3fa0e46bd896e674a2931ec6b1`
- Authority seal file SHA-256:
  `13a07654d2eba6b2f1072d4a6a70636a90437e1da18e0bbeb8630ab841e026c1`

The installer passed `py_compile`, 8/8 hostile primitive self-tests, a
no-write frozen preflight, the real transaction, and a fresh-process stable
installed-state replay.  It used `O_EXCL|O_NOFOLLOW|O_CLOEXEC`, file and
parent-directory `fsync`, immutable `0444` files, `0500` bundle directories,
and `renameat2(RENAME_NOREPLACE)`.  The final seal is the sole semantic commit
point; either compatibility pointer without that exact seal is non-authority.

Installed nodes:

```text
30f289738d4e3d28a3fa230ad19253b29ef7373f33689181a3e50b1c7867fae4  .cm2-runtime/c48-current-successor-token
f80179317dee4b7e02cfe651e23f059d1219ffe753c5e9f5b1d970721b0490be  .cm2-runtime/c48-current-successor-audit-token
13a07654d2eba6b2f1072d4a6a70636a90437e1da18e0bbeb8630ab841e026c1  .cm2-runtime/c48-current-task-authority-seal
00338955b3225d96670806ab482775313e0afb68ebf7cafe01608787d828561b  .cm2-runtime/c48-successor-audits/c48-independent-audit-cf0531127a5c-v1/installation_receipt.json
```

No transaction staging node remains.

## Stable predecessor and strict scope

The transaction held and terminally reread the C42 candidate pointer, C42
audit pointer, C42 authority seal, canonical status, and canonical companion.
Their file SHA-256 values remained respectively:

```text
fbc5dd3c55bfdd3098ed34ae09ae633a9526a9c9cc6f40b3d87b5669b2ea7f07  .cm2-runtime/c42-current-token
59aca53c4c35260801b3c559648c88ee974db01ae950f045a5e5aecd64aa36e5  .cm2-runtime/c42-current-audit-token
0e5a76059b2c9407340d88e07f4fcc356d376f5c24b7173e6b95fd5e06bc312d  .cm2-runtime/c42-current-authority-seal
c4d77168b85070ab20c20d64c26d0c0cfcf0b9e3d0ef0acd2fad3006d08e9be9  deliverables/CM2_LATEST_STATUS.md
a9a5b00f605eacc2fa669a3b71d3a82b8b648a5c92c4ca77fa07e2074ab97639  deliverables/CM2_LATEST_STATUS.sha256
```

The installed wrapper recognizes exactly one audited task-level successor;
the embedded checkpoint retains its zero-credit lock and reports 513 pending
tasks in C46 shard 2.  Across the frozen C41 logical inventory, the task-level
pending count after installed C42 and this installed C48 successor is 33,640.
The coarse authority remains `574 paired / 1,150 unresolved / 575 reps` and
all D02 gate credit remains zero.

Fresh installed-state replay:

```bash
.cm2-runtime/python-flint-0.9.0/bin/python -I -B \
  deliverables/cm2_round306c48_d02a_pair668_generation1_successor_installer_v1.py \
  --verify-installed \
  --expect-installer-sha256 7c1c01d38d128bfe2556cc2b00574bfc280736c640e44bd63ab457352dfa9853
```
