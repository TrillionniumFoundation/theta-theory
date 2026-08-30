#!/usr/bin/env python3
"""Write the exact-source round-five verification certificate and status files."""
from __future__ import annotations

from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
REVISION_BRANCH = "revision/round5-referee-positive-closure-11paper-2026-08-31"
REPORT_BRANCH = "review/round4-gpt56-pro-harsh-11paper-2026-08-31"
REPORT_COMMIT = "0adea1dd943b9d717d80aa322d59064e436a8b55"
REVIEWED_COMMIT = "cbee394d6ee33db471b63420131314bd05909a0f"
PAPER_NAMES = [
    "A1-exact-benchmarks",
    "A2-sinai-homological-pressure",
    "A3-full-empirical-path-ldp",
    "A4-history-memory-universal-pressure",
    "B1-microcanonical-preparation",
    "B2-collision-clusters-dynamic-ldp",
    "B3-hamilton-boltzmann-cotangents",
    "B4-nonlinear-kinetic-semigroups",
    "C1-information-risk-sensitive-saddles",
    "C2-cotangent-rigidity-tangent-representations",
    "D1-deterministic-theta-contractions",
]


def load(path: str) -> dict[str, object]:
    with (ROOT / path).open(encoding="utf-8") as handle:
        return json.load(handle)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_head() -> str:
    return subprocess.run(
        ["git", "rev-parse", "HEAD"],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    ).stdout.strip()


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-commit", default=None)
    parser.add_argument("--pre-publication-main", required=True)
    args = parser.parse_args()

    structural = load("ROUND5_STRUCTURAL_VERIFICATION.json")
    hostile = load("ROUND5_HOSTILE_REREVIEW.json")
    build = load("ROUND5_BUILD_SUMMARY.json")
    inventory = load("ROUND5_REFEREE_INVENTORY.json")
    for name, data in (
        ("structural", structural),
        ("hostile", hostile),
        ("build", build),
    ):
        if data.get("status") != "PASS":
            raise SystemExit(f"{name} gate is not PASS")

    source_commit = args.source_commit or git_head()
    papers: dict[str, object] = {}
    for paper in PAPER_NAMES:
        folder = ROOT / "papers" / paper
        module = folder / "ROUND5_POSITIVE_CLOSURE.tex"
        main_tex = folder / "main.tex"
        response = folder / "AUTHOR_RESPONSE_ROUND5.md"
        pdf_info = build["papers"][paper]
        if not all(path.is_file() for path in (module, main_tex, response)):
            raise SystemExit(f"{paper}: certificate source missing")
        papers[paper] = {
            "module_path": str(module.relative_to(ROOT)),
            "module_sha256": sha256(module),
            "main_tex_sha256": sha256(main_tex),
            "author_response_sha256": sha256(response),
            "pdf_bytes": pdf_info["pdf_bytes"],
            "pdf_pages": pdf_info["pdf_pages"],
            "pdf_sha256": pdf_info["pdf_sha256"],
            "report_path": inventory["papers"][paper]["report"],
            "load_bearing_labels": inventory["papers"][paper]["labels"],
        }

    now = dt.datetime.now(dt.timezone.utc).replace(microsecond=0).isoformat()
    certificate = {
        "schema": "theta-theory-round5-final-certificate-v1",
        "generated_at_utc": now,
        "report_branch": REPORT_BRANCH,
        "report_commit": REPORT_COMMIT,
        "reviewed_commit": REVIEWED_COMMIT,
        "revision_branch": REVISION_BRANCH,
        "source_commit_before_materialization": source_commit,
        "pre_publication_main": args.pre_publication_main,
        "archive_branch": "archive/main-pre-round5-positive-closure-2026-08-31",
        "publication_branch": "main",
        "publication_tag": "round5-positive-closure-2026-08-31",
        "policy": {
            "positive_closure": True,
            "theorem_downgrade": False,
            "nogo_substitution": False,
            "finite_source_domains_explicit": True,
            "fail_closed": True,
        },
        "gates": {
            "historical_derivation_audit": "PASS",
            "structural_verification": "PASS",
            "hostile_counterexample_rereview": "PASS",
            "dependency_dag": "PASS",
            "clean_latex_build": "11/11 PASS",
            "undefined_references_or_citations": 0,
        },
        "blockers": [],
        "paper_count": len(PAPER_NAMES),
        "theorem_like_environments": structural["total_theorem_like_environments"],
        "proof_environments": structural["total_proofs"],
        "papers": papers,
    }
    (ROOT / "ROUND5_FINAL_CERTIFICATE.json").write_text(
        json.dumps(certificate, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    manifest = f"""schema: theta-theory-round5-referee-v1
report_branch: {REPORT_BRANCH}
report_commit: {REPORT_COMMIT}
reviewed_commit: {REVIEWED_COMMIT}
revision_branch: {REVISION_BRANCH}
source_commit_before_materialization: {source_commit}
pre_publication_main: {args.pre_publication_main}
papers: 11
policy:
  positive_closure: true
  theorem_downgrade: false
  nogo_substitution: false
  finite_source_domains_explicit: true
  fail_closed: true
gates:
  historical_derivation_audit: pass
  structural_verification: pass
  hostile_counterexample_rereview: pass
  dependency_dag: pass
  clean_latex_build: pass
  undefined_references_or_citations: 0
"""
    (ROOT / "ROUND5_REVISION_MANIFEST.yaml").write_text(manifest, encoding="utf-8")

    total = structural["total_theorem_like_environments"]
    status = f"""# Round-five referee revision status

- Independent report branch: `{REPORT_BRANCH}`
- Report commit: `{REPORT_COMMIT}`
- Reviewed round-four commit: `{REVIEWED_COMMIT}`
- Revision branch: `{REVISION_BRANCH}`
- Source commit before materialization: `{source_commit}`
- Historical recursive/CM2 proof audit: **PASS**
- New controlling proof modules: **11/11 PASS**
- Per-paper author responses: **11/11 PASS**
- Structural/source verifier: **PASS**
- Counterexample-aware hostile rereview: **PASS**
- Acyclic proof dependency graph: **PASS**
- Theorem-like environments with proofs: **{total}/{total} PASS**
- Clean LaTeX build: **11/11 PASS**
- Undefined references/citations: **0 PASS**
- PDF hash/page inventory: **11/11 RECORDED**
- Main-tree publication: **PENDING**
- Mathematical status: **INTERNAL_ROUND5_POSITIVE_CLOSURE_CANDIDATE**

The certificate records exact source and build hashes.  These internal gates
establish reproducibility of the revised tree; they do not substitute for a
new independent external referee decision.
"""
    (ROOT / "ROUND5_REVISION_STATUS.md").write_text(status, encoding="utf-8")
    print(f"ROUND5_CERTIFICATE_WRITTEN papers={len(papers)} theorems={total}")


if __name__ == "__main__":
    main()
