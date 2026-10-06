#!/usr/bin/env python3
"""Restore the inherited evidence naming contract; immutable objects only."""
from pathlib import Path
import base64,hashlib,json,os,urllib.request
root=Path('papers/A2-DYN-v24-referee-response')
oldtree='a4ec722325135f2fc524de8e818c6c9c3788a7cd'
script=root/'build.sh'
before=script.read_bytes()
old=b'> "evidence/${script}.json"'
new=b'> "evidence/${script}.py.json"'
if before.count(old)!=1:raise RuntimeError('build naming patch is not unique')
after=before.replace(old,new,1)
manifest=json.loads((root/'SOURCE_MANIFEST.json').read_text())
if hashlib.sha256(before).hexdigest()!=manifest['source_sha256']['build.sh']:
    raise RuntimeError('build source hash mismatch before repair')
manifest['source_sha256']['build.sh']=hashlib.sha256(after).hexdigest()
files={'build.sh':after,'SOURCE_MANIFEST.json':(json.dumps(manifest,indent=2,sort_keys=True)+'\n').encode()}
api='https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/'
headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json',
 'Content-Type':'application/json','User-Agent':'a2-dyn-build-contract-repair'}
def request(endpoint,body=None):
    if not (endpoint in ('blobs','trees') or endpoint=='trees/'+oldtree):raise RuntimeError('immutable objects only')
    req=urllib.request.Request(api+endpoint,data=None if body is None else json.dumps(body).encode(),
                              headers=headers,method='GET' if body is None else 'POST')
    with urllib.request.urlopen(req,timeout=60) as response:return json.load(response)
entries=[]
for name,data in files.items():
    result=request('blobs',{'encoding':'base64','content':base64.b64encode(data).decode()})
    expected=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if result['sha']!=expected:raise RuntimeError('blob mismatch')
    entries.append({'path':name,'mode':'100755' if name=='build.sh' else '100644','type':'blob','sha':expected})
base=request('trees/'+oldtree)
if base.get('truncated'):raise RuntimeError('truncated paper tree')
items={e['path']:{k:e[k] for k in ('path','mode','type','sha')} for e in base['tree']}
for e in entries:items[e['path']]=e
body=b''
for e in sorted(items.values(),key=lambda e:(e['path']+('/' if e['type']=='tree' else '')).encode()):
    body+=e['mode'].lstrip('0').encode()+b' '+e['path'].encode()+b'\0'+bytes.fromhex(e['sha'])
expected=hashlib.sha1(b'tree '+str(len(body)).encode()+b'\0'+body).hexdigest()
result=request('trees',{'base_tree':oldtree,'tree':entries})
if result['sha']!=expected:raise RuntimeError('new tree mismatch')
receipt={'paper_tree':expected,'prior_paper_tree':oldtree,'changed_blobs':entries,
 'build_sha256':manifest['source_sha256']['build.sh'],'mathematical_source_changed':False,
 'branch_refs_changed':False,'commits_created':False,'reason':'restore evidence/${script}.py.json expected by verify_v2.py'}
Path('v24-buildfix-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
