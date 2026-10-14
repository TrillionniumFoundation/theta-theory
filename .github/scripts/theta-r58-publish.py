#!/usr/bin/env python3
"""Additive R58 publication with an exact, non-executable source delta."""
from pathlib import Path
import argparse,base64,hashlib,json,lzma,os,shutil,subprocess,sys,zipfile,io
ROOT=Path(__file__).resolve().parents[2]
PAPER=Path('papers/General-Theta-Foundations-I-restart')
DEST=PAPER/'r58-reference-stability'; OLD=PAPER/'r57-role-aware-transfer'
BRANCH='foundation/general-theta-restart-r58-reference-stability-research-2026-10-14'
BASE='97cf6bb4719d15482f79162569766403dab607e8'
CANON='18000b21e4bfd89180ccb069e46ac0f21621f34d'
REVIEW='73d3876b1186672d83ab2df515221bff2abd391f'
XZ='1dffb5d258a48f2e4555175f0d4d23895946d4d969eaa6df70b287b424658ffd'
PAYLOAD='72ffb786d10f607e8f02d7fa075fce032096653ab226d281e8fe6636e433ffb7'
MANIFEST='fea8ca55592c59d8cac848cf7e98872fb26c15c213916a92f69ce1823cfa9e0f'
PROJECTION='85e02e0aeb1e200f1bad7388bb7b55512b94a2db'
OUTER='558e4fdee6ab775217028db6001a5c05bdef9e2942720c99813fc95b6fdf33e8'
INNER='bdf7ff7c082f9ff0b71db0b69f2f788e8456e5032c3f082d015b9054c4d8e9a9'
def need(ok,msg):
 if not ok: raise RuntimeError(msg)
def sha(b): return hashlib.sha256(b).hexdigest()
def git(*args): return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def run(*args): subprocess.run(list(args),cwd=ROOT,check=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
def remote(): return git('ls-remote','origin','refs/heads/'+BRANCH).split()[0]
def publish(expected):
 need(remote()==expected,'remote lease changed; refusing to push')
 run('git','push','origin','HEAD:refs/heads/'+BRANCH)
def bind(name,value):
 print(name+'='+value)
 if os.environ.get('GITHUB_OUTPUT'):
  with open(os.environ['GITHUB_OUTPUT'],'a') as f: f.write(name+'='+value+'\n')
def relpath(name):
 p=Path(name)
 need(not p.is_absolute() and '..' not in p.parts and not {'.git','artifacts','evidence','__pycache__'}.intersection(p.parts),'unsafe source path')
 return p
def preservation(source):
 need(git('rev-parse',source+':'+str(OLD))==git('rev-parse',BASE+':'+str(OLD)),'R57 tree changed')
 controls=['foundations/general-theta/General_Theta_Foundations_v0.1.md','foundations/general-theta/RESTART_CHARTER.md',str(PAPER/'THEOREM_TARGETS.md'),'foundations/general-theta/REALIZATION_REGISTRY.md']
 for p in controls: need(git('rev-parse',source+':'+p)==git('rev-parse',CANON+':'+p),'control changed '+p)
 changed=git('diff','--name-only',BASE,source).splitlines()
 allowed=lambda p:p.startswith(str(DEST)+'/') or p.startswith('.github/data/theta-r58-') or p in {'.github/scripts/theta-r58-publish.py','.github/workflows/theta-r58-complete.yml','.github/workflows/theta-r58-inputs.yml'}
 need(all(allowed(p) for p in changed),'unrelated change relative to pinned R57')
 need(not git('diff','--name-only','--diff-filter=D',BASE,source),'historical deletion')
 return {'canonical':CANON,'latest_external_review':REVIEW,'inherited_r57_source':BASE,'inherited_r57_tree':git('rev-parse',source+':'+str(OLD)),'controls_unchanged':True,'only_new_R58_paths_changed':True}
def prepare():
 before=git('rev-parse','HEAD'); need(remote()==before,'wrong initial remote head'); preservation(before)
 parts=sorted((ROOT/'.github/data').glob('theta-r58-source.part*')); need(len(parts)==6,'six transport parts required')
 compressed=base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True); need(sha(compressed)==XZ,'transport digest')
 raw=lzma.decompress(compressed); need(sha(raw)==PAYLOAD,'payload digest'); records=json.loads(raw); need(len(records)==51,'source inventory cardinality')
 need(not (ROOT/DEST).exists(),'R58 exists; do not overwrite')
 for name,rec in records.items():
  rel=relpath(name); old=ROOT/OLD/relpath(rec['base_path']); oldtext=old.read_text() if old.exists() else ''
  need(sha(oldtext.encode())==rec['base_sha256'],'base mismatch '+name); lines=oldtext.splitlines(keepends=True); result=[]
  for piece in rec['pieces']:
   if isinstance(piece,str): result.append(piece)
   else:
    need(isinstance(piece,list) and len(piece)==2 and all(type(x)is int for x in piece) and 0<=piece[0]<=piece[1]<=len(lines),'invalid slice')
    result.append(''.join(lines[piece[0]:piece[1]]))
  data=''.join(result).encode(); need(sha(data)==rec['sha256'],'reconstruction '+name)
  target=ROOT/DEST/rel; target.parent.mkdir(parents=True,exist_ok=True); target.write_bytes(data)
 # Correct two provenance strings against the pinned commit's actual root tree.
 actual_root=git('rev-parse',BASE+'^{tree}'); need(actual_root=='c427eb8036b6118f99a3859fbf26ec24c16f04b9','pinned root tree')
 for name in ['PINNED_INPUTS.json','SOURCE_LINEAGE.md']:
  p=ROOT/DEST/name; text=p.read_text(); wrong='8d88c7e9f3bcc5a5a6e6e86c5e91d3d6e61a7aa5'
  need(text.count(wrong)==1,'expected provenance correction'); p.write_text(text.replace(wrong,actual_root))
 run(sys.executable,str(ROOT/DEST/'seal.py'))
 audit=json.loads(subprocess.check_output([sys.executable,str(ROOT/DEST/'verify.py')],cwd=ROOT,text=True))
 need(sha((ROOT/DEST/'SOURCE_MANIFEST.json').read_bytes())==MANIFEST,'sealed manifest mismatch')
 need(audit['ordinary_source_projection_tree_sha']==PROJECTION,'source projection mismatch')
 run('git','add','--',str(DEST)); run('git','commit','-m','math(theta): R58 two-sided calibrated acquired-geometry transfer and metastable occupation bounds')
 source=git('rev-parse','HEAD'); need(git('rev-parse','HEAD^')==before,'source parent'); preservation(source); publish(before); bind('source_sha',source)
def historical(archive:Path,target:Path):
 data=archive.read_bytes(); need(sha(data)==OUTER,'R56 artifact hash')
 with zipfile.ZipFile(io.BytesIO(data)) as z:
  names=[n for n in z.namelist() if n.endswith('R56_prepared_sources.zip')]; need(len(names)==1,'prepared input ambiguity'); inner=z.read(names[0])
 need(sha(inner)==INNER,'R56 prepared archive hash'); need(not target.exists(),'prepared destination must be fresh'); target.mkdir(parents=True)
 with zipfile.ZipFile(io.BytesIO(inner)) as z:
  for item in z.infolist():
   p=Path(item.filename); need(not p.is_absolute() and '..' not in p.parts and '.git' not in p.parts,'unsafe historical zip path')
   need((item.external_attr>>16)&0o170000 !=0o120000,'symlink disallowed'); z.extract(item,target)
 snapshot={p.relative_to(target).as_posix():sha(p.read_bytes()) for p in target.rglob('*') if p.is_file()}
 for subtree in [OLD,DEST]:
  dest=target/subtree; need(not dest.exists(),'historical additive collision'); shutil.copytree(ROOT/subtree,dest,ignore=shutil.ignore_patterns('artifacts','evidence','__pycache__'))
 report=(ROOT/OLD/'review_inputs/R56_EXTERNAL_REFEREE_REPORT.md').read_bytes()
 need(hashlib.sha1(b'blob '+str(len(report)).encode()+b'\0'+report).hexdigest()=='15c692a39c17a34a408e2979f049c87b804179f8','R56 report pin')
 report_path=target/'GENERAL_THETA_FOUNDATIONS_I_RESTART_R56_BALANCED_TASK_TRANSFER_EXTERNAL_REFEREE_REPORT_R56.md'
 need(not report_path.exists() or report_path.read_bytes()==report,'historical report collision'); report_path.write_bytes(report)
 need(all(sha((target/n).read_bytes())==h for n,h in snapshot.items()),'historical input mutation')
 bind('prepared_root',str(target)); bind('retained_input_files',str(len(snapshot)))
def store(build:Path):
 source=git('rev-parse','HEAD'); need(remote()==source,'source head changed'); keep=preservation(source)
 need(not git('diff','--name-only',source,'--',str(DEST)),'source working tree changed')
 receipt=json.loads((build/'BUILD_RECEIPT.json').read_text()); need(receipt['status']=='PASS' and receipt['source_commit']==source,'build/source binding')
 need(receipt['ordinary_source_projection_tree_sha']==PROJECTION,'build/source projection')
 dest=ROOT/DEST/'artifacts'; need(not dest.exists(),'artifact destination collision'); dest.mkdir()
 files=list(sorted(build.glob('*.pdf')))+[build/'BUILD_RECEIPT.json',build/'R58_prepared_sources.zip',build/'R58_LATEX_BUILD.log']
 need(len(list(build.glob('*.pdf')))==30,'complete thirty-PDF packet required')
 for f in files: need(f.is_file(),'missing artifact '+str(f)); shutil.copyfile(f,dest/f.name)
 pub={'source_commit':source,'source_root_tree':git('rev-parse',source+'^{tree}'),'preservation':keep,'transport_sha256':XZ,'payload_sha256':PAYLOAD,'build_run_id':os.environ.get('GITHUB_RUN_ID'),'files':{f.name:sha(f.read_bytes()) for f in files},'scope':'source, artifacts and final independent read-only evidence are separately committed; tests are not proof certificates'}
 (dest/'SOURCE_PUBLICATION.json').write_text(json.dumps(pub,indent=2,sort_keys=True)+'\n')
 run('git','add','-f','--',str(dest)); run('git','commit','-m','build(theta): bind complete R58 PDF packet and read-only receipts to ordinary source')
 artifact=git('rev-parse','HEAD'); need(git('rev-parse','HEAD^')==source,'artifact parent must be source'); preservation(artifact); publish(source)
 complete=build/'download/complete'; complete.mkdir(parents=True)
 for f in files+[dest/'SOURCE_PUBLICATION.json']: shutil.copyfile(f,complete/f.name)
 (complete/'SOURCE_SHA.txt').write_text(source+'\n'); (complete/'ARTIFACT_SHA.txt').write_text(artifact+'\n'); (complete/'ARTIFACT_TREE.txt').write_text(git('rev-parse','HEAD^{tree}')+'\n')
 bind('artifact_sha',artifact)
if __name__=='__main__':
 p=argparse.ArgumentParser(); p.add_argument('mode',choices=['prepare','historical','store']); p.add_argument('--build',type=Path); p.add_argument('--archive',type=Path); p.add_argument('--target',type=Path); a=p.parse_args()
 need(os.environ.get('GITHUB_REF_NAME')==BRANCH,'wrong branch')
 run('git','config','user.name','github-actions[bot]'); run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
 if a.mode=='prepare': prepare()
 elif a.mode=='historical': need(a.archive is not None and a.target is not None,'historical arguments'); historical(a.archive.resolve(),a.target.resolve())
 else: need(a.build is not None,'build directory required'); store(a.build.resolve())
