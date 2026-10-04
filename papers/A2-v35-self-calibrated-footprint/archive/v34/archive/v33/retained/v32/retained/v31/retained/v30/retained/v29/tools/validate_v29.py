#!/usr/bin/env python3
"""Fail-closed qualification of A2 v29 and eleven unchanged retained documents."""
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
RETAINED_TREE = 'b17c9c051f3e279d6f7610e3d1c5e56d0733216a'
WORKFLOW = '.github/workflows/a2-v29-verify.yml'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    result = subprocess.run(['git','-C',str(ROOT),*args], text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.stdout.strip() if result.returncode == 0 else None


def manifest(root: Path = ROOT) -> dict[str, str]:
    paths = [root/'main.tex', root/'references.tex']
    paths += sorted((root/'core').glob('*.tex'))
    paths += sorted((root/'tools').glob('*.py'))
    return {str(p.relative_to(root)): digest(p) for p in paths}


def check_sources(root: Path = ROOT) -> dict:
    required = ['SOURCE_PINS.json','main.tex','references.tex','core/01_reversal.tex',
                'core/02_local_acquisition.tex','core/03_periods.tex',
                'core/04_finite_experiment.tex','core/05_comparison.tex',
                'tools/verify_v29.py','tools/validate_v29.py','tools/test_contract.py']
    for name in required:
        if not (root/name).is_file():
            raise RuntimeError('missing required source: '+name)
    pins = json.loads((root/'SOURCE_PINS.json').read_text())
    if pins.get('schema') != 'a2-v29-source-pins-1':
        raise RuntimeError('incorrect source-pin schema')
    if pins.get('source_sha256') != manifest(root):
        raise RuntimeError('source manifest differs or is incompletely pinned')
    if pins.get('retained_v28_tree') != RETAINED_TREE:
        raise RuntimeError('retained source pin differs')
    return pins


def require_commit(actual: str | None, expected: str | None) -> None:
    if expected is not None and (not re.fullmatch(r'[0-9a-f]{40}', expected) or actual != expected):
        raise RuntimeError('expected commit differs from actual checkout')


def retained_documents(receipt: dict, commit: str) -> list[dict]:
    if (receipt.get('status') != 'passed' or not receipt.get('full_package_qualified')
        or receipt.get('scope') != 'all_declared_volumes' or receipt.get('source_commit') != commit):
        raise RuntimeError('retained package lacks a current exact-source full pass')
    docs = receipt.get('documents', []) + receipt.get('retained_documents', [])
    if len(docs) != 11 or receipt.get('declared_document_count') != 11:
        raise RuntimeError('retained document inventory is not eleven')
    for doc in docs:
        if not isinstance(doc.get('pages'), int) or doc['pages'] < 1 or not doc.get('pdf_sha256'):
            raise RuntimeError('incomplete retained PDF record')
    return docs


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--all-volumes', action='store_true')
    ap.add_argument('--require-checkout', action='store_true')
    ap.add_argument('--expected-commit')
    ap.add_argument('--output-dir', default='verification/current')
    args = ap.parse_args()
    out = (ROOT/args.output_dir).resolve()
    if not out.is_relative_to((ROOT/'verification').resolve()):
        raise ValueError('output must remain within verification/')
    out.mkdir(parents=True, exist_ok=True)
    actual = git('rev-parse','HEAD') if args.require_checkout else None
    record = {'schema':'a2-v29-source-validation-1','status':'running',
        'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope':'all_declared_volumes' if args.all_volumes else 'primary_only',
        'source_commit':actual, 'source_tree':git('rev-parse','HEAD^{tree}') if actual else None,
        'github_sha':os.getenv('GITHUB_SHA'), 'github_run_id':os.getenv('GITHUB_RUN_ID'),
        'platform':platform.platform(), 'python':sys.version, 'commands':[], 'documents':[],
        'source_unchanged':False, 'full_package_qualified':False,
        'hosted_full_package_qualified':False, 'formal_proof_certificate':False,
        'physical_sensor_executed':False}
    hosted = bool(os.getenv('GITHUB_ACTIONS') == 'true' and record['github_run_id']
                  and args.require_checkout and record['github_sha'] == actual and actual)
    record['execution_kind'] = ('hosted_exact_checkout' if hosted else
                                'local_exact_checkout' if actual else 'source_content')

    def run(argv: list[str], cwd: Path, label: str) -> str:
        p = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        log = out/(label+'.log'); log.write_text(p.stdout)
        record['commands'].append({'argv':argv,'cwd':str(cwd.relative_to(ROOT)),
            'exit_code':p.returncode,'log':log.name,'log_sha256':digest(log)})
        if p.returncode:
            raise RuntimeError(label+': exit '+str(p.returncode))
        return p.stdout

    try:
        pins = check_sources(); before = manifest()
        record['source_manifest'] = before
        record['source_pins_sha256'] = digest(ROOT/'SOURCE_PINS.json')
        if args.all_volumes and not args.require_checkout:
            raise RuntimeError('full package requires exact checkout validation')
        require_commit(actual, args.expected_commit)
        require_commit(actual, record['github_sha'])
        if args.require_checkout:
            if not actual or git('diff','--name-only','HEAD','--','.') != '':
                raise RuntimeError('clean tracked checkout is required')
            prefix = git('rev-parse','--show-prefix') or ''
            if git('rev-parse','HEAD:'+prefix+'retained/v28') != RETAINED_TREE:
                raise RuntimeError('retained v28 native tree differs')
            top = Path(git('rev-parse','--show-toplevel') or '')
            if not (top/WORKFLOW).is_file() or digest(top/WORKFLOW) != pins['workflow_sha256']:
                raise RuntimeError('workflow absent or pin mismatch')
            record['retained_tree_verified'] = RETAINED_TREE
        for script, label in [('verify_v29.py','mathematical-diagnostics'),
                               ('test_contract.py','validation-contract')]:
            normal = run([sys.executable,'tools/'+script], ROOT, label+'-normal')
            optimized = run([sys.executable,'-O','tools/'+script], ROOT, label+'-optimized')
            if normal != optimized:
                raise RuntimeError('normal and optimized output differ: '+label)
            record[label] = json.loads(normal)
        record['normal_optimized_identical'] = True
        run(['pdflatex','--version'], ROOT, 'tex-version')
        run(['latexmk','-v'], ROOT, 'latexmk-version')
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-outdir=build','main.tex'], ROOT, 'primary-build')
        log, pdf = ROOT/'build/main.log', ROOT/'build/main.pdf'
        diagnostics = re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                                  log.read_text(errors='replace'), re.M)
        info = run(['pdfinfo',str(pdf)], ROOT, 'primary-pdfinfo')
        pages = re.search(r'^Pages:\s+(\d+)', info, re.M)
        if not pages:
            raise RuntimeError('missing PDF page inventory')
        record['documents'].append({'source':'main.tex','pdf':'build/main.pdf',
            'pages':int(pages.group(1)), 'pdf_sha256':digest(pdf),
            'tex_log_sha256':digest(log), 'final_tex_diagnostics':diagnostics,
            'layout_wrapper_applied':False})
        if diagnostics:
            raise RuntimeError('primary has final TeX diagnostics')
        record['declared_document_count'] = 1
        if args.all_volumes:
            inherited = ROOT/'retained/v28'
            run([sys.executable,'tools/validate_v28.py','--all-volumes','--require-checkout',
                 '--expected-commit',actual,'--output-dir','verification/v29-requalification'],
                inherited, 'retained-v28-full-package')
            path = inherited/'verification/v29-requalification/receipt.json'
            nested = json.loads(path.read_text())
            record['retained_documents'] = retained_documents(nested, actual)
            record['retained_receipt'] = {'path':str(path.relative_to(ROOT)),
                'sha256':digest(path),'receipt':nested}
            record['declared_document_count'] = 12
            record['historical_layout_policy'] = ('Retained drivers preserve raw layout warnings '
                'and any disclosed stage-only wrappers. No inherited mathematical source is edited.')
        if manifest() != before:
            raise RuntimeError('mathematical or tool sources changed during execution')
        if args.require_checkout and git('diff','--name-only','HEAD','--','.') != '':
            raise RuntimeError('tracked source changed during execution')
        record['source_unchanged'] = True
        record['full_package_qualified'] = bool(args.all_volumes)
        record['hosted_full_package_qualified'] = bool(args.all_volumes and hosted)
        record['status'] = 'passed'
    except Exception as exc:
        record['status'] = 'failed'; record['error'] = str(exc)
        record['full_package_qualified'] = False
        record['hosted_full_package_qualified'] = False
    finally:
        record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps(record,indent=2,sort_keys=True))
    return 0 if record['status'] == 'passed' else 1

if __name__ == '__main__':
    raise SystemExit(main())
