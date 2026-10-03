#!/usr/bin/env python3
"""Read-only v22 primary or exact-checkout all-volume qualification."""
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

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification/current'
PRESERVED_TREE = 'a13f1cabd3bc11214bc92ecb6fb49ea51fde87bb'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    p = subprocess.run(['git','-C',str(ROOT),*args], text=True,
                       stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode == 0 else None


def source_manifest() -> dict[str,str]:
    paths = [ROOT/'main.tex',ROOT/'references.tex']
    paths += sorted((ROOT/'core').glob('*.tex'))
    paths += sorted((ROOT/'tools').glob('*.py'))
    return {str(p.relative_to(ROOT)):digest(p) for p in paths}


def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--all-volumes',action='store_true')
    ap.add_argument('--require-checkout',action='store_true')
    args=ap.parse_args()
    OUT.mkdir(parents=True,exist_ok=True)
    before=source_manifest()
    record={'schema':'a2-v22-source-validation-1','status':'running',
        'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope':'all_volumes' if args.all_volumes else 'primary_only',
        'source_commit':git('rev-parse','HEAD'),
        'source_tree':git('rev-parse','HEAD^{tree}'),
        'github_sha':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID'),
        'runner_image':os.getenv('ImageOS'),'runner_version':os.getenv('ImageVersion'),
        'platform':platform.platform(),'python':sys.version,
        'commands':[],'documents':[],'diagnostics':[],
        'source_manifest':before,'formal_proof_certificate':False}
    record['execution_kind']='git_checkout' if record['source_commit'] else 'source_content_not_git_checkout'

    def run(argv: list[str],cwd: Path,label: str) -> str:
        p=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        log=OUT/(label+'.log'); log.write_text(p.stdout)
        record['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
            'exit_code':p.returncode,'log':log.name,'log_sha256':digest(log)})
        if p.returncode:
            raise RuntimeError(f'{label}: exit {p.returncode}')
        return p.stdout

    def paired(script: str,cwd: Path,label: str,extra: list[str]) -> None:
        normal=run([sys.executable,script,*extra],cwd,label+'-normal')
        optimized=run([sys.executable,'-O',script,*extra],cwd,label+'-optimized')
        if normal!=optimized: raise RuntimeError(label+': normal/optimized outputs differ')
        record['diagnostics'].append({'label':label,'normal_optimized_identical':True,
                                      'result':json.loads(normal)})

    def inspect_pdf(directory: Path,name: str,source: str,label: str) -> None:
        pdf=directory/(name+'.pdf'); log=directory/(name+'.log')
        diagnostics=re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                               log.read_text(errors='replace'),re.M)
        info=run(['pdfinfo',str(pdf)],ROOT,label+'-pdfinfo')
        match=re.search(r'^Pages:\s+(\d+)',info,re.M)
        record['documents'].append({'source':source,'pdf':str(pdf.relative_to(ROOT)),
            'pages':int(match.group(1)) if match else None,'pdf_sha256':digest(pdf),
            'final_tex_log_sha256':digest(log),'final_tex_diagnostics':diagnostics})
        if diagnostics: raise RuntimeError(label+': final TeX diagnostics remain')

    try:
        pins=json.loads((ROOT/'SOURCE_PINS.json').read_text())
        if pins['source_sha256']!=before:
            raise RuntimeError('source pins differ from the complete current source manifest')
        if args.all_volumes or args.require_checkout:
            if not record['source_commit']:
                raise RuntimeError('a real Git checkout is required')
            if git('diff','--name-only','HEAD','--','.')!='':
                raise RuntimeError('tracked sources are not clean')
            prefix=git('rev-parse','--show-prefix')
            actual=git('rev-parse','HEAD:'+(prefix or '')+'retained/v21')
            record['preserved_tree']={'expected':PRESERVED_TREE,'actual':actual}
            if actual!=PRESERVED_TREE:
                raise RuntimeError('retained v21 tree differs from the reviewed source')
            for relative in before:
                committed=git('rev-parse','HEAD:'+(prefix or '')+relative)
                working=git('hash-object',str(ROOT/relative))
                if working!=committed: raise RuntimeError('unbound source: '+relative)
        if record['github_sha'] and record['github_sha']!=record['source_commit']:
            raise RuntimeError('actual checkout differs from the triggering SHA')
        paired('tools/verify_v22.py',ROOT,'v22',['--geometry'])
        run(['pdflatex','--version'],ROOT,'tex-version')
        run(['latexmk','-v'],ROOT,'latexmk-version')
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-outdir=build','main.tex'],ROOT,'primary-build')
        inspect_pdf(ROOT/'build','main','main.tex','primary')
        if args.all_volumes:
            original=ROOT/'retained/v21'
            if not (original/'main.tex').is_file():
                raise RuntimeError('retained source checkout is incomplete')
            paired('tools/verify_v19.py',original,'retained-v19',['--geometry'])
            paired('tools/verify_v21.py',original,'retained-v21',[])
            stage=OUT/'retained-stage'
            if stage.exists(): shutil.rmtree(stage)
            shutil.copytree(original,stage)
            # Cross-referenced Supplement S documents need both auxiliary passes.
            targets=[(stage,'main','retained/v21/main.tex','v21'),
                (stage/'retained/v18','main','retained/v21/retained/v18/main.tex','v18'),
                (stage/'complete','two_collision','retained/v21/complete/two_collision.tex','auxiliary'),
                (stage/'complete','main','retained/v21/complete/main.tex','smooth')]
            for pass_no in range(2):
                for directory,name,source,label in targets:
                    run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
                         name+'.tex'],directory,f'{label}-pass-{pass_no}')
            for directory,name,source,label in targets:
                inspect_pdf(directory,name,source,label)
        record['source_unchanged']=source_manifest()==before
        if not record['source_unchanged']:
            raise RuntimeError('qualification modified mathematical or tool sources')
        if record['source_commit'] and git('diff','--name-only','HEAD','--','.')!='':
            raise RuntimeError('tracked source changes during qualification')
        record['status']='passed'
    except Exception as exc:
        record['status']='failed';record['error']=str(exc)
    finally:
        record['source_manifest_sha256']=hashlib.sha256(
            json.dumps(before,sort_keys=True,separators=(',',':')).encode()).hexdigest()
        record['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        (OUT/'receipt.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
        print(json.dumps(record,sort_keys=True,indent=2))
    return 0 if record['status']=='passed' else 1

if __name__=='__main__': raise SystemExit(main())
