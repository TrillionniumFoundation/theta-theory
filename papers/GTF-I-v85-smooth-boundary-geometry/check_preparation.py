#!/usr/bin/env python3
"""Exact finite regression for the v68 coding and local testing estimates."""
from __future__ import annotations
import copy
from fractions import Fraction as F
from math import comb
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import hashlib
import preparation_codec as c
import choi_streaming as old
from instrument_streaming import zero,product,adjoint,trace

ROOT=Path(__file__).resolve().parent
COUNT=0
NEG=[]

def require(condition,message):
    global COUNT
    COUNT+=1
    if not condition:raise RuntimeError(message)

def rejects(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError):NEG.append(name)
    else:raise RuntimeError('negative control escaped: '+name)

def bern_tv(N,p,q):
    return sum(F(comb(N,j))*abs(p**j*(1-p)**(N-j)-q**j*(1-q)**(N-j)) for j in range(N+1))/2

def binary_cases():
    cases=0
    for N in [1,2,3,4,9,16,25,49,100]:
        for i in range(13):
            for j in range(i,13):
                p,q=F(i,12),F(j,12);tv=bern_tv(N,p,q)
                require(tv*tv>=F(9,1024)*min(N*(p-q)**2,1),'uniform local binary lower bound')
                cases+=1
    for N in [1,2,5,16,81]:
        for den in [10**3,10**12,10**40]:
            for p in [F(0),F(1,den),F(1,2),F(1)-F(2,den)]:
                q=p+F(1,den);tv=bern_tv(N,p,q)
                require(tv*tv>=F(9,1024)*min(N*(q-p)**2,1),'tiny gap and rare probability lower bound')
                cases+=1
    return cases

def from_factors(factors,d=1):
    blocks=[product(x,adjoint(x)) for x in factors];n=len(blocks[0])
    T=sum(trace(x) for x in blocks)
    return c.lift_blocks(blocks,d,n,T)

def block_f2(a,b):
    A,B=c.preparation_blocks(a),c.preparation_blocks(b)
    return sum((F(x,a.denominator)-F(y,b.denominator))**2 for u,v in zip(A,B)
               for r,s in zip(u,v) for z,w in zip(r,s) for x,y in zip(z,w))

def matrix_rank(mat):
    # Independent elimination over Gaussian rationals, not the codec's PSD pivots.
    A=[[(F(x),F(y)) for x,y in row] for row in mat]
    n=len(A);rank=0
    for j in range(n):
        ix=next((i for i in range(rank,n) if A[i][j]!=(0,0)),None)
        if ix is None:continue
        A[rank],A[ix]=A[ix],A[rank]
        u=A[rank][j];den=u[0]*u[0]+u[1]*u[1]
        row=[]
        for x in A[rank]:
            z=c.mul(x,c.conj(u));row.append((z[0]/den,z[1]/den))
        A[rank]=row
        for i in range(n):
            if i==rank:continue
            t=A[i][j]
            A[i]=[(x[0]-y[0],x[1]-y[1]) for x,y in zip(A[i],[c.mul(t,x) for x in row])]
        rank+=1
    return rank

def code_cases():
    rng=random.Random(6801);cases=0
    example=None
    for n in range(1,5):
        for m in range(1,4):
            for iteration in range(8):
                factors=[];ranks=[]
                for y in range(m):
                    A=zero(n);r=rng.randrange(n+1)
                    # Some factors have leading zero rows and nonleading pivots.
                    start=n-r if iteration%2 else 0
                    for i in range(start,n):
                        for j in range(r):A[i][j]=(rng.randint(-7,7),rng.randint(-7,7))
                    factors.append(A)
                if not sum(trace(product(A,adjoint(A))) for A in factors):factors[0][n-1][0]=(1,0)
                target=from_factors(factors,d=1+iteration%2)
                original=c.preparation_blocks(target)
                ranks=[matrix_rank(x) for x in original]
                pivots,data=c.triangular_data(original,target.denominator)
                require([len(p) for p in pivots]==ranks,'Schur rank equals independent rank')
                require(sum(q for _,q in data)==1,'factor squares sum to one')
                for B in [1,3,17,4096]:
                    raw=c.encode(target,B,ranks);got=c.decode(raw)
                    require(c.verify(target,raw),'target-bound exact replay')
                    out=c.preparation_blocks(got)
                    require(sum(trace(x) for x in out)==got.denominator,'decoded trace one')
                    require(all(old.rational_psd(x) for x in out),'decoded exact positive semidefinite blocks')
                    require(all(matrix_rank(x)<=r for x,r in zip(out,ranks)),'no block rank increase')
                    require(all(x==zero(n) for x,r in zip(out,ranks) if r==0),'zero outcomes exact')
                    require(block_f2(target,got)<=F(raw['one_use_error_squared_upper']),'actual Frobenius difference bounded')
                    anchor=max(range(len(data)),key=lambda i:data[i][1]);aq=data[anchor][1]
                    for _,q in data:
                        z=c.sqrt_floor(B*B*q/aq)
                        require(z*z<=B*B*q/aq<(z+1)*(z+1),'exact signed factor floor')
                    require(B*B<=got.denominator<=raw['factor_coordinates']*B*B,'normalization denominator bound')
                    require(c.body_capacity(B,raw['factor_coordinates'])<=c.body_capacity(B,raw['rank_family_dimension']+1),'fixed alphabet capacity')
                    cases+=1
                ad=c.adaptive(target,37,F(1,100),ranks)
                require(c.verify(target,ad),'adaptive target-bound replay')
                require(F(ad['error_squared_upper'])<=F(1,10000),'adaptive certificate sufficient')
                if n==3 and m==3 and iteration==3:example=target
    require(example is not None,'boundary example produced')
    # A genuinely rank-deficient, zero-outcome input with a very small eigenvalue.
    factors=[zero(3) for _ in range(3)]
    factors[0][0][0]=(10**35,0);factors[0][1][1]=(1,0)
    factors[1][2][0]=(1,3)
    tiny=from_factors(factors,2)
    raw=c.adaptive(tiny,10**6,F(1,10**12),[2,1,0])
    got=c.validate_adaptive(raw)
    require(c.verify(tiny,raw),'extreme rational eigenvalue certificate')
    require(c.preparation_blocks(got)[2]==zero(3),'known zero at extreme precision')
    for y,r in zip(c.preparation_blocks(got),[2,1,0]):require(matrix_rank(y)<=r,'extreme example ranks')
    # Input dimension cannot change the preparation distance or encoded factor payload.
    base=c.preparation_blocks(tiny)
    same=c.lift_blocks(base,1,3,tiny.denominator)
    one=c.encode(same,64,[2,1,0]);two=c.encode(tiny,64,[2,1,0])
    require(one['body_hex']==two['body_hex'] and one['fixed_length_bits']==two['fixed_length_bits'],'erased input dimension does not affect factor code')
    return cases,tiny

def product_cases():
    cases=0
    # Pure-state trace distance after N copies is exactly computable by its square.
    for n in [2,3,4]:
        for t in range(1,10):
            A=zero(n)
            for i in range(n):A[i][0]=(t-i,i+1)
            target=from_factors([A]);sigma=c.preparation_blocks(target)[0]
            for B in [1,2,7,100]:
                raw=c.encode(target,B,[1]);got=c.decode(raw);tau=c.preparation_blocks(got)[0]
                st=product(sigma,tau)
                require(sum(st[i][i][1] for i in range(n))==0,'Hermitian product trace real')
                overlap=F(sum(st[i][i][0] for i in range(n)),target.denominator*got.denominator)
                require(0<=overlap<=1,'pure-state overlap')
                for N in [1,2,3,9,40]:
                    actual_sq=4*(1-overlap**N)
                    require(actual_sq<=N*F(raw['one_use_error_squared_upper']),'pure product error squared')
                    cases+=1
    for p in [F(0),F(1,10000),F(1,5),F(1,2),F(1)]:
        target=c.lift_blocks([[[(p.numerator,0)]],[[(p.denominator-p.numerator,0)]]],1,1,p.denominator)
        for B in [1,3,17,1000]:
            raw=c.encode(target,B);got=c.decode(raw)
            q=F(got.outcomes[0][0][0][0],got.denominator)
            for N in [1,2,10,50]:
                require(4*bern_tv(N,p,q)**2<=N*F(raw['one_use_error_squared_upper']),'classical product upper bound')
                cases+=1
    return cases

def negative_cases(target):
    good=c.encode(target,64,[2,1,0])
    changes=[('zero-grid','grid',0),('bool-grid','grid',True),('wrong-convention','convention','output-first'),
        ('all-zero-ranks','rank_bounds',[0,0,0]),('over-rank','rank_bounds',[4,1,0]),
        ('float-rank','rank_bounds',[2.0,1,0]),('rank-length','rank_bounds',[2,1]),
        ('duplicate-pivots','pivot_sets',[[0,0],[2],[]]),('unordered-pivots','pivot_sets',[[1,0],[2],[]]),
        ('negative-pivot','pivot_sets',[[-1],[2],[]]),('false-zero-block','pivot_sets',[[0,1],[2],[0]]),
        ('wrong-coordinates','factor_coordinates',0),('wrong-dimension','rank_family_dimension',0),
        ('wrong-bits','fixed_length_bits',0),('empty-body','body_hex',''),('noncanonical-hex','body_hex','00'),
        ('signed-body','body_hex','-1'),('overlong-body','body_hex','f'*10000),('wrong-error','one_use_error_squared_upper','0')]
    for name,key,value in changes:
        bad=copy.deepcopy(good);bad[key]=value
        rejects(name,lambda b=bad:c.decode(b))
        require(not c.verify(target,bad),'tampered certificate '+name)
    bad=copy.deepcopy(good);bad['body_hex']=format(c.body_capacity(64,bad['factor_coordinates']),'x')
    rejects('body-out-of-range',lambda:c.decode(bad))
    rejects('zero-divisor',lambda:c.triangular_data(c.preparation_blocks(target),0))
    rejects('zero-pivot-nonzero-row',lambda:c.triangular_data([[[(0,0),(1,0)],[(1,0),(1,0)]]],1))
    rejects('false-rank-promise',lambda:c.encode(target,64,[1,1,0]))
    # Identity channel is CP/TP but is not a preparation channel.
    omega=[(1,0),(0,0),(0,0),(1,0)]
    J=[[c.mul(x,c.conj(y)) for y in omega] for x in omega]
    unitary=old.Instrument(2,2,1,[J]);unitary.validate()
    rejects('nonpreparation-identity-channel',lambda:c.encode(unitary,64))
    rejects('noninteger-grid',lambda:c.encode(target,F(5),[2,1,0]))
    rejects('zero-horizon',lambda:c.adaptive(target,0,F(1,100)))
    rejects('float-error',lambda:c.adaptive(target,4,0.01))
    rejects('zero-error',lambda:c.adaptive(target,4,F(0)))
    ad=c.adaptive(target,100,F(1,32),[2,1,0])
    for name,key,value in [('bad-adaptive-bound','error_squared_upper','0'),('bad-adaptive-horizon','horizon',True),
        ('noncanonical-error','requested_unhalved_error','2/64'),('false-accuracy','requested_unhalved_error','1/100000000000000000000')]:
        x=copy.deepcopy(ad);x[key]=value;rejects(name,lambda z=x:c.validate_adaptive(z))
    altered=c.lift_blocks(list(reversed(c.preparation_blocks(target))),target.d,target.n,target.denominator)
    require(not c.verify(altered,good),'legal code does not certify another target');NEG.append('wrong-target-replay')
    singleton=c.lift_blocks([[[(0,0)]],[[(1,0)]],[[(0,0)]]],3,1,1)
    ss=c.encode(singleton,1,[0,1,0]);require(ss['fixed_length_bits']==0,'public singleton takes zero payload')
    sb=copy.deepcopy(ss);sb['body_hex']='1';rejects('singleton-extra-word',lambda:c.decode(sb))

def cli_cases():
    source=ROOT/'inputs/preparation-boundary.json'
    with tempfile.TemporaryDirectory() as td:
        code=Path(td)/'code.json'
        result=subprocess.run([sys.executable,str(ROOT/'preparation_codec.py'),'adaptive','--input',str(source),
            '--horizon','1000','--error','1/1000','--ranks','[2,1,0]'],capture_output=True,check=True)
        code.write_bytes(result.stdout)
        subprocess.run([sys.executable,str(ROOT/'preparation_codec.py'),'decode','--input',str(code)],capture_output=True,check=True)
        ver=subprocess.run([sys.executable,str(ROOT/'preparation_codec.py'),'verify','--input',str(source),'--certificate',str(code)],capture_output=True,check=True)
        require(json.loads(ver.stdout)['status']=='success','CLI target verification')
        bad=subprocess.run([sys.executable,str(ROOT/'preparation_codec.py'),'encode','--input',str(source),'--grid','0'],capture_output=True)
        require(bad.returncode==2,'CLI bad grid rejects');NEG.append('CLI-bad-grid')
    return hashlib.sha256(result.stdout).hexdigest()

def main():
    binary=binary_cases();words,target=code_cases();products=product_cases();negative_cases(target);cli=cli_cases()
    print(json.dumps({'schema':'gtf68.exact-regression/1','status':'success','exact_assertions':COUNT,
        'binary_cases':binary,'code_cases':words,'product_cases':products,'negative_controls':NEG,
        'cli_sha256':cli,'uses_float_decisions':False,
        'scope':'Exact finite checks of binary inequalities, rational factors, CP/TP, ranks, zero outcomes, product errors, parsing and target-bound certificates. Not universal proof or priority certification.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
