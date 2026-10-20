#!/usr/bin/env python3
"""Reconstruct the exact original transport package in a separate new directory.

Only the Python standard library is required. The archive is inspected without
extracting or executing any member. The delivered parts and metadata stay intact.
"""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import stat
import sys
import tarfile


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def git_blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def canonical_json(value):
    return (json.dumps(value, sort_keys=True, ensure_ascii=True, separators=(",", ":")) + "\n").encode("ascii")


def relative_path(root, name):
    require(isinstance(name, str) and name and "\\" not in name and not name.startswith("/"), "A relative POSIX member name")
    require(all(part not in ("", ".", "..") for part in name.split("/")), "No empty or traversing path component")
    path = root.joinpath(*name.split("/"))
    require(path.resolve().is_relative_to(root), "A file remains inside the explicit delivery directory")
    for ancestor in [path, *path.parents]:
        if ancestor == root:
            break
        require(not ancestor.is_symlink(), "No symbolic link in a delivered path")
    return path


def checked_read(root, name, expected):
    path = relative_path(root, name)
    before = path.stat(follow_symlinks=False)
    require(stat.S_ISREG(before.st_mode), "An ordinary delivered file")
    data = path.read_bytes()
    after = path.stat(follow_symlinks=False)
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), "File unchanged during read")
    require(len(data) == expected["bytes"] and sha256(data) == expected["sha256"], "Exact delivered file bytes: " + name)
    if "git_blob_sha" in expected:
        require(git_blob(data) == expected["git_blob_sha"], "Exact Git blob identity: " + name)
    return data


def verify_seal(root):
    path = root / "SEAL.json"
    if not path.exists():
        return {"present": False, "scope": "Preparation execution occurred before the final delivery seal was written. The manifest, every part, original metadata and archive members are independently checked below."}
    data = path.read_bytes()
    seal = json.loads(data)
    require(seal["schema"] == 1 and seal["self_excluded"] == "SEAL.json", "The final seal excludes only itself")
    rows = seal["files"]
    require(len({row["path"] for row in rows}) == len(rows), "Unique sealed paths")
    actual = {path.relative_to(root).as_posix() for path in root.rglob("*") if path.is_file()}
    require(actual == {row["path"] for row in rows} | {"SEAL.json"}, "Complete delivery file coverage")
    require(sha256(canonical_json(rows)) == seal["file_inventory_sha256"], "Exact aggregate seal inventory digest")
    for row in rows:
        checked_read(root, row["path"], row)
    return {"present": True, "sha256": sha256(data), "sealed_files_checked": len(rows),
            "scope": "Unkeyed content-integrity verification, not a digital signature or a claim about remote publication."}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--delivery-dir", type=Path, default=Path(__file__).resolve().parent,
                        help="Directory containing DELIVERY_MANIFEST.json, parts and original-package-metadata")
    parser.add_argument("--output-dir", type=Path, required=True,
                        help="A separate directory that does not yet exist; the complete original package is reconstructed there")
    args = parser.parse_args()
    root, output = args.delivery_dir.resolve(), args.output_dir.resolve()
    require(root.is_dir(), "The explicit delivery directory exists")
    require(output != root and not output.is_relative_to(root) and not root.is_relative_to(output),
            "Use a separate output directory outside the delivery directory")
    require(not output.exists(), "Choose a new output directory; existing files are never overwritten")
    started = datetime.now(timezone.utc).isoformat()
    seal_result = verify_seal(root)
    manifest_bytes = (root / "DELIVERY_MANIFEST.json").read_bytes()
    manifest = json.loads(manifest_bytes)
    require(manifest["schema"] == 1, "Supported delivery schema")
    original_rows = manifest["original_package"]["files"]
    original = {row["path"]: row for row in original_rows}
    require(len(original) == len(original_rows) == 8, "All eight original package files are mapped")
    require(sha256(canonical_json(original_rows)) == manifest["original_package"]["aggregate_sha256"], "Original complete package identity digest")
    archive_row = manifest["archive"]
    archive_name = archive_row["path"]
    require(archive_name in original and "/" not in archive_name, "Original archive filename")
    for key in ("bytes", "sha256", "git_blob_sha"):
        require(archive_row[key] == original[archive_name][key], "Archive identity agrees with the complete original package")
    require(len(manifest["parts"]) == 8 and manifest["maximum_part_bytes"] == 4 * 1024 * 1024, "The declared eight-part, 4 MiB storage contract")
    require(manifest["reassembler"]["path"] == Path(__file__).name and
            sha256(Path(__file__).read_bytes()) == manifest["reassembler"]["sha256"], "The exact supplied reassembler source")
    mapping = manifest["storage_map"]
    require(set(mapping) == set(original), "A storage mapping for every original package file")
    metadata = {}
    for name, row in original.items():
        if name == archive_name:
            require(mapping[name]["kind"] == "ordered_binary_parts", "The archive is explicitly represented by parts")
            require(mapping[name]["parts"] == [part["path"] for part in manifest["parts"]], "Exact ordered archive part mapping")
        else:
            require(mapping[name]["kind"] == "exact_metadata_copy", "Metadata is an exact original byte copy")
            metadata[name] = checked_read(root, mapping[name]["path"], row)
    predecessor_manifest = json.loads(metadata["PACKAGE_FILE_IDENTITIES.json"])
    require(predecessor_manifest["self_excluded"] == "PACKAGE_FILE_IDENTITIES.json", "Exact original package self-exclusion convention")
    require({row["path"] for row in predecessor_manifest["files"]} == set(original) - {"PACKAGE_FILE_IDENTITIES.json"},
            "The original identity manifest covers every other reconstructed original file")
    for row in predecessor_manifest["files"]:
        require(all(row[key] == original[row["path"]][key] for key in ("bytes", "sha256", "git_blob_sha")), "Original package identity manifest agrees exactly")
    source_inventory = json.loads(metadata["SOURCE_FILE_IDENTITIES.json"])
    source_rows = source_inventory["files"]
    sources = {row["path"]: row for row in source_rows}
    require(len(sources) == len(source_rows) == archive_row["expected_tar_members"] == 957, "All original archive-member identities are retained")

    output.mkdir(parents=True)
    pending = output / (archive_name + ".partial")
    archive_sha256 = hashlib.sha256()
    archive_git = hashlib.sha1(b"blob " + str(archive_row["bytes"]).encode("ascii") + b"\0")
    position, verified_parts = 0, []
    with pending.open("xb") as stream:
        for index, part in enumerate(manifest["parts"], 1):
            require(part["index"] == index and part["offset"] == position, "Contiguous original part order and offsets")
            require(0 < part["bytes"] <= manifest["maximum_part_bytes"], "Every binary part is at most 4 MiB")
            data = checked_read(root, part["path"], part)
            stream.write(data)
            archive_sha256.update(data)
            archive_git.update(data)
            position += len(data)
            verified_parts.append({"index": index, "path": part["path"], "bytes": len(data), "sha256": sha256(data)})
    require(position == archive_row["bytes"] and archive_sha256.hexdigest() == archive_row["sha256"]
            and archive_git.hexdigest() == archive_row["git_blob_sha"], "Concatenated parts reconstruct the exact complete original archive")

    seen, member_bytes = set(), 0
    with tarfile.open(pending, mode="r|xz") as tar:
        for member in tar:
            require(member.isfile() and member.name in sources and member.name not in seen, "Each archive member is an original unique ordinary file")
            expected = sources[member.name]
            require(member.size == expected["bytes"] and member.mode == int(expected["file_mode"], 8), "Original archive member size and mode")
            require(member.uid == member.gid == member.mtime == 0 and member.uname == member.gname == "", "Original deterministic tar metadata")
            data = tar.extractfile(member).read()
            require(len(data) == expected["bytes"] and sha256(data) == expected["sha256"]
                    and git_blob(data) == expected["git_blob_sha"], "Exact decompressed original member bytes: " + member.name)
            member_bytes += len(data)
            seen.add(member.name)
    require(seen == set(sources), "All 957 original tar members were read and verified")
    for name, data in metadata.items():
        require("/" not in name and "\\" not in name and name not in (".", ".."), "Original package metadata uses simple filenames")
        path = output / name
        with path.open("xb") as stream:
            stream.write(data)
        os.chmod(path, int(original[name]["file_mode"], 8))
    pending.rename(output / archive_name)
    os.chmod(output / archive_name, int(original[archive_name]["file_mode"], 8))
    checked_original_rows = []
    for row in original_rows:
        data = checked_read(output, row["path"], row)
        checked_original_rows.append({**row, "bytes": len(data), "sha256": sha256(data), "git_blob_sha": git_blob(data)})
    require(sha256(canonical_json(checked_original_rows)) == manifest["original_package"]["aggregate_sha256"], "The complete reconstructed original package has its exact original aggregate identity")
    receipt = {"schema": 1, "status": "passed", "started_utc": started,
               "finished_utc": datetime.now(timezone.utc).isoformat(), "python": sys.version,
               "delivery_directory": str(root), "output_directory": str(output),
               "delivery_manifest_sha256": sha256(manifest_bytes), "delivery_seal": seal_result,
               "reassembler_sha256": sha256(Path(__file__).read_bytes()),
               "original_package_aggregate_sha256": manifest["original_package"]["aggregate_sha256"],
               "archive": {key: archive_row[key] for key in ("path", "bytes", "sha256", "git_blob_sha")},
               "verified_parts": verified_parts, "archive_members_read_and_hashed": len(seen),
               "original_archive_member_bytes": member_bytes, "reconstructed_original_files": checked_original_rows,
               "scope": "Exact local byte reconstruction and complete archive-member verification. Archive members were neither extracted nor executed. Original delivery files are unchanged. No Git, remote publication, CI or mathematical certification is performed."}
    receipt_path = output / "REASSEMBLY_VERIFICATION.json"
    with receipt_path.open("x", encoding="utf-8") as stream:
        json.dump(receipt, stream, sort_keys=True, indent=2)
        stream.write("\n")
    print(json.dumps({"status": "passed", "archive": str(output / archive_name),
                      "archive_sha256": archive_row["sha256"], "tar_members_verified": len(seen),
                      "original_files_reconstructed": len(original_rows), "receipt": str(receipt_path),
                      "receipt_sha256": sha256(receipt_path.read_bytes())}, indent=2))


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        sys.stderr.write(type(error).__name__ + ": " + str(error) + "\n")
        raise SystemExit(1)
