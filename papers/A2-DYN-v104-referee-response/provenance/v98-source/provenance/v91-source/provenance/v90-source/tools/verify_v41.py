#!/usr/bin/env python3
"""Exact ordinary-source identity and finite tests. Not a continuum proof certificate."""
from pathlib import Path
import hashlib,json,os,re
import verify_v40 as prior
from check_transition_bridge_v41 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v40-referee-response'
BASE_TREE='647d3d842655bf71e1d64afdc3321b016c190229'
REPORT='reviews/a2-dyn-v39-external-top4-review-2026-10-08/REFEREE_REPORT.md'
REPORT_BLOB='34fd05b1740816104f38ca84c75826b11eec1694'
WORKFLOW='.github/workflows/a2-dyn-v41-qualification.yml'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree

def require(ok,message):
    if not ok: raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==41,'revision identity')
    require(manifest['active_directory']=='papers/A2-DYN-v41-referee-response','active directory')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v40 tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==86 and len(scripts)==99,'complete v40 corpus')
    for p in cores+scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited source '+p.name)
    require(edits['core_replacements']==[],'no inherited core modification permitted')
    for rel in ['references.tex','appendices/return_statements.tex']:
        require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'inherited bibliography or synopsis')
    for name in ('main.tex','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','SOURCE_MANIFEST.json','README.md','VALIDATION.md'):
        require((ROOT/('provenance/V40_'+name)).read_bytes()==(BASE/name).read_bytes(),'old provenance '+name)
    main=(ROOT/'main.tex').read_text();appendix=(ROOT/'appendices/return_statements.tex').read_text()
    require('October 8, 2026. A2-DYN, revision 41' in main,'main identity')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==89,'all 89 core inclusions')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    require(main.count(r'\begin{leadtheorem}')==6 and appendix.count(r'\begin{maintheorem}')==24,'principal results and A--X')
    tex=main+'\n'+appendix+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+appendix+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label preservation')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control characters')
    require(not re.search(r'(^|\n)ef\{',tex), 'split reference command')
    require(r'\nef{' not in tex, 'malformed reference command')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()));cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(v.strip() for v in group.split(','))
    require(len(bib)==18 and cites<=bib,'bibliography/citations')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'complete source Merkle identity')
    require(len(actual)==manifest['ordinary_payload_file_count'],'ordinary payload count')
    for key in ('full_raw_return_LLT_proved','full_return_complement_proved','common_pointwise_return_correction_proved',
                'exact_return_index_Gaussian_asymptotic_proved','full_occupation_torus_cancellation_proved',
                'pointwise_roof_density_LLT_proved','independent_human_review','formal_proof_certificate',
                'arithmetic_factor_identically_one_proved','pointwise_roof_conditioned_bridge_proved'):
        require(manifest[key] is False,'unsupported endpoint '+key)
    for key in ('single_return_index_concentration_upper_proved','arbitrarily_slow_diverging_return_windows_proved',
                'original_covariance_normalization_proved','exact_fixed_torus_remainder_identity_proved',
                'measurable_resonance_group_classified','section_source_spectral_cancellation_proved',
                'pure_occupation_Abel_estimate_proved','full_fixed_band_occupation_power_bounds_proved',
                'nonzero_roof_resonances_excluded','all_resonance_endpoint_residues_proved',
                'uniform_fixed_band_resonant_reduction_proved','fixed_radius_arithmetic_interval_LLT_proved',
                'uniform_transition_interval_LLT_proved','uniform_exact_event_bridge_with_denominator_proved',
                'fixed_radius_positive_class_bridge_proved','fixed_finite_packet_LLT_proved',
                'zero_section_residue_criterion_proved','existential_shrinking_roof_interval_proved'):
        require(manifest[key] is True,'missing result '+key)
    needed={'thm:v39-resonance-structure','thm:v39-section-source','thm:v39-abel-section','prop:v39-induced-arithmetic','thm:LLT','thm:v37-return-window','thm:v38-singleton-concentration','thm:v38-occupation-mesoscopic',
            'thm:v38-fine-return-windows','prop:v38-exact-index-remainder','lem:v38-product-envelopes','thm:intro-arithmetic-return',
            'lem:v40-linear-cuts','lem:v40-occupation-matching','thm:v40-polynomial-LY',
            'thm:v40-full-peripheral','thm:v40-no-roof-resonance','prop:v40-general-residue',
            'prop:v40-resonant-curvature','thm:v40-uniform-resonant-reduction',
            'thm:v40-arithmetic-return-LLT','cor:v40-explicit-fixed-complement'}
    needed.update({'thm:intro-v41-bridge','lem:v41-scalar-continuity','lem:v41-moving-maxima',
                   'thm:v41-uniform-transition','cor:v41-shrinking-roof','lem:v41-pinned-factorization',
                   'lem:v41-peak-derivatives','prop:v41-pinned-fourth',
                   'thm:v41-collision-conditional-bridge','thm:v41-actual-return-bridge',
                   'thm:v41-zero-residue-criterion','thm:v41-finite-packet'})
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
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':89,'inherited_core_byte_identical':86,
            'inherited_python_byte_identical':99,'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
            'retained_introductory_theorems':24,'leading_theorems':6,'bibliography_items':18,
            'verified_file_count':len(actual),'source_payload_tree':payload_tree(ROOT),
            'controlling_report_verified':verified,'qualification_workflow_sha256':digest(wf),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':41,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_finite_checks':{'v40':prior.finite_checks(),'v39':prior.prior.finite_checks(),
                                 'v38':prior.prior.prior.finite_checks(),
                                 'v37':prior.prior.prior.prior.finite_checks()},
        'continuum_proof_certified':False,'full_raw_return_LLT_certified':False},indent=2,sort_keys=True))
