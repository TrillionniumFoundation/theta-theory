#!/usr/bin/env python3
"""Offline provenance verification for the frozen A2-DYN source census.

Reads only this article's audit records and the preserved 660-object archive.
No network, Git checkout, scratch directory, or installed mathematical package
is needed. This is a source-identity check, not a mathematical verification.
"""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import gzip
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import tarfile

ROOT = Path(__file__).resolve().parents[1]
CARRIER = "d6c3c6754fb3a1b4ad3eea8e6dcc51642e312b28"
SOURCE = "85f206907f56773e32fae9b61302924ca16603aa"
ARTICLE_TREE = "381d0aa576a93d874bf974b0edcf090378aaa41b"
PACKET = "A2-DYN-section-multipliers-exact-inversion-author-revision"
ADDED_REF = "refs/heads/revision/a2-dyn-section-multipliers-exact-inversion-2026-10-23"
HEX40 = re.compile(r"[0-9a-f]{40}\Z")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def unique(rows, key, description):
    result = {row[key]: row for row in rows}
    require(len(result) == len(rows), f"Duplicate {description}")
    return result


def object_id(kind, body):
    return hashlib.sha1(kind.encode()+b" "+str(len(body)).encode()+b"\0"+body).hexdigest()


def tree_id(entries):
    """Reconstruct canonical Git tree bytes, including directory-name sorting."""
    require(len({e["name"] for e in entries}) == len(entries), "Duplicate tree entry")
    encoded = []
    for entry in entries:
        name, oid = entry["name"], entry["oid"]
        require("/" not in name and "\0" not in name and name not in ("", ".", ".."),
                "Invalid direct tree name")
        require(HEX40.fullmatch(oid) is not None, "Invalid tree child object ID")
        mode = format(int(entry["mode"], 8), "o")
        require(entry["type"] in ("tree", "blob", "commit"), "Unknown Git entry type")
        require((mode == "40000") == (entry["type"] == "tree"), "Git tree mode/type mismatch")
        raw_name = name.encode("utf-8")
        key = raw_name+(b"/" if entry["type"] == "tree" else b"")
        encoded.append((key, mode.encode()+b" "+raw_name+b"\0"+bytes.fromhex(oid)))
    return object_id("tree", b"".join(value for _, value in sorted(encoded)))


def verify_api_tree(payload, recursive):
    require(payload.get("truncated") is False, "Truncated fresh Git tree payload")
    entries = unique(payload["tree"], "path", "fresh tree paths")
    groups = defaultdict(list)
    for path, entry in entries.items():
        parts = PurePosixPath(path).parts
        require(parts and not path.startswith("/") and all(p not in (".", "..") for p in parts),
                "Unsafe/noncanonical API tree path")
        parent = "/".join(parts[:-1])
        if not recursive:
            require(not parent, "Expected a direct, not recursive, papers tree")
        elif parent:
            require(parent in entries and entries[parent]["type"] == "tree", "Missing API parent tree")
        groups[parent].append({"name": parts[-1], "oid": entry["sha"],
                               "type": entry["type"], "mode": entry["mode"]})
    expected = {"": payload["sha"]}
    if recursive:
        expected.update({path: e["sha"] for path, e in entries.items() if e["type"] == "tree"})
    for path, oid in expected.items():
        require(tree_id(groups.get(path, [])) == oid, f"Fresh tree hash mismatch: {path or '/'}")
    return entries, expected


def verify():
    identities = []
    checks = []

    def raw(name):
        require(name.startswith("audit/") or name == "history/ALL_660_NATIVE_SOURCE_OBJECTS.tar.gz",
                "Verifier input must be a preserved article audit/archive")
        data = (ROOT/name).read_bytes()
        identities.append({"path": name, "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()})
        return data

    def read(name):
        data = raw(name)
        return json.loads(gzip.decompress(data) if name.endswith(".gz") else data)

    def passed(name, details):
        checks.append({"name": name, "passed": True, "details": details})

    old = read("audit/ALL435_DIRECT_SOURCE_ROLE_CENSUS.json")
    fresh = read("audit/refs_snapshot.json")
    initial_raw = raw("audit/INITIAL_REMOTE_HEADS.json.gz")
    initial_bytes = gzip.decompress(initial_raw)
    initial = json.loads(initial_bytes)
    require(hashlib.sha256(initial_bytes).hexdigest() == old["input_sha256"],
            "Original direct census is not bound to the preserved initial ref response")
    prior = {k: row["sha"] for k, row in unique(old["refs"], "ref", "historical refs").items()}
    current_all = {k: row["sha"] for k, row in unique(fresh["refs"], "ref", "fresh refs").items()}
    initial_refs = unique(initial, "ref", "initial refs")
    initial_a2 = {ref: row["object"]["sha"] for ref, row in initial_refs.items() if "a2-dyn" in ref.lower()}
    current = {ref: sha for ref, sha in current_all.items() if "a2-dyn" in ref.lower()}
    added = {ref: sha for ref, sha in current.items() if ref not in prior}
    removed = {ref: sha for ref, sha in prior.items() if ref not in current}
    changed = {ref: {"old": sha, "new": current[ref]} for ref, sha in prior.items()
               if ref in current and current[ref] != sha}
    require(len(initial_refs) == 1304 and initial_a2 == prior, "Historical 435-ref identity mismatch")
    require(len(current_all) == 1306 and len(prior) == 435 and len(current) == 436, "Fresh ref-count mismatch")
    require(not removed and not changed and added == {ADDED_REF: CARRIER}, "Unexpected A2-DYN ref delta")
    passed("frozen ref reconciliation", {"initial_total": 1304, "fresh_total": 1306,
           "historical_a2_dyn": 435, "fresh_a2_dyn": 436, "unchanged": 435, "added": added})

    dag = read("audit/SCOPED_GIT_OBJECT_CENSUS.json.gz")
    commits = unique(dag["commits"], "sha", "DAG commits")
    trees = unique(dag["trees"], "oid", "DAG trees")
    blobs = unique(dag["blobs"], "oid", "DAG blobs")
    dag_refs = unique(dag["refs"], "ref", "DAG refs")
    require({k: v["sha"] for k, v in dag_refs.items()} == prior, "DAG refs differ from direct census")
    require(set(commits) == set(old["commits"]) and len(commits) == 219, "DAG commit identity mismatch")
    require(len(trees) == 950 and len(blobs) == 5631, "Scoped DAG object count mismatch")
    for sha, record in old["commits"].items():
        dc = commits[sha]
        header = dc["commit_header"].splitlines()
        require(dc["tree"] == record["root_tree"] and "tree "+dc["tree"] in header,
                "Commit/root-tree metadata mismatch")
        require([line[7:] for line in header if line.startswith("parent ")] == record["parents"],
                "Commit parent metadata mismatch")
        require(dc["subject"] == record["subject"], "Commit subject metadata mismatch")
    for ref, item in dag_refs.items():
        require(item["sha"] in commits and item["tree"] == commits[item["sha"]]["tree"],
                "Ref-to-commit/root lookup does not close")
    outside_parents = sorted({parent for c in old["commits"].values() for parent in c["parents"]}-set(commits))
    passed("original head commit lookup", {"recorded_commits": 219,
           "parents_outside_recorded_headset": outside_parents,
           "qualification": "Header/metadata reconciliation; absent full commit bodies and unrecorded ancestors are not rehashed or declared present."})

    for oid, tree in trees.items():
        require(tree_id(tree["entries"]) == oid, f"Historical Git tree hash mismatch: {oid}")
        for entry in tree["entries"]:
            collection = trees if entry["type"] == "tree" else blobs if entry["type"] == "blob" else commits
            require(entry["oid"] in collection, "Scoped child lookup does not close")
    scope = {(s["commit"], s["path"]): s for s in dag["scope_roots"]}
    require(len(scope) == len(dag["scope_roots"]) == 39276, "Duplicate/missing scope-root records")
    for item in scope.values():
        require(item["commit"] in commits, "Scope root has absent commit")
        require(item["oid"] in (trees if item["type"] == "tree" else blobs), "Scope root has absent object")
    visited, active, reached_blobs = set(), set(), set()

    def walk(oid):
        require(oid not in active, "Cycle in recorded tree DAG")
        if oid in visited:
            return
        active.add(oid)
        for entry in trees[oid]["entries"]:
            if entry["type"] == "tree":
                walk(entry["oid"])
            elif entry["type"] == "blob":
                reached_blobs.add(entry["oid"])
        active.remove(oid)
        visited.add(oid)

    for item in scope.values():
        if item["type"] == "tree":
            walk(item["oid"])
        else:
            reached_blobs.add(item["oid"])
    require(visited == set(trees) and reached_blobs == set(blobs), "Unreachable scoped tree/blob metadata")
    passed("original scoped tree DAG", {"tree_object_hashes_recomputed": 950,
           "blob_metadata_reachable": 5631, "scope_root_records": 39276,
           "qualification": "Only the 660 native blobs below have their body bytes rehashed; the other blob bodies are not claimed present."})

    leaf_lookups = 0
    for sha, commit in old["commits"].items():
        for field, section, leaf, folder in [
            ("papers_tree", "paper_sets", "article_trees", "papers"),
            ("reviews_tree", "review_sets", "report_directory_trees", "reviews")]:
            tree = commit.get(field)
            if tree is None:
                continue
            require(tree in old[section], "Missing direct paper/review set")
            for name, sub in old[section][tree].items():
                require(sub in old[leaf] and sub in trees, "Missing direct source/report directory")
                scoped = scope.get((sha, folder+"/"+name))
                require(scoped is not None and scoped["type"] == "tree" and scoped["oid"] == sub,
                        "Direct-source lookup differs from scoped Git DAG")
                leaf_lookups += 1
    for oid, article in old["article_trees"].items():
        direct = {e["name"]: {"type": e["type"], "sha": e["oid"], "mode": int(e["mode"], 8)}
                  for e in trees[oid]["entries"]}
        expected = {name: {"type": e["type"], "sha": e["sha"], "mode": int(e["mode"], 8)}
                    for name, e in article["direct_entries"].items()}
        # The direct-role census intentionally records selected diagnostic
        # entries. The scoped DAG holds the complete tree whose ID is rehashed.
        require(all(name in direct and direct[name] == entry for name, entry in expected.items()),
                "Historical article's recorded direct entry differs from hashed tree")
        require(("main.tex" in expected) == ("main.tex" in direct)
                == article["native_main_present"], "Historical main presence flag differs from hashed tree")
    for oid, report in old["report_directory_trees"].items():
        entries = {e["name"]: e for e in trees[oid]["entries"]}
        for entry in report["direct_reports"]:
            require(entry["name"] in entries and entries[entry["name"]]["oid"] == entry["sha"]
                    and entries[entry["name"]]["type"] == entry["type"], "Direct report identity mismatch")
    require(len(old["article_trees"]) == 122 and len(old["report_directory_trees"]) == 91,
            "Direct directory count mismatch")
    passed("direct source/report closure", {"commit_directory_lookups": leaf_lookups,
           "article_trees": 122, "report_directory_trees": 91, "missing_lookups": 0})

    manifest = read("audit/NATIVE_SOURCE_CONTENT_IDENTITIES.json")
    by_oid = unique(manifest, "oid", "native manifest objects")
    native_dag = {oid for oid, item in blobs.items() if any(n.endswith(".tex") for n in item["names"])}
    require(len(by_oid) == 660 and set(by_oid) == native_dag, "Native archive/DAG coverage mismatch")
    archive_name = "history/ALL_660_NATIVE_SOURCE_OBJECTS.tar.gz"
    raw(archive_name)  # Record the compressed archive identity; members are never extracted.
    body_checks = []
    with tarfile.open(ROOT/archive_name, "r:gz") as archive:
        members = archive.getmembers()
        require(len(members) == 660 and all(member.isfile() for member in members), "Archive contains nonnative members")
        require(len({member.name for member in members}) == 660, "Duplicate archive members")
        require({member.name for member in members} == {oid+".tex" for oid in by_oid}, "Archive member names mismatch")
        for member in members:
            oid = member.name[:-4]
            stream = archive.extractfile(member)
            require(stream is not None, "Unreadable native archive member")
            body = stream.read()
            actual = {"git_blob": object_id("blob", body), "bytes": len(body),
                      "sha256": hashlib.sha256(body).hexdigest()}
            item = by_oid[oid]
            require(actual["git_blob"] == oid and actual["bytes"] == item["bytes"]
                    and actual["sha256"] == item["sha256"], f"Native body identity mismatch: {oid}")
            body_checks.append(actual)
    body_checks.sort(key=lambda item: item["git_blob"])
    mains, no_main = [], []
    for tree, article in old["article_trees"].items():
        entry = article["direct_entries"].get("main.tex")
        if entry is None:
            no_main.append({"article_tree": tree, "first_seen_path": article["first_seen_path"]})
        else:
            require(entry["type"] == "blob" and entry["sha"] in by_oid, "Historical main missing from verified archive")
            mains.append({"article_tree": tree, "main_blob": entry["sha"]})
    require(len(mains) == 120 and len(no_main) == 2, "Historical main-source coverage mismatch")
    passed("all archived native bodies and direct mains", {"git_blob_and_sha256_and_size_verified": 660,
           "direct_article_main_entries_covered": 120, "packets_without_main": no_main,
           "qualification": "Entry/body coverage does not establish historical include closure, successful compilation, or mathematical completeness."})

    papers = read("audit/LATEST_PAPERS_TREE.json")
    article = read("audit/LATEST_ARTICLE_TREE.json")
    paper_entries, paper_hashes = verify_api_tree(papers, recursive=False)
    article_entries, article_hashes = verify_api_tree(article, recursive=True)
    require(paper_entries[PACKET]["type"] == "tree"
            and paper_entries[PACKET]["sha"] == article["sha"] == ARTICLE_TREE, "Fresh author article identity mismatch")
    download = read("audit/BASELINE_DOWNLOAD_RECEIPT.json")
    require(download["commit"] == CARRIER and download["article_tree"] == ARTICLE_TREE, "Baseline receipt identity mismatch")
    for item in download["files"]:
        entry = article_entries.get(item["path"])
        require(entry is not None and entry["type"] == "blob" and entry["sha"] == item["git_blob"]
                and entry["size"] == item["bytes"], "Downloaded-file receipt does not match fresh article tree")
    passed("fresh direct/recursive tree payloads", {"carrier_commit": CARRIER,
           "papers_tree": papers["sha"], "article_tree": ARTICLE_TREE,
           "fresh_tree_object_hashes_recomputed": len(paper_hashes)+len(article_hashes),
           "download_receipt_entries_bound_to_tree": len(download["files"]),
           "qualification": "Receipt entries are checked against Git metadata; this step does not claim a second download or body rehash of the current author packet."})

    compare = read("audit/SOURCE_TO_CARRIER_COMPARE.json")
    require(compare["base"] == SOURCE and compare["head"] == CARRIER and compare["status"] == "ahead",
            "Source/carrier comparison endpoints mismatch")
    require((compare["ahead_by"], compare["behind_by"], compare["total_commits"]) == (1, 0, 1),
            "Source/carrier comparison graph mismatch")
    require(compare["base_commit"]["sha"] == compare["merge_base_commit"]["sha"] == SOURCE,
            "Source/carrier merge base mismatch")
    files = [f.get("filename", f.get("path")) for f in compare["files"]]
    prefix = "papers/"+PACKET+"/"
    require(len(files) == len(set(files)) == 30, "Source/carrier changed-path count mismatch")
    for path, item in zip(files, compare["files"]):
        require(path in (prefix+"PUBLICATION_STATUS.json", prefix+"VALIDATION_REPORT.md") or
                (path.startswith(prefix+"evidence/github/") and path.endswith(".json")),
                "Source/carrier change is not one of the permitted metadata/evidence paths")
        require(item["status"] in ("added", "modified") and item.get("previous_filename") is None,
                "Hidden rename/removal in source/carrier comparison")
    passed("source-to-carrier metadata-only comparison", {"source": SOURCE, "carrier": CARRIER,
           "ahead_by": 1, "changed_paths": files, "native_source_paths_changed": 0})

    delta = read("audit/CURRENT_SOURCE_CENSUS_DELTA.json")
    require(delta["snapshot_utc"] == fresh["captured_at"] and delta["added_refs"] == added
            and not delta["removed_refs"] and not delta["changed_refs"] and not delta["lookup_failures"],
            "Preserved reconciliation delta mismatch")
    require({item["ref"]: item["sha"] for item in delta["all_refs"]} == current,
            "Preserved reconciliation ref list mismatch")
    require(sorted(delta["native_body_checks"], key=lambda x: x["git_blob"]) == body_checks,
            "Preserved reconciliation native-body checks mismatch")
    require(sorted(delta["historical_direct_main_blobs_in_verified_archive"], key=lambda x: x["article_tree"])
            == sorted(mains, key=lambda x: x["article_tree"]), "Preserved reconciliation main coverage mismatch")
    latest = delta["latest_source"]
    require(latest["source_commit"] == SOURCE and latest["carrier_commit"] == CARRIER
            and latest["carrier_papers_tree"] == papers["sha"] and latest["carrier_article_tree"] == ARTICLE_TREE
            and latest["changed_paths"] == files, "Preserved latest-source identities mismatch")
    legacy_map = {
        "baseline/audit/ALL435_DIRECT_SOURCE_ROLE_CENSUS.json": "audit/ALL435_DIRECT_SOURCE_ROLE_CENSUS.json",
        "research/refs_snapshot.json": "audit/refs_snapshot.json",
        "baseline/audit/NATIVE_SOURCE_CONTENT_IDENTITIES.json": "audit/NATIVE_SOURCE_CONTENT_IDENTITIES.json",
        "research/LATEST_PAPERS_TREE.json": "audit/LATEST_PAPERS_TREE.json",
        "research/latest_article_tree.json": "audit/LATEST_ARTICLE_TREE.json",
        "research/SOURCE_TO_CARRIER_COMPARE.json": "audit/SOURCE_TO_CARRIER_COMPARE.json"}
    by_path = {item["path"]: item for item in identities}
    require(len(delta["input_identities"]) == len(legacy_map), "Unexpected prior reconciliation input set")
    for item in delta["input_identities"]:
        require(item["path"] in legacy_map, "Unknown legacy provenance label")
        preserved = by_path[legacy_map[item["path"]]]
        require(item["bytes"] == preserved["bytes"] and item["sha256"] == preserved["sha256"],
                "A preserved input differs from the original research execution")
    passed("preserved research reconciliation independently reproduced", {"input_identities_matched": 6,
           "legacy_paths": "Labels only; no legacy or external path is opened."})

    return {"schema": "a2-dyn-portable-census-verification-v1", "status": "PASS", "all_passed": True,
            "scope": "Offline provenance only: frozen ref reconciliation, preserved scoped Git DAG and direct-source lookups, exact tree/native-blob identities, main-entry coverage, and source/carrier metadata comparison. No network freshness, complete ancestor DAG, build result, referee acceptance, mathematical theorem, or raw LLT is certified.",
            "snapshot_utc": fresh["captured_at"], "input_identities": identities,
            "checks": checks, "check_groups": len(checks), "historical_ref_count": len(prior),
            "fresh_ref_count": len(current), "fresh_total_ref_count": len(current_all),
            "unchanged_historical_refs": len(prior), "added_refs": added,
            "fresh_role_hints": dict(Counter(ref.split("/")[2] for ref in current)),
            "historical_tree_hashes_recomputed": len(trees),
            "fresh_tree_hashes_recomputed": len(paper_hashes)+len(article_hashes),
            "native_body_checks": body_checks,
            "historical_direct_main_blobs_in_verified_archive": sorted(mains, key=lambda x: x["article_tree"]),
            "historical_packets_without_main": no_main}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify()
    except Exception as exc:
        result = {"schema": "a2-dyn-portable-census-verification-v1", "status": "FAIL",
                  "all_passed": False, "scope": "Offline provenance only", "error": str(exc),
                  "error_type": type(exc).__name__}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2)+"\n")
    print(json.dumps({key: result[key] for key in
          ("status", "check_groups", "fresh_ref_count", "fresh_total_ref_count", "error") if key in result}))
    raise SystemExit(0 if result["all_passed"] else 1)


if __name__ == "__main__":
    main()
