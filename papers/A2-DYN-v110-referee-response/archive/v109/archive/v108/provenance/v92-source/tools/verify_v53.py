#!/usr/bin/env python3
"""Verify exact ordinary source, frozen reports and finite algebra."""
from pathlib import Path
import argparse,hashlib,json,os,re
import verify_v52 as prior
from check_transport_v53 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v52-referee-response'
BASE_TREE='a5f687493f1f574c700cf28c10f24f25841ad0d7'
WORKFLOW='.github/workflows/a2-dyn-v53-qualification.yml'
REPORTS={
 'reviews/a2-dyn-v49-external-top4-review-2026-10-09/REFEREE_REPORT.md':'cad56babdd60f941c0e554dc88c99e90c20335b4',
 'reviews/a2-dyn-v50-external-top4-review-2026-10-09/REFEREE_REPORT.md':'fa4b5109f7c38d8286f93cd723d6c751378df439',
 'reviews/a2-dyn-v51-external-top4-review-2026-10-09/REFEREE_REPORT.md':'a46a201ebef4fcc56e4b80df5494d7358389e42a',
 'reviews/a2-dyn-v52-external-top4-review-2026-10-09/REFEREE_REPORT.md':'9f50c9909cc137d67babfd69f6508de2ce3254cf'}
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree


def require(ok,message):
    if not ok: raise RuntimeError(message)


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def compiled(root):
    seen=[]
    def read(rel):
        if not rel.endswith('.tex'): rel+='.tex'
        require(rel not in seen,'duplicate inclusion '+rel);seen.append(rel)
        text=(root/rel).read_text()
        return text+'\n'+'\n'.join(read(p) for p in re.findall(r'\\input\{([^}]+)\}',text))
    return read('main.tex'),seen


def source_checks(local_preflight=False):
    require(not local_preflight,'v53 requires all frozen reports; no preflight exception')
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==53,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen full v52 tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==111 and len(scripts)==143,'incomplete baseline')
    replacements=edits['core_replacements']
    changed={r['path'] for r in replacements}
    require(changed=={'core/110_path_valued_raw_inversion.tex','core/111_same_roof_conditional_bridges.tex'},'unexpected edited core')
    for p in cores:
        rel=p.relative_to(BASE).as_posix();data=p.read_text()
        for r in replacements:
            if r['path']==rel:
                require(data.count(r['old'])==r['occurrences']==1,'nonunique repair '+rel)
                data=data.replace(r['old'],r['new'],1)
        require(data.encode()==(ROOT/rel).read_bytes(),'unexpected inherited change '+rel)
    for p in scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited script '+p.name)
    require(edits['inherited_scripts_replacements']==[],'inherited script replacement')
    for p in (BASE/'appendices').glob('*.tex'):
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed compiled appendix')
    oldbib=(BASE/'references.tex').read_text();newbib=(ROOT/'references.tex').read_text()
    prefix,suffix=oldbib.split(r'\end{thebibliography}')
    require(newbib.startswith(prefix) and newbib.endswith(r'\end{thebibliography}'+suffix),'inherited bibliography modified')
    for name in ('main.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','VALIDATION.md','PUBLICATION_STATUS.json','references.tex'):
        require((ROOT/('provenance/v52-'+name)).read_bytes()==(BASE/name).read_bytes(),'provenance '+name)
    for rel in changed:
        require((ROOT/('provenance/v52-core-'+Path(rel).name)).read_bytes()==(BASE/rel).read_bytes(),'archived core '+rel)
    text,inputs=compiled(ROOT);oldtext,oldinputs=compiled(BASE)
    actual_cores={p for p in inputs if p.startswith('core/')}
    require(len(actual_cores)==114 and actual_cores=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'114 core inclusions')
    labels=re.findall(r'\\label\{([^}]+)\}',text);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label identity/retention')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined refs '+str(refs-set(labels)))
    main=(ROOT/'main.tex').read_text()
    require('October 9, 2026. A2-DYN, revision 53' in main,'revision metadata')
    require(main.count(r'\begin{leadtheorem}')==3,'three leading theorems')
    require(text.count(r'\begin{maintheorem}')==24,'A-X retained')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in text),'control character')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):cites.update(v.strip() for v in group.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    require(len(bib)==19 and cites<=bib,'bibliography/citations')
    required={'thm:intro-v51-lower','lem:v51-local-convolution-height','prop:v51-positive-principle',
       'thm:v51-positive-error','cor:v51-positive-criterion','cor:v51-lower-denominators',
       'thm:v51-conditional-minorization','app:v51-input-map','thm:LLT',
       'thm:intro-v52-path','lem:v52-path-endpoint-budget','lem:v52-fixed-band-path',
       'thm:v52-path-remainder','lem:v52-return-transfer','thm:v52-same-roof-mean',
       'prop:v52-pointwise-path-charge','lem:v53-signed-compactness','thm:v53-abstract-transfer',
       'lem:v53-factorial-derivatives','prop:v53-all-increment-moments','thm:v53-exponential-maximal',
       'cor:v53-exponential-defect','thm:v53-unbounded-raw-paths','lem:v53-transport-upgrade',
       'thm:v53-same-roof-Wp','cor:v53-conditional-moments'}
    require(required<=set(labels),'missing theorem')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'ordinary payload Merkle tree')
    require(len(actual)==manifest['ordinary_payload_file_count'],'payload count')
    for key in ('full_raw_return_LLT_proved','pointwise_roof_density_LLT_proved','full_signed_correction_proved',
      'pointwise_roof_conditioned_bridge_proved','grazing_boundary_pointwise_smallness_proved',
      'clearance_boundary_pointwise_smallness_proved','arithmetic_factor_identically_one_proved',
      'independent_human_review','formal_proof_certificate','forward_likelihood_convergence_proved'):
        require(manifest[key] is False,'unsupported complete endpoint '+key)
    for key in ('pointwise_lower_local_law_proved','positive_physical_error_representation_proved',
       'positive_physical_height_equivalence_proved','fixed_band_smoothed_physical_height_proved',
       'essential_roof_denominator_lower_bound_proved','exact_window_conditional_minorization_proved',
       'reverse_likelihood_convergence_proved','path_valued_raw_local_variation_proved',
       'same_roof_conditional_bridge_in_mean_proved','common_positive_path_remainder_proved',
       'scalar_height_suffices_for_pointwise_bridge_proved',
       'factorial_all_order_pinned_moments_proved','exponential_pinned_path_moment_proved',
       'polynomial_growth_raw_path_law_proved','same_roof_finite_Wasserstein_mean_proved',
       'exponential_physical_defect_local_moment_proved','reusable_positive_path_transfer_proved'):
        require(manifest[key] is True,'missing new result '+key)
    checked={};missing=[]
    for rel,expected in REPORTS.items():
        report=ROOT.parents[1]/rel
        if not report.exists():
            require(local_preflight,'missing frozen report '+rel);missing.append(rel);checked[rel]=False
        else:
            data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
            require(blob==expected,'frozen report differs '+rel);checked[rel]=True
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'workflow write permission')
    require('--local-preflight' not in wf.read_text(),'workflow uses local exception')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':114,'inherited_core_byte_identical':109,'inherited_core_exactly_repaired':2,
       'inherited_python_byte_identical':143,'retained_mathematical_labels':len(oldlabels),
       'total_labels':len(labels),'inherited_leading_theorems':oldtext.count(r'\begin{leadtheorem}'),
       'retained_A_X_theorems':24,'source_payload_tree':payload_tree(ROOT),'verified_file_count':len(actual),
       'frozen_reports_verified':checked,'missing_reports':missing,'local_preflight':local_preflight,
       'qualification_workflow_sha256':digest(wf),'source_sha256':actual}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--local-preflight',action='store_true');args=parser.parse_args()
    inherited={'v52':prior.finite_checks(),'v51':prior.prior.finite_checks(),'v49':prior.prior.prior.finite_checks()}
    module=prior.prior.prior.prior
    for revision in range(48,36,-1):
        inherited['v'+str(revision)]=module.finite_checks();module=module.prior
    print(json.dumps({'revision':53,'source':source_checks(args.local_preflight),'new_finite_checks':finite_checks(),
       'inherited_finite_checks':inherited,'continuum_proof_certified':False,'full_pointwise_raw_return_LLT_certified':False},indent=2,sort_keys=True))
