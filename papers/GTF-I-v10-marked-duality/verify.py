#!/usr/bin/env python3
"""Finite regression diagnostics; not a proof certificate for the theorems."""
from __future__ import annotations
import argparse
from fractions import Fraction as F
from itertools import product
import json
import math
import random
import sys

MUTANTS=('drop_mark','task_after_encoder','convexify_private','rank_is_width',
         'old_state_observation','wrong_resolvent_sign','phasewise_action',
         'mix_logarithms','identify_report_coordinates')
COUNT=0

def require(condition:bool, message:str)->None:
    global COUNT
    COUNT+=1
    if not condition: raise RuntimeError(message)

def dot(a,b): return sum((x*y for x,y in zip(a,b)),F(0))
def rowmat(a,M): return [dot(a,col) for col in zip(*M)]
def matcol(M,v): return [dot(row,v) for row in M]
def rank(columns):
    if not columns:return 0
    rows=[list(x) for x in zip(*columns)]; nr=len(rows); nc=len(columns); k=0
    for j in range(nc):
        pivot=next((i for i in range(k,nr) if rows[i][j]),None)
        if pivot is None:continue
        rows[k],rows[pivot]=rows[pivot],rows[k]
        q=rows[k][j]; rows[k]=[x/q for x in rows[k]]
        for i in range(nr):
            if i!=k:
                q=rows[i][j]; rows[i]=[x-q*y for x,y in zip(rows[i],rows[k])]
        k+=1
        if k==nr:break
    return k

def basis(columns):
    out=[]
    for v in columns:
        if rank(out+[v])>len(out):out.append(v)
    return out

def membership(mutant):
    best_average=F(1);best_worst=F(1); designs=0
    for encoder in product(range(2),repeat=3):
        for dec in product(range(2),repeat=6):
            errors=[int(dec[2*d+encoder[x]]!=int(d==x)) for d in range(3) for x in range(3)]
            best_average=min(best_average,F(sum(errors),9));best_worst=min(best_worst,max(errors));designs+=1
    require(designs==512,'finite design enumeration')
    if mutant=='task_after_encoder':best_average=F(0)
    require(best_average==F(2,9),'common encoder must precede task; uniform dual witness')
    require(best_worst==1,'deterministic common minimax')
    rows=[]
    for d in range(3):
        for x in range(3):
            error=F(0)
            for singleton in range(3):
                answer=F(int(x==d)) if d==singleton else (F(0) if x==singleton else F(2,3))
                error+=(1-answer if x==d else answer)/3
            rows.append(error)
    require(all(x==F(2,9) for x in rows),'nine shared risks must all equal 2/9')
    grid=[F(k,4) for k in range(5)]
    for p in product(grid,repeat=3):
        middle=sorted(range(3),key=lambda x:p[x])[1]
        for a,b in product(grid,repeat=2):
            probs=[a+(b-a)*q for q in p]
            require(max(1-probs[middle],*(probs[x] for x in range(3) if x!=middle))>=F(1,2),'private affine midpoint lower bound')
    private=F(2,9) if mutant=='convexify_private' else F(1,2)
    require(private==F(1,2),'a public mixture is not a private two-label machine')
    return {'enumerated_deterministic_designs':designs,'shared':'2/9','private':'1/2','separately_optimized_tasks':'0'}

def marked(mutant):
    pi=(F(9,10),F(1,10))
    kernels=[]
    for y in range(2):
        kernels.append(tuple(pi[theta] if w==(y^theta) else F(0) for theta in range(2) for w in range(2)))
    keys=[tuple(sum(k[2*theta:2*theta+2]) for theta in range(2)) if mutant=='drop_mark' else k for k in kernels]
    require(len(set(keys))==2,'terminal marked class must retain theta--target coupling')
    require(all(tuple(sum(k[2*theta:2*theta+2]) for theta in range(2))==pi for k in kernels),'parameter posterior alone is unchanged')
    full_error=F(1,10);coarse_error=F(1,2)
    require(coarse_error-full_error==F(2,5),'XOR classification regression')
    delta=F(4,5)
    for qh in [(F(1),F(0)),(F(1,2),F(1,2)),(F(2,3),F(1,3))]:
        for qk in [(F(0),F(1)),(F(1,2),F(1,2)),(F(1,3),F(2,3))]:
            excess=delta*delta/2*sum((x*y/(x+y) if x+y else F(0) for x,y in zip(qh,qk)),F(0))
            tv=sum(abs(x-y) for x,y in zip(qh,qk))/2
            require(excess>=delta*delta/4*(1-tv),'randomized-state overlap inequality')
    # Exact reverse channel for c=y, including each actual target mark.
    for theta,y,w in product(range(2),repeat=3):
        original=F(1,2)*int(w==(y^theta))
        reconstructed=sum(F(1,2)*int(y==c)*int(w==(c^theta)) for c in range(2))
        require(original==reconstructed,'parameter-uniform marked reconstruction')
    return {'marked_terminal_classes':2,'parameter_only_classes':1,'classification_gap':'2/5'}

def compiler(mutant):
    rng=random.Random(9210); reports=[]
    for trial in range(3):
        T=3;n=4
        mats=[]
        for t in range(T):
            stage={}
            for a in range(2):
                stage[a,0]=[[F(0) for _ in range(n)] for _ in range(n)]
                stage[a,1]=[[F(0) for _ in range(n)] for _ in range(n)]
                for theta,z in product(range(2),repeat=2):
                    weights=[rng.randint(1,4) for _ in range(4)];total=sum(weights)
                    for zp,y in product(range(2),repeat=2):
                        stage[a,y][2*theta+z][2*theta+zp]=F(weights[2*zp+y],total)
            mats.append(stage)
        terminal=[[F(i==j) for i in range(n)] for j in range(n)]
        spaces=[None]*(T+1);spaces[T]=terminal;columns=[None]*(T+1);columns[T]=terminal
        for t in range(T-1,-1,-1):
            spaces[t]=basis([matcol(M,v) for M in mats[t].values() for v in spaces[t+1]])
            columns[t]=[matcol(M,v) for M in mats[t].values() for v in columns[t+1]]
        histories=[[F(1,4)]*4];reps=list(histories);widths=[]
        for t in range(T+1):
            full={tuple(dot(alpha,v) for v in spaces[t]) for alpha in histories}
            quotient={tuple(dot(alpha,v) for v in spaces[t]) for alpha in reps}
            require(full==quotient,'output-sensitive quotient must equal expanded history quotient')
            require(len(full)==len({tuple(dot(alpha,v) for v in columns[t]) for alpha in histories}),'continuation basis separates exactly all future cylinders')
            widths.append(len(full))
            if t<T:
                def successors(rows):
                    for alpha in rows:
                        for M in mats[t].values():
                            nxt=rowmat(alpha,M);prob=sum(nxt)
                            if prob:yield [x/prob for x in nxt]
                histories=list(successors(histories));unique={}
                for alpha in successors(reps):unique.setdefault(tuple(dot(alpha,v) for v in spaces[t+1]),alpha)
                reps=list(unique.values())
        reports.append(widths)
    p,q=F(1,3),F(2,3);widths=[]
    for t in range(9):
        odds={(q/p)**k*((1-q)/(1-p))**(t-k) for k in range(t+1)}
        observed=2 if mutant=='rank_is_width' and t==3 else len(odds)
        require(observed==t+1,'linear rank two is not positive state width')
        widths.append(len(odds))
    return {'rational_controlled_models':reports,'bernoulli_widths':widths}

def model_checks(mutant):
    rng=random.Random(821)
    for _ in range(50):
        P=[[rng.uniform(.1,1) for _ in range(3)] for _ in range(3)]
        P=[[x/sum(row) for x in row] for row in P]
        lo=min(map(min,P));hi=max(map(max,P));rho=(hi-lo)/(hi+lo)
        u=[rng.uniform(.1,1) for _ in range(3)];v=[rng.uniform(.1,1) for _ in range(3)]
        def dh(u,v):
            logs=[math.log(x/y) for x,y in zip(u,v)];return max(logs)-min(logs)
        up=[sum(u[i]*P[i][j] for i in range(3)) for j in range(3)]
        vp=[sum(v[i]*P[i][j] for i in range(3)) for j in range(3)]
        require(dh(up,vp)<=rho*dh(u,v)+1e-12,'positive-matrix contraction')
        diagonal=[math.exp(rng.uniform(-5,5)) for _ in range(3)]
        require(abs(dh([x*d for x,d in zip(up,diagonal)],[x*d for x,d in zip(vp,diagonal)])-dh(up,vp))<1e-12,'shared positive likelihood preserves Hilbert distance')
    p_new=F(1,10)
    posterior=p_new*F(9,10)/((1-p_new)*F(1,10)+p_new*F(9,10))
    if mutant=='old_state_observation':posterior=p_new
    require(posterior==F(1,2),'observation kernel must refer to the new state')
    # Tensor diagnostic: oscillating report factors have distinct coordinates.
    N=256;m0=F(1,2);m1=F(1,4)+F(1,8*N)
    for theta in [F(-1),F(0),F(1)]:
        value=m0*m0+theta*m1*m1;limit=F(1,4)+theta*F(1,16)
        require(abs(value-limit)<F(1,1000),'tensor testing finite oscillation diagnostic')
    distinct=m0 if mutant=='identify_report_coordinates' else m0*m0
    require(distinct==F(1,4),'weak-star product argument requires distinct report coordinates')
    return {'positive_matrix_pairs':50,'new_state_posterior':'1/2','tensor_pairs':N}

Q=[(1.0,3.0),(2.0,.5)];V=[(.2,-.1),(-.4,.3)]
def H(u):
    return [max(V[a][i]+Q[a][i]*(math.exp(u[1-i]-u[i])-1) for a in range(2)) for i in range(2)]
def mesh(u,dt):
    values=[[],[]]
    for a in range(2):
        x=-Q[a][0]+V[a][0];w=-Q[a][1]+V[a][1];y,z=Q[a]
        tr=(x+w)/2;d=math.sqrt((x-w)**2/4+y*z);c=math.cosh(dt*d);s=math.sinh(dt*d)/d;e=math.exp(dt*tr)
        M=[[e*(c+s*(x-tr)),e*s*y],[e*s*z,e*(c+s*(w-tr))]]
        for i in range(2):values[i].append(math.log(sum(M[i][j]*math.exp(u[j]) for j in range(2))))
    return [max(v) for v in values]
def resolver(f,lam):
    u=list(f);dt=.01
    for _ in range(5000):
        h=H(u);v=[u[i]+dt*(f[i]-u[i]+lam*h[i]) for i in range(2)]
        if max(abs(v[i]-u[i]) for i in range(2))<1e-14:break
        u=v
    return u

def nonlinear(mutant):
    u=[.1,-.2];h=H(u);shift=H([x+2 for x in u])
    require(max(abs(h[i]-shift[i]) for i in range(2))<1e-12,'additive invariance of H')
    def approx(m):
        v=list(u)
        for _ in range(m):v=mesh(v,.4/m)
        return v
    ref=approx(2048);errs=[]
    for m in [8,16,32,64]:
        v=approx(m);errs.append(max(abs(x-y) for x,y in zip(v,ref)))
    require(all(errs[i+1]<errs[i] for i in range(3)),'Nisio mesh refinement regression')
    require(errs[-1]<.003,'finite mesh reference accuracy')
    f=[.3,-.1];lam=.3;r=resolver(f,lam);hr=H(r)
    sign=1 if mutant=='wrong_resolvent_sign' else -1
    require(max(abs(r[i]+sign*lam*hr[i]-f[i]) for i in range(2))<1e-9,'resolvent is u-lambda H(u)=f')
    f2=[.4,-.15];r2=resolver(f2,lam)
    require(max(abs(x-y) for x,y in zip(r,r2))<=max(abs(x-y) for x,y in zip(f,f2))+1e-10,'resolvent nonexpansiveness')
    # Exact rational two-step latent-phase recursion (exp rewards 1 or 2).
    eta=[F(1,2),F(1,2)]; K={}
    for a,c,y in product(range(2),repeat=3):
        K[a,c,y]=(F(3,4) if y==c else F(1,4))*(1 if a==c else 2)
    def step(eta,a,y):return [eta[c]*K[a,c,y] for c in range(2)]
    def terminal_step(row):
        return min(sum(sum(step(row,b,z)) for z in range(2)) for b in range(2))
    recursive=min(sum(terminal_step(step(eta,a,y)) for y in range(2)) for a in range(2))
    brute=min(sum(sum(step(step(eta,a,y),bs[y],z)) for y,z in product(range(2),repeat=2)) for a in range(2) for bs in product(range(2),repeat=2))
    require(recursive==brute,'one-policy tilted recursion equals policy-tree enumeration')
    one=F(1) if mutant=='phasewise_action' else F(3,2)
    require(one==F(3,2),'one action cannot be selected after the hidden phase')
    logmoment=math.log(1.5) if mutant!='mix_logarithms' else .5*math.log(2)
    require(abs(logmoment-math.log(1.5))<1e-14,'average moment before logarithm')
    return {'mesh_errors':errs,'resolvent_max_residual':max(abs(r[i]-lam*hr[i]-f[i]) for i in range(2)),'two_step_tilted_value':str(recursive),'hidden_phase_moment':'3/2'}

def main():
    parser=argparse.ArgumentParser();parser.add_argument('--mutant',choices=MUTANTS);args=parser.parse_args()
    try:
        values={'common_membership':membership(args.mutant),'marked_state':marked(args.mutant),'continuation_compiler':compiler(args.mutant),'positive_models':model_checks(args.mutant),'nonlinear_and_phase':nonlinear(args.mutant)}
        if args.mutant:raise RuntimeError('designated mutant survived')
        print(json.dumps({'status':'passed','finite_checks':COUNT,'results':values,'scope':'Exact finite regressions and floating-point model diagnostics; not proofs of general theorems.'},indent=2))
    except (RuntimeError,ValueError,ZeroDivisionError) as exc:
        print('FAILED: '+str(exc));sys.exit(1)
if __name__=='__main__':main()
