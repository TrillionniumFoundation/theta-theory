#!/usr/bin/env python3
"""Publish only from the genuine remote base; never push an overlay root.
Uses ordinary Git authentication already configured by the operator. It does
not read or print credentials, modify previous refs, or use force-push.
"""
from __future__ import annotations
import argparse,datetime,hashlib,json,os,shutil,subprocess,sys
from pathlib import Path
SOURCE=Path(__file__).resolve().parents[1]
BASE='796e70b65ec17bccb165e047534ed07dd4b148e0'
BRANCH='revision/a2-dyn-summable-physical-source-2026-10-17'
COPY_BRANCH='revision/a2-dyn-summable-physical-source-referee-copy-2026-10-17'
ARTICLE='papers/A2-DYN-summable-physical-source-author-revision'
WORKFLOW='.github/workflows/a2-dyn-summable-physical-source-20261017.yml'
def main():
    ap=argparse.ArgumentParser();ap.add_argument('--workspace',type=Path,required=True)
    ap.add_argument('--receipt',type=Path,required=True);a=ap.parse_args()
    a.workspace.mkdir(parents=True,exist_ok=True);a.receipt.parent.mkdir(parents=True,exist_ok=True)
    rec={'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
         'base':BASE,'intended_branch':BRANCH,'remote_commit':None,'remote_push_completed':False,
         'source_manifest_sha256':hashlib.sha256((SOURCE/'SOURCE_MANIFEST.json').read_bytes()).hexdigest(),
         'commands':[],'restriction':'new added A2-DYN directory and its new dedicated workflow only; no previous ref changes'}
    env=dict(os.environ,GIT_TERMINAL_PROMPT='0',GIT_ASKPASS='/bin/false')
    def run(cmd,allow_failure=False):
        p=subprocess.run(cmd,cwd=a.workspace,env=env,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=25)
        rec['commands'].append({'command':cmd,'exit_code':p.returncode,'output':p.stdout})
        if p.returncode and not allow_failure:raise RuntimeError('command failed: '+' '.join(cmd))
        return p
    try:
        if (a.workspace/'.git').exists():raise RuntimeError('refusing to reuse an existing transport worktree')
        run(['git','init'])
        run(['git','remote','add','origin','https://github.com/TrillionniumFoundation/theta-theory.git'])
        run(['git','config','core.sparseCheckout','true'])
        (a.workspace/'.git/info/sparse-checkout').write_text('/'+ARTICLE+'/\n/'+WORKFLOW+'\n')
        existing=run(['git','ls-remote','--heads','origin','refs/heads/'+BRANCH,'refs/heads/'+COPY_BRANCH])
        if existing.stdout.strip():raise RuntimeError('new target ref already exists; no existing ref may move')
        run(['git','fetch','--no-tags','--filter=blob:none','--depth=1','origin',BASE])
        run(['git','checkout','-b',BRANCH,'FETCH_HEAD'])
        if run(['git','rev-parse','HEAD']).stdout.strip()!=BASE:raise RuntimeError('base identity mismatch')
        if run(['git','cat-file','-e',BASE+':'+ARTICLE],True).returncode==0:raise RuntimeError('target article already exists')
        if run(['git','cat-file','-e',BASE+':'+WORKFLOW],True).returncode==0:raise RuntimeError('target workflow already exists')
        dest=a.workspace/ARTICLE
        def ignore(directory,names):
            rejected={n for n in names if n in ('__pycache__','.git')}
            if Path(directory)==SOURCE:rejected.update(n for n in names if n in ('build','delivery'))
            return rejected
        shutil.copytree(SOURCE,dest,ignore=ignore)
        wf=a.workspace/WORKFLOW;wf.parent.mkdir(parents=True,exist_ok=True)
        shutil.copy2(SOURCE/'ci/a2-dyn-summable-physical-source-20261017.yml',wf)
        run(['git','add','--',ARTICLE,WORKFLOW])
        diff=run(['git','diff','--cached','--name-status']).stdout.splitlines()
        for line in diff:
            status,path=line.split('\t',1)
            if status!='A' or not(path.startswith(ARTICLE+'/') or path==WORKFLOW):raise RuntimeError('out-of-scope modification '+line)
        run(['git','-c','user.name=A2-DYN author revision workspace','-c','user.email=a2-dyn-revision@localhost',
             'commit','-m','A2-DYN: summable physical gap, singular critical closure and exact observation transport'])
        rec['local_repository_commit']=run(['git','rev-parse','HEAD']).stdout.strip()
        run(['git','push','--atomic','origin','HEAD:refs/heads/'+BRANCH,'HEAD:refs/heads/'+COPY_BRANCH])
        remote=run(['git','ls-remote','--heads','origin','refs/heads/'+BRANCH]).stdout.split()
        if not remote or remote[0]!=rec['local_repository_commit']:raise RuntimeError('remote ref not equal to committed source')
        copied=run(['git','ls-remote','--heads','origin','refs/heads/'+COPY_BRANCH]).stdout.split()
        if not copied or copied[0]!=remote[0]:raise RuntimeError('paired-copy ref mismatch')
        rec['paired_ref_readback']=True
        rec['remote_commit']=remote[0];rec['remote_push_completed']=True;rec['status']='published'
    except Exception as e:
        rec['status']='not_published';rec['error']=str(e)
    finally:
        rec['completed_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
        a.receipt.write_text(json.dumps(rec,indent=2,sort_keys=True)+'\n')
    print(json.dumps({'status':rec['status'],'remote_push_completed':rec['remote_push_completed'],'receipt':str(a.receipt)},indent=2))
    return 0 if rec['remote_push_completed'] else 1
if __name__=='__main__':sys.exit(main())
