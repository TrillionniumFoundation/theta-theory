#!/usr/bin/env python3
"""Exact ordinary-source checks and finite diagnostics; no continuum certification."""
from pathlib import Path
import hashlib,json,os,re
import verify_v63 as prior
from check_caustic_profiles_v65 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v63-referee-response'
BASE_TREE='0d019a183d79d8de977bd705aa4ab1e228d6cc17'
WORKFLOW='.github/workflows/a2-dyn-v65-qualification.yml'
REPORTS=dict(prior.REPORTS)
ordinary,tree_hash,payload_tree,compiled=prior.ordinary,prior.tree_hash,prior.payload_tree,prior.compiled


def require(ok,message):
    if not ok:raise RuntimeError(message)


def digest(path):return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    oldmanifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==edits['revision']==65,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'exact v63 baseline')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==136 and len(scripts)==187,'baseline completeness')
    require(edits['core_replacements']==edits['inherited_scripts_replacements']==edits['compiled_appendix_replacements']==[],'inherited replacement')
    for p in cores+scripts+list((BASE/'appendices').glob('*.tex')):
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'inherited edit '+p.name)
    for name in edits['metadata_replacements']:
        require((ROOT/'provenance'/('v63-'+name)).read_bytes()==(BASE/name).read_bytes(),'metadata archive '+name)
    oldbib=(BASE/'references.tex').read_text();newbib=(ROOT/'references.tex').read_text()
    require(newbib==oldbib.replace(r'\end{thebibliography}',(ROOT/'BIBLIOGRAPHY_ADDITION.tex.txt').read_text()+r'\end{thebibliography}'),'append-only bibliography')
    text,inputs=compiled(ROOT);oldtext,oldinputs=compiled(BASE)
    actual={p for p in inputs if p.startswith('core/')}
    require(len(actual)==139 and actual=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'complete core inclusion')
    require(set(oldinputs)<=set(inputs),'inherited compiled input omitted')
    labels=re.findall(r'\\label\{([^}]+)\}',text);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(oldlabels)==1809 and len(labels)==len(set(labels)) and oldlabels<=set(labels),'label preservation')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    main=(ROOT/'main.tex').read_text()
    require('October 10, 2026. A2-DYN, revision 65' in main,'date/revision')
    require(main.count(r'\begin{leadtheorem}')==4,'new leading theorem')
    require(text.count(r'\begin{maintheorem}')==oldtext.count(r'\begin{maintheorem}')==24,'A-X retention')
    for env in ['theorem','lemma','proposition','corollary','proof','leadtheorem','maintheorem','align','equation','tabular','array','aligned','gathered']:
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in text),'control characters')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):cites.update(x.strip() for x in group.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',newbib))
    require(len(bib)==24 and cites<=bib,'bibliography/citation mismatch')
    required={'thm:intro-v65-caustic','thm:v65-reversible-weight','thm:v65-seam-profile',
              'thm:v65-cluster-height','thm:v65-affine-label-profile','eq:v65-jet-budget',
              'cor:v65-multiple-seam-trace','end:v65-new-mathematics','thm:LLT','cor:v51-positive-criterion'}
    require(required<=set(labels),'new theorem or old target missing')
    for key,value in oldmanifest.items():
        if key.endswith('_proved') or key in ['independent_human_review','formal_proof_certificate']:
            require(manifest[key] is value,'inherited proved-status changed '+key)
    for key in ['lorentz_reversible_critical_weight_identity_proved','lorentz_simple_seam_local_profile_proved',
                'lorentz_affine_exact_label_local_profile_proved','lorentz_local_profile_finite_jet_budget_proved']:
        require(manifest[key] is True,'new result absent '+key)
    require(manifest['uniform_reversible_critical_trace_concentration_proved'] is False,'unproved trace marked closed')
    hashes={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'payload hash')
    require(len(hashes)==manifest['ordinary_payload_file_count'],'payload count')
    reports={}
    for rel,expected in REPORTS.items():
        p=ROOT.parents[1]/rel;require(p.exists(),'missing frozen report '+rel)
        data=p.read_bytes();actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(actual==expected,'frozen report changed '+rel);reports[rel]=True
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'workflow privileges')
    require('--local-preflight' not in wf.read_text(),'qualification bypass')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':139,'inherited_core_byte_identical':136,
            'inherited_python_byte_identical':187,'retained_mathematical_labels':1809,'total_labels':len(labels),
            'retained_A_X_theorems':24,'source_payload_tree':payload_tree(ROOT),'verified_file_count':len(hashes),
            'frozen_reports_verified':reports,'local_preflight':False,
            'qualification_workflow_sha256':digest(wf),'source_sha256':hashes}


if __name__=='__main__':
    inherited={};module=prior
    while hasattr(module,'finite_checks'):
        inherited[module.__name__]=module.finite_checks()
        if not hasattr(module,'prior') or module.__name__=='verify_v37':break
        module=module.prior
    print(json.dumps({'revision':65,'source':source_checks(),'new_finite_checks':finite_checks(),
                      'inherited_finite_checks':inherited,'continuum_proof_certified':False,
                      'full_pointwise_raw_return_LLT_certified':False},indent=2,sort_keys=True))
