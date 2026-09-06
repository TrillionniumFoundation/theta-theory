#!/usr/bin/env python3
"""Execute the v15 author checks and full build, with optional pinned review probe.

No neighboring source folder is required for the standalone v15 validation.
The optional review probe deliberately uses the unchanged v14 source, never
its altered successor. Every test is executed; no success receipt is reused.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time
from manifest import verify

ROOT = Path(__file__).resolve().parent
EXPECTED = {10: 7904, 11: 8207, 12: 26158, 13: 12944, 14: 7400, 15: 5868}

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(command, log):
    start = time.monotonic()
    with log.open('w') as stream:
        completed = subprocess.run(command, cwd=ROOT, stdout=stream,
                                   stderr=subprocess.STDOUT, text=True, timeout=900)
    if completed.returncode:
        raise RuntimeError(f'Command failed ({completed.returncode}); see {log}')
    return round(time.monotonic() - start, 3)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--prior-review', action='store_true')
    args = parser.parse_args()
    out = ROOT / 'validation'; out.mkdir(exist_ok=True)
    (out/'EXECUTION_REPORT.json').unlink(missing_ok=True)
    report = {'version': 15, 'python': platform.python_version(),
              'source_files_verified': verify(),
              'controlling_review': '3d58bb33ae122ebb2430874e2a57a5863e6a876a',
              'submission_basis': 'ffb9214b0fc7e218d6183c1f81bccb3e47587421',
              'workflow_run_id': os.environ.get('GITHUB_RUN_ID'),
              'workflow_input_commit': os.environ.get('GITHUB_SHA'),
              'author_suites': [], 'prior_review_probe': None,
              'scope': 'Executed finite diagnostics and source preservation; not formal proof verification or a journal recommendation.'}
    old = json.loads((ROOT/'history/V14_SOURCE_MANIFEST.json').read_text())
    old_files = old['files']
    unchanged = ['finite_compiler.py','certified_compiler.py','construction_contracts.py']
    unchanged += [f'tests/test_v{n}.py' for n in range(10,15)]
    for name in unchanged:
        if digest(ROOT/name) != old_files[name]:
            raise ValueError('An inherited compiler/test source changed: '+name)
    report['unchanged_compiler_and_test_files'] = unchanged
    for version,count in EXPECTED.items():
        name = (f'V{version}_AUTHOR_RERUN.json' if version < 14 else
                'V14_DIRECTIONAL_DIAGNOSTICS.json' if version == 14 else 'V15_CIRCULAR_DIAGNOSTICS.json')
        target = out/name
        elapsed = run([sys.executable, f'tests/test_v{version}.py', str(target)],
                      out/f'v{version}-stdout.txt')
        data = json.loads(target.read_text())
        if data['assertions'] != count or not (data.get('passed') is True or data.get('status') == 'passed'):
            raise ValueError('Unexpected author suite result: '+str(version))
        report['author_suites'].append({'version':version, 'assertions':count,
            'passed':True,'seconds':elapsed,'source_sha256':digest(ROOT/f'tests/test_v{version}.py'),
            'result_sha256':digest(target)})
        (out/'EXECUTION_PROGRESS.json').write_text(json.dumps(report,indent=2)+'\n')
    report['unchanged_author_suite_total'] = sum(EXPECTED[n] for n in range(10,15))
    report['new_author_diagnostic_total'] = EXPECTED[15]
    report['author_assertion_total'] = sum(EXPECTED.values())
    if args.prior_review:
        repo = ROOT.parents[1]
        script = repo/'reviews/a1-english-v14-geometric-2026-09-06/reproduce_review.py'
        baseline = ROOT.parent/'A1-english-v14'
        if not script.is_file() or not baseline.is_dir():
            raise FileNotFoundError('Optional prior review requires the full pinned repository')
        target = out/'PRIOR_REVIEW_RERUN.json'
        elapsed = run([sys.executable,str(script),'--source',str(baseline),'--output',str(target)],out/'prior-review-stdout.txt')
        data = json.loads(target.read_text())
        if data['assertions'] != 21691 or data.get('passed') is not True:
            raise ValueError('Unexpected original v14 review-probe outcome')
        report['prior_review_probe'] = {'source_version':14,'assertions':data['assertions'],
            'passed':True,'seconds':elapsed,'result_sha256':digest(target),
            'scope':'Original independent-review probe rerun on its unchanged submission, not a new independent review of v15.'}
    report['build_seconds'] = run([sys.executable,'build.py'],out/'build-stdout.txt')
    report['build'] = json.loads((ROOT/'BUILD_REPORT.json').read_text())
    pdfinfo = subprocess.run(['pdfinfo',str(ROOT/'main.pdf')],check=True,capture_output=True,text=True)
    report['pdf_pages'] = int(next(x.split(':',1)[1] for x in pdfinfo.stdout.splitlines() if x.startswith('Pages:')))
    report['pdf_sha256'] = digest(ROOT/'main.pdf')
    report['source_files_verified_after_execution'] = verify()
    report['passed'] = True
    (out/'EXECUTION_REPORT.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps(report,indent=2))

if __name__ == '__main__':
    main()
