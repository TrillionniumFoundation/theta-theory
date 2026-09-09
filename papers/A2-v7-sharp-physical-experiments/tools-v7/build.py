#!/usr/bin/env python3
"""Build the complete A2 v7 referee manuscript and record mechanical evidence."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, data: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, sort_keys=True)+"\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=Path)
    args = parser.parse_args()
    paper = Path(__file__).resolve().parents[1]
    repo = args.repo_root.resolve() if args.repo_root else paper.parents[1]
    baseline = repo / "papers/A2-v6-relative-transfer-count-experiments"
    if not baseline.is_dir():
        raise RuntimeError("The pinned inherited v6 directory is required for preservation checks")
    out, evidence = paper / "build", paper / "verification-v7"
    out.mkdir(exist_ok=True)
    evidence.mkdir(exist_ok=True)
    allowed = {"main.tex", "preamble.tex", "README.md"}
    unchanged, changed, missing = [], [], []
    for source in sorted(baseline.rglob("*")):
        if not source.is_file():
            continue
        relative = source.relative_to(baseline).as_posix()
        target = paper / relative
        if not target.is_file():
            missing.append(relative)
        elif source.read_bytes() == target.read_bytes():
            unchanged.append(relative)
        elif relative in allowed:
            changed.append(relative)
        else:
            raise RuntimeError("Unplanned alteration of an inherited file: " + relative)
    if missing:
        raise RuntimeError("Inherited files missing: " + repr(missing))
    for name in ["main.tex", "preamble.tex", "README.md"]:
        archived = paper / "history" / ("v6-reviewed-"+name)
        if archived.read_bytes() != (baseline/name).read_bytes():
            raise RuntimeError("The replaced v6 entry point is not exactly archived: "+name)
    old_main = (baseline/"main.tex").read_text(encoding="utf-8")
    new_main = (paper/"main.tex").read_text(encoding="utf-8")
    old_inputs = re.findall(r"\\input\{([^}]+)\}", old_main)
    new_inputs = re.findall(r"\\input\{([^}]+)\}", new_main)
    removed = set(old_inputs)-set(new_inputs)-{"v5/references"}
    if removed:
        raise RuntimeError("An active inherited body input was removed: "+repr(sorted(removed)))
    def keys(text: str) -> set[str]:
        return set(re.findall(r"\\bibitem(?:\[[^\]]*\])?\{([^}]+)\}", text))
    old_keys = keys((paper/"v5/references.tex").read_text(encoding="utf-8"))
    new_keys = keys((paper/"v7/references.tex").read_text(encoding="utf-8"))
    if not old_keys <= new_keys:
        raise RuntimeError("An inherited bibliography entry was dropped")
    abstract = re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}",new_main,re.S)
    if abstract is None:
        raise RuntimeError("No abstract found")
    abstract_words = len(abstract.group(1).split())
    if abstract_words > 150:
        raise RuntimeError("Abstract exceeds 150 words: "+str(abstract_words))
    normal = evidence/"checks-normal.json"
    optimized = evidence/"checks-optimized.json"
    for options, destination in [([],normal),(["-O"],optimized)]:
        result = subprocess.run([sys.executable,*options,str(paper/"tools-v7/checks.py"),"--output",str(destination)],cwd=paper,text=True,capture_output=True,timeout=90)
        if result.returncode:
            raise RuntimeError("Finite diagnostics failed:\n"+result.stdout+result.stderr)
    if normal.read_bytes() != optimized.read_bytes():
        raise RuntimeError("Normal and optimized checks produced different evidence")
    checks = json.loads(normal.read_text(encoding="utf-8"))
    if shutil.which("pdflatex") is None:
        raise RuntimeError("pdflatex is required; no PDF build is being claimed")
    documents = {}
    for stem, passes in [("two_collision",2),("main",4)]:
        for number in range(1,passes+1):
            result = subprocess.run(["pdflatex","-no-shell-escape","-interaction=nonstopmode","-halt-on-error","-file-line-error",stem+".tex"],cwd=paper,text=True,capture_output=True,timeout=180)
            (out/(stem+"-pass-"+str(number)+".txt")).write_text(result.stdout+result.stderr,encoding="utf-8")
            if result.returncode:
                raise RuntimeError("TeX build failed for "+stem+"; inspect "+str(out/(stem+"-pass-"+str(number)+".txt")))
        log = (paper/(stem+".log")).read_text(encoding="utf-8",errors="replace")
        undefined = [line for line in log.splitlines() if ("undefined" in line.lower() and ("reference" in line.lower() or "citation" in line.lower())) or "multiply defined" in line.lower()]
        if undefined:
            raise RuntimeError("Unresolved or multiply defined references: "+repr(undefined))
        pages = re.search(r"Output written on .*?\.pdf\s*\((\d+) pages?",log,re.S)
        if pages is None:
            raise RuntimeError("Cannot identify PDF page count in TeX log")
        for suffix in ["pdf","log"]:
            shutil.copy2(paper/(stem+"."+suffix),out/(stem+"."+suffix))
        documents[stem] = {"pages":int(pages.group(1)),"passes":passes,"sha256":digest(out/(stem+".pdf")),"undefined_references_or_citations":0,"overfull_hbox_warnings":len(re.findall(r"Overfull \\hbox",log)),"overfull_vbox_warnings":len(re.findall(r"Overfull \\vbox",log))}
    hashes = {p.relative_to(paper).as_posix():digest(p) for p in sorted(paper.rglob("*.tex"))}
    write_json(evidence/"source-sha256.json",hashes)
    report = {
        "status":"PASS",
        "scope":"Compilation, source preservation, and finite diagnostics only; not mathematical certification, editorial acceptance, or formal page-limit compliance.",
        "source_commit":os.environ.get("GITHUB_SHA","local-unpinned"),
        "workflow_run_id":os.environ.get("GITHUB_RUN_ID"),
        "python":sys.version,
        "abstract_word_count":abstract_words,
        "preservation":{"missing_inherited_files":missing,"unchanged_inherited_file_count":len(unchanged),"replaced_entry_points_archived_exactly":changed,"removed_active_body_inputs":sorted(removed),"inherited_bibliography_keys_retained":sorted(old_keys)},
        "diagnostics":{"total_checks":checks["total_checks"],"normal_equals_optimized":True,"script_sha256":digest(paper/"tools-v7/checks.py"),"result_sha256":digest(normal)},
        "documents":documents,
        "evidence_distinctions":{"new_proofs":"Written in v7 source; independent mathematical review remains separate.","finite_diagnostics":"Actually executed by this build.","historical_verification":"Inherited V5/V6 evidence is retained, not re-certified by this file.","visual_inspection":"Not performed by this build script; record separately after rendering."}
    }
    write_json(evidence/"BUILD_V7.json",report)
    for stem in ["main","two_collision"]:
        for suffix in ["aux","out","toc","log","pdf"]:
            path = paper/(stem+"."+suffix)
            if path.exists():
                path.unlink()
    print(json.dumps(report,indent=2,sort_keys=True))

if __name__ == "__main__":
    main()
