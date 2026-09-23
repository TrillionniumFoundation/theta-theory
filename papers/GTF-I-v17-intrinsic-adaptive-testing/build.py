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
REVIEW='b59d8527c8edc0361be3085604bcf3a920dbfbda'
MUTANTS=('negative_coefficient','wrong_adaptive_weight','convexify_private','hide_visible_seed','drop_actual_mark','erase_collision','omit_bayes_denominator','halve_presentation_error')

def sha(path:Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()
def require(ok:bool,message:str)->None:
    if not ok:raise RuntimeError(message)
def run(args:list[str],cwd:Path=HERE,ok:bool=True,env:dict|None=None)->subprocess.CompletedProcess:
    print("RUN "+" ".join(args),file=sys.stderr,flush=True)
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
    if os.environ.get('GITHUB_ACTIONS') == 'true':
        require(source_commit==os.environ.get('GTF_SOURCE_COMMIT'),'Workflow source identity mismatch')
        checkout_kind='source-pinned GitHub Actions checkout'
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
        run([sys.executable,str(HERE/'verify.py'),'--write-certificates',str(evidence)])
        for flags in ([],['-O']):
            for mutant in MUTANTS:
                p=run([sys.executable,*flags,str(HERE/'verify.py'),'--mutant',mutant],ok=False)
                require(p.returncode!=0 and 'FAILED:' in p.stdout and 'designated mutant survived' not in p.stdout,'Incorrect variant was not rejected at its intended check: '+mutant)
                negatives.append({'mode':'optimized' if flags else 'ordinary','mutant':mutant,'exit_code':p.returncode,'message':p.stdout.strip()})
        for edition,path in [('v16','GTF-I-v16-constructive-causal-certification/verify.py'),('v15','GTF-I-v15-certified-physical-comparison/verify.py'),('v14','GTF-I-v14-deficiency-certification/verify.py'),('v13','GTF-I-v13-intrinsic-deficiency/verify.py'),('v12','GTF-I-v12-causal-completion/verify.py'),('v11','GTF-I-v11-resource-comparison/verify.py'),('v10','GTF-I-v10-marked-duality/verify.py'),('v9','GTF-I-v9-causal-minimax/verify.py'),('v8','GTF-I-v8-decision-spectrum/verify.py'),('v7','GTF-I-v7-structural/verify.py'),('v6','GTF-I-v6-markov/verify.py'),('v5','GTF-I-v5-intrinsic/verify.py'),('v4','GTF-I-v4/verify.py'),('v3','GTF-I-v3/verify.py'),('v2','GTF-I-v2/verify.py'),('v1','GTF-I-v2/legacy/tools/verify.py')]:
            f=HERE.parent/path;p=run([sys.executable,str(f)],cwd=f.parent)
            (evidence/('INHERITED_'+edition.upper()+'.txt')).write_text(p.stdout)
            old.append({'edition':edition,'exit_code':p.returncode,'log_sha256':sha(evidence/('INHERITED_'+edition.upper()+'.txt'))})
        (evidence/'NEGATIVE_CONTROLS.json').write_text(json.dumps(negatives,indent=2)+'\n')
    compiler=run(['pdflatex','--version']).stdout.splitlines()[0]
    env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1790121600';env['FORCE_SOURCE_DATE']='1'
    versions={}; maps={}; compiled=set();all_bodies=set();canonical_inputs=set()
    with tempfile.TemporaryDirectory(prefix='gtf-v17-build-') as work:
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
            (evidence/(pdf+'.log')).write_text(log)
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
                        else:
                            require(f.parent==HERE,'Canonical source escapes the local submission tree: '+rel)
                            canonical_inputs.add(rel)
            versions[pdf]={'pages':pages,'sha256':sha(HERE/(pdf+'.pdf')),'passes':number,'labels':maps[pdf]}
    core={k for k in maps['paper'] if not k.endswith('@cref')}
    require(all(k in maps['complete-development'] and maps['paper'][k]['number']==maps['complete-development'][k]['number'] for k in core),'Canonical/companion numbering mismatch')
    retained=set()
    for rel in all_bodies:
        if rel in inherited:
            retained.update(re.findall(r'\\label\{([^}]+)\}',(REPO/rel).read_text()))
    require(retained<=set(maps['complete-development']),'Unresolved retained labels: '+str(retained-set(maps['complete-development'])))
    predecessor=json.loads((HERE/'PREDECESSOR_LABELS.json').read_text())['labels']
    require(set(predecessor)<=set(maps['complete-development']),'Missing v16 companion labels: '+str(set(predecessor)-set(maps['complete-development'])))
    for rel,digest in {**inherited,**new}.items():
        require(sha(REPO/rel)==digest,'Input changed during build: '+rel)
    submission=evidence/'SUBMISSION_SOURCES.zip'
    with zipfile.ZipFile(submission,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in sorted(canonical_inputs):
            item=zipfile.ZipInfo(Path(rel).name,date_time=(2026,9,23,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16
            z.writestr(item,(REPO/rel).read_bytes())
        z.writestr('README.txt','Compile main.tex with pdflatex three times. All TeX inputs are local. No font files are included.\n')
    metrics={'new_adaptive_certificate':None,'retained_v16_polynomial':None}
    if result:
        metrics['new_adaptive_certificate']={'raw_row_dimension':2,'selected_test_observable_dimension':2,'full_law_affine_dimension':3,'affine_tests_including_zero':4,'occupied_weights':3,'weight_degree_in_behavior':3,'Bernstein_degree_univariate':16,'coefficient_count':17,'derivative_nonnegative_terms':9,'maximum_stored_integer_bits':result['adaptive']['largest_integer_bit_length'],'actual_certificate_file_bytes':(evidence/'ADAPTIVE_CERTIFICATE.json').stat().st_size,'strict_lower_level':'2/5','certified_extra_margin':'9/8960','scope':'Test size and this verification certificate only; not a universal bit-complexity bound.'}
        # Recompute original exact v16 coefficient values for an honest size comparison.
        import importlib.util
        old_file=HERE.parent/'GTF-I-v16-constructive-causal-certification/certified_examples.py'
        spec=importlib.util.spec_from_file_location('retained_examples',old_file);module=importlib.util.module_from_spec(spec);sys.modules[spec.name]=module;spec.loader.exec_module(module)
        den,arr=module.bernstein_scaled(module.gap_polynomial(),96)
        compact=json.dumps({'denominator':str(den),'numerators':[[str(x)for x in row]for row in arr]},separators=(',',':')).encode()
        metrics['retained_v16_polynomial']={'D':2,'m':4,'p':12,'n':96,'coefficient_count':97**2,'maximum_stored_integer_bits':max(abs(den).bit_length(),max(abs(x).bit_length()for row in arr for x in row)),'recomputed_compact_array_bytes':len(compact),'strict_lower_level':'2/5','scope':'Recomputed compact numeric payload, not the byte size of the prior pretty-printed artifact.'}
    (evidence/'CERTIFICATE_COMPLEXITY.json').write_text(json.dumps(metrics,indent=2)+'\n')
    archive=evidence/'COMPILED_SOURCES.zip'
    paths=sorted(input_paths)
    with zipfile.ZipFile(archive,'w',compression=zipfile.ZIP_DEFLATED,compresslevel=9) as z:
        for rel in paths:
            item=zipfile.ZipInfo(rel,date_time=(2026,9,23,0,0,0));item.compress_type=zipfile.ZIP_DEFLATED;item.external_attr=0o100644<<16
            z.writestr(item,(REPO/rel).read_bytes())
    receipt={'edition':'General Theta Foundations I, seventeenth intrinsic-adaptive-testing revision','review_commit':REVIEW,'source_commit':source_commit,'checkout_kind':checkout_kind,
             'source_inputs_clean_at_build':not dirty_inputs,'remote_publication_claimed':False,'workflow_run':os.environ.get('GITHUB_RUN_ID'),'compiler':compiler,'source_date_epoch':env['SOURCE_DATE_EPOCH'],
             'inherited_inputs_checked':len(inherited),'new_source_inputs_checked':len(new),'compiled_tex_inputs':len(compiled),'archive_inputs':len(paths),'archive_sha256':sha(archive),'standalone_submission_inputs':len(canonical_inputs),'standalone_submission_sha256':sha(submission),'standalone_submission_bytes':submission.stat().st_size,'canonical_inputs_all_local':True,'certificate_complexity':metrics,
             'source_manifest_sha256':sha(HERE/'SOURCE_MANIFEST.json'),'preserved_v16_companion_labels':len(predecessor),'retained_labels_resolved':len(retained),'shared_canonical_labels_same_numbers':len(core),
             'views':versions,'diagnostics_executed':not args.skip_diagnostics,'finite_checks':result['checks'] if result else None,
             'negative_control_executions':negatives,'inherited_diagnostics':old,'pipeline_contract':pipeline,'scope':'Local build, exact input preservation and finite diagnostics only. Not a mathematical proof certificate, remote publication receipt, independent referee approval or journal acceptance.'}
    (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps({'status':'passed','source_commit':source_commit,'checkout_kind':checkout_kind,'pages':{k:v['pages'] for k,v in versions.items()},'finite_checks':receipt['finite_checks'],'retained_labels':len(retained),'shared_labels':len(core),'archive_inputs':len(paths)},indent=2))
if __name__=='__main__':main()
