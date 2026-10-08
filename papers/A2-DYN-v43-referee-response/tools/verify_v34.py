#!/usr/bin/env python3
"""Complete source identity and finite diagnostics, not a mathematical certificate."""
from pathlib import Path
import hashlib,json,os,re
import verify_v33 as prior
from check_microscopic_closure import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v33-referee-response'
BASE_TREE='42ba62ef825d1e555f6c6bf83e647792bba67de8'
REPORT='reviews/a2-dyn-v33-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB='5159113603f557e654792626bf88c2aa5396e3c9'
WORKFLOW='.github/workflows/a2-dyn-v34-qualification.yml'
ordinary,tree_hash=prior.ordinary,prior.tree_hash

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def payload_tree(root):
    """Git Merkle tree of every ordinary source except the root manifest."""
    def obj(kind,data):
        return hashlib.sha1(kind.encode()+b' '+str(len(data)).encode()+b'\0'+data).digest()
    def walk(directory):
        rows=[]
        for p in directory.iterdir():
            if p.name in ('build','evidence','__pycache__') or (directory==root and p.name=='SOURCE_MANIFEST.json'):
                continue
            if p.is_dir():
                mode='40000';value=walk(p);key=p.name+'/'
            else:
                mode='100755' if p.stat().st_mode&0o111 else '100644';value=obj('blob',p.read_bytes());key=p.name
            rows.append((key,mode.encode()+b' '+p.name.encode()+b'\0'+value))
        return obj('tree',b''.join(value for _,value in sorted(rows)))
    return walk(root).hex()

def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==34,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen baseline tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==68 and len(scripts)==75,'complete baseline corpus')
    for p in cores+scripts+[BASE/'references.tex']:
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'inherited change '+p.name)
    old=(BASE/'main.tex').read_text()
    require((ROOT/'provenance/V33_MAIN.tex').read_bytes()==(BASE/'main.tex').read_bytes(),'old main preserved')
    oldabstract=re.search(r'\\begin\{abstract\}(.*?)\\end\{abstract\}',old,re.S).group(1)
    require((ROOT/'provenance/V33_ABSTRACT.tex').read_text()==oldabstract,'old abstract preserved')
    syn=old[old.index(edits['synopsis_begin']):old.index(edits['synopsis_end'])]
    for item in edits['synopsis_replacements']:
        require(syn.count(item['before'])==1,'unique synopsis title edit')
        syn=syn.replace(item['before'],item['after'],1)
    appendix=(ROOT/'appendices/return_statements.tex').read_text()
    require(appendix.endswith(syn),'all A--X statements and proofs retained in compiled appendix')
    main=(ROOT/'main.tex').read_text()
    require('A2-DYN, revision 34' in main,'main identity')
    require(main.count(r'\begin{leadtheorem}')==1 and appendix.count(r'\begin{maintheorem}')==24,'one leading theorem and A--X')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==71,'complete core input set')
    require({s+'.tex' for s in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'unlisted core')
    require(r'\input{appendices/return_statements}' in main,'compiled complementary statements')
    tex=main+'\n'+appendix+'\n'+'\n'.join((ROOT/(s+'.tex')).read_text() for s in inputs)
    oldtex=old+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and len(oldlabels)==924 and oldlabels<=set(labels),'duplicate or missing labels')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','leadtheorem','align','equation','tabular','array','aligned'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in tex),'control characters')
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()));cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(v.strip() for v in group.split(','))
    require(len(bib)==18 and cites<=bib,'bibliography and citations')
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'complete ordinary source Merkle manifest')
    require(len(actual)==manifest['ordinary_payload_file_count'],'ordinary payload count')
    for key in ('full_raw_return_LLT_proved','full_return_complement_proved','common_pointwise_return_correction_proved',
                'arbitrary_selected_path_Gaussian_amplitude_proved','microscopic_conditional_path_bridge_proved',
                'independent_human_review','formal_proof_certificate'):
        require(manifest[key] is False,'unsupported endpoint '+key)
    for key in ('compact_frequency_raw_collision_spectrum_proved','two_endpoint_collision_interval_LLT_proved',
                'stationary_physical_microscopic_LLT_proved','stationary_signed_middle_smallness_proved',
                'stationary_microscopic_denominator_proved','regular_endpoint_selected_LLT_proved',
                'normalized_original_trajectory_band_comparison_proved'):
        require(manifest[key] is True,'missing new theorem '+key)
    needed={'lem:backward-flight-multiplier','lem:collision-action-weights','prop:bounded-band-LY',
        'thm:compact-collision-spectrum','lem:collision-interval-envelopes','thm:two-endpoint-collision-LLT',
        'cor:local-endpoint-measures','lem:overlap-local-admissibility','thm:stationary-microscopic-LLT',
        'cor:stationary-middle-vanishes','thm:stationary-endpoint-selected-LLT','cor:normalized-physical-band'}
    require(needed<=set(labels),'missing load-bearing new statement')
    report=ROOT.parents[1]/REPORT
    if report.exists():
        data=report.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==REPORT_BLOB==manifest['controlling_review_blob'],'exact controlling report');verified=True
    else:
        require(not os.environ.get('GITHUB_ACTIONS'),'remote checkout lacks controlling report');verified=False
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'read-only qualification')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':71,'inherited_core_byte_identical':68,
        'inherited_python_byte_identical':75,'retained_mathematical_labels':924,'total_labels':len(labels),
        'retained_introductory_theorems':24,'leading_theorems':1,'bibliography_items':18,
        'verified_file_count':len(actual),'source_payload_tree':payload_tree(ROOT),'controlling_report_verified':verified,
        'controlling_report_bytes_boundary':None if verified else 'absent from local author archive; required remotely',
        'qualification_workflow_sha256':digest(wf),'source_sha256':actual}

if __name__=='__main__':
    print(json.dumps({'revision':34,'source':source_checks(),'new_finite_checks':finite_checks(),
        'inherited_finite_checks':{'v33':prior.finite_checks(),'v32':prior.prior.finite_checks()},
        'continuum_proof_certified':False,'full_raw_return_LLT_certified':False},indent=2,sort_keys=True))
