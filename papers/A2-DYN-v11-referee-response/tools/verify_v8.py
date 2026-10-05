#!/usr/bin/env python3
"""Exact source preservation and finite algebra checks; not a continuum proof."""
from __future__ import annotations
from fractions import Fraction as F
from pathlib import Path
import hashlib
import itertools
import json
import math
import re

ROOT = Path(__file__).resolve().parents[1]

def require(ok: bool, message: str) -> None:
    if not ok:
        raise RuntimeError(message)

def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def zero(n):
    return [[F(0) for _ in range(n)] for _ in range(n)]

def mul(a,b):
    return [[sum(a[i][k]*b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]

def add(a,b):
    return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]

def scale(a,s):
    return [[s*x for x in row] for row in a]

def power(a,k):
    out=eye(len(a))
    for _ in range(k):
        out=mul(out,a)
    return out

def inv(a):
    n=len(a)
    a=[row[:]+unit for row,unit in zip(a,eye(n))]
    for j in range(n):
        piv=next(i for i in range(j,n) if a[i][j])
        a[j],a[piv]=a[piv],a[j]
        d=a[j][j]
        a[j]=[x/d for x in a[j]]
        for i in range(n):
            if i != j:
                d=a[i][j]
                a[i]=[x-d*y for x,y in zip(a[i],a[j])]
    return [row[n:] for row in a]

def source_check():
    manifest=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
    for name,expected in manifest['preserved_core_sha256'].items():
        require(hashlib.sha256((ROOT/'core'/name).read_bytes()).hexdigest()==expected,
                'changed preceding mathematical source: '+name)
    for name,expected in manifest['preserved_tools_sha256'].items():
        require(hashlib.sha256((ROOT/'tools'/name).read_bytes()).hexdigest()==expected,
                'changed historical diagnostic: '+name)
    main=(ROOT/'main.tex').read_text()
    require('A2-DYN, revision 8' in main,'revision metadata')
    names=re.findall(r'\\input\{(core/[^}]+)\}',main)
    require(len(names)==len(set(names))==21,'complete unique core inclusion')
    text=main+'\n'+'\n'.join((ROOT/(x+'.tex')).read_text() for x in names)
    labels=re.findall(r'\\label\{([^}]+)\}',text)
    require(len(labels)==len(set(labels)),'duplicate labels')
    refs=re.findall(r'\\(?:eqref|ref|pageref|autoref)\{([^}]+)\}',text)
    require(not (set(refs)-set(labels)),'unresolved cross-references')
    # Check balanced explicit proof environments, not the validity of proofs.
    begins=text.count(r'\begin{proof}')
    require(begins==text.count(r'\end{proof}'),'unbalanced proof environments')
    required=('thm:cumulative-return-tail','prop:linear-count-budget',
              'thm:common-renewal','thm:common-scale-holomorphy')
    require(all(x in labels for x in required),'missing new statements')
    return {'preserved_core_files':len(manifest['preserved_core_sha256']),
            'preserved_historical_scripts':len(manifest['preserved_tools_sha256']),
            'included_core_files':len(names),'labels':len(labels),'proof_environments':begins,
            'tex_sha256':{str(x.relative_to(ROOT)):hashlib.sha256(x.read_bytes()).hexdigest()
                          for x in sorted(ROOT.rglob('*.tex'))}}

def model_check():
    checks=0
    for size,section in ((7,[0,2,5]),(8,[0,1,4,6])):
        weights=[F(-1 if i%3==0 else 1) for i in range(size)]
        A=zero(size)
        for i in range(size): A[(i+1)%size][i]=weights[i]
        P=zero(size)
        for i in section: P[i][i]=F(1)
        Q=add(eye(size),scale(P,F(-1)))
        returns={}
        for i in section:
            j=i;length=0;phase=F(1)
            while True:
                phase*=weights[j]; j=(j+1)%size;length+=1
                if j in section: break
            returns[i]=(j,length,phase)
        R=[]
        for m in range(1,size+1):
            op=mul(mul(P,A),mul(power(mul(Q,A),m-1),P))
            direct=zero(size)
            for i,(j,length,phase) in returns.items():
                if length==m: direct[j][i]=phase
            require(op==direct,'first-return operator/order')
            R.append(op);checks+=1
        for m in range(1,2*size+1):
            lhs=mul(mul(P,power(A,m)),P)
            rhs=zero(size)
            for r in range(1,min(m,size)+1):
                rhs=add(rhs,mul(mul(mul(P,power(A,m-r)),P),R[r-1]))
            require(lhs==rhs,'chronological renewal coefficient');checks+=1
        for z in (F(1,3),F(-1,2)):
            Rz=zero(size)
            for m,op in enumerate(R,1): Rz=add(Rz,scale(op,z**m))
            U=mul(mul(P,inv(add(eye(size),scale(A,-z)))),P)
            induced=[[Rz[i][j] for j in section] for i in section]
            Usection=[[U[i][j] for j in section] for i in section]
            require(Usection==inv(add(eye(len(section)),scale(induced,F(-1)))),
                    'exact rational resolvent identity');checks+=1
            schur=add(scale(mul(mul(P,A),P),z),
                      scale(mul(mul(mul(mul(mul(P,A),Q),
                      inv(add(eye(size),scale(mul(mul(Q,A),Q),-z)))),Q),mul(A,P)),z*z))
            require(schur==Rz,'exact rational Schur identity');checks+=1
            for n in range(1,9):
                paired=sum(sum(row) for row in power(induced,n))/len(section)
                actual=F(0)
                for i in section:
                    current=i;count=0;phase=F(1)
                    for _ in range(n):
                        j,length,w=returns[current]
                        count+=length;phase*=w;current=j
                    actual+=z**count*phase
                require(paired==actual/len(section),'dependent n-return pairing');checks+=1
    # The deterministic counting comparison holds before any expectation.
    for length in range(0,8):
        for symbols in itertools.product((0,1,2),repeat=length):
            visits=sum(x>0 for x in symbols)
            chi=sum(F(x,2) for x in symbols)
            for n in (1,2,4,8):
                if visits<n:
                    require(chi<=n-1,'soft-count comparison')
                checks+=1
    # Cutoff budgets, including exponentially growing bands.
    for n in (1,10,100,1000):
        a,c,logC,logM=0.2,0.03,math.log(5),math.log(3)
        for kappa,delta in ((0.0,0.1),(0.4,0.2),(2.0,1.0)):
            logV=kappa*n
            L=math.ceil((a*n+max(0,logC+logM+logV+delta*n))/c)
            require(logC+logM+logV+a*n-c*L<=-delta*n+1e-10,
                    'linear finite-band error budget');checks+=1
    return checks

def main():
    out=source_check()
    out.update(status='passed',finite_checks=model_check(),
               scope='exact source hashes, syntactic references, rational finite invertible models, cutoff algebra',
               continuum_proofs_verified_by_tests=False,full_raw_LLT_verified=False,
               independent_human_review=False)
    print(json.dumps(out,indent=2,sort_keys=True))

if __name__=='__main__':
    main()
