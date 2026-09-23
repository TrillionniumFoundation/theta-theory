#!/usr/bin/env python3
"""Build the complete v20 article; append and verify every predecessor page."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,zipfile
from pathlib import Path
import fitz
P=Path(__file__).resolve().parent
BASE=P.parent/'GTF-I-v19-referee-resolution'
REVIEW='01679f4eac720dfd256594333e577b5db8145246'
BASE_PDF_SHA='479c27d73c280429c00288ba3c51a2c8cafafbda9a06dbf44fa78467ca709221'

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def command(args:list[str],**kwargs):
    return subprocess.run(args,cwd=P,check=True,text=True,**kwargs)

def main():
    evidence=P/'evidence';evidence.mkdir(exist_ok=True)
    manifest=json.loads((P/'INHERITANCE.json').read_text())
    for name,digest in manifest['unchanged_math_modules'].items():
        if sha(P/name)!=digest or sha(BASE/name)!=digest:
            raise RuntimeError('inherited source mismatch: '+name)
    if sha(BASE/'complete-development.pdf')!=BASE_PDF_SHA:
        raise RuntimeError('unrecognized predecessor PDF')
    normal=command([sys.executable,'verify.py'],capture_output=True).stdout
    optimized=command([sys.executable,'-O','verify.py'],capture_output=True).stdout
    if json.loads(normal)!=json.loads(optimized):raise RuntimeError('optimized diagnostics changed')
    (evidence/'FINITE_CHECKS.json').write_text(normal)
    negative=[]
    for opt in [[],['-O']]:
        for mutant in ['triangle','response','labels','profile','margin','clip']:
            run=subprocess.run([sys.executable,*opt,'verify.py','--mutant',mutant],cwd=P,text=True,capture_output=True)
            if run.returncode==0:raise RuntimeError('undetected mutant: '+mutant)
            negative.append({'mode':'optimized' if opt else 'normal','mutant':mutant,'detected':True,
                             'last_error':run.stderr.splitlines()[-1]})
    (evidence/'NEGATIVE_CONTROLS.json').write_text(json.dumps(negative,indent=2)+'\n')
    env=os.environ.copy();env['SOURCE_DATE_EPOCH']='1790121600';env['FORCE_SOURCE_DATE']='1'
    for turn in range(3):
        with (evidence/f'LATEX_PASS_{turn+1}.txt').open('w') as log:
            command(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],stdout=log,stderr=subprocess.STDOUT,env=env)
    log=(P/'main.log').read_text(errors='replace')
    forbidden=['Overfull \\hbox','Overfull \\vbox','There were undefined references','multiply defined','LaTeX Warning: Reference','LaTeX Warning: Citation']
    hits=[x for x in forbidden if x in log]
    if hits:raise RuntimeError('typesetting defects: '+repr(hits))
    shutil.copyfile(P/'main.pdf',P/'paper.pdf')
    article=fitz.open(P/'paper.pdf');old=fitz.open(BASE/'complete-development.pdf')
    complete=fitz.open();complete.insert_pdf(article);complete.insert_pdf(old)
    complete.set_metadata({'title':'General Theta Foundations I — complete preserved development, v20','author':'Qian Qi'})
    complete.save(P/'complete-development.pdf',garbage=4,deflate=True)
    combined=fitz.open(P/'complete-development.pdf')
    equality=[]
    for i in range(len(old)):
        a=old[i];b=combined[len(article)+i]
        same_text=a.get_text()==b.get_text()
        same_raster=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples==b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples
        if not same_text or not same_raster:raise RuntimeError(f'predecessor page changed: {i+1}')
        
        if (i+1)%50==0: print(f'Preserved {i+1}/{len(old)} predecessor pages',file=sys.stderr,flush=True)
        equality.append({'old_page':i+1,'new_page':len(article)+i+1,'text_equal':same_text,'raster_equal':same_raster})
    (evidence/'PRESERVED_PAGES.json').write_text(json.dumps(equality,indent=2)+'\n')
    aux=(P/'main.aux').read_text()
    labels={m.group(1):{'number':m.group(2),'page':int(m.group(3))} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',aux)}
    new_labels={k:v for k,v in labels.items() if ':v20-' in k}
    (evidence/'THEOREM_LOCATIONS.json').write_text(json.dumps(new_labels,indent=2,sort_keys=True)+'\n')
    sources={f.name:sha(f) for f in sorted(P.glob('*.tex'))}
    digest=hashlib.sha256(json.dumps(sources,sort_keys=True).encode()).hexdigest()
    receipt={'schema':'gtf20.build-receipt/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-source-snapshot'),
      'review_commit':REVIEW,'base_commit':'9cf70fe7c8aa289d1be26934451e223364aa06ef',
      'workflow_run':os.environ.get('GITHUB_RUN_ID'),'canonical_pages':len(article),
      'predecessor_pages':len(old),'complete_pages':len(combined),'all_predecessor_pages_text_and_raster_equal':True,
      'canonical_sources_sha256':digest,'source_hashes':sources,
      'pdf_sha256':sha(P/'paper.pdf'),'complete_pdf_sha256':sha(P/'complete-development.pdf'),
      'finite_diagnostic_checks':json.loads(normal)['checks'],'normal_optimized_equal':True,
      'negative_control_executions':len(negative),'undefined_references':False,'overfull_boxes':False,
      'analytic_proofs_independently_verified':False,'original_norberg_proof_crosswalk':'unverified: original full text not obtained',
      'all_algorithms_peak_memory_optimum':'not asserted; exact task optimum is at the designated decision cut',
      'fonts_distributed':False}
    (evidence/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    # A portable package with all current source and the frozen predecessor PDF.
    with zipfile.ZipFile(evidence/'SUBMISSION_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in sorted(P.iterdir()):
            if f.suffix in {'.tex','.md','.json','.py','.txt'}:z.write(f,'GTF-I-v20/'+f.name)
        z.write(BASE/'complete-development.pdf','GTF-I-v19-referee-resolution/complete-development.pdf')
        for name in manifest['unchanged_math_modules']:z.write(BASE/name,'GTF-I-v19-referee-resolution/'+name)
    print(json.dumps({k:v for k,v in receipt.items() if k!='source_hashes'},indent=2))
    # Build products retained only under explicit publication names.
    for ext in ['aux','log','out','toc','pdf']:
        f=P/('main.'+ext)
        if f.exists():f.unlink()

if __name__=='__main__':main()
