#!/usr/bin/env python3
from __future__ import annotations
from pathlib import Path
import concurrent.futures, hashlib, json, re, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
papers=sorted(p for p in (ROOT/"papers").iterdir() if p.is_dir())
logdir=ROOT/"ROUND14_BUILD_LOGS"; logdir.mkdir(exist_ok=True)
bad_re=re.compile(
    r"LaTeX Warning: (?:Reference|Citation).*undefined|"
    r"There were undefined references|There were undefined citations"
)

def build(p):
    subprocess.run(["latexmk","-C"],cwd=p,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    proc=subprocess.run(
        ["latexmk","-pdf","-interaction=nonstopmode","-halt-on-error","main.tex"],
        cwd=p,capture_output=True,text=True
    )
    transcript=proc.stdout+"\n"+proc.stderr
    (logdir/f"{p.name}.log").write_text(transcript,encoding="utf-8",errors="replace")
    pdf=p/"main.pdf"
    final_log=(p/"main.log").read_text(encoding="utf-8",errors="replace") if (p/"main.log").exists() else ""
    undefined=bad_re.findall(final_log)
    pages=None
    if pdf.exists():
        info=subprocess.run(["pdfinfo",str(pdf)],capture_output=True,text=True)
        m=re.search(r"^Pages:\s+(\d+)",info.stdout,re.M)
        pages=int(m.group(1)) if m else None
    status="PASS" if proc.returncode==0 and pdf.exists() and not undefined else "FAIL"
    return p.name,{
        "returncode":proc.returncode,
        "status":status,
        "pdf_bytes":pdf.stat().st_size if pdf.exists() else 0,
        "pdf_sha256":hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.exists() else None,
        "pdf_pages":pages,
        "undefined_reference_lines":[line for line in final_log.splitlines() if bad_re.search(line)],
        "transcript":str((logdir/f"{p.name}.log").relative_to(ROOT)),
    }

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as ex:
    results=dict(ex.map(build,papers))
failed=[k for k,v in results.items() if v["status"]!="PASS"]
summary={
    "schema":"theta-theory-round14-build-summary-v1",
    "paper_count":len(results),
    "passed":len(results)-len(failed),
    "failed":failed,
    "total_pdf_pages":sum(v["pdf_pages"] or 0 for v in results.values()),
    "papers":results,
    "status":"PASS" if not failed else "FAIL",
}
(ROOT/"ROUND14_BUILD_SUMMARY.json").write_text(
    json.dumps(summary,indent=2,sort_keys=True)+"\n",encoding="utf-8"
)
if failed:
    for p in failed: print("ROUND14_BUILD_FAIL",p,file=sys.stderr)
    raise SystemExit(1)
print(f"ROUND14_BUILD_PASS {len(results)}/11 pages={summary['total_pdf_pages']}")
