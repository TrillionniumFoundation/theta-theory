#!/usr/bin/env python3
"""Exact finite regression of v72 arithmetic and interfaces, not universal proofs."""
from __future__ import annotations
import copy
from fractions import Fraction as F
import hashlib
from itertools import product as cart
import json
from pathlib import Path
import random
import subprocess
import sys
import tempfile
import readout_codec as c
from check_preparation import from_factors, matrix_rank
from check_conditional import same
from instrument_streaming import zero
from choi_streaming import Instrument

ROOT=Path(__file__).resolve().parent
COUNT=0
NEG=[]

def require(ok,msg):
    global COUNT
    COUNT+=1
    if not ok:raise RuntimeError(msg)

def rejects(name,fn):
    try:fn()
    except (ValueError,TypeError,KeyError,IndexError,ZeroDivisionError,ArithmeticError):NEG.append(name)
    else:raise RuntimeError('negative control escaped: '+name)

def row(n,vecs):
    factors=[]
    for cols in vecs:
        a=zero(n)
        for j,col in enumerate(cols):
            for i,z in enumerate(col):a[i][j]=z
        factors.append(a)
    return from_factors(factors)

def example(d=2):
    L=c.gi(d)
    for i in range(d):
        for j in range(i):L[i][j]=(F(i+1,j+2),F((-1)**i,j+3))
    P=c.flag_from_chart(list(reversed(range(d))),L)
    rr=[]
    for x in range(d):
        rr.append(row(2,[[[(x+2,0),(1,x+1)]],[]] if x%2==0 else [[],[[(2,1),(3,0)]]]))
    return c.target_to_dict(P,rr)

def bounds(raw):
    P,rr=c.target_from_dict(raw)
    return [[matrix_rank(A) for A in a.outcomes] for a in rr]

def chart_checks():
    rng=random.Random(7246);cases=0
    for d in range(1,6):
        for j in range(10):
            L=c.gi(d)
            for i in range(d):
                for k in range(i):L[i][k]=(F(rng.randint(-7,7),rng.randint(1,7)),F(rng.randint(-5,5),rng.randint(1,9)))
            perm=list(range(d));rng.shuffle(perm)
            P=c.flag_from_chart(perm,L);p,U=c.flag_chart(P)
            require(c.flag_from_chart(p,U)==P,'pivoted LU preserves ordered flag')
            require(all(c.abs2(U[i][k])<=1 for i in range(d) for k in range(i)),'bounded LU multipliers')
            require(c.flag_from_dict(c.flag_to_dict(P))==P,'rational flag envelope')
            for B in [1,3,17]:
                w=c.flag_encode(P,B);Q=c.flag_decode(w,d)
                require(len(w['digits'])==d*(d-1),'phase-free coordinate dimension')
                q2=sum(c.frob2(a,b) for a,b in zip(P,Q))
                # q^2 <= d*(4K)^2*b/B^2, a stronger intermediate estimate.
                require(q2<=F(16*d*(2*d)**(2*d-2)*d*(d-1),B*B),'flag projector perturbation bound')
                require(d*q2<=F(c.flag_constant(d)**2,B*B),'one-use block bound certificate')
                c.validate_flag(Q);cases+=1
    # Rational projections may have no normalized Gaussian-rational lift.
    L=c.gi(3);L[1][0]=c.ONE;L[2][0]=c.ONE
    P=c.flag_from_chart([0,1,2],L)
    require(all(z==(F(1,3),F(0)) for row_ in P[0] for z in row_),'rank-one rational all-ones/3 projector')
    require(c.flag_from_chart(*c.flag_chart(P))==P,'no square root of three is required')
    return cases

def codec_checks():
    rng=random.Random(7204);cases=0
    for d,n,m in [(1,1,2),(2,1,2),(2,2,2),(3,1,2),(3,2,2)]:
        for rep in range(4):
            L=c.gi(d)
            for i in range(d):
                for k in range(i):L[i][k]=(F(rng.randrange(-5,6),7),F(rng.randrange(-5,6),11))
            P=c.flag_from_chart(list(range(d)),L);rr=[]
            for x in range(d):
                factors=[]
                for y in range(m):
                    A=zero(n)
                    if (x+y+rep)%3:
                        for i in range(n):
                            for k in range(1+(rep% n)):A[i][k]=(rng.randrange(-3,4),rng.randrange(-3,4))
                    factors.append(A)
                if all(all(z==(0,0) for r in a for z in r) for a in factors):factors[-1][-1][0]=(1,0)
                rr.append(from_factors(factors))
            t=c.target_to_dict(P,rr);ranks=bounds(t)
            for N,e in [(1,F(1,16)),(7,F(1,100))]:
                enc=c.encode(t,N,e,ranks);Q,ss=c.decode_parts(enc)
                require(c.verify(t,enc),'canonical target replay')
                out=c.assemble(Q,ss);out.validate()
                require(enc['flag_dimension']==d*d-d,'flag dimension d squared minus d')
                require(enc['row_dimension']==sum(c.prep.rank_dimension(n,r) for r in ranks),'conditional dimension')
                require(F(enc['basis_error_upper'])<=e/2,'basis budget')
                require(F(enc['row_error_squared_upper'])<=e*e/4,'row budget')
                for x,(a,b) in enumerate(zip(rr,ss)):
                    for y,(old,new) in enumerate(zip(a.outcomes,b.outcomes)):
                        r=matrix_rank(old);s=matrix_rank(new)
                        require(s<=r,'rank nonincrease')
                        require(r!=0 or s==0,'zero conditional block')
                        require(matrix_rank(out.outcomes[x*m+y])==s,'rank of flagged Choi product')
                cases+=1
    t=example(3);P,rr=c.target_from_dict(t)
    A=zero(2);A[0][0]=(10**24,0);A[1][1]=(1,0)
    rr[0]=from_factors([A,zero(2)])
    t=c.target_to_dict(P,rr);enc=c.encode(t,15,F(1,10**8),bounds(t))
    require(c.verify(t,enc),'tiny positive eigenvalue and large denominator')
    # Pure programme product trace distances are exact without eigenvalue routines.
    t=example(2);P,rr=c.target_from_dict(t)
    for N in [1,3,11]:
        enc=c.encode(t,N,F(1,50),bounds(t));_,ss=c.decode_parts(enc);overlap=F(1)
        for a,b in zip(rr,ss):
            z=c.Z
            for A,B in zip(a.outcomes,b.outcomes):
                z=c.ga(z,c.sumg(c.gm((F(A[i][j][0],a.denominator),F(A[i][j][1],a.denominator)),(F(B[j][i][0],b.denominator),F(B[j][i][1],b.denominator))) for i in range(2) for j in range(2)))
            require(z[1]==0 and 0<=z[0]<=1,'pure flagged overlap')
            overlap*=z[0]**N
        require(4*(1-overlap)<=F(enc['row_error_squared_upper']),'exact pure programme tensor bound')
    return cases+4

def exact_probability(Px,rho):
    z=c.sumg(c.gm(Px[i][j],rho[j][i]) for i in range(len(Px)) for j in range(len(Px)))
    require(z[1]==0,'real probability');return z[0]

def outcome_paths(P,rr,N):
    d=len(P);m=len(rr[0].outcomes);out={}
    # Inputs depend on both preceding x and y, but not private state.
    def rec(h,p):
        if len(h)==N:out[h]=p;return
        k=(sum(x+2*y for x,y in h)+len(h))%d
        for x,a in enumerate(rr):
            px=P[x][k][k][0]
            for y,A in enumerate(a.outcomes):rec(h+((x,y),),p*px*F(A[0][0][0],a.denominator))
    rec((),F(1));return out

def interfaces():
    L=c.gi(2);L[1][0]=(F(0),F(1));P=c.flag_from_chart([0,1],L)
    rr=[Instrument(1,1,1,[[[(1,0)]]]) for _ in range(2)]
    inst=c.assemble(P,rr)
    den,rho=c.integer_matrices([P[0]])
    out=inst.branch(rho[0],0)
    prob=F(out[0][0][0],inst.denominator*den)
    require(prob==1,'complex input-first Choi transpose')
    wrong=[[c.gc(z) for z in row_] for row_ in P[0]]
    require(exact_probability(wrong,P[0])==0,'omitting transpose changes complex probabilities')
    common=row(2,[[[(1,1),(2,0)]],[]]);rows=[common,common]
    standard=[[[c.ONE if i==j==x else c.Z for j in range(2)] for i in range(2)] for x in range(2)]
    require(same(c.assemble(P,rows,False),c.assemble(standard,rows,False)),'equal unflagged rows erase basis exactly')
    require(not same(c.assemble(P,rows),c.assemble(standard,rows)),'retained readout prevents this collapse')
    require(not same(c.assemble(P,rows),c.assemble(list(reversed(P)),rows)),'label permutations are not gauge')
    t=example(2);P,rr=c.target_from_dict(t);emb=c.assemble(P,rr,False,True);flagged=c.assemble(P,rr)
    d,n,m=len(P),rr[0].n,len(rr[0].outcomes)
    for x,y,i,j,k,l in cart(range(d),range(m),range(d),range(d),range(n),range(n)):
        a=emb.outcomes[y][i*d*n+x*n+k][j*d*n+x*n+l]
        b=flagged.outcomes[x*m+y][i*n+k][j*n+l]
        require(all(u*flagged.denominator==v*emb.denominator for u,v in zip(a,b)),'orthogonal output support recovers label')
    # Known two-query perfect discrimination of computational/Hadamard measurement.
    H=[[(F(1,2),F(0)),(F(1,2),F(0))],[(F(1,2),F(0)),(F(1,2),F(0))]]
    Q=[H,[[c.gs(c.gi(2)[i][j],H[i][j]) for j in range(2)] for i in range(2)]]
    def bell_events(flag):
        return [sum(((-1)**(i+j))*c.gm(flag[x][j][i],flag[y][j][i])[0]/2 for i in range(2) for j in range(2)) for x,y in cart(range(2),repeat=2)]
    p,q=bell_events(standard),bell_events(Q)
    require(sum(p)==sum(q)==1 and sum(abs(a-b) for a,b in zip(p,q))==2,'two-shot projective discrimination exact example')
    # Actual classical adaptive paths in the observable family.
    L=c.gi(2);L[1][0]=(F(2,7),F(0));P=c.flag_from_chart([0,1],L)
    rr=[Instrument(1,1,13,[[[(2,0)]],[[(11,0)]]]),Instrument(1,1,13,[[[(9,0)]],[[(4,0)]]])]
    t=c.target_to_dict(P,rr)
    for N in range(1,5):
        enc=c.encode(t,N,F(1,8),[[1,1],[1,1]]);Q,ss=c.decode_parts(enc)
        p,q=outcome_paths(P,rr,N),outcome_paths(Q,ss,N)
        require(sum(p.values())==sum(q.values())==1,'adaptive path normalization')
        require(sum(abs(p[h]-q[h]) for h in p)<=F(1,8),'adaptive path error within requested unhalved norm')


def seizing():
    for p in [[F(1),F(0),F(0),F(0)],[F(1,4)]*4,[F(1,7),F(2,7),F(0),F(4,7)],[F(1,10**30),1-F(1,10**30),F(0),F(0)]]:
        a=c.pauli_channel(p);q=c.seize_pauli(a)
        require(q==p,'Pauli Bell seizing exact identity')
        require(same(c.pauli_channel(q),a),'Pauli retraction fixed point')
        require(matrix_rank(a.outcomes[0])==sum(z>0 for z in p),'Pauli Choi rank equals support')
        den,ints=c.integer_matrices([[[(z,F(0))]] for z in p]);s=Instrument(1,1,den,ints)
        for B in [3,21,1001]:
            code=c.prep.encode(s,B,[int(z>0) for z in p]);r=c.prep.decode(code)
            pp=[F(A[0][0][0],r.denominator) for A in r.outcomes]
            require(all(z!=0 or w==0 for z,w in zip(p,pp)),'Pauli encoder keeps zero probabilities')
            require(matrix_rank(c.pauli_channel(pp).outcomes[0])<=matrix_rank(a.outcomes[0]),'Pauli encoder rank nonincrease')
    U=[[(F(1,2),F(1,2)),(F(1,2),F(1,2))],[(F(-1,2),F(1,2)),(F(1,2),F(-1,2))]]
    require(c.mm(U,c.adj(U))==c.gi(2),'rank-increase example is unitary')
    v=[U[k][i] for i in range(2) for k in range(2)]
    den,mats=c.integer_matrices([[[c.gm(a,c.gc(b)) for b in v] for a in v]])
    a=Instrument(2,2,den,mats);a.validate();p=c.seize_pauli(a)
    require(matrix_rank(a.outcomes[0])==1 and p==[F(1,4)]*4,'unitary Bell distribution')
    require(matrix_rank(c.pauli_channel(p).outcomes[0])==4,'arbitrary-centre retraction increases rank')


def negatives():
    t=example(2);raw=c.encode(t,5,F(1,50),bounds(t))
    changes={'wrong-schema':('schema','x'),'extra-field':('extra',1),'bool-horizon':('horizon',True),
      'wrong-horizon':('horizon',6),'zero-error':('requested_unhalved_error','0'),
      'maximal-error':('requested_unhalved_error','2'),'noncanonical-error':('requested_unhalved_error','2/100'),
      'overcount-column-phases':('flag_dimension',3),'wrong-row-dimension':('row_dimension',1),
      'wrong-basis-certificate':('basis_error_upper','0'),'wrong-row-certificate':('row_error_squared_upper','1'),
      'wrong-payload':('fixed_length_bits',0),'wrong-row-grid':('row_grid',1),'row-count':('rows',raw['rows'][:1])}
    for name,(k,v) in changes.items():
        q=copy.deepcopy(raw);q[k]=v;rejects(name,lambda q=q:c.decode_parts(q))
    for name,k,v in [('duplicate-permutation','permutation',[0,0]),('bool-permutation','permutation',[False,True]),('missing-digit','digits',[]),('out-of-range-digit','digits',[raw['flag']['grid']+1,0]),('extra-flag-field','extra',0)]:
        q=copy.deepcopy(raw);q['flag'][k]=v;rejects(name,lambda q=q:c.decode_parts(q))
    q=copy.deepcopy(raw);q['flag']['digits'][0]+=1
    rejects('altered-valid-body-target-replay',lambda:c.verify(t,q))
    q=copy.deepcopy(raw);q['rows'][0]['body_hex']='0'+q['rows'][0]['body_hex']
    rejects('row-noncanonical-body',lambda:c.decode_parts(q))
    tt=copy.deepcopy(t);tt['rows'].reverse();rejects('wrong-target',lambda:c.verify(tt,raw))
    rejects('rank-violation',lambda:c.encode(t,1,F(1,2),[[0,1],[0,1]]))
    tt=copy.deepcopy(t);tt['flag']['projectors'][0][0][0][0]+=1
    rejects('nonprojective-target',lambda:c.target_from_dict(tt))
    tt=copy.deepcopy(t);tt['rows']=tt['rows'][:1]
    rejects('target-row-count',lambda:c.target_from_dict(tt))
    rejects('nonfraction-error',lambda:c.encode(t,1,0.1))
    rejects('malformed-pauli-simplex',lambda:c.pauli_channel([F(1)]*4))
    rejects('complex-zero-divisor',lambda:c.gd(c.ONE,c.Z))


def cli():
    inp=ROOT/'inputs/varying-readout-qubit.json'
    require(json.loads(inp.read_text())==example(2),'committed rational qubit input')
    require(json.loads((ROOT/'inputs/varying-readout-qutrit.json').read_text())==example(3),'committed rational qutrit input')
    cmd=[sys.executable,str(ROOT/'readout_codec.py')]
    with tempfile.TemporaryDirectory() as tmp:
        p=Path(tmp)/'code.json'
        z=subprocess.run(cmd+['encode','--input',str(inp),'--horizon','12','--error','1/100','--ranks','[[1,0],[0,1]]'],capture_output=True,check=True)
        p.write_bytes(z.stdout)
        a=subprocess.run(cmd+['decode','--input',str(p)],capture_output=True,check=True)
        Instrument.from_dict(json.loads(a.stdout)).validate()
        v=subprocess.run(cmd+['verify','--input',str(inp),'--certificate',str(p)],capture_output=True,check=True)
        require(json.loads(v.stdout)['target_bound'],'actual CLI canonical replay')
        q=json.loads(p.read_text());q['extra']='bad';p.write_text(json.dumps(q))
        no=subprocess.run(cmd+['verify','--input',str(inp),'--certificate',str(p)],capture_output=True)
        require(no.returncode==2,'CLI rejects noncanonical certificate')
        return hashlib.sha256(z.stdout).hexdigest()


def main():
    chart=chart_checks();codes=codec_checks();interfaces();seizing();negatives();digest=cli()
    print(json.dumps({'schema':'gtf72.readout-regression/1','status':'success','exact_assertions':COUNT,
        'flag_chart_cases':chart,'codec_cases':codes,'negative_controls':NEG,'cli_example_sha256':digest,
        'arithmetic':'Gaussian rational pairs and integer operations; no floating-point oracle',
        'scope':'Finite identities, codecs and explicit tester examples only. Not continuum covering, all adaptive testers, the imported measurement-discrimination theorem, or independent priority.'},indent=2,sort_keys=True))

if __name__=='__main__':main()
