#!/usr/bin/env python3
"""Additive R57 publication. Static checked delta; no historical publisher executed."""
from pathlib import Path
import argparse,base64,hashlib,json,lzma,os,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parents[2]
PAPER=Path('papers/General-Theta-Foundations-I-restart')
DEST=PAPER/'r57-role-aware-transfer';OLD=PAPER/'r56-balanced-task-transfer'
BRANCH='foundation/general-theta-restart-r57-role-aware-transfer-research-2026-10-14'
BASE='0d26798b229ea0221db59f136519f8806ca49b25'
REVIEW='73d3876b1186672d83ab2df515221bff2abd391f'
REPORT='GENERAL_THETA_FOUNDATIONS_I_RESTART_R56_BALANCED_TASK_TRANSFER_EXTERNAL_REFEREE_REPORT_R56.md'
XZ='bdc72f9d59dbd01ce2de20edb6240cdc3968742d76549c224a091cd4ef9b8f04'
PAYLOAD='81830530b1f74325c95736f33fe096b8143b26db9ae63fef544bb91747ca8836'
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(data):return hashlib.sha256(data).hexdigest()
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT,text=True).strip()
def run(*args):subprocess.run(list(args),cwd=ROOT,check=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
def remote():return git('ls-remote','origin','refs/heads/'+BRANCH).split()[0]
def publish(expected):
 need(remote()==expected,'remote lease changed; refusing to push')
 run('git','push','origin','HEAD:refs/heads/'+BRANCH)
def bind(name,value):
 print(name+'='+value)
 if os.environ.get('GITHUB_OUTPUT'):
  with open(os.environ['GITHUB_OUTPUT'],'a') as f:f.write(name+'='+value+'\n')
def prepare():
 before=git('rev-parse','HEAD');need(remote()==before,'wrong initial remote head')
 need(git('rev-parse',f'{REVIEW}:{OLD}')==git('rev-parse',f'HEAD:{OLD}'),'retained native tree changed')
 parts=sorted((ROOT/'.github/data').glob('theta-r57-source.part*'));need(len(parts)==6,'six delta transport parts required')
 compressed=base64.b64decode(''.join(p.read_text().strip() for p in parts),validate=True);need(sha(compressed)==XZ,'transport digest')
 raw=lzma.decompress(compressed);need(sha(raw)==PAYLOAD,'payload digest');records=json.loads(raw)
 need(not (ROOT/DEST).exists(),'R57 source already exists; do not overwrite')
 for name,rec in records.items():
  rel=Path(name);need(not rel.is_absolute() and '..' not in rel.parts and not {'.git','artifacts','evidence','__pycache__'}.intersection(rel.parts),'unsafe source path')
  old=ROOT/OLD/rel;oldtext=old.read_text() if old.exists() else '';need(sha(oldtext.encode())==rec['base_sha256'],'base mismatch '+name)
  lines=oldtext.splitlines(keepends=True);result=[]
  for piece in rec['pieces']:
   if isinstance(piece,str):result.append(piece)
   else:
    need(isinstance(piece,list) and len(piece)==2 and all(type(x)is int for x in piece) and 0<=piece[0]<=piece[1]<=len(lines),'invalid slice')
    result.append(''.join(lines[piece[0]:piece[1]]))
  data=''.join(result).encode();need(sha(data)==rec['sha256'],'reconstructed digest '+name)
  target=ROOT/DEST/rel;target.parent.mkdir(parents=True,exist_ok=True);target.write_bytes(data)
 report=(ROOT/REPORT).read_bytes();blob=hashlib.sha1(b'blob '+str(len(report)).encode()+b'\0'+report).hexdigest();need(blob=='15c692a39c17a34a408e2979f049c87b804179f8','latest review pin')
 target=ROOT/DEST/'review_inputs/R56_EXTERNAL_REFEREE_REPORT.md';target.parent.mkdir(exist_ok=True);target.write_bytes(report)
 run(sys.executable,str(ROOT/DEST/'seal.py'));run(sys.executable,str(ROOT/DEST/'verify.py'))
 run('git','add','--',str(DEST));run('git','commit','-m','math(theta): R57 role-aware causal transfer, sharp approximate balance and directional sensing')
 source=git('rev-parse','HEAD');need(git('rev-parse','HEAD^')==before,'source parent')
 changed=git('diff','--name-only',BASE,source).splitlines()
 allowed=lambda p:p.startswith(str(DEST)+'/') or p.startswith('.github/data/theta-r57-') or p in {'.github/scripts/theta-r57-publish.py','.github/workflows/theta-r57.yml'}
 need(all(allowed(p) for p in changed),'unrelated modification')
 need(not git('diff','--name-only','--diff-filter=D',BASE,source),'deletion forbidden')
 publish(before);bind('source_sha',source)
def store(build:Path):
 source=git('rev-parse','HEAD');need(remote()==source,'source head changed')
 receipt=json.loads((build/'BUILD_RECEIPT.json').read_text());need(receipt['status']=='PASS' and receipt['source_commit']==source,'build/source binding')
 dest=ROOT/DEST/'artifacts';dest.mkdir()
 files=list(build.glob('*.pdf'))+[build/'BUILD_RECEIPT.json',build/'R57_prepared_sources.zip',build/'R57_LATEX_BUILD.log']
 for f in files:need(f.is_file(),'missing artifact '+str(f));shutil.copyfile(f,dest/f.name)
 preserved={'r56_tree':git('rev-parse',f'{source}:{OLD}'),'review_r56_tree':git('rev-parse',f'{REVIEW}:{OLD}'),'review_commit':REVIEW,'canonical':'18000b21e4bfd89180ccb069e46ac0f21621f34d'}
 need(preserved['r56_tree']==preserved['review_r56_tree'],'retained tree mutation')
 controls=['foundations/general-theta/General_Theta_Foundations_v0.1.md','foundations/general-theta/RESTART_CHARTER.md',str(PAPER/'THEOREM_TARGETS.md'),'foundations/general-theta/REALIZATION_REGISTRY.md']
 for p in controls:need(git('rev-parse',source+':'+p)==git('rev-parse',preserved['canonical']+':'+p),'control changed '+p)
 pub={'source_commit':source,'source_root_tree':git('rev-parse',source+'^{tree}'),'preservation':preserved,'transport_sha256':XZ,'payload_sha256':PAYLOAD,'build_run_id':os.environ.get('GITHUB_RUN_ID'),'files':{f.name:sha(f.read_bytes()) for f in files},'scope':'ordinary source, binary artifacts and final external read-only evidence have separate commits'}
 (dest/'SOURCE_PUBLICATION.json').write_text(json.dumps(pub,indent=2,sort_keys=True)+'\n')
 run('git','add','-f','--',str(dest));run('git','commit','-m','build(theta): store R57 complete PDF packet and source-bound build receipts')
 artifact=git('rev-parse','HEAD');need(git('rev-parse','HEAD^')==source,'artifact parent must be source');publish(source)
 packaging=build/'download';native=packaging/'native';native.mkdir(parents=True)
 for name in ['General_Theta_Foundations_I_restart_R57.pdf','BUILD_RECEIPT.json','R57_prepared_sources.zip','R57_LATEX_BUILD.log']:
  shutil.copyfile(build/name,native/name)
 shutil.copyfile(dest/'SOURCE_PUBLICATION.json',native/'SOURCE_PUBLICATION.json')
 (native/'SOURCE_SHA.txt').write_text(source+'\n');(native/'ARTIFACT_SHA.txt').write_text(artifact+'\n');(native/'ARTIFACT_TREE.txt').write_text(git('rev-parse','HEAD^{tree}')+'\n')
 group=1;size=0
 for f in sorted(build.glob('*.pdf')):
  if f.name=='General_Theta_Foundations_I_restart_R57.pdf':continue
  if size+f.stat().st_size>4500000:group+=1;size=0
  d=packaging/f'retained-{group}';d.mkdir(exist_ok=True);shutil.copyfile(f,d/f.name);size+=f.stat().st_size
 need(group<=6,'artifact grouping capacity');bind('artifact_sha',artifact);bind('artifact_groups',str(group))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','store']);p.add_argument('--build',type=Path);a=p.parse_args()
 need(os.environ.get('GITHUB_REF_NAME')==BRANCH,'wrong branch');run('git','config','user.name','github-actions[bot]');run('git','config','user.email','41898282+github-actions[bot]@users.noreply.github.com')
 if a.mode=='prepare':prepare()
 else:need(a.build is not None,'build directory required');store(a.build.resolve())
