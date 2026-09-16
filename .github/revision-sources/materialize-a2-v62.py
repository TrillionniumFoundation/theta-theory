#!/usr/bin/env python3
"""Materialize checked v62 text sources; preserve old entries and all proof modules."""
from pathlib import Path
import hashlib, json, lzma
ROOT=Path(__file__).resolve().parents[2]
PREFIX='papers/A2-v17-boundary-information-coarsening/'
PARTS=('a2-v62-payload-00.xz','a2-v62-payload-01.xz')

def need(ok, message):
    if not ok: raise RuntimeError(message)

def main():
    raw=lzma.decompress(b''.join((Path(__file__).parent/name).read_bytes() for name in PARTS))
    need(hashlib.sha256(raw).hexdigest()=='b0bf113f1126d0a16ea589181a61912a70041803395594f53174385a6a2264eb','Payload digest mismatch')
    data=json.loads(raw)
    for name,text in data['files'].items():
        path=Path(name)
        need(not path.is_absolute() and '..' not in path.parts and '\\' not in name,'Unsafe path')
        need(name.startswith(PREFIX) or name in ('README.md','A2_REVISION_V62_INDEX.md'),'Unapproved target')
        dest=ROOT/path
        need(not dest.is_symlink(),'Symlink target')
        if dest.exists():
            old=dest.read_bytes()
            if name in data['expected']:
                need(hashlib.sha256(old).hexdigest()==data['expected'][name] or old==text.encode(),'Unexpected existing source: '+name)
            elif name!='README.md':
                need(old==text.encode(),'Refusing to overwrite new path: '+name)
    archive=ROOT/PREFIX/'history/v61-review-baseline'
    archive.mkdir(parents=True,exist_ok=True)
    for name,digest in data['expected'].items():
        dest=archive/Path(name).name
        if not dest.exists():
            old=(ROOT/name).read_bytes()
            need(hashlib.sha256(old).hexdigest()==digest,'Cannot archive already modified original')
            dest.write_bytes(old)
        need(hashlib.sha256(dest.read_bytes()).hexdigest()==digest,'Archive identity mismatch')
    root_archive=archive/'REPOSITORY_README.md'
    if not root_archive.exists(): root_archive.write_bytes((ROOT/'README.md').read_bytes())
    for name,text in data['files'].items():
        dest=ROOT/name; dest.parent.mkdir(parents=True,exist_ok=True); dest.write_text(text,encoding='utf-8')
    result={'version':62,'materialized_files':len(data['files']),'archived_originals':4,
            'payload_sha256':hashlib.sha256(raw).hexdigest(),'deleted_paths':[],'proof_certification':False}
    print(json.dumps(result,indent=2,sort_keys=True))

if __name__=='__main__':main()
