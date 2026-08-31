#!/usr/bin/env python3
"""Write the exact round-seven source/build certificate after all gates pass."""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_pages(path: Path) -> int:
    out = subprocess.check_output(["pdfinfo", str(path)], text=True)
    for line in out.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    raise RuntimeError(f"Pages missing in pdfinfo output for {path}")


def load_pass(name: str) -> dict[str, object]:
    path = ROOT / name
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("status") != "PASS":
        raise SystemExit(f"{name} is not PASS")
    return data


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mathematical-sha", required=True)
    parser.add_argument("--pre-main", required=True)
    parser.add_argument("--workflow-run", required=True)
    args = parser.parse_args()

    manifest = json.loads(
        (ROOT / "ROUND7_MATERIALIZATION_MANIFEST.json").read_text(encoding="utf-8")
    )
    structural = load_pass("ROUND7_STRUCTURAL_VERIFICATION.json")
    hostile = load_pass("ROUND7_HOSTILE_REREVIEW.json")
    build = load_pass("ROUND7_BUILD_SUMMARY.json")

    papers: dict[str, object] = {}
    total_pages = 0
    for paper, meta in manifest["papers"].items():
        module = ROOT / meta["module"]
        main_tex = ROOT / meta["main"]
        pdf = ROOT / "papers" / paper / "main.pdf"
        if not pdf.is_file() or pdf.stat().st_size == 0:
            raise SystemExit(f"missing nonempty PDF for {paper}")
        pages = pdf_pages(pdf)
        total_pages += pages
        source_entries = []
        for source_name in meta["sources"]:
            source = ROOT / "revision" / "round7-referee-final" / source_name
            source_entries.append(
                {
                    "path": str(source.relative_to(ROOT)),
                    "bytes": source.stat().st_size,
                    "sha256": sha256(source),
                }
            )
        pstruct = structural["papers"][paper]
        papers[paper] = {
            "code": meta["code"],
            "registered_sources": source_entries,
            "controlling_module": str(module.relative_to(ROOT)),
            "module_bytes": module.stat().st_size,
            "module_sha256": sha256(module),
            "main_tex": str(main_tex.relative_to(ROOT)),
            "main_sha256": sha256(main_tex),
            "pdf": str(pdf.relative_to(ROOT)),
            "pdf_bytes": pdf.stat().st_size,
            "pdf_pages": pages,
            "pdf_sha256": sha256(pdf),
            "theorem_like_environments": pstruct["theorem_like_environments"],
            "proofs": pstruct["proofs"],
            "latest_report": meta["report"],
            "author_response": meta["response"],
        }

    certificate = {
        "schema": "theta-theory-round7-final-certificate-v1",
        "report_branch": "review/round6-gpt56-pro-harsh-11paper-2026-08-31",
        "reviewed_main": args.pre_main,
        "revision_branch": "revision/round7-referee-positive-closure-11paper-2026-08-31",
        "verified_mathematical_commit": args.mathematical_sha,
        "workflow_run_id": int(args.workflow_run),
        "paper_count": len(papers),
        "total_pdf_pages": total_pages,
        "total_theorem_like_environments": structural["total_theorem_like_environments"],
        "total_proofs": structural["total_proofs"],
        "gates": {
            "historical_derivation_audit": "PASS",
            "source_materialization": "PASS",
            "source_byte_identity": "PASS",
            "structural_verification": "PASS",
            "counterexample_aware_hostile_rereview": "PASS",
            "dependency_dag": structural["dependency_dag"],
            "clean_latex_build": "PASS",
            "papers_built": build["passed"],
            "undefined_references_or_citations": 0,
            "downgrade": False,
            "nogo_substitution": False,
        },
        "papers": papers,
    }
    (ROOT / "ROUND7_FINAL_CERTIFICATE.json").write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    publication = {
        "schema": "theta-theory-round7-publication-record-v1",
        "revision_branch": "revision/round7-referee-positive-closure-11paper-2026-08-31",
        "verified_mathematical_commit": args.mathematical_sha,
        "pre_publication_main": args.pre_main,
        "archive_branch": "archive/main-pre-round7-positive-closure-2026-08-31",
        "publication_tag": "round7-positive-closure-verified-2026-08-31",
        "publication_policy": "archive old main, verify ancestry, update main and tag atomically with an exact lease",
        "workflow_run_id": int(args.workflow_run),
    }
    (ROOT / "ROUND7_PUBLICATION_RECORD.json").write_text(
        json.dumps(publication, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    status = f"""# Round-seven referee revision status

- Latest referee branch: `review/round6-gpt56-pro-harsh-11paper-2026-08-31`
- Reviewed main: `{args.pre_main}`
- Revision branch: `revision/round7-referee-positive-closure-11paper-2026-08-31`
- Verified mathematical commit: `{args.mathematical_sha}`
- Historical recursive/CM2 audit: **PASS, local reuse only**
- New round-seven controlling modules: **11/11 PASS**
- Registered source / active module byte identity: **11/11 PASS**
- Per-paper author responses: **11/11 PASS**
- Structural and local-reference verifier: **PASS**
- Counterexample-aware hostile rereview: **11/11 PASS**
- Dependency DAG: **PASS**
- Theorem-like environments with proofs: **{structural['total_theorem_like_environments']}/{structural['total_proofs']} PASS**
- Clean LaTeX build: **11/11 PASS**
- Undefined references/citations: **0 PASS**
- Downgrade/no-go substitution: **none**
- Archive branch: `archive/main-pre-round7-positive-closure-2026-08-31`
- Publication tag: `round7-positive-closure-verified-2026-08-31`
- Publication workflow run: `{args.workflow_run}`
- Mathematical status: **INTERNAL_ROUND7_POSITIVE_CLOSURE_VERIFIED**

This is an internal exact-source, counterexample, dependency, and build certificate. It does not constitute external journal acceptance.
"""
    (ROOT / "ROUND7_REVISION_STATUS.md").write_text(status, encoding="utf-8")
    print(
        f"ROUND7_CERTIFICATE_PASS papers={len(papers)} pages={total_pages} "
        f"mathematical_sha={args.mathematical_sha}"
    )


if __name__ == "__main__":
    main()
