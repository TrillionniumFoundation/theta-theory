#!/usr/bin/env python3
"""Verify exact ordinary source, frozen reports and finite algebra."""
from pathlib import Path
import argparse,hashlib,json,os,re
import verify_v49 as prior
from check_positive_v51 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v49-referee-response'
BASE_TREE='c583e9f175d668a427759812ac84dcca25259132'
WORKFLOW='.github/workflows/a2-dyn-v51-qualification.yml'
REPORTS={
 'reviews/a2-dyn-v49-external-top4-review-2026-10-09/REFEREE_REPORT.md':'cad56babdd60f941c0e554dc88c99e90c20335b4',
 'reviews/a2-dyn-v50-external-top4-review-2026-10-09/REFEREE_REPORT.md':'fa4b5109f7c38d8286f93cd723d6c751378df439'}
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
    require(not(local_preflight and os.environ.get('GITHUB_ACTIONS')),'local mode forbidden remotely')
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==51,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen full v49 tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==107 and len(scripts)==135,'incomplete baseline')
    for p in cores+scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited source '+p.name)
    require(edits['core_replacements']==edits['inherited_scripts_replacements']==[],'inherited replacement')
    for p in [BASE/'references.tex']+list((BASE/'appendices').glob('*.tex')):
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed retained appendix/bibliography')
    for name in ('main.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','VALIDATION.md','PUBLICATION_STATUS.json'):
        require((ROOT/('provenance/v49-'+name)).read_bytes()==(BASE/name).read_bytes(),'provenance '+name)
    text,inputs=compiled(ROOT);oldtext,oldinputs=compiled(BASE)
    actual_cores={p for p in inputs if p.startswith('core/')}
    require(len(actual_cores)==109 and actual_cores=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'109 core inclusions')
    labels=re.findall(r'\\label\{([^}]+)\}',text);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label identity/retention')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined refs '+str(refs-set(labels)))
    main=(ROOT/'main.tex').read_text()
    require('October 9, 2026. A2-DYN, revision 51' in main,'revision metadata')
    require(main.count(r'\begin{leadtheorem}')==2,'two leading theorems')
    require(text.count(r'\begin{maintheorem}')==24,'A-X retained')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in text),'control character')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):cites.update(v.strip() for v in group.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()))
    require(len(bib)==18 and cites<=bib,'bibliography/citations')
    required={'thm:intro-v51-lower','lem:v51-local-convolution-height','prop:v51-positive-principle',
       'thm:v51-positive-error','cor:v51-positive-criterion','cor:v51-lower-denominators',
       'thm:v51-conditional-minorization','app:v51-input-map','thm:LLT'}
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
       'reverse_likelihood_convergence_proved'):
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
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':109,'inherited_core_byte_identical':107,
       'inherited_python_byte_identical':135,'retained_mathematical_labels':len(oldlabels),
       'total_labels':len(labels),'inherited_leading_theorems':oldtext.count(r'\begin{leadtheorem}'),
       'retained_A_X_theorems':24,'source_payload_tree':payload_tree(ROOT),'verified_file_count':len(actual),
       'frozen_reports_verified':checked,'missing_reports':missing,'local_preflight':local_preflight,
       'qualification_workflow_sha256':digest(wf),'source_sha256':actual}


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--local-preflight',action='store_true');args=parser.parse_args()
    inherited={'v49':prior.finite_checks()};module=prior.prior
    for revision in range(48,36,-1):
        inherited['v'+str(revision)]=module.finite_checks();module=module.prior
    print(json.dumps({'revision':51,'source':source_checks(args.local_preflight),'new_finite_checks':finite_checks(),
       'inherited_finite_checks':inherited,'continuum_proof_certified':False,'full_pointwise_raw_return_LLT_certified':False},indent=2,sort_keys=True))
