#!/usr/bin/env python3
"""Isolated local build. No network, shell escape, publication or Git mutations."""
from pathlib import Path
import argparse, json, os, re, shutil, subprocess, sys, tempfile
from verify import ROOT, audit, sha256

def run(args,cwd,env=None):
    p=subprocess.run(args,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True)
    if p.returncode: raise RuntimeError('command failed: '+repr(args)+'\n'+p.stdout[-12000:])
    return p.stdout

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--source-sha',required=True);ap.add_argument('--source-tree',required=True);ap.add_argument('--preliminary',action='store_true');a=ap.parse_args()
    if not re.fullmatch('[0-9a-f]{40}',a.source_sha): raise RuntimeError('invalid source SHA')
    info=audit()
    if a.source_tree!=info['native_tree_sha']: raise RuntimeError('native tree differs from bound remote source')
    normal=run([sys.executable,'regression.py'],ROOT);opt=run([sys.executable,'-O','regression.py'],ROOT)
    if normal!=opt: raise RuntimeError('ordinary/optimized regression mismatch')
    regression=json.loads(normal)
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text());names=[f['path'] for f in manifest['files']]+['SOURCE_MANIFEST.json']
    builds=[];pdfs=[];env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1791244800',FORCE_SOURCE_DATE='1',TZ='UTC')
    for repeat in range(2):
        with tempfile.TemporaryDirectory(prefix='gtf-r5-rebuild-') as tmp:
            dest=Path(tmp)
            for name in names:
                target=dest/name;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes((ROOT/name).read_bytes())
            if audit(dest)!=info: raise RuntimeError('isolated source changed')
            for _ in range(3): run(['pdflatex','-no-shell-escape','-interaction=nonstopmode','-halt-on-error','main.tex'],dest,env)
            log=(dest/'main.log').read_text();pdf=(dest/'main.pdf').read_bytes()
            errors=['undefined references','multiply defined','Citation `','Reference `','Overfull \\hbox','Overfull \\vbox']
            if any(x in log for x in errors): raise RuntimeError('unresolved TeX diagnostics:\n'+log[-9000:])
            pages=int(re.search(r'Output written on main\.pdf \((\d+) pages?',log).group(1))
            builds.append({'pages':pages,'sha256':sha256(pdf),'overfull_boxes':0});pdfs.append(pdf)
    if pdfs[0]!=pdfs[1]: raise RuntimeError('independent PDFs are not byte-identical')
    evidence=ROOT/'evidence';evidence.mkdir(exist_ok=True)
    receipt={'source_commit':a.source_sha,'source_binding':'exact native paper-subtree Git identity; not a claim of full repository checkout','source_audit':info,'builds':builds,'independent_rebuild_identical':True,'normal_optimized_identical':True,'preliminary':a.preliminary,'continuum_proof_by_tests':False,'compiler':run(['pdflatex','--version'],ROOT).splitlines()[0],'source_date_epoch':1791244800,'hosted_ci_run':None}
    (ROOT/'paper.pdf').write_bytes(pdfs[0]);(evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');(evidence/'REGRESSION.json').write_text(json.dumps(regression,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,sort_keys=True))

if __name__=='__main__': main()
