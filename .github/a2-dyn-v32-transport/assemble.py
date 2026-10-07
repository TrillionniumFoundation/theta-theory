#!/usr/bin/env python3
"""One-time checksum-bound source transport. Creates blobs/trees only."""
from pathlib import Path
import base64, hashlib, json, lzma, os, shutil, time, urllib.request, urllib.error
EXPECTED='d6462c94e0cb7a702bf4e46e60da0440fb94a5ac'
PACKET='f8c9d3dff3090c517df3ed8d38ddb10c51a1a0b500c2a810f3d38ade250f4826'
BASE_TREE='06d63ae32efec644d907a0d3d0118c54b8e74c4c'
REPO='TrillionniumFoundation/theta-theory'
SKIP={'build','evidence','__pycache__'}

def require(value, message):
    if not value: raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def obj(kind, data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()

def ordinary(root):return [p for p in sorted(root.rglob('*')) if p.is_file() and not any(x in SKIP for x in p.relative_to(root).parts)]

def tree_hash(root):
    rows=[]
    for p in root.iterdir():
        if p.name in SKIP:continue
        require(not p.is_symlink(),'unexpected symlink')
        if p.is_dir():mode='40000';sha=tree_hash(p);key=p.name+'/'
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';sha=obj('blob',p.read_bytes());key=p.name
        rows.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+sha))
    return obj('tree',b''.join(row for _,row in sorted(rows)))

def post(suffix, data):
    # The only permitted writes in this transport are immutable objects.
    require(suffix in ('git/blobs','git/trees'),'forbidden write endpoint')
    url='https://api.github.com/repos/'+REPO+'/'+suffix
    headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'}
    payload=json.dumps(data).encode()
    for attempt in range(3):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,payload,headers,method='POST'),timeout=60) as response:return json.load(response)
        except urllib.error.HTTPError as e:
            if e.code not in (429,500,502,503,504) or attempt==2:raise
            time.sleep(2**attempt)
    raise RuntimeError('unreachable')

root=Path.cwd();transport=root/'.github/a2-dyn-v32-transport'
encoded=''.join((transport/f'part{i}.b64').read_text().strip() for i in range(1,5))
packed=base64.b64decode(encoded,validate=True)
require(hashlib.sha256(packed).hexdigest()==PACKET,'packet digest')
payload=json.loads(lzma.decompress(packed))
require(payload['base_tree']==BASE_TREE and payload['target_tree']==EXPECTED,'tree targets')
base=root/'papers/A2-DYN-v31-referee-response';target=root/'papers/A2-DYN-v32-referee-response'
require(tree_hash(base).hex()==BASE_TREE,'actual baseline tree')
require(not target.exists(),'target already present; refusing overwrite')
shutil.copytree(base,target,ignore=shutil.ignore_patterns(*SKIP))
for rel,entry in payload['files'].items():
    p=target/rel;require(p.resolve().is_relative_to(target.resolve()),'unsafe relative source path')
    p.parent.mkdir(parents=True,exist_ok=True);p.write_text(entry['content']);p.chmod(int(entry['mode'],8))
ledger=json.loads((target/'INHERITED_EDITS.json').read_text())
for edit in ledger['edits']:
    p=target/edit['path'];text=p.read_text()
    require(text.count(edit['before'])==1,'nonunique edit '+edit['path'])
    p.write_text(text.replace(edit['before'],edit['after'],1))
manifest=payload['manifest_header']
manifest['baseline_sha256']={p.relative_to(base).as_posix():digest(p) for p in ordinary(base)}
manifest['source_sha256']={p.relative_to(target).as_posix():digest(p) for p in ordinary(target) if p.name!='SOURCE_MANIFEST.json'}
(target/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
require(tree_hash(target).hex()==EXPECTED,'replayed ordinary paper tree')
report=root/manifest['controlling_review_path']
require(obj('blob',report.read_bytes()).hex()==manifest['controlling_review_blob'],'frozen controlling report')
workflow=payload['qualification_workflow']
require(hashlib.sha256(workflow.encode()).hexdigest()==manifest['qualification_workflow_sha256'],'qualification workflow digest')
changed=[]
for p in ordinary(target):
    rel=p.relative_to(target).as_posix();old=base/rel
    mode='100755' if p.stat().st_mode&0o111 else '100644'
    if old.exists() and old.read_bytes()==p.read_bytes() and bool(old.stat().st_mode&0o111)==bool(p.stat().st_mode&0o111):continue
    blob=post('git/blobs',{'content':base64.b64encode(p.read_bytes()).decode(),'encoding':'base64'})['sha']
    require(blob==obj('blob',p.read_bytes()).hex(),'uploaded blob '+rel)
    changed.append({'path':rel,'type':'blob','mode':mode,'sha':blob})
actual=post('git/trees',{'base_tree':BASE_TREE,'tree':changed})['sha']
require(actual==EXPECTED,'remote immutable paper tree')
receipt={'revision':32,'paper_tree':actual,'baseline_tree':BASE_TREE,'packet_sha256':PACKET,'changed_objects':changed,'ordinary_file_count':len(ordinary(target)),'stage_sha':os.environ.get('GITHUB_SHA'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'controlling_review_verified':True,'commits_created':False,'refs_moved':False,'qualification_pending':True}
(root/'v32-assembly-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'paper_tree':actual,'changed_object_count':len(changed),'commits_created':False,'refs_moved':False}))
