#!/usr/bin/env python3
"""Executed source-bound build receipt, explicitly not formal proof verification."""
from pathlib import Path
import hashlib,json,re,platform,os
import fitz,sympy,numpy
ROOT=Path(__file__).resolve().parent
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
m=json.loads((ROOT/'PROVENANCE_MANIFEST.json').read_text())
def collect(driver):
    seen=set();parts=[]
    def visit(n):
        if n in seen:return
        if Path(n).is_absolute() or '..' in Path(n).parts:raise RuntimeError(n)
        seen.add(n);t=(ROOT/n).read_text();parts.append(t)
        for f in re.findall(r'\\input\{([^}]+)\}',t):visit(f)
    visit(driver+'.tex')
    text='\n'.join(parts)
    return seen,re.findall(r'\\label\{([^}]+)\}',text),text
inputs,labels,text=collect('complete');main_inputs,main_labels,main_text=collect('geometry')
supp_inputs,supp_labels,_=collect('supplement')
pdf_info={};logs={};logchecks={}
for name in ['geometry','supplement','complete']:
    p=ROOT/(name+'.pdf');log=(ROOT/(name+'.log')).read_text(errors='replace');logs[name]=log
    with fitz.open(p) as doc:
        pdf_info[name]={'pages':len(doc),'sha256':sha(p),'bytes':p.stat().st_size}
        first=doc[0].get_text()
    logchecks[name+'_title_revision136']='Revision 136' in first
    logchecks[name+'_no_undefined_references']='undefined references' not in log.lower()
    logchecks[name+'_no_undefined_citations']='undefined citations' not in log.lower()
    logchecks[name+'_no_duplicate_labels']='multiply defined' not in log.lower()
    logchecks[name+'_no_latex_errors']='! LaTeX Error' not in log and '\n! ' not in log
r136=json.loads((ROOT/'evidence/REVISION136_EXACT.json').read_text())
r135=json.loads((ROOT/'evidence/REVISION135_EXACT.json').read_text())
r134=json.loads((ROOT/'evidence/REVISION134_EXACT.json').read_text())
r133=json.loads((ROOT/'evidence/REVISION133_EXACT.json').read_text())
r132=json.loads((ROOT/'evidence/REVISION132_EXACT.json').read_text())
r131=json.loads((ROOT/'evidence/REVISION131_EXACT.json').read_text())
scripts=['exact_k3','exact_corank_two','stratified_rank_two','boundary_atlas','generic_boundary_atlas',
 'revision131_exact','revision132_exact','revision133_exact','revision134_exact','revision135_exact','revision136_exact']
checks={**logchecks,
 'focused_article_under_40_pages':pdf_info['geometry']['pages']<40,
 'complete_mathematics_retained':pdf_info['complete']['pages']>=86,
 'all_241_or_more_inherited_labels_retained':set(m['inherited_mathematical_labels'])<=set(labels),
 'no_duplicate_complete_labels':len(labels)==len(set(labels)),
 'article_supplement_label_partition':not(set(main_labels)&set(supp_labels)) and set(main_labels)|set(supp_labels)==set(labels),
 'all_source_hashes_match':all(sha(ROOT/n)==h for n,h in m['assembled_sha256'].items()),
 'accepted_universal_readout_byte_identical':all(sha(ROOT/n)==m['unchanged_inherited_tex_sha256'][n] for n in ['parts/12a-universal-readout.tex']),
 'new_proof_pivots_in_main':all(n in main_labels for n in ['lem:shear-descent','lem:orthogonal-exterior-cube','lem:schur-contraction-kernel','prop:schur-subspace-pullbacks']),
 'ambient_scheme_lemma_in_supplement':'lem:residual-cartier-sections' in supp_labels,
 'no_boundary_atlas_in_main':not any('atlas' in n or '12c-' in n or '12e-' in n for n in main_inputs),
 'full_smooth_locus_theorem_retained':'thm:main-web-reconstruction' in main_labels and 'eq:global-reconstruction-open-equality' in main_labels,
 'all_eleven_script_execution_logs_present':all((ROOT/'evidence'/(n+'.log')).exists() for n in scripts),
 'new136_exact_checks':r136['ok'],
 'uniform_theorems_and_intrinsic_repairs_in_main':all(n in main_labels for n in ['thm:uniform-contraction','thm:uniform-support-table','thm:uniform-recombination','lem:oriented-segre-descent','lem:intrinsic-residual-ideal']),
 'inherited135_exact_checks':r135['ok'] and r135['SO4_invariant_multiplicity']==0,
 'inherited134_exact_checks':r134['ok'] and r134['independent_polarization_columns']==35,
 'inherited133_exact_checks':r133['ok'],
 'inherited132_exact_checks':r132['ok'],
 'inherited131_exact_checks':r131['ok'],
 'no_control_characters_in_tex':all(not any(ord(c)<32 and c not in '\n\t\r' for c in (ROOT/n).read_text()) for n in inputs),
 'documentary_issue_not_falsely_closed':not json.loads((ROOT/'ISSUE_MATRIX.json').read_text())['Ballico_1993_full_text_obtained'],
}
receipt={'revision':136,'source_commit':m['assembly_commit'],'reviewed_commit':m['reviewed_commit'],
 'controlling_review_commit':m['controlling_review_commit'],'controlling_review':m['controlling_review'],
 'additional_review_commit':m['additional_review_commit'],
 'execution_environment':'github_actions' if os.getenv('GITHUB_ACTIONS')=='true' else 'local_preflight',
 'github_run_id':os.getenv('GITHUB_RUN_ID'),
 'review_input_sha256':m.get('review_input_sha256',{}),
 'pdfs':pdf_info,'checks':checks,'ok':all(checks.values()),
 'preserved_label_count':len(m['inherited_mathematical_labels']),'current_label_count':len(labels),
 'unchanged_inherited_tex_count':len(m['unchanged_inherited_tex_sha256']),
 'source_sha256':m['assembled_sha256'],'scripts_executed':[n+'.py' for n in scripts],
 'dependencies':{'python':platform.python_version(),'sympy':sympy.__version__,'numpy':numpy.__version__,'pymupdf':fitz.VersionBind},
 'new_exact_result':r136,
 'overfull_box_warnings':{n:[l for l in log.splitlines() if 'Overfull' in l] for n,log in logs.items()},
 'evidence_scope':{'structural_proofs_not_machine_certified':r136['structural_proofs_not_machine_certified']+r135['structural_proofs_not_machine_certified']+r134['structural_proofs_not_machine_certified'],
 'documentary_open':['R2-B135.2 / R1-B135.1: complete theorem-level comparison with Ballico 1993'],
 'not_claimed':['historically exhaustive novelty clearance','journal-issued acceptance',
 'complete higher-corank embedded-primary atlas','scheme-theoretic equality of support pullback ideals',
 'classification of the entire ambient binary-Jacobian boundary','abstract failure-scheme readout in dimensions greater than four']}}
(ROOT/'evidence/BUILD_RECEIPT.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:v for k,v in receipt.items() if k!='source_sha256'},indent=2))
if not receipt['ok']:raise SystemExit('v136 verification failed')
