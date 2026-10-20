#!/usr/bin/env python3
"""Check received publication bytes and archived validation evidence."""
import hashlib
import io
import json
from pathlib import Path
import zipfile

root = Path(__file__).resolve().parent
manifest = json.loads((root / 'DELIVERY_MANIFEST.json').read_text())
for item in manifest['files']:
    path = root / item['path']
    if not path.is_file() or path.stat().st_size != item['bytes']:
        raise SystemExit('Missing or wrong-sized file: ' + item['path'])
    if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
        raise SystemExit('SHA-256 mismatch: ' + item['path'])
prefix = 'General_Theta_Foundations_I_R74_Validation/'
parts_manifest=json.loads((root/'archives/ARCHIVE_PARTS.json').read_text())
validation_bytes=None
for item in parts_manifest['archives']:
    data=b''.join((root/part['path']).read_bytes() for part in item['parts'])
    if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
        raise SystemExit('Complete archive identity mismatch: '+item['file'])
    if item['file']=='General_Theta_Foundations_I_R74_Validation.zip':
        validation_bytes=data
if validation_bytes is None:
    raise SystemExit('Validation archive not found')
with zipfile.ZipFile(io.BytesIO(validation_bytes)) as archive:
    if archive.testzip() is not None:
        raise SystemExit('Validation archive CRC failure')
    internal = json.loads(archive.read(prefix + 'ARCHIVE_MANIFEST.json'))
    for item in internal['files']:
        data = archive.read(prefix + item['path'])
        if len(data) != item['bytes'] or hashlib.sha256(data).hexdigest() != item['sha256']:
            raise SystemExit('Validation payload mismatch: ' + item['path'])
print(json.dumps({'status':'PASS','publication_files':len(manifest['files']),
    'validation_payload_files':len(internal['files']),
    'source_commit':manifest['source_commit'],
    'scope':'File-integrity verification only; not proof, review or editorial certification.'},indent=2))
