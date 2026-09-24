#!/usr/bin/env python3
"""Source-pinned A2 v151 assembly, exact regressions and native PDF publication.
Writes only this revision folder and CURRENT_REVIEW_ENTRY.md; no proof certification.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,os,re,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'v149';ROOT=HERE.parents[3]
PREFIX='papers/A2-v17-boundary-information-coarsening/article/v151'
BRANCH='revision/a2-v151-canonical-gcd-boundary-normalization-2026-09-24'
REVIEW='ddcef32b3cf491aacb293e466c393ec4af3caecd'
REPORT='reviews/a2-v149-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md'
REPORT_BLOB='2878e4dd16cf49e631b933b8c34bafdc896eed8f'
GENERATED={'SOURCE_LOCK_V151.json','NONDELETION_V151.json','PROVENANCE_MANIFEST_V151.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t)
def dump(p,x):put(p,json.dumps(x,indent=2)+'\n')
def source(p,r):return p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'} and not any(k in r.parts for k in ('evidence','__pycache__'))
def expand(p,root):return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(root/(m[1] if m[1].endswith('.tex') else m[1]+'.tex'),root),p.read_text())
def entry(commit=None):
 lead=(f'Native PDFs and 27 successful regression scripts are bound to source commit `{commit}`.' if commit else 'Revision source published; completed verification is asserted only in the v151 build receipt.')
 put(ROOT/'CURRENT_REVIEW_ENTRY.md',f'''# A2 referee entry — revision 151

{lead} Finite checks do not certify universal proofs, historical priority, or journal acceptance.

Revision branch: `{BRANCH}`. Controlling v149 review tip: `{REVIEW}`.
Report addressed: [{REPORT}]({REPORT}). This owner-requested report is not a journal editorial decision.

**Principal article:** [geometry.pdf]({PREFIX}/geometry.pdf) · [LaTeX]({PREFIX}/geometry.tex).

[Response to v149]({PREFIX}/RESPONSE_TO_V149_REPORT.md) · [Reading guide]({PREFIX}/README.md) · [Issue matrix]({PREFIX}/ISSUE_MATRIX_V151.json).

New mathematics: canonical divisor-incidence functor over arbitrary bases; finite normalization of its scheme-theoretic image; exact normal locus and complete nonreduced fibre equations; intrinsic first-relation algebra boundary; universal properties of the two rigidifications; explicit common closed pencil specialization with finite-flat failure lift. All v149 principal mathematical blocks and labels are retained.

[Build receipt]({PREFIX}/evidence/BUILD_RECEIPT_V151.json) · [Source lock]({PREFIX}/SOURCE_LOCK_V151.json) · [Preservation]({PREFIX}/NONDELETION_V151.json) · [Literature audit]({PREFIX}/LITERATURE_AUDIT_V151.md) · [Proof-scope audit]({PREFIX}/PROOF_SCOPE_AUDIT_V151.md).

[Applications]({PREFIX}/applications.pdf) remain separate; the [historical archive]({PREFIX}/archive-v144.pdf) remains non-submitted. Both mathematical drivers are unchanged. Only geometry.pdf is the principal article.

**Documentary item still open:** complete Ballico 1993 theorem/proof text was not obtained. No theorem numbers, nonanticipation claim, or historical priority clearance are fabricated.
''')
def assemble():
 if not BASE.is_dir():raise RuntimeError('Pinned predecessor source tree missing')
 hist=HERE/'history/v149-root';hist.mkdir(parents=True,exist_ok=True);records={}
 for p in BASE.rglob('*'):
  r=p.relative_to(BASE)
  if not source(p,r):continue
  dest=hist/p.name if len(r.parts)==1 else HERE/r
  if dest.exists() and sha(dest)!=sha(p):raise RuntimeError('Inherited bytes differ: '+str(r))
  if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
  active=HERE/r
  if not active.exists():active.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,active)
  records[str(r)]={'sha256':sha(p),'preserved_at':str(dest.relative_to(HERE))}
 dump(HERE/'INHERITED_SOURCE_V151.json',{'predecessor_review_commit':REVIEW,'files':records})
 report=ROOT/REPORT
 if report.exists():
  blob=hashlib.sha1(b'blob '+str(report.stat().st_size).encode()+b'\0'+report.read_bytes()).hexdigest()
  if blob!=REPORT_BLOB:raise RuntimeError('Controlling review report differs from pinned blob')
  dest=HERE/'review_inputs/v149_REFEREE_REPORT.md';dest.parent.mkdir(exist_ok=True);shutil.copy2(report,dest)
 elif os.environ.get('GITHUB_ACTIONS'):raise RuntimeError('Pinned review report missing in remote checkout')
 entry();print('Preserved',len(records),'predecessor source files',flush=True)
def build():
 os.chdir(HERE);evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
 names='exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact revision132_exact revision133_exact revision134_exact revision135_exact revision136_exact revision137_exact revision138_exact revision139_exact revision140_exact revision141_spectral_exact revision141_likelihood_exact revision142_exact revision143_critical_exact revision144_projective_exact'.split()
 scripts=['checks/'+n+'.py' for n in names]+['check_v145.py','check_v146.py','check_local_v146.py','check_v147.py','check_v148.py','check_v149.py','check_v151.py'];records=[]
 for script in scripts:
  print('Executing',script,flush=True);log=evidence/(Path(script).stem+'.log')
  with log.open('w') as f:r=subprocess.run([sys.executable,script],stdout=f,stderr=subprocess.STDOUT)
  records.append({'script':script,'sha256':sha(HERE/script),'returncode':r.returncode,'log':str(log.relative_to(HERE))})
  dump(evidence/'EXECUTED_CHECKS_V151.json',records)
  if r.returncode:print(log.read_text()[-12000:]);raise RuntimeError('Regression failed: '+script)
 for name in ('geometry','applications','archive-v144'):
  for ext in ('aux','out','toc'):(HERE/(name+'.'+ext)).unlink(missing_ok=True)
  for k in range(1,4):
   print('Native LaTeX',name,k,flush=True)
   with (evidence/(name+'-pass'+str(k)+'.log')).open('w') as f:r=subprocess.run(['pdflatex','-interaction=nonstopmode','-halt-on-error',name+'.tex'],stdout=f,stderr=subprocess.STDOUT)
   if r.returncode:raise RuntimeError('Native build failed: '+name)
  aux=(HERE/(name+'.aux')).read_text()
  put(HERE/(name+'-labels.aux'),'\n'.join(l for l in aux.splitlines() if l.startswith('\\newlabel{') and not l.startswith('\\newlabel{tocindent'))+'\n')
  shutil.copy2(HERE/(name+'.log'),evidence/(name+'-final.log'))
 verify()
def verify():
 evidence=HERE/'evidence';texts={n:expand(HERE/(n+'.tex'),HERE) for n in ('geometry','applications','archive-v144')}
 labels=lambda t:re.findall(r'\\label\{([^}]+)\}',t)
 refs=lambda t:set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',t))
 checks={};main=texts['geometry'];old=expand(BASE/'geometry.tex',BASE)
 checks['principal_references_self_contained']=not(refs(main)-set(labels(main))) and '\\externaldocument' not in main
 checks['applications_references_resolve']=not(refs(texts['applications'])-set(labels(main))-set(labels(texts['applications'])))
 checks['archive_references_resolve']=not(refs(texts['archive-v144'])-set(labels(texts['archive-v144'])))
 pdfs={}
 for n,t in texts.items():
  log=(evidence/(n+'-final.log')).read_text(errors='replace')
  checks[n+'_unique_labels']=len(labels(t))==len(set(labels(t)))
  checks[n+'_resolved_references']=not bool(re.search(r'(There were undefined references|Citation .+ undefined|Reference .+ undefined|multiply defined|Rerun to get cross-references)',log))
  checks[n+'_no_overfull_boxes']=not bool(re.search(r'Overfull \\[hv]box',log))
  pdf=HERE/(n+'.pdf');info=subprocess.check_output(['pdfinfo',str(pdf)],text=True)
  pdfs[n]={'pages':int(re.search(r'^Pages:\s*(\d+)',info,re.M)[1]),'bytes':pdf.stat().st_size,'sha256':sha(pdf)}
 records=json.loads((evidence/'EXECUTED_CHECKS_V151.json').read_text())
 checks['all_27_scripts_pass']=len(records)==27 and all(r['returncode']==0 and sha(HERE/r['script'])==r['sha256'] for r in records)
 newexact=json.loads((evidence/'REVISION151_EXACT.json').read_text());checks['new_exact_witnesses_pass']=newexact['ok'] is True
 inherited=json.loads((HERE/'INHERITED_SOURCE_V151.json').read_text())['files']
 checks['every_v149_source_preserved']=all((HERE/r['preserved_at']).is_file() and sha(HERE/r['preserved_at'])==r['sha256'] for r in inherited.values())
 checks['all_v149_parts_unchanged']=all(sha(HERE/p.relative_to(BASE))==sha(p) for p in (BASE/'parts').rglob('*.tex'))
 pattern=r'\\begin\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}[\s\S]*?\\end\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}'
 oldblocks=re.findall(pattern,old);newblocks=re.findall(pattern,main)
 checks['all_v149_principal_math_blocks_retained']=not(Counter(oldblocks)-Counter(newblocks))
 checks['all_v149_principal_labels_retained']=set(labels(old))<=set(labels(main))
 checks['applications_driver_unchanged']=sha(HERE/'applications.tex')==sha(BASE/'applications.tex')
 checks['archive_driver_unchanged']=sha(HERE/'archive-v144.tex')==sha(BASE/'archive-v144.tex')
 required={'prop:incidence-v151','lem:fibre-equations-v151','thm:boundary-normalization-v151','cor:canonical-exact-v151','cor:algebra-boundary-v151','thm:rigidification-v151','cor:two-rigidifications-v151','thm:closed-pencil-v151','cor:closed-failure-v151'}
 checks['all_nine_new_results_in_principal_article']=required<=set(labels(main))
 abstract=re.search(r'\\begin\{abstract\}([\s\S]*?)\\end\{abstract\}',main)[1]
 checks['abstract_at_most_200_words']=len(abstract.split())<=200
 checks['specific_AI_idea_disclosure']='GPT-6 Astra Pro assisted specifically' in main
 commit=os.environ.get('A2_SOURCE_COMMIT','LOCAL-PREFLIGHT-NOT-REMOTE')
 receipt={'revision':151,'source_commit':commit,'controlling_review_commit':REVIEW,'controlling_review_blob':REPORT_BLOB,'all_checks_pass':all(checks.values()),'checks':checks,'executed_script_count':len(records),'new_exact_check_count':newexact['check_count'],'executed_scripts':records,'pdfs':pdfs,'labels':{n:len(labels(t)) for n,t in texts.items()},'preserved_predecessor_source_files':len(inherited),'preserved_principal_math_blocks':len(oldblocks),'proof_certified_by_computation':False,'Ballico_1993_full_text_comparison_completed':False,'historical_priority_certified':False,'journal_acceptance_asserted':False}
 locator={}
 for lab,num,page in re.findall(r'\\newlabel\{([^}]+)\}\{\{([^}]+)\}\{([^}]+)\}',(HERE/'geometry.aux').read_text()):
  if lab in required:locator[lab]={'number':num,'page':page}
 dump(evidence/'THEOREM_LOCATOR_V151.json',locator)
 dump(evidence/'BUILD_RECEIPT_V151.json',receipt)
 dump(HERE/'NONDELETION_V151.json',{'source_commit':commit,'predecessor_review_commit':REVIEW,'all_source_bytes_preserved':checks['every_v149_source_preserved'],'all_principal_math_blocks_retained':checks['all_v149_principal_math_blocks_retained'],'all_v149_parts_unchanged':checks['all_v149_parts_unchanged'],'source_files':inherited,'preservation_is_not_proof_certification':True})
 dump(HERE/'PROVENANCE_MANIFEST_V151.json',{'source_commit':commit,'sha256':{str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if source(p,p.relative_to(HERE)) and p.name not in GENERATED}})
 dump(HERE/'SOURCE_LOCK_V151.json',{'revision':151,'source_commit':commit,'controlling_review_commit':REVIEW,'principal_manuscript':'geometry.pdf','separate_application':'applications.pdf','non_submitted_archive':'archive-v144.pdf','receipt':'evidence/BUILD_RECEIPT_V151.json','all_checks_pass':receipt['all_checks_pass'],'historical_priority_certified':False})
 print(json.dumps(receipt,indent=2),flush=True)
 if not receipt['all_checks_pass']:raise RuntimeError('v151 audit failed')
 entry(commit)
if __name__=='__main__':
 if len(sys.argv)!=2 or sys.argv[1] not in {'assemble','build','verify'}:raise SystemExit('Usage: revision_v151.py assemble|build|verify')
 globals()[sys.argv[1]]()
