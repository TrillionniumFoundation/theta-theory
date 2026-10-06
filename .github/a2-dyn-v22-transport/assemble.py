"""Create immutable Git objects for an exact validated source; never move refs."""
from pathlib import Path
import base64,gzip,hashlib,json,os,shutil,subprocess,time,urllib.request,urllib.error
REPO='TrillionniumFoundation/theta-theory'
EXPECTED='48ee252fdffc68d779069ce7a6c43ac564f8217f'
PACKET_SHA='e61807e43e4ec08eaf537b1d6872595fd0c9a111765165c5b0e8dccb3d7acbc9'
root=Path(__file__).resolve().parents[2]
base=root/'papers/A2-DYN-v20-referee-response'
target=root/'papers/A2-DYN-v22-referee-response'
def require(ok,msg):
    if not ok:raise RuntimeError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def object_sha(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).hexdigest()
def ordinary(path):
    return [p for p in sorted(path.rglob('*')) if p.is_file() and not any(x in ('build','evidence','__pycache__') for x in p.relative_to(path).parts)]
def tree_hash(path):
    entries=[]
    for p in path.iterdir():
        if p.name in ('build','evidence','__pycache__'):continue
        if p.is_dir():mode='40000';h=tree_hash(p);key=p.name+'/'
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';h=object_sha('blob',p.read_bytes());key=p.name
        entries.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+bytes.fromhex(h)))
    return object_sha('tree',b''.join(v for _,v in sorted(entries)))
require(os.environ['GITHUB_REPOSITORY']==REPO,'unexpected repository')
require(os.environ['GITHUB_REF_NAME']=='revision/a2-dyn-v22-referee-response-2026-10-06','unexpected assembly branch')
encoded=''.join(p.read_text().strip() for p in sorted(Path(__file__).parent.glob('part*.b64')))
compressed=base64.b64decode(encoded,validate=True)
require(sha(compressed)==PACKET_SHA,'transport digest mismatch')
data=json.loads(gzip.decompress(compressed))
require(data['expected_tree']==EXPECTED,'unexpected target tree')
require(tree_hash(base)==data['baseline_tree'],'baseline tree mismatch')
shutil.copytree(base,target)
for entry in data['files']:
    rel=Path(entry['path'])
    require(not rel.is_absolute() and '..' not in rel.parts,'unsafe source path')
    content=entry['content'].encode();require(object_sha('blob',content)==entry['blob'],'changed source blob')
    out=target/rel;out.parent.mkdir(parents=True,exist_ok=True);out.write_bytes(content)
    out.chmod(0o755 if entry['mode']=='100755' else 0o644)
ledger=json.loads((target/'INHERITED_EDITS.json').read_text())
for e in ledger['edits']:
    require(e['path'] in ('main.tex','references.tex'),'unexpected inherited edit')
    p=target/e['path'];s=p.read_text();require(s.count(e['before'])==1,'nonunique inherited edit')
    p.write_text(s.replace(e['before'],e['after'],1))
man=data['manifest_fields']
man['baseline_sha256']={p.relative_to(base).as_posix():sha(p.read_bytes()) for p in ordinary(base)}
man['source_sha256']={p.relative_to(target).as_posix():sha(p.read_bytes()) for p in ordinary(target) if p.name!='SOURCE_MANIFEST.json'}
(target/'SOURCE_MANIFEST.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
require(tree_hash(target)==EXPECTED,'assembled source differs from validated ordinary tree')

def post(endpoint,payload):
    require(endpoint in ('git/blobs','git/trees'),'only immutable objects may be written')
    body=json.dumps(payload).encode()
    req=urllib.request.Request('https://api.github.com/repos/'+REPO+'/'+endpoint,data=body,method='POST',headers={
      'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'})
    for attempt in range(4):
        try:
            with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
        except urllib.error.HTTPError as e:
            if e.code not in (429,500,502,503,504) or attempt==3:raise
            time.sleep(2**attempt)
    raise RuntimeError('immutable-object upload failed')
entries=[]
for p in ordinary(target):
    rel=p.relative_to(target).as_posix();bp=base/rel;content=p.read_bytes()
    mode='100755' if p.stat().st_mode&0o111 else '100644'
    if bp.exists() and bp.read_bytes()==content and bool(bp.stat().st_mode&0o111)==bool(p.stat().st_mode&0o111):continue
    h=object_sha('blob',content)
    remote=post('git/blobs',{'content':content.decode(),'encoding':'utf-8'})
    require(remote['sha']==h,'remote blob mismatch')
    entries.append({'path':rel,'mode':mode,'type':'blob','sha':h})
result=post('git/trees',{'base_tree':data['baseline_tree'],'tree':entries})
require(result['sha']==EXPECTED,'remote paper tree mismatch')
receipt={'event_sha':os.environ['GITHUB_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'paper_tree':EXPECTED,
 'transport_sha256':PACKET_SHA,'created_changed_blobs':len(entries),'commits_created':0,'branch_refs_moved':0}
out=root/'v22-assembly-receipt.json';out.write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n');print(out.read_text())
