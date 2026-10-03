#!/usr/bin/env python3
"""Read-only source qualification; local primary runs are not Git checkouts."""
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

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def git(*args: str) -> str | None:
    p=subprocess.run(['git','-C',str(ROOT),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode==0 else None

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--all-volumes',action='store_true')
    ap.add_argument('--require-checkout',action='store_true')
    ap.add_argument('--output',default='verification/current')
    args=ap.parse_args()
    out=(ROOT/args.output).resolve()
    if not out.is_relative_to(ROOT/'verification'):
        raise ValueError('output must be below verification/')
    out.mkdir(parents=True,exist_ok=True)
    commit=git('rev-parse','HEAD')
    receipt={'schema':'a2-v19-validation-1','status':'running',
             'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
             'scope':'all_volumes' if args.all_volumes else 'primary_only',
             'source_commit':commit,'source_tree':git('rev-parse','HEAD^{tree}'),
             'execution_kind':'git_checkout' if commit else 'source_content_not_git_checkout',
             'github_run_id':os.getenv('GITHUB_RUN_ID'),'github_sha':os.getenv('GITHUB_SHA'),
             'runner_image':os.getenv('ImageOS'),'runner_image_version':os.getenv('ImageVersion'),
             'platform':platform.platform(),'python':sys.version,'commands':[],
             'diagnostics':[],'documents':[],'formal_proof_certificate':False}
    def run(argv: list[str],cwd: Path,label: str) -> str:
        p=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        log=out/(label+'.log');log.write_text(p.stdout)
        receipt['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
                                    'exit_code':p.returncode,'log':log.name,'log_sha256':sha(log)})
        if p.returncode: raise RuntimeError(f'{label}: exit {p.returncode}')
        return p.stdout
    def pair(script: Path,cwd: Path,label: str,extra: list[str]) -> None:
        argv=[str(script),*extra]
        normal=run([sys.executable,*argv],cwd,label+'-normal')
        optimized=run([sys.executable,'-O',*argv],cwd,label+'-optimized')
        if normal!=optimized: raise RuntimeError(label+': outputs differ under -O')
        receipt['diagnostics'].append({'suite':label,'normal_optimized_identical':True,
                                      'normal_log_sha256':sha(out/(label+'-normal.log'))})
    def inspect(directory: Path,name: str,label: str,strict: bool) -> None:
        log=directory/(name+'.log');pdf=directory/(name+'.pdf')
        text=log.read_text(errors='replace')
        warnings=re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',text,re.M)
        info=run(['pdfinfo',str(pdf)],ROOT,label+'-pdfinfo')
        pages=re.search(r'^Pages:\s+(\d+)',info,re.M)
        receipt['documents'].append({'label':label,'pages':int(pages.group(1)) if pages else None,
            'pdf':str(pdf.relative_to(ROOT)),'pdf_sha256':sha(pdf),'tex_log_sha256':sha(log),
            'final_tex_diagnostics':warnings})
        if any('undefined' in s.lower() or 'multiply defined' in s.lower() for s in warnings):
            raise RuntimeError(label+': unresolved TeX references')
        if strict and warnings: raise RuntimeError(label+': final TeX diagnostics')
    try:
        pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
        before={name:sha(ROOT/name) for name in pins['new_source_sha256']}
        if before!=pins['new_source_sha256']: raise RuntimeError('pinned source bytes differ')
        receipt['source_manifest']=before
        receipt['source_manifest_sha256']=hashlib.sha256(json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        if args.require_checkout or args.all_volumes:
            if not commit: raise RuntimeError('this mode requires a real Git checkout')
            if git('diff','--name-only','HEAD','--','.')!='': raise RuntimeError('dirty tracked sources')
            prefix=git('rev-parse','--show-prefix') or ''
            actual=git('rev-parse','HEAD:'+prefix+'retained/v18')
            if actual!=pins['retained_v18_tree']: raise RuntimeError('retained v18 tree differs')
            actual_s=git('rev-parse','HEAD:'+prefix+'complete')
            if actual_s!=pins['complete_tree']: raise RuntimeError('Supplement S tree differs')
            receipt['retained_trees']={'v18':actual,'complete':actual_s}
        if receipt['github_sha'] and receipt['github_sha']!=commit:
            raise RuntimeError('triggering SHA differs from checkout')
        pair(ROOT/'tools/verify_v19.py',ROOT,'v19',['--geometry'])
        receipt['new_check_result']=json.loads((out/'v19-normal.log').read_text())
        run(['pdflatex','--version'],ROOT,'tex-version')
        run(['latexmk','-v'],ROOT,'latexmk-version')
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error','-outdir=build','main.tex'],ROOT,'primary-build')
        inspect(ROOT/'build','main','primary',True)
        if args.all_volumes:
            retained=ROOT/'retained/v18'
            for script,extra in [('verify_exact.py',[]),('verify_revision.py',[]),('verify_two_window.py',['--geometry'])]:
                pair(retained/'tools'/script,retained,'retained-'+Path(script).stem,extra)
            stage=out/'retained-build'
            if stage.exists(): shutil.rmtree(stage)
            shutil.copytree(retained,stage)
            run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error','main.tex'],stage,'supplement-R-build')
            inspect(stage,'main','supplement-R',False)
            for round_no in range(2):
                for name in ('two_collision','main'):
                    run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',name+'.tex'],
                        stage/'complete',f'supplement-S-{round_no}-{name}')
            inspect(stage/'complete','main','supplement-S',False)
            inspect(stage/'complete','two_collision','supplement-S-auxiliary',False)
        if before!={name:sha(ROOT/name) for name in before}:
            raise RuntimeError('qualification changed mathematical or tool sources')
        if commit and git('diff','--name-only','HEAD','--','.')!='':
            raise RuntimeError('qualification changed tracked sources')
        receipt['source_unchanged']=True
        receipt['status']='passed'
    except Exception as exc:
        receipt['status']='failed';receipt['error']=str(exc)
    finally:
        receipt['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n')
        print(json.dumps(receipt,sort_keys=True,indent=2))
    return 0 if receipt['status']=='passed' else 1

if __name__=='__main__':
    raise SystemExit(main())
