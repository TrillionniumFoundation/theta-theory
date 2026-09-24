#!/usr/bin/env python3
"""Build v23; check actual inheritance, exact diagnostics and PDF preservation."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,zipfile
from pathlib import Path
import fitz
P=Path(__file__).resolve().parent
BASE=Path(os.environ.get('GTF_PREDECESSOR_DIR',str(P.parent/'GTF-I-v22-sample-memory-frontier'))).resolve()
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,**kw):return subprocess.run(args,cwd=P,check=True,text=True,**kw)
def main():
 E=P/'evidence';E.mkdir(exist_ok=True)
 m=json.loads((P/'INHERITANCE.json').read_text())
 for n,h in m['unchanged_math_modules'].items():
  if sha(P/n)!=h or sha(BASE/n)!=h:raise RuntimeError('inherited module: '+n)
 for n,h in m['archived_v22_sources'].items():
  if sha(P/'history/v22'/n)!=h:raise RuntimeError('archived source: '+n)
 if sha(P/'HISTORICAL_PIPELINE_V20.json')!=m['historical_graph_sha256']:raise RuntimeError('historical graph changed')
 visited=set();pending=['main.tex']
 while pending:
  n=pending.pop()
  if n in visited:continue
  visited.add(n);pending += [a+'.tex' for a in re.findall(r'\\input\{([^}]+)\}',(P/n).read_text())]
 if not set(m['unchanged_math_modules']).issubset(visited):raise RuntimeError('missing inherited canonical module')
 old=(BASE/'introduction.tex').read_text();i=old.index('\\begin{theorem}');j=old.index('\\end{proof}',i)+len('\\end{proof}')
 if old[i:j] not in (P/'v22-organizing-theorem.tex').read_text():raise RuntimeError('v22 organizing proof changed')
 oldbib=(BASE/'references-main.tex').read_text().split('\\end{thebibliography}')[0]
 if not (P/'references-main.tex').read_text().startswith(oldbib):raise RuntimeError('old bibliography changed')
 if sha(BASE/'complete-development.pdf')!=m['predecessor_pdf_sha256']:raise RuntimeError('predecessor PDF changed')
 suites=[('v23','verify_v23.py',['minimax-as-bayes','wrong-terminal-denominator','drop-minors','shared-row-free','unpriced-calibration','fair-bit-exact','wrong-roc-order']),('v22','verify.py',['walk-absorption','walk-time','revelation-prior','revelation-bottleneck','frontier-rounding','active-budget','confidence-gap','physical-buffer']),('v21','verify_v21.py',['block-default','block-hazard','precision','capacity','physical-margin','clock','confidence','training-transport']),('v20','verify_v20.py',['triangle','response','labels','profile','margin','clip'])]
 results={};negative=[]
 for label,script,mutants in suites:
  a=run([sys.executable,script],capture_output=True).stdout;b=run([sys.executable,'-O',script],capture_output=True).stdout
  if json.loads(a)!=json.loads(b):raise RuntimeError('optimized mismatch: '+label)
  results[label]=json.loads(a);(E/(label.upper()+'_FINITE_CHECKS.json')).write_text(a)
  for opt in [[],['-O']]:
   for mutant in mutants:
    r=subprocess.run([sys.executable,*opt,script,'--mutant',mutant],cwd=P,text=True,capture_output=True)
    if r.returncode==0:raise RuntimeError('undetected mutant: '+mutant)
    negative.append({'suite':label,'mode':'optimized' if opt else 'normal','mutant':mutant,'detected':True,'last_error':r.stderr.splitlines()[-1]})
  print('Passed '+label,flush=True)
 (E/'NEGATIVE_CONTROLS.json').write_text(json.dumps(negative,indent=2)+'\n')
 env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790208000',FORCE_SOURCE_DATE='1')
 for i in range(3):
  with (E/f'LATEX_PASS_{i+1}.txt').open('w') as out:run(['pdflatex','-interaction=nonstopmode','-halt-on-error','main.tex'],stdout=out,stderr=subprocess.STDOUT,env=env)
 log=(P/'main.log').read_text(errors='replace')
 defects=[x for x in ['Overfull \\hbox','Overfull \\vbox','There were undefined references','multiply defined','LaTeX Warning: Reference','LaTeX Warning: Citation'] if x in log]
 if defects:raise RuntimeError('typesetting: '+repr(defects))
 shutil.copyfile(P/'main.pdf',P/'paper.pdf');article=fitz.open(P/'paper.pdf');old=fitz.open(BASE/'complete-development.pdf')
 if len(old)!=553:raise RuntimeError('expected 553 predecessor pages')
 joined=fitz.open();joined.insert_pdf(article);joined.insert_pdf(old);joined.set_metadata({'title':'General Theta Foundations I: complete preserved development, v23','author':'Qian Qi'})
 out=P/'complete-development.pdf'
 if out.exists():out.unlink()
 joined.save(out,garbage=4,deflate=True);joined.close();joined=fitz.open(out)
 preserved=[]
 for i in range(len(old)):
  a,b=old[i],joined[len(article)+i]
  t=a.get_text()==b.get_text();r=a.get_pixmap(alpha=False).samples==b.get_pixmap(alpha=False).samples
  if not(t and r):raise RuntimeError('changed predecessor page '+str(i+1))
  preserved.append({'old_page':i+1,'new_page':len(article)+i+1,'text_equal':t,'raster_equal':r})
 (E/'PRESERVED_PAGES.json').write_text(json.dumps(preserved,indent=2)+'\n')
 labels={x.group(1):{'number':x.group(2),'page':int(x.group(3))} for x in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',(P/'main.aux').read_text())}
 (E/'THEOREM_LOCATIONS.json').write_text(json.dumps({k:v for k,v in labels.items() if ':v23-' in k},indent=2,sort_keys=True)+'\n')
 files=[f for f in sorted(P.rglob('*')) if f.is_file() and f.suffix in {'.tex','.md','.json','.py'} and 'evidence' not in f.relative_to(P).parts]
 hashes={f.relative_to(P).as_posix():sha(f) for f in files}
 (E/'SOURCE_HASHES.json').write_text(json.dumps(hashes,indent=2,sort_keys=True)+'\n')
 canonical={f.name:sha(f) for f in sorted(P.glob('*.tex'))}
 receipt={'schema':'gtf23.build-receipt/1','source_commit':os.environ.get('GTF_SOURCE_COMMIT','local-source-snapshot'),'review_commit':m['review_commit'],'base_commit':m['base_commit'],'workflow_run':os.environ.get('GITHUB_RUN_ID'),'canonical_pages':len(article),'predecessor_pages':len(old),'complete_pages':len(joined),'all_predecessor_pages_text_and_raster_equal':True,'unchanged_math_modules_verified':len(m['unchanged_math_modules']),'all_inherited_math_modules_in_canonical':True,'v22_organizing_statement_and_proof_preserved':True,'canonical_sources_sha256':hashlib.sha256(json.dumps(canonical,sort_keys=True).encode()).hexdigest(),'pdf_sha256':sha(P/'paper.pdf'),'complete_pdf_sha256':sha(out),'finite_diagnostic_checks':sum(v['checks'] for v in results.values()),'new_finite_diagnostic_checks':results['v23']['checks'],'normal_optimized_equal':True,'negative_control_executions':len(negative),'undefined_references':False,'overfull_boxes':False,'analytic_proofs_independently_verified':False,'new_exact_frontier':'noisy Bayes profiles; arbitrary-horizon uncontrolled binary-register minimax; closed all-profile three-report Bayes/minimax','stochastic_grid_is_continuum_proof':False,'physical_fixed_sample_pareto_evaluated':False,'norberg_original_proof_comparison':'incomplete; original proof not obtained','old_repository_paths_modified':[],'old_repository_paths_deleted':[],'fonts_distributed':False}
 (E/'BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
 dirname='GTF-I-v23-compatible-frontiers'
 with zipfile.ZipFile(E/'SUBMISSION_SOURCES.zip','w',zipfile.ZIP_DEFLATED) as z:
  for f in files:z.write(f,dirname+'/'+f.relative_to(P).as_posix())
  required=set(m['unchanged_math_modules'])|{'complete-development.pdf','introduction.tex','references-main.tex'}
  for n in sorted(required):z.write(BASE/n,'GTF-I-v22-sample-memory-frontier/'+n)
 R=E/'renders';R.mkdir(exist_ok=True);selected={0}
 for k in ['thm:v23-occupation','thm:v23-dual','thm:v23-interval','thm:v23-minimax-recursion','thm:v23-bsc','eq:v23-gap-certificate','thm:v23-calibration','cor:v23-confidence']:selected.add(labels[k]['page']-1)
 for i in sorted(selected):article[i].get_pixmap(matrix=fitz.Matrix(1.2,1.2),alpha=False).save(R/f'page-{i+1:03d}.png')
 print(json.dumps(receipt,indent=2),flush=True)
 for ext in ['aux','log','out','toc','pdf']:
  f=P/('main.'+ext)
  if f.exists():f.unlink()
if __name__=='__main__':main()
