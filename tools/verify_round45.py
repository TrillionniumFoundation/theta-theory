#!/usr/bin/env python3
"""Verify committed sources; optionally build and write a source-bound receipt.
No source generator is invoked. The receipt is evidence of these checks only.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run(command, log):
    p = subprocess.run(command, cwd=ROOT, text=True, stdout=subprocess.PIPE,
                       stderr=subprocess.STDOUT, check=False)
    (ROOT/log).write_text(p.stdout, encoding='utf-8')
    if p.returncode:
        raise RuntimeError(f'{command!r} returned {p.returncode}; see {log}')
    return {'command':command, 'returncode':p.returncode,
            'log':log, 'log_sha256':digest(ROOT/log)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--build', action='store_true')
    parser.add_argument('--source-sha', required=True)
    parser.add_argument('--write-record')
    args = parser.parse_args()
    if not re.fullmatch('[0-9a-f]{40}', args.source_sha):
        parser.error('--source-sha must be a complete Git commit SHA')
    manifest = json.loads((ROOT/'round45/SOURCE_MANIFEST.json').read_text())
    failures = []
    for e in manifest['files']:
        p = ROOT/e['path']
        if not p.is_file() or digest(p)!=e['sha256'] or p.stat().st_size!=e['bytes']:
            failures.append(e['path'])
    if failures:
        raise RuntimeError(f'manifest mismatch: {failures}')
    workflows = sorted(p.name for p in (ROOT/'.github/workflows').glob('*.y*ml'))
    if workflows != ['verify-round45.yml']:
        raise RuntimeError(f'unexpected review workflows: {workflows}')
    workflow = (ROOT/'.github/workflows/verify-round45.yml').read_text()
    if 'contents: read' not in workflow or 'contents: write' in workflow or 'git push' in workflow:
        raise RuntimeError('review workflow is not read-only')
    result = {'source_commit':args.source_sha,
        'generated_at_utc':datetime.now(timezone.utc).isoformat(),
        'manifest_sha256':digest(ROOT/'round45/SOURCE_MANIFEST.json'),
        'checked_files':len(manifest['files']),
        'formal_proof_assistant':False,
        'scope':'Exact finite algebra, source graph, hashes, and TeX build; analytic proofs remain subject to independent review.'}
    result['tests'] = run([sys.executable,'-m','unittest','discover','-s','tests',
                           '-p','test_round45.py','-v'],'ROUND45_TESTS.log')
    if args.build:
        engine = subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0]
        result['tex_engine'] = engine
        result['builds'] = [run(['pdflatex','-no-shell-escape','-interaction=nonstopmode',
                                  '-halt-on-error','ROUND45_REVISION.tex'],f'ROUND45_BUILD_{i}.log')
                            for i in range(1,4)]
        log = (ROOT/'ROUND45_REVISION.log').read_text(errors='replace')
        forbidden = ['! LaTeX Error','There were undefined references','Citation `',
                     'Reference `','Overfull \\hbox','Fatal error','multiply defined']
        errors = [x for x in forbidden if x in log]
        if errors:raise RuntimeError(f'TeX diagnostics: {errors}')
        pdf = ROOT/'ROUND45_REVISION.pdf'
        match = re.search(r'Output written on .*?\((\d+) pages?',log)
        if not match or not pdf.is_file():raise RuntimeError('missing completed PDF')
        result['pdf'] = {'path':pdf.name,'pages':int(match.group(1)),
                         'bytes':pdf.stat().st_size,'sha256':digest(pdf)}
        result['tex_log_sha256'] = digest(ROOT/'ROUND45_REVISION.log')
        result['nonfatal_underfull_boxes'] = log.count('Underfull \\hbox')
    # Check that compilation and tests did not modify any source byte.
    for e in manifest['files']:
        if digest(ROOT/e['path']) != e['sha256']:raise RuntimeError(f'source changed: {e["path"]}')
    result['all_requested_checks_passed'] = True
    text = json.dumps(result,indent=2,sort_keys=True)+'\n'
    if args.write_record:(ROOT/args.write_record).write_text(text)
    print(text,end='')


if __name__ == '__main__':
    main()
