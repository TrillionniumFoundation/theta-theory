#!/usr/bin/env python3
"""Prepare small exact archive parts and actually verify complete reconstruction."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys


ARCHIVE_NAME = "C1_C2_TRANSPORT_SNAPSHOT.tar.xz"
ARCHIVE_BYTES = 30438628
ARCHIVE_SHA256 = "4971853efc8648407331ad7e714cefc5783a8f2f546af0d41c84da03be601c3e"
ORIGINAL_IDENTITY_SHA256 = "f0d1bdd3a3a41ec1cab620ce84e48cd4215a9c99632731cb38f4717c4b9074de"
PART_LIMIT = 4 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def canonical_json(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode("ascii")


def file_identity(path, name=None):
    before = path.stat(follow_symlinks=False)
    require(stat.S_ISREG(before.st_mode), "Only ordinary files are read")
    data = path.read_bytes()
    after = path.stat(follow_symlinks=False)
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), "Stable file read")
    return {"path": name if name is not None else path.name, "bytes": len(data),
            "sha256": digest(data), "git_blob_sha": blob(data),
            "file_mode": format(stat.S_IMODE(after.st_mode), "04o")}


def save_json(path, value):
    require(not path.exists(), "Never overwrite a saved artifact")
    path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original-package", type=Path, required=True)
    parser.add_argument("--delivery-dir", type=Path, required=True)
    parser.add_argument("--verification-output", type=Path, required=True)
    args = parser.parse_args()
    original, delivery, verification_output = (path.resolve() for path in
        (args.original_package, args.delivery_dir, args.verification_output))
    require(original != delivery and not original.is_relative_to(delivery) and not delivery.is_relative_to(original), "Separate original and delivery directories")
    require(delivery.is_dir() and {path.name for path in delivery.iterdir()} == {"reassemble_transport_archive.py"},
            "A fresh delivery directory containing only the prepared reassembler source")
    require(not verification_output.exists() and not verification_output.is_relative_to(delivery), "A new separate reconstruction directory")
    started = now()
    original_paths = sorted(original.iterdir(), key=lambda path: path.name.encode("utf-8"))
    require(len(original_paths) == 8 and all(path.is_file() for path in original_paths), "The complete eight-file original package")
    originals = [file_identity(path) for path in original_paths]
    indexed = {row["path"]: row for row in originals}
    require(indexed[ARCHIVE_NAME]["bytes"] == ARCHIVE_BYTES and indexed[ARCHIVE_NAME]["sha256"] == ARCHIVE_SHA256,
            "The exact previously verified complete archive")
    require(indexed["PACKAGE_FILE_IDENTITIES.json"]["sha256"] == ORIGINAL_IDENTITY_SHA256, "The unchanged original package identity manifest")
    original_declared = json.loads((original / "PACKAGE_FILE_IDENTITIES.json").read_bytes())
    require({row["path"] for row in original_declared["files"]} == set(indexed) - {"PACKAGE_FILE_IDENTITIES.json"}, "Complete original identity coverage")
    for row in original_declared["files"]:
        require(all(row[key] == indexed[row["path"]][key] for key in ("bytes", "sha256", "git_blob_sha")), "Every original package file matches its prior sealed identity")
    package_aggregate = digest(canonical_json(originals))
    metadata_dir, parts_dir = delivery / "original-package-metadata", delivery / "parts"
    metadata_dir.mkdir()
    parts_dir.mkdir()
    storage_map = {}
    for path in original_paths:
        if path.name == ARCHIVE_NAME:
            continue
        destination = metadata_dir / path.name
        destination.write_bytes(path.read_bytes())
        os.chmod(destination, int(indexed[path.name]["file_mode"], 8))
        require(file_identity(destination) == indexed[path.name], "Exact original metadata copy")
        storage_map[path.name] = {"kind": "exact_metadata_copy", "path": destination.relative_to(delivery).as_posix()}
    parts, offset = [], 0
    with (original / ARCHIVE_NAME).open("rb") as stream:
        while True:
            data = stream.read(PART_LIMIT)
            if not data:
                break
            index = len(parts) + 1
            destination = parts_dir / ("archive.part-" + str(index).zfill(4) + ".bin")
            destination.write_bytes(data)
            row = file_identity(destination, destination.relative_to(delivery).as_posix())
            row.update({"index": index, "offset": offset})
            parts.append(row)
            offset += len(data)
    require(len(parts) == 8 and offset == ARCHIVE_BYTES and all(row["bytes"] <= PART_LIMIT for row in parts), "Eight exact bounded binary parts")
    storage_map[ARCHIVE_NAME] = {"kind": "ordered_binary_parts", "parts": [row["path"] for row in parts]}
    original_receipt = json.loads((original / "ARCHIVE_VERIFICATION_RECEIPT.json").read_bytes())
    manifest = {"schema": 1, "created_utc": now(), "scope": "Split storage of the complete already verified C1/C2 transport evidence package; original bytes and event scopes are unchanged.",
        "archive": {**indexed[ARCHIVE_NAME], "format": "tar.xz", "expected_tar_members": 957},
        "original_package": {"file_count": len(originals), "files": originals, "aggregate_sha256": package_aggregate,
                             "aggregate_definition": "SHA-256 of ASCII JSON for the path-sorted files array, using sorted object keys, ensure_ascii=True, separators=(',', ':'), and one terminal newline. Includes all eight original files, including the original PACKAGE_FILE_IDENTITIES.json itself.",
                             "identity_manifest_sha256": ORIGINAL_IDENTITY_SHA256,
                             "original_snapshot_cutoff_utc": original_receipt["source_snapshot_identified_utc"]},
        "storage_map": storage_map, "maximum_part_bytes": PART_LIMIT, "parts": parts,
        "reassembler": file_identity(delivery / "reassemble_transport_archive.py"),
        "original_metadata_scope": "The exact original metadata describe the reconstructed original package. This split delivery does not claim to contain the complete archive as one physical file; its explicit mapping is the ordered binary parts."}
    save_json(delivery / "DELIVERY_MANIFEST.json", manifest)
    validation = delivery / "validation"
    validation.mkdir()
    command = [sys.executable, str(delivery / "reassemble_transport_archive.py"), "--output-dir", str(verification_output)]
    command_started = now()
    with (validation / "COMMAND_STDOUT.json").open("wb") as stdout, (validation / "COMMAND_STDERR.txt").open("wb") as stderr:
        done = subprocess.run(command, stdout=stdout, stderr=stderr,
                              env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    command_finished = now()
    require(done.returncode == 0, "Actual full reassembly command must succeed; its raw stdout/stderr remain preserved")
    reconstructed_receipt_bytes = (verification_output / "REASSEMBLY_VERIFICATION.json").read_bytes()
    reconstructed = json.loads(reconstructed_receipt_bytes)
    require(reconstructed["status"] == "passed" and reconstructed["archive_members_read_and_hashed"] == 957,
            "Actual portable reassembler read and verified all original tar members")
    require(reconstructed["archive"]["sha256"] == ARCHIVE_SHA256 and reconstructed["archive"]["bytes"] == ARCHIVE_BYTES,
            "Actual complete reconstructed archive identity")
    for path in original_paths:
        require((verification_output / path.name).read_bytes() == path.read_bytes(), "Independent byte equality for every reconstructed original package file")
    require([file_identity(path) for path in original_paths] == originals and sorted(path.name for path in original.iterdir()) == sorted(indexed),
            "The original sealed package and its complete file set are unchanged")
    (validation / "REASSEMBLY_VERIFICATION.json").write_bytes(reconstructed_receipt_bytes)
    (delivery / "prepare_split_transport_delivery.py").write_bytes(Path(__file__).read_bytes())
    receipt = {"schema": 1, "status": "passed", "started_utc": started, "finished_utc": now(),
        "program_sha256": digest(Path(__file__).read_bytes()), "python": sys.version,
        "original_package_directory": str(original), "original_package_files_before_and_after": originals,
        "original_package_aggregate_sha256": package_aggregate, "original_package_bytewise_unchanged": True,
        "binary_part_count": len(parts), "maximum_part_bytes": PART_LIMIT, "parts": parts,
        "original_archive": indexed[ARCHIVE_NAME], "independent_byte_comparison_of_all_eight_files": "passed",
        "actual_command": command, "actual_command_started_utc": command_started,
        "actual_command_finished_utc": command_finished, "actual_command_exit_code": done.returncode,
        "actual_stdout": file_identity(validation / "COMMAND_STDOUT.json", "validation/COMMAND_STDOUT.json"),
        "actual_stderr": file_identity(validation / "COMMAND_STDERR.txt", "validation/COMMAND_STDERR.txt"),
        "actual_reassembly_receipt": file_identity(validation / "REASSEMBLY_VERIFICATION.json", "validation/REASSEMBLY_VERIFICATION.json"),
        "verified_tar_member_count": 957, "verified_original_archive_member_bytes": reconstructed["original_archive_member_bytes"],
        "validation_order": "The actual reconstruction checked manifest, all parts, all metadata, the complete archive and all members before the final SEAL was written. The final SEAL was then separately checked against every completed delivery file.",
        "scope": "Exact split-storage delivery and actual complete local byte reconstruction. No article/source/index, Git ref, remote operation, CI result or continuous mathematical proof is changed or certified."}
    save_json(delivery / "PREPARATION_AND_REASSEMBLY_RECEIPT.json", receipt)
    readme = f"""# Complete C1/C2 transport evidence in eight bounded binary parts

This directory delivers the exact previously verified transport package through **eight binary parts**, each at most **4 MiB (4,194,304 bytes)**. It retains all original package files by exact reconstruction. No archive member, original metadata or recorded remote event has been removed or rewritten.

The original archive is **{ARCHIVE_BYTES:,} bytes**, SHA-256 **`{ARCHIVE_SHA256}`**, Git blob **`{indexed[ARCHIVE_NAME]['git_blob_sha']}`**. Parts 1–7 each contain 4,194,304 bytes; part 8 contains **{parts[-1]['bytes']:,} bytes**. `DELIVERY_MANIFEST.json` records each exact offset, length, SHA-256 and Git blob, and maps every original package filename to its actual storage here.

## Reconstruct the complete original package

Use Python 3.9 or later with its standard-library XZ support. Run the supplied plain-text program with a **new, separate output directory**:

```bash
python reassemble_transport_archive.py --output-dir /absolute/path/to/new-reconstructed-transport-package
```

The output directory must not already exist and must be outside this delivery directory. The program verifies the final delivery SEAL when present, reads and verifies all eight parts, concatenates them in the recorded order, verifies the complete archive, and opens the archive to read and hash **all 957 original tar members**. It does not extract or execute archive members. It restores the seven exact original metadata files beside the complete archive, recreating all **eight original package files**, and writes a separate `REASSEMBLY_VERIFICATION.json` recording that actual run.

The original metadata under `original-package-metadata/` are unmodified historical documents describing that reconstructed output package. In particular, their references to a complete `C1_C2_TRANSPORT_SNAPSHOT.tar.xz` refer to the original/reconstructed package. This split delivery stores that file through `parts/`, not as an absent or falsely claimed whole file. `storage_map` states the relationship explicitly.

## Complete identity and actual validation

The original package's exact path-aware aggregate SHA-256 is **`{package_aggregate}`**. Its definition is in `DELIVERY_MANIFEST.json`: canonical ASCII JSON of the sorted eight-file identity array, including the original identity manifest itself, with one terminal newline. The original `PACKAGE_FILE_IDENTITIES.json` is preserved with SHA-256 **`{ORIGINAL_IDENTITY_SHA256}`**.

An actual invocation of the portable reassembler already completed successfully in a separate scratch output directory. `PREPARATION_AND_REASSEMBLY_RECEIPT.json` and `validation/` preserve its command, start/end times, exit code, exact stdout/stderr and complete reconstruction receipt. All 957 members were read and checked; all eight reconstructed original files were additionally compared byte for byte with the sealed original package. The original package was checked again and remained unchanged.

`SEAL.json` is the final delivery integrity manifest. It covers every delivered file except itself, including the plain-text programs, README, mapping, original metadata, binary parts and actual validation evidence. Its aggregate digest is the SHA-256 of the canonical files array. This is an unkeyed integrity record, not a digital signature. The preparation reconstruction necessarily preceded the final SEAL; that ordering is explicitly recorded. A normal later reconstruction also verifies the completed SEAL.

## Preserved scope

The reconstructed archive preserves the full C1/C2 transport snapshot from **{original_receipt['source_snapshot_identified_utc']}**: 934 C1 files, 16 C2 files and seven shared preparation/provenance files. The original operation index separately locates actual response records, unsuccessful root requests, the successful nested-path retry, commit/ref observations, and prepared-only payloads. Splitting storage does not turn a prepared request into an executed event or a successful tree transport into completed CI. The original mathematical and CI limitations remain unchanged.
"""
    (delivery / "README.md").write_text(readme, encoding="utf-8")
    seal_rows = [file_identity(path, path.relative_to(delivery).as_posix())
                 for path in sorted(delivery.rglob("*"), key=lambda path: path.relative_to(delivery).as_posix()) if path.is_file()]
    require(not any(row["path"] == "SEAL.json" for row in seal_rows), "The final seal has not been created prematurely")
    seal = {"schema": 1, "status": "sealed_after_actual_reassembly_verification", "created_utc": now(),
            "self_excluded": "SEAL.json", "file_inventory_sha256": digest(canonical_json(seal_rows)),
            "files": seal_rows, "scope": "Complete final delivery file identities excluding only this SEAL.json; no external publication or proof certification is inferred."}
    save_json(delivery / "SEAL.json", seal)
    actual_files = {path.relative_to(delivery).as_posix() for path in delivery.rglob("*") if path.is_file()}
    require(actual_files == {row["path"] for row in seal_rows} | {"SEAL.json"}, "Final SEAL excludes only itself and covers every other delivered file")
    for row in seal_rows:
        require(file_identity(delivery / row["path"], row["path"]) == row, "Every completed delivery file matches its final seal")
    require([file_identity(path) for path in original_paths] == originals, "Original sealed package remains unchanged after final sealing")
    print(json.dumps({"status": "passed", "delivery_directory": str(delivery),
        "parts": len(parts), "archive_sha256": ARCHIVE_SHA256,
        "original_package_aggregate_sha256": package_aggregate,
        "final_seal": file_identity(delivery / "SEAL.json"), "sealed_files_excluding_seal": len(seal_rows),
        "actual_reassembler_exit_code": done.returncode, "tar_members_verified": 957}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        sys.stderr.write(type(error).__name__ + ": " + str(error) + "\n")
        raise SystemExit(1)
