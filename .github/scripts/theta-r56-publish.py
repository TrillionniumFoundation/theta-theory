#!/usr/bin/env python3
"""Additive R56 source/artifact publication. Not a mathematical proof tool."""
from pathlib import Path
import hashlib,json,lzma,os,shutil,subprocess,sys
BRANCH='foundation/general-theta-restart-r56-balanced-task-transfer-research-2026-10-14'
REL='papers/General-Theta-Foundations-I-restart/r56-balanced-task-transfer'
BASE='01e8745b04d4cbaf850fed042ceb7560562fd3fb'
PAYLOAD_SHA='9203613a0c9fe9b41c95a2b51ece5729691c230ccbcf5ec32e5bfd094536aa41'
PARTS=5
ROOT=Path(os.environ['GITHUB_WORKSPACE']);TMP=Path(os.environ['RUNNER_TEMP'])
OUT=TMP/'r56-output';PACK=TMP/'r56-packets'
ALLOWED={'.github/workflows/theta-r56-build.yml','.github/scripts/theta-r56-publish.py',*{'.github/data/theta-r56-source.xz.'+str(i) for i in range(PARTS)}}
def check(ok,msg):
 if not ok:raise RuntimeError(msg)
def run(*args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
def sha(data):return hashlib.sha256(data).hexdigest()
def ref():return run('git','ls-remote','origin','refs/heads/'+BRANCH).split()[0]
def changes(commit):
 rows=run('git','diff','--name-status',BASE,commit).splitlines()
 for row in rows:
  status,path=row.split('\t',1)
  check(status=='A' and (path.startswith(REL+'/') or path in ALLOWED),'historical mutation: '+row)
 return rows
def env(name,value):
 with open(os.environ['GITHUB_ENV'],'a') as f:f.write(name+'='+value+'\n')
def main():
 check(os.environ['GITHUB_REF_NAME']==BRANCH,'wrong write branch')
 mode=sys.argv[1];transport=os.environ['GITHUB_SHA']
 if mode=='source':
  check(run('git','rev-parse','HEAD')==transport and ref()==transport,'transport head raced');changes(transport)
  raw=b''.join((ROOT/('.github/data/theta-r56-source.xz.'+str(i))).read_bytes() for i in range(PARTS))
  check(sha(raw)==PAYLOAD_SHA,'source transport digest mismatch');records=json.loads(lzma.decompress(raw));dest=ROOT/REL
  check(run('git','hash-object',str(dest/'review_inputs/R53_EXTERNAL_REFEREE_REPORT.md'))=='9c86a6fe706ad991765720f48fb78dde6b597a2b','pinned review differs')
  for name,item in records.items():
   p=Path(name);check(not p.is_absolute() and '..' not in p.parts and not {'.git','artifacts','evidence','transport','__pycache__'}.intersection(p.parts),'unsafe ordinary source path')
   data=item['text'].encode();check(sha(data)==item['sha256'],'decoded digest mismatch '+name)
   f=dest/p;check(not f.exists() or f.read_bytes()==data,'different existing source '+name);f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
  run(sys.executable,str(dest/'seal.py'));audit=json.loads(run(sys.executable,str(dest/'verify.py')))
  check(ref()==transport,'research head moved before source commit')
  run('git','config','user.name','github-actions[bot]');run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
  run('git','add','--',REL);run('git','commit','-m','source(theta R56): raw joint task balance and complete paid acquired-risk transfer')
  source=run('git','rev-parse','HEAD');check(run('git','rev-parse','HEAD^')==transport,'source parent mismatch');rows=changes(source)
  run('git','push','origin','HEAD:refs/heads/'+BRANCH)
  record={'status':'PASS','source_commit':source,'transport_commit':transport,'transport_sha256':PAYLOAD_SHA,'decoded_ordinary_files':len(records),'source_root_tree':run('git','rev-parse','HEAD^{tree}'),'native_source_tree':run('git','rev-parse','HEAD:'+REL),'source_audit':audit,'retained_input':BASE,'retained_paths_unchanged':True,'source_changes':rows,'workflow_run':os.environ['GITHUB_RUN_ID']}
  (TMP/'R56_SOURCE_PUBLICATION.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n');env('R56_SOURCE_SHA',source)
 elif mode=='artifacts':
  source=os.environ['R56_SOURCE_SHA'];check(run('git','rev-parse','HEAD')==source and ref()==source,'source head raced');check(not run('git','status','--porcelain'),'build changed checkout')
  receipt=json.loads((OUT/'BUILD_RECEIPT.json').read_text());check(receipt['status']=='PASS' and receipt['source_commit']==source,'unbound build')
  for name,item in receipt['delivery_pdfs'].items():check(sha((OUT/name).read_bytes())==item['sha256'],'PDF differs '+name)
  dest=ROOT/REL/'artifacts';check(not dest.exists(),'artifact path exists');dest.mkdir()
  for f in sorted(OUT.iterdir()):
   if f.is_file() and f.suffix in {'.pdf','.json','.log','.zip'}:shutil.copyfile(f,dest/f.name)
  shutil.copyfile(TMP/'R56_SOURCE_PUBLICATION.json',dest/'SOURCE_PUBLICATION.json')
  rec={'status':'PASS','source_commit':source,'native_source_tree':run('git','rev-parse',source+':'+REL),'retained_input':BASE,'retained_paths_unchanged':True,'source_changes':changes(source),'workflow_run':os.environ['GITHUB_RUN_ID'],'artifact_parent_must_equal_source':True,'files':{f.name:sha(f.read_bytes()) for f in sorted(dest.iterdir())}}
  (dest/'PUBLICATION_RECEIPT.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
  check(ref()==source,'head moved before artifact push');run('git','add','--',REL+'/artifacts');run('git','commit','-m','artifacts(theta R56): full native and retained builds bound to immutable source')
  artifact=run('git','rev-parse','HEAD');check(run('git','rev-parse','HEAD^')==source,'artifact parent mismatch');run('git','push','origin','HEAD:refs/heads/'+BRANCH);env('R56_ARTIFACT_SHA',artifact)
 elif mode=='packets':
  source=os.environ['R56_SOURCE_SHA'];artifact=run('git','rev-parse','HEAD');check(run('git','rev-parse','HEAD^')==source,'artifact not direct child')
  native=PACK/'native';native.mkdir(parents=True)
  names=['General_Theta_Foundations_I_restart_R56.pdf','R56_prepared_sources.zip','BUILD_RECEIPT.json','R56_LATEX_BUILD.log']
  for name in names:shutil.copyfile(OUT/name,native/name)
  for name in ['SOURCE_PUBLICATION.json','PUBLICATION_RECEIPT.json']:shutil.copyfile(ROOT/REL/'artifacts'/name,native/name)
  (native/'SOURCE_SHA.txt').write_text(source+'\n');(native/'ARTIFACT_SHA.txt').write_text(artifact+'\n');(native/'GIT_TREE.txt').write_text(run('git','ls-tree','-r',source)+'\n')
  groups=[PACK/('retained-'+str(i)) for i in range(1,4)];sizes=[0,0,0]
  for g in groups:g.mkdir()
  for f in sorted(OUT.glob('*.pdf'),key=lambda p:p.stat().st_size,reverse=True):
   if f.name==names[0]:continue
   i=min(range(3),key=lambda j:sizes[j]);shutil.copyfile(f,groups[i]/f.name);sizes[i]+=f.stat().st_size
  for g in groups:(g/'SOURCE_SHA.txt').write_text(source+'\n');(g/'ARTIFACT_SHA.txt').write_text(artifact+'\n')
  print(json.dumps({'source_commit':source,'artifact_commit':artifact,'group_bytes':sizes},indent=2))
 else:raise RuntimeError('unsupported mode')
if __name__=='__main__':main()
