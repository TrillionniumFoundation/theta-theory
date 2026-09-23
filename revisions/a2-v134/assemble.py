#!/usr/bin/env python3
"""Assemble only A2/v134 from an immutable review and checked source overlays."""
from pathlib import Path, PurePosixPath
import argparse
import base64
import hashlib
import io
import json
import re
import shutil
import subprocess
import tarfile
import tempfile

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
BASE = 'a75f534c6694513ae6c493166d1cba1ea56a98fd'
REVIEWED = 'bbbb697e852d1ca93b88eb7d3bfe6fbd15f396a7'
SOURCE = Path('papers/A2-v17-boundary-information-coarsening/article/v133')
DEST = SOURCE.with_name('v134')
REVIEW = 'reviews/a2-v133-independent-harsh-top4-2026-09-23/REFEREE_REPORT.md'
PAYLOAD_SHA = '8507d9e8c49303a0de4132d8b5bee9d85994d24435b497a4ab5ddc7bca801831'
PART_SHA = [
    '00ea1e2b89234cd2dc94ad1aa92fc03022ca7bac',
    '6e39599c0401f5fb5b2bb202508435b083c87e05',
    'ba0becd3a9b2369bd6c056a39de8c76df19208cc',
    'ef32a6be22eeb1f218215d1950bf80b7ad61815e',
    'a6e391e3cb60b3ba03c8f9e215175038abe0c363',
]
sha = lambda b: hashlib.sha256(b).hexdigest()
def git_blob_sha(b):
    return hashlib.sha1(b'blob ' + str(len(b)).encode() + b'\0' + b).hexdigest()

def payload_bytes():
    chunks = []
    for i, expected in enumerate(PART_SHA):
        path = HERE / f'payload.part{i}'
        raw = path.read_bytes()
        if i == 0 and git_blob_sha(raw) == '616952ee242d449af66939989266788e0488361b':
            # Normalize one identified base64 transfer insertion in the initial
            # transport commit. The normalized part is committed by the build.
            text = base64.b64encode(raw).decode('ascii')
            if len(text) != 10000 or text.count('LyaonaWWyg') != 1:
                raise RuntimeError('Unexpected initial transport representation')
            text = text.replace('LyaonaWWyg', 'LyaonaWyg') + 'e'
            raw = base64.b64decode(text, validate=True)
            if git_blob_sha(raw) != expected:
                raise RuntimeError('Transport normalization did not recover expected bytes')
            path.write_bytes(raw)
        if git_blob_sha(raw) != expected:
            raise RuntimeError(f'Transfer part {i} hash mismatch')
        chunks.append(raw)
    data = b''.join(chunks)
    if sha(data) != PAYLOAD_SHA:
        raise RuntimeError('Full transfer payload SHA-256 mismatch')
    return data

def safe_unpack(data, destination):
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:*') as archive:
        for member in archive.getmembers():
            p = PurePosixPath(member.name)
            if p.is_absolute() or '..' in p.parts or not (member.isfile() or member.isdir()):
                raise RuntimeError(f'Unsafe archive member: {member.name}')
            target = destination / member.name
            if member.isdir():
                target.mkdir(parents=True, exist_ok=True)
            else:
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(archive.extractfile(member).read())

def compiled(root):
    seen, text = set(), []
    def visit(name):
        if name in seen:
            return
        if Path(name).is_absolute() or '..' in Path(name).parts:
            raise RuntimeError(f'Nonlocal LaTeX input: {name}')
        seen.add(name)
        source = (root / name).read_text()
        text.append(source)
        for child in re.findall(r'\\input\{([^}]+)\}', source):
            visit(child)
    visit('geometry.tex')
    return seen, set(re.findall(r'\\label\{([^}]+)\}', '\n'.join(text)))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--local', action='store_true', help='Artifact-based preflight, not a remote build')
    args = parser.parse_args()
    payload = payload_bytes()
    with tempfile.TemporaryDirectory(prefix='a2-v134-') as temp:
        temp = Path(temp)
        if args.local:
            base = ROOT / SOURCE
            assembly = 'local-preflight-not-a-remote-commit'
        else:
            subprocess.run(['git', 'merge-base', '--is-ancestor', BASE, 'HEAD'], cwd=ROOT, check=True)
            archive = subprocess.check_output(['git', 'archive', BASE, str(SOURCE)], cwd=ROOT)
            safe_unpack(archive, temp / 'reviewed')
            base = temp / 'reviewed' / SOURCE
            assembly = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=ROOT, text=True).strip()
        prior = json.loads((base / 'PROVENANCE_MANIFEST.json').read_text())
        for name, expected in prior['assembled_sha256'].items():
            if sha((base / name).read_bytes()) != expected:
                raise RuntimeError(f'Immutable reviewed source mismatch: {name}')
        original_inputs, original_labels = compiled(base)
        target = temp / 'article'
        shutil.copytree(base, target)
        shutil.rmtree(target / 'evidence', ignore_errors=True)
        for path in list(target.rglob('__pycache__')):
            shutil.rmtree(path)
        for ext in ['pdf', 'aux', 'out', 'log']:
            (target / f'geometry.{ext}').unlink(missing_ok=True)
        safe_unpack(payload, target)
        current_inputs, current_labels = compiled(target)
        if not original_inputs <= current_inputs or not original_labels <= current_labels:
            raise RuntimeError('An inherited compiled input or mathematical label was lost')
        for name in ['parts/12a-universal-readout.tex', 'parts/12b-functoriality.tex']:
            if (base / name).read_bytes() != (target / name).read_bytes():
                raise RuntimeError(f'Accepted proof was changed: {name}')
        sources = {str(p.relative_to(target)): sha(p.read_bytes())
                   for p in sorted(target.rglob('*')) if p.is_file()
                   and p.suffix in {'.tex', '.py', '.sh', '.md', '.json'}
                   and p.name not in {'PROVENANCE_MANIFEST.json', 'PROVENANCE_MANIFEST.md'}
                   and 'evidence' not in p.parts}
        unchanged = {str(p.relative_to(base)): sha(p.read_bytes())
                     for p in sorted(base.rglob('*.tex'))
                     if (target / p.relative_to(base)).read_bytes() == p.read_bytes()}
        manifest = {
            'revision': 134, 'assembly_commit': assembly, 'reviewed_commit': REVIEWED,
            'controlling_review_commit': BASE, 'controlling_review': REVIEW,
            'payload_sha256': PAYLOAD_SHA,
            'inherited_compiled_inputs': sorted(original_inputs),
            'inherited_mathematical_labels': sorted(original_labels),
            'unchanged_inherited_tex_sha256': unchanged, 'assembled_sha256': sources,
        }
        (target / 'PROVENANCE_MANIFEST.json').write_text(json.dumps(manifest, indent=2) + '\n')
        (target / 'PROVENANCE_MANIFEST.md').write_text(
            '# A2 v134 source provenance\n\nComplete v133 source at controlling review commit `' + BASE +
            '`; every prior source hash verified before applying full-source overlays.\n'
            'All inherited compiled inputs and mathematical labels are retained.\n'
            'The accepted universal readout and common-projective-transformation proofs are byte-identical.\n'
            'The manifest binds the exact source and normalized transfer payload.\n'
            'The executed receipt distinguishes finite checks from written structural proofs.\n')
        final = ROOT / DEST
        if final.exists():
            old = final / 'PROVENANCE_MANIFEST.json'
            if not old.exists() or json.loads(old.read_text()).get('revision') != 134:
                raise RuntimeError('Refusing to overwrite an unrecognized destination')
            shutil.rmtree(final)
        shutil.copytree(target, final)
        print(json.dumps({'destination': str(DEST), 'assembly_commit': assembly,
              'inherited_compiled_inputs': len(original_inputs),
              'inherited_mathematical_labels': len(original_labels),
              'unchanged_tex_files': len(unchanged), 'source_files': len(sources)}, indent=2))

if __name__ == '__main__':
    main()
