#!/usr/bin/env python3
"""Materialize the complete v96 native tree; transport alone is not a manuscript.

The input is an exact, hash-checked set of line-edit recipes against the frozen
v94 native source. No code from the transport is evaluated. The readable native
files must be committed and pushed before the production manuscript build.
"""
from pathlib import Path
import base64
import hashlib
import importlib.util
import json
import lzma
import shutil
import tempfile

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / 'papers/GTF-I-v94-spectral-value'
DST = ROOT / 'papers/GTF-I-v96-referee-resolution'
REPORTS = Path('/tmp/gtf96-reports')
HERE = Path(__file__).resolve().parent
DIGEST = '7abbf149d47907ec05b47c64eb74bdd6d73f36b7a5e1bd1f1c64b6262560baf5'
CHUNKS = 7


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def path(name):
    p = Path(name)
    require(not p.is_absolute() and '..' not in p.parts and p.as_posix() == name,
            'Unsafe source path: ' + str(name))
    return p


def inventory_digest(inv):
    return sha(json.dumps(inv, sort_keys=True, separators=(',', ':')).encode())


def main():
    require(not DST.exists(), 'Refusing to overwrite an existing native edition')
    payload = base64.b64decode(''.join((HERE / f'payload-{i}.b64').read_text().strip()
                                     for i in range(CHUNKS)), validate=True)
    require(sha(payload) == DIGEST, 'Incomplete or altered source transport')
    raw = lzma.decompress(payload)
    require(len(raw) < 2000000, 'Unexpected source-transport size')
    recipe = json.loads(raw)
    spec = importlib.util.spec_from_file_location('frozen_v94_build', SRC / 'build_revision.py')
    old = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(old)
    inv = old.sources(SRC)
    require(len(inv) == recipe['base_files_count'] == 870, 'Wrong v94 native count')
    require(inventory_digest(inv) == recipe['base_inventory_digest'], 'Wrong v94 native bytes')
    require(inv == json.loads((SRC / 'evidence/SOURCE_HASHES.json').read_text()),
            'Published v94 inventory does not match its native files')
    baseline = {
        'commit': 'db6739da3487be8787a67fc175b9086bd62f0e80',
        'source_commit': '24f48c90d6bcc1eae1d4c38ac5195405ac21da7d',
        'publication_commit': '0919ff61895716ea3de1d6a0f2a6a291935764d0',
        'files': inv, 'graphs': {}
    }
    for entry in old.DOCS:
        files, labels = old.graph(SRC, entry)
        baseline['graphs'][entry] = {'files': sorted(files), 'labels': sorted(labels)}
    generated = {'V94_BASELINE.json': json.dumps(baseline, indent=2, sort_keys=True) + '\n'}
    with tempfile.TemporaryDirectory(prefix='gtf96-native-', dir=ROOT / 'papers') as temp:
        work = Path(temp)
        for name in inv:
            target = work / path(name)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(SRC / name, target)
        for item in recipe['recipes']:
            name = path(item['path'])
            if 'text' in item:
                text = item['text']
            else:
                location, reference = item.get('copy', item.get('edit'))
                reference = path(reference).as_posix()
                if location == 'base':
                    require(reference in inv, 'Unknown base source')
                    text = (SRC / reference).read_text()
                elif location == 'generated':
                    text = generated[reference]
                elif location == 'reports':
                    require(reference in {'FROZEN_R61_REPORT.md', 'FROZEN_R61_PIPELINE_AUDIT.md',
                                          'FROZEN_R62_REPORT.md'}, 'Unknown report source')
                    text = (REPORTS / reference).read_text()
                elif location == 'current':
                    text = (work / reference).read_text()
                else:
                    raise RuntimeError('Unknown transport reference kind')
                if 'edit' in item:
                    lines = text.splitlines(keepends=True)
                    previous = len(lines) + 1
                    for start, end, replacement in reversed(item['ops']):
                        require(isinstance(start, int) and isinstance(end, int)
                                and 0 <= start <= end <= len(lines) and end < previous,
                                'Invalid or overlapping source edit')
                        require(isinstance(replacement, str), 'Non-text replacement')
                        lines[start:end] = [replacement]
                        previous = start
                    text = ''.join(lines)
            require(isinstance(text, str), 'Non-text source entry')
            target = work / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text)
        actual = old.sources(work)
        require(len(actual) == recipe['final_count'] == 932, 'Incomplete native result')
        require(inventory_digest(actual) == recipe['final_inventory_digest'],
                'Reconstructed native source differs from the reviewed local source')
        work.rename(DST)
    print(json.dumps({'status': 'materialized', 'native_directory': str(DST.relative_to(ROOT)),
                      'native_files': len(actual), 'inventory_digest': inventory_digest(actual),
                      'publication_or_final_head_qualified': False}, sort_keys=True))


if __name__ == '__main__':
    main()
