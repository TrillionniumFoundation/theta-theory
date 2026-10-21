#!/usr/bin/env python3
"""Verify the complete pinned predecessor and the current native input closure.

The predecessor's own verifier is executed on its unchanged archive. Its
standard-library identity/TeX parser is reused; none of its mathematical
claims is inferred from this source-identity check. Every gate survives -O.
"""
from __future__ import annotations
import argparse
import importlib.util
import json
from pathlib import Path
import sys

sys.dont_write_bytecode = True
ROOT = Path(__file__).resolve().parents[1]
BASE_COMMIT = "4d83de89d16bae7f9e9439dcc80e099b8f8f5c4e"
BASE_ROOT_TREE = "a1a8677340dfe0bcc3c1be806d6df2c2a200769e"
BASE_ARTICLE_TREE = "7bcaba2bc1ef7ab393c81a7df84f3e45983c4dfa"
ANCHOR_SHA256 = "1f7eff3e4300875a81a01482e3299a99c4893239ec844c0b883a1516e2d50474"
ARCHIVE = "history/predecessor"
spec = importlib.util.spec_from_file_location(
    "preserved_critical_source_verifier",
    ROOT / ARCHIVE / "tools/check_source_preservation.py")
legacy = importlib.util.module_from_spec(spec)
spec.loader.exec_module(legacy)
VerificationError = legacy.VerificationError
require = legacy.require
identity = legacy.identity
checked_path = legacy.checked_path
git_tree = legacy.git_tree
tex_closure = legacy.tex_closure
strip_comments = legacy.strip_comments


def verify(root: Path, manifest_required: bool = True) -> dict:
    root = Path(root).resolve()
    anchor_path = checked_path(root, "CURRENT_SOURCE_ANCHOR.json")
    require(identity(anchor_path)["sha256"] == ANCHOR_SHA256,
            "The complete 4d83 predecessor anchor changed")
    anchor = json.loads(anchor_path.read_text())
    require(anchor["source_commit"] == BASE_COMMIT
            and anchor["source_root_tree"] == BASE_ROOT_TREE
            and anchor["source_article_tree"] == BASE_ARTICLE_TREE
            and anchor["archive_root"] == ARCHIVE,
            "Wrong complete author parent")
    rows = anchor["files"]
    require(len(rows) == anchor["file_count"] == 4393,
            "Incomplete 4d83 predecessor file map")
    require(git_tree(rows) == BASE_ARTICLE_TREE,
            "Pinned path/mode/blob map does not reconstruct the article tree")
    expected = {row["path"] for row in rows}
    require(len(expected) == len(rows), "Duplicate archive placement")
    actual_paths = {p.relative_to(root).as_posix()
                    for p in (root / ARCHIVE).rglob("*")
                    if p.is_file() or p.is_symlink()}
    require(actual_paths == expected, "Archive path set changed")
    for row in rows:
        require(row["path"] == ARCHIVE + "/" + row["original_path"],
                "Relocated predecessor file")
        legacy._check_identity(identity(checked_path(root, row["path"])),
                               row, row["path"])
    require(sum(row["bytes"] for row in rows) == anchor["bytes"] == 544226975,
            "Predecessor byte count changed")
    inherited = {row["original_path"] for row in rows
                 if row["original_path"] in {"model.tex", "inputs.tex"}
                 or legacy.CORE_RE.fullmatch(row["original_path"])}
    require(inherited == set(anchor["inherited_active_paths"])
            and len(inherited) == 65,
            "The complete 260--322 proof/model inheritance map changed")
    archive_map = {row["original_path"]: row for row in rows}
    for name in sorted(inherited):
        legacy._check_identity(identity(checked_path(root, name)),
                               archive_map[name], name)
    predecessor_verification = legacy.verify(root / ARCHIVE, True)
    fresh = json.loads((root / "audit/fresh-provenance/FRESH_PROVENANCE_SUMMARY.json").read_text())
    require(fresh["baseline"]["commit"] == BASE_COMMIT
            and fresh["baseline"]["article_tree"] == BASE_ARTICLE_TREE
            and fresh["remote_snapshot"]["remote_heads"] == 1298
            and fresh["prior_heads_unchanged"] == 1296
            and not fresh["changed_old_heads"]
            and not fresh["removed_old_heads"],
            "Fresh full-ref applicability audit changed")
    require(fresh["controlling_report"]["blob"]
            == "9c68b0e8b31cd196c732514a29ebd44d95964243"
            and fresh["controlling_report"]["direct_native_scope"] == [260, 276]
            and fresh["controlling_report"]["later_native_modules_reviewed"] is False,
            "Controlling report identity or applicability changed")
    closure = tex_closure(root)
    manifest = legacy._check_manifest(root, closure, manifest_required)
    return {
        "status": "passed",
        "scope": "Immutable source/history identities and native closure; not a proof or independent expert certification",
        "source_commit": BASE_COMMIT, "source_root_tree": BASE_ROOT_TREE,
        "source_article_tree": BASE_ARTICLE_TREE,
        "reconstructed_original_tree": BASE_ARTICLE_TREE,
        "current_source_anchor_sha256": ANCHOR_SHA256,
        "original_files_preserved": len(rows),
        "original_bytes_preserved": anchor["bytes"],
        "immutable_active_proof_and_model_files": len(inherited),
        "predecessor_verification": predecessor_verification,
        "fresh_remote_heads": 1298, "fresh_a2_dyn_heads": 433,
        "original_review_heads": 178, "original_report_blobs": 91,
        "tex_closure": closure, "source_manifest": manifest,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--allow-unfrozen", action="store_true")
    args = parser.parse_args()
    try:
        result = verify(args.root, not args.allow_unfrozen)
    except (VerificationError, OSError, KeyError, ValueError, TypeError) as exc:
        result = {"status": "failed", "error": str(exc),
                  "scope": "Source identity and native closure only"}
    data = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data)
    sys.stdout.write(data)
    return 0 if result["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
