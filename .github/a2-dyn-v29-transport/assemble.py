#!/usr/bin/env python3
"""Replay a checksum-bound manuscript delta; create Git objects, never commits or refs."""
from pathlib import Path, PurePosixPath
import base64,gzip,hashlib,json,os,shutil,tempfile,time,urllib.request,urllib.error
from concurrent.futures import ThreadPoolExecutor
PACKET_SHA='e0b24d9b0adfb36bfd34db90193d192684e238f876a59e2a50d273155bcd5c42'
EXPECTED_TREE='512509ff9d5a3141e3f53183bafe7fba61b4eebb'
BASE_TREE='ae335b52f013e3569e4a6b79b899cfc00e26b8e4'
repo=Path.cwd();base=repo/'papers/A2-DYN-v27-referee-response'

def require(ok,msg):
    if not ok:raise RuntimeError(msg)

def obj(kind,data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()

def tree(root):
    rows=[]
    for p in root.iterdir():
        if p.name in ('build','evidence','__pycache__'):continue
        if p.is_dir():mode='40000';sha=tree(p);key=p.name+'/'
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';sha=obj('blob',p.read_bytes());key=p.name
        rows.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+sha))
    return obj('tree',b''.join(row for _,row in sorted(rows)))

def ordinary(root):
    return [p for p in sorted(root.rglob('*')) if p.is_file()
            and not any(x in ('build','evidence','__pycache__') for x in p.relative_to(root).parts)]

def sha256(p):return hashlib.sha256(p.read_bytes()).hexdigest()

source=Path(__file__).parent
raw=base64.b64decode(''.join((source/f'piece{i:02}.b64').read_text().strip() for i in range(11)),validate=True)
require(hashlib.sha256(raw).hexdigest()==PACKET_SHA,'packet hash')
packet=json.loads(gzip.decompress(raw));require(packet['expected_tree']==EXPECTED_TREE,'expected target')
require(packet['baseline_tree']==BASE_TREE==tree(base).hex(),'frozen baseline')
with tempfile.TemporaryDirectory(prefix='a2-dyn-v29-') as temp:
    out=Path(temp)/'paper'
    shutil.copytree(base,out,ignore=shutil.ignore_patterns('build','evidence','__pycache__'))
    for rel,row in packet['new_files'].items():
        pp=PurePosixPath(rel);require(not pp.is_absolute() and '..' not in pp.parts,'unsafe relative path')
        p=out/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(row['text'])
        p.chmod(0o755 if row['mode']=='100755' else 0o644)
    main=(base/'main.tex').read_text()
    for e in json.loads((out/'INHERITED_EDITS.json').read_text())['edits']:
        require(e['path']=='main.tex' and main.count(e['before'])==1,'unique main replay')
        main=main.replace(e['before'],e['after'],1)
    (out/'main.tex').write_text(main)
    require(sha256(out/'main.tex')==packet['main_sha256'],'main identity')
    man=dict(packet['manifest_metadata'])
    man['baseline_sha256']={p.relative_to(base).as_posix():sha256(p) for p in ordinary(base)}
    man['source_sha256']={p.relative_to(out).as_posix():sha256(p) for p in ordinary(out) if p.name!='SOURCE_MANIFEST.json'}
    (out/'SOURCE_MANIFEST.json').write_text(json.dumps(man,indent=2,sort_keys=True)+'\n')
    require(tree(out).hex()==EXPECTED_TREE,'full reconstructed source identity')
    token=os.environ['GITHUB_TOKEN'];endpoint='https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']
    def post(path,data):
        require(path in ('/git/blobs','/git/trees'),'object-only endpoint')
        for attempt in range(4):
            req=urllib.request.Request(endpoint+path,json.dumps(data).encode(),
                {'Authorization':'Bearer '+token,'Accept':'application/vnd.github+json',
                 'X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json'},method='POST')
            try:
                with urllib.request.urlopen(req,timeout=45) as resp:return json.load(resp)
            except urllib.error.HTTPError as exc:
                if exc.code not in (429,500,502,503,504) or attempt==3:raise
                time.sleep(2**attempt)
        raise RuntimeError('unreachable')
    changed=[]
    for p in ordinary(out):
        rel=p.relative_to(out).as_posix();bp=base/rel
        mode='100755' if p.stat().st_mode&0o111 else '100644'
        if bp.exists() and p.read_bytes()==bp.read_bytes() and bool(p.stat().st_mode&0o111)==bool(bp.stat().st_mode&0o111):continue
        changed.append((rel,mode,p.read_bytes()))
    def upload(row):
        rel,mode,data=row
        result=post('/git/blobs',{'encoding':'base64','content':base64.b64encode(data).decode()})
        require(result['sha']==obj('blob',data).hex(),'server blob identity '+rel)
        return {'path':rel,'mode':mode,'type':'blob','sha':result['sha']}
    with ThreadPoolExecutor(max_workers=4) as pool:entries=list(pool.map(upload,changed))
    result=post('/git/trees',{'base_tree':BASE_TREE,'tree':entries})
    require(result['sha']==EXPECTED_TREE,'server paper tree identity')
    receipt={'stage_sha':os.environ['GITHUB_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],
             'packet_sha256':PACKET_SHA,'baseline_paper_tree':BASE_TREE,'paper_tree':result['sha'],
             'ordinary_files':len(ordinary(out)),'changed_blob_count':len(entries),
             'created_commits':False,'moved_branch_refs':False,'mathematical_qualification':False}
    (repo/'assembly-v29.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    print(json.dumps(receipt,indent=2,sort_keys=True))
