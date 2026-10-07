"""One-time checksum-bound source transport; creates objects, never commits or refs."""
from pathlib import Path
import base64,hashlib,json,os,shutil,stat,urllib.request,zlib
ROOT=Path.cwd(); TRANS=ROOT/'.github/a2-dyn-v30-transport'
EXPECTED='0330507c574373cc1fadf0c0deb5c15a164b23c5eac757fa3039da2ce2b5f6b8'
TARGET='7e47c9606ea21b79836319a7fa25d34bdf2a4b3c'
BASE='512509ff9d5a3141e3f53183bafe7fba61b4eebb'

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def ordinary(root):
    return sorted(p for p in root.rglob('*') if p.is_file() and not any(x in ('build','evidence','__pycache__') for x in p.relative_to(root).parts))

def obj(kind,data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()

def tree_hash(root):
    payload=b''
    for p in sorted(root.iterdir(),key=lambda x:x.name+('/' if x.is_dir() else '')):
        if p.name in ('build','evidence','__pycache__'):continue
        require(not p.is_symlink(),'symlink not allowed')
        if p.is_dir():mode='40000';h=tree_hash(p)
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';h=obj('blob',p.read_bytes())
        payload+=mode.encode()+b' '+p.name.encode()+b'\0'+h
    return obj('tree',payload)

s=''.join(''.join(p.read_text().split()) for p in sorted(TRANS.glob('part*.b64')))
# Correct explicitly identified transport transcription errors before the immutable checksum.
fixes=[('rfaB3vqeBLPb','rfaB3v9qLPb'),('O+2YdvWh','O+2dvWh'),
 ('QawZbPc5cB29','QawZbPc5bB29'),('Yr4fcaxWyc1tn','Yr4fcaxW1tn'),
 ('d8AQNTJJrb','d8AQNTJrb'),('L06LKXdlJJ35','L06LKXdlJ35'),
 ('wojPg0FhxJJdm','wojPg0FhxJdm'),('Y7ERbfcfBe12','Y7ERb7e12'),('d52HPd68XNX','d52HPd68NX')]
for before,after in fixes:
    if before in s:
        require(s.count(before)==1,'ambiguous transport repair');s=s.replace(before,after,1)
raw=base64.b64decode(s,validate=True)
require(hashlib.sha256(raw).hexdigest()==EXPECTED,'compressed source checksum mismatch')
data=json.loads(zlib.decompress(raw));require(data['target_tree']==TARGET and data['base_tree']==BASE,'wrong packet trees')
require(data['base_directory']=='papers/A2-DYN-v29-referee-response' and data['target_directory']=='papers/A2-DYN-v30-referee-response','wrong scope')
b=ROOT/data['base_directory'];p=ROOT/data['target_directory']
require(tree_hash(b).hex()==BASE,'baseline ordinary tree differs')
require(not p.exists(),'target already exists')
shutil.copytree(b,p,ignore=shutil.ignore_patterns('build','evidence','__pycache__'))
for name,text in data['files'].items():
    rel=Path(name);require(not rel.is_absolute() and '..' not in rel.parts,'unsafe relative path')
    f=p/rel;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(text)
ledger=json.loads((p/'INHERITED_EDITS.json').read_text())
for edit in ledger['edits']:
    require(edit['path']=='main.tex','unexpected inherited edit scope')
    f=p/edit['path'];s=f.read_text();require(s.count(edit['before'])==1,'edit is not unique');f.write_text(s.replace(edit['before'],edit['after'],1))
man=data['manifest_metadata'];man['baseline_sha256']={x.relative_to(b).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in ordinary(b)}
man['source_sha256']={x.relative_to(p).as_posix():hashlib.sha256(x.read_bytes()).hexdigest() for x in ordinary(p) if x.name!='SOURCE_MANIFEST.json'}
(p/'SOURCE_MANIFEST.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
require(tree_hash(p).hex()==TARGET,'assembled ordinary tree differs')
API='https://api.github.com/repos/TrillionniumFoundation/theta-theory/git/'
def post(endpoint,payload):
    req=urllib.request.Request(API+endpoint,data=json.dumps(payload).encode(),method='POST',headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json'})
    with urllib.request.urlopen(req,timeout=45) as response:return json.load(response)
entries=[]
for f in ordinary(p):
    rel=f.relative_to(p).as_posix();old=b/rel
    if old.exists() and old.read_bytes()==f.read_bytes() and bool(old.stat().st_mode&0o111)==bool(f.stat().st_mode&0o111):continue
    blob=post('blobs',{'content':base64.b64encode(f.read_bytes()).decode(),'encoding':'base64'})
    require(blob['sha']==obj('blob',f.read_bytes()).hex(),'remote blob differs')
    entries.append({'path':rel,'mode':'100755' if f.stat().st_mode&0o111 else '100644','type':'blob','sha':blob['sha']})
tree=post('trees',{'base_tree':BASE,'tree':entries});require(tree['sha']==TARGET,'remote paper tree differs')
receipt={'event_sha':os.environ.get('GITHUB_SHA'),'run_id':os.environ.get('GITHUB_RUN_ID'),'paper_tree':TARGET,'compressed_sha256':EXPECTED,'created_changed_blobs':len(entries),'commits_created':False,'refs_moved':False}
Path('/tmp/a2-dyn-v30-assembly.json').write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt))
