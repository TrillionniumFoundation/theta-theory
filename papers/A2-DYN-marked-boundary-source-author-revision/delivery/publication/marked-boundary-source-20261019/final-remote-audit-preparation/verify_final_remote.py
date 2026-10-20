#!/usr/bin/env python3
"""Verify saved actual final publication GETs; never fetch, mutate, or infer CI.

This program requires the final identities and exact staged inventory. Preparing
it is not an actual remote audit. Its case directory must be new and contain
the listed immutable inputs and exact raw API readbacks before it is executed.
"""
from __future__ import annotations

import argparse
import collections
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path, PurePosixPath
import re

API = "https://api.github.com/repos/TrillionniumFoundation/theta-theory"
PARENT_COMMIT = "efde9fa6c45e7835989b653622a9870e59027530"
PARENT_ROOT = "b5d618b8a4b356f8ca07f1c9f1238e35d879ede8"
PARENT_ARTICLE = "b4add0580cc8211223dfa57e6e618e2bf9546d09"
ARTICLE_NAME = "A2-DYN-marked-boundary-source-author-revision"
WORKFLOW_NAME = "a2-dyn-marked-boundary-source-20261019.yml"
WORKFLOW_BLOB = "56e44c7a4e978494c5dba8df023bef5fc8b7cfa4"
FROZEN_MANIFEST_BLOB = "4cf536e1f6912ede215b6a3ef305956ae07db983"
MATHEMATICAL_SHA256 = "ee0bd027bf5b4263ea5c6eebfb8ffe2d24c8fa0b21d1187f0967bfcaf0a221a5"
MODIFIED = {"PUBLICATION_RECEIPT.json", "PUBLICATION_STATUS.json", "REMOTE_TRANSPORT_STATUS.md"}
NEW_REFS = {prefix + "/a2-dyn-marked-boundary-source-2026-10-19"
            for prefix in ("revision", "referee-copy", "referee-response")}
REF_FILES = {"author_ref": "revision", "copy_ref": "referee-copy", "response_ref": "referee-response"}


def now():
    return datetime.now(timezone.utc).isoformat()


def load(path):
    return json.loads(path.read_bytes())


def digest(data):
    return hashlib.sha256(data).hexdigest()


def identity(path):
    data = path.read_bytes()
    return {"path": str(path.resolve()), "bytes": len(data), "sha256": digest(data)}


def triple(entry):
    return {k: entry[k] for k in ("mode", "type", "sha")}


def tree_hash(entries):
    raw = b"".join(
        e["mode"].lstrip("0").encode() + b" " + e["path"].encode()
        + b"\0" + bytes.fromhex(e["sha"])
        for e in sorted(entries, key=lambda x:
                        (x["path"] + ("/" if x["type"] == "tree" else "")).encode()))
    return hashlib.sha1(b"tree " + str(len(raw)).encode() + b"\0" + raw).hexdigest()


def mathematical_path(path):
    p = PurePosixPath(path)
    return ((len(p.parts) == 1 and p.suffix == ".tex") or
            (len(p.parts) == 2 and p.parts[0] == "core" and p.suffix == ".tex") or
            (len(p.parts) == 2 and p.parts[0] == "tools" and p.suffix == ".py"))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", type=Path, required=True)
    parser.add_argument("--config", type=Path, required=True)
    args = parser.parse_args()
    started = now()
    case = args.case.resolve()
    raw, inputs = case / "readbacks", case / "inputs"
    output = case / "INDEPENDENT_FINAL_PUBLICATION_AUDIT.json"
    if output.exists():
        raise RuntimeError("Existing audit output must remain intact; use a fresh case directory")
    config = load(args.config)
    for key in ("commit", "root_tree", "article_tree"):
        if not isinstance(config.get(key), str) or not re.fullmatch(r"[0-9a-f]{40}", config[key]):
            raise RuntimeError("Final published identity is required, not a placeholder: " + key)
    if not re.fullmatch(r"[0-9a-f]{64}", config.get("expected_inventory_sha256", "")):
        raise RuntimeError("Exact staged inventory SHA-256 is required")
    current, root_sha, article_sha = (config[k] for k in ("commit", "root_tree", "article_tree"))
    failures = []

    def require(condition, description):
        if not condition:
            failures.append(description)

    expected_path = inputs / "EXPECTED_FILE_IDENTITIES.json"
    expected = load(expected_path)
    require(digest(expected_path.read_bytes()) == config["expected_inventory_sha256"],
            "Exact expected inventory hash")
    require(expected["root_tree_sha"] == root_sha and expected["article_tree_sha"] == article_sha
            and expected["article_path"] == "papers/" + ARTICLE_NAME, "Expected staged identities and article scope")
    commit = load(raw / "final_commit.json")
    require(commit["sha"] == current and commit["tree"]["sha"] == root_sha,
            "Actual final commit and root identity")
    require([p["sha"] for p in commit["parents"]] == [PARENT_COMMIT], "Final commit is a direct C2 successor")
    article = load(raw / "article_recursive.json")
    old_article = load(inputs / "immutable-c2-readbacks/article_recursive.json")
    require(article["sha"] == article_sha and article.get("truncated") is False,
            "Actual final recursive article identity and complete response")
    require(old_article["sha"] == PARENT_ARTICLE and old_article.get("truncated") is False,
            "Actual immutable C2 article reused with its original identity")
    require(len(article["tree"]) == len({e["path"] for e in article["tree"]}), "Unique final article paths")
    require(all(e["type"] in {"blob", "tree"} for e in article["tree"]), "Only expected Git object types")
    files = {e["path"]: e for e in article["tree"] if e["type"] == "blob"}
    old_files = {e["path"]: e for e in old_article["tree"] if e["type"] == "blob"}
    wanted = {e["path"]: e for e in expected["files"]}
    require(len(wanted) == len(expected["files"]) and set(files) == set(wanted), "Complete unique file path set")
    file_mismatches = [{"path": p, "expected": e, "actual": files.get(p)}
                       for p, e in wanted.items() if p not in files or triple(files[p]) != triple(e)
                       or files[p]["size"] != e["bytes"]]
    require(not file_mismatches, "Every final file mode, type, blob and byte size matches the staged inventory")
    trees = {"": article["sha"], **{e["path"]: e["sha"] for e in article["tree"] if e["type"] == "tree"}}
    require(set(trees) == set(expected["subtree_hashes"]), "Complete final directory path set")
    children = collections.defaultdict(list)
    for e in article["tree"]:
        parent, _, name = e["path"].rpartition("/")
        children[parent].append({**e, "path": name})
    tree_checks = [{"path": p, "entries": len(children[p]), "expected_sha": h,
                    "remote_sha": trees.get(p), "recomputed_sha": tree_hash(children[p]),
                    "matches": h == trees.get(p) == tree_hash(children[p])}
                   for p, h in expected["subtree_hashes"].items()]
    require(all(x["matches"] for x in tree_checks), "Every final directory Git SHA reconstructed from actual entries")
    changes = []
    for p in sorted(set(old_files) | set(files)):
        old, new = old_files.get(p), files.get(p)
        if old is None:
            changes.append({"path": p, "status": "added", "new": triple(new)})
        elif new is None:
            changes.append({"path": p, "status": "deleted", "old": triple(old)})
        elif triple(old) != triple(new) or old["size"] != new["size"]:
            changes.append({"path": p, "status": "modified", "old": triple(old), "new": triple(new)})
    require({x["path"] for x in changes if x["status"] == "modified"} == MODIFIED,
            "Only exactly three root publication metadata files are modified")
    additions = [x for x in changes if x["status"] == "added"]
    require(additions and all(x["path"].startswith("delivery/publication/") for x in additions),
            "All additions are new publication evidence")
    require(not any(x["status"] == "deleted" for x in changes), "No C2 file is deleted")
    old_archives = {p for p in old_files if p.startswith("delivery/publication/")}
    require(all(p in files and triple(files[p]) == triple(old_files[p]) for p in old_archives),
            "Every existing publication archive is unchanged")

    old_math = {p for p in old_files if mathematical_path(p)}
    new_math = {p for p in files if mathematical_path(p)}
    require(old_math == new_math and len(new_math) == 107, "Exactly the same 107 mathematical source files")
    math_checks = [{"path": p, "C2_blob": old_files[p]["sha"], "final_blob": files[p]["sha"],
                    "matches": triple(old_files[p]) == triple(files[p])} for p in sorted(old_math & new_math)]
    require(all(x["matches"] for x in math_checks), "Every mathematical source byte/mode identity is unchanged")
    math_rows = [{"path": p, "sha256": wanted[p]["sha256"]} for p in sorted(new_math)]
    math_fingerprint = digest(json.dumps(math_rows, sort_keys=True).encode())
    require(math_fingerprint == MATHEMATICAL_SHA256, "Expected complete mathematical fingerprint is unchanged")
    manifest_path = inputs / "FROZEN_SOURCE_MANIFEST.json"
    manifest_bytes = manifest_path.read_bytes()
    manifest_blob = hashlib.sha1(b"blob " + str(len(manifest_bytes)).encode() + b"\0" + manifest_bytes).hexdigest()
    manifest = json.loads(manifest_bytes)
    require(manifest_blob == FROZEN_MANIFEST_BLOB == old_files["SOURCE_MANIFEST.json"]["sha"]
            == files["SOURCE_MANIFEST.json"]["sha"], "Exact immutable schema-5 source manifest")
    require(manifest["schema"] == 5 and len(manifest["files"]) == manifest["source_count"] == 1837
            and len({r["path"] for r in manifest["files"]}) == 1837
            and sum(r["bytes"] for r in manifest["files"]) == manifest["source_bytes"] == 139367900,
            "Complete unique frozen source count and byte total")
    frozen_checks = []
    for row in manifest["files"]:
        p = row["path"]
        old, new = old_files.get(p), files.get(p)
        matched = (old is not None and new is not None and row["git_blob"] == old["sha"] == new["sha"]
                   and row["bytes"] == old["size"] == new["size"] and triple(old) == triple(new))
        frozen_checks.append({"path": p, "frozen_blob": row["git_blob"],
                              "C2_blob": old["sha"] if old else None,
                              "final_blob": new["sha"] if new else None, "matches": matched})
    require(all(x["matches"] for x in frozen_checks), "All 1837 frozen source files are unchanged")

    isolation, immediate = {}, {}
    for level, allowed in (("root", {"papers"}), ("papers", {ARTICLE_NAME})):
        old = load(inputs / ("immutable-c2-readbacks/c2_" + level + ".json"))
        new = load(raw / ("final_" + level + ".json"))
        immediate[level] = old, new
        old_entries, new_entries = ({e["path"]: triple(e) for e in t["tree"]} for t in (old, new))
        changed = {p: {"C2": old_entries[p], "final": new_entries[p]}
                   for p in old_entries.keys() & new_entries.keys() if old_entries[p] != new_entries[p]}
        require(set(old_entries) == set(new_entries) and set(changed) == allowed,
                "Every unrelated immediate entry is unchanged: " + level)
        require(old.get("truncated") is False and new.get("truncated") is False
                and tree_hash(old["tree"]) == old["sha"] and tree_hash(new["tree"]) == new["sha"],
                "Both complete immediate trees independently reconstructed: " + level)
        isolation[level] = {"C2_tree": old["sha"], "final_tree": new["sha"],
                            "C2_entries": len(old_entries), "final_entries": len(new_entries),
                            "unchanged_entries": sum(old_entries[p] == new_entries[p]
                                                      for p in old_entries.keys() & new_entries.keys()),
                            "changed": changed}
    old_root, new_root = immediate["root"]
    old_papers, new_papers = immediate["papers"]
    require(old_root["sha"] == PARENT_ROOT and new_root["sha"] == root_sha, "Both actual root identities")
    for r, p, a in ((old_root, old_papers, PARENT_ARTICLE), (new_root, new_papers, article_sha)):
        require(next(e["sha"] for e in r["tree"] if e["path"] == "papers") == p["sha"]
                and next(e["sha"] for e in p["tree"] if e["path"] == ARTICLE_NAME) == a,
                "Actual root to papers to article linkage")
    github_unchanged = triple(next(e for e in old_root["tree"] if e["path"] == ".github")) == triple(
        next(e for e in new_root["tree"] if e["path"] == ".github"))
    require(github_unchanged, "Entire .github/workflows subtree is unchanged from C2")
    old_github = load(inputs / "immutable-c1-readbacks/c1_github.json")
    old_workflows = load(inputs / "immutable-c1-readbacks/c1_workflows.json")
    require(tree_hash(old_github["tree"]) == old_github["sha"]
            == next(e["sha"] for e in new_root["tree"] if e["path"] == ".github")
            and next(e["sha"] for e in old_github["tree"] if e["path"] == "workflows") == old_workflows["sha"],
            "Actual final root links the immutable .github and workflows objects")
    workflow = next(e for e in old_workflows["tree"] if e["path"] == WORKFLOW_NAME)
    require(workflow["sha"] == WORKFLOW_BLOB and tree_hash(old_workflows["tree"]) == old_workflows["sha"],
            "Exact unchanged dedicated workflow identity, inherited from sealed C1/C2")

    original_isolation = {}
    for level, new in (("root", new_root), ("papers", new_papers),
                       ("github", old_github), ("workflows", old_workflows)):
        old = load(inputs / ("immutable-original-readbacks/parent_" + level + ".json"))
        a, b = ({e["path"]: triple(e) for e in t["tree"]} for t in (old, new))
        added = {p: b[p] for p in sorted(b.keys() - a.keys())}
        removed = {p: a[p] for p in sorted(a.keys() - b.keys())}
        changed = {p: {"original": a[p], "final": b[p]}
                   for p in sorted(a.keys() & b.keys()) if a[p] != b[p]}
        require(not removed and tree_hash(old["tree"]) == old["sha"]
                and old.get("truncated") is False and new.get("truncated") is False,
                "Original complete tree reconstructed without a removed entry: " + level)
        expected_added = {ARTICLE_NAME} if level == "papers" else ({WORKFLOW_NAME} if level == "workflows" else set())
        expected_changed = {"papers", ".github"} if level == "root" else ({"workflows"} if level == "github" else set())
        require(set(added) == expected_added and set(changed) == expected_changed,
                "Original baseline to final isolation at " + level)
        original_isolation[level] = {"original_tree": old["sha"], "final_tree": new["sha"],
                                     "original_entries": len(a), "final_entries": len(b),
                                     "unchanged_entries": sum(a[p] == b[p] for p in a.keys() & b.keys()),
                                     "added": added, "changed": changed, "removed": removed}
    require(original_isolation["root"]["original_tree"] == "dba7d9a6e14d2509291f03cbf269b4ceb78b9549",
            "Original complete B root is the fixed 0933e9b baseline")

    baseline = load(inputs / "BASELINE_ALL_BRANCHES_READBACK.json")
    old_heads = {b["name"]: b["commit"]["sha"] for b in baseline["branches"]}
    require(len(old_heads) == len(baseline["branches"]) == 1293, "Exact original 1293-head baseline")
    page_numbers = sorted(int(m.group(1)) for p in raw.glob("branches_*.json")
                          if (m := re.fullmatch(r"branches_(\d+)\.json", p.name)))
    require(page_numbers == list(range(1, 15)), "Fresh complete branch pagination with terminal empty page")
    pages = [load(raw / ("branches_" + str(p) + ".json")) for p in page_numbers]
    require(all(isinstance(p, list) for p in pages), "Actual branch list response types")
    page_counts = [len(p) for p in pages]
    branch_rows = [row for page in pages for row in page]
    heads = {b["name"]: b["commit"]["sha"] for b in branch_rows}
    require(page_counts == [100] * 12 + [96, 0] and len(heads) == len(branch_rows) == 1296,
            "Exactly 1296 unique current branches, fully paginated")
    missing_heads = sorted(old_heads.keys() - heads.keys())
    changed_heads = {p: {"baseline": old_heads[p], "observed": heads[p]}
                     for p in old_heads.keys() & heads.keys() if old_heads[p] != heads[p]}
    added_heads = {p: heads[p] for p in sorted(heads.keys() - old_heads.keys())}
    require(not missing_heads and not changed_heads, "Every original branch remains at its exact SHA")
    require(set(added_heads) == NEW_REFS and set(added_heads.values()) == {current}, "Only three added heads, all at final commit")
    refs = {}
    for name in REF_FILES:
        response = load(raw / (name + ".json"))
        require(response["object"]["type"] == "commit", "Actual direct commit ref: " + name)
        refs[response["ref"]] = response["object"]["sha"]
    require(set(refs) == {"refs/heads/" + r for r in NEW_REFS} and set(refs.values()) == {current},
            "All three individual actual ref readbacks agree with final commit")

    expected_urls = {
        "final_commit": API + "/git/commits/" + current,
        "final_root": API + "/git/trees/" + root_sha,
        "final_papers": API + "/git/trees/" + new_papers["sha"],
        "article_recursive": API + "/git/trees/" + article_sha + "?recursive=1",
        **{name: API + "/git/ref/heads/" + prefix + "/a2-dyn-marked-boundary-source-2026-10-19"
           for name, prefix in REF_FILES.items()},
        **{"branches_" + str(p): API + "/branches?per_page=100&page=" + str(p) for p in page_numbers},
    }
    raw_records = []
    for name, url in expected_urls.items():
        metadata_path = raw / (name + ".request.json")
        metadata = load(metadata_path)
        require(metadata["request_url"] == url and metadata["body_file"] == name + ".json"
                and metadata["tool_isError"] is False, "Actual GET provenance and endpoint: " + name)
        requested, observed = metadata.get("requested_utc"), metadata.get("observed_utc")
        require(isinstance(requested, str) and isinstance(observed, str)
                and datetime.fromisoformat(requested.replace("Z", "+00:00"))
                <= datetime.fromisoformat(observed.replace("Z", "+00:00")), "Real ordered GET timestamps: " + name)
        raw_records.append({"name": name, "request_url": url, "requested_utc": requested,
                            "observed_utc": observed, "request_identity": identity(metadata_path),
                            "body_identity": identity(raw / (name + ".json"))})
    require(len(list(raw.glob("*.request.json"))) == len(expected_urls) == 21,
            "Complete exact set of 21 actual final GET responses")
    receipt = {
        "schema": "A2-DYN-independent-final-remote-preservation-v1",
        "status": "passed" if not failures else "failed", "started_utc": started, "finished_utc": now(),
        "scope": "Actual immutable final Git objects and exact source/evidence identities; separately timed moving branch heads. No remote mutation.",
        "commit": current, "root_tree": root_sha, "article_tree": article_sha, "sole_parent": PARENT_COMMIT,
        "program_identity": identity(Path(__file__)), "config_identity": identity(args.config),
        "expected_inventory_identity": identity(expected_path),
        "file_count": len(files), "article_blob_bytes": sum(e["size"] for e in files.values()),
        "file_identity_mismatches": file_mismatches, "tree_checks_including_root": tree_checks,
        "exact_C2_to_final_file_changes": changes, "existing_archive_files_unchanged": len(old_archives),
        "mathematical_source_checks": math_checks, "mathematical_source_sha256": math_fingerprint,
        "frozen_manifest_identity": identity(manifest_path), "frozen_source_checks": frozen_checks,
        "frozen_source_count": manifest["source_count"], "frozen_source_bytes": manifest["source_bytes"],
        "unrelated_tree_isolation": isolation, "original_baseline_to_final_isolation": original_isolation,
        "github_tree_unchanged": github_unchanged,
        "unchanged_workflow_blob": workflow["sha"], "branch_page_counts": page_counts,
        "baseline_branch_count": len(old_heads), "current_branch_count": len(heads),
        "baseline_observation_interval": [baseline["observed_started_utc"], baseline["observed_finished_utc"]],
        "missing_original_branches": missing_heads, "changed_original_branches": changed_heads,
        "added_branches_as_observed": added_heads, "three_refs_as_observed": refs,
        "branch_scope": "Complete branches/heads only, not tags; observed during the recorded GET interval, not an atomic global snapshot or a future-head assertion.",
        "raw_GET_records": raw_records,
        "CI_success_claimed": False, "current_commit_CI_completion_verified": False,
        "CI_scope": "This Git preservation audit does not certify CI. A C2 artifact-data audit, if cited separately, is not evidence of structured workflow completion at C2 or a CI execution at this final commit.",
        "continuum_mathematical_proof_certificate": False, "failures": failures,
    }
    output.write_text(json.dumps(receipt, indent=2) + "\n")
    (case / "RAW_RESPONSE_MANIFEST.json").write_text(json.dumps(raw_records, indent=2) + "\n")
    (case / "ALL_BRANCHES_AS_OBSERVED.json").write_text(json.dumps({"page_counts": page_counts, "branches": branch_rows}, indent=2) + "\n")
    print(json.dumps({"status": receipt["status"], "commit": current, "files": len(files),
                      "trees": len(tree_checks), "changes": len(changes), "frozen_sources": len(frozen_checks),
                      "mathematical_sources": len(math_checks), "original_heads_unchanged": len(old_heads) - len(missing_heads) - len(changed_heads),
                      "CI_success_claimed": False, "failures": failures}))
    if failures:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
