#!/usr/bin/env python3
"""Read-only source qualification. A source-content run is not a Git checkout.

--all-volumes requires --require-checkout and stages retained documents before
building them. Receipts preserve actual failures and null hosted/checkout IDs.
"""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
V22='65c432ddf3233b4931a15e1ee86cbc051503e682'
COMPLETE='14b2e5379e5b223bc0bdc823c97fd77c2dca2cda'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    p=subprocess.run(['git','-C',str(ROOT),*args],text=True,
                     stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode==0 else None


def source_manifest() -> dict[str,str]:
    paths=[ROOT/'main.tex',ROOT/'references.tex']
    paths+=sorted((ROOT/'core').glob('*.tex'))
    paths+=sorted((ROOT/'tools').glob('*.py'))
    return {str(p.relative_to(ROOT)):sha(p) for p in paths}


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--all-volumes',action='store_true')
    ap.add_argument('--require-checkout',action='store_true')
    ap.add_argument('--output-dir',default='verification/current')
    args=ap.parse_args()
    out=(ROOT/args.output_dir).resolve()
    if not out.is_relative_to(ROOT/'verification'):
        raise ValueError('output directory must be below verification/')
    out.mkdir(parents=True,exist_ok=True)
    before=source_manifest()
    record={'schema':'a2-v23-validation-1','status':'running',
            'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
            'execution_kind':'git_checkout' if git('rev-parse','HEAD') else 'source_content_not_git_checkout',
            'scope':'all_declared_volumes' if args.all_volumes else 'primary_only',
            'source_commit':git('rev-parse','HEAD'),'source_tree':git('rev-parse','HEAD^{tree}'),
            'github_sha':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID'),
            'runner_image':os.getenv('ImageOS'),'runner_image_version':os.getenv('ImageVersion'),
            'python':sys.version,'platform':platform.platform(),'commands':[],
            'documents':[],'source_manifest':before,'formal_proof_certificate':False,
            'executed_physical_scanner':False}

    def run(argv: list[str],cwd: Path,label: str) -> str:
        p=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        log=out/(label+'.log'); log.write_text(p.stdout)
        record['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
             'exit_code':p.returncode,'log':log.name,'log_sha256':sha(log)})
        if p.returncode: raise RuntimeError(f'{label}: exit {p.returncode}')
        return p.stdout

    def document(directory: Path,stem: str,source: str,label: str) -> None:
        pdf=directory/(stem+'.pdf'); log=directory/(stem+'.log')
        diagnostic=re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                              log.read_text(errors='replace'),re.M)
        info=run(['pdfinfo',str(pdf)],ROOT,label+'-pdfinfo')
        pages=re.search(r'^Pages:\s+(\d+)',info,re.M)
        record['documents'].append({'source':source,'pages':int(pages.group(1)) if pages else None,
             'pdf':str(pdf.relative_to(ROOT)),'pdf_sha256':sha(pdf),
             'tex_log_sha256':sha(log),'final_tex_diagnostics':diagnostic})
        if diagnostic: raise RuntimeError(f'{source}: final TeX diagnostics remain')

    try:
        pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
        for name,want in pins['source_sha256'].items():
            if sha(ROOT/name)!=want: raise RuntimeError('source pin differs: '+name)
        record['source_pins_sha256']=sha(ROOT/'SOURCE_PINS.json')
        if args.all_volumes and not args.require_checkout:
            raise RuntimeError('all-volume qualification requires --require-checkout')
        if args.require_checkout:
            if not record['source_commit']: raise RuntimeError('no Git checkout')
            if git('diff','--name-only','HEAD','--','.')!='':
                raise RuntimeError('tracked source differs from checkout')
            if record['github_sha'] and record['github_sha']!=record['source_commit']:
                raise RuntimeError('checkout differs from triggering SHA')
            prefix=git('rev-parse','--show-prefix') or ''
            snapshots={'retained/v22':V22,'complete':COMPLETE}
            for path,want in snapshots.items():
                actual=git('rev-parse','HEAD:'+prefix+path)
                if actual!=want: raise RuntimeError('retained tree differs: '+path)
            record['verified_retained_trees']=snapshots
        normal=run([sys.executable,'tools/verify_v23.py','--geometry'],ROOT,'v23-normal')
        optimized=run([sys.executable,'-O','tools/verify_v23.py','--geometry'],ROOT,'v23-optimized')
        if normal!=optimized: raise RuntimeError('normal and optimized outputs differ')
        record['diagnostics']=json.loads(normal)
        record['normal_optimized_identical']=True
        run(['pdflatex','--version'],ROOT,'tex-version')
        run(['latexmk','-v'],ROOT,'latexmk-version')
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-outdir=build','main.tex'],ROOT,'primary-build')
        document(ROOT/'build','main','main.tex','primary')
        if args.all_volumes:
            stage=out/'retained-build'
            if stage.exists(): shutil.rmtree(stage)
            shutil.copytree(ROOT/'retained/v22',stage)
            # Run the unmodified prior checker in its own staged source tree.
            n=run([sys.executable,'tools/verify_v22.py'],stage,'retained-v22-normal')
            o=run([sys.executable,'-O','tools/verify_v22.py'],stage,'retained-v22-optimized')
            if n!=o: raise RuntimeError('retained outputs differ')
            record['retained_v22_diagnostics']=json.loads(n)
            targets=[(stage,'main','retained/v22/main.tex'),
                     (stage/'retained/v21','main','retained/v22/retained/v21/main.tex'),
                     (stage/'retained/v21/retained/v18','main','retained/v22/retained/v21/retained/v18/main.tex'),
                     (stage/'retained/v21/complete','two_collision','complete/two_collision.tex'),
                     (stage/'retained/v21/complete','main','complete/main.tex')]
            # A second pass resolves any two-document cross references in S.
            for pass_no in range(2):
                for i,(directory,stem,source) in enumerate(targets):
                    run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',stem+'.tex'],
                        directory,f'retained-{i}-pass-{pass_no}')
            for i,(directory,stem,source) in enumerate(targets):
                document(directory,stem,source,f'retained-{i}')
        if source_manifest()!=before: raise RuntimeError('source changed during validation')
        if args.require_checkout and git('diff','--name-only','HEAD','--','.')!='':
            raise RuntimeError('tracked source changed during validation')
        record['source_unchanged']=True; record['status']='passed'
    except Exception as exc:
        record['status']='failed'; record['error']=str(exc)
    finally:
        record['source_manifest_sha256']=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        record['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
        print(json.dumps(record,sort_keys=True,indent=2))
    return 0 if record['status']=='passed' else 1

if __name__=='__main__': raise SystemExit(main())
