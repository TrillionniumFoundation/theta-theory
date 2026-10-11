#!/usr/bin/env python3
"""Exact finite diagnostics, not proofs of the continuum theorems."""
from __future__ import annotations
import argparse, hashlib, itertools, json, random, subprocess, sys
from fractions import Fraction as F
from pathlib import Path
import numpy as np
ROOT=Path(__file__).resolve().parent
COUNTS={}
def check(ok,category):
    if not ok: raise RuntimeError('finite diagnostic failed: '+category)
    COUNTS[category]=COUNTS.get(category,0)+1

def eye(n):return [[F(i==j) for j in range(n)] for i in range(n)]
def zero(m,n):return [[F(0) for _ in range(n)] for _ in range(m)]
def add(a,b):return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def sub(a,b):return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def scale(a,x):return [[v*x for v in row] for row in a]
def mul(a,b):return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def norm(a):return max(sum(abs(v) for v in row) for row in a)
def inv(a):
    n=len(a);x=[a[i][:]+eye(n)[i] for i in range(n)]
    for j in range(n):
        k=next((k for k in range(j,n) if x[k][j]),None)
        if k is None:raise RuntimeError('singular exact matrix')
        x[j],x[k]=x[k],x[j];v=x[j][j];x[j]=[z/v for z in x[j]]
        for i in range(n):
            if i!=j:
                v=x[i][j];x[i]=[u-v*w for u,w in zip(x[i],x[j])]
    return [row[n:] for row in x]
def reach(p):
    n=len(p);r=[[bool(p[i][j]) or i==j for j in range(n)] for i in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):r[i][j]=r[i][j] or (r[i][k] and r[k][j])
    return r

def projection(p):
    n=len(p);r=reach(p);classes=[];seen=set()
    for i in range(n):
        if i in seen:continue
        c=[j for j in range(n) if r[i][j] and r[j][i]];seen.update(c)
        if all(not p[a][b] for a in c for b in range(n) if b not in c):classes.append(c)
    recurrent=set(sum(classes,[]));t=[i for i in range(n) if i not in recurrent];pi=zero(n,n)
    for c in classes:
        k=len(c);a=[[F(i==j)-p[c[j]][c[i]] for j in range(k)] for i in range(k)]
        a[-1]=[F(1)]*k;b=[[F(i==k-1)] for i in range(k)];stationary=mul(inv(a),b)
        for i in c:
            for j,jj in enumerate(c):pi[i][jj]=stationary[j][0]
    if t:
        fundamental=inv([[F(i==j)-p[ii][jj] for j,jj in enumerate(t)] for i,ii in enumerate(t)])
        for c in classes:
            h=mul(fundamental,[[sum(p[i][j] for j in c)] for i in t])
            for k,i in enumerate(t):
                for j in c:pi[i][j]+=h[k][0]*pi[c[0]][j]
    return pi,classes

def group(p):
    pi,c=projection(p);return sub(inv(add(sub(eye(len(p)),p),pi)),pi),pi,c

def polyadd(a,b):
    x=[F(0)]*max(len(a),len(b))
    for i,v in enumerate(a):x[i]+=v
    for i,v in enumerate(b):x[i]+=v
    return x

def polymul(a,b):
    x=[F(0)]*(len(a)+len(b)-1)
    for i,u in enumerate(a):
        for j,v in enumerate(b):x[i+j]+=u*v
    return x

def detpoly(a):
    n=len(a)
    if n==0:return [F(1)]
    out=[F(0)]*(n+1)
    for perm in itertools.permutations(range(n)):
        sign=(-1)**sum(perm[i]>perm[j] for i in range(n) for j in range(i+1,n));term=[F(sign)]
        for i,j in enumerate(perm):term=polymul(term,a[i][j])
        out=polyadd(out,term)
    return out

def finite_matrices():
    rng=random.Random(250010);cases=[]
    for n in range(1,5):
        cases.append(eye(n));cases.append([[F(j==(i+1)%n) for j in range(n)] for i in range(n)])
        for _ in range(28):
            p=[]
            for i in range(n):
                nums=[rng.randrange(4) if rng.randrange(3) else 0 for _ in range(n)]
                if not sum(nums):nums[i]=1
                p.append([F(x,sum(nums)) for x in nums])
            cases.append(p)
    for p in cases:
        n=len(p);I=eye(n);G,Pi,classes=group(p);A=sub(I,p);Z=zero(n,n)
        for x,y in [(mul(A,G),sub(I,Pi)),(mul(G,A),sub(I,Pi)),(mul(Pi,G),Z),(mul(G,Pi),Z),(mul(Pi,Pi),Pi),(mul(p,Pi),Pi)]:check(x==y,'group_inverse_exact')
        power=I;total=zero(n,n)
        for k in range(1,13):
            total=add(total,power);power=mul(power,p)
            check(sub(total,scale(Pi,k))==mul(sub(I,power),G),'cesaro_identity_exact')
        roots=[max(c,key=lambda j:Pi[c[0]][j]) for c in classes];rest=[i for i in range(n) if i not in roots]
        if rest:
            H=inv([[F(i==j)-p[ii][jj] for j,jj in enumerate(rest)] for i,ii in enumerate(rest)])
            check(max(sum(row) for row in H)<=(2*n+1)*norm(G),'root_hitting_bound_exact')
        d=[F(2+i%3) for i in range(n)];S=[[F(i==j)-(F(i==j)-p[i][j])/d[i] for j in range(n)] for i in range(n)]
        GS,PS,cs=group(S);check(cs==classes,'time_change_classes_exact')
        check(norm(GS)<=4*max(d)*(2*n+1)*norm(G),'time_change_group_bound_exact')
        L=sub(I,S);poly=[[[L[i][j],F(i==j)] for j in range(n)] for i in range(n)];coeff=detpoly(poly);k=len(classes)
        check(all(v==0 for v in coeff[:k]) and coeff[k]>0,'forest_denominator_exact')
        adj=zero(n,n)
        for i in range(n):
            for j in range(n):
                minor=[[poly[a][b] for b in range(n) if b!=i] for a in range(n) if a!=j]
                z=detpoly(minor);adj[i][j]=(-1)**(i+j)*(z[k-1] if len(z)>k-1 else 0)/coeff[k]
        check(adj==PS,'forest_projection_exact')
    for i in range(0,len(cases)-1,3):
        P=cases[i];Q=cases[i+1]
        if len(P)!=len(Q):continue
        G,Pi,_=group(P);H,Pj,_=group(Q);E=sub(Q,P)
        check(sub(Pj,Pi)==add(mul(mul(Pj,E),G),mul(mul(H,E),Pi)),'projection_perturbation_exact')
    # The counted Q x J lift, including reducible and periodic boundary chains.
    for P in cases[:60]:
        q=len(P);j=2;A=zero(q*j,q);K=zero(q,q*j)
        for a in range(q):
            for b in range(j):A[a*j+b][a]=1
            for c in range(q):
                K[a][c*j]=P[a][c]/3;K[a][c*j+1]=2*P[a][c]/3
        Pstar=mul(A,K);G,Pi,_=group(P);Gs,Pis,_=group(Pstar)
        check(mul(K,A)==P,'counted_lift_exact')
        check(Pis==mul(mul(A,Pi),K),'counted_lift_exact')
        check(Gs==add(sub(eye(q*j),Pis),mul(mul(A,G),K)),'counted_lift_exact')
        check(norm(Gs)<=2+norm(G),'counted_lift_exact')

def queue_and_renewal():
    for p in [F(1,10),F(1,4),F(2,5)]:
        q=1-p;b=q-p
        def m(w):return F(w)/b
        def s(w):return F(w*w)/(b*b)+4*p*q*w/(b*b*b)
        for w in range(1,30):
            check(m(w)==1+p*m(w+1)+q*m(w-1),'queue_moment_equations_exact')
            check(s(w)==1+2*(p*m(w+1)+q*m(w-1))+p*s(w+1)+q*s(w-1),'queue_moment_equations_exact')
    check(F(1,4)*2+F(3,4)/2==F(7,8),'queue_17_constants_exact')
    check(15+3==18 and F(18,2)==9,'queue_17_constants_exact')
    for a in [F(3,16),F(1,4),F(1,2),F(3,4)]:
        for b in [F(3,16),F(1,4),F(1,2),F(3,4)]:
            for d0,d1 in itertools.product([F(2),F(5,2),F(3)],repeat=2):
                for c0,c1 in itertools.product([F(0),F(1,4),F(1,2),F(1)],repeat=2):
                    r0=d0*c0;r1=d1*c1;g=(b*r0+a*r1)/(b*d0+a*d1);f0=r0-g*d0;f1=r1-g*d1
                    span=abs(f0-f1)/(a+b)
                    check(span<=8,'queue_17_bias_exact')
    for eta in [F(1,4),F(1,10),F(1,100)]:
        for n in range(1,30):
            prob=F(0);cost=F(0)
            for _ in range(n):cost+=prob;prob=eta+(1-2*eta)*prob
            check(cost/n==F(1,2)-(1-(1-2*eta)**n)/(4*eta*n),'metastable_rate_exact')
    P=[[F(0),F(1,2),F(1,2)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]];d=[F(2),F(2),F(4)];r=[F(0),F(0),F(4)]
    S=[[F(i==j)-(F(i==j)-P[i][j])/d[i] for j in range(3)] for i in range(3)]
    _,Pi,_=group(P);_,PS,_=group(S)
    check(sum(PS[0][i]*r[i]/d[i] for i in range(3))==F(1,2),'multichain_ratio_counterexample_exact')
    check(sum(Pi[0][i]*r[i] for i in range(3))/sum(Pi[0][i]*d[i] for i in range(3))==F(2,3),'multichain_ratio_counterexample_exact')
    rng=random.Random(117)
    for _ in range(80):
        pmfs=[]
        for i in range(3):
            w=[rng.randint(1,5) for _ in range(6)];pmfs.append([F(x,sum(w)) for x in w])
        K=max(sum(prob*(t+1)**2 for t,prob in enumerate(pmf)) for pmf in pmfs)
        for N in range(1,15):
            tails=sum(max(sum(prob*max(0,t+1-s) for t,prob in enumerate(pmf)) for pmf in pmfs) for s in range(N+1))
            check(tails<=3*K,'conditional_moment_finite_label_factor_exact')

def joint_task():
    for e in [F(1,2),F(1,8),F(1,32)]:
        # Complete common-task records include true, nonreplaceable audit B.
        target={};source={}
        for rare,prob in [(0,1-e),(1,e)]:
            for bit in [0,1]:
                target[(rare,bit,bit)]=target.get((rare,bit,bit),0)+prob/2
                if rare:
                    for guess in [0,1]:source[(rare,guess,bit)]=source.get((rare,guess,bit),0)+prob/4
                else:source[(rare,bit,bit)]=source.get((rare,bit,bit),0)+prob/2
        tv=sum(abs(target.get(k,0)-source.get(k,0)) for k in set(target)|set(source))/2
        check(tv==e/2,'fresh_bit_task_defect_exact')
        for decision in [F(i,16) for i in range(17)]:
            check(((decision-1)**2+decision**2)/2>=F(1,4),'fresh_bit_readout_lower_exact')
        for delta in [F(0),F(1,10),F(1,2),F(1)]:
            for decision in [F(i,10) for i in range(-10,11)]:
                check(((decision-delta)**2+(decision+delta)**2)/2==decision**2+delta**2,'fixed_calibration_lower_exact')
    for k in range(1,16):
        e=F(1,2**k);ell=2**((k+1)//2);mu=2+e*(ell-1);moment=4*(1-e)+e*(ell+1)**2
        check(moment<=13,'rare_long_second_moment_exact')
        check(e*ell/(4*mu)>0,'attained_long_cycle_error_exact')

def quantum_diagnostics():
    s=np.diag(np.sqrt([.25,.75]));pauli=np.array([[0.,1.],[1.,0.]]);z=np.diag([1.,-1.])
    previous=None
    for angle in np.linspace(.1,1.1,11):
        u=np.array([[np.cos(angle),-np.sin(angle)],[np.sin(angle),np.cos(angle)]])
        k=s@u;js=[]
        for j,v in enumerate([.25,.75]):
            a=np.zeros((2,2));a[0,j]=np.sqrt(1-v);js.append(a@u)
        complete=k.T@k+sum((a.T@a for a in js),np.zeros((2,2)))
        check(np.max(np.abs(complete-np.eye(2)))<1e-12,'quantum_finite_matrix_diagnostic')
        check(np.linalg.eigvalsh(k.T@k).max()<=.75+1e-12,'quantum_finite_matrix_diagnostic')
        check(all(np.linalg.matrix_rank(a,tol=1e-10)==1 for a in js),'quantum_finite_matrix_diagnostic')
        if previous is not None:check(np.linalg.norm(k@previous-previous@k)>1e-4,'quantum_noncommutation_diagnostic')
        previous=k
    c=.25;hs=[pauli,np.array([[0.,-1j],[1j,0.]]),z];effects=[(np.eye(2)+sgn*c*h)/6 for h in hs for sgn in [-1,1]]
    check(np.linalg.norm(sum(effects)-np.eye(2))<1e-12,'informationally_complete_effects_diagnostic')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    finite_matrices();queue_and_renewal();joint_task();quantum_diagnostics()
    cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(ROOT.parent/'r24-renewal-geometry'/'regression.py')]
    child=subprocess.run(cmd,text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    if child.returncode:raise RuntimeError('retained R24 regression failed: '+child.stderr)
    inherited=json.loads(child.stdout)
    result={'status':'PASS','native_checks':sum(COUNTS.values()),'categories':COUNTS,'exact_arithmetic':'Fraction for all identities except explicitly labeled finite quantum diagnostics','inherited_R24':inherited,'inherited_output_sha256':hashlib.sha256(child.stdout.encode()).hexdigest(),'scope':'Finite checks are not proofs of any continuum theorem. Nested historical counts are not added to native_checks.'}
    text=json.dumps(result,sort_keys=True,indent=2)+'\n'
    if args.output:
        out=Path(args.output);out.mkdir(parents=True,exist_ok=True);(out/'R25_FINITE_CHECKS.json').write_text(text)
    print(text,end='')
if __name__=='__main__':main()
