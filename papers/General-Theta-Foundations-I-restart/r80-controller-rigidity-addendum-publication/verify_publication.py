#!/usr/bin/env python3
import hashlib,json
from pathlib import Path
p=Path(__file__).resolve().parent
r=json.load(open(p/'PUBLICATION_RECEIPT.json'))
for x in r['artifacts']:
 f=p/x['path']
 if not f.is_file() or len(f.read_bytes())!=x['bytes'] or hashlib.sha256(f.read_bytes()).hexdigest()!=x['sha256']:
  raise RuntimeError('Artifact mismatch: '+x['path'])
b=json.load(open(p/'BUILD_RECEIPT.json'))
if b['status']!='PASS' or b['source_commit']!=r['source_commit']:
 raise RuntimeError('Wrong strict source receipt')
print(json.dumps({'status':'PASS','artifacts':len(r['artifacts']),'source_commit':r['source_commit'],'scope':'Artifact hashes and source-receipt correspondence; not mathematical proof.'},indent=2))
