#!/usr/bin/env python3
"""Replay six declared edits and create immutable Git objects only; never move refs."""
from pathlib import Path,PurePosixPath
import base64,hashlib,json,os,shutil,sys,tempfile,time,urllib.request,urllib.error,zlib
PACKED='e82c4f2bf50445e9ba155f5d2f663699461bf6dfe3bae0c9cde6a206cafcff41'
PACKET='9de12b77b28d33c7cffa67346ca4422d1619de6a1b8677788be6b3364152e047'
EXPECTED='06d63ae32efec644d907a0d3d0118c54b8e74c4c'
BASE_TREE='7e47c9606ea21b79836319a7fa25d34bdf2a4b3c'
REPOSITORY='TrillionniumFoundation/theta-theory'
BASE=Path.cwd()/'papers/A2-DYN-v30-referee-response'
HERE=Path(__file__).resolve().parent

def need(ok,msg):
    if not ok:raise RuntimeError(msg)
def h(raw):return hashlib.sha256(raw).hexdigest()
def obj(kind,raw):return hashlib.sha1(kind.encode()+b' '+str(len(raw)).encode()+b'\0'+raw).digest()
def ordinary(root):
    return [p for p in sorted(root.rglob('*')) if p.is_file() and not any(s in ('build','evidence','__pycache__') for s in p.relative_to(root).parts)]
def mode(p):return '100755' if p.stat().st_mode&0o111 else '100644'
def tree(root):
    rows=[]
    for p in root.iterdir():
        if p.name in ('build','evidence','__pycache__'):continue
        if p.is_dir():m='40000';sha=tree(p);key=p.name+'/'
        else:m=mode(p);sha=obj('blob',p.read_bytes());key=p.name
        rows.append((key,m.encode()+b' '+p.name.encode()+b'\0'+sha))
    return obj('tree',b''.join(v for _,v in sorted(rows)))
def api(path,payload):
    url='https://api.github.com/repos/'+REPOSITORY+path
    body=json.dumps(payload).encode()
    headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json','User-Agent':'a2-dyn-v31-exact-objects'}
    for attempt in range(4):
        try:
            with urllib.request.urlopen(urllib.request.Request(url,data=body,headers=headers,method='POST'),timeout=60) as r:return json.load(r)
        except urllib.error.HTTPError as err:
            if err.code not in (429,500,502,503,504) or attempt==3:raise
            time.sleep(2**attempt)

def main():
    packed=base64.b64decode(''.join((HERE/f'chunk{i:02}.b64').read_text().strip() for i in range(1,17)),validate=True)
    need(h(packed)==PACKED,'packed digest')
    raw=zlib.decompress(packed);need(h(raw)==PACKET,'packet digest');data=json.loads(raw)
    need(data['expected_paper_tree']==EXPECTED and data['baseline_paper_tree']==BASE_TREE,'expected trees')
    need(tree(BASE).hex()==BASE_TREE,'checkout baseline tree')
    with tempfile.TemporaryDirectory() as temporary:
        target=Path(temporary)/'paper';target.mkdir()
        for f in ordinary(BASE):
            dst=target/f.relative_to(BASE);dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dst)
        seen=set()
        for f in data['files']:
            rel=PurePosixPath(f['path']);need(not rel.is_absolute() and '..' not in rel.parts,'unsafe relative path')
            need(str(rel) not in seen,'duplicate file');seen.add(str(rel));content=f['content'].encode();need(h(content)==f['sha256'],'file hash '+str(rel))
            dst=target/str(rel);dst.parent.mkdir(parents=True,exist_ok=True);dst.write_bytes(content);dst.chmod(int(f['mode'],8))
        ledger=json.loads((target/'INHERITED_EDITS.json').read_text());need(len(ledger['edits'])==6,'edit count')
        for rel in ('main.tex','references.tex'):
            text=(BASE/rel).read_text()
            for edit in ledger['edits']:
                if edit['path']!=rel:continue
                need(text.count(edit['before'])==1,'unique edit anchor '+rel);text=text.replace(edit['before'],edit['after'],1)
            (target/rel).write_text(text)
        manifest=data['manifest_metadata']
        manifest['baseline_sha256']={p.relative_to(BASE).as_posix():h(p.read_bytes()) for p in ordinary(BASE)}
        manifest['source_sha256']={p.relative_to(target).as_posix():h(p.read_bytes()) for p in ordinary(target) if p.name!='SOURCE_MANIFEST.json'}
        (target/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,sort_keys=True,indent=2)+'\n')
        need(h((target/'SOURCE_MANIFEST.json').read_bytes())==data['manifest_sha256'],'manifest replay hash')
        need(tree(target).hex()==EXPECTED,'complete ordinary source tree')
        receipt={'expected_paper_tree':EXPECTED,'baseline_paper_tree':BASE_TREE,'ordinary_files':len(ordinary(target)),'exact_inherited_edits':6,'packet_sha256':PACKET,'stage_sha':os.environ.get('GITHUB_SHA'),'workflow_run_id':os.environ.get('GITHUB_RUN_ID'),'commits_created':False,'branch_refs_modified':False}
        if '--dry-run' not in sys.argv:
            need(os.environ.get('GITHUB_REPOSITORY')==REPOSITORY,'repository scope')
            entries=[]
            for f in ordinary(target):
                rel=f.relative_to(target);old=BASE/rel
                if old.exists() and old.read_bytes()==f.read_bytes() and mode(old)==mode(f):continue
                content=f.read_bytes();sha=api('/git/blobs',{'content':base64.b64encode(content).decode(),'encoding':'base64'})['sha'];need(sha==obj('blob',content).hex(),'remote blob identity')
                entries.append({'path':rel.as_posix(),'mode':mode(f),'type':'blob','sha':sha})
            remote=api('/git/trees',{'base_tree':BASE_TREE,'tree':entries})['sha'];need(remote==EXPECTED,'remote paper identity')
            workflow=data['qualification_workflow'].encode();need(h(workflow)==manifest['qualification_workflow_sha256'],'qualification workflow identity')
            workflow_sha=api('/git/blobs',{'content':base64.b64encode(workflow).decode(),'encoding':'base64'})['sha'];need(workflow_sha==obj('blob',workflow).hex(),'workflow blob identity')
            receipt.update({'remote_paper_tree':remote,'qualification_workflow_blob':workflow_sha,'blobs_written':len(entries)+1})
        out=Path(os.environ.get('RUNNER_TEMP','/mnt/data'))/'a2-v31-assembly';out.mkdir(exist_ok=True)
        (out/'v31-assembly-receipt.json').write_text(json.dumps(receipt,sort_keys=True,indent=2)+'\n');print(json.dumps(receipt,indent=2,sort_keys=True))
if __name__=='__main__':main()
