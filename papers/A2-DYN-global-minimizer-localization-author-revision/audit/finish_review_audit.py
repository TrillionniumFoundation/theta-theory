#!/usr/bin/env python3
"""Rebuild author-side documentary navigation and explicit recovery receipts."""
from collections import Counter, defaultdict
import hashlib
import json
import re
from pathlib import Path

A = Path(__file__).resolve().parent
R = A.parent
REPO = "TrillionniumFoundation/theta-theory"
INV_PATH = R / "history/PRE_MAINTENANCE_TRANSPORT_INVENTORY.json"
INV = json.loads(INV_PATH.read_text())
OLD = {x["path"]: x for x in INV["files"]}

def ident(p):
    b = p.read_bytes()
    return {"path": str(p.relative_to(R)), "bytes": len(b),
            "sha256": hashlib.sha256(b).hexdigest(),
            "git_blob": hashlib.sha1(b"blob " + str(len(b)).encode() + b"\0" + b).hexdigest()}

def put(name, data):
    p = A / name
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n")

def decode_response(x):
    if "structuredContent" in x:
        c = x["structuredContent"].get("content")
        if isinstance(c, str):
            return json.loads(c)
    return x

branches = json.loads((A / "recovery/BRANCHES_READBACK_20261018.json").read_text())["branches"]
dyn = [b for b in branches if "a2-dyn" in b["name"].lower()]
author = json.loads((R / "history/all-author-head-commits.json").read_text())
articles = json.loads((R / "history/all-author-article-variants.json").read_text())
reports = json.loads((A / "reports_index.json").read_text())
report_map = {x["commit_sha"]: x for x in reports}
author_map = {x["commit"]: x for x in author["commits"]}
canonical = {x["branch"] for x in reports}

def role(n):
    if n.startswith("research/"):
        return "historical_research_source"
    if n.startswith("review/"):
        return "canonical_report" if n in canonical else "report_copy_or_alias"
    if "referee-copy" in n:
        return "author_referee_copy"
    if "referee-response" in n:
        return "author_referee_response"
    return "author_revision"

ref_records = []
for b in dyn:
    s = b["commit"]["sha"]
    p = {"ref": b["name"], "head_sha": s, "role": role(b["name"]),
         "protected_at_readback": b["protected"], "immutable_commit_url":
         "https://github.com/" + REPO + "/commit/" + s}
    if s in author_map:
        p["repository_tree_sha"] = author_map[s]["tree"]
    if s in report_map:
        rr = report_map[s]
        p.update({"report_blob_sha": rr["blob_sha"], "report_sha256": rr["sha256"],
                  "report_path": rr["report_path"], "report_artifact": rr["artifact_relative_report_path"]})
    ref_records.append(p)

ci_readbacks = json.loads((R / "history/HISTORICAL_CI_ACTUAL_READBACK.json").read_text())
job_paths = {
    "summable_physical_source": "history/SUMMABLE_FAILED_CI_JOBS.json",
    "sublevel_clearance": "audit/recovery/CI_JOB_READBACK_2.json",
    "physical_source": "audit/recovery/CI_JOB_READBACK_3.json",
    "reviewed_v115": "audit/recovery/CI_JOB_reviewed-v115.json",
    "workflow_only_v113": "audit/recovery/CI_JOB_workflow-only-v113.json",
}
ci_scopes = {
    "summable_physical_source": "Completed failure. Native source execution failed; no complete native qualification pass.",
    "sublevel_clearance": "Completed failure. Native continuation validation/build failed; no complete native qualification pass.",
    "physical_source": "Completed success is only a source/ref freeze and archive success: dependency installation and native qualification were both skipped.",
    "reviewed_v115": "Later completed native checks/build success. At the controlling report's earlier freeze the run was queued; that historical observation remains correct.",
    "workflow_only_v113": "Completed source-export success. Workflow-only/export source is not a complete native manuscript or mathematical qualification.",
}
ci = []
for r in ci_readbacks["records"]:
    raw = decode_response(r["response"])
    jobs = decode_response(json.loads((R / job_paths[r["name"]]).read_text()))
    ci.append({
        "source_name": r["name"], "head_sha": r["sha"], "interpretation": ci_scopes[r["name"]],
        "raw_run_list": "history/HISTORICAL_CI_ACTUAL_READBACK.json",
        "raw_jobs": job_paths[r["name"]],
        "runs": [{k: w.get(k) for k in ("id", "head_branch", "head_sha", "name", "path", "status", "conclusion", "created_at", "updated_at", "html_url")} for w in raw["workflow_runs"]],
        "jobs": [{"id": j["id"], "name": j["name"], "status": j["status"], "conclusion": j["conclusion"],
                  "steps": [{k: s.get(k) for k in ("name", "number", "status", "conclusion", "started_at", "completed_at")} for s in j["steps"]]} for j in jobs["jobs"]],
    })
excluded_geometry = [{ "ref": b["name"], "head_sha": b["commit"]["sha"],
                      "reason": "A2 geometry source/report, not A2-DYN dynamics review"}
    for b in branches if re.match(r"review/a2(?:-|/)", b["name"]) and "a2-dyn" not in b["name"]]

pipeline = {
 "purpose": "Complete observed A2-DYN ref census, exact source/review crosswalk and explicitly scoped CI/publication evidence",
 "recovery": "Fresh metadata reconstruction from independently read immutable objects after maintenance; no identity claim for the former lost JSON serialization.",
 "readback_date": "2026-10-18", "repository": REPO,
 "branch_pagination": {"pages_read": 14, "page_counts": [100]*12+[83, 0], "repository_branch_count": len(branches)},
 "a2_dyn_ref_count": len(dyn), "role_counts": dict(Counter(x["role"] for x in ref_records)),
 "author_named_ref_count": sum(b["name"].startswith(("revision/", "research/")) for b in dyn),
 "author_distinct_commit_count": author["count"], "distinct_article_tree_count": articles["article_tree_count"],
 "distinct_numbered_native_blobs": articles["numbered_blob_union_count"],
 "canonical_report_count": len(reports), "review_ref_count_with_aliases": sum(b["name"].startswith("review/") for b in dyn),
 "complete_author_tree_census": "history/all-author-article-variants.json",
 "complete_author_commit_metadata": "history/all-author-head-commits.json",
 "complete_report_identity_and_text": "audit/reports_index.json",
 "all_original_report_section_navigation": "audit/review_status_matrix.json",
 "controlling_report": next(x for x in reports if x["commit_sha"] == "f01482035a0b945b50f1f9c30f30ef35077558dc"),
 "controller_reviewed_author_sha": "31792379408c5ace2c09284c2eb22d2331023433",
 "controller_reviewed_repository_tree": "008dba443ce2ca29b3e276b1bf05bcf7021011c1",
 "controller_active_scope": "260--276; does not review subsequent 277--309",
 "latest_complete_native_continuation_sha": "fb99e4d67ef74912f6c69b05c9abff3207572e7a",
 "completeness_is_not_CI_success_or_final_theorem_completion": True,
 "fresh_CI_scope": "Exact-head run lists and every returned job/step for the five decisive source candidates below. Other historical CI statements remain frozen report evidence; this is not a claim to reread every historical GitHub Actions run.",
 "ci_readbacks": ci,
 "new_revision_publication_at_this_audit_snapshot": {
     "requested_branch": "revision/a2-dyn-global-minimizer-localization-2026-10-18",
     "workflow_path": ".github/workflows/a2-dyn-global-minimizer-localization-20261018.yml",
     "scope": "Workflow authored and byte verified. Use root PUBLICATION_STATUS.json and exact-head post-push readbacks for subsequent commit/push/CI facts; this audit does not invent them.",
     "raw_pointwise_LLT_or_four_coordinate_inversion_complete": False},
 "A2_geometry_reports_excluded": excluded_geometry,
 "refs": ref_records,
}
put("PIPELINE_REF_CENSUS.json", pipeline)

# Census status is generated from the actual final native and preserved TeX/text.
bib = json.loads((A / "HISTORICAL_BIBLIOGRAPHY_CENSUS.json").read_text())
detail = {
 "AFP": ("Ambrosio--Fusco--Pallara, Functions of bounded variation", "BV/coarea and trace hypotheses, representative choices and physical paired traces must be matched; bulk-null sets do not establish null traces."),
 "BDL": ("Baladi--Demers--Liverani, Exponential decay of correlations for finite-horizon Sinai billiard flows", "Retain the source-pinned corrected arXiv version, observable norms and flow singularity hypotheses; correlation decay alone does not establish raw roof height."),
 "BHN": ("Bruin--Holland--Nicol, Livsic regularity for Markov systems", "Match actual inducing/Markov representation and regularity transfer; an auxiliary Markov theorem must not replace the real billiard."),
 "BMN": ("Basu--Mohammad-Nezhad, Effective Lojasiewicz inequalities", "Historical locator Theorem 4, arXiv:2211.10034v2; polynomial degree/dimension and effective constants need matching on the actual charts."),
 "BPR": ("Basu--Pollack--Roy, connected components of sign conditions", "Historical locator Section 3.2, equation (3.3), version 3; actual variable/degree and sign-condition counts must be retained."),
 "BT65": ("Bolotin--Treschev, Hill's formula", "General determinant convention and orientation require matching; the relevant elementary two-dimensional reversible identity is native."),
 "BVNotes": ("Boyd--Vandenberghe, convex duality lecture notes", "Background only. The new global variational, midpoint and disk normal arguments have native proofs and import no theorem from the notes."),
 "CMInt": ("Cluckers--Miller, stability under integration of constructible functions", "Historical Theorems 1.3 and 3.11 require actual definability and integrability; they do not give unsupplied uniform roof constants."),
 "CVExt": ("Carneiro--Vaaler, Some extremal functions in Fourier analysis II", "Match test class, exponential type and transform conventions before using a majorant in inversion."),
 "Coste": ("Coste, An introduction to o-minimal geometry", "Definability and finite decomposition are distinct from a collision-uniform analytic or normalized capacity estimate."),
 "CosteSAG": ("Coste, An introduction to semialgebraic geometry", "Historical Sections 2.2--2.3 and Theorem 2.12 need matching to the actual algebraic projection/closure construction."),
 "DJS": ("Doering--Jansen--Schubert, The method of cumulants for the normal approximation", "Cumulant order, scale and norm dependence must remain uniform in the parameters used by the native spectral argument."),
 "DPZ": ("Demers--Pene--Zhang, Local limit theorem for randomly deforming billiards", "Historical arXiv:1902.06850v1 concerns its stated random deformation model; it cannot be substituted for the deterministic triangular gas."),
 "DZ11": ("Demers--Zhang, Spectral analysis of the transfer operator for the Lorentz gas", "A distinct older paper from DZ/DZUniform. Its spaces, twist perturbation and spectral hypotheses have not all been freshly reconstructed."),
 "GouezelRenewal": ("Gouezel, Sharp polynomial estimates for the decay of correlations", "The actual induced operator spaces, renewal hypotheses and tail bounds must be established for the native return map."),
 "HL": ("Herve--Ledoux, A local limit theorem for densities of finite Markov additive processes", "Auxiliary finite-state density theorem only; not a physical-word roof estimate for the deterministic billiard."),
 "HLuniform": ("Herve--Ledoux, Additional material on finite Markov additive processes", "Historical Section 6 uniformity belongs to its stated family of finite Markov additive processes; no automatic radius-uniform billiard transfer."),
 "MN": ("Melbourne--Nicol, Almost sure invariance principle for nonuniformly hyperbolic systems", "ASIP topology does not furnish the microscopic exact-label raw pointwise density or changing conditional event."),
 "SV": ("Szasz--Varju, Local limit theorem for the Lorentz process", "Match observable dimension, lattice subgroup, time, test topology and exact record; a lower-dimensional LLT is not the four-coordinate target."),
 "SYZ": ("Stenlund--Young--Zhang, Dispersing billiards with moving scatterers", "Historical arXiv version 4, Section 3.1; match actual curve class and finite-horizon family, rather than infer all optical pressure bounds."),
 "Villani": ("Villani, Optimal transport: old and new", "Chapters 5--6 provide abstract transport theory, not abundance of the actual same-roof nongrazing comparison pool."),
 "Young": ("Young, Statistical properties of dynamical systems with some hyperbolicity", "Historical ESI 445, Section 8/Theorem 6: native tower, return-tail and regularity assumptions remain necessary."),
}
bywork = defaultdict(list)
for r in bib["records"]:
    if r["classification"] == "external":
        bywork[r["canonical_work_key"]].append(r)
lines = [
 "# Historical bibliography census and theorem-application status",
 "",
 "This is an author-revision audit of the actual preserved source corpus. It is not a new review, a blanket import certificate, or a claim that bibliography metadata proves applicability.",
 "",
 "The census was rerun on the restored current main and all preserved historical TeX/text. It records %d distinct source contents, %d defined bibliography keys, %d cited keys and %d external works. Undefined citation keys: %s." % (bib["distinct_source_contents"], bib["definition_key_count"], bib["cited_key_count"], bib["external_distinct_works"], repr(bib["undefined_citation_keys"])),
 "",
 "There are three fresh primary theorem/object checks: DZ/DZUniform, BDPressure and DN/DNFlow. Boyd--Vandenberghe is background for native proofs. The other 21 historical external works are retained with their exact citation contexts; this iteration does not claim fresh independent reconstruction of all their theorem applications. Thus 22 of 25 works have no full fresh theorem-application certification, including that background item. Even the three direct checks have the narrower scopes stated below.",
 "",
 "The machine-readable census preserves every bibliography-definition variant, citation command, source SHA-256, line locator and surrounding source text. Its aliases identify DZUniform with DZ and DNFlow with DN. The six repository-native keys A2G, Q108, Q109, Q110, Q111 and Q114 are source references, not external works or journal endorsements.",
 "",
 "| Work / source keys | Actual check status | Application boundary |",
 "|---|---|---|",
]
for work, records in sorted(bywork.items()):
    keys = ", ".join(x["key"] for x in records)
    v = records[0]["verification"]
    if work in detail:
        title, boundary = detail[work]
    else:
        title = work
        boundary = v["scope"]
    status = v["status"].replace("_", " ")
    if work in ("DZ", "BDPressure", "DN"):
        status += "; " + v["checked"]
    lines.append("| %s (%s) | %s | %s |" % (title, keys, status, boundary))
lines.extend([
 "", "## The already solved geometric hypotheses remain solved", "",
 "Native modules 281--283 match the actual angular-source curves to the inspected Demers--Zhang short-curve growth hypotheses. Native 287 proves tau_max <= sqrt(3847/124) < 28/5, with the entire ratio under the square root. Native 294 proves a strict all-point/all-direction buffer 179/400 < R_-, excluding all-tangent lines. The stronger finite-horizon geometry in Baladi--Demers is therefore satisfied on the original triangular radius family. This does not prove the pressure gap, identify the exact weighted partition object, or provide all radius-uniform strong/weak operator constants.",
 "", "## Scope of the new elementary proofs", "",
 "Modules 304--309 add native variational, transverse geometric, clock, collar and positive-source proofs. They use no new external theorem. The roof-height conclusions in 306 and 309 explicitly depend on the inherited physical pressure input and original one-copy domination. The complete raw pointwise LLT, original conditioning denominator, singular paired traces, exact arithmetic inversion error, and four-coordinate inversion are not certified by these bibliography checks.",
 "", "## Recovery and locators", "",
 "The portable census script was recovered byte exactly. This status prose was reconstructed after maintenance and does not assert the lost status document's old hash. See LITERATURE_RECHECK_20261018.md for the detailed primary theorem/object checks and HISTORICAL_BIBLIOGRAPHY_CENSUS.json for every actual historical citation context.",
])
(A / "HISTORICAL_BIBLIOGRAPHY_STATUS.md").write_text("\n".join(lines) + "\n")

# The old comparison discovered 66 distinct manuscript/bibliography texts.
# All are now preserved, with original aliases in the source agent's manifest.
variant_manifest = R / "history/historical-manuscript-variants/SOURCE_MANIFEST.json"
variants = json.loads(variant_manifest.read_text())
variant_rows = []
for x in variants["files"]:
    p = R / x["artifact_path"]
    row = ident(p)
    row["original_source_alias_count"] = len(x.get("source_paths", []))
    row["complete_immutable_alias_manifest"] = "history/historical-manuscript-variants/SOURCE_MANIFEST.json"
    row["matches_preserved_manifest"] = row["sha256"] == x["sha256"] and row["git_blob"] == x["git_blob"]
    variant_rows.append(row)
if not all(x["matches_preserved_manifest"] for x in variant_rows):
    raise RuntimeError("A preserved historical manuscript variant changed")
put("HISTORICAL_TEX_NOT_IN_NEW_PACKET.json", {
    "purpose": "Resolved historical manuscript/bibliography omission comparison; every one of the 66 distinct texts is now preserved",
    "recovery": "Reconstructed identity/navigation, not the lost comparison JSON bytes",
    "old_index_identity": OLD.get("audit/HISTORICAL_TEX_NOT_IN_NEW_PACKET.json"),
    "complete_alias_manifest": ident(variant_manifest),
    "formerly_additional_distinct_text_count": 66,
    "current_missing_distinct_text_count": 0,
    "preserved": variant_rows,
})
log_response_path = R / "history/SUMMABLE_FAILED_CI_JOB_LOG_RESPONSE.json"
log_response_path.write_text(json.dumps({
    "scope": "Fresh exact-job log API readback after maintenance, not the former response serialization",
    "old_response_identity": OLD.get("history/SUMMABLE_FAILED_CI_JOB_LOG_RESPONSE.json"),
    "run_id": 39096822675, "job_id": 117584906141,
    "exact_restored_plain_log": ident(R / "history/SUMMABLE_FAILED_CI_JOB.log"),
    "response": json.loads((A / "recovery/SUMMABLE_FAILED_CI_LOG_READBACK.json").read_text()),
}, ensure_ascii=False, indent=2) + "\n")

# The retained reports themselves are exact; regenerated metadata is separately identified.
owned_old = [x for x in INV["files"] if x["path"].startswith("audit/") or
             x["path"] in ("history/HISTORICAL_CI_ACTUAL_READBACK.json",
                           "history/SUMMABLE_FAILED_CI_JOB.log",
                           "history/SUMMABLE_FAILED_CI_JOBS.json",
                           "history/SUMMABLE_FAILED_CI_JOB_LOG_RESPONSE.json",
                           "ci/a2-dyn-global-minimizer-localization-20261018.yml")]
recovered = []
for x in owned_old:
    p = R / x["path"]
    n = {"path": x["path"], "old_identity": x}
    if x["path"] == "audit/REVIEW_AUDIT_DELIVERY.json":
        n["status"] = "reconstructed_receipt; self-referential current hash omitted; outer source manifest authoritative"
    elif not p.is_file():
        n["status"] = "old_serialization_not_recovered; no byte-identity or old execution claim"
    else:
        cur = ident(p)
        n["current_identity"] = cur
        n["status"] = "exact_pre_maintenance_bytes" if cur["sha256"] == x["sha256"] else "reconstructed_or_fresh_readback; not_old_bytes"
    recovered.append(n)
put("recovery/AUDIT_RECOVERY_STATUS.json", {
    "purpose": "Explicit old/current byte identity for this agent's audit, review and CI metadata outputs",
    "pre_maintenance_inventory": ident(INV_PATH),
    "scope": "Old execution evidence is claimed preserved only when actual bytes match the original SHA-256. Fresh runs and reread remote metadata have separate identities.",
    "counts": dict(Counter(x["status"] for x in recovered)),
    "all_1178_known_remote_placements_and_699_blobs_verified": "audit/recovery/KNOWN_GIT_BLOB_RESTORE.json",
    "all_90_original_report_plaintexts_byte_exact": True,
    "files": recovered,
})
put("REVIEW_AUDIT_DELIVERY.json", {
    "purpose": "Current author-side audit delivery after maintenance; not a journal review or theorem certification",
    "pre_maintenance_delivery_receipt": OLD.get("audit/REVIEW_AUDIT_DELIVERY.json"),
    "old_receipt_byte_identity_claimed": False,
    "report_count": len(reports), "branch_count": len(branches), "a2_dyn_ref_count": len(dyn),
    "source_review_counts": {"author_refs": 242, "author_commits": author["count"], "article_trees": articles["article_tree_count"], "numbered_variants": articles["numbered_blob_union_count"]},
    "bibliography_counts": {k: bib[k] for k in ("distinct_source_contents", "definition_key_count", "cited_key_count", "external_distinct_works", "undefined_citation_keys", "fresh_primary_work_keys")},
    "current_new_native_source_identities": [ident(p) for p in sorted((R/"core").glob("30[4-9]_*.tex"))],
    "remote_publication_scope": "Use separate exact-head root publication readback; this receipt asserts local audit bytes only.",
    "files": [ident(p) for p in sorted(A.rglob("*")) if p.is_file() and p.name != "REVIEW_AUDIT_DELIVERY.json" and "__pycache__" not in p.parts],
})
print(json.dumps({"refs": len(dyn), "reports": len(reports), "bibliography_works": len(bywork),
                  "audit_recovery_counts": dict(Counter(x["status"] for x in recovered))}, indent=2))
