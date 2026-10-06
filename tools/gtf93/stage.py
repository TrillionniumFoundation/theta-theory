#!/usr/bin/env python3
"""Stage the checked v93 source without changing any existing paper directory."""
from pathlib import Path
import argparse
import base64
import gzip
import hashlib
import importlib.util
import json
import shutil

p=argparse.ArgumentParser()
p.add_argument('--source',default='papers/GTF-I-v92-rank-memory')
p.add_argument('--dest',default='papers/GTF-I-v93-spectral-rigidity')
a=p.parse_args()
src=Path(a.source).resolve();dst=Path(a.dest).resolve()
if dst.exists():
    raise RuntimeError('Refusing to overwrite an existing native revision')

def sha(data):
    return hashlib.sha256(data).hexdigest()

def gitblob(data):
    return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()

def relative(name):
    rel=Path(name)
    if rel.is_absolute() or '..' in rel.parts:
        raise RuntimeError('Unsafe patch path')
    return rel

parts=[(Path(__file__).parent/f'payload-{i}.b64').read_text() for i in range(3)]
# Four literal transport transcription repairs. The corrected archive and
# every reconstructed file are checked against the preflight SHA-256 values.
if gitblob(parts[2].encode())=='a73af0665c50eb9a258a0f4329308c78c9518640':
    for old,new in [
        ('gu5X+a3Z3bLoAgZ6d2G','gu5X+a3ZLoAgZ6d2G'),
        ('sN3frPTvSbqXZO4OHT','sN3frPTvTbqXZO4OHT'),
        ('IUB+0LrXLZRZRqwpU8','IUB+0LrXLZRqwpU8'),
        ('gzzWZjVaV2htnkaE5Kh','gzzWZjVaV2htnka5Kh')]:
        if parts[2].count(old)!=1:
            raise RuntimeError('Transport repair anchor is not unique')
        parts[2]=parts[2].replace(old,new)
if gitblob(parts[2].encode())!='a57597e6f3828e390d4daa47e28c82df979f1f60':
    raise RuntimeError('Transport part differs from checked source')
payload=base64.b64decode(''.join(parts),validate=True)
if sha(payload)!='2f98ae8c33e0047a2814947baec4930e4fc5468fe86af6c303b2f8315850e4ee':
    raise RuntimeError('Complete patch archive digest mismatch')
patch=json.loads(gzip.decompress(payload))
if not isinstance(patch,dict):
    raise RuntimeError('Invalid patch dictionary')
spec=importlib.util.spec_from_file_location('v92_helpers',src/'build_revision.py')
old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
inv=old.sources(src)
if inv!=json.loads((src/'evidence/SOURCE_HASHES.json').read_text()):
    raise RuntimeError('Pinned v92 native source inventory mismatch')
base={'commit':'a7081ca8cfb1df8f6369a5820e4f3b5027b66ca2',
      'source_commit':'33811525dd80dbc3c0c70059114fb779e9ac9c84',
      'files':inv,'graphs':{}}
for entry in old.DOCS:
    files,labels=old.graph(src,entry)
    base['graphs'][entry]={'files':sorted(files),'labels':sorted(labels)}
# Validate every source delta before writing the new directory.
files={}
for name,entry in patch.items():
    rel=relative(name)
    if 'text' in entry:
        text=entry['text']
    else:
        original=(src/relative(entry['base'])).read_text()
        if sha(original.encode())!=entry['base_sha256']:
            raise RuntimeError('Delta base changed: '+name)
        text=original;previous=len(original)+1
        for start,end,replacement in reversed(entry['edits']):
            if not (0<=start<=end<=len(original) and end<previous):
                raise RuntimeError('Invalid or overlapping source delta: '+name)
            text=text[:start]+replacement+text[end:];previous=start
    if not isinstance(text,str) or sha(text.encode())!=entry['sha256']:
        raise RuntimeError('Reconstructed source differs from preflight: '+name)
    files[name]=text
for name in inv:
    target=dst/name;target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copy2(src/name,target)
for name,text in files.items():
    target=dst/name
    if name in inv and target.read_bytes()!=text.encode():
        saved=dst/'predecessor-v92-audit'/name
        saved.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(target,saved)
    target.parent.mkdir(parents=True,exist_ok=True);target.write_text(text)
(dst/'V92_BASELINE.json').write_text(json.dumps(base,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'staged','destination':str(dst),
                 'base_native_files':len(inv),'checked_patch_files':len(files),
                 'preflight_archive_sha256':sha(payload)},sort_keys=True))
