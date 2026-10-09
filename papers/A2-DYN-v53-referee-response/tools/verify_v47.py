#!/usr/bin/env python3
"""Check the full ordinary source and finite regressions; never certify continuum proofs."""
from pathlib import Path
import hashlib, json, os, re
import verify_v46 as prior
from check_endpoint_boundary_v47 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v46-referee-response'
BASE_TREE='9bea85c50917e3f3de1410cb140cdce9966d6f8d'
REPORT='reviews/a2-dyn-v46-external-top4-review-2026-10-08/REFEREE_REPORT.md'
REPORT_BLOB='b222d90012ac419cd0cfe3b09a21e680da672205'
WORKFLOW='.github/workflows/a2-dyn-v47-qualification.yml'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree


def require(ok,message):
    if not ok: raise RuntimeError(message)


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==47, 'revision identity')
    require(manifest['active_directory']=='papers/A2-DYN-v47-referee-response', 'active directory')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'], 'frozen v46 paper tree')
    cores=sorted((BASE/'core').glob('*.tex')); scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==99 and len(scripts)==123, 'complete baseline corpus')
    for p in cores+scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(), 'changed inherited source '+p.name)
    require(edits['core_replacements']==[], 'unreported inherited edit')
    for rel in ('references.tex','appendices/return_statements.tex'):
        require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(), 'changed bibliography/synopsis')
    for name in ('main.tex','references.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md'):
        require((ROOT/('provenance/v46-'+name)).read_bytes()==(BASE/name).read_bytes(), 'provenance '+name)
    main=(ROOT/'main.tex').read_text(); appendix=(ROOT/'appendices/return_statements.tex').read_text()
    require('October 8, 2026. A2-DYN, revision 47' in main, 'main identity')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}', main)
    require(len(inputs)==len(set(inputs))==101, 'all 101 core inclusions')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')}, 'unlisted core')
    require(main.count(r'\begin{leadtheorem}')==10 and appendix.count(r'\begin{maintheorem}')==24, 'theorem synopses')
    tex=main+'\n'+appendix+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+appendix+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex); oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels), 'label retention')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels), 'undefined references '+str(refs-set(labels)))
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'), 'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex), 'control character')
    require(not re.search(r'(^|\n)ef\{',tex) and r'\nef{' not in tex, 'malformed reference')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text())); cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex): cites.update(v.strip() for v in group.split(','))
    require(len(bib)==18 and cites<=bib, 'bibliography/citations')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'], 'complete payload Merkle identity')
    require(len(actual)==manifest['ordinary_payload_file_count'], 'payload file count')
    for key in ('full_raw_return_LLT_proved','full_return_complement_proved','common_pointwise_return_correction_proved',
                'pointwise_roof_density_LLT_proved','independent_human_review','formal_proof_certificate',
                'arithmetic_factor_identically_one_proved','pointwise_roof_conditioned_bridge_proved',
                'central_scale_boundary_source_smallness_proved','full_signed_correction_proved',
                'prescribed_count_dependent_protection_rate_proved','global_noncritical_inverse_proved',
                'grazing_boundary_pointwise_smallness_proved','clearance_boundary_pointwise_smallness_proved',
                'interior_decision_boundary_pointwise_smallness_proved'):
        require(manifest[key] is False, 'unsupported endpoint '+key)
    for key in ('protected_complete_signed_correction_proved','endpoint_decision_density_smallness_proved',
                'endpoint_decision_all_band_correction_proved','bounded_insertion_endpoint_boundary_proved',
                'positive_first_bad_margin_decomposition_proved','ordered_bandwidth_endpoint_depth_proved'):
        require(manifest[key] is True, 'missing qualified result '+key)
    required={'thm:LLT','thm:v41-uniform-transition','thm:v43-arithmetic-raw-criterion',
              'thm:v46-protected-correction','thm:v46-boundary-reduction',
              'lem:v47-small-endpoint-local','lem:v47-endpoint-envelopes',
              'lem:v47-free-decision-continuation','prop:v47-high-gradient-boundary',
              'lem:v47-free-critical-cluster','thm:v47-endpoint-boundary-smallness',
              'cor:v47-endpoint-jumps','prop:v47-first-defect-masses',
              'thm:v47-ordered-boundary-removal','cor:v47-arithmetic-residual',
              'thm:intro-v47-boundary-decisions'}
    require(required<=set(labels),'missing theorem')
    report=ROOT.parents[1]/REPORT
    checked=False
    if report.exists():
        data=report.read_bytes(); blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'], 'controlling report identity')
        checked=True
    else:
        # Explicit local-only recovery mode; CI always requires the actual report bytes.
        require(os.environ.get('A2_DYN_ALLOW_MISSING_REVIEW')=='1' and not os.environ.get('GITHUB_ACTIONS'),
                'missing controlling review; not an exact qualified packet')
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'], 'workflow identity')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(), 'read-only qualification')
    return {'baseline_paper_tree':BASE_TREE, 'included_core_files':101,
            'inherited_core_byte_identical':99, 'inherited_python_byte_identical':123,
            'retained_mathematical_labels':len(oldlabels), 'total_labels':len(labels),
            'retained_introductory_theorems':24, 'leading_theorems':10,
            'bibliography_items':18, 'verified_file_count':len(actual),
            'source_payload_tree':payload_tree(ROOT), 'controlling_report_verified':checked,
            'local_missing_review_recovery_mode':not checked,
            'qualification_workflow_sha256':digest(wf), 'source_sha256':actual}


if __name__=='__main__':
    inherited={}; module=prior
    for revision in range(46,36,-1):
        inherited['v'+str(revision)]=module.finite_checks(); module=module.prior
    print(json.dumps({'revision':47,'source':source_checks(), 'new_finite_checks':finite_checks(),
       'inherited_finite_checks':inherited,'continuum_proof_certified':False,
       'full_raw_return_LLT_certified':False},indent=2,sort_keys=True))
