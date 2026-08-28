# Round294-B dual-seed cold replay

Run from the workspace root. These commands never write bytecode. The
`--no-write` replays do not modify any deliverable.

## Producer

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=294201 \
  python3 -B \
  deliverables/cm2_round294b_source_g_registry_builder_admission_closure.py \
  --seed 294201 --no-write

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=294997 \
  python3 -B \
  deliverables/cm2_round294b_source_g_registry_builder_admission_closure.py \
  --seed 294997 --no-write
```

Both runs returned the same PASS status and commitments:

```text
result_sha256
c7737386ce2db72315d71a05cfedf474c0b1ff4a00306851a5294f6a6e58e221

result_file_sha256
656676d6f5dd4accc7b9aa473a14d9c1326b83eff2fe8974e7b43694adb44ccc
```

Observed runtimes were 6.65 and 6.64 seconds; peak RSS was 56,616 and
56,312 KiB.

## Independent verifier

```bash
PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=294271 \
  python3 -B \
  deliverables/cm2_round294b_source_g_registry_builder_admission_closure_verifier.py \
  --seed 294271 --no-write

PYTHONDONTWRITEBYTECODE=1 PYTHONHASHSEED=294929 \
  python3 -B \
  deliverables/cm2_round294b_source_g_registry_builder_admission_closure_verifier.py \
  --seed 294929 --no-write
```

Both runs independently rebuilt the admission object before candidate read,
rejected all 38 attacks, and returned identical commitments:

```text
verification_sha256
1746adb7b71607909eae031da879671885deee8602fdb5685dc561ba9afa4179

verification_file_sha256
b1440432a082b392de744bc6f4ca20e893122cb923a3236899357ccfb4fd6581

attack_suite_sha256
113f8d6b6b636b1f6116f5cec32438a33e16d2fdcf6c2b9bcf13bf9c6bb68499

attack_file_sha256
4d4f99615078062b0fbc544ff04245f6bd9055beb3ca8807480e0aff4aacdcff
```

Observed runtimes were 6.20 and 6.26 seconds; peak RSS was 57,060 and
57,056 KiB.

Every replay keeps the registry at 431,208 rows and the binding table at
46,288 rows. It grants zero registry, binding, occurrence, alias, component,
DSU, seam, `Jx/Jy`, maximality, fibre, global-disposition, D02, or CM2 credit.
