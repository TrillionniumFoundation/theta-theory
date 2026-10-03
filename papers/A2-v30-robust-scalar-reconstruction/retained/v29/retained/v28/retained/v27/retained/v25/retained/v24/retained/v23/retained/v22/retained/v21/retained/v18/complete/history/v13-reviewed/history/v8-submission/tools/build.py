#!/usr/bin/env python3
"""Clean-build the A2 v8 article and companion; record actual diagnostics.
Requires a TeX distribution providing latexmk, pdflatex and the source packages.
Builds in a temporary directory without any inherited auxiliary files.
"""
from __future__ import annotations
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile


def main() -> None:
    root=Path(__file__).resolve().parents[1]
    if not shutil.which('latexmk'):
        raise SystemExit('latexmk is required.')
    out=root/'verification';out.mkdir(exist_ok=True)
    result={'schema':'a2-v8-clean-build-v1','clean_auxiliary_state':True,
            'order':['two_collision','main'],'documents':{},
            'remote_ci':False,'formal_proof_verification':False}
    with tempfile.TemporaryDirectory(prefix='a2-v8-clean-') as tmp:
        work=Path(tmp)
        for p in root.rglob('*'):
            if p.is_file() and p.suffix in ('.tex','.bib','.sty','.cls','.bst'):
                dest=work/p.relative_to(root);dest.parent.mkdir(parents=True,exist_ok=True)
                shutil.copy2(p,dest)
        env=dict(os.environ)
        # Fix PDF metadata time to the source date; cross-engine byte identity is not promised.
        env['SOURCE_DATE_EPOCH']='1788948233';env['FORCE_SOURCE_DATE']='1'
        for stem in result['order']:
            cmd=['latexmk','-pdf','-interaction=nonstopmode','-halt-on-error',stem+'.tex']
            run=subprocess.run(cmd,cwd=work,env=env,text=True,stdout=subprocess.PIPE,
                               stderr=subprocess.STDOUT,check=False)
            (out/(stem+'.build.txt')).write_text(run.stdout,encoding='utf-8')
            if run.returncode:
                raise RuntimeError(f'{stem}: build failed; inspect verification/{stem}.build.txt')
            log=(work/(stem+'.log')).read_text(errors='replace')
            fatal=re.findall(r'^.*(?:LaTeX Warning:|Package .* Warning:|Overfull|'
                r'Undefined control sequence|multiply defined).*$',log,re.MULTILINE)
            if fatal:raise RuntimeError(stem+': unresolved diagnostics: '+str(fatal))
            data=(work/(stem+'.pdf')).read_bytes()
            shutil.copy2(work/(stem+'.pdf'),root/(stem+'.pdf'))
            shutil.copy2(work/(stem+'.aux'),out/(stem+'.aux'))
            shutil.copy2(work/(stem+'.log'),out/(stem+'.log'))
            pages=re.search(r'Output written on .*?\((\d+) pages?',log)
            result['documents'][stem]={'command':cmd,'return_code':run.returncode,
                'pages':int(pages.group(1)) if pages else None,'bytes':len(data),
                'pdf_sha256':hashlib.sha256(data).hexdigest(),
                'unresolved_references_or_overfull_boxes':False,
                'underfull_vbox_notices':log.count('Underfull \\vbox'),
                'font_expansion_notices':log.count('font should be expanded before its first use')}
    result['status']='pass'
    (out/'build.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))


if __name__=='__main__':main()
