#!/usr/bin/env python3
"""Exact ordinary-source identity, explicit edits, finite checks; not proof certification."""
from pathlib import Path
import hashlib,json,os,re
import verify_v34 as prior
from check_action_family import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v34-referee-response'
BASE_TREE='b6457e9d07e3efaf4418e1f48143fc0e07333158'
REPORT='reviews/a2-dyn-v34-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB='776a78aaecf82ea2dc92cd661e49c8bddf58e522'
WORKFLOW='.github/workflows/a2-dyn-v35-qualification.yml'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==35,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v34 tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==71 and len(scripts)==79,'complete v34 corpus')
    exceptions={e['path']:e for e in edits['core_edits']}
    for p in cores:
        rel=p.relative_to(BASE).as_posix();expected=p.read_text()
        if rel in exceptions:
            for change in exceptions[rel]['replacements']:
                require(expected.count(change['before'])==1,'unique exact edit')
                expected=expected.replace(change['before'],change['after'],1)
        require((ROOT/rel).read_text()==expected,'unexpected inherited edit '+rel)
    for p in scripts:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'changed inherited diagnostic '+p.name)
    require((ROOT/'appendices/return_statements.tex').read_bytes()==(BASE/'appendices/return_statements.tex').read_bytes(),'A--X appendix')
    for name,target in [('main.tex','V34_MAIN.tex'),('references.tex','V34_REFERENCES.tex'),
                        ('core/70_collision_mixing_local_limit.tex','V34_LOCAL_ENDPOINT_MEASURES.tex')]:
        require((ROOT/'provenance'/target).read_bytes()==(BASE/name).read_bytes(),'frozen prior source '+name)
    b=edits['bibliography_replacement'];oldbib=(BASE/'references.tex').read_text()
    require(oldbib.count(b['before'])==1,'unique bibliography correction')
    require((ROOT/'references.tex').read_text()==oldbib.replace(b['before'],b['after'],1),'bibliography beyond publication correction')
    main=(ROOT/'main.tex').read_text();appendix=(ROOT/'appendices/return_statements.tex').read_text()
    require('A2-DYN, revision 35' in main,'main identity')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==75,'complete core inclusion')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted source')
    require(main.count(r'\begin{leadtheorem}')==2 and appendix.count(r'\begin{maintheorem}')==24,'two leading theorems and A--X')
    require(main.index(r'\input{core/72_action_norm_details}')<main.index(r'\part{The actual-return record and raw inversion}'),'direct proof route')
    tex=main+'\n'+appendix+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+appendix+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and len(oldlabels)==967 and oldlabels<=set(labels),'label preservation')
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
    for key in ('rotation_free_finite_cover_phase_theorem','expanded_action_norm_proof',
                'compact_action_family_local_principle','uniform_oriented_ellipse_local_law',
                'stationary_physical_microscopic_LLT_proved','regular_endpoint_selected_LLT_proved',
                'normalized_original_trajectory_band_comparison_proved'):
        require(manifest[key] is True,'missing stated result '+key)
    needed={'thm:v35-rotation-free-rigidity','prop:v35-expanded-LY','lem:v35-faithful-strong',
            'lem:v35-peripheral-density','thm:v35-action-family-LLT','lem:v35-ellipse-geometry',
            'cor:v35-family-posterior','thm:LLT','cor:local-endpoint-measures'}
    require(needed<=set(labels),'load-bearing result missing')
    report=ROOT.parents[1]/REPORT
    if report.exists():
        data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'controlling report blob');verified=True
    else:
        require(not os.environ.get('GITHUB_ACTIONS'),'remote source lacks controlling report');verified=False
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow identity')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'read-only qualification')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':75,'inherited_core_byte_identical':70,
        'inherited_core_exactly_edited':list(exceptions),'inherited_python_byte_identical':79,
        'retained_mathematical_labels':967,'total_labels':len(labels),'retained_introductory_theorems':24,
        'leading_theorems':2,'bibliography_items':18,'verified_file_count':len(actual),
        'source_payload_tree':payload_tree(ROOT),'controlling_report_verified':verified,
        'qualification_workflow_sha256':digest(wf),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':35,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_finite_checks':{'v34':prior.finite_checks(),'v33':prior.prior.finite_checks()},
        'continuum_proof_certified':False,'full_raw_return_LLT_certified':False},indent=2,sort_keys=True))
