#!/usr/bin/env python3
"""Rebuild and identify both manuscript views. Evidence is not proof certification."""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE=Path(__file__).resolve().parent
REPO=HERE.parents[1]
REVIEW='fc6d51a47b42a3f097ea530b67616591c421db3b'
MUTANTS=('task_after_encoder','collapsed_likelihood','drop_compatibility','raw_energy_threshold',
         'marginal_is_realized','free_transcript','product_closure')

def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok:bool,message:str)->None:
    if not ok:raise RuntimeError(message)
def run(args:list[str],cwd:Path=HERE,ok:bool=True,env:dict|None=None)->subprocess.CompletedProcess:
    p=subprocess.run(args,cwd=cwd,text=True,encoding="utf-8",errors="replace",stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
    if ok and p.returncode:raise RuntimeError('Command failed: '+' '.join(args)+'\n'+p.stdout[-6000:])
    return p

def labels(path:Path)->dict:
    return {m.group(1):{'number':m.group(2),'page':int(m.group(3))}
            for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',path.read_text())}

def main()->None:
    parser=argparse.ArgumentParser();parser.add_argument('--skip-diagnostics',action='store_true',help='typesetting/preservation only; receipt explicitly records diagnostics not rerun');args=parser.parse_args()
    evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
    inherited=json.loads((HERE/'INHERITED_INPUTS.json').read_text())['files']
    new=json.loads((HERE/'SOURCE_MANIFEST.json').read_text())['files']
    for rel,digest in {**inherited,**new}.items():
        p=REPO/rel;require(p.is_file(),'Missing input '+rel);require(sha(p)==digest,'Input digest mismatch '+rel)
    require(not any(Path(p).suffix.lower() in {'.ttf','.otf','.pfb','.woff','.woff2'} for p in {**inherited,**new}),'Font files must not be packaged')
    git=run(['git','rev-parse','HEAD'],cwd=REPO,ok=False)
    source_commit=git.stdout.strip() if git.returncode==0 else None
    full_base=run(['git','cat-file','-e',REVIEW+'^{commit}'],cwd=REPO,ok=False).returncode==0 if source_commit else False
    checkout_kind='remote-history checkout' if full_base else ('local source-archive reconstruction' if source_commit else 'standalone extracted archive')
    changed=run(['git','status','--porcelain','--untracked-files=all'],cwd=REPO,ok=False).stdout.splitlines() if source_commit else []
    input_paths=set(inherited)|set(new)|{str((HERE/'SOURCE_MANIFEST.json').relative_to(REPO))}
    dirty_inputs=[line for line in changed if line[3:] in input_paths]
    require(not dirty_inputs,'Refusing to bind dirty mathematical/source inputs to HEAD: '+str(dirty_inputs[:8]))
    pipeline=json.loads(run([sys.executable,str(HERE/'verify_pipeline.py')]).stdout)
    (evidence/'PIPELINE_CONTRACT_CHECK.json').write_text(json.dumps(pipeline,indent=2)+'\n')
    result=None;negatives=[];old=[]
    if not args.skip_diagnostics:
        normal=run([sys.executable,str(HERE/'verify.py')]).stdout
        optimized=run([sys.executable,'-O',str(HERE/'verify.py')]).stdout
        result=json.loads(normal);require(result==json.loads(optimized),'Normal/optimized diagnostic mismatch')
        (evidence/'DIAGNOSTICS.json').write_text(normal)
        for flags in ([],['-O']):
            for mutant in MUTANTS:
                p=run([sys.executable,*flags,str(HERE/'verify.py'),'--mutant',mutant],ok=False)
                require(p.returncode!=0 and 'FAILED:' in p.stdout and 'designated mutant survived' not in p.stdout,'Incorrect variant was not rejected at its intended check: '+mutant)
                negatives.append({'mode':'optimized' if flags else 'ordinary','mutant':mutant,'exit_code':p.returncode,'message':p.stdout.strip()})
        for edition,path in [('v7','GTF-I-v7-structural/verify.py'),('v6','GTF-I-v6-markov/verify.py'),('v5','GTF-I-v5-intrinsic/verify.py'),('v4','GTF-I-v4/verify.py'),('v3','GTF-I-v3/verify.py'),('v2','GTF-I-v2/verify.py'),('v1','GTF-I-v2/legacy/tools/verify.py')]:
            f=HERE.parent/path;p=run([sys.executable,str(f)],cwd=f.parent)
            (evidence/('INHERITED_'+edition.upper()+'.txt')).write_text(p.stdout)
            old.append({'edition':edition,'exit_code':p.returncode,'log_sha256':sha(evidence/('INHERITED_'+edition.upper()+'.txt'))})
        (evidence/'NEGATIVE_CONTROLS.json').write_text(json.dumps(negatives,indent=2)+'\n')
    compiler=run(['pdflatex','--version']).stdout.splitlines()[0]
    env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1790121600';env['FORCE_SOURCE_DATE']='1'
    versions={}; maps={}; compiled=set();all_bodies=set()
    with tempfile.TemporaryDirectory(prefix='gtf-v8-build-') as work:
        work=Path(work)
        for tex,pdf in [('main','paper'),('development','complete-development')]:
            out=work/tex;out.mkdir()
            previous=None;stable=False
            for number in range(1,6):
                p=run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory='+str(out),tex+'.tex'],env=env)
                current=((out/(tex+'.aux')).read_bytes(),(out/(tex+'.toc')).read_bytes())
                if number>=3 and current==previous:stable=True;break
                previous=current
            require(stable,'TeX references failed to stabilize for '+tex)
            log=(out/(tex+'.log')).read_text(errors='replace')
            bad=('undefined references','There were undefined','multiply defined','Overfull \\hbox','Overfull \\vbox','Citation `')
            require(not any(s in log for s in bad),'Unresolved reference, duplicate label or overflow in '+tex)
            shutil.copy2(out/(tex+'.pdf'),HERE/(pdf+'.pdf'))
            shutil.copy2(out/(tex+'.aux'),evidence/(pdf+'.aux'))
            (evidence/(pdf+'.log')).write_text(log)
            maps[pdf]=labels(out/(tex+'.aux'))
            info=run(['pdfinfo',str(HERE/(pdf+'.pdf'))]).stdout
            pages=int(re.search(r'^Pages:\s+(\d+)',info,re.M).group(1))
            # Every repository-local LaTeX input must be hash-pinned, including dependencies.
            for line in (out/(tex+'.fls')).read_text().splitlines():
                if line.startswith('INPUT '):
                    f=Path(line[6:]);f=f if f.is_absolute() else HERE/f
                    f=f.resolve()
                    try:rel=str(f.relative_to(REPO))
                    except ValueError:continue
                    if f.suffix=='.tex':
                        require(rel in input_paths,'Unpinned TeX input '+rel);compiled.add(rel)
                        if pdf=='complete-development':all_bodies.add(rel)
            versions[pdf]={'pages':pages,'sha256':sha(HERE/(pdf+'.pdf')),'passes':number,'labels':maps[pdf]}
    core={k for k in maps['paper'] if not k.endswith('@cref')}
    require(all(k in maps['complete-development'] and maps['paper'][k]['number']==maps['complete-development'][k]['number'] for k in core),'Canonical/companion numbering mismatch')
    retained=set()
    for rel in all_bodies:
        if rel in inherited:
            retained.update(re.findall(r'\\label\{([^}]+)\}',(REPO/rel).read_text()))
    require(retained<=set(maps['complete-development']),'Unresolved retained labels: '+str(retained-set(maps['complete-development'])))
    archive=evidence/'COMPILED_SOURCES.zip'
    paths=sorted(input_paths)
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in paths:
            item=zipfile.ZipInfo(rel,date_time=(2026,9,23,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16
            z.writestr(item,(REPO/rel).read_bytes())
    receipt={'edition':'General Theta Foundations I, eighth decision-spectrum revision','review_commit':REVIEW,'source_commit':source_commit,'checkout_kind':checkout_kind,
             'source_inputs_clean_at_build':not dirty_inputs,'remote_publication_claimed':False,'workflow_run':None,'compiler':compiler,'source_date_epoch':env['SOURCE_DATE_EPOCH'],
             'inherited_inputs_checked':len(inherited),'new_source_inputs_checked':len(new),'compiled_tex_inputs':len(compiled),'archive_inputs':len(paths),'archive_sha256':sha(archive),
             'source_manifest_sha256':sha(HERE/'SOURCE_MANIFEST.json'),'retained_labels_resolved':len(retained),'shared_canonical_labels_same_numbers':len(core),
             'views':versions,'diagnostics_executed':not args.skip_diagnostics,'finite_checks':result['finite_checks'] if result else None,
             'negative_control_executions':negatives,'inherited_diagnostics':old,'pipeline_contract':pipeline,'scope':'Local build, exact input preservation and finite diagnostics only. Not a mathematical proof certificate, remote publication receipt, independent referee approval or journal acceptance.'}
    (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'passed','source_commit':source_commit,'checkout_kind':checkout_kind,'pages':{k:v['pages'] for k,v in versions.items()},'finite_checks':receipt['finite_checks'],'retained_labels':len(retained),'shared_labels':len(core),'archive_inputs':len(paths)},indent=2))
if __name__=='__main__':main()
