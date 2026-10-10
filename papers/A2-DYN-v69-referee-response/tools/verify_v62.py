#!/usr/bin/env python3
"""Strict ordinary-source verification and finite checks; not a proof certificate."""
from pathlib import Path
import argparse,hashlib,json,os,re
import verify_v61 as prior
from check_clearance_v62 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v61-referee-response'
BASE_TREE='a377d9bd972092af8e7fcd263de7d72f5509629b'
WORKFLOW='.github/workflows/a2-dyn-v62-qualification.yml'
REPORT='reviews/a2-dyn-v60-external-top4-review-2026-10-09/REFEREE_REPORT.md'
REPORTS=dict(prior.REPORTS);REPORTS[REPORT]='5e2f3538ce3d09d3ee1075464f05c2e6354e0709'
ordinary,tree_hash,payload_tree,compiled=prior.ordinary,prior.tree_hash,prior.payload_tree,prior.compiled

def require(ok,message):
    if not ok:raise RuntimeError(message)

def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()

def source_checks(local_preflight=False):
    require(not(local_preflight and os.environ.get('GITHUB_ACTIONS')),'preflight forbidden in Actions')
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    oldmanifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==edits['revision']==62,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'frozen v61 paper tree')
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==132 and len(scripts)==179,'incomplete baseline')
    require(edits['core_replacements']==edits['inherited_scripts_replacements']==[],'undeclared inherited edits')
    for p in cores+scripts+list((BASE/'appendices').glob('*.tex')):
        require(p.read_bytes()==(ROOT/p.relative_to(BASE)).read_bytes(),'inherited change '+p.name)
    archives=['main.tex','SOURCE_MANIFEST.json','RESPONSE_TO_REFEREE.md','PROOF_LEDGER.md','VALIDATION.md',
      'PUBLICATION_STATUS.json','README.md','REFEREE_STATUS.md','REVISION_CHARTER.md','SPECIALIST_AUDIT_MAP.md',
      'HISTORICAL_DERIVATION_AUDIT.md','INHERITED_EDITS.json','references.tex','JOURNAL_ROUTE.md']
    for name in archives:
        require((ROOT/('provenance/v61-'+name)).read_bytes()==(BASE/name).read_bytes(),'provenance '+name)
    oldbib=(BASE/'references.tex').read_text();newbib=(ROOT/'references.tex').read_text()
    addition=(ROOT/'BIBLIOGRAPHY_ADDITION.tex.txt').read_text()
    require(newbib==oldbib.replace(r'\end{thebibliography}',addition+r'\end{thebibliography}'),'bibliography not append-only')
    text,inputs=compiled(ROOT);oldtext,_=compiled(BASE)
    actual={p for p in inputs if p.startswith('core/')}
    require(len(actual)==134 and actual=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'134 core inclusions')
    labels=re.findall(r'\\label\{([^}]+)\}',text);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(oldlabels)==1761 and len(labels)==len(set(labels)) and oldlabels<=set(labels),'label retention/uniqueness')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined references '+str(refs-set(labels)))
    main=(ROOT/'main.tex').read_text()
    require('October 10, 2026. A2-DYN, revision 62' in main,'revision metadata')
    require(main.count(r'\begin{leadtheorem}')==3 and text.count(r'\begin{leadtheorem}')==oldtext.count(r'\begin{leadtheorem}') and text.count(r'\begin{maintheorem}')==24,'principal statement retention')
    for env in ['theorem','lemma','proposition','corollary','proof','leadtheorem','maintheorem','align','equation','tabular','array','aligned']:
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\t\r' for c in text),'control character')
    cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',text):cites.update(x.strip() for x in group.split(','))
    bib=set(re.findall(r'\\bibitem\{([^}]+)\}',newbib))
    require(len(bib)==22 and cites<=bib,'bibliography/citations')
    expected={'lem:v62-sublevel','lem:v62-jet-complexity','thm:v62-finite-type-height',
      'cor:v62-fold-clearance','thm:v62-caustic-finite','lem:v62-caustic-separation',
      'thm:v62-caustic-localization','cor:v62-caustic-raw-error','lem:v62-caustic-tube',
      'cor:v62-caustic-mass','thm:LLT','cor:v51-positive-criterion'}
    require(expected<=set(labels),'new or retained proof missing')
    for key,value in oldmanifest.items():
        if key.endswith('_proved') or key in ['independent_human_review','formal_proof_certificate']:
            require(manifest[key] is value,'inherited status changed '+key)
    for key in ['lorentz_finite_type_clearance_height_proved','lorentz_fold_clearance_height_proved',
      'lorentz_clearance_caustic_finiteness_proved','lorentz_caustic_positive_localization_proved',
      'lorentz_caustic_tube_mass_proved']:
        require(manifest[key] is True,'missing new result '+key)
    hashes={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(payload_tree(ROOT)==manifest['source_payload_tree'],'ordinary payload identity')
    require(len(hashes)==manifest['ordinary_payload_file_count'],'payload count')
    checked={}
    for rel,expected_blob in REPORTS.items():
        p=ROOT.parents[1]/rel
        if not p.exists() and local_preflight and rel==REPORT:
            checked[rel]=False;continue
        require(p.exists(),'missing frozen report '+rel)
        data=p.read_bytes();blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
        require(blob==expected_blob,'frozen report differs '+rel);checked[rel]=True
    wf=ROOT.parents[1]/WORKFLOW
    require(digest(wf)==manifest['qualification_workflow_sha256'],'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(),'workflow privileges')
    require('--local-preflight' not in wf.read_text(),'workflow has preflight exception')
    return {'baseline_paper_tree':BASE_TREE,'included_core_files':134,'inherited_core_byte_identical':132,
      'inherited_python_byte_identical':179,'retained_mathematical_labels':len(oldlabels),'total_labels':len(labels),
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
    print(json.dumps({'revision':62,'source':source_checks(args.local_preflight),'new_finite_checks':finite_checks(),
      'inherited_finite_checks':inherited,'continuum_proof_certified':False,
      'full_pointwise_raw_return_LLT_certified':False},indent=2,sort_keys=True))
