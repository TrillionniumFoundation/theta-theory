#!/usr/bin/env python3
"""Exact finite regression witnesses; NOT proofs of arbitrary-kernel theorems."""
from __future__ import annotations
import argparse, hashlib, itertools, json
from fractions import Fraction as F
from functools import lru_cache
from pathlib import Path

COUNTS: dict[str,int] = {}
def check(ok: bool, group: str, detail: str='') -> None:
    if not ok:
        raise RuntimeError(f'{group}: {detail}')
    COUNTS[group] = COUNTS.get(group,0)+1

def eye(n): return [[F(i==j) for j in range(n)] for i in range(n)]
def add(a,b): return [[x+y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def neg(a): return [[-x for x in r] for r in a]
def scale(a,s): return [[x*s for x in r] for r in a]
def mm(a,b): return [[sum((a[i][k]*b[k][j] for k in range(len(b))),F(0)) for j in range(len(b[0]))] for i in range(len(a))]
def mv(a,v): return [sum((x*y for x,y in zip(r,v)),F(0)) for r in a]
def sub(a,b): return add(a,neg(b))
def inverse(a):
    n=len(a); w=[r[:]+q for r,q in zip(a,eye(n))]
    for j in range(n):
        pivot=next((i for i in range(j,n) if w[i][j]),None)
        if pivot is None: raise ValueError('singular matrix')
        w[j],w[pivot]=w[pivot],w[j]; den=w[j][j];w[j]=[x/den for x in w[j]]
        for i in range(n):
            if i!=j:
                c=w[i][j];w[i]=[x-c*y for x,y in zip(w[i],w[j])]
    return [r[n:] for r in w]
def matnorm(a):return max(sum(abs(x) for x in r) for r in a)
def proj2(p,q):
    if p+q==0:return eye(2)
    return [[q/(p+q),p/(p+q)]]*2

def exact_matrices():
    vals=[F(j,4) for j in range(5)]
    for p,q in itertools.product(vals,repeat=2):
        P=[[1-p,p],[q,1-q]]; Pi=proj2(p,q); I=eye(2)
        A=sub(I,P); G=sub(inverse(add(A,Pi)),Pi)
        for ok in [mm(A,G)==sub(I,Pi),mm(G,A)==sub(I,Pi),mm(G,Pi)==[[0,0],[0,0]],mm(P,Pi)==Pi]:
            check(ok,'group_inverse')
        power=I; acc=[[F(0)]*2 for _ in range(2)]
        for n in range(1,9):
            acc=add(acc,sub(power,Pi));power=mm(power,P)
            check(acc==mm(sub(I,power),G),'cesaro_identity')
            b=[F(2,3),F(-1,4)]
            u=[F(0),F(0)]; power2=I; average=[F(0),F(0)]
            for k in range(n):
                v=mv(power2,b);u=[x+(1-F(k,n))*y for x,y in zip(u,v)]
                power2=mm(power2,P)
                average=[x+y/F(n) for x,y in zip(average,mv(power2,b))]
            check(mv(A,u)==[x-y for x,y in zip(b,average)],'approximate_coboundary')
        for durations in ([[1,3],[2,1]],[[2,1],[1,3]],[[1,1],[1,1]]):
            T=[[P[i][j]*durations[i][j] for j in range(2)] for i in range(2)]
            d=[sum(row) for row in T]
            S=add(I,[[(P[i][j]-I[i][j])/d[i] for j in range(2)] for i in range(2)])
            Ps=proj2(S[0][1],S[1][0]); cost=[F(1,4),F(3,4)];r=[d[i]*cost[i] for i in range(2)]
            g=mv(Ps,cost); b=[x-y for x,y in zip(r,mv(T,g))]; u=mv(G,b)
            check(mv(P,g)==g,'marked_bias');check(mv(Pi,b)==[0,0],'marked_bias');check(mv(A,u)==b,'marked_bias')
            check(max(u)-min(u)<=2*max(d)*matnorm(G),'marked_constant')
            @lru_cache(None)
            def total(i,n):
                if n==0:return F(0)
                return sum((P[i][j]*(min(n,durations[i][j])*cost[i]+(total(j,n-durations[i][j]) if n>durations[i][j] else 0)) for j in range(2)),F(0))
            for n in range(1,13):
                tail=sum((max(sum((P[i][j]*max(durations[i][j]-t,0) for j in range(2)),F(0)) for i in range(2)) for t in range(1,n+1)),F(0))/n
                for i in range(2):
                    check(abs(total(i,n)/n-g[i])<=(max(u)-min(u))/n+tail,'physical_call_bound')
    P=[[F(0),F(1,2),F(1,2)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]]
    T=[[F(0),F(1,2),F(3,2)],[F(0),F(1),F(0)],[F(0),F(0),F(1)]]
    g=[F(1,2),F(0),F(1)]; r=[F(0),F(0),F(1)];u=[F(-3,2),F(0),F(0)]
    check(mv(sub(eye(3),P),u)==[x-y for x,y in zip(r,mv(T,g))],'duration_exit_counterexample')
    for n in range(3,31):
        actual=F(n-3,2*n)
        check(actual==F(1,2)-F(3,2*n),'duration_exit_counterexample')
    Pi=[[F(1),F(0)],[F(1),F(0)]]
    check(mv(Pi,[0,0])==[0,0],'task_visible_rank_change')
    check(mv(Pi,[0,1])!=[0,1],'task_visible_rank_change')

def diagnostic():
    def value(t,lam,n):
        # Exact geometric sum, avoiding repeated enormous rational powers.
        return t/2 if not lam else t*(1-(1-lam)**n)/(2*n*lam)
    for k in range(2,6):
        for den in range(2,10):
            a=F(1,den)
            for j in range(1,den+1):
                t=F(j,den);lam=t**k;span=max(t-a,0)/lam
                check(abs(t-lam*span)<=a,'corrector_residual')
                check(span<=a**(1-k),'corrector_price_upper')
                for n in (1,2,4,8,16):
                    risk=value(t,lam,n)
                    check(risk<=a+span/n,'corrector_risk_bound')
                    # Exact pair risk from the retained-label transition recurrence.
                    wrong=F(1,2);acc=F(0)
                    for _ in range(n):acc+=t*wrong;wrong*=1-lam
                    check(acc/n==risk,'retained_program_exact_risk')
            if a<=F(1,2):
                t=2*a
                check((t-a)/t**k==a**(1-k)/2**k,'corrector_price_lower')
        for ell in range(1,5):
            n=ell**k; invn=F(1,ell)
            for z in (0,2,3,4):
                e=F(0) if z==0 else F(1,z)**k; eroot=F(0) if z==0 else F(1,z)
                threshold=max(invn,eroot)
                for j in range(1,21):
                    t=F(j,20);lam=max(t**k-e,0)
                    check(value(t,lam,n)<=4*(invn+eroot),'erasure_uniform_upper')
                check(value(invn,max(invn**k-e,0),n)>=invn/4,'acquisition_lower')
                if e:check(value(eroot,F(0),n)==eroot/2,'blind_threshold_lower')
    for e in (F(0),F(1,8),F(1,4),F(1,2)):
        mu_plus=[e,F(0),1-e];mu_minus=[F(0),e,1-e]
        tv=lambda a,b:sum(abs(x-y) for x,y in zip(a,b))/2
        check(tv(mu_plus,mu_minus)==e,'deficiency_pair_distance')
        for a in range(9):
            for b in range(9-a):
                simulated=[F(a,8),F(b,8),1-F(a+b,8)]
                check(max(tv(simulated,mu_plus),tv(simulated,mu_minus))>=e/2,'deficiency_all_grid_laws')
    for M in range(2,100):
        J=M//2
        check(2*J<=M and J>=F(M,3),'counted_joint_state')

def singular_marks():
    for depth in range(1,8):
        points=[sum((F(2*b,3**(j+1)) for j,b in enumerate(bits)),F(0)) for bits in itertools.product((0,1),repeat=depth)]
        for k in range(depth+1):
            tail_mean=sum((F(1,3**j) for j in range(k+1,depth+1)),F(0))
            centers=[sum((F(2*b,3**(j+1)) for j,b in enumerate(bits)),F(0))+tail_mean for bits in itertools.product((0,1),repeat=k)]
            loss=sum((min((x-c)**2 for c in centers) for x in points),F(0))/len(points)
            check(loss==F(1,8)*(F(1,9**k)-F(1,9**depth)),'cantor_prefix_distortion')

def quantum_diagnostics():
    import numpy as np
    for c in (.2,.5,.8):
        a=np.sqrt((1+c)/2);b=np.sqrt((1-c)/2)
        psi=[np.array([0.,a,b]),np.array([0.,a,-b])];v=np.array([1.,0.,0.])
        vp=np.array([0.,b,a]);vm=np.array([0.,b,-a])
        Ep=np.outer(vp,vp)/(1+c);Em=np.outer(vm,vm)/(1+c);E0=np.eye(3)-Ep-Em
        for E in (Ep,Em,E0):check(np.linalg.eigvalsh(E).min()>-1e-12,'quantum_matrix_diagnostics')
        check(np.max(np.abs(Ep+Em+E0-np.eye(3)))<1e-12,'quantum_matrix_diagnostics')
        for k in (2,3,4):
            for t in (0.,.1,.4,.8,1.):
                states=[(1-t**k)*np.outer(v,v)+t**k*np.outer(p,p) for p in psi]
                for idx,rho in enumerate(states):
                    good=Ep if idx==0 else Em;bad=Em if idx==0 else Ep
                    check(abs(np.trace(good@rho)-(1-c)*t**k)<1e-12,'quantum_matrix_diagnostics')
                    check(abs(np.trace(bad@rho))<1e-12,'quantum_matrix_diagnostics')
                if t>0:
                    check(np.linalg.norm(states[0]@states[1]-states[1]@states[0])>0,'quantum_matrix_diagnostics')
        # The physically explicit realization uses two calls per diagnostic.
        check(np.isclose((1-c**2)/(1+c),1-c),'quantum_matrix_diagnostics')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output');args=ap.parse_args()
    exact_matrices();diagnostic();singular_marks();quantum_diagnostics()
    q=COUNTS.get('quantum_matrix_diagnostics',0)
    result={'status':'PASS','component':'R26 native finite regression','checks':sum(COUNTS.values()),'exact_rational_checks':sum(COUNTS.values())-q,'floating_quantum_diagnostics':q,'groups':dict(sorted(COUNTS.items())),'limitations':'Finite identities and witnesses only. Not a proof of arbitrary Borel compactness, continuum inequalities, quantifier-elimination correctness, or mathematical priority. Historical nested counts are not added.'}
    if args.output:
        out=Path(args.output);out.mkdir(parents=True,exist_ok=True);(out/'REGRESSION.json').write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':main()
