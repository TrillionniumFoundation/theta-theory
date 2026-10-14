#!/usr/bin/env python3
"""Exact ordinary-source identity and finite regressions, not proof certification."""
from pathlib import Path
import hashlib,json,os,re
import verify_v41 as prior
from check_critical_packet_v42 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v41-referee-response'
BASE_TREE='20e17443eac838e4b1af93dcfb057276540e1340'
REPORT='reviews/a2-dyn-v41-external-top4-review-2026-10-08/REFEREE_REPORT.md'
REPORT_BLOB='0c1b4cea20c1aabe8a6686812a6df894c59c41db'
WORKFLOW='.github/workflows/a2-dyn-v42-qualification.yml'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==42,'revision identity')
    require(manifest['active_directory']=='papers/A2-DYN-v42-referee-response','active directory')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v41 source tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==89 and len(scripts)==103,'complete v41 corpus')
    for p in cores+scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited source '+p.name)
    require(edits['core_replacements']==[],'unexpected inherited edits')
    for rel in ('references.tex','appendices/return_statements.tex'):
        require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'inherited bibliography or synopsis')
    for name in ('main.tex','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','SOURCE_MANIFEST.json','README.md','VALIDATION.md','REFEREE_STATUS.md','REVISION_CHARTER.md','PUBLICATION_STATUS.json','INHERITED_EDITS.json','HISTORICAL_DERIVATION_AUDIT.md','SPECIALIST_AUDIT_MAP.md'):
        require((ROOT/('provenance/V41_'+name)).read_bytes()==(BASE/name).read_bytes(),'old provenance '+name)
    main=(ROOT/'main.tex').read_text();appendix=(ROOT/'appendices/return_statements.tex').read_text()
    require('October 8, 2026. A2-DYN, revision 42' in main,'main identity')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==91,'all 91 core inclusions')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    require(main.count(r'\begin{leadtheorem}')==7 and appendix.count(r'\begin{maintheorem}')==24,'principal and A--X statements')
    tex=main+'\n'+appendix+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+appendix+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label preservation')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control characters')
    require(not re.search(r'(^|\n)ef\{',tex) and r'\nef{' not in tex,'malformed reference')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()));cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(v.strip() for v in group.split(','))
    require(len(bib)==18 and cites<=bib,'bibliography/citations')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'complete payload Merkle identity')
    require(len(actual)==manifest['ordinary_payload_file_count'],'ordinary payload count')
    for key in ('full_raw_return_LLT_proved','full_return_complement_proved','common_pointwise_return_correction_proved','pointwise_roof_density_LLT_proved','independent_human_review','formal_proof_certificate','arithmetic_factor_identically_one_proved','pointwise_roof_conditioned_bridge_proved','infinite_critical_jet_sum_convergent_proved','pointwise_boundary_source_bound_proved'):
        require(manifest[key] is False,'unsupported endpoint '+key)
    for key in ('guarded_two_jet_packet_proved','finite_cutoff_summed_W21_budget_proved','pointwise_guarded_packet_inverse_proved','positive_guard_margin_jet_compatibility_proved','fixed_radius_arithmetic_phase_posterior_proved','fixed_radius_phase_bridge_product_proved','uniform_transition_interval_LLT_proved','fixed_radius_arithmetic_interval_LLT_proved'):
        require(manifest[key] is True,'missing proved result '+key)
    needed={'thm:LLT','prop:general-edge','thm:v41-uniform-transition','thm:v41-actual-return-bridge','thm:v41-zero-residue-criterion','thm:intro-v42-critical-packet','lem:v42-critical-coordinates','lem:v42-two-jet','thm:v42-regular-critical-packet','cor:v42-pointwise-packet','lem:v42-class-source','thm:v42-endpoint-posterior','cor:v42-phase-bridge-product'}
    require(needed<=set(labels),'missing theorem')
    report=ROOT.parents[1]/REPORT
    if report.exists():
        data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'controlling report blob');verified=True
    else:
        require(not os.environ.get('GITHUB_ACTIONS'),'remote source lacks controlling report');verified=False
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow identity')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'read-only qualification')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':91,'inherited_core_byte_identical':89,
            'inherited_python_byte_identical':103,'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
            'retained_introductory_theorems':24,'leading_theorems':7,'bibliography_items':18,
            'verified_file_count':len(actual),'source_payload_tree':payload_tree(ROOT),
            'controlling_report_verified':verified,'qualification_workflow_sha256':digest(wf),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':42,'source':source_checks(),'new_finite_checks':finite_checks(),
      'inherited_finite_checks':{'v41':prior.finite_checks(),'v40':prior.prior.finite_checks(),
       'v39':prior.prior.prior.finite_checks(),'v38':prior.prior.prior.prior.finite_checks(),
       'v37':prior.prior.prior.prior.prior.finite_checks()},
      'continuum_proof_certified':False,'full_raw_return_LLT_certified':False},indent=2,sort_keys=True))
