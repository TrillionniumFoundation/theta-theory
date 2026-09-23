#!/usr/bin/env python3
"""Assemble the complete v132 article from the immutable reviewed v131 tree.

Only the v132 output directory is replaced. No historical source or review is
modified. The expected hashes were recorded after local execution of all seven
exact checks and the complete 71-page LaTeX build; CI re-executes the build.
"""
from pathlib import Path, PurePosixPath
import hashlib
import io
import json
import os
import re
import shutil
import subprocess
import tarfile

ROOT = Path(__file__).resolve().parents[2]
STAGING = Path(__file__).resolve().parent
REVIEW = 'f0ac12d5ce2084fffec3a6245e3cbe8c2e2b39ff'
MANUSCRIPT = '1b3a82d09970ad6545c750733c80ff728a347cd4'
BRANCH = 'revision/a2-v132-galois-descent-higher-residual-2026-09-23'
BASE = PurePosixPath('papers/A2-v17-boundary-information-coarsening/article/v131')
DEST = PurePosixPath('papers/A2-v17-boundary-information-coarsening/article/v132')
TARGET = ROOT / str(DEST)
REPORT = 'reviews/a2-v131-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md'


def git(*args: str) -> bytes:
    return subprocess.check_output(['git', *args], cwd=ROOT)


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def main() -> None:
    ref = os.environ.get('GITHUB_REF')
    if ref and ref != 'refs/heads/' + BRANCH:
        raise SystemExit('Refusing to assemble on a different publication branch')
    git('merge-base', '--is-ancestor', REVIEW, 'HEAD')
    git('diff', '--exit-code', REVIEW, '--', str(BASE), 'reviews')
    source_commit = git('rev-parse', 'HEAD').decode().strip()
    archive = git('archive', REVIEW, str(BASE))
    inherited = {}
    old_tex = []
    if TARGET.exists():
        shutil.rmtree(TARGET)
    TARGET.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:') as tar:
        for member in tar:
            path = PurePosixPath(member.name)
            if not path.is_relative_to(BASE) or path == BASE:
                continue
            relative = path.relative_to(BASE)
            if '..' in relative.parts:
                raise RuntimeError('Unsafe archive path')
            if member.isdir():
                continue
            if not member.isfile():
                raise RuntimeError('Non-regular source entry: ' + member.name)
            stream = tar.extractfile(member)
            if stream is None:
                raise RuntimeError('Missing archive content')
            data = stream.read()
            inherited[str(relative)] = digest(data)
            if relative.suffix == '.tex':
                old_tex.append(data.decode('utf-8'))
            # Never reuse an old PDF, execution log, receipt, or Python cache.
            if 'evidence' in relative.parts or '__pycache__' in relative.parts:
                continue
            if relative.name.startswith('geometry.') and relative.suffix != '.tex':
                continue
            if relative.suffix == '.pyc':
                continue
            destination = TARGET / str(relative)
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(data)
    for patch in ('02-integration.patch', '03-validation.patch', '04-response.patch'):
        subprocess.run(['git', 'apply', '--whitespace=nowarn',
                        '--directory=' + str(DEST), str(STAGING / patch)],
                       cwd=ROOT, check=True)
    for source in sorted((STAGING / 'overrides').rglob('*')):
        if source.is_file():
            relative = source.relative_to(STAGING / 'overrides')
            destination = TARGET / relative
            destination.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, destination)
    expected = json.loads((STAGING / 'expected-source-sha256.json').read_text())
    actual = {name: digest((TARGET / name).read_bytes()) for name in expected}
    differences = {name: {'expected': expected[name], 'actual': actual[name]}
                   for name in expected if actual[name] != expected[name]}
    if differences:
        raise SystemExit('Transferred source differs from locally checked source:\n' +
                         json.dumps(differences, indent=2))
    labels = sorted(set(re.findall(r'\\label\{((?:thm|lem|prop|cor|eq):[^}]+)\}',
                                   '\n'.join(old_tex))))
    manifest = {
        'revision': 132,
        'assembly_commit': source_commit,
        'reviewed_commit': REVIEW,
        'reviewed_manuscript_commit': MANUSCRIPT,
        'controlling_review': REPORT,
        'inherited_mathematical_labels': labels,
        'inherited_sha256': inherited,
        'assembled_sha256': actual,
        'assembly_inputs_sha256': {
            str(p.relative_to(STAGING)): digest(p.read_bytes())
            for p in sorted(STAGING.rglob('*'))
            if p.is_file() and '__pycache__' not in p.parts
        },
        'local_validation': 'Same source hashes passed all seven scripts and a 71-page build before publication; CI executes them again.',
        'historical_source_and_reviews_modified': False,
    }
    (TARGET / 'PROVENANCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
    (TARGET / 'evidence').mkdir(exist_ok=True)
    print(json.dumps({'assembled_source': str(DEST), 'assembly_commit': source_commit,
                      'verified_source_files': len(actual),
                      'inherited_mathematical_labels': len(labels)}, indent=2))


if __name__ == '__main__':
    main()
