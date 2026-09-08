#!/usr/bin/env python3
"""Reproduce the v11 referee's transition mutation without modifying v11.

This independent wrapper pins the three author sources used in that report.
It executes in a fresh Python process and changes both compiler call sites.
The expected pass is evidence of the OLD defect, not acceptance of a mutation.
"""
import hashlib
import importlib.util
from pathlib import Path
from dataclasses import replace
import json
import sys

EXPECTED={
 'finite_compiler.py':'5e6335160cec538c13f7b0fbfb3d6ad89ec55946734ee7d527dae564ac654fda',
 'certified_compiler.py':'6965862f93bd2ef8f107eca30fd53fb3c8ce52e696f99c893a343aad980a226c',
 'tests/test_v11.py':'4cfe2c0a6a492cdff3ca87053ce2de541c6ce90fe97f51fa3238122a6019b2b6'}

def main():
    if len(sys.argv)!=3:raise SystemExit('usage: reproduce_v11_transition.py V11_ROOT OUTPUT.json')
    root=Path(sys.argv[1]).resolve();out=Path(sys.argv[2]).resolve()
    def verify():
        for name,sha in EXPECTED.items():
            if hashlib.sha256((root/name).read_bytes()).hexdigest()!=sha:
                raise RuntimeError('v11 source mismatch: '+name)
    verify();sys.path.insert(0,str(root))
    import certified_compiler as cc
    spec=importlib.util.spec_from_file_location('pinned_v11_suite',root/'tests/test_v11.py')
    suite=importlib.util.module_from_spec(spec);spec.loader.exec_module(suite)
    original=cc.compile_tables
    counts={'compiler_calls':0,'transition_entries':0,'changed_entries':0}
    def collapse(*args,**kwargs):
        p,a=original(*args,**kwargs);counts['compiler_calls']+=1
        for stage in p.transitions:
            for row in stage:
                for reports in row:
                    counts['transition_entries']+=len(reports)
                    counts['changed_entries']+=sum(j!=0 for j in reports)
        transitions=tuple(tuple(tuple(tuple(0 for _ in reports) for reports in row)
                                for row in stage) for stage in p.transitions)
        return replace(p,transitions=transitions),a
    cc.compile_tables=suite.compile_tables=collapse
    suite.physical_tests();suite.adaptive_tests();suite.separated_floor_tests()
    n=sum(suite.COUNTS.values())
    if (n,counts['compiler_calls'],counts['transition_entries'],counts['changed_entries'])!=(8207,52,1389,775):
        raise AssertionError((n,counts))
    verify()
    receipt={'old_suite_passed_despite_mutation':True,'assertions':n,**counts,
             'source_sha256':EXPECTED,'categories':dict(suite.COUNTS),
             'interpretation':'Reproduced the old diagnostic defect. V12 rejects the same call-site mutation independently.'}
    out.parent.mkdir(parents=True,exist_ok=True);out.write_text(json.dumps(receipt,indent=2)+'\n')
    print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
