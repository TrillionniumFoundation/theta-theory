#!/usr/bin/env python3
"""Fail-closed source and stale-receipt controls. No builds or network calls."""
from __future__ import annotations
import importlib.util
import json
from pathlib import Path
import shutil
import tempfile

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('v28_validation',ROOT/'tools/validate_v28.py')
if spec is None or spec.loader is None:
    raise RuntimeError('cannot load source gate')
v=importlib.util.module_from_spec(spec); spec.loader.exec_module(v)
count=0


def require(ok):
    global count
    if not ok:
        raise RuntimeError('negative control failed')
    count+=1


def rejects(call):
    try:
        call()
    except (RuntimeError,FileNotFoundError,KeyError,ValueError):
        require(True)
    else:
        require(False)


def stage_at(stage):
    for name in ('main.tex','references.tex','SOURCE_PINS.json'):
        shutil.copy2(ROOT/name,stage/name)
    shutil.copytree(ROOT/'core',stage/'core')
    shutil.copytree(ROOT/'tools',stage/'tools',ignore=shutil.ignore_patterns('__pycache__'))


def main():
    for missing in ('SOURCE_PINS.json','tools/verify_v28.py','tools/validate_v28.py',
                    'tools/test_validation_contract.py','core/00_local_period_recognition.tex'):
        with tempfile.TemporaryDirectory() as d:
            stage=Path(d); stage_at(stage)
            require(v.check_sources(stage)['schema']=='a2-v28-source-pins-1')
            (stage/missing).unlink(); rejects(lambda:v.check_sources(stage))
    for mutation in ('corrupt_new','corrupt_retained','extra_source','omit_manifest_entry','wrong_schema'):
        with tempfile.TemporaryDirectory() as d:
            stage=Path(d); stage_at(stage)
            if mutation.startswith('corrupt'):
                name='00_local_period_recognition' if mutation=='corrupt_new' else '00_fixed_aperture'
                with (stage/'core'/f'{name}.tex').open('a') as f:
                    f.write('% deliberately corrupted source\n')
            elif mutation=='extra_source':
                (stage/'core/unpinned.tex').write_text('new unpinned source\n')
            else:
                p=stage/'SOURCE_PINS.json'; pins=json.loads(p.read_text())
                if mutation=='wrong_schema': pins['schema']='a2-v27-source-pins-1'
                else: del pins['source_sha256']['main.tex']
                p.write_text(json.dumps(pins))
            rejects(lambda:v.check_sources(stage))
    require(v.require_commit('a'*40,'a'*40) is None)
    for actual,expected in [(None,'a'*40),('a'*40,'b'*40),('a'*40,'main')]:
        rejects(lambda:v.require_commit(actual,expected))
    good={'status':'passed','scope':'all_declared_volumes','full_package_qualified':True,
          'source_commit':'a'*40}
    require(v.check_nested(good,'a'*40) is None)
    for key,bad in [('status','failed'),('scope','primary_only'),
                    ('full_package_qualified',False),('source_commit','b'*40)]:
        altered={**good,key:bad}
        rejects(lambda:v.check_nested(altered,'a'*40))
    require(len(v.document_list({'documents':[{}], 'inherited_receipt':{'documents':[{},{}]}}))==3)
    print(json.dumps({'status':'passed','checks':count,
      'scope':'missing/corrupt/unpinned source, wrong commit and stale/partial retained receipt controls',
      'formal_proof_certificate':False},sort_keys=True))

if __name__=='__main__':
    main()
