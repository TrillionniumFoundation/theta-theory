#!/usr/bin/env python3
"""Exact-source and finite-model checks, not continuum proof certification."""
from pathlib import Path
import argparse, hashlib, json, os, re
import verify_v58 as prior
from check_markov_v59 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v58-referee-response'
BASE_TREE='e7be5ba545bfc80e08c86e3c596e36b483bbedf7'
WORKFLOW='.github/workflows/a2-dyn-v59-qualification.yml'
REPORTS=dict(prior.REPORTS)
REPORTS['reviews/a2-dyn-v58-external-top4-review-2026-10-09/REFEREE_REPORT.md']='d70134c2f027a53d8bde20187a2b3b706011782c'
ordinary,tree_hash,payload_tree,compiled=prior.ordinary,prior.tree_hash,prior.payload_tree,prior.compiled

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks(local_preflight=False):
    require(not(local_preflight and os.environ.get('GITHUB_ACTIONS')),'preflight forbidden in Actions')
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    oldmanifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==edits['revision']==59,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v58 tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==124 and len(scripts)==167,'incomplete baseline')
    require(edits['core_replacements']==edits['inherited_scripts_replacements']==[],'unexpected inherited edits')
    for p in cores+scripts+list((BASE/'appendices').glob('*.tex')):
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'inherited change '+p.name)
    archives=['main.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','VALIDATION.md',
      'PUBLICATION_STATUS.json','README.md','REFEREE_STATUS.md','REVISION_CHARTER.md','SPECIALIST_AUDIT_MAP.md',
      'HISTORICAL_DERIVATION_AUDIT.md','INHERITED_EDITS.json','references.tex']
    for name in archives:
        require((ROOT/('provenance/v58-'+name)).read_bytes()==(BASE/name).read_bytes(),'provenance '+name)
    oldbib=(BASE/'references.tex').read_text();newbib=(ROOT/'references.tex').read_text()
    require(newbib.startswith(oldbib.split(r'\end{thebibliography}')[0]),'bibliography not append-only')
    text,inputs=compiled(ROOT);oldtext,_=compiled(BASE)
    actual={p for p in inputs if p.startswith('core/')}
    require(len(actual)==127 and actual=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'127 core inclusions')
    labels=re.findall(r'\\label\{([^}]+)\}',text);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label retention/uniqueness')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    main=(ROOT/'main.tex').read_text()
    require('October 9, 2026. A2-DYN, revision 59' in main,'revision metadata')
    require(main.count(r'\begin{leadtheorem}')==2 and text.count(r'\begin{leadtheorem}')==oldtext.count(r'\begin{leadtheorem}') and text.count(r'\begin{maintheorem}')==24,'principal statement retention')
    for env in ['theorem','lemma','proposition','corollary','proof','leadtheorem','maintheorem','align','equation','tabular','array','aligned']:
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in text),'control character')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):cites.update(x.strip() for x in group.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',newbib))
    require(len(bib)==20 and cites<=bib,'bibliography/citations')
    expected={'lem:v59-physical-root','lem:v59-witness-cover','lem:v59-accretive-gaussian',
      'thm:v59-markov-contact','lem:v59-markov-lattice','lem:v59-cylinder-local',
      'thm:v59-markov-density','thm:v59-markov-boundary-height','thm:LLT','cor:v51-positive-criterion'}
    require(expected<=set(labels),'new or retained proof missing')
    # Inherited truth flags retain their exact scope; no pointwise Lorentz upgrade.
    for key,value in oldmanifest.items():
        if key.endswith('_proved') or key in ['independent_human_review','formal_proof_certificate']:
            require(manifest[key] is value,'inherited status changed '+key)
    for key in ['physical_root_lemma_proved','accretive_gaussian_details_proved','correlated_markov_pressure_realization_proved',
      'markov_continuous_roof_pointwise_LLT_proved','markov_boundary_essential_height_proved']:
        require(manifest[key] is True,'new result missing '+key)
    hashes={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'ordinary payload identity')
    require(len(hashes)==manifest['ordinary_payload_file_count'],'payload count')
    checked={}
    for rel,expected_blob in REPORTS.items():
        p=ROOT.parents[1]/rel
        if not p.exists() and local_preflight and 'a2-dyn-v58-external' in rel:
            checked[rel]=False;continue
        require(p.exists(),'missing frozen report '+rel)
        data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==expected_blob,'frozen report differs '+rel);checked[rel]=True
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'workflow privileges')
    require('--local-preflight' not in wf.read_text(),'workflow has preflight exception')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':127,'inherited_core_byte_identical':124,
      'inherited_python_byte_identical':167,'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
      'retained_A_X_theorems':24,'source_payload_tree':payload_tree(ROOT),'verified_file_count':len(hashes),
      'frozen_reports_verified':checked,'local_preflight':local_preflight,
      'qualification_workflow_sha256':digest(wf),'source_sha256':hashes}

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--local-preflight',action='store_true');args=parser.parse_args()
    inherited={};module=prior
    while hasattr(module,'finite_checks'):
        inherited[module.__name__]=module.finite_checks()
        if not hasattr(module,'prior') or module.__name__=='verify_v37':break
        module=module.prior
    print(json.dumps({'revision':59,'source':source_checks(args.local_preflight),'new_finite_checks':finite_checks(),
      'inherited_finite_checks':inherited,'continuum_proof_certified':False,
      'full_pointwise_raw_return_LLT_certified':False},indent=2,sort_keys=True))
