"""One-time immutable Git-object transport, not the manuscript build."""
from pathlib import Path, PurePosixPath
import base64, hashlib, json, os, shutil, urllib.request, zlib
REPO='TrillionniumFoundation/theta-theory'
BASE_TREE='57ea4229c9e344f9d61fd08be6ef7f7954d29feb'
EXPECTED='cbfa76a8957d3d327655a9969d55cb4a9d3e24bb'
PACKET_SHA='fe228cf71b306fbd4eac3b9c60f7b2ecfbe9f77919b70ce237cd0ac4a0041990'
workspace=Path(os.environ['GITHUB_WORKSPACE']).resolve()
if os.environ['GITHUB_REPOSITORY']!=REPO:raise RuntimeError('wrong repository')
base=workspace/'papers/A2-DYN-v19-referee-response'
root=workspace/'papers/A2-DYN-v20-referee-response'
transport=Path(__file__).resolve().parent
payload=base64.b64decode(''.join((transport/f'part{n}.b64').read_text().strip() for n in range(1,6)),validate=True)
if hashlib.sha256(payload).hexdigest()!=PACKET_SHA:raise RuntimeError('transport checksum mismatch')
obj=json.loads(zlib.decompress(payload))
if obj['baseline_tree']!=BASE_TREE or obj['expected_tree']!=EXPECTED:raise RuntimeError('wrong source identity')
def ordinary(folder):
    return [p for p in sorted(folder.rglob('*')) if p.is_file() and not any(s in ('build','evidence','__pycache__') for s in p.relative_to(folder).parts)]
def gh(kind,data):return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()
def tree(folder):
    rows=[]
    for p in folder.iterdir():
        if p.name in ('build','evidence','__pycache__'):continue
        if p.is_symlink():raise RuntimeError('unexpected symbolic link')
        if p.is_dir():mode='40000';digest=tree(p);key=p.name+'/'
        else:mode='100755' if p.stat().st_mode&0o111 else '100644';digest=gh('blob',p.read_bytes());key=p.name
        rows.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+digest))
    return gh('tree',b''.join(v for _,v in sorted(rows)))
if tree(base).hex()!=BASE_TREE:raise RuntimeError('wrong baseline bytes')
if root.exists():raise RuntimeError('refuse to replace an existing draft')
shutil.copytree(base,root)
for entry in obj['files']:
    rel=PurePosixPath(entry['path'])
    if rel.is_absolute() or '..' in rel.parts or len(rel.parts)>2:raise RuntimeError('unsafe path')
    if entry['mode'] not in ('100644','100755'):raise RuntimeError('unexpected mode')
    target=root/str(rel);target.parent.mkdir(parents=True,exist_ok=True)
    target.write_text(entry['content']);target.chmod(int(entry['mode'],8)&0o777)
ledger=json.loads((root/'INHERITED_EDITS.json').read_text())
if len(ledger['edits'])!=7:raise RuntimeError('wrong exact-edit count')
allowed={'main.tex','core/39_compressed_return_resolvents.tex','core/40_finite_count_edge_extraction.tex'}
for edit in ledger['edits']:
    if edit['path'] not in allowed:raise RuntimeError('unapproved inherited edit')
    path=root/edit['path'];text=path.read_text()
    if text.count(edit['before'])!=1:raise RuntimeError('nonunique inherited replacement')
    path.write_text(text.replace(edit['before'],edit['after'],1))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
manifest=obj['manifest_meta']
manifest['baseline_sha256']={p.relative_to(base).as_posix():sha(p) for p in ordinary(base)}
manifest['source_sha256']={p.relative_to(root).as_posix():sha(p) for p in ordinary(root) if p.name!='SOURCE_MANIFEST.json'}
(root/'SOURCE_MANIFEST.json').write_text(json.dumps(manifest,indent=2,sort_keys=True)+'\n')
if tree(root).hex()!=EXPECTED:raise RuntimeError('ordinary source tree differs')
entries=[]
for p in ordinary(root):
    rel=p.relative_to(root).as_posix();old=base/rel
    mode='100755' if p.stat().st_mode&0o111 else '100644'
    if not old.exists() or p.read_bytes()!=old.read_bytes() or bool(p.stat().st_mode&0o111)!=bool(old.stat().st_mode&0o111):
        entries.append({'path':rel,'mode':mode,'type':'blob','content':p.read_text()})
data=json.dumps({'base_tree':BASE_TREE,'tree':entries}).encode()
request=urllib.request.Request('https://api.github.com/repos/'+REPO+'/git/trees',data=data,method='POST',headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','Content-Type':'application/json','X-GitHub-Api-Version':'2022-11-28'})
with urllib.request.urlopen(request,timeout=90) as response:created=json.load(response)
if created['sha']!=EXPECTED:raise RuntimeError('remote immutable tree differs')
receipt={'event_sha':os.environ['GITHUB_SHA'],'run_id':os.environ['GITHUB_RUN_ID'],'packet_sha256':PACKET_SHA,'paper_tree':created['sha'],'source_files':len(ordinary(root)),'changed_or_added_files':len(entries),'commits_created':False,'branch_refs_moved':False}
(workspace/'assembly-receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2,sort_keys=True))
