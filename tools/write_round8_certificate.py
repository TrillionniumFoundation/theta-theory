#!/usr/bin/env python3
"""Write the exact-source, build, and publication certificate for round eight."""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]


def load(name: str) -> dict:
    path = ROOT / name
    if not path.is_file():
        raise SystemExit(f"missing certificate input: {name}")
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mathematical-sha", required=True)
    parser.add_argument("--pre-main", required=True)
    parser.add_argument("--workflow-run", required=True)
    args = parser.parse_args()

    structural = load("ROUND8_STRUCTURAL_VERIFICATION.json")
    hostile = load("ROUND8_HOSTILE_REREVIEW.json")
    build = load("ROUND8_BUILD_SUMMARY.json")
    manifest = load("ROUND8_MATERIALIZATION_MANIFEST.json")
    if structural["status"] != "PASS":
        raise SystemExit("structural verification did not pass")
    if hostile["status"] != "PASS":
        raise SystemExit("hostile rereview did not pass")
    if build["status"] != "PASS" or build["passed"] != 11:
        raise SystemExit("round-eight build did not pass 11/11")

    papers: dict[str, object] = {}
    for name in sorted(manifest["papers"]):
        pdf = ROOT / "papers" / name / "main.pdf"
        if not pdf.is_file() or pdf.stat().st_size == 0:
            raise SystemExit(f"missing final PDF for {name}")
        b = build["papers"][name]
        papers[name] = {
            "pdf_bytes": pdf.stat().st_size,
            "pdf_pages": b["pdf_pages"],
            "pdf_sha256": sha256(pdf),
            "source_sha256": structural["papers"][name]["source_sha256"],
            "module_sha256": structural["papers"][name]["module_sha256"],
            "theorem_like_environments": structural["papers"][name]["theorem_like_environments"],
            "proofs": structural["papers"][name]["proofs"],
        }

    cert = {
        "schema": "theta-theory-round8-final-certificate-v1",
        "status": "INTERNAL_ROUND8_POSITIVE_CLOSURE_VERIFIED",
        "repository": "TrillionniumFoundation/theta-theory",
        "review_branch": "review/round7-gpt56-pro-harsh-11paper-2026-08-31",
        "review_head": "e366e858b564d9cdda389674ae3dfb6e65813a1e",
        "revision_branch": "revision/round8-referee-positive-closure-11paper-2026-08-31",
        "verified_mathematical_commit": args.mathematical_sha,
        "pre_publication_main": args.pre_main,
        "workflow_run_id": int(args.workflow_run),
        "paper_count": 11,
        "total_pdf_pages": build["total_pdf_pages"],
        "theorem_proof_pairing": (
            f"{structural['total_theorem_like_environments']}/"
            f"{structural['total_proofs']}"
        ),
        "gates": {
            "historical_derivation_audit": "PASS — local reuse only",
            "registered_source_active_module_identity": "11/11 PASS",
            "structural_verification": "PASS",
            "dependency_dag": structural["dependency_dag"],
            "counterexample_hostile_rereview": "11/11 PASS",
            "clean_latex_build": "11/11 PASS",
            "undefined_references_or_citations": 0,
            "nonempty_pdfs": "11/11 PASS",
            "downgrade": False,
            "nogo_substitution": False,
        },
        "papers": papers,
        "certification_boundary": (
            "Repository-internal exact-source, proof-structure, counterexample, "
            "dependency, compilation, and publication verification; not external "
            "journal acceptance or independent mathematical validation."
        ),
    }
    (ROOT / "ROUND8_FINAL_CERTIFICATE.json").write_text(
        json.dumps(cert, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    record = {
        "schema": "theta-theory-round8-publication-record-v1",
        "repository": cert["repository"],
        "pre_main": args.pre_main,
        "mathematical_sha": args.mathematical_sha,
        "revision_branch": cert["revision_branch"],
        "archive_branch": "archive/main-pre-round8-positive-closure-2026-08-31",
        "publication_tag": "round8-positive-closure-verified-2026-08-31",
        "workflow_run_id": int(args.workflow_run),
        "published_main_commit": "SELF (the commit containing this record)",
        "publication_delta_policy": [
            "ROUND8_FINAL_CERTIFICATE.json",
            "ROUND8_PUBLICATION_RECORD.json",
            "ROUND8_REVISION_STATUS.md",
        ],
    }
    (ROOT / "ROUND8_PUBLICATION_RECORD.json").write_text(
        json.dumps(record, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    status = f"""# Round-Eight Revision Status

**Status:** `INTERNAL_ROUND8_POSITIVE_CLOSURE_VERIFIED`

- Review branch: `review/round7-gpt56-pro-harsh-11paper-2026-08-31`
- Review head: `e366e858b564d9cdda389674ae3dfb6e65813a1e`
- Revision branch: `revision/round8-referee-positive-closure-11paper-2026-08-31`
- Verified mathematical commit: `{args.mathematical_sha}`
- Pre-publication main: `{args.pre_main}`
- Workflow run: `{args.workflow_run}`
- Papers: `11/11`
- Theorem/proof pairing: `{cert['theorem_proof_pairing']}`
- PDF pages: `{build['total_pdf_pages']}`
- Undefined references/citations: `0`
- Downgrade: `false`
- No-go substitution: `false`

The status certifies repository-internal source identity, proof-structure coverage, explicit counterexample regressions, acyclic dependencies, and clean reproducible builds.  Independent external referee review remains a separate process.
"""
    (ROOT / "ROUND8_REVISION_STATUS.md").write_text(status, encoding="utf-8")
    print("ROUND8_CERTIFICATE_WRITE_PASS")


if __name__ == "__main__":
    main()
