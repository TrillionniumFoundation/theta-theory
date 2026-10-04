#!/usr/bin/env python3
"""Read-only exact-checkout qualification of A2 v18 and all retained volumes."""
from __future__ import annotations
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
OUT = ROOT / 'verification' / 'v18'
CORE = 'c3b071000a410b8337d8765d6149ff56e7444592'
COMPLETE = '14b2e5379e5b223bc0bdc823c97fd77c2dca2cda'


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(['git', '-C', str(ROOT), *args],
                                   text=True, stderr=subprocess.STDOUT).strip()


def manifest() -> dict[str, str]:
    paths = [ROOT/'main.tex', ROOT/'references.tex', ROOT/'proof_extract.tex']
    paths += sorted((ROOT/'core').glob('*.tex'))
    paths += sorted((ROOT/'tools').glob('*.py'))
    return {str(p.relative_to(ROOT)): digest(p) for p in paths}


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    record = {'schema':'a2-v18-exact-checkout-validation-1', 'status':'running',
              'started_utc':dt.datetime.now(dt.timezone.utc).isoformat(),
              'platform':platform.platform(), 'python':sys.version,
              'github_run_id':os.getenv('GITHUB_RUN_ID'),
              'github_sha':os.getenv('GITHUB_SHA'),
              'runner_image':os.getenv('ImageOS'),
              'runner_image_version':os.getenv('ImageVersion'),
              'commands':[], 'formal_proof_certificate':False}

    def run(argv: list[str], label: str) -> str:
        p = subprocess.run(argv, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,
                           env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1','TERM':'dumb'})
        log = OUT/(label+'.log')
        log.write_text(p.stdout)
        record['commands'].append({'argv':argv, 'exit_code':p.returncode,
                                   'log':str(log.relative_to(ROOT)),
                                   'log_sha256':digest(log)})
        if p.returncode:
            raise RuntimeError(f'{label}: exit {p.returncode}')
        return p.stdout

    try:
        record['source_commit'] = git('rev-parse','HEAD')
        record['source_tree'] = git('rev-parse','HEAD^{tree}')
        if record['github_sha'] and record['github_sha'] != record['source_commit']:
            raise RuntimeError('triggering commit differs from checkout')
        if git('diff','--name-only','HEAD','--','.'):
            raise RuntimeError('tracked sources are not clean')
        prefix = git('rev-parse','--show-prefix')
        if git('rev-parse','HEAD:'+prefix+'complete') != COMPLETE:
            raise RuntimeError('preserved supplement tree differs')
        record['complete_tree'] = COMPLETE
        retained = {}
        for line in git('ls-tree','-r',CORE).splitlines():
            meta, name = line.split('\t',1)
            mode, kind, expected = meta.split()
            if kind != 'blob' or mode != '100644':
                raise RuntimeError('unexpected retained core entry')
            actual = git('hash-object',str(ROOT/'core'/name))
            if actual != expected:
                raise RuntimeError('retained mathematical source differs: '+name)
            retained[name] = actual
        record['retained_core_blobs'] = retained
        pins = json.loads((ROOT/'SOURCE_PINS.json').read_text())
        for name, expected in pins['new_source_sha256'].items():
            if digest(ROOT/name) != expected:
                raise RuntimeError('local/publication source binding differs: '+name)
        before = manifest()
        record['source_manifest'] = before
        normal = run([sys.executable,'tools/verify_two_window.py','--geometry'],
                     'two-window-normal')
        optimized = run([sys.executable,'-O','tools/verify_two_window.py','--geometry'],
                        'two-window-optimized')
        if normal != optimized:
            raise RuntimeError('new normal/optimized outputs differ')
        record['new_diagnostics'] = [json.loads(s) for s in normal.splitlines() if s.strip()]
        record['normal_optimized_identical'] = True
        run(['latexmk','-g','-pdf','-interaction=nonstopmode','-halt-on-error',
             '-outdir=extract-build','proof_extract.tex'],'proof-extract-build')
        log = ROOT/'extract-build/proof_extract.log'
        warnings = re.findall(r'^.*(?:Warning|Overfull|Underfull|undefined).*$',
                              log.read_text(errors='replace'),re.M)
        record['extract_final_tex_diagnostics'] = warnings
        if warnings:
            raise RuntimeError('new extract has final TeX diagnostics')
        record['extract_pdf_sha256'] = digest(ROOT/'extract-build/proof_extract.pdf')
        # The unchanged driver executes the retained suites and all three volumes.
        # Its historical schema is nested, never relabelled as a previous SHA pass.
        run([sys.executable,'tools/run_validation.py','--all-volumes'],
            'retained-driver-all-volumes')
        nested_path = ROOT/'verification/current/receipt.json'
        nested = json.loads(nested_path.read_text())
        if (nested['status'] != 'passed' or nested['scope'] != 'all_volumes'
                or nested['source_commit'] != record['source_commit']):
            raise RuntimeError('all-volume receipt does not bind a current pass')
        record['all_volume_receipt_sha256'] = digest(nested_path)
        record['documents'] = nested['documents']
        record['retained_diagnostics'] = nested['diagnostics']
        if manifest() != before or git('diff','--name-only','HEAD','--','.'):
            raise RuntimeError('qualification modified tracked or mathematical sources')
        record['source_unchanged'] = True
        record['status'] = 'passed'
    except Exception as exc:
        record['status'] = 'failed'
        record['error'] = str(exc)
    finally:
        record['finished_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        (OUT/'receipt.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
        print(json.dumps(record,indent=2,sort_keys=True))
    return 0 if record['status'] == 'passed' else 1


if __name__ == '__main__':
    raise SystemExit(main())
