#!/usr/bin/env python3
"""Freeze and verify an exact C1/C2 transport evidence snapshot in scratch only."""

import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import io
import json
import lzma
import os
from pathlib import Path
import stat
import sys
import tarfile
import traceback


WORK = Path(__file__).resolve().parents[1]


def require(value, message):
    if not value:
        raise RuntimeError(message)


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def blob(data):
    return hashlib.sha1(b"blob " + str(len(data)).encode("ascii") + b"\0" + data).hexdigest()


def read_stable(path):
    before = path.stat(follow_symlinks=False)
    require(stat.S_ISREG(before.st_mode), "Only ordinary files are archived: " + str(path))
    data = path.read_bytes()
    after = path.stat(follow_symlinks=False)
    require((before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns) ==
            (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns), "File stayed stable during its read")
    require(len(data) == after.st_size, "Complete source bytes")
    return data, stat.S_IMODE(after.st_mode)


def phase_for(path):
    name = path.lower()
    if "/c2-" in name or "/c2_" in name:
        return "C2"
    if "/c1-" in name or "/c1_" in name:
        return "C1"
    return "shared_preparation_or_provenance"


def file_class(path):
    if path.startswith("current-transport-operations/"):
        return "saved_operation_or_retry_preparation_record"
    if "/blob-parts/" in path:
        return "generated_base64_transport_chunk"
    if any(part in path for part in ("/blob-payloads/", "/article-batches/", "/control-trees/")) or path.endswith("NESTED_ROOT_REQUEST.json"):
        return "generated_request_payload"
    if path.endswith("EXPECTED_FILE_IDENTITIES.json"):
        return "complete_staged_article_inventory"
    if path.endswith(".py"):
        return "local_helper_source"
    if path.endswith("PLAN.json"):
        return "generated_plan_not_an_execution_receipt"
    return "local_verification_or_documentation"


def operation_kind(path):
    name = path.lower()
    if "/c1-blobs/" in name or "create_blob" in name:
        return "create_blob"
    if "/c1-article-trees/" in name or "create_article_tree" in name:
        return "create_article_tree"
    if "/c1-control-trees/" in name:
        return "create_root_tree" if name.endswith("/root.json") else "create_control_tree"
    if any(part in name for part in ("commit_base_root_retry", "nested_path_root_retry", "create_nested_root", "root_direct_retry_response")):
        return "create_root_tree"
    if "create_commit" in name:
        return "create_commit"
    if "create_branches" in name:
        return "create_ref"
    if "fast_forward_refs" in name:
        return "update_ref"
    if any(part in name for part in ("remote_readback", "precreation_ref_checks", "after_timeout_fetch")):
        return "read_only_lookup"
    return "other_saved_tool_response"


def response_rows(value, pointer=""):
    if isinstance(value, dict):
        if isinstance(value.get("isError"), bool) and ("content" in value or "structuredContent" in value):
            yield pointer or "/", value
            return
        for key, child in value.items():
            escaped = str(key).replace("~", "~0").replace("/", "~1")
            yield from response_rows(child, pointer + "/" + escaped)
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from response_rows(child, pointer + "/" + str(index))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    out = args.output.resolve()
    require(out.is_relative_to(WORK / "current-publication-evidence") and not out.exists(), "A fresh scratch evidence directory")
    out.mkdir(parents=True)
    events = []

    def emit(phase, **values):
        row = {"phase": phase, "observed_utc": now(), **values}
        events.append(row)
        with (out / "PHASE_EVENTS.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(row, sort_keys=True) + "\n")
        print(json.dumps(row, sort_keys=True), flush=True)

    def save(name, value):
        path = out / name
        require(not path.exists(), "Never overwrite existing evidence")
        path.write_text(json.dumps(value, sort_keys=True, indent=2) + "\n", encoding="utf-8")

    try:
        started = now()
        directories = [WORK / "current-transport", WORK / "current-transport-operations"]
        sources = sorted((path for directory in directories for path in directory.rglob("*") if path.is_file()),
                         key=lambda path: path.relative_to(WORK).as_posix())
        require(sources, "A real transport corpus is present")
        inputs, source_map = [], {}
        for path in sources:
            data, mode = read_stable(path)
            relative = path.relative_to(WORK).as_posix()
            require(relative not in source_map, "No duplicate evidence path")
            row = {"path": relative, "bytes": len(data), "sha256": digest(data), "git_blob_sha": blob(data),
                   "file_mode": format(mode, "04o"), "git_mode": "100755" if mode & 0o111 else "100644",
                   "phase": phase_for(relative), "classification": file_class(relative)}
            inputs.append(row)
            source_map[relative] = row
        for path, expected in {
            "current-transport/prepare_git_transport.py": "ca8891fa527e3836ba916fda521c14eacd6dda00e37fe0091bd8d8d2bb344d42",
            "current-transport/c1-staged-753cfd8/TRANSPORT_PLAN.json": "80bbafc24d887cf7cd5bdde8c620685537d2290456fc04daa2e63c2612c040b7",
            "current-transport/c1-staged-753cfd8/EXPECTED_FILE_IDENTITIES.json": "24a4681755df84e5806863682f6ae67ffc7db5f7395c3827879e5cf4d9e5ad98",
            "current-transport/c1-independent-replay.json": "d81674b009da05fa3091158ad8bdffa838b276491c353eb5346b4a7320fd36bd",
        }.items():
            require(source_map[path]["sha256"] == expected, "The sealed C1 identity is unchanged: " + path)
        snapshot_cutoff = now()
        emit("source_snapshot_identified", files=len(inputs), bytes=sum(row["bytes"] for row in inputs),
             cutoff_utc=snapshot_cutoff)
        save("SOURCE_FILE_IDENTITIES.json", {"schema": 1, "snapshot_started_utc": started,
            "snapshot_identified_utc": snapshot_cutoff, "scope": "All files in both explicit transport directories at this cutoff; C1, C2 and shared preparation are individually labelled.",
            "source_roots": [path.name for path in directories], "files": inputs})

        operations, no_response = [], []
        for row in inputs:
            relative = row["path"]
            if not relative.startswith("current-transport-operations/"):
                continue
            value = json.loads((WORK / relative).read_bytes())
            found = list(response_rows(value))
            if not found:
                no_response.append({"path": relative, "scope": "No actual tool response is stored in this file; it is not counted as an executed operation."})
            for pointer, response in found:
                structured = response.get("structuredContent", {})
                structured = structured if isinstance(structured, dict) else {}
                canonical_response = json.dumps(response, ensure_ascii=True, sort_keys=True, separators=(",", ":")).encode("ascii")
                record = {"file": relative, "response_json_pointer": pointer, "phase": phase_for(relative),
                          "operation_kind": operation_kind(relative), "isError": response["isError"],
                          "response_canonical_json_sha256": digest(canonical_response)}
                for key in ("sha", "branch", "success", "error_code", "error_data"):
                    if key in structured:
                        record[key] = structured[key]
                operations.append(record)
        observed_counts = Counter((row["phase"], row["operation_kind"], "error" if row["isError"] else "response_without_error") for row in operations)
        save("ACTUAL_OPERATION_INDEX.json", {"schema": 1, "source_snapshot_identified_utc": snapshot_cutoff,
            "scope": "One row per actual saved outer MCP response locator. Generated payloads, repeated nested content representations and prepared-only retry plans are not extra executed requests. No remote request is made by this packager.",
            "counts": [{"phase": phase, "operation_kind": kind, "outcome": outcome, "response_count": count}
                       for (phase, kind, outcome), count in sorted(observed_counts.items())],
            "actual_response_locators": operations, "operation_files_without_a_response": no_response})

        c1 = json.loads((WORK / "current-transport/c1-staged-753cfd8/TRANSPORT_PLAN.json").read_bytes())
        for row in c1["base64_blob_uploads"]:
            actual = json.loads((WORK / "current-transport-operations/c1-blobs" / (row["expected_blob_sha"] + ".json")).read_bytes())
            require(actual["expected_blob_sha"] == row["expected_blob_sha"] and actual["bytes"] == row["bytes"]
                    and actual["source_sha256"] == row["sha256"] and not actual["actual_response"]["isError"]
                    and actual["actual_response"]["structuredContent"]["sha"] == row["expected_blob_sha"], "Exact actual C1 blob receipt matches its generated request")
        for row in c1["article_batches"]:
            actual = json.loads((WORK / "current-transport-operations/c1-article-trees" / (str(row["index"]).zfill(4) + ".json")).read_bytes())
            require(actual["index"] == row["index"] and actual["base_tree_sha"] == row["base_tree_sha"]
                    and actual["payload_sha256"] == row["payload_sha256"] and not actual["actual_response"]["isError"]
                    and actual["actual_response"]["structuredContent"]["sha"] == row["expected_tree_sha"], "Exact actual C1 article-tree receipt matches its generated request")
        nested = json.loads((WORK / "current-transport-operations/C1_NESTED_PATH_ROOT_RETRY.json").read_bytes())
        require(not nested["actual_response"]["isError"] and
                nested["actual_response"]["structuredContent"]["sha"] == c1["expected_root_tree_sha"], "Actual successful nested-path root")
        commit_record = json.loads((WORK / "current-transport-operations/C1_CREATE_COMMIT.json").read_bytes())
        c1_commit = commit_record["actual_response"]["structuredContent"]["sha"]
        require(c1_commit == "409fc85c84a5f239d071b8452da48cb73694365f" and
                commit_record["request"]["tree_sha"] == c1["expected_root_tree_sha"] and
                commit_record["request"]["parent_sha"] == "0933e9b44f5b0fd1d1a624d37ffd881d352496f8", "Actual C1 commit/tree/parent linkage")
        branches = json.loads((WORK / "current-transport-operations/C1_CREATE_BRANCHES.json").read_bytes())
        require(len(branches) == 3 and all(not row["actual_response"]["isError"] and row["request"]["sha"] == c1_commit
                and row["actual_response"]["structuredContent"]["branch"] == row["request"]["branch_name"] for row in branches), "Actual three new C1 ref responses")
        readbacks = json.loads((WORK / "current-transport-operations/C1_INITIAL_REMOTE_READBACK.json").read_bytes())
        bodies = {row["url"]: json.loads(row["response"]["structuredContent"]["content"]) for row in readbacks}
        api = "https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/"
        actual_commit = bodies[api + "commits/" + c1_commit]
        require(actual_commit["sha"] == c1_commit and actual_commit["tree"]["sha"] == c1["expected_root_tree_sha"]
                and [row["sha"] for row in actual_commit["parents"]] == ["0933e9b44f5b0fd1d1a624d37ffd881d352496f8"], "Actual C1 GET commit linkage")
        actual_root = bodies[api + "trees/" + c1["expected_root_tree_sha"]]
        require(actual_root["sha"] == c1["expected_root_tree_sha"] and actual_root.get("truncated") is False, "Actual nontruncated C1 root GET")
        for row in branches:
            reference = bodies[api + "ref/heads/" + row["request"]["branch_name"]]
            require(reference["object"]["sha"] == c1_commit, "Actual C1 ref GET matches the created commit")

        # Put each full blob request directly before its original base64 pieces.
        # A 16 MiB LZMA dictionary can retain the largest full request (under 8 MiB)
        # while compressing its duplicate chunks. Every original file is retained.
        paths = [row["path"] for row in inputs]
        deferred = {path for path in paths if "/blob-payloads/" in path or "/blob-parts/" in path}
        order = sorted(set(paths) - deferred)
        for payload in sorted(path for path in deferred if "/blob-payloads/" in path):
            prefix, filename = payload.split("/blob-payloads/", 1)
            identity = filename.removesuffix(".json")
            order.append(payload)
            order.extend(sorted(path for path in deferred if path.startswith(prefix + "/blob-parts/" + identity + "/")))
        require(len(order) == len(paths) and set(order) == set(paths), "Archive order retains every source file exactly once")
        archive = out / "C1_C2_TRANSPORT_SNAPSHOT.tar.xz"
        filters = [{"id": lzma.FILTER_LZMA2, "dict_size": 16 * 1024 * 1024,
                    "lc": 3, "lp": 0, "pb": 2, "mode": lzma.MODE_NORMAL,
                    "nice_len": 64, "mf": lzma.MF_BT4, "depth": 0}]
        emit("archive_compression_started", members=len(order))
        with lzma.open(archive, "wb", format=lzma.FORMAT_XZ, check=lzma.CHECK_CRC64, filters=filters) as compressed:
            with tarfile.open(fileobj=compressed, mode="w|", format=tarfile.PAX_FORMAT) as tar:
                for relative in order:
                    data, mode = read_stable(WORK / relative)
                    expected = source_map[relative]
                    require(len(data) == expected["bytes"] and digest(data) == expected["sha256"], "Snapshot bytes remain exact during packing")
                    info = tarfile.TarInfo(relative)
                    info.size = len(data)
                    info.mode = mode
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mtime = 0
                    tar.addfile(info, io.BytesIO(data))
        archive_data = archive.read_bytes()
        archive_identity = {"path": archive.name, "bytes": len(archive_data), "sha256": digest(archive_data), "git_blob_sha": blob(archive_data)}
        emit("archive_compression_finished", **archive_identity)
        seen = []
        with tarfile.open(archive, mode="r|xz") as tar:
            for member in tar:
                require(member.isfile() and member.name in source_map and member.name not in seen, "Safe unique ordinary archive member")
                expected = source_map[member.name]
                require(member.size == expected["bytes"] and member.mode == int(expected["file_mode"], 8)
                        and member.uid == member.gid == member.mtime == 0 and member.uname == member.gname == "", "Exact canonical tar header")
                data = tar.extractfile(member).read()
                require(len(data) == expected["bytes"] and digest(data) == expected["sha256"]
                        and blob(data) == expected["git_blob_sha"], "Every decompressed member exactly reconstructs its original bytes")
                seen.append(member.name)
        require(seen == order, "Complete exact archive-member order")
        for relative in order:
            data, mode = read_stable(WORK / relative)
            require(digest(data) == source_map[relative]["sha256"] and format(mode, "04o") == source_map[relative]["file_mode"], "All snapshot source files stayed unchanged during packaging")
        later_paths = sorted(path.relative_to(WORK).as_posix() for directory in directories
                             for path in directory.rglob("*") if path.is_file() and path.relative_to(WORK).as_posix() not in source_map)
        emit("all_members_and_original_sources_verified", members=len(seen), later_files_outside_snapshot=len(later_paths))
        (out / "build_transport_evidence.py").write_bytes(Path(__file__).read_bytes())
        receipt = {"schema": 1, "status": "passed", "started_utc": started, "finished_utc": now(),
            "source_snapshot_identified_utc": snapshot_cutoff, "python": sys.version,
            "program_sha256": digest(Path(__file__).read_bytes()), "archive": archive_identity,
            "source_file_count": len(inputs), "source_bytes": sum(row["bytes"] for row in inputs),
            "source_phase_counts": dict(Counter(row["phase"] for row in inputs)),
            "source_classification_counts": dict(Counter(row["classification"] for row in inputs)),
            "saved_operation_file_count": sum(row["path"].startswith("current-transport-operations/") for row in inputs),
            "actual_saved_response_locators": len(operations), "operation_files_without_response": len(no_response),
            "verified_c1_blob_receipts": len(c1["base64_blob_uploads"]),
            "verified_c1_article_tree_receipts": len(c1["article_batches"]),
            "verified_c1_commit": c1_commit, "verified_c1_root": c1["expected_root_tree_sha"],
            "verified_c1_initial_ref_readbacks": 3, "verified_c1_nontruncated_root_readback": True,
            "archive_members_read_and_hashed": len(seen), "archive_member_order": order,
            "compression": {"format": "xz", "check": "CRC64", "filters": filters,
                            "tar_format": "PAX", "all_mtimes": 0, "all_uid_gid": 0,
                            "all_uname_gname": "", "mode_policy": "exact original permission mode"},
            "later_files_outside_snapshot": later_paths,
            "scope": "Exact local evidence preservation and readback reconstruction. C1 and C2 records are separately labelled. This packager performs no Git, article/index, remote, commit/ref or CI action. No CI success or continuous mathematical theorem is inferred."}
        save("ARCHIVE_VERIFICATION_RECEIPT.json", receipt)
        readme = f"""# C1 complete transport and C2 CI-trigger transport: exact evidence snapshot

This package preserves all files present in `current-transport` and `current-transport-operations` at the recorded snapshot cutoff **{snapshot_cutoff}**. The directory name is historical; the manifest explicitly labels **C1**, **C2**, and shared local preparation. C2 operations are never counted as C1 operations.

The archive contains **{len(inputs)} original files**, totaling **{sum(row['bytes'] for row in inputs):,} uncompressed bytes**. Every original full request payload, all base64 chunks, both staged-tree plans and complete inventories, the unchanged sealed planner, independent replay, root-timeout diagnosis and all actual operation records at this cutoff are retained byte for byte. No redundant source file was silently dropped. The deterministic tar headers retain original file modes and fix owner/time metadata; the documented member order places each complete blob request immediately before its exact chunks. XZ with a 16 MiB dictionary compresses those duplicate bytes without changing any member.

`C1_C2_TRANSPORT_SNAPSHOT.tar.xz` is **{len(archive_data):,} bytes**, SHA-256 **`{digest(archive_data)}`**. The archive was reopened and **every member** was read, size/hash/Git-blob checked and compared with its original source. No archive code was executed or extracted during verification.

## Files and their meanings

- `SOURCE_FILE_IDENTITIES.json`: every original member path, bytes, SHA-256, Git blob, permissions, phase and evidence class.
- `ACTUAL_OPERATION_INDEX.json`: exact file and JSON-pointer locators for each saved outer MCP response. Nested duplicate content representations are counted once. Generated payloads and the prepared but unexecuted GitHub-only incremental root plan do not become execution receipts.
- `ARCHIVE_VERIFICATION_RECEIPT.json`: actual execution times, archive identity, all-member verification, C1 request/response matching and original commit/root/ref GET linkage, deterministic compression settings, and the explicit snapshot cutoff.
- `PHASE_EVENTS.jsonl`: the actual packaging phases as they occurred.
- `build_transport_evidence.py`: the exact new standard-library packaging source.
- `PACKAGE_FILE_IDENTITIES.json`: identities of this package's files except the identity file itself, avoiding a fictitious self-reference.

The complete C1 scientific commit is **`409fc85c84a5f239d071b8452da48cb73694365f`**, with root **`753cfd8589bc0b7c93942a727ed6925abc214bc2`** and sole parent **`0933e9b44f5b0fd1d1a624d37ffd881d352496f8`**. This packager independently matched the 98 actual base64 blob responses and 28 actual article-tree responses to the generated plan, and parsed the saved actual C1 commit/root/three-ref GET readbacks. The 336 inline blob creations are contents inside tree requests, not 336 separate `create_blob` calls.

All root failures remain: the tree-base immediate-pointer timeout, the baseless all-root-entries timeout, the additional commit-base timeout, and the root lookup that returned 404 before success. The exact successful C1 nested-path request returned the originally expected root. The earlier unchanged diagnosis was written before this combined snapshot; the later commit-base retry is additionally preserved and separately indexed here. No absent historical successful request fields are invented.

C2 uses its own plan and actual response records, including the full-article-path root request. Its expected root is **`b5d618b8a4b356f8ca07f1c9f1238e35d879ede8`** and expected article tree **`b4add0580cc8211223dfa57e6e618e2bf9546d09`**. The manifest and operation index identify all C2 files actually present at the snapshot cutoff. Later files, if any appeared during packaging, are listed separately in the verification receipt and must be archived in the later evidence package; their bytes are not fabricated here.

This is an exact **transport evidence** package. It does not claim that either a prepared request or a created tree constitutes completed CI. Actual CI observation and artifact verification have their separate receipts. This script made no network request, Git change, article/index modification, commit or ref update. Successful finite transport checks do not complete the Lorentz-gas continuum proof obligations.
"""
        (out / "README.md").write_text(readme, encoding="utf-8")
        package_rows = []
        for path in sorted(out.iterdir()):
            if path.is_file():
                data = path.read_bytes()
                package_rows.append({"path": path.name, "bytes": len(data), "sha256": digest(data), "git_blob_sha": blob(data)})
        save("PACKAGE_FILE_IDENTITIES.json", {"schema": 1, "self_excluded": "PACKAGE_FILE_IDENTITIES.json", "files": package_rows})
        print(json.dumps({"status": "passed", "package": str(out), "archive": archive_identity,
                          "source_files": len(inputs), "actual_saved_response_locators": len(operations)}, indent=2), flush=True)
    except Exception as error:
        save("FAILED_PACKAGING_RECEIPT.json", {"status": "failed", "observed_utc": now(),
                                              "error": repr(error), "traceback": traceback.format_exc()})
        raise


if __name__ == "__main__":
    try:
        main()
    except Exception as error:
        sys.stderr.write(type(error).__name__ + ": " + str(error) + "\n")
        raise SystemExit(1)
