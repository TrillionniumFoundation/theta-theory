"""Materialize the exact v58 native delta and retained source, without network."""
from pathlib import Path
import base64
import hashlib
import json
import lzma

HOME = Path(__file__).resolve().parent
BASE = HOME.parent / 'GTF-I-v57-uniform-orbit'
PAYLOAD = '5ce2fdbb0bf1f93b0f6ba69caeb7046e4ea2f25a0659816ef5c35b6c39b0e799'
INVENTORY = '86d2722884d4d1f0883243148d68732858c3ae8c1b020f6624c925c8b967a281'
REPORT = 'c530ec0f755d2aa9a9d23b3d99dc4675fcacc679'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def safe(name):
    path = Path(name)
    require(not path.is_absolute() and '..' not in path.parts, 'Unsafe native path')
    return path


def main():
    parts = sorted((HOME / 'assembly').glob('part-*.b64'))
    require(len(parts) == 5, 'Incomplete native delta')
    encoded = ''.join(p.read_text().strip() for p in parts)
    require(len(encoded) == 50432, 'Native delta length mismatch')
    decoder = lzma.LZMADecompressor()
    data = decoder.decompress(base64.b64decode(encoded, validate=True), max_length=2000001)
    require(decoder.eof and not decoder.unused_data and len(data) <= 2000000,
            'Invalid native delta archive')
    require(hashlib.sha256(data).hexdigest() == PAYLOAD, 'Native delta digest mismatch')
    delta = json.loads(data)
    require(len(delta) == 47, 'Unexpected native delta file count')
    for name, entry in delta.items():
        target = HOME / safe(name)
        if isinstance(entry, str):
            text = entry
        else:
            raw = (BASE / safe(entry['base'])).read_bytes()
            require(hashlib.sha256(raw).hexdigest() == entry['sha256'],
                    'Delta base changed: ' + name)
            lines = raw.decode('utf-8').splitlines(keepends=True)
            chunks = []
            for op in entry['ops']:
                if isinstance(op, str):
                    chunks.append(op)
                else:
                    i, j = op
                    require(isinstance(i, int) and isinstance(j, int) and
                            0 <= i <= j <= len(lines), 'Invalid copy range')
                    chunks.append(''.join(lines[i:j]))
            text = ''.join(chunks)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
    raw = (BASE / 'evidence/SOURCE_HASHES.json').read_bytes()
    require(hashlib.sha256(raw).hexdigest() == INVENTORY, 'Predecessor inventory changed')
    files = json.loads(raw)
    require(len(files) == 181, 'Unexpected retained native count')
    for name, digest in files.items():
        data = (BASE / safe(name)).read_bytes()
        require(hashlib.sha256(data).hexdigest() == digest, 'Retained source changed: ' + name)
        target = HOME / 'retained-v57' / safe(name)
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    manifest = {'predecessor_publication': '0e07470b9693a2789af00222f063e715a83ff454',
                'review_commit': '5b2fb03f87a6b28bddcef51d498a0c78429bfa22',
                'review_blob': REPORT, 'files': files}
    (HOME / 'PRESERVATION_MANIFEST.json').write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + '\n')
    report = (HOME / 'FROZEN_R38_REPORT.md').read_bytes()
    blob = hashlib.sha1(b'blob ' + str(len(report)).encode() + b'\0' + report).hexdigest()
    require(blob == REPORT, 'Controlling report changed')
    print(json.dumps({'status': 'native-source-materialized',
                      'new_native_files': 49, 'retained_native_files': 181,
                      'frozen_report': True, 'qualification': 'not yet run'}))


if __name__ == '__main__':
    main()
