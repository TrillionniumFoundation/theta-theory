#!/usr/bin/env python3
"""Finite comparison/normalization fixtures; not a continuum proof certificate."""
from __future__ import annotations
from fractions import Fraction as F
import itertools
import json
import math
from pathlib import Path
import subprocess
import tempfile

def require(ok: bool, message: str) -> None:
    if not ok: raise RuntimeError(message)

def overlap(a,b,c,d):
    return max(F(0),min(b,d)-max(a,c))

def checks():
    counts={'positive_balance':0,'interval_comparison':0,'physical_overlap':0,
            'stationary_arms':0,'old_clock_failure':0,'schedule':0,
            'nested_git_enumeration':0}
    values=[F(0),F(1,10),F(1,2),F(1),F(3),F(11)]
    for C,D,kappa in itertools.product(values,values,[F(1,3),F(1),F(4),F(17)]):
        alpha=min(F(1),kappa*D/C) if C else F(0)
        require(0<=alpha<=1,'positive split')
        require(alpha*C<=kappa*D,'paid positive comparison')
        require((1-alpha)*C==max(F(0),C-kappa*D),'exact comparison deficit')
        counts['positive_balance']+=3
    # Each angle is represented by an atom only for this finite fixture.
    # The continuum argument uses angular integrals and Fubini, not atoms.
    for sign in (-1,1):
        source=[(F(0),F(1),F(1,3)),(F(1,5),F(4,5),F(2,3))]
        donor=[(F(-1),F(2),F(1,4)),(F(-2),F(3),F(1,2))]
        r=F(1,2);C=sum(x[2] for x in source);D=sum(x[2] for x in donor)
        for kappa in (F(1,4),F(1),F(2),F(10)):
            alpha=min(F(1),kappa*D/C)
            for t in [F(j,20) for j in range(-20,41)]:
                for selectors in itertools.product((F(0),F(1,3),F(1)),repeat=2):
                    lhs=alpha*sum(w*h for (a,b,w),h in zip(source,selectors) if a<t<b)
                    lo,hi=(t,t+r) if sign==1 else (t-r,t)
                    rhs=kappa/r*sum(w*overlap(lo,hi,a,b) for a,b,w in donor)
                    require(lhs<=rhs,'one-sided original selector comparison')
                    counts['interval_comparison']+=1
    for N in (1,2,3,7):
        for a,b in itertools.product(range(6),repeat=2):
            multiplicities=[min(a,N),min(b,N)]
            weights=[F(1,7),F(11,13)]
            require(sum(x*w for x,w in zip(multiplicities,weights))<=N*sum(weights),
                    'physical comparison overlap, not chamber cardinality')
            counts['physical_overlap']+=1
    lam=9*math.sqrt(19)/200;Lam=47/6
    for k,mu,dfrac in itertools.product((1,2,3,5,9,17,31),(0.01,0.2,0.75,1.),(0.,.2,.5)):
        x1=.5**(1/k);x2=2.**(1/k);x3=3.**(1/k)
        require(x3-x2>=x1*math.log(1.5)/k*(1-1e-12),'stationary width ratio')
        require(x1/(x3-x2)<=k/math.log(1.5)*(1+1e-12),'stationary comparison balance')
        require(dfrac+.5<=1 and dfrac+3<4,'actual residence collar')
        require(Lam/lam*x1/(mu*(x3-x2))<=Lam/lam*k/(mu*math.log(1.5))*(1+1e-12),
                'incoming angular Hessian and average outgoing fraction')
        counts['stationary_arms']+=4
    for k,q in itertools.product((2,3,5,9),(0.01,0.1,0.5)):
        x=10.**(-6*k);s=q/16
        forward=k*x**(k-1)*((x**k+1)**(1/k)-x)
        backward=x**k
        require(forward+backward<q,'outgoing gap clock can fail')
        require(4*s<q,'relative clock can fail')
        require(.5**(1/k)/(3**(1/k)-2**(1/k))<=k/math.log(1.5)*(1+1e-12),
                'positive interval comparison still holds')
        counts['old_clock_failure']+=3
    require(F(1,16)-F(1,32)==F(1,32),'growing balance budget')
    require(F(4)-F(1)-F(1,32)==F(95,32),'guard variation exponent')
    require(F(1,12)*F(1,32)==F(1,384),'recovered B exponent')
    require(F(1,12)*F(1,16)==F(1,192),'uniform arm B exponent')
    counts['schedule']+=4
    counts['paid_trace_deficit']=0
    for P,E,kappa in itertools.product(values,values,[F(1,4),F(1),F(7)]):
        if E>P:continue
        D=P-E
        for frac in (F(0),F(1,3),F(1)):
            C=frac*kappa*P
            require(max(F(0),C-kappa*D)<=kappa*E,'entire positive shortage paid by trace variation')
            counts['paid_trace_deficit']+=1
    counts['common_critical_window']=0
    for a,tau,ell in itertools.product([F(i,5) for i in range(-5,6)],(F(1,10),F(1,2),F(9,10)),(F(2),F(3),F(7,2))):
        t=a+tau
        require(t-F(1)<a and a+ell<t+F(4),'all comparison interiors in one original-roof window')
        counts['common_critical_window']+=1
    # Regression for the actual v103 failure: ls-tree run below the root
    # silently applies the cwd prefix unless --full-tree is supplied.
    with tempfile.TemporaryDirectory(prefix='a2dyn-full-tree-') as td:
        root=Path(td);paper=root/'papers/P';(paper/'core').mkdir(parents=True)
        (paper/'core/one.tex').write_text('proof\n');(paper/'README.md').write_text('source\n')
        def git(*args,cwd=root):
            return subprocess.check_output(['git',*args],cwd=cwd,stderr=subprocess.DEVNULL)
        git('init','-q');git('add','.');tree=git('write-tree').decode().strip()
        pt=git('rev-parse',tree+':papers/P').decode().strip()
        broken=git('ls-tree','-rz',pt,cwd=paper)
        fixed=git('ls-tree','-rz','--full-tree',pt,cwd=paper)
        require(broken==b'','nested cwd reproduces empty inherited enumeration')
        names=[x.split(b'\t',1)[1].decode() for x in fixed.split(b'\0') if x]
        require(sorted(names)==['README.md','core/one.tex'],'full-tree enumerates complete baseline')
        counts['nested_git_enumeration']+=2
    return {'counts':counts,'total_checks':sum(counts.values()),
            'scope':'finite rational comparisons, numerical stationary profiles and nested-Git regression',
            'formal_proof_certificate':False,'independent_human_review':False,
            'full_raw_return_LLT_proved':False}
if __name__=='__main__':print(json.dumps(checks(),indent=2,sort_keys=True))
