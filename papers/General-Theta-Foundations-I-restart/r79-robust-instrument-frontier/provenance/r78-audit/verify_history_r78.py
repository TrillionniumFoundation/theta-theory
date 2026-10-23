#!/usr/bin/env python3
"""Authenticate the complete 7,137-blob R78 historical text census portably.

Stream the retained R77 archive parts/deltas and the minimal R78 delta.
No Git cache, external workspace, network, third-party library or archive
extraction is used. The only write is the explicitly requested receipt.
This authenticates historical text, not mathematical proofs or priority.
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import sys
import tarfile

R77_AUDIT = "provenance/r77-audit"
R78_AUDIT = "provenance/r78-audit"
R77_MANIFEST_SHA256 = "c60897eb52bfa2f5f1a8e343b8d09cdd5c17784290faeaf14c42a24961a0a6fd"
R78_INDEX_SHA256 = "f2e351561ff93a68b2d680a8adc1f24531afe7f6212b48f941f973a149c445bb"
R78_DELTA_SHA256 = "88ed4c197de6301b88ef9c9bbd9a269bcfb7c5153ed47e76001efa5310b48d6e"
R78_DELTA_BYTES = 2087744
EXPECTED_OLD = 7024
EXPECTED_NEW = 113
EXPECTED_TOTAL = 7137
EXPECTED_BYTES = 108165876
EXPECTED_DELTA_BYTES = 7265672


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def source_file(root: Path, relative: str) -> Path:
    path = PurePosixPath(relative)
    require(not path.is_absolute() and ".." not in path.parts,
            "Invalid source-relative input: " + relative)
    result = root.joinpath(*path.parts)
    require(result.is_file() and not result.is_symlink()
            and root in result.resolve().parents,
            "Missing, nonregular or escaped source input: " + relative)
    return result


def file_digest(path: Path, accumulator=None) -> tuple[int, str]:
    digest = hashlib.sha256()
    length = 0
    with path.open("rb") as stream:
        while True:
            block = stream.read(1024 * 1024)
            if not block:
                break
            length += len(block)
            digest.update(block)
            if accumulator is not None:
                accumulator.update(block)
    return length, digest.hexdigest()


def authenticate_file(path: Path, expected: dict, accumulator=None) -> dict:
    length, digest = file_digest(path, accumulator)
    require(length == expected["bytes"] and digest == expected["sha256"],
            "Archive/index bytes or SHA-256 differ: " + str(path))
    return {"bytes": length, "sha256": digest}


def read_index(path: Path, expected_sha256: str | None = None,
               expected: dict | None = None) -> dict:
    if expected is not None:
        authenticate_file(path, expected)
    raw = path.read_bytes()
    require(expected_sha256 is None or sha256(raw) == expected_sha256,
            "Pinned census index differs: " + str(path))
    rows = json.loads(gzip.decompress(raw))
    require(isinstance(rows, list), "Index is not a record list: " + str(path))
    result = {}
    for row in rows:
        blob = row.get("git_blob", "")
        require(re.fullmatch(r"[0-9a-f]{40}", blob) is not None
                and blob not in result, "Invalid or duplicated indexed blob: " + blob)
        require(type(row.get("bytes")) is int and row["bytes"] >= 0
                and re.fullmatch(r"[0-9a-f]{64}", row.get("sha256", "")) is not None,
                "Malformed indexed identity: " + blob)
        result[blob] = row
    return result


def compact_identity(row: dict) -> dict:
    return {key: row[key] for key in ("bytes", "sha256")}


class JoinedParts(io.RawIOBase):
    """Expose a sequence of existing parts as one non-seeking byte stream."""
    def __init__(self, paths: list[Path]):
        super().__init__()
        self.paths = iter(paths)
        self.current = None

    def readable(self) -> bool:
        return True

    def readinto(self, buffer) -> int:
        while True:
            if self.current is None:
                try:
                    self.current = next(self.paths).open("rb")
                except StopIteration:
                    return 0
            count = self.current.readinto(buffer)
            if count:
                return count
            self.current.close()
            self.current = None

    def close(self) -> None:
        if self.current is not None:
            self.current.close()
            self.current = None
        super().close()


def stream_members(paths: list[Path], index: dict, expected: set[str],
                   seen: set[str], name: str) -> dict:
    members = set()
    total_bytes = 0
    latin1 = []
    with io.BufferedReader(JoinedParts(paths)) as joined:
        with tarfile.open(fileobj=joined, mode="r|gz") as archive:
            for member in archive:
                require(member.isfile(), "Nonregular archive member in " + name)
                path = PurePosixPath(member.name)
                require(len(path.parts) == 2 and path.parts[0] == "blobs"
                        and path.suffix == ".txt"
                        and re.fullmatch(r"[0-9a-f]{40}", path.stem) is not None,
                        "Unexpected archive member path: " + member.name)
                blob = path.stem
                require(blob in expected and blob not in seen and blob not in members,
                        "Unindexed, overlapping or duplicate archive member: " + blob)
                handle = archive.extractfile(member)
                require(handle is not None, "Unreadable archive member: " + blob)
                raw = handle.read()
                handle.close()
                fixed = index[blob]
                require(len(raw) == member.size == fixed["bytes"],
                        "Truncated or differently sized archive member: " + blob)
                actual_git = hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()
                require(actual_git == blob and sha256(raw) == fixed["sha256"],
                        "Git/SHA-256 content identity mismatch: " + blob)
                encoding = fixed.get("encoding", "utf-8")
                require(encoding in {"utf-8", "latin-1"},
                        "Unexpected indexed decoding policy: " + blob)
                text = raw.decode(encoding)
                if "lines" in fixed:
                    require(len(text.splitlines()) == fixed["lines"],
                            "Decoded line count differs: " + blob)
                if encoding == "latin-1":
                    latin1.append(blob)
                total_bytes += len(raw)
                members.add(blob)
    require(members == expected, "Archive member set differs for " + name)
    seen.update(members)
    return {"group": name, "unique_text_blobs": len(members),
            "authenticated_uncompressed_bytes": total_bytes,
            "latin1_log_blobs": sorted(latin1)}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source-root", required=True, type=Path,
                        help="the standalone R78 source directory")
    parser.add_argument("--receipt", required=True, type=Path,
                        help="write the actual completed authentication receipt here")
    args = parser.parse_args()
    root = args.source_root.resolve()
    require(root.is_dir(), "Source root is not a directory")
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    old_manifest_path = source_file(root, R77_AUDIT + "/history-delta/HISTORY_DELTA_MANIFEST.json")
    old_manifest_raw = old_manifest_path.read_bytes()
    require(sha256(old_manifest_raw) == R77_MANIFEST_SHA256,
            "The pinned R77 archive manifest differs")
    manifest = json.loads(old_manifest_raw)
    require(manifest.get("schema") == "theta.r77.history-base-plus-delta.v1",
            "Unexpected retained archive manifest schema")
    index_path = source_file(root, R78_AUDIT + "/current-census/HISTORICAL_TEXT_INDEX.json.gz")
    index = read_index(index_path, expected_sha256=R78_INDEX_SHA256)
    old_index_path = source_file(root, R77_AUDIT + "/full-scan/HISTORICAL_TEXT_INDEX.json.gz")
    old_index = read_index(old_index_path, expected=manifest["current_index"])
    extra_index_path = source_file(root, R77_AUDIT + "/all-ref-scope-extension/ADDITIONAL_TEXT_INDEX.json.gz")
    extra_index = read_index(extra_index_path, expected=manifest["all_ref_extension"]["index"])
    require(not set(old_index) & set(extra_index), "Retained old indexes overlap")
    old_combined = {**old_index, **extra_index}
    require(len(index) == EXPECTED_TOTAL and len(old_combined) == EXPECTED_OLD
            and set(old_combined) <= set(index), "Unexpected current/retained census sets")
    for blob, fixed in old_combined.items():
        require(compact_identity(fixed) == compact_identity(index[blob]),
                "The R78 index changed an inherited text identity: " + blob)
    new_set = set(index) - set(old_combined)
    require(len(new_set) == EXPECTED_NEW, "The exact R78 delta is not 113 blobs")
    require(sum(row["bytes"] for row in index.values()) == EXPECTED_BYTES
            and sum(index[blob]["bytes"] for blob in new_set) == EXPECTED_DELTA_BYTES,
            "Unexpected current/delta uncompressed byte total")

    parts = []
    part_receipts = []
    concatenated = hashlib.sha256()
    compressed_bytes = 0
    for record in manifest["base"]["parts"]:
        relative = R77_AUDIT + "/history-base-parts/" + PurePosixPath(record["path"]).name
        path = source_file(root, relative)
        identity = authenticate_file(path, record, concatenated)
        parts.append(path)
        part_receipts.append({"path": relative, **identity})
        compressed_bytes += identity["bytes"]
    require(compressed_bytes == manifest["base"]["bytes"]
            and concatenated.hexdigest() == manifest["base"]["sha256"],
            "Concatenated retained base archive differs")
    old_delta_path = source_file(root, R77_AUDIT + "/history-delta/HISTORICAL_TEXT_DELTA_R77.tar.gz")
    old_delta_identity = authenticate_file(old_delta_path, manifest["delta"])
    extension_path = source_file(root, R77_AUDIT + "/all-ref-scope-extension/ADDITIONAL_TEXT_CORPUS.tar.gz")
    extension_identity = authenticate_file(extension_path, manifest["all_ref_extension"]["archive"])
    new_delta_path = source_file(root, R78_AUDIT + "/HISTORICAL_TEXT_DELTA_R78.tar.gz")
    new_delta_identity = authenticate_file(new_delta_path,
                                         {"bytes": R78_DELTA_BYTES, "sha256": R78_DELTA_SHA256})
    old_delta_set = {row["git_blob"] for row in manifest["delta"]["members"]}
    require(len(old_delta_set) == manifest["delta"]["member_count"]
            and old_delta_set <= set(old_index), "Invalid old-delta member list")
    base_set = set(old_index) - old_delta_set
    require(len(base_set) == manifest["base"]["member_count"],
            "Unexpected retained base member count")
    seen: set[str] = set()
    groups = [stream_members(parts, index, base_set, seen, "retained_R76_base"),
              stream_members([old_delta_path], index, old_delta_set, seen, "retained_R77_delta"),
              stream_members([extension_path], index, set(extra_index), seen, "retained_R77_all_ref_extension"),
              stream_members([new_delta_path], index, new_set, seen, "R78_delta")]
    require(seen == set(index) and sum(row["authenticated_uncompressed_bytes"] for row in groups) == EXPECTED_BYTES,
            "Portable archive reconstruction differs from the complete current census")
    receipt = {"schema": "theta.r78.portable-history-reconstruction.v1", "status": "PASS",
               "started_utc": started, "completed_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "source_root": str(root), "command": [sys.executable, *sys.argv],
               "verifier_sha256": sha256(Path(__file__).read_bytes()),
               "r77_manifest_sha256": R77_MANIFEST_SHA256,
               "r78_census_index_sha256": R78_INDEX_SHA256,
               "retained_base_parts": part_receipts,
               "retained_base_concatenated_archive_sha256": concatenated.hexdigest(),
               "retained_r77_delta_archive": old_delta_identity,
               "retained_all_ref_extension_archive": extension_identity,
               "r78_delta_archive": {**new_delta_identity, "members": EXPECTED_NEW,
                                     "uncompressed_bytes": EXPECTED_DELTA_BYTES,
                                     "overlap_with_retained_archives": 0},
               "groups": groups, "retained_text_blobs": EXPECTED_OLD,
               "added_text_blobs": EXPECTED_NEW, "total_unique_text_blobs": len(seen),
               "total_authenticated_uncompressed_bytes": EXPECTED_BYTES,
               "decoded_text_blobs": len(seen),
               "latin1_log_blobs": sorted(blob for row in groups for blob in row["latin1_log_blobs"]),
               "duplicate_members": 0, "hash_mismatches": 0, "missing_members": 0,
               "uses_git": False, "uses_network": False, "uses_external_workspace": False,
               "extracts_archives": False,
               "scope": "Portable exact historical-text reconstruction and decoding only; not mathematical reproof, a new referee report, priority certification, independent human assessment or editorial approval."}
    target = args.receipt.resolve()
    protected = {old_manifest_path, index_path, old_index_path, extra_index_path,
                 old_delta_path, extension_path, new_delta_path, *parts, Path(__file__).resolve()}
    require(target not in {path.resolve() for path in protected},
            "The receipt target would overwrite a required source input")
    target.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(receipt, indent=2, sort_keys=True) + "\n"
    target.write_text(raw, encoding="utf-8")
    print(raw, end="")


if __name__ == "__main__":
    main()
