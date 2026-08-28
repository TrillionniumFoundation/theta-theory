# CM2 Round 134 — cold replay

Date: 2026-07-24

Two clean verifier replays were run with:

- `PYTHONHASHSEED=134071`;
- `PYTHONHASHSEED=134129`;
- `LC_ALL=C`;
- `TZ=UTC`;
- `PYTHONDONTWRITEBYTECODE=1`.

Both used the Python environment containing `python-flint`:

```bash
.venv-neurips/bin/python \
  deliverables/cm2_round134_round28_exact_seed_occurrence_incidence_frontier_verifier.py \
  --certificate \
  deliverables/cm2-round134-round28-exact-seed-occurrence-incidence-frontier-2026-07-24.json \
  --output /tmp/cm2-r134-verification.json
```

Both returned exit code 0 and `PASS`.  Their artifacts were byte-for-byte
identical to each other and to the formal verification artifact.

Frozen hashes:

- producer:
  `6bcac3d0b74f974fe0b07cd22aa8e407221ff4da94242ca28c746c31a97b7b1e`;
- certificate:
  `1d09f4371d72e2d63dc3398d82b45f515a29f8a3db33009e5c6212e53fcb7e6e`;
- certificate result:
  `263a5215ecbeae30cd858af2e3b18131a759103480ea58f000975b92d5ef2704`;
- verifier:
  `dc956666828837bf93c4ebba3ff25b71b0a30dc74c0706c8f8866a2f2a22178a`;
- verification:
  `d145ddc109742568aa1cee464f13ff554e554c2956e63c0ec1f149e6cda22786`;
- verification result:
  `cfdcd7db1d34ab704c4d39d89defc45362aec138b96af55625adc1c6c922180c`.

The replay independently reconstructed:

- all 64 Round132 records and their `44/20` compatible/type-mismatch split;
- 16 unique signed sheets and 12 unique target lifts;
- twelve 2048-bit outward-rounded whole-rectangle discriminant enclosures;
- the `2/10/0` positive/negative/zero discriminant census;
- the strict uniform absolute margin above `1/100`;
- 24 Round122 children, 72 child-stage rows and 4056 candidate checks;
- zero exact-seed physical faces and zero residual faces.

The corner values were recomputed only as auxiliary agreement checks.  The
verifier used full-product-box interval evaluation for the rectangle-wide
proof.

The verifier rejected all 69 re-signed semantic mutations and all 18
strict-JSON attacks.

Negative I/O replay used `PYTHONHASHSEED=134191`.  Each hostile case returned
nonzero without creating a result or changing the pre-existing target:

- missing certificate;
- byte-tampered certificate;
- certificate symlink;
- certificate hardlink;
- output symlink;
- output hardlink;
- output FIFO;
- protected upstream output target;
- a valid custom certificate used simultaneously as `--certificate` and
  `--output`.

The formal certificate, protected Round113 artifact and same-path custom
certificate retained their original hashes.  A byte-identical custom
certificate at a distinct regular path passed, and its verification output
was byte-identical to the formal artifact.
