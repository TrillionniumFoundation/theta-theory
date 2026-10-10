#!/usr/bin/env python3
"""Exact-source preservation and finite diagnostics, never continuum certification."""
from pathlib import Path
import hashlib
import json
import re
import verify_v67 as prior
ordinary,tree_hash,payload_tree,compiled=prior.ordinary,prior.tree_hash,prior.payload_tree,prior.compiled
from check_radial_persistence_v68 import finite_checks
ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent / 'A2-DYN-v67-referee-response'
BASE_TREE = '266c432351a184e230b7e4df4f970c9d9f87208c'
WORKFLOW = '.github/workflows/a2-dyn-v68-qualification.yml'


def require(ok, message):
    if not ok:
        raise RuntimeError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks():
    manifest = json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    edits = json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    oldmanifest = json.loads((BASE/'SOURCE_MANIFEST.json').read_text())
    require(manifest['revision'] == edits['revision'] == 68, 'revision identity')
    require(tree_hash(BASE).hex() == BASE_TREE == manifest['baseline_paper_tree'], 'frozen complete v67 paper tree')
    cores = sorted((BASE/'core').glob('*.tex'))
    scripts = sorted(BASE.rglob('*.py'))
    require(len(cores) == 145 and len(scripts) == 197, 'complete inherited source')
    kept = cores + scripts + list((BASE/'appendices').glob('*.tex')) + [BASE/'references.tex']
    for path in kept:
        require(path.read_bytes() == (ROOT/path.relative_to(BASE)).read_bytes(), 'inherited change: '+str(path))
    require(edits['core_replacements'] == edits['inherited_scripts_replacements'] == edits['compiled_appendix_replacements'] == [], 'undeclared mathematical edit')
    for name in edits['metadata_replacements'] + ['main.tex']:
        require((ROOT/'provenance'/('v67-'+name)).read_bytes() == (BASE/name).read_bytes(), 'missing old metadata: '+name)
    oldmain = (BASE/'main.tex').read_text()
    oldabstract = oldmain.split(r'\begin{abstract}',1)[1].split(r'\end{abstract}',1)[0]
    oldintro = oldmain.split(r'\maketitle',1)[1].split(r'\part{The complete arithmetic record}',1)[0]
    retained = (ROOT/'appendices/v67_frontmatter.tex').read_text()
    require(oldabstract in retained and retained.endswith(oldintro), 'old abstract/introduction changed')
    text, inputs = compiled(ROOT)
    oldtext, oldinputs = compiled(BASE)
    included = {p for p in inputs if p.startswith('core/')}
    require(len(included) == 148 and included == {p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')}, 'full 148-core inclusion')
    require(set(oldinputs) <= set(inputs), 'old compiled input omitted')
    labels = re.findall(r'\\label\{([^}]+)\}', text)
    oldlabels = set(re.findall(r'\\label\{([^}]+)\}', oldtext))
    require(len(labels) == len(set(labels)) and oldlabels <= set(labels), 'old label retention or duplicate')
    refs = set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}', text))
    require(refs <= set(labels), 'undefined references: '+str(refs-set(labels)))
    for env in ['theorem','lemma','proposition','corollary','proof','leadtheorem','maintheorem','align','equation','tabular','array','aligned']:
        require(text.count('\\begin{'+env+'}') == text.count('\\end{'+env+'}'), 'unbalanced '+env)
    require('revision 68' in (ROOT/'main.tex').read_text(), 'active manuscript revision')
    require(text.count(r'\begin{maintheorem}') == oldtext.count(r'\begin{maintheorem}') == 24, 'A-X statements')
    require(text.count(r'\begin{leadtheorem}') == oldtext.count(r'\begin{leadtheorem}')+2, 'new/retained leading theorems')
    for key, value in oldmanifest.items():
        if key.endswith('_proved') or key in ['independent_human_review','formal_proof_certificate']:
            require(manifest[key] is value, 'inherited proof status changed: '+key)
    for key in ['lorentz_uniform_angular_loss_proved','lorentz_complete_source_coverage_proved','lorentz_angular_condition_tail_proved']:
        require(manifest[key] is False, 'unsupported new endpoint: '+key)
    for key in ['lorentz_analytic_angular_germ_classification_proved','lorentz_all_order_relative_radial_profile_proved','lorentz_order_free_annular_comparison_proved','lorentz_zero_tangent_all_order_strata_height_proved','lorentz_positive_center_guard_nonseam_strata_height_proved']:
        require(manifest[key] is True, 'new scoped proof absent: '+key)
    wf = ROOT.parents[1]/WORKFLOW
    require(digest(wf) == manifest['qualification_workflow_sha256'], 'workflow hash')
    require('contents: read' in wf.read_text() and 'contents: write' not in wf.read_text(), 'qualification privileges')
    require(payload_tree(ROOT) == manifest['source_payload_tree'], 'ordinary payload hash')
    hashes = {p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name != 'SOURCE_MANIFEST.json'}
    require(len(hashes) == manifest['ordinary_payload_file_count'], 'ordinary payload count')
    return {'baseline_paper_tree': BASE_TREE, 'inherited_core_byte_identical': len(cores),
            'inherited_python_byte_identical': len(scripts), 'included_core_modules': len(included),
            'retained_labels':len(oldlabels), 'total_labels':len(labels),
            'all_old_abstract_and_introduction_retained':True, 'inherited_appendix_byte_identical':len(list((BASE/'appendices').glob('*.tex'))),
            'source_payload_tree':manifest['source_payload_tree'],
            'qualification_workflow_sha256':digest(wf), 'source_sha256':hashes}


if __name__ == '__main__':
    inherited = {}
    module = prior
    while hasattr(module, 'finite_checks'):
        inherited[module.__name__] = module.finite_checks()
        if not hasattr(module, 'prior') or module.__name__ == 'verify_v37':
            break
        module = module.prior
    print(json.dumps({'revision':68, 'source':source_checks(), 'new_finite_checks':finite_checks(),
                     'inherited_finite_checks':inherited, 'continuum_proof_certified':False,
                     'full_pointwise_raw_return_LLT_certified':False}, indent=2, sort_keys=True))
