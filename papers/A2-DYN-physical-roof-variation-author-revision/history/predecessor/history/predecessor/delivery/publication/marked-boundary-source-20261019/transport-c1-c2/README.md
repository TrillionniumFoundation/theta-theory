# Complete C1/C2 transport evidence in eight bounded binary parts

This directory delivers the exact previously verified transport package through **eight binary parts**, each at most **4 MiB (4,194,304 bytes)**. It retains all original package files by exact reconstruction. No archive member, original metadata or recorded remote event has been removed or rewritten.

The original archive is **30,438,628 bytes**, SHA-256 **`4971853efc8648407331ad7e714cefc5783a8f2f546af0d41c84da03be601c3e`**, Git blob **`5007fd5307dc257b8cb1dbc812b3d78365f8be8c`**. Parts 1–7 each contain 4,194,304 bytes; part 8 contains **1,078,500 bytes**. `DELIVERY_MANIFEST.json` records each exact offset, length, SHA-256 and Git blob, and maps every original package filename to its actual storage here.

## Reconstruct the complete original package

Use Python 3.9 or later with its standard-library XZ support. Run the supplied plain-text program with a **new, separate output directory**:

```bash
python reassemble_transport_archive.py --output-dir /absolute/path/to/new-reconstructed-transport-package
```

The output directory must not already exist and must be outside this delivery directory. The program verifies the final delivery SEAL when present, reads and verifies all eight parts, concatenates them in the recorded order, verifies the complete archive, and opens the archive to read and hash **all 957 original tar members**. It does not extract or execute archive members. It restores the seven exact original metadata files beside the complete archive, recreating all **eight original package files**, and writes a separate `REASSEMBLY_VERIFICATION.json` recording that actual run.

The original metadata under `original-package-metadata/` are unmodified historical documents describing that reconstructed output package. In particular, their references to a complete `C1_C2_TRANSPORT_SNAPSHOT.tar.xz` refer to the original/reconstructed package. This split delivery stores that file through `parts/`, not as an absent or falsely claimed whole file. `storage_map` states the relationship explicitly.

## Complete identity and actual validation

The original package's exact path-aware aggregate SHA-256 is **`2bf984f95079bd2c546863c88d09d66dedf66cc36a2a84116e6800d341f837e8`**. Its definition is in `DELIVERY_MANIFEST.json`: canonical ASCII JSON of the sorted eight-file identity array, including the original identity manifest itself, with one terminal newline. The original `PACKAGE_FILE_IDENTITIES.json` is preserved with SHA-256 **`f0d1bdd3a3a41ec1cab620ce84e48cd4215a9c99632731cb38f4717c4b9074de`**.

An actual invocation of the portable reassembler already completed successfully in a separate scratch output directory. `PREPARATION_AND_REASSEMBLY_RECEIPT.json` and `validation/` preserve its command, start/end times, exit code, exact stdout/stderr and complete reconstruction receipt. All 957 members were read and checked; all eight reconstructed original files were additionally compared byte for byte with the sealed original package. The original package was checked again and remained unchanged.

`SEAL.json` is the final delivery integrity manifest. It covers every delivered file except itself, including the plain-text programs, README, mapping, original metadata, binary parts and actual validation evidence. Its aggregate digest is the SHA-256 of the canonical files array. This is an unkeyed integrity record, not a digital signature. The preparation reconstruction necessarily preceded the final SEAL; that ordering is explicitly recorded. A normal later reconstruction also verifies the completed SEAL.

## Preserved scope

The reconstructed archive preserves the full C1/C2 transport snapshot from **2026-10-19T16:00:49.204947+00:00**: 934 C1 files, 16 C2 files and seven shared preparation/provenance files. The original operation index separately locates actual response records, unsuccessful root requests, the successful nested-path retry, commit/ref observations, and prepared-only payloads. Splitting storage does not turn a prepared request into an executed event or a successful tree transport into completed CI. The original mathematical and CI limitations remain unchanged.
