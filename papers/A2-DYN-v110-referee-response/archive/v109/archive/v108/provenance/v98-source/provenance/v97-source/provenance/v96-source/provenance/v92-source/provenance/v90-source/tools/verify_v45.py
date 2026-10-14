#!/usr/bin/env python3
"""Exact ordinary-source checks and finite regressions, not proof certification."""
from pathlib import Path
import hashlib,json,os,re
import verify_v44 as prior
from check_critical_collars_v45 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v44-referee-response'
BASE_TREE='4424a31936f55a927e360b9818ae2a0fc183eaba'
REPORT='reviews/a2-dyn-v43-external-top4-review-2026-10-08/REFEREE_REPORT.md'
REPORT_BLOB='6d223bd63ddd76a5a2efc3351c475d0261e93839'
WORKFLOW='.github/workflows/a2-dyn-v45-qualification.yml'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree


def require(ok,message):
    if not ok:raise RuntimeError(message)


def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()


def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==45,'revision identity')
    require(manifest['active_directory']=='papers/A2-DYN-v45-referee-response','active directory')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v44 paper tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==95 and len(scripts)==115,'complete v44 corpus')
    for p in cores+scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited source '+p.name)
    require(edits['core_replacements']==[],'unexpected inherited edit')
    for rel in ('references.tex','appendices/return_statements.tex'):
        require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'changed bibliography or synopsis')
    for name in ('main.tex','references.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md'):
        require((ROOT/('provenance/v44-'+name)).read_bytes()==(BASE/name).read_bytes(),'old provenance '+name)
    main=(ROOT/'main.tex').read_text();appendix=(ROOT/'appendices/return_statements.tex').read_text()
    require('October 8, 2026. A2-DYN, revision 45' in main,'main identity')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==97,'all 97 core inclusions')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    require(main.count(r'\begin{leadtheorem}')==8 and appendix.count(r'\begin{maintheorem}')==24,'principal and A--X statements')
    tex=main+'\n'+appendix+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+appendix+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label preservation')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control character')
    require(not re.search(r'(^|\n)ef\{',tex) and r'\nef{' not in tex,'malformed reference')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()));cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(v.strip() for v in group.split(','))
    require(len(bib)==18 and cites<=bib,'bibliography/citations')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'complete payload Merkle identity')
    require(len(actual)==manifest['ordinary_payload_file_count'],'ordinary payload count')
    for key in ('full_raw_return_LLT_proved','full_return_complement_proved','common_pointwise_return_correction_proved','pointwise_roof_density_LLT_proved','independent_human_review','formal_proof_certificate','arithmetic_factor_identically_one_proved','pointwise_roof_conditioned_bridge_proved','central_scale_boundary_source_smallness_proved','full_signed_correction_proved'):
        require(manifest[key] is False,'unsupported endpoint '+key)
    for key in ('graded_margin_endpoint_collars_proved','relative_critical_source_distortion_proved','two_normal_strip_local_upper_bound_proved','intrinsic_critical_cluster_deconcentration_proved','protected_critical_source_pointwise_smallness_proved','protected_critical_all_band_smallness_proved'):
        require(manifest[key] is True,'missing v45 result '+key)
    required={'thm:LLT','thm:v41-uniform-transition','thm:v43-arithmetic-raw-criterion','thm:v44-complete-density-bound','thm:v44-jump-cusp-extraction','prop:general-edge','thm:intro-v45-critical-cluster','lem:v45-endpoint-collar','lem:v45-relative-distortion','prop:v45-mass-collar','lem:v45-two-strip-local','thm:v45-critical-cluster','thm:v45-critical-source-smallness','cor:v45-critical-unsmoothing'}
    require(required<=set(labels),'missing theorem')
    report=ROOT.parents[1]/REPORT
    require(report.exists(),'missing controlling report')
    data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'report identity')
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow identity')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'read-only qualification')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':97,'inherited_core_byte_identical':95,
       'inherited_python_byte_identical':115,'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
       'retained_introductory_theorems':24,'leading_theorems':8,'bibliography_items':18,
       'verified_file_count':len(actual),'source_payload_tree':payload_tree(ROOT),'controlling_report_verified':True,
       'qualification_workflow_sha256':digest(wf),'source_sha256':actual}


if __name__=='__main__':
    inherited={};module=prior
    for revision in range(44,36,-1):
        inherited['v'+str(revision)]=module.finite_checks();module=module.prior
    print(json.dumps({'revision':45,'source':source_checks(),'new_finite_checks':finite_checks(),
       'inherited_finite_checks':inherited,'continuum_proof_certified':False,
       'full_raw_return_LLT_certified':False},indent=2,sort_keys=True))
