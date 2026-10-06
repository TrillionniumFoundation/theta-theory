"""One-time immutable Git-object transport; never creates commits or moves refs."""
from pathlib import Path
import base64,hashlib,json,lzma,os,shutil,tempfile,urllib.request
repo=Path.cwd()
transport=repo/'.github/a2-dyn-v16-transport'
encoded=''.join((transport/f'part{i}.b64').read_text().strip() for i in range(1,5))
compressed=base64.b64decode(encoded,validate=True)
expected='2fbb1d352a520f33d5125377b9e2d81c2b7e03534f860c2f91578ce54c5d9818'
if hashlib.sha256(compressed).hexdigest()!=expected:raise RuntimeError('transport checksum')
raw=lzma.decompress(compressed)
if hashlib.sha256(raw).hexdigest()!='415995a71f4fee5f16d4f1301ed4d295a420ffa048d3098ba306d6d66aa1a837':raise RuntimeError('decoded checksum')
p=json.loads(raw)
base=repo/'papers/A2-DYN-v15-referee-response'
work=Path(tempfile.mkdtemp(prefix='a2-dyn-v16-'))/'paper'
shutil.copytree(base,work,ignore=shutil.ignore_patterns('build','evidence','__pycache__'))
for e in p['changes']:
    rel=Path(e['path'])
    if rel.is_absolute() or '..' in rel.parts:raise RuntimeError('invalid transport path')
    f=work/rel;f.parent.mkdir(parents=True,exist_ok=True)
    f.write_text(e['content']);f.chmod(int(e['mode'],8))
ledger=json.loads((work/'INHERITED_EDITS.json').read_text())
for e in ledger['edits']:
    f=work/e['path'];t=f.read_text()
    if t.count(e['before'])!=1:raise RuntimeError('inherited edit not unique')
    f.write_text(t.replace(e['before'],e['after'],1))
def sha256(f):return hashlib.sha256(f.read_bytes()).hexdigest()
m=p['manifest_template']
inherited=sorted((base/'core').glob('*.tex'))+[base/'main.tex',base/'references.tex']
m['baseline_sha256']={f.relative_to(base).as_posix():sha256(f) for f in inherited}
files=sorted(f for f in work.rglob('*') if f.is_file() and f.name!='SOURCE_MANIFEST.json')
m['source_sha256']={f.relative_to(work).as_posix():sha256(f) for f in files}
(work/'SOURCE_MANIFEST.json').write_text(json.dumps(m,indent=2,sort_keys=True)+'\n')
def obj(kind,b):return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()
def git_tree(d):
    entries=[]
    for f in d.iterdir():
        if f.is_dir():entries.append((f.name+'/',b'40000',f.name,git_tree(f)))
        else:entries.append((f.name,b'100755' if f.stat().st_mode&0o111 else b'100644',f.name,obj('blob',f.read_bytes())))
    body=b''.join(mode+b' '+name.encode()+b'\0'+bytes.fromhex(sha) for _,mode,name,sha in sorted(entries))
    return obj('tree',body)
if git_tree(base)!=p['base_paper_tree']:raise RuntimeError('baseline tree differs')
assembled=git_tree(work)
if assembled!=p['expected_paper_tree']:raise RuntimeError('assembled tree differs: '+assembled)
files=sorted(f for f in work.rglob('*') if f.is_file())
if len(files)!=p['file_count']:raise RuntimeError('file count differs')
changes=[]
for f in files:
    rel=f.relative_to(work).as_posix();old=base/rel
    if not old.exists() or f.read_bytes()!=old.read_bytes():
        changes.append({'path':rel,'mode':'100755' if f.stat().st_mode&0o111 else '100644','type':'blob','content':f.read_text()})
if os.environ.get('ASSEMBLY_DRY_RUN')!='1':
    request=urllib.request.Request('https://api.github.com/repos/'+os.environ['GITHUB_REPOSITORY']+'/git/trees',
        data=json.dumps({'base_tree':p['base_paper_tree'],'tree':changes}).encode(),method='POST',
        headers={'Authorization':'Bearer '+os.environ['GH_TOKEN'],'Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json'})
    with urllib.request.urlopen(request,timeout=90) as r:result=json.load(r)
    if result['sha']!=assembled:raise RuntimeError('remote tree differs')
receipt={'revision':16,'event_sha':os.environ.get('GITHUB_SHA'),'run_id':os.environ.get('GITHUB_RUN_ID'),
         'base_paper_tree':p['base_paper_tree'],'paper_tree':assembled,'transport_sha256':expected,
         'ordinary_source_files':len(files),'changed_files':len(changes),'commits_created':False,'branch_refs_changed':False}
Path('assembly-evidence').mkdir(exist_ok=True)
Path('assembly-evidence/receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps(receipt,indent=2))
