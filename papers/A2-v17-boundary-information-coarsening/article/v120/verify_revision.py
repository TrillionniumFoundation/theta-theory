#!/usr/bin/env python3
"""Portable v120 diagnostics, retaining every mathematical v119 check."""
from __future__ import annotations
from pathlib import Path
import hashlib
import importlib.util
import json
import platform
import re
import time
import sympy

HERE=Path(__file__).resolve().parent

def load(name,path):
    if not path.is_file():
        raise FileNotFoundError(f'Required vendored diagnostic is missing: {path}')
    spec=importlib.util.spec_from_file_location(name,path)
    if spec is None or spec.loader is None:
        raise ImportError(str(path))
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def preservation():
    old=HERE/'inherited-v119/source'
    old_files=list(old.glob('*.tex'))+list((old/'parts').glob('*.tex'))
    active=list(HERE.glob('*.tex'))+list((HERE/'parts').glob('*.tex'))
    labels=lambda files:set().union(*(set(re.findall(r'\\label\{([^}]+)\}',p.read_text())) for p in files))
    old_labels,current=labels(old_files),labels(active)
    missing=sorted(old_labels-current)
    assert not missing, ('missing inherited labels',missing)
    retained=[]
    for path in sorted((old/'parts').glob('*.tex')):
        target=HERE/'parts'/path.name
        assert target.is_file() and path.read_bytes()==target.read_bytes(), ('changed inherited mathematical part',path.name)
        retained.append({'path':'parts/'+path.name,'sha256':digest(path)})
    for path in active:
        text=path.read_text()
        for env in ('theorem','proof','lemma','proposition','corollary','remark'):
            assert text.count(r'\begin{'+env+'}')==text.count(r'\end{'+env+'}'),(path.name,env)
    return {'frozen_v119_source':'59437d7eb88b4791769eaf856bb6dd0f9c6c3a2b',
            'old_label_count':len(old_labels),'current_label_count':len(current),
            'missing_old_labels':missing,'byte_identical_inherited_parts':retained,
            'byte_identical_part_count':len(retained),
            'preservation_checked_against_vendored_frozen_source':True}

def main():
    started=time.monotonic()
    (HERE/'evidence').mkdir(exist_ok=True)
    old=load('a2_v119_checks',HERE/'inherited-v119/source/verify_revision.py')
    prior=load('a2_v118_checks',HERE/'inherited-v118/verify_revision.py')
    new=load('a2_v120_checks',HERE/'checks/loewy.py')
    data={'revision':120,'kind':'exact finite regression checks, not proof or priority certification',
          'python':platform.python_version(),'sympy':sympy.__version__,
          'v119_primary':old.primary_checks(),
          'v119_incidence':old.incidence_check(),
          'v119_rank_and_staircase':old.rank_and_staircase_checks(),
          'v119_cubic_and_compression':old.cubic_and_compression_checks(),
          'v118_substitution':prior.substitution_tests(),
          'v118_conductor':prior.conductor_tests(),
          'v118_action':prior.action_tests(),
          'v120_boundary':new.run(),
          'preservation':preservation(),
          'proof_certification':False,'priority_certification':False}
    data['elapsed_seconds']=round(time.monotonic()-started,3)
    (HERE/'evidence/DIAGNOSTICS.json').write_text(json.dumps(data,indent=2)+'\n')
    (HERE/'evidence/PRESERVATION.json').write_text(json.dumps(data['preservation'],indent=2)+'\n')
    print(json.dumps(data,indent=2))

if __name__=='__main__':
    main()
