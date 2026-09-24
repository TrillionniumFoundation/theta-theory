#!/usr/bin/env python3
"""Audit publication boundaries, inherited bytes, labels and native PDF builds."""
from pathlib import Path
import os,re,json,hashlib,subprocess
ROOT=Path(__file__).resolve().parent
E=ROOT/'evidence';E.mkdir(exist_ok=True)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()

def expand(p):
 return re.sub(r'\\input\{([^}]+)\}',lambda m:expand(ROOT/(m[1] if m[1].endswith('.tex') else m[1]+'.tex')),p.read_text())

main=expand(ROOT/'geometry.tex');apps=expand(ROOT/'applications.tex');archive=expand(ROOT/'archive-v144.tex')
def labels(t):return re.findall(r'\\label\{([^}]+)\}',t)
def refs(t):return set(re.findall(r'\\(?:ref|eqref|pageref)\{([^}]+)\}',t))
checks={}
checks['main_no_external_document']='\\externaldocument' not in main
checks['main_all_references_internal']=not (refs(main)-set(labels(main)))
checks['applications_references_resolve']=not (refs(apps)-set(labels(main))-set(labels(apps)))
for name,t in [('geometry',main),('applications',apps),('archive-v144',archive)]:
 checks[name+'_no_duplicate_labels']=len(labels(t))==len(set(labels(t)))
 if name=='archive-v144':checks['archive_references_resolve']=not(refs(t)-set(labels(t)))
 log=(E/(name+'-final.log')).read_text(errors='replace')
 checks[name+'_no_unresolved_references_or_citations']=not bool(re.search(r'(There were undefined references|Citation .+ undefined|Reference .+ undefined|multiply defined|Rerun to get cross-references)',log))
 checks[name+'_no_overfull_boxes']='Overfull \\hbox' not in log and 'Overfull \\vbox' not in log
 checks[name+'_native_pdf_exists']=(ROOT/(name+'.pdf')).exists()
checks['new_curve_results_present']={'thm:curve-reconstruction-v145','cor:schubert-line-reconstruction-v145'}<=set(labels(main))
checks['original_all_pencil_and_universal_results_present']={'thm:sharp-finite-pencil','thm:natural-pencil-reconstruction','thm:universal-finite-neighbourhood','thm:finite-parameter-immersion'}<=set(labels(main))
checks['no_main_critical_web_or_operator_proof'] = all(k not in labels(main) for k in ['thm:projective-critical-v144','thm:main-web-reconstruction','sec:operator-dictionary-v143'])
checks['applications_preserve_critical_and_real_theorems']={'thm:projective-critical-v144','thm:critical-ramification-v144','thm:totally-real-reciprocal-likelihood'}<=set(labels(apps))
checks['new_exact_regression_ok']=json.loads((E/'REVISION145_EXACT.json').read_text())['ok']
original=json.loads((ROOT/'INHERITED_SOURCE_V145.json').read_text())
checks['all_original_parts_and_checks_byte_identical']=all(sha(ROOT/k)==v for k,v in original['original_parts_and_checks_sha256'].items())
old=ROOT.parent/'v144'
if old.exists():
 def expold(p):return re.sub(r'\\input\{([^}]+)\}',lambda m:expold(old/(m[1] if m[1].endswith('.tex') else m[1]+'.tex')),p.read_text())
 text=expold(old/'complete.tex')
 blocks=lambda t:re.findall(r'\\begin\{(theorem|lemma|proposition|corollary|proof|equation|align)\*?\}[\s\S]*?\\end\{\1\*?\}',t)
 # Hash full environment contents, not their environment names.
 patt=r'\\begin\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}[\s\S]*?\\end\{(?:theorem|lemma|proposition|corollary|proof|equation|align)\*?\}'
 oldblocks=re.findall(patt,text);newblocks=re.findall(patt,archive)
 from collections import Counter
 checks['all_v144_mathematical_blocks_preserved_in_archive']=not(Counter(oldblocks)-Counter(newblocks))
 checks['all_v144_labels_preserved_in_archive']=set(labels(text))<=set(labels(archive))
 else_unused=None
else:raise SystemExit('Pinned predecessor is required for preservation audit')
names='exact_k3 exact_corank_two stratified_rank_two boundary_atlas generic_boundary_atlas revision131_exact revision132_exact revision133_exact revision134_exact revision135_exact revision136_exact revision137_exact revision138_exact revision139_exact revision140_exact revision141_exact revision141_spectral_exact revision141_likelihood_exact revision142_exact revision143_critical_exact revision144_projective_exact'.split()
# revision141_exact was never part of the v144 twenty-script sequence.
names.remove('revision141_exact')
checks['twenty_inherited_scripts_have_execution_logs']=all((E/(n+'.log')).exists() for n in names)
source=os.environ.get('A2_SOURCE_COMMIT','LOCAL-PREFLIGHT-NOT-A-REMOTE-SOURCE')
files={}
for p in ROOT.rglob('*'):
 if p.is_file() and 'evidence' not in p.relative_to(ROOT).parts and '__pycache__' not in p.parts and p.suffix in {'.tex','.py','.sh','.md','.json'} and p.name not in {'SOURCE_LOCK_V145.json','NONDELETION_V145.json','PROVENANCE_MANIFEST_V145.json'}:files[str(p.relative_to(ROOT))]=sha(p)
pdfs={}
for name in ['geometry','applications','archive-v144']:
 info=subprocess.check_output(['pdfinfo',str(ROOT/(name+'.pdf'))],text=True)
 pdfs[name]={'pages':int(re.search(r'^Pages:\s*(\d+)',info,re.M)[1]),'sha256':sha(ROOT/(name+'.pdf')),'bytes':(ROOT/(name+'.pdf')).stat().st_size}
result={'revision':145,'source_commit':source,'predecessor_commit':original['predecessor_commit'],'controlling_review_commit':original['review_commit'],'checks':checks,'all_checks_pass':all(checks.values()),'labels':{k:len(labels(t)) for k,t in [('geometry',main),('applications',apps),('archive',archive)]},'inherited_math_blocks':len(oldblocks),'original_parts_and_checks':len(original['original_parts_and_checks_sha256']),'executed_script_count':21,'pdfs':pdfs,'proof_certified_by_computation':False,'Ballico_1993_full_text_comparison_completed':False}
(E/'BUILD_RECEIPT_V145.json').write_text(json.dumps(result,indent=2)+'\n')
(ROOT/'SOURCE_LOCK_V145.json').write_text(json.dumps({'source_commit':source,'revision':145,'review_commit':original['review_commit'],'predecessor_commit':original['predecessor_commit'],'publication_object':'geometry.pdf only','separate_application':'applications.pdf','non_submitted_archive':'archive-v144.pdf','source_manifest':'PROVENANCE_MANIFEST_V145.json','receipt':'evidence/BUILD_RECEIPT_V145.json','historical_priority_certified':False},indent=2)+'\n')
(ROOT/'PROVENANCE_MANIFEST_V145.json').write_text(json.dumps({'source_commit':source,'sha256':files},indent=2)+'\n')
(ROOT/'NONDELETION_V145.json').write_text(json.dumps({'original_parts_and_checks':original['original_parts_and_checks_sha256'],'archive_math_blocks_preserved':checks['all_v144_mathematical_blocks_preserved_in_archive'],'archive_labels_preserved':checks['all_v144_labels_preserved_in_archive'],'archive_status':'not submitted, retained for separate review; preservation is not certification'},indent=2)+'\n')
print(json.dumps(result,indent=2))
if not all(checks.values()):raise SystemExit('v145 audit failed')
