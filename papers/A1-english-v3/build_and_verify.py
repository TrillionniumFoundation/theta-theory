#!/usr/bin/env python3
"""Build the standalone principal manuscript and record actual finite checks.
The corrected foundation companion has its own source; this command does not
claim to compile or rerun its historical validation suite.
"""
from __future__ import annotations
import hashlib
import json
import re
import shutil
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(__file__).resolve().parent

def run(argv: list[str]) -> str:
    result=subprocess.run(argv,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}): {argv}\n{result.stdout}')
    return result.stdout

def main() -> int:
    for command in ('pdflatex','pdfinfo'):
        if shutil.which(command) is None:
            raise RuntimeError(f'{command} is required on PATH')
    build=ROOT/'build';build.mkdir(exist_ok=True)
    validation=ROOT/'validation';validation.mkdir(exist_ok=True)
    logs={}
    for name,script in [('referee_rerun','referee_checks.py'),('revision_checks','test_revision.py')]:
        logs[name]=run([sys.executable,str(ROOT/'tests'/script),'--output',str(validation/f'{name}.json')])
        (validation/f'{name}.log').write_text(logs[name],encoding='utf-8')
    tex_sources=[ROOT/'main.tex',*sorted((ROOT/'sections').glob('*.tex')),ROOT/'references.tex']
    joined='\n'.join(p.read_text(encoding='utf-8') for p in tex_sources)
    labels=re.findall(r'\\label\{([^}]+)\}',joined)
    refs=re.findall(r'\\(?:eqref|ref)\{([^}]+)\}',joined)
    duplicates=sorted({x for x in labels if labels.count(x)>1})
    missing=sorted(set(refs)-set(labels))
    if duplicates or missing:
        raise RuntimeError(f'Label defects: duplicate={duplicates}, missing={missing}')
    for attempt in range(1,4):
        output=run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-output-directory=build','main.tex'])
        (validation/f'latex_pass_{attempt}.log').write_text(output,encoding='utf-8')
    log=(build/'main.log').read_text(encoding='utf-8',errors='replace')
    defects=[line for line in log.splitlines() if 'Overfull' in line or 'undefined' in line.lower() or 'multiply defined' in line.lower()]
    if defects:
        raise RuntimeError('Unresolved TeX diagnostics:\n'+'\n'.join(defects))
    info=run(['pdfinfo',str(build/'main.pdf')]);pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M)[1])
    proof_entries=re.findall(r'\\begin\{(theorem|proposition|lemma|corollary)\}',joined)
    manifest={}
    sources=tex_sources+[ROOT/'build_and_verify.py',ROOT/'requirements.txt',*sorted((ROOT/'tests').glob('*.py'))]
    for p in sources:
        data=p.read_bytes();manifest[str(p.relative_to(ROOT))]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest(),'git_blob':hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()}
    pdf=(build/'main.pdf').read_bytes()
    receipt={'recorded_at_utc':datetime.now(timezone.utc).isoformat(),'scope':'new standalone principal manuscript only','passed':True,'latex_passes':3,'pdf_pages':pages,'proof_bearing_entries':len(proof_entries),'duplicate_labels':duplicates,'missing_source_labels':missing,'unresolved_tex_diagnostics':defects,
             'pdf_sha256':hashlib.sha256(pdf).hexdigest(),'pdf_bytes':len(pdf),'tex_engine':run(['pdflatex','--version']).splitlines()[0],'source_manifest':manifest,
             'foundation_companion_compiled':False,'historical_author_suite_rerun':False,'formal_verification':False,'visual_inspection':'recorded separately after rendering'}
    (validation/'build_receipt.json').write_text(json.dumps(receipt,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:v for k,v in receipt.items() if k!='source_manifest'},indent=2))
    return 0

if __name__=='__main__':
    try:sys.exit(main())
    except (RuntimeError,OSError) as exc:
        print(str(exc),file=sys.stderr);sys.exit(1)
