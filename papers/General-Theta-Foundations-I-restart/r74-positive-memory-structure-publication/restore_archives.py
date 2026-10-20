#!/usr/bin/env python3
"""Restore complete R74 delivery archives from verified ordinary Git blobs."""
import argparse
import hashlib
import json
from pathlib import Path

parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--out',type=Path,required=True)
args=parser.parse_args()
root=Path(__file__).resolve().parent
manifest=json.loads((root/'archives/ARCHIVE_PARTS.json').read_text())
args.out.mkdir(parents=True,exist_ok=True)
for item in manifest['archives']:
    bodies=[]
    for part in item['parts']:
        data=(root/part['path']).read_bytes()
        if len(data)!=part['bytes'] or hashlib.sha256(data).hexdigest()!=part['sha256']:
            raise SystemExit('Part identity mismatch: '+part['path'])
        bodies.append(data)
    data=b''.join(bodies)
    if len(data)!=item['bytes'] or hashlib.sha256(data).hexdigest()!=item['sha256']:
        raise SystemExit('Complete archive identity mismatch: '+item['file'])
    target=args.out/item['file']
    if target.exists():
        if hashlib.sha256(target.read_bytes()).hexdigest()!=item['sha256']:
            raise SystemExit('Refusing to replace a different existing file: '+str(target))
    else:
        target.write_bytes(data)
    print(json.dumps({'file':str(target),'bytes':len(data),'sha256':item['sha256'],'status':'VERIFIED'}))
