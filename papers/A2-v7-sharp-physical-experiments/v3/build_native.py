#!/usr/bin/env python3
"""Build the complete new article and the unchanged two-collision companion.

No shell escape, theorem stubs, or fabricated cross references are used.
The receipt identifies pre-publication sources by their Git object hashes.
"""
from __future__ import annotations
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification-v3'

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def blob(path: Path) -> str:
    b=path.read_bytes()
    return hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()

def closure(name: str, seen: set[str]) -> None:
    if not name.endswith('.tex'): name+='.tex'
    if name in seen: return
    p=(ROOT/name).resolve()
    if not p.is_relative_to(ROOT) or not p.is_file():
        raise FileNotFoundError(name)
    seen.add(name)
    text='\n'.join(re.split(r'(?<!\\)%',line)[0] for line in p.read_text().splitlines())
    for sub in re.findall(r'\\(?:input|include)\{([^}]+)\}',text): closure(sub,seen)

def main() -> int:
    compiler=shutil.which('pdflatex')
    if not compiler: raise RuntimeError('pdflatex is required')
    active:set[str]=set()
    closure('main',active); closure('two_collision',active)
    OUT.mkdir(exist_ok=True)
    logs=OUT/'build-logs'; logs.mkdir(exist_ok=True)
    receipt={'status':'STARTED','started_utc':datetime.now(timezone.utc).isoformat(),
        'source_commit':None,'source_commit_reason':'Content-addressed build before publication',
        'scope':'Complete main.tex and exact original two_collision.tex',
        'compiler':subprocess.run([compiler,'--version'],capture_output=True,text=True,check=True).stdout.splitlines()[0],
        'builder_sha256':sha(Path(__file__)),
        'source_git_blob':{s:blob(ROOT/s) for s in sorted(active)},
        'source_sha256':{s:sha(ROOT/s) for s in sorted(active)},
        'passes':[],'stubbed_references':False,'substituted_statements':False,
        'pdf_visual_inspection':'RECORDED_SEPARATELY'}
    try:
        for stem in ('main','two_collision'):
            for ext in ('aux','out','toc','log','pdf','fls'):
                (ROOT/f'{stem}.{ext}').unlink(missing_ok=True)
        prev=None
        for cycle in range(1,7):
            for stem in ('two_collision','main'):
                cmd=[compiler,'-no-shell-escape','-recorder','-interaction=nonstopmode',
                     '-halt-on-error','-file-line-error',stem+'.tex']
                run=subprocess.run(cmd,cwd=ROOT,capture_output=True,text=True,
                                   encoding='utf-8',errors='replace',timeout=90)
                dest=logs/f'{stem}-{cycle}.log'; dest.write_text(run.stdout+'\n'+run.stderr)
                receipt['passes'].append({'entry':stem,'cycle':cycle,'returncode':run.returncode,
                                          'stdout_sha256':sha(dest)})
                if run.returncode: raise RuntimeError(f'{stem}, cycle {cycle}: {dest.name}')
            state=tuple(sha(ROOT/(s+'.aux')) for s in ('main','two_collision'))
            if cycle>=3 and state==prev: break
            prev=state
        else: raise RuntimeError('Auxiliary files did not stabilize')
        receipt['auxiliary_files_stable']=True
        receipt['pdfs']={}; receipt['layout_warnings']={}
        actual:set[str]=set()
        for stem in ('main','two_collision'):
            logtext=(ROOT/(stem+'.log')).read_text(errors='replace')
            hard=['undefined on input line','There were undefined references',
                  'There were undefined citations','multiply defined','Label(s) may have changed']
            bad=[v for v in hard if v in logtext]
            if bad: raise RuntimeError(f'{stem}: {bad}')
            overflow=re.findall(r'Overfull \\[hv]box[^\n]*',logtext)
            receipt['layout_warnings'][stem]=overflow
            if overflow: raise RuntimeError(f'{stem}: overfull box; inspect log')
            count=re.search(r'Output written on .*?\((\d+) pages?',logtext,re.S)
            if count is None: raise RuntimeError(f'{stem}: missing page count')
            pdf=ROOT/(stem+'.pdf')
            receipt['pdfs'][pdf.name]={'sha256':sha(pdf),'bytes':pdf.stat().st_size,
                                      'pages':int(count.group(1))}
            for line in (ROOT/(stem+'.fls')).read_text().splitlines():
                if line.startswith('INPUT '):
                    p=Path(line[6:]); p=(ROOT/p).resolve() if not p.is_absolute() else p.resolve()
                    if p.is_relative_to(ROOT) and p.suffix=='.tex': actual.add(str(p.relative_to(ROOT)))
        if actual!=active: raise RuntimeError(f'Source recorder mismatch: {actual^active}')
        for s in active:
            if sha(ROOT/s)!=receipt['source_sha256'][s]: raise RuntimeError('Source changed during build')
        receipt['recorder_matches_declared_inputs']=True
        receipt['status']='COMPILED_REFERENCES_RESOLVED'
    except Exception as exc:
        receipt['status']='FAILED'; receipt['failure']=str(exc)
        raise
    finally:
        receipt['finished_utc']=datetime.now(timezone.utc).isoformat()
        (OUT/'NATIVE_BUILD.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':receipt['status'],'pdfs':receipt['pdfs']},indent=2))
    return 0

if __name__=='__main__': raise SystemExit(main())
