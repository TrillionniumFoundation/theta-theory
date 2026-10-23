#!/usr/bin/env python3
"""Seal the complete R78 source inventory; this is not a build or proof verdict.

Run only after the compiled THEOREM_INDEX.json has been copied into this
source directory. The manifest excludes itself and includes every other
regular source file, including the complete retained R58 companion.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MANIFEST = "SOURCE_MANIFEST.json"
MANIFEST_SCHEMA = "theta.r78.exact-source-manifest.v1"
BASE_COMMIT = '300807bad3eb00ad8e1975ae9ff1ea1971a333db'
BASE_SOURCE_COMMIT = '18b76a739898d2734c4f5bfcb609db0786cd4c11'
BASE_PATH = 'papers/General-Theta-Foundations-I-restart/r77-shared-preparation-and-memory'
BASE_TREE = 'c48519790add40e3c67aa245aa8e5ee1fcc47de6'
BASE_MANIFEST = "inputs/r77/SOURCE_MANIFEST.json"
BASE_MANIFEST_SHA256 = '044ccaff49d976ed1cfd8d6e37314684ccecd646ee88c98ce457ccb53b5df012'
COMPLETE_PRESERVATION = "provenance/R77_COMPLETE_PRESERVATION.json"
EXPECTED_PREDECESSOR_FILES = 622
COMPANION_PATH = "companion-r58"
COMPANION_TREE = "007a1d7d5f5b880c670fc6f47a812ebd476bfb00"
REVIEW_PATH = "provenance/R65_REFEREE_REPORT.md"
REVIEW_COMMIT = "358481b21ceeeedb1205ebd30f86982e32a2cb04"
REVIEW_BLOB = "d1ff9c5662390156ee212c82b173e86a21180e84"
REVIEW_SHA256 = "8c7d45d762736009fda667621fdf5019fa934f5f45f39364c747f837e6d7343c"
BODY_IDENTITIES = "provenance/R78_RETAINED_BODY_IDENTITIES.json"
SUFFIX_IDENTITY = "provenance/R78_SUPPLEMENT_SUFFIX_IDENTITY.json"
OLD_INDEX = "inputs/r77/THEOREM_INDEX.json"
INDEX = "THEOREM_INDEX.json"
EXPECTED_OLD_STATEMENTS = 235
# Fixed after direct parsing of the integrated active native sources:
# 235 inherited statement labels plus five R78 numbered additions.
EXPECTED_CURRENT_STATEMENTS = 240
IGNORED_DIRECTORIES = {".git", "__pycache__"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def git_object(kind: str, data: bytes) -> str:
    header = f"{kind} {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def file_mode(path: Path) -> str:
    mode = path.stat().st_mode
    require(stat.S_ISREG(mode), f"Not a regular source file: {path}")
    return "100755" if mode & 0o111 else "100644"


def regular_files(root: Path = ROOT) -> list[Path]:
    """Return the exact regular-file inventory without following symlinks."""
    result: list[Path] = []

    def visit(directory: Path) -> None:
        for item in sorted(directory.iterdir(), key=lambda p: p.name.encode("utf-8")):
            require(not item.is_symlink(), f"Source symlinks are not permitted: {item}")
            if item.is_dir():
                if item.name not in IGNORED_DIRECTORIES:
                    visit(item)
            elif item.is_file():
                result.append(item)
            else:
                raise RuntimeError(f"Nonregular source entry: {item}")

    visit(root)
    return sorted(result, key=lambda p: p.relative_to(root).as_posix().encode("utf-8"))


def git_tree(root: Path = ROOT) -> str:
    """Compute Git's tree identity, omitting empty directories as Git does."""
    def visit(directory: Path) -> tuple[str, bool]:
        entries: list[tuple[bytes, bytes]] = []
        for item in directory.iterdir():
            require(not item.is_symlink(), f"Source symlinks are not permitted: {item}")
            if item.is_dir():
                if item.name in IGNORED_DIRECTORIES:
                    continue
                identity, has_files = visit(item)
                if not has_files:
                    continue
                mode, sort_name = "40000", item.name + "/"
            elif item.is_file():
                identity = git_object("blob", item.read_bytes())
                mode, sort_name = file_mode(item), item.name
            else:
                raise RuntimeError(f"Nonregular source entry: {item}")
            payload = f"{mode} {item.name}".encode("utf-8") + b"\0" + bytes.fromhex(identity)
            entries.append((sort_name.encode("utf-8"), payload))
        body = b"".join(payload for _, payload in sorted(entries))
        return git_object("tree", body), bool(entries)

    return visit(root)[0]


def file_identity(path: Path, root: Path = ROOT) -> dict:
    require(not path.is_symlink(), f"Source symlinks are not permitted: {path}")
    raw = path.read_bytes()
    return {"path": path.relative_to(root).as_posix(), "mode": file_mode(path),
            "bytes": len(raw), "git_blob": git_object("blob", raw), "sha256": sha256(raw)}


def contained_path(relative: str, root: Path = ROOT) -> Path:
    candidate = Path(relative)
    require(not candidate.is_absolute() and ".." not in candidate.parts,
            f"Invalid source-relative path: {relative}")
    result = root / candidate
    require(root.resolve() in result.resolve().parents, f"Path escaped source root: {relative}")
    require(not result.is_symlink(), f"Source symlink: {relative}")
    return result


def read_json(relative: str) -> dict | list:
    return json.loads(contained_path(relative).read_text(encoding="utf-8"))


def complete_predecessor_checks() -> dict:
    """Authenticate every preserved R77 file, including replaced wrappers.

    The fixed old-manifest hash prevents a shortened preservation list from
    silently declaring omitted files irrelevant. Strict verification also
    compares this exact inventory with the actual predecessor Git tree.
    """
    old_manifest_raw = contained_path(BASE_MANIFEST).read_bytes()
    require(sha256(old_manifest_raw) == BASE_MANIFEST_SHA256,
            "The archived complete R77 source manifest differs")
    old_manifest = json.loads(old_manifest_raw)
    require(old_manifest.get("schema") == "theta.r77.exact-source-manifest.v1",
            "Unexpected predecessor source manifest schema")
    expected = {row["path"]: row for row in old_manifest["files"]}
    require(len(expected) == len(old_manifest["files"])
            and MANIFEST not in expected, "Invalid predecessor manifest inventory")
    expected[MANIFEST] = {"path": MANIFEST, "mode": "100644",
                          "bytes": len(old_manifest_raw),
                          "git_blob": git_object("blob", old_manifest_raw),
                          "sha256": sha256(old_manifest_raw)}
    preservation = read_json(COMPLETE_PRESERVATION)
    require(preservation.get("predecessor_commit") == BASE_COMMIT
            and preservation.get("source_commit") == BASE_SOURCE_COMMIT
            and preservation.get("predecessor_path") == BASE_PATH
            and preservation.get("predecessor_tree") == BASE_TREE,
            "Wrong controlling R77 identity in complete preservation map")
    rows = preservation["files"]
    old_paths = [row["predecessor_path"] for row in rows]
    new_paths = [row["current_preserved_path"] for row in rows]
    require(preservation.get("file_count") == EXPECTED_PREDECESSOR_FILES
            and len(rows) == EXPECTED_PREDECESSOR_FILES
            and len(old_paths) == len(set(old_paths))
            and len(new_paths) == len(set(new_paths))
            and set(old_paths) == set(expected),
            "The complete preservation map must contain all 622 distinct R77 files")
    for row in rows:
        fixed = expected[row["predecessor_path"]]
        require(all(row[key] == fixed[key] for key in ("bytes", "git_blob", "sha256")),
                "Preservation pointer differs from fixed R77 manifest: "
                + row["predecessor_path"])
        identity = file_identity(contained_path(row["current_preserved_path"]))
        require(all(identity[key] == fixed[key]
                    for key in ("mode", "bytes", "git_blob", "sha256")),
                "Preserved R77 file or mode differs: " + row["current_preserved_path"])
    return {"predecessor_file_count": len(rows),
            "predecessor_source_manifest_sha256": BASE_MANIFEST_SHA256,
            "complete_preservation_map_sha256": sha256(contained_path(COMPLETE_PRESERVATION).read_bytes()),
            "preserved_same_path": sum(row["predecessor_path"] == row["current_preserved_path"]
                                        for row in rows),
            "preserved_archival_path": sum(row["predecessor_path"] != row["current_preserved_path"]
                                            for row in rows)}


def pinned_body_checks() -> dict:
    complete = complete_predecessor_checks()
    bodies = read_json(BODY_IDENTITIES)
    require(isinstance(bodies, list) and bool(bodies), "Invalid retained-body identity list")
    paths = [row["path"] for row in bodies]
    require(len(paths) == len(set(paths)), "Duplicate retained-body identities")
    for row in bodies:
        require(row["inherited_from_commit"] == BASE_COMMIT,
                "Wrong predecessor in retained-body identity: " + row["path"])
        raw = contained_path(row["path"]).read_bytes()
        require(len(raw) == row["bytes"] and sha256(raw) == row["sha256"]
                and git_object("blob", raw) == row["git_blob"],
                "Inherited current theorem body differs: " + row["path"])

    suffix = read_json(SUFFIX_IDENTITY)
    require(suffix["predecessor_commit"] == BASE_COMMIT
            and suffix["predecessor_path"] == BASE_PATH + "/supplement.tex",
            "Wrong predecessor for retained supplement suffix")
    raw = contained_path(suffix["new_path"]).read_bytes()
    marker = suffix["retained_start_marker"].encode("utf-8")
    require(raw.count(marker) == 1, "Retained supplement marker is missing or ambiguous")
    retained = raw[raw.index(marker):]
    require(len(retained) == suffix["suffix_bytes"]
            and sha256(retained) == suffix["suffix_sha256"],
            "Inherited supplement suffix differs")

    report = contained_path(REVIEW_PATH).read_bytes()
    require(git_object("blob", report) == REVIEW_BLOB and sha256(report) == REVIEW_SHA256,
            "Controlling R65 report body differs")
    companion = ROOT / COMPANION_PATH
    require(companion.is_dir() and git_tree(companion) == COMPANION_TREE,
            "Complete R58 companion tree differs")

    old = read_json(OLD_INDEX)
    labels = [row["label"] for row in old["statements"]]
    require(len(labels) == EXPECTED_OLD_STATEMENTS and len(set(labels)) == len(labels),
            "The inherited index must contain 235 distinct statement labels")
    return {**complete, "inherited_current_bodies": len(bodies),
            "inherited_supplement_suffix_bytes": len(retained),
            "inherited_supplement_suffix_sha256": sha256(retained),
            "r58_companion_git_tree": COMPANION_TREE,
            "r58_companion_file_count": len(regular_files(companion)),
            "r65_report_git_blob": REVIEW_BLOB, "r65_report_sha256": REVIEW_SHA256,
            "inherited_statement_labels": len(labels)}


def verify_index_structure() -> dict:
    index = read_json(INDEX)
    require(type(EXPECTED_CURRENT_STATEMENTS) is int
            and EXPECTED_CURRENT_STATEMENTS > EXPECTED_OLD_STATEMENTS,
            "The explicit R78 statement count has not been finalized")
    require(index.get("schema") == "theta.r78.compiled-theorem-index.v1",
            "The current theorem index has not been generated by verify.py")
    rows = index["statements"]
    labels = [row["label"] for row in rows]
    require(len(labels) == EXPECTED_CURRENT_STATEMENTS and len(set(labels)) == len(labels),
            f"The current compiled index must contain {EXPECTED_CURRENT_STATEMENTS} distinct statement labels")
    old_labels = {row["label"] for row in read_json(OLD_INDEX)["statements"]}
    require(old_labels <= set(labels), "An inherited statement is absent from the current index")
    for row in rows:
        require(row["document"] in {"main", "supplement"}
                and isinstance(row["page"], int) and row["page"] > 0
                and isinstance(row["number"], str) and bool(row["number"]),
                "Malformed compiled theorem entry: " + row["label"])
        text = contained_path(row["source"]).read_text(encoding="utf-8")
        require(re.search(r"\\label\{" + re.escape(row["label"]) + r"\}", text) is not None,
                "Theorem label absent from its indexed source: " + row["label"])
    return index


def make_manifest() -> dict:
    retained = pinned_body_checks()
    verify_index_structure()
    files = [file_identity(path) for path in regular_files()
             if path.relative_to(ROOT).as_posix() != MANIFEST]
    return {"schema": MANIFEST_SCHEMA,
            "meaning": "Complete source inventory and inherited-byte identities; not a verification verdict.",
            "predecessor": {"commit": BASE_COMMIT, "source_commit": BASE_SOURCE_COMMIT,
                            "path": BASE_PATH, "git_tree": BASE_TREE,
                            "source_manifest_sha256": BASE_MANIFEST_SHA256},
            "controlling_report": {"commit": REVIEW_COMMIT, "path": REVIEW_PATH,
                                   "git_blob": REVIEW_BLOB, "sha256": REVIEW_SHA256},
            "retained_r58": {"path": COMPANION_PATH, "git_tree": COMPANION_TREE,
                             "file_count": retained["r58_companion_file_count"]},
            "retained_body_identity_file": BODY_IDENTITIES,
            "retained_suffix_identity_file": SUFFIX_IDENTITY,
            "complete_predecessor_preservation_file": COMPLETE_PRESERVATION,
            "complete_predecessor_file_count": retained["predecessor_file_count"],
            "inherited_theorem_index": OLD_INDEX,
            "current_theorem_index": INDEX,
            "inherited_statement_count": EXPECTED_OLD_STATEMENTS,
            "current_indexed_statement_count": EXPECTED_CURRENT_STATEMENTS,
            "files": files,
            "excluded": ["The root SOURCE_MANIFEST.json itself", ".git directories", "__pycache__ directories"],
            "empty_directories": "Omitted from Git tree identities, as in Git."}


def verify_manifest() -> tuple[dict, dict]:
    recorded = read_json(MANIFEST)
    require(recorded.get("schema") == MANIFEST_SCHEMA, "Unexpected source manifest schema")
    actual = make_manifest()
    if recorded != actual:
        before = {row["path"]: row for row in recorded.get("files", [])}
        after = {row["path"]: row for row in actual["files"]}
        changed = sorted(p for p in set(before) | set(after) if before.get(p) != after.get(p))
        raise RuntimeError("Source manifest mismatch; changed, missing, or unlisted files: "
                           + ", ".join(changed[:30])
                           + ("; metadata differs" if not changed else ""))
    return recorded, pinned_body_checks()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check an existing seal without writing")
    args = parser.parse_args()
    if args.check:
        manifest, retained = verify_manifest()
        action = "SOURCE_SEAL_CHECKED"
    else:
        manifest = make_manifest()
        (ROOT / MANIFEST).write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        retained = pinned_body_checks()
        action = "SOURCE_SEALED_NOT_YET_BUILT"
    print(json.dumps({"status": action, "source_files": len(manifest["files"]) + 1,
                      "source_git_tree": git_tree(),
                      "source_manifest_sha256": sha256((ROOT / MANIFEST).read_bytes()),
                      "retention": retained,
                      "limitation": "Sealing source hashes is not compilation, mathematical proof, remote publication, or CI."},
                     indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
