#!/usr/bin/env python3
"""Check the complete ordinary source and finite diagnostics at a frozen baseline."""
from __future__ import annotations
from pathlib import Path
import hashlib,json,re,os
import verify_v30 as old
from check_geometric_extraction import finite_checks
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT.parent/'A2-DYN-v30-referee-response'
BASE_TREE='7e47c9606ea21b79836319a7fa25d34bdf2a4b3c'
REPORT='reviews/a2-dyn-v30-external-top4-review-2026-10-07/REFEREE_REPORT.md'
REPORT_BLOB='5a92130e7ef47c27cd77d34337e02c02205eccc2'
WORKFLOW='.github/workflows/a2-dyn-v31-qualification.yml'
ordinary,tree_hash=old.ordinary,old.tree_hash


def require(ok: bool,message: str)->None:
    if not ok:raise RuntimeError(message)


def digest(path: Path)->str:return hashlib.sha256(path.read_bytes()).hexdigest()


def source_checks()->dict:
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    ledger=json.loads((ROOT/'INHERITED_EDITS.json').read_text())
    require(manifest['revision']==ledger['revision']==31,'revision identity')
    require(tree_hash(BASE).hex()==BASE_TREE==manifest['baseline_paper_tree'],'baseline ordinary tree')
    require({p.relative_to(BASE).as_posix():digest(p) for p in ordinary(BASE)}==manifest['baseline_sha256'],'complete baseline hashes')
    edits=ledger['edits']
    require(len(edits)==6 and {x['path'] for x in edits}=={'main.tex','references.tex'},'exact inherited edit scope')
    for rel in ('main.tex','references.tex'):
        text=(BASE/rel).read_text()
        for edit in edits:
            if edit['path']!=rel:continue
            require(text.count(edit['before'])==1,'unique replay anchor '+rel)
            text=text.replace(edit['before'],edit['after'],1)
        require(text.encode()==(ROOT/rel).read_bytes(),'exact replay '+rel)
    main=(ROOT/'main.tex').read_text()
    cores=sorted((BASE/'core').glob('*.tex'));scripts=sorted((BASE/'tools').glob('*.py'))
    require(len(cores)==62 and len(scripts)==63,'complete inherited source')
    for path in cores+scripts:
        require(path.read_bytes()==(ROOT/path.relative_to(BASE)).read_bytes(),'changed inherited source: '+path.name)
    actual={p.relative_to(ROOT).as_posix():digest(p) for p in ordinary(ROOT) if p.name!='SOURCE_MANIFEST.json'}
    require(actual==manifest['source_sha256'],'complete actual source hashes')
    inputs=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(inputs)==len(set(inputs))==64,'core count')
    require({x+'.tex' for x in inputs}=={p.relative_to(ROOT).as_posix() for p in (ROOT/'core').glob('*.tex')},'all mathematical modules included')
    tex=main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in inputs)
    oldtex=(BASE/'main.tex').read_text()+'\n'+'\n'.join(p.read_text() for p in cores)
    labels=re.findall(r'\\label\{([^}]+)\}',tex);oldlabels=set(re.findall(r'\\label\{([^}]+)\}',oldtex))
    require(len(labels)==len(set(labels)) and oldlabels<=set(labels),'duplicate/deleted mathematical label')
    refs=set(re.findall(r'\\(?:ref|eqref|pageref|autoref)\{([^}]+)\}',tex))
    require(refs<=set(labels),'unresolved refs: '+str(refs-set(labels)))
    require(len(oldlabels)==813,'inherited label count')
    require('October 7, 2026. A2-DYN, revision 31' in main,'article revision')
    require(tex.count(r'\begin{maintheorem}')==22,'Theorems A--V')
    items=set(re.findall(r'\\bibitem\{([^}]+)\}',(ROOT/'references.tex').read_text()));cites=set()
    for group in re.findall(r'\\cite(?:\[[^\]]*\])?\{([^}]+)\}',tex):cites.update(x.strip() for x in group.split(','))
    require(cites<=items,'missing bibliography')
    for env in ('theorem','lemma','proposition','corollary','proof','maintheorem','align','equation','tabular'):
        require(tex.count('\\begin{'+env+'}')==tex.count('\\end{'+env+'}'),'unbalanced '+env)
    require(not any(ord(c)<32 and c not in '\n\r\t' for c in tex),'control character')
    needed={'thm:wide-collision-band','thm:projected-collision-windows','lem:stationary-length-bias',
            'prop:stationary-observation-coupling','thm:stationary-physical-windows',
            'cor:stationary-weighted-selection','thm:intro-stationary-physical-windows',
            'thm:LLT','thm:shape-volume-criterion','thm:averaged-common-raw-remainder',
            'thm:intro-stationary-window-bridge','thm:multiblock-collision-band',
            'prop:window-conditional-characteristic','thm:collision-window-bridge',
            'lem:whole-physical-clock-coupling','thm:stationary-physical-bridge',
            'cor:bridge-cylinder-events','cor:bridge-path-weighted-denominator',
            'thm:intro-geometric-raw-reduction','lem:roof-transverse-direction',
            'lem:uniform-collision-cutoff','thm:geometric-extraction-budget',
            'thm:microscopic-finite-band-reduction','cor:linear-cutoff-microscopic-inversion',
            'eq:geometric-common-raw-ledger'}
    require(needed<=set(labels),'missing required theorem')
    for key in ('full_raw_LLT_proved','full_fixed_return_complementary_integral_proved',
                'uniform_long_time_raw_derivative_bound_proved','pointwise_common_raw_remainder_proved',
                'microscopic_exact_event_replacement_proved','arbitrary_path_weight_denominator_proved',
                'full_isotropic_one_tenth_band_proved','independent_human_review','formal_proof_certificate'):
        require(manifest[key] is False,'unsupported endpoint flag '+key)
    for key in ('stationary_suspension_window_denominator_proved','stationary_suspension_window_replacement_proved',
                'fixed_collision_nine_hundredths_band_proved','stationary_window_conditioned_functional_limit_proved',
                'fixed_interior_cylinder_denominator_proved','geometric_long_time_residual_derivative_bound_proved',
                'microscopic_fixed_label_finite_band_reduction_proved'):
        require(manifest[key] is True,'missing scoped new theorem '+key)
    report=ROOT.parents[1]/REPORT;data=report.read_bytes()
    report_blob=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    require(report_blob==REPORT_BLOB==manifest['controlling_review_blob'],'exact controlling report')
    workflow=ROOT.parents[1]/WORKFLOW
    require(digest(workflow)==manifest['qualification_workflow_sha256'],'exact read-only workflow')
    require('contents: read' in workflow.read_text() and 'contents: write' not in workflow.read_text(),'qualification permissions')
    return {'baseline_paper_tree':BASE_TREE,'inherited_core_byte_identical':len(cores),
            'inherited_python_files_byte_identical':len(scripts),'retained_mathematical_labels':len(oldlabels),
            'included_core_files':len(inputs),'total_labels':len(labels),'bibliography_items':len(items),
            'exact_inherited_edits':len(edits),'verified_file_count':len(actual),
            'controlling_report_verified':True,'qualification_workflow_sha256':digest(workflow),
            'source_sha256':actual}


if __name__=='__main__':
    print(json.dumps({'revision':31,'source':source_checks(),'new_finite_checks':finite_checks(),
      'inherited_finite_checks':{'v30':old.finite_checks()},
      'continuum_proof_certified':False,'full_raw_LLT_certified':False},indent=2,sort_keys=True))
