#!/usr/bin/env python3
"""Re-execute the v12 referee's fault model against pinned v12 source bytes.

This is an author reproduction, not a newly commissioned independent review.
The original review script remains unchanged in reviews/ and is also run by
validate.py when the complete repository is present.
"""
from pathlib import Path
from fractions import Fraction as F
from dataclasses import replace
import hashlib, json, sys
ROOT=Path(sys.argv[1]).resolve()
OUT=Path(sys.argv[2])
BLOBS={'finite_compiler.py':'286c956da1e8b4845d8457488e56845cf15c352b',
       'certified_compiler.py':'205bf39543f81eab85eb22425572206c810f598e',
       'construction_contracts.py':'ec778394962114c3ad9a0e6bef0fb7796c65c266'}
def identities():
    d={}
    for name, expected in BLOBS.items():
        b=(ROOT/name).read_bytes()
        actual=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
        assert actual==expected,(name,actual)
        d[name]={'git_blob':actual,'sha256':hashlib.sha256(b).hexdigest()}
    return d
before=identities()
sys.path.insert(0,str(ROOT))
import certified_compiler as cc
import finite_compiler as fc
from construction_contracts import inspect_construction
original=cc.compile_tables

def interval(b,h,tau=None):
    segments=max(1,1<<max(0,b-2))
    grid=tuple(F(1,4)+F(j,2*segments) for j in range(segments+1))
    def state(hist):
        s=F(1,2)
        for u,_ in hist:s=(s+grid[u])/2
        return (s,)
    return len(grid),state,state,grid

def finite(b,h,tau=None):
    grid=(F(1,4),F(1,2),F(3,4))
    def state(hist):
        s=F(1,2)
        for u,_ in hist:s=(s+grid[u])/2
        return (s,)
    return len(grid),state,state,grid

def invoke(routine,T,M,factory,A):
    if routine=='ordinary':
        return cc.adaptive_compile(T,1,M,A,factory,absolute_tolerance=F(1,128),max_bits=12)
    return cc.robust_adaptive_compile(T,1,M,A,factory,F(1,128),max_bits=12)

rows=[];horizons=[]
try:
    for routine in ('ordinary','robust'):
        for M in (1,2):
            for fault in ('none','zero_bits'):
                def mutated(*a,**kw):
                    a=list(a);a[4]=0
                    return original(*a,**kw)
                cc.compile_tables=original if fault=='none' else mutated
                p,a,trace,grid=invoke(routine,1,M,interval,F(1,2))
                e=F(1,8*M);valid=all(t['lower']<=e<=t['upper'] for t in trace)
                assert valid==(fault=='none')
                assert all(t['construction_accepted'] for t in trace)
                rows.append({'routine':routine,'M':M,'fault':fault,'true_radius':e,
                             'all_brackets_valid':valid,'returned_bits':p.output_bits,
                             'last_stage':trace[-1]})
        def short(*a,**kw):
            a=list(a);a[0]=1
            return original(*a,**kw)
        cc.compile_tables=short
        p,a,trace,_=invoke(routine,2,2,finite,F(0))
        assert len(p.transitions)==1 and all(t['construction_accepted'] for t in trace)
        machine=fc.Machine();machine.step(p,0,0,0)
        try:machine.step(p,1,0,0)
        except IndexError:runtime='IndexError on second requested transition'
        else:raise AssertionError('missing stage not detected at runtime')
        horizons.append({'routine':routine,'requested_horizon':2,'returned_horizon':1,
                         'runtime':runtime,'last_stage':trace[-1]})
finally:cc.compile_tables=original
assert before==identities()
result={'status':'passed: historical faults reproduced','source_identity':before,
        'source_files_unchanged':True,'nominal_controls':4,
        'accepted_false_precision_brackets':4,'accepted_short_horizons':2,
        'precision_cases':rows,'horizon_cases':horizons,
        'scope':'Author re-execution of the exact referee fault models; not formal verification.'}
OUT.parent.mkdir(exist_ok=True,parents=True)
OUT.write_text(json.dumps(result,indent=2,default=str)+'\n')
print(json.dumps({k:v for k,v in result.items() if k not in ('precision_cases','horizon_cases','source_identity')},indent=2))
