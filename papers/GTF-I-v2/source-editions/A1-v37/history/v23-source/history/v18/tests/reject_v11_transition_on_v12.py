#!/usr/bin/env python3
"""Apply the referee's exact two-call-site mutation to v12 + unchanged v11 suite.

The old physical residual tests still accept a poor table; that fact is not
concealed. The v12 adaptive construction gate rejects the same mutation before
returning a table, so this historical suite can no longer finish successfully.
"""
from dataclasses import replace
import importlib.util
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
import certified_compiler as cc
from construction_contracts import ContractError


def main():
    spec=importlib.util.spec_from_file_location('unchanged_v11',ROOT/'tests/test_v11.py')
    suite=importlib.util.module_from_spec(spec);spec.loader.exec_module(suite)
    original=cc.compile_tables
    counts={'compiler_calls_before_rejection':0,'entries_seen':0,'entries_changed':0}
    def collapse(*args,**kwargs):
        p,a=original(*args,**kwargs);counts['compiler_calls_before_rejection']+=1
        for stage in p.transitions:
            for row in stage:
                for targets in row:
                    counts['entries_seen']+=len(targets)
                    counts['entries_changed']+=sum(j!=0 for j in targets)
        t=tuple(tuple(tuple(tuple(0 for _ in reports) for reports in row)
                      for row in stage) for stage in p.transitions)
        return replace(p,transitions=t),a
    cc.compile_tables=suite.compile_tables=collapse
    suite.physical_tests()
    before=sum(suite.COUNTS.values())
    try:suite.adaptive_tests()
    except ContractError as error:
        receipt={'mutation_rejected':True,'same_two_call_sites_as_referee':True,
                 'unchanged_legacy_physical_assertions_before_gate':before,
                 'assertions_before_rejection':sum(suite.COUNTS.values()),**counts,
                 'rejection':str(error),
                 'interpretation':'Residual validity is preserved. Construction acceptance is independently enforced.'}
    else:raise AssertionError('collapsed historical suite unexpectedly completed')
    out=Path(sys.argv[1]);out.parent.mkdir(parents=True,exist_ok=True)
    out.write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps(receipt,indent=2))
if __name__=='__main__':main()
