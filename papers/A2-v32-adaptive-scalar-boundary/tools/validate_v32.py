#!/usr/bin/env python3
"""Fail-closed v32 primary or exact-checkout fifteen-document qualification."""
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
RETAINED_TREE = 'ff74e5124141dc46b0f08f7e38a5cf258b87e642'
REVIEW = 'f2e2a13a9a742c412a4b1a59b43388a2ba385bda'
WORKFLOW = '.github/workflows/a2-v32-verify.yml'
REQUIRED = ('main.tex', 'references.tex', 'core/00_setting.tex',
            'core/01_local_queries.tex', 'core/02_adaptive_boundary.tex',
            'core/03_period_recognition.tex', 'core/04_information_bound.tex',
            'core/05_comparison.tex', 'tools/adaptive_scalar.py',
            'tools/verify_v32.py', 'tools/test_contract.py', 'tools/validate_v32.py')


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def manifest(root: Path = ROOT) -> dict[str, str]:
    paths = [root/'main.tex', root/'references.tex']
    paths += sorted((root/'core').glob('*.tex'))
    paths += sorted((root/'tools').glob('*.py'))
    return {str(p.relative_to(root)): digest(p) for p in paths}


def check_sources(root: Path = ROOT) -> dict:
    for name in (*REQUIRED, 'SOURCE_PINS.json'):
        if not (root/name).is_file():
            raise RuntimeError('missing required source: ' + name)
    pins = json.loads((root/'SOURCE_PINS.json').read_text())
    if (pins.get('schema') != 'a2-v32-source-pins-1' or pins.get('review_commit') != REVIEW
            or pins.get('retained_v31_tree') != RETAINED_TREE):
        raise RuntimeError('incorrect revision, review or retained-tree pin')
    if pins.get('source_sha256') != manifest(root):
        raise RuntimeError('source digest inventory incomplete or different')
    if not re.fullmatch('[0-9a-f]{64}', pins.get('workflow_sha256', '')):
        raise RuntimeError('workflow digest missing or malformed')
    if pins.get('full_package_document_count') != 15:
        raise RuntimeError('declared package must have fifteen documents')
    return pins


def require_commit(actual: str | None, expected: str | None) -> None:
    if expected is not None and (not re.fullmatch('[0-9a-f]{40}', expected) or actual != expected):
        raise RuntimeError('expected commit differs from checkout')


def retained_documents(receipt: dict, commit: str) -> list[dict]:
    if (receipt.get('status') != 'passed' or receipt.get('full_package_qualified') is not True
            or receipt.get('scope') != 'all_declared_volumes'
            or receipt.get('source_commit') != commit):
        raise RuntimeError('retained package is not qualified at current commit')
    docs = receipt.get('documents', []) + receipt.get('retained_documents', [])
    if len(docs) != 14 or receipt.get('declared_document_count') != 14:
        raise RuntimeError('retained package does not have fourteen qualified documents')
    for d in docs:
        if (type(d.get('pages')) is not int or d['pages'] < 1
                or not re.fullmatch('[0-9a-f]{64}', d.get('pdf_sha256', ''))):
            raise RuntimeError('incomplete retained PDF inventory')
    return docs


def output_path(root: Path, chosen: str) -> Path:
    p = (root/chosen).resolve()
    if not p.is_relative_to((root/'verification').resolve()):
        raise ValueError('output must be inside verification/')
    return p


def execution_kind(actual: str | None, required: bool, env: dict) -> str:
    if (actual and required and env.get('GITHUB_ACTIONS') == 'true'
            and env.get('GITHUB_RUN_ID') and env.get('GITHUB_SHA') == actual):
        return 'hosted_exact_checkout'
    return 'local_exact_checkout' if actual and required else 'source_content'


def git(*args: str) -> str | None:
    p = subprocess.run(['git', '-C', str(ROOT), *args], text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout.strip() if p.returncode == 0 else None


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--all-volumes', action='store_true')
    ap.add_argument('--require-checkout', action='store_true')
    ap.add_argument('--expected-commit')
    ap.add_argument('--output-dir', default='verification/current')
    args = ap.parse_args()
    out = output_path(ROOT, args.output_dir)
    out.mkdir(parents=True, exist_ok=True)
    actual = git('rev-parse', 'HEAD') if args.require_checkout else None
    record = {'schema': 'a2-v32-source-validation-1', 'status': 'running',
              'scope': 'all_declared_volumes' if args.all_volumes else 'primary_only',
              'source_commit': actual,
              'source_tree': git('rev-parse', 'HEAD^{tree}') if actual else None,
              'github_sha': os.getenv('GITHUB_SHA'), 'github_run_id': os.getenv('GITHUB_RUN_ID'),
              'execution_kind': execution_kind(actual, args.require_checkout, dict(os.environ)),
              'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
              'platform': platform.platform(), 'python': sys.version,
              'commands': [], 'documents': [], 'source_unchanged': False,
              'full_package_qualified': False, 'hosted_full_package_qualified': False,
              'physical_sensor_executed': False, 'formal_proof_certificate': False}

    def run(argv: list[str], cwd: Path, label: str) -> str:
        p = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, env={**os.environ,
                           'PYTHONDONTWRITEBYTECODE': '1', 'OPENBLAS_NUM_THREADS': '1',
                           'OMP_NUM_THREADS': '1', 'TERM': 'dumb'})
        path = out/(label+'.log'); path.write_text(p.stdout)
        record['commands'].append({'argv': argv, 'cwd': str(cwd.relative_to(ROOT)),
                                  'exit_code': p.returncode, 'log': path.name,
                                  'log_sha256': digest(path)})
        if p.returncode:
            raise RuntimeError(label + ': exit ' + str(p.returncode))
        return p.stdout

    try:
        pins = check_sources(); before = manifest()
        record['source_manifest'] = before
        record['source_pins_sha256'] = digest(ROOT/'SOURCE_PINS.json')
        if args.all_volumes and not args.require_checkout:
            raise RuntimeError('full qualification requires an exact checkout')
        require_commit(actual, args.expected_commit)
        require_commit(actual, record['github_sha'])
        if args.require_checkout:
            if not actual or git('diff', '--name-only', 'HEAD', '--', '.') != '':
                raise RuntimeError('clean tracked checkout required')
            prefix = git('rev-parse', '--show-prefix') or ''
            if git('rev-parse', 'HEAD:'+prefix+'retained/v31') != RETAINED_TREE:
                raise RuntimeError('retained v31 native tree mismatch')
            workflow = Path(git('rev-parse', '--show-toplevel') or '')/WORKFLOW
            if not workflow.is_file() or digest(workflow) != pins['workflow_sha256']:
                raise RuntimeError('workflow absent or changed')
            record['retained_tree_verified'] = RETAINED_TREE
        for script, label in [('verify_v32.py', 'mathematical-diagnostics'),
                              ('test_contract.py', 'validation-contract')]:
            normal = run([sys.executable, 'tools/'+script], ROOT, label+'-normal')
            optimized = run([sys.executable, '-O', 'tools/'+script], ROOT, label+'-optimized')
            if normal != optimized:
                raise RuntimeError('ordinary/optimized output mismatch: '+label)
            record[label] = json.loads(normal)
        record['normal_optimized_identical'] = True
        run(['pdflatex', '--version'], ROOT, 'tex-version')
        run(['latexmk', '-v'], ROOT, 'latexmk-version')
        run(['latexmk', '-g', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
             '-outdir=build', 'main.tex'], ROOT, 'primary-build')
        pdf, log = ROOT/'build/main.pdf', ROOT/'build/main.log'
        warnings = re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                              log.read_text(errors='replace'), re.M)
        info = run(['pdfinfo', str(pdf)], ROOT, 'primary-pdfinfo')
        match = re.search(r'^Pages:\s+(\d+)', info, re.M)
        if not match or warnings:
            raise RuntimeError('primary PDF/TeX qualification failed: '+str(warnings))
        record['documents'] = [{'source': 'main.tex', 'pdf': 'build/main.pdf',
            'pages': int(match.group(1)), 'pdf_sha256': digest(pdf),
            'tex_log_sha256': digest(log), 'final_tex_diagnostics': warnings,
            'layout_wrapper_applied': False}]
        record['declared_document_count'] = 1
        if args.all_volumes:
            retained = ROOT/'retained/v31'
            run([sys.executable, 'tools/validate_v31.py', '--all-volumes', '--require-checkout',
                 '--expected-commit', actual, '--output-dir', 'verification/v32-requalification'],
                retained, 'retained-v31-full-package')
            path = retained/'verification/v32-requalification/receipt.json'
            nested = json.loads(path.read_text())
            record['retained_documents'] = retained_documents(nested, actual)
            record['retained_receipt'] = {'path': str(path.relative_to(ROOT)),
                                         'sha256': digest(path), 'receipt': nested}
            record['declared_document_count'] = 15
            record['historical_layout_policy'] = ('Original warnings and disclosed stage-only '
                'wrappers remain in nested receipts; no retained mathematical source is edited.')
        if manifest() != before:
            raise RuntimeError('validation changed mathematical/tool sources')
        if args.require_checkout and git('diff', '--name-only', 'HEAD', '--', '.') != '':
            raise RuntimeError('validation changed tracked sources')
        record['source_unchanged'] = True
        record['full_package_qualified'] = bool(args.all_volumes)
        record['hosted_full_package_qualified'] = bool(args.all_volumes and
                                                     record['execution_kind']=='hosted_exact_checkout')
        record['status'] = 'passed'
    except Exception as exc:
        record['status'] = 'failed'; record['error'] = str(exc)
        record['full_package_qualified'] = False; record['hosted_full_package_qualified'] = False
    finally:
        record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
        print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if record['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
