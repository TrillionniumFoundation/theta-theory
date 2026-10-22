#!/usr/bin/env python3
"""Reconstruct the recorded A2-DYN publication scope, offline and read-only.

Inputs are PUBLICATION_TREE_CHECK.json and its pinned ALL_REMOTE_HEADS.txt.
No Git checkout, network access, dependencies, or filesystem writes are used.
The article subtree and workflow blob are pinned object IDs: this program
reconstructs their embedding, not their contents. Workflow byte comparisons,
article-file verification, and CI are separate evidence in the source report.
"""

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


REPORT_SHA256 = "04ca41e4301c9e1bc177015bf888b37912d1f571304afd07d0863c358579b30f"
SNAPSHOT_SHA256 = "0dcf61bb69ac3e8910d5d169f27bdd72eb076a2920fc73fb86d61d7c61dc4b27"
BASE_COMMIT = "03d651b8709d28d90aa435fc12d608ad9c945e23"
BASE_ROOT = "d65973a6db0eb2c477359d10b43194cc5f99fa2f"
ARTICLE = "A2-DYN-localized-clearance-records-author-revision"
ARTICLE_TREE = "1fb3b20b29e3fe447bdae42f0faca0baf4f6b9cc"
WORKFLOW = "a2-dyn-localized-clearance-records-20261021.yml"
WORKFLOW_BLOB = "b1dcd980bfde8d195fd7c59b600861a520f6c6de"
NEW_ROOT = "d7a4a55f8b5b485bf766eb1fe8bf660618a20902"
COMMIT = "9bd4ab343bb8a0f78b6a6380ae1f1e80a976d761"
BRANCH = "refs/heads/revision/a2-dyn-localized-clearance-records-2026-10-21"
PREFIX_COUNTS = {
    "heads/revision/a2-dyn": 248,
    "heads/review/a2-dyn": 178,
    "heads/referee-copy/a2-dyn": 4,
    "heads/referee-response/a2-dyn": 4,
    "heads/research/a2-dyn": 1,
}
API = "https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/"
CHECKS = 0


class VerificationError(Exception):
    pass


def require(condition, message):
    global CHECKS
    if not condition:
        raise VerificationError(message)
    CHECKS += 1


def oid(value):
    return isinstance(value, str) and re.fullmatch(r"[0-9a-f]{40}", value) is not None


def tree(entries):
    """Return the canonical Git SHA-1 and payload size of a complete tree."""
    names = set()
    modes = {"040000": "tree", "100644": "blob", "100755": "blob",
             "120000": "blob", "160000": "commit"}
    for entry in entries:
        require(set(entry) == {"path", "mode", "type", "sha"}, "tree entry fields")
        name = entry["path"]
        require(isinstance(name, str) and name not in ("", ".", "..")
                and "/" not in name and "\0" not in name, "tree basename")
        require(name not in names, "duplicate tree basename")
        names.add(name)
        require(modes.get(entry["mode"]) == entry["type"], "tree mode/type")
        require(oid(entry["sha"]), "tree entry object ID")
    ordered = sorted(entries, key=lambda e: e["path"].encode("utf-8")
                     + (b"/" if e["type"] == "tree" else b""))
    payload = b"".join(
        ("40000" if e["mode"] == "040000" else e["mode"]).encode("ascii")
        + b" " + e["path"].encode("utf-8") + b"\0" + bytes.fromhex(e["sha"])
        for e in ordered)
    digest = hashlib.sha1(b"tree " + str(len(payload)).encode("ascii")
                          + b"\0" + payload).hexdigest()
    return {"sha": digest, "entries": len(entries), "payload_bytes": len(payload)}


def changes(before, after):
    old = {e["path"]: e for e in before}
    new = {e["path"]: e for e in after}
    return [{"path": n, "before": old.get(n), "after": new.get(n)}
            for n in sorted(set(old) | set(new)) if old.get(n) != new.get(n)]


def verify(report_path, snapshot_path):
    raw = report_path.read_bytes()
    snapshot = snapshot_path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == REPORT_SHA256, "pinned report SHA-256")
    require(hashlib.sha256(snapshot).hexdigest() == SNAPSHOT_SHA256,
            "pinned reference snapshot SHA-256")
    r = json.loads(raw)
    require(r["base_commit"] == BASE_COMMIT and r["base_root"] == BASE_ROOT,
            "base identity")
    require(r["new_article_path"] == "papers/" + ARTICLE
            and r["new_article_tree"] == ARTICLE_TREE, "article identity")
    require(r["expected_new_root"] == r["reconstructed_new_root"] == NEW_ROOT,
            "recorded new root")
    require(r["base_commit_api_response"]["sha"] == BASE_COMMIT
            and r["base_commit_api_response"]["tree"]["sha"] == BASE_ROOT,
            "recorded base commit/tree relationship")
    require(r["workflow"]["git_blob"] == WORKFLOW_BLOB
            and r["workflow"]["git_mode"] == "100644"
            and Path(r["workflow"]["path"]).name == WORKFLOW,
            "workflow object identity")

    api_inputs = r["complete_base_api_tree_inputs"]
    paths = {"root", "papers", ".github", ".github/workflows"}
    require(set(api_inputs) == paths, "four complete base tree inputs")
    base = {}
    base_checks = {e["path"]: e for e in r["base_tree_object_checks"]}
    require(set(base_checks) == paths and len(r["base_tree_object_checks"]) == 4,
            "four recorded base tree checks")
    old = {}
    for path, response in api_inputs.items():
        require(response["truncated"] is False, "base tree is not truncated: " + path)
        old[path] = response["tree"]
        base[path] = tree(old[path])
        require(base[path]["sha"] == response["sha"], "base canonical hash: " + path)
        require(response["url"] == API + "trees/" + response["sha"], "base API URL")
        require(base_checks[path] == {
            "path": path, "api_sha": response["sha"],
            "reconstructed_sha": base[path]["sha"],
            "entries": base[path]["entries"],
            "payload_bytes": base[path]["payload_bytes"],
            "matches": True, "truncated": False}, "base receipt agreement: " + path)
    require(base["root"]["sha"] == BASE_ROOT, "canonical base root")
    for parent, name, child in [("root", "papers", "papers"),
                                ("root", ".github", ".github"),
                                (".github", "workflows", ".github/workflows")]:
        entry = next((e for e in old[parent] if e["path"] == name), None)
        require(entry == {"path": name, "mode": "040000", "type": "tree",
                          "sha": base[child]["sha"]}, "base parent-child binding")

    new = {p: [dict(e) for e in rows] for p, rows in old.items()}
    for parent, name, sha, kind, mode in [
            ("papers", ARTICLE, ARTICLE_TREE, "tree", "040000"),
            (".github/workflows", WORKFLOW, WORKFLOW_BLOB, "blob", "100644")]:
        require(not any(e["path"] == name for e in new[parent]), "new path was absent")
        new[parent].append({"path": name, "mode": mode, "type": kind, "sha": sha})
    rebuilt = {p: tree(new[p]) for p in ("papers", ".github/workflows")}
    for parent, name, child in [(".github", "workflows", ".github/workflows"),
                                ("root", ".github", ".github"),
                                ("root", "papers", "papers")]:
        next(e for e in new[parent] if e["path"] == name)["sha"] = rebuilt[child]["sha"]
        rebuilt[parent] = tree(new[parent])
    require(rebuilt == r["new_trees"], "all four new canonical tree objects")
    require(rebuilt["root"]["sha"] == NEW_ROOT, "expected canonical publication root")
    diffs = {p: changes(old[p], new[p]) for p in old}
    require(diffs == r["tree_differences"], "recorded exact tree differences")
    allowed = {"root": [".github", "papers"], "papers": [ARTICLE],
               ".github": ["workflows"], ".github/workflows": [WORKFLOW]}
    require({p: [d["path"] for d in rows] for p, rows in diffs.items()} == allowed,
            "only authorized paths and necessary ancestor pointers changed")
    require(r["root_matches_expected"] is True
            and r["only_authorized_new_article_and_workflow"] is True,
            "recorded scope conclusions")

    f = r["a2_dyn_ref_freshness"]
    require(f["snapshot_sha256"] == SNAPSHOT_SHA256, "snapshot receipt binding")
    old_refs = {}
    for line in snapshot.decode("utf-8").splitlines():
        fields = line.split()
        require(len(fields) == 2, "snapshot row shape")
        sha, ref = fields
        require(oid(sha) and ref.startswith("refs/heads/") and ref not in old_refs,
                "snapshot unique valid head")
        old_refs[ref] = sha
    old_a2 = {ref: sha for ref, sha in old_refs.items() if "a2-dyn" in ref.lower()}
    queries = f["query_responses"]
    require(len(queries) == 5 and {q["prefix"] for q in queries} == set(PREFIX_COUNTS),
            "complete recorded five-prefix coverage")
    fresh = {}
    for q in queries:
        prefix = q["prefix"]
        require(q["url"] == API + "matching-refs/" + prefix, "matching-ref API URL")
        require(len(q["refs"]) == PREFIX_COUNTS[prefix], "recorded prefix count")
        for row in q["refs"]:
            ref, sha = row["ref"], row["sha"]
            require(set(row) == {"ref", "sha", "type"} and row["type"] == "commit"
                    and ref.startswith("refs/" + prefix) and oid(sha)
                    and ref not in fresh, "unique valid matching ref")
            fresh[ref] = sha
    covered = all(any(ref.startswith("refs/" + p) for p in PREFIX_COUNTS) for ref in old_a2)
    require(covered and f["all_snapshot_a2_dyn_refs_covered_by_queried_prefixes"] is True,
            "all old A2-DYN heads covered by queries")
    added = [{"ref": ref, "sha": fresh[ref]} for ref in sorted(fresh.keys() - old_a2.keys())]
    removed = [{"ref": ref, "sha": old_a2[ref]} for ref in sorted(old_a2.keys() - fresh.keys())]
    moved = [{"ref": ref, "before": old_a2[ref], "after": fresh[ref]}
             for ref in sorted(old_a2.keys() & fresh.keys()) if old_a2[ref] != fresh[ref]]
    require(added == f["added"] == [{"ref": BRANCH, "sha": COMMIT}], "only new author head added")
    require(removed == f["removed"] == [], "no historical A2-DYN head removed")
    require(moved == f["moved"] == [], "no historical A2-DYN head moved")
    old_review = {k: v for k, v in old_a2.items() if k.startswith("refs/heads/review/")}
    fresh_review = {k: v for k, v in fresh.items() if k.startswith("refs/heads/review/")}
    counts = {
        "snapshot_all_repository_heads": len(old_refs),
        "snapshot_a2_dyn_heads": len(old_a2), "fresh_a2_dyn_heads": len(fresh),
        "fresh_a2_dyn_distinct_commits": len(set(fresh.values())),
        "unchanged_count": sum(fresh.get(k) == v for k, v in old_a2.items()),
        "old_review_heads": len(old_review), "fresh_review_heads": len(fresh_review)}
    require(counts == {k: f[k] for k in counts}, "recomputed reference counts")
    require(list(counts.values()) == [1301, 434, 435, 219, 434, 178, 178],
            "pinned census and freshness totals")
    require(old_review == fresh_review and f["all_review_head_commit_ids_unchanged"] is True,
            "all historical review head IDs unchanged")

    publication = r["published_commit_identity_check"]
    commit = publication["api_commit"]
    require(commit["sha"] == COMMIT and commit["tree"]["sha"] == rebuilt["root"]["sha"],
            "published commit API binds the reconstructed tree")
    require([p["sha"] for p in commit["parents"]] == [BASE_COMMIT], "sole published parent")
    require(publication["expected_parent"] == BASE_COMMIT
            and publication["expected_root"] == NEW_ROOT
            and publication["parent_matches"] is True
            and publication["root_matches_independent_reconstruction"] is True,
            "published identity receipt agreement")
    require(r["remote_write_performed"] is False and r["current_ci_success_claimed"] is False,
            "source report scope excludes remote writes and CI certification")
    return {
        "status": "passed", "explicit_conditions_checked": CHECKS,
        "input_sha256": {"report": REPORT_SHA256, "reference_snapshot": SNAPSHOT_SHA256},
        "base_commit": BASE_COMMIT, "base_canonical_trees": base,
        "article_subtree_object_id": ARTICLE_TREE, "workflow_blob_object_id": WORKFLOW_BLOB,
        "reconstructed_publication_trees": rebuilt,
        "changed_paths_in_parent_trees": allowed,
        "reference_counts": counts, "added": added, "removed": removed, "moved": moved,
        "published_commit": COMMIT, "sole_parent": BASE_COMMIT,
        "scope": "Offline canonical-tree and recorded ref-difference reconstruction only.",
        "limits": ["Article subtree and workflow blob contents are separately verified inputs.",
                   "Commit/tree/parent binding is checked in recorded API data; commit bytes are not rehashed.",
                   "Ref freshness is only as of the recorded GETs, not the time this checker is run.",
                   "No network, repository mutation, current CI check, or mathematical certification is performed."]}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    args = parser.parse_args()
    try:
        result = verify(args.report, args.snapshot)
    except (OSError, ValueError, KeyError, TypeError, StopIteration, VerificationError) as error:
        print(json.dumps({"status": "failed", "error": str(error),
                          "explicit_conditions_passed_before_failure": CHECKS}, indent=2),
              file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
