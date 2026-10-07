#!/usr/bin/env python3
"""Checksum-bound ordinary-source transport; creates no commits or refs."""
from pathlib import Path
import base64,hashlib,json,lzma,os,shutil,tempfile,time,urllib.request,urllib.error
BASE_TREE='6101fe93f514d9586658d748e08a0ffd6c610044'
TARGET='ae335b52f013e3569e4a6b79b899cfc00e26b8e4'
XZ_SHA='bf382cb79b3df631954e1665a48a8fcbea6c87ab4d913db1b17d788ca3e4b5dd'
JSON_SHA='c53d0a8ede9aa8513d078d7b9491657a8ce504311297356f53a8b20c3ae97b02'
HERE=Path(__file__).resolve().parent
REPO=Path(os.environ.get('GITHUB_WORKSPACE','/mnt/data/theta-work'))
BASE=REPO/'papers/A2-DYN-v26-referee-response'
SKIP={'build','evidence','__pycache__','.git'}
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def ordinary(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(s in SKIP for s in p.relative_to(root).parts))
def sha(data):return hashlib.sha256(data).hexdigest()
def gitobj(kind,data):return hashlib.sha1(kind+b' '+str(len(data)).encode()+b'\0'+data).digest()
def tree(root):
    entries=[]
    for p in root.iterdir():
        if p.name in SKIP:continue
        if p.is_dir():mode='40000';ident=tree(p);key=p.name+'/'
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';ident=gitobj(b'blob',p.read_bytes());key=p.name
        entries.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+ident))
    return gitobj(b'tree',b''.join(v for _,v in sorted(entries)))
parts=sorted(HERE.glob('part*.b64'))
require(len(parts)==5,'expected five packet parts')
xz=base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True)
require(sha(xz)==XZ_SHA,'transport checksum')
data=lzma.decompress(xz);require(sha(data)==JSON_SHA,'decoded checksum')
packet=json.loads(data)
require(packet['expected_paper_tree']==TARGET,'declared target')
require(tree(BASE).hex()==BASE_TREE,'exact author baseline')
with tempfile.TemporaryDirectory(prefix='a2-dyn-v27-') as temp:
    root=Path(temp)/'paper'
    shutil.copytree(BASE,root,ignore=shutil.ignore_patterns(*SKIP))
    for rel,item in packet['files'].items():
        p=Path(rel);require(not p.is_absolute() and '..' not in p.parts,'unsafe relative path')
        dst=root/p;dst.parent.mkdir(parents=True,exist_ok=True)
        dst.write_text(item['content'],encoding='utf-8')
        dst.chmod(int(item['mode'],8))
    ledger=json.loads((root/'INHERITED_EDITS.json').read_text())
    require(len(ledger['edits'])==6,'edit count')
    for edit in ledger['edits']:
        require(edit['path'] in ('main.tex','references.tex'),'edit scope')
        dst=root/edit['path'];text=dst.read_text()
        require(text.count(edit['before'])==1,'nonunique exact edit')
        dst.write_text(text.replace(edit['before'],edit['after'],1))
    man=packet['manifest_template']
    man['baseline_sha256']={p.relative_to(BASE).as_posix():sha(p.read_bytes()) for p in ordinary(BASE)}
    man['source_sha256']={p.relative_to(root).as_posix():sha(p.read_bytes()) for p in ordinary(root) if p.name!='SOURCE_MANIFEST.json'}
    (root/'SOURCE_MANIFEST.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
    actual=tree(root).hex();require(actual==TARGET,'ordinary source tree mismatch: '+actual)
    changed=[]
    for p in ordinary(root):
        rel=p.relative_to(root).as_posix();old=BASE/rel
        if not old.exists() or old.read_bytes()!=p.read_bytes() or (old.stat().st_mode&0o111)!=(p.stat().st_mode&0o111):
            changed.append({'path':rel,'mode':'100755' if p.stat().st_mode&0o111 else '100644','type':'blob','content':p.read_text()})
    if not os.environ.get('A2_DYN_TRANSPORT_DRY_RUN'):
        token=os.environ['GH_TOKEN']
        body=json.dumps({'base_tree':BASE_TREE,'tree':changed}).encode()
        request=urllib.request.Request('https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/trees',data=body,method='POST',headers={'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28','User-Agent':'a2-dyn-exact-source-transport'})
        for attempt in range(5):
            try:
                with urllib.request.urlopen(request,timeout=90) as response:result=json.load(response)
                break
            except urllib.error.HTTPError as error:
                if error.code not in (429,500,502,503,504) or attempt==4:raise
                time.sleep(2**attempt)
        require(result['sha']==TARGET,'remote immutable tree mismatch')
    receipt={'staging_sha':os.environ.get('GITHUB_SHA'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'baseline_paper_tree':BASE_TREE,'ordinary_paper_tree':TARGET,'ordinary_files':len(ordinary(root)),'changed_entries':len(changed),'xz_sha256':XZ_SHA,'json_sha256':JSON_SHA,'created_commits':False,'moved_branch_refs':False,'dry_run':bool(os.environ.get('A2_DYN_TRANSPORT_DRY_RUN'))}
    Path('/tmp/a2-dyn-v27-assembly.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))
