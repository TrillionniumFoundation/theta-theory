#!/usr/bin/env python3
"""Executed source-bound checks; not formal proof or priority certification."""
from pathlib import Path
import hashlib,json,re,os,platform,subprocess
import fitz,sympy,numpy
ROOT=Path(__file__).resolve().parent
OLD=Path(os.getenv('A2_PREDECESSOR_DIR',str(ROOT.parent/'v141')))
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
PIN='8cd389f4048a1047be9aa8e8e4f642595175a555'
REVIEW='a10f8f1ea938e0ef8ce5a4aca4ee8e4a662ee84c'
def collect(driver,root=ROOT):
 seen=set();texts=[]
 def visit(n):
  if n in seen:return
  if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError(n)
  seen.add(n);txt=(root/n).read_text();texts.append(txt)
  for f in re.findall(r'\\input\{([^}]+)\}',txt):visit(f)
 visit(driver+'.tex')
 return seen,re.findall(r'\\label\{([^}]+)\}','\n'.join(texts))
_,old_labels=collect('complete',OLD)
_,all_labels=collect('complete');_,main=collect('geometry');_,supp=collect('supplement')
changed=['geometry.tex','complete.tex','supplement.tex','frontmatter.tex','references.tex','build.sh','README.md','ISSUE_MATRIX.json']
oldparts=list((OLD/'parts').glob('*.tex'));oldscripts=list((OLD/'checks').glob('*.py'))
checks={
 'all_inherited_parts_byte_identical':all(sha(p)==sha(ROOT/'parts'/p.name) for p in oldparts),
 'all_inherited_checks_byte_identical':all(sha(p)==sha(ROOT/'checks'/p.name) for p in oldscripts),
 'changed_predecessor_archived_exactly':all(sha(OLD/p)==sha(ROOT/'history/v141'/p) for p in changed),
 'all_inherited_labels_retained':set(old_labels)<=set(all_labels),
 'no_duplicate_labels':len(all_labels)==len(set(all_labels)),
 'main_supplement_label_partition':not(set(main)&set(supp)) and set(main)|set(supp)==set(all_labels),
 'new_theorems_in_main':all(x in main for x in ['thm:mixed-jacobian-contraction','cor:singular-kernel-mixed','thm:contraction-singular-values','thm:fixed-spectral-classification','prop:first-syzygy-hilbert']),
 'post_review_v141_theorems_retained':all(x in main for x in ['thm:universal-finite-neighbourhood','thm:relative-spectral-readout','thm:totally-real-reciprocal-likelihood'])}
source_commit=os.getenv('A2_SOURCE_COMMIT')
try:
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
 if source_commit:checks['checkout_equals_source_commit']=source_commit==head
 else:source_commit=head
 repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
 subprocess.run(['git','diff','--exit-code',PIN,'--',str(OLD.relative_to(repo))],cwd=repo,check=True,stdout=subprocess.PIPE)
 checks['pinned_predecessor_tree_unchanged']=True
 p=str(ROOT.relative_to(repo))
 subprocess.run(['git','diff','--exit-code','HEAD','--',p+'/parts',p+'/checks',p+'/*.tex',p+'/build.sh',p+'/verify_v142.py'],cwd=repo,check=True,stdout=subprocess.PIPE)
 checks['mathematical_sources_equal_commit']=True
except (subprocess.CalledProcessError,FileNotFoundError,ValueError):
 if os.getenv('GITHUB_ACTIONS'):raise
 source_commit=source_commit or 'local-preflight'
pdfs={}
for name in ['geometry','supplement','complete']:
 log=(ROOT/(name+'.log')).read_text(errors='replace');p=ROOT/(name+'.pdf')
 with fitz.open(p) as doc:
  outside=[i+1 for i,page in enumerate(doc) for b in page.get_text('blocks') if b[0]<-1 or b[1]<-1 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1]
  pdfs[name]={'pages':len(doc),'sha256':sha(p),'bytes':p.stat().st_size,'outside_page_blocks':outside}
  checks[name+'_metadata']='revision 142' in doc.metadata.get('title','').lower()
 checks[name+'_page_bounds']=not outside
 checks[name+'_no_overfull']='Overfull' not in log
 checks[name+'_no_unresolved_labels']=not any(x in log.lower() for x in ['undefined references','undefined citations','multiply defined'])
 checks[name+'_no_latex_error']='\n! ' not in log
scripts=['exact_k3','exact_corank_two','stratified_rank_two','boundary_atlas','generic_boundary_atlas']+['revision'+str(i)+'_exact' for i in range(131,141)]+['revision141_spectral_exact','revision141_likelihood_exact','revision142_exact']
checks['all_eighteen_scripts_executed']=all((ROOT/'evidence'/(x+'.log')).exists() for x in scripts)
for v in range(131,141):checks[f'exact_{v}']=json.loads((ROOT/f'evidence/REVISION{v}_EXACT.json').read_text())['ok']
for tag in ['SPECTRAL','LIKELIHOOD']:checks['exact_141_'+tag.lower()]=json.loads((ROOT/f'evidence/REVISION141_{tag}_EXACT.json').read_text())['ok']
r=json.loads((ROOT/'evidence/revision142-exact.json').read_text())
checks['exact_142_completed']=len(r['gram_identities'])==5 and len(r['rank_strata'])==18 and r['mixed_identity_evaluations']==84 and r['partition_pairs']==14832
files=[p for p in ROOT.rglob('*') if p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'} and 'evidence' not in p.relative_to(ROOT).parts and p.name not in {'PROVENANCE_MANIFEST_V142.json','NONDELETION_V142.json'}]
manifest={'revision':142,'source_commit':source_commit,'review_commit':REVIEW,'mathematical_predecessor':PIN,'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(files)},'Ballico_1993_full_text_obtained':False,'exhaustive_priority_verified':False}
(ROOT/'PROVENANCE_MANIFEST_V142.json').write_text(json.dumps(manifest,indent=2)+'\n')
nondeletion={'review_commit':REVIEW,'mathematical_predecessor':PIN,'inherited_part_count':len(oldparts),'inherited_check_count':len(oldscripts),'inherited_labels':old_labels,'current_label_count':len(all_labels),'all_old_part_hashes':{p.name:sha(p) for p in oldparts},'changed_wrapper_archives':{n:sha(OLD/n) for n in changed},'all_inherited_parts_unchanged':checks['all_inherited_parts_byte_identical']}
(ROOT/'NONDELETION_V142.json').write_text(json.dumps(nondeletion,indent=2)+'\n')
receipt={'revision':142,'ok':all(checks.values()),'checks':checks,'pdfs':pdfs,'inherited_label_count':len(old_labels),'current_label_count':len(all_labels),'source_commit':source_commit,'review_commit':REVIEW,'mathematical_predecessor':PIN,'github_run_id':os.getenv('GITHUB_RUN_ID'),'executed_scripts':scripts,'source_manifest_sha256':sha(ROOT/'PROVENANCE_MANIFEST_V142.json'),'runtime':{'python':platform.python_version(),'sympy':sympy.__version__,'numpy':numpy.__version__,'pymupdf':fitz.VersionBind},'documentary_open':['B140.2: full Ballico 1993 six-axis comparison','B140.3: exhaustive historical priority beyond inspected operator statements'],'not_certified':['formal verification of all proofs','exhaustive historical priority','top-four editorial acceptance','unmarked moduli-stack equivalence']}
(ROOT/'evidence/BUILD_RECEIPT_V142.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
if not receipt['ok']:raise SystemExit('v142 checks failed')
