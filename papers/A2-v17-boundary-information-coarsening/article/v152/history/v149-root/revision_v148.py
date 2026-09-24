#!/usr/bin/env python3
"""Assemble and verify the isolated A2 v148 source and native publication.
The exact checks are regression witnesses, not universal proof certificates.
No source outside v148 and the A2 review entry is written.
"""
from pathlib import Path
from collections import Counter
import hashlib,json,os,re,shutil,subprocess,sys
HERE=Path(__file__).resolve().parent
BASE=HERE.parent/'v147'
ROOT=HERE.parents[3]
PREFIX='papers/A2-v17-boundary-information-coarsening/article/v148'
BRANCH='revision/a2-v148-coefficient-symmetries-moving-pencils-2026-09-24'
REVIEW='17fb7ba7cab6545f5da6d4fcde5283318bd26725'
REPORT='reviews/a2-v147-independent-harsh-top4-2026-09-24/REFEREE_REPORT.md'
GENERATED={'SOURCE_LOCK_V148.json','NONDELETION_V148.json','PROVENANCE_MANIFEST_V148.json'}
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def put(p,t):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(t)
def dump(p,x):put(p,json.dumps(x,indent=2)+'\n')
def source(p,r):return p.is_file() and p.suffix in {'.tex','.py','.sh','.md','.json'} and not any(k in r.parts for k in ('evidence','__pycache__'))
def expand(p,root):
 return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(root/(m[1] if m[1].endswith('.tex') else m[1]+'.tex'),root),p.read_text())
def entry(commit=None):
 lead=(f'Native PDFs and 25 successful regression scripts are bound to source commit `{commit}`.' if commit else 'The complete revision source is published; native build status is recorded only in the v148 build receipt.')
 put(ROOT/'CURRENT_REVIEW_ENTRY.md',f'''# A2 referee entry — revision 148

{lead} These checks do not certify universal proofs, historical priority, or journal acceptance.

Revision branch: `{BRANCH}`. Controlling review tip: `{REVIEW}`.
Latest report addressed: [{REPORT}]({REPORT}).

**Principal article:** [geometry.pdf]({PREFIX}/geometry.pdf) · [LaTeX]({PREFIX}/geometry.tex).

[Response to v147]({PREFIX}/RESPONSE_TO_V147_REPORT.md) · [Reading guide]({PREFIX}/README.md) · [Issue matrix]({PREFIX}/ISSUE_MATRIX_V148.json).

The new results give an intrinsic recognition criterion, exact coefficient stabilizers and transpose ambiguity, including the global zero/full case. They realize the equivalence problem for maps of the projective line inside one fibre orbit of moving quadratic pencils, with identical fibre algebras and all graded vector bundles. All v147 mathematical blocks and source bytes are retained.

[Build receipt]({PREFIX}/evidence/BUILD_RECEIPT_V148.json) · [Source lock]({PREFIX}/SOURCE_LOCK_V148.json) · [Preservation]({PREFIX}/NONDELETION_V148.json) · [Literature audit]({PREFIX}/LITERATURE_AUDIT_V148.md).

[Applications]({PREFIX}/applications.pdf) are separate; the [historical archive]({PREFIX}/archive-v144.pdf) is non-submitted. Only geometry.pdf is the principal article.

**Documentary item still unresolved:** Ballico 1993 full theorem/proof text was not obtained. The six-axis comparison remains open; no claim that the new mathematics settles historical priority is made.
''')
def assemble():
 if not BASE.is_dir():raise RuntimeError('Pinned v147 source tree missing')
 hist=HERE/'history/v147-root';hist.mkdir(parents=True,exist_ok=True)
 records={}
 for p in BASE.rglob('*'):
  r=p.relative_to(BASE)
  if not source(p,r):continue
  dest=hist/p.name if len(r.parts)==1 else HERE/r
  if dest.exists() and sha(dest)!=sha(p):raise RuntimeError('Inherited bytes differ: '+str(r))
  if not dest.exists():dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,dest)
  active=HERE/r
  if not active.exists():active.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(p,active)
  records[str(r)]={'sha256':sha(p),'preserved_at':str(dest.relative_to(HERE))}
 dump(HERE/'INHERITED_SOURCE_V148.json',{'predecessor_review_commit':REVIEW,'files':records})
 report=ROOT/REPORT
 if report.exists():
  # The original report remains unchanged; this is a source-bound review copy.
  copy=HERE/'review_inputs/v147_REFEREE_REPORT.md';shutil.copy2(report,copy)
  blob=hashlib.sha1(b'blob '+str(report.stat().st_size).encode()+b'\0'+report.read_bytes()).hexdigest()
  if blob!='4eb25c1d3e3b19a1e06c47ceb1c2214864593c4c':raise RuntimeError('Controlling report differs from pinned review')
 entry();print('Preserved',len(records),'v147 source files',flush=True)
def build():
 os.chdir(HERE);evidence=HERE/'evidence';evidence.mkdir(exist_ok=True)
 names='exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact revision132_exact revision133_exact revision134_exact revision135_exact revision136_exact revision137_exact revision138_exact revision139_exact revision140_exact revision141_spectral_exact revision141_likelihood_exact revision142_exact revision143_critical_exact revision144_projective_exact'.split()
 scripts=['checks/'+n+'.py' for n in names]+['check_v145.py','check_v146.py','check_local_v146.py','check_v147.py','check_v148.py']
 records=[]
 for script in scripts:
  print('Executing',script,flush=True);log=evidence/(Path(script).stem+'.log')
  with log.open('w') as f:r=subprocess.run([sys.executable,script],stdout=f,stderr=subprocess.STDOUT)
  records.append({'script':script,'sha256':sha(HERE/script),'returncode':r.returncode,'log':str(log.relative_to(HERE))})
  dump(evidence/'EXECUTED_CHECKS_V148.json',records)
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
 checks['principal_proofs_self_contained']=not(refs(main)-set(labels(main))) and '\\externaldocument' not in main
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
 records=json.loads((evidence/'EXECUTED_CHECKS_V148.json').read_text())
 checks['all_25_scripts_pass']=len(records)==25 and all(r['returncode']==0 and sha(HERE/r['script'])==r['sha256'] for r in records)
 checks['new_exact_witnesses_pass']=json.loads((evidence/'REVISION148_EXACT.json').read_text())['ok'] is True
 inherited=json.loads((HERE/'INHERITED_SOURCE_V148.json').read_text())['files']
 checks['every_v147_source_preserved']=all((HERE/r['preserved_at']).is_file() and sha(HERE/r['preserved_at'])==r['sha256'] for r in inherited.values())
 checks['all_v147_parts_unchanged']=all(sha(HERE/p.relative_to(BASE))==sha(p) for p in (BASE/'parts').rglob('*.tex'))
 pattern=r'\\begin\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}[\s\S]*?\\end\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}'
 oldblocks=re.findall(pattern,old);newblocks=re.findall(pattern,main)
 checks['all_v147_principal_math_blocks_retained']=not(Counter(oldblocks)-Counter(newblocks))
 checks['all_v147_principal_labels_retained']=set(labels(old))<=set(labels(main))
 checks['separate_manuscript_drivers_unchanged']=all(sha(HERE/n)==sha(BASE/n) for n in ('applications.tex','archive-v144.tex'))
 required={'thm:recognition-dichotomy-v148','thm:exact-coefficient-stabilizer-v148','prop:full-global-ambiguity-v148','cor:intrinsic-orbits-v148','thm:covering-pencil-moduli-v148','cor:pencil-native-pair-v148'}
 checks['all_six_new_results_in_principal_article']=required<=set(labels(main))
 commit=os.environ.get('A2_SOURCE_COMMIT','LOCAL-PREFLIGHT-NOT-REMOTE')
 receipt={'revision':148,'source_commit':commit,'controlling_review_commit':REVIEW,'all_checks_pass':all(checks.values()),'checks':checks,'executed_script_count':len(records),'executed_scripts':records,'pdfs':pdfs,'labels':{n:len(labels(t)) for n,t in texts.items()},'preserved_predecessor_source_files':len(inherited),'preserved_principal_math_blocks':len(oldblocks),'proof_certified_by_computation':False,'Ballico_1993_full_text_comparison_completed':False,'historical_priority_certified':False,'journal_acceptance_asserted':False}
 dump(evidence/'BUILD_RECEIPT_V148.json',receipt)
 dump(HERE/'NONDELETION_V148.json',{'source_commit':commit,'predecessor_review_commit':REVIEW,'all_source_bytes_preserved':checks['every_v147_source_preserved'],'all_principal_math_blocks_retained':checks['all_v147_principal_math_blocks_retained'],'all_v147_parts_unchanged':checks['all_v147_parts_unchanged'],'source_files':inherited,'preservation_is_not_proof_certification':True})
 dump(HERE/'PROVENANCE_MANIFEST_V148.json',{'source_commit':commit,'sha256':{str(p.relative_to(HERE)):sha(p) for p in HERE.rglob('*') if source(p,p.relative_to(HERE)) and p.name not in GENERATED}})
 dump(HERE/'SOURCE_LOCK_V148.json',{'revision':148,'source_commit':commit,'controlling_review_commit':REVIEW,'principal_manuscript':'geometry.pdf','separate_application':'applications.pdf','non_submitted_archive':'archive-v144.pdf','receipt':'evidence/BUILD_RECEIPT_V148.json','all_checks_pass':receipt['all_checks_pass'],'historical_priority_certified':False})
 print(json.dumps(receipt,indent=2),flush=True)
 if not receipt['all_checks_pass']:raise RuntimeError('v148 audit failed')
 entry(commit)
if __name__=='__main__':
 if len(sys.argv)!=2 or sys.argv[1] not in {'assemble','build','verify'}:raise SystemExit('Usage: revision_v148.py assemble|build|verify')
 globals()[sys.argv[1]]()
