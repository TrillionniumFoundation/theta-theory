#!/usr/bin/env python3
"""Restore the checksummed, locally validated v10 source overlay only.

The transport archive is not the manuscript: publication commits the readable
sources, complete inherited proofs, executable checks and the compiled PDF.
No existing historical file may be changed by this bootstrap.
"""
from pathlib import Path, PurePosixPath
import base64, hashlib, io, json, tarfile
ROOT=Path(__file__).resolve().parents[1]
EXPECTED='534b5c31c18e85c4ea22149f86e0f6ef1a44d793148f0a0d711ba8f17256415f'

def main():
    parts=sorted((ROOT/'scripts/a1-v10-overlay').glob('part-*.b64'))
    if len(parts)!=5: raise RuntimeError('Expected exactly five transport parts')
    archive=base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True)
    if hashlib.sha256(archive).hexdigest()!=EXPECTED:
        raise RuntimeError('Source transport checksum mismatch')
    restored=[]
    with tarfile.open(fileobj=io.BytesIO(archive),mode='r:xz') as tf:
        members=tf.getmembers()
        if len(members)!=15: raise RuntimeError('Unexpected overlay member count')
        for m in members:
            p=PurePosixPath(m.name)
            if (not m.isfile() or p.is_absolute() or '..' in p.parts
                or not (m.name.startswith('papers/A1-english-v10/')
                        or m.name=='scripts/materialize_a1_v10.py')):
                raise RuntimeError('Disallowed overlay path: '+m.name)
            stream=tf.extractfile(m)
            if stream is None: raise RuntimeError('Missing regular-file bytes')
            data=stream.read();dest=ROOT/m.name
            if dest.exists() and dest.read_bytes()!=data:
                raise RuntimeError('Refusing to overwrite a changed source: '+m.name)
            dest.parent.mkdir(parents=True,exist_ok=True)
            dest.write_bytes(data)
            restored.append({'path':m.name,'sha256':hashlib.sha256(data).hexdigest()})
    print(json.dumps({'archive_sha256':EXPECTED,'restored':restored},indent=2))
if __name__=='__main__':main()
