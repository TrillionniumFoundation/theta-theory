#!/usr/bin/env python3
"""Check immutable source preservation and the declared active TeX closure.

Pure standard library; no Git executable, network, or optional package is used.
All gates use explicit exceptions, including under python -O. This verifies
source identity and static native-source closure, not mathematical truth.

Public API:
    tex_closure(root: Path) -> dict
    verify(root: Path, manifest_required: bool = True) -> dict
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import stat
import sys

BASE_COMMIT = "6cdd9ae88cd358d524ecb89092361ac1522ba351"
BASE_ROOT_TREE = "49f5bd3917dcedf64a96bd47507c5d6033d43543"
BASE_ARTICLE_TREE = "a1d21789f9d7c1be801ff4a54d1befad2a47340f"
ANCHOR_SHA256 = "e49c3b8d9002cc2e431a4e7b846490a5a9f347f47fa236a1c609146f16bcfe1b"
ANCHOR_PATH = "CURRENT_SOURCE_ANCHOR.json"
CENSUS = "audit/current-census"
ARCHIVE = "history/predecessor"
CORE_RE = re.compile(r"core/(\d+)_[^/]+\.tex")
INPUT_RE = re.compile(r"\\(?:input|include)\b\s*(?:\{([^{}]*)\}|([^\s{}]+))")
LABEL_RE = re.compile(r"\\label\s*\{([^{}]+)\}")
REF_RE = re.compile(
    r"\\(?:ref|eqref|pageref|autoref|nameref|[cC]ref|[vV]ref|[cC]pageref)"
    r"\*?\s*\{([^{}]+)\}"
)


class VerificationError(RuntimeError):
    """An explicit failure that remains active with optimized Python."""


def require(condition: bool, message: str) -> None:
    if not condition:
        raise VerificationError(message)


def checked_path(root: Path, relative: str) -> Path:
    q = PurePosixPath(relative)
    require(bool(relative) and not q.is_absolute() and ".." not in q.parts
            and str(q) == relative, f"Unsafe or noncanonical path: {relative!r}")
    current = root
    for part in q.parts:
        current = current / part
        require(not current.is_symlink(), f"Symlink in retained source path: {relative}")
    return current


def identity(path: Path) -> dict:
    require(path.is_file(), f"Missing source file: {path}")
    before = path.stat()
    require(stat.S_ISREG(before.st_mode), f"Nonregular source file: {path}")
    sha1 = hashlib.sha1(b"blob " + str(before.st_size).encode() + b"\0")
    sha256 = hashlib.sha256()
    count = 0
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            count += len(chunk)
            sha1.update(chunk)
            sha256.update(chunk)
    require(count == before.st_size, f"File changed while hashing: {path}")
    return {"bytes": count, "git_blob": sha1.hexdigest(),
            "sha256": sha256.hexdigest(),
            "mode": "100755" if before.st_mode & 0o111 else "100644"}


def read_json(root: Path, relative: str) -> dict | list:
    return json.loads(checked_path(root, relative).read_text(encoding="utf-8"))


def git_tree(rows: list[dict], path_key: str = "original_path",
             mode_key: str = "mode") -> str:
    """Reconstruct the exact Git tree identity without writing any Git object."""
    tree: dict = {}
    for row in rows:
        relative = row[path_key]
        parts = PurePosixPath(relative).parts
        require(parts and ".." not in parts and not relative.startswith("/"),
                f"Invalid tree member: {relative}")
        node = tree
        for part in parts[:-1]:
            child = node.setdefault(part, {})
            require(isinstance(child, dict), f"Tree/file name collision: {relative}")
            node = child
        require(parts[-1] not in node, f"Duplicate tree member: {relative}")
        mode, blob = row[mode_key], row["git_blob"]
        require(mode in {"100644", "100755", "120000"}
                and re.fullmatch(r"[0-9a-f]{40}", blob) is not None,
                f"Invalid Git entry: {relative}")
        node[parts[-1]] = (mode, blob)

    def digest(node: dict) -> str:
        entries = []
        for name, value in node.items():
            is_dir = isinstance(value, dict)
            mode, oid = ("40000", digest(value)) if is_dir else value
            raw_name = name.encode("utf-8")
            sort_key = raw_name + (b"/" if is_dir else b"")
            entries.append((sort_key, mode.encode() + b" " + raw_name
                            + b"\0" + bytes.fromhex(oid)))
        body = b"".join(data for _, data in sorted(entries))
        return hashlib.sha1(b"tree " + str(len(body)).encode() + b"\0" + body).hexdigest()

    return digest(tree)


def strip_comments(text: str) -> str:
    """Remove TeX comments, retaining an escaped percent and real newlines."""
    result = []
    for line in text.splitlines(keepends=True):
        cut = None
        for i, char in enumerate(line):
            if char != "%":
                continue
            slashes, k = 0, i - 1
            while k >= 0 and line[k] == "\\":
                slashes, k = slashes + 1, k - 1
            if slashes % 2 == 0:
                cut = i
                break
        result.append(line if cut is None else line[:cut] + "\n")
    return "".join(result)


def tex_closure(root: Path) -> dict:
    """Resolve this native paper's literal root-relative TeX input graph.

    This is deliberately not a TeX interpreter. Actual compiler/FLS closure
    is a separate build gate. Unsupported dynamic input names fail here.
    """
    root = Path(root).resolve()
    occurrences: list[str] = []
    texts: dict[str, str] = {}
    edges: list[dict] = []
    expanded: list[str] = []

    def visit(relative: str, stack: tuple[str, ...]) -> None:
        require(relative not in stack, "Cyclic TeX input: " + " -> ".join(stack + (relative,)))
        source = checked_path(root, relative)
        require(source.is_file(), f"Missing reachable TeX input: {relative}")
        text = texts.setdefault(relative, strip_comments(source.read_text(encoding="utf-8")))
        require(re.search(r"\\includeonly\b", text) is None,
                f"Unsupported selective include in {relative}")
        occurrences.append(relative)
        expanded.append(text)
        for match in INPUT_RE.finditer(text):
            name = (match.group(1) if match.group(1) is not None else match.group(2)).strip()
            require(name and not any(c in name for c in "\\#$"),
                    f"Dynamic or empty TeX input in {relative}: {name!r}")
            target = name if PurePosixPath(name).suffix else name + ".tex"
            checked_path(root, target)
            require(target.endswith(".tex"), f"Non-TeX native input: {target}")
            edges.append({"source": relative, "target": target})
            visit(target, stack + (relative,))

    visit("main.tex", ())
    counts = Counter(occurrences)
    duplicates = {path: n for path, n in counts.items() if n != 1}
    require(not duplicates, f"Multiply included active TeX files: {duplicates}")
    active_core = sorted(path for path in counts if CORE_RE.fullmatch(path))
    on_disk = sorted(path.relative_to(root).as_posix()
                     for path in (root / "core").glob("*.tex"))
    require(active_core == on_disk, "Active core closure differs from actual core/*.tex")
    ids = [int(CORE_RE.fullmatch(path).group(1)) for path in active_core]
    require(ids and min(ids) == 260 and max(ids) >= 318,
            "The active inherited native core must begin at 260 and retain 318")
    require(len(ids) == len(set(ids)), "More than one active file has the same core number")
    require(sorted(ids) == list(range(260, max(ids) + 1)),
            f"Missing native core number in 260..{max(ids)}")

    all_text = "\n".join(expanded)
    labels = Counter(label.strip() for label in LABEL_RE.findall(all_text))
    repeated_labels = sorted(label for label, count in labels.items() if count != 1)
    require(not repeated_labels, f"Duplicate active labels: {repeated_labels}")
    references = set()
    for names in REF_RE.findall(all_text):
        references.update(part.strip() for part in names.split(","))
    references.update(re.findall(r"\\hyperref\s*\[([^\]]+)\]", all_text))
    unresolved = sorted(references - labels.keys())
    require(not unresolved, f"Unresolved active native references: {unresolved}")
    citations = set()
    for names in re.findall(r"\\(?:cite|citep|citet|nocite)\*?"
                            r"(?:\s*\[[^\]]*\]){0,2}\s*\{([^{}]+)\}", all_text):
        citations.update(part.strip() for part in names.split(",") if part.strip() != "*")
    bibitems = set(re.findall(r"\\bibitem(?:\s*\[[^\]]*\])?\s*\{([^{}]+)\}", all_text))
    require(not citations - bibitems,
            f"Unresolved active bibliography keys: {sorted(citations - bibitems)}")
    structure = {
        "documentclass": len(re.findall(r"\\documentclass\b", all_text)),
        "begin_document": len(re.findall(r"\\begin\s*\{document\}", all_text)),
        "end_document": len(re.findall(r"\\end\s*\{document\}", all_text)),
    }
    require(all(n == 1 for n in structure.values()),
            f"Invalid full native document structure: {structure}")
    return {
        "status": "passed",
        "reachable_tex_files": sorted(counts),
        "active_core_files": active_core,
        "active_core_start": 260,
        "active_core_end": max(ids),
        "reachable_tex_count": len(counts),
        "active_core_count": len(active_core),
        "input_edges": edges,
        "active_label_count": len(labels),
        "active_reference_count": len(references),
        "active_bibliography_keys": sorted(bibitems),
        "duplicate_labels": [],
        "unresolved_references": [],
        "each_active_core_included_once": True,
        "document_structure": structure,
    }


def _check_identity(actual: dict, row: dict, relative: str,
                    check_mode: bool = True) -> None:
    keys = ("bytes", "git_blob", "sha256", "mode") if check_mode else ("bytes", "git_blob", "sha256")
    for key in keys:
        require(key in row and row[key] == actual[key],
                f"{key} mismatch in {relative}: {row.get(key)!r} != {actual[key]!r}")


def _check_census(root: Path, anchor: dict, archived: dict[str, dict]) -> dict:
    full = checked_path(root, CENSUS + "/ALL_REMOTE_HEADS_1296.tsv").read_text().splitlines()
    scoped = checked_path(root, CENSUS + "/A2_DYN_REMOTE_HEADS_432.tsv").read_text().splitlines()
    require(len(full) == 1296 and len(set(full)) == 1296, "Full frozen ref census is not 1,296 unique rows")
    require(len(scoped) == 432 and len(set(scoped)) == 432, "A2-DYN frozen ref census is not 432 unique rows")
    full_pairs = [line.split() for line in full]
    require(all(len(pair) == 2 and re.fullmatch(r"[0-9a-f]{40}", pair[0])
                and pair[1].startswith("refs/heads/") for pair in full_pairs),
            "Malformed frozen ref row")
    require(len({pair[1] for pair in full_pairs}) == 1296, "Duplicated frozen ref name")
    expected_scoped = {line for line in full if "a2-dyn" in line.split()[1].lower()}
    require(set(scoped) == expected_scoped, "Scoped refs do not equal the A2-DYN named frozen refs")
    compressed = read_json(root, CENSUS + "/COMPRESSED_AUDIT_MANIFEST.json")
    for row in compressed:
        data = checked_path(root, CENSUS + "/" + row["gzip_filename"]).read_bytes()
        require(len(data) == row["gzip_bytes"] and hashlib.sha256(data).hexdigest() == row["gzip_sha256"],
                "Compressed census identity mismatch: " + row["gzip_filename"])
        unpacked = gzip.decompress(data)
        require(len(unpacked) == row["original_bytes"]
                and hashlib.sha256(unpacked).hexdigest() == row["original_sha256"],
                "Compressed census roundtrip mismatch: " + row["gzip_filename"])
        json.loads(unpacked)
    source_blobs = read_json(root, CENSUS + "/source-blob-manifest.json")
    require(len(source_blobs) == 1595
            and len({row["git_blob"] for row in source_blobs}) == 1595,
            "Mathematical blob readback does not contain 1,595 unique objects")
    require(sum(row["bytes"] for row in source_blobs) == 18705400,
            "Mathematical blob readback byte count changed")
    census = read_json(root, CENSUS + "/review_branch_census.json")
    require(census["total_review_branches"] == 178 and len(census["branches"]) == 178,
            "Original review ref census count changed")
    require(len({row["branch"] for row in census["branches"]}) == 178, "Duplicated review ref")
    report_sources: dict[str, list] = defaultdict(list)
    for row in census["branches"]:
        report_sources[row["expected_report_blob"]].append(
            {key: row[key] for key in ("branch", "commit_sha", "repository_tree", "expected_report_path")}
        )
    require(len(report_sources) == census["unique_report_blobs"] == 91,
            "Original report-body census is not 91 distinct blobs")
    report_path = anchor["review_preservation_path"]
    require(identity(checked_path(root, report_path))["sha256"] == anchor["review_preservation_sha256"],
            "Fixed original report-preservation map changed")
    report_map = read_json(root, report_path)
    require(report_map["review_ref_count"] == 178 and report_map["distinct_report_count"] == 91,
            "Original report preservation count changed")
    require(len(report_map["reports"]) == 91
            and {row["git_blob"] for row in report_map["reports"]} == set(report_sources),
            "Original report preservation set differs from the exhausted ref census")
    for row in report_map["reports"]:
        path = row["archive_path"]
        require(path in archived, f"Original report is outside the fixed archive: {path}")
        _check_identity(archived[path], row, path, check_mode=False)
        for alternate in row["all_archive_paths"]:
            require(alternate in archived and archived[alternate]["git_blob"] == row["git_blob"],
                    f"Original report alternate preservation path changed: {alternate}")
        key = lambda item: (item["branch"], item["commit_sha"], item["expected_report_path"])
        require(sorted(row["original_sources"], key=key)
                == sorted(report_sources[row["git_blob"]], key=key),
                "Original review applicability map differs from census: " + row["git_blob"])
    control = identity(checked_path(root, CENSUS + "/REFEREE_REPORT_v115.md"))
    require(control["git_blob"] == "9c68b0e8b31cd196c732514a29ebd44d95964243"
            and control["sha256"] == "4d560d8ffde372f67629ea93919bb3e918367502a0fd04e222b1cae17f682b06",
            "Controlling report readback changed")
    return {"frozen_remote_refs": 1296, "a2_dyn_remote_refs": 432,
            "original_review_refs": 178, "original_report_bodies": 91,
            "mathematical_readback_blobs": 1595,
            "compressed_inventory_roundtrips": len(compressed)}


def _check_old_anchors(root: Path, anchor: dict, archived: dict[str, dict]) -> list[dict]:
    results = []
    for item in anchor["original_anchors"]:
        path = item["path"]
        require(path in archived and archived[path]["sha256"] == item["sha256"],
                "Inherited anchor identity changed: " + path)
        old = read_json(root, path)
        rows = old.get("files")
        if rows is None:
            rows = [row for group in old["groups"].values() for row in group["files"]]
        require(len(rows) == item["placements"], "Inherited anchor placement count changed: " + path)
        for row in rows:
            target = ARCHIVE + "/" + row["path"]
            require(target in archived, "Missing inherited anchor placement: " + target)
            _check_identity(archived[target], row, target, check_mode=False)
        result = {"path": path, "placements_verified": len(rows), "status": "passed"}
        if "files" in old and "source_article_tree" in old:
            actual_tree = git_tree(rows, mode_key="original_mode")
            require(actual_tree == old["source_article_tree"],
                    "Inherited complete original tree mismatch: " + path)
            result["original_article_tree_reconstructed"] = actual_tree
        results.append(result)
    return results


def _check_manifest(root: Path, closure: dict, required: bool) -> dict:
    target = root / "SOURCE_MANIFEST.json"
    if not target.is_file():
        require(not required, "SOURCE_MANIFEST.json is absent; final source verification requires a frozen manifest")
        return {"status": "not_yet_frozen", "required": False}
    manifest = read_json(root, "SOURCE_MANIFEST.json")
    require(isinstance(manifest, dict) and manifest.get("schema")
            and isinstance(manifest.get("files"), list), "Invalid current source manifest schema")
    rows = manifest["files"]
    names = [row.get("path") for row in rows]
    require(all(isinstance(name, str) for name in names)
            and len(names) == len(set(names)), "Missing or duplicate current manifest paths")
    require("SOURCE_MANIFEST.json" not in names, "Current source manifest must not hash itself")
    require(not any(name.startswith(("history/", "audit/", "evidence/")) for name in names),
            "Current mathematical manifest crosses into separately anchored history/audit/evidence")
    for row in rows:
        _check_identity(identity(checked_path(root, row["path"])), row, row["path"])
    canonical = {path.relative_to(root).as_posix()
                 for pattern in ("*.tex", "core/*.tex", "tools/*.py") for path in root.glob(pattern)}
    for name in ("requirements.txt", "build.sh"):
        require((root / name).is_file(), f"Missing mathematical build input: {name}")
        canonical.add(name)
    require(canonical.issubset(set(names)),
            "Unmanifested mathematical build sources: " + repr(sorted(canonical - set(names))))
    for key in ("active_core_files", "reachable_tex_files"):
        declared = manifest.get(key)
        require(isinstance(declared, list) and len(declared) == len(set(declared))
                and set(declared) == set(closure[key]),
                "Declared current source closure differs from actual closure: " + key)
        require(set(declared).issubset(set(names)), "Manifest omits declared active sources: " + key)
    return {"status": "passed", "declared_source_files": len(rows),
            "required_mathematical_build_files": len(canonical),
            "sha256": identity(target)["sha256"]}


def verify(root: Path, manifest_required: bool = True) -> dict:
    root = Path(root).resolve()
    anchor_identity = identity(checked_path(root, ANCHOR_PATH))
    require(anchor_identity["sha256"] == ANCHOR_SHA256, "The fixed complete predecessor anchor changed")
    anchor = read_json(root, ANCHOR_PATH)
    require(anchor["source_commit"] == BASE_COMMIT and anchor["source_root_tree"] == BASE_ROOT_TREE
            and anchor["source_article_tree"] == BASE_ARTICLE_TREE and anchor["archive_root"] == ARCHIVE,
            "Incorrect fixed source identity")
    rows = anchor["files"]
    require(len(rows) == anchor["file_count"] == 3864, "Incomplete original file map")
    require(git_tree(rows) == BASE_ARTICLE_TREE, "Original path/mode/blob map does not reconstruct the exact source tree")
    expected = {row["path"] for row in rows}
    require(len(expected) == len(rows), "Duplicated archive placement")
    actual_paths = {path.relative_to(root).as_posix()
                    for path in checked_path(root, ARCHIVE).rglob("*")
                    if path.is_file() or path.is_symlink()}
    require(actual_paths == expected,
            "Archive path set mismatch: missing=" + repr(sorted(expected - actual_paths))
            + "; extra=" + repr(sorted(actual_paths - expected)))
    archived = {}
    for row in rows:
        require(row["path"] == ARCHIVE + "/" + row["original_path"], "Original path was relocated within archive")
        actual = identity(checked_path(root, row["path"]))
        _check_identity(actual, row, row["path"])
        archived[row["path"]] = actual
    require(sum(row["bytes"] for row in rows) == anchor["bytes"],
            "Complete original byte count changed")
    expected_inherited = {row["original_path"] for row in rows
                          if row["original_path"] in {"model.tex", "inputs.tex"}
                          or CORE_RE.fullmatch(row["original_path"])}
    require(set(anchor["inherited_active_paths"]) == expected_inherited
            and len(expected_inherited) == 61, "Incomplete inherited active proof/model map")
    for path in sorted(expected_inherited):
        actual = identity(checked_path(root, path))
        _check_identity(actual, archived[ARCHIVE + "/" + path], path)
    old_anchors = _check_old_anchors(root, anchor, archived)
    census = _check_census(root, anchor, archived)
    closure = tex_closure(root)
    current_manifest = _check_manifest(root, closure, manifest_required)
    return {
        "status": "passed",
        "scope": "Exact source preservation and native input closure; not mathematical correctness or CI execution",
        "source_commit": BASE_COMMIT,
        "source_article_tree": BASE_ARTICLE_TREE,
        "reconstructed_original_tree": BASE_ARTICLE_TREE,
        "current_source_anchor_sha256": ANCHOR_SHA256,
        "original_files_preserved": len(rows),
        "original_bytes_preserved": anchor["bytes"],
        "immutable_active_proof_and_model_files": len(expected_inherited),
        "original_anchors": old_anchors,
        "census": census,
        "tex_closure": closure,
        "source_manifest": current_manifest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-unfrozen", action="store_true",
                        help="For preparation only; final verification requires SOURCE_MANIFEST.json")
    args = parser.parse_args()
    try:
        result = verify(args.root, manifest_required=not args.allow_unfrozen)
    except (VerificationError, OSError, KeyError, ValueError, TypeError) as exc:
        result = {"status": "failed", "error": str(exc),
                  "scope": "Source identity and native closure; no mathematical certification"}
    serialized = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(serialized, encoding="utf-8")
    sys.stdout.write(serialized)
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
