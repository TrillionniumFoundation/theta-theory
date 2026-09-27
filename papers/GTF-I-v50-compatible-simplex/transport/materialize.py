"""Restore explicitly hashed v50 UTF-8 sources; never write outside this revision."""
from __future__ import annotations
import base64
import hashlib
import json
import lzma
from pathlib import Path
import subprocess
import sys

HERE = Path(__file__).resolve().parent
DEST = HERE.parent

def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def main() -> None:
    manifest = json.loads((HERE / 'MANIFEST.json').read_text())
    if manifest.get('schema') != 'gtf50.native-transport/1':
        raise RuntimeError('Unknown transport schema')
    parts = manifest['parts']
    expected_names = [f'part-{i:02d}.b64' for i in range(5)]
    if sorted(parts) != expected_names:
        raise RuntimeError('Incomplete or unexpected transport parts')
    encoded = []
    for name in expected_names:
        data = (HERE / name).read_bytes().strip()
        if digest(data) != parts[name]:
            raise RuntimeError('Transport SHA256 mismatch: ' + name)
        encoded.append(data)
    packed = base64.b64decode(b''.join(encoded), validate=True)
    decoder = lzma.LZMADecompressor(memlimit=256 * 1024 * 1024)
    raw = decoder.decompress(packed, max_length=1024 * 1024)
    if not decoder.eof or decoder.unused_data:
        raise RuntimeError('Oversize, incomplete or trailing transport stream')
    if digest(raw) != manifest['uncompressed_sha256']:
        raise RuntimeError('Native transport aggregate SHA256 mismatch')
    files = json.loads(raw)
    if set(files) != set(manifest['files']):
        raise RuntimeError('Native source inventory mismatch')
    for name, text in files.items():
        if not isinstance(text, str) or Path(name).name != name or name in {'.', '..'}:
            raise RuntimeError('Unsafe native source entry')
        if Path(name).suffix not in {'.py', '.tex', '.md', '.json'}:
            raise RuntimeError('Unexpected native source type')
        data = text.encode('utf-8')
        if digest(data) != manifest['files'][name]:
            raise RuntimeError('Native file SHA256 mismatch: ' + name)
    # All entries are checked before the first native write.
    for name, text in files.items():
        (DEST / name).write_bytes(text.encode('utf-8'))
    subprocess.run([sys.executable, str(DEST / 'prepare.py')], check=True)
    for name, checksum in manifest['files'].items():
        if digest((DEST / name).read_bytes()) != checksum:
            raise RuntimeError('Native source changed during materialization: ' + name)
    amendments = HERE / 'POST_MATERIALIZE_PATCHES.json'
    prepared = []
    if amendments.exists():
        patchset = json.loads(amendments.read_text())
        if patchset.get('schema') != 'gtf50.post-materialization-patches/1':
            raise RuntimeError('Unknown amendment schema')
        seen = set()
        for patch in patchset['patches']:
            name = patch['file']
            if name not in manifest['files'] or name in seen:
                raise RuntimeError('Invalid or duplicate amendment target')
            seen.add(name)
            data = (DEST / name).read_bytes()
            if digest(data) != patch['before_sha256']:
                raise RuntimeError('Amendment preimage drift: ' + name)
            text = data.decode('utf-8')
            if text.count(patch['old']) != 1:
                raise RuntimeError('Amendment anchor is not unique: ' + name)
            result = text.replace(patch['old'], patch['new']).encode('utf-8')
            if digest(result) != patch['after_sha256']:
                raise RuntimeError('Amendment postimage drift: ' + name)
            prepared.append((name, result))
        for name, result in prepared:
            (DEST / name).write_bytes(result)
    print(json.dumps({'status': 'success', 'native_files_restored': len(files),
                      'explicit_source_amendments': len(prepared),
                      'transport_sha256': manifest['uncompressed_sha256']}))

if __name__ == '__main__':
    main()
