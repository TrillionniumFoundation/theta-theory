#!/usr/bin/env python3
"""Exact source preservation plus finite fixtures, never proof certification."""
from pathlib import Path
import argparse
import hashlib
import json
import os
import re
import subprocess
import verify_v71 as prior
from check_complete_current_v72 import finite_checks
ROOT=Path(__file__).resolve().parents[1]
REPO=ROOT.parents[1]
BASE=ROOT.parent/'A2-DYN-v71-referee-response'
WORKFLOW='.github/workflows/a2-dyn-v72-qualification.yml'


def require(ok,message):
    if not ok:
        raise RuntimeError(message)


def git(*args):
    return subprocess.check_output(['git','-C',str(REPO),*args]).decode().strip()


def files(directory,local):
    if local:
        return sorted(p.relative_to(directory).as_posix() for p in directory.rglob('*')
                      if p.is_file() and not {'build','evidence','__pycache__'}&set(p.relative_to(directory).parts)
                      and p.suffix!='.pyc')
    raw=subprocess.check_output(['git','-C',str(REPO),'ls-tree','-r','--name-only','-z','HEAD:'+directory.relative_to(REPO).as_posix()])
    return sorted(x.decode() for x in raw.split(b'\0') if x)


def compiled(directory):
    inputs=[]
    def expand(rel,stack):
        require(rel not in stack,'cyclic TeX input: '+rel)
        path=directory/rel
        require(path.is_file(),'missing TeX input: '+rel)
        inputs.append(rel)
        text=path.read_text()
        return re.sub(r'\\input\{([^}]+)\}',lambda m: expand(m[1] if m[1].endswith('.tex') else m[1]+'.tex',stack+[rel]),text)
    return expand('main.tex',[]),inputs


def source_checks(local):
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==edits['revision']==72,'revision identity')
    require(manifest['active_directory']==ROOT.relative_to(REPO).as_posix(),'active directory')
    if not local:
        require(git('rev-parse','HEAD:'+manifest['baseline_directory'])==manifest['baseline_paper_tree']=='1689e32821be45fc3daca28f5da0cf6f8a374e07','frozen v71 paper tree')
        require(git('rev-parse','HEAD:'+manifest['controlling_review_path'])==manifest['controlling_review_blob']=='129f78b849ebf2639130090189bb7b6e9bfebf8d','frozen v71 report')
        if os.environ.get('GITHUB_SHA'):
            require(git('rev-parse','HEAD')==os.environ['GITHUB_SHA'],'actual checkout SHA')
    oldfiles=files(BASE,local)
    replaced=set(edits['metadata_replacements'])|{'main.tex'}
    for rel in oldfiles:
        require((ROOT/rel).is_file(),'inherited file omitted: '+rel)
        if rel not in replaced:
            require((ROOT/rel).read_bytes()==(BASE/rel).read_bytes(),'undeclared inherited change: '+rel)
    cores=[x for x in oldfiles if x.startswith('core/') and x.endswith('.tex')]
    scripts=[x for x in oldfiles if x.endswith('.py')]
    appendices=[x for x in oldfiles if x.startswith('appendices/') and x.endswith('.tex')]
    require((len(cores),len(scripts),len(appendices))==(156,209,11),'inherited complete source counts')
    for field in ['core_replacements','inherited_scripts_replacements','compiled_appendix_replacements','deletions']:
        require(edits[field]==[],'unauthorized replacement/deletion')
    for name in ['main.tex','SOURCE_MANIFEST.json']:
        require((ROOT/'provenance'/('v71-'+name)).read_bytes()==(BASE/name).read_bytes(),'exact provenance '+name)
    oldmain=(BASE/'main.tex').read_text()
    abstract=oldmain.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    intro=oldmain.split(r'\maketitle',1)[1].split(r'\part{Physical capacity recovery and signed radial balance}',1)[0]
    retained=(ROOT/'appendices/v71_frontmatter.tex').read_text()
    require(abstract in retained and retained.endswith(intro),'old opening changed')
    text,inputs=compiled(ROOT);oldtext,oldinputs=compiled(BASE)
    require(set(oldinputs)<=set(inputs),'inherited compiled input missing')
    included={x for x in inputs if x.startswith('core/')}
    require(len(included)==159 and included=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'all 159 core modules compiled')
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtext))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'labels duplicated or removed')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',text))
    require(refs<=set(labels),'undefined references: '+str(sorted(refs-set(labels))))
    for env in ['theorem','lemma','proposition','corollary','proof','leadtheorem','maintheorem','align','align*','equation','tabular','array','aligned']:
        require(text.count('\\begin{'+env+'}')==text.count('\\end{'+env+'}'),'unbalanced '+env)
    require(text.count(r'\begin{maintheorem}')==oldtext.count(r'\begin{maintheorem}'),'inherited main statements changed')
    require(text.count(r'\begin{leadtheorem}')==oldtext.count(r'\begin{leadtheorem}')+1,'leading theorem coverage')
    require('revision 72' in (ROOT/'main.tex').read_text(),'active TeX revision')
    effective=prior.effective_status(ROOT,manifest)
    for key in ['full_raw_return_LLT_proved','lorentz_complete_current_excess_decay_proved','lorentz_full_source_finite_measure_current_proved','lorentz_directed_flux_power_bound_proved','lorentz_outside_source_height_proved','lorentz_complete_first_incidence_height_proved','independent_human_review','formal_proof_certificate']:
        require(effective[key] is False,'unsupported full claim: '+key)
    require(effective['lorentz_all_source_recovered_height_proved'] is True,'missing new scoped height')
    wf=(REPO/WORKFLOW).read_text()
    require('contents: read' in wf and 'contents: write' not in wf,'read-only qualification')
    return {'mode':'local extracted-source check; not remote qualification' if local else 'exact remote-SHA qualification',
            'commit':None if local else git('rev-parse','HEAD'),
            'active_paper_tree':None if local else git('rev-parse','HEAD:'+manifest['active_directory']),
            'frozen_baseline_tree_verified':not local,'baseline_paper_tree':manifest['baseline_paper_tree'],
            'inherited_core_byte_identical':len(cores),'inherited_python_byte_identical':len(scripts),
            'inherited_appendix_byte_identical':len(appendices),'included_core_modules':len(included),
            'retained_labels':len(oldlabels),'total_labels':len(labels),'old_opening_retained_verbatim':True,
            'effective_proof_status':effective,
            'tracked_source_sha256':{rel:hashlib.sha256((ROOT/rel).read_bytes()).hexdigest() for rel in files(ROOT,local)}}


if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--local',action='store_true')
    args=parser.parse_args()
    require(not(args.local and os.environ.get('GITHUB_ACTIONS')=='true'),'local mode forbidden in Actions')
    inherited={};module=prior
    while hasattr(module,'finite_checks'):
        inherited[module.__name__]=module.finite_checks()
        if not hasattr(module,'prior') or module.__name__=='verify_v37':
            break
        module=module.prior
    print(json.dumps({'revision':72,'source':source_checks(args.local),'new_finite_checks':finite_checks(),
                      'inherited_finite_checks':inherited,'continuum_proof_certified':False,
                      'complete_pointwise_endpoint_certified':False},indent=2,sort_keys=True))
