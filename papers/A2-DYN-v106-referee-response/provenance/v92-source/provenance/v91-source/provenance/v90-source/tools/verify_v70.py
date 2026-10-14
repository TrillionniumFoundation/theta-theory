#!/usr/bin/env python3
"""Frozen-source audit and finite diagnostics, with an explicit local-only mode."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import verify_v69 as prior
from check_overlap_v70 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
BASE=ROOT.parent/'A2-DYN-v69-referee-response'
BASE_TREE='8209e73091651e5e95eebec221b1f0517a5d4863'
WORKFLOW='.github/workflows/a2-dyn-v70-qualification.yml'


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args]).decode().strip()


def tracked(directory, local):
    if local:
        return sorted(p.relative_to(directory).as_posix() for p in directory.rglob('*')
                      if p.is_file() and not {'build','evidence','__pycache__'} & set(p.relative_to(directory).parts)
                      and p.suffix != '.pyc')
    raw=subprocess.check_output(['git','-C',str(REPO),'ls-tree','-r','--name-only','-z','HEAD:'+directory.relative_to(REPO).as_posix()])
    return [p.decode() for p in raw.split(b'\0') if p]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def effective_status(directory, manifest):
    effective={}
    snapshot=manifest.get('inherited_status_snapshot','').split(';',1)[0].strip()
    if snapshot:
        path=directory/snapshot
        require(path.is_file(),'missing inherited status snapshot: '+snapshot)
        parent=json.loads(path.read_text())
        require(parent['revision'] < manifest['revision'],'cyclic status inheritance')
        effective.update(effective_status(directory,parent))
    for key,value in manifest.items():
        if isinstance(value,bool):
            if key in effective:
                require(value is effective[key],'inherited boolean changed: '+key)
            effective[key]=value
    return effective


def source_checks(local=False):
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==70,'active revision identity')
    require(manifest['active_directory']==ROOT.relative_to(REPO).as_posix(),'active directory')
    if not local:
        require(git('rev-parse','HEAD:'+BASE.relative_to(REPO).as_posix())==BASE_TREE==manifest['baseline_paper_tree'],'frozen complete baseline tree')
        require(git('rev-parse','HEAD:'+manifest['controlling_review_path'])==manifest['controlling_review_blob'],'frozen controlling report')
        if os.environ.get('GITHUB_SHA'):
            require(git('rev-parse','HEAD')==os.environ['GITHUB_SHA'],'actual checkout SHA')
    oldfiles=tracked(BASE,local)
    replaced=set(edits['metadata_replacements'])|{'main.tex'}
    for rel in oldfiles:
        require((ROOT/rel).is_file(),'inherited file omitted: '+rel)
        if rel not in replaced:
            require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'undeclared inherited change: '+rel)
    cores=[x for x in oldfiles if x.startswith('core/') and x.endswith('.tex')]
    scripts=[x for x in oldfiles if x.endswith('.py')]
    appendices=[x for x in oldfiles if x.startswith('appendices/') and x.endswith('.tex')]
    require((len(cores),len(scripts),len(appendices))==(151,203,9),'complete inherited sources')
    for name in ['core_replacements','inherited_scripts_replacements','compiled_appendix_replacements','deletions']:
        require(edits[name]==[],'nonempty mathematical replacement or deletion declaration')
    for name in ['main.tex','SOURCE_MANIFEST.json']:
        require((ROOT/'provenance'/('v69-'+name)).read_bytes()==(BASE/name).read_bytes(),'exact provenance: '+name)
    oldmain=(BASE/'main.tex').read_text()
    abstract=oldmain.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    intro=oldmain.split(r'\maketitle',1)[1].split(r'\part{Positive-source comparison and raw height}',1)[0]
    retained=(ROOT/'appendices/v69_frontmatter.tex').read_text()
    require(abstract in retained and retained.endswith(intro),'verbatim old opening')
    compiled=prior.prior.compiled
    text,inputs=compiled(ROOT)
    oldtext,oldinputs=compiled(BASE)
    included={p for p in inputs if p.startswith('core/')}
    require(len(included)==154 and included=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'all 154 cores compiled')
    require(set(oldinputs)<=set(inputs),'old input omitted')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'label duplication or loss')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined references: '+str(sorted(refs-set(labels))))
    for env in ['theorem','lemma','proposition','corollary','proof','leadtheorem','maintheorem','align','equation','tabular','array','aligned']:
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(text.count(r'\begin{maintheorem}')==oldtext.count(r'\begin{maintheorem}'),'inherited A-X statements')
    require(text.count(r'\begin{leadtheorem}')==oldtext.count(r'\begin{leadtheorem}')+2,'new and retained leading statements')
    require('revision 70' in (ROOT/'main.tex').read_text(),'active TeX revision')
    require((ROOT/'SPECIALIST_AUDIT_MAP.md').read_text().startswith('# Specialist audit map — revision 70'),'current specialist audit')
    effective=effective_status(ROOT,manifest)
    for key in ['lorentz_ordered_angular_loss_height_proved','lorentz_radial_moment_bound_proved','full_raw_return_LLT_proved','lorentz_complete_source_coverage_proved','independent_human_review','formal_proof_certificate']:
        require(effective[key] is False,'unsupported complete status: '+key)
    for key in ['lorentz_finite_scale_overlap_height_proved','lorentz_no_radial_loss_inner_height_proved','lorentz_fixed_word_radial_BV_proved','lorentz_signed_physical_boundary_current_identity_proved','lorentz_whole_chart_overlap_height_proved','lorentz_overlap_band_rate_proved']:
        require(effective[key] is True,'missing scoped theorem: '+key)
    wf=(REPO/WORKFLOW).read_text()
    require('contents: read' in wf and 'contents: write' not in wf,'qualification privileges')
    return {'mode':'local extracted-source check; not remote qualification' if local else 'exact remote-SHA qualification',
            'commit':None if local else git('rev-parse','HEAD'),
            'active_paper_tree':None if local else git('rev-parse','HEAD:'+ROOT.relative_to(REPO).as_posix()),
            'frozen_baseline_tree_verified':not local,'baseline_paper_tree':BASE_TREE,
            'inherited_core_byte_identical':len(cores),'inherited_python_byte_identical':len(scripts),
            'inherited_appendix_byte_identical':len(appendices),'included_core_modules':len(included),
            'retained_labels':len(oldlabels),'total_labels':len(labels),'old_opening_retained_verbatim':True,
            'effective_proof_status':effective,'qualification_workflow_sha256':digest(REPO/WORKFLOW),
            'tracked_source_sha256':{rel:digest(ROOT/rel) for rel in tracked(ROOT,local)}}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--local',action='store_true',help='no remote-SHA or frozen Git object claim')
    args=parser.parse_args()
    inherited={}
    module=prior
    while hasattr(module,'finite_checks'):
        inherited[module.__name__]=module.finite_checks()
        if not hasattr(module,'prior') or module.__name__=='verify_v37':
            break
        module=module.prior
    print(json.dumps({'revision':70,'source':source_checks(args.local),'new_finite_checks':finite_checks(),
                      'inherited_finite_checks':inherited,'continuum_proof_certified':False,
                      'complete_pointwise_endpoint_certified':False},indent=2,sort_keys=True))
