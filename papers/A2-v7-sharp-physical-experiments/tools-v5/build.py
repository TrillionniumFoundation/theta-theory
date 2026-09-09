#!/usr/bin/env python3
"""Audit and build the complete A2 v5 native article and companion."""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'verification-v5'
OUT.mkdir(exist_ok=True)

def run(command: list[str], logfile: str | None=None) -> subprocess.CompletedProcess:
    result=subprocess.run(command,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if logfile:
        (OUT/logfile).write_text(result.stdout,encoding='utf-8')
    if result.returncode:
        print(result.stdout[-14000:])
        raise RuntimeError(f'Command failed ({result.returncode}): {command}')
    return result

def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def collect(name: str, seen: set[str], active: list[str]) -> str:
    if name in seen:
        raise RuntimeError(f'Duplicate or cyclic active input: {name}')
    seen.add(name)
    path=ROOT/name
    if not path.is_file():
        raise FileNotFoundError(path)
    active.append(name)
    text=re.sub(r'(?<!\\)%[^\n]*','',path.read_text(encoding='utf-8'))
    parts=[text]
    for child in re.findall(r'\\input\{([^}]+)\}',text):
        child=child if child.endswith('.tex') else child+'.tex'
        parts.append(collect(child,seen,active))
    return '\n'.join(parts)

def source_audit() -> dict:
    active: list[str]=[]
    text=collect('main.tex',set(),active)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    refs=re.findall(r'\\(?:ref|eqref|autoref|pageref)\{([^}]+)\}',text)
    duplicates=sorted({x for x in labels if labels.count(x)>1})
    missing=sorted(set(x for x in refs if x not in labels and not x.startswith('TC-')))
    bib=set(re.findall(r'\\bibitem(?:\[[^]]*\])?\{([^}]+)\}',text))
    cited=set()
    for item in re.findall(r'\\cite(?:\[[^]]*\])?\{([^}]+)\}',text):
        cited.update(x.strip() for x in item.split(','))
    report=dict(active_inputs=active,label_count=len(labels),duplicate_labels=duplicates,missing_references=missing,missing_citations=sorted(cited-bib))
    (OUT/'source_audit.json').write_text(json.dumps(report,indent=2)+'\n')
    if duplicates or missing or cited-bib:
        raise RuntimeError(f'Native source audit failed: {report}')
    pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
    gitroot=Path(run(['git','rev-parse','--show-toplevel']).stdout.strip())
    rel=ROOT.relative_to(gitroot).as_posix()
    for name,expected in pins['unchanged_subtrees'].items():
        actual=run(['git','rev-parse',f'HEAD:{rel}/{name}']).stdout.strip()
        if actual!=expected:
            raise RuntimeError(f'Changed inherited subtree {name}: {actual} != {expected}')
    return report

def main() -> None:
    audit=source_audit()
    check=ROOT/'tools-v5/independent_checks.py'
    normal=OUT/'checks.json'
    optimized=OUT/'checks.optimized.json'
    run([sys.executable,str(check),'--output',str(normal)],'checks.stdout.txt')
    run([sys.executable,'-O',str(check),'--output',str(optimized)],'checks.optimized.stdout.txt')
    if normal.read_bytes()!=optimized.read_bytes():
        raise RuntimeError('Normal and optimized diagnostic outputs differ')
    compiled={}
    for stem in ('two_collision','main'):
        for iteration in range(1,4):
            run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error',stem+'.tex'],f'{stem}.pass{iteration}.txt')
        log=(ROOT/(stem+'.log')).read_text(errors='replace')
        if 'There were undefined references' in log or 'multiply-defined labels' in log or re.search(r'(?:Reference|Citation)[^\n]*undefined',log):
            raise RuntimeError(f'Unresolved references in {stem}.log')
        pages=re.search(r'Output written on .*?\((\d+) pages?',log,re.S)
        compiled[stem]=dict(pages=int(pages.group(1)) if pages else None,pdf_sha256=digest(ROOT/(stem+'.pdf')),overfull_boxes=len(re.findall(r'Overfull \\[hv]box',log)))
    result=dict(status='passed',commit=run(['git','rev-parse','HEAD']).stdout.strip(),active_input_count=len(audit['active_inputs']),diagnostic_script_sha256=digest(check),diagnostic_output_sha256=digest(normal),diagnostics=json.loads(normal.read_text())['counts'],total_checks=json.loads(normal.read_text())['total'],normal_optimized_identical=True,compiled=compiled,scope='Build and finite diagnostics only; not theorem certification.')
    (OUT/'build_result.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
