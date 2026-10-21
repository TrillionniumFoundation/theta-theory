#!/usr/bin/env python3
"""Verify and restore complete General Theta delivery archives.

Uses only Python's standard library. Identities come from the actual delivery
manifests; no source commit, publication commit or verification result is
hard-coded. Verification reads every delivered file, every archive part,
every source/validation member, and the complete historical text corpus.
"""
from __future__ import annotations

import argparse
import contextlib
import gzip
import hashlib
import json
import os
import re
import shutil
import stat
import sys
import tarfile
import tempfile
import zipfile
from pathlib import Path, PurePosixPath

sys.dont_write_bytecode = True
CHUNK = 1024 * 1024
HISTORY_INDEX = "provenance/current-full-scan/HISTORICAL_TEXT_INDEX.json.gz"


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def unique_object(pairs: list[tuple[str, object]]) -> dict:
    result = {}
    for key, value in pairs:
        require(key not in result, "Duplicate JSON key: " + key)
        result[key] = value
    return result


def parse_json(data: bytes) -> object:
    return json.loads(data.decode("utf-8"), object_pairs_hook=unique_object)


def relative_name(value: object, *, directory: bool = False) -> str:
    require(isinstance(value, str) and bool(value), "Empty or non-string relative path")
    name = value[:-1] if directory and value.endswith("/") else value
    require(bool(name) and "\\" not in name and "\x00" not in name,
            "Unsafe relative path: " + repr(value))
    parts = name.split("/")
    require(not name.startswith("/") and all(part not in ("", ".", "..") for part in parts)
            and ":" not in parts[0], "Unsafe relative path: " + repr(value))
    require(PurePosixPath(name).as_posix() == name, "Noncanonical relative path: " + name)
    return name


def local_file(root: Path, name: str) -> Path:
    name = relative_name(name)
    path = root
    for part in PurePosixPath(name).parts:
        path = path / part
        require(not path.is_symlink(), "Symlink is not a delivery file: " + name)
    require(path.is_file(), "Missing regular delivery file: " + name)
    return path


def identity_fields(item: dict, description: str) -> None:
    require(type(item.get("bytes")) is int and item["bytes"] >= 0,
            "Invalid byte count: " + description)
    require(isinstance(item.get("sha256"), str)
            and re.fullmatch(r"[0-9a-f]{64}", item["sha256"]) is not None,
            "Invalid SHA-256: " + description)


def digest_stream(stream, size: int | None = None) -> tuple[int, str, str | None]:
    count, sha256 = 0, hashlib.sha256()
    blob = hashlib.sha1(b"blob " + str(size).encode("ascii") + b"\0") if size is not None else None
    while True:
        data = stream.read(CHUNK)
        if not data:
            break
        count += len(data)
        sha256.update(data)
        if blob is not None:
            blob.update(data)
    return count, sha256.hexdigest(), blob.hexdigest() if blob is not None else None


def verify_file(path: Path, item: dict, description: str) -> None:
    identity_fields(item, description)
    require(path.is_file() and not path.is_symlink(), "Missing regular file: " + description)
    require(path.stat().st_size == item["bytes"], "Wrong byte count: " + description)
    with path.open("rb") as stream:
        count, digest, _ = digest_stream(stream)
    require(count == item["bytes"] and digest == item["sha256"],
            "SHA-256 or byte mismatch: " + description)


def row_inventory(rows: object, description: str) -> dict[str, dict]:
    require(isinstance(rows, list) and bool(rows), "Empty or invalid file inventory: " + description)
    result = {}
    for row in rows:
        require(isinstance(row, dict), "Invalid file record: " + description)
        name = relative_name(row.get("path"))
        require(name not in result, "Duplicate file inventory path: " + name)
        identity_fields(row, name)
        result[name] = row
    return result


def archive_role(item: dict) -> str:
    name = item["file"]
    inferred = ("source" if name.endswith("_Source.zip") else
                "validation" if name.endswith("_Validation.zip") else
                "historical" if name.endswith("_Historical_Text_Corpus.tar.gz") else None)
    role = item.get("role", inferred)
    require(role in {"source", "validation", "historical"}, "Unknown archive role: " + name)
    return role


def read_delivery(root: Path, expected_commit: str | None = None,
                  expected_tree: str | None = None) -> tuple[dict, dict, dict]:
    manifest = parse_json(local_file(root, "DELIVERY_MANIFEST.json").read_bytes())
    require(isinstance(manifest, dict), "Delivery manifest must be an object")
    match = re.fullmatch(r"theta\.(r\d+)\.delivery-manifest\.v1", str(manifest.get("schema")))
    require(match is not None, "Unsupported delivery-manifest schema")
    revision = match.group(1)
    for field in ("source_commit", "source_paper_tree"):
        require(isinstance(manifest.get(field), str)
                and re.fullmatch(r"[0-9a-f]{40}", manifest[field]) is not None,
                "Missing full actual Git identity: " + field)
    if expected_commit is not None:
        require(manifest["source_commit"] == expected_commit, "Delivery source commit differs from the supplied pin")
    if expected_tree is not None:
        require(manifest["source_paper_tree"] == expected_tree, "Delivery paper tree differs from the supplied pin")
    require(manifest.get("manifest_excludes_itself") is True, "Delivery manifest must explicitly exclude only its own self-hash")
    files = row_inventory(manifest.get("files"), "delivery")
    require("DELIVERY_MANIFEST.json" not in files, "Delivery manifest cannot hash itself")
    for name, row in files.items():
        verify_file(local_file(root, name), row, name)
    require("archives/ARCHIVE_PARTS.json" in files, "Archive-parts manifest is not delivery-hashed")
    parts = parse_json(local_file(root, "archives/ARCHIVE_PARTS.json").read_bytes())
    require(isinstance(parts, dict) and parts.get("schema") == f"theta.{revision}.lossless-archive-parts.v1",
            "Archive-parts schema/revision mismatch")
    require(parts.get("source_commit") == manifest["source_commit"], "Archive-parts source commit mismatch")
    require(isinstance(parts.get("archives"), list) and len(parts["archives"]) == 3,
            "Require complete source, validation and historical archives")
    roles, archive_names, part_names = {}, set(), set()
    for item in parts["archives"]:
        require(isinstance(item, dict), "Invalid archive record")
        name = relative_name(item.get("file"))
        require("/" not in name and name not in archive_names, "Duplicate or non-flat archive filename: " + name)
        archive_names.add(name)
        identity_fields(item, name)
        require(item.get("format") == "ordered raw byte concatenation", "Unsupported archive part format: " + name)
        role = archive_role(item)
        require(role not in roles, "Duplicate archive role: " + role)
        roles[role] = item
        require(isinstance(item.get("parts"), list) and bool(item["parts"]), "Archive has no parts: " + name)
        total = 0
        for part in item["parts"]:
            path = relative_name(part.get("path"))
            identity_fields(part, path)
            require(path not in part_names, "Archive part reused or duplicated: " + path)
            part_names.add(path)
            require(path in files and all(part[key] == files[path][key] for key in ("bytes", "sha256")),
                    "Part and delivery identities disagree: " + path)
            total += part["bytes"]
        require(total == item["bytes"], "Part sizes do not sum to complete archive size: " + name)
    require(set(roles) == {"source", "validation", "historical"}, "Incomplete archive-role inventory")
    optional = manifest.get("optional_local_reconstructions_excluded", [])
    require(isinstance(optional, list) and len(set(optional)) == len(optional), "Invalid optional reconstruction list")
    require(set(optional) <= archive_names, "Optional exclusions may name only the complete declared archives")
    allowed = set(files) | {"DELIVERY_MANIFEST.json"} | set(optional)
    actual = set()
    for path in root.rglob("*"):
        require(not path.is_symlink(), "Unexpected symlink in publication directory: " + str(path))
        if path.is_file():
            actual.add(path.relative_to(root).as_posix())
    require(actual <= allowed, "Unmanifested publication files: " + ", ".join(sorted(actual - allowed)))
    for name in optional:
        path = root / name
        if path.exists():
            item = next(row for row in parts["archives"] if row["file"] == name)
            verify_file(path, item, "optional complete archive " + name)
    return manifest, parts, {"revision": revision, "roles": roles, "files": files}


@contextlib.contextmanager
def assembled_archives(root: Path, parts: dict):
    """Join parts in the declared order into temporary verified files."""
    with tempfile.TemporaryDirectory(prefix="theta-delivery-") as temporary:
        output = {}
        for item in parts["archives"]:
            target = Path(temporary) / item["file"]
            whole, total = hashlib.sha256(), 0
            with target.open("xb") as destination:
                for part in item["parts"]:
                    digest, count = hashlib.sha256(), 0
                    with local_file(root, part["path"]).open("rb") as source:
                        while True:
                            data = source.read(CHUNK)
                            if not data:
                                break
                            destination.write(data)
                            count += len(data)
                            total += len(data)
                            digest.update(data)
                            whole.update(data)
                    require(count == part["bytes"] and digest.hexdigest() == part["sha256"],
                            "Archive part mismatch: " + part["path"])
            require(total == item["bytes"] and whole.hexdigest() == item["sha256"],
                    "Reassembled archive mismatch: " + item["file"])
            output[archive_role(item)] = target
        yield output


def zip_inventory(archive: zipfile.ZipFile) -> dict[str, zipfile.ZipInfo]:
    files, names = {}, set()
    for item in archive.infolist():
        name = relative_name(item.filename, directory=item.is_dir())
        require(item.filename not in names, "Duplicate ZIP member: " + item.filename)
        names.add(item.filename)
        mode = item.external_attr >> 16
        require(not stat.S_ISLNK(mode), "ZIP symlink is not an ordinary payload: " + name)
        require(not item.flag_bits & 1, "Encrypted ZIP payload is unsupported: " + name)
        if item.is_dir():
            continue
        require(stat.S_IFMT(mode) in (0, stat.S_IFREG), "Nonregular ZIP payload: " + name)
        require(name not in files, "Duplicate normalized ZIP member: " + name)
        files[name] = item
    return files


def zip_prefix(item: dict) -> str:
    prefix = item.get("archive_prefix", item["file"][:-4] + "/")
    return relative_name(prefix, directory=True) + "/"


def verify_zip_payload(archive: zipfile.ZipFile, member: zipfile.ZipInfo,
                       row: dict, name: str, *, blob: bool = False) -> str | None:
    identity_fields(row, name)
    require(member.file_size == row["bytes"], "ZIP member size mismatch: " + name)
    with archive.open(member, "r") as stream:
        count, digest, git_blob = digest_stream(stream, row["bytes"] if blob else None)
    require(count == row["bytes"] and digest == row["sha256"], "ZIP member SHA-256 mismatch: " + name)
    if blob:
        require(git_blob == row.get("git_blob"), "ZIP member Git-blob mismatch: " + name)
    return git_blob


def git_blob(data: bytes) -> str:
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def git_tree(rows: dict[str, dict]) -> str:
    tree = {}
    for name, row in rows.items():
        node = tree
        parts = PurePosixPath(name).parts
        for part in parts[:-1]:
            child = node.setdefault(part, {})
            require(isinstance(child, dict), "File/directory conflict in source manifest: " + name)
            node = child
        require(parts[-1] not in node, "Duplicate source-tree leaf: " + name)
        require(row.get("mode") in ("100644", "100755"), "Unsupported source Git mode: " + name)
        require(re.fullmatch(r"[0-9a-f]{40}", str(row.get("git_blob"))) is not None,
                "Invalid source Git blob: " + name)
        node[parts[-1]] = (row["mode"], row["git_blob"])
    def digest(node: dict) -> str:
        entries = []
        for name, value in node.items():
            is_dir = isinstance(value, dict)
            mode, oid = ("40000", digest(value)) if is_dir else value
            sort_key = name.encode("utf-8") + (b"/" if is_dir else b"")
            payload = mode.encode("ascii") + b" " + name.encode("utf-8") + b"\0" + bytes.fromhex(oid)
            entries.append((sort_key, payload))
        body = b"".join(value for _, value in sorted(entries))
        return hashlib.sha1(b"tree " + str(len(body)).encode("ascii") + b"\0" + body).hexdigest()
    return digest(tree)


def verify_source(path: Path, item: dict, delivery: dict, revision: str) -> tuple[dict, list]:
    prefix = zip_prefix(item)
    with zipfile.ZipFile(path) as archive:
        members = zip_inventory(archive)
        manifest_name = prefix + "SOURCE_MANIFEST.json"
        require(manifest_name in members, "Source ZIP lacks its native SOURCE_MANIFEST.json")
        raw = archive.read(manifest_name)
        source = parse_json(raw)
        require(source.get("schema") == f"theta.{revision}.exact-source-manifest.v1", "Source-manifest revision mismatch")
        rows = row_inventory(source.get("files"), "source ZIP")
        require("SOURCE_MANIFEST.json" not in rows, "Source manifest unexpectedly lists itself")
        expected = {prefix + name for name in rows} | {manifest_name}
        require(set(members) == expected, "Source ZIP file membership differs from the exact native manifest")
        for name, row in rows.items():
            verify_zip_payload(archive, members[prefix + name], row, name, blob=True)
        tree_rows = dict(rows)
        tree_rows["SOURCE_MANIFEST.json"] = {"mode": "100644", "git_blob": git_blob(raw)}
        tree = git_tree(tree_rows)
        require(tree == delivery["source_paper_tree"], "Reconstructed source Git tree differs from the delivery pin")
        require(HISTORY_INDEX in rows, "Source lacks the complete historical-text identity index")
        history = parse_json(gzip.decompress(archive.read(prefix + HISTORY_INDEX)))
        require(isinstance(history, list) and bool(history), "Historical text index is empty")
        theorem_name = source.get("current_theorem_index", "THEOREM_INDEX.json")
        require(theorem_name in rows, "Source lacks its current theorem index")
        theorem_hash = rows[theorem_name]["sha256"]
    return {"payload_files": len(rows) + 1, "source_manifest_sha256": hashlib.sha256(raw).hexdigest(),
            "source_paper_tree": tree, "current_theorem_index_sha256": theorem_hash,
            "source_manifest_membership_exact": True}, history


def verify_historical(path: Path, expected_rows: list) -> dict:
    expected = {}
    for row in expected_rows:
        blob = row.get("git_blob")
        require(isinstance(blob, str) and re.fullmatch(r"[0-9a-f]{40}", blob) is not None,
                "Historical index has an invalid Git blob")
        name = "blobs/" + blob + ".txt"
        require(name not in expected, "Duplicate historical identity: " + blob)
        identity_fields(row, name)
        require(row.get("encoding") in ("utf-8", "latin-1"), "Unexpected historical text encoding: " + name)
        expected[name] = row
    seen, total, encodings = set(), 0, {}
    with tarfile.open(path, "r:gz") as archive:
        for item in archive:
            name = relative_name(item.name, directory=item.isdir())
            require(name not in seen, "Duplicate TAR member: " + name)
            if item.isdir():
                continue
            require(item.isfile(), "Nonregular historical TAR member: " + name)
            require(name in expected, "Unexpected historical TAR member: " + name)
            seen.add(name)
            row = expected[name]
            require(item.size == row["bytes"], "Historical member size mismatch: " + name)
            stream = archive.extractfile(item)
            require(stream is not None, "Unreadable historical member: " + name)
            with stream:
                data = stream.read()
            require(len(data) == row["bytes"] and hashlib.sha256(data).hexdigest() == row["sha256"]
                    and git_blob(data) == row["git_blob"], "Historical member identity mismatch: " + name)
            text = data.decode(row["encoding"])
            require(text.encode(row["encoding"]) == data, "Historical decoding is not byte reversible: " + name)
            total += len(data)
            encodings[row["encoding"]] = encodings.get(row["encoding"], 0) + 1
    require(seen == set(expected), "Historical corpus is missing indexed blobs")
    return {"payload_files": len(seen), "payload_bytes": total, "encodings": encodings,
            "full_index_membership_exact": True, "git_blob_sha256_and_bytes_checked": True}


def verify_validation(path: Path, item: dict, root: Path, delivery: dict,
                      revision: str, source_result: dict) -> dict:
    prefix = zip_prefix(item)
    with zipfile.ZipFile(path) as archive:
        members = zip_inventory(archive)
        manifest_relative = item.get("internal_manifest", "ARCHIVE_MANIFEST.json")
        manifest_name = prefix + relative_name(manifest_relative)
        require(manifest_name in members, "Validation ZIP lacks ARCHIVE_MANIFEST.json")
        internal = parse_json(archive.read(manifest_name))
        require(internal.get("schema") == f"theta.{revision}.validation-archive.v1", "Validation archive schema/revision mismatch")
        require(internal.get("source_commit") == delivery["source_commit"], "Validation archive source commit mismatch")
        require(internal.get("manifest_excludes_itself") is True, "Validation manifest must explicitly exclude itself")
        rows = row_inventory(internal.get("files"), "validation ZIP")
        require(manifest_relative not in rows, "Validation manifest cannot list itself")
        expected = {prefix + name for name in rows} | {manifest_name}
        require(set(members) == expected, "Validation ZIP membership differs from its internal manifest")
        for name, row in rows.items():
            verify_zip_payload(archive, members[prefix + name], row, name)
        receipt_relative = internal.get("build_receipt", "build/BUILD_RECEIPT.json")
        require(receipt_relative in rows, "Validation ZIP lacks its declared strict build receipt")
        receipt_raw = archive.read(prefix + receipt_relative)
        receipt = parse_json(receipt_raw)
        require(receipt.get("schema") == f"theta.{revision}.native-verification.v1", "Build-receipt schema/revision mismatch")
        require(receipt.get("status") == "PASS" and receipt.get("mode") == "strict", "Stored receipt is not a successful strict execution")
        require(receipt.get("declared_source_commit") == delivery["source_commit"]
                and receipt.get("source_commit_verified") is True, "Stored receipt does not verify the delivered source commit")
        require(receipt.get("diagnostics_skipped") is False and receipt.get("ordinary_optimized_identity") is True,
                "Stored strict receipt skipped diagnostics or lacks ordinary/optimized identity")
        require(receipt.get("source_unchanged_during_build") is True
                and receipt.get("sealed_theorem_index_matched") is True, "Stored strict receipt lacks unchanged-source/index gates")
        require(receipt.get("source_git_tree_before") == receipt.get("source_git_tree_after")
                == delivery["source_paper_tree"], "Stored receipt's source tree differs from the delivered tree")
        require(receipt.get("source_manifest_sha256") == source_result["source_manifest_sha256"]
                and receipt.get("source_files_verified") == source_result["payload_files"],
                "Stored receipt's source inventory differs from the delivered source ZIP")
        require(receipt.get("generated_theorem_index_sha256") == source_result["current_theorem_index_sha256"],
                "Stored receipt's theorem index differs from the delivered source")
        require(receipt.get("git_identity", {}).get("head") == delivery["source_commit"]
                and receipt.get("git_identity", {}).get("committed_paper_tree") == delivery["source_paper_tree"],
                "Stored receipt's committed Git identities differ")
        if "BUILD_RECEIPT.json" in {row["path"] for row in delivery["files"]}:
            require(local_file(root, "BUILD_RECEIPT.json").read_bytes() == receipt_raw,
                    "Top-level and archived strict build receipts differ")
        documents = receipt.get("documents")
        require(isinstance(documents, list) and len(documents) == 3, "Stored build must contain manuscript, supplement and companion")
        require({row.get("document") for row in documents} == {"manuscript", "supplement", "companion"},
                "Stored build document roles are incomplete")
        for document in documents:
            name = relative_name(document.get("file"))
            require(name in {row["path"] for row in delivery["files"]}, "Compiled PDF is not a declared delivery file: " + name)
            verify_file(local_file(root, name), document, "compiled PDF " + name)
            text_name = "build/" + relative_name(document.get("text_file"))
            require(text_name in rows and rows[text_name]["sha256"] == document.get("text_sha256"),
                    "Archived extracted PDF text differs from the stored receipt: " + name)
    return {"payload_files": len(rows), "internal_manifest_membership_exact": True,
            "stored_strict_receipt_identity_verified": True,
            "stored_source_commit": receipt["declared_source_commit"],
            "stored_diagnostic_suite_count": receipt["diagnostic_suite_count"],
            "stored_compiled_statement_count": receipt["compiled_statement_count"],
            "stored_total_checks": receipt["total_checks"],
            "compiled_pdf_hashes_match_stored_receipt": True,
            "build_or_diagnostics_executed_now": False}


def verify_contents(root: Path, delivery: dict, metadata: dict, paths: dict) -> dict:
    source, historical_index = verify_source(paths["source"], metadata["roles"]["source"], delivery, metadata["revision"])
    history = verify_historical(paths["historical"], historical_index)
    validation = verify_validation(paths["validation"], metadata["roles"]["validation"], root,
                                   delivery, metadata["revision"], source)
    return {"status": "PASS", "revision": metadata["revision"],
            "source_commit": delivery["source_commit"], "source_paper_tree": delivery["source_paper_tree"],
            "publication_files_verified": len(delivery["files"]),
            "archive_parts_verified": sum(len(row["parts"]) for row in metadata["roles"].values()),
            "complete_archives_verified": 3,
            "archives": {role: {"file": item["file"], "bytes": item["bytes"], "sha256": item["sha256"]}
                         for role, item in metadata["roles"].items()},
            "source_archive": source, "historical_archive": history, "validation_archive": validation,
            "scope": "Received byte, archive, Git-tree and stored-receipt consistency only. This does not rerun the build, diagnostics, mathematical proofs, human review or an editorial decision."}


def arguments(description: str, *, restore: bool) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parent,
                        help="Directory containing the complete publication delivery (default: this script's directory)")
    parser.add_argument("--expect-source-commit", help="Optional independently pinned full source commit")
    parser.add_argument("--expect-paper-tree", help="Optional independently pinned full source paper tree")
    if restore:
        parser.add_argument("--out", type=Path, required=True, help="Directory for the three complete archives; existing differing files are never replaced")
    return parser.parse_args()


def main() -> None:
    args = arguments(__doc__, restore=True)
    root = args.root.resolve()
    delivery, parts, metadata = read_delivery(root, args.expect_source_commit, args.expect_paper_tree)
    output = args.out.resolve()
    require(output == root or root not in output.parents,
            "Use an output directory outside the publication folder, or the publication folder itself")
    if output == root:
        require({item["file"] for item in parts["archives"]}
                <= set(delivery.get("optional_local_reconstructions_excluded", [])),
                "In-place reconstructions are not declared in the delivery manifest")
    with assembled_archives(root, parts) as paths:
        report = verify_contents(root, delivery, metadata, paths)
        output.mkdir(parents=True, exist_ok=True)
        restored = []
        for role, item in metadata["roles"].items():
            target = output / item["file"]
            require(not target.is_symlink(), "Refusing a symlink output: " + str(target))
            if target.exists():
                verify_file(target, item, "existing reconstruction " + str(target))
                action = "existing identical file retained"
            else:
                created = False
                try:
                    with target.open("xb") as destination, paths[role].open("rb") as source:
                        created = True
                        shutil.copyfileobj(source, destination, CHUNK)
                        destination.flush()
                        os.fsync(destination.fileno())
                    verify_file(target, item, "restored archive " + str(target))
                except BaseException:
                    if created:
                        target.unlink(missing_ok=True)
                    raise
                action = "restored and verified"
            restored.append({"file": str(target), "action": action, "bytes": item["bytes"], "sha256": item["sha256"]})
        report["restored"] = restored
    print(json.dumps(report, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, KeyError, TypeError, zipfile.BadZipFile, tarfile.TarError) as error:
        raise SystemExit("FAIL: " + str(error)) from error
