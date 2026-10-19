#!/usr/bin/env python3
"""Rebuild only the verified native historical main and supplement.

This execution helper was reconstructed after workspace pruning. It preserves
the original 390 source identities and runs the unchanged original assembler.
Every new attempt has a separate receipt; missing historical logs are not made up.
"""
from pathlib import Path
import argparse
import datetime as dt
import hashlib
import json
import re
import subprocess
import sys
import time

PAPER = Path(__file__).resolve().parent
ARTICLE = PAPER.parents[1]
TABLE_SHA256 = '27573612967769a36d9571798369d80ed26a82cddb861a076378078dbc3f4a04'
SUPPLEMENT_SOURCE_SHA256 = 'f48c2d14e8647a40a585626075fa9aa959a819fcb081bc9b027049f8bea7da37'


def digest(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
            'git_blob': hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()}


def check_sources():
    data = json.loads((PAPER / 'SOURCE_IDENTITY.json').read_text())
    rows = sorted([{k: x[k] for k in ('path', 'bytes', 'sha256', 'git_blob')} for x in data['files']], key=lambda x: x['path'])
    canonical = json.dumps(rows, sort_keys=True, separators=(',', ':')).encode()
    if len(rows) != 390 or hashlib.sha256(canonical).hexdigest() != TABLE_SHA256:
        raise RuntimeError('Historical native source identity table changed')
    if sum(x['path'].endswith('.tex') for x in rows) != 345 or sum(x['path'].endswith('.py') for x in rows) != 45:
        raise RuntimeError('Historical native source type counts changed')
    for row in rows:
        rel = Path(row['path'])
        if rel.is_absolute() or '..' in rel.parts:
            raise RuntimeError('Unsafe historical source path')
        p = PAPER / rel
        if not p.is_file() or p.is_symlink():
            raise RuntimeError('Missing or symlinked historical source: ' + row['path'])
        current = digest(p.read_bytes())
        if any(current[k] != row[k] for k in current):
            raise RuntimeError('Historical source identity mismatch: ' + row['path'])
    return len(rows)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence-dir', type=Path, default=ARTICLE / 'evidence/current-execution/historical-recovery')
    args = parser.parse_args()
    stamp = dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    evidence = args.evidence_dir.resolve() / stamp
    evidence.mkdir(parents=True, exist_ok=False)
    receipt = {'scope': 'Actual post-pruning native historical rebuild; not a recreation of earlier command logs',
               'started_utc': dt.datetime.now(dt.timezone.utc).isoformat(), 'cwd': str(PAPER),
               'historical_whole_repository_gate_executed': False, 'mathematical_proof_certificate': False,
               'python': sys.version, 'source_files_checked': 0, 'commands': [], 'documents': []}

    def save():
        (evidence / 'REBUILD_RECEIPT.json').write_text(json.dumps(receipt, indent=2) + '\n')

    def run(args, name):
        start = dt.datetime.now(dt.timezone.utc).isoformat()
        clock = time.monotonic()
        output = evidence / (name + '.stdout.log')
        with output.open('wb') as stream:
            result = subprocess.run(args, cwd=PAPER, stdout=stream, stderr=subprocess.STDOUT, check=False)
        receipt['commands'].append({'argv': args, 'cwd': str(PAPER), 'started_utc': start,
            'elapsed_seconds': time.monotonic() - clock, 'returncode': result.returncode,
            'output': str(output), 'output_identity': digest(output.read_bytes())})
        save()
        if result.returncode:
            raise RuntimeError(f'Command failed ({result.returncode}): {args!r}; see {output}')
        return output.read_text(errors='replace')

    try:
        receipt['source_files_checked'] = check_sources()
        (PAPER / 'build').mkdir(exist_ok=True)
        save()
        run([sys.executable, 'tools/assemble_v105.py'], '01-assembler')
        generated = PAPER / 'build/supplement-source.tex'
        if hashlib.sha256(generated.read_bytes()).hexdigest() != SUPPLEMENT_SOURCE_SHA256:
            raise RuntimeError('Generated native supplement differs from the previously verified source SHA256')
        receipt['generated_supplement_source'] = digest(generated.read_bytes())
        # The historical main imports the supplement's auxiliary labels via xr.
        # Build that actual dependency first, including on a clean checkout.
        for document in ('supplement', 'main'):
            for pass_number in range(1, 4):
                run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error', '-file-line-error',
                     '-output-directory=build', document + '.tex'], f'{document}-pdflatex-{pass_number}')
        for document, expected_pages in [('main', 26), ('supplement', 883)]:
            pdf = PAPER / 'build' / (document + '.pdf')
            log = PAPER / 'build' / (document + '.log')
            info = run(['pdfinfo', str(pdf)], document + '-pdfinfo')
            m = re.search(r'^Pages:\s+(\d+)\s*$', info, re.MULTILINE)
            if not m or int(m.group(1)) != expected_pages:
                raise RuntimeError('Unexpected native historical page count: ' + document)
            log_text = log.read_text(errors='replace')
            diagnostics = [line for line in log_text.splitlines() if any(t in line for t in ('Warning:', 'Overfull', 'Missing character:', 'undefined references'))]
            (evidence / (document + '.final.log')).write_bytes(log.read_bytes())
            receipt['documents'].append({'document': document, 'pages': int(m.group(1)),
                'pdf': dict(path=str(pdf), **digest(pdf.read_bytes())),
                'log': dict(path=str(log), **digest(log.read_bytes())), 'diagnostics': diagnostics})
            if any('undefined references' in line or 'Overfull' in line or 'Missing character:' in line or 'Package xr Warning:' in line for line in diagnostics):
                raise RuntimeError('Unresolved references or layout diagnostics in historical ' + document)
        receipt['completed_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        receipt['success'] = True
        save()
        print(json.dumps({'receipt': str(evidence / 'REBUILD_RECEIPT.json'), 'success': True,
                          'documents': receipt['documents']}, indent=2))
        return 0
    except Exception as exc:
        receipt['success'] = False
        receipt['failure'] = f'{type(exc).__name__}: {exc}'
        receipt['completed_utc'] = dt.datetime.now(dt.timezone.utc).isoformat()
        save()
        print(json.dumps({'receipt': str(evidence / 'REBUILD_RECEIPT.json'), 'success': False,
                          'failure': receipt['failure']}, indent=2), file=sys.stderr)
        return 1


if __name__ == '__main__':
    raise SystemExit(main())
