#!/usr/bin/env python3
"""One-time immutable-object transport; no commits or reference writes."""
from pathlib import Path, PurePosixPath
import base64, hashlib, json, lzma, os, shutil, tempfile, time
from urllib.request import Request, urlopen
from urllib.error import HTTPError

PACKET_SHA='6c7dccf493019458a4b9fda00bec8d51b79b8942f9ba32533cbb0f7401ce2d2c'
BASE_TREE='d6462c94e0cb7a702bf4e46e60da0440fb94a5ac'
EXPECTED_TREE='42ba62ef825d1e555f6c6bf83e647792bba67de8'

def require(ok,msg):
    if not ok: raise RuntimeError(msg)

def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def ordinary(root):
    return [p for p in sorted(root.rglob('*')) if p.is_file() and not any(s in ('build','evidence','__pycache__') for s in p.relative_to(root).parts)]

def obj(kind,data):
    return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()

def tree_hash(root):
    rows=[]
    for p in root.iterdir():
        if p.name in ('build','evidence','__pycache__'):continue
        if p.is_dir(): mode='40000';sha=tree_hash(p);key=p.name+'/'
        else: mode='100755' if p.stat().st_mode&0o111 else '100644';sha=obj('blob',p.read_bytes());key=p.name
        rows.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+sha))
    return obj('tree',b''.join(row for _,row in sorted(rows)))

def post(repo,endpoint,data):
    require(endpoint in ('git/blobs','git/trees'),'unapproved endpoint')
    req=Request('https://api.github.com/repos/'+repo+'/'+endpoint,data=json.dumps(data).encode(),method='POST',headers={'Authorization':'Bearer '+os.environ['GITHUB_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'})
    for attempt in range(4):
        try:
            with urlopen(req,timeout=60) as response:return json.load(response)
        except HTTPError as e:
            if e.code not in (429,500,502,503,504) or attempt==3:raise
            time.sleep(2**attempt)

def main():
    here=Path(__file__).resolve().parent
    chunks=sorted(here.glob('part*.b64'),key=lambda p:int(p.stem[4:]))
    packed=base64.b64decode(''.join(p.read_text().strip() for p in chunks),validate=True)
    require(hashlib.sha256(packed).hexdigest()==PACKET_SHA,'transport checksum')
    data=json.loads(lzma.decompress(packed));require(data['revision']==33 and data['baseline_tree']==BASE_TREE and data['expected_tree']==EXPECTED_TREE,'packet identity')
    repo_root=Path(os.environ['GITHUB_WORKSPACE'])
    baseline=repo_root/'papers/A2-DYN-v32-referee-response'
    require(tree_hash(baseline).hex()==BASE_TREE,'complete frozen baseline')
    work=Path(tempfile.mkdtemp(prefix='a2-dyn-v33-'))/'paper'
    shutil.copytree(baseline,work,ignore=shutil.ignore_patterns('build','evidence','__pycache__'))
    seen=set()
    for item in data['files']:
        rel=PurePosixPath(item['path'])
        require(not rel.is_absolute() and '..' not in rel.parts and str(rel) not in seen,'unsafe or duplicate path')
        seen.add(str(rel));require(item['mode'] in ('100644','100755'),'file mode')
        content=item['content'].encode();require(hashlib.sha256(content).hexdigest()==item['sha256'],'file checksum')
        p=work/str(rel);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(content);p.chmod(0o755 if item['mode']=='100755' else 0o644)
    ledger=json.loads((work/'INHERITED_EDITS.json').read_text());main_tex=(baseline/'main.tex').read_text()
    require(len(ledger['edits'])==5,'edit count')
    for edit in ledger['edits']:
        require(edit['path']=='main.tex' and main_tex.count(edit['before'])==1,'exact edit anchor')
        main_tex=main_tex.replace(edit['before'],edit['after'],1)
    (work/'main.tex').write_text(main_tex)
    manifest=data['manifest_metadata'];manifest['baseline_sha256']={p.relative_to(baseline).as_posix():digest(p) for p in ordinary(baseline)}
    manifest['source_sha256']={p.relative_to(work).as_posix():digest(p) for p in ordinary(work) if p.name!='SOURCE_MANIFEST.json'}
    (work/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
    require(tree_hash(work).hex()==EXPECTED_TREE,'complete reconstructed source differs')
    entries=[]
    for p in ordinary(work):
        rel=p.relative_to(work).as_posix();old=baseline/rel;mode='100755' if p.stat().st_mode&0o111 else '100644'
        if old.exists() and p.read_bytes()==old.read_bytes() and bool(p.stat().st_mode&0o111)==bool(old.stat().st_mode&0o111):continue
        sha=obj('blob',p.read_bytes()).hex()
        got=post(os.environ['GITHUB_REPOSITORY'],'git/blobs',{'content':base64.b64encode(p.read_bytes()).decode(),'encoding':'base64'})
        require(got['sha']==sha,'remote blob mismatch')
        entries.append({'path':rel,'mode':mode,'type':'blob','sha':sha})
    got=post(os.environ['GITHUB_REPOSITORY'],'git/trees',{'base_tree':BASE_TREE,'tree':entries})
    require(got['sha']==EXPECTED_TREE,'remote paper tree mismatch')
    receipt={'revision':33,'event_sha':os.environ.get('GITHUB_SHA'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'packet_sha256':PACKET_SHA,'baseline_tree':BASE_TREE,'paper_tree':EXPECTED_TREE,'ordinary_files':len(ordinary(work)),'changed_blobs':len(entries),'remote_objects_created':True,'commit_created':False,'branch_ref_written':False,'proof_certification':False}
    print(json.dumps(receipt,indent=2))
    (repo_root/'v33-assembly-receipt.json').write_text(json.dumps(receipt,indent=2)+'\n')
if __name__=='__main__':main()
