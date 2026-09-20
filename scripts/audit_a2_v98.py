#!/usr/bin/env python3
"""Bind A2 v98 sources and optional native products to the checked-out head."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT/'papers/A2-v17-boundary-information-coarsening'
BASE = '3b1f657871936a8807f0b3a3b6e86fd75851c9f8'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(['git','-C',str(ROOT),*args],text=True).strip()


def allowed(path: str) -> bool:
    return (path.startswith('papers/A2-v17-boundary-information-coarsening/article/v98/')
            or path.startswith('revisions/a2-v98/')
            or path in {'scripts/audit_a2_v98.py','scripts/verify_a2_v98_math.py',
                        '.github/workflows/a2-v98.yml'}
            or path in {f'papers/A2-v17-boundary-information-coarsening/rigidity_v98{s}.tex'
                        for s in ('','_archive','_complete')})


def main() -> None:
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo',action='store_true')
    ap.add_argument('--build',action='store_true')
    ap.add_argument('--principal-only',action='store_true')
    ap.add_argument('--output',type=Path,required=True)
    args=ap.parse_args()
    manifest=json.loads((ROOT/'revisions/a2-v98/SOURCE_MANIFEST.json').read_text())
    for path,expected in manifest['sha256'].items():
        if sha(ROOT/path)!=expected: raise AssertionError(f'source mismatch: {path}')
    receipt={'source_manifest_sha256':sha(ROOT/'revisions/a2-v98/SOURCE_MANIFEST.json'),
             'source_files_checked':len(manifest['sha256']),
             'basis_review_head':BASE,'checkout_head':None,
             'scope':'local staging, not a Git checkout','products':{},
             'ci_run_id':os.environ.get('GITHUB_RUN_ID')}
    if args.repo:
        head=git('rev-parse','HEAD')
        if os.environ.get('EXPECTED_HEAD',head)!=head: raise AssertionError('wrong checkout head')
        subprocess.check_call(['git','-C',str(ROOT),'merge-base','--is-ancestor',BASE,head])
        changes=git('diff','--name-status',BASE,head).splitlines()
        if not changes: raise AssertionError('empty revision')
        for row in changes:
            status,path=row.split('\t',1)
            if status!='A' or not allowed(path): raise AssertionError(f'non-additive change: {row}')
        receipt.update(checkout_head=head,scope='exact Git checkout',addition_only=True,
                       changed_paths=[row.split('\t',1)[1] for row in changes])
    if args.build:
        names=['rigidity_v98'] if args.principal_only else [
            'rigidity_v98','rigidity_v98_archive','rigidity_v98_complete']
        for name in names:
            pdf,log,fls=[PAPER/(name+ext) for ext in ('.pdf','.log','.fls')]
            text=log.read_text(errors='replace')
            bad=re.findall(r'^.*(?:LaTeX Error|undefined references|undefined citations|Citation .* undefined|Reference .* undefined).*$'
                           ,text,re.M)
            if bad: raise AssertionError(f'{name}: {bad}')
            if name=='rigidity_v98' and 'Overfull \\hbox' in text:
                raise AssertionError('principal overfull box')
            info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
            match=re.search(r'^Pages:\s+(\d+)',info,re.M)
            if not match: raise AssertionError('missing page count')
            inputs={}
            for line in fls.read_text().splitlines():
                if not line.startswith('INPUT '):continue
                p=Path(line[6:])
                if not p.is_absolute(): p=PAPER/p
                p=p.resolve()
                try: rel=p.relative_to(ROOT)
                except ValueError: continue
                if p.is_file() and p.suffix in {'.tex','.sty','.cls','.bib','.pdf'}:
                    inputs[str(rel)]=sha(p)
            if not inputs: raise AssertionError('empty recorded input graph')
            receipt['products'][name]={'pdf_sha256':sha(pdf),'log_sha256':sha(log),
                'fls_sha256':sha(fls),'pages':int(match[1]),'recorded_inputs':inputs,
                'warnings':re.findall(r'^.*(?:Warning|Underfull|Overfull).*$',text,re.M)}
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print('PASS',receipt['scope'],len(receipt['products']),'native products')

if __name__=='__main__': main()
