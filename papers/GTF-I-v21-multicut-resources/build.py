#!/usr/bin/env python3
"""Reproduce v21, finite diagnostics, and the untouched 400-page history."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,zipfile
from pathlib import Path
import fitz
P=Path(__file__).resolve().parent
BASE=P.parent/'GTF-I-v20-continuation-classification'

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def command(args:list[str],**kwargs):
    return subprocess.run(args,cwd=P,check=True,text=True,**kwargs)

def main():
    E=P/'evidence';E.mkdir(exist_ok=True)
    manifest=json.loads((P/'INHERITANCE.json').read_text())
    for name,digest in manifest['unchanged_math_modules'].items():
        if sha(P/name)!=digest or sha(BASE/name)!=digest:raise RuntimeError('inherited source mismatch: '+name)
    for name,repair in manifest['explicit_mathematical_source_repairs'].items():
        if sha(P/name)!=repair['after_sha256'] or sha(BASE/name)!=repair['before_sha256']:
            raise RuntimeError('unrecognized inherited source repair: '+name)
    if sha(BASE/'complete-development.pdf')!=manifest['predecessor_pdf_sha256']:
        raise RuntimeError('unrecognized predecessor PDF')
    checks={};negative=[]
    suites=[('v21','verify.py',['block-default','block-hazard','precision','capacity','physical-margin','clock','confidence','training-transport']),
            ('v20','verify_v20.py',['triangle','response','labels','profile','margin','clip'])]
    for name,script,mutants in suites:
        normal=command([sys.executable,script],capture_output=True).stdout
        optimized=command([sys.executable,'-O',script],capture_output=True).stdout
        if json.loads(normal)!=json.loads(optimized):raise RuntimeError('optimization changed '+name)
        checks[name]=json.loads(normal)
        (E/(name.upper()+'_FINITE_CHECKS.json')).write_text(normal)
        for opt in [[],['-O']]:
            for mutant in mutants:
                run=subprocess.run([sys.executable,*opt,script,'--mutant',mutant],cwd=P,text=True,capture_output=True)
                if run.returncode==0:raise RuntimeError('undetected mutant: '+name+'/'+mutant)
                negative.append({'suite':name,'mode':'optimized' if opt else 'normal','mutant':mutant,'detected':True,'last_error':run.stderr.splitlines()[-1]})
        print('Verified diagnostics and negative controls: '+name,file=sys.stderr,flush=True)
    (E/'NEGATIVE_CONTROLS.json').write_text(json.dumps(negative,indent=2)+'\n')
    env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1790208000';env['FORCE_SOURCE_DATE']='1'
    for turn in range(3):
        with (E/f'LATEX_PASS_{turn+1}.txt').open('w') as log:
            command(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],stdout=log,stderr=subprocess.STDOUT,env=env)
    log=(P/'main.log').read_text(errors='replace')
    forbidden=['Overfull \\hbox','Overfull \\vbox','There were undefined references','multiply defined','LaTeX Warning: Reference','LaTeX Warning: Citation']
    if any(x in log for x in forbidden):raise RuntimeError('typesetting defects: '+repr([x for x in forbidden if x in log]))
    shutil.copyfile(P/'main.pdf',P/'paper.pdf')
    article=fitz.open(P/'paper.pdf');old=fitz.open(BASE/'complete-development.pdf')
    if len(old)!=400:raise RuntimeError('expected complete 400-page predecessor')
    combined=fitz.open();combined.insert_pdf(article);combined.insert_pdf(old)
    combined.set_metadata({'title':'General Theta Foundations I: complete preserved development, v21','author':'Qian Qi'})
    out=P/'complete-development.pdf'
    if out.exists():out.unlink()
    combined.save(out,garbage=4,deflate=True);combined.close();combined=fitz.open(out)
    equality=[]
    for i in range(len(old)):
        a,b=old[i],combined[len(article)+i]
        same_text=a.get_text()==b.get_text()
        same_raster=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples==b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples
        if not same_text or not same_raster:raise RuntimeError('predecessor page changed: '+str(i+1))
        equality.append({'old_page':i+1,'new_page':len(article)+i+1,'text_equal':same_text,'raster_equal':same_raster})
        if (i+1)%50==0:print(f'Preserved {i+1}/400 predecessor pages',file=sys.stderr,flush=True)
    (E/'PRESERVED_PAGES.json').write_text(json.dumps(equality,indent=2)+'\n')
    aux=(P/'main.aux').read_text()
    labels={m.group(1):{'number':m.group(2),'page':int(m.group(3))} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',aux)}
    (E/'THEOREM_LOCATIONS.json').write_text(json.dumps({k:v for k,v in labels.items() if ':v21-' in k},indent=2,sort_keys=True)+'\n')
    source_hashes={f.name:sha(f) for f in sorted(P.iterdir()) if f.suffix in {'.tex','.md','.json','.py','.txt'}}
    canonical_hashes={f.name:sha(f) for f in sorted(P.glob('*.tex'))}
    receipt={'schema':'gtf21.build-receipt/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-source-snapshot'),
      'review_commit':manifest['review_commit'],'base_commit':manifest['base_commit'],'workflow_run':os.environ.get('GITHUB_RUN_ID'),
      'canonical_pages':len(article),'predecessor_pages':len(old),'complete_pages':len(combined),
      'all_predecessor_pages_text_and_raster_equal':True,'unchanged_math_modules_verified':len(manifest['unchanged_math_modules']),
      'canonical_sources_sha256':hashlib.sha256(json.dumps(canonical_hashes,sort_keys=True).encode()).hexdigest(),
      'source_hashes':source_hashes,'pdf_sha256':sha(P/'paper.pdf'),'complete_pdf_sha256':sha(out),
      'finite_diagnostic_checks':sum(x['checks'] for x in checks.values()),'new_finite_diagnostic_checks':checks['v21']['checks'],
      'inherited_finite_diagnostic_checks':checks['v20']['checks'],'normal_optimized_equal':True,'negative_control_executions':len(negative),
      'undefined_references':False,'overfull_boxes':False,'analytic_proofs_independently_verified':False,
      'general_end_to_end_bound':'kappa <= W <= W_rational <= 12*d*kappa; separately priced external clock',
      'physical_peak_interval':[3,12],'physical_exact_peak_optimum_asserted':False,
      'original_norberg_proof_crosswalk':'incomplete: original full proof text not obtained',
      'old_repository_paths_modified':[],'old_repository_paths_deleted':[],'fonts_distributed':False}
    (E/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    with zipfile.ZipFile(E/'SUBMISSION_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(P.iterdir()):
            if f.suffix in {'.tex','.md','.json','.py','.txt'}:z.write(f,P.name+'/'+f.name)
        z.write(BASE/'complete-development.pdf',BASE.name+'/complete-development.pdf')
        for name in sorted(set(manifest['unchanged_math_modules'])|set(manifest['explicit_mathematical_source_repairs'])):
            z.write(BASE/name,BASE.name+'/'+name)
    print(json.dumps({k:v for k,v in receipt.items() if k!='source_hashes'},indent=2))
    for ext in ['aux','log','out','toc','pdf']:
        f=P/('main.'+ext)
        if f.exists():f.unlink()

if __name__=='__main__':main()
