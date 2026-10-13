#!/usr/bin/env python3
"""Bind verified outputs only; never modify ordinary mathematics or old refs."""
from pathlib import Path
import hashlib,json,os,shutil,subprocess,sys
BRANCH='foundation/general-theta-restart-r53-stopped-calibration-transfer-research-2026-10-13'
REL='papers/General-Theta-Foundations-I-restart/r53-stopped-calibration-transfer'
BASE='d0836f0348c2cc961196d34228d655cd1de10616'
NATIVE_TREE='794ee2032d99a16440be949fc85cbb618cf9d41d'
ROOT=Path(os.environ['GITHUB_WORKSPACE'])
OUT=Path(os.environ['RUNNER_TEMP'])/'r53-output'
PACK=Path(os.environ['RUNNER_TEMP'])/'r53-packets'
def check(ok,msg):
    if not ok:raise RuntimeError(msg)
def run(*args):return subprocess.check_output(args,cwd=ROOT,text=True).strip()
def sha(data):return hashlib.sha256(data).hexdigest()
def main():
    check(os.environ['GITHUB_REF_NAME']==BRANCH,'wrong write branch')
    source=os.environ['GITHUB_SHA'];mode=sys.argv[1]
    if mode=='artifacts':
        check(run('git','rev-parse','HEAD')==source,'source HEAD moved')
        check(run('git','rev-parse',source+':'+REL)==NATIVE_TREE,'native source differs')
        check(not run('git','status','--porcelain'),'build changed repository')
        changes=run('git','diff','--name-status',BASE,source).splitlines()
        allowed={'.github/workflows/theta-r53-build.yml','.github/scripts/theta-r53-artifacts.py'}
        for line in changes:
            status,path=line.split('\t',1)
            check(status=='A' and (path.startswith(REL+'/') or path in allowed),'changed inherited path: '+line)
        receipt=json.loads((OUT/'BUILD_RECEIPT.json').read_text())
        check(receipt['status']=='PASS' and receipt['source_commit']==source,'unbound build receipt')
        for name,item in receipt['delivery_pdfs'].items():
            check(sha((OUT/name).read_bytes())==item['sha256'],'PDF differs: '+name)
        dest=ROOT/REL/'artifacts';check(not dest.exists(),'artifact path already exists');dest.mkdir()
        for p in sorted(OUT.iterdir()):
            if p.is_file() and (p.suffix in {'.pdf','.json','.log','.zip'}):shutil.copyfile(p,dest/p.name)
        record={'status':'PASS','source_commit':source,'source_root_tree':run('git','rev-parse',source+'^{tree}'),'native_source_tree':NATIVE_TREE,'retained_head':BASE,'retained_paths_unchanged':True,'source_changes':changes,'workflow_run':os.environ['GITHUB_RUN_ID'],'artifact_parent_must_equal_source':True,'files':{p.name:sha(p.read_bytes()) for p in sorted(dest.iterdir())}}
        (dest/'PUBLICATION_RECEIPT.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    elif mode=='packets':
        artifact=run('git','rev-parse','HEAD')
        check(run('git','rev-parse','HEAD^')==source,'artifact is not direct child of source')
        native=PACK/'native';native.mkdir(parents=True)
        names=['General_Theta_Foundations_I_restart_R53.pdf','R53_prepared_sources.zip','BUILD_RECEIPT.json','R53_LATEX_BUILD.log']
        for name in names:shutil.copyfile(OUT/name,native/name)
        shutil.copyfile(ROOT/REL/'artifacts/PUBLICATION_RECEIPT.json',native/'PUBLICATION_RECEIPT.json')
        (native/'SOURCE_SHA.txt').write_text(source+'\n');(native/'ARTIFACT_SHA.txt').write_text(artifact+'\n')
        (native/'GIT_TREE.txt').write_text(run('git','ls-tree','-r',source)+'\n')
        groups=[PACK/('retained-'+str(i)) for i in range(1,4)]
        sizes=[0,0,0]
        for group in groups:group.mkdir()
        for p in sorted(OUT.glob('*.pdf'),key=lambda p:p.stat().st_size,reverse=True):
            if p.name==names[0]:continue
            i=min(range(3),key=lambda j:sizes[j]);shutil.copyfile(p,groups[i]/p.name);sizes[i]+=p.stat().st_size
        for group in groups:
            (group/'SOURCE_SHA.txt').write_text(source+'\n');(group/'ARTIFACT_SHA.txt').write_text(artifact+'\n')
        print(json.dumps({'source_commit':source,'artifact_commit':artifact,'retained_group_bytes':sizes},indent=2))
    else:raise RuntimeError('unsupported operation')
if __name__=='__main__':main()
