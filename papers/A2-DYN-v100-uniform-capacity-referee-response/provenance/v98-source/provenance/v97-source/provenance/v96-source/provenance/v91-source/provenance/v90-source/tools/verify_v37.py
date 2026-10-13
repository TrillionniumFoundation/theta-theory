#!/usr/bin/env python3
"""Frozen ordinary source, declared edits and finite models; not proof certification."""
from pathlib import Path
import hashlib,json,os,re
import verify_v35 as prior
from check_occupation_v37 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v35-referee-response'
BASE_TREE='1634006e867a2258b09d85db6f9fcecc668f53d1'
REPORT='reviews/a2-dyn-v36-external-top4-review-2026-10-08/REFEREE_REPORT.md'
REPORT_BLOB='a3b919fec33408b58505649125f4f74c3a9af5ef'
WORKFLOW='.github/workflows/a2-dyn-v37-qualification.yml'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==37,'revision identity')
    require(manifest['active_directory']=='papers/A2-DYN-v37-referee-response','active directory')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v35 tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==75 and len(scripts)==83,'complete v35 corpus')
    changes={}
    for item in edits['core_replacements']:changes.setdefault(item['path'],[]).append(item)
    for p in cores:
        rel=p.relative_to(BASE).as_posix();expected=p.read_text()
        for change in changes.get(rel,[]):
            require(expected.count(change['before'])==1,'unique exact edit '+rel)
            expected=expected.replace(change['before'],change['after'],1)
        require((ROOT/rel).read_text()==expected,'unrecorded inherited edit '+rel)
    for p in scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited script '+p.name)
    for rel in ['references.tex','appendices/return_statements.tex']:
        require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'inherited bibliography or synopsis')
    for rel in ['main.tex','core/72_action_norm_details.tex','core/74_compact_family_local_principle.tex']:
        require((ROOT/'provenance'/('V35_'+Path(rel).name)).read_bytes()==(BASE/rel).read_bytes(),'provenance '+rel)
    main=(ROOT/'main.tex').read_text();appendix=(ROOT/'appendices/return_statements.tex').read_text()
    require('October 8, 2026. A2-DYN, revision 37' in main,'main identity')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==79,'complete core inclusion')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core source')
    require(main.count(r'\begin{leadtheorem}')==3 and appendix.count(r'\begin{maintheorem}')==24,'principal results and A--X')
    tex=main+'\n'+appendix+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+appendix+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label preservation')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control characters')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()));cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(v.strip() for v in group.split(','))
    require(len(bib)==18 and cites<=bib,'bibliography and citations')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'complete source Merkle identity')
    require(len(actual)==manifest['ordinary_payload_file_count'],'ordinary payload count')
    for key in ('full_raw_return_LLT_proved','full_return_complement_proved','common_pointwise_return_correction_proved',
                'arbitrary_selected_path_Gaussian_amplitude_proved','microscopic_conditional_path_bridge_proved',
                'independent_human_review','formal_proof_certificate'):
        require(manifest[key] is False,'unsupported endpoint '+key)
    for key in ('exact_section_multiplier_proved','mixed_occupation_local_central_limit_proved',
                'actual_return_window_local_limit_proved','noncircular_strong_faithfulness_endpoint',
                'finite_cover_mixing_input_verified','nonelliptic_support_family_verified'):
        require(manifest[key] is True,'missing new result '+key)
    needed={'thm:LLT','lem:v35-faithful-strong','thm:v35-action-family-LLT','lem:v37-section-multiplier',
            'thm:v37-occupation-local-central','prop:v37-exact-return-disintegration',
            'thm:v37-return-window','prop:v37-finite-cover-mixing','prop:v37-support-family'}
    require(needed<=set(labels),'missing proof-chain label')
    report=ROOT.parents[1]/REPORT
    if report.exists():
        data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'controlling report blob');verified=True
    else:
        require(not os.environ.get('GITHUB_ACTIONS'),'remote source lacks controlling report');verified=False
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow identity')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'read-only qualification')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':79,'inherited_core_byte_identical':75-len(changes),
        'inherited_core_exactly_edited':sorted(changes),'exact_core_replacements':len(edits['core_replacements']),
        'inherited_python_byte_identical':83,'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
        'retained_introductory_theorems':24,'leading_theorems':3,'bibliography_items':18,
        'verified_file_count':len(actual),'source_payload_tree':payload_tree(ROOT),
        'controlling_report_verified':verified,'qualification_workflow_sha256':digest(wf),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':37,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_finite_checks':{'v35':prior.finite_checks(),'v34':prior.prior.finite_checks()},
        'continuum_proof_certified':False,'full_raw_return_LLT_certified':False},indent=2,sort_keys=True))
