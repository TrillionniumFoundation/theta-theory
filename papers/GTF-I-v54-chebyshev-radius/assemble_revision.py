"""Materialize the hash-pinned authored native v54 files; no network access.

This transfer helper is not needed to rebuild the published native-source
archive. It touches only the exact eighteen new-revision paths below.
"""
from __future__ import annotations
import base64
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath

HOME = Path(__file__).resolve().parent
COMPRESSED_SHA256 = 'fa2fcb60c1c8fa1380f472bda2a96f646c94298541a223358ea70b3a9d8ec1a9'
NATIVE_JSON_SHA256 = '8d10c29ab57ff2cdeb6845e789eca0936687eedf96214fad43c1c0a00b5b3882'
EXPECTED = {'HISTORY_AND_PIPELINE_AUDIT.md', 'LITERATURE_AUDIT.md',
    'PRESERVATION_MANIFEST.json', 'PROOF_STATUS.json', 'README.md',
    'RESPONSE_TO_REFEREE.md', 'REVISION_SCOPE.md', 'build.py',
    'check_revision.py', 'main.tex', 'sections/01-classification.tex',
    'sections/02-localization.tex', 'sections/03-consequences.tex',
    'sections/04-width-laws.tex', 'sections/05-algebraic-circle.tex',
    'sections/06-effective.tex', 'sections/07-comparison.tex',
    'sections/08-bibliography.tex'}

def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)

def main() -> None:
    parts = [HOME/'assembly'/f'part-{i}.b64' for i in range(5)]
    require(all(p.is_file() and not p.is_symlink() for p in parts), 'Missing or unsafe payload part')
    compressed = base64.b64decode(b''.join(p.read_bytes() for p in parts), validate=True)
    require(hashlib.sha256(compressed).hexdigest() == COMPRESSED_SHA256, 'Compressed payload hash mismatch')
    raw = lzma.decompress(compressed, memlimit=268435456)
    require(len(raw) == 139544, 'Unexpected native payload length')
    require(hashlib.sha256(raw).hexdigest() == NATIVE_JSON_SHA256, 'Native JSON hash mismatch')
    payload = json.loads(raw)
    require(payload.get('schema') == 'gtf54.native-payload/1', 'Unknown payload schema')
    files = payload.get('files')
    require(isinstance(files, dict) and set(files) == EXPECTED, 'Unexpected file inventory')
    for name, text in sorted(files.items()):
        rel = PurePosixPath(name)
        require(not rel.is_absolute() and '..' not in rel.parts and isinstance(text, str), 'Unsafe native entry')
        target = HOME.joinpath(*rel.parts)
        require(not target.is_symlink(), 'Refusing symlink target')
        require(target.resolve().is_relative_to(HOME), 'Target escapes revision directory')
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(text.encode('utf-8'))
    print(json.dumps({'status':'success', 'native_files':len(files),
        'compressed_sha256':COMPRESSED_SHA256, 'native_json_sha256':NATIVE_JSON_SHA256}, sort_keys=True))

if __name__ == '__main__':
    main()
