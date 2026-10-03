#!/usr/bin/env python3
"""Exact finite regression, not a proof of continuum metric-entropy theorems."""
from __future__ import annotations
import copy
from fractions import Fraction as F
import hashlib
from itertools import product as cartesian
import json
from math import comb
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import conditional_codec as c
from check_preparation import matrix_rank, from_factors
from instrument_streaming import zero, product, adjoint, trace
from choi_streaming import Instrument

ROOT=Path(__file__).resolve().parent
COUNT=0
NEG=[]


def require(ok, message):
    global COUNT
    COUNT += 1
    if not ok: raise RuntimeError(message)


def rejects(name, fn):
    try: fn()
    except (ValueError, TypeError, KeyError, IndexError, ZeroDivisionError): NEG.append(name)
    else: raise RuntimeError('negative control escaped: '+name)


def same(a,b):
    return a.d==b.d and a.n==b.n and len(a.outcomes)==len(b.outcomes) and all(
        x*b.denominator==y*a.denominator
        for A,B in zip(a.outcomes,b.outcomes) for ra,rb in zip(A,B)
        for za,zb in zip(ra,rb) for x,y in zip(za,zb))


def example():
    n=3
    A=zero(n); A[0][0]=(2,0); A[2][0]=(1,1)
    B=zero(n); B[1][0]=(1,0)
    row0=from_factors([A,B,zero(n)])
    C=zero(n); C[2][0]=(3,0)
    D=zero(n); D[0][0]=(1,0); D[1][1]=(2,1)
    row1=from_factors([zero(n),C,D])
    return c.join([row0,row1])


def rank_bounds(t):
    return [[matrix_rank(mat) for mat in a.outcomes] for a in c.rows(t)]


def randomized_codes():
    rng=random.Random(7103); cases=0
    for d,n,m in cartesian([1,2,3],[1,2,3],[1,2,3]):
        for iteration in range(4):
            rr=[]
            for x in range(d):
                factors=[]
                for y in range(m):
                    A=zero(n); r=rng.randrange(n+1)
                    start=n-r if iteration%2 else 0
                    for i in range(start,n):
                        for j in range(r): A[i][j]=(rng.randint(-3,3),rng.randint(-3,3))
                    factors.append(A)
                if not sum(trace(product(A,adjoint(A))) for A in factors):
                    factors[-1][n-1][0]=(1,0)
                rr.append(from_factors(factors))
            target=c.join(rr); ranks=rank_bounds(target)
            for N,error in [(1,F(7,4)),(3,F(1,4)),(20,F(1,1000))]:
                raw=c.encode(target,N,error,ranks); decoded=c.decode(raw); decoded.validate()
                require(c.verify(target,raw),'canonical replay')
                require(same(target,c.join(c.rows(target))),'row extraction/join identity')
                require(same(decoded,c.retract(decoded)),'decoded fixed-point identity')
                V=sum(c.prep.rank_dimension(n,r) for r in ranks)
                require(raw['rank_family_dimension']==V,'rank dimension')
                B=raw['grid']; q=F(16*N*V)/error**2
                require(B*B>=q and (B==1 or (B-1)**2<q),'least sufficient integer grid')
                require(F(raw['error_squared_upper'])<=error**2,'squared accuracy certificate')
                require(raw['fixed_length_bits']==sum(a['fixed_length_bits'] for a in raw['rows']),'payload sum')
                bound=1
                for old,new,code in zip(c.rows(target),c.rows(decoded),raw['rows']):
                    bound*=code['factor_coordinates']*B*B
                    for a,b in zip(old.outcomes,new.outcomes):
                        require(matrix_rank(b)<=matrix_rank(a),'conditional rank nonincrease')
                        require(trace(a)!=0 or trace(b)==0,'exact zero conditional block')
                require(decoded.denominator<=bound,'expanded denominator bound')
                cases+=1
    # Very small positive eigenvalues and a nonleading pure pivot.
    A=zero(3);A[0][0]=(10**30,0);A[2][1]=(1,0)
    B=zero(3);B[2][0]=(1,0)
    t=c.join([from_factors([A,zero(3)]),from_factors([zero(3),B])])
    require(c.verify(t,c.encode(t,100,F(1,10**12),rank_bounds(t))),'extreme eigenvalue ratio')
    return cases+1


def pure_product_bounds():
    cases=0
    for d in [1,2,3]:
        rr=[]
        for x in range(d):
            A=zero(2);A[0][0]=(3+x,0);A[1][0]=(4,x)
            rr.append(from_factors([A]))
        t=c.join(rr)
        for N,e in cartesian([1,2,8,31],[F(1,50),F(1,4),F(3,2)]):
            raw=c.encode(t,N,e,[[1] for _ in rr]); s=c.decode(raw)
            affinity=F(1)
            for a,b in zip(c.rows(t),c.rows(s)):
                mat=product(a.outcomes[0],b.outcomes[0])
                require(sum(mat[i][i][1] for i in range(a.n))==0,'real trace of PSD product')
                h=sum(mat[i][i][0] for i in range(a.n))
                z=F(h,a.denominator*b.denominator)
                require(0<=z<=1,'pure overlap range');affinity*=z**N
            exact_sq=4*(1-affinity)
            require(exact_sq<=F(raw['error_squared_upper']),'tensor programme pure trace bound')
            cases+=1
    return cases


def classical_paths(t,N,rule):
    rr=c.rows(t);out={}
    def rec(history,p):
        if len(history)==N:out[history]=p;return
        x=rule(history)%len(rr);r=rr[x]
        for y,mat in enumerate(r.outcomes):
            prob=F(mat[0][0][0],r.denominator)
            rec(history+(y,),p*prob)
    rec((),F(1));return out


def adaptive_classical():
    rr=[Instrument(1,1,10,[[[(1,0)]],[[(9,0)]]]),
        Instrument(1,1,10,[[[(7,0)]],[[(3,0)]]])]
    t=c.join(rr);cases=0
    for N,e in cartesian(range(1,6),[F(1,5),F(5,4)]):
        raw=c.encode(t,N,e,[[1,1],[1,1]]);s=c.decode(raw)
        for a,b in cartesian(range(3),range(3)):
            rule=lambda h:a*sum(h)+b*len(h)+(h[-1] if h else 0)
            P,Q=classical_paths(t,N,rule),classical_paths(s,N,rule)
            norm=sum(abs(P[k]-Q[k]) for k in P)
            require(norm**2<=F(raw['error_squared_upper']),'adaptive classical transcript bound')
            cases+=1
    require(classical_paths(t,1,lambda h:0)!=classical_paths(t,1,lambda h:1),'outcome depends on input')
    return cases


def geometry_and_retraction():
    bell=zero(4)
    for i,j in cartesian([0,3],repeat=2):bell[i][j]=(1,0)
    identity=Instrument(2,2,1,[bell]);identity.validate()
    rejects('coherent-target-is-not-silently-dephased',lambda:c.rows(identity))
    r=c.retract(identity)
    require(same(r,c.retract(r)),'retraction is idempotent')
    require(matrix_rank(bell)==1 and matrix_rank(r.outcomes[0])==2,'centre retraction may increase rank')
    require(r.outcomes[0][0][3]==(0,0) and bell[0][3]==(1,0),'retraction removes Bell Choi coherence')
    for n in range(1,5):
        for d in range(1,5):
            for m in range(1,5):
                b=m*(d*n)**2;C0=2*d*d*b*b
                for N in [1,b,max(1,b-1),b+1,2*b-1,3*b]:
                    if N<b:require(F(d*d)<=F(C0,N),'small sample zero estimator')
                    else:require(F(d*d*b,N//b)<=F(C0,N),'finite estimator variance bound')
    for k in [1,2,5,13]:
        for p in [F(0),F(1,1000),F(1,2),F(1)]:
            mean=sum(F(comb(k,j))*p**j*(1-p)**(k-j)*F(2*j-k,k) for j in range(k+1))
            var=sum(F(comb(k,j))*p**j*(1-p)**(k-j)*(F(2*j-k,k)-mean)**2 for j in range(k+1))
            require(mean==2*p-1 and var==4*p*(1-p)/k,'signed mean and variance identity')
    # Four mutually singular targets are all covered by one uniform centre
    # at unhalved error 3/2: a one-target-per-centre argument would be false.
    delta=F(3,2);K=4
    require((1-delta/2)*K==1 and 2<2*delta,'large-error multiplicity control')
    for cap in [F(1,32),F(1),F(3,2),F(199,100)]:
        eta=(2-cap)/4
        require(1-eta-cap/2==eta and eta>0,'submaximal-error common-event coefficient')


def negative_controls():
    t=example();r=c.encode(t,7,F(1,100),rank_bounds(t))
    modifications={'wrong-grid':('grid',r['grid']+1),'bool-grid':('grid',True),
      'wrong-horizon':('horizon',8),'bool-horizon':('horizon',True),
      'zero-error':('requested_unhalved_error','0'),'maximal-error':('requested_unhalved_error','2'),
      'noncanonical-error':('requested_unhalved_error','2/200'),
      'wrong-error-certificate':('error_squared_upper','0'),
      'wrong-dimension':('rank_family_dimension',0),'wrong-bits':('fixed_length_bits',0),
      'wrong-schema':('schema','gtf68.preparation-code/1'),'row-count':('rows',r['rows'][:1]),
      'empty-rank-row':('rank_bounds',[[0,0,0],r['rank_bounds'][1]])}
    for name,(key,val) in modifications.items():
        q=copy.deepcopy(r);q[key]=val;rejects(name,lambda q=q:c.decode(q))
    for name,key,val in [('row-grid','grid',1),('row-input-dimension','input_dimension',2),
                         ('noncanonical-body','body_hex','0'+r['rows'][0]['body_hex'])]:
        q=copy.deepcopy(r);q['rows'][0][key]=val;rejects(name,lambda q=q:c.decode(q))
    swapped=c.join(list(reversed(c.rows(t))))
    rejects('wrong-target-replay',lambda:c.verify(swapped,r))
    q=copy.deepcopy(r);q['extra']='unbound';rejects('extra-field-target-binding',lambda:c.verify(t,q))
    rejects('rank-bound-violation',lambda:c.encode(t,1,F(1,10),[[0,1,0],[0,1,1]]))
    rejects('negative-square-root',lambda:c.ceil_sqrt(F(-1)))
    rejects('non-fraction-error',lambda:c.encode(t,1,0.1))


def cli():
    source=ROOT/'inputs/conditional-boundary.json'
    require(same(Instrument.from_dict(json.loads(source.read_text())),example()),'committed target example')
    cmd=[sys.executable,str(ROOT/'conditional_codec.py')]
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/'code.json'
        z=subprocess.run(cmd+['encode','--input',str(source),'--horizon','100','--error','1/1000','--ranks','[[1,1,0],[0,1,2]]'],capture_output=True,check=True)
        p.write_bytes(z.stdout)
        a=subprocess.run(cmd+['decode','--input',str(p)],capture_output=True,check=True)
        Instrument.from_dict(json.loads(a.stdout)).validate()
        v=subprocess.run(cmd+['verify','--input',str(source),'--certificate',str(p)],capture_output=True,check=True)
        require(json.loads(v.stdout)['target_bound'],'real CLI canonical replay')
        r=subprocess.run(cmd+['retract','--input',str(source)],capture_output=True,check=True)
        require(same(Instrument.from_dict(json.loads(r.stdout)),example()),'CLI retraction')
        bad=subprocess.run(cmd+['encode','--input',str(source),'--horizon','0','--error','1/2'],capture_output=True)
        require(bad.returncode==2,'CLI failure status')
        return hashlib.sha256(z.stdout).hexdigest()


def main():
    codecases=randomized_codes();purecases=pure_product_bounds();pathcases=adaptive_classical()
    geometry_and_retraction();negative_controls();digest=cli()
    print(json.dumps({'schema':'gtf71.conditional-regression/1','status':'success',
       'exact_assertions':COUNT,'code_cases':codecases,'pure_programme_cases':purecases,
       'adaptive_classical_policy_cases':pathcases,'negative_controls':NEG,
       'cli_example_sha256':digest,'uses_floating_point_decisions':False,
       'scope':'Exact finite legality, ranks, row-dependent policies, rational certificates, estimator variance identities and multiplicity controls. Does not prove continuum coding, optimal learning, independent priority or general quantum simulation.'},sort_keys=True,indent=2))

if __name__=='__main__':main()
