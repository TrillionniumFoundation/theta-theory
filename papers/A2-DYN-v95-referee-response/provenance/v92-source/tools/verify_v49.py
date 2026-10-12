#!/usr/bin/env python3
"""Exact ordinary source and finite checks. No mathematical certification."""
from pathlib import Path
import hashlib,json,os,re
import verify_v48 as prior
from check_physical_v49 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v48-referee-response'
BASE_TREE='8918ca0a31f4966750326217f15b79ad71ba6df7'
REPORT='reviews/a2-dyn-v48-external-top4-review-2026-10-09/REFEREE_REPORT.md'
REPORT_BLOB='931f8f23563434275fb6d02b7077bfccda740954'
WORKFLOW='.github/workflows/a2-dyn-v49-qualification.yml'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree


def require(ok,message):
    if not ok: raise RuntimeError(message)


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()


def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==49,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v48 tree')
    cores=sorted((BASE/'core').glob('*.tex')); scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==104 and len(scripts)==131,'baseline corpus')
    for p in cores+scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited source '+p.name)
    require(edits['core_replacements']==[],'unreported core changes')
    for rel in ('references.tex','appendices/return_statements.tex'):
        require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'changed retained text '+rel)
    for name in ('main.tex','references.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md'):
        require((ROOT/('provenance/v48-'+name)).read_bytes()==(BASE/name).read_bytes(),'provenance '+name)
    main=(ROOT/'main.tex').read_text(); appendix=(ROOT/'appendices/return_statements.tex').read_text()
    retained=(ROOT/'appendices/v48_leading_statements.tex').read_text()
    oldmain=(BASE/'main.tex').read_text()
    original=oldmain[oldmain.index(r'\begin{leadtheorem}'):oldmain.index(r'\part{Action, arithmetic and the physical local law}')]
    # One ordinal reference is changed to a stable theorem label, as recorded.
    original=original.replace('in Theorem 5.','in Theorem~\\ref{thm:intro-arithmetic-return}.')
    require(retained.endswith(original),'retained leading statements')
    require('October 9, 2026. A2-DYN, revision 49' in main,'main date and revision')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==107,'all 107 core inclusions')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    tex=main+'\n'+appendix+'\n'+retained+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=oldmain+'\n'+appendix+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex); oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label retention')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined refs '+str(refs-set(labels)))
    require(retained.count(r'\begin{leadtheorem}')==11 and main.count(r'\begin{leadtheorem}')==1,'leading statements')
    require(appendix.count(r'\begin{maintheorem}')==24,'A-X retained')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control character')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text())); cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex): cites.update(v.strip() for v in group.split(','))
    require(len(bib)==18 and cites<=bib,'bibliography')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'ordinary payload Merkle tree')
    require(len(actual)==manifest['ordinary_payload_file_count'],'payload file count')
    for key in ('full_raw_return_LLT_proved','pointwise_roof_density_LLT_proved','full_signed_correction_proved',
                'pointwise_roof_conditioned_bridge_proved','grazing_boundary_pointwise_smallness_proved',
                'clearance_boundary_pointwise_smallness_proved','arithmetic_factor_identically_one_proved',
                'independent_human_review','formal_proof_certificate'):
        require(manifest[key] is False,'unsupported pointwise claim '+key)
    for key in ('physical_thin_layer_multiplier_proved','physical_marked_local_upper_proved',
                'all_depth_physical_local_variation_proved','complete_local_variation_correction_proved',
                'full_source_local_variation_LLT_proved','central_mixed_measure_TV_proved',
                'exact_window_conditional_roof_TV_proved'):
        require(manifest[key] is True,'missing new result '+key)
    required={'thm:intro-v49-local-TV','lem:v49-physical-envelope','prop:v49-physical-multiplier',
              'thm:v49-physical-marked-local','thm:v49-physical-remainder-local','cor:v49-physical-all-band',
              'thm:v49-full-local-correction','thm:v49-raw-local-TV','cor:v49-mixed-TV',
              'cor:v49-conditional-roof-TV','thm:LLT','thm:v48-two-source-reduction'}
    require(required<=set(labels),'missing key theorem')
    report=ROOT.parents[1]/REPORT; checked=False
    if report.exists():
        data=report.read_bytes(); blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'controlling report blob');checked=True
    else:
        require(os.environ.get('A2_DYN_ALLOW_MISSING_REVIEW')=='1' and not os.environ.get('GITHUB_ACTIONS'),
                'missing exact controlling review')
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'read-only workflow')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':107,'inherited_core_byte_identical':104,
            'inherited_python_byte_identical':131,'retained_mathematical_labels':len(oldlabels),
            'total_labels':len(labels),'retained_introductory_theorems':24,'retained_leading_theorems':11,
            'new_leading_theorems':1,'verified_file_count':len(actual),'source_payload_tree':payload_tree(ROOT),
            'controlling_report_verified':checked,'local_missing_review_recovery_mode':not checked,
            'qualification_workflow_sha256':digest(wf),'source_sha256':actual}


if __name__=='__main__':
    inherited={}; module=prior
    for revision in range(48,36,-1):
        inherited['v'+str(revision)]=module.finite_checks(); module=module.prior
    print(json.dumps({'revision':49,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_finite_checks':inherited,'continuum_proof_certified':False,
        'full_pointwise_raw_return_LLT_certified':False},indent=2,sort_keys=True))
