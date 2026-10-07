#!/usr/bin/env python3
"""Frozen source, exact edits, full payload Merkle identity and finite diagnostics."""
from pathlib import Path
import hashlib,json,os,re
import verify_v35 as prior
from check_exact_path_bridge import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v35-referee-response'
BASE_TREE='1634006e867a2258b09d85db6f9fcecc668f53d1'
REPORT='reviews/a2-dyn-v35-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB='e7d2a7ea4932d5d7354ddfbd279ae04047e7b647'
WORKFLOW='.github/workflows/a2-dyn-v36-qualification.yml'
ordinary,tree_hash,payload_tree=prior.ordinary,prior.tree_hash,prior.payload_tree

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==36,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v35 full tree')
    cores=sorted((BASE/'core').glob('*.tex')); scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==75 and len(scripts)==83,'complete v35 corpus')
    exceptions={e['path']:e for e in edits['core_edits']}
    for path in cores:
        rel=path.relative_to(BASE).as_posix(); text=path.read_text()
        if rel in exceptions:
            for change in exceptions[rel]['replacements']:
                require(text.count(change['before'])==1,'unique exact source edit '+rel)
                text=text.replace(change['before'],change['after'],1)
        require((ROOT/rel).read_text()==text,'unrecorded inherited change '+rel)
    for path in scripts+[BASE/'references.tex',BASE/'appendices/return_statements.tex']:
        require(path.read_bytes()==(ROOT/path.relative_to(BASE)).read_bytes(),'inherited file '+path.name)
    for name,target in [('main.tex','V35_MAIN.tex'),('core/72_action_norm_details.tex','V35_ACTION_NORM_DETAILS.tex'),
                        ('core/74_compact_family_local_principle.tex','V35_COMPACT_FAMILY.tex')]:
        require((ROOT/'provenance'/target).read_bytes()==(BASE/name).read_bytes(),'prior source archive')
    main=(ROOT/'main.tex').read_text(); appendix=(ROOT/'appendices/return_statements.tex').read_text()
    require('A2-DYN, revision 36' in main,'main identity')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==79,'all 79 core inclusions')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    require(main.count(r'\begin{leadtheorem}')==3 and appendix.count(r'\begin{maintheorem}')==24,'three principal results and all A--X')
    tex=main+'\n'+appendix+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+appendix+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex); oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and len(oldlabels)==1010 and oldlabels<=set(labels),'label retention')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined refs '+str(refs-set(labels)))
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control character')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text())); cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(v.strip() for v in group.split(','))
    require(len(bib)==18 and cites<=bib,'bibliography identities')
    needed={'thm:v36-microscopic-path-bridge','prop:v36-local-fourth','lem:v36-local-block-probes',
            'cor:v36-conditional-tightness','cor:v36-band-posterior-bridge','prop:v36-cover-mixing',
            'prop:v36-support-family','lem:v35-faithful-strong','thm:LLT'}
    require(needed<=set(labels),'new and inherited endpoints')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'all-source Merkle identity')
    require(len(actual)==manifest['ordinary_payload_file_count'],'all-source file count')
    for key in ('full_raw_return_LLT_proved','full_return_complement_proved','common_pointwise_return_correction_proved',
                'arbitrary_selected_path_Gaussian_amplitude_proved','independent_human_review','formal_proof_certificate'):
        require(manifest[key] is False,'unsupported certificate '+key)
    for key in ('stationary_microscopic_path_bridge_proved','local_microscopic_fourth_moments_proved',
                'separated_family_hypotheses','finite_cover_mixing_input_verified','direct_strong_faithfulness_argument',
                'uniform_noncentrally_symmetric_support_family'):
        require(manifest[key] is True,'missing revision conclusion '+key)
    require('exact stationary' in manifest['microscopic_path_bridge_scope'],'bridge scope')
    report=ROOT.parents[1]/REPORT
    verified=False
    if report.exists():
        data=report.read_bytes(); blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'frozen controlling report'); verified=True
    else:require(not os.environ.get('GITHUB_ACTIONS'),'remote report absent')
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'read-only workflow')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':79,'inherited_core_byte_identical':73,
            'inherited_core_exactly_edited':list(exceptions),'inherited_python_byte_identical':83,
            'retained_mathematical_labels':1010,'total_labels':len(labels),'retained_introductory_theorems':24,
            'leading_theorems':3,'bibliography_items':18,'verified_file_count':len(actual),
            'source_payload_tree':payload_tree(ROOT),'controlling_report_verified':verified,
            'qualification_workflow_sha256':digest(wf),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':36,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_finite_checks':{'v35':prior.finite_checks(),'v34':prior.prior.finite_checks()},
        'continuum_proof_certified':False,'full_raw_return_LLT_certified':False},indent=2,sort_keys=True))
