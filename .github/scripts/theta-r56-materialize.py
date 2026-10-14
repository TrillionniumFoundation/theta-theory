#!/usr/bin/env python3
"""Store previously built, hash-verified R56 PDFs despite inherited ignore rules."""
from pathlib import Path
import hashlib,json,os,subprocess,zipfile
ROOT=Path(os.environ['GITHUB_WORKSPACE']);TMP=Path(os.environ['RUNNER_TEMP'])/'r56-materialization';TMP.mkdir()
BRANCH='foundation/general-theta-restart-r56-balanced-task-transfer-research-2026-10-14'
REL='papers/General-Theta-Foundations-I-restart/r56-balanced-task-transfer/artifacts'
SOURCE='808ef512a73d5b1911257af2669a4e7ed97107ed';INITIAL='14163ae4c88360d2772575b1a62f6922aff696fa'
IDS=[(11863579443,'558e4fdee6ab775217028db6001a5c05bdef9e2942720c99813fc95b6fdf33e8'),(11863862965,'618bbb43c74cd731755768cb84a4a9d34e1eb3eea2ea58ae229978c2c20765db'),(11863773242,'389f88c1d1995dfb4ff1fde9f68e6bd182a6d91ecb3f88be941c2dae2305289e'),(11863739110,'2556ed17cf2bebba89b73a2879e6b45903ada59b965bb870675b4471c155aa40')]
def check(ok,msg):
 if not ok:raise RuntimeError(msg)
def run(*args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
def sha(b):return hashlib.sha256(b).hexdigest()
def remote():return run('git','ls-remote','origin','refs/heads/'+BRANCH).split()[0]
check(os.environ['GITHUB_REF_NAME']==BRANCH,'wrong target');parent=run('git','rev-parse','HEAD');check(remote()==parent,'research raced')
check(run('git','rev-parse','HEAD^')==INITIAL,'materialization parent differs')
check(run('git','diff','--name-only',INITIAL,parent).splitlines()==['.github/scripts/theta-r56-materialize.py','.github/workflows/theta-r56-materialize.yml'],'unexpected infrastructure changes')
receipt=json.loads((ROOT/REL/'PUBLICATION_RECEIPT.json').read_text());check(receipt['source_commit']==SOURCE,'source binding differs')
written={}
for aid,digest in IDS:
 path=TMP/(str(aid)+'.zip')
 with path.open('wb') as f:subprocess.run(['gh','api','repos/TrillionniumFoundation/theta-theory/actions/artifacts/'+str(aid)+'/zip'],cwd=ROOT,stdout=f,check=True)
 check(sha(path.read_bytes())==digest,'download differs')
 with zipfile.ZipFile(path) as z:
  check(z.read('SOURCE_SHA.txt').decode().strip()==SOURCE and z.read('ARTIFACT_SHA.txt').decode().strip()==INITIAL,'packet binding differs')
  for name in z.namelist():
   if not (name.endswith('.pdf') or name=='R56_LATEX_BUILD.log'):continue
   check(Path(name).name==name and name not in written,'unsafe or duplicate artifact')
   b=z.read(name);check(sha(b)==receipt['files'][name],'built bytes differ '+name)
   dest=ROOT/REL/name;check(not dest.exists(),'refusing to overwrite '+name);dest.write_bytes(b);written[name]=sha(b)
expected={n for n in receipt['files'] if n.endswith('.pdf') or n=='R56_LATEX_BUILD.log'};check(set(written)==expected and len(written)==29,'incomplete artifact materialization')
record={'status':'PASS','source_commit':SOURCE,'initial_artifact_receipt_commit':INITIAL,'materialization_infrastructure_commit':parent,'original_build_run':38496786241,'materialization_run':os.environ['GITHUB_RUN_ID'],'reason':'Inherited ignore rules omitted PDFs and log from initial Git artifact commit; existing verified build bytes are now explicitly stored. No mathematical source was changed or rebuilt.','files':written,'pdf_count':28,'source_unchanged':True}
recordpath=ROOT/REL/'BINARY_PUBLICATION.json';recordpath.write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
run('git','config','user.name','github-actions[bot]');run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
run('git','add','-f','--',*[REL+'/'+n for n in sorted(written)],REL+'/BINARY_PUBLICATION.json')
staged=run('git','diff','--cached','--name-status').splitlines();check(len(staged)==30 and all(row.startswith('A\t'+REL+'/') for row in staged),'non-additive artifact stage')
check(remote()==parent,'head moved before push');run('git','commit','-m','artifacts(theta R56): explicitly retain all verified PDF and log bytes in Git');head=run('git','rev-parse','HEAD');run('git','push','origin','HEAD:refs/heads/'+BRANCH)
proof=TMP/'proof';proof.mkdir();(proof/'BINARY_PUBLICATION.json').write_bytes(recordpath.read_bytes());(proof/'ARTIFACT_SHA.txt').write_text(head+'\n');(proof/'GIT_TREE.txt').write_text(run('git','ls-tree','-r',head)+'\n')
print(json.dumps({'artifact_commit':head,'source_commit':SOURCE,'status':'PASS'},indent=2))
