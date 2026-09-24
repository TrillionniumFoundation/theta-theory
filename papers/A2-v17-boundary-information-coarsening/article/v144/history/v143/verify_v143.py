#!/usr/bin/env python3
"""Source-bound preservation, routing, native-PDF and executed-test checks."""
from pathlib import Path
from collections import Counter
import hashlib,json,re,os,platform,subprocess
import fitz,sympy,numpy
ROOT=Path(__file__).resolve().parent
OLD=Path(os.getenv('A2_PREDECESSOR_DIR',str(ROOT.parent/'v142')))
PIN='4deb7a35f4488a0c8b686261569ce4ef324ca750'
REVIEW='3afecca5e65d7fe9c6784020ea6e813122938140'
REVIEWED='8cd389f4048a1047be9aa8e8e4f642595175a555'
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
def collect(driver,root=ROOT):
 seen=set();texts=[]
 def visit(n):
  if n in seen:return
  if Path(n).is_absolute() or '..' in Path(n).parts:raise ValueError(n)
  seen.add(n);txt=(root/n).read_text();texts.append(txt)
  for f in re.findall(r'\\input\{([^}]+)\}',txt):visit(f)
 visit(driver+'.tex')
 text='\n'.join(texts)
 return seen,re.findall(r'\\label\{([^}]+)\}',text),text
_,old_labels,oldtext=collect('complete',OLD)
active,labels,text=collect('complete');_,main,_=collect('geometry');_,supp,_=collect('supplement')
def blocks(txt,envs):
 pat=r'\\begin\{('+ '|'.join(envs)+r')\}.*?\\end\{\1\}'
 return Counter(re.sub(r'\s+',' ',m.group(0)).strip() for m in re.finditer(pat,txt,re.S))
oldproof=blocks(oldtext,['theorem','lemma','proposition','corollary','proof'])
newproof=blocks(text,['theorem','lemma','proposition','corollary','proof'])
oldnumbered=blocks(oldtext,['equation','align','gather'])
newnumbered=blocks(text,['equation','align','gather'])
parts=list((OLD/'parts').glob('*.tex'));scripts_old=list((OLD/'checks').glob('*.py'))
archive_files=[p for p in OLD.rglob('*') if p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'} and 'evidence' not in p.relative_to(OLD).parts]
issue=json.loads((ROOT/'ISSUE_MATRIX.json').read_text())
checks={
 'all_inherited_part_files_byte_identical':all(sha(p)==sha(ROOT/'parts'/p.name) for p in parts),
 'all_inherited_check_files_byte_identical':all(sha(p)==sha(ROOT/'checks'/p.name) for p in scripts_old),
 'complete_predecessor_source_archive_exact':all(sha(p)==sha(ROOT/'history/v142'/p.relative_to(OLD)) for p in archive_files),
 'all_inherited_labels_active':set(old_labels)<=set(labels),
 'all_inherited_theorem_and_proof_blocks_active_unchanged':not (oldproof-newproof),
 'all_inherited_numbered_equation_blocks_active_unchanged':not (oldnumbered-newnumbered),
 'no_duplicate_labels':len(labels)==len(set(labels)),
 'main_supplement_label_partition':not(set(main)&set(supp)) and set(main)|set(supp)==set(labels),
 'principal_theorem_and_new_critical_results_in_main':all(x in main for x in ['thm:principal-finite-v143','thm:sharp-finite-pencil','thm:universal-finite-neighbourhood','thm:relative-spectral-readout','thm:critical-correspondence-v143','thm:real-critical-cover-v143']),
 'full_web_and_operator_theorems_in_supplement':all(x in supp and x not in main for x in ['thm:main-web-reconstruction','thm:uniform-contraction','thm:contraction-singular-values']),
 'current_issue_matrix_revision':issue['revision']==143,
 'current_issue_matrix_controlling_report':issue['controlling_referee_report_commit']==REVIEW,
 'current_issue_matrix_reviewed_source':issue['reviewed_manuscript_commit']==REVIEWED,
}
source_commit=os.getenv('A2_SOURCE_COMMIT')
try:
 head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,stderr=subprocess.DEVNULL,text=True).strip()
 if source_commit:checks['checkout_equals_source_commit']=source_commit==head
 else:source_commit=head
 repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip())
 subprocess.run(['git','diff','--exit-code',PIN,'--',str(OLD.relative_to(repo))],cwd=repo,check=True,stdout=subprocess.PIPE)
 checks['pinned_predecessor_tree_unchanged']=True
 p=str(ROOT.relative_to(repo))
 subprocess.run(['git','diff','--exit-code','HEAD','--',p+'/parts',p+'/checks',p+'/*.tex',p+'/build.sh',p+'/verify_v143.py'],cwd=repo,check=True,stdout=subprocess.PIPE)
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
  checks[name+'_metadata']='revision 143' in doc.metadata.get('title','').lower()
 checks[name+'_page_bounds']=not outside
 checks[name+'_no_overfull']='Overfull' not in log
 checks[name+'_no_unresolved_labels']=not any(x in log.lower() for x in ['undefined references','undefined citations','multiply defined'])
 checks[name+'_no_latex_error']='\n! ' not in log
scripts=['exact_k3','exact_corank_two','stratified_rank_two','boundary_atlas','generic_boundary_atlas']+['revision'+str(i)+'_exact' for i in range(131,141)]+['revision141_spectral_exact','revision141_likelihood_exact','revision142_exact','revision143_critical_exact']
checks['all_nineteen_scripts_executed']=all((ROOT/'evidence'/(x+'.log')).exists() for x in scripts)
for v in range(131,141):checks[f'exact_{v}']=json.loads((ROOT/f'evidence/REVISION{v}_EXACT.json').read_text())['ok']
for tag in ['SPECTRAL','LIKELIHOOD']:checks['exact_141_'+tag.lower()]=json.loads((ROOT/f'evidence/REVISION141_{tag}_EXACT.json').read_text())['ok']
r=json.loads((ROOT/'evidence/revision142-exact.json').read_text())
checks['exact_142_completed']=len(r['gram_identities'])==5 and len(r['rank_strata'])==18 and r['mixed_identity_evaluations']==84 and r['partition_pairs']==14832
checks['exact_143_critical_algebra']=json.loads((ROOT/'evidence/REVISION143_CRITICAL_EXACT.json').read_text())['ok']
excluded={'PROVENANCE_MANIFEST_V143.json','NONDELETION_V143.json','SOURCE_LOCK_V143.json'}
files=[p for p in ROOT.rglob('*') if p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'} and 'evidence' not in p.relative_to(ROOT).parts and str(p.relative_to(ROOT)) not in excluded]
manifest={'revision':143,'source_commit':source_commit,'review_commit':REVIEW,'reviewed_manuscript_commit':REVIEWED,'mathematical_predecessor':PIN,'source_sha256':{str(p.relative_to(ROOT)):sha(p) for p in sorted(files)},'Ballico_1993_full_text_obtained':False,'exhaustive_priority_verified':False}
(ROOT/'PROVENANCE_MANIFEST_V143.json').write_text(json.dumps(manifest,indent=2)+'\n')
nondeletion={'revision':143,'predecessor':PIN,'inherited_labels':old_labels,'inherited_label_count':len(old_labels),'current_label_count':len(labels),'inherited_mathematical_blocks':sum(oldproof.values()),'unchanged_blocks_retained':not(oldproof-newproof),'inherited_numbered_blocks':sum(oldnumbered.values()),'unchanged_numbered_blocks_retained':not(oldnumbered-newnumbered),'all_old_part_hashes':{p.name:sha(p) for p in parts},'all_old_check_hashes':{p.name:sha(p) for p in scripts_old},'active_inputs':sorted(active),'missing_mathematical_blocks':list((oldproof-newproof).keys()),'missing_numbered_blocks':list((oldnumbered-newnumbered).keys())}
(ROOT/'NONDELETION_V143.json').write_text(json.dumps(nondeletion,indent=2)+'\n')
receipt={'revision':143,'ok':all(checks.values()),'checks':checks,'pdfs':pdfs,'inherited_label_count':len(old_labels),'current_label_count':len(labels),'inherited_mathematical_blocks':sum(oldproof.values()),'source_commit':source_commit,'review_commit':REVIEW,'reviewed_manuscript_commit':REVIEWED,'mathematical_predecessor':PIN,'github_run_id':os.getenv('GITHUB_RUN_ID'),'workflow_trigger_commit':os.getenv('GITHUB_SHA'),'executed_scripts':scripts,'source_manifest_sha256':sha(ROOT/'PROVENANCE_MANIFEST_V143.json'),'runtime':{'python':platform.python_version(),'sympy':sympy.__version__,'numpy':numpy.__version__,'pymupdf':fitz.VersionBind},'documentary_open':['B140.2: full Ballico 1993 theorem-level six-axis comparison','B140.3: no exhaustive historical-priority certification; exact inspected-source comparison and operator identity supplied'],'not_certified':['formal verification of all proofs','exhaustive historical priority','top-four editorial acceptance','unmarked moduli-stack equivalence']}
(ROOT/'evidence/BUILD_RECEIPT_V143.json').write_text(json.dumps(receipt,indent=2)+'\n')
lock={'revision':143,'source_commit':source_commit,'controlling_referee_report_commit':REVIEW,'reviewed_manuscript_commit':REVIEWED,'mathematical_predecessor_commit':PIN,'pdfs':pdfs,'receipt_sha256':sha(ROOT/'evidence/BUILD_RECEIPT_V143.json'),'source_manifest_sha256':sha(ROOT/'PROVENANCE_MANIFEST_V143.json'),'run_id':os.getenv('GITHUB_RUN_ID'),'freeze_policy':'The exact source SHA, not the movable branch name, defines this review object. A subsequent mathematical revision requires a new branch.'}
(ROOT/'SOURCE_LOCK_V143.json').write_text(json.dumps(lock,indent=2)+'\n')
print(json.dumps(receipt,indent=2))
if not receipt['ok']:raise SystemExit('v143 checks failed')
