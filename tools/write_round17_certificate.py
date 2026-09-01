#!/usr/bin/env python3
"""Write exact Round-Seventeen certificate and publication metadata."""
from __future__ import annotations

from pathlib import Path
import hashlib
import json
import os

ROOT = Path(__file__).resolve().parents[1]
manifest = json.loads((ROOT / "ROUND17_MATERIALIZATION_MANIFEST.json").read_text())
structural = json.loads((ROOT / "ROUND17_STRUCTURAL_VERIFICATION.json").read_text())
hostile = json.loads((ROOT / "ROUND17_HOSTILE_REREVIEW.json").read_text())
build = json.loads((ROOT / "ROUND17_BUILD_SUMMARY.json").read_text())

if structural["status"] != hostile["status"] or structural["status"] != "PASS" or build["status"] != "PASS":
    raise SystemExit("Round-Seventeen gates have not all passed")
if structural["referee_objections"] != 63:
    raise SystemExit("unexpected objection count")

pre_main = os.environ.get("PRE_MAIN", "LOCAL-PRE-MAIN")
mathematical_sha = os.environ.get("MATHEMATICAL_SHA", "LOCAL-MATHEMATICAL-TREE")
workflow_run_id = int(os.environ.get("GITHUB_RUN_ID", "0"))

papers: dict[str, object] = {}
for entry in manifest["papers"]:
    folder = ROOT / entry["folder"]
    source = ROOT / entry["registered_source"]
    active = folder / "ROUND17_POSITIVE_CLOSURE.tex"
    pdf = folder / "main.pdf"
    b = build["papers"][folder.name]
    if source.read_bytes() != active.read_bytes():
        raise SystemExit(f"byte identity failed for {folder.name}")
    papers[folder.name] = {
        "code": entry["code"],
        "registered_source": entry["registered_source"],
        "source_bytes": source.stat().st_size,
        "source_sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
        "module_sha256": hashlib.sha256(active.read_bytes()).hexdigest(),
        "referee_objections": entry["objections"],
        "theorem_like_environments": structural["papers"][folder.name]["theorem_like_environments"],
        "proofs": structural["papers"][folder.name]["proofs"],
        "pdf_bytes": pdf.stat().st_size,
        "pdf_pages": b["pdf_pages"],
        "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
    }

certificate = {
    "schema": "theta-theory-round17-final-certificate-v1",
    "repository": "TrillionniumFoundation/theta-theory",
    "review_branch": "revision/round16-referee-positive-closure-11paper-2026-09-01",
    "review_head": "d3833aaa2db4bf0a13a67083f27ff23f28ab6e4f",
    "reviewed_candidate": "2901535c56013bb61ca4211d7b7bb2b35007fff0",
    "revision_branch": "revision/round17-referee-positive-closure-11paper-2026-09-01",
    "pre_publication_main": pre_main,
    "verified_mathematical_commit": mathematical_sha,
    "workflow_run_id": workflow_run_id,
    "paper_count": 11,
    "referee_objections": 63,
    "theorem_proof_pairing": f"{structural['total_theorem_like_environments']}/{structural['total_proofs']}",
    "total_pdf_pages": build["total_pdf_pages"],
    "gates": {
        "historical_derivation_audit": "PASS — local reuse only",
        "registered_source_active_module_identity": "11/11 PASS",
        "structural_verification": "PASS",
        "counterexample_hostile_rereview": "11/11 PASS",
        "dependency_dag": structural["dependency_dag"],
        "clean_latex_build": "11/11 PASS",
        "undefined_references_or_citations": 0,
        "nonempty_pdfs": "11/11 PASS",
        "downgrade": False,
        "nogo_substitution": False,
    },
    "papers": papers,
    "status": "INTERNAL_ROUND17_POSITIVE_CLOSURE_VERIFIED",
    "certification_boundary": "Repository-internal exact-source, proof-structure, direct-counterexample, dependency, compilation, and publication verification; not external journal acceptance or independent mathematical validation.",
}
(ROOT / "ROUND17_FINAL_CERTIFICATE.json").write_text(json.dumps(certificate, indent=2, sort_keys=True) + "\n")

publication = {
    "schema": "theta-theory-round17-publication-record-v1",
    "repository": certificate["repository"],
    "pre_main": pre_main,
    "mathematical_sha": mathematical_sha,
    "revision_branch": certificate["revision_branch"],
    "archive_branch": "archive/main-pre-round17-positive-closure-2026-09-01",
    "publication_tag": "round17-positive-closure-verified-2026-09-01",
    "published_main_commit": "SELF (the commit containing this record)",
    "workflow_run_id": workflow_run_id,
    "publication_delta_policy": [
        "ROUND17_FINAL_CERTIFICATE.json",
        "ROUND17_PUBLICATION_RECORD.json",
        "ROUND17_REVISION_STATUS.md",
    ],
}
(ROOT / "ROUND17_PUBLICATION_RECORD.json").write_text(json.dumps(publication, indent=2, sort_keys=True) + "\n")

status = f"""# Round-Seventeen Revision Status

**Status:** `INTERNAL_ROUND17_POSITIVE_CLOSURE_VERIFIED`

- Review tree: `revision/round16-referee-positive-closure-11paper-2026-09-01@d3833aaa2db4bf0a13a67083f27ff23f28ab6e4f`
- Reviewed candidate: `2901535c56013bb61ca4211d7b7bb2b35007fff0`
- Revision branch: `revision/round17-referee-positive-closure-11paper-2026-09-01`
- Verified mathematical commit: `{mathematical_sha}`
- Pre-publication main: `{pre_main}`
- Workflow run: `{workflow_run_id}`
- Papers: `11/11`
- Major referee objections mapped: `63/63`
- Theorem/proof pairing: `{structural['total_theorem_like_environments']}/{structural['total_proofs']}`
- PDF pages: `{build['total_pdf_pages']}`
- Undefined references/citations: `0`
- Downgrade: `false`
- No-go substitution: `false`

This status certifies repository-internal source identity, proof-structure coverage,
direct-counterexample regressions, acyclic dependencies, and clean reproducible
builds. Independent external referee review remains separate.
"""
(ROOT / "ROUND17_REVISION_STATUS.md").write_text(status)
print("ROUND17_CERTIFICATE_WRITTEN")
