#!/usr/bin/env python3
"""Actual mutation checks for the reconstructed source identity helper.

The fixture uses the exact older complete native main through303 and all original
source groups. This is a structural utility test, not a new manuscript/CI proof.
"""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import shutil
import subprocess
import sys

WORK = Path('/workspace/scratch/b5cc344d4c8e')
ROOT = WORK / 'theta-theory/papers/A2-DYN-global-minimizer-localization-author-revision'
FIXTURE = WORK / 'recovery-source/manifest-fixture'
OUT = ROOT / 'evidence/current-execution/manifest-reconstruction'
OUT.mkdir(parents=True, exist_ok=True)
if FIXTURE.exists():
    shutil.rmtree(FIXTURE)
shutil.copytree(ROOT, FIXTURE, ignore=shutil.ignore_patterns('build', '__pycache__', 'current-execution', 'publication'))
for f in (FIXTURE / 'core').glob('*.tex'):
    if int(f.name.split('_', 1)[0]) >= 304:
        f.unlink()
for rel in ('main.tex', 'preamble.tex', 'model.tex', 'inputs.tex', 'references.tex'):
    old = FIXTURE / 'history/predecessor-source' / rel
    if old.exists():
        shutil.copyfile(old, FIXTURE / rel)
results = []


def command(case, optimized=False, phase='verify', expect=0):
    argv = [sys.executable] + (['-O'] if optimized else []) + ['tools/package_source_manifest.py', '.', phase]
    env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
    started = dt.datetime.now(dt.timezone.utc).isoformat()
    p = subprocess.run(argv, cwd=FIXTURE, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    name = f'{len(results):02d}-{case}-' + ('optimized' if optimized else 'normal') + '.log'
    (OUT / name).write_bytes(p.stdout)
    row = {'case': case, 'argv': argv, 'cwd': str(FIXTURE), 'started_utc': started,
           'returncode': p.returncode, 'expected_success': expect == 0, 'output': name,
           'output_sha256': hashlib.sha256(p.stdout).hexdigest()}
    results.append(row)
    if (p.returncode == 0) != (expect == 0):
        raise RuntimeError('Unexpected result for ' + case + ': ' + p.stdout.decode(errors='replace'))
    return p.stdout


def pair(case, expect=0):
    first = command(case, False, expect=expect)
    second = command(case, True, expect=expect)
    if first != second:
        raise RuntimeError('Normal/optimized gate outputs differ: ' + case)


def mutated(case, relative, replacement):
    p = FIXTURE / relative
    old = p.read_bytes()
    try:
        p.write_bytes(replacement(old))
        pair(case, 1)
    finally:
        p.write_bytes(old)


try:
    command('freeze-complete-original-fixture', phase='freeze')
    pair('untampered')
    variants = sorted((FIXTURE / 'history/numbered-variants').glob('*.tex'))
    mutated('immutable-native-byte', variants[0].relative_to(FIXTURE).as_posix(), lambda b: b+b'\n')
    mutated('current-source-byte', 'model.tex', lambda b: b+b'\n')
    mutated('anchor-byte', 'history/IMMUTABLE_SOURCE_ANCHOR.json', lambda b: b+b'\n')
    def corrupt_manifest(b):
        obj=json.loads(b);obj['files'][0]['bytes']+=1
        return (json.dumps(obj,indent=2)+'\n').encode()
    mutated('manifest-identity-row', 'SOURCE_MANIFEST.json', corrupt_manifest)
    unlisted=FIXTURE/'UNLISTED_SOURCE.tex';unlisted.write_text('Not an author proof. A mutation test only.\n')
    try:pair('unlisted-source',1)
    finally:unlisted.unlink()
    missing=variants[-1];saved=missing.read_bytes();missing.unlink()
    try:pair('missing-immutable-native',1)
    finally:missing.write_bytes(saved)
    source_rows=json.loads((FIXTURE/'SOURCE_MANIFEST.json').read_text())['files']
    paths={x['path'] for x in source_rows}
    for required in ('history/predecessor-source/SOURCE_MANIFEST.json','history/predecessor-source/PUBLICATION_STATUS.json'):
        if required not in paths:
            raise RuntimeError('Historical same-named evidence incorrectly excluded: '+required)
    excluded=FIXTURE/'evidence/current-execution/test-output.log';excluded.parent.mkdir(parents=True,exist_ok=True);excluded.write_text('Regenerable output is intentionally outside the source manifest.\n')
    pair('excluded-current-output')
    summary={'scope':'Fresh structural verification of reconstructed source helper, using the actual complete predecessor native source plus every unchanged inherited source group; not current mathematical proof or remote CI',
             'success':True,'commands':results,'normal_optimized_pair_outputs_identical':True,
             'negative_controls':['immutable-native-byte','current-source-byte','anchor-byte','manifest-identity-row','unlisted-source','missing-immutable-native'],
             'historical_self_and_publication_named_files_remain_manifested':True}
except Exception as exc:
    summary={'success':False,'failure':str(exc),'commands':results}
    (OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
    raise
(OUT/'SUMMARY.json').write_text(json.dumps(summary,indent=2)+'\n')
shutil.copyfile(Path(__file__),OUT/'TEST_PROGRAM.py')
print(json.dumps({'success':True,'commands':len(results),'receipt':str(OUT/'SUMMARY.json')},indent=2))
