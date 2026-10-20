#!/usr/bin/env python3
"""Read only the immutable published Git objects; write only scratch audit output."""
from pathlib import Path,PurePosixPath
from datetime import datetime,timezone
import subprocess,json,hashlib,io,tarfile,re,importlib.util,sys
REPO=Path('/workspace/scratch/35c64a3513c5/theta-theory')
OUT=REPO.parent/'post-publication-audit'
COMMIT='86c947eccea6029258d9a362624866a475118a66'
PARENT='6cdd9ae88cd358d524ecb89092361ac1522ba351'
ARTICLE='papers/A2-DYN-critical-source-transport-author-revision'
WORKFLOW='.github/workflows/a2-dyn-critical-source-transport-20261020.yml'
EXPECTED_TREE='4624f0eef13e655c39d6313f6779e6c72a86870e'
EXPECTED_ARTICLE='6830d79a554645422869c3531715f1a32161ce20'
BASE_ARTICLE='a1d21789f9d7c1be801ff4a54d1befad2a47340f'
ANCHOR_SHA='e49c3b8d9002cc2e431a4e7b846490a5a9f347f47fa236a1c609146f16bcfe1b'
MATH_SHA='cbe6dac9cab2bf80dd73119aaeda4d9f3122b42898807a4d0b6ac869eaecbc82'
MANIFEST_SHA='775943e1aa70d53e725956c8ab9eb01edb710c555b89cdcc5f1f9064d463f6c1'
errors=[]
def require(ok,msg):
 if not ok: errors.append(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=REPO)
def textgit(*args):return git(*args).decode().strip()
def dump(name,data):(OUT/name).write_text(json.dumps(data,indent=2,ensure_ascii=False,sort_keys=True)+'\n')
entries=json.loads((OUT/'published-article-tree.json').read_text())
by_path={e['path']:e for e in entries}
nonhist={k:v for k,v in by_path.items()if not k.startswith('history/predecessor/')}
objects={}
def batch(oids):
 wanted=sorted(set(oids)-objects.keys())
 if not wanted:return
 raw=subprocess.check_output(['git','cat-file','--batch'],cwd=REPO,input=''.join(x+'\n'for x in wanted).encode())
 pos=0
 for wanted_oid in wanted:
  end=raw.index(b'\n',pos);header=raw[pos:end].decode().split();pos=end+1
  if len(header)!=3 or header[1]!='blob':raise RuntimeError('Unavailable/nonblob '+repr(header))
  oid,kind,length=header;length=int(length);data=raw[pos:pos+length];pos+=length
  if raw[pos:pos+1]!=b'\n':raise RuntimeError('Bad batch record framing')
  pos+=1
  require(oid==wanted_oid,'Batch object order mismatch')
  require(hashlib.sha1(b'blob '+str(length).encode()+b'\0'+data).hexdigest()==oid,'Git blob identity mismatch '+oid)
  objects[oid]=data
 require(pos==len(raw),'Unconsumed batch output')
batch(e['git_blob']for e in nonhist.values())
def get(path):return objects[by_path[path]['git_blob']]
def getjson(path):return json.loads(get(path))
manifest=getjson('SOURCE_MANIFEST.json');delivery=getjson('DELIVERY_MANIFEST.json');anchor=getjson('CURRENT_SOURCE_ANCHOR.json');pub=getjson('PUBLICATION_STATUS.json')
require(sha(get('SOURCE_MANIFEST.json'))==MANIFEST_SHA,'Frozen source manifest digest differs')
require(sha(get('CURRENT_SOURCE_ANCHOR.json'))==ANCHOR_SHA,'Fixed predecessor anchor digest differs')
require(textgit('rev-parse',COMMIT+'^')==PARENT,'Wrong parent')
require(textgit('rev-parse',COMMIT+'^{tree}')==EXPECTED_TREE,'Wrong root tree')
require(textgit('rev-parse',COMMIT+':'+ARTICLE)==EXPECTED_ARTICLE,'Wrong article tree')
require(textgit('rev-parse',PARENT+':'+anchor['source_article_path'])==BASE_ARTICLE,'Baseline source article identity differs')
require(textgit('rev-parse',COMMIT+':'+ARTICLE+'/history/predecessor')==BASE_ARTICLE,'Published archive subtree identity differs')
archive_paths={k for k in by_path if k.startswith('history/predecessor/')}
require({r['path']for r in anchor['files']}==archive_paths,'Fixed archive map path set differs')
require(len(archive_paths)==3864 and len(anchor['files'])==3864,'Fixed archive count differs')
require(sum(r['bytes']for r in anchor['files'])==anchor['bytes']==485851107,'Fixed archive byte sum differs')
for row in anchor['files']:
 require(row['path']=='history/predecessor/'+row['original_path'],'Anchor relocation '+row['path'])
 e=by_path[row['path']]
 require(e['git_blob']==row['git_blob'] and e['mode']==row['mode'],'Archive blob/mode differs '+row['path'])
# Every inherited current body is pinned to its original archived Git object.
for path in anchor['inherited_active_paths']:
 a=by_path['history/predecessor/'+path];b=by_path[path]
 require(a['git_blob']==b['git_blob']and a['mode']==b['mode'],'Inherited active source differs '+path)
original_anchor_checks=[]
batch(by_path[r['path']]['git_blob']for r in anchor['original_anchors'])
for row in anchor['original_anchors']:
 require(sha(get(row['path']))==row['sha256'],'Older preserved anchor hash differs '+row['path'])
 original_anchor_checks.append({'path':row['path'],'sha256':sha(get(row['path'])),'git_blob':by_path[row['path']]['git_blob'],'placements':row['placements']})
reviews=getjson(anchor['review_preservation_path'])
require(sha(get(anchor['review_preservation_path']))==anchor['review_preservation_sha256'],'Original review preservation map digest differs')
require(len(reviews['reports'])==91 and reviews['distinct_report_count']==91 and reviews['review_ref_count']==178,'Review census count differs')
require(len({r['git_blob']for r in reviews['reports']})==91,'Duplicate distinct original report body')
for row in reviews['reports']:
 for p in row['all_archive_paths']:
  require(p in by_path and by_path[p]['git_blob']==row['git_blob'],'Original report missing/different '+p)
# Verify every nonhistorical delivery byte against the manifest, not just its path.
deliv_paths=[r['path']for r in delivery['files']]
require(len(deliv_paths)==len(set(deliv_paths)),'Duplicate delivery path')
require(set(deliv_paths)==set(nonhist)-{'DELIVERY_MANIFEST.json'},'Delivery manifest file set differs')
for row in delivery['files']:
 data=get(row['path']);require(len(data)==row['bytes']and sha(data)==row['sha256'],'Delivery byte/hash differs '+row['path'])
source_paths=[r['path']for r in manifest['files']]
require(len(source_paths)==len(set(source_paths)),'Duplicate mathematical manifest path')
for row in manifest['files']:
 data=get(row['path']);entry=by_path[row['path']]
 require(len(data)==row['bytes']and sha(data)==row['sha256']and entry['git_blob']==row['git_blob']and entry['mode']==row['mode'],'Mathematical input identity differs '+row['path'])
canonical=sorted(p for p in nonhist if (len(PurePosixPath(p).parts)==1 and p.endswith('.tex')) or (p.startswith('core/')and len(PurePosixPath(p).parts)==2 and p.endswith('.tex'))or(p.startswith('tools/')and len(PurePosixPath(p).parts)==2 and p.endswith('.py'))or p in {'requirements.txt','build.sh'})
math_rows=[{'path':p,'sha256':sha(get(p))}for p in canonical]
math_digest=sha(json.dumps(math_rows,sort_keys=True).encode())
require(math_digest==MATH_SHA,'Mathematical source digest differs')
require(set(source_paths)==set(canonical)|{'ci/a2-dyn-critical-source-transport-20261020.yml'},'Canonical build/math plus workflow file set differs')
require(delivery['mathematical_source_sha256']==math_digest==pub['mathematical_source_sha256'],'Publication/delivery math digest differs')
require(pub['source_manifest_sha256']==MANIFEST_SHA,'Publication source manifest digest differs')
workflow_blob=textgit('rev-parse',COMMIT+':'+WORKFLOW)
require(workflow_blob==by_path['ci/a2-dyn-critical-source-transport-20261020.yml']['git_blob'],'Dedicated workflow and frozen mirror differ')
# Extract only current mathematical source and reviewed root documents for a source-closure recheck.
snapshot=OUT/'published-source-snapshot';snapshot.mkdir(exist_ok=True)
for p in source_paths:
 dest=snapshot/p;dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(get(p));dest.chmod(int(by_path[p]['mode'][-3:],8))
docnames=['main.tex','revision-introduction.tex','README.md','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','MATHEMATICAL_AUDIT.md','LITERATURE_AUDIT.md','SOURCE_MANIFEST.md','HISTORY_PRESERVATION_AUDIT.md','VALIDATION.md','PUBLICATION_STATUS.json']
for p in docnames:(snapshot/p).write_bytes(get(p))
sys.dont_write_bytecode=True
spec=importlib.util.spec_from_file_location('published_source_preservation',snapshot/'tools/check_source_preservation.py');checker=importlib.util.module_from_spec(spec);spec.loader.exec_module(checker)
closure=checker.tex_closure(snapshot)
require(closure['reachable_tex_files']==manifest['reachable_tex_files'],'Manifest native input graph differs')
require(closure['active_core_files']==manifest['active_core_files'],'Manifest active core files differ')
require(closure['active_core_start']==260 and closure['active_core_end']==322,'Active core range differs')
require(checker.git_tree(anchor['files'])==BASE_ARTICLE,'Frozen predecessor map does not reconstruct baseline tree')
# Reopen the exact published execution bundles and bind each preserved output to the index.
bundles=getjson('evidence/EVIDENCE_INDEX.json');bundle_checks=[]
for row in bundles['bundles']:
 p='evidence/'+row['archive'];data=get(p)
 require(len(data)==row['bytes']and sha(data)==row['sha256'],'Evidence bundle identity differs '+p)
 expected={r['path']:r for r in row['files']};found={}
 with tarfile.open(fileobj=io.BytesIO(data),mode='r:gz')as archive:
  for member in archive.getmembers():
   if member.isdir():continue
   require(member.isfile(),'Nonregular evidence member '+member.name)
   payload=archive.extractfile(member).read();found[member.name]={'bytes':len(payload),'sha256':sha(payload)}
   require(member.name in expected,'Undeclared evidence member '+member.name)
   if member.name in expected:
    r=expected[member.name];require(len(payload)==r['bytes']and sha(payload)==r['sha256'],'Evidence member bytes differ '+member.name)
 require(set(found)==set(expected),'Evidence member path set differs '+p)
 bundle_checks.append({'archive':p,'bytes':len(data),'sha256':sha(data),'files':len(found)})
# Relative Markdown link checks use the immutable Git tree, including directories.
paths=set(by_path)
directories=set()
for p in paths:
 directories.update(str(q)for q in PurePosixPath(p).parents if str(q)!='.')
link_checks=[]
for p in docnames:
 if not p.endswith('.md'):continue
 content=get(p).decode()
 for match in re.finditer(r'\[[^\]\n]*\]\(([^)\n]+)\)',content):
  dest=match.group(1).split(' "',1)[0].strip().strip('<>');base=dest.split('#',1)[0]
  if not base or re.match(r'^[A-Za-z][A-Za-z0-9+.-]*:',base):continue
  resolved=str(PurePosixPath(p).parent/PurePosixPath(base)).rstrip('/')
  exists=resolved in paths or resolved in directories
  link_checks.append({'source':p,'target':dest,'resolved':resolved,'exists_in_published_tree':exists,'line':content[:match.start()].count('\n')+1})
summary={'schema':'a2-dyn-published-source-read-only-audit-v1','checked_utc':datetime.now(timezone.utc).isoformat(),'source_commit':COMMIT,'root_tree':EXPECTED_TREE,'article_tree':EXPECTED_ARTICLE,'parent':PARENT,'scope':'Pinned Git source objects, source closure, preservation and delivery byte identities; no mathematical or CI re-execution','errors':errors,'passed':not errors,'archive_files':3864,'archive_bytes_from_fixed_manifest':485851107,'archive_tree':BASE_ARTICLE,'archive_verification':'Every path/mode/Git blob matched fixed anchor; exact full subtree identity equals baseline; old SHA256 map pinned by its independently fixed digest','archive_anchor_sha256':ANCHOR_SHA,'inherited_active_paths_verified':len(anchor['inherited_active_paths']),'old_anchors_verified':original_anchor_checks,'original_distinct_report_blobs_verified':91,'review_refs':178,'source_manifest_files_verified':len(source_paths),'source_manifest_sha256':sha(get('SOURCE_MANIFEST.json')),'source_manifest_git_blob':by_path['SOURCE_MANIFEST.json']['git_blob'],'delivery_manifest_files_verified':len(deliv_paths),'delivery_manifest_sha256':sha(get('DELIVERY_MANIFEST.json')),'delivery_manifest_git_blob':by_path['DELIVERY_MANIFEST.json']['git_blob'],'nonhistorical_published_files':len(nonhist),'nonhistorical_published_bytes':sum(len(get(p))for p in nonhist),'mathematical_digest_files':len(canonical),'mathematical_source_sha256':math_digest,'main_tex_sha256':sha(get('main.tex')),'main_pdf_sha256':sha(get('compiled/main.pdf')),'workflow_git_blob':workflow_blob,'workflow_mirror_equal':True,'active_core_start':closure['active_core_start'],'active_core_end':closure['active_core_end'],'active_core_files':len(closure['active_core_files']),'reachable_tex_files':len(closure['reachable_tex_files']),'closure':{k:v for k,v in closure.items()if k not in {'reachable_tex_files','active_core_files','input_edges'}},'evidence_bundles':bundle_checks,'evidence_bundle_files':sum(r['files']for r in bundle_checks),'broken_relative_markdown_links':[r for r in link_checks if not r['exists_in_published_tree']],'publication_status_at_source_commit':pub}
dump('source-identity-verification.json',summary);dump('published-native-closure.json',closure);dump('relative-document-links.json',link_checks);dump('verified-nonhistorical-file-identities.json',[{'path':p,'git_blob':by_path[p]['git_blob'],'mode':by_path[p]['mode'],'bytes':len(get(p)),'sha256':sha(get(p))}for p in sorted(nonhist)])
print(json.dumps({k:v for k,v in summary.items()if k not in {'publication_status_at_source_commit','closure','old_anchors_verified','evidence_bundles'}},indent=2))
print('Closure summary',json.dumps(summary['closure'],sort_keys=True))
if errors:raise SystemExit(1)
