#!/usr/bin/env python3
"""Replay a checksum-bound source delta; create only immutable blobs and trees."""
from pathlib import Path,PurePosixPath
import base64,hashlib,json,lzma,os,shutil,subprocess,sys,tempfile,urllib.request
REPO='TrillionniumFoundation/theta-theory'
BASE_COMMIT='68618cdaad6824912b49b505d58c9a9fcb0ab823'
BASE_TREE='e19803bed418d2a1402781124f91737c136b595b'
EXPECTED='57ea4229c9e344f9d61fd08be6ef7f7954d29feb'
RAW_SHA='9aa319112c1a0592912d8dd21c1b727d196d67e726ae77eebae27350c639feef'
COMPRESSED_SHA='1422c1b2faadf023258b01153523ad8f752f2e8c40680709b048dce7020e8f3d'
HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise RuntimeError(message)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def obj(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()
def tree_hash(root):
    rows=[]
    for p in root.iterdir():
        if p.is_dir():mode='40000';value=tree_hash(p);key=p.name+'/'
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';value=obj('blob',p.read_bytes());key=p.name
        rows.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+value))
    return obj('tree',b''.join(value for _,value in sorted(rows)))
def files(root):return sorted(p for p in root.rglob('*') if p.is_file())
def post(kind,payload):
    require(kind in ('blobs','trees'),'only immutable Git objects may be written')
    req=urllib.request.Request('https://api.github.com/repos/'+REPO+'/git/'+kind,
        method='POST',data=json.dumps(payload).encode(),headers={
        'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Accept':'application/vnd.github+json',
        'Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28',
        'User-Agent':'A2-DYN-v19-exact-object-transport'})
    with urllib.request.urlopen(req,timeout=60) as r:return json.load(r)
local='--local-check' in sys.argv
checkout=Path('/mnt/data/theta-work') if local else Path.cwd()
with tempfile.TemporaryDirectory() as td:
    base=Path(td)/'base'
    shutil.copytree(checkout/'papers/A2-DYN-v18-referee-response',base,
                    ignore=shutil.ignore_patterns('build','evidence','__pycache__'))
    require(tree_hash(base).hex()==BASE_TREE,'baseline tree mismatch')
    encoded=''.join((HERE/f'part{i}.b64').read_text().strip() for i in range(1,7))
    compressed=base64.b64decode(encoded,validate=True)
    require(hashlib.sha256(compressed).hexdigest()==COMPRESSED_SHA,'compressed checksum')
    raw=lzma.decompress(compressed);require(hashlib.sha256(raw).hexdigest()==RAW_SHA,'packet checksum')
    packet=json.loads(raw)
    require(packet['baseline_commit']==BASE_COMMIT and packet['baseline_paper_tree']==BASE_TREE,'baseline metadata')
    require(packet['expected_paper_tree']==EXPECTED,'target metadata')
    out=Path(td)/'paper';shutil.copytree(base,out);seen=set()
    for f in packet['files']:
        p=PurePosixPath(f['path']);require(not p.is_absolute() and '..' not in p.parts and str(p) not in seen,'unsafe or duplicate path')
        require(f['mode'] in ('100644','100755'),'file mode');seen.add(str(p))
        dest=out/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_text(f['content']);dest.chmod(int(f['mode'][-3:],8))
    ledger=json.loads((out/'INHERITED_EDITS.json').read_text())
    require(ledger['baseline']==BASE_COMMIT and len(ledger['edits'])==5,'edit ledger identity')
    for e in ledger['edits']:
        require(e['path']=='main.tex','unlisted inherited edit')
        path=out/e['path'];text=path.read_text();require(text.count(e['before'])==1,'nonunique edit')
        path.write_text(text.replace(e['before'],e['after'],1))
    man=packet['manifest_metadata']
    man['baseline_sha256']={p.relative_to(base).as_posix():sha(p) for p in files(base)}
    man['source_sha256']={p.relative_to(out).as_posix():sha(p) for p in files(out) if p.name!='SOURCE_MANIFEST.json'}
    (out/'SOURCE_MANIFEST.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
    require(tree_hash(out).hex()==EXPECTED,'ordinary source hash after replay')
    changed=[p for p in files(out) if not(base/p.relative_to(out)).exists() or p.read_bytes()!=(base/p.relative_to(out)).read_bytes()]
    if local:
        reference=checkout/'papers/A2-DYN-v19-referee-response'
        require(all(p.read_bytes()==(reference/p.relative_to(out)).read_bytes() for p in files(out)),'local compiled bytes differ')
        print(json.dumps({'ordinary_paper_tree':EXPECTED,'ordinary_files':len(files(out)),
                          'changed_files':len(changed),'local_byte_match':True},indent=2))
    else:
        require(os.environ.get('GITHUB_REPOSITORY')==REPO,'wrong repository')
        head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
        require(head==os.environ['GITHUB_SHA'],'not event checkout')
        entries=[];blobs={}
        for p in changed:
            rel=p.relative_to(out).as_posix();mode='100755' if p.stat().st_mode&0o111 else '100644'
            h=post('blobs',{'content':p.read_text(),'encoding':'utf-8'})['sha']
            require(h==obj('blob',p.read_bytes()).hex(),'remote blob mismatch')
            blobs[rel]=h;entries.append({'path':rel,'mode':mode,'type':'blob','sha':h})
        h=post('trees',{'base_tree':BASE_TREE,'tree':entries})['sha'];require(h==EXPECTED,'remote tree mismatch')
        Path('assembly-receipt.json').write_text(json.dumps({'event_sha':head,'workflow_run_id':os.environ['GITHUB_RUN_ID'],
            'baseline_commit':BASE_COMMIT,'baseline_paper_tree':BASE_TREE,'ordinary_paper_tree':h,
            'ordinary_files':len(files(out)),'created_blobs':blobs,'packet_sha256':RAW_SHA,
            'commits_or_refs_written':False},indent=2,sort_keys=True)+'\n')
        print('Verified immutable paper tree '+h)
