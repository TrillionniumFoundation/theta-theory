# CM2 Round144 cold replay

Date: 2026-07-24

## Commands

```bash
env PYTHONHASHSEED=144001 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round144_round137_v1_superseding_migration_schema.py \
  --output /tmp/cm2-r144-producer-A.json

env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round144_round137_v1_superseding_migration_schema.py \
  --output /tmp/cm2-r144-producer-B.json

env PYTHONHASHSEED=144144 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round144_round137_v1_superseding_migration_schema_verifier.py \
  --certificate \
  deliverables/cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json \
  --output /tmp/cm2-r144-verifier-A.json

env PYTHONHASHSEED=987654321 LC_ALL=C TZ=UTC PYTHONDONTWRITEBYTECODE=1 \
  /usr/bin/time -v .venv-neurips/bin/python \
  deliverables/cm2_round144_round137_v1_superseding_migration_schema_verifier.py \
  --certificate \
  deliverables/cm2-round144-round137-v1-superseding-migration-schema-2026-07-24.json \
  --output /tmp/cm2-r144-verifier-B.json
```

## Results

- Producer seed A: exit 0, wall 0.26 s, maximum RSS 19,376 KiB.
- Producer seed B: exit 0, wall 0.22 s, maximum RSS 20,188 KiB.
- Both producer artifacts are byte-identical to the frozen certificate.
- The seed-B run atomically replaced a pre-existing sentinel; inode
  `39331121 -> 39331149`.
- Verifier seed A: exit 0, wall 0.53 s, maximum RSS 21,008 KiB.
- Verifier seed B: exit 0, wall 0.82 s, maximum RSS 21,336 KiB.
- Both verifier artifacts are byte-identical to each other and to the frozen
  verification.

Artifact hashes:

```text
bd2f4f0262b58e2847ab578fb2bad3c7ca01305bbd113f6c330697714276675f  producer output / frozen certificate
dabd57057c1a6fe7f9afa47f7445a4696297aa7488dc89ad808d5b8307bff9b5  verifier output / frozen verification
```

No dependency, producer, certificate, or verifier byte changed during replay.

