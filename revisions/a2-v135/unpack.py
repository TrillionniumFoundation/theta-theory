#!/usr/bin/env python3
"""Verify and unpack the complete editable v135 source overlay."""
from pathlib import Path, PurePosixPath
import hashlib, io, tarfile
HERE = Path(__file__).resolve().parent
PARTS = [('0','c7b2454d87efbefc4208d00589c66bc094f51fd9'),('1','3dac4639d23ac04bd53193118e7c8de9f843a4a4'),('2a','7c8915a41ec71bcc6fb56b55bcf0a09c7c252812'),('2b','2476baa2f927471cf0bdeb32dd23468f0d8ee36b'),('3','7ccb2efb074a1c62d902895acfcd7fb5201edc9c'),('4','7c5da7088e8cb1487fd66d009ea04df772f8d76f')]
chunks = []
for suffix, expected in PARTS:
    data = (HERE / ('payload.part'+suffix)).read_bytes()
    actual = hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if actual != expected:
        raise RuntimeError('Transfer part hash mismatch: '+suffix)
    chunks.append(data)
data = b''.join(chunks)
if hashlib.sha256(data).hexdigest() != 'd86b95a03d7d688482a91a3cca3f9eb59b7effd40914c9a244d99bc70989e9b4':
    raise RuntimeError('Transfer payload SHA-256 mismatch')
with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
    for member in archive.getmembers():
        p = PurePosixPath(member.name)
        if p.is_absolute() or '..' in p.parts or not member.isfile():
            raise RuntimeError('Unsafe archive member: '+member.name)
        if member.name != 'assemble.py' and not member.name.startswith('overlay/'):
            raise RuntimeError('Unexpected archive member: '+member.name)
        target = HERE / member.name
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(archive.extractfile(member).read())
print('Verified source payload: 25789 bytes; editable assembler and overlays unpacked.')
