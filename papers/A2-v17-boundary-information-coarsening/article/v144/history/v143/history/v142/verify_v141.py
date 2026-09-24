#!/usr/bin/env python3
"""Source-bound reproducibility and finite audits; not formal proof certification."""
from pathlib import Path
import hashlib,json,re,os,platform,subprocess
import fitz,sympy,numpy
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def collect(driver):
 seen=set();parts=[]
 def visit(n):
  if n in seen:return
  if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError(n)
  seen.add(n);txt=(ROOT/n).read_text();parts.append(txt)
  for f in re.findall(r'\\input\{([^}]+)\}',txt):visit(f)
 visit(driver+'.tex');return seen,re.findall(r'\\label\{([^}]+)\}','\n'.join(parts))
m=json.loads((ROOT/'PROVENANCE_MANIFEST_V141.json').read_text())
_,all_labels=collect('complete');_,main=collect('geometry');_,supp=collect('supplement')
checks={'inherited_labels_retained':set(m['inherited_labels'])<=set(all_labels),
 'no_duplicate_labels':len(all_labels)==len(set(all_labels)),
 'main_supplement_label_partition':not(set(main)&set(supp)) and set(main)|set(supp)==set(all_labels),
 'all_source_hashes_match':all((ROOT/n).is_file() and sha(ROOT/n)==h for n,h in m['source_sha256'].items()),
 'predecessor_archives_exact':all(sha(ROOT/a['archive'])==a['sha256'] for a in m['changed_predecessor'].values()),
 'all_unchanged_predecessor_sources_exact':all(sha(ROOT/n)==h for n,h in m['unchanged_predecessor_sha256'].items()),
 'new_theorems_in_main':all(x in main for x in ['thm:universal-finite-neighbourhood','thm:relative-spectral-readout','thm:totally-real-reciprocal-likelihood','lem:spectral-sheaf-similarity','lem:artinian-polynomial-square-root']),
 'all_inherited_check_sources_exact':all(sha(ROOT/n)==h for n,h in m['inherited_check_sha256'].items()),
 'documentary_limitations_recorded':m['Ballico_1993_full_text_obtained'] is False and m['exhaustive_priority_verified'] is False}
pdfs={}
for name in ['geometry','supplement','complete']:
 log=(ROOT/(name+'.log')).read_text(errors='replace');p=ROOT/(name+'.pdf')
 with fitz.open(p) as doc:
  outside=[i+1 for i,page in enumerate(doc) for b in page.get_text('blocks') if b[0]<-1 or b[1]<-1 or b[2]>page.rect.width+1 or b[3]>page.rect.height+1]
  pdfs[name]={'pages':len(doc),'sha256':sha(p),'bytes':p.stat().st_size,'outside_page_blocks':outside}
  checks[name+'_metadata']='revision 141' in doc.metadata.get('title','').lower()
 checks[name+'_page_bounds']=not outside
 checks[name+'_no_overfull']='Overfull' not in log
 checks[name+'_no_unresolved_labels']=not any(x in log.lower() for x in ['undefined references','undefined citations','multiply defined'])
 checks[name+'_no_latex_error']='\n! ' not in log
scripts=['exact_k3','exact_corank_two','stratified_rank_two','boundary_atlas','generic_boundary_atlas']+['revision'+str(i)+'_exact' for i in range(131,141)]+['revision141_spectral_exact','revision141_likelihood_exact']
checks['all_seventeen_scripts_executed']=all((ROOT/'evidence'/(x+'.log')).exists() for x in scripts)
for v in range(131,141):
 r=json.loads((ROOT/f'evidence/REVISION{v}_EXACT.json').read_text());checks[f'exact_{v}']=r['ok']
for tag in ['SPECTRAL','LIKELIHOOD']:
 r=json.loads((ROOT/f'evidence/REVISION141_{tag}_EXACT.json').read_text());checks['exact_141_'+tag.lower()]=r['ok']
source_commit=os.getenv('A2_SOURCE_COMMIT')
if not source_commit:
 try:source_commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
 except (subprocess.CalledProcessError,FileNotFoundError):source_commit='local-preflight'
receipt={'revision':141,'ok':all(checks.values()),'checks':checks,'pdfs':pdfs,
 'inherited_label_count':len(m['inherited_labels']),'current_label_count':len(all_labels),
 'unchanged_inherited_tex_count':sum(n.endswith('.tex') for n in m['unchanged_predecessor_sha256']),
 'source_commit':source_commit,'workflow_trigger_commit':os.getenv('GITHUB_SHA'),'github_run_id':os.getenv('GITHUB_RUN_ID'),
 'executed_scripts':scripts,'source_manifest_sha256':sha(ROOT/'PROVENANCE_MANIFEST_V141.json'),
 'runtime':{'python':platform.python_version(),'sympy':sympy.__version__,'numpy':numpy.__version__,'pymupdf':fitz.VersionBind},
 'documentary_open':['B140.2: full Ballico 1993 six-axis comparison','B140.3: exhaustive expert priority assessment for the exact contraction theorem'],
 'not_certified':['formal verification of all mathematical proofs','first historical priority for the likelihood proof','top-four editorial acceptance','equivalence of unmarked moduli stacks']}
(ROOT/'evidence/BUILD_RECEIPT_V141.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
if not receipt['ok']:raise SystemExit('v141 checks failed')
