#!/usr/bin/env python3
"""Compile this standalone manuscript and bind actual checks to source hashes."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile

ROOT=Path(__file__).resolve().parent

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def run(cmd: list[str], *, env: dict[str,str] | None=None) -> subprocess.CompletedProcess:
    return subprocess.run(cmd,cwd=ROOT,env=env,text=True,stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,check=False)

def main() -> None:
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,default=ROOT/'build')
    args=parser.parse_args()
    output=args.output.resolve(); output.mkdir(parents=True,exist_ok=True)
    for tool in ('pdflatex','pdfinfo'):
        if shutil.which(tool) is None:
            raise SystemExit(f'Required executable not found: {tool}')
    verify=ROOT/'tools/verify.py'
    outputs=[]
    for flags,name in [([], 'diagnostics.json'),(['-O'],'diagnostics-optimized.json')]:
        p=run([sys.executable,*flags,str(verify)])
        (output/name).write_text(p.stdout)
        if p.returncode:
            raise SystemExit(f'Diagnostic failure; see {output/name}')
        outputs.append(p.stdout)
    if outputs[0]!=outputs[1]:
        raise SystemExit('Ordinary and optimized diagnostic outputs differ')
    negative={}
    for mutant in ['omit-jacobian-q0','omit-pressure-beta']:
        p=run([sys.executable,str(verify),'--mutant',mutant])
        (output/f'mutant-{mutant}.txt').write_text(p.stdout)
        if p.returncode==0:
            raise SystemExit(f'Mutant was not rejected: {mutant}')
        negative[mutant]={'rejected':True,'exit_code':p.returncode}
    env=os.environ.copy()
    env['SOURCE_DATE_EPOCH']='1790035200'
    env['FORCE_SOURCE_DATE']='1'
    previous=None; passes=0
    with tempfile.TemporaryDirectory(prefix='gtf-i-build-') as tmp:
        temp=Path(tmp)
        for number in range(1,7):
            cmd=['pdflatex','-interaction=nonstopmode','-halt-on-error',
                 '-file-line-error','-recorder',f'-output-directory={temp}','main.tex']
            p=run(cmd,env=env)
            (output/f'pdflatex-pass-{number}.txt').write_text(p.stdout)
            if p.returncode:
                raise SystemExit(f'LaTeX failed on pass {number}')
            passes=number
            state=tuple(sha(temp/f'main.{ext}') if (temp/f'main.{ext}').exists() else ''
                        for ext in ['aux','toc','out'])
            log=(temp/'main.log').read_text(errors='replace')
            if state==previous and number>=2:
                break
            previous=state
        else:
            raise SystemExit('References did not stabilize after six passes')
        forbidden=['There were undefined references','There were undefined citations',
                   'multiply defined','Overfull \\hbox','Overfull \\vbox']
        if any(x in log for x in forbidden):
            (output/'main.log').write_text(log)
            raise SystemExit('Final LaTeX log contains a forbidden warning')
        for ext in ['pdf','log','aux','toc','fls']:
            if (temp/f'main.{ext}').exists():
                shutil.copy2(temp/f'main.{ext}',output/f'main.{ext}')
    info=run(['pdfinfo',str(output/'main.pdf')]).stdout
    pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
    sources=[ROOT/'main.tex',ROOT/'preamble.tex',ROOT/'references.tex',ROOT/'build.py',verify]
    sources+=sorted((ROOT/'sections').glob('*.tex'))
    tex='\n'.join(p.read_text() for p in sources if p.suffix=='.tex')
    counts={name:len(re.findall(r'\\begin\{'+name+r'\}',tex))
            for name in ['theorem','lemma','proposition','corollary','proof','definition','example']}
    receipt={'status':'passed','kind':'local-or-runner-executed-build',
        'python':platform.python_version(),'pdflatex':run(['pdflatex','--version']).stdout.splitlines()[0],
        'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sources},
        'pdf_sha256':sha(output/'main.pdf'),'pdf_pages':pages,'compiler_invocations':passes,
        'source_counts':counts,'diagnostics':json.loads(outputs[0]),
        'optimized_output_identical':True,'negative_controls':negative,
        'final_undefined_references':False,'final_overfull_boxes':False,
        'visual_review':'not performed by this script',
        'scope':'Compilation and finite diagnostics are not formal proof verification or peer review.'}
    (output/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'pages':pages,'compiler_invocations':passes,
         'diagnostic_checks':receipt['diagnostics']['total'],'output':str(output)},indent=2))

if __name__=='__main__':
    main()
