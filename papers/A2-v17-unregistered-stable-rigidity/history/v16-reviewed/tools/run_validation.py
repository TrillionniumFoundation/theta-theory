#!/usr/bin/env python3
"""Read-only source validation. Run --all-volumes in a full Git checkout."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "verification" / "current"


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest() -> dict[str, str]:
    paths = [ROOT / "main.tex", ROOT / "references.tex"]
    paths += sorted((ROOT / "core").glob("*.tex"))
    paths += sorted((ROOT / "tools").glob("*.py"))
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def git(*args: str) -> str | None:
    p = subprocess.run(["git", "-C", str(ROOT), *args], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode == 0 else None


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--all-volumes", action="store_true")
    args = parser.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    before = manifest()
    receipt = {"schema": "a2-v16-source-validation-1",
               "started_utc": dt.datetime.now(dt.timezone.utc).isoformat(),
               "source_commit": git("rev-parse", "HEAD"),
               "source_tree": git("rev-parse", "HEAD^{tree}"),
               "github_run_id": os.environ.get("GITHUB_RUN_ID"),
               "github_sha": os.environ.get("GITHUB_SHA"),
               "runner_os": os.environ.get("RUNNER_OS"),
               "runner_image": os.environ.get("ImageOS"),
               "runner_image_version": os.environ.get("ImageVersion"),
               "platform": platform.platform(), "python": sys.version,
               "scope": "all_volumes" if args.all_volumes else "primary_only",
               "commands": [], "documents": [], "status": "running",
               "formal_proof_certificate": False}

    def run(argv: list[str], cwd: Path, label: str) -> str:
        p = subprocess.run(argv, cwd=cwd, text=True,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                           env={**os.environ, "PYTHONDONTWRITEBYTECODE":"1", "TERM":"dumb"})
        log = OUT / (label + ".log")
        log.write_text(p.stdout)
        receipt["commands"].append({"argv":argv, "cwd":str(cwd.relative_to(ROOT)),
                                    "exit_code":p.returncode, "log":log.name,
                                    "log_sha256":digest(log)})
        if p.returncode:
            raise RuntimeError(f"{label}: exit {p.returncode}")
        return p.stdout

    try:
        normal = run([sys.executable, "tools/verify_exact.py"], ROOT, "exact-normal")
        optimized = run([sys.executable, "-O", "tools/verify_exact.py"], ROOT, "exact-optimized")
        if normal != optimized:
            raise RuntimeError("optimized and normal diagnostics differ")
        receipt["diagnostics"] = json.loads(normal)
        receipt["normal_optimized_identical"] = True
        run(["pdflatex", "--version"], ROOT, "tex-version")
        run(["latexmk", "-v"], ROOT, "latexmk-version")
        jobs = [(ROOT, "main.tex", "build")]
        if args.all_volumes:
            if not (ROOT / "complete/main.tex").exists():
                raise RuntimeError("complete volume absent in this checkout")
            # The unchanged volume uses external .aux references in its own directory.
            jobs += [(ROOT/"complete", "two_collision.tex", None),
                     (ROOT/"complete", "main.tex", None)]
        for index, (cwd, tex, build) in enumerate(jobs):
            command=["latexmk", "-g", "-pdf", "-interaction=nonstopmode", "-halt-on-error"]
            if build:
                command.append("-outdir="+build)
            run(command+[tex], cwd, f"build-{index}")
            target=cwd/build if build else cwd
            log=target/Path(tex).with_suffix(".log")
            warnings=re.findall(r"^.*(?:Warning|Overfull|Underfull|undefined).*$", log.read_text(errors="replace"), re.M)
            if warnings:
                raise RuntimeError(f"final TeX diagnostics in {log}: {warnings}")
            pdf=target/Path(tex).with_suffix(".pdf")
            info=run(["pdfinfo", str(pdf)], ROOT, f"pdfinfo-{index}")
            pages=re.search(r"^Pages:\s+(\d+)", info, re.M)
            receipt["documents"].append({"source":str((cwd/tex).relative_to(ROOT)),
                 "pdf":str(pdf.relative_to(ROOT)), "pages":int(pages.group(1)) if pages else None,
                 "pdf_sha256":digest(pdf), "final_tex_log_sha256":digest(log),
                 "final_tex_diagnostics":warnings})
        receipt["source_unchanged"] = before == manifest()
        if not receipt["source_unchanged"]:
            raise RuntimeError("validation changed primary mathematical or tool sources")
        if args.all_volumes:
            relative=git("rev-parse", "--show-prefix")
            expected="14b2e5379e5b223bc0bdc823c97fd77c2dca2cda"
            actual=git("rev-parse", "HEAD:"+(relative or "")+"complete")
            receipt["complete_tree"]={"expected":expected,"actual":actual}
            if actual != expected:
                raise RuntimeError("complete volume tree is not the pinned preserved tree")
            changed=git("diff", "--name-only", "HEAD", "--", ".")
            receipt["tracked_changes_after_execution"]=changed
            if changed is None or changed:
                raise RuntimeError("tracked source changed or git diff unavailable")
        receipt["status"]="passed"
    except Exception as exc:
        receipt["status"]="failed"
        receipt["error"]=str(exc)
    finally:
        receipt["source_manifest"] = before
        serialized=json.dumps(before,sort_keys=True,separators=(",", ":")).encode()
        receipt["source_manifest_sha256"]=hashlib.sha256(serialized).hexdigest()
        receipt["finished_utc"]=dt.datetime.now(dt.timezone.utc).isoformat()
        (OUT/"receipt.json").write_text(json.dumps(receipt,indent=2,sort_keys=True)+"\n")
        print(json.dumps(receipt,indent=2,sort_keys=True))
    return 0 if receipt["status"]=="passed" else 1


if __name__ == "__main__":
    raise SystemExit(main())
