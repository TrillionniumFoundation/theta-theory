#!/usr/bin/env python3
"""Replay the checksum-bound source delta; create Git objects, never commits or refs."""
from pathlib import Path, PurePosixPath
import base64, hashlib, json, os, shutil, sys, tempfile, urllib.request, zlib
PACKET_SHA='e65a001d529f5a758bcb06af39307c3cf12770c4e84a0f18d2890258a9b9ace9'
BASE_TREE='48ee252fdffc68d779069ce7a6c43ac564f8217f'
PAPER_TREE='37e6f9a75ad1a6bb4f2c8710494cc50edac9e7c9'
REPO='TrillionniumFoundation/theta-theory'
base=Path('papers/A2-DYN-v22-referee-response')
transport=Path(__file__).resolve().parent

def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def object_hash(kind,data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()
def ordinary(root):
    return [p for p in sorted(root.rglob('*')) if p.is_file()
            and not any(x in ('build','evidence','__pycache__') for x in p.relative_to(root).parts)]
def tree_hash(root):
    rows=[]
    for p in root.iterdir():
        if p.name in ('build','evidence','__pycache__'):continue
        if p.is_dir(): mode='40000';sha=tree_hash(p);key=p.name+'/'
        else: mode='100755' if p.stat().st_mode&0o111 else '100644';sha=object_hash('blob',p.read_bytes());key=p.name
        rows.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+sha))
    return object_hash('tree',b''.join(row for _,row in sorted(rows)))
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()

parts=sorted(transport.glob('part*.b64'))
require(len(parts)==5,'wrong transport part count')
raw=zlib.decompress(base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True))
require(hashlib.sha256(raw).hexdigest()==PACKET_SHA,'transport checksum')
payload=json.loads(raw)
require(payload['revision']==23 and payload['baseline_tree']==BASE_TREE and payload['paper_tree']==PAPER_TREE,'source identity')
require(tree_hash(base).hex()==BASE_TREE,'frozen baseline differs')
with tempfile.TemporaryDirectory(prefix='a2-dyn-v23-') as tmp:
    root=Path(tmp)/'paper'
    shutil.copytree(base,root,ignore=shutil.ignore_patterns('build','evidence','__pycache__'))
    for rel,record in payload['files'].items():
        pure=PurePosixPath(rel)
        require(not pure.is_absolute() and '..' not in pure.parts and '.git' not in pure.parts,'unsafe source path')
        require(record['mode'] in ('100644','100755'),'unexpected source mode')
        p=root/rel;p.parent.mkdir(parents=True,exist_ok=True)
        p.write_text(record['content'],encoding='utf-8');p.chmod(int(record['mode'][-3:],8))
    ledger=json.loads((root/'INHERITED_EDITS.json').read_text())
    require(ledger['baseline_paper_tree']==BASE_TREE and len(ledger['edits'])==5,'edit identity')
    main=(base/'main.tex').read_text()
    for e in ledger['edits']:
        require(e['path']=='main.tex' and main.count(e['before'])==1,'unexpected inherited edit')
        main=main.replace(e['before'],e['after'],1)
    (root/'main.tex').write_text(main)
    man=payload['manifest_metadata']
    man['baseline_sha256']={p.relative_to(base).as_posix():sha(p) for p in ordinary(base)}
    man['source_sha256']={p.relative_to(root).as_posix():sha(p) for p in ordinary(root) if p.name!='SOURCE_MANIFEST.json'}
    (root/'SOURCE_MANIFEST.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
    require(tree_hash(root).hex()==PAPER_TREE,'replayed paper tree differs')
    changes=[]
    for p in ordinary(root):
        rel=p.relative_to(root).as_posix();old=base/rel
        mode='100755' if p.stat().st_mode&0o111 else '100644'
        if not old.exists() or old.read_bytes()!=p.read_bytes() or (old.stat().st_mode&0o111)!=(p.stat().st_mode&0o111):
            changes.append((rel,mode,p.read_bytes()))
    receipt={'packet_sha256':PACKET_SHA,'baseline_tree':BASE_TREE,'paper_tree':PAPER_TREE,
             'changed_files':len(changes),'ordinary_files':len(ordinary(root)),
             'source_event_sha':os.environ.get('GITHUB_SHA'),'run_id':os.environ.get('GITHUB_RUN_ID'),
             'commits_created':False,'branch_refs_changed':False}
    if '--dry-run' not in sys.argv:
        require(os.environ.get('GITHUB_REPOSITORY')==REPO,'unexpected repository')
        token=os.environ['GH_TOKEN']
        def post(endpoint,data):
            require(endpoint in ('git/blobs','git/trees'),'non-object endpoint forbidden')
            req=urllib.request.Request('https://api.github.com/repos/'+REPO+'/'+endpoint,
                data=json.dumps(data).encode(),method='POST',headers={'Authorization':'Bearer '+token,
                'Accept':'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'})
            with urllib.request.urlopen(req,timeout=90) as response:return json.load(response)
        entries=[]
        for rel,mode,data in changes:
            result=post('git/blobs',{'content':data.decode('utf-8'),'encoding':'utf-8'})
            digest=object_hash('blob',data).hex();require(result['sha']==digest,'remote blob differs')
            entries.append({'path':rel,'mode':mode,'type':'blob','sha':digest})
        result=post('git/trees',{'base_tree':BASE_TREE,'tree':entries})
        require(result['sha']==PAPER_TREE,'remote ordinary tree differs')
        receipt['remote_paper_tree']=result['sha']
    Path('assembly-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))
