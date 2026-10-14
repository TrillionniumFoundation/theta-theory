#!/usr/bin/env python3
"""Strict exact-source verification and finite algebra; not proof certification."""
from pathlib import Path
import hashlib,json,re
import verify_v53 as prior
from check_integrability_v54 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v53-referee-response'
BASE_TREE='95d7b6f3239a487cf83f2690fb8acf84e14f1f86'
WORKFLOW='.github/workflows/a2-dyn-v54-qualification.yml'
REPORTS=prior.REPORTS
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree
compiled=prior.compiled


def require(ok,message):
    if not ok:raise RuntimeError(message)


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==54,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v53 tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==114 and len(scripts)==147,'incomplete v53 baseline')
    require(edits['core_replacements']==edits['inherited_scripts_replacements']==[],'unexpected inherited repair')
    for p in cores+scripts+list((BASE/'appendices').glob('*.tex'))+[BASE/'references.tex']:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited file '+p.name)
    archives=['main.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','VALIDATION.md',
      'PUBLICATION_STATUS.json','README.md','REFEREE_STATUS.md','REVISION_CHARTER.md','SPECIALIST_AUDIT_MAP.md',
      'HISTORICAL_DERIVATION_AUDIT.md','INHERITED_EDITS.json']
    for name in archives:
        require((ROOT/('provenance/v53-'+name)).read_bytes()==(BASE/name).read_bytes(),'provenance '+name)
    text,inputs=compiled(ROOT);oldtext,_=compiled(BASE)
    actual_cores={p for p in inputs if p.startswith('core/')}
    require(len(actual_cores)==116 and actual_cores=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'116 core inclusions')
    labels=re.findall(r'\\label\{([^}]+)\}',text);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label retention/uniqueness')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    main=(ROOT/'main.tex').read_text()
    require('October 9, 2026. A2-DYN, revision 54' in main,'revision metadata')
    require(main.count(r'\begin{leadtheorem}')==3 and text.count(r'\begin{maintheorem}')==24,'leading/A-X statements')
    for env in ['theorem','lemma','proposition','corollary','proof','leadtheorem','maintheorem','align','equation','tabular','array','aligned']:
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in text),'control character')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):cites.update(x.strip() for x in group.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    require(len(bib)==19 and cites<=bib,'bibliography/citations')
    expected={'thm:LLT','cor:v51-positive-criterion','thm:v53-same-roof-Wp','thm:v52-path-remainder',
      'lem:v54-fixed-band-windows','prop:v54-protected-height','lem:v54-tail-principle',
      'thm:v54-uniform-integrability','thm:v54-physical-Lq','thm:v54-raw-Lq','thm:v54-forward-likelihood',
      'eq:v54-admissible-exponent','eq:v54-forward-divergences'}
    require(expected<=set(labels),'missing theorem')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'ordinary payload Merkle identity')
    require(len(actual)==manifest['ordinary_payload_file_count'],'payload count')
    for key in ['full_raw_return_LLT_proved','pointwise_roof_density_LLT_proved','full_signed_correction_proved',
      'pointwise_roof_conditioned_bridge_proved','grazing_boundary_pointwise_smallness_proved',
      'clearance_boundary_pointwise_smallness_proved','arithmetic_factor_identically_one_proved',
      'independent_human_review','formal_proof_certificate','forward_essential_likelihood_convergence_proved']:
        require(manifest[key] is False,'unsupported pointwise/certification claim '+key)
    for key in ['finite_count_polynomial_protected_height_proved','complete_density_higher_integrability_proved',
      'physical_remainder_local_Lq_proved','full_source_local_Lq_LLT_proved','path_dual_roof_Lq_LLT_proved',
      'forward_likelihood_convergence_proved','forward_relative_entropy_convergence_proved',
      'forward_small_order_Renyi_convergence_proved','reverse_likelihood_convergence_proved',
      'same_roof_finite_Wasserstein_mean_proved']:
        require(manifest[key] is True,'missing proved conclusion '+key)
    checked={}
    for rel,expected_blob in REPORTS.items():
        p=ROOT.parents[1]/rel
        require(p.exists(),'missing frozen report '+rel)
        data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==expected_blob,'frozen report differs '+rel);checked[rel]=True
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'workflow privileges')
    require('--local-preflight' not in wf.read_text(),'workflow has report exception')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':116,'inherited_core_byte_identical':114,
      'inherited_python_byte_identical':147,'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
      'retained_A_X_theorems':24,'source_payload_tree':payload_tree(ROOT),'verified_file_count':len(actual),
      'frozen_reports_verified':checked,'local_preflight':False,'qualification_workflow_sha256':digest(wf),
      'source_sha256':actual}


if __name__=='__main__':
    inherited={};module=prior
    while hasattr(module,'finite_checks'):
        inherited[module.__name__]=module.finite_checks()
        if not hasattr(module,'prior') or module.__name__=='verify_v37':break
        module=module.prior
    print(json.dumps({'revision':54,'source':source_checks(),'new_finite_checks':finite_checks(),
      'inherited_finite_checks':inherited,'continuum_proof_certified':False,
      'full_pointwise_raw_return_LLT_certified':False},indent=2,sort_keys=True))
