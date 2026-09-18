#!/usr/bin/env python3
"""Build A2 v83 from the checked-out sources; default includes the expanded edition."""
from __future__ import annotations
import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAPER = ROOT / 'papers/A2-v17-boundary-information-coarsening'
OUT = PAPER / 'build-v83'
INCLUDE = re.compile(r'\\(?:input|include)\{([^}]+)\}')


def digest(path: Path) -> dict:
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob_sha': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}


def source_graph(entry: str) -> dict[str, dict]:
    found: dict[str, dict] = {}
    def visit(name: str) -> None:
        path = (PAPER / name).with_suffix('.tex').resolve()
        if not path.is_relative_to(PAPER.resolve()):
            raise RuntimeError(f'Input escapes the paper directory: {name}')
        key = str(path.relative_to(ROOT))
        if key in found:
            return
        if not path.is_file():
            raise FileNotFoundError(f'Missing manuscript input: {path}')
        found[key] = digest(path)
        text = re.sub(r'(?<!\\)%[^\n]*', '', path.read_text(encoding='utf-8'))
        for target in INCLUDE.findall(text):
            visit(target)
    visit(entry)
    return found


def run(command: list[str], log: Path, cwd: Path = ROOT) -> None:
    with log.open('w', encoding='utf-8') as stream:
        result = subprocess.run(command, cwd=cwd, stdout=stream, stderr=subprocess.STDOUT, check=False)
    if result.returncode:
        raise RuntimeError(f'Command failed ({result.returncode}); see {log}: {command}')


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--main-only', action='store_true', help='Explicitly omit the expanded-edition build')
    args = parser.parse_args()
    for executable in ('latexmk', 'pdflatex', 'pdfinfo'):
        if shutil.which(executable) is None:
            raise RuntimeError(f'Required executable not found: {executable}')
    OUT.mkdir(parents=True, exist_ok=True)
    records = {}
    for optimized in (False, True):
        name = 'checks-optimized' if optimized else 'checks-normal'
        command = [sys.executable] + (['-O'] if optimized else [])
        command += [str(ROOT/'scripts/test_a2_v83.py'), '--output', str(OUT/f'{name}.json')]
        run(command, OUT/f'{name}.log')
        record = json.loads((OUT/f'{name}.json').read_text())
        if not record['passed'] or record['tests_run'] != 22:
            raise RuntimeError(f'Unexpected mathematical regression result: {record}')
        records[name] = record
    entries = ['rigidity_v83'] + ([] if args.main_only else ['rigidity_v83_full'])
    graphs = {name: source_graph(name) for name in entries}
    retention = {'checked': False, 'reason': 'Expanded edition explicitly omitted by --main-only'}
    if not args.main_only:
        old_text = (PAPER/'rigidity_v82.tex').read_text()
        old_inputs = set(INCLUDE.findall(old_text)) - {'article/v82/frontmatter', 'article/v82/references_full'}
        full_text = (PAPER/'rigidity_v83_full.tex').read_text()
        new_inputs = set(INCLUDE.findall(full_text))
        missing = sorted(old_inputs - new_inputs)
        if missing:
            raise RuntimeError(f'Inherited mathematical inputs removed: {missing}')
        retention = {'checked': True, 'inherited_direct_inputs': sorted(old_inputs), 'missing': missing}
    built = {}
    for name in entries:
        command = ['latexmk', '-pdf', '-halt-on-error', '-interaction=nonstopmode',
                   '-file-line-error', '-recorder', f'-outdir={OUT}', name+'.tex']
        run(command, OUT/f'{name}-command.log', PAPER)
        log = (OUT/f'{name}.log').read_text(errors='replace')
        diagnostics = {
            'undefined_references_or_citations': len(re.findall(r'(?:Reference|Citation) .+ undefined|There were undefined references', log)),
            'multiply_defined_labels': len(re.findall(r'multiply defined|multiply-defined', log)),
            'overfull_boxes': len(re.findall(r'Overfull \\[hv]box', log)),
            'underfull_boxes': len(re.findall(r'Underfull \\[hv]box', log))}
        if diagnostics['undefined_references_or_citations'] or diagnostics['multiply_defined_labels']:
            raise RuntimeError(f'Unresolved TeX diagnostics for {name}: {diagnostics}')
        info = subprocess.check_output(['pdfinfo', str(OUT/f'{name}.pdf')], text=True)
        pages = int(re.search(r'^Pages:\s+(\d+)', info, re.M).group(1))
        built[name] = {'status': 'native_build_completed', 'pages': pages,
                       'pdf': digest(OUT/f'{name}.pdf'), 'diagnostics': diagnostics,
                       'visual_inspection': 'Not asserted by this automated script'}
    report = {'entries': built, 'source_graphs': graphs, 'retention': retention, 'regression_checks': records,
              'scope': 'Executed build and regression results, not independent mathematical proof certification.'}
    try:
        report['checkout_head'] = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True, stderr=subprocess.DEVNULL).strip()
    except (subprocess.CalledProcessError, FileNotFoundError):
        report['checkout_head'] = None
    (OUT/'build-report.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps({'entries': built, 'report': str(OUT/'build-report.json')}, indent=2))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (RuntimeError, OSError, ValueError) as error:
        print(f'BUILD FAILED: {error}', file=sys.stderr)
        raise SystemExit(1)
