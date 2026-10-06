#!/usr/bin/env python3
"""Exact rational spectral arithmetic for Theorem spectralvalue94.

Input is a supplied eigenvalue list, not a measured/calibrated device.  The
root is enclosed by rational bisection; no floating point is used here.
"""
from __future__ import annotations
import argparse
from fractions import Fraction as F
import json
from pathlib import Path
from typing import Iterable

def rational(value: object) -> F:
    if isinstance(value, bool) or not isinstance(value, (str, int, F)):
        raise ValueError('Use integer or rational-string data, not floats or booleans')
    try:
        return F(value)
    except (ValueError, ZeroDivisionError) as exc:
        raise ValueError('Invalid rational datum') from exc

def integer(value: object, lo: int, hi: int, name: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or not lo <= value <= hi:
        raise ValueError(f'{name} must be an integer in [{lo},{hi}]')
    return value

def majorant(values: Iterable[F], rank: int) -> tuple[F, ...]:
    v=tuple(sorted((rational(x) for x in values),reverse=True))
    if not v or any(x<0 for x in v):
        raise ValueError('A nonempty nonnegative vector is required')
    integer(rank,1,len(v),'rank')
    m=0
    while m<rank-1 and v[m]>sum(v[m:])/(rank-m):
        m+=1
    tail=sum(v[m:])/(rank-m)
    return v[:m]+(tail,)*(rank-m)+(F(0),)*(len(v)-rank)

def root_interval(values: Iterable[F], bits: int=80) -> tuple[F,F]:
    integer(bits,1,4096,'bits')
    v=tuple(rational(x) for x in values)
    if not v or any(x<0 for x in v):
        raise ValueError('A nonempty nonnegative vector is required')
    v=tuple(x for x in v if x)
    if len(v)<2:return F(0),F(0)
    low,high=F(0),sum(v)
    for _ in range(bits):
        mid=(low+high)/2
        test=sum(x/(x+mid) for x in v)-1
        if test==0:return mid,mid
        if test>0:low=mid
        else:high=mid
    return low,high

def certify(data: dict) -> dict:
    if not isinstance(data,dict):raise ValueError('Input must be an object')
    allowed={'spectrum','old_dimension','fresh_dimension','t','bits'}
    if set(data)-allowed:raise ValueError('Unknown input keys: '+str(sorted(set(data)-allowed)))
    if 'spectrum' not in data or not isinstance(data['spectrum'],list):raise ValueError('spectrum must be a list')
    v=tuple(rational(x) for x in data['spectrum']);d=len(v)
    if d<2 or any(x<0 for x in v) or sum(v)!=1:raise ValueError('At least two nonnegative eigenvalues summing to one required')
    v=tuple(sorted(v,reverse=True));k=integer(data.get('old_dimension',d),1,d,'old_dimension')
    ell=integer(data.get('fresh_dimension',d),1,d,'fresh_dimension');r=min(k,ell)
    bits=integer(data.get('bits',80),1,4096,'bits');t=rational(data.get('t','1'))
    if not 0<=t<=1:raise ValueError('t must lie in [0,1]')
    q=majorant(v,r);a,b=root_interval(q,bits);na,nb=root_interval(v[:r],bits)
    L=2*(d+1)-t*t;base=F(d+1)/L;scale=t*t/(2*L)
    intervals=lambda pair:[str(x) for x in pair]
    result={'schema':'gtf94.spectral-value/1','status':'success','dimension':d,
      'spectrum':list(map(str,v)),'old_dimension':k,'fresh_dimension':ell,'active_rank':r,
      'initial_rank':sum(x>0 for x in v),'t':str(t),'prior_alternative':str(base),
      'majorant':list(map(str,q)),'root_interval':intervals((a,b)),
      'score_interval':intervals((base+scale*a,base+scale*b)),
      'no_message_comparison':{'old_dimension':d,'fresh_dimension':r,
        'score_interval':intervals((base+scale*na,base+scale*nb)),
        'strict_gain_criterion':bool(t>0 and 2<=r<sum(x>0 for x in v)),
        'gain_interval':intervals((scale*(a-nb),scale*(b-na)))},
      'root_enclosure_width_bound':str(F(1,2**bits)),
      'scope':{'rational_spectral_arithmetic':True,'spectrum_supplied_not_measured':True,
        'rank_cuts_as_defined_in_manuscript':True,'shared_device_index':True,
        'equal_prior_formula_claimed':False,'physical_reset_calibration':False,
        'continuum_proof_by_replay':False,'independent_priority_clearance':False,
        'general_efficient_design_synthesis':False}}
    if a==b and a>0:
        bs=[x/(x+a)**2 for x in q];total=sum(bs)
        result['fresh_eigenvalues_for_majorant_atom']=list(map(str,(x/total for x in bs)))
    return result

def main() -> int:
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('input',type=Path);p.add_argument('--output',type=Path)
    args=p.parse_args()
    try:
        out=json.dumps(certify(json.loads(args.input.read_text())),indent=2,sort_keys=True)+'\n'
        if args.output:args.output.write_text(out)
        else:print(out,end='')
    except (OSError,ValueError,TypeError) as exc:
        p.exit(2,'spectral_value: '+str(exc)+'\n')
    return 0
if __name__=='__main__':raise SystemExit(main())
