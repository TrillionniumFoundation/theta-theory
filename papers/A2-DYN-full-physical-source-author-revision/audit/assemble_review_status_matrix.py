#!/usr/bin/env python3
"""Recover an author-side historical report index from immutable readbacks.

This regenerates navigation after workspace maintenance. It does not create a
new referee report or claim byte identity with the pre-maintenance index.
"""
from pathlib import Path
import hashlib
import json
import re

BASE = Path(__file__).resolve().parent
ARTICLE = BASE.parent
READBACK = BASE / "recovery"
records = []
for path in sorted(READBACK.glob("REVIEW_PRIMARY_READBACK_*.json")):
    records.extend(json.loads(path.read_text())["records"])
if len(records) != 90:
    raise RuntimeError("Expected all 90 freshly verified original reports")
branches = json.loads((READBACK / "BRANCHES_READBACK_20261018.json").read_text())["branches"]
branch_map = {b["name"]: b["commit"]["sha"] for b in branches}
inventory_path = ARTICLE / "history/PRE_MAINTENANCE_TRANSPORT_INVENTORY.json"
if not inventory_path.exists():
    inventory_path = Path("/workspace/scratch/b5cc344d4c8e/transport/inventory.json")
inventory = json.loads(inventory_path.read_text())
prior = {r["path"]: r for r in inventory["files"]}
index = []
matrix = []
raw_commits = []
for record in records:
    name = record["branch"].removeprefix("review/")
    rel = "audit/reports/" + name + ".md"
    path = ARTICLE / rel
    raw = path.read_bytes()
    digest = hashlib.sha256(raw).hexdigest()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    expected = prior[rel]
    if (digest, blob, len(raw)) != (expected["sha256"], expected["git_blob"], expected["bytes"]):
        raise RuntimeError("Original report byte mismatch: " + rel)
    commit_response = record["commit_response"]
    report_response = record["report_response"]
    if commit_response.get("isError") or report_response.get("isError"):
        raise RuntimeError("Primary readback error: " + record["branch"])
    commit = json.loads(commit_response["structuredContent"]["content"])
    fetched = report_response["structuredContent"]
    if commit["sha"] != record["commit_sha"] or fetched["sha"] != blob:
        raise RuntimeError("Primary commit/path identity mismatch")
    if fetched["content"].encode("utf-8") != raw:
        raise RuntimeError("Fetched report path has different bytes")
    text = raw.decode("utf-8")
    lines = text.splitlines()
    aliases = sorted(k for k,v in branch_map.items()
                     if v == commit["sha"] and "a2-dyn" in k and k.startswith("review/"))
    item = {
        "branch": record["branch"], "commit_sha": commit["sha"],
        "review_commit_sha": commit["sha"], "review_repository_tree_sha": commit["tree"]["sha"],
        "review_commit_utc": commit["committer"]["date"],
        "review_commit_parents": [x["sha"] for x in commit.get("parents",[])],
        "report_path": record["report_path"], "blob_sha": blob,
        "sha256": digest, "bytes": len(raw),
        "local_path": "reports/" + name + ".md",
        "artifact_relative_report_path": rel,
        "branch_aliases_same_commit": aliases,
        "immutable_report_url": "https://github.com/TrillionniumFoundation/theta-theory/blob/"
                                + commit["sha"] + "/" + record["report_path"],
        "primary_commit_and_report_path_verified": True,
    }
    index.append(item)
    starts = [(i, line) for i,line in enumerate(lines) if re.match(r"^#{1,6}\s+\S",line)]
    sections=[]
    for ordinal,(start,heading) in enumerate(starts):
        stop = starts[ordinal+1][0] if ordinal+1 < len(starts) else len(lines)
        sections.append({"heading":heading,"line_start":start+1,"line_end":stop,
                         "original_text":"\n".join(lines[start:stop])+"\n"})
    header_stop = next((i for i,line in enumerate(lines[1:],1) if line.startswith("## ")),
                       min(150,len(lines)))
    source_header = "\n".join(lines[:header_stop])
    mentions=[]
    for i,line in enumerate(lines[:min(180,len(lines))]):
        for sha in re.findall(r"\b[0-9a-f]{40}\b",line):
            mentions.append({"sha":sha,"line":i+1,"original_context":line})
    required = [s for s in sections if re.search(
        r"remaining|revision|request|obstacle|unresolved|major|minor|proof|"
        r"recommendation|source|qualification|critical|capacity|incidence|clearance",
        s["heading"],re.I)]
    matrix.append({**item,"source_identity_header":source_header,
                   "sha_mentions_in_first_180_lines":mentions,
                   "all_original_sections":sections,
                   "revision_or_obstruction_sections":required,
                   "interpretation_scope":"Original report text/navigation; no fresh referee judgment."})
    raw_commits.append({"branch":record["branch"],"commit_sha":commit["sha"],
                        "response":commit_response})
index.sort(key=lambda x:(x["review_commit_utc"],x["branch"]))
matrix.sort(key=lambda x:(x["review_commit_utc"],x["branch"]))
(BASE/"reports_index.json").write_text(json.dumps(index,ensure_ascii=False,indent=2)+"\n")
controller = next(x for x in index if x["commit_sha"] == "f01482035a0b945b50f1f9c30f30ef35077558dc")
output = {
    "purpose":"Author revision history and source-scope matrix; not a new referee review",
    "recovery_status":"Regenerated after workspace maintenance from byte-verified original reports and fresh immutable API readbacks; prior output byte identity is not claimed.",
    "pre_maintenance_matrix_sha256":prior["audit/review_status_matrix.json"]["sha256"],
    "pre_maintenance_index_sha256":prior["audit/reports_index.json"]["sha256"],
    "report_count":len(index), "latest_valid_controller":controller,
    "controlling_report_reviewed_author_commit":"31792379408c5ace2c09284c2eb22d2331023433",
    "controlling_report_reviewed_repository_tree":"008dba443ce2ca29b3e276b1bf05bcf7021011c1",
    "controlling_report_active_native_scope":"260--276; substantive unreviewed increment 270--276",
    "subsequent_277_309_reviewed_by_controller":False,
    "A2_geometry_favorable_review_is_A2_DYN_review":False,
    "all_original_section_count":sum(len(x["all_original_sections"]) for x in matrix),
    "revision_or_obstruction_section_count":sum(len(x["revision_or_obstruction_sections"]) for x in matrix),
    "records":matrix,
}
(BASE/"review_status_matrix.json").write_text(json.dumps(output,ensure_ascii=False,indent=2)+"\n")
for i in range(3):
    obj={"scope":"Fresh immutable Git commit readbacks after workspace maintenance; original response-file serialization is not claimed.",
         "records":raw_commits[i*30:(i+1)*30]}
    (BASE/f"review_commit_metadata_{i}.response.json").write_text(json.dumps(obj,ensure_ascii=False,indent=2)+"\n")
report = ARTICLE/controller["artifact_relative_report_path"]
text=report.read_text()
start=text.index("## 18. The decisive remaining mathematical obstruction")
end=text.index("## 22. Final assessment")
header=("# Controlling report: required revisions and exact source identity\n\n"
        "This file reproduces the original report's Sections 18--21 as author-response navigation; it is not a new review.\n\n"
        "- Report commit: "+controller["commit_sha"]+".\n"
        "- Report blob: "+controller["blob_sha"]+".\n"
        "- Report SHA-256: "+controller["sha256"]+".\n"
        "- Reviewed author commit: 31792379408c5ace2c09284c2eb22d2331023433.\n"
        "- Reviewed repository tree: 008dba443ce2ca29b3e276b1bf05bcf7021011c1.\n"
        "- Actual reviewed active mathematical scope: modules 260--276. The report does not review 277--309.\n"
        "- Immutable report: "+controller["immutable_report_url"]+"\n\n")
(BASE/"CONTROL_REPORT_REQUIRED_REVISIONS_EXCERPT.md").write_text(header+text[start:end])
print(json.dumps({k:output[k] for k in ("report_count","all_original_section_count","revision_or_obstruction_section_count")},
                 indent=2))

