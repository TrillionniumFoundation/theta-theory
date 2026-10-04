#!/usr/bin/env python3
"""Fail-closed A2 v27 source qualification, with explicit historical scopes.

All-volume mode requires a clean checkout and executes every declared build.
A missing driver is an error, never a successful archive-only substitute.
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
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]
SNAPSHOTS = {
    'retained/v26': 'eb47d317f691162303de1686f6c9233cb9d8ccb4',
    'retained/v25': 'c48d900f6596eea1e8df1f729481674fb1bf6175',
    'complete': '14b2e5379e5b223bc0bdc823c97fd77c2dca2cda',
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str | None:
    result = subprocess.run(['git', '-C', str(ROOT), *args], text=True,
                            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return result.stdout.strip() if result.returncode == 0 else None


def manifest(root: Path = ROOT) -> dict[str, str]:
    paths = [root/'main.tex', root/'references.tex']
    paths += sorted((root/'core').glob('*.tex'))
    paths += sorted((root/'tools').glob('*.py'))
    return {str(p.relative_to(root)): sha(p) for p in paths}


def check_sources(root: Path = ROOT) -> dict:
    required = ['SOURCE_PINS.json', 'tools/verify_v27.py', 'tools/validate_v27.py',
                'tools/test_validation_contract.py', 'core/00_fixed_aperture.tex']
    for name in required:
        if not (root/name).is_file():
            raise RuntimeError('required source is absent: '+name)
    pins = json.loads((root/'SOURCE_PINS.json').read_text())
    if pins['schema'] != 'a2-v27-source-pins-1':
        raise RuntimeError('wrong source-pin schema')
    if pins['source_sha256'] != manifest(root):
        raise RuntimeError('source pins do not exactly cover the current manifest')
    return pins


def require_expected_commit(actual: str | None, expected: str | None) -> None:
    if expected is not None and actual != expected:
        raise RuntimeError('expected commit differs from the actual checkout')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--all-volumes', action='store_true')
    parser.add_argument('--require-checkout', action='store_true')
    parser.add_argument('--expected-commit')
    parser.add_argument('--output-dir', default='verification/current')
    args = parser.parse_args()
    out = (ROOT/args.output_dir).resolve()
    if not out.is_relative_to(ROOT/'verification'):
        raise ValueError('output must be below verification/')
    out.mkdir(parents=True, exist_ok=True)
    record = {'schema': 'a2-v27-source-validation-1', 'status': 'running',
        'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(),
        'scope': 'all_declared_volumes' if args.all_volumes else 'primary_only',
        'full_package_qualified': False, 'hosted_full_package_qualified': False,
        'source_commit': git('rev-parse', 'HEAD'),
        'source_tree': git('rev-parse', 'HEAD^{tree}'),
        'github_sha': os.getenv('GITHUB_SHA'), 'github_run_id': os.getenv('GITHUB_RUN_ID'),
        'runner_image': os.getenv('ImageOS'), 'runner_image_version': os.getenv('ImageVersion'),
        'platform': platform.platform(), 'python': sys.version,
        'commands': [], 'documents': [], 'physical_sensor_executed': False,
        'formal_proof_certificate': False}
    record['execution_kind'] = ('hosted_exact_checkout' if record['github_run_id']
        else ('local_validation_checkout' if record['source_commit']
              else 'source_content_not_git_checkout'))

    def run(argv: list[str], cwd: Path, label: str) -> str:
        result = subprocess.run(argv, cwd=cwd, text=True, stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1', 'TERM': 'dumb'})
        log = out/(label+'.log')
        log.write_text(result.stdout)
        record['commands'].append({'argv': argv, 'cwd': str(cwd.relative_to(ROOT)),
            'exit_code': result.returncode, 'log': log.name, 'log_sha256': sha(log)})
        if result.returncode:
            raise RuntimeError(label+': exit '+str(result.returncode))
        return result.stdout

    def build(cwd: Path, output: Path, name: str) -> None:
        output.mkdir(parents=True, exist_ok=True)
        run(['latexmk', '-g', '-pdf', '-interaction=nonstopmode', '-halt-on-error',
             '-outdir='+str(output), 'main.tex'], cwd, name+'-build')
        pdf, log = output/'main.pdf', output/'main.log'
        diagnostics = re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                                log.read_text(errors='replace'), re.M)
        info = run(['pdfinfo', str(pdf)], ROOT, name+'-pdfinfo')
        pages = re.search(r'^Pages:\s+(\d+)', info, re.M)
        record['documents'].append({'source': str((cwd/'main.tex').relative_to(ROOT)),
            'pages': int(pages.group(1)) if pages else None,
            'pdf': str(pdf.relative_to(ROOT)), 'pdf_sha256': sha(pdf),
            'tex_log_sha256': sha(log), 'final_tex_diagnostics': diagnostics,
            'layout_wrapper_applied': False})
        if diagnostics:
            raise RuntimeError(name+': final TeX diagnostics remain')

    try:
        check_sources()
        before = manifest()
        record['source_manifest'] = before
        record['source_pins_sha256'] = sha(ROOT/'SOURCE_PINS.json')
        if args.all_volumes and not args.require_checkout:
            raise RuntimeError('all-volume qualification requires --require-checkout')
        require_expected_commit(record['source_commit'], args.expected_commit)
        require_expected_commit(record['source_commit'], record['github_sha'])
        if args.require_checkout:
            if not record['source_commit'] or git('diff', '--name-only', 'HEAD', '--', '.') != '':
                raise RuntimeError('a clean tracked Git checkout is required')
            prefix = git('rev-parse', '--show-prefix') or ''
            for name, expected in SNAPSHOTS.items():
                if git('rev-parse', 'HEAD:'+prefix+name) != expected:
                    raise RuntimeError('retained native tree differs: '+name)
            record['verified_retained_trees'] = SNAPSHOTS
        pairs = [('verify_v27.py', 'v27-diagnostics'),
                 ('test_validation_contract.py', 'validation-contract')]
        for script, label in pairs:
            normal = run([sys.executable, 'tools/'+script], ROOT, label+'-normal')
            optimized = run([sys.executable, '-O', 'tools/'+script], ROOT, label+'-optimized')
            if normal != optimized:
                raise RuntimeError(label+': normal and optimized output differ')
            record[label] = json.loads(normal)
        record['normal_optimized_identical'] = True
        run(['pdflatex', '--version'], ROOT, 'tex-version')
        run(['latexmk', '-v'], ROOT, 'latexmk-version')
        build(ROOT, ROOT/'build', 'primary')
        if args.all_volumes:
            build(ROOT/'retained/v26', out/'v26-build', 'reviewed-v26')
            inherited = ROOT/'retained/v25'
            inherited_output = 'verification/v27-requalification'
            run([sys.executable, 'tools/validate_v25.py', '--all-volumes',
                 '--require-checkout', '--output-dir', inherited_output],
                inherited, 'inherited-v25-driver')
            path = inherited/inherited_output/'receipt.json'
            nested = json.loads(path.read_text())
            if (nested.get('status') != 'passed' or nested.get('scope') != 'all_declared_volumes'
                    or nested.get('source_commit') != record['source_commit']):
                raise RuntimeError('inherited receipt does not bind current all-volume success')
            record['inherited_receipt'] = {'path': str(path.relative_to(ROOT)),
                'sha256': sha(path), 'schema': nested['schema'],
                'source_commit': nested['source_commit'], 'documents': nested['documents'],
                'nested_receipt': nested.get('inherited_receipt')}
            record['historical_layout_policy'] = (
                'unchanged v24/v25 drivers; raw historical diagnostics and disclosed '
                'reversible stage-only layout wrappers are retained in their receipts')
        if manifest() != before:
            raise RuntimeError('qualification modified mathematical or tool sources')
        if args.require_checkout and git('diff', '--name-only', 'HEAD', '--', '.') != '':
            raise RuntimeError('qualification modified tracked files')
        record['source_unchanged'] = True
        record['full_package_qualified'] = bool(args.all_volumes)
        record['hosted_full_package_qualified'] = bool(args.all_volumes and record['github_run_id'])
        record['status'] = 'passed'
    except Exception as exc:
        record['status'] = 'failed'
        record['error'] = str(exc)
        record['full_package_qualified'] = False
        record['hosted_full_package_qualified'] = False
    finally:
        record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        (out/'receipt.json').write_text(json.dumps(record, indent=2, sort_keys=True)+'\n')
        print(json.dumps(record, indent=2, sort_keys=True))
    return 0 if record['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
