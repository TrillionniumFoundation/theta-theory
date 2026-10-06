#!/usr/bin/env python3
"""One-time immutable Git-object transport. Never writes commits or refs."""
from pathlib import Path, PurePosixPath
import base64,hashlib,json,lzma,os,shutil,subprocess,sys,tempfile,urllib.request

REPO='TrillionniumFoundation/theta-theory'
BASE_COMMIT='253f7c56de1f198ff9bd5e13fa2009baf4551495'
BASE_TREE='0af99c96122be5032f1818feac344676ff31c705'
EXPECTED='e19803bed418d2a1402781124f91737c136b595b'
PACKET_SHA='8ce23c7cec4cc75c7c0810cd70374889838e0e1bab69aea368cad5f30e4a7cc8'
COMPRESSED_SHA='fce63d57f4da4419aeb47473660848d903ac15b6d6397147b70c6061f50f2fec'
HERE=Path(__file__).resolve().parent

def require(ok,message):
    if not ok:raise RuntimeError(message)
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def object_hash(kind,data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()
def tree_hash(root):
    entries=[]
    for p in root.iterdir():
        if p.is_dir():mode='40000';sha=tree_hash(p);key=p.name+'/'
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';sha=object_hash('blob',p.read_bytes());key=p.name
        entries.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+sha))
    return object_hash('tree',b''.join(data for _,data in sorted(entries)))
def ordinary(root):
    return [p for p in sorted(root.rglob('*')) if p.is_file() and not any(v in ('build','evidence','__pycache__') for v in p.parts)]
def post(kind,payload):
    require(kind in ('blobs','trees'),'non-object endpoint')
    req=urllib.request.Request('https://api.github.com/repos/'+REPO+'/git/'+kind,
        data=json.dumps(payload).encode(),method='POST',headers={
          'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],
          'Accept':'application/vnd.github+json','Content-Type':'application/json',
          'X-GitHub-Api-Version':'2022-11-28','User-Agent':'A2-DYN-v18-exact-object-transport'})
    with urllib.request.urlopen(req,timeout=60) as response:return json.load(response)

local='--local-check' in sys.argv
checkout=Path('/mnt/data/theta-work') if local else Path.cwd()
base=checkout/'papers/A2-DYN-v17-referee-response'
# Local diagnostic imports may have generated ignored Python bytecode.
with tempfile.TemporaryDirectory() as td:
    cleanbase=Path(td)/'base'
    shutil.copytree(base,cleanbase,ignore=shutil.ignore_patterns('build','evidence','__pycache__'))
    require(tree_hash(cleanbase).hex()==BASE_TREE,'baseline paper tree mismatch')
    encoded=''.join((HERE/f'part{i}.b64').read_text().strip() for i in range(1,7))
    compressed=base64.b64decode(encoded,validate=True)
    require(hashlib.sha256(compressed).hexdigest()==COMPRESSED_SHA,'compressed checksum')
    raw=lzma.decompress(compressed)
    require(hashlib.sha256(raw).hexdigest()==PACKET_SHA,'packet checksum')
    packet=json.loads(raw)
    require(packet['baseline_commit']==BASE_COMMIT and packet['baseline_paper_tree']==BASE_TREE,'baseline identities')
    require(packet['expected_paper_tree']==EXPECTED,'target identity')
    out=Path(td)/'paper';shutil.copytree(cleanbase,out)
    seen=set()
    for f in packet['files']:
        path=PurePosixPath(f['path'])
        require(not path.is_absolute() and '..' not in path.parts and path.as_posix() not in seen,'unsafe/duplicate path')
        require(f['mode'] in ('100644','100755'),'mode')
        seen.add(path.as_posix());dest=out/path;dest.parent.mkdir(parents=True,exist_ok=True)
        dest.write_text(f['content'],encoding='utf-8');dest.chmod(int(f['mode'][-3:],8))
    ledger=json.loads((out/'INHERITED_EDITS.json').read_text())
    require(ledger['baseline']==BASE_COMMIT and len(ledger['edits'])==6,'edit ledger')
    for e in ledger['edits']:
        require(e['path'] in ('main.tex','references.tex'),'unexpected inherited edit')
        dest=out/e['path'];s=dest.read_text()
        require(s.count(e['before'])==1,'nonunique exact edit')
        dest.write_text(s.replace(e['before'],e['after'],1))
    man=packet['manifest_metadata']
    man['baseline_sha256']={p.relative_to(cleanbase).as_posix():digest(p) for p in ordinary(cleanbase)}
    man['source_sha256']={p.relative_to(out).as_posix():digest(p) for p in ordinary(out) if p.name!='SOURCE_MANIFEST.json'}
    (out/'SOURCE_MANIFEST.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
    require(tree_hash(out).hex()==EXPECTED,'replayed ordinary source tree mismatch')
    changed=[p for p in ordinary(out) if not (cleanbase/p.relative_to(out)).exists() or
             p.read_bytes()!=(cleanbase/p.relative_to(out)).read_bytes()]
    if local:
        reference=checkout/'papers/A2-DYN-v18-referee-response'
        require(all(p.read_bytes()==(reference/p.relative_to(out)).read_bytes() for p in ordinary(out)),'local validated bytes differ')
        print(json.dumps({'expected_paper_tree':EXPECTED,'ordinary_files':len(ordinary(out)),'changed_files':len(changed),'local_byte_match':True},indent=2))
    else:
        require(os.environ.get('GITHUB_REPOSITORY')==REPO,'repository')
        head=subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip()
        require(head==os.environ['GITHUB_SHA'],'event checkout')
        tree=[];blobs={}
        for p in changed:
            rel=p.relative_to(out).as_posix();mode='100755' if p.stat().st_mode&0o111 else '100644'
            h=post('blobs',{'content':p.read_text(),'encoding':'utf-8'})['sha']
            require(h==object_hash('blob',p.read_bytes()).hex(),'remote blob differs')
            tree.append({'path':rel,'mode':mode,'type':'blob','sha':h});blobs[rel]=h
        result=post('trees',{'base_tree':BASE_TREE,'tree':tree})['sha']
        require(result==EXPECTED,'remote ordinary source differs')
        Path('assembly-receipt.json').write_text(json.dumps({'event_sha':head,'workflow_run_id':os.environ['GITHUB_RUN_ID'],
            'baseline_commit':BASE_COMMIT,'baseline_paper_tree':BASE_TREE,'ordinary_paper_tree':result,
            'ordinary_files':len(ordinary(out)),'created_blobs':blobs,'packet_sha256':PACKET_SHA,
            'commits_or_refs_written':False},indent=2,sort_keys=True)+'\n')
        print('Verified immutable paper tree '+result)
