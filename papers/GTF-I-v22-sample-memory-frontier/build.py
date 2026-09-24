#!/usr/bin/env python3
"""Build v22 and verify its full source and 472-page predecessor preservation."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,zipfile
from pathlib import Path
import fitz
P=Path(__file__).resolve().parent
BASE=Path(os.environ.get('GTF_PREDECESSOR_DIR',str(P.parent/'GTF-I-v21-multicut-resources'))).resolve()

def sha(p:Path)->str:return hashlib.sha256(p.read_bytes()).hexdigest()
def execute(args:list[str],**kw):return subprocess.run(args,cwd=P,check=True,text=True,**kw)

def main():
    E=P/'evidence';E.mkdir(exist_ok=True)
    manifest=json.loads((P/'INHERITANCE.json').read_text())
    for name,digest in manifest['unchanged_math_modules'].items():
        if sha(P/name)!=digest or sha(BASE/name)!=digest:raise RuntimeError('inherited module mismatch: '+name)
    for name,digest in manifest['archived_frontmatter_sources'].items():
        if sha(P/'history'/name)!=digest:raise RuntimeError('archived source mismatch: '+name)
    visited=set();pending=['main.tex']
    while pending:
        name=pending.pop()
        if name in visited:continue
        visited.add(name)
        text=(P/name).read_text()
        pending.extend(x+'.tex' for x in re.findall(r'\\input\{([^}]+)\}',text))
    if not set(manifest['unchanged_math_modules']).issubset(visited):
        raise RuntimeError('an inherited mathematical module is not included in the article')
    old_intro=(P/'history/introduction-v21.tex').read_text()
    start=old_intro.index('\\begin{theorem}');end=old_intro.index('\\end{proof}',start)+len('\\end{proof}')
    if old_intro[start:end] not in (P/'v21-organizing-theorem.tex').read_text():
        raise RuntimeError('v21 organizing theorem or proof was changed')
    old_bib=(P/'history/references-main-v21.tex').read_text().split('\\end{thebibliography}')[0]
    if not (P/'references-main.tex').read_text().startswith(old_bib):
        raise RuntimeError('an inherited bibliography entry was changed')
    if sha(BASE/'complete-development.pdf')!=manifest['predecessor_pdf_sha256']:
        raise RuntimeError('unrecognized predecessor PDF')
    suites=[('v22','verify.py',['walk-absorption','walk-time','revelation-prior','revelation-bottleneck','frontier-rounding','active-budget','confidence-gap','physical-buffer']),
       ('v21','verify_v21.py',['block-default','block-hazard','precision','capacity','physical-margin','clock','confidence','training-transport']),
       ('v20','verify_v20.py',['triangle','response','labels','profile','margin','clip'])]
    results={};negative=[]
    for label,script,mutants in suites:
        normal=execute([sys.executable,script],capture_output=True).stdout
        optimized=execute([sys.executable,'-O',script],capture_output=True).stdout
        if json.loads(normal)!=json.loads(optimized):raise RuntimeError('optimization mismatch: '+label)
        results[label]=json.loads(normal);(E/(label.upper()+'_FINITE_CHECKS.json')).write_text(normal)
        for opt in [[],['-O']]:
            for mutant in mutants:
                run=subprocess.run([sys.executable,*opt,script,'--mutant',mutant],cwd=P,text=True,capture_output=True)
                if run.returncode==0:raise RuntimeError('undetected mutant: '+label+'/'+mutant)
                negative.append({'suite':label,'mode':'optimized' if opt else 'normal','mutant':mutant,'detected':True,'last_error':run.stderr.splitlines()[-1]})
        print('Passed suite and negative controls: '+label,file=sys.stderr,flush=True)
    (E/'NEGATIVE_CONTROLS.json').write_text(json.dumps(negative,indent=2)+'\n')
    env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790208000',FORCE_SOURCE_DATE='1')
    for i in range(3):
        with (E/f'LATEX_PASS_{i+1}.txt').open('w') as out:
            execute(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],stdout=out,stderr=subprocess.STDOUT,env=env)
    log=(P/'main.log').read_text(errors='replace')
    bad=[s for s in ['Overfull \\hbox','Overfull \\vbox','There were undefined references','multiply defined','LaTeX Warning: Reference','LaTeX Warning: Citation'] if s in log]
    if bad:raise RuntimeError('typesetting defects: '+repr(bad))
    shutil.copyfile(P/'main.pdf',P/'paper.pdf')
    article=fitz.open(P/'paper.pdf');old=fitz.open(BASE/'complete-development.pdf')
    if len(old)!=472:raise RuntimeError('expected 472 predecessor pages')
    joined=fitz.open();joined.insert_pdf(article);joined.insert_pdf(old)
    joined.set_metadata({'title':'General Theta Foundations I: complete preserved development, v22','author':'Qian Qi'})
    out=P/'complete-development.pdf'
    if out.exists():out.unlink()
    joined.save(out,garbage=4,deflate=True);joined.close();joined=fitz.open(out)
    preservation=[]
    for i in range(len(old)):
        a,b=old[i],joined[len(article)+i]
        text=a.get_text()==b.get_text()
        raster=a.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples==b.get_pixmap(matrix=fitz.Matrix(1,1),alpha=False).samples
        if not text or not raster:raise RuntimeError('changed predecessor page: '+str(i+1))
        preservation.append({'old_page':i+1,'new_page':len(article)+i+1,'text_equal':text,'raster_equal':raster})
        if (i+1)%100==0:print(f'Preserved {i+1}/472 pages',file=sys.stderr,flush=True)
    (E/'PRESERVED_PAGES.json').write_text(json.dumps(preservation,indent=2)+'\n')
    aux=(P/'main.aux').read_text()
    labels={m.group(1):{'number':m.group(2),'page':int(m.group(3))} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',aux)}
    (E/'THEOREM_LOCATIONS.json').write_text(json.dumps({k:v for k,v in labels.items() if ':v22-' in k},indent=2,sort_keys=True)+'\n')
    sourcefiles=[f for f in sorted(P.rglob('*')) if f.is_file() and f.suffix in {'.tex','.md','.json','.py'} and 'evidence' not in f.parts and 'bootstrap' not in f.parts]
    hashes={f.relative_to(P).as_posix():sha(f) for f in sourcefiles}
    canonical={f.name:sha(f) for f in sorted(P.glob('*.tex'))}
    (E/'SOURCE_HASHES.json').write_text(json.dumps(hashes,indent=2,sort_keys=True)+'\n')
    receipt={'schema':'gtf22.build-receipt/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-source-snapshot'),
      'base_commit':manifest['base_commit'],'review_commit':manifest['review_commit'],'workflow_run':os.environ.get('GITHUB_RUN_ID'),
      'canonical_pages':len(article),'predecessor_pages':len(old),'complete_pages':len(joined),
      'all_predecessor_pages_text_and_raster_equal':True,'unchanged_math_modules_verified':len(manifest['unchanged_math_modules']),'all_inherited_math_modules_in_canonical':True,'v21_organizing_statement_and_proof_preserved':True,
      'canonical_sources_sha256':hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest(),
      'pdf_sha256':sha(P/'paper.pdf'),'complete_pdf_sha256':sha(out),'source_hashes_file':'evidence/SOURCE_HASHES.json',
      'finite_diagnostic_checks':sum(r['checks'] for r in results.values()),'new_finite_diagnostic_checks':results['v22']['checks'],
      'exhaustive_transition_tables_evaluated':results['v22']['exhaustive_transition_tables_evaluated'],
      'normal_optimized_equal':True,'negative_control_executions':len(negative),'undefined_references':False,'overfull_boxes':False,
      'analytic_proofs_independently_verified':False,'exact_frontier_scope':'Bayesian erasure-revelation experiments, arbitrary fixed prior and cut profile, all stochastic machines',
      'physical_resource_points':[[399,40602],[320000,1604],['12800*2^400',12]],'physical_exact_peak_optimum_asserted':False,
      'original_norberg_proof_crosswalk':'incomplete; no original proof text obtained','old_repository_paths_modified':[],
      'old_repository_paths_deleted':[],'fonts_distributed':False}
    (E/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
    with zipfile.ZipFile(E/'SUBMISSION_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in sourcefiles:z.write(f,P.name+'/'+f.relative_to(P).as_posix())
        z.write(BASE/'complete-development.pdf','GTF-I-v21-multicut-resources/complete-development.pdf')
        for name in manifest['unchanged_math_modules']:z.write(BASE/name,'GTF-I-v21-multicut-resources/'+name)
    # Selected mathematical pages are rendered for human visual inspection.
    R=E/'renders';R.mkdir(exist_ok=True)
    selected={0}
    for key in ['thm:v22-tournament','thm:v22-revelation','thm:v22-active','thm:v22-physical','thm:v22-confidence']:
        selected.add(labels[key]['page']-1)
    for index in sorted(selected):article[index].get_pixmap(matrix=fitz.Matrix(1.25,1.25),alpha=False).save(R/f'page-{index+1:03d}.png')
    print(json.dumps(receipt,indent=2),flush=True)
    for ext in ['aux','log','out','toc','pdf']:
        f=P/('main.'+ext)
        if f.exists():f.unlink()

if __name__=='__main__':main()
