#!/usr/bin/env python3
"""One-use, checksum-bound transport of already-authored native sources."""
from __future__ import annotations
import base64
import hashlib
import json
import lzma
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
PAPER = ROOT / 'papers/General-Theta-Foundations-I-restart'
TARGET = PAPER / 'r3'
EXPECTED = 'facc873d722b791fa6966a467f2e5e5cd46b395a1cbaaa0a241dab26ca8af8ca'

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def safe(name: str) -> PurePosixPath:
    p = PurePosixPath(name)
    require(not p.is_absolute() and '..' not in p.parts and str(p) == name,
            'Invalid payload path')
    return p

chunks = sorted(HERE.glob('chunk-*.b64'))
require([p.name for p in chunks] == [f'chunk-{i:03d}.b64' for i in range(5)],
        'Wrong delivery chunk set')
raw = base64.b64decode(''.join(p.read_text() for p in chunks), validate=True)
require(sha(raw) == EXPECTED, 'Compressed source transport checksum mismatch')
obj = json.loads(lzma.decompress(raw))
require(obj['format'] == 'native-r3-source-delta-v2', 'Unknown format')
require(not TARGET.exists(), 'Refuse to overwrite any existing revision')
outputs = {}
for name, item in obj['files'].items():
    path = safe(name)
    if 'text' in item:
        text = item['text']
    else:
        base_path = safe(item['base'])
        require(base_path.parts[0] == 'r2', 'Base is not the preserved predecessor')
        data = (PAPER / base_path).read_bytes()
        require(sha(data) == item['base_sha256'], 'Predecessor source checksum mismatch')
        lines = data.decode('utf-8').splitlines(keepends=True)
        last = 0
        for a, b, replacement in item['line_edits']:
            require(0 <= last <= a <= b <= len(lines), 'Invalid source delta')
            last = b
        for a, b, replacement in reversed(item['line_edits']):
            lines[a:b] = [replacement]
        text = ''.join(lines)
    data = text.encode('utf-8')
    require(sha(data) == item['sha256'], 'Native output checksum mismatch: ' + name)
    outputs[path] = data
require(len(outputs) == 34, 'Unexpected native source count')
manifest = json.loads(outputs[PurePosixPath('SOURCE_MANIFEST.json')])
require({str(p) for p in outputs} == {x['path'] for x in manifest['files']} | {'SOURCE_MANIFEST.json'},
        'Manifest and delivered native file set differ')
for item in manifest['files']:
    data = outputs[PurePosixPath(item['path'])]
    require(sha(data) == item['sha256'] and len(data) == item['bytes'],
            'Native manifest mismatch')
for path, data in outputs.items():
    p = TARGET / path
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(data)
print(json.dumps({'status': 'success', 'native_files': len(outputs),
                  'transport_sha256': EXPECTED,
                  'manifest_sha256': sha(outputs[PurePosixPath('SOURCE_MANIFEST.json')])}, sort_keys=True))
