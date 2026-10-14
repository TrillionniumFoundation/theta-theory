#!/usr/bin/env python3
"""R54 additive source/artifact publication; not a mathematical proof tool."""
from pathlib import Path
import hashlib,json,lzma,os,shutil,subprocess,sys
BRANCH='foundation/general-theta-restart-r54-predictable-geometry-research-2026-10-13'
REL='papers/General-Theta-Foundations-I-restart/r54-predictable-geometry'
BASE='e8eed6849b34afd200bf9532eaa1a68f32e9ee48'
PAYLOAD_SHA='cd64fe047d6acaa4cde5ae66ec67ae1b2fe7ede122e4cd262ca4c7534f969138'
ROOT=Path(os.environ['GITHUB_WORKSPACE']);TMP=Path(os.environ['RUNNER_TEMP'])
OUT=TMP/'r54-output';PACK=TMP/'r54-packets'
ALLOWED={'.github/workflows/theta-r54-build.yml','.github/scripts/theta-r54-publish.py',*{'.github/data/theta-r54-source.xz.'+str(i) for i in range(6)}}
def check(ok,msg):
 if not ok:raise RuntimeError(msg)
def run(*args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
def sha(data):return hashlib.sha256(data).hexdigest()
def ref():return run('git','ls-remote','origin','refs/heads/'+BRANCH).split()[0]
def allowed_changes(commit):
 changes=run('git','diff','--name-status',BASE,commit).splitlines()
 for line in changes:
  status,path=line.split('\t',1)
  check(status=='A' and (path.startswith(REL+'/') or path in ALLOWED),'historical mutation: '+line)
 return changes
def save_env(name,value):
 with open(os.environ['GITHUB_ENV'],'a') as f:f.write(name+'='+value+'\n')
def main():
 check(os.environ['GITHUB_REF_NAME']==BRANCH,'wrong write branch')
 mode=sys.argv[1];transport=os.environ['GITHUB_SHA']
 if mode=='source':
  check(run('git','rev-parse','HEAD')==transport and ref()==transport,'transport head raced')
  allowed_changes(transport)
  blob=b''.join((ROOT/('.github/data/theta-r54-source.xz.'+str(i))).read_bytes() for i in range(6));check(sha(blob)==PAYLOAD_SHA,'transport digest mismatch')
  records=json.loads(lzma.decompress(blob));dest=ROOT/REL
  check(run('git','hash-object',str(dest/'review_inputs/R53_EXTERNAL_REFEREE_REPORT.md'))=='9c86a6fe706ad991765720f48fb78dde6b597a2b','latest referee input differs')
  for name,item in records.items():
   rel=Path(name);check(not rel.is_absolute() and '..' not in rel.parts and not {'.git','artifacts','evidence','transport','__pycache__'}.intersection(rel.parts),'unsafe native path')
   data=item['text'].encode();check(sha(data)==item['sha256'],'decoded source digest mismatch')
   f=dest/rel;check(not f.exists() or f.read_bytes()==data,'different existing source '+name)
   f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(data)
  run(sys.executable,str(dest/'seal.py'));run(sys.executable,str(dest/'verify.py'))
  check(ref()==transport,'research head moved before ordinary source commit')
  run('git','config','user.name','github-actions[bot]');run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
  run('git','add','--',REL);run('git','commit','-m','source(theta R54): predictable acquired geometry, intrinsic calibration and physical-command memory')
  source=run('git','rev-parse','HEAD');check(run('git','rev-parse','HEAD^')==transport,'source parent mismatch')
  changes=allowed_changes(source);run('git','push','origin','HEAD:refs/heads/'+BRANCH)
  record={'status':'PASS','source_commit':source,'transport_commit':transport,'transport_sha256':PAYLOAD_SHA,'decoded_ordinary_files':len(records),'source_root_tree':run('git','rev-parse','HEAD^{tree}'),'native_source_tree':run('git','rev-parse','HEAD:'+REL),'review_input_blob':'9c86a6fe706ad991765720f48fb78dde6b597a2b','retained_review_head':BASE,'retained_tree_unchanged':True,'source_changes':changes,'workflow_run':os.environ['GITHUB_RUN_ID']}
  (TMP/'R54_SOURCE_PUBLICATION.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n');save_env('R54_SOURCE_SHA',source)
 elif mode=='artifacts':
  source=os.environ['R54_SOURCE_SHA'];check(run('git','rev-parse','HEAD')==source and ref()==source,'source head raced')
  check(not run('git','status','--porcelain'),'build changed repository')
  changes=allowed_changes(source);receipt=json.loads((OUT/'BUILD_RECEIPT.json').read_text())
  check(receipt['status']=='PASS' and receipt['source_commit']==source,'unbound build')
  for name,item in receipt['delivery_pdfs'].items():check(sha((OUT/name).read_bytes())==item['sha256'],'PDF differs '+name)
  dest=ROOT/REL/'artifacts';check(not dest.exists(),'artifact path exists');dest.mkdir()
  for f in sorted(OUT.iterdir()):
   if f.is_file() and f.suffix in {'.pdf','.json','.log','.zip'}:shutil.copyfile(f,dest/f.name)
  shutil.copyfile(TMP/'R54_SOURCE_PUBLICATION.json',dest/'SOURCE_PUBLICATION.json')
  rec={'status':'PASS','source_commit':source,'native_source_tree':run('git','rev-parse',source+':'+REL),'retained_review_head':BASE,'retained_paths_unchanged':True,'source_changes':changes,'workflow_run':os.environ['GITHUB_RUN_ID'],'artifact_parent_must_equal_source':True,'files':{f.name:sha(f.read_bytes()) for f in sorted(dest.iterdir())}}
  (dest/'PUBLICATION_RECEIPT.json').write_text(json.dumps(rec,sort_keys=True,indent=2)+'\n')
  check(ref()==source,'head moved before artifact push');run('git','add','--',REL+'/artifacts');run('git','commit','-m','artifacts(theta R54): bind complete native and retained mathematics to immutable source')
  artifact=run('git','rev-parse','HEAD');check(run('git','rev-parse','HEAD^')==source,'artifact parent mismatch');run('git','push','origin','HEAD:refs/heads/'+BRANCH);save_env('R54_ARTIFACT_SHA',artifact)
 elif mode=='packets':
  source=os.environ['R54_SOURCE_SHA'];artifact=run('git','rev-parse','HEAD');check(run('git','rev-parse','HEAD^')==source,'artifact is not direct child')
  native=PACK/'native';native.mkdir(parents=True)
  names=['General_Theta_Foundations_I_restart_R54.pdf','R54_prepared_sources.zip','BUILD_RECEIPT.json','R54_LATEX_BUILD.log']
  for name in names:shutil.copyfile(OUT/name,native/name)
  for name in ['SOURCE_PUBLICATION.json','PUBLICATION_RECEIPT.json']:shutil.copyfile(ROOT/REL/'artifacts'/name,native/name)
  (native/'SOURCE_SHA.txt').write_text(source+'\n');(native/'ARTIFACT_SHA.txt').write_text(artifact+'\n');(native/'GIT_TREE.txt').write_text(run('git','ls-tree','-r',source)+'\n')
  groups=[PACK/('retained-'+str(i)) for i in range(1,4)];sizes=[0,0,0]
  for g in groups:g.mkdir()
  for f in sorted(OUT.glob('*.pdf'),key=lambda f:f.stat().st_size,reverse=True):
   if f.name==names[0]:continue
   i=min(range(3),key=lambda i:sizes[i]);shutil.copyfile(f,groups[i]/f.name);sizes[i]+=f.stat().st_size
  for g in groups:(g/'SOURCE_SHA.txt').write_text(source+'\n');(g/'ARTIFACT_SHA.txt').write_text(artifact+'\n')
  print(json.dumps({'source_commit':source,'artifact_commit':artifact,'group_bytes':sizes},indent=2))
 else:raise RuntimeError('unsupported operation')
if __name__=='__main__':main()
