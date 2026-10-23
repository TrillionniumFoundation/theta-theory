#!/usr/bin/env python3
"""Build the complete R80 article + one author addendum without duplicating history.
All inherited inputs are read from an exact, unchanged sibling source tree.
"""
from pathlib import Path
import argparse, datetime, hashlib, importlib.util, json, os, re, shutil, subprocess, sys
sys.dont_write_bytecode=True
ROOT=Path(__file__).resolve().parent
BASE=ROOT.parent/'r80-stability-and-saturation'
BASE_SOURCE='c0ac246181c2f4214e3e830952386adffb7d82df'
BASE_PUBLICATION='304357fcada3771a5d01a29cdd93b4f42434cb7d'
BASE_TREE='d9d760358cc951be5dff54c4495810d4bd342185'
BASE_PREFIX='papers/General-Theta-Foundations-I-restart/r80-stability-and-saturation'
PREFIX='papers/General-Theta-Foundations-I-restart/r80-controller-rigidity-addendum'
NEW_LABEL='thm:dot-first-order-controller-rigidity'
MANIFEST='SOURCE_MANIFEST.json'

def require(ok,message):
    if not ok: raise RuntimeError(message)
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def git(*a): return subprocess.check_output(['git',*a],cwd=ROOT,text=True).strip()
def files():
    return {p.relative_to(ROOT).as_posix():{'sha256':sha(p),'bytes':p.stat().st_size}
            for p in sorted(ROOT.rglob('*')) if p.is_file() and p.name!=MANIFEST and '__pycache__' not in p.parts}
def write(p,obj): Path(p).write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def seal(): write(ROOT/MANIFEST,{'schema':'theta.controller-rigidity.source.v1','base_source':BASE_SOURCE,'base_tree':BASE_TREE,'files':files()})
def run(cmd,cwd,log,env):
    with open(log,'wb') as f: subprocess.run(cmd,cwd=cwd,env=env,stdout=f,stderr=subprocess.STDOUT,check=True)

def main():
    p=argparse.ArgumentParser(); p.add_argument('--seal',action='store_true'); p.add_argument('--draft',action='store_true'); p.add_argument('--source-commit'); p.add_argument('--out',type=Path); p.add_argument('--skip-inherited-diagnostics',action='store_true'); a=p.parse_args()
    if a.seal: seal(); return
    require(a.out is not None,'--out required'); out=a.out.resolve(); require(not out.exists(),'Use a fresh output directory'); require(ROOT not in out.parents,'Build outside the sealed source'); out.mkdir(parents=True)
    receipt={'schema':'theta.controller-rigidity.build.v1','status':'RUNNING','mode':'draft' if a.draft else 'strict','started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'base_source_commit':BASE_SOURCE,'base_publication_commit':BASE_PUBLICATION,'base_paper_tree':BASE_TREE}
    try:
        before=files(); require(BASE.is_dir(),'Materialize the pinned R80 sibling; see README')
        expected_main=(BASE/'main.tex').read_text().replace('General_Theta_Foundations_I_R80_Supplement.pdf','General_Theta_Foundations_I_Controller_Rigidity_Supplement.pdf').replace(r'\input{sections/57-sharp-stability}',r'\input{sections/57-sharp-stability}'+chr(10)+r'\input{sections/60-first-order-controller-rigidity}')
        require((ROOT/'main.tex').read_text()==expected_main,'Unexpected inherited main-wrapper alteration')
        require((ROOT/'supplement.tex').read_text()==(BASE/'supplement.tex').read_text().replace('General_Theta_Foundations_I_R80.pdf','General_Theta_Foundations_I_Controller_Rigidity.pdf'),'Unexpected inherited supplement alteration')
        require(git('rev-parse',BASE_SOURCE+':'+BASE_PREFIX)==BASE_TREE,'Wrong R80 source object')
        require(git('rev-parse',BASE_PUBLICATION+':'+BASE_PREFIX)==BASE_TREE,'Publication changed its source')
        require(git('rev-parse','HEAD:'+BASE_PREFIX)==BASE_TREE,'HEAD changed the R80 source tree')
        require(subprocess.run(['git','diff','--quiet','HEAD','--',':(top)'+BASE_PREFIX],cwd=ROOT).returncode==0,'Dirty inherited source')
        if not a.draft:
            require(a.source_commit is not None and re.fullmatch('[0-9a-f]{40}',a.source_commit),'Full source commit required')
            require(git('rev-parse','HEAD')==a.source_commit,'HEAD is not the exact declared source commit')
            require(json.loads((ROOT/MANIFEST).read_text())['files']==before,'Addendum source seal mismatch')
            git('merge-base','--is-ancestor',BASE_PUBLICATION,a.source_commit)
            changed=git('diff','--no-relative','--name-only',BASE_PUBLICATION,a.source_commit).splitlines()
            require(changed and all(x.startswith(PREFIX+'/') for x in changed),'Source commit changes unrelated paths')
            require(not a.skip_inherited_diagnostics,'Cannot skip inherited diagnostics in strict mode')
            require(subprocess.run(['git','diff','--quiet',a.source_commit,'--',':(top)'+PREFIX],cwd=ROOT).returncode==0,'Dirty addendum source relative to declared commit')
            tracked=set(git('ls-tree','--full-tree','-r','--name-only',a.source_commit+':'+PREFIX).splitlines()); require(tracked==set(before)|{MANIFEST},'Unlisted current source files or omissions')
            receipt['source_commit']=a.source_commit; receipt['source_git_tree']=git('rev-parse','HEAD:'+PREFIX)
        sys.path.insert(0,str(BASE))
        spec=importlib.util.spec_from_file_location('pinned_r80_verify',BASE/'verify.py'); v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
        v.verify_manifest(); require(v.git_tree()==BASE_TREE,'Local inherited tree differs from the immutable R80 tree'); receipt['base_manifest_sha256']=sha(BASE/'SOURCE_MANIFEST.json')
        env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1',MKL_NUM_THREADS='1')
        # Fixed build epoch. Source identity is recorded separately, never inferred from a PDF date.
        env['SOURCE_DATE_EPOCH']='1792763911'
        if not a.skip_inherited_diagnostics:
            print('Running all 32 inherited diagnostic suites in ordinary and optimized Python',flush=True)
            receipt['inherited_diagnostics']=v.run_diagnostics(out,env)
        else: receipt['inherited_diagnostics_skipped_in_draft']=True
        for opt,name in [([], 'rigidity-normal.json'),(['-O'],'rigidity-optimized.json')]:
            run([sys.executable,'-B',*opt,'diagnostics_rigidity.py'],ROOT,out/name,env)
        require((out/'rigidity-normal.json').read_bytes()==(out/'rigidity-optimized.json').read_bytes(),'New diagnostic ordinary/optimized mismatch')
        receipt['new_diagnostic']=json.loads((out/'rigidity-normal.json').read_text())
        require(receipt['new_diagnostic']['status']=='PASS','New diagnostic failed')
        paired=out/'paired'; companion=out/'companion'; paired.mkdir(); companion.mkdir()
        penv=dict(env,TEXINPUTS=os.pathsep.join([str(paired),'.',str(BASE),env.get('TEXINPUTS','')]))
        for n in range(1,4):
            for stem in ['main','supplement']:
                print(f'Native {stem}, pass {n}/3',flush=True)
                run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-no-shell-escape','-recorder',f'-output-directory={paired}',stem+'.tex'],ROOT,paired/f'{stem}-pass-{n}.txt',penv)
                v.cross_labels(paired,stem)
        cenv=dict(env,TEXINPUTS=os.pathsep.join(['.',str(BASE/'companion-r58'),env.get('TEXINPUTS','')]))
        for n in range(1,4):
            run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-no-shell-escape','-recorder',f'-output-directory={companion}','main.tex'],BASE/'companion-r58',companion/f'pass-{n}.txt',cenv)
        old=json.loads((BASE/'THEOREM_INDEX.json').read_text()); oldlabels={r['label'] for r in old['statements']}; require(len(oldlabels)==267,'Wrong inherited statement inventory')
        origins={r['label']:r['source'] for r in old['statements']}; origins[NEW_LABEL]='sections/60-first-order-controller-rigidity.tex'
        labels=set(); rows=[]
        for stem in ['main','supplement']:
            for label,(number,page) in v.aux_labels(paired,stem).items():
                if label.split(':')[0] not in v.STATEMENT_PREFIXES: continue
                require(label not in labels,'Duplicate active statement: '+label); labels.add(label)
                require(label in origins and page.isdigit() and number,'Unknown or unresolved statement: '+label)
                rows.append({'label':label,'number':number,'page':int(page),'document':stem,'source':origins[label],'inherited_from_r80':label in oldlabels})
        require(labels==oldlabels|{NEW_LABEL},'Missing inherited or new statement')
        index={'schema':'theta.controller-rigidity.index.v1','inherited_statements':267,'new_statements':1,'statements':rows}
        write(out/'THEOREM_INDEX.json',index)
        if not a.draft: require(json.loads((ROOT/'THEOREM_INDEX.json').read_text())==index,'Sealed theorem locators differ')
        docs=[]
        for stem,folder,filename in [('main',paired,'General_Theta_Foundations_I_Controller_Rigidity.pdf'),('supplement',paired,'General_Theta_Foundations_I_Controller_Rigidity_Supplement.pdf'),('main',companion,'General_Theta_Foundations_I_Retained_Companion_R58.pdf')]:
            v.check_native_log(folder,stem,filename); target=out/filename; shutil.copyfile(folder/(stem+'.pdf'),target)
            info=subprocess.check_output(['pdfinfo',str(target)],text=True); pages=int(re.search(r'Pages:\s+(\d+)',info).group(1))
            txt=target.with_suffix('.txt'); subprocess.run(['pdftotext',str(target),str(txt)],check=True)
            docs.append({'file':filename,'sha256':sha(target),'bytes':target.stat().st_size,'pages':pages,'text_sha256':sha(txt),'passes':3,'no_shell_escape':True,'unresolved_or_overfull':False})
        require(files()==before,'Addendum source changed during build'); v.verify_manifest()
        receipt['python']=sys.version; receipt['pdflatex']=subprocess.check_output(['pdflatex','--version'],text=True).splitlines()[0]
        receipt['source_date_epoch']=env['SOURCE_DATE_EPOCH']; receipt['new_diagnostic_ordinary_optimized_identity']=True
        receipt['diagnostic_suite_count']=len(receipt.get('inherited_diagnostics',{}))+1
        receipt['total_checks']=sum(x['total_checks'] for x in receipt.get('inherited_diagnostics',{}).values())+receipt['new_diagnostic']['exact_checks']
        receipt.update(status='DRAFT_PASS' if a.draft else 'PASS',documents=docs,compiled_statement_count=len(rows),source_unchanged=True,source_manifest_sha256=sha(ROOT/MANIFEST) if (ROOT/MANIFEST).exists() else None,completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),limitations=['This is native execution and finite diagnostics, not a universal proof or external referee verdict.','The mathematical addition is the first-order optimizer iff in one fixed two-model/two-label family.','The full R80 source and its 267 statements are inherited, not newly discovered.'])
    except Exception as e:
        receipt.update(status='FAIL',error=repr(e),completed_utc=datetime.datetime.now(datetime.timezone.utc).isoformat()); write(out/'BUILD_RECEIPT.json',receipt); raise
    write(out/'BUILD_RECEIPT.json',receipt); print(json.dumps({'status':receipt['status'],'compiled_statements':receipt['compiled_statement_count'],'receipt':str(out/'BUILD_RECEIPT.json')},indent=2))
if __name__=='__main__': main()
