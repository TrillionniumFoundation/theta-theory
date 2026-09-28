#!/usr/bin/env python3
"""Verify and compare the v61/v62 frozen source ZIPs inside native artifacts."""
from zipfile import ZipFile
from io import BytesIO
from pathlib import Path
import argparse, json, hashlib

def sha(data): return hashlib.sha256(data).hexdigest()
def blob(data): return hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
def load(path):
    with ZipFile(path) as outer:
        raw=outer.read('native-source.zip')
    with ZipFile(BytesIO(raw)) as inner:
        manifest=json.loads(inner.read('SOURCE_MANIFEST.json'))
        files={}
        for name,rec in manifest['files'].items():
            data=inner.read('source/'+name)
            if (len(data),sha(data),blob(data))!=(rec['bytes'],rec['sha256'],rec['git_blob']):
                raise RuntimeError('Frozen source mismatch: '+name)
            files[name]=data
    return files

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('old',type=Path);ap.add_argument('new',type=Path)
    a=ap.parse_args();old=load(a.old);new=load(a.new)
    missing=sorted(set(old)-set(new));changed=sorted(n for n in old.keys() & new.keys() if old[n]!=new[n])
    print(json.dumps({'old_frozen_files_verified':len(old),'new_frozen_files_verified':len(new),
        'missing_inherited_files':missing,'changed_inherited_files':changed,
        'byte_identical_inherited_files':sum(new.get(n)==b for n,b in old.items()),
        'added_paths':sorted(set(new)-set(old)),
        'old_artifact_sha256':sha(a.old.read_bytes()),'new_artifact_sha256':sha(a.new.read_bytes())},indent=2))
