#!/usr/bin/env python3
"""Two isolated PDF builds, both Python modes, and explicit source-bound receipts."""
import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from verify import ROOT,require,verify,sha256,git_hash

PAPER='General_Theta_Foundations_I_restart_r11.pdf'

def run(cmd,cwd=None,env=None):
    proc=subprocess.run(cmd,cwd=cwd,env=env,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    if proc.returncode:
        raise RuntimeError('command failed: '+repr(cmd)+'\n'+proc.stdout[-12000:])
    return proc.stdout

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--source-sha')
    ap.add_argument('--expected-tree')
    ap.add_argument('--output',default=str(ROOT/'artifacts'))
    ap.add_argument('--receipt',default=str(ROOT/'evidence'/'BUILD_RECEIPT.json'))
    args=ap.parse_args()
    if args.source_sha:
        require(bool(re.fullmatch(r'[0-9a-f]{40}',args.source_sha)), 'source SHA must be a full Git commit')
    audit=verify(); before=audit['native_source_tree_sha']
    if args.expected_tree:
        require(before==args.expected_tree,'native source tree differs from expected remote tree')
    normal=run([sys.executable,str(ROOT/'regression.py')])
    optimized=run([sys.executable,'-O',str(ROOT/'regression.py')])
    require(normal==optimized,'normal/optimized regression output differs')
    regression=json.loads(normal)
    env=os.environ.copy();env.update({'SOURCE_DATE_EPOCH':'1791331200','FORCE_SOURCE_DATE':'1','TZ':'UTC','LC_ALL':'C.UTF-8'})
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    versions=run(['pdflatex','--version']).splitlines()[0]
    products=[]
    for i in range(2):
        with tempfile.TemporaryDirectory(prefix='theta-r11-clean-') as td:
            work=Path(td)/'source'; work.mkdir()
            for name in list(manifest['files'])+['SOURCE_MANIFEST.json']:
                dest=work/name;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(ROOT/name,dest)
            run([sys.executable,str(work/'verify.py')],cwd=work)
            out=work/'output';out.mkdir()
            for _ in range(3):
                run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','-recorder','-output-directory='+str(out),'main.tex'],cwd=work,env=env)
            log=(out/'main.log').read_text(errors='replace')
            for forbidden in ('There were undefined references','There were multiply-defined labels','Citation `','Reference `','Overfull \\hbox','Overfull \\vbox'):
                require(forbidden not in log,'LaTeX audit failure: '+forbidden)
            fls=(out/'main.fls').read_text(errors='replace')
            loaded=set()
            for line in fls.splitlines():
                if line.startswith('INPUT '):
                    p=Path(line[6:]);p=p if p.is_absolute() else work/p
                    try: rel=p.resolve().relative_to(work).as_posix()
                    except ValueError: continue
                    if rel.endswith('.tex'): loaded.add(rel)
            require(loaded==set(audit['active_tex']),'recorder source input mismatch: '+str(loaded))
            data=(out/'main.pdf').read_bytes()
            info=run(['pdfinfo',str(out/'main.pdf')])
            pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
            products.append((data,log,pages))
    require(products[0][0]==products[1][0],'isolated PDF rebuild is not byte identical')
    require(verify()['native_source_tree_sha']==before,'build mutated source')
    output=Path(args.output);output.mkdir(parents=True,exist_ok=True)
    pdf,log,pages=products[0]
    (output/PAPER).write_bytes(pdf)
    (output/'LATEX_BUILD.log').write_text(log)
    receipt={
       'status':'PASS','source_commit':args.source_sha,
       'binding':'remote source commit and native tree' if args.source_sha else 'uncommitted preflight; native tree only',
       'native_source_tree_sha':before,'source_audit':audit,'regression':regression,
       'normal_and_optimized_equal':True,'isolated_rebuilds':2,'passes_per_rebuild':3,
       'pdf_byte_identical':True,'pdf_pages':pages,'pdf_sha256':sha256(pdf),
       'pdf_git_blob_sha':git_hash('blob',pdf),'pdf_bytes':len(pdf),
       'tex_engine':versions,'overfull_boxes':0,'undefined_references':0,
       'source_mutation':False,'hosted_run_id':os.environ.get('GITHUB_RUN_ID'),
       'limitations':'Native r11 subtree build, not a repository-wide rebuild; finite regression does not prove theorems.'}
    rp=Path(args.receipt);rp.parent.mkdir(parents=True,exist_ok=True)
    rp.write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
    print(json.dumps(receipt,sort_keys=True,indent=2))

if __name__=='__main__':
    main()
