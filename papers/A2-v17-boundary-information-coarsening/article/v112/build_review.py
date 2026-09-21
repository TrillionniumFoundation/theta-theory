#!/usr/bin/env python3
"""Build the review package and write an execution receipt only after success."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

BASE = "cafc6c1bd403dae4acc66177fb43feee54c02b1d"
ROOT = Path(__file__).resolve().parent

def run(args, cwd=ROOT):
    result = subprocess.run(args, cwd=cwd, text=True, stdout=subprocess.PIPE,
                            stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        sys.stderr.write(result.stdout)
        raise subprocess.CalledProcessError(result.returncode, args, output=result.stdout)
    return result.stdout

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect(pdf, log):
    text = log.read_text(errors="replace")
    warnings = {"undefined": len(re.findall(r"(?:Reference|Citation).*undefined|There were undefined", text)),
                "multiply_defined": text.count("multiply defined"),
                "overfull": text.count("Overfull")}
    info = run(["pdfinfo", str(pdf)])
    return {"pdf_sha256": digest(pdf), "log_sha256": digest(log),
            "pages": int(re.search(r"Pages:\s+(\d+)", info).group(1)),
            "warnings": warnings}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--local", action="store_true",
                        help="Principal only; does not claim Git-bound preservation or companion execution.")
    args = parser.parse_args()
    evidence = ROOT / "evidence"
    evidence.mkdir(exist_ok=True)
    repo = None if args.local else ROOT.parents[3]
    check_args = [sys.executable, str(ROOT / "verify_revision.py"), "--out", str(evidence / "diagnostics.json")]
    source_commit = None
    if repo:
        source_commit = run(["git", "rev-parse", "HEAD"], repo).strip()
        expected = os.environ.get("GITHUB_SHA")
        if expected and expected != source_commit:
            raise RuntimeError("Checkout does not match triggering source commit")
        check_args += ["--repository", str(repo)]
    (evidence / "diagnostics.stdout").write_text(run(check_args))
    command = ["latexmk", "-g", "-pdf", "-interaction=nonstopmode", "-halt-on-error", "-file-line-error", "paper.tex"]
    (evidence / "latexmk.stdout").write_text(run(command))
    principal = inspect(ROOT / "paper.pdf", ROOT / "paper.log")
    if any(principal["warnings"].values()):
        raise RuntimeError("Principal LaTeX warning audit failed: " + str(principal["warnings"]))
    companions = {}
    if repo:
        paper_root = ROOT.parent.parent
        for version in ("v111", "v110", "v109", "v108"):
            out = repo / "build-v112" / version
            out.mkdir(parents=True, exist_ok=True)
            command = ["latexmk", "-g", "-pdf", "-interaction=nonstopmode", "-halt-on-error",
                       "-file-line-error", "-outdir=" + str(out)]
            if version == "v111":
                command += ["paper.tex"]
                companion_cwd = paper_root / "article" / version
            else:
                command += ["article/" + version + "/paper.tex"]
                companion_cwd = paper_root
            (out / "latexmk.stdout").write_text(run(command, companion_cwd))
            companions[version] = inspect(out / "paper.pdf", out / "paper.log")
    sources = {str(p.relative_to(ROOT)): digest(p) for p in sorted(ROOT.rglob("*.tex"))}
    scripts = {name: digest(ROOT / name) for name in ("verify_revision.py", "build_review.py")}
    run_id = os.environ.get("GITHUB_RUN_ID")
    receipt = {"status": "passed", "source_bound": not args.local,
               "scope": "principal-only local" if args.local else "exact-source five-volume review",
               "source_commit": source_commit, "controlling_review_commit": BASE,
               "run_url": "https://github.com/TrillionniumFoundation/theta-theory/actions/runs/" + run_id if run_id else None,
               "principal": principal, "companions": companions,
               "tex_sha256": sources, "scripts_sha256": scripts,
               "diagnostics_sha256": digest(evidence / "diagnostics.json"),
               "pdflatex": run(["pdflatex", "--version"]).splitlines()[0],
               "latexmk": run(["latexmk", "-v"]).strip(),
               "python": sys.version,
               "limitation": "Build integrity and finite diagnostics are not formal proof checking or journal assessment."}
    name = "local-receipt.json" if args.local else "ci-receipt.json"
    (evidence / name).write_text(json.dumps(receipt, indent=2) + "\n")
    (evidence / "principal.log").write_bytes((ROOT / "paper.log").read_bytes())
    print(json.dumps({"status": "passed", "source_commit": source_commit,
                      "principal_pages": principal["pages"], "companions": list(companions)}))

if __name__ == "__main__":
    main()
