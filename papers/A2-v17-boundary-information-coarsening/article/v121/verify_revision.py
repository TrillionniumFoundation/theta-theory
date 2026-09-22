#!/usr/bin/env python3
"""A2 v121 exact regression and preservation checks."""
from __future__ import annotations
from pathlib import Path
import hashlib, importlib.util, json, re, sys, platform, time
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'v120'
def load(name,path):
    if not path.is_file(): raise FileNotFoundError(path)
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def preservation():
    files=lambda d: list(d.glob('*.tex'))+list((d/'parts').glob('*.tex'))
    labels=lambda ps:set().union(*(set(re.findall(r'\\label\{([^}]+)\}',p.read_text())) for p in ps))
    before,after=labels(files(OLD)),labels(files(HERE))
    assert not before-after,sorted(before-after)
    edited={'00a-conductor-introduction.tex','03c-loewy-boundary-primary.tex'}
    records=[]
    for p in sorted((OLD/'parts').glob('*.tex')):
        q=HERE/'parts'/p.name
        assert q.is_file(),str(q)
        identical=p.read_bytes()==q.read_bytes()
        assert identical or p.name in edited,p.name
        records.append({'path':'parts/'+p.name,'byte_identical':identical,
                        'old_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
                        'new_sha256':hashlib.sha256(q.read_bytes()).hexdigest()})
    # Every old core input remains in the active new core.
    old_inputs=re.findall(r'\\input\{([^}]+)\}',(OLD/'core.tex').read_text())
    new_inputs=re.findall(r'\\input\{([^}]+)\}',(HERE/'core.tex').read_text())
    assert set(old_inputs)<=set(new_inputs)
    for p in files(HERE):
        text=p.read_text()
        for env in ('theorem','lemma','proof','proposition','corollary','remark'):
            assert text.count(r'\begin{'+env+'}')==text.count(r'\end{'+env+'}'),(p,env)
    return {'old_label_count':len(before),'new_label_count':len(after),'missing_old_labels':[],
            'old_core_inputs_preserved':True,'old_parts':records,
            'edited_parts_explanation':{'00a-conductor-introduction.tex':'section heading only',
                '03c-loewy-boundary-primary.tex':'scope-qualified theorem title and replacement of compressed descent paragraph by formal lemma/corollary references'},
            'original_v120_is_retained':True}

def main():
    start=time.monotonic(); (HERE/'evidence').mkdir(exist_ok=True)
    v120=load('prior_v120',OLD/'verify_revision.py')
    v119=load('prior_v119',OLD/'inherited-v119/source/verify_revision.py')
    v118=load('prior_v118',OLD/'inherited-v118/verify_revision.py')
    loewy=load('loewy_checks',OLD/'checks/loewy.py')
    new=load('flag_checks',HERE/'checks/flags_elliptic.py')
    results={'revision':121,'python':platform.python_version(),
      'v119_primary':v119.primary_checks(),'v119_incidence':v119.incidence_check(),
      'v119_rank_and_staircase':v119.rank_and_staircase_checks(),
      'v119_cubic_and_compression':v119.cubic_and_compression_checks(),
      'v118_substitution':v118.substitution_tests(),'v118_conductor':v118.conductor_tests(),
      'v118_action':v118.action_tests(),'v120_boundary':loewy.run(),
      'v120_frozen_preservation':v120.preservation(),
      'v121_flags_and_elliptic':new.run(),'preservation':preservation(),
      'proof_certification':False,'priority_certification':False,
      'E120_1_full_text_comparison':'not completed: full Ballico 1993 text unavailable'}
    results['elapsed_seconds']=round(time.monotonic()-start,3)
    (HERE/'evidence/DIAGNOSTICS.json').write_text(json.dumps(results,indent=2)+'\n')
    (HERE/'evidence/PRESERVATION.json').write_text(json.dumps(results['preservation'],indent=2)+'\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
