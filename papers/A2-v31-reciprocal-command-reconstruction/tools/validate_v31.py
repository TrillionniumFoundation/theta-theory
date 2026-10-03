#!/usr/bin/env python3
"""Fail-closed A2 v31 qualification; full mode delegates the exact retained tree."""
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

ROOT = Path(__file__).resolve().parents[1]
RETAINED_TREE = '1a6f8f32ec62aec586883e67753b3a72895f875c'
WORKFLOW = '.github/workflows/a2-v31-verify.yml'
REQUIRED = ('main.tex','references.tex','core/00_overview.tex','core/01_reversal.tex',
            'core/02_local_acquisition.tex','core/03_periods.tex','core/04_finite_experiment.tex',
            'core/05_comparison.tex','core/06_calibrated_launches.tex',
            'core/07_constructive_patch.tex','core/08_hit_functionals.tex',
            'tools/reconstruct_scalar.py','tools/reciprocal_intervals.py',
            'tools/verify_v31.py','tools/validate_v31.py','tools/test_v31_contract.py',
            'core/00a_reciprocal_overview.tex','core/09_mean_exit_inverse.tex',
            'core/10_pooled_finite_experiment.tex')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    p = subprocess.run(['git','-C',str(ROOT),*args],text=True,
                       stdout=subprocess.PIPE,stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode == 0 else None


def manifest(root: Path = ROOT) -> dict[str,str]:
    paths = [root/'main.tex',root/'references.tex']
    paths += sorted((root/'core').glob('*.tex'))
    paths += sorted((root/'tools').glob('*.py'))
    return {str(p.relative_to(root)):digest(p) for p in paths}


def check_sources(root: Path = ROOT) -> dict:
    for name in (*REQUIRED,'SOURCE_PINS.json'):
        if not (root/name).is_file():
            raise RuntimeError('missing required file: '+name)
    pins = json.loads((root/'SOURCE_PINS.json').read_text())
    if pins.get('schema') != 'a2-v31-source-pins-1':
        raise RuntimeError('incorrect source-pin schema')
    if pins.get('retained_v30_tree') != RETAINED_TREE:
        raise RuntimeError('incorrect retained native tree pin')
    if pins.get('source_sha256') != manifest(root):
        raise RuntimeError('source manifest differs or is incomplete')
    if not re.fullmatch('[0-9a-f]{64}',pins.get('workflow_sha256','')):
        raise RuntimeError('workflow hash missing or malformed')
    for name, expected in pins.get('retained_active_core_sha256', {}).items():
        if digest(root/name) != expected:
            raise RuntimeError('retained active core modified: '+name)
    if len(pins.get('retained_active_core_sha256', {})) != 9:
        raise RuntimeError('retained active core inventory is not nine')
    return pins


def require_commit(actual: str | None, expected: str | None) -> None:
    if expected is not None and (not re.fullmatch('[0-9a-f]{40}',expected) or actual != expected):
        raise RuntimeError('expected SHA differs from actual checkout')


def retained_documents(receipt: dict, commit: str) -> list[dict]:
    if (receipt.get('status') != 'passed' or receipt.get('full_package_qualified') is not True
            or receipt.get('scope') != 'all_declared_volumes'
            or receipt.get('source_commit') != commit):
        raise RuntimeError('retained package lacks a current full qualification')
    docs = receipt.get('documents',[]) + receipt.get('retained_documents',[])
    if len(docs) != 13 or receipt.get('declared_document_count') != 13:
        raise RuntimeError('retained document inventory is not thirteen')
    for d in docs:
        if (type(d.get('pages')) is not int or d['pages'] < 1
                or not re.fullmatch('[0-9a-f]{64}',d.get('pdf_sha256',''))):
            raise RuntimeError('incomplete retained PDF qualification')
    return docs


def execution_kind(actual: str | None, require_checkout: bool, env: dict) -> str:
    if (actual and require_checkout and env.get('GITHUB_ACTIONS') == 'true'
            and env.get('GITHUB_RUN_ID') and env.get('GITHUB_SHA') == actual):
        return 'hosted_exact_checkout'
    return 'local_exact_checkout' if actual and require_checkout else 'source_content'


def output_path(root: Path, selected: str) -> Path:
    path = (root/selected).resolve()
    if not path.is_relative_to((root/'verification').resolve()):
        raise ValueError('output must be inside verification/')
    return path


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--all-volumes',action='store_true')
    ap.add_argument('--require-checkout',action='store_true')
    ap.add_argument('--expected-commit')
    ap.add_argument('--output-dir',default='verification/current')
    args = ap.parse_args()
    out = output_path(ROOT,args.output_dir); out.mkdir(parents=True,exist_ok=True)
    actual = git('rev-parse','HEAD') if args.require_checkout else None
    record = {'schema':'a2-v31-source-validation-1','status':'running',
        'scope':'all_declared_volumes' if args.all_volumes else 'primary_only',
        'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'source_commit':actual,'source_tree':git('rev-parse','HEAD^{tree}') if actual else None,
        'github_sha':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID'),
        'execution_kind':execution_kind(actual,args.require_checkout,dict(os.environ)),
        'platform':platform.platform(),'python':sys.version,'commands':[],'documents':[],
        'source_unchanged':False,'full_package_qualified':False,
        'hosted_full_package_qualified':False,'physical_sensor_executed':False,
        'formal_proof_certificate':False}

    def run(argv: list[str], cwd: Path, label: str) -> str:
        p = subprocess.run(argv,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,
                           env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1',
                                'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','TERM':'dumb'})
        path = out/(label+'.log'); path.write_text(p.stdout)
        record['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
                                   'exit_code':p.returncode,'log':path.name,'log_sha256':digest(path)})
        if p.returncode:
            raise RuntimeError(label+': exit '+str(p.returncode))
        return p.stdout

    try:
        pins = check_sources(); before = manifest()
        record['source_manifest'] = before
        record['source_pins_sha256'] = digest(ROOT/'SOURCE_PINS.json')
        if args.all_volumes and not args.require_checkout:
            raise RuntimeError('full qualification requires exact checkout')
        require_commit(actual,args.expected_commit)
        require_commit(actual,record['github_sha'])
        if args.require_checkout:
            if not actual or git('diff','--name-only','HEAD','--','.') != '':
                raise RuntimeError('clean tracked checkout required')
            prefix = git('rev-parse','--show-prefix') or ''
            if git('rev-parse','HEAD:'+prefix+'retained/v30') != RETAINED_TREE:
                raise RuntimeError('retained native tree mismatch')
            workflow = Path(git('rev-parse','--show-toplevel') or '')/WORKFLOW
            if not workflow.is_file() or digest(workflow) != pins['workflow_sha256']:
                raise RuntimeError('workflow absent or modified')
            for name in pins['retained_active_core_sha256']:
                old_blob = git('rev-parse','HEAD:'+prefix+'retained/v30/'+name)
                if git('hash-object',str(ROOT/name)) != old_blob:
                    raise RuntimeError('active core differs from retained checkout: '+name)
            record['retained_tree_verified'] = RETAINED_TREE
        for script,label in [('verify_v31.py','mathematical-diagnostics'),
                             ('test_v31_contract.py','validation-contract')]:
            normal = run([sys.executable,'tools/'+script],ROOT,label+'-normal')
            optimized = run([sys.executable,'-O','tools/'+script],ROOT,label+'-optimized')
            if normal != optimized:
                raise RuntimeError('normal/optimized output mismatch: '+label)
            record[label] = json.loads(normal)
        record['normal_optimized_identical'] = True
        run(['pdflatex','--version'],ROOT,'tex-version')
        run(['latexmk','-v'],ROOT,'latexmk-version')
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-outdir=build','main.tex'],ROOT,'primary-build')
        pdf,log = ROOT/'build/main.pdf',ROOT/'build/main.log'
        diagnostics = re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                                  log.read_text(errors='replace'),re.M)
        info = run(['pdfinfo',str(pdf)],ROOT,'primary-pdfinfo')
        pages = re.search(r'^Pages:\s+(\d+)',info,re.M)
        if not pages or diagnostics:
            raise RuntimeError('primary PDF inventory or final TeX diagnostics failed: '+str(diagnostics))
        record['documents'].append({'source':'main.tex','pdf':'build/main.pdf',
            'pages':int(pages.group(1)),'pdf_sha256':digest(pdf),
            'tex_log_sha256':digest(log),'final_tex_diagnostics':diagnostics,
            'layout_wrapper_applied':False})
        record['declared_document_count'] = 1
        if args.all_volumes:
            inherited = ROOT/'retained/v30'
            run([sys.executable,'tools/validate_v30.py','--all-volumes','--require-checkout',
                 '--expected-commit',actual,'--output-dir','verification/v31-requalification'],
                inherited,'retained-v30-full-package')
            path = inherited/'verification/v31-requalification/receipt.json'
            nested = json.loads(path.read_text())
            record['retained_documents'] = retained_documents(nested,actual)
            record['retained_receipt'] = {'path':str(path.relative_to(ROOT)),
                'sha256':digest(path),'receipt':nested}
            record['declared_document_count'] = 14
            record['historical_layout_policy'] = ('Inherited raw warnings and disclosed stage-only '
                'wrappers remain in nested receipts; no retained mathematical source is edited.')
        if manifest() != before:
            raise RuntimeError('validation changed mathematical or tool sources')
        if args.require_checkout and git('diff','--name-only','HEAD','--','.') != '':
            raise RuntimeError('validation changed tracked sources')
        record['source_unchanged'] = True
        record['full_package_qualified'] = bool(args.all_volumes)
        record['hosted_full_package_qualified'] = bool(args.all_volumes and
            record['execution_kind'] == 'hosted_exact_checkout')
        record['status'] = 'passed'
    except Exception as exc:
        record['status'] = 'failed'; record['error'] = str(exc)
        record['full_package_qualified'] = False; record['hosted_full_package_qualified'] = False
    finally:
        record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps(record,indent=2,sort_keys=True))
    return 0 if record['status'] == 'passed' else 1

if __name__ == '__main__':
    raise SystemExit(main())
