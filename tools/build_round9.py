#!/usr/bin/env python3
"""Parallel clean-build of all eleven round-nine manuscripts."""
from __future__ import annotations

from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
import hashlib, json, os, re, shutil, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
PAPERS = [
    "A1-exact-benchmarks", "A2-sinai-homological-pressure",
    "A3-full-empirical-path-ldp", "A4-history-memory-universal-pressure",
    "B1-microcanonical-preparation", "B2-collision-clusters-dynamic-ldp",
    "B3-hamilton-boltzmann-cotangents", "B4-nonlinear-kinetic-semigroups",
    "C1-information-risk-sensitive-saddles",
    "C2-cotangent-rigidity-tangent-representations",
    "D1-deterministic-theta-contractions",
]
LOG_DIR = ROOT / "ROUND9_BUILD_LOGS"; SUMMARY = ROOT / "ROUND9_BUILD_SUMMARY.json"
WARNING_RE = re.compile(r"LaTeX Warning: (?:Reference|Citation).*undefined|There were undefined references|There were undefined citations|Please \(re\)run Biber", re.I)
ERROR_RE = re.compile(r"(^! |LaTeX Error:|Package .* Error:|Undefined control sequence|Emergency stop|Fatal error|^.*\.tex:\d+:)", re.I|re.M)


def run(cmd: list[str], cwd: Path) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, text=True, stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT, check=False)

def sha(path: Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()

def inspect(name: str, transcript_label: str) -> tuple[bool, dict[str, object], str]:
    paper=ROOT/"papers"/name; pdf=paper/"main.pdf"; log=paper/"main.log"
    undefined=[]
    if log.is_file(): undefined=[l for l in log.read_text(errors="replace").splitlines() if WARNING_RE.search(l)]
    pages=0
    if pdf.is_file() and pdf.stat().st_size:
        info=run(["pdfinfo","main.pdf"],paper); m=re.search(r"^Pages:\s*(\d+)",info.stdout,re.M)
        if m: pages=int(m.group(1))
    ok=pdf.is_file() and pdf.stat().st_size>0 and log.is_file() and pages>0 and not undefined
    result={"status":"PASS" if ok else "FAIL", "pdf_bytes":pdf.stat().st_size if pdf.is_file() else 0,
            "pdf_pages":pages, "undefined_reference_lines":undefined[:50], "transcript":transcript_label}
    if ok: result["pdf_sha256"]=sha(pdf)
    return ok,result,""

def build_one(name: str, resume: bool) -> tuple[str,bool,dict[str,object],str]:
    paper=ROOT/"papers"/name; transcript=LOG_DIR/f"{name}.log"
    if resume:
        ok,res,_=inspect(name,"RESUMED_EXISTING_FINAL_LOG")
        if ok: return name,ok,res,""
    run(["latexmk","-C","main.tex"],paper)
    cp=run(["latexmk","-pdf","-interaction=nonstopmode","-halt-on-error","-file-line-error","main.tex"],paper)
    transcript.write_text(cp.stdout,encoding="utf-8",errors="replace")
    ok,res,_=inspect(name,str(transcript.relative_to(ROOT)))
    if cp.returncode!=0: ok=False; res["status"]="FAIL"; res["returncode"]=cp.returncode
    lines=cp.stdout.splitlines(); hits=[i for i,l in enumerate(lines) if ERROR_RE.search(l)]
    context="\n".join(lines[-100:] if not hits else sum((lines[max(0,i-5):min(len(lines),i+8)]+["---"] for i in hits[:8]),[]))
    return name,ok,res,context

def main() -> None:
    for exe in ("latexmk","biber","pdfinfo"):
        if not shutil.which(exe): raise SystemExit(f"{exe} is not installed")
    LOG_DIR.mkdir(exist_ok=True)
    resume=os.environ.get("ROUND9_RESUME")=="1"
    if not resume:
        for p in LOG_DIR.glob("*.log"): p.unlink()
    results={}; failures=[]; total_pages=0
    workers=min(4, max(1,int(os.environ.get("ROUND9_BUILD_WORKERS","4"))))
    with ThreadPoolExecutor(max_workers=workers) as pool:
        futs={pool.submit(build_one,n,resume):n for n in PAPERS}
        for fut in as_completed(futs):
            name,ok,res,context=fut.result(); results[name]=res
            if ok:
                total_pages += int(res["pdf_pages"])
                print(f"ROUND9_BUILD_PASS {name} pages={res['pdf_pages']} pdf_bytes={res['pdf_bytes']}")
            else:
                failures.append(name); print(f"ROUND9_BUILD_FAIL_BEGIN {name}\n{context}\nROUND9_BUILD_FAIL_END {name}",file=sys.stderr)
    ordered={n:results[n] for n in PAPERS}
    summary={"schema":"theta-theory-round9-build-summary-v1","status":"PASS" if not failures else "FAIL",
             "paper_count":11,"passed":11-len(failures),"failed":sorted(failures),
             "total_pdf_pages":total_pages,"papers":ordered}
    SUMMARY.write_text(json.dumps(summary,indent=2,sort_keys=True)+"\n")
    if failures: raise SystemExit("ROUND9_BUILD_SUMMARY_FAIL failed="+",".join(sorted(failures)))
    print(f"ROUND9_BUILD_SUMMARY_PASS papers=11 total_pages={total_pages}")

if __name__=="__main__": main()
