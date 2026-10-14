#!/usr/bin/env python3
"""Frozen-source and finite-diagnostic audit; not continuum certification."""
from pathlib import Path
import hashlib
import json
import re
import subprocess
import verify_v68 as prior
from check_absolute_guard_v69 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
BASE=ROOT.parent/'A2-DYN-v68-referee-response'
BASE_TREE='dce4295d9d660f64e4d25bb0463045dddc546249'
WORKFLOW='.github/workflows/a2-dyn-v69-qualification.yml'


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args]).decode().strip()


def tracked(directory):
    relative=directory.relative_to(REPO).as_posix()
    raw=subprocess.check_output(['git','-C',str(REPO),'ls-tree','-r','--name-only','-z','HEAD:'+relative])
    return [p.decode() for p in raw.split(b'\0') if p]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    oldmanifest=json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision']==edits['revision']==69,'revision identity')
    require(git('rev-parse','HEAD:papers/A2-DYN-v68-referee-response')==BASE_TREE==manifest['baseline_paper_tree'],'frozen complete baseline tree')
    require(git('rev-parse','HEAD:'+manifest['controlling_review_path'])==manifest['controlling_review_blob'],'frozen controlling report')
    oldfiles=tracked(BASE)
    replaced=set(edits['metadata_replacements'])|{'main.tex'}
    for rel in oldfiles:
        require((ROOT/rel).is_file(),'inherited file omitted: '+rel)
        if rel not in replaced:
            require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'undeclared inherited edit: '+rel)
    cores=[x for x in oldfiles if x.startswith('core/') and x.endswith('.tex')]
    scripts=[x for x in oldfiles if x.endswith('.py')]
    appendices=[x for x in oldfiles if x.startswith('appendices/') and x.endswith('.tex')]
    require(len(cores)==148 and len(appendices)==8,'complete inherited mathematics')
    require(edits['core_replacements']==edits['inherited_scripts_replacements']==edits['compiled_appendix_replacements']==edits['deletions']==[],'mathematical edit declaration')
    require((ROOT/'provenance/v68-main.tex').read_bytes()==(BASE/'main.tex').read_bytes(),'archived old main')
    require((ROOT/'provenance/v68-SOURCE_MANIFEST.json').read_bytes()==(BASE/'SOURCE_MANIFEST.json').read_bytes(),'archived old status')
    oldmain=(BASE/'main.tex').read_text()
    oldabstract=oldmain.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    oldintro=oldmain.split(r'\maketitle',1)[1].split(r'\part{The complete arithmetic record}',1)[0]
    retained=(ROOT/'appendices/v68_frontmatter.tex').read_text()
    require(oldabstract in retained and oldintro in retained,'old abstract/introduction text not retained exactly')
    text,inputs=prior.compiled(ROOT)
    oldtext,oldinputs=prior.compiled(BASE)
    included={p for p in inputs if p.startswith('core/')}
    require(len(included)==151 and included=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'complete 151-core inclusion')
    require(set(oldinputs)<=set(inputs),'old compiled input omitted')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label duplication or loss')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined references: '+str(sorted(refs-set(labels))))
    for env in ['theorem','lemma','proposition','corollary','proof','leadtheorem','maintheorem','align','equation','tabular','array','aligned']:
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(text.count(r'\begin{maintheorem}')==oldtext.count(r'\begin{maintheorem}'),'inherited A-X statements')
    require(text.count(r'\begin{leadtheorem}')==oldtext.count(r'\begin{leadtheorem}')+2,'new and retained leading statements')
    require('revision 69' in (ROOT/'main.tex').read_text(),'active revision title')
    effective={k:v for k,v in oldmanifest.items() if isinstance(v,bool)}
    for key,value in manifest.items():
        if isinstance(value,bool):
            if key in effective:
                require(value is effective[key],'inherited status changed: '+key)
            effective[key]=value
    for key in ['lorentz_radial_moment_bound_proved','lorentz_angular_persistence_tail_proved','lorentz_complete_zero_center_guard_height_proved','full_raw_return_LLT_proved','lorentz_complete_source_coverage_proved','independent_human_review','formal_proof_certificate']:
        require(effective[key] is False,'unsupported complete status: '+key)
    for key in ['lorentz_unguarded_physical_comparison_trace_proved','lorentz_absolute_guard_all_center_strata_height_proved','lorentz_zero_center_guard_strata_height_proved','lorentz_finite_scale_radial_strata_height_proved','lorentz_weighted_radial_tail_implication_proved']:
        require(effective[key] is True,'new scoped theorem status: '+key)
    wf=(REPO/WORKFLOW).read_text()
    require('contents: read' in wf and 'contents: write' not in wf,'qualification privileges')
    hashes={rel:digest(ROOT/rel) for rel in tracked(ROOT)}
    return {'commit':git('rev-parse','HEAD'),'active_paper_tree':git('rev-parse','HEAD:'+ROOT.relative_to(REPO).as_posix()),'baseline_paper_tree':BASE_TREE,
            'inherited_core_byte_identical':len(cores),'inherited_python_byte_identical':len(scripts),'inherited_appendix_byte_identical':len(appendices),'included_core_modules':len(included),
            'retained_labels':len(oldlabels),'total_labels':len(labels),'old_opening_text_retained_exactly':True,
            'effective_proof_status':effective,'qualification_workflow_sha256':digest(REPO/WORKFLOW),'tracked_source_sha256':hashes}


if __name__=='__main__':
    inherited={}
    module=prior
    while hasattr(module,'finite_checks'):
        inherited[module.__name__]=module.finite_checks()
        if not hasattr(module,'prior') or module.__name__=='verify_v37':
            break
        module=module.prior
    print(json.dumps({'revision':69,'source':source_checks(),'new_finite_checks':finite_checks(),'inherited_finite_checks':inherited,
                      'continuum_proof_certified':False,'complete_pointwise_endpoint_certified':False},indent=2,sort_keys=True))
