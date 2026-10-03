#!/usr/bin/env python3
"""Read-only v17 build; --all-volumes requires a real pinned Git checkout."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "verification" / "current"
COMPLETE_TREE = "14b2e5379e5b223bc0bdc823c97fd77c2dca2cda"


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    p = subprocess.run(["git", "-C", str(ROOT), *args], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode == 0 else None


def manifest() -> dict[str, str]:
    paths = [ROOT / "main.tex", ROOT / "references.tex"]
    paths += sorted((ROOT / "core").glob("*.tex"))
    paths += sorted((ROOT / "tools").glob("*.py"))
    paths += sorted(p for p in (ROOT / "complete").rglob("*")
                    if p.is_file() and p.suffix in (".tex", ".sty", ".cls", ".bib", ".py"))
    return {str(p.relative_to(ROOT)): sha(p) for p in paths}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--all-volumes", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    before = manifest()
    receipt = {"schema":"a2-v17-source-validation-1", "status":"running",
        "started_utc":dt.datetime.now(dt.timezone.utc).isoformat(),
        "scope":"all_volumes" if args.all_volumes else "primary_only",
        "source_commit":git("rev-parse","HEAD"), "source_tree":git("rev-parse","HEAD^{tree}"),
        "github_run_id":os.getenv("GITHUB_RUN_ID"), "github_sha":os.getenv("GITHUB_SHA"),
        "runner_image":os.getenv("ImageOS"), "runner_image_version":os.getenv("ImageVersion"),
        "platform":platform.platform(), "python":sys.version,
        "commands":[], "diagnostics":[], "documents":[], "formal_proof_certificate":False}

    def run(argv: list[str], cwd: Path, label: str) -> str:
        p = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           env={**os.environ,"PYTHONDONTWRITEBYTECODE":"1","TERM":"dumb"})
        log = OUT / (label + ".log")
        log.write_text(p.stdout)
        receipt["commands"].append({"argv":argv,"cwd":str(cwd.relative_to(ROOT)),
            "exit_code":p.returncode,"log":log.name,"log_sha256":sha(log)})
        if p.returncode:
            raise RuntimeError(f"{label}: exit {p.returncode}")
        return p.stdout

    try:
        if args.all_volumes:
            prefix = git("rev-parse","--show-prefix")
            actual = git("rev-parse","HEAD:"+(prefix or "")+"complete")
            receipt["complete_tree"] = {"expected":COMPLETE_TREE,"actual":actual}
            if actual != COMPLETE_TREE or not (ROOT/"complete/main.tex").exists():
                raise RuntimeError("all-volume build requires the exact preserved supplement tree")
            if git("diff","--name-only","HEAD","--",".") != "":
                raise RuntimeError("checkout is not clean before qualification")
        if receipt["github_sha"] and receipt["github_sha"] != receipt["source_commit"]:
            raise RuntimeError("triggering SHA differs from actual checkout")
        for script in ("verify_exact.py", "verify_revision.py"):
            normal = run([sys.executable,"tools/"+script],ROOT,script+"-normal")
            optimized = run([sys.executable,"-O","tools/"+script],ROOT,script+"-optimized")
            if normal != optimized:
                raise RuntimeError("normal and optimized output differ: "+script)
            record = json.loads(normal)
            record["normal_optimized_identical"] = True
            receipt["diagnostics"].append(record)
        for argv,label in ((["pdflatex","--version"],"tex-version"),
                           (["latexmk","-v"],"latexmk-version")):
            run(argv,ROOT,label)
        run(["latexmk","-g","-pdf","-interaction=nonstopmode","-halt-on-error",
             "-outdir=build","main.tex"],ROOT,"primary-build")
        targets = [(ROOT/"build","main.tex","main.tex")]
        if args.all_volumes:
            stage = OUT / "supplement-build"
            if stage.exists():
                shutil.rmtree(stage)
            shutil.copytree(ROOT/"complete",stage)
            # Build both cross-referenced documents twice; inspect only final logs.
            for round_no in range(2):
                for tex in ("two_collision.tex","main.tex"):
                    run(["latexmk","-g","-pdf","-interaction=nonstopmode","-halt-on-error",tex],
                        stage,f"supplement-{round_no}-{Path(tex).stem}")
            targets += [(stage,"two_collision.tex","complete/two_collision.tex"),
                        (stage,"main.tex","complete/main.tex")]
        for index,(directory,tex,source) in enumerate(targets):
            pdf = directory/Path(tex).with_suffix(".pdf")
            log = directory/Path(tex).with_suffix(".log")
            warnings = re.findall(r"^.*(?:Warning|Overfull|Underfull|undefined).*$",
                                  log.read_text(errors="replace"),re.M)
            info = run(["pdfinfo",str(pdf)],ROOT,f"pdfinfo-{index}")
            match = re.search(r"^Pages:\s+(\d+)",info,re.M)
            receipt["documents"].append({"source":source,"pdf":str(pdf.relative_to(ROOT)),
                "pages":int(match.group(1)) if match else None,"pdf_sha256":sha(pdf),
                "final_tex_log_sha256":sha(log),"final_tex_diagnostics":warnings})
            if warnings:
                raise RuntimeError("final TeX diagnostics: "+str(warnings))
        receipt["source_unchanged"] = before == manifest()
        if not receipt["source_unchanged"]:
            raise RuntimeError("validation modified mathematical or tool sources")
        if args.all_volumes and git("diff","--name-only","HEAD","--",".") != "":
            raise RuntimeError("tracked sources changed during qualification")
        receipt["status"] = "passed"
    except Exception as exc:
        receipt["status"] = "failed"
        receipt["error"] = str(exc)
    finally:
        receipt["source_manifest"] = before
        receipt["source_manifest_sha256"] = hashlib.sha256(
            json.dumps(before,sort_keys=True,separators=(",",":")).encode()).hexdigest()
        receipt["finished_utc"] = dt.datetime.now(dt.timezone.utc).isoformat()
        (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        print(json.dumps(receipt,indent=2,sort_keys=True))
    return 0 if receipt["status"] == "passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
