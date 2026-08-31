#!/usr/bin/env python3
"""Parallel clean-build of all eleven Round-Ten papers."""
from __future__ import annotations
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib, json, re, subprocess, sys

ROOT=Path(__file__).resolve().parents[1]
PAPERS=[
'A1-exact-benchmarks','A2-sinai-homological-pressure','A3-full-empirical-path-ldp','A4-history-memory-universal-pressure',
'B1-microcanonical-preparation','B2-collision-clusters-dynamic-ldp','B3-hamilton-boltzmann-cotangents','B4-nonlinear-kinetic-semigroups',
'C1-information-risk-sensitive-saddles','C2-cotangent-rigidity-tangent-representations','D1-deterministic-theta-contractions']
LOGDIR=ROOT/'ROUND10_BUILD_LOGS'; LOGDIR.mkdir(exist_ok=True)
WARN_RE=re.compile(r'(LaTeX Warning: (?:Reference|Citation).*undefined|There were undefined references|There were undefined citations)',re.I)

def build(name:str)->tuple[str,dict]:
    d=ROOT/'papers'/name
    subprocess.run(['latexmk','-C','main.tex'],cwd=d,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
    cp=subprocess.run(['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error','-file-line-error','main.tex'],cwd=d,capture_output=True,text=True)
    transcript=(cp.stdout or '')+(cp.stderr or '')
    (LOGDIR/f'{name}.log').write_text(transcript,encoding='utf-8',errors='replace')
    pdf=d/'main.pdf'; final_log=d/'main.log'
    final_text=final_log.read_text(encoding='utf-8',errors='replace') if final_log.exists() else ''
    undefined=[line for line in final_text.splitlines() if WARN_RE.search(line)]
    pages=0
    if pdf.exists():
        pi=subprocess.run(['pdfinfo',str(pdf)],capture_output=True,text=True)
        m=re.search(r'^Pages:\s+(\d+)',pi.stdout,re.M); pages=int(m.group(1)) if m else 0
    status='PASS' if cp.returncode==0 and pdf.exists() and pdf.stat().st_size>0 and not undefined else 'FAIL'
    return name,{
      'status':status,'returncode':cp.returncode,
      'pdf_bytes':pdf.stat().st_size if pdf.exists() else 0,
      'pdf_pages':pages,
      'pdf_sha256':hashlib.sha256(pdf.read_bytes()).hexdigest() if pdf.exists() else None,
      'undefined_reference_lines':undefined,
      'transcript':f'ROUND10_BUILD_LOGS/{name}.log',
    }

summary={'schema':'theta-theory-round10-build-summary-v1','papers':{},'failed':[]}
with ThreadPoolExecutor(max_workers=4) as pool:
    futures=[pool.submit(build,n) for n in PAPERS]
    for fut in as_completed(futures):
        name,entry=fut.result(); summary['papers'][name]=entry
        print(f'ROUND10_BUILD {name} {entry["status"]} pages={entry["pdf_pages"]} bytes={entry["pdf_bytes"]}',flush=True)
for name in PAPERS:
    if summary['papers'][name]['status']!='PASS': summary['failed'].append(name)
summary['paper_count']=len(PAPERS);summary['passed']=len(PAPERS)-len(summary['failed'])
summary['total_pdf_pages']=sum(x['pdf_pages'] for x in summary['papers'].values())
summary['status']='PASS' if not summary['failed'] else 'FAIL'
(ROOT/'ROUND10_BUILD_SUMMARY.json').write_text(json.dumps(summary,indent=2,sort_keys=True)+'\n')
if summary['failed']:
    print('ROUND10_BUILD_FAILED '+','.join(summary['failed']),file=sys.stderr); raise SystemExit(1)
print(f'ROUND10_BUILD_PASS 11/11 pages={summary["total_pdf_pages"]}')
