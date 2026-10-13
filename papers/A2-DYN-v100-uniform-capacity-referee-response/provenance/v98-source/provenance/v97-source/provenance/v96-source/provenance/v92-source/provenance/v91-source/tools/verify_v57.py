#!/usr/bin/env python3
"""Strict exact-source verification and finite algebra; not proof certification."""
from pathlib import Path
import argparse,hashlib,json,os,re
import verify_v56 as prior
from check_global_v57 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v56-referee-response'
BASE_TREE='c3210ca54af8edb21aa048796172a13832d1335f'
WORKFLOW='.github/workflows/a2-dyn-v57-qualification.yml'
REPORTS=dict(prior.REPORTS)
REPORTS['reviews/a2-dyn-v56-external-top4-review-2026-10-09/REFEREE_REPORT.md']='01e36e830daee2b04036320b562990f9daf47485'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree
compiled=prior.compiled


def require(ok,message):
    if not ok:raise RuntimeError(message)


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def source_checks(local_preflight=False):
    require(not (local_preflight and os.environ.get('GITHUB_ACTIONS')),'preflight forbidden in Actions')
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==57,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v56 tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==120 and len(scripts)==159,'incomplete v56 baseline')
    require(edits['core_replacements']==edits['inherited_scripts_replacements']==[],'unexpected inherited repair')
    for p in cores+scripts+list((BASE/'appendices').glob('*.tex'))+[BASE/'references.tex']:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited file '+p.name)
    archives=['main.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','VALIDATION.md',
      'PUBLICATION_STATUS.json','README.md','REFEREE_STATUS.md','REVISION_CHARTER.md','SPECIALIST_AUDIT_MAP.md',
      'HISTORICAL_DERIVATION_AUDIT.md','INHERITED_EDITS.json']
    for name in archives:
        require((ROOT/('provenance/v56-'+name)).read_bytes()==(BASE/name).read_bytes(),'provenance '+name)
    oldmain=(BASE/'main.tex').read_text()
    oldfront=oldmain.split(r'\maketitle',1)[1].split(r'\part{Action, arithmetic',1)[0]
    moved=(ROOT/'appendices/v56_frontmatter.tex').read_text()
    require(moved.endswith(oldfront),'front-matter move changed old text')
    text,inputs=compiled(ROOT);oldtext,_=compiled(BASE)
    actual_cores={p for p in inputs if p.startswith('core/')}
    require(len(actual_cores)==122 and actual_cores=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'122 core inclusions')
    labels=re.findall(r'\\label\{([^}]+)\}',text);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label retention/uniqueness')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    main=(ROOT/'main.tex').read_text()
    require('October 9, 2026. A2-DYN, revision 57' in main,'revision metadata')
    require(main.count(r'\begin{leadtheorem}')==1 and text.count(r'\begin{leadtheorem}')==oldtext.count(r'\begin{leadtheorem}')+1 and text.count(r'\begin{maintheorem}')==24,'leading/A-X statements')
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
      'eq:v54-admissible-exponent','eq:v54-forward-divergences',
      'lem:v55-global-layer','lem:v55-two-regimes','thm:v55-error-free-mass',
      'thm:v55-endpoint-principle','cor:v55-physical-endpoint','thm:v55-physical-remainders',
      'thm:v55-raw-endpoint','thm:v55-endpoint-likelihood',
      'lem:v56-covering','thm:v56-finite-maximal','cor:v56-ordered-localization',
      'thm:v56-all-resolutions','cor:v56-interval-posteriors','cor:v56-anchor-probability',
      'thm:v56-return-maximal'}
    expected.update({'lem:v57-centered-pressure','thm:v57-damped-drift','lem:v57-transition-envelope',
      'thm:v57-global-raw-TV','cor:v57-fixed-radius-raw','lem:v57-joint-local','thm:v57-global-coupled',
      'thm:v57-selection','thm:intro-v57-global','app:v57-retained-front'})
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
    for key in ['pressure_drift_damping_proved','global_transition_gaussian_envelope_proved',
      'untruncated_mixed_TV_proved','joint_collision_return_graph_bridge_proved',
      'record_observation_postselection_proved']:
        require(manifest[key] is True,'missing new conclusion '+key)
    checked={}
    for rel,expected_blob in REPORTS.items():
        p=ROOT.parents[1]/rel
        if not p.exists() and local_preflight and 'a2-dyn-v56-external' in rel:
            checked[rel]=False
            continue
        require(p.exists(),'missing frozen report '+rel)
        data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==expected_blob,'frozen report differs '+rel);checked[rel]=True
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'workflow privileges')
    require('--local-preflight' not in wf.read_text(),'workflow has report exception')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':122,'inherited_core_byte_identical':120,
      'inherited_python_byte_identical':159,'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
      'retained_A_X_theorems':24,'source_payload_tree':payload_tree(ROOT),'verified_file_count':len(actual),
      'frozen_reports_verified':checked,'local_preflight':local_preflight,'qualification_workflow_sha256':digest(wf),
      'source_sha256':actual}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--local-preflight',action='store_true')
    args=parser.parse_args()
    inherited={};module=prior
    while hasattr(module,'finite_checks'):
        inherited[module.__name__]=module.finite_checks()
        if not hasattr(module,'prior') or module.__name__=='verify_v37':break
        module=module.prior
    print(json.dumps({'revision':57,'source':source_checks(args.local_preflight),'new_finite_checks':finite_checks(),
      'inherited_finite_checks':inherited,'continuum_proof_certified':False,
      'full_pointwise_raw_return_LLT_certified':False},indent=2,sort_keys=True))
