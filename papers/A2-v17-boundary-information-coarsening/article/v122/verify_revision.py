#!/usr/bin/env python3
"""A2 v122 exact regressions and byte-for-byte preservation audit."""
from __future__ import annotations
from pathlib import Path
import hashlib, importlib.util, json, re, platform, time
HERE=Path(__file__).resolve().parent
OLD=HERE.parent/'v121'

def load(name,path):
    if not path.is_file(): raise FileNotFoundError(path)
    spec=importlib.util.spec_from_file_location(name,path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def preservation():
    files=lambda d:list(d.glob('*.tex'))+list((d/'parts').glob('*.tex'))
    labels=lambda ps:set().union(*(set(re.findall(r'\\label\{([^}]+)\}',p.read_text())) for p in ps))
    before,after=labels(files(OLD)),labels(files(HERE))
    assert not before-after,sorted(before-after)
    records=[]
    for p in sorted((OLD/'parts').glob('*.tex')):
        q=HERE/'parts'/p.name
        assert q.is_file() and q.read_bytes()==p.read_bytes(),p.name
        records.append({'path':'parts/'+p.name,'byte_identical':True,
                        'sha256':hashlib.sha256(p.read_bytes()).hexdigest()})
    old_inputs=re.findall(r'\\input\{([^}]+)\}',(OLD/'core.tex').read_text())
    new_inputs=re.findall(r'\\input\{([^}]+)\}',(HERE/'core.tex').read_text())
    assert set(old_inputs)<=set(new_inputs)
    for name in ('paper.tex','geometry.tex','applications.tex'):
        assert (HERE/name).read_bytes()==(OLD/name).read_bytes(),name
    keys=lambda p:set(re.findall(r'\\bibitem\{([^}]+)\}',p.read_text()))
    assert keys(OLD/'references.tex')<=keys(HERE/'references.tex')
    for p in files(HERE):
        text=p.read_text()
        for env in ('theorem','lemma','proof','proposition','corollary','remark'):
            assert text.count(r'\begin{'+env+'}')==text.count(r'\end{'+env+'}'),(p,env)
    return {'old_revision':121,'old_label_count':len(before),'new_label_count':len(after),
            'missing_old_labels':[],'old_core_inputs_preserved':True,
            'all_old_mathematical_parts_byte_identical':True,'old_parts':records,
            'all_old_bibliography_keys_preserved':True,'original_v121_unchanged':True}

def main():
    start=time.monotonic(); (HERE/'evidence').mkdir(exist_ok=True)
    p121=load('p121',OLD/'verify_revision.py')
    p120=load('p120',HERE.parent/'v120/verify_revision.py')
    p119=load('p119',OLD/'inherited-v119/source/verify_revision.py')
    p118=load('p118',OLD/'inherited-v118/verify_revision.py')
    loewy=load('loewy',OLD/'checks/loewy.py')
    flags=load('flags',OLD/'checks/flags_elliptic.py')
    new=load('new',HERE/'checks/ramification_intrinsic.py')
    results={'revision':122,'python':platform.python_version(),
      'v119_primary':p119.primary_checks(),'v119_incidence':p119.incidence_check(),
      'v119_rank_and_staircase':p119.rank_and_staircase_checks(),
      'v119_cubic_and_compression':p119.cubic_and_compression_checks(),
      'v118_substitution':p118.substitution_tests(),'v118_conductor':p118.conductor_tests(),
      'v118_action':p118.action_tests(),'v120_boundary':loewy.run(),
      'v120_frozen_preservation':p120.preservation(),
      'v121_frozen_preservation':p121.preservation(),'v121_flags_and_elliptic':flags.run(),
      'v122_ramification_and_intrinsic_powers':new.run(),'preservation':preservation(),
      'proof_certification':False,'priority_certification':False,
      'RII120_1_full_text_comparison':'not completed: full Ballico 1993 text unavailable'}
    results['elapsed_seconds']=round(time.monotonic()-start,3)
    (HERE/'evidence/DIAGNOSTICS.json').write_text(json.dumps(results,indent=2)+'\n')
    (HERE/'evidence/PRESERVATION.json').write_text(json.dumps(results['preservation'],indent=2)+'\n')
    print(json.dumps(results,indent=2))
if __name__=='__main__': main()
