#!/usr/bin/env python3
"""Build from a committed, manifested native source; repeat in two clean directories."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import verify

ROOT=Path(__file__).resolve().parent

def run(cmd, cwd, env=None):
    p=subprocess.run(cmd,cwd=cwd,env=env,text=True,capture_output=True)
    if p.returncode:
        raise RuntimeError('Command failed: '+repr(cmd)+'\n'+p.stdout[-5000:]+'\n'+p.stderr[-3000:])
    return p.stdout

def clean_build(tag):
    with tempfile.TemporaryDirectory(prefix='gtf-r3-'+tag+'-') as td:
        dst=Path(td)
        files=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())['files']
        for f in files:
            source=ROOT/f['path']; target=dst/f['path']
            target.parent.mkdir(parents=True,exist_ok=True)
            shutil.copyfile(source,target)
        shutil.copyfile(ROOT/'SOURCE_MANIFEST.json',dst/'SOURCE_MANIFEST.json')
        env=os.environ.copy()
        env.update(SOURCE_DATE_EPOCH='1791244800',FORCE_SOURCE_DATE='1',TZ='UTC')
        for _ in range(3):
            run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],dst,env)
        log=(dst/'main.log').read_text(errors='replace')
        forbidden=('Undefined control sequence','There were undefined references','undefined citations',
                   'multiply defined','Label(s) may have changed','Rerun to get cross-references right')
        for bad in forbidden:
            verify.require(bad not in log,'TeX diagnostic: '+bad)
        overfull=re.findall(r'Overfull \\hbox \(([^)]+)\)',log)
        verify.require(not overfull,'Overfull TeX boxes: '+str(overfull))
        pdf=(dst/'main.pdf').read_bytes()
        info=run(['pdfinfo','main.pdf'],dst)
        pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
        return pdf,{'pages':pages,'sha256':hashlib.sha256(pdf).hexdigest(),
                    'tex_log_sha256':hashlib.sha256(log.encode()).hexdigest(),
                    'overfull_boxes':len(overfull)}

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-sha',required=True)
    ap.add_argument('--allow-uncommitted',action='store_true')
    args=ap.parse_args()
    if not args.allow_uncommitted:
        head=run(['git','rev-parse','HEAD'],ROOT).strip()
        verify.require(head==args.source_sha,'Build head is not the supplied source SHA')
        verify.require(not run(['git','status','--porcelain','--untracked-files=no'],ROOT).strip(),
                       'Source checkout is dirty')
    audit=verify.source_audit()
    normal=verify.regressions(False);optimized=verify.regressions(True)
    verify.require(normal==optimized,'Optimized regression mismatch')
    pdf,first=clean_build('first');other,second=clean_build('independent')
    verify.require(pdf==other,'Independent native rebuild is not byte-identical')
    (ROOT/'paper.pdf').write_bytes(pdf)
    ev=ROOT/'evidence';ev.mkdir(exist_ok=True)
    regression={'normal':normal,'optimized':optimized,'identical':normal==optimized,
                'continuum_proof_by_tests':False}
    (ev/'REGRESSION.json').write_text(json.dumps(regression,indent=2,sort_keys=True)+'\n')
    receipt={'source_commit':args.source_sha,'preliminary_uncommitted':args.allow_uncommitted,
             'source_audit':audit,'paper_sha256':first['sha256'],
             'pages':first['pages'],'first_build':first,'independent_build':second,
             'independent_rebuild_identical':pdf==other,
             'normal_optimized_identical':normal==optimized,
             'compiler':run(['pdflatex','--version'],ROOT).splitlines()[0],
             'source_date_epoch':1791244800,'continuum_proof_by_tests':False,
             'artifact_commit':'recorded by the artifact child and final read-only receipt; not self-referential'}
    (ev/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
