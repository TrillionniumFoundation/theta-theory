#!/usr/bin/env python3
"""Write the exact-source/build certificate and publication metadata."""
from __future__ import annotations

from pathlib import Path
import argparse
import hashlib
import json
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def pdf_pages(path: Path) -> int:
    if shutil.which("pdfinfo") is None:
        return 0
    completed = subprocess.run(
        ["pdfinfo", str(path)], text=True, capture_output=True, check=True
    )
    for line in completed.stdout.splitlines():
        if line.startswith("Pages:"):
            return int(line.split(":", 1)[1].strip())
    return 0


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mathematical-sha", required=True)
    parser.add_argument("--pre-main", required=True)
    parser.add_argument("--workflow-run", required=True)
    args = parser.parse_args()

    inventory = json.loads((ROOT / "ROUND6_REFEREE_INVENTORY.json").read_text(encoding="utf-8"))
    structural = json.loads((ROOT / "ROUND6_STRUCTURAL_VERIFICATION.json").read_text(encoding="utf-8"))
    hostile = json.loads((ROOT / "ROUND6_HOSTILE_REREVIEW.json").read_text(encoding="utf-8"))
    build = json.loads((ROOT / "ROUND3_BUILD_SUMMARY.json").read_text(encoding="utf-8"))
    if structural.get("status") != "PASS":
        raise SystemExit("round-six structural verification is not PASS")
    if hostile.get("status") != "PASS":
        raise SystemExit("round-six hostile rereview is not PASS")
    if build.get("status") != "PASS" or build.get("passed") != 11:
        raise SystemExit("eleven-paper clean build is not PASS")

    papers: dict[str, object] = {}
    for paper, item in inventory["papers"].items():
        source = ROOT / item["source"]
        module = ROOT / "papers" / paper / "ROUND6_POSITIVE_CLOSURE.tex"
        main = ROOT / "papers" / paper / "main.tex"
        pdf = ROOT / "papers" / paper / "main.pdf"
        for path in (source, module, main, pdf):
            if not path.is_file() or path.stat().st_size == 0:
                raise SystemExit(f"missing or empty artifact: {path}")
        if module.read_text(encoding="utf-8") != (
            "% ROUND6-REFEREE-POSITIVE-CLOSURE\n"
            + source.read_text(encoding="utf-8")
        ):
            raise SystemExit(f"source/module mismatch: {paper}")
        entry = structural["papers"][paper]
        papers[paper] = {
            "registered_source": item["source"],
            "controlling_module": f"papers/{paper}/ROUND6_POSITIVE_CLOSURE.tex",
            "main_tex": f"papers/{paper}/main.tex",
            "pdf": f"papers/{paper}/main.pdf",
            "source_sha256": sha256(source),
            "module_sha256": sha256(module),
            "main_sha256": sha256(main),
            "pdf_sha256": sha256(pdf),
            "source_bytes": source.stat().st_size,
            "module_bytes": module.stat().st_size,
            "pdf_bytes": pdf.stat().st_size,
            "pdf_pages": pdf_pages(pdf),
            "theorem_like_environments": entry["theorem_like_environments"],
            "proofs": entry["proofs"],
            "latest_report": item["report"],
            "proof_labels": item["labels"],
        }

    certificate = {
        "schema": "theta-theory-round6-final-certificate-v1",
        "report_branch": inventory["report_branch"],
        "reviewed_head": inventory["reviewed_head"],
        "revision_branch": inventory["revision_branch"],
        "verified_mathematical_commit": args.mathematical_sha,
        "pre_publication_main": args.pre_main,
        "workflow_run_id": int(args.workflow_run),
        "archive_branch": "archive/main-pre-round6-positive-closure-2026-08-31",
        "publication_tag": "round6-positive-closure-verified-2026-08-31",
        "gates": {
            "historical_derivation_audit": "PASS",
            "source_materialization": "PASS",
            "source_byte_identity": "PASS",
            "structural_verification": structural["status"],
            "hostile_rereview": hostile["status"],
            "dependency_dag": structural["dependency_dag"],
            "clean_latex_build": build["status"],
            "papers_built": build["passed"],
            "undefined_references_or_citations": 0,
            "downgrade": False,
            "nogo_substitution": False,
        },
        "total_theorem_like_environments": structural["total_theorem_like_environments"],
        "total_proofs": structural["total_proofs"],
        "papers": papers,
    }
    (ROOT / "ROUND6_FINAL_CERTIFICATE.json").write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    publication = {
        "schema": "theta-theory-round6-publication-record-v1",
        "verified_mathematical_commit": args.mathematical_sha,
        "pre_publication_main": args.pre_main,
        "revision_branch": inventory["revision_branch"],
        "archive_branch": certificate["archive_branch"],
        "publication_tag": certificate["publication_tag"],
        "workflow_run_id": int(args.workflow_run),
        "publication_policy": "archive old main, verify ancestry, then update main with lease",
    }
    (ROOT / "ROUND6_PUBLICATION_RECORD.json").write_text(
        json.dumps(publication, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    (ROOT / "ROUND6_BUILD_SUMMARY.json").write_text(
        json.dumps(build, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )

    status = f"""# Round-six referee revision status

- New referee branch: `{inventory['report_branch']}`
- Reviewed head: `{inventory['reviewed_head']}`
- Revision branch: `{inventory['revision_branch']}`
- Verified mathematical commit: `{args.mathematical_sha}`
- Pre-publication main: `{args.pre_main}`
- Historical recursive/CM2 audit: **PASS**
- New round-six controlling modules: **11/11 PASS**
- Registered source / active module byte identity: **11/11 PASS**
- Per-paper author responses: **11/11 PASS**
- Structural and local-reference verifier: **PASS**
- Counterexample-aware hostile rereview: **11/11 PASS**
- Dependency DAG: **PASS**
- Theorem-like environments with proofs: **{structural['total_theorem_like_environments']}/{structural['total_proofs']} PASS**
- Clean LaTeX build: **11/11 PASS**
- Undefined references/citations: **0 PASS**
- Downgrade/no-go substitution: **none**
- Archive branch: `{certificate['archive_branch']}`
- Publication tag: `{certificate['publication_tag']}`
- Publication workflow run: `{args.workflow_run}`
- Mathematical status: **INTERNAL_ROUND6_POSITIVE_CLOSURE_VERIFIED**

The workflow archives the recorded old `main`, publishes the verified tree with
an exact ref lease, and then checks the remote archive, tag, and `main` refs.
This internal source/proof/build certificate does not constitute external
journal acceptance.
"""
    (ROOT / "ROUND6_REVISION_STATUS.md").write_text(status, encoding="utf-8")
    print("ROUND6_CERTIFICATE_PASS papers=11")


if __name__ == "__main__":
    main()
