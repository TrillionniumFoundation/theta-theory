#!/usr/bin/env python3
"""Reproducible publication build. A receipt identifies evidence, not mathematical truth."""
from __future__ import annotations
import hashlib,json,os,re,shutil,subprocess,sys,tempfile,zipfile
from pathlib import Path
import fitz
P=Path(__file__).resolve().parent; R=P.parents[1]; OLD=P.parent/'GTF-I-v17-intrinsic-adaptive-testing'; E=P/'evidence'
REVIEW='a94ec98d6e33d9719f72deec160f5c8270ce006f'
OLDPDF='a17207665449f820f41d55fbc0d5bd979d56a1ebb3c5348e93fe06f4c3b95d0d'
NEW_MUTANTS=('resample_candidate','unpriced_erasure_memory','omit_innovation_shift','wrong_collision_modulus','insufficient_training','erase_preparation_mark')
OLD_MUTANTS=('negative_coefficient','wrong_adaptive_weight','convexify_private','hide_visible_seed','drop_actual_mark','erase_collision','omit_bayes_denominator','halve_presentation_error')
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def need(ok,msg):
 if not ok:raise RuntimeError(msg)
def dump(path,obj):Path(path).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def run(args,cwd=P,ok=True,env=None):
 print('RUN '+' '.join(map(str,args)),file=sys.stderr,flush=True)
 p=subprocess.run([str(a)for a in args],cwd=cwd,text=True,encoding='utf-8',errors='replace',stdout=subprocess.PIPE,stderr=subprocess.STDOUT,env=env)
 if ok and p.returncode:raise RuntimeError('Command failed: '+str(args)+'\n'+p.stdout[-10000:])
 return p

def main():
 E.mkdir(exist_ok=True)
 inherited=json.loads((P/'INHERITED_SOURCES.json').read_text())['files'];new=json.loads((P/'SOURCE_MANIFEST.json').read_text())['files']
 for rel,h in {**inherited,**new}.items():
  need((R/rel).is_file(),'Missing input '+rel);need(sha(R/rel)==h,'Changed input '+rel)
 need(sha(OLD/'complete-development.pdf')==OLDPDF,'Predecessor PDF changed')
 git=run(['git','rev-parse','HEAD'],R,False);source=git.stdout.strip() if git.returncode==0 else None
 if os.getenv('GITHUB_ACTIONS')=='true':need(source and source==os.getenv('GTF_SOURCE_COMMIT'),'Unpinned workflow source')
 if source:
  status=run(['git','status','--porcelain','--untracked-files=all'],R).stdout.splitlines()
  bad=[x for x in status if x[3:] in set(new)|set(inherited)]
  need(not bad,'Dirty source inputs: '+str(bad))
 pipeline=json.loads(run([sys.executable,P/'verify_pipeline.py']).stdout);dump(E/'PIPELINE_CONTRACT_CHECK.json',pipeline)
 reportchecks=[]
 if source:
  for blob,description in [('b1515103564c6c0de02b1751dad24ea23bee1f5f','controlling v17 r3 report'),('09646a80c6b6fc9f89a3e575d6e2dd2a832a200f','pipeline v17 r2 report'),('1e6c5a870ca1ecf3319c1f1d950a1f0f1564dfb4','historical B4 source'),('6fa8639339ebae9a19122cbdba339ec6f275b562','historical C2 source')]:
   out=run(['git','cat-file','-t',blob],R);need(out.stdout.strip()=='blob','Historical blob absent');reportchecks.append({'description':description,'blob':blob,'present':True})
 normal=run([sys.executable,P/'verify.py']).stdout;optimized=run([sys.executable,'-O',P/'verify.py']).stdout
 result=json.loads(normal);need(result==json.loads(optimized),'Optimized diagnostic mismatch');(E/'DIAGNOSTICS.json').write_text(normal)
 run([sys.executable,P/'verify.py','--write-certificates',E])
 negative=[]
 for script,variants in [(P/'verify.py',NEW_MUTANTS),(OLD/'verify.py',OLD_MUTANTS)]:
  for mode in ([],['-O']):
   for mutant in variants:
    out=run([sys.executable,*mode,script,'--mutant',mutant],script.parent,False)
    need(out.returncode!=0 and 'FAILED:' in out.stdout and 'survived' not in out.stdout,'Mutant not rejected: '+mutant)
    negative.append({'edition':'v18' if script.parent==P else 'v17','mode':'optimized' if mode else 'ordinary','mutant':mutant,'returncode':out.returncode,'message':out.stdout.strip()})
 dump(E/'NEGATIVE_CONTROLS.json',negative)
 inherited_runs=[]
 paths=[('v17',OLD/'verify.py'),('v16',P.parent/'GTF-I-v16-constructive-causal-certification/verify.py'),('v15',P.parent/'GTF-I-v15-certified-physical-comparison/verify.py'),('v14',P.parent/'GTF-I-v14-deficiency-certification/verify.py'),('v13',P.parent/'GTF-I-v13-intrinsic-deficiency/verify.py'),('v12',P.parent/'GTF-I-v12-causal-completion/verify.py'),('v11',P.parent/'GTF-I-v11-resource-comparison/verify.py'),('v10',P.parent/'GTF-I-v10-marked-duality/verify.py'),('v9',P.parent/'GTF-I-v9-causal-minimax/verify.py'),('v8',P.parent/'GTF-I-v8-decision-spectrum/verify.py'),('v7',P.parent/'GTF-I-v7-structural/verify.py'),('v6',P.parent/'GTF-I-v6-markov/verify.py'),('v5',P.parent/'GTF-I-v5-intrinsic/verify.py'),('v4',P.parent/'GTF-I-v4/verify.py'),('v3',P.parent/'GTF-I-v3/verify.py'),('v2',P.parent/'GTF-I-v2/verify.py'),('v1',P.parent/'GTF-I-v2/legacy/tools/verify.py')]
 for ed,script in paths:
  out=run([sys.executable,script],script.parent);dest=E/('INHERITED_'+ed.upper()+'.txt');dest.write_text(out.stdout)
  inherited_runs.append({'edition':ed,'returncode':out.returncode,'log_sha256':sha(dest)})
 # Canonical article built in a clean temporary output directory.
 env=os.environ.copy();env.update(SOURCE_DATE_EPOCH='1790121600',FORCE_SOURCE_DATE='1',OPENBLAS_NUM_THREADS='1',OMP_NUM_THREADS='1')
 compiler=run(['pdflatex','--version']).stdout.splitlines()[0]
 with tempfile.TemporaryDirectory(prefix='gtf18-typeset-') as work:
  work=Path(work); previous=None;passes=0
  for k in range(1,7):
   out=run(['pdflatex','-interaction=nonstopmode','-halt-on-error','-file-line-error','-recorder','-output-directory',work,'main.tex'],P,env=env);passes=k
   aux=(work/'main.aux').read_bytes()
   if k>=3 and aux==previous:break
   previous=aux
  else:raise RuntimeError('Canonical references did not stabilize')
  log=(work/'main.log').read_text(errors='replace')
  for pattern in [r'Overfull \\[hv]box',r'LaTeX Warning: (?:Reference|Citation).*undefined',r'There were undefined references',r'multiply defined']:
   need(not re.search(pattern,log,re.S if 'undefined' in pattern and '.*' in pattern else 0),'Typesetting preflight failure: '+pattern)
  shutil.copy2(work/'main.pdf',P/'paper.pdf');shutil.copy2(work/'main.log',E/'LATEX.log')
  auxtext=(work/'main.aux').read_text();labels={m.group(1):{'number':m.group(2),'page':int(m.group(3))} for m in re.finditer(r'\\newlabel\{([^}]+)\}\{\{([^}]*)\}\{(\d+)\}',auxtext)}
  dump(E/'THEOREM_LOCATIONS.json',labels)
 # Two-view preservation: retain the entire historical PDF page stream.
 paper=fitz.open(P/'paper.pdf');old=fitz.open(OLD/'complete-development.pdf');full=fitz.open();full.insert_pdf(paper);offset=len(paper);full.insert_pdf(old)
 toc=paper.get_toc()+[[1,'Preserved v17 complete development',offset+1]]+[[row[0]+1,row[1],row[2]+offset] for row in old.get_toc()]
 full.set_toc(toc);full.set_metadata({'title':'General Theta Foundations I v18 — complete development','author':'Qian Qi','subject':'Canonical v18 article followed by the unchanged v17 development'})
 full.save(P/'complete-development.pdf',garbage=4,deflate=True);full.close();full=fitz.open(P/'complete-development.pdf')
 need(len(old)==256,'Unexpected inherited page count');need(len(full)==offset+256,'Incomplete companion')
 for k,page in enumerate(old):
  other=full[offset+k]
  need(page.get_text()==other.get_text(),'Historical page text changed '+str(k+1))
  need(page.get_pixmap(matrix=fitz.Matrix(.35,.35),alpha=False).samples==other.get_pixmap(matrix=fitz.Matrix(.35,.35),alpha=False).samples,'Historical page rendering changed '+str(k+1))
 pagecheck=[]
 for k,page in enumerate(paper):
  outside=[]
  for b in page.get_text('blocks'):
   if b[6]==0 and (b[0]<-1 or b[1]<-1 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1):outside.append(b[:4])
  need(not outside,'Canonical text outside page '+str(k+1));pagecheck.append({'page':k+1,'text_inside_page':True})
 dump(E/'PAGE_CHECK.json',{'canonical':pagecheck,'inherited_text_and_raster_pages_equal':256,'raster_scale':0.35,'scope':'Automated geometry and preservation checks; separate visual inspection remains necessary.'})
 bound=json.loads((P/'PROOF_STATUS.json').read_text())
 for row in bound['statements']:
  row['source_commit']=source;row['compiled_location']=labels.get(row['id'])
  need(row['compiled_location'],'Unresolved theorem '+row['id'])
 dump(E/'BOUND_PROOF_STATUS.json',bound)
 # Archive closure; installed font files are never collected.
 def archive(dest,files):
  with zipfile.ZipFile(dest,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
   for rel,file in sorted(files.items()):
    need(Path(rel).suffix.lower() not in {'.ttf','.otf','.pfb','.woff','.woff2'},'Font file in archive')
    zi=zipfile.ZipInfo(rel,(2026,9,23,0,0,0));zi.compress_type=zipfile.ZIP_DEFLATED;zi.external_attr=0o100644<<16;z.writestr(zi,Path(file).read_bytes())
 archive(E/'SUBMISSION_SOURCES.zip',{f.name:f for f in P.glob('*.tex')}|{'README.md':P/'README.md'})
 allfiles={rel:R/rel for rel in set(inherited)|set(new)};allfiles[str((P/'SOURCE_MANIFEST.json').relative_to(R))]=P/'SOURCE_MANIFEST.json';allfiles[str((OLD/'complete-development.pdf').relative_to(R))]=OLD/'complete-development.pdf'
 archive(E/'COMPILED_SOURCES.zip',allfiles)
 receipt={'edition':'GTF-I-v18-continuation-transport','controlling_review_commit':REVIEW,'source_commit':source,'checkout_kind':'GitHub source checkout' if source else 'local extracted source closure','workflow_run':os.getenv('GITHUB_RUN_ID'),'compiler':compiler,'tex_passes':passes,'source_inputs_clean_at_build':True,'inherited_sources_checked':len(inherited),'new_sources_checked':len(new),'report_source_blobs_checked':reportchecks,'finite_exact_checks':result['checks'],'ordinary_optimized_equal':True,'negative_control_executions':len(negative),'inherited_diagnostic_runs':inherited_runs,'canonical_pages':offset,'complete_development_pages':len(full),'preserved_inherited_pages':256,'preserved_inherited_pdf_sha256':OLDPDF,'inherited_raster_and_text_pages_checked':256,'theorem_statement_count':len(bound['statements']),'resolved_label_count':len(labels),'no_unresolved_references_or_citations':True,'no_overfull_boxes':True,'pipeline_contract':pipeline,'artifacts':{name:{'sha256':sha(P/name),'bytes':(P/name).stat().st_size} for name in ('paper.pdf','complete-development.pdf','evidence/SUBMISSION_SOURCES.zip','evidence/COMPILED_SOURCES.zip')},'scope':'Executed source/preservation/build/finite-identity checks only. No independent analytic certification, priority certification, referee acceptance or journal acceptance is asserted.'}
 dump(E/'BUILD_RECEIPT.json',receipt)
 print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
