#!/usr/bin/env python3
"""Fail-closed exact-source qualification of the primary and ten retained volumes."""
from __future__ import annotations
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import subprocess
import sys

ROOT=Path(__file__).resolve().parents[1]
RETAINED_TREE='c9e18bc786b795e61a6ed8c0048249bb14713a04'
WORKFLOW='.github/workflows/a2-v28-verify.yml'


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    p=subprocess.run(['git','-C',str(ROOT),*args],text=True,
                     stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode==0 else None


def manifest(root: Path=ROOT) -> dict[str,str]:
    paths=[root/'main.tex',root/'references.tex']
    paths+=sorted((root/'core').glob('*.tex'))
    paths+=sorted((root/'tools').glob('*.py'))
    return {str(p.relative_to(root)):sha(p) for p in paths}


def check_sources(root: Path=ROOT) -> dict:
    required=['SOURCE_PINS.json','main.tex','references.tex','tools/verify_v28.py',
              'tools/validate_v28.py','tools/test_validation_contract.py',
              'core/00_local_period_recognition.tex']
    for name in required:
        if not (root/name).is_file():
            raise RuntimeError('required source is absent: '+name)
    pins=json.loads((root/'SOURCE_PINS.json').read_text())
    if pins['schema']!='a2-v28-source-pins-1':
        raise RuntimeError('incorrect source-pin schema')
    if pins['source_sha256']!=manifest(root):
        raise RuntimeError('manifest is not exactly covered by source pins')
    for name,expected in pins['retained_active_core_blobs'].items():
        b=(root/name).read_bytes()
        if hashlib.sha1(f'blob {len(b)}\0'.encode()+b).hexdigest()!=expected:
            raise RuntimeError('a retained active core was changed: '+name)
    return pins


def require_commit(actual: str | None, expected: str | None) -> None:
    if expected is not None:
        if not re.fullmatch(r'[0-9a-f]{40}',expected) or actual!=expected:
            raise RuntimeError('expected commit differs from actual checkout')


def check_nested(nested: dict, commit: str) -> None:
    if (nested.get('status')!='passed' or nested.get('scope')!='all_declared_volumes'
        or not nested.get('full_package_qualified') or nested.get('source_commit')!=commit):
        raise RuntimeError('retained package lacks a current exact-source full pass')


def document_list(receipt: dict, scope: str='retained/v27') -> list[dict]:
    result=[{'scope':scope,**d} for d in receipt.get('documents',[])]
    for key in ('inherited_receipt','nested_receipt'):
        child=receipt.get(key)
        if isinstance(child,dict):
            result+=document_list(child,scope+'/'+key)
    return result


def main() -> int:
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--all-volumes',action='store_true')
    ap.add_argument('--require-checkout',action='store_true')
    ap.add_argument('--expected-commit')
    ap.add_argument('--output-dir',default='verification/current')
    args=ap.parse_args()
    out=(ROOT/args.output_dir).resolve()
    if not out.is_relative_to(ROOT/'verification'):
        raise ValueError('output must be under verification/')
    out.mkdir(parents=True,exist_ok=True)
    record={'schema':'a2-v28-source-validation-1','status':'running',
      'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
      'scope':'all_declared_volumes' if args.all_volumes else 'primary_only',
      'source_commit':git('rev-parse','HEAD') if args.require_checkout else None,
      'source_tree':git('rev-parse','HEAD^{tree}') if args.require_checkout else None,
      'git_context_commit':git('rev-parse','HEAD'),
      'github_sha':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID'),
      'runner_image':os.getenv('ImageOS'),'runner_image_version':os.getenv('ImageVersion'),
      'platform':platform.platform(),'python':sys.version,'commands':[],'documents':[],
      'source_unchanged':False,'full_package_qualified':False,
      'hosted_full_package_qualified':False,'formal_proof_certificate':False,
      'physical_sensor_executed':False}
    hosted=(os.getenv('GITHUB_ACTIONS')=='true' and bool(record['github_run_id'])
            and args.require_checkout)
    record['execution_kind']=('hosted_exact_checkout' if hosted else
        ('local_validation_snapshot' if record['source_commit'] else 'source_content'))

    def run(argv: list[str],cwd: Path,label: str) -> str:
        p=subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        log=out/(label+'.log'); log.write_text(p.stdout)
        record['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
            'exit_code':p.returncode,'log':log.name,'log_sha256':sha(log)})
        if p.returncode:
            raise RuntimeError(label+': exit '+str(p.returncode))
        return p.stdout

    try:
        pins=check_sources(); before=manifest()
        record['source_manifest']=before
        record['source_pins_sha256']=sha(ROOT/'SOURCE_PINS.json')
        if args.all_volumes and not args.require_checkout:
            raise RuntimeError('all-volume qualification requires a checked source snapshot')
        require_commit(record['source_commit'],args.expected_commit)
        require_commit(record['source_commit'],record['github_sha'])
        if args.require_checkout:
            if not record['source_commit'] or git('diff','--name-only','HEAD','--','.')!='':
                raise RuntimeError('clean tracked source checkout required')
            prefix=git('rev-parse','--show-prefix') or ''
            if git('rev-parse','HEAD:'+prefix+'retained/v27')!=RETAINED_TREE:
                raise RuntimeError('retained v27 native tree differs')
            top=Path(git('rev-parse','--show-toplevel') or '')
            if not (top/WORKFLOW).is_file() or sha(top/WORKFLOW)!=pins['workflow_sha256']:
                raise RuntimeError('workflow is absent or does not match its pin')
            record['verified_retained_tree']=RETAINED_TREE
            record['workflow_sha256']=pins['workflow_sha256']
        for script,label in [('verify_v28.py','v28-diagnostics'),
                             ('test_validation_contract.py','validation-contract')]:
            normal=run([sys.executable,'tools/'+script],ROOT,label+'-normal')
            optimized=run([sys.executable,'-O','tools/'+script],ROOT,label+'-optimized')
            if normal!=optimized:
                raise RuntimeError(label+': ordinary and optimized outputs differ')
            record[label]=json.loads(normal)
        record['normal_optimized_identical']=True
        run(['pdflatex','--version'],ROOT,'tex-version')
        run(['latexmk','-v'],ROOT,'latexmk-version')
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-outdir=build','main.tex'],ROOT,'primary-build')
        log=ROOT/'build/main.log'; pdf=ROOT/'build/main.pdf'
        diagnostics=re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                               log.read_text(errors='replace'),re.M)
        info=run(['pdfinfo',str(pdf)],ROOT,'primary-pdfinfo')
        pages=re.search(r'^Pages:\s+(\d+)',info,re.M)
        record['documents'].append({'source':'main.tex','pdf':'build/main.pdf',
            'pages':int(pages.group(1)) if pages else None,'pdf_sha256':sha(pdf),
            'tex_log_sha256':sha(log),'final_tex_diagnostics':diagnostics,
            'layout_wrapper_applied':False})
        if diagnostics:
            raise RuntimeError('primary has final TeX diagnostics')
        if args.all_volumes:
            inherited=ROOT/'retained/v27'
            run([sys.executable,'tools/validate_v27.py','--all-volumes',
                '--require-checkout','--expected-commit',record['source_commit'],
                '--output-dir','verification/v28-requalification'],
                inherited,'retained-v27-all-volumes')
            path=inherited/'verification/v28-requalification/receipt.json'
            nested=json.loads(path.read_text())
            check_nested(nested,record['source_commit'])
            record['retained_receipt']={'path':str(path.relative_to(ROOT)),
                'sha256':sha(path),'receipt':nested}
            docs=document_list(nested)
            if len(docs)!=10:
                raise RuntimeError('retained declared document count is not ten')
            record['retained_documents']=docs
            record['declared_document_count']=1+len(docs)
            record['historical_layout_policy']=(
                'unchanged inherited drivers retain raw layout warnings and their '
                'disclosed stage-only wrappers; mathematical sources are not rewritten')
        if manifest()!=before:
            raise RuntimeError('qualification changed mathematical or tool sources')
        if args.require_checkout and git('diff','--name-only','HEAD','--','.')!='':
            raise RuntimeError('qualification changed tracked source')
        record['source_unchanged']=True
        record['full_package_qualified']=bool(args.all_volumes)
        record['hosted_full_package_qualified']=bool(args.all_volumes and hosted
             and args.require_checkout and record['github_sha']==record['source_commit'])
        record['status']='passed'
    except Exception as exc:
        record['status']='failed'; record['error']=str(exc)
        record['full_package_qualified']=False
        record['hosted_full_package_qualified']=False
    finally:
        record['finished_utc']=dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps(record,indent=2,sort_keys=True))
    return 0 if record['status']=='passed' else 1

if __name__=='__main__':
    raise SystemExit(main())
