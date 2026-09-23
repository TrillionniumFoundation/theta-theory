#!/usr/bin/env python3
"""Publish a source-bound reproducibility record; never an analytic certificate."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
import fitz
P=Path(__file__).resolve().parent; ROOT=P.parents[1]
OLD=P.parent/'GTF-I-v18-continuation-transport'; E=P/'evidence'
BASE='e7d020c49959009a775081ea9aa70c7e7fec5d52'
OLDPDF='f4a0c5d719b679bdb7d44111ddc3e9e36158744907b086448e0800900504cf7a'
MUTANTS=('majority_off_by_one','likelihood_margin','counter_clip','insufficient_training','unpriced_transcript','backward_coefficient')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def need(ok,message):
 if not ok:raise RuntimeError(message)
def dump(p,value):Path(p).write_text(json.dumps(value,indent=2,ensure_ascii=False)+'\n')
def run(args,cwd=P,required=True,env=None):
 out=subprocess.run(list(map(str,args)),cwd=cwd,env=env,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
 if required and out.returncode:raise RuntimeError(str(args)+'\n'+out.stdout[-10000:])
 return out

def main():
 E.mkdir(exist_ok=True)
 manuscript=''.join(f.name+' '+sha(f)+'\n' for f in sorted(P.glob('*.tex')))
 manuscript_hash=hashlib.sha256(manuscript.encode()).hexdigest()
 need(manuscript_hash=='fa27a4e69e6c854b7db6434cdb326a20d71aefb1aca3e1a2c70e7de93f9ff67d','Canonical source differs from inspected local manuscript')
 source=run(['git','rev-parse','HEAD'],ROOT,False)
 commit=source.stdout.strip() if source.returncode==0 else None
 if os.getenv('GITHUB_ACTIONS')=='true':need(commit==os.getenv('GTF_SOURCE_COMMIT') and bool(commit),'Source commit mismatch')
 preservation=json.loads((P/'PRESERVATION_MAP.json').read_text())
 for row in preservation['files']:
  need(sha(ROOT/row['source'])==row['source_sha256'],'Inherited source changed: '+row['source'])
  if row['canonical_copy']:need(sha(P/row['canonical_copy'])==row['source_sha256'],'Canonical copy differs')
 need(sha(OLD/'complete-development.pdf')==OLDPDF,'Pinned predecessor PDF differs')
 graph=json.loads((P/'PIPELINE_STATUS.json').read_text())
 need(graph['inherited_v18_graph']==json.loads((OLD/'PIPELINE_GRAPH.json').read_text()),'Inherited pipeline graph altered')
 need(graph['current_credit']['A2_primary_chain']=='independent_not_consumed','Invented A2 dependency')
 need(not graph['current_credit']['full_historical_program_closed_by_gtf_v19'],'Unjustified global closure')
 normal=run([sys.executable,P/'verify.py']).stdout
 optimized=run([sys.executable,'-O',P/'verify.py']).stdout
 need(json.loads(normal)==json.loads(optimized),'Optimization changes diagnostics')
 (E/'DIAGNOSTICS.json').write_text(normal)
 negative=[]
 for flags in ([],['-O']):
  for mutant in MUTANTS:
   out=run([sys.executable,*flags,P/'verify.py','--mutant',mutant],required=False)
   need(out.returncode!=0 and 'FAILED:' in out.stdout and 'unknown or surviving' not in out.stdout,'Negative control survived: '+mutant)
   negative.append({'mutant':mutant,'mode':'optimized' if flags else 'ordinary','returncode':out.returncode,'last_line':out.stdout.splitlines()[-1]})
 dump(E/'NEGATIVE_CONTROLS.json',negative)
 inherited=[]
 for name in ('GTF-I-v18-continuation-transport','GTF-I-v17-intrinsic-adaptive-testing'):
  script=P.parent/name/'verify.py';out=run([sys.executable,script],script.parent)
  dest=E/(name+'-diagnostics.txt');dest.write_text(out.stdout)
  inherited.append({'source':str(script.relative_to(ROOT)),'returncode':out.returncode,'log_sha256':sha(dest)})
 env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790121600',FORCE_SOURCE_DATE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
 compiler=run(['pdflatex','--version']).stdout.splitlines()[0]
 with tempfile.TemporaryDirectory(prefix='gtf19-') as work:
  w=Path(work);previous=None
  for passes in range(1,7):
   run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory',w,'main.tex'],env=env)
   aux=(w/'main.aux').read_bytes()
   if passes>=3 and aux==previous:break
   previous=aux
  else:raise RuntimeError('Cross-references did not stabilize')
  log=(w/'main.log').read_text(errors='replace')
  for pattern in (r'Overfull \\[hv]box',r'There were undefined references',r'LaTeX Warning: (Reference|Citation).*undefined',r'multiply defined'):
   need(not re.search(pattern,log),'Typesetting error: '+pattern)
  shutil.copy2(w/'main.pdf',P/'paper.pdf');shutil.copy2(w/'main.log',E/'LATEX.log')
  labels={m.group(1):{'number':m.group(2),'page':int(m.group(3))}for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',(w/'main.aux').read_text())}
 dump(E/'THEOREM_LOCATIONS.json',labels)
 dependencies={'thm:v19-main':['thm:v19-residual','thm:v19-binarywidth','thm:v19-composition'],'thm:v19-residual':['thm:v18-continuation'],'thm:v19-binarywidth':['thm:v19-residual','thm:v18-auditlower'],'lem:v19-posterior':[],'thm:v19-global':['lem:v19-posterior','thm:v18-gaussian','thm:v18-entropic'],'lem:v19-counter':['thm:v18-continuation','thm:v17-markedgap'],'thm:v19-composition':['lem:v19-counter','thm:v18-microscopic','thm:v19-global']}
 old_status=json.loads((OLD/'PROOF_STATUS.json').read_text())
 old_rows={r['id']:r for r in old_status['statements']}
 statements=[]
 for file in sorted(P.glob('*.tex')):
  text=file.read_text()
  for match in re.finditer(r'\\begin\{(theorem|lemma|proposition|corollary|definition|example)\}.*?\\end\{\1\}',text,re.S):
   body=match.group();identifier=re.search(r'\\label\{([^}]+)\}',body)
   if not identifier:continue
   identifier=identifier.group(1);need(identifier in labels,'Unresolved statement '+identifier)
   row={'id':identifier,'source_file':file.name,'source_sha256':sha(file),'statement_sha256':hashlib.sha256(body.encode()).hexdigest(),'source_commit':commit,'compiled_location':labels[identifier],'version_credit':'new_v19' if identifier.startswith(('thm:v19','lem:v19','prop:v19','cor:v19'))else 'inherited','current_status':('definition_stated' if match.group(1)=='definition' else 'example_argument_supplied' if match.group(1)=='example' else 'proof_supplied_in_manuscript'),'review_status':'independent_review_pending' if ':v19-' in identifier else 'inherited_status_not_upgraded_by_reproduction','upstream_dependencies':dependencies.get(identifier,old_rows.get(identifier,{}).get('upstream_dependencies',[]))}
   if identifier in old_rows:row['inherited_status_record']=old_rows[identifier]
   statements.append(row)
 need(len({r['id']for r in statements})==len(statements),'Duplicate statement identity')
 status={'schema':'gtf.statement-status/2','edition':'v19','source_commit':commit,'statements':statements,'scope':'Statement identity and declared status, not analytic verification.'}
 dump(P/'PROOF_STATUS.json',status);dump(E/'BOUND_PROOF_STATUS.json',status)
 paper=fitz.open(P/'paper.pdf');old=fitz.open(OLD/'complete-development.pdf');need(len(old)==294,'Unexpected predecessor page count')
 full=fitz.open();full.insert_pdf(paper);offset=len(paper);full.insert_pdf(old)
 full.set_toc(paper.get_toc()+[[1,'Unchanged v18 complete development',offset+1]]+[[a+1,b,c+offset]for a,b,c in old.get_toc()])
 full.set_metadata({'title':'General Theta Foundations I v19 — complete development','author':'Qian Qi','subject':'Canonical v19 article and unchanged v18 historical development'})
 full.save(P/'complete-development.pdf',garbage=4,deflate=True);full.close();full=fitz.open(P/'complete-development.pdf')
 for i,page in enumerate(old):
  other=full[offset+i]
  need(page.get_text()==other.get_text(),'Predecessor text changed at page '+str(i+1))
  need(page.get_pixmap(matrix=fitz.Matrix(.35,.35),alpha=False).samples==other.get_pixmap(matrix=fitz.Matrix(.35,.35),alpha=False).samples,'Predecessor raster changed at page '+str(i+1))
 geometry=[]
 for i,page in enumerate(paper):
  bad=[b[:4]for b in page.get_text('blocks')if b[6]==0 and(b[0]<-1 or b[1]<-1 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1)]
  need(not bad,'Text outside page '+str(i+1));geometry.append({'page':i+1,'inside_page':True})
 dump(E/'PAGE_CHECK.json',{'canonical':geometry,'inherited_text_and_raster_equal_pages':294,'raster_scale':.35,'scope':'Automated geometry and page preservation; visual review recorded separately.'})
 def archive(dest,files):
  with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9)as z:
   for name,path in sorted(files.items()):
    need(path.suffix.lower()not in {'.ttf','.otf','.pfb','.woff','.woff2'},'Font file forbidden')
    info=zipfile.ZipInfo(name,(2026,9,23,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16;z.writestr(info,path.read_bytes())
 archive(E/'SUBMISSION_SOURCES.zip',{f.name:f for f in P.glob('*.tex')}|{'README.md':P/'README.md'})
 closure={}
 for folder in P.parent.glob('GTF-I-*'):
  for file in folder.rglob('*'):
   if file.is_file()and'evidence'not in file.parts and file.suffix in {'.tex','.py','.md','.json','.txt'}:
    closure[str(file.relative_to(ROOT))]=file
 closure[str((OLD/'complete-development.pdf').relative_to(ROOT))]=OLD/'complete-development.pdf'
 archive(E/'COMPILED_SOURCES.zip',closure)
 artifacts={name:{'sha256':sha(P/name),'bytes':(P/name).stat().st_size}for name in ('paper.pdf','complete-development.pdf','evidence/SUBMISSION_SOURCES.zip','evidence/COMPILED_SOURCES.zip')}
 receipt={'schema':'gtf.v19.build-receipt/1','source_commit':commit,'base_commit':BASE,'canonical_sources_sha256':manuscript_hash,'controlling_review_commit':'a94ec98d6e33d9719f72deec160f5c8270ce006f','workflow_run':os.getenv('GITHUB_RUN_ID'),'compiler':compiler,'passes':passes,'canonical_pages':len(paper),'complete_pages':len(full),'inherited_pages_verified':294,'finite_checks':json.loads(normal)['total'],'normal_optimized_equal':True,'negative_control_executions':len(negative),'inherited_diagnostic_runs':inherited,'statements':len(statements),'resolved_labels':len(labels),'artifacts':artifacts,'analytic_proofs_independently_certified':False,'norberg_original_proof_audit':'unverified','new_theorem_review':'pending','fonts_distributed':False}
 dump(E/'BUILD_RECEIPT.json',receipt)
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
